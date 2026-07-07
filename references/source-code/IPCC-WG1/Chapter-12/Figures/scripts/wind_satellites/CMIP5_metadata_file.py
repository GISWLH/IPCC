# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/wind_satellites/CMIP5_metadata_file.ipynb

# %% cell 4
from climaf.api import *

# %% cell 6
lom_per_exp = dict()

# %% cell 7
req_dict = dict(project='CMIP5',
                frequency='monthly',
                table = 'Amon',
                version='latest'
               )

exp_dict_list = dict(
    baseline = dict(experiment='historical',
         period='1995-2005'
        ),
    baseline_ext = dict(experiment='rcp85',
         period='2006-2015'
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
                     variable = 'sfcWind',
                     **wreq
                    )
        if not check_time_consistency_CMIP(req_test):
            print model+' not fully covered'
        else:
            print model+' is fine'
            ok_models.append(model)
            ens_exp_dict[exp][model] = req_test.explore('resolve')

    lom_per_exp[exp] = ok_models

# %% cell 9
lom_baseline     = lom_per_exp['baseline']
lom_baseline_ext = lom_per_exp['baseline_ext']
print 'Models not in both sets:'
print set(lom_baseline) ^ set(lom_baseline_ext)
print 'Models in common:'
common_lom_baseline = list( set(lom_baseline) & set(lom_baseline_ext) )
print common_lom_baseline

# %% cell 11
wreq_dict = req_dict.copy()
wreq_dict.update(exp_dict_list['baseline'])
ens_baseline_hist = eds(model=common_lom_baseline,
                        variable = 'sfcWind',
                        **wreq_dict
                       )

wreq_dict = req_dict.copy()
wreq_dict.update(exp_dict_list['baseline_ext'])
ens_baseline_ext = eds(model=common_lom_baseline,
                       variable = 'sfcWind',
                       **wreq_dict
                      )

# %% cell 13
ens_baseline_dict = dict()
for model in common_lom_baseline:
    
    # -- Cat baseline and ext
    ens_baseline_dict[model] = ccdo2(ens_baseline_hist[model], ens_baseline_ext[model], operator='cat')
    print(model)
    
    print(cfile(ens_baseline_dict[model]))

# %% cell 15
ens_clim_exp_dict = dict()

for exp in ['rcp26_mid','rcp26_far','rcp85_mid','rcp85_far']:    
    print '--> '+exp
    ens_clim_exp_dict[exp] = clim_average(cens(ens_exp_dict[exp]), 'ANM')

# %% cell 17
for exp in ens_exp_dict:
    for mem in ens_exp_dict[exp]:
        print ens_exp_dict[exp][mem]

# %% cell 18
import xarray as xr
def get_tracking_id(ncfile):
    nc = xr.open_dataset(ncfile)
    tracking_id = nc.tracking_id
    nc.close()
    return tracking_id


rows = [['DATA_REF_SYNTAX','FREQUENCY','MODELING_REALM','TABLE_ID','ENS_MEMBER','VERSION_NO','VAR_NAME','HANDLE']]
for exp in ens_exp_dict:
    for mem in ens_exp_dict[exp]:
        try:
            dat = ens_exp_dict[exp][mem]
            print dat.baseFiles()
        except:
            dat = ens_exp_dict[exp][mem].operands[0]
            print dat.baseFiles()
        ds_kvp = dat.explore('resolve').kvp
        ncfile = dat.baseFiles().split(' ')[0]
        try:
            tracking_id = get_tracking_id(ncfile)
        except:
            tracking_id = ''
        dataset_descr = 'CMIP5.output.'+dat.baseFiles().split('/')[4]+'.'+ds_kvp['model']+'.'+ds_kvp['experiment']
        dataset_descr += ','+ds_kvp['frequency']
        dataset_descr += ','+ds_kvp['realm']
        dataset_descr += ','+ds_kvp['table']
        dataset_descr += ','+ds_kvp['realization']
        dataset_descr += ',version_no'
        dataset_descr += ','+ds_kvp['variable']
        dataset_descr += ','+tracking_id
        print(dataset_descr)
        rows.append([dataset_descr])

# %% cell 19
new_rows = []
for row in rows:
    if (len(row)==1):
        print row[0].split(',')
        new_rows.append(row[0].split(','))
    else:
        print row
        new_rows.append(row)

# %% cell 20
import csv
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.5/CMIP5_sfcWind_time_periods.csv'

with open(output_metadata_filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|')
    for row in new_rows:
        writer.writerow(row)

# %% cell 24
ens_baseline = cens(ens_baseline_dict)
ens_clim_exp_dict['baseline'] = clim_average(ens_baseline, 'ANM')

# %% cell 25
ens_clim_exp_dict['baseline'].keys()

# %% cell 27
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

# %% cell 28
ens_dict_per_GWL = dict()
list_of_GWLs = ['1.5','2','3','4']
for GWL in list_of_GWLs:
    ens_dict_per_GWL[GWL] = dict()

for scenario in ['26','85']:
    list_of_models = lom_per_exp['rcp'+scenario+'_far']
    for wmodel in list_of_models:
        if wmodel in GWL_dict:
            print 'We have : ', wmodel
            print GWL_dict[wmodel]
            for GWL in list_of_GWLs:
                if scenario=='26': GWL_scenario = GWL+'_rcp26'
                if scenario=='85': GWL_scenario = GWL+'_rcp85'

                # --> file nc
                # --> period
                central_year = GWL_dict[wmodel][GWL_scenario]
                if central_year not in ['NA','9999'] and int(central_year)>2015:
                    start_year = str( int(central_year)-9 )
                    end_year = str( int(central_year)+10 )
                    dat = ds(model = wmodel,
                             experiment='rcp'+scenario,
                             period=start_year+'-'+end_year,
                             variable = 'sfcWind',
                             **req_dict
                             )
                    ens_dict_per_GWL[GWL][wmodel+'_'+scenario] = clim_average(dat, 'ANM')
                    print cfile(ens_dict_per_GWL[GWL][wmodel+'_'+scenario])
        else:
            print 'We dont have GWL info for ',wmodel

# %% cell 29
ens_dict_per_GWL[GWL]

# %% cell 30
import xarray as xr
def get_tracking_id(ncfile):
    nc = xr.open_dataset(ncfile)
    tracking_id = nc.tracking_id
    nc.close()
    return tracking_id


rows = [['DATA_REF_SYNTAX','FREQUENCY','MODELING_REALM','TABLE_ID','ENS_MEMBER','VERSION_NO','VAR_NAME','HANDLE']]
mems_15 = ens_dict_per_GWL['1.5'].keys()
mems_2 = ens_dict_per_GWL['2'].keys()
mems_4 = ens_dict_per_GWL['4'].keys()
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
        dat = ens_dict_per_GWL[GWL][mem]
        print dat.baseFiles()
    except:
        dat = ens_dict_per_GWL[GWL][mem].operands[0]
        print dat.baseFiles()
    ds_kvp = dat.explore('resolve').kvp
    ncfile = dat.baseFiles().split(' ')[0]
    try:
        tracking_id = get_tracking_id(ncfile)
    except:
        tracking_id = ''
    dataset_descr = ['CMIP5.output.'+dat.baseFiles().split('/')[4]+'.'+ds_kvp['model']+'.'+ds_kvp['experiment']]
    dataset_descr.append(ds_kvp['frequency'])
    dataset_descr.append(ds_kvp['realm'])
    dataset_descr.append(ds_kvp['table'])
    dataset_descr.append(ds_kvp['realization'])
    dataset_descr.append('version_no')
    dataset_descr.append(ds_kvp['variable'])
    dataset_descr.append(tracking_id)
    dataset_descr = dataset_descr+tmp_GWL_per_mem
    
    print(dataset_descr)
    rows.append(dataset_descr)

# %% cell 31
import csv
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.5/CMIP5_sfcWind_gwl.csv'

with open(output_metadata_filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|')
    for row in rows:
        writer.writerow(row)

# %% cell 32
rows

# %% cell 33
#We dont have GWL info for  GISS-E2-H
#We dont have GWL info for  GISS-E2-R
#We dont have GWL info for  GISS-E2-H-CC
#We dont have GWL info for  GISS-E2-R-CC
#We dont have GWL info for  HadGEM2-AO
#We dont have GWL info for  CMCC-CESM
#We dont have GWL info for  MRI-ESM1
