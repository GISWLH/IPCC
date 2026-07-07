#This script contains several functions to read data, apply corrections, concatenate data, and remove data after calculation.

import xarray as xr
import os
import sys
import shutil
import feather
import datetime
import cftime
import numpy as np
import time as t_util
import paramiko
import yaml


# Grid description for CDO remapping
#Input:
#  - model: model name (string)
#  - file_name: file name (string)
#  - dir_regr: directory for storing output (string)
#  - variable: variable name (string)
def get_grid_description(model, file_name, dir_regr, variable):
    
    #Create grid description
    os.system("cdo griddes -selvar," + variable + " " + file_name + " > " + dir_regr + 'grid_xy_' + model)
    os.system('cdo -f nc -topo,'+ dir_regr + 'grid_xy_' + model + " " + dir_regr + "Standard_grid_" + model + ".nc")

#Mask with land grid cells (without Antarctica)
#Input:
#  - model: model name (string)
#  - dir_data: Data directory (string)
def get_land_gridcells(model, dir_data='/div/amoc/exhaustion/Heat_Health_Global/Data/'):

    #Read data
    dir_LSM  = dir_data + 'Masks_Heights_Grids/Land_sea_masks/'
    files_LSM = os.listdir(dir_LSM)
    fname_LSM = [file for file in files_LSM if (model in file) and ('sftlf' in file)][0]
    data = xr.open_dataset(dir_LSM + fname_LSM)

    #Select land data and delete Antarctica
    m = data.sftlf.max().values
    land = data.sftlf>0.5*m
    land = land.where(land.lat>-60, False)

    #Create data set
    land = land.to_dataset(name='selection')
    if 'type' in land: land = land.drop('type')

    #Save in file
    file_out = dir_LSM + "Land_without_Antarctica_" + model + ".nc"
    land.to_netcdf(file_out)
    
    
#Define calendars without leap years for reference period and whole period
#Input:
#  - folder_out: folder where output should be stored (string)
#  - y_sta: start year (string)
#  - y_end: end year (string)
#Output:
#  - dates_noleap: Vector with dates for 365-day calendar (cftime vector)
#  - dates_360_day:  Vector with dates for 360-day calendar (cftime vector)
def define_calendar_noleap(folder_out, y_sta='1981', y_end='2100'):
    
    #Create vector with no leap years
    dates_noleap = xr.cftime_range(start=y_sta + '0101', end=y_end + '1231', freq='D', calendar='noleap')

    #Save in files
    DOY    = dates_noleap.dayofyear
    YEARS  = dates_noleap.year
    MONTHS = dates_noleap.month
    np.savetxt(folder_out + y_sta + "-" + y_end + "_dates_DOY_365.csv", DOY, fmt='%i', delimiter=",")
    np.savetxt(folder_out + y_sta + "-" + y_end + "_dates_YEARS_365.csv", YEARS, fmt='%i', delimiter=",")
    np.savetxt(folder_out + y_sta + "-" + y_end + "_dates_MONTHS_365.csv", MONTHS, fmt='%i', delimiter=",")
    
    #Create vector with no leap years
    dates_360_day = xr.cftime_range(start=y_sta + '0101', end=y_end + '1230', freq='D', calendar='360_day')

    #Save in files
    DOY360    = dates_360_day.dayofyear
    YEARS360  = dates_360_day.year
    MONTHS360 = dates_360_day.month
    np.savetxt(folder_out + y_sta + "-" + y_end + "_dates_DOY_360.csv", DOY360, fmt='%i', delimiter=",")
    np.savetxt(folder_out + y_sta + "-" + y_end + "_dates_YEARS_360.csv", YEARS360, fmt='%i', delimiter=",")
    np.savetxt(folder_out + y_sta + "-" + y_end + "_dates_MONTHS_360.csv", MONTHS360, fmt='%i', delimiter=",")    
    
    return(dates_noleap, dates_360_day)


