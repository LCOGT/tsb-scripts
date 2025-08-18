#! /usr/bin/env python

#
# PmcMirrorLog.py
#
# This Python script is used for a quick analysis of a PMC mirror support log, 
# producing some quick statistical analysis and plotting some useful graphs.
#
# Note :-
# Currently each plot window needs to be individually closed, otherwise they
# become headless. This needs to be sorted.
#

# Specify whether PMC data (otherwise SIF)
PMC = 1

# Specify which graphs are to be plotted
GraphLoad    = 1
GraphAxial   = 1
GraphLateral = 1
GraphAngle   = 1
GraphVector  = 1

# Define linestyles
StyleDash  = '--'
StyleSolid = '-'
StyleDots  = ':'

# Import packages
import sys
import numpy
import matplotlib
import matplotlib.pyplot as plt
from math import sqrt

# Define nano-seconds per second
NanoSecPerSec = 1000000000

# Define a function for RMS
def qmean( num ) :
   return sqrt( sum( n * n for n in num ) / len( num ) )

# Definition of useful columns in mirror support log
if PMC :
   # Define columns from PMC log
   ColTime = 0
   RedAxialLoad = 1
   YelAxialLoad = 2
   BluAxialLoad = 3
   RedRadialLoad = 4
   YelRadialLoad = 5
   BluRadialLoad = 6
   RedValveFeedback = 7
   YelValveFeedback = 8
   BluValveFeedback = 9
   Lateral1LoadValveFeedback = 10
   Lateral1PreLoadValveFeedback = 11
   Lateral2LoadValveFeedback = 12
   Lateral2PreLoadValveFeedback = 13
   RedAxialDrive = 14
   YelAxialDrive = 15
   BluAxialDrive = 16
   Lateral1LoadDrive = 17
   Lateral1PreLoadDrive = 18
   Lateral2LoadDrive = 19
   Lateral2PreLoadDrive = 20
   Angle = 21
   NorthSouthVector = 22
   EastWestVector = 23
   Reference = 24
else :
   # Define columns from SIF log (note some not present)
   ColSecs = 18
   ColNSec = 19
   ColTime = 0
   RedAxialLoad = 1
   YelAxialLoad = 2
   BluAxialLoad = 3
   RedRadialLoad = 4
   YelRadialLoad = 5
   BluRadialLoad = 6
   RedValveFeedback = 7
   YelValveFeedback = 8
   BluValveFeedback = 9
   Lateral1LoadValveFeedback = 10
   Lateral1PreLoadValveFeedback = 11
   Lateral2LoadValveFeedback = -1
   Lateral2PreLoadValveFeedback = -1
   RedAxialDrive = 12
   YelAxialDrive = 13
   BluAxialDrive = 14
   Lateral1LoadDrive = 15
   Lateral1PreLoadDrive = 16
   Lateral2LoadDrive = -1
   Lateral2PreLoadDrive = -1
   Angle = 17
   NorthSouthVector = 20
   EastWestVector = 21
   Reference = 22

# Dummy function to discard the date string
def date2str( String ):
   return 0

# Take copy of the filename, passed in on the command-line
Filename = sys.argv[ 1 ]
print "Filename : ", Filename

# Open the file and read the line of headings
File = open( Filename )
Line = File.readline()
File.close()

# Determine how many headings have been read
Heading = Line.split( '\t' )
print "Headings :", len( Heading )
if PMC :
   # Delete the first two unwanted headings
   del Heading[ 0:2 ]

# Read in the actual data
if PMC :
   Data = numpy.loadtxt( Filename, dtype=float, skiprows=1, usecols=range(2,27) )
   print "Data read in, row x col", Data.shape, "Size", Data.size, "bytes"
else :
   Data = numpy.loadtxt( Filename, dtype=float, skiprows=1, usecols=range(0,23) )
   print "Data read in, row x col", Data.shape, "Size", Data.size, "bytes"

# Perform a min, max, mean and stdev on the data
Min = numpy.nanmin( Data, axis=0 )
Max = numpy.nanmax( Data, axis=0 )
Mean  = numpy.mean( Data, axis=0 )
Stdev = numpy.std( Data, axis=0 )

# For SIF data, time column is actually a loop count
if PMC == 0 :
   for i in range( len( Data ) ) :
      Data[ :, ColTime ] = Data[ :, ColSecs ] + ( Data[ :, ColNSec ] / NanoSecPerSec )

# Report some statistics about the timing periods
Period = Data[ :, ColTime ] - Data[ 0, ColTime ]
for i in range( len( Period ) ) :
   if ( i > 0 ) :
      Period[ i ] = ( Data[ i, ColTime ] - Data[ i - 1, ColTime ] )
