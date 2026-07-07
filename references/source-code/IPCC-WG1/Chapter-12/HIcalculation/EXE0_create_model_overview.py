# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/HIcalculation/EXE0_create_model_overview.ipynb

# %% cell 3
#List of models
mods_CMIP5_26 = ['bcc-csm1-1', 'bcc-csm1-1-m', 'BNU-ESM', 'CanESM2', 'CESM1-CAM5', 'CNRM-CM5', 'CSIRO-Mk3-6-0',
                 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'HadGEM2-AO', 'HadGEM2-ES', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR',
                 'MRI-CGCM3', 'NorESM1-M']
mods_CMIP5_85 = ['ACCESS1-0', 'ACCESS1-3', 'bcc-csm1-1', 'bcc-csm1-1-m', 'BNU-ESM', 'CanESM2', 'CESM1-CAM5', 'CNRM-CM5',
                 'CSIRO-Mk3-6-0', 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES', 
                 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'IPSL-CM5B-LR', 'MRI-CGCM3', 'MRI-ESM1', 'NorESM1-M']

# Neglected models:

# - RCP2.6:
#   MIROC5, MIROC-ESM, MIROC-ESM-CHEM: neglect MIROC models due to temperature jump over North America (see Mathias Hauser's e-mail)

# - RCP8.5:
#   MIROC5, MIROC-ESM, MIROC-ESM-CHEM: neglect MIROC models due to temperature jump over North America (see Mathias Hauser's e-mail)

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CMIP5_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_CMIP5_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CMIP5_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_CMIP5_85):
        filehandle.write('%s\n' % listitem)

# %% cell 5
#List of models
mods_CMIP6_126 = ['ACCESS-CM2', 'ACCESS-ESM1-5', 'BCC-CSM2-MR', 'CNRM-CM6-1', 'CNRM-CM6-1-HR', 'CNRM-ESM2-1',
                  'CanESM5', 'EC-Earth3', 'EC-Earth3-Veg', 'FGOALS-g3',             'GFDL-ESM4', 'HadGEM3-GC31-LL',
                  'HadGEM3-GC31-MM', 'INM-CM4-8', 'INM-CM5-0', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC-ES2L',
                  'MPI-ESM1-2-HR', 'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NorESM2-LM', 'NorESM2-MM', 'UKESM1-0-LL']
mods_CMIP6_585 = ['ACCESS-CM2', 'ACCESS-ESM1-5', 'BCC-CSM2-MR', 'CNRM-CM6-1', 'CNRM-CM6-1-HR', 'CNRM-ESM2-1',
                  'CanESM5', 'EC-Earth3', 'EC-Earth3-Veg', 'FGOALS-g3', 'GFDL-CM4', 'GFDL-ESM4', 'HadGEM3-GC31-LL',
                  'HadGEM3-GC31-MM', 'INM-CM4-8', 'INM-CM5-0', 'KACE-1-0-G', 'KIOST-ESM', 'MIROC-ES2L', 
                  'MPI-ESM1-2-HR', 'MPI-ESM1-2-LR', 'MRI-ESM2-0', 'NorESM2-LM', 'NorESM2-MM', 'UKESM1-0-LL']

# Neglected models:

# - SSP1-2.6
#   + IPSL-CM6A-LR: due to instabilities in tas it is advised to not use tasmax and huss (https://errata.es-doc.org/static/view.html?uid=19f2d958-8b2a-f69f-ab47-f3d8b13088cf)
#   + CMCC-CM2-SR5: Corrupted raw data made tasmin and tasmax unusable

# - SSP5-8.5
#   + IPSL-CM6A-LR: due to instabilities in tas it is advised to not use tasmax and huss (https://errata.es-doc.org/static/view.html?uid=19f2d958-8b2a-f69f-ab47-f3d8b13088cf)
#   + CMCC-CM2-SR5: Corrupted raw data made tasmin and tasmax unusable

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save SSP1-2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CMIP6_SSP126.txt', 'w') as filehandle:
    for listitem in sorted(mods_CMIP6_126):
        filehandle.write('%s\n' % listitem)
        
#Save SSP5-8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CMIP6_SSP585.txt', 'w') as filehandle:
    for listitem in sorted(mods_CMIP6_585):
        filehandle.write('%s\n' % listitem)

