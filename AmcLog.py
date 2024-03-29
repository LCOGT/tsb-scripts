#! /usr/bin/env python

#
# AmcLog.py
#
# This Python script is used for a quick analysis of an AMC servo log, producing
# some quick statistical analysis and plotting some useful graphs.
#
# Note :-
# Currently each plot window needs to be individually closed, otherwise they
# become headless. This needs to be sorted.
#

# Import packages
import sys
import numpy
import matplotlib
import matplotlib.pyplot as plt

# Define milli-arcseconds per degree
MasPerDeg = 3600000

# Definearcseconds per degree
AsPerDeg = 3600

# Define milli-arcseconds per arcsecond
MasPerAs = 1000

# Define nano-seconds per second
NSecPerSec = 1000000000

# Define milliseconds per second
MSecPerSec = 1000

# Definition of useful columns in AMC log
ColSecs = 0
ColState = 21
ColDmdVel = 3
ColDmdPos = 4
ColPos = 5
ColVel = 8
ColMaxErr = 12
ColRmsErr = 13
ColTrackTimeSec = 14
ColTrackTimeNSec = 15
ColTgtPos = 16
ColMotor1Pos = 6
ColMotor2Pos = 7
ColMotor1Vel = 9
ColMotor2Vel = 10

ColDmdTrq = 29
ColTrqCor = 17
ColTrqPre = 18
ColTrqPost = 19

ColPeriod = 23
ColLatency = 32

ColNum = 36

# Take copy of the filename, passed in on the command-line
Filename = sys.argv[ 1 ]
print("Filename : ", Filename)

# Open the file and read the line of headings
File = open( Filename )
Line = File.readline()
File.close()

# Determine how many headings have been read
Heading = Line.split( '\t' )
Heading = Heading[2:]
print( "Headings :", len( Heading ))

# Read in the actual data
Data = numpy.loadtxt( Filename, dtype=float, skiprows=1, usecols=range( 2, ColNum) )
print( "Data read in, row x col", Data.shape, "Size", Data.size, "bytes")

# Perform a min, max, mean and stdev on the data
Min = numpy.nanmin( Data, axis=0 )
Max = numpy.nanmax( Data, axis=0 )
Mean  = numpy.mean( Data, axis=0 )
Stdev = numpy.std( Data, axis=0 )

# Report some statistics about the position
Col = ColPos
print(Heading[ Col ],)
print(" min : %.3f," % Min[ Col ], " max : %.3f," % Max[ Col ], "mean : %.3f," % Mean[ Col ], "stdev : %.3f," % Stdev[ Col ])

# Report some statistics about the velocity
Col = ColVel
print(Heading[ Col ],)
print(" min : %.3f," % Min[ Col ], " max : %.3f," % Max[ Col ], "mean : %.3f," % Mean[ Col ], "stdev : %.3f," % Stdev[ Col ])

# Compute the mean RMS over the second half of samples (assume tracking by then)
MeanRms = numpy.mean( Data[ int(len( Data ) / 2) : len( Data ) + 1, ColRmsErr ] )
print( "MeanRMS tracking (second half) : %5d (mas)" % MeanRms)

# Compute the mean RMS over the final quarter of samples (must be tracking by then)
MeanRms = numpy.mean( Data[ int(len( Data ) / 4 * 3) : len( Data ) + 1, ColRmsErr ] )
print( "MeanRMS tracking (final quarter) : %5d (mas)" % MeanRms)

# Write the time axis back into the Data array, as sec+nsec
ColTime = ColSecs

# Take a copy of the data
NewData = numpy.array( Data )

# Now sort the data into time-order
StartIndex = 0
for i in range( len( Data ) ) :
   if ( i > 0 ) :
      if ( Data[ i - 1, ColTime ] > Data[ i, ColTime ] ) :
         StartIndex = i
for i in range( len( Data ) ) :
   if ( i < ( len( Data ) - StartIndex ) ) :
      Index = StartIndex + i
   else :
      Index = StartIndex + i - len( Data )
   NewData[ i ] = Data[ Index ]

# Now remove the time offset
Offset = NewData[ 0, ColTime ]
for i in range( len( NewData ) ) :
   NewData[ i, ColTime ] = NewData[ i, ColTime ] - Offset

