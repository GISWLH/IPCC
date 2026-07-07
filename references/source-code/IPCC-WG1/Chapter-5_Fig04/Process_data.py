"""
Class for processing all the data for plotting 3gases from paleo to recent period.

"""

import os, sys, glob
import datetime

from math import pi, sqrt, atan2
from scipy import optimize
from scipy import stats
from scipy import interpolate
from scipy import fftpack
import numpy as np
from math import *
import pandas as pd

###################################################
#************** Defined Functions *****************
####################################################

#######################################
# Find files from the directory
#++++++++++++++++++++++++++++++++++++++
def ListFiles(pathin):
 filenames=[]
 for root, dirs, files in os.walk(pathin):
    files1 = glob.glob(root + '*.txt')
    for fname in files1:
        filenames.append(fname)
 files=np.array(filenames)
 nfile=files.size; print('nfile=', nfile)
 return files, nfile

#########################################
# Function for calculating yearly mean
#++++++++++++++++++++++++++++++++++++++++
ft = []; gt =[]; trn = []
def YearlyMean(dyr, yr, val):
  emis = []
  for i in range(dyr.shape[0]):
    ij = np.where(int(dyr[i]) == yr)
    if(np.array(ij).size) > 0:
      emis.append(np.nanmean(val[ij]))
    else:
      emis.append(np.nanmean(np.nan))
  emis = np.array(emis)
  return emis

#########################################################
#************** End of defining functions ************
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ************ Read CO2 observations ****************
def StnCO2read(datpath, dum_yr, stn): 

  " " " Read Station CO2 data " " "
  vdat = np.zeros([dum_yr.shape[0], stn.size])

  # Find file list from directory
  files1, nfile1 = ListFiles(datpath)

  # Read data
  for ifile in files1:
 
    vals  = []
    ss    = ifile.split('/')[-1].split('_')[0]; print(ss)
    vals  = np.loadtxt(ifile,dtype='float',skiprows=60)
    yr    = np.array(vals[:,0],dtype=np.int)#; print(yr$^{-1}$)
    dat   = np.array(vals[:,4]) # obs_fitted
    dat[dat<250] = np.nan

    # Station wise yearly mean
    for jj in range(stn.size):
      id1 = []; mvals = []
      id1 = np.where(stn[jj] == ss)
      if(np.array(id1).size) > 0:
        # Yearly mean
        mvals = YearlyMean(dum_yr, yr, dat)
        vdat[:,jj] = mvals
  
  return vdat


# ************ Read CH4 observations ****************
def StnCH4read(datpath, dum_yr, stn):

  " " " Read Station CH4 data " " "
  vdat = np.zeros([dum_yr.shape[0], stn.size])

  # Find file list from directory
  files1, nfile1 = ListFiles(datpath)

  # Read data
  for ifile in files1:

    vals  = []
    ss    = ifile.split('/')[-1].split('_')[0]; print(ss)
    vals  = np.loadtxt(ifile, dtype='S').astype(str)
    yr    = np.array(vals[:,2],dtype='d')#; print(yr$^{-1}$)
    dat   = np.array(vals[:,13], dtype='d')

    # Station wise yearly mean
    for jj in range(stn.size):
      id1 = []; mvals = []
      id1 = np.where(stn[jj] == ss)
      if(np.array(id1).size) > 0:
        # Yearly mean
        mvals = YearlyMean(dum_yr, yr, dat)
        vdat[:,jj] = mvals

  return vdat

# ************ Read CH4 observations ****************
def StnN2Oread(datpath, dum_yr, stn):

  " " " Read Station CH4 data " " "
  vdat = np.zeros([dum_yr.shape[0], stn.size])

  # Find file list from directory
  files1, nfile1 = ListFiles(datpath)

  # Read data
  for ifile in files1:

    vals  = []
    ss    = ifile.split('/')[-1].split('_')[0]; print(ss)
    vals  = np.loadtxt(ifile, dtype='S').astype(str)
    yr    = np.array(vals[:,2],dtype='d')#; print(yr$^{-1}$)
    dat   = np.array(vals[:,7], dtype='d')

    # Station wise yearly mean
    for jj in range(stn.size):
      id1 = []; mvals = []
      id1 = np.where(stn[jj] == ss)
      if(np.array(id1).size) > 0:
        # Yearly mean
        mvals = YearlyMean(dum_yr, yr, dat)
        vdat[:,jj] = mvals

  return vdat

# ************ Read ice core data ******************

