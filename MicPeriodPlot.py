#! /usr/bin/env python

#
# MicPeriodPlot.py
#
# This Python script is used for analysis of timing data from an MCA servo log,
# in this case for servo periods.
#
# Note :-
# Currently each plot window needs to be individually closed, otherwise they
# become headless. This needs to be sorted.
#

#
# This script accepts a filename as a command-line argument, and this file is
# expected to contain a list of servo logs to analyse, one per line in the form
# of filename then title separated by whitespace, for example :-
#  myservolog.dat	MyAxisTest
#

# Import packages
import sys
import numpy
import matplotlib
import matplotlib.pyplot as plt

# Define milli-arcseconds per degree
MasPerDeg = 3600000

# Define milli-arcseconds per arcsecond
MasPerAs = 1000

# Define nano-seconds per second
NSecPerSec = 1000000000

# Define milliseconds per second
MSecPerSec = 1000

# Definition of columns in filelist
ColFileName = 0
ColFileDescription = 1

# Definition of useful columns in servo log
ColTime = 0
ColPeriod = 25
ColLatency = 34

#
# Definitions to use for this particular analysis
#
# This section is used to define the parameters necessary to customise for 
# specific purposes
#
Col = ColPeriod
Title = "Servo Periods"
PlotMarker = '.'
ThreshALower = 2.4
ThreshAUpper = 2.6
ThreshBLower = 2.49
ThreshBUpper = 2.51

# Dummy function to discard the date string
def date2str( String ):
   return 0

# Take copy of the filename, passed in on the command-line
Filename = sys.argv[ 1 ]
print "Filename : ", Filename

# Read in the list of servo log files
Files = numpy.loadtxt( Filename, dtype=str )
for i in range( len( Files ) ) :
   print "%-20s " % Files[ i ][ ColFileDescription ], " : %s" % Files[ i ][ ColFileName ]

print

# Create list to hold data
Data = []

# Read in the data
for i in range( len( Files ) ) :
   Data.append( [] )
   Data[ i ] = numpy.loadtxt( Files[ i ][ ColFileName ], dtype=float, skiprows=1, usecols=[ Col ] )

# Perform a min, max, mean and stdev on the data
Min = numpy.nanmin( Data, axis=1 )
Max = numpy.nanmax( Data, axis=1 )
Mean  = numpy.mean( Data, axis=1 )
Stdev = numpy.std( Data, axis=1 )

# Report some statistics
for i in range( len( Files ) ) :
   print "%-20s" % Files[ i ][ ColFileDescription ], " min : %.2f," % Min[ i ], " max : %.2f," % Max[ i ], "mean : %.2f," % Mean[ i ], "stdev : %.3f," % Stdev[ i ]

print

# Determine the number outside thresholds
for i in range( len( Files ) ) :
   TallyA = 0
   TallyB = 0
   Samples = 0
   for j in range( len( Data[ i ] ) ) :
      Samples += 1
      if ( ( Data[ i ][ j ] < ThreshALower ) or ( Data[ i ][ j ] > ThreshAUpper ) ) :
         TallyA += 1
      if ( ( Data[ i ][ j ] < ThreshBLower ) or ( Data[ i ][ j ] > ThreshBUpper ) ) :
         TallyB += 1
   print "%-20s" % Files[ i ][ ColFileDescription ], ThreshALower, " < x > ", ThreshAUpper, ": %5d,  " % TallyA, ThreshBLower, " < x > ", ThreshBUpper, ": %5d" % TallyB

print

# Determine the percentage outside thresholds
for i in range( len( Files ) ) :
   TallyA = 0
   TallyB = 0
   Samples = 0
   for j in range( len( Data[ i ] ) ) :
      Samples += 1
      if ( ( Data[ i ][ j ] < ThreshALower ) or ( Data[ i ][ j ] > ThreshAUpper ) ) :
         TallyA += 1
      if ( ( Data[ i ][ j ] < ThreshBLower ) or ( Data[ i ][ j ] > ThreshBUpper ) ) :
         TallyB += 1
   PercentA = ( TallyA * 100.0 ) / Samples
   PercentB = ( TallyB * 100.0 ) / Samples
   print "%-20s" % Files[ i ][ ColFileDescription ], ThreshALower, " < x > ", ThreshAUpper, ": %7.3f%%,  " % PercentA, ThreshBLower, " < x > ",  ThreshBUpper, ": %7.3f%%" % PercentB

# Plot a graph (auto-scaled)
plt.figure( 1, figsize=( 8, 6 ) )
for i in range( len( Files ) ) :
   plt.plot( Data[ i ][ : ], linestyle='None', marker=PlotMarker, label=Files[ i ][ ColFileDescription ] )
plt.title( Title )
#plt.xlabel( "Time (sec)" )
plt.ylabel( "Time (msec)" )
plt.legend( loc=0 )
#plt.xlim( 10, 20 )
#plt.ylim( 0, 999999 )

# Plot a graph (zoomed in)
plt.figure( 2, figsize=( 8, 6 ) )
for i in range( len( Files ) ) :
   plt.plot( Data[ i ][ : ], linestyle='None', marker=PlotMarker, label=Files[ i ][ ColFileDescription ] )
plt.title( Title )
#plt.xlabel( "Time (sec)" )
plt.ylabel( "Time (msec)" )
plt.legend( loc=0 )
#plt.xlim( 10, 20 )
plt.ylim( ThreshALower, ThreshAUpper )

# Plot a graph (further zoomed)
plt.figure( 3, figsize=( 8, 6 ) )
for i in range( len( Files ) ) :
   plt.plot( Data[ i ][ : ], linestyle='None', marker=PlotMarker, label=Files[ i ][ ColFileDescription ] )
plt.title( Title )
#plt.xlabel( "Time (sec)" )
plt.ylabel( "Time (msec)" )
plt.legend( loc=0 )
#plt.xlim( 10, 20 )
plt.ylim( ThreshBLower, ThreshBUpper )

# Display the graphs
plt.show()

