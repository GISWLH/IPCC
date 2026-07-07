# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/HIcalculation/EXE2_Prepare_data_for_IPCC.ipynb

# %% cell 2
import os
import sys
import numpy as np
import xarray as xr
import yaml

# %% cell 4
dir_data  = '/div/amoc/exhaustion/Heat_Health_Global/Data/IPCC_AR6/Threshold_exceedance/'
dir_out   = '/div/amoc/exhaustion/Heat_Health_Global/Data/IPCC_AR6/Threshold_exceedance/IPCC_ready/'
dir_GWL   = '/div/amoc/exhaustion/Heat_Health_Global/Data/IPCC_AR6/Warming_levels_CMIP5_CMIP6/warming_levels/'
dir_names = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

# %% cell 6
#Select CMIP version (CMIP5 or CMIP6)
CMIPvers = 'CMIP5'
#CMIPvers = 'CMIP6'


if CMIPvers=='CMIP5':
    scen1 = 'rcp85'
    scen2 = 'rcp26'
elif CMIPvers=='CMIP6':
    scen1 = 'ssp585'
    scen2 = 'ssp126'

#Define models and RCPs which should be used
all_models = dict()
all_models[scen1] = []
all_models[scen2] = []
with open(dir_names + 'Models_' + CMIPvers + '_' + scen1.upper() + '.txt', 'r') as filehandle:
    for line in filehandle:
        all_models[scen1].append(line[:-1])
with open(dir_names + 'Models_' + CMIPvers + '_' + scen2.upper() + '.txt', 'r') as filehandle:
    for line in filehandle:
        all_models[scen2].append(line[:-1])

#Define heat indices and scenarios
HSI     = 'HI_NOAA' #'WBGTindoor'
HSI_out = 'HI' #'WBGTindoor'

scenarios = [scen1, scen2]

#Define reference period and application periods for BC
time_fix = [[1995, 2014],
            [2041, 2060], 
            [2081, 2100]]

#Read warming levels
if CMIPvers=='CMIP5':
    fname = dir_GWL + CMIPvers.lower() + '_all_ens/' + CMIPvers.lower() + '_warming_levels_all_ens_1850_1900_no_bounds_check.yml'
elif CMIPvers=='CMIP6':
    fname = dir_GWL + CMIPvers.lower() + '_all_ens/' + CMIPvers.lower() + '_warming_levels_all_ens_1850_1900.yml'
    
with open(fname, 'r') as file:
    GWL_data = yaml.safe_load(file)

#Define warming levels
GWL_levels = ['15', '20', '30', '40']  

#Define thresholds
if HSI=='WBGTindoor':
    thresholds = [31, 33, 35]
elif HSI=='HI_NOAA':
    thresholds = [27, 32, 41]
elif HSI in ['TXmean', 'tasmax']:
    thresholds = [35]
else:
    sys.exit('No thresholds defined for this HSI. Please define them first!')

# %% cell 8
print("*********** Preparing " + HSI + " for " + CMIPvers + " ***********")