# Determine an adjusted time axis for time-stamped track demands
TrackTime = ( NewData[ :, ColTrackTimeSec ] ) + ( NewData[ :, ColTrackTimeNSec ] / NSecPerSec )  - Offset

# Start the motor positions at zero
NewData[ :, ColMotor1Pos ] = NewData[ :, ColMotor1Pos ] - NewData[ 0, ColMotor1Pos ]
NewData[ :, ColMotor2Pos ] = NewData[ :, ColMotor2Pos ] - NewData[ 0, ColMotor2Pos ]

# Ensure adjusted track-demand times are in the correct range
for i in range( len( NewData ) ) :
   if ( TrackTime[ i ] <  0 ) :
      TrackTime[ i ] = 0

# Log any changes of state
for i in range( len( NewData ) ) :
   if ( NewData[ i, ColState ] != NewData[ i - 1, ColState ] ) :
      print("%3.3f" % NewData[ i, ColSecs ], " : State change %d" % NewData[ i - 1, ColState ], " -> %d" % NewData[ i, ColState ])

# Plot a graph of actual, demanded and target position
plt.figure( 1, figsize=( 8, 6 ) )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColPos ] / MasPerAs,    label=Heading[ ColPos ] )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColDmdPos ] / MasPerAs, label=Heading[ ColDmdPos ] )
plt.plot( TrackTime,             NewData[ :, ColTgtPos ] / MasPerAs, label=Heading[ ColTgtPos ] )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColTgtPos ] / MasPerAs, label="Raw TrackTargetPosition (mas)" )
plt.title( "%s" % ( Filename ) )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Position (arcsec)" )
plt.legend( loc=0 )

# Plot a graph of actual, demanded velocity
plt.figure( 2, figsize=( 8, 6 ) )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColVel ],               label=Heading[ ColVel ] )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColDmdVel ],            label=Heading[ ColDmdVel ] )
plt.title( "%s" % ( Filename ) )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Velocity (arcsec/sec)" )
plt.legend( loc=0 )

# Compute the per-cycle position error 
PosErr = NewData[ :, ColDmdPos ] - NewData[ :, ColPos ]
# Plot a graph of maximum and RMS servo errors, plus position error
plt.figure( 3, figsize=( 8, 6 ) )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColMaxErr ] / MasPerAs, label=Heading[ ColMaxErr ] )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColRmsErr ] / MasPerAs, label=Heading[ ColRmsErr ] )
plt.plot( NewData[ :, ColTime ], PosErr[ : ] / MasPerAs,             label="Position Error" )
plt.title( "%s" % ( Filename ) )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Position Error (arcsec)" )
plt.legend( loc=0 )

# Plot the motor positions
plt.figure( 4, figsize=( 8, 6 ) )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColMotor1Pos ] / MasPerAs, label=Heading[ ColMotor1Pos ] )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColMotor2Pos ] / MasPerAs, label=Heading[ ColMotor2Pos ] )
plt.title( "%s" % ( Filename ) )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Motor Positions (arcsec)" )
plt.legend( loc=0 )

# Plot the motor velocities
plt.figure( 5, figsize=( 8, 6 ) )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColMotor1Vel ] / MasPerAs, label=Heading[ ColMotor1Vel ] )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColMotor2Vel ] / MasPerAs, label=Heading[ ColMotor2Vel ] )
plt.title( "%s" % ( Filename ) )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Motor Velocities (arcsec)" )
plt.legend( loc=0 )

# Plot the latency & Period
plt.figure( 6, figsize=( 8, 6 ) )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColPeriod] , label=Heading[ ColPeriod ] )
plt.title( "%s" % ( Filename ) )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Period (ms)" )
plt.legend( loc=0 )
plt.figure( 7, figsize=( 8, 6 ) )
plt.plot( NewData[ :, ColTime ], NewData[ :, ColLatency ] , label=Heading[ ColLatency ] )
plt.title( "%s" % ( Filename ) )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Latency(ms)" )
plt.legend( loc=0 )

# Display the graphs
plt.show()