# Merge historical and RCP/SSP data for CMIP5/CMIP6 and create file for reference and for total period
#Input:
#  - model: model name (string)
#  - var_names: Variable names (list of strings)
#  - dir_data: Data directory (string)
#  - SSP: SSP or RCP (string)
#  - member: ensemble member (string)
#  - CMIPvers: CMIP5 or CMIP6 (string)
#Output:
#  - calendar: Calendar of output NetCDF file
def concat_CMIP(model, var_names, dir_data, SSP, member='r1i1p1f1', CMIPvers='CMIP6'):
    
    print("  Merging " + CMIPvers + " files:")
    
    #Create and define folders
    dir_CMIP     = dir_data + CMIPvers + '/' + CMIPvers + '_downloaded/' + model + '/'
    dir_CMIP_sel = dir_data + CMIPvers + '/' + CMIPvers + '_merged/' + model + '_tmp/'
    dir_DOY      = dir_data + CMIPvers + '/' + CMIPvers + '_merged/'
    dir_orog     = '/div/amoc/exhaustion/Heat_Health_Global/Data/Masks_Heights_Grids/Orography/'
    if not os.path.exists(dir_DOY): os.mkdir(dir_DOY)
    if not os.path.exists(dir_CMIP_sel): os.mkdir(dir_CMIP_sel)
    
    # Get (and save) dates of no-leap years
    dates_noleap, dates_360_day = define_calendar_noleap(dir_DOY)
    
    #Loop over all selected variables
    for variab in var_names:
        
        print("  -variable " + variab)

        #Read files
        file_hist = [file for file in os.listdir(dir_CMIP) if (variab + '_' in file) and ('historical_' in file) and ('_1980' in file) and (member in file)]
        file_rcp  = [file for file in os.listdir(dir_CMIP) if (variab + '_' in file) and (SSP + '_' in file) and (member in file)]
        data_hist = xr.open_dataset(dir_CMIP + file_hist[0])
        data_rcp  = xr.open_dataset(dir_CMIP + file_rcp[0])
        
        #Rename variable 'time_bnds' and remove 'height'
        if 'time_bnds' in data_hist: data_hist = data_hist.rename({'time_bnds': 'time_bounds'})
        if 'time_bnds' in data_rcp: data_rcp = data_rcp.rename({'time_bnds': 'time_bounds'})   
        if 'height' in data_hist: data_hist = data_hist.drop('height')
        if 'height' in data_rcp: data_rcp = data_rcp.drop('height')   
        
        #Merge data and select time period
        data_all = xr.concat((data_hist, data_rcp), dim='time')
        data_all = data_all.sel(time=slice('1981', '2100'))
        
        #Read calendar
        data_cal = xr.open_dataset(dir_CMIP + file_hist[0], decode_cf=False)
        calendar = data_cal.time.calendar
        
        #Set correct time 
        if calendar=='360_day':
            data_all['time'] = dates_360_day
        else:
            #Delete 29th of February and add new time
            sel_all = ~((data_all.time.dt.month==2) & (data_all.time.dt.day==29))
            data_all = data_all.isel(time=sel_all)
            data_all['time'] = dates_noleap            

        #Save data in file
        fname_all = variab + "_" + model + "_historical-" + SSP + "_" + member + "_1981-2100.nc"
        if os.path.exists(fname_all): os.remove(fname_all)
        data_all.to_netcdf(dir_CMIP_sel + fname_all)
        
    #Correct pressure
    if 'psl' in var_names:

        print("  -correcting pressure...")

        #Select temperature
        if 'tasmax' in var_names:    T_corr = 'tasmax'
        elif 'tasmin' in var_names:  T_corr = 'tasmin'
        
        #Read data
        data_p = xr.open_dataset(dir_CMIP_sel + "psl_" + model + "_historical-" + SSP + "_" + member + "_1981-2100.nc")
        data_T = xr.open_dataset(dir_CMIP_sel +  T_corr + "_" + model + "_historical-" + SSP + "_" + member + "_1981-2100.nc")
        attrs = data_p['psl'].attrs
        
        #Read orography data for altitude correction of pressure
        data_orog = read_orog_data(dir_orog, model)
        
        #Reindex orography field
        check1 = np.max(np.abs(data_orog.lat.values - data_p.lat.values))
        check2 = np.max(np.abs(data_orog.lon.values - data_p.lon.values))
        if (check1<1e-3) and (check2<1e-3):
            data_orog = data_orog.reindex({'lat': data_p['lat'], 'lon': data_p['lon']}, method='nearest')

        #Correct pressure
        p = corr_press(data_p.psl, data_orog.orog, data_T[T_corr])
        data_p = data_p.assign({'sp': p})
        data_p = data_p.drop('psl')
        data_p['sp'].attrs = attrs

        #Save corrected pressure in file and delete old pressure file
        data_p.to_netcdf(dir_CMIP_sel + "sp_" + model + "_historical-" + SSP + "_" + member + "_1981-2100.nc")
        os.remove(dir_CMIP_sel + "psl_" + model + "_historical-" + SSP + "_" + member + "_1981-2100.nc")
    
    return calendar