Period[ 0 ] = Period[ 1 ]
# Report some statistics about the period
Col = ColTime
print "Periods",
print "  min : %.3f," % numpy.nanmin( Period ), " max : %.3f," % numpy.nanmax( Period ), "mean : %.3f," % numpy.mean( Period ), "stdev : %.3f," % numpy.std( Period )

# Report some statistics about the reference
Col = Reference
print Heading[ Col ],
print " min : %.3f," % Min[ Col ], " max : %.3f," % Max[ Col ], "mean : %.3f," % Mean[ Col ], "stdev : %.3f," % Stdev[ Col ]

# Determine the RMS of the Red Axial Load over the third quarter of data (assume support stable by then)
print "RMS Red Axial Load     (third quarter) : %8.2f (milli Volt)" % ( qmean( Data[ len( Data ) * 2 / 4 : len( Data ) * 3 / 4, RedAxialLoad ] ) * 1000.0 )

# Determine the RMS of the Yellow Axial Load over the third quarter of data (assume support stable by then)
print "RMS Yellow Axial Load  (third quarter) : %8.2f (milli Volt)" % ( qmean( Data[ len( Data ) * 2 / 4 : len( Data ) * 3 / 4, YelAxialLoad ] ) * 1000.0 )

# Determine the RMS of the Blue Axial Load over the third quarter of data (assume support stable by then)
print "RMS Blue Axial Load    (third quarter) : %8.2f (milli Volt)" % ( qmean( Data[ len( Data ) * 2 / 4 : len( Data ) * 3 / 4, BluAxialLoad ] ) * 1000.0 )

# Determine the RMS of the Red Radial Load over the third quarter of data (assume support stable by then)
print "RMS Red Radial Load    (third quarter) : %8.2f (milli Volt)" % ( qmean( Data[ len( Data ) * 2 / 4 : len( Data ) * 3 / 4, RedRadialLoad ] ) * 1000.0 )

# Determine the RMS of the Yellow Radial Load over the third quarter of data (assume support stable by then)
print "RMS Yellow Radial Load (third quarter) : %8.2f (milli Volt)" % ( qmean( Data[ len( Data ) * 2 / 4 : len( Data ) * 3 / 4, YelRadialLoad ] ) * 1000.0 )

# Determine the RMS of the Blue Radial Load over the third quarter of data (assume support stable by then)
print "RMS Blue Radial Load   (third quarter) : %8.2f (milli Volt)" % ( qmean( Data[ len( Data ) * 2 / 4 : len( Data ) * 3 / 4, BluRadialLoad ] ) * 1000.0 )

# Determine the RMS of the NorthSouth vector over the third quarter of data (assume support stable by then)
print "RMS North/South vector (third quarter) : %8.2f (milli Volt)" % ( qmean( Data[ len( Data ) * 2 / 4 : len( Data ) * 3 / 4, NorthSouthVector ] ) * 1000.0 )

# Determine the RMS of the NorthSouth vector over the third quarter of data (assume support stable by then)
print "RMS East/West   vector (third quarter) : %8.2f (milli Volt)" % ( qmean( Data[ len( Data ) * 2 / 4 : len( Data ) * 3 / 4, EastWestVector ] ) * 1000.0 )

# Determine a time axis for plotting graphs
Time = Data[ :, ColTime ] - Data[ 0, ColTime ]

Count=0

if GraphLoad :
   # Plot a graph of the loads
   Count += 1
   Fig = plt.figure( Count, figsize=( 8, 6 ) )
   Fig.canvas.set_window_title( "Loads" )
   plt.plot( Time, Data[ :, RedAxialLoad ] , label=Heading[ RedAxialLoad  ], c='r', linestyle=StyleSolid )
   plt.plot( Time, Data[ :, YelAxialLoad ] , label=Heading[ YelAxialLoad  ], c='y', linestyle=StyleSolid )
   plt.plot( Time, Data[ :, BluAxialLoad ] , label=Heading[ BluAxialLoad  ], c='b', linestyle=StyleSolid )
   plt.plot( Time, Data[ :, RedRadialLoad ], label=Heading[ RedRadialLoad ], c='r', linestyle=StyleDash )
   plt.plot( Time, Data[ :, YelRadialLoad ], label=Heading[ YelRadialLoad ], c='y', linestyle=StyleDash )
   plt.plot( Time, Data[ :, BluRadialLoad ], label=Heading[ BluRadialLoad ], c='b', linestyle=StyleDash )
   plt.title( Filename )
   plt.xlabel( "Time (sec)" )
   plt.ylabel( "Load (V)" )
   plt.legend( loc=0 )
   #plt.xlim( 10, 20 )
   #plt.ylim( 0, 999999 )

