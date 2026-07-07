#!/usr/bin/env python
# coding: utf-8

#This function calculates the yearly number of threshold exceedances for the given thresholds.

import os
import sys
import numpy as np
import xarray as xr
import cftime

#Input:
#  - model: model name (string)
#  - RCP: RCP or SSP (string)
#  - dir_HIday: directory where heat stress indicators are stored (string)
#  - dir_save: directory where output should be stored (string)
#  - heat_ind: name of heat stress indicator (string)
#  - BC_methods: name of bias correction methods that should be considered (list of strings)
#  - time_range: time period that should be considered (numpy array with two elements)
#  - member: model member (string)
#  - MODvers: Name of dataset (CMIP5, CMIP6, CORDEX region) (string)
def calc_thresh_IPCC(model, RCP, dir_HIday, dir_save, heat_ind, BC_methods, time_range, member='', MODvers='CMIP6'):

    dir_regr = '/div/amoc/exhaustion/Heat_Health_Global/Data/Masks_Heights_Grids/Regridding/'    
    
    #Define standard ensemble member
    if (member=='') and ('CMIP' in MODvers):      member = 'r1i1p1f1'
    elif (member=='') and ('CORDEX' in MODvers):  member = 'r1i1p1'  
            
    #Define model string
    if 'CORDEX' in MODvers:
        regr_str = MODvers + '_' + model
    else:
        regr_str = model

    ############ JUST TEMPORARY ###############
    if 'CORDEX' in MODvers and 'tmp_clemens' in dir_HIday:
        regr_str2 = model
    else:
        regr_str2 = regr_str
    ############ JUST TEMPORARY ###############
    
    #Define compression level
    comp = dict(zlib=True, complevel=2)

    #Define thresholds
    if heat_ind=='WBGTindoor':
        thresholds = [31, 33, 35]
    elif heat_ind=='HI_NOAA':
        thresholds = [27, 32, 41]
    elif heat_ind in ['TXmean', 'tasmax']:
        thresholds = [35]
    else:
        sys.exit('No thresholds defined for this HSI. Please define them first!')
    
    #Loop over bias correction methods
    for BC_met, time_sel in zip(BC_methods, time_range):
        
        time_str = str(time_sel[0]) + '-' + str(time_sel[1])

        #Read data
        if model=='ERA5':
            fname = dir_HIday + heat_ind + '_' + model + '_' + time_str + '.nc'
            re_index = False
        else:
            folder_mod = dir_HIday + regr_str2 + BC_met + '/'
            fname = folder_mod + heat_ind + '_' + regr_str + '_' + RCP + '_' + member + '_' + time_str + '.nc'
            re_index = True

        #Read data and drop unnecessary variables
        data = xr.open_dataset(fname)
        vars_drop = set(data.data_vars).difference([heat_ind])
        data = data.drop(vars_drop)
        
        #Convert K to °C if necessary
        if heat_ind in ['TXmean', 'tasmax']:
            
            if data[heat_ind].mean()>150:
                data = data - 273.15

        #Loop over thresholds
        create = 1
        for i in range(0, len(thresholds)):

            #Read and apply threshold
            thresh = thresholds[i]
            data_exceed = data>thresh

            #Calculate number of days that exceed threshold each month
            data_exceed = data_exceed.resample(time='1Y').sum()
            data_exceed[heat_ind].expand_dims('threshold')

            #Merge data
            if create==1:
                data_coll = data_exceed
                create = 0
            else:    
                data_coll = xr.concat((data_coll, data_exceed), dim='threshold')

        #Assign threshold names and define data type
        data_coll['threshold'] = thresholds
        data_coll['threshold'].attrs['Explanation'] = 'Thresholds for WBGT: 31, 33, and 35 degC'        
        data_coll[heat_ind] = data_coll[heat_ind].astype('int16')

        #Re-index to standard grid
        if re_index==True:
            grid_std  = xr.open_dataset(dir_regr + "Standard_grid_" + regr_str + ".nc")
            if 'lat' in data_coll:   lat_name, lon_name = 'lat', 'lon'
            if 'rlat' in data_coll:  lat_name, lon_name = 'rlat', 'rlon'
            if 'x' in data_coll:     lat_name, lon_name = 'x', 'y'
            check_lat = np.sum(np.abs(data_coll[lat_name].values - grid_std[lat_name].values))
            check_lon = np.sum(np.abs(data_coll[lon_name].values - grid_std[lon_name].values))
            if (check_lat + check_lon)>0:
                try:
                    data_coll = data_coll.reindex({lat_name: grid_std[lat_name], lon_name: grid_std[lon_name]}, method='nearest')
                except:
                    data_coll[lat_name] = grid_std[lat_name]
                    data_coll[lon_name] = grid_std[lon_name]

        #Create output folders and filename
        dir_thr = dir_save + 'Threshold_exceedance/'
        dir_mod = dir_thr + MODvers + '/'
        dir_out = dir_mod + model + '/'
        if not os.path.exists(dir_thr): os.mkdir(dir_thr)
        if not os.path.exists(dir_mod): os.mkdir(dir_mod)
        if not os.path.exists(dir_out): os.mkdir(dir_out)
        if model=='ERA5':
            fname_out = dir_out + 'ThreshExceed-' + heat_ind + '_' + model + '_' + time_str + BC_met + '.nc'
        else:
            fname_out = dir_out + 'ThreshExceed-' + heat_ind + '_' + model + '_' + RCP + '_' + member + '_' + time_str + BC_met + '.nc'

        #Remove file if it exists
        if os.path.exists(fname_out): os.remove(fname_out)
        
        #Save in file
        encoding = {var: comp for var in data_coll.data_vars}
        data_coll.to_netcdf(fname_out, encoding=encoding)
        