#!/usr/bin/env python
#
# Description:
# This script generates Figures 3.2a and 3.44
# of IPCC WGI contribution to AR6, Chapter 3
#
# Creator: Masa Kageyama, LSCE, France
# Creation Date: December 2019
# Last revision: March 2021
# 
# This script was run in a python 2.7 environment, created with conda, 
# and based on the CDAT 8.1 environment developed at PCMDI 
# (https://github.com/cdat/cdat/releases/tag/v8.1) and other standard python packages 
# like matplotlib, available on conda-forge
#
# Full installation details available at: 
# https://wiki.lsce.ipsl.fr/pmip3/doku.php/other:uvcdat:cdat_conda:cdat_8_1
#
# Contents:
# In Part I this script computes spatial averages, and then temporal mean and standard deviations
# from these time series
#           - for reconstructions (taking into account the estimated uncertainty on the reconstructions)
#           - for model output
#           - and for model output sampled on grid points for which there are reconstructions
#           for model output, the range of results is computed considering averages over 50 years
#           taken randomly in the time series.
# input files for this step contain time series of annual values of:
#           - mean annual temperature
#           - mean temperature of the warmest month
#           - mean temperature of the coldest month
#           - mean annual precipitation
#
# the results are stored in the "dic_res" dictionary
# and saved in a file called : DMC_LGM_MH_PMIP3_PMIP4_IPCC_save_res2.dat
# Part I can be skipped by reading this file directly,
# to do that, choose compute_averages_again = 'no' in the options below
#
# In Part II, this script plots the results stored in "dic_res" to create Fig 3.2a and Fig 3.44 
# 
# the regions over which the distance is computed are defined in dic_regions and list_regions;
# the periods for which the distance is computed to be defined in list_periods;
# the models for which the distance is computed to be defined in dic_models and list_models;

# import necessary packages
import cdms2 as c, numpy as N, cdutil, MV2 as MV
import random
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerErrorbar
import shelve
from os import system
from os import path
import glob,commands

list_periods = ['LGM','MH']

compute_averages_again = 'yes'#'yes' #'no'#
compute_monte_carlo_averages = 'yes' #'no' #'yes' # relevant only if compute_averages_again == 'yes'
plot_deltaTland_vs_deltaTocean = 'yes' # for Fig 3.2a
version='20210326'


# defining list of models
# LGM
# PMIP3
list_pmip3_models_lgm = ['IPSL','CNRM', 'MIROC','MPI-p1','MPI-p2','MRI','GISSE2-p1','GISSE2-p2','CESM',]
# PMIP4
list_pmip4_models_lgm = ['CESM2.1','CESM1-2','AWI-ESM-1-1-LR','AWIESM2','iLOVECLIM-ICE-6G','iLOVECLIM-GLAC1D','INM-CM4-8','MIROC-ES2L','MPI-ESM1-2-LR','UT-CCSM4','IPSLCM5A2',]
# all together
list_models_lgm = list_pmip3_models_lgm + list_pmip4_models_lgm

# MH
list_pmip3_models_mh = ['bcc-csm1-1','CCSM4','CNRM-CM5','CSIRO-Mk3-6-0','CSIRO-Mk3L-1-2',
                   'FGOALS-g2','FGOALS-s2',
                   'GISS-E2-R','HadGEM2-ES','IPSL-CM5A-LR','MIROC-ESM','MPI-ESM-P','MRI-CGCM3',]
list_pmip4_models_mh = ['AWI-ESM-1-1-LR','CESM2','EC-Earth3-LR','FGOALS-f3-L','FGOALS-g3','GISS-E2-1-G',
                   'HadGEM3-GC31','INM-CM4-8',
                   'IPSL-CM6A-LR','MIROC-ES2L','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','NorESM1-F',
                   'NorESM2-LM','UofT-CCSM-4']
list_models_mh = list_pmip3_models_mh + list_pmip4_models_mh

# PMIP3 models
list_pmip3_models = list_pmip3_models_lgm + list_pmip3_models_mh
# PMIP4 models
list_pmip4_models = list_pmip4_models_lgm + list_pmip4_models_mh + ['ACCESS-ESM1-5','CNRM-CM6-1']
# CMIP6 models
list_cmip6_models = ['ACCESS-ESM1-5','AWI-ESM-1-1-LR','CESM2','CESM2.1','EC-Earth3-LR','FGOALS-f3-L','FGOALS-g3','GISS-E2-1-G',
                     'HadGEM3-GC31','INM-CM4-8','IPSL-CM6A-LR','MIROC-ES2L','MPI-ESM1-2-LR','MRI-ESM2-0','NESM3','NorESM2-LM',]

# for Fig 3.44 panel a. Data provided by Dan Lunt (computed for Chapter 7)
# GSAT anomalies
# for LIG (Last Interglacial)
dic_global_mean_lig = {'ACCESS-ESM1-5':0.33,
                       'AWI-ESM-1-1-LR':-0.25,
                       'AWIESM2':-0.20,
                       'CESM2':-0.11,
                       'CNRM-CM6-1':0.4,
                       'EC-Earth3-LR':0.45,
                       'FGOALS-f3-L':-0.48,
                       'FGOALS-g3':0.38,
                       'GISS-E2-1-G':-0.12,
                       'HadGEM3-GC31':0.56,
                       'INM-CM4-8':-0.2,
                       'IPSL-CM6A-LR':-0.29,
                       'MIROC-ES2L':-0.4,
                       'MPI-ESM1-2-LR':-0.12,
                       'NESM3':0.07,
                       'NorESM1-F':-0.24,
                       'NorESM2-LM':-0.11,
                       }
# for the mid-Pliocene
dic_global_mean_plio = {'CCSM4-plio':2.64831,
                        'CCSM4-UoT': 3.79105,
                        'CCSM4-Utrecht': 4.67974,
                        'CESM1.2': 4.03265,
                        'CESM2': 5.22695,
                        'COSMOS': 3.32687,
                        'EC-Earth3-LR': 4.84114,
                        'GISS-E2-1-G': 2.08071,
                        'HadCM3': 2.89054,
                        'IPSL-CM6A-LR': 3.47365,
                        'IPSLCM5A': 2.29695,
                        'IPSLCM5A2': 2.16866,
                        'MIROC4m': 3.13146,
                        'MRI-CGCM2.3': 2.45558,
                        'NorESM-L': 2.09194,
                        'NorESM1-F': 1.73549,
                        'HadGEM3':5.05506,
                        }
 # for the Eocene
dic_global_mean_eocene = {'CESM1.2_CAM5-deepmip_stand_6xCO2': 16.5428,
                          'COSMOS-landveg_r2413-deepmip_sens_4xCO2': 13.0424,
                          'GFDL_CM2.1-deepmip_stand_6xCO2': 14.5911,
                          'GFDL_CM2.1-deepmip_sens_4xCO2': 11.8548,
                          'INM-CM4-8-deepmip_stand_6xCO2': 10.1490,
                          'NorESM1_F-deepmip_sens_4xCO2':9.61720,
                        }

# For Figure 3.44 panel a, estimates from reconstructions, cf Figure 2.34 and section 2.3.1.1
darrell_s_delta_gsat_estimates = {'MH':[0.2,1.0],
                                  'LGM':[-7,-4],
                                  'LIG':[0.5,1.5],
                                  'MPWP':[2.5,4],
                                  'EECO':[11,17],
                                 }
 

list_regions = ['Globe','WesternEurope','NAmerica','WestAfrica',]

#list_reconstructions = ['Tierney2020DA','Tierney2019','Bartlein2011','Cleator2019' ,'Cleator2019_B2011pts','MARGO2009']
list_reconstructions = ['Tierney2019','Bartlein2011','Cleator2019']

