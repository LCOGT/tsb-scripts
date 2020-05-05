#! /usr/bin/env python

#
# StdTorquePlot.py
#
# This Python script is used for a quick analysis of an STD data file, i.e. data
# extracted from SDB files.
#
# This script expects the data to be extracted using the STD '-gnuplot' option.
#
# Follow the various numbered stages to configure operation to suit purposes.
#
# This script is aimed at plotting axis positions and torques. 
#
# Notes :-
# - currently each plot window needs to be individually closed, otherwise they
#   become headless (needs to be sorted)
#

# Import packages
import sys
import numpy
import matplotlib
import matplotlib.pyplot as plt

# Various constants
MasPerDeg = 3600000
MasPerAs = 1000
NSecPerSec = 1000000000
MilliPerUnit = 1000
MicroPerUnit = 1000000

# Dummy function to discard the date string
def date2str( String ):
   return 0

# Take copy of the filename, passed in on the command-line
Filename = sys.argv[ 1 ]
print "Filename : ", Filename

## Open the file to replace empty entries with 'NaN'
#File = open( Filename )
#Contents = File.read()
#File.close()
#NewContents = Contents.replace( '\t\t', '\tNaN\t' )
#File = open( "temp.txt", "w" )
#File.write( NewContents )
#File.close()

# Open the file and read the line of headings
File = open( Filename )
Line = File.readline()
File.close()

# Determine how many headings have been read
Heading = Line.split( '\t' )
print Heading
print "Headings :", len( Heading )
TotalCols = len( Heading )
# Delete the first two unwanted headings
del Heading[ 0:2 ]

# Read in the actual data
Data = numpy.loadtxt( Filename, dtype=float, skiprows=1 , usecols=range( 2, TotalCols - 1 ) )
print "Data read in, row x col", Data.shape, "Size", Data.size, "bytes"

# Perform a min, max, mean and stdev on the data
Min = numpy.nanmin( Data, axis=0 )
Max = numpy.nanmax( Data, axis=0 )
Mean  = numpy.mean( Data, axis=0 )
Stdev = numpy.std( Data, axis=0 )

# Define some useful columns
ColTime = 0
ColFirstData = 1

##########
#
# 1) Define user columns
#
##########
ColPosTarget = 1
ColPosDemand = 2
ColPosActual = 3
ColPosDiff   = 4

AXIS_TORQUE_LIMIT = 5
AXIS_TORQUE_DEMAND = 6
CLAMPED_AXIS_TORQUE_DEMAND = 7
AXIS_TORQUE_CLAMP_FLAG = 8

MOTOR_FULL_PRELOAD_TORQUE = 9
MOTOR_PRELOAD_TORQUE = 10
MOTOR_TORQUE_MIN_LIMIT = 11
MOTOR_TORQUE_MAX_LIMIT = 12
MOTOR_TORQUE_CORRECTION = 13

CLAMPED_MOTOR_1_TORQUE_DEMAND = 14
CLAMPED_MOTOR_2_TORQUE_DEMAND = 15

MOT1_TORQUE_CLAMP_FLAG = 16
MOT2_TORQUE_CLAMP_FLAG = 17

MOTOR_1_MEASURED_TORQUE = 18
MOTOR_2_MEASURED_TORQUE = 19


##########
#
# 2) Fill in the reporting of any statistics
#
##########
Col = ColFirstData
print Heading[ Col ],
print " min : %.3f," % Min[ Col ], " max : %.3f," % Max[ Col ], "mean : %.3f," % Mean[ Col ], "stdev : %.3f," % Stdev[ Col ]

##########
#
# 3) Perform any specific computations to create new data
#
##########
DiffDemand = Data[ :, ColPosDemand ] - Data[ :, ColPosActual ]
DiffTarget = Data[ :, ColPosTarget ] - Data[ :, ColPosActual ]

# Determine a time axis for plotting graphs
Time = Data[ :, ColTime ] - Data[ 0, ColTime ]

##########
#
# 4) Set the parameters to plot the first graph
#
##########
plt.figure( 1, figsize=( 12, 9 ) )
plt.plot( Time, Data[ :, ColPosTarget ] / MasPerAs, label=Heading[ ColPosTarget ], marker='.' )
plt.plot( Time, Data[ :, ColPosDemand ] / MasPerAs, label=Heading[ ColPosDemand ], marker='.' )
plt.plot( Time, Data[ :, ColPosActual ] / MasPerAs, label=Heading[ ColPosActual ], marker='.' )
plt.title( Filename )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Position (arcsec)" )
plt.legend( loc=1 )
#plt.xlim( 420, 600 )
#plt.ylim( -520000, -460000 )

