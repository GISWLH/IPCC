# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/HIcalculation/EXE1_calcHI_performBC_CMIP5.ipynb

# %% cell 2
import os
import sys
import rpy2.robjects as ro
import xarray as xr
import time as t_util
import numpy as np
import yaml

#My functions
sys.path.insert(0,'/div/amoc/exhaustion/Heat_Health_Global/Scripts/functions_Py/')
import my_functions as my_fun
import regrid_WFDE5 as rg_WFDE5
import GET_heat_indices_v2 as getHI
import GET_HI_average_thresh_exeedance as getMEAN_THRES

# %% cell 4
dir_data    = '/div/amoc/archive/tmp_clemens/'
dir_CMIP    = '/div/amoc/archive/tmp_clemens/CMIP5/'
dir_WFDE5   = dir_data + 'WFDE5/'
dir_scripts = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/'
dir_names   = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'
dir_regr    = '/div/amoc/exhaustion/Heat_Health_Global/Data/Masks_Heights_Grids/Regridding/'
dir_indic   = '/div/amoc/exhaustion/Heat_Health_Global/Data/Heat_Indices/'
dir_GWL     = '/div/amoc/exhaustion/Heat_Health_Global/Data/IPCC_AR6/Warming_levels_CMIP5_CMIP6/warming_levels/cmip5/'
dir_HIday   = '/div/amoc/exhaustion/Heat_Health_Global/Data/Heat_Indices/Heat_indices_daily/'
dir_save    = '/div/amoc/exhaustion/Heat_Health_Global/Data/IPCC_AR6/'

# %% cell 6
#Source R functions
r = ro.r
r.source(dir_scripts + 'functions_R/quant_delta_map_vTimeSlices.r')

#Define models and RCPs which should be used
all_models = dict()
all_models['rcp85'] = []
all_models['rcp26'] = []
with open(dir_names + 'Models_CMIP5_RCP26.txt', 'r') as filehandle:
    for line in filehandle:
        all_models['rcp26'].append(line[:-1])
with open(dir_names + 'Models_CMIP5_RCP85.txt', 'r') as filehandle:
    for line in filehandle:
        all_models['rcp85'].append(line[:-1])

#Define heat indices, RCPs and BC method
heat_indices = ['HI_NOAA']
RCPs         = ['rcp85', 'rcp26']
BC_methods   = ['_QDM_HI']

#Define variables
var_names_ORIG = ['tasmax', 'huss', 'psl']
var_names_CORR = ['tasmax', 'huss', 'sp']

#Define periods for downloading data
time_orig = [1981, 2100]
time_per  = [[1980, 2014], [2015, 2100]]
sel_time  = ['>1980', '<2100']

#Define reference period and application periods for BC
time_ref = [1981, 2010]
time_fix = [[1995, 2014],
            [2041, 2060], 
            [2081, 2100]]

#Read warming levels
fname = dir_GWL + 'cmip5_warming_levels_one_ens_1850_1900_no_bounds_check.yml'
with open(fname, 'r') as file:
    GWL_data = yaml.safe_load(file)

#Define warming levels
GWL_levels = ['15', '20', '30', '40']
    
#Define CMIP version
CMIPvers = 'CMIP5'

#Use all grid cells (also ocean) if false
mask_land = False

#Set if model version should be extracted and where it should be stored
extract_version = True
dir_vers = '/div/amoc/exhaustion/Heat_Health_Global/Data/IPCC_AR6/Model_versions/CMIP5/'