# define masks to be used for reconstructions
dic_rds_masks = {'Bartlein2011' : 'own',
                'Cleator2019': 'own',
                'Tierney2019':'own',
                }

# list of percentiles to be computed
#list_perc = [50,]

### information on reconstructions
rep_data = '/home/users/'
dic_data_files = {}
dic_data_files['MARGO2009'] = {}
dic_data_files['MARGO2009']['MATocean'] = {'LGM':'masa/GRAPH/VCDAT/MARGO_data.nc', }

dic_data_files['Tierney2019']={}
#dic_data_files['Tierney2019']['MATocean'] = {'LGM':'masa/GRAPH/VCDAT/Scripts_PMIP/LGM_5x5_deltaSST_JTierney2019.nc', }
dic_data_files['Tierney2019']['MATocean'] = {'LGM':'masa/GRAPH/VCDAT/Scripts_PMIP/MarineData/Tierney2020_ProxyData_5x5_deltaSST.nc', }
 
dic_data_files['Tierney2020DA']={}
dic_data_files['Tierney2020DA']['MATocean'] = {'LGM':'masa/GRAPH/VCDAT/Scripts_PMIP/MarineData/Tierney2020_DA_atm_cdmssed.nc', }
#dic_data_files['Tierney2020DA']['MATocean'] = {'LGM':'masa/GRAPH/VCDAT/Scripts_PMIP/MarineData/Tierney2020_DA_oce_regrid_cdmssed.nc', }

dic_data_files['Bartlein2011'] = {}
dic_data_files['Bartlein2011']['MAT'] = {'MH':'masa/GRAPH/VCDAT/Scripts_PMIP/Bartlein-et-al-data/mat_delta_06ka_ALL_grid_2x2.nc',
                                         'LGM':'masa/GRAPH/VCDAT/Scripts_PMIP/Bartlein-et-al-data/mat_delta_21ka_ALL_grid_2x2.nc'}
dic_data_files['Bartlein2011']['MTCO'] = {'MH':'masa/GRAPH/VCDAT/Scripts_PMIP/Bartlein-et-al-data/coldtemp_delta_06ka_ALL_grid_2x2.nc',
                                          'LGM':'masa/GRAPH/VCDAT/Scripts_PMIP/Bartlein-et-al-data/coldtemp_delta_21ka_ALL_grid_2x2.nc'}
dic_data_files['Bartlein2011']['MTWA'] = {'MH':'masa/GRAPH/VCDAT/Scripts_PMIP/Bartlein-et-al-data/warmtemp_delta_06ka_ALL_grid_2x2.nc',
                                          'LGM':'masa/GRAPH/VCDAT/Scripts_PMIP/Bartlein-et-al-data/warmtemp_delta_21ka_ALL_grid_2x2.nc'}
dic_data_files['Bartlein2011']['MAP'] = {'MH':'masa/GRAPH/VCDAT/Scripts_PMIP/Bartlein-et-al-data/map_delta_06ka_ALL_grid_2x2.nc',
                                         'LGM':'masa/GRAPH/VCDAT/Scripts_PMIP/Bartlein-et-al-data/map_delta_21ka_ALL_grid_2x2.nc'}

dic_data_files['Cleator2019'] = {}
for var in ['MAT','MTCO','MTWA','MAP']:
    #dic_data_files['Cleator2019'][var] = {'LGM':'jypeter/CDAT/Progs/Devel/PMIP4_CMIP6/Cleator_LGM/cleator_data_v190924.nc'}
    dic_data_files['Cleator2019'][var] = {'LGM':'jypeter/CDAT/Progs/Devel/PMIP4_CMIP6/Cleator_LGM/cleator_data_v200319.nc'}

    
dic_data_files['Cleator2019_B2011pts'] = {}
for var in ['MAT','MTCO','MTWA','MAP']:
    dic_data_files['Cleator2019_B2011pts'][var] = {'LGM':'jypeter/CDAT/Progs/Devel/PMIP4_CMIP6/Cleator_LGM/cleator_data_v200319.nc'}


dic_rec_varnames = {}
dic_rec_varnames['Bartlein2011'] ={'MTCO':['mtco','_anm_mean','_se_mean'],
                                   'MAT':['mat','_anm_mean','_se_mean'],
                                   'MTWA':['mtwa','_anm_mean','_se_mean'],
                                   'MAP':['map','_anm_mean','_se_mean'],
                                   }

dic_rec_varnames['Cleator2019'] ={'MTCO':['MTCO','','_SD'],
                                  'MAT':['MAT','','_SD'],
                                  'MTWA':['MTWA','','_SD'],
                                  'MAP':['MAP','','_SD'],
                                   }

dic_rec_varnames['Cleator2019_B2011pts'] ={'MTCO':['MTCO','','_SD'],
                                  'MAT':['MAT','','_SD'],
                                  'MTWA':['MTWA','','_SD'],
                                  'MAP':['MAP','','_SD'],
                                   }

dic_rec_varnames['MARGO2009']={'SSTjfmanom':['lgmanomjfmsst','lgmanomjfmmin','lgmanomjfmmax'],
                               'SSTjasanom':['lgmanomjassst','lgmanomjasmin','lgmanomjasmax'],
                               #'MATocean':['lgmanomann','sst','toterr'],
                               'MATocean':['lgmanomann','sst','std'],
                               }

dic_rec_varnames['Tierney2019'] = {'MATocean':['','deltaSST','std'],}

dic_rec_varnames['Tierney2020DA'] = {'MATocean':['','deltaSAToverOceans','errdeltaSAToverOceans'],}
#dic_rec_varnames['Tierney2020DA'] = {'MATocean':['','deltaSST','errdeltaSST'],}

#
# variables to be read from reconstruction syntheses, for LGM and MH
# MTCO: mean temperature of the coldest month
# MTWA: mean temperature of the warmest month
# MAT: mean annual temperature
# MAP: mean annual precipitation
# MATocean: mean annual temperatures over the oceans
dic_list_vars={}
dic_list_vars['LGM'] = {
                        'Bartlein2011' : ['MTCO','MAT','MTWA','MAP',],
                        'Cleator2019' : ['MTCO','MAT','MTWA','MAP',],
                        'Tierney2019':['MATocean',],
                        }
dic_list_vars['MH'] = {'Bartlein2011' : ['MTCO','MAT','MTWA','MAP',],}

# the following directories allow to build the model output file names 
# that are used for comparison with reconstructed variables listed in dic_list_vars
#
# correspondance between variable names in dic_list_vars and variable name in model output files
dic_model_varnames = {'MTCO':'tas',
                      'MAT':'tas',
                      'MTWA':'tas',
                      'MAP':'pr',
                      'MATocean':'tas',
                      }

# correspondance between variable names in dic_list_vars and diagnostic type
dic_model_diagnames = {'MTCO':'MIN', # minimum in the year
                      'MAT':'YR', # annual average
                      'MTWA':'MAX', # maximum in the year
                      'MAP':'YR',
                      'MATocean':'YR',
                      }

