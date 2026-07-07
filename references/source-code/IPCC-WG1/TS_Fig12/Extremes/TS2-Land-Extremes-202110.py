#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:12:01 2021

@author: gkrinner
"""

import numpy as np
from xlrd import open_workbook
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path
from matplotlib.textpath import TextToPath
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import csv

selectlevels = ['1.0', '1.5', '2.0', '3.0', '4.0']
dx = .1
sizeref = 100
size0 = .25*sizeref
size1 = 1*sizeref
size2 = 1.5*sizeref
size3 = 2.25*sizeref
large = 2.3*dx

def get_positions(dx0,selectlevels):

    npos = len(selectlevels)
    retpos = np.empty((npos),np.float)

    if (False):
        retpos = np.arange(dx0, np.float(npos)+dx0)
    else:
        for i in range(npos):
           retpos[i] = dx0 + float(selectlevels[i])
    
    return retpos

def read_csv(filename):

   varout = np.empty((nsGWL,nrange),np.float)

   fields = []
   with open(filename, 'r') as csvfile:
      csvreader = csv.reader(csvfile)
      fields = next(csvreader)
      for row in csvreader:
         for iGWL in range(nsGWL):
            if (float(row[0]) == float(selectlevels[iGWL])):
               for ir in range(nrange):
                  varout[iGWL,ir] = float(row[ir+1])

   return varout

fp = FontProperties(fname=r"Font Awesome 5 Free-Solid-900.otf")

symbols = dict(thermometer = "\uf2c9",
               cloudshowersheavy = "\uf740",
               hourglass = "\uf253",
               stopwatch = "\uf2f2",
               nowater = "\uf5c7")

def get_marker(symbol):
    v, codes = TextToPath().get_text_path(fp, symbol)
    v = np.array(v)
    mean = np.mean([np.max(v,axis=0), np.min(v, axis=0)], axis=0)
    return Path(v-mean, codes, closed=False)

nGWL = 5
nrange = 5

i50 = 0; i17 = 1; i83 = 2; i5 = 3; i95 = 4
# iup = i83; ilo = i17
iup = i95; ilo = i5

c10 = "sandybrown"
c50 = "saddlebrown"

nsGWL = len(selectlevels)

FreqTXx10s = np.empty((nsGWL,nrange),np.float)
FreqTXx50s = np.empty((nsGWL,nrange),np.float)
IntTXx10s = np.empty((nsGWL,nrange),np.float)
IntTXx50s = np.empty((nsGWL,nrange),np.float)

FreqRx1day10s = np.empty((nsGWL,nrange),np.float)
FreqRx1day50s = np.empty((nsGWL,nrange),np.float)
IntRx1day10s = np.empty((nsGWL,nrange),np.float)
IntRx1day50s = np.empty((nsGWL,nrange),np.float)

FreqDrought10s = np.empty((nsGWL,nrange),np.float)
IntDrought10s = np.empty((nsGWL,nrange),np.float)

filename = 'TXx_freq_change_50_year_event.csv'
FreqTXx50s = read_csv(filename)

filename = 'TXx_freq_change_10_year_event.csv'
FreqTXx10s = read_csv(filename)

filename = 'TXx_intens_change_50_year_event.csv'
IntTXx50s = read_csv(filename)

filename = 'Rx1day_freq_change_50_year_event.csv'
FreqRx1day50s = read_csv(filename)

filename = 'Rx1day_freq_change_10_year_event.csv'
FreqRx1day10s = read_csv(filename)

filename = 'Rx1day_intens_change_50_year_event.csv'
IntRx1day50s = read_csv(filename)

filename = 'Rx1day_intens_change_10_year_event.csv'
IntRx1day10s = read_csv(filename)

filename = 'TXx_intens_change_10_year_event.csv'
IntTXx10s = read_csv(filename)

filename = 'drought_freq_change_10_year_event.csv'
FreqDrought10s = read_csv(filename)

filename = 'drought_intens_change_10_year_event.csv'
IntDrought10s = read_csv(filename) * (-1.)

"""
TXx
"""

fig, ax = plt.subplots()

dx0 = -1.5*dx
positions = get_positions(dx0,selectlevels)
ax.scatter(positions, FreqTXx10s[:,i50],
        marker=get_marker(symbols["stopwatch"]), 
        s = size2, c=c10, edgecolors="none", linewidth=2,
        label="10-year event, frequency")
ax.scatter(positions, FreqTXx10s[:,iup], marker='1', s = size0, c=c10, edgecolors="none", linewidth=1)
ax.scatter(positions, FreqTXx10s[:,ilo], marker='2', s = size0, c=c10, edgecolors="none", linewidth=1)

axr = ax.twinx()
dx0 = -.5*dx
positions = get_positions(dx0,selectlevels)
axr.scatter(positions, IntTXx10s[:,i50],
        marker=get_marker(symbols["thermometer"]), 
        s = size3, c=c10, edgecolors="none", linewidth=2,
        label="10-year event, intensity")
axr.scatter(positions, IntTXx10s[:,iup], marker='1', s = size0, c=c10, edgecolors="none", linewidth=1)
axr.scatter(positions, IntTXx10s[:,ilo], marker='2', s = size0, c=c10, edgecolors="none", linewidth=1)

dx0 = .5*dx
positions = get_positions(dx0,selectlevels)
ax.scatter(positions, FreqTXx50s[:,i50],
        marker=get_marker(symbols["stopwatch"]), 
        s = size2, c=c50, edgecolors="none", linewidth=2,
        label="50-year event, frequency")
ax.scatter(positions, FreqTXx50s[:,iup], marker='1', s = size0, c=c50, edgecolors="none", linewidth=1)
ax.scatter(positions, FreqTXx50s[:,ilo], marker='2', s = size0, c=c50, edgecolors="none", linewidth=1)

dx0 = 1.5*dx
positions = get_positions(dx0,selectlevels)
axr.scatter(positions, IntTXx50s[:,i50],
        marker=get_marker(symbols["thermometer"]), 
        s = size3, c=c50, edgecolors="none", linewidth=2,
        label="50-year event, intensity")
axr.scatter(positions, IntTXx50s[:,iup], marker='1', s = size0, c=c50, edgecolors="none", linewidth=1)
axr.scatter(positions, IntTXx50s[:,ilo], marker='2', s = size0, c=c50, edgecolors="none", linewidth=1)

ax.set_ylabel('Relative frequency (Preindustrial=1)')

dx0 = 0.
positions = get_positions(dx0,selectlevels)
ax.set_xticks(positions)
ax.set_xticklabels(selectlevels)
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.tick_params(which='minor',length=15)

# fond
for i in range(nsGWL):
    ax.axvspan(float(selectlevels[i])-large,float(selectlevels[i])+large, alpha=0.1, color='grey')

axr.set_ylabel('Intensity change (°C)')
fig.legend(bbox_to_anchor=(.53, .87), labelspacing=.8)
ax.set_xlabel('Global surface temperature change since 1850-1900 (°C)')
ax.set_title('a) Hot extreme events')
plt.savefig("TXx.pdf")
plt.savefig("TXx.png")


"""
Rx1day
"""

fig, ax = plt.subplots()

dx0 = -1.5*dx
positions = get_positions(dx0,selectlevels)
ax.scatter(positions, FreqRx1day10s[:,i50],
        marker=get_marker(symbols["stopwatch"]), 
        s = size2, c=c10, edgecolors="none", linewidth=2,
        label="10-year event, frequency")
ax.scatter(positions, FreqRx1day10s[:,iup], marker='1', s = size0, c=c10, edgecolors="none", linewidth=1)
ax.scatter(positions, FreqRx1day10s[:,ilo], marker='2', s = size0, c=c10, edgecolors="none", linewidth=1)

axr = ax.twinx()
dx0 = -.5*dx
positions = get_positions(dx0,selectlevels)
axr.scatter(positions, IntRx1day10s[:,i50],
        marker=get_marker(symbols["cloudshowersheavy"]), 
        s = size1, c=c10, edgecolors="none", linewidth=2,
        label="10-year event, intensity")
axr.scatter(positions, IntRx1day10s[:,iup], marker='1', s = size0, c=c10, edgecolors="none", linewidth=1)
axr.scatter(positions, IntRx1day10s[:,ilo], marker='2', s = size0, c=c10, edgecolors="none", linewidth=1)

dx0 = .5*dx
positions = get_positions(dx0,selectlevels)
ax.scatter(positions, FreqRx1day50s[:,i50],
        marker=get_marker(symbols["stopwatch"]), 
        s = size2, c=c50, edgecolors="none", linewidth=2,
        label="50-year event, frequency")
ax.scatter(positions, FreqRx1day50s[:,iup], marker='1', s = size0, c=c50, edgecolors="none", linewidth=1)
ax.scatter(positions, FreqRx1day50s[:,ilo], marker='2', s = size0, c=c50, edgecolors="none", linewidth=1)

dx0 = 1.5*dx
positions = get_positions(dx0,selectlevels)
axr.scatter(positions, IntRx1day50s[:,i50],
        marker=get_marker(symbols["cloudshowersheavy"]), 
        s = size1, c=c50, edgecolors="none", linewidth=2,
        label="50-year event, intensity")
axr.scatter(positions, IntRx1day50s[:,iup], marker='1', s = size0, c=c50, edgecolors="none", linewidth=1)
axr.scatter(positions, IntRx1day50s[:,ilo], marker='2', s = size0, c=c50, edgecolors="none", linewidth=1)

ax.set_ylabel('Relative frequency (Preindustrial=1)')

dx0 = 0.
positions = get_positions(dx0,selectlevels)
ax.set_xticks(positions)
ax.set_xticklabels(selectlevels)
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.tick_params(which='minor',length=15)

# fond
for i in range(nsGWL):
    ax.axvspan(float(selectlevels[i])-large,float(selectlevels[i])+large, alpha=0.1, color='grey')

axr.set_ylabel('Intensity change (%)')
fig.legend(bbox_to_anchor=(.53, .87), labelspacing=.8)

ax.set_xlabel('Global surface temperature change since 1850-1900 (°C)')
ax.set_title('b) Heavy precipitation events')
plt.savefig("Rx1day.pdf")
plt.savefig("Rx1day.png")

"""
Drought
"""

fig, ax = plt.subplots()

dx0 = -.5*dx
positions = get_positions(dx0,selectlevels)
ax.scatter(positions, FreqDrought10s[:,i50],
        marker=get_marker(symbols["stopwatch"]), 
        s = size2, c=c10, edgecolors="none", linewidth=2,
        label="10-year event, frequency")
ax.scatter(positions, FreqDrought10s[:,iup], marker='1', s = size0, c=c10, edgecolors="none", linewidth=1)
ax.scatter(positions, FreqDrought10s[:,ilo], marker='2', s = size0, c=c10, edgecolors="none", linewidth=1)

axr = ax.twinx()
dx0 = .5*dx
positions = get_positions(dx0,selectlevels)
axr.scatter(positions, IntDrought10s[:,i50],
        marker=get_marker(symbols["nowater"]), 
        s = size3, c=c10, edgecolors="none", linewidth=2,
        label="10-year event, intensity")
axr.scatter(positions, IntDrought10s[:,ilo], marker='1', s = size0, c=c10, edgecolors="none", linewidth=1)
axr.scatter(positions, IntDrought10s[:,iup], marker='2', s = size0, c=c10, edgecolors="none", linewidth=1)

ax.set_ylabel('Relative frequency (Preindustrial=1)')

dx0 = 0.
positions = get_positions(dx0,selectlevels)
ax.set_xticks(positions)
ax.set_xticklabels(selectlevels)
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.tick_params(which='minor',length=15)

# fond
for i in range(nsGWL):
    ax.axvspan(float(selectlevels[i])-large,float(selectlevels[i])+large, alpha=0.1, color='grey')

axr.set_ylabel('Amplitude of annual soil moisture decrease (-)')
fig.legend(bbox_to_anchor=(.53, .87), labelspacing=.8)

ax.set_xlabel('Global surface temperature change since 1850-1900 (°C)')
ax.set_title('c) Droughts in drought-prone regions')
plt.savefig("Droughts.pdf")
plt.savefig("Droughts.png")

# special output for Sophie & Peter CSB2

iout = [0, 1, 3]

print()
print ('Frequency TXx 10y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], FreqTXx10s[ilev,i5], FreqTXx10s[ilev,i17], FreqTXx10s[ilev,i50], FreqTXx10s[ilev,i83], FreqTXx10s[ilev,i95]))

print()
print ('Intensity TXx 10y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], IntTXx10s[ilev,i5], IntTXx10s[ilev,i17], IntTXx10s[ilev,i50], IntTXx10s[ilev,i83], IntTXx10s[ilev,i95]))

print()
print ('Frequency TXx 50y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], FreqTXx50s[ilev,i5], FreqTXx50s[ilev,i17], FreqTXx50s[ilev,i50], FreqTXx50s[ilev,i83], FreqTXx50s[ilev,i95]))

print()
print ('Intensity TXx 50y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], IntTXx50s[ilev,i5], IntTXx50s[ilev,i17], IntTXx50s[ilev,i50], IntTXx50s[ilev,i83], IntTXx50s[ilev,i95]))

print()
print ('Frequency Rx1day 10y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], FreqRx1day10s[ilev,i5], FreqRx1day10s[ilev,i17], FreqRx1day10s[ilev,i50], FreqRx1day10s[ilev,i83], FreqRx1day10s[ilev,i95]))

print()
print ('Intensity Rx1day 10y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], IntRx1day10s[ilev,i5], IntRx1day10s[ilev,i17], IntRx1day10s[ilev,i50], IntRx1day10s[ilev,i83], IntRx1day10s[ilev,i95]))

print()
print ('Frequency Rx1day 50y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], FreqRx1day50s[ilev,i5], FreqRx1day50s[ilev,i17], FreqRx1day50s[ilev,i50], FreqRx1day50s[ilev,i83], FreqRx1day50s[ilev,i95]))

print()
print ('Intensity Rx1day 50y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], IntRx1day50s[ilev,i5], IntRx1day50s[ilev,i17], IntRx1day50s[ilev,i50], IntRx1day50s[ilev,i83], IntRx1day50s[ilev,i95]))

print()
print ('Frequency Drought 10y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], FreqDrought10s[ilev,i95], FreqDrought10s[ilev,i83], FreqDrought10s[ilev,i50], FreqDrought10s[ilev,i17], FreqDrought10s[ilev,i5]))

print()
print ('Intensity Drought 10y: 5 17 50 83 95')
for i, ilev in enumerate(iout):
   print("{} °C: {} {} {} {} {}".format(selectlevels[ilev], IntDrought10s[ilev,i95], IntDrought10s[ilev,i83], IntDrought10s[ilev,i50], IntDrought10s[ilev,i17], IntDrought10s[ilev,i5]))
