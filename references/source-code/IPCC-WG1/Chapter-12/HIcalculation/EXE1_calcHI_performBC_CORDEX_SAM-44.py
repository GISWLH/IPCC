# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/HIcalculation/EXE1_calcHI_performBC_CORDEX_SAM-44.ipynb

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
dir_WFDE5   = dir_data + 'WFDE5/'
dir_scripts = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/'
dir_names   = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'
dir_regr    = '/div/amoc/exhaustion/Heat_Health_Global/Data/Masks_Heights_Grids/Regridding/'
dir_GWL     = '/div/amoc/exhaustion/Heat_Health_Global/Data/IPCC_AR6/Warming_levels_CMIP5_CMIP6/warming_levels/cmip5_all_ens/'
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
with open(dir_names + 'Models_CORDEX-SAM-44_RCP26.txt', 'r') as filehandle:
    for line in filehandle:
        all_models['rcp26'].append(eval(line[:-1]))
with open(dir_names + 'Models_CORDEX-SAM-44_RCP85.txt', 'r') as filehandle:
    for line in filehandle:
        all_models['rcp85'].append(eval(line[:-1]))

#Define heat indices, RCPs and BC method
heat_indices = ['HI_NOAA']
RCPs         = ['rcp85', 'rcp26']
BC_methods   = ['_QDM_HI']

#Define variables and RCPs
var_names_ORIG = ['tasmax', 'huss', 'ps']
var_names_CORR = ['tasmax', 'huss', 'sp']

#Define reference period and application periods for BC
time_orig = [1981, 2100]
time_ref  = [1981, 2010]
time_fix  = [[1995, 2014],
             [2041, 2060], 
             [2081, 2100]]

#Read warming levels
fname = dir_GWL + 'cmip5_warming_levels_all_ens_1850_1900_no_bounds_check.yml'
with open(fname, 'r') as file:
    GWL_data = yaml.safe_load(file)

#Define warming levels
GWL_levels = ['15', '20', '30', '40']

#Use all grid cells (also ocean) if false
mask_land = False

#CORDEX region and directories
CORDEX_reg = 'SAM-44'
CORDEX_str = 'CORDEX-' + CORDEX_reg
dir_CORDEX_files = '/div/amoc/CORDEX/rawfiles/' + CORDEX_reg + '/'
dir_LSM_in       = dir_CORDEX_files + 'historical/sftlf/'
dir_CORDEX_reg   = dir_data + CORDEX_reg + '/'

#Define regrid name
regrid_name = CORDEX_reg + '_rlat-stand'