# for same colors as in Chris's paper
dic_color_models = {
#PMIP4
    'AWI-ESM-1-1-LR':(0.6,0,1),#'orange',
    'AWI-ESM-1-1-LR':(0.6,0,1),#'orange',
    'AWIESM2':'sandybrown',
    'CESM1-2':'skyblue',
    'CESM2':(0.26,0.70,0.85),#'turquoise',
    'CESM2.1':(0.26,0.70,0.85),#'turquoise',
    'EC-Earth3-LR':(0.49,0.39,0.72),#'deeppink',
    'FGOALS-f3-L':(0.97,0.6,0.11),#'mediumblue',
    'FGOALS-g3':(0.97,0.6,0.11),#'cornflowerblue',
    'GISS-E2-1-G':(0.47,0.11,0.48),#'blueviolet',
    'HadGEM3-GC31':(0.48,0.55,0.15),#'mediumseagreen',
    'INM-CM4-8':(0.97,0.26,0.26),#'hotpink',
    'IPSL-CM6A-LR':(0.36,0.33,0.68),#'sienna',
    'IPSLCM5A2':'chocolate',
    'MIROC-ES2L':(0.72,0.37,0.71),#'orchid',
    'MPI-ESM1-2-LR':(0.36,0.63,0.64),#'brown',
    'MPI-ESM1-2-LR':(0.36,0.63,0.64),#'brown',
    'MRI-ESM2-0':'darkseagreen',
    'NESM3':(0.68,1.,0.18),#'cadetblue',
    'NorESM1-F':'steelblue',
    'NorESM2-LM':(0.95,0.23,0.65),#'gold',
    'UofT-CCSM-4':'darkgreen',
    'iLOVECLIM-ICE-6G':'darkviolet',
    'iLOVECLIM-GLAC1D':'slateblue',
    'UT-CCSM4':'darkgreen',
    'ACCESS-ESM1-5':'blue',
    'CNRM-CM6-1':'green',
}


### definition of the regions: latrange, lonrange
dic_regions = {'Globe':[(-90,90,'cc'),(-180,180,'co')],
               'WesternEurope':[(35,70,'cc'),(-10,30,'cc')],
               'WestAfrica':[(0,30,'cc'),(-20,30,'cc'),],
               'NAmerica':[(20,50,'cc'),(-140,-60,'cc'),],
               }
# labels
dic_labels = {
    'Bartlein2011':'Bartlein et al., 2011',
    'GISSE2-p1':'GISS-E2-R-p150',
    'GISSE2-p2':'GISS-E2-R-p151',
    'MRI':'MRI-CGCM3',
    'MIROC':'MIROC-ESM-CMIP5',
    'MPI-p2':'MPI-ESM-P-p1',
    'MPI-p1':'MPI-ESM-P-p2',
    'CNRM':'CNRM-CM5',
    'IPSL':'IPSL-CM5A-LR',
    'FGOALS':'FGOALS-g2',
    'Cleator2019':'Cleator2020',
    'CESM':'CCSM4',
    'MPI-ESM1-2-LR':'MPI-ESM-1.2',
    'MIROC-ES2L':'MIROC-ES2L',
    'UT-CCSM4':'UoT-CCSM4',
    #'Cleator':'Cleator et al., 2019',
    #'MARGO2009':'MARGO 2009',
    'Tierney2019':'Tierney2020',
    #'Tierney2020DA':'Tierney2020_DA',
    'CESM2':'CESM2',
    'INM-CM4-8':'INM-CM4-8',
    'iLOVECLIM':'iLOVECLIM',
    'CESM1-2':'CESM1.2',
    'IPSLCM5A2':'IPSLCM5A2',
    'AWI-ESM-1-1-LR':'AWI-ESM-1-1-LR',
    'AWIESM2':'AWI-ESM-2-1-LR',
    }

### information on models
# directories
dir_lgm =  '/home/clim01/masa/PMIP3-PMIP4-analyses-sept2020/'
dir_mh = '/home/clim01/masa/PMIP3-PMIP4-analyses2/PMIP4_MH_from_Chris2/'

# file names 
dic_models = {}
dic_models['PI'] = {}
dic_models['MH'] = {}
dic_models['LGM'] = {}

# files for pre-industrial
dic_models['PI'] = {
    'IPSL':'PMIP3/IPSL-CM5A-LR/%s_Amon_IPSL-CM5A-LR_piControl_r1i1p1_180001-279912_%s.nc',
    'CNRM':'PMIP3/CNRM-CM5/%s_Amon_CNRM-CM5_piControl_r1i1p1_185001-269912_%s.nc',
    'MIROC':'PMIP3/MIROC-ESM/%s_Amon_MIROC-ESM_piControl_r1i1p1_180001-242912_%s.nc',
    'MPI-p1':'PMIP3/MPI-ESM-P/%s_Amon_MPI-ESM-P_piControl_r1i1p1_185001-300512_%s.nc',
    'MPI-p2':'PMIP3/MPI-ESM-P/%s_Amon_MPI-ESM-P_piControl_r1i1p1_185001-300512_%s.nc',
    'MRI':'PMIP3/MRI-CGCM3/%s_Amon_MRI-CGCM3_piControl_r1i1p1_185101-235012_%s.nc',
    'GISSE2-p1':'PMIP3/GISS-E2-R/%s_Amon_GISS-E2-R_piControl_r1i1p2_359001-412012_%s.nc',
    'GISSE2-p2':'PMIP3/GISS-E2-R/%s_Amon_GISS-E2-R_piControl_r1i1p2_359001-412012_%s.nc',
    'CESM':'PMIP3/CCSM4/%s_Amon_CCSM4_piControl_r1i1p1_025001-130012_%s.nc',
    'MIROC-ES2L':'PMIP4/MIROC-ES2L/%s_Amon_MIROC-ES2L_piControl_r1i1p1f2_gn_185001-234912_%s.nc',
    'MPI-ESM1-2-LR':'PMIP4/MPI-ESM1-2-LR/%s-MPI-ESM_lgm_ATM_2000-2099_PI_%s.nc',
    'UT-CCSM4':'PMIP4/UT-CCSM4/%s_Amon_UofT-CCSM4_PI_r1i1p1f1_gn_last100yrs_%s.nc',
    'CESM2':'PMIP4/CESM2/%s_Amon_CESM2_piControl_r1i1p1f1_gn_000101-120012_%s.nc',
    'CESM2.1':'PMIP4/CESM2.1/%s_CESM2.1_PI_%s.nc',
    'FGOALS-g3-r1':'PMIP4/%s/%s_Amon_FGOALS-g3_piControl_r1i1p1f1_gn_020001-089912_%s.nc',
    'FGOALS-g3-r2':'PMIP4/%s/%s_Amon_FGOALS-g3_piControl_r1i1p1f1_gn_020001-089912_%s.nc',
    'FGOALS-g3-r3':'PMIP4/%s/%s_Amon_FGOALS-g3_piControl_r1i1p1f1_gn_020001-089912_%s.nc',
    'IPSLCM6A-f1':'PMIP4/%s/%s_Amon_IPSL-CM6A-LR_piControl_r1i1p1f1_gr_185001-304912_%s.nc',
    'IPSLCM6A-f2':'PMIP4/%s/%s_Amon_IPSL-CM6A-LR_piControl_r1i1p1f1_gr_185001-304912_%s.nc',
    'IPSLCM6A-f3':'PMIP4/%s/%s_Amon_IPSL-CM6A-LR_piControl_r1i1p1f1_gr_185001-304912_%s.nc',
    'IPSLCM6A-f4':'PMIP4/%s/%s_Amon_IPSL-CM6A-LR_piControl_r1i1p1f1_gr_185001-304912_%s.nc',
    'MRI-ESM2':'PMIP4/%s/%s_Amon_MRI-ESM2-0_piControl_r1i1p1f1_gn_185001-255012_%s.nc',
    'NESM3':'PMIP4/%s/%s_Amon_NESM3_piControl_r1i1p1f1_gn_050001-079912_%s.nc',
    'NorESM1-F':'PMIP4/%s/%s_Amon_NorESM1-F_piControl_r1i1p1f1_gn_150101-170012_%s.nc',
    'AWI-ESM-1-1-LR':'PMIP4/AWIESM1/%s_PI-AWIESM1_lgm_ATM_%s.nc',
    'AWIESM2':'PMIP4/AWIESM2/%s_PI-AWIESM2_lgm_ATM_%s.nc',
    'INM-CM4-8':'PMIP4/INM-CM4-8/%s_Amon_INM-CM4-8_piControl_r1i1p1f1_gr1_185001-238012_%s.nc',
    'iLOVECLIM-GLAC1D':'PMIP4/iLOVECLIM-PI/%s_Amon_iLOVECLIM_PI_PI_%s.nc',
    'iLOVECLIM-ICE-6G':'PMIP4/iLOVECLIM-PI/%s_Amon_iLOVECLIM_PI_PI_%s.nc',
    'CESM1-2':'PMIP4/CESM1.2/%s_CESM1.2_PI_%s.nc',
    'IPSLCM5A2':'PMIP4/IPSLCM5A2/%s_IPSLCM5A2_PI_%s.nc',
    }               

