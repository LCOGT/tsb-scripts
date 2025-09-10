#!/usr/bin/env python3
"""
PmcMirrorLog.py (Python 3)

Quick analysis of a PMC mirror support log, producing basic stats
and several plots. Converted for Python 3 / modern Matplotlib.

Notes
-----
- Close each plot window to proceed if running interactively.
- Uses fig.canvas.manager.set_window_title(...) which works on
  modern Matplotlib backends; falls back gracefully if not available.
"""

# --- Configuration toggles ---
PMC = 1  # 1: PMC data format, 0: SIF format

# Which graphs to plot
GraphLoad    = 1
GraphAxial   = 1
GraphLateral = 1
GraphAngle   = 1
GraphVector  = 1

# Linestyles
StyleDash  = "--"
StyleSolid = "-"
StyleDots  = ":"

# --- Imports ---
import sys
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# --- Constants ---
NanoSecPerSec = 1_000_000_000

# --- Helpers ---
def qmean(arr_like):
    """Root-mean-square of a sequence/array."""
    a = np.asarray(arr_like, dtype=float)
    return math.sqrt(np.mean(a * a))

# Definition of useful columns in mirror support log
if PMC:
    # PMC log columns
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
else:
    # SIF log columns
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

# Dummy function to discard the date string (kept for parity)
def date2str(_):
    return 0

# --- CLI args ---
if len(sys.argv) < 2:
    sys.exit("Usage: {} <logfile.tsv>".format(sys.argv[0]))

Filename = sys.argv[1]
print("Filename:", Filename)

# Read the heading row
with open(Filename, "r", encoding="utf-8", errors="replace") as fh:
    header_line = fh.readline()

Heading = header_line.rstrip("\n").split("\t")
print("Headings:", len(Heading))
if PMC:
    # Delete the first two unwanted headings
    del Heading[0:2]

# Load numeric data
if PMC:
    Data = np.loadtxt(Filename, dtype=float, skiprows=1, usecols=range(2, 27))
else:
    Data = np.loadtxt(Filename, dtype=float, skiprows=1, usecols=range(0, 23))

if Data.ndim == 1:  # handle single-line file gracefully
    Data = Data[np.newaxis, :]

print("Data read in, row x col", Data.shape, "Elements", Data.size)

# Stats
Min = np.nanmin(Data, axis=0)
Max = np.nanmax(Data, axis=0)
Mean = np.nanmean(Data, axis=0)
Stdev = np.nanstd(Data, axis=0)

# For SIF data, time column is actually computed from secs + nsecs
if not PMC:
    Data[:, ColTime] = Data[:, ColSecs] + (Data[:, ColNSec] / NanoSecPerSec)

# Periods between samples
Period = Data[:, ColTime] - Data[0, ColTime]
if len(Period) >= 2:
    Period[1:] = Data[1:, ColTime] - Data[:-1, ColTime]
    Period[0] = Period[1]

print(
    "Periods",
    "  min : {:.3f},".format(float(np.nanmin(Period))),
    " max : {:.3f},".format(float(np.nanmax(Period))),
    "mean : {:.3f},".format(float(np.nanmean(Period))),
    "stdev : {:.3f},".format(float(np.nanstd(Period))),
)

# Reference stats
col = Reference
print(
    Heading[col],
    " min : {:.3f},".format(float(Min[col])),
    " max : {:.3f},".format(float(Max[col])),
    "mean : {:.3f},".format(float(Mean[col])),
    "stdev : {:.3f},".format(float(Stdev[col])),
)

# Third-quarter slices (use integer indexing)
start = (len(Data) * 2) // 4
end = (len(Data) * 3) // 4

print(
    "RMS Red Axial Load     (third quarter) : %8.2f (milli Volt)"
    % (qmean(Data[start:end, RedAxialLoad]) * 1000.0)
)
print(
    "RMS Yellow Axial Load  (third quarter) : %8.2f (milli Volt)"
    % (qmean(Data[start:end, YelAxialLoad]) * 1000.0)
)
print(
    "RMS Blue Axial Load    (third quarter) : %8.2f (milli Volt)"
    % (qmean(Data[start:end, BluAxialLoad]) * 1000.0)
)
print(
    "RMS Red Radial Load    (third quarter) : %8.2f (milli Volt)"
    % (qmean(Data[start:end, RedRadialLoad]) * 1000.0)
)
print(
    "RMS Yellow Radial Load (third quarter) : %8.2f (milli Volt)"
    % (qmean(Data[start:end, YelRadialLoad]) * 1000.0)
)
print(
    "RMS Blue Radial Load   (third quarter) : %8.2f (milli Volt)"
    % (qmean(Data[start:end, BluRadialLoad]) * 1000.0)
)
print(
    "RMS North/South vector (third quarter) : %8.2f (milli Volt)"
    % (qmean(Data[start:end, NorthSouthVector]) * 1000.0)
)
print(
    "RMS East/West   vector (third quarter) : %8.2f (milli Volt)"
    % (qmean(Data[start:end, EastWestVector]) * 1000.0)
)