# %% cell 8
#Define model string
model = ['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'rlat-stand']
COR_MOD_str = CORDEX_str + '_' + model[0] + '_' + model[1]

#Create grid description
dir_CORDEX_orig = dir_CORDEX_files + '/historical/tasmax/'
file_grid = dir_CORDEX_orig + [file for file in os.listdir(dir_CORDEX_orig) if model[0] in file and model[1] in file][0]
os.system("cdo griddes -selvar,tasmax " + file_grid + " > " + dir_regr + 'grid_xy_' + COR_MOD_str)

#Regrid WFDE5 data to model grid
rg_WFDE5.regrid_HSIs_WFDE5_to_CORDEX(COR_MOD_str, heat_indices, dir_WFDE5, regrid_name, 'bil', time_ref[0], time_ref[1])

# %% cell 10
#Loop over RCPs
for RCP in RCPs:

    #Select models
    models = all_models[RCP]

    #Loop over models
    for model in models:
        
        #Get all necessary strings
        model_str = model[0] + '_' + model[1]
        member    = model[2]
        COR_MOD_str = CORDEX_str + '_' + model_str
        BC_str      = CORDEX_str + '_' + model[1]
        time_str     = str(time_orig[0]) + '-' + str(time_orig[1])
        time_str_ref = str(time_ref[0]) + '-' + str(time_ref[1])
        
        print(model_str)
        
        #Get name of CMIP5 driving model
        if ('CNRM-CERFAC' in model[0]) or ('CSIRO-QCCCE' in model[0]) or ('MPI-M' in model[0]) or ('NOAA-GFDL' in model[0]) or ('CSIRO-BOM' in model[0]):
            mod_CMIP5 = '-'.join(model[0].split('-')[2:])
        else:
            mod_CMIP5 = '-'.join(model[0].split('-')[1:])

        #Define and create folders
        dir_WFDE5_out  = dir_WFDE5 + 'WFDE5_regrid/' + regrid_name + '_grid/'
        dir_CORDEX_in  = dir_CORDEX_reg + COR_MOD_str + '/'
        dir_CORDEX_out = dir_HIday + COR_MOD_str + '/'
        dir_CORDEX_QDM = dir_HIday + COR_MOD_str + '_QDM_HI/'
        if not os.path.exists(dir_CORDEX_out):  os.mkdir(dir_CORDEX_out)
        if not os.path.exists(dir_CORDEX_QDM):  os.mkdir(dir_CORDEX_QDM)

        #Define year vectors for subsetting heat index calculation
        vec_orig, dyear_orig = np.arange(time_orig[0], time_orig[1], 10), 10
        vec_QDM,  dyear_QDM  = np.arange(1991, 2090, 10), 10

        
        ########### PREPARE DATA ###########

        #Copy and concatenated data
        calendar = my_fun.concat_CORDEX(model, var_names_ORIG, RCP, dir_data, CORDEX_reg, time_orig, member, extract_version=True)
        if '360' in calendar:  DOYs = 360
        else:                  DOYs = 365
            
        #Create grid description and standard grid NetCDF file
        file_grid = [file for file in os.listdir(dir_CORDEX_in) if 'tasmax_' in file]
        file_grid = dir_CORDEX_in + file_grid[0]
        os.system("cdo griddes -selvar,tasmax " + file_grid + " > " + dir_regr + 'grid_xy_' + COR_MOD_str)
        os.system('cdo -f nc -topo,'+ dir_regr + 'grid_xy_' + COR_MOD_str + " " + dir_regr + "Standard_grid_" + COR_MOD_str + ".nc")

        #Read time periods when certain global warming levels (GWL) are reached
        time_GWL = []
        for level in GWL_levels:
            data_level = GWL_data['warming_level_' + level]
            entry_sel = [entry for entry in data_level if entry['model']==mod_CMIP5 and entry['exp']==RCP and entry['ensemble']==member]
            if len(entry_sel)==1:
                time_GWL.append([entry_sel[0]['start_year'], entry_sel[0]['end_year']])
            else:
                print('Level in ' + mod_CMIP5 + ' for ' + str(int(level)/10) + ' K not available')
        
        #Define all time slices (fixed times and GWL times)
        time_app = time_fix + time_GWL
        
        #Loop over heat indices
        for heat_ind in heat_indices:
            
            #Calculate HSI for CORDEX data
            getHI.GET_heat_indices_v2(COR_MOD_str, RCP, member, heat_ind, dir_CORDEX_in, dir_CORDEX_out, vec_orig, dyear_orig)
            
            #Loop over application time periods
            for time_sel in time_app:
                
                #String for application time
                time_app_str = str(time_sel[0]) + '-' + str(time_sel[1])
                
                #Define files and folders for output
                fname_OBS = dir_WFDE5_out + heat_ind + '_WFDE5_' + time_str_ref + '.nc'
                fname_MOD = dir_CORDEX_out + heat_ind + '_' + COR_MOD_str + '_' + RCP + '_' + member + '_' + time_str + '.nc'
                fname_out = dir_CORDEX_QDM + heat_ind + '_' + COR_MOD_str + '_' + RCP + '_' + member + '_' + time_app_str + '.nc'
                dir_QDM_files = dir_CORDEX_QDM + 'Files_' + time_app_str + '/'
                if not os.path.exists(dir_QDM_files): os.mkdir(dir_QDM_files)

                #Perform quantile mapping
                t_start = t_util.time()
                waldo = r.quant_delta_map_vTimeSlices(BC_str, fname_OBS, fname_MOD, dir_data, dir_QDM_files, heat_ind, time_ref, time_sel, time_orig, DOYs, mask_land)
                my_fun.collect_BC_data(dir_QDM_files, fname_MOD, fname_out, heat_ind, time_ref, time_sel)
                
                #Print time
                t_stop = t_util.time()
                print("Time for BC: " + str(t_stop - t_start))
                
                #Calculate threshold exceedance
                getMEAN_THRES.calc_thresh_IPCC(model_str, RCP, dir_HIday, dir_save, heat_ind, BC_methods, [time_sel], member, CORDEX_str)
       
        #Remove all temporary model data on amoc
        my_fun.remove_directories_CORDEX(dir_CORDEX_reg, model_str, COR_MOD_str, dir_data, dir_HIday, regrid_name, False)

#Remove WFDE5 data
my_fun.remove_directories_CORDEX(dir_CORDEX_reg, model_str, COR_MOD_str, dir_data, dir_HIday, regrid_name, True)