# files for LGM simulations
dic_models['LGM'] = {
    'IPSL': 'PMIP3/IPSL-CM5A-LR/%s_Amon_IPSL-CM5A-LR_lgm_r1i1p1_260101-280012_%s.nc',
    'CNRM':'PMIP3/CNRM-CM5/%s_Amon_CNRM-CM5_lgm_r1i1p1_180001-199912_%s.nc',
    'MIROC':'PMIP3/MIROC-ESM/%s_Amon_MIROC-ESM_lgm_r1i1p1_460001-469912_%s.nc',
    'MPI-p1':'PMIP3/MPI-ESM-P/%s_Amon_MPI-ESM-P_lgm_r1i1p1_185001-194912_%s.nc',
    'MPI-p2':'PMIP3/MPI-ESM-P/%s_Amon_MPI-ESM-P_lgm_r1i1p2_185001-194912_%s.nc',
    'MRI':'PMIP3/MRI-CGCM3/%s_Amon_MRI-CGCM3_lgm_r1i1p1_250101-260012_%s.nc',
    'GISSE2-p1':'PMIP3/GISS-E2-R/%s_Amon_GISS-E2-R_lgm_r1i1p150_300001-309912_%s.nc',
    'GISSE2-p2':'PMIP3/GISS-E2-R/%s_Amon_GISS-E2-R_lgm_r1i1p151_300001-309912_%s.nc',
    'CESM':'PMIP3/CCSM4/%s_Amon_CCSM4_lgm_r1i1p1_180001-190012_%s.nc',
    'MIROC-ES2L':'PMIP4/MIROC-ES2L/%s_Amon_MIROC-ES2L_lgm_r1i1p1f2_gn_320001-329912_%s.nc',
    'MPI-ESM1-2-LR':'PMIP4/MPI-ESM1-2-LR/%s-MPI-ESM_lgm_ATM_2000-2099_LGM_%s.nc',
    'UT-CCSM4':'PMIP4/UT-CCSM4/%s_Amon_UofT-CCSM4_LGM_r1i1p1f1_gn_last100yrs_%s.nc',
    'AWI-ESM-1-1-LR':'PMIP4/AWIESM1/%s_LGM-AWIESM1_lgm_ATM_%s.nc',
    'AWIESM2':'PMIP4/AWIESM2/%s_LGM-AWIESM2_lgm_ATM_%s.nc',
    #'Cleator':'../../../../../home/users/masa/GRAPH/VCDAT/Scripts_PMIP/Cleator-et-al-data/cleator_data_v190924.nc',
    'INM-CM4-8':'PMIP4/INM-CM4-8/%s_Amon_INM-CM4-8_lgm_r1i1p1f1_gr1_190001-209912_%s.nc',
    'iLOVECLIM-GLAC1D':'PMIP4/iLOVECLIM-GLAC-1D/%s_Amon_iLOVECLIM_GLAC-1D_LGM_%s.nc',
    'iLOVECLIM-ICE-6G':'PMIP4/iLOVECLIM-ICE-6G-C/%s_Amon_iLOVECLIM_ICE-6G-C_LGM_%s.nc',
    'CESM1-2':'PMIP4/CESM1.2/%s_CESM1.2_LGM_%s.nc',
    'IPSLCM5A2':'PMIP4/IPSLCM5A2/%s_IPSLCM5A2_LGM_%s.nc',
    'CESM2.1':'PMIP4/CESM2.1/%s_CESM2.1_LGM_%s.nc',
    }               

# files for the Mid Holocene
dic_models['MH'] = {
    'CESM':'PMIP3/%s/%s%s_Amon_CCSM4_midHolocene_r1i1p1_100001-130012.nc',
    'CNRM':'PMIP3/%s/%s%s_Amon_CNRM-CM5_midHolocene_r1i1p1.nc',
    'GISSE2-p1':'PMIP3/%s/%s%s_Amon_GISS-E2-R_midHolocene_r1i1p1.nc',
    'IPSL':'PMIP3/%s/%s%s_Amon_IPSL-CM5A-LR_midHolocene_r1i1p1_230101-280012.nc',
    'MIROC':'PMIP3/%s/%s%s_Amon_MIROC-ESM_midHolocene_r1i1p1_233001-242912.nc',
    'MPI-p1':'PMIP3/%s/%s%s_Amon_MPI-ESM-P_midHolocene_r1i1p1_185001-194912.nc',
    'MPI-p2':'PMIP3/%s/%s%s_Amon_MPI-ESM-P_midHolocene_r1i1p2_185001-194912.nc',
    'MRI':'PMIP3/%s/%s%s_Amon_MRI-CGCM3_midHolocene_r1i1p1_195101-205012.nc',
    'CESM2':'PMIP4/%s/%s%s_Amon_CESM2_midHolocene_r1i1p1f1_gn_000101-070012.nc',
    'FGOALS-f3':'PMIP4/%s/%s%s_Amon_FGOALS-f3-L_midHolocene_r1i1p1f1_gr_072001-121912.nc',
    'FGOALS-g3-r1':'PMIP4/%s/%s%s_Amon_FGOALS-g3_midHolocene_r1i1p1f1_gn_065701-112612.nc',
    'FGOALS-g3-r2':'PMIP4/%s/%s%s_Amon_FGOALS-g3_midHolocene_r2i1p1f1_gn_063001-109912.nc',
    'FGOALS-g3-r3':'PMIP4/%s/%s%s_Amon_FGOALS-g3_midHolocene_r3i1p1f1_gn_036001-083912.nc',
    'IPSLCM6A-f1':'PMIP4/%s/%s%s_Amon_IPSL-CM6A-LR_midHolocene_r1i1p1f1_gr_185001-239912.nc',
    'IPSLCM6A-f2':'PMIP4/%s/%s%s_Amon_IPSL-CM6A-LR_midHolocene_r1i1p1f2_gr_185001-204912.nc',
    'IPSLCM6A-f3':'PMIP4/%s/%s%s_Amon_IPSL-CM6A-LR_midHolocene_r1i1p1f3_gr_185001-204912.nc',
    'IPSLCM6A-f4':'PMIP4/%s/%s%s_Amon_IPSL-CM6A-LR_midHolocene_r1i1p1f4_gr_185001-214912.nc',
    'MIROC-ES2L':'PMIP4/%s/%s%s_Amon_MIROC-ES2L_midHolocene_r1i1p1f2_gn_800001-809912.nc',
    'MRI-ESM2':'PMIP4/%s/%s%s_Amon_MRI-ESM2-0_midHolocene_r1i1p1f1_gn_195101-215012.nc',
    'NESM3':'PMIP4/%s/%s%s_Amon_NESM3_midHolocene_r1i1p1f1_gn_179801-189712.nc',
    'NorESM1-F':'PMIP4/%s/%s%s_Amon_NorESM1-F_midHolocene_r1i1p1f1_gn_150101-170012.nc',
}