# Time axis
Time = Data[:, ColTime] - Data[0, ColTime]

# --- Plotting ---

def _set_title(fig, title):
    fig.suptitle(title)
    try:
        # Modern Matplotlib path
        fig.canvas.manager.set_window_title(title)
    except Exception:
        # Some non-interactive backends don't have a window manager
        pass

count = 0

if GraphLoad:
    count += 1
    fig = plt.figure(count, figsize=(8, 6))
    _set_title(fig, "Loads")
    plt.plot(Time, Data[:, RedAxialLoad], label=Heading[RedAxialLoad], c="r", linestyle=StyleSolid)
    plt.plot(Time, Data[:, YelAxialLoad], label=Heading[YelAxialLoad], c="y", linestyle=StyleSolid)
    plt.plot(Time, Data[:, BluAxialLoad], label=Heading[BluAxialLoad], c="b", linestyle=StyleSolid)
    plt.plot(Time, Data[:, RedRadialLoad], label=Heading[RedRadialLoad], c="r", linestyle=StyleDash)
    plt.plot(Time, Data[:, YelRadialLoad], label=Heading[YelRadialLoad], c="y", linestyle=StyleDash)
    plt.plot(Time, Data[:, BluRadialLoad], label=Heading[BluRadialLoad], c="b", linestyle=StyleDash)
    plt.xlabel("Time (sec)")
    plt.ylabel("Load (V)")
    plt.legend(loc=0)

if GraphAxial:
    count += 1
    fig = plt.figure(count, figsize=(8, 6))
    _set_title(fig, "Axial")
    plt.plot(Time, Data[:, RedAxialDrive], label=Heading[RedAxialDrive], c="r", linestyle=StyleDots)
    plt.plot(Time, Data[:, YelAxialDrive], label=Heading[YelAxialDrive], c="y", linestyle=StyleDots)
    plt.plot(Time, Data[:, BluAxialDrive], label=Heading[BluAxialDrive], c="b", linestyle=StyleDots)
    plt.plot(Time, Data[:, RedValveFeedback], label=Heading[RedValveFeedback], c="r", linestyle=StyleSolid)
    plt.plot(Time, Data[:, YelValveFeedback], label=Heading[YelValveFeedback], c="y", linestyle=StyleSolid)
    plt.plot(Time, Data[:, BluValveFeedback], label=Heading[BluValveFeedback], c="b", linestyle=StyleSolid)
    plt.xlabel("Time (sec)")
    plt.ylabel("Drive/Feedback (V)")
    plt.legend(loc=0)

if GraphLateral:
    count += 1
    fig = plt.figure(count, figsize=(8, 6))
    _set_title(fig, "Lateral")
    plt.plot(Time, Data[:, Lateral1LoadDrive], label=Heading[Lateral1LoadDrive], c="k", linestyle=StyleDots)
    plt.plot(Time, Data[:, Lateral1PreLoadDrive], label=Heading[Lateral1PreLoadDrive], c="g", linestyle=StyleDots)
    if PMC:
        plt.plot(Time, Data[:, Lateral2LoadDrive], label=Heading[Lateral2LoadDrive], c="c", linestyle=StyleDots)
        plt.plot(Time, Data[:, Lateral2PreLoadDrive], label=Heading[Lateral2PreLoadDrive], c="m", linestyle=StyleDots)
    plt.plot(Time, Data[:, Lateral1LoadValveFeedback], label=Heading[Lateral1LoadValveFeedback], c="k", linestyle=StyleSolid)
    plt.plot(Time, Data[:, Lateral1PreLoadValveFeedback], label=Heading[Lateral1PreLoadValveFeedback], c="g", linestyle=StyleSolid)
    if PMC:
        plt.plot(Time, Data[:, Lateral2LoadValveFeedback], label=Heading[Lateral2LoadValveFeedback], c="c", linestyle=StyleSolid)
        plt.plot(Time, Data[:, Lateral2PreLoadValveFeedback], label=Heading[Lateral2PreLoadValveFeedback], c="m", linestyle=StyleSolid)
    plt.xlabel("Time (sec)")
    plt.ylabel("Drive/Feedback (V)")
    plt.legend(loc=0)

if GraphAngle:
    count += 1
    fig = plt.figure(count, figsize=(8, 6))
    _set_title(fig, "Zenith Angle")
    plt.plot(Time, Data[:, Angle], label=Heading[Angle], c="k")
    plt.xlabel("Time (sec)")
    plt.ylabel("Angle (deg)")
    plt.legend(loc=0)
    plt.ylim(90, -10)

if GraphVector:
    count += 1
    fig = plt.figure(count, figsize=(8, 6))
    _set_title(fig, "Vectors")
    plt.plot(Time, Data[:, NorthSouthVector], label=Heading[NorthSouthVector], c="g")
    plt.plot(Time, Data[:, EastWestVector], label=Heading[EastWestVector], c="m")
    plt.xlabel("Time (sec)")
    plt.ylabel("Vector (V)")
    plt.legend(loc=0)

plt.show()

