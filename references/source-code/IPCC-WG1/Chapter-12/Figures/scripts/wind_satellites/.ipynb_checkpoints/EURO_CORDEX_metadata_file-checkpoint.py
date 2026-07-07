# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/wind_satellites/.ipynb_checkpoints/EURO_CORDEX_metadata_file-checkpoint.ipynb

# %% cell 1
import regionmask
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import json
import glob

from climaf.api import *

pattern = '/data/jservon/IPCC/wind/CORDEX_individual_models/CORDEX-${CORDEX_domain}_${experiment}_${variable}_${period}_${member}.nc'
cproject('wind_individual_models_cordex_ch12','CORDEX_domain','experiment','period','member',('variable','wind'), ensemble=['member'], separator='%')
dataloc(project='wind_individual_models_cordex_ch12', url=pattern)    

exp_dict_list = dict(
    baseline = dict(experiment='historical',
         period='1995-2005'
        ),
    baseline_ext = dict(experiment='rcp85',
         period='2006-2014'
        ),
    rcp26_mid = dict(experiment='rcp26',
         period='2041-2060'
        ),
    rcp26_far = dict(experiment='rcp26',
         period='2081-2100'
        ),
    rcp85_mid = dict(experiment='rcp85',
         period='2041-2060'
        ),
    rcp85_far = dict(experiment='rcp85',
         period='2081-2100'
        )  
)


AR6regions_by_CORDEX_domain = dict(
    AUS = ['NAU','CAU','EAU','SAU','NZ'],
    SEA = ['SEA'],
    WAS = ['ARP','SAS','WCA'],#,'TIB'],
    EAS = ['TIB','ECA','EAS'],#'SAS'
    CAM = ['NSA','SCA','CAR'],
    SAM = ['NWS','NSA','SAM','NES','SWS','SES','SSA'],
    NAM = ['NWN','NEN','WNA','CNA','ENA','NCA'],#,'GAP'],
    #EUR = ['MED','WCE','NEU'],
    AFR = ['WAF','SAH','CAF','WSAF','ESAF','MDG','SEAF','NEAF','ARP']
)


CORDEX_domains = AR6regions_by_CORDEX_domain.keys()

all_CORDEX_domains_ens_exp_dict = dict()

for CORDEX_domain in CORDEX_domains:

    ens_exp_dict = dict()
    lom_per_exp = dict()
    for exp in exp_dict_list:
        print exp

        experiment = exp_dict_list[exp]['experiment']
        period = exp_dict_list[exp]['period']

        req = ds(experiment=experiment,
                 CORDEX_domain = CORDEX_domain,
                 period=period,
                 member='*',
                 project='wind_individual_models_cordex_ch12')
        try:
            ens_exp = req.explore('ensemble')
            #
            # -- Climatologies
            clim_exp      = clim_average(ens_exp, 'ANM')

            lom_per_exp[exp] = clim_exp.keys()

            # -- Changes = Scenario minus baselines
            ens_exp_dict[exp] = clim_exp
        except:
            lom_per_exp[exp] = []
            # -- Changes = Scenario minus baselines
            ens_exp_dict[exp] = dict()
            

    lom_baseline     = lom_per_exp['baseline']
    lom_baseline_ext = lom_per_exp['baseline_ext']
    print 'Models not in both sets:'
    print set(lom_baseline) ^ set(lom_baseline_ext)
    print 'Models in common:'
    common_lom_baseline = list( set(lom_baseline) & set(lom_baseline_ext) )
    print common_lom_baseline



    req_dict = dict(project='wind_individual_models_cordex_ch12')
    wreq_dict = req_dict.copy()
    wreq_dict.update(exp_dict_list['baseline'])
    ens_baseline_hist = eds(member=common_lom_baseline,
                            CORDEX_domain = CORDEX_domain,
                            **wreq_dict
                           )

    wreq_dict = req_dict.copy()
    wreq_dict.update(exp_dict_list['baseline_ext'])
    ens_baseline_ext = eds(member=common_lom_baseline,
                           CORDEX_domain = CORDEX_domain,
                           **wreq_dict
                          )
    ens_baseline_dict = dict()
    for mem in ens_baseline_hist:
        ens_baseline_dict[mem] = ccdo2(ens_baseline_hist[mem], ens_baseline_ext[mem], operator='cat')

    # -- Add to the list of ensembles
    ens_baseline = cens(ens_baseline_dict)
    ens_exp_dict['baseline'] = clim_average(ens_baseline, 'ANM')

    ens_exp_dict.pop('baseline_ext')
    
    all_CORDEX_domains_ens_exp_dict[CORDEX_domain] = ens_exp_dict