#Concatenate CORDEX datasets
#Input:
#  - model: model name (string)
#  - var_names: Variable names (list of strings)
#  - RCP: RCP (string)
#  - dir_CORDEX: Data directory (string)
#  - CORDEX_reg: Name of CORDEX region (string)
#  - time_lim: Time vector for selecting application time (2-element numpy array)
#  - member: ensemble member (string)
#  - extract_version: Get version number from NetCDF file (if avaialable) (bool)
#Output:
#  - calendar: Calendar of output NetCDF file
def concat_CORDEX(model, var_names, RCP, dir_CORDEX, CORDEX_reg, time_lim, member='r1i1p1', extract_version=False):
       
    model_str      = 'CORDEX-' + CORDEX_reg + '_' + model[0] + '_'  + model[1]
    dir_orig       = '/div/amoc/CORDEX/rawfiles/' + CORDEX_reg + '/'
    dir_CORDEX_out = dir_CORDEX + CORDEX_reg + '/' + model_str + '/'  
    dir_DOY        = dir_CORDEX + CORDEX_reg + '/'
    dir_orog       = dir_orig + '/historical/orog/'
    if not os.path.exists(dir_DOY): os.mkdir(dir_DOY)
    if not os.path.exists(dir_CORDEX_out): os.mkdir(dir_CORDEX_out)
        
    #Get time limits
    y_sta = time_lim[0]
    y_end = time_lim[1]

    #Get (and save) dates of no-leap years
    dates_noleap, dates_360_day = define_calendar_noleap(dir_DOY, str(y_sta), str(y_end))

    #Loop over all selected variables
    for variab in var_names:

        print("  -variable " + variab)
        
        #Define variable for file
        if variab=='ps': varout = 'sp'
        else:            varout = variab

        #Filenames for output files
        fname_out1 = dir_CORDEX_out + variab + "_" + model_str + "_historical-" + RCP + "_merged.nc"
        fname_out2 = dir_CORDEX_out + varout + "_" + model_str + "_historical-" + RCP + "_" + member + "_" + str(y_sta) + "-" + str(y_end) + ".nc"
        if os.path.exists(fname_out1): os.remove(fname_out1)
        
        #Folders for historical and RCP data
        dir_hist = dir_orig + 'historical/' + variab + '/'
        dir_rcp  = dir_orig + RCP + '/' + variab + '/'

        #Get historical files
        files_hist = [file for file in os.listdir(dir_hist) if (model[0] + '_' in file) and (model[1] + '_' in file) and (member in file)]
        files_hist = [file for file in files_hist if (int(file.split('-')[-1][0:4]) >= y_sta)]
        files_hist = [dir_hist + file for file in files_hist]
        files_hist = sorted(files_hist)

        #Get RCP files
        files_rcp = [file for file in os.listdir(dir_rcp) if (model[0] + '_' in file) and (model[1] + '_' in file) and (member in file)]
        files_rcp = [file for file in files_rcp if (int(file.split('_')[-1][0:4]) <= y_end)]
        files_rcp = [dir_rcp + file for file in files_rcp]
        files_rcp = sorted(files_rcp)
        
        #Save model version number in file
        if extract_version==True:

            #Loop over historical and RCP files
            files_loop = [files_hist[0], files_rcp[0]]
            scen_loop  = ['historical', RCP]
            for file, scen in zip(files_loop, scen_loop):
                
                #Define outpult folder and file name
                dir_vers = '/div/amoc/exhaustion/Heat_Health_Global/Data/IPCC_AR6/Model_versions/CORDEX-' + CORDEX_reg + '/'
                if not os.path.exists(dir_vers): os.mkdir(dir_vers)
                fname_vers = dir_vers + 'RCMversions_' + model[0] + '_'  + model[1] + '.yml'

                #Read file with versions or create new dictionary
                if os.path.exists(fname_vers):
                    with open(fname_vers, 'r') as file_vers:
                        data_vers = yaml.full_load(file_vers)
                else:
                    data_vers = dict()

                #Add entry to dictionary
                data_tmp = xr.open_dataset(file, decode_times=False)
                if 'rcm_version_id' in data_tmp.attrs:
                    data_vers[variab + '_' + scen] = data_tmp.attrs['rcm_version_id']
                else:
                    data_vers[variab + '_' + scen] = 'NaN'

                #Save in file
                with open(fname_vers, 'w') as file_vers:
                    yaml.dump(data_vers, file_vers)              
        

        #Add 1 January 2006 for ICHEC-EC-EARTH_MPI-CSC-REMO2009
        if (((CORDEX_reg=='AFR-44') and (RCP=='rcp26') and (model[0]=='ICHEC-EC-EARTH') and (model[1]=='MPI-CSC-REMO2009')) or 
            ((CORDEX_reg=='SAM-44') and (model[0]=='MPI-M-MPI-ESM-LR') and (model[1]=='MPI-CSC-REMO2009'))):

            #Read data
            with xr.open_dataset(files_rcp[0], use_cftime=True) as ds:
                data_read = ds.load()
                ds.close()

            #Create filling array
            data_fill = data_read.isel(time=0)
            data_fill['time'] = cftime.DatetimeProlepticGregorian(2006, 1, 1, 12)
            data_fill = data_fill.expand_dims('time')
            data_fill[variab] = (('time', 'rlat', 'rlon'), np.empty(data_fill[variab].shape) *  np.NaN)
            data_fill[variab].attrs = data_read[variab].attrs
            data_fill['time'].attrs = data_read.time.attrs

            #Save to NetCDF
            fname_add = dir_CORDEX_out + 'add_2006_01_01.nc'
            data_fill.to_netcdf(fname_add)

            #Add filename to rcp files
            files_rcp = [fname_add] + files_rcp
                    
        #Add 31 December in some years for MPI-M-MPI-ESM-MR_ICTP-RegCM4-4
        files_del = []
        if ((CORDEX_reg=='EAS-22') and (model[0]=='MPI-M-MPI-ESM-MR') and (model[1]=='ICTP-RegCM4-4')):

            #Select files with missing 31 December
            files_extend = [file for file in files_rcp if '1230.nc' in file]
            
            #Loop over files
            for file_sel in files_extend:
                
                #Read data
                with xr.open_dataset(file_sel, use_cftime=True) as ds:
                    data_read = ds.load()
                    ds.close()

                #Create filling array
                year_fill = int(file_sel[-11:-7])
                data_fill = data_read.isel(time=0)
                data_fill['time'] = cftime.DatetimeProlepticGregorian(year_fill, 12, 31, 12)
                data_fill = data_fill.expand_dims('time')
                data_fill[variab] = (('time', 'y', 'x'), np.empty(data_fill[variab].shape) *  np.NaN)
                data_fill[variab].attrs = data_read[variab].attrs
                data_fill['time'].attrs = data_read.time.attrs

                #Save to NetCDF
                fname_add = file_sel[0:-20] + str(year_fill) + '1231-' + str(year_fill) + '1231.nc'
                data_fill.to_netcdf(fname_add) 

                #Add filename to rcp files
                files_rcp = [fname_add] + files_rcp
                files_del.append(fname_add)

            #Sort files in correct order
            files_rcp = sorted(files_rcp)

        #Delete November/December 2005 in RCP8.5 files for this model combination
        if (CORDEX_reg=='EUR-11')  and (model[1]=='ICTP-RegCM4-6'):
            files_rcp = [file for file in files_rcp if '2005' not in file]        
        if (CORDEX_reg=='CAM-22') and (model[1]=='ICTP-RegCM4-7'):
            files_rcp = [file for file in files_rcp if '2005' not in file]              

        #Correct grid of historical files to match RCP files for UCAN-WRF341I
        if (CORDEX_reg=='SAM-44') and (model[1]=='UCAN-WRF341I'):
            
            #Get correct grid description
            file_grid  = files_rcp[0]
            fname_grid = dir_CORDEX_out + 'grid_xy_UCAN-WRF341I_corrected'
            os.system("cdo griddes -selvar," + variab + " " + file_grid + " > " + fname_grid)
            
            #Loop over historical files
            files_corr = []
            files_del  = []
            for file in files_hist:
                
                #Remap to RCP grid
                f_out = dir_CORDEX_out + file.split('/')[-1]
                os.system('cdo remapbil,' + fname_grid + ' ' + file + " " + f_out)
                files_corr.append(f_out)
                files_del.append(f_out)
                
            #Put corrected file names in list of historical files and remove grid file
            files_hist = files_corr
            os.remove(fname_grid)
            
        #Merge files to a single file
        if len(files_hist + files_rcp)>900:

            #Split files into 2 batches
            files_hist_rcp = files_hist + files_rcp
            files_all1 = " ".join(files_hist_rcp[0:900])
            files_all2 = " ".join(files_hist_rcp[900::])
            fname_merge1 = fname_out1[0:-3] + '_batch1.nc'
            fname_merge2 = fname_out1[0:-3] + '_batch2.nc'

            #Merge with CDO
            os.system("cdo mergetime " + files_all1 + " " + fname_merge1)
            os.system("cdo mergetime " + files_all2 + " " + fname_merge2)
            os.system("cdo mergetime " + fname_merge1 + " " + fname_merge2 + " " + fname_out1)
            os.remove(fname_merge1)
            os.remove(fname_merge2)

        else:

            #Join to one string for merging
            files_all = " ".join(files_hist + files_rcp)

            #Merge with CDO
            os.system("cdo mergetime " + files_all + " " + fname_out1)

        #Delete additional files (if they exist)
        for file_del in files_del:
            os.remove(file_del)
        
        #Delete additional file
        if (CORDEX_reg=='AFR-44') and (RCP=='rcp26') and (model[0]=='ICHEC-EC-EARTH') and (model[1]=='MPI-CSC-REMO2009'):
            os.remove(fname_add)

        #Add year 2100 where it is missing
        check_EAS_NorESM_RegCM4 = ('NorESM1-M' in model[0]) and (model[1]=='ICTP-RegCM4-4') and (CORDEX_reg=='EAS-22')
        if (((model[0]=='MOHC-HadGEM2-ES') and (y_end>=2099)) or
            ((CORDEX_reg=='AUS-44') and (model[0]=='CCCma-CanESM2') and (y_end>=2099)) or 
            ((CORDEX_reg=='AUS-22') and (model[1]=='ICTP-RegCM4-7') and (y_end>=2099)) or 
            ((CORDEX_reg=='SAM-22') and (model[1]=='ICTP-RegCM4-7') and (y_end>=2099)) or
            ((CORDEX_reg=='CAM-22') and (model[1]=='ICTP-RegCM4-7') and (y_end>=2099)) or
            ((CORDEX_reg=='WAS-22') and (model[1]=='ICTP-RegCM4-7') and (y_end>=2099)) or
            ((CORDEX_reg=='SEA-22') and (model[1]=='ICTP-RegCM4-7') and (y_end>=2099)) or
            ((CORDEX_reg=='AFR-22') and (model[1]=='ICTP-RegCM4-7') and (y_end>=2099)) or
            ((CORDEX_reg=='NAM-22') and (model[0]=='NOAA-GFDL-GFDL-ESM2M') and (model[1]=='NCAR-WRF') and (y_end>=2099)) or
            ((CORDEX_reg=='NAM-22') and (model[0]=='NOAA-GFDL-GFDL-ESM2M') and (model[1]=='ISU-RegCM4') and (y_end>=2099)) or
            ((CORDEX_reg=='WAS-44') and (model[1]=='IITM-RegCM4-4') and (model[0]!='CNRM-CERFACS-CNRM-CM5') and (y_end>=2099)) or
            ((CORDEX_reg=='WAS-22') and (model[1]=='CLMcom-ETH-COSMO-crCLIM-v1-1') and (y_end>=2099)) or
            ((CORDEX_reg=='EAS-44') and (model[0]=='MPI-M-MPI-ESM-LR') and (y_end>=2099)) or
            ((CORDEX_reg=='EAS-22') and (model[0]=='MPI-M-MPI-ESM-MR') and (model[1]=='ICTP-RegCM4-4') and (y_end>=2099)) or
            ((CORDEX_reg=='EAS-22') and ('NorESM1-M' in model[0]) and (model[1]=='ICTP-RegCM4-4') and (RCP=='rcp26') and (y_end>=2099)) or
            (check_EAS_NorESM_RegCM4 and (RCP=='rcp85') and (variab=='huss') and (y_end>=2099))):

            fname_add    = dir_CORDEX + CORDEX_reg + '/' + model_str + '/' + variab + '_add_2100_data.nc'
            fname_add2   = dir_CORDEX + CORDEX_reg + '/' + model_str + '/' + variab + '_add_2100_data_corr.nc'
            fname_merged = dir_CORDEX + CORDEX_reg + '/' + model_str + '/' + variab + '_data_merged_all.nc'

            #Select two years
            os.system("cdo selyear,2095/2096 " + fname_out1 + " " + fname_add)

            #Read data
            data_help = xr.open_dataset(fname_out1, decode_cf=False)
            data_orig = xr.open_dataset(fname_out1)

            with xr.open_dataset(fname_add) as ds:
                data_add = ds.load()
                ds.close()    

            #Create time vector
            calendar = data_help.time.calendar
            times    = data_help.time[-1].values + 1
            units    = data_help.time.units
            t_sta    = cftime.num2date(times, units, calendar=calendar)
            t_len    = len(data_add.time)
            
            #Change datetime class if necessary
            if isinstance(t_sta, datetime.datetime) and calendar in ['standard', 'gregorian', 'proleptic_gregorian']:
                t_sta = cftime.DatetimeGregorian(t_sta.year, t_sta.month, t_sta.day, t_sta.hour)
                
            dates_add = xr.cftime_range(start=t_sta, periods=t_len, freq='D', calendar=data_help.time.calendar)

            #Add correct time bounds
            if 'time_bnds' in data_orig:    var_bnds = 'time_bnds'
            if 'time_bounds' in data_orig:  var_bnds = 'time_bounds'
            tbnds_fill = np.arange(1, len(dates_add) + 1)
            tbnds_fill = np.repeat(np.expand_dims(tbnds_fill, 1), 2, axis=1)
            tbnds_fill = tbnds_fill + data_help[var_bnds][-1,:].values
            tbnds_fill[:,0] = tbnds_fill[:,0] - 1

            #Set time vector to data
            data_add['time'] = dates_add
            data_add[var_bnds] = (('time', 'bnds'), tbnds_fill)

            #Set data to NaN
            data_add[variab] = data_add[variab] * np.NaN

            #Get right lat & lon names
            if 'rlat' in data_add: lat_name, lon_name = 'rlat', 'rlon'
            if 'x' in data_add:    lat_name, lon_name = 'x', 'y'

            #Set attributes, longitude and latitude
            data_add.time.attrs = data_orig.time.attrs
            data_add[variab].attrs = data_orig[variab].attrs
            if 'latitude' in data_orig.coords:
                data_add['latitude']  = data_orig.latitude
                data_add['longitude'] = data_orig.longitude                
            else:
                data_add['lat'] = data_orig.lat
                data_add['lon'] = data_orig.lon
            data_add[lat_name] = data_orig[lat_name]
            data_add[lon_name] = data_orig[lon_name]

            #Save in NetCDF
            data_add.to_netcdf(fname_add2)
            data_add.close()

            #Merge all data
            os.system("cdo mergetime " + fname_out1 + " " + fname_add2 + " " + fname_merged)

            #Remove original file and set updated file name
            os.remove(fname_out1)
            os.remove(fname_add)
            os.remove(fname_add2)
            fname_out1 = fname_merged
        
        #Fill missing days for some model combinations
        models_check = ['CCCma-CanESM2', 'CNRM-CERFACS-CNRM-CM5', 'NOAA-GFDL-GFDL-ESM2M']
        check_EAS_NorESM_RegCM4 = ('NorESM1-M' in model[0]) and (model[1]=='ICTP-RegCM4-4') and (CORDEX_reg=='EAS-22')
        if (((CORDEX_reg=='NAM-22') and (model[1]=='OURANOS-CRCM5') and (model[0] in models_check) and (variab=='tasmax')) or
            ((CORDEX_reg=='NAM-22') and (model[1]=='UQAM-CRCM5')) or
            ((CORDEX_reg=='NAM-22') and (model[0]=='MPI-M-MPI-ESM-LR') and (model[1]=='NCAR-RegCM4')) or
            ((CORDEX_reg=='NAM-44') and (model[1]=='UQAM-CRCM5')) or
            ((CORDEX_reg=='AFR-22') and (model[1]=='ICTP-RegCM4-7') and (variab=='huss')) or
            ((CORDEX_reg=='EUR-11') and (model[0]=='MPI-M-MPI-ESM-LR') and (model[1]=='ICTP-RegCM4-6')) or
            ((CORDEX_reg=='EAS-22') and (model[0]=='MPI-M-MPI-ESM-MR') and (model[1]=='ICTP-RegCM4-4')) or
            ((CORDEX_reg=='WAS-44') and (model[0]=='CNRM-CERFACS-CNRM-CM5') and (model[1]=='IITM-RegCM4-4')) or
            ((CORDEX_reg=='CAM-22') and ('HadGEM' in model[0]) and (model[1]=='ICTP-RegCM4-7') and (RCP=='rcp26') and (variab=='huss')) or
            ((CORDEX_reg=='SEA-22') and (model[0]=='ICHEC-EC-EARTH') and (model[1]=='ICTP-RegCM4-3')) or
            ((CORDEX_reg=='SEA-22') and (model[0]=='NOAA-GFDL-GFDL-ESM2M') and (model[1]=='ICTP-RegCM4-3')) or
            ((CORDEX_reg=='SEA-22') and ('HadGEM' in model[0]) and ('RegCM' in model[1]) and (RCP=='rcp85') and (variab=='huss')) or
            ((CORDEX_reg=='SEA-22') and ('NCC-NorESM' in model[0]) and ('RegCM' in model[1]) and (RCP=='rcp26') and (variab=='huss')) or
            (check_EAS_NorESM_RegCM4 and (RCP=='rcp85') and (variab in ['tasmax', 'ps']))):

            #Open datasets (without/with decoding times)
            data     = xr.open_dataset(fname_out1, decode_times=False)
            data_cal = xr.open_dataset(fname_out1)

            #Select how many days should be filled
            if (CORDEX_reg=='CAM-22') and ('HadGEM' in model[0]) and (model[1]=='ICTP-RegCM4-7') and (RCP=='rcp26') and (variab=='huss'):
                date_start = ['2059-04-30', '2059-05-30']
                N = [1, 1]
            elif (CORDEX_reg=='EUR-11') and (model[0]=='MPI-M-MPI-ESM-LR') and (model[1]=='ICTP-RegCM4-6') and (RCP=='rcp85'):
                date_start = [data_cal.time[-1]]
                N = [31]
            elif (CORDEX_reg=='SEA-22') and ('GFDL' in model[0]) and (model[1]=='ICTP-RegCM4-3') and (RCP=='rcp85') and (variab=='huss'):
                date_start = ['2040-11-30', '2096-03-31', data_cal.time[-1]]
                N = [31, 30, 31]
            elif (CORDEX_reg=='SEA-22') and (model[0]=='ICHEC-EC-EARTH') and (model[1]=='ICTP-RegCM4-3'):
                date_start = [data_cal.time[-1]]
                N = [31 + 30 + 31 + 31 + 30 + 31 + 30 + 31] #May-Dec
            elif (CORDEX_reg=='SEA-22') and (model[0]=='NOAA-GFDL-GFDL-ESM2M') and (model[1]=='ICTP-RegCM4-3'):
                date_start = [data_cal.time[-1]]
                N = [31]         
            elif (CORDEX_reg=='SEA-22') and ('HadGEM' in model[0]) and ('RegCM' in model[1]) and (RCP=='rcp85') and (variab=='huss'):
                date_start = ['2009-05-30']
                N = [30]      
            elif (CORDEX_reg=='SEA-22') and ('NCC-NorESM' in model[0]) and ('RegCM' in model[1]) and (RCP=='rcp26') and (variab=='huss'):
                date_start = ['2098-03-31']
                N = [1]   
            elif (CORDEX_reg=='AFR-22') and (model[0]=='MOHC-HadGEM2-ES') and (model[1]=='ICTP-RegCM4-7') and (RCP=='rcp26'):
                date_start = ['2034-02-30', '2034-03-30', '2034-04-30', '2034-05-30', '2034-06-30', '2034-07-30', '2034-08-30',
                              '2034-09-30', '2034-10-30', '2034-11-30']
                N = np.ones(len(date_start), dtype=int)
            elif (CORDEX_reg=='AFR-22') and (model[0]=='MPI-M-MPI-ESM-MR') and (model[1]=='ICTP-RegCM4-7') and (RCP=='rcp26'):
                date_start = ['2012-12-31', '2013-01-31', '2013-02-28', '2013-03-31', '2013-04-30', '2013-05-31', '2013-06-30', 
                              '2013-07-31']
                N = np.ones(len(date_start), dtype=int)
            elif (CORDEX_reg=='AFR-22') and (model[0]=='MOHC-HadGEM2-ES') and (model[1]=='ICTP-RegCM4-7') and (RCP=='rcp85'):
                date_start = ['2033-10-30', '2033-11-30', '2033-12-30', '2034-01-30', '2034-02-30', '2034-03-30', '2034-04-30', 
                              '2034-05-30', '2034-06-30']
                N = np.ones(len(date_start), dtype=int)
            elif (CORDEX_reg=='AFR-22') and (model[0]=='MPI-M-MPI-ESM-MR') and (model[1]=='ICTP-RegCM4-7') and (RCP=='rcp85'):
                date_start = ['2015-01-31', '2015-02-28', '2015-03-31', '2015-04-30', '2015-05-31', '2015-06-30', '2015-07-31', 
                              '2015-08-31', '2015-09-30', '2015-10-31']
                N = np.ones(len(date_start), dtype=int)
            elif (CORDEX_reg=='AFR-22') and (model[0]=='NCC-NorESM1-M') and (model[1]=='ICTP-RegCM4-7') and (RCP=='rcp85'):
                date_start = ['2022-02-28', '2022-03-31', '2022-04-30', '2022-05-31', '2022-06-30', '2022-07-31', '2022-08-31', 
                              '2022-09-30']
                N = np.ones(len(date_start), dtype=int)
            else:
                date_start = [data_cal.time[-1]]
                N = [1]
        
            #Loop over the different time periods to be filled
            ind_coll = []
            for i_time, (date_sta, n_time) in enumerate(zip(date_start, N)):

                ind_time = data_cal.time.values==data_cal.sel(time=date_sta).time.values
                ind_time = [i for i, x in enumerate(ind_time) if x][0]

                #Add one day to last time value in data set
                time_new = data.time[ind_time].data + np.arange(1, n_time+1)

                #Extract data of one time step, replace with new date, and fill with NaNs
                data_fill = data.isel(time=slice(0, n_time))
                data_fill = data_fill.reindex({"time": time_new})
                data_fill = data_fill.ffill("time")

                #Check if filling worked
                if np.sum(~np.isnan(data_fill[variab]))!=0:
                    sys.exit('Filling with NaNs did not succeed!')

                #Save time in list
                ind_coll.append(ind_time)

                if i_time==0:
                    data_part = data.isel(time=slice(0, ind_time + 1))
                    if len(date_start)>1:
                        data_corr = xr.concat((data_part, data_fill), dim='time')
                    else:
                        data_part2 = data.isel(time=slice(ind_time + 1, None))
                        data_corr  = xr.concat((data_part, data_fill, data_part2), dim='time')
                elif i_time!=len(date_start)-1:
                    data_part = data.isel(time=slice(ind_coll[i_time-1] + 1, ind_time + 1))
                    data_corr = xr.concat((data_corr, data_part, data_fill), dim='time')
                else:
                    data_part1 = data.isel(time=slice(ind_coll[i_time-1] + 1, ind_time + 1))
                    data_part2 = data.isel(time=slice(ind_time + n_time, None))
                    data_corr = xr.concat((data_corr, data_part1, data_fill, data_part2), dim='time')    

            #Save in NetCDF
            fname_out_corr = fname_out1[0:-3] + '_v2.nc'
            data_corr.to_netcdf(fname_out_corr)

            #Delete original data and change file name for further processing
            os.remove(fname_out1)
            fname_out1 = fname_out_corr
            
        #Read and select merged data
        data_all = xr.open_dataset(fname_out1, decode_times=False)
        data_all = data_all.assign(time=xr.conventions.decode_cf_variable('time', data_all.time))
        data_all = data_all.sel(time=slice(str(y_sta), str(y_end)))

        #Read calendar
        data_cal = xr.open_dataset(fname_out1, decode_cf=False)
        calendar = data_cal.time.calendar
        
        #Set correct time 
        if calendar=='360_day':
            data_all['time'] = dates_360_day
        else:
            #Delete 29th of February and add new time
            sel_all = ~((data_all.time.dt.month==2) & (data_all.time.dt.day==29))
            data_all = data_all.isel(time=sel_all)
            data_all['time'] = dates_noleap            

        #Correct coordinates
        if (model[0]=='MOHC-HadGEM2-ES') and (model[1]=='ICTP-RegCM4-6'):           
                data_all = data_all.assign_coords({'lat': data_all.lat, 'lon': data_all.lon})
            
        #Convert °C to K
        if (model[0]=='CNRM-CERFACS-CNRM-CM5') and (model[1]=='CNRM-ALADIN53') and ('tasmax' in variab):
            sel_data = data_all.time.dt.year>=2006
            sel_data = sel_data * 273.15
            data_all[variab] = data_all[variab] + sel_data

        #Add rlon if it does not exist as coordinate
        if not 'rlon' in data_all.coords:
            data_all['rlon'] = data_all.lon[0, :]
            data_all.rlon.attrs = []
            data_all.rlon.attrs['axis'] = 'X'
            data_all.rlon.attrs['standard_name'] = 'grid_longitude'
            data_all.rlon.attrs['long_name'] = 'longitude in rotated pole grid'
            data_all.rlon.attrs['units'] = 'degrees'
            
        #Change name ps -> sp
        if variab=='ps':
            data_all = data_all.rename({'ps': 'sp'})

            #Convert from hPa to Pa for models with wrong units
            if (((CORDEX_reg=='WAS-44') and (model[1]=='IITM-RegCM4-4')) or
                ((CORDEX_reg=='SEA-22') and (model[1]=='ICTP-RegCM4-3')) or
                ((CORDEX_reg=='EUR-11') and (model[1]=='CNRM-ALADIN53'))):
                
                data_all = 100 * data_all  # hPa -> Pa
             
            if np.mean(data_all.sp)<90000:
                sys.exit('Units of sp are not correct!')
                           
        #Correct wrong x- and y-values for CNRM-ALADIN53
        if (CORDEX_reg=='EUR-11') and (model[1]=='CNRM-ALADIN53'):
            data_all.x.values[107] = 1337.5
            data_all.y.values[107] = 1337.5
            
        #Save data in file        
        if os.path.exists(fname_out2): os.remove(fname_out2)
        data_all.to_netcdf(fname_out2)

        #Delete merged files
        os.remove(fname_out1)

    #Correct pressure
    if 'psl' in var_names:

        print("  -correcting pressure...")

        #Select temperature
        if 'tasmax' in var_names:    T_corr = 'tasmax'
        elif 'tasmin' in var_names:  T_corr = 'tasmin'
            
        #Read data
        data_p = xr.open_dataset(dir_CORDEX_out + "psl_" + model_str + "_historical-" + RCP + "_" + member + "_" + str(y_sta) + "-" + str(y_end) + ".nc")
        data_T = xr.open_dataset(dir_CORDEX_out + T_corr + "_" + model_str + "_historical-" + RCP + "_" + member + "_" + str(y_sta) + "-" + str(y_end) + ".nc")
        attrs = data_p['psl'].attrs
        
        #Read orography data for altitude correction of pressure
        if CORDEX_reg=='AFR-44':
            fname_orog = [file for file in os.listdir(dir_orog) if (model[1] + '_' in file)]
        else:
            fname_orog = [file for file in os.listdir(dir_orog) if (model[0] + '_' in file) and (model[1] + '_' in file)]
        data_orog = xr.open_dataset(dir_orog + fname_orog[0])
        if 'rlat' in data_p:  lat_name, lon_name = 'rlat', 'rlon'
        if 'x' in data_p:     lat_name, lon_name = 'x', 'y'
            
        #Reindex orography field
        check1 = np.max(np.abs(data_orog[lat_name].values - data_p[lat_name].values))
        check2 = np.max(np.abs(data_orog[lon_name].values - data_p[lon_name].values))
        if (check1<1e-3) and (check2<1e-3):
            data_orog = data_orog.reindex({lat_name: data_p[lat_name], lon_name: data_p[lon_name]}, method='nearest')

        #Correct pressure
        p = corr_press(data_p.psl, data_orog.orog, data_T[T_corr])
        data_p = data_p.assign({'sp': p})
        data_p = data_p.drop('psl')
        data_p['sp'].attrs = attrs

        #Save corrected pressure in file and delete old pressure file
        data_p.to_netcdf(dir_CORDEX_out + "sp_" + model_str + "_historical-" + RCP + "_" + member + "_" + str(y_sta) + "-" + str(y_end) + ".nc")
        os.remove(dir_CORDEX_out + "psl_" + model_str + "_historical-" + RCP + "_" + member + "_" + str(y_sta) + "-" + str(y_end) + ".nc")
            
    return calendar


