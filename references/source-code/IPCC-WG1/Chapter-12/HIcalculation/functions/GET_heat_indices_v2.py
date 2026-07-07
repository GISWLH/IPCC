#!/usr/bin/env python
# coding: utf-8

#This script organizes the calculation of the heat stress indicators. It reads the relevant data and stores the calculate heat stress indicators (i.e. HI) in the correct folder.

import os
import sys
import xarray as xr
import numpy as np
import dask.array as da
import time as t_util
from multiprocessing import Pool

sys.path.insert(0,'/div/amoc/exhaustion/Heat_Health_Global/Scripts/functions_Py/')
import calc_heat_health_indices as CalcHHI


#Master function for creating folders and call function to calculate heat indices
#Input:
#  - model: model name (string)
#  - SSP: RCP or SSP (string)
#  - member: model member (string)
#  - heat_index: heat stress indicator (in this case HI_NOAA) (string)
#  - dir_in: directory where input files are stored (string)
#  - dir_out: directory where calculated heat stress indicator should be stored (string)
#  - year_vec: vector of years for which the heat stress indicator is calculated (1d numpy array)
#  - dyear (integer)
#  - var_names: variables names of input variables (list of strings)
def GET_heat_indices_v2(model, SSP, member, heat_index, dir_in, dir_out, year_vec, dyear, var_names=['tasmax', 'huss', 'sp'], var_files=['tasmax', 'huss', 'sp']):

    #Input order for variables must be: 1) temperature, 2) pressure, 3) humidity !!
    
    #Calculate heat indices for CMIP6
    param_dict = dict({'scenario': SSP, 'ens_member': member, 'dir_in': dir_in, 'dir_out': dir_out, 'year_vec': year_vec, 'dyear': dyear})
    calc_heat_indices(model, heat_index, param_dict, var_names, var_files)


#Calculate heat indices
def calc_heat_indices(model, heat_index, param_dict, var_names, var_files):

    #Get parameters
    dir_in   = param_dict['dir_in']
    dir_out  = param_dict['dir_out']
    year_vec = param_dict['year_vec']
    dyear    = param_dict['dyear']

    #Define correct variable names
    SSP    = param_dict['scenario']
    member = param_dict['ens_member']

    print('  -calculating ' + heat_index + '... ', end = '')
    start = t_util.time()

    create = 1
    for year in year_vec:

        print(str(year) + ', ', end='')
        
        #Select years
        year_sel = [year, year + dyear - 1]

        #Read data
        data = read_data(dir_in, model, var_files, var_names, SSP, member, year_sel)
        
        # Define chunks
        if heat_index not in ['PT', 'SETstar', 'PET']:
            data = data.chunk(chunks={'time': 6 * dyear})
        
        #Set variable names
        data = data.rename({var_names[0]: 'TX', var_names[1]: 'q', var_names[2]: 'p'})
        
        #Remove unnecessary information
        if 'height' in data.coords: data = data.drop('height')

        #Calculate vapour pressure and relative humidity
        e, RH = CalcHHI.get_humidity(data.q, data.p, data.TX)

        #Define variable names
        data = data.assign({'e': e, 'RH': RH})
        
        # Update chunks
        if heat_index not in ['PT', 'SETstar', 'PET']:
            data = data.chunk(chunks={'time': 6 * dyear})

        # Select heat index
        if heat_index=='HI_NOAA':
            index = CalcHHI.HI_NOAA(data.TX, data.RH)
            
        #Rename dataset and compute index
        index = index.to_dataset(name=heat_index)
        index = index.load()
        index[heat_index].attrs = {'units': '1'}

        #Collect all years
        if create==1:
            index_out = index
            create = 0
        else:
            index_out = xr.concat((index_out, index), dim='time')        

    stop = t_util.time()
    print(' time = ' + "{:.2f}".format(stop - start))

    #Get years and scenario for file name
    t1 = str(year_vec[0])
    t2 = str(year_vec[-1] + dyear - 1)
    if param_dict['scenario']=='':
        scen_out = ''
    else:
        scen_out = param_dict['scenario'] + '_'   
    if param_dict['ens_member']=='':
        ens_out = ''
    else:
        ens_out = param_dict['ens_member'] + '_'   
    
    #Add tasmin to heat index file name
    if var_names[0]=='tasmin':
        T_out = '-tasmin'
    else:
        T_out = ''
    
    #Save heat index to file
    fname_out = dir_out + heat_index + T_out + '_' + model + '_' + scen_out + ens_out + t1 + '-' + t2 + '.nc'
    index_out.astype('float32').to_netcdf(fname_out)


#Read data
def read_data(folder, model, var_files, var_names, SSP, member, year_sel):

    #Folder for regridding
    dir_regr = '/div/amoc/exhaustion/Heat_Health_Global/Data/Masks_Heights_Grids/Regridding/'
    
    #Loop over variables
    create = 1
    for var_f, var_n in zip(var_files, var_names):
        
        file_name = [file for file in os.listdir(folder) if (model + '_' in file) and (var_f + '_' in file) and (SSP + '_' in file) and (member in file)]
        
        #Make sure that only file is selected
        if len(file_name)>1:
            
            file_name = [file for file in file_name if str(year_sel[0]) in file and str(year_sel[1]) in file]
            
            if len(file_name)!=1:
                print(file_name)
                print('File name is not unambiguous!')
                
        #Read and select data
        data = xr.open_dataset(folder + file_name[0])
        data = data.sel(time=slice(str(year_sel[0]), str(year_sel[1])))
        
        #Re-index to standard grid
        fname_std_grid = dir_regr + "Standard_grid_" + model + ".nc"
        if os.path.exists(fname_std_grid):
            grid_std = xr.open_dataset(fname_std_grid)
            if 'rlat' in data: lat_name, lon_name = 'rlat', 'rlon'
            elif 'x' in data:  lat_name, lon_name = 'x', 'y'
            else:              lat_name, lon_name = 'lat', 'lon'
            check1 = np.max(np.abs(data[lat_name].values - grid_std[lat_name].values))
            check2 = np.max(np.abs(data[lon_name].values - grid_std[lon_name].values))
            if (check1!=0) or (check2!=0):
                try:
                    data = data.reindex({lat_name: grid_std[lat_name], lon_name: grid_std[lon_name]}, method='nearest')
                except:
                    ('Standard grid re-indexing not applied for calculating HSIs.')
                    data = data
        else:
            if model!='ERA5':
                print('Standard grid re-indexing not applied for calculating HSIs.')
        
        #Store data in one dataset
        if create==1:
            data_all = data
            create = 0
        else:
            data_all[var_n] = data[var_n]

    return data_all