import csv

GWL_csv = '/home/jservon/Chapter12_IPCC/scripts/ATLAS/warming-levels/CMIP5_Atlas_WarmingLevels.csv'

GWL_dict = dict()
i = 0
with open(GWL_csv) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')#, quotechar='|')
    for row in spamreader:
        print row
        model = row[0].split('_')[0]
        print model
        GWL_dict[model] = dict()
        if i==0:
            colnames = row
        j = 0
        for elt in row:
            print elt
            GWL_dict[model][colnames[j]] = row[j]
            j = j + 1
        i = i + 1
        
#

all_CORDEX_domains_ens_dict_per_GWL = dict()

for CORDEX_domain in CORDEX_domains:

    ens_dict_per_GWL = dict()
    list_of_GWLs = ['1.5','2','4']

    for GWL in list_of_GWLs:
        ens_dict_per_GWL[GWL] = dict()

    req_dict = dict(project='wind_individual_models_cordex_ch12')

    for scenario in ['26','85']:
        list_of_models = all_CORDEX_domains_ens_exp_dict[CORDEX_domain]['rcp'+scenario+'_far'].keys()
        for wmodel_realization in list_of_models:
            wmodel = wmodel_realization.split('_')[0]
            GWL_model = None
            for tmp_GWL_model in GWL_dict:
                if tmp_GWL_model in wmodel:
                    GWL_model = tmp_GWL_model
                    break
                    
            if GWL_model:
                print 'We have : ', wmodel
                print GWL_dict[GWL_model]
                for GWL in list_of_GWLs:
                    if scenario=='26': GWL_scenario = GWL+'_rcp26'
                    if scenario=='85': GWL_scenario = GWL+'_rcp85'

                    # --> file nc
                    # --> period
                    central_year = GWL_dict[GWL_model][GWL_scenario]
                    if central_year not in ['NA','9999'] and float(central_year)>=2024:
                        start_year = str( int(central_year)-9 )
                        end_year = str( int(central_year)+10 )

                        dat = ds(member = wmodel_realization,
                                 CORDEX_domain = CORDEX_domain,
                                 experiment = 'rcp'+scenario,
                                 period=start_year+'-'+end_year,
                                 **req_dict
                                 )
                        ens_dict_per_GWL[GWL][wmodel_realization+'_'+scenario] = clim_average(dat, 'ANM')
                        print cfile(ens_dict_per_GWL[GWL][wmodel_realization+'_'+scenario])
            else:
                print 'We dont have GWL info for ',wmodel
    #    
    all_CORDEX_domains_ens_dict_per_GWL[CORDEX_domain] = ens_dict_per_GWL

# %% cell 3
from climaf.api import *

clog('critical')
pattern = '/data/jservon/IPCC/WSPD/${experiment}/sfcWind.${member}.${clim_period}.nc'
cproject('wind_individual_models_EURO_cordex_ch12',('CORDEX_domain','EUR'),'experiment',('period','fx'),'clim_period','member',('variable','sfcWind'), ensemble=['member'], separator='%')
dataloc(project='wind_individual_models_EURO_cordex_ch12', url=pattern)

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