##########
#
# 5) Set the parameters for subsequent graphs (e.g. the computed data)
#
##########
plt.figure( 2, figsize=( 12, 9 ) )
plt.plot( Time, Data[ :, ColPosDiff ] / MasPerAs, label=Heading[ ColPosDiff ], marker='.' )
#plt.plot( Time, DiffDemand[ : ] / MasPerAs, label="DiffDemand", marker='.' )
#plt.plot( Time, DiffTarget[ : ] / MasPerAs, label="DiffTarget", marker='.' )
plt.title( Filename )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Position Difference (arcsec)" )
plt.legend( loc=2 )
#plt.xlim( 420, 600 )
#plt.ylim( 0, 1000 )


plt.figure( 3, figsize=( 12, 9 ) )
plt.plot( Time, Data[ :, AXIS_TORQUE_DEMAND ], label=Heading[ AXIS_TORQUE_DEMAND ], marker='.' )
plt.plot( Time, Data[ :, MOTOR_TORQUE_CORRECTION ], label=Heading[ MOTOR_TORQUE_CORRECTION ], marker='.' )
plt.plot( Time, Data[ :, MOTOR_1_MEASURED_TORQUE ], label=Heading[ MOTOR_1_MEASURED_TORQUE ], marker='.' )
plt.plot( Time, Data[ :, MOTOR_2_MEASURED_TORQUE ], label=Heading[ MOTOR_2_MEASURED_TORQUE ], marker='.' )
plt.plot( Time, Data[ :, CLAMPED_MOTOR_1_TORQUE_DEMAND ], label=Heading[ CLAMPED_MOTOR_1_TORQUE_DEMAND ], marker='.' )
plt.plot( Time, Data[ :, CLAMPED_MOTOR_2_TORQUE_DEMAND ], label=Heading[ CLAMPED_MOTOR_2_TORQUE_DEMAND ], marker='.' )
plt.title( Filename )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Torque" )
plt.legend( loc=1 )
#plt.xlim( 420, 600 )
#plt.ylim( -3000, 2000 )


#plt.figure( 4, figsize=( 8, 6 ) )
#plt.plot( Time, Data[ :, AXIS_TORQUE_LIMIT ], label=Heading[ AXIS_TORQUE_LIMIT ], marker='.' )
#plt.plot( Time, Data[ :, MOTOR_FULL_PRELOAD_TORQUE ], label=Heading[ MOTOR_FULL_PRELOAD_TORQUE ], marker='.' )
#plt.plot( Time, Data[ :, MOTOR_PRELOAD_TORQUE ], label=Heading[ MOTOR_PRELOAD_TORQUE ], marker='.' )
#plt.plot( Time, Data[ :, MOTOR_TORQUE_MIN_LIMIT ], label=Heading[ MOTOR_TORQUE_MIN_LIMIT ], marker='.' )
#plt.plot( Time, Data[ :, MOTOR_TORQUE_MAX_LIMIT ], label=Heading[ MOTOR_TORQUE_MAX_LIMIT ], marker='.' )
#plt.xlabel( "Time (sec)" )
#plt.ylabel( "Torque Limits" )
##plt.legend( loc=0 )
#plt.legend( loc='upper left' )
##plt.xlim( 420, 600 )
##plt.ylim( -400000, 200000 )


#plt.figure( 5, figsize=( 8, 6 ) )
#plt.plot( Time, Data[ :, AXIS_TORQUE_CLAMP_FLAG ], label=Heading[ AXIS_TORQUE_CLAMP_FLAG ], marker='.' )
#plt.plot( Time, Data[ :, MOT1_TORQUE_CLAMP_FLAG ], label=Heading[ MOT1_TORQUE_CLAMP_FLAG ], marker='.' )
#plt.plot( Time, Data[ :, MOT2_TORQUE_CLAMP_FLAG ], label=Heading[ MOT2_TORQUE_CLAMP_FLAG ], marker='.' )
#plt.title( Filename )
#plt.xlabel( "Time (sec)" )
#plt.ylabel( "Torque Flags" )
##plt.legend( loc=0 )
#plt.legend( loc='upper left' )
#plt.xlim( 420, 600 )
##plt.ylim( -550000, -450000 )


##########
#
# 6) Any more graphs...
#
##########
#plt.figure( 3, figsize=( 8, 6 ) )

# Display the actual graphs
plt.show()