# %% cell 7
mods_EUR11_26 = [
['CNRM-CERFACS-CNRM-CM5', 'CNRM-ALADIN63', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'GERICS-REMO2015', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'KNMI-RACMO22E', 'r1i1p1'],
['ICHEC-EC-EARTH', 'CLMcom-CCLM4-8-17', 'r12i1p1'],
['ICHEC-EC-EARTH', 'DMI-HIRHAM5', 'r3i1p1'],
['ICHEC-EC-EARTH', 'GERICS-REMO2015', 'r12i1p1'],
['ICHEC-EC-EARTH', 'KNMI-RACMO22E', 'r12i1p1'],
['ICHEC-EC-EARTH', 'MOHC-HadREM3-GA7-05', 'r12i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['IPSL-IPSL-CM5A-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MIROC-MIROC5', 'CLMcom-CCLM4-8-17', 'r1i1p1'],
['MIROC-MIROC5', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'DMI-HIRHAM5', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-6', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'KNMI-RACMO22E', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'MOHC-HadREM3-GA7-05', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'ICTP-RegCM4-6', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'KNMI-RACMO22E', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r2i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'KNMI-RACMO22E', 'r1i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2G', 'GERICS-REMO2015', 'r1i1p1']]

mods_EUR11_85 = [
['CCCma-CanESM2', 'CLMcom-CCLM4-8-17', 'r1i1p1'],
['CCCma-CanESM2', 'GERICS-REMO2015', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'CLMcom-CCLM4-8-17', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'CNRM-ALADIN53', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'CNRM-ALADIN63', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'DMI-HIRHAM5', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'GERICS-REMO2015', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'IPSL-WRF381P', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'KNMI-RACMO22E', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'SMHI-RCA4', 'r1i1p1'],
['ICHEC-EC-EARTH', 'CLMcom-CCLM4-8-17', 'r12i1p1'],
['ICHEC-EC-EARTH', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r12i1p1'],
['ICHEC-EC-EARTH', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r1i1p1'],
['ICHEC-EC-EARTH', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r3i1p1'],
['ICHEC-EC-EARTH', 'DMI-HIRHAM5', 'r12i1p1'],
['ICHEC-EC-EARTH', 'DMI-HIRHAM5', 'r1i1p1'],
['ICHEC-EC-EARTH', 'DMI-HIRHAM5', 'r3i1p1'],
['ICHEC-EC-EARTH', 'GERICS-REMO2015', 'r12i1p1'],
['ICHEC-EC-EARTH', 'ICTP-RegCM4-6', 'r12i1p1'],
['ICHEC-EC-EARTH', 'IPSL-WRF381P', 'r12i1p1'],
['ICHEC-EC-EARTH', 'KNMI-RACMO22E', 'r12i1p1'],
['ICHEC-EC-EARTH', 'KNMI-RACMO22E', 'r1i1p1'],
['ICHEC-EC-EARTH', 'KNMI-RACMO22E', 'r3i1p1'],
['ICHEC-EC-EARTH', 'MOHC-HadREM3-GA7-05', 'r12i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r1i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r3i1p1'],
['IPSL-IPSL-CM5A-MR', 'DMI-HIRHAM5', 'r1i1p1'],
['IPSL-IPSL-CM5A-MR', 'GERICS-REMO2015', 'r1i1p1'],
['IPSL-IPSL-CM5A-MR', 'IPSL-WRF381P', 'r1i1p1'],
['IPSL-IPSL-CM5A-MR', 'KNMI-RACMO22E', 'r1i1p1'],
['IPSL-IPSL-CM5A-MR', 'SMHI-RCA4', 'r1i1p1'],
['MIROC-MIROC5', 'CLMcom-CCLM4-8-17', 'r1i1p1'],
['MIROC-MIROC5', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'CLMcom-CCLM4-8-17', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'CNRM-ALADIN63', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'DMI-HIRHAM5', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-6', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'IPSL-WRF381P', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'KNMI-RACMO22E', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'MOHC-HadREM3-GA7-05', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-CCLM4-8-17', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r2i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r3i1p1'],
['MPI-M-MPI-ESM-LR', 'CNRM-ALADIN63', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'DMI-HIRHAM5', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r3i1p1'],
['MPI-M-MPI-ESM-LR', 'ICTP-RegCM4-6', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'KNMI-RACMO22E', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MOHC-HadREM3-GA7-05', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r2i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r2i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r3i1p1'],
['NCC-NorESM1-M', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r1i1p1'],
['NCC-NorESM1-M', 'CNRM-ALADIN63', 'r1i1p1'],
['NCC-NorESM1-M', 'DMI-HIRHAM5', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'IPSL-WRF381P', 'r1i1p1'],
['NCC-NorESM1-M', 'KNMI-RACMO22E', 'r1i1p1'],
['NCC-NorESM1-M', 'MOHC-HadREM3-GA7-05', 'r1i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-EUR-11_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_EUR11_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-EUR-11_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_EUR11_85):
        filehandle.write('%s\n' % listitem)

# %% cell 9
mods_AFR22_26 = [
['MOHC-HadGEM2-ES', 'CLMcom-KIT-CCLM5-0-15', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-KIT-CCLM5-0-15', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'CLMcom-KIT-CCLM5-0-15', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1']]

mods_AFR22_85 = [
['CCCma-CanESM2', 'CCCma-CanRCM4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'CLMcom-KIT-CCLM5-0-15', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-KIT-CCLM5-0-15', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'CLMcom-KIT-CCLM5-0-15', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-AFR-22_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_AFR22_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-AFR-22_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_AFR22_85):
        filehandle.write('%s\n' % listitem)

# %% cell 11
mods_AFR44_26 = [
['ICHEC-EC-EARTH', 'KNMI-RACMO22T', 'r12i1p1'],
['ICHEC-EC-EARTH', 'MPI-CSC-REMO2009', 'r12i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['IPSL-IPSL-CM5A-LR', 'GERICS-REMO2009', 'r1i1p1'],
['MIROC-MIROC5', 'GERICS-REMO2009', 'r1i1p1'],
['MIROC-MIROC5', 'SMHI-RCA4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2009', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'KNMI-RACMO22T', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2G', 'GERICS-REMO2009', 'r1i1p1']]

mods_AFR44_85 = [
['CCCma-CanESM2', 'SMHI-RCA4', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'CLMcom-CCLM4-8-17', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'SMHI-RCA4', 'r1i1p1'],
['CSIRO-QCCCE-CSIRO-Mk3-6-0', 'SMHI-RCA4', 'r1i1p1'],
['ICHEC-EC-EARTH', 'CLMcom-CCLM4-8-17', 'r12i1p1'],
['ICHEC-EC-EARTH', 'DMI-HIRHAM5', 'r3i1p1'],
['ICHEC-EC-EARTH', 'KNMI-RACMO22T', 'r1i1p1'],
['ICHEC-EC-EARTH', 'MPI-CSC-REMO2009', 'r12i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r1i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r3i1p1'],
['IPSL-IPSL-CM5A-LR', 'GERICS-REMO2009', 'r1i1p1'],
['IPSL-IPSL-CM5A-MR', 'SMHI-RCA4', 'r1i1p1'],
['MIROC-MIROC5', 'GERICS-REMO2009', 'r1i1p1'],
['MIROC-MIROC5', 'SMHI-RCA4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'CLMcom-CCLM4-8-17', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2009', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'KNMI-RACMO22T', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-CCLM4-8-17', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r2i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r3i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'SMHI-RCA4', 'r1i1p1']
]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-AFR-44_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_AFR44_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-AFR-44_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_AFR44_85):
        filehandle.write('%s\n' % listitem)

# %% cell 13
mods_NAM22_26 = [
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1']]

mods_NAM22_85 = [
['CCCma-CanESM2', 'CCCma-CanRCM4', 'r1i1p1'],
['CCCma-CanESM2', 'OURANOS-CRCM5', 'r1i1p1'],
['CCCma-CanESM2', 'UQAM-CRCM5', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'OURANOS-CRCM5', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ISU-RegCM4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'NCAR-WRF', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'NCAR-RegCM4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'OURANOS-CRCM5', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'UA-WRF', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'UQAM-CRCM5', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'UQAM-CRCM5', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'ISU-RegCM4', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'NCAR-WRF', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'OURANOS-CRCM5', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-NAM-22_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_NAM22_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-NAM-22_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_NAM22_85):
        filehandle.write('%s\n' % listitem)

# %% cell 15
mods_NAM44_26 = [
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1']]

mods_NAM44_85 = [
['CCCma-CanESM2', 'SMHI-RCA4', 'r1i1p1'],
['CCCma-CanESM2', 'UQAM-CRCM5', 'r1i1p1'],
['ICHEC-EC-EARTH', 'DMI-HIRHAM5', 'r3i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['MPI-M-MPI-ESM-LR', 'UQAM-CRCM5', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-NAM-44_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_NAM44_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-NAM-44_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_NAM44_85):
        filehandle.write('%s\n' % listitem)

# %% cell 17
mods_AUS22_26 = [
['MOHC-HadGEM2-ES', 'CLMcom-HZG-CCLM5-0-15', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-HZG-CCLM5-0-15', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'CLMcom-HZG-CCLM5-0-15', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1']]

mods_AUS22_85 = [
['MOHC-HadGEM2-ES', 'CLMcom-HZG-CCLM5-0-15', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-HZG-CCLM5-0-15', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'CLMcom-HZG-CCLM5-0-15', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1']]
    
#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-AUS-22_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_AUS22_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-AUS-22_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_AUS22_85):
        filehandle.write('%s\n' % listitem)

# %% cell 19
mods_AUS44_85 = [
['CCCma-CanESM2', 'UNSW-WRF360J', 'r1i1p1'],
['CCCma-CanESM2', 'UNSW-WRF360K', 'r1i1p1'],
['CSIRO-BOM-ACCESS1-0', 'UNSW-WRF360J', 'r1i1p1'],
['CSIRO-BOM-ACCESS1-0', 'UNSW-WRF360K', 'r1i1p1'],
['CSIRO-BOM-ACCESS1-3', 'UNSW-WRF360J', 'r1i1p1'],
['CSIRO-BOM-ACCESS1-3', 'UNSW-WRF360K', 'r1i1p1'],
['ICHEC-EC-EARTH', 'CLMcom-CCLM4-8-17-CLM3-5', 'r12i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-CCLM4-8-17-CLM3-5', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

# #Save RCP2.6 models for heat stress indicator calculations in text file
# with open(folder_out + 'Models_CORDEX-AUS-44_RCP26.txt', 'w') as filehandle:
#     for listitem in sorted(mods_AUS44_26):
#         filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-AUS-44_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_AUS44_85):
        filehandle.write('%s\n' % listitem)

# %% cell 21
mods_SAM22_26 = [
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1']]

mods_SAM22_85 = [
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-SAM-22_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_SAM22_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-SAM-22_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_SAM22_85):
        filehandle.write('%s\n' % listitem)

# %% cell 23
mods_SAM44_26 = [
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['MIROC-MIROC5', 'SMHI-RCA4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1']]

mods_SAM44_85 = [
['CCCma-CanESM2', 'SMHI-RCA4', 'r1i1p1'],
['CCCma-CanESM2', 'UCAN-WRF341I', 'r1i1p1'],
['CSIRO-QCCCE-CSIRO-Mk3-6-0', 'SMHI-RCA4', 'r1i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['IPSL-IPSL-CM5A-MR', 'SMHI-RCA4', 'r1i1p1'],
['MIROC-MIROC5', 'SMHI-RCA4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'SMHI-RCA4', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-SAM-44_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_SAM44_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-SAM-44_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_SAM44_85):
        filehandle.write('%s\n' % listitem)

# %% cell 25
mods_EAS22_26 = [
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-4', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-4', 'r1i1p1']]

mods_EAS22_85 = [
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-4', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-4', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-EAS-22_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_EAS22_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-EAS-22_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_EAS22_85):
        filehandle.write('%s\n' % listitem)

# %% cell 27
mods_EAS44_85 = [
['CNRM-CERFACS-CNRM-CM5', 'CLMcom-CCLM5-0-2', 'r1i1p1'],
['ICHEC-EC-EARTH', 'CLMcom-CCLM5-0-2', 'r12i1p1'],
['ICHEC-EC-EARTH', 'DMI-HIRHAM5', 'r3i1p1'],
['MOHC-HadGEM2-ES', 'CLMcom-CCLM5-0-2', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-CCLM5-0-2', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

# #Save RCP2.6 models for heat stress indicator calculations in text file
# with open(folder_out + 'Models_CORDEX-EAS-44_RCP26.txt', 'w') as filehandle:
#     for listitem in sorted(mods_EAS44_26):
#         filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-EAS-44_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_EAS44_85):
        filehandle.write('%s\n' % listitem)

# %% cell 29
mods_WAS22_26 = [
['MIROC-MIROC5', 'ICTP-RegCM4-7', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1']]

mods_WAS22_85 = [
['ICHEC-EC-EARTH', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r12i1p1'],
['MIROC-MIROC5', 'ICTP-RegCM4-7', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'CLMcom-ETH-COSMO-crCLIM-v1-1', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-WAS-22_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_WAS22_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-WAS-22_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_WAS22_85):
        filehandle.write('%s\n' % listitem)

# %% cell 31
mods_WAS44_26 = [
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['MIROC-MIROC5', 'SMHI-RCA4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1']]

mods_WAS44_85 = [
['CCCma-CanESM2', 'IITM-RegCM4-4', 'r1i1p1'],
['CCCma-CanESM2', 'SMHI-RCA4', 'r1i1p1'],
# ['CNRM-CERFACS-CNRM-CM5', 'IITM-RegCM4-4', 'r1i1p1'], #don't include because it only runs until 2085
['CNRM-CERFACS-CNRM-CM5', 'SMHI-RCA4', 'r1i1p1'],
['CSIRO-QCCCE-CSIRO-Mk3-6-0', 'IITM-RegCM4-4', 'r1i1p1'],
['CSIRO-QCCCE-CSIRO-Mk3-6-0', 'SMHI-RCA4', 'r1i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['IPSL-IPSL-CM5A-LR', 'IITM-RegCM4-4', 'r1i1p1'],
['IPSL-IPSL-CM5A-MR', 'SMHI-RCA4', 'r1i1p1'],
['MIROC-MIROC5', 'SMHI-RCA4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'MPI-CSC-REMO2009', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'IITM-RegCM4-4', 'r1i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'IITM-RegCM4-4', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'SMHI-RCA4', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-WAS-44_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_WAS44_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-WAS-44_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_WAS44_85):
        filehandle.write('%s\n' % listitem)

# %% cell 33
mods_CAM22_26 = [
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'ICTP-RegCM4-7', 'r1i1p1']]

mods_CAM22_85 = [
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'ICTP-RegCM4-7', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-CAM-22_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_CAM22_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-CAM-22_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_CAM22_85):
        filehandle.write('%s\n' % listitem)

# %% cell 35
mods_CAM44_26 = [
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['MIROC-MIROC5', 'SMHI-RCA4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1']]

mods_CAM44_85 = [
['CCCma-CanESM2', 'SMHI-RCA4', 'r1i1p1'],
['CNRM-CERFACS-CNRM-CM5', 'SMHI-RCA4', 'r1i1p1'],
['CSIRO-QCCCE-CSIRO-Mk3-6-0', 'SMHI-RCA4', 'r1i1p1'],
['ICHEC-EC-EARTH', 'SMHI-RCA4', 'r12i1p1'],
['IPSL-IPSL-CM5A-MR', 'SMHI-RCA4', 'r1i1p1'],
['MIROC-MIROC5', 'SMHI-RCA4', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'SMHI-RCA4', 'r1i1p1'],
['NCC-NorESM1-M', 'SMHI-RCA4', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'SMHI-RCA4', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-CAM-44_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_CAM44_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-CAM-44_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_CAM44_85):
        filehandle.write('%s\n' % listitem)

# %% cell 37
mods_SEA22_26 = [
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1']]

mods_SEA22_85 = [
['ICHEC-EC-EARTH', 'ICTP-RegCM4-3', 'r1i1p1'],
['IPSL-IPSL-CM5A-LR', 'ICTP-RegCM4-3', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'GERICS-REMO2015', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'ICTP-RegCM4-7', 'r1i1p1'],
['MOHC-HadGEM2-ES', 'SMHI-RCA4', 'r1i1p1'],
['MPI-M-MPI-ESM-LR', 'GERICS-REMO2015', 'r1i1p1'],
['MPI-M-MPI-ESM-MR', 'ICTP-RegCM4-7', 'r1i1p1'],
['NCC-NorESM1-M', 'GERICS-REMO2015', 'r1i1p1'],
['NCC-NorESM1-M', 'ICTP-RegCM4-7', 'r1i1p1'],
['NOAA-GFDL-GFDL-ESM2M', 'ICTP-RegCM4-3', 'r1i1p1']]

#Output folder
folder_out = '/div/amoc/exhaustion/Heat_Health_Global/Scripts/PROJECT_IPCC_AR6/Model_lists/'

#Save RCP2.6 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-SEA-22_RCP26.txt', 'w') as filehandle:
    for listitem in sorted(mods_SEA22_26):
        filehandle.write('%s\n' % listitem)
        
#Save RCP8.5 models for heat stress indicator calculations in text file
with open(folder_out + 'Models_CORDEX-SEA-22_RCP85.txt', 'w') as filehandle:
    for listitem in sorted(mods_SEA22_85):
        filehandle.write('%s\n' % listitem)