# %% cell 8
#Loop over RCPs
for RCP in RCPs:
    
    #Define scenarios
    scenarios = ['historical', RCP]
    models = all_models[RCP]

    #Loop over models
    for model in models:

        print(model)     
            
        #Define and create folders
        dir_WFDE5_out = dir_WFDE5 + 'WFDE5_regrid/' + model + '_grid/'
        dir_CMIP_in  = dir_CMIP + CMIPvers + '_merged/' + model + '_tmp/'
        dir_CMIP_out = dir_HIday + model + '/'
        if not os.path.exists(dir_CMIP_out):      os.mkdir(dir_CMIP_out)
        if not os.path.exists(dir_WFDE5_out):  os.mkdir(dir_WFDE5_out)

        #Define year vectors for subsetting heat index calculation
        vec_orig, dyear_orig = np.arange(time_orig[0], time_orig[1], 10), 10
        vec_QDM,  dyear_QDM  = np.arange(1991, 2090, 10), 10

        
        ########### PREPARE DATA ###########
        
        #Download data
        member = download_data.get_CMIP5(model, RCP, dir_CMIP, extract_version, dir_vers)

        #Prepare grid file, and land grid cells
        dir_regr_in  = dir_data + CMIPvers + '/' + CMIPvers + '_downloaded/' + model + '/'
        file_grid = [file for file in os.listdir(dir_regr_in) if 'tasmax_' in file]
        file_grid = dir_regr_in + file_grid[0]
        my_fun.get_grid_description(model, file_grid, dir_regr, 'tasmax')
        my_fun.get_land_gridcells(model)

        #Merge downloaded CMIP files
        calendar = my_fun.concat_CMIP(model, var_names_ORIG, dir_data, RCP, member, CMIPvers)
        if '360' in calendar:  DOYs = 360
        else:                  DOYs = 365

        #Regrid WFDE5 data do model grid
        rg_WFDE5.regrid_HSIs_WFDE5_to_CMIP(model, heat_indices, dir_WFDE5, dir_WFDE5_out, 'WFDE5', time_ref[0], time_ref[1])
        
        #Read time periods when certain global warming levels (GWL) are reached
        time_GWL = []
        for level in GWL_levels:
            data_level = GWL_data['warming_level_' + level]
            entry_sel = [entry for entry in data_level if entry['model']==model and entry['exp']==RCP and entry['ensemble']==member]
            if len(entry_sel)==1:
                time_GWL.append([entry_sel[0]['start_year'], entry_sel[0]['end_year']])
            else:
                print('Level in ' + model + ' for ' + str(int(level)/10) + ' K not available')
        
        #Define all time slices (fixed times and GWL times)
        time_app = time_fix + time_GWL
        
        
        ########### CALCULATE HSIs AND PERFORM BIAS CORRECTION ###########
        
        #Loop over heat indices
        for heat_ind in heat_indices:
            
            #Calculate heat indices for original CMIP data, regridded WFDE5 data, and bias corrected CMIP data
            getHI.GET_heat_indices_v2(model, RCP, member, heat_ind, dir_CMIP_in, dir_CMIP_out, vec_orig, dyear_orig)
            
            #Loop over application time periods
            for time_sel in time_app:
                
                #String for application time
                time_app_str = str(time_sel[0]) + '-' + str(time_sel[1])

                #Define files and folders for output
                dir_MOD = dir_indic + 'Heat_indices_daily/' + model + '/'
                dir_out = dir_indic + 'Heat_indices_daily/' + model + '_QDM_HI/'
                dir_QDM_files = dir_out + 'Files_' + time_app_str + '/'
                if not os.path.exists(dir_out): os.mkdir(dir_out)
                if not os.path.exists(dir_QDM_files): os.mkdir(dir_QDM_files)
                fname_OBS = dir_WFDE5_out + heat_ind + "_WFDE5_" + str(time_ref[0]) + "-" + str(time_ref[1]) + ".nc"
                fname_MOD = dir_MOD + heat_ind + "_" + model + "_" + RCP + "_" + member + "_" + str(time_orig[0]) + "-" + str(time_orig[1]) + ".nc"
                fname_out = dir_out + heat_ind + "_" + model + "_" + RCP + "_" + member + "_" + str(time_sel[0]) + "-" + str(time_sel[1]) + ".nc"

                #Perform quantile mapping
                t_start = t_util.time()
                waldo = r.quant_delta_map_vTimeSlices(model, fname_OBS, fname_MOD, dir_data, dir_QDM_files, heat_ind, time_ref, time_sel, time_orig, DOYs, mask_land)
                my_fun.collect_BC_data(dir_QDM_files, fname_MOD, fname_out, heat_ind, time_ref, time_sel)
                
                #Print time
                t_stop = t_util.time()
                print("Time for BC: " + str(t_stop - t_start))
                
                #Calculate threshold exceedance
                getMEAN_THRES.calc_thresh_IPCC(model, RCP, dir_HIday, dir_save, heat_ind, BC_methods, [time_sel], member, CMIPvers)

        #Remove all temporary model data on amoc
        my_fun.remove_directories(model, dir_data, dir_HIday, CMIPvers, 'WFDE5')