#################################
# PART I: compute averages
# only executed if compute_averages_again == 'yes'
# otherwise saved results from previous execution of script are used
#################################

if compute_averages_again != 'yes':
    saved_dic = shelve.open('DMC_LGM_MH_PMIP3_PMIP4_IPCC_save_res2')
    dic_res = saved_dic['dic_res']
    saved_dic.close()
else:
    # defining a dictionary to store the results
    dic_res = {}

    # initialisating the dic_res dictionnary
    for period in list_periods:
        dic_res[period] = {}
        for var in ['MAT','MTCO','MTWA','MAP','MATocean']:
            dic_res[period][var] = {}
            for region in list_regions:
                dic_res[period][var][region] = {}
                for rds in list_reconstructions:
                    dic_res[period][var][region][rds] = {} 

    # start computing averages
    for period in list_periods:
        if period == 'LGM':
            list_models = list_models_lgm
            dir_models = dir_lgm
        if period == 'MH':
            list_models = list_models_mh
            dir_models = dir_mh
        for region in list_regions:
            # define region
            # latitudes
            latrange = dic_regions[region][0]
            # longitudes
            lonrange = dic_regions[region][1]
            # get the list of variables to be computed for each reconstruction
            for rds in list_reconstructions:
                # select reconstruction
                if rds in dic_list_vars[period].keys():
                    list_vars = dic_list_vars[period][rds]
                else:
                    continue
                for var in list_vars:
                    print "analysis for period ",period, ", variable ", var, ", region ",region," dataset",rds
                    #
                    # WORK FIRST ON RECONSTRUCTIONS
                    #
                    # read reconstructions
                    f = c.open(rep_data + dic_data_files[rds][var][period])
                    # read reconstructed mean
                    # (keep orig variable for masking model output later on)
                    rmevarname = dic_rec_varnames[rds][var][0] + dic_rec_varnames[rds][var][1]
                    rmeorig = f(rmevarname,lat=latrange,lon=lonrange)
                    # read reconstructed standard errors
                    rsevarname  = dic_rec_varnames[rds][var][0] + dic_rec_varnames[rds][var][2]
                    rseorig = f(rsevarname,lat=latrange,lon=lonrange)
                    # save grid and mask for further use
                    recgrid = rmeorig.getGrid()
                    if rds in ['Tierney2019',]:
                        rmeorig =  MV.masked_where(N.isnan(rmeorig),rmeorig)
                        rseorig =  MV.masked_where(N.isnan(rseorig),rseorig)
                    # compute common mask to rse and rme and impose it to both fields
                    rsemask = rseorig.mask
                    rmemask = rmeorig.mask
                    recmask = rsemask + rmemask
                    rmeorig = MV.masked_where(recmask,rmeorig)
                    rseorig = MV.masked_where(recmask,rseorig)
                    # keep mask from chosen data set
                    if dic_rds_masks[rds] == 'own':
                        chosenmask = recmask
                        dic_res[period][var][region][rds]['mask'] = recmask
                    else:
                        print('this case is not encountered for IPCC figs 3.2a and 3.44')
                    
                    # number of grid points with reconstructions
                    nrec = rmeorig.count()
                    # saving this number in dic_res
                    dic_res[period][var][region][rds]['nbpts'] = nrec

                    # compute weights for spatial averaging
                    recweights = cdutil.area_weights(rmeorig)
                    recweights /= N.sum(recweights)
                    # only keep unmasked values for mean, std, and weights
                    rme = rmeorig.compressed()
                    recwei = recweights.compressed()
                    rse = rseorig.compressed()
                    # close file
                    f.close()
                    #
                    # compute mean/std over region
                    niter = 10000
                    # create niter realisations of the average of the reconstructions
                    # given their standard errors
                    rrave = []
                    for n in range(niter):
                        rrave += [N.sum(random.gauss(rme,rse)*recwei)]
                    # compute mean and std of the average of the reconstructions over the region
                    frave = N.average(rrave)
                    frstd = N.std(rrave)
                    print rds, " reconstructions. average: ", frave, ", std: ", frstd, ", nb points:", nrec
                    # saving the results in dic_res
                    dic_res[period][var][region][rds]['reconstructions'] = {}
                    dic_res[period][var][region][rds]['reconstructions']['mean'] = frave
                    dic_res[period][var][region][rds]['reconstructions']['std'] = frstd
                    #
                    # MODELS
                    #
                    for model in list_models:
                        # initialising dic_res to save the results later on
                        dic_res[period][var][region][rds][model] = {}

                        # read PI model output for selected region
                        diag = dic_model_diagnames[var]
                        modvarname = dic_model_varnames[var]
                            
                        # get name of pi file and read data
                        if period == 'MH':
                            files = path.join(dir_models,'*',modvarname,diag+modvarname+'*'+model+'*'+'piControl'+'*.nc')
                            file_list = glob.glob(files)
                            if len(file_list) == 1:
                                fnamepi = file_list[0]
                                print var, diag, modvarname, model,fnamepi
                            else:
                                print var, diag, model, period, "Houston we have a problem ", file_list
                        elif period == 'LGM':
                            fnamepi = path.join(dir_models,dic_models['PI'][model] % (modvarname,diag))

                        # read variable for pi
                        fpi = c.open(fnamepi)
                        vpi = fpi(modvarname,lat=latrange,lon=lonrange)
                        fpi.close()

                        # same for midHolocene or LGM
                        if period == 'MH':
                            files = path.join(dir_models,'*',modvarname,diag+modvarname+'*'+model+'*'+'midHolocene'+'*.nc')
                            file_list = glob.glob(files)
                            if len(file_list) == 1:
                                fnamepast = file_list[0]
                                print var, model,fnamepast
                            else:
                                print var, diag, model, "Houston we have a problem ", file_list
                        elif period == 'LGM':
                            fnamepast = path.join(dir_models,dic_models[period][model] % (modvarname,diag))
                        fpast = c.open(fnamepast)
                        vpast = fpast(modvarname,lat=latrange,lon=lonrange)
                        fpast.close()

                        # change units
                        if var in ['MAT','MTCO','MTWA','MATocean']:
                            vpi -= 273.15
                            vpast -= 273.15
                        if var in ['MAP',]:
                            if model not in ['iLOVECLIM-ICE-6G','iLOVECLIM-GLAC1D',]:
                                vpi *= 86400.*365
                                vpast *= 86400.*365

                        # regrid model output on 2x2 data grid
                        vpir = vpi.regrid(recgrid, regridTool='regrid2')
                        vpastr = vpast.regrid(recgrid, regridTool='regrid2')

                        # create new variables masked where there is no reconstructions
                        # create 3D mask for time-dependent model output
                        maskpi = N.repeat(N.reshape(chosenmask,(1,)+chosenmask.shape),vpi.shape[0],axis=0)
                        maskpast = N.repeat(N.reshape(chosenmask,(1,)+chosenmask.shape),vpast.shape[0],axis=0)
                        # apply it
                        vpim = MV.masked_where(maskpi,vpir)
                        vpastm = MV.masked_where(maskpast,vpastr)

                        # compute regional average for all years for all model points
                        vpimall = cdutil.averager(vpi,axis='12',weights=['weighted','weighted'],combinewts=1).compressed()
                        vpastmall =  cdutil.averager(vpast,axis='12',weights=['weighted','weighted'],combinewts=1).compressed()

                        # compute regional average for subselection of model points, where there are reconstructions
                        vpirall = cdutil.averager(vpim,axis='12',weights=['weighted','weighted'],combinewts=1).compressed()
                        vpastrall =  cdutil.averager(vpastm,axis='12',weights=['weighted','weighted'],combinewts=1).compressed()

                        # computation of the temporal averages, with ot without estimate of standard deviation
                        niterdist = niter # number of averages to be computed,
                                          # if we choose to compute a distribution of averages over nbyrs randomly picked up in the time series
                        nbyrs = 50 # number of years to compute averages, 
                                   # if we choose to compute a distribution of averages over nbyrs randomly picked up in the time series
                        # niterdist and nbyrs are only used in case compute_monte_carlo_averages == 'yes'
                        #
                        # define names for storing the results in dic_res
                        dic_stat_vars = {
                            'allmodelpts':[vpimall,vpastmall], # all model points
                            'modelonrecpts': [vpirall,vpastrall] # model on reconstruction points
                            }
                        for case in dic_stat_vars.keys():
                            dic_res[period][var][region][rds][model][case] = {}

                        # computation of time averages, either on all years, only once
                        if compute_monte_carlo_averages != 'yes':
                            deltamave = N.average(vpastmall) - N.average(vpimall)
                            deltarave = N.average(vpastrall) - N.average(vpirall)
                            # storing the files
                            dic_res[period][var][region][rds][model]['allmodelpts']['delta_mean'] = deltamave
                            dic_res[period][var][region][rds][model]['modelonrecpts']['delta_mean'] = deltarave
                            dic_res[period][var][region][rds][model]['allmodelpts']['delta_std'] = 0.
                            dic_res[period][var][region][rds][model]['modelonrecpts']['delta_std'] = 0.
                        # or niterdist times, on 50 yrs taken randomly in the time series
                        else:
                            for case in dic_stat_vars.keys():
                                distpi = []
                                distpast = []
                                for n in range(niterdist):
                                    distpi.append(N.average(N.random.choice(dic_stat_vars[case][0],nbyrs,replace=0)))
                                    distpast.append(N.average(N.random.choice(dic_stat_vars[case][1],nbyrs,replace=0)))
                                distpi = N.array(distpi)
                                distpast = N.array(distpast)
                                #distrec = rrave
                                deltam = distpast - distpi # model anomaly
                                #dmdist = deltam - distrec
                                dic_res[period][var][region][rds][model][case]['delta_mean'] = N.average(deltam)
                                dic_res[period][var][region][rds][model][case]['delta_std'] = N.std(deltam)
                        linetmp= "results for : %s, %s, %s, %s, %s, %7.2f, %7.2f"#, %7.2f, %7.2f, %7.2f, %7.2f"
                        print linetmp % (period, model, region, var, rds, 
                                         dic_res[period][var][region][rds][model]['allmodelpts']['delta_mean'],
                                         dic_res[period][var][region][rds][model]['allmodelpts']['delta_std'])

    #
    save_res = shelve.open('DMC_LGM_MH_PMIP3_PMIP4_IPCC_save_res2')
    save_res['dic_res'] = dic_res
    save_res.close()