#Loop over scenarios
for scen in scenarios:
    
    #Get model list
    models = all_models[scen]

    #Loop over models
    for i, model in enumerate(models):

        print('Run ' + str(i+1) + ' of ' + str(len(models)), end=': ')
        print(model)

        #Select ensemble member
        if CMIPvers=='CMIP5':
            
            member = 'r1i1p1'
            
        elif CMIPvers=='CMIP6':
            
            if model in ['CNRM-CM6-1', 'CNRM-ESM2-1', 'CNRM-CM6-1-HR', 'UKESM1-0-LL', 'MIROC-ES2L']:
                member = "r1i1p1f2"
            elif model in ['HadGEM3-GC31-LL', 'HadGEM3-GC31-MM']:
                member = "r1i1p1f3"
            elif model=='KACE-1-0-G':
                member = "r2i1p1f1"
            else:
                member = "r1i1p1f1"
        
        #Folder of model and get file list
        dir_model = dir_data + CMIPvers + '/' + model + '/'

        #Output folder
        dir_CMIP_out = dir_out + CMIPvers + '/'
        dir_mod_out  = dir_CMIP_out + model + '/'
        if not os.path.exists(dir_CMIP_out): os.mkdir(dir_CMIP_out)
        if not os.path.exists(dir_mod_out): os.mkdir(dir_mod_out)

        #Read time periods when certain global warming levels (GWL) are reached
        time_GWL = []
        GWL_levels_sel = []
        for level in GWL_levels:
            data_level = GWL_data['warming_level_' + level]
            entry_sel = [entry for entry in data_level if entry['model']==model and entry['exp']==scen and entry['ensemble']==member]
            if len(entry_sel)==1:
                time_GWL.append([entry_sel[0]['start_year'], entry_sel[0]['end_year']])
                GWL_levels_sel.append("{:.1f}".format(int(level)/10) + 'K')
            else:
                print('Level in ' + model + ' for ' + str(int(level)/10) + ' K not available')

        #Define all time slices (fixed times and GWL times)
        time_app = time_fix + time_GWL
        time_str = [str(time[0]) + '-' + str(time[1]) for time in time_fix]
        time_str = time_str + GWL_levels_sel
        
        #Loop over files
        for time_sel, time_out in zip(time_app, time_str):

            #Define input file name
            time_str_read = str(time_sel[0]) + '-' + str(time_sel[1])
            fname = 'ThreshExceed-' + HSI + '_' + model + '_' + scen + '_' + member + '_' + time_str_read + '_QDM_HI.nc'

            #Read data
            data_CMIP = xr.open_dataset(dir_model + fname)
            data_CMIP = data_CMIP.rename({HSI: HSI_out})

            #Mask 2018 due to issues with psl and a potential longitudinal displacement in the tasmax
            if (model=='KIOST-ESM') and scen=='ssp585':
                time_mask = data_CMIP.time.dt.year!=2018
                data_CMIP = data_CMIP.where(time_mask)
            
            #Loop over thresholds
            for threshold in thresholds:

                #Select data
                data_out = data_CMIP.sel(threshold=threshold)    

                #Define output file name
                fname_out = HSI_out + '_Exceed' + str(threshold) + '_' + model + '_' + scen + '_' + member + '_' + time_out + '_QDM_HI.nc'
                
                #Save in file
                comp = dict(zlib=True, complevel=3)
                encoding = {var: comp for var in data_out.data_vars}                      
                data_out.to_netcdf(dir_mod_out + fname_out, encoding=encoding)

# %% cell 10
#CORDEX regions
CORDEX_regions = ['AFR-22', 'AFR-44', 'AUS-22', 'AUS-44', 'CAM-22', 'CAM-44', 'EAS-22', 'EAS-44', 'EUR-11', 'NAM-22', 'NAM-44', 'SAM-22', 'SAM-44', 'SEA-22', 'WAS-22', 'WAS-44']

#Define heat indices, RCPs and BC method, and ensemble member
HSI     = 'HI_NOAA'
HSI_out = 'HI'

#Define reference period and application periods for BC
time_fix = [[1995, 2014],
            [2041, 2060], 
            [2081, 2100]]

#Read warming levels
fname = dir_GWL + 'cmip5_all_ens/cmip5_warming_levels_all_ens_1850_1900_no_bounds_check.yml'
with open(fname, 'r') as file:
    GWL_data = yaml.safe_load(file)

#Define warming levels
GWL_levels = ['15', '20', '30', '40']  

#Define thresholds
if HSI=='WBGTindoor':
    thresholds = [31, 33, 35]
elif HSI=='HI_NOAA':
    thresholds = [27, 32, 41]
elif HSI in ['TXmean', 'tasmax']:
    thresholds = [35]
else:
    sys.exit('No thresholds defined for this HSI. Please define them first!')