def IceDatRead(path1, path2, path3):

  " " " lawDomeIce core (AD) " " "
  co2 = np.loadtxt(path1, dtype='float', skiprows=1)
  ch4 = np.loadtxt(path2, dtype='float', skiprows=1)
  n2o = np.loadtxt(path3, dtype='float', skiprows=1)

  c1 = np.zeros([co2.shape[0], 2])
  c2 = np.zeros([ch4.shape[0], 2])
  c3 = np.zeros([n2o.shape[0], 2])

  c1[:,0] = np.array(co2[:,0],dtype='d')
  c1[:,1] = np.array(co2[:,1],dtype='d')*1.01 # For scaling with axis

  c2[:,0] = np.array(ch4[:,0],dtype='d')
  c2[:,1] = np.array(ch4[:,2],dtype='d')

  c3[:,0] = np.array(n2o[:,0],dtype='d')
  c3[:,1] = np.array(n2o[:,1],dtype='d')

  # Store all the data in an array
  ff = []
  ff.append([c1, c2, c3])
  ice_dat = np.array(ff)

  return ice_dat


# ************ Read Vostock/EPA data ******************

def VosDatRead(path1, path2, path3):

  " " " EPA Dome data (800 kyr$^{-1}$ BC) " " "
  co2 = np.loadtxt(path1, dtype='float', skiprows=1)
  ch4 = np.loadtxt(path2, dtype='S', skiprows=28).astype(str)
  n2o = np.loadtxt(path3, dtype='float', skiprows=38)

  c1 = np.zeros([co2.shape[0], 2])
  c2 = np.zeros([ch4.shape[0], 2])
  c3 = np.zeros([n2o.shape[0], 2])

  c1[:,0] = np.array(co2[:,0],dtype='d') #/1000
  c1[:,1] = np.array(co2[:,1],dtype='d')

  c2[:,0] = np.array(ch4[:,1],dtype='d')/1000
  c2[:,1] = np.array(ch4[:,2],dtype='d')

  c3[:,0] = np.array(n2o[:,2],dtype='d')/1000
  c3[:,1] = np.array(n2o[:,3],dtype='d')

  # Store all the data in an array
  ff = []
  ff.append([c1, c2, c3])
  VOS_dat = np.array(ff)

  return VOS_dat


# ************ High resolution data ******************

def WdcDatRead(path1):

   " " " West Antartic Divide " " "
   df = pd.read_excel (path1+r'nature13799-s1.xlsx', header=2, usecols = [2,3], converters= {1: pd.to_datetime}, sheet_name="WDC CO2", names = ['Gas_Age','CO2'])
   df1 = pd.read_excel (path1+r'nature13799-s1.xlsx', header=2, usecols = [2,3], converters= {1: pd.to_datetime}, sheet_name="WDC CH4", names = ['Gas_Age','CH4'])

   #CO2
   tt     = np.array(df.Gas_Age)
   ntime  = tt.size
   WDC_CO2 = np.zeros([ntime,2])

   WDC_CO2[:,0] = np.array(df.Gas_Age, dtype = 'float')
   WDC_CO2[:,1] = np.array(df.CO2, dtype = 'float')

   #CH4
   tt     = np.array(df1.Gas_Age)
   ntime  = tt.size
   WDC_CH4 = np.zeros([ntime,2])

   WDC_CH4[:,0] = np.array(df1.Gas_Age, dtype = 'float')
   WDC_CH4[:,1] = np.array(df1.CH4, dtype = 'float')

   # Store all the data in an array
   ff = []
   ff.append([WDC_CO2,WDC_CH4])
   WDC_dat = np.array(ff)

   return WDC_dat


# ************ Long lived greenhouse gases ******************

def LLGHGDatRead(path1):

   " " " Histories of long-lived greenhouse gases (global annual mean at Earth's surface) derived from multiple sources. " " "
   df = pd.read_excel (path1+r'LLGHG_history_AR6_v9_updated.xlsx', header=22, usecols = [0,1,2,3], sheet_name="MR_output", names = ['Year','CO2', 'CH4', 'N2O'])

   tt     = np.array(df.Year)
   ntime  = tt.size
   dat = np.zeros([ntime,4])

   dat[:,0] = np.array(df.Year, dtype = 'float')
   dat[:,1] = np.array(df.CO2, dtype = 'float')
   dat[:,2] = np.array(df.CH4, dtype = 'float')
   dat[:,3] = np.array(df.N2O, dtype = 'float')

   return dat