###########################
# Part II:  plots
###########################


################
# Figure 3.44
################

# define variables to be plotted in each graph: period, variable, region, reconstruction data set for comparison
dic_summary_plots_ipcc_3_43_with_global_means={}
ncols = 8
nlines = 3
dic_summary_plots_ipcc_3_43_with_global_means['nameplot'] = '_MH_LGM_3_44_with_global_means'
dic_summary_plots_ipcc_3_43_with_global_means['datasets'] = ['Cleator2019','Bartlein2011',]
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,2)] = ['MH','MAT','Globe','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,3)] = ['LGM','MAT','Globe','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,4)] = ['LIG','MAT','Globe','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,5)] = ['MPWP','MAT','Globe','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,6)] = ['EECO','MAT','Globe','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,ncols + 4)] = ['MH','MTCO','WesternEurope','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,2*ncols+4)] = ['LGM','MTCO','WesternEurope','Cleator2019']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,ncols + 5)] = ['MH','MTWA','WesternEurope','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,2*ncols+5)] = ['LGM','MTWA','WesternEurope','Cleator2019']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,ncols + 6)] = ['MH','MAP','WesternEurope','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,2*ncols+6)] = ['LGM','MAP','WesternEurope','Cleator2019']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,ncols + 1)] = ['MH','MTCO','NAmerica','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,2*ncols+1)] = ['LGM','MTCO','NAmerica','Cleator2019']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,ncols + 2)] = ['MH','MTWA','NAmerica','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,2*ncols+2)] = ['LGM','MTWA','NAmerica','Cleator2019']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,ncols + 3)] = ['MH','MAP','NAmerica','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,2*ncols+3)] = ['LGM','MAP','NAmerica','Cleator2019']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,ncols + 7)] = ['MH','MAP','WestAfrica','Bartlein2011']
dic_summary_plots_ipcc_3_43_with_global_means[(nlines,ncols,2*ncols+7)] = ['LGM','MAP','WestAfrica','Cleator2019']

dic_markers_rds = {'Bartlein2011':['x','black'],
                   'Cleator2019':['X','black'],
                   'MARGO2009':['s','black'],
                   'Tierney2019':['D','black'],
                   'Cleator2019_B2011pts':['X','black'],}

linetpl = "%10s; %7s; %15s; %7.2f; \n"
for dic_summ_plots in [dic_summary_plots_ipcc_3_43_with_global_means,]:
    # save numerical values
    f = open('IPCC_Fig3.44_numerical_values_'+version+'.txt','w')
    f.write('Numerical values for IPCC AR6 WGI chapter 3 Figure 3_44\n')
    f.write('Creator: Masa Kageyama, LSCE, France\n')
    f.write('========================================================\n')
    # prepare plots
    dic_legend_params = {}
    fig = plt.figure(figsize=(12,10))
    fig.suptitle('Data-model comparison summary CMIP5-PMIP3 vs CMIP6-PMIP4')
    vx = [-10,10]
    sp_list = dic_summ_plots.keys()
    sp_list.remove('nameplot')
    sp_list.remove('datasets')
    nlines = sp_list[0][0]
    ncols = sp_list[0][1]

    # loop on subplots
    for sp in sp_list:
        # read parameters for the subplot
        period = dic_summ_plots[sp][0]
        var = dic_summ_plots[sp][1]
        region = dic_summ_plots[sp][2]
        rds = dic_summ_plots[sp][3]
        # save those in txt file
        f.write('region: %s; variable: %s, period: %s\n' %(region,var,period))
        f.write('reconstructioni data set: %s\n' %(dic_labels[rds],))
        # prepare plot
        p=fig.add_subplot(sp[0],sp[1],sp[2])#,facecolor=bgcolor)
        p.set_xlim(0,3)
        p.set_xticks([],minor=False)
        # adjusting y axis scale
        if region == 'Globe':
            p.set_ylim(-15,20)

            
        if region == 'NAmerica':
            regionname = 'North America'
        elif region == 'WesternEurope':
            regionname = 'Western Europe'
        elif region == 'WestAfrica':
            regionname = 'West Africa'
        elif region == 'Globe':
            regionname = 'Globe'
        else:
            regionname = region

        # defining subplot title
        if dic_summ_plots == dic_summary_plots_ipcc_3_43_with_global_means and region == 'Globe':
           title = period + ' GSAT'
        else:
           title = period + ' ' + var + '\n' + regionname
        p.set_title(title,fontsize=10)#,pad=-12)
        #
        # plot horizontal 0 line
        myplot = p.plot([-1,5],[0,0],ls='--',color='black')

        # get reconstructed values to be plotted and plot them
        if region == 'Globe':
            [deltamin,deltamax] = darrell_s_delta_gsat_estimates[period]
            myplot = p.fill_between(vx,deltamin,deltamax,facecolor='navajowhite',zorder=1,alpha=0.5,label='assessed range from \n the reconstructions')
        else:
            delta = dic_res[period][var][region][rds]['reconstructions']['mean']
            deltaerr = dic_res[period][var][region][rds]['reconstructions']['std']
            deltamin = [delta-deltaerr,delta-deltaerr]
            deltamax = [delta+deltaerr,delta+deltaerr]
            myplot = p.fill_between(vx,deltamin,deltamax,facecolor='navajowhite',zorder=1,alpha=0.5,)#label='assessed range from \n the reconstructions')
            myplot = p.plot([-1,5],[delta,delta],ls='-',color='firebrick',marker='_',markersize=12,label='average \nreconstructions ')# + period)
        # save numerical value
        f.write('reconstructions, average (std): %7.2f (%7.2f) \n' % (delta,deltaerr))
        #
        # now deal with model output
        if period == 'LGM':
            list_models = list_models_lgm
        if period == 'MH':
            list_models = list_models_mh
        if period == 'LIG':
            list_models = dic_global_mean_lig.keys()
        if period == 'MPWP':
            list_models = dic_global_mean_plio.keys()
        if period == 'EECO':
            list_models = dic_global_mean_eocene.keys()
        
        # initialise lists to be used for computing ensemble averages
        list_ens_means_cmip6 = []
        list_ens_means_pmip4 = []
        list_ens_means_pmip3 = []

        # prepating for saving numerical values
        f.write('model results - average (std)\n')
        # loop on models
        for model in list_models:
            if model in list_pmip3_models_lgm:
                i = list_pmip3_models_lgm.index(model)
            if model in list_pmip4_models_lgm:
                i = list_pmip4_models_lgm.index(model)
            if model in list_pmip3_models_mh:
                i = list_pmip3_models_mh.index(model)
            if model in list_pmip4_models_mh:
                i = list_pmip4_models_mh.index(model)
            if region == 'Globe':
               if period in ['MH','LGM']:
                  delta = dic_res[period][var][region][rds][model]['allmodelpts']['delta_mean']
                  deltaerr = 0
                  if model in list_pmip3_models:
                     pmipphase = 'PMIP3'
                  if model in list_pmip4_models:
                     pmipphase = 'PMIP4'
                  print period, pmipphase, model, dic_res[period][var][region][rds][model]['allmodelpts']['delta_mean']
               if period in ['LIG']:
                  delta = dic_global_mean_lig[model]
                  deltaerr = 0
                  pmipphase = 'PMIP4'
               if period in ['MPWP']:
                  delta = dic_global_mean_plio[model]
                  deltaerr = 0
                  pmipphase = 'PMIP4'
               if period in ['EECO']:
                  delta = dic_global_mean_eocene[model]
                  deltaerr = 0
                  pmipphase = 'PMIP4'
            else:
               delta = dic_res[period][var][region][rds][model]['modelonrecpts']['delta_mean']
               deltaerr = dic_res[period][var][region][rds][model]['modelonrecpts']['delta_std']

            # define symbols, colors, labels
            if period in ['MH','LGM']:
                list_pmip4_models2 = list_pmip4_models
            else:
                list_pmip4_models2 = list_models
            if model in list_cmip6_models:
                elw = 1
                xm = 2
                mark = 'o' #'x'
                step = 0
                col = dic_color_models[model]
                incol = dic_color_models[model]
                msize = 4
                list_ens_means_cmip6 += [delta]
                zod = 10
            elif model in list_pmip4_models2 :
                elw = 1
                xm = 2
                mark = 'o' #'X'
                step = 0
                col = 'gray'
                incol = 'gray'
                msize = 3
                list_ens_means_pmip4 += [delta]
                zod = 5
            else:
                elw = 1
                xm = 1
                mark = 'o' #'x'
                step = 0 #0.05
                col = 'gray'
                incol = 'white'
                msize = 3
                list_ens_means_pmip3 += [delta]
                zod = 5

            # plot values
            myplot = p.errorbar(x = xm + step*i , xerr = 0.,
                                y = delta,yerr = deltaerr,
                                 fmt = mark, mec = col, mfc=incol, ecolor = col,
                                 markersize=msize,elinewidth=elw,zorder = zod)
            # save numerical values
            if model in dic_labels.keys():
                modelname = dic_labels[model]
            else:
                modelname = model
            f.write('%20s, %7.2f (%5.2f)\n' % (modelname,delta,deltaerr))
 
        # compute ensemble means
        ens_mean_ar6 = N.mean(list_ens_means_cmip6+list_ens_means_pmip4)
        ens_mean_ar5 = N.mean(list_ens_means_pmip3)
        # plotting PMIP3 and PMIP4+CMIP6 ensemble means
        myplot = p.errorbar(x = 0.5 , xerr = 0., 
                           y = ens_mean_ar5, yerr = 0.,
                           fmt = '*', mec = 'black', mfc='white',
                           markersize=10)
        myplot = p.errorbar(x = 2.5 , xerr = 0.,
                           y = ens_mean_ar6, yerr = 0.,
                           marker = '*', mec = 'black', mfc='black',
                           markersize=10)
        # save numerical values
        f.write('%20s: %7.2f \n' % ('Ensemble mean PMIP3-CMIP5',ens_mean_ar5))
        f.write('%20s: %7.2f \n' % ('Ensemble mean PMIP4-CMIP6',ens_mean_ar6))
        f.write('========================================================\n')

        # print legend
        ncollegendmh = 7
        nlignelegendmh = 0
        ncollegendlgm = 7
        nlignelegendlgm = 1
        xposmh = 1.2
        xposlgm = 1.2

        # legend
        if sp == (nlines,ncols,nlignelegendlgm*ncols + ncollegendlgm):
            p.plot([],[],marker='s',c='navajowhite',markersize=15,label='assessed range from \n the reconstructions')
            p.plot([],[],marker='o',c='gray',mfc='white',markersize=3,label = 'PMIP3 models')
            p.plot([],[],marker='o',c='gray',markersize=3,label = 'non-CMIP6 PMIP4 models')
            p.plot([],[],marker='*',c='black',mfc='white',markersize=10,label = 'PMIP3 ensemble mean')
            p.plot([],[],marker='*',c='black',mfc='black',markersize=10,label = 'PMIP4 ensemble mean')
            for model in list_cmip6_models :
                if model not in ['AWIESM1','MPI-PMIP4','CESM2.1']:
                   if model in dic_labels.keys():
                      label = dic_labels[model]
                   else:
                      label = model
                   p.plot([],[],marker='o',c=dic_color_models[model],markersize=3,label = label)
            p.legend(handler_map=dic_legend_params,
                      bbox_to_anchor=(xposlgm, 1), loc=2, borderaxespad=0.,
                      frameon=0, handlelength=0)
            dic_legend_params[myplot] = HandlerErrorbar(xerr_size=0, yerr_size=0)
        # labels for each line
        if sp == (nlines, ncols, 2):
            p.text(-2,21,'(a)',fontsize=14)
        if sp == (nlines, ncols, ncols + 1):
            p.text(-2,1,'(b)',fontsize=14)
        if sp == (nlines, ncols, 2*ncols + 1):
            p.text(-2,1,'(c)',fontsize=14)

    fig.subplots_adjust(left=0.05, bottom=0.1, right=0.85, top=0.9, wspace=0.6, hspace=0.2)
    fig.savefig('DMC_'+version+dic_summ_plots['nameplot'])
    fig.savefig('DMC_'+version+dic_summ_plots['nameplot']+'.pdf')
    f.close()
            

##############
# Figure 3.2a
##############
dic_lims_region = {'Globe':[-13,1],}

if plot_deltaTland_vs_deltaTocean == 'yes':
    # open file to save numerical values for fig 3.2a
    f = open('IPCC_Fig3.2a_numerical_values_'+version+'.txt','w')
    f.write('Numerical values for IPCC AR6 WGI chapter 3 Figure 3_2a\n')
    f.write('Creator: Masa Kageyama, LSCE, France\n')
    f.write('========================================================\n')
    # LGM land vs ocean delta T
    period = 'LGM'
    for region in ['Globe',]:
        fig = plt.figure(figsize=(10,12))
        dic_legend_params = {}
        pl1 = fig.add_subplot(2,1,1)
        list_pl = [pl1,]
        for pl in [pl1,]:
            pl.set_xlabel('Temperature anomaly over oceans - on reconstruction data pts')
            pl.set_ylabel('Temperature anomaly over land - on reconstruction data pts')
            pl.set_xlim(dic_lims_region[region][0],dic_lims_region[region][1])
            pl.set_ylim(dic_lims_region[region][0],dic_lims_region[region][1])
            pl.plot([0,0],[dic_lims_region[region][0],dic_lims_region[region][1]],c='black',ls= '--',linewidth=1)
            pl.plot([dic_lims_region[region][0],dic_lims_region[region][1]],[0,0],c='black',ls= '--',linewidth=1)
            pl.plot([dic_lims_region[region][0],dic_lims_region[region][1]],
                    [dic_lims_region[region][0],dic_lims_region[region][1]],
                    c='black',ls= '-',linewidth=1)
            pl.plot([],[],marker='o',c='gray',mfc='white',markersize=8,label = 'PMIP3 models')
            pl.plot([],[],marker='o',c='gray',markersize=8,label = 'non-CMIP6 PMIP4 models')

    
        fig.subplots_adjust(left=0.1,right=0.6)
        
        # choose reconstructions: setrds contains [ land data set , marine data set ]
        for indplot, setrds in enumerate([['Cleator2019','Tierney2019'],]):

            rdsl = setrds[0] # reconstruction over land
            rdso = setrds[1] # reconstruction over ocean
	    pl = list_pl[indplot]
            # reconstructions
            deltaO = dic_res[period]['MATocean'][region][rdso]['reconstructions']['mean']
            deltaOerr = dic_res[period]['MATocean'][region][rdso]['reconstructions']['std']
            deltaL = dic_res[period]['MAT'][region][rdsl]['reconstructions']['mean']
            deltaLerr  = dic_res[period]['MAT'][region][rdsl]['reconstructions']['std']
            if rdsl in dic_labels.keys():
               labelrdsl = dic_labels[rdsl]
            else:
               labelrdsl = rdsl
            if rdso in dic_labels.keys():
               labelrdso = dic_labels[rdso]
            else:
               labelrdsl = rdso
            labell = labelrdsl# + '(' +  str(dic_res[period]['MAT'][region][rdsl]['nbpts']) + ')' 
            labelo = labelrdso #+ '(' +  str(dic_res[period]['MATocean'][region][rdso]['nbpts']) + ')' 
            label = labell + '/' + labelo
            myplot = pl.errorbar(x = deltaO, xerr = deltaOerr,
                                 y = deltaL,yerr = deltaLerr,
                                 fmt = 'D', c = 'black',
                                 markersize=8,elinewidth=3,label=label)
            vx = [-20,20]
            vy = [-20,20]
            deltaLmin = [deltaL - deltaLerr,deltaL - deltaLerr]
            deltaLmax = [deltaL + deltaLerr,deltaL + deltaLerr]
            deltaOmin = [deltaO - deltaOerr,deltaO - deltaOerr]
            deltaOmax = [deltaO + deltaOerr,deltaO + deltaOerr]
            myplot = pl.fill_between(vx,deltaLmin,deltaLmax,facecolor='lightgrey',zorder=1,alpha=0.5)
            myplot = pl.fill_betweenx(vy,deltaOmin,deltaOmax,facecolor='lightgrey',zorder=1,alpha=0.5)
            
            # save numerical values for reconstructions
            f.write('region: %s\n' % (region,))
            f.write('Continental reconstructions from : %s\n' % (dic_labels[rdsl],))
            f.write('MAT LGM - PI anomaly, average (standard deviation), in degC \n')
            f.write('%7.2f (%7.2f) \n' % (deltaL, deltaLerr))
            f.write('Marine reconstructions from : %s \n' % (dic_labels[rdso],))
            f.write('MAT LGM - PI anomaly, average (standard deviation), in degC \n')
            f.write('%7.2f (%7.2f) \n' % (deltaO, deltaOerr))
            f.write('model results (model output only taken over reconstruction sites)\n')
            f.write('model name, average (std) over land, average (std) over oceans\n')


            for indexmodel,model in enumerate(list_models_lgm):
                deltaO = dic_res[period]['MATocean'][region][rdso][model]['modelonrecpts']['delta_mean']
                deltaOerr = dic_res[period]['MATocean'][region][rdso][model]['modelonrecpts']['delta_std']
                deltaL = dic_res[period]['MAT'][region][rdsl][model]['modelonrecpts']['delta_mean']
                deltaLerr = dic_res[period]['MAT'][region][rdsl][model]['modelonrecpts']['delta_std']

                fs = 'full'
                if model in list_cmip6_models:
                    elw = 1
                    xm = 2
                    mark = 'o' #'x'
                    step = 0
                    col = dic_color_models[model]
                    incol = dic_color_models[model]
                    msize = 8
                    if model in dic_labels.keys():
                       label = dic_labels[model]
                    else:
                       label = model
                elif model in list_pmip4_models2 :
                    elw = 1
                    xm = 2
                    mark = 'o' #'X'
                    step = 0
                    col = 'gray'
                    incol = 'gray'
                    msize = 8
                    label = ''
                else:
                    elw = 1
                    xm = 1
                    mark = 'o' #'x'
                    step = 0 #0.05
                    col = 'gray'
                    incol = 'white'
                    msize = 8
                    label = ''

                myplot = pl.errorbar(x = deltaO,xerr = deltaOerr,
                                 y = deltaL,yerr = deltaLerr,elinewidth=elw,
                                 fmt = mark, mec= col, mfc= incol, ecolor = col,
                                 markersize=msize,fillstyle=fs,label = label)
                # save numerical values
                if model in dic_labels.keys():
                    label = dic_labels[model]
                else:
                    label = model
                f.write('%20s, %7.2f (%5.2f), %7.2f (%5.2f)\n' % (label, deltaL, deltaLerr, deltaO, deltaOerr))
            f.write('=====================================\n')
            # legend
            for model in list_cmip6_models :
                if model in dic_labels.keys():
                   label = dic_labels[model]
                else:
                   label = model
            #    myplot = p.plot([],[],marker='o',c=dic_color_models[model],markersize=8,label = label)

            myplot = pl.legend(handler_map=dic_legend_params,
                      bbox_to_anchor=(0.02, 0.92), loc=2, borderaxespad=0.,
                      frameon=1, edgecolor='white',framealpha=0,handlelength=0,fontsize='small')
            #pl.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,
            #          frameon=0, )
            dic_legend_params[myplot] = HandlerErrorbar(xerr_size=0, yerr_size=0)
        fig.savefig('deltaTocean_vs_deltaTland_CMIP5_CMIP6_'+version+'_recpts_'+region)
        fig.savefig('deltaTocean_vs_deltaTland_CMIP5_CMIP6_'+version+'_recpts_'+region+'.pdf')
        f.close()