#Loop over CORDEX regions
for CORDEX_reg in CORDEX_regions:

    print("*********** Preparing " + HSI + " for " + CORDEX_reg + " ***********")
    
    #Define models and RCPs which should be used
    RCPs = []
    all_models = dict()
    all_models['rcp85'] = []
    all_models['rcp26'] = []
    if os.path.exists(dir_names + 'Models_CORDEX-' + CORDEX_reg + '_RCP26.txt'):
        RCPs.append('rcp26')
        with open(dir_names + 'Models_CORDEX-' + CORDEX_reg + '_RCP26.txt', 'r') as filehandle:
            for line in filehandle:
                all_models['rcp26'].append(eval(line[:-1]))
    if os.path.exists(dir_names + 'Models_CORDEX-' + CORDEX_reg + '_RCP85.txt'):
        RCPs.append('rcp85')
        with open(dir_names + 'Models_CORDEX-' + CORDEX_reg + '_RCP85.txt', 'r') as filehandle:
            for line in filehandle:
                all_models['rcp85'].append(eval(line[:-1]))

    #CORDEX directories
    CORDEX_str = 'CORDEX-' + CORDEX_reg
    dir_CORDEX = dir_data + CORDEX_str + '/'

    #Loop over RCPs
    for RCP in RCPs:

        print('')
        print(RCP.upper())

        #Get model list
        models = all_models[RCP]

        #Loop over models
        for i, model in enumerate(models):

            #Get model string and member
            model_str = model[0] + '_' + model[1]
            member    = model[2]

            #Define model folder, and get file list
            dir_model = dir_CORDEX + model_str + '/'
            print("  " + str(i+1) + ') ' + model_str)

            #Output folder
            dir_COR_out = dir_out + CORDEX_str + '/'
            dir_mod_out = dir_COR_out + model_str + '/'
            if not os.path.exists(dir_COR_out): os.mkdir(dir_COR_out)
            if not os.path.exists(dir_mod_out): os.mkdir(dir_mod_out)

            #Get name of CMIP5 driving model
            if ('CNRM-CERFAC' in model[0]) or ('CSIRO-QCCCE' in model[0]) or ('MPI-M' in model[0]) or ('NOAA-GFDL' in model[0]) or ('CSIRO-BOM' in model[0]):
                mod_CMIP5 = '-'.join(model[0].split('-')[2:])
            else:
                mod_CMIP5 = '-'.join(model[0].split('-')[1:])            

            #Read time periods when certain global warming levels (GWL) are reached
            time_GWL = []
            GWL_levels_sel = []
            for level in GWL_levels:
                data_level = GWL_data['warming_level_' + level]
                entry_sel = [entry for entry in data_level if entry['model']==mod_CMIP5 and entry['exp']==RCP and entry['ensemble']==member]
                if len(entry_sel)==1:
                    time_GWL.append([entry_sel[0]['start_year'], entry_sel[0]['end_year']])
                    GWL_levels_sel.append("{:.1f}".format(int(level)/10) + 'K')
                else:
                    print('     -Level in ' + mod_CMIP5 + ' for ' + str(int(level)/10) + ' K not available')

            #Define all time slices (fixed times and GWL times)
            time_app = time_fix + time_GWL
            time_str = [str(time[0]) + '-' + str(time[1]) for time in time_fix]
            time_str = time_str + GWL_levels_sel

            #Loop over files
            for  time_sel, time_out in zip(time_app, time_str):

                #Define input file name
                time_str_read = str(time_sel[0]) + '-' + str(time_sel[1])
                fname = 'ThreshExceed-' + HSI + '_' + model_str + '_' + RCP + '_' + member + '_' + time_str_read + '_QDM_HI.nc'

                #Read data
                data_COR = xr.open_dataset(dir_model + fname)
                data_COR = data_COR.rename({HSI: HSI_out})

                #Correct wrong x and y values for ALADIN53
                if ('ALADIN53' in model_str) and (CORDEX_reg=='EUR-11'):
                    data_COR.x.values[107] = 1337.5
                    data_COR.y.values[107] = 1337.5

                #Mask 2100 in HadGEM2-ES
                if ('HadGEM2-ES' in model_str):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2100 in HadGEM2-ES
                if ('HadGEM2-ES' in model_str):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2100
                if (model[0]=='CCCma-CanESM2') and (CORDEX_reg=='AUS-44'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)                    
                    
                #Mask 2100 in MPI-M-MPI-ESM-LR_ICTP-RegCM4-6 for RCP8.5 because December 2100 is missing
                if (CORDEX_reg=='EUR-11') and (model[0]=='MPI-M-MPI-ESM-LR') and (model[1]=='ICTP-RegCM4-6') and (RCP=='rcp85'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2099 because data for 2099 is missing
                if (CORDEX_reg=='EUR-11') and (model[0]=='MOHC-HadGEM2-ES') and (model[1]=='CLMcom-ETH-COSMO-crCLIM-v1-1') and (RCP=='rcp85'):
                    time_mask = data_COR.time.dt.year!=2099
                    data_COR  = data_COR.where(time_mask)                    
                    
                #Mask 2100 because of potentially spurious data in that year (check variable tasmax)
                if (CORDEX_reg=='EUR-11') and (model[0]=='ICHEC-EC-EARTH') and (model[1]=='MOHC-HadREM3-GA7-05') and (RCP=='rcp26'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2100 because of potentially spurious data in that year (check variable tasmax)
                if (CORDEX_reg=='EUR-11') and (model[0]=='NCC-NorESM1-M') and (model[1]=='CLMcom-ETH-COSMO-crCLIM-v1-1') and (RCP=='rcp85'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2100 because of potentially spurious data in that year (check variable tasmax)
                if (CORDEX_reg=='AUS-22') and (model[0]=='NCC-NorESM1-M') and (model[1]=='CLMcom-HZG-CCLM5-0-15'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)

                #Mask 2099 in MOHC-HadGEM2-ES_CLMcom-HZG-CCLM5-0-15 for RCP8.5 because data for 2098 is missing
                if (CORDEX_reg=='AUS-22') and (model[0]=='MOHC-HadGEM2-ES') and (model[1]=='CLMcom-HZG-CCLM5-0-15') and (RCP=='rcp26'):
                    time_mask = data_COR.time.dt.year!=2099
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2088 in MPI-M-MPI-ESM-LR_ICTP-MPI-CSC-REMO2009 for RCP8.5 because some data in that year is missing
                if (CORDEX_reg=='SAM-44') and (model[0]=='MPI-M-MPI-ESM-LR') and (model[1]=='MPI-CSC-REMO2009') and (RCP=='rcp85'):
                    time_mask = data_COR.time.dt.year!=2088
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2039 and 2075 in MPI-M-MPI-ESM-LR_ICTP-MPI-CSC-REMO2009 for RCP2.6 because some data in those years is missing
                if (CORDEX_reg=='SAM-44') and (model[0]=='MPI-M-MPI-ESM-LR') and (model[1]=='MPI-CSC-REMO2009') and (RCP=='rcp26'):
                    time_mask = (data_COR.time.dt.year!=2039) & (data_COR.time.dt.year!=2075)
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2100 because some data in those years is missing
                if (CORDEX_reg=='NAM-22') and (model[0]=='NOAA-GFDL-GFDL-ESM2M'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2099 in MOHC-HadGEM2-ES_CLMcom-CCLM5-0-2 because some data in those years is missing
                if (CORDEX_reg=='EAS-44') and (model[0]=='MOHC-HadGEM2-ES') and (model[1]=='CLMcom-CCLM5-0-2'):
                    time_mask = data_COR.time.dt.year!=2099
                    data_COR  = data_COR.where(time_mask)                   
                    
                #Mask 2100 in MPI-M-MPI-ESM-LR_CLMcom-CCLM5-0-2 because some data in those years is missing
                if (CORDEX_reg=='EAS-44') and (model[0]=='MPI-M-MPI-ESM-LR') and (model[1]=='CLMcom-CCLM5-0-2'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2099 in MOHC-HadGEM2-ES_CLMcom-HZG-CCLM5-0-15 for RCP8.5 because data for 2099 is (partly) missing
                if (CORDEX_reg=='EAS-22') and (model[0]=='MOHC-HadGEM2-ES') and (model[1]=='ICTP-RegCM4-4'):
                    time_mask = data_COR.time.dt.year!=2099
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2100 in ICTP-RegCM4-4 because some data in those years is missing
                if (CORDEX_reg=='EAS-22') and (model[1]=='ICTP-RegCM4-4'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)

                #Mask 2040, 2096, and 2100 because some data in those years is missing
                if (CORDEX_reg=='SEA-22') and (model[0]=='NOAA-GFDL-GFDL-ESM2M') and (model[1]=='ICTP-RegCM4-3') and (RCP=='rcp85'):
                    time_mask = (data_COR.time.dt.year!=2040) & (data_COR.time.dt.year!=2096) & (data_COR.time.dt.year!=2100)
                    data_COR  = data_COR.where(time_mask)                    
                    
                #Mask 2100 because some data in those years is missing
                if (CORDEX_reg=='SEA-22') and (model[0]=='ICHEC-EC-EARTH') and (model[1]=='ICTP-RegCM4-3') and (RCP=='rcp85'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)                    
         
                #Mask 2009 because of 30 missing days for huss
                if (CORDEX_reg=='SEA-22') and (model[0]=='MOHC-HadGEM2-ES') and (model[1]=='ICTP-RegCM4-7') and (RCP=='rcp85'):
                    time_mask = data_COR.time.dt.year!=2009
                    data_COR  = data_COR.where(time_mask)   

                #Mask 2100 in ICTP-RegCM4-7 because some data in those years is missing
                if (CORDEX_reg=='WAS-22') and (model[1]=='CLMcom-ETH-COSMO-crCLIM-v1-1'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2100 in ICTP-RegCM4-4 because some data in those years is missing
                if (CORDEX_reg=='WAS-44') and (model[1]=='IITM-RegCM4-4'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2099 because 2099 is missing
                if (CORDEX_reg=='AFR-22') and (model[0]=='MOHC-HadGEM2-ES') and (model[1]=='CLMcom-KIT-CCLM5-0-15') and (RCP=='rcp26'):
                    time_mask = data_COR.time.dt.year!=2099
                    data_COR  = data_COR.where(time_mask)                    
                    
                #Mask 2100 because there seems to be an issue with huss and pressure in 2100 in RCP2.6
                if (CORDEX_reg=='AFR-22') and (model[0]=='NCC-NorESM1-M') and (model[1]=='CLMcom-KIT-CCLM5-0-15') and (RCP=='rcp26'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                    
                #Mask 2100 in ICTP-RegCM4-7 because some data in those years is missing
                if (CORDEX_reg in ['CAM-22', 'SEA-22', 'WAS-22', 'SAM-22', 'AUS-22', 'AFR-22']) and (model[1]=='ICTP-RegCM4-7'):
                    time_mask = data_COR.time.dt.year!=2100
                    data_COR  = data_COR.where(time_mask)
                
                #Loop over thresholds
                for threshold in thresholds:

                    #Select data
                    data_out = data_COR.sel(threshold=threshold)    

                    #Define output file name
                    fname_out = HSI_out + '_Exceed' + str(threshold) + '_' + model_str + '_' + RCP + '_' + member + '_' + time_out + '_QDM_HI.nc'

                    #Save in file
                    comp = dict(zlib=True, complevel=2)
                    encoding = {var: comp for var in data_out.data_vars}
                    data_out.to_netcdf(dir_mod_out + fname_out, encoding=encoding)
    
    print('\n')