if GraphAxial :
   # Plot a graph of the axial data
   Count += 1
   Fig = plt.figure( Count, figsize=( 8, 6 ) )
   Fig.canvas.set_window_title( "Axial" )
   plt.plot( Time, Data[ :, RedAxialDrive ] , label=Heading[ RedAxialDrive  ], c='r', linestyle=StyleDots )
   plt.plot( Time, Data[ :, YelAxialDrive ] , label=Heading[ YelAxialDrive  ], c='y', linestyle=StyleDots )
   plt.plot( Time, Data[ :, BluAxialDrive ] , label=Heading[ BluAxialDrive  ], c='b', linestyle=StyleDots )
   plt.plot( Time, Data[ :, RedValveFeedback ] , label=Heading[ RedValveFeedback  ], c='r', linestyle=StyleSolid )
   plt.plot( Time, Data[ :, YelValveFeedback ] , label=Heading[ YelValveFeedback  ], c='y', linestyle=StyleSolid )
   plt.plot( Time, Data[ :, BluValveFeedback ] , label=Heading[ BluValveFeedback  ], c='b', linestyle=StyleSolid )
   plt.title( Filename )
   plt.xlabel( "Time (sec)" )
   plt.ylabel( "Drive/Feedback (V)" )
   plt.legend( loc=0 )
   #plt.xlim( 10, 20 )
   #plt.ylim( 0, 999999 )

if GraphLateral :
   # Plot a graph of the lateral data
   Count += 1
   Fig = plt.figure( Count, figsize=( 8, 6 ) )
   Fig.canvas.set_window_title( "Lateral" )
   plt.plot( Time, Data[ :, Lateral1LoadDrive ], label=Heading[ Lateral1LoadDrive ],       c='k', linestyle=StyleDots )
   plt.plot( Time, Data[ :, Lateral1PreLoadDrive ], label=Heading[ Lateral1PreLoadDrive ], c='g', linestyle=StyleDots )
   if PMC :
      plt.plot( Time, Data[ :, Lateral2LoadDrive ], label=Heading[ Lateral2LoadDrive ],       c='c', linestyle=StyleDots )
      plt.plot( Time, Data[ :, Lateral2PreLoadDrive ], label=Heading[ Lateral2PreLoadDrive ], c='m', linestyle=StyleDots )
   plt.plot( Time, Data[ :, Lateral1LoadValveFeedback ], label=Heading[ Lateral1LoadValveFeedback ],       c='k', linestyle=StyleSolid )
   plt.plot( Time, Data[ :, Lateral1PreLoadValveFeedback ], label=Heading[ Lateral1PreLoadValveFeedback ], c='g', linestyle=StyleSolid )
   if PMC :
      plt.plot( Time, Data[ :, Lateral2LoadValveFeedback ], label=Heading[ Lateral2LoadValveFeedback ],       c='c', linestyle=StyleSolid )
      plt.plot( Time, Data[ :, Lateral2PreLoadValveFeedback ], label=Heading[ Lateral2PreLoadValveFeedback ], c='m', linestyle=StyleSolid )
   plt.title( Filename )
   plt.xlabel( "Time (sec)" )
   plt.ylabel( "Drive/Feedback (V)" )
   plt.legend( loc=0 )
   #plt.xlim( 10, 20 )
   #plt.ylim( 0, 999999 )

if GraphAngle :
   # Plot the zenith angle
   Count += 1
   Fig = plt.figure( Count, figsize=( 8, 6 ) )
   Fig.canvas.set_window_title( "Zenith Angle" )
   plt.plot( Time, Data[ :, Angle ], label=Heading[ Angle ], c='k' )
   plt.title( Filename )
   plt.xlabel( "Time (sec)" )
   plt.ylabel( "Angle (deg)" )
   plt.legend( loc=0 )
   #plt.xlim( 10, 20 )
   plt.ylim( 90, -10 )

if GraphVector :
   # Plot the resolved vectors
   Count += 1
   Fig = plt.figure( Count, figsize=( 8, 6 ) )
   Fig.canvas.set_window_title( "Vectors" )
   plt.plot( Time, Data[ :, NorthSouthVector ], label=Heading[ NorthSouthVector ], c='g' )
   plt.plot( Time, Data[ :, EastWestVector ], label=Heading[ EastWestVector ], c='m' )
   plt.title( Filename )
   plt.xlabel( "Time (sec)" )
   plt.ylabel( "Vector (V)" )
   plt.legend( loc=0 )
   #plt.xlim( 10, 20 )
   #plt.ylim( 0, 999999 )


# Display the graphs
plt.show()


