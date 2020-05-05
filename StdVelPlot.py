#! /usr/bin/env python

#
# StdPlot.py
#
# This Python script is used for a quick analysis of an STD data file, i.e. data
# extracted from SDB files.
#
# Follow the various numbered stages to configure operation to suit purposes.
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
import math

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
ColSecondData = 2

ColAzmBrake=2
ColAltBrake=7
ColCasBrake=12

ColAzmPos=3
ColAltPos=8
ColCasPos=13

ColAzmVel=4
ColAltVel=9
ColCasVel=14


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

Data[ 0, ColAzmBrake ] = 0
Data[ 0, ColAltBrake ] = 0
Data[ 0, ColCasBrake ] = 0

AzmAdj = 0
AltAdj = 0
CasAdj = 0

for i in range( len( Data ) ) :

   if ( math.isnan( Data[ i, ColAzmPos ] ) ) :
      Data[ i, ColAzmPos ] = Data[ i - 1, ColAzmPos ]
   else :
      if ( AzmAdj == 0  ) :
         AzmAdj = Data[ i, ColAzmPos ]
   if ( math.isnan( Data[ i, ColAltPos ] ) ) :
      Data[ i, ColAltPos ] = Data[ i - 1, ColAltPos ]
   else :
      if ( AltAdj == 0  ) :
         AltAdj = Data[ i, ColAltPos ]
   if ( math.isnan( Data[ i, ColCasPos ] ) ) :
      Data[ i, ColCasPos ] = Data[ i - 1, ColCasPos ]
   else :
      if ( CasAdj == 0  ) :
         CasAdj = Data[ i, ColCasPos ]

for i in range( len( Data ) ) :

   Data[ i, ColAzmPos ] = Data[ i, ColAzmPos ] - AzmAdj
   Data[ i, ColAltPos ] = Data[ i, ColAltPos ] - AltAdj
   Data[ i, ColCasPos ] = Data[ i, ColCasPos ] - CasAdj

   if ( i > 0 ) :
      Data[ i, ColAzmVel ] = ( Data[ i, ColAzmPos ] - Data[ i - 1, ColAzmPos ] ) * 400
      Data[ i, ColAltVel ] = ( Data[ i, ColAltPos ] - Data[ i - 1, ColAltPos ] ) * 400
      Data[ i, ColCasVel ] = ( Data[ i, ColCasPos ] - Data[ i - 1, ColCasPos ] ) * 400

   if ( math.isnan( Data[ i, ColAzmBrake ] ) ) :
      Data[ i, ColAzmBrake ] = Data[ i - 1, ColAzmBrake ]
   if ( math.isnan( Data[ i, ColAltBrake ] ) ) :
      Data[ i, ColAltBrake ] = Data[ i - 1, ColAltBrake ]
   if ( math.isnan( Data[ i, ColCasBrake ] ) ) :
      Data[ i, ColCasBrake ] = Data[ i - 1, ColCasBrake ]

Data[ 0, ColAzmVel ] = 0
Data[ 0, ColAltVel ] = 0
Data[ 0, ColCasVel ] = 0

# Determine a time axis for plotting graphs
Time = Data[ :, ColTime ] - Data[ 0, ColTime ]

##########
#
# 4) Set the parameters to plot the first graph
#
##########
plt.figure( 1, figsize=( 8, 6 ) )
#plt.plot( Time, Data[ :, ColFirstData ] / MasPerAs, label=Heading[ ColFirstData ] )
#plt.plot( Time, Data[ :, ColSecondData] / MasPerAs, label=Heading[ ColSecondData ] )
plt.plot( Time, Data[ :, ColAzmPos], label=Heading[ ColAzmPos ] )
plt.plot( Time, Data[ :, ColAltPos], label=Heading[ ColAltPos ] )
plt.plot( Time, Data[ :, ColCasPos], label=Heading[ ColCasPos ] )
plt.title( Filename )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Position" )
plt.legend( loc=0 )

##########
#
# 5) Set the parameters for subsequent graphs (e.g. the computed data)
#
##########
plt.figure( 2, figsize=( 8, 6 ) )
plt.plot( Time, Data[ :, ColAzmVel], label=Heading[ ColAzmVel ] )
plt.plot( Time, Data[ :, ColAltVel], label=Heading[ ColAltVel ] )
plt.plot( Time, Data[ :, ColCasVel], label=Heading[ ColCasVel ] )
plt.title( Filename )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Velocity" )
plt.legend( loc=0 )
#plt.plot( Time, NewData[ : ], label="New Data" )
#plt.title( Filename )
#plt.xlabel( "Time (sec)" )
#plt.ylabel( "SecondCol-FirstCol" )
#plt.legend( loc=0 )

##########
#
# 6) Any more graphs...
#
##########
#plt.figure( 3, figsize=( 8, 6 ) )
#plt.plot( Time, Data[ :, ColAzmBrake], label=Heading[ ColAzmBrake ] )
#plt.plot( Time, Data[ :, ColAltBrake], label=Heading[ ColAltBrake ] )
#plt.plot( Time, Data[ :, ColCasBrake], label=Heading[ ColCasBrake ] )
#plt.title( Filename )
#plt.xlabel( "Time (sec)" )
#plt.ylabel( "Brakes" )
#plt.legend( loc=0 )

# Display the actual graphs
plt.show()


