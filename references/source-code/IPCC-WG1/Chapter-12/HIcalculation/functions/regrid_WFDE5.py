#!/usr/bin/env python
# coding: utf-8

#This functions regrid WFDE5 data to the respective cliamte model grid (for CMIP5, CMIP6, and CORDEX)

import os
import sys
import xarray as xr
import numpy as np
import time as t_util


# Regrid WFDE5 to CMIP grids
#Input:
#  - model: model name (string)
#  - HSIs: Heat stress indicators (list of strings)
#  - dir_WFDE_orig: Folder where reference data are stored (string)
#  - dir_WFDE5_out: Folder where regridded reference data should be stored (string)
#  - version: Name of reference data (string)
#  - y_sta: Start year (integer)
#  - y_end: End year (integer)
def regrid_HSIs_WFDE5_to_CMIP(model, HSIs, dir_WFDE_orig, dir_WFDE5_out, version='WFDE5', y_sta=1981, y_end=2010):
    
    print('  Regridding ' + version + ' data to ' + model + ' grid...')
    
    #Define grid folder
    dir_grids = '/div/amoc/exhaustion/Heat_Health_Global/Data/Masks_Heights_Grids/'

    #Get year string
    y_staS = str(y_sta)
    y_endS = str(y_end)
    years  = [y_staS, y_endS]

    #Create vector with no leap years and save it
    dates_noleap = xr.cftime_range(start=y_staS + '0101', end=y_endS + '1231', freq='D', calendar='noleap')

    #Save in files
    DOY    = dates_noleap.dayofyear
    YEARS  = dates_noleap.year
    MONTHS = dates_noleap.month
    np.savetxt(dir_WFDE_orig + y_staS + "-" + y_endS + "_dates_DOY_365.csv", DOY, fmt='%i', delimiter=",")
    np.savetxt(dir_WFDE_orig + y_staS + "-" + y_endS + "_dates_YEARS_365.csv", YEARS, fmt='%i', delimiter=",")
    np.savetxt(dir_WFDE_orig + y_staS + "-" + y_endS + "_dates_MONTHS_365.csv", MONTHS, fmt='%i', delimiter=",")
    
    #Get filename of grid file for CMIP6 model 
    file_grid = dir_grids + "Regridding/" + 'grid_xy_' + model

    #Loop over all selected heat stress indicators
    for HSI in HSIs:

        print('  -' + HSI, end='')
        start = t_util.time()

        #Re-map WFDE5 data
        file_WFDE5 = dir_WFDE_orig + HSI + '_WFDE5_1981-2010.nc'
        file_out_WFDE = dir_WFDE5_out + HSI + "_WFDE5_" + years[0] + "-" + years[1] + ".nc"
        os.system("cdo -b F32 remapcon," + file_grid + " " + file_WFDE5 + " " + file_out_WFDE)
        
        #Open data set
        with xr.open_dataset(file_out_WFDE) as ds:
            data_WFDE5 = ds.load()
            ds.close()

        if 'time_bnds' in data_WFDE5:
            data_WFDE5 = data_WFDE5.drop('time_bnds')
            
        #Select data only between 1981 and 2010
        data_WFDE5 = data_WFDE5.sel(time=slice(years[0], years[1]))

        #Delete 29th of February
        sel_WFDE5 = ~((data_WFDE5.time.dt.month==2) & (data_WFDE5.time.dt.day==29))
        data_WFDE5 = data_WFDE5.isel(time=sel_WFDE5)
        data_WFDE5['time'] = dates_noleap

        #Save data in file
        data_WFDE5.to_netcdf(file_out_WFDE)

        stop = t_util.time()
        print(', time = ' + "{:.2f}".format(stop - start))

        
# Regrid WFDE5 to CORDEX grids
#Input:
#  - model: model name (string)
#  - HSIs: Heat stress indicators (list of strings)
#  - dir_WFDE_orig: Folder where reference data are stored (string)
#  - name_out: Output name that defines output filename based on name of CORDEX region (string)
#  - method: Select interpolation method (string)
#  - y_sta: Start year (integer)
#  - y_end: End year (integer)
def regrid_HSIs_WFDE5_to_CORDEX(model, HSIs, dir_WFDE_orig, name_out, method='con', y_sta=1981, y_end=2010):
    
    print('  Regridding WFDE5 data to ' + model + ' grid...')
    
    #Define folders
    dir_grids = '/div/amoc/exhaustion/Heat_Health_Global/Data/Masks_Heights_Grids/'
    dir_WFDE5_regr = dir_WFDE_orig + '/WFDE5_regrid/'
    dir_WFDE5_out  = dir_WFDE5_regr + name_out + '_grid/'
    if not os.path.exists(dir_WFDE5_out): os.mkdir(dir_WFDE5_out)  
    if not os.path.exists(dir_WFDE5_regr): os.mkdir(dir_WFDE5_regr)
    
    #Get DOY for no-leap calendar
    y_staS = str(y_sta)
    y_endS = str(y_end)
    years = [y_staS, y_endS]

    #Create vector with no leap years and save it
    dates_noleap = xr.cftime_range(start=y_staS + '0101', end=y_endS + '1231', freq='D', calendar='noleap')

    #Save in files
    DOY    = dates_noleap.dayofyear
    YEARS  = dates_noleap.year
    MONTHS = dates_noleap.month
    np.savetxt(dir_WFDE_orig + y_staS + "-" + y_endS + "_dates_DOY_365.csv", DOY, fmt='%i', delimiter=",")
    np.savetxt(dir_WFDE_orig + y_staS + "-" + y_endS + "_dates_YEARS_365.csv", YEARS, fmt='%i', delimiter=",")
    np.savetxt(dir_WFDE_orig + y_staS + "-" + y_endS + "_dates_MONTHS_365.csv", MONTHS, fmt='%i', delimiter=",")
    
    #Get filename of grid file for CMIP6 model 
    file_grid = dir_grids + "Regridding/" + 'grid_xy_' + model
    
    #Loop over all selected heat stress indicators
    for HSI in HSIs:

        print('  -' + HSI, end='')
        start = t_util.time()

        #Re-map WFDE5 data
        file_WFDE5 = dir_WFDE_orig + HSI + '_WFDE5_1981-2010.nc'
        file_out_WFDE = dir_WFDE5_out + HSI + "_WFDE5_" + years[0] + "-" + years[1] + ".nc"
        if method=='con':
            os.system("cdo -b F32 remapcon," + file_grid + " " + file_WFDE5 + " " + file_out_WFDE)
        elif method=='bil':
            os.system("cdo -b F32 remapbil," + file_grid + " " + file_WFDE5 + " " + file_out_WFDE)
            
        #Open data set
        with xr.open_dataset(file_out_WFDE) as ds:
            data_WFDE5 = ds.load()
            ds.close()

        #Select data only between 1981 and 2010
        data_WFDE5 = data_WFDE5.sel(time=slice(years[0], years[1]))

        #Delete 29th of February
        sel_WFDE5 = ~((data_WFDE5.time.dt.month==2) & (data_WFDE5.time.dt.day==29))
        data_WFDE5 = data_WFDE5.isel(time=sel_WFDE5)
        data_WFDE5['time'] = dates_noleap
        
        #Save data in file
        data_WFDE5.to_netcdf(file_out_WFDE)

        stop = t_util.time()
        print(', time = ' + "{:.2f}".format(stop - start))
