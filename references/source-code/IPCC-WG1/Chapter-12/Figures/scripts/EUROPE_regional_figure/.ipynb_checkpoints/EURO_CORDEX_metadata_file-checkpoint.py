# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/EUROPE_regional_figure/.ipynb_checkpoints/EURO_CORDEX_metadata_file-checkpoint.ipynb

# %% cell 1
import regionmask
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import json
import glob

from climaf.api import *

# -- CORDEX
pattern ='/projsu/cmip-work/rvautard/IPCC/SWE${experiment}/snw100seas.${model}.${clim_period}.meanG.nc'
cproject('SWE_cordex_ch12','experiment',('period','fx'),'clim_period','model', ('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='SWE_cordex_ch12', url=pattern) 

clog('critical')

exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='RCP85',
         clim_period = 'ref'),    
    # -- Mid term
    dict(experiment='RCP85',
         clim_period = 'mce'),
    dict(experiment='RCP26',
         clim_period = 'mce'),
    # -- Late term
    dict(experiment='RCP85',
         clim_period = 'ece'),
    dict(experiment='RCP26',
         clim_period = 'ece'),
]

ens_exp_dict = dict()
ens_GWL_dict = dict()

for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    clim_period = exp['clim_period']

    # -- Create ensemble object for the scenario
    req_dict = dict(project='SWE_cordex_ch12',
                  experiment = experiment,
                  clim_period = clim_period,
                 )
    #
    req_exp = ds(model = '*', **req_dict)
    lom = req_exp.explore('choices')['model']

    ens_dict = dict()
    for model in lom:
        ens_dict[model] = ds(model=model, **req_dict).explore('resolve')
    ens = cens(ens_dict)
    
    ens_exp_dict[experiment+'_'+clim_period] = ens

# %% cell 2
ens_exp_dict.keys()

# %% cell 4
ens_GWL_dict = dict()
for GWL in ['15','2','4']:
    #
    req_GWL = ds(project='SWE_cordex_ch12',
                 experiment='GWL',
                 clim_period = 'gwl'+GWL,
                 model = '*',
                )
    GWL_ens = req_GWL.explore('ensemble')
    # -- Climatologies
    ens_GWL_dict[GWL] = GWL_ens

# %% cell 7
import xarray as xr
rows = [['DATA_REF_SYNTAX','MODEL_ID','RCM_VERSION_ID','FREQUENCY','VAR_NAME','VERSION_NO','HANDLE','SUBPANEL']]
CORDEX_domain = 'EUR'
for exp in ens_exp_dict:
    for mem in ens_exp_dict[exp]:
        try:
            dat = ens_exp_dict[exp][mem]
            print dat.baseFiles()
        except:
            dat = ens_exp_dict[exp][mem].operands[0]
            print dat.baseFiles()
        nc = xr.open_dataset(dat.baseFiles().split(' ')[0])
        institute_id = nc.institute_id
        driving_model_id = nc.driving_model_id
        frequency = nc.frequency
        model_version = nc.rcm_version_id
        realization = nc.driving_model_ensemble_member
        experiment = nc.driving_experiment_name
        try:
            tracking_id = nc.tracking_id
        except:
            tracking_id = 'none'
        rcm = nc.model_id
        variable = 'snw'
        CORDEX_domain_id = nc.CORDEX_domain
        nc.close()
        #project_id.product.CORDEX_domain.institute_id.driving_model_id.driving_experiment_name.driving_model_ensemble_member
        dataset_descr = ['CORDEX.output.'+CORDEX_domain_id+'.'+institute_id+'.'+driving_model_id+'.'+experiment+'.'+realization,
                         rcm,
                         model_version,
                         frequency,
                         variable,
                         'version_no',
                         tracking_id,
                         'NEU','WCE','MED']
        print dataset_descr
        rows.append(dataset_descr)

# %% cell 8
import csv
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_12.9/EURO_CORDEX_snw_time_periods.csv'

with open(output_metadata_filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in rows:
        writer.writerow(row)

# %% cell 10
import xarray as xr
rows = [['DATA_REF_SYNTAX','MODEL_ID','RCM_VERSION_ID','FREQUENCY','VAR_NAME','VERSION_NO','HANDLE','GWLs','SUBPANEL']]
CORDEX_domain = 'EUR'
short_CORDEX_domain = CORDEX_domain[0:3]


mems_15 = ens_GWL_dict['15'].keys()
mems_2 = ens_GWL_dict['2'].keys()
mems_4 = ens_GWL_dict['4'].keys()
all_mems = set(mems_15 + mems_2 + mems_4)
for mem in all_mems:
    tmp_GWL_per_mem = []
    if mem in mems_15:
        tmp_GWL_per_mem.append('1.5')
        GWL = '15'
    else:
        tmp_GWL_per_mem.append('none')
    if mem in mems_2:
        tmp_GWL_per_mem.append('2')
        GWL = '2'
    else:
        tmp_GWL_per_mem.append('none')
    if mem in mems_4:
        tmp_GWL_per_mem.append('4')
        GWL = '4'
    else:
        tmp_GWL_per_mem.append('none')
    try:
        dat = ens_GWL_dict[GWL][mem]
        print dat.baseFiles()
    except:
        dat = ens_GWL_dict[GWL][mem].operands[0]
        print dat.baseFiles()
    nc = xr.open_dataset(dat.baseFiles().split(' ')[0])
    institute_id = nc.institute_id
    driving_model_id = nc.driving_model_id
    frequency = nc.frequency
    model_version = nc.rcm_version_id
    realization = nc.driving_model_ensemble_member
    experiment = nc.driving_experiment_name
    try:
        tracking_id = nc.tracking_id
    except:
        tracking_id = 'none'
    rcm = nc.model_id
    variable = 'sfcWind'
    CORDEX_domain_id = nc.CORDEX_domain
    nc.close()
    #project_id.product.CORDEX_domain.institute_id.driving_model_id.driving_experiment_name.driving_model_ensemble_member
    dataset_descr = ['CORDEX.output.'+CORDEX_domain_id+'.'+institute_id+'.'+driving_model_id+'.'+experiment+'.'+realization,
                     rcm,
                     model_version,
                     frequency,
                     variable,
                     'version_no',
                     tracking_id]
    dataset_descr = dataset_descr + tmp_GWL_per_mem + ['NEU','WCE','MED']
    print dataset_descr
    rows.append(dataset_descr)

# %% cell 11
import csv
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_12.9/EURO_CORDEX_snw_gwls.csv'

with open(output_metadata_filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in rows:
        writer.writerow(row)
