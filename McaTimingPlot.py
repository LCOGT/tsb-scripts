#! /usr/bin/env python

#
# AmcLog.py
#
# This Python script is used for a quick analysis of the Mca timing log data
#
# Note :-
# Currently each plot window needs to be individually closed, otherwise they
# become headless. This needs to be sorted.
#

# Import packages
import sys
import numpy
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# Define nano-seconds per second
NSecPerMSec = 1000000


# Definition of useful columns in AMC log
ColDate = 0
ColTime = 1
ColSec = 0
ColFifo = 1
ColPos = 2
ColExtraRx = 3
ColState = 4
ColServo = 5
ColApply = 6
ColStatus = 7
ColRx = 8
ColHouse = 9
ColEnd = 10
ColTotal = 11

ColDelta = 12
ColFifoDelta = 13

ColNum = 14

# Take copy of the filename, passed in on the command-line
Filename = sys.argv[ 1 ]
print("Filename : ", Filename)

# Open the file and read the line of headings
File = open( Filename )
Line = File.readline()
File.close()

# Determine how many headings have been read
Heading = Line.split( )
Heading = Heading[2:]
print( "Headings :", len( Heading ))

# Read in the actual data
Data = numpy.loadtxt( Filename, dtype=float, skiprows=1, usecols=range( 2, ColNum) )
print( "Data read in, row x col", Data.shape, "Size", Data.size, "bytes")

# Convert nanoseconds → milliseconds for all columns (except ColSec, which is already seconds)
Data[:, 2:] = Data[:, 2:] / NSecPerMSec

# Compute delta of ColSec (time difference between rows)
delta_sec = numpy.diff(Data[:, ColSec], prepend=numpy.nan)
# Append as a new column
Data = numpy.hstack((Data, delta_sec.reshape(-1, 1)))
# Update heading list
Heading.append("DeltaServo")

# Compute delta of Fifo to Servo Loop
delta_fifo = Data[:, ColSec] - Data[:, ColFifo]
# Append as a new column
Data = numpy.hstack((Data, delta_fifo.reshape(-1, 1)))
# Update heading list
Heading.append("DeltaFifo")

# Perform a min, max, mean and stdev on the data
Min = numpy.nanmin( Data, axis=0 )
Max = numpy.nanmax( Data, axis=0 )
Mean  = numpy.nanmean( Data, axis=0 )
Stdev = numpy.nanstd( Data, axis=0 )

# Report some statistics
Col = ColApply
print(Heading[ Col ],)
print(" min : %.3f," % Min[ Col ], " max : %.3f," % Max[ Col ], "mean : %.3f," % Mean[ Col ], "stdev : %.3f, ms" % Stdev[ Col ])
Col = ColEnd
print(Heading[ Col ],)
print(" min : %.3f," % Min[ Col ], " max : %.3f," % Max[ Col ], "mean : %.3f," % Mean[ Col ], "stdev : %.3f, ms" % Stdev[ Col ])
Col = ColDelta
print(Heading[ Col ],)
print(" min : %.4f," % Min[ Col ], " max : %.4f," % Max[ Col ], "mean : %.6f," % Mean[ Col ], "stdev : %.6f, s" % Stdev[ Col ])
Col = ColFifoDelta
print(Heading[ Col ],)
print(" min : %.6f," % Min[ Col ], " max : %.6f," % Max[ Col ], "mean : %.6f," % Mean[ Col ], "stdev : %.6f, s" % Stdev[ Col ])

# Take a copy of the data
NewData = numpy.array( Data )

# Plot a graph of total
plt.figure( 1, figsize=( 8, 6 ) )
plt.plot( NewData[ :, ColSec ], NewData[ :, ColApply ],    label=Heading[ ColApply ] )
plt.title( "%s" % ( Filename ) )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Duration (msec)" )
plt.legend( loc=0 )

# Plot a graph of total
plt.figure( 2, figsize=( 8, 6 ) )
plt.plot( NewData[ :, ColSec ], NewData[ :, ColEnd ],    label=Heading[ ColEnd ] )
plt.title( "%s" % ( Filename ) )
plt.xlabel( "Time (sec)" )
plt.ylabel( "Duration (msec)" )
plt.legend( loc=0 )

plt.figure(3, figsize=(8, 6))
plt.plot(NewData[:, ColSec], NewData[:, ColDelta], label="DeltaSec")
plt.title(Filename)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.xlabel("Time (sec)", fontsize=20)
plt.ylabel("Δ Time (sec)", fontsize=20)
plt.legend(loc=0, fontsize=20)


plt.figure(4, figsize=(8, 6))
plt.plot(NewData[:, ColSec], NewData[:, ColFifoDelta], label="DeltaFifoSec")
plt.title(Filename)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.xlabel("Time (sec)", fontsize=20)
plt.ylabel("Δ Time (sec)", fontsize=20)
plt.legend(loc=0, fontsize=20)
# Display the graphs
plt.show()



