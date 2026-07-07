# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/wind_satellites/.ipynb_checkpoints/CMIP5_metadata_file-checkpoint.ipynb

# %% cell 1
from climaf.api import *

req_dict = dict(project='CMIP5',
                frequency='monthly',
                table = 'Amon',
                version='latest'
               )

exp_dict_list = dict(
    baseline = dict(experiment='historical',
         period='1995-2005'
        ),
    rcp26_far = dict(experiment='rcp26',
         period='2081-2100'
        ),
    rcp85_far = dict(experiment='rcp85',
         period='2081-2100'
        )  
)


ens_exp_dict = dict()
for exp in exp_dict_list:
    ens_exp_dict[exp] = dict()
    print exp
    wreq = req_dict.copy()
    wreq.update(exp_dict_list[exp])

    req = ds(model='*',
             variable = 'sfcWind',
             **wreq
            )
    models = req.explore('choices')['model']
    ok_models = []
    for model in models:
        req_test = ds(model=model,
                     #variable = 'sfcWind',
                     variable = 'sfcWind',
                     **wreq
                    )
        ok_models.append(model)
        ens_exp_dict[exp][model] = req_test.explore('resolve')

    lom_per_exp[exp] = ok_models

# %% cell 4
all_CORDEX_domains_ens_dict_per_GWL = dict()
all_CORDEX_domains_ens_dict_per_GWL['EUR'] = dict()

for gwl in ['1.5', '2', '4']:
    
    req = ds(project = 'wind_individual_models_EURO_cordex_ch12',
              clim_period = 'gwl'+gwl.replace('.',''),
              member = '*',
              experiment = '*'
             )
    all_CORDEX_domains_ens_dict_per_GWL['EUR'][gwl] = req.explore('ensemble')

# %% cell 5
all_CORDEX_domains_ens_exp_dict = dict()
all_CORDEX_domains_ens_exp_dict['EUR'] = dict()
for clim_period in ['rcp85_mid', 'rcp26_mid', 'rcp85_far', 'rcp26_far', 'baseline']:
    if clim_period=='baseline':
        wclim_period = 'ref'
        experiment = 'RCP85'
    if '_' in clim_period:
        experiment = clim_period.split('_')[0].upper()
    if 'far' in clim_period:
        wclim_period = 'ece'
    if 'mid' in clim_period:
        wclim_period = 'mce'
    req = ds(project = 'wind_individual_models_EURO_cordex_ch12',
              clim_period = wclim_period,
              member = '*',
              experiment = experiment
             )
    all_CORDEX_domains_ens_exp_dict['EUR'][clim_period] = req.explore('ensemble')

# %% cell 7
import xarray as xr
rows = [['DATA_REF_SYNTAX','MODEL_ID','RCM_VERSION_ID','FREQUENCY','VAR_NAME','VERSION_NO','HANDLE','SUBPANEL']]
CORDEX_domain = 'EUR'
short_CORDEX_domain = CORDEX_domain[0:3]
for exp in all_CORDEX_domains_ens_exp_dict[CORDEX_domain]:
    for mem in all_CORDEX_domains_ens_exp_dict[CORDEX_domain][exp]:
        try:
            dat = all_CORDEX_domains_ens_exp_dict[CORDEX_domain][exp][mem]
            print dat.baseFiles()
        except:
            dat = all_CORDEX_domains_ens_exp_dict[CORDEX_domain][exp][mem].operands[0]
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
                         tracking_id,
                         'NEU','WCE','MED']
        print dataset_descr
        rows.append(dataset_descr)

# %% cell 8
import csv
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.5/EURO_CORDEX_sfcWind_time_periods.csv'

with open(output_metadata_filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in rows:
        writer.writerow(row)

# %% cell 10
import xarray as xr
rows = [['DATA_REF_SYNTAX','MODEL_ID','RCM_VERSION_ID','FREQUENCY','VAR_NAME','VERSION_NO','HANDLE','GWLs','SUBPANEL']]
CORDEX_domain = 'EUR'
short_CORDEX_domain = CORDEX_domain[0:3]


mems_15 = all_CORDEX_domains_ens_dict_per_GWL[CORDEX_domain]['1.5'].keys()
mems_2 = all_CORDEX_domains_ens_dict_per_GWL[CORDEX_domain]['2'].keys()
mems_4 = all_CORDEX_domains_ens_dict_per_GWL[CORDEX_domain]['4'].keys()
all_mems = set(mems_15 + mems_2 + mems_4)
for mem in all_mems:
    tmp_GWL_per_mem = []
    if mem in mems_15:
        tmp_GWL_per_mem.append('1.5')
        GWL = '1.5'
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
        dat = all_CORDEX_domains_ens_dict_per_GWL[CORDEX_domain][GWL][mem]
        print dat.baseFiles()
    except:
        dat = all_CORDEX_domains_ens_dict_per_GWL[CORDEX_domain][GWL][mem].operands[0]
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
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.5/EURO_CORDEX_sfcWind_gwls.csv'

with open(output_metadata_filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in rows:
        writer.writerow(row)