#Read orography data
def read_orog_data(folder, model):
    
    file_name = [file for file in os.listdir(folder) if (model + '_' in file)]
    
    if len(file_name)==1:
        orog_data = xr.open_dataset(folder + file_name[0])
    else:
        print(file_name)
        sys.exit('Orography file not found or too many orography files!')
#         orog_data = xr.open_dataset(folder + 'orog_fx_EC-Earth3_hist_r1i1p1f2_gr.nc')
    
    return orog_data


#Correct pressure for altitude effect
def corr_press(psl, orog, T):
    
    #Physical constants
    M_air = 28.964/1000 # kg/mol for dry air
    R     = 8.314472 # J K-1 mol-1
    g     = 9.81 # m s-2

    #Apply height correction
    p_corr = psl * np.exp(-M_air * g * orog /(R * T))
    
    return p_corr
    

#Collect all files produced by QDM in R, store them in an xarray and save the file
#Input
#  - folder_files: Folder in which bias corrected files are stored (string)
#  - fname_orig: File name of non-bias corrected heat stress indicator data (string)
#  - fname_out: File name of output file (string)
#  - variab: Name of variable that should be considered (string)
#  - time_ref: Reference period of bias correction (2-element numpy array)
#  - time_app: Application period of bias correction (2-element numpy array)
#  - compress: Compress NetCDF file (bool)
def collect_BC_data(folder_files, fname_orig, fname_out, variab, time_ref=[], time_app=[], compress=True):

    #Set compression level to 2
    comp = dict(zlib=True, complevel=2)

    #Read original (not BC) data
    data_orig = xr.open_dataset(fname_orig)

    #Get lat and lon names
    if 'rlat' in data_orig:       lat_name, lon_name = 'rlat', 'rlon'
    elif 'x' in data_orig:        lat_name, lon_name = 'y', 'x'
    elif 'lat' in data_orig:      lat_name, lon_name = 'lat', 'lon'
    elif 'latitude' in data_orig: lat_name, lon_name = 'latitude', 'longitude'

    #Read time selection data
    fname_time = folder_files + 'Time_selection.feather'
    time_sel = feather.read_dataframe(fname_time)
    time_sel = np.array(time_sel).flatten()
    time_sel = time_sel>0

    #Create empty numpy array
    size = (sum(time_sel), len(data_orig[lat_name]), len(data_orig[lon_name]))
    data_QDM = np.empty(size, dtype=np.float32) * np.NaN

    #Loop over all files
    files = os.listdir(folder_files)
    for file in files:

        #Skip time file
        if file=='Time_selection.feather':
            continue

        #Read data
        df = feather.read_dataframe(folder_files + file)

        #Get lat and lon ID
        lat_id = file.split('_')[2]
        lon_id = file.split('_')[1]
        lat_id = int(lat_id) - 1
        lon_id = int(lon_id) - 1    

        #Save in array
        data_QDM[:, lat_id, lon_id] = np.array(df).flatten()

    #Select time
    data_BC = data_orig.isel(time=time_sel)

    #Set data in xarray
    data_BC[variab] = (('time', lat_name, lon_name), data_QDM)
    data_BC[variab] = data_BC[variab].astype('float32')    

    #Add attributes
    if not time_ref==[]:  data_BC.attrs['Bias adjustment reference period'] = str(time_ref[0]) + '-'  + str(time_ref[1])
    if not time_app==[]:  data_BC.attrs['Bias adjustment application period'] = str(time_app[0]) + '-'  + str(time_app[1])
    data_BC.attrs['Reference dataset'] = 'ERA5'

    #Save to NetCDF
    if compress==True:
        encoding = {var: comp for var in data_BC.data_vars}
        data_BC.to_netcdf(fname_out, encoding=encoding)
    else:
        data_BC.to_netcdf(fname_out)

    #Delete files
    shutil.rmtree(folder_files, ignore_errors=True)
    shutil.rmtree(folder_files, ignore_errors=True)


#Delete directories of heat index calculation
#Input
#  - model: model name (string)
#  - dir_data: folder where data are stored (string)
#  - dir_HIday: folder where heat stress indicators are stored (string)
#  - CMIPvers: CMIP5 or CMIP6 (string)
#  - ref_name: Name of reference dataset for bias correction (string)
#  - dir_add: Additional folder that should be deleted (string)
def remove_directories(model, dir_data, dir_HIday, CMIPvers='CMIP6', ref_name='ERA5', dir_add=''):

    BC_methods1 = ['QDM', 'QM', 'MBCn']
    BC_methods2 = ['', '_QDM_VAR', '_QDM_HI', '_QM_VAR', '_QM_HI', '_MBCn']

    #Remove folder with downloaded CMIP files
    if dir_data!=[]:
        dir_download = dir_data + CMIPvers + '/' + CMIPvers + '_downloaded/' + model + '/'
        shutil.rmtree(dir_download, ignore_errors=True)
    
    #Remove folder with merged CMIP files
    if dir_data!=[]:
        dir_merged = dir_data + CMIPvers + '/' + CMIPvers + '_merged/' + model + '_tmp/'
        shutil.rmtree(dir_merged, ignore_errors=True)

    #Remove folder with bias corrected CMIP data
    if dir_data!=[]:
        for BC_met in BC_methods1:
            dir_biascorr = dir_data + CMIPvers + '/' + CMIPvers + '_bias_corrected/' + model + '_' + BC_met + '/'
            shutil.rmtree(dir_biascorr, ignore_errors=True)

    #Remove folder with regridded data from reference dataset
    if dir_data!=[]:
        dir_ref = dir_data + ref_name + '/' + ref_name +'_regrid/' + model + '_grid/'
        shutil.rmtree(dir_ref, ignore_errors=True)  

    #Remove folder with daily heat indices for CMIP model
    for BC_met in BC_methods2:
        dir_HI = dir_HIday + model + BC_met + '/'
        shutil.rmtree(dir_HI, ignore_errors=True)  

    #Remove folder with daily heat indices from reference dataset
    dir_HI_ref = dir_HIday + ref_name + '_on_' + model + '_grid/'
    shutil.rmtree(dir_HI_ref, ignore_errors=True)

    if dir_add!='':
        shutil.rmtree(dir_add, ignore_errors=True)
    
#Remove CORDEX folders
#Input
#  - dir_CORDEX_reg: folder where CORDEX data are stored (string)
#  - model_str: CORDEX model name (string)
#  - COR_MOD_str: CORDEX name string (string)
#  - dir_data: folder where data are stored (string)
#  - dir_HIday: folder where heat stress indicators are stored (string)
#  - grid_name: name of grid given for regridding (string)
#  - remove_ref: flag for removing reference (bool)
#  - ref_name: Name of reference dataset for bias correction (string)
def remove_directories_CORDEX(dir_CORDEX_reg, model_str, COR_MOD_str, dir_data, dir_HIday, grid_name, remove_ref, ref_name='WFDE5'):
    
    BC_methods = ['', '_QDM_VAR', '_QDM_HI']

    #Remove folder with merged CMIP files
    if dir_CORDEX_reg!=[]:
        dir_merged = dir_CORDEX_reg + COR_MOD_str + '/'
        shutil.rmtree(dir_merged, ignore_errors=True)

    #Remove folder with regridded data from reference dataset
    if (remove_ref==True) and (dir_data!=[]):
        dir_ref = dir_data + ref_name + '/' + ref_name + '_regrid/' + grid_name + '_grid/'
        shutil.rmtree(dir_ref, ignore_errors=True) 

    #Remove folder with daily heat indices for CMIP model
    for BC_met in BC_methods:
        dir_HI = dir_HIday + COR_MOD_str + BC_met + '/'
        shutil.rmtree(dir_HI, ignore_errors=True)

    #Remove folder with daily heat indices from reference dataset
    dir_HI_ref = dir_HIday + ref_name + '_on_' + COR_MOD_str + '_grid/'
    shutil.rmtree(dir_HI_ref, ignore_errors=True)  
    