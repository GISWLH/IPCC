# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/SM_satellites/Prepare_time_slices_GWLs_soilmoisture_CORDEX.ipynb

# %% cell 4
from climaf.api import *

# %% cell 6
lom_per_exp = dict()

# %% cell 7
# List all the GCM_RCM realization per CORDEX_domain, for historical, rcp26 and rcp85

# %% cell 8
from natsort import natsorted

req_dict = dict(project='CORDEX',
                frequency='mon',
                table = 'Lmon',
                version='latest'
               )

exp_dict_list = dict(
    historical = dict(experiment='historical',
         period='2000'
        ),
    rcp85 = dict(experiment='rcp85',
         period='2050'
        ),
    rcp26 = dict(experiment='rcp26',
         period='2050'
        ),
    #baseline_ext = dict(experiment='rcp85',
    #     period='2006-2015'
    #    ),
    #rcp26_mid = dict(experiment='rcp26',
    #     period='2041-2060'
    #    ),
    #rcp26_far = dict(experiment='rcp26',
    #     period='2081-2100'
    #    ),
    #rcp85_mid = dict(experiment='rcp85',
    #     period='2041-2060'
    #    ),
    #rcp85_far = dict(experiment='rcp85',
    #     period='2081-2100'
    #    )  
)

CORDEX_domains = [
    # -- Africa
    'AFR-44','AFR-22',
    # -- AustralAsia
    'AUS-44','AUS-22',
    # -- Central America
    'CAM-44','CAM-22',
    # -- North America
    'NAM-44','NAM-22',
    # -- South America
    'SAM-44','SAM-22',
    # -- Asia
    'EAS-44','EAS-22',
    'WAS-44','WAS-22',
    'SEA-22',
    # -- Europe
    'EUR-11',
    
]

# %% cell 9
listing_ens_exp_dict = dict()
clog('critical')

for CORDEX_domain in CORDEX_domains:

    listing_ens_exp_dict[CORDEX_domain] = dict()
    
    for exp in exp_dict_list:
        listing_ens_exp_dict[CORDEX_domain][exp] = dict()
        print exp
        wreq = req_dict.copy()
        wreq.update(exp_dict_list[exp])

        req = ds(driving_model = '*',
                 model = '*',
                 realization = '*',
                 CORDEX_domain = CORDEX_domain,
                 variable = 'mrso',
                 **wreq
                )
        choices = req.explore('choices')
        if 'driving_model' in choices:
            for GCM in choices['driving_model']:
                for RCM in choices['model']:
                    GCM_RCM = GCM+'_'+RCM
                    model_version = None
                    req2 = ds(driving_model = GCM,
                             model = RCM,
                             realization = '*',
                             CORDEX_domain = CORDEX_domain,
                             variable = 'mrso',
                             **wreq
                            )
                    req2_choices = req2.explore('choices')
                    #if 'model_version' in req2_choices:
                    #    model_version = natsorted(req2_choices['model_version'])[-1]
                    if 'realization' in req2_choices:
                        if 'r1i1p1' in req2_choices['realization']:
                            realization = 'r1i1p1'
                        else:
                            realization = natsorted(req2_choices['realization'])[0]
                        req3 = ds(driving_model = GCM,
                                 model = RCM,
                                 realization = realization,
                                 CORDEX_domain = CORDEX_domain,
                                 variable = 'mrso',
                                 **wreq
                                )
                        req3_choices = req3.explore('choices')
                        if 'model_version' in req3_choices:
                            if not isinstance(req3_choices['model_version'], str):
                                model_versions = req3_choices['model_version']
                                model_version = natsorted(model_versions)[-1]
                            else:
                                model_version = req3_choices['model_version']
                            dat = ds(driving_model = GCM,
                                     model = RCM,
                                     realization = realization,
                                     CORDEX_domain = CORDEX_domain,
                                     model_version = model_version,
                                     variable = 'mrso',
                                     **wreq
                                    ).explore('resolve')
                        else:
                            dat = req3.explore('resolve')
                        # -- Add to the ensemble
                        if dat.baseFiles():
                            listing_ens_exp_dict[CORDEX_domain][exp][GCM_RCM] = dat
                    else:
                        if 'model_version' in req2_choices:
                            if not isinstance(req2_choices['model_version'], str):
                                model_versions = req2_choices['model_version']
                                model_version = natsorted(model_versions)[-1]
                            else:
                                model_version = req2_choices['model_version']
                            dat = ds(driving_model = GCM,
                                     model = RCM,
                                     realization = realization,
                                     CORDEX_domain = CORDEX_domain,
                                     model_version = model_version,
                                     variable = 'mrso',
                                     **wreq
                                    ).explore('resolve')
                            if dat.baseFiles():
                                listing_ens_exp_dict[CORDEX_domain][exp][GCM_RCM] = dat
                        else:
                            try:
                                dat = req2.explore('resolve')
                                if dat.baseFiles():
                                    listing_ens_exp_dict[CORDEX_domain][exp][GCM_RCM] = dat
                            except:
                                print 'No file found for ',req2

            print '==> ensemble for ',CORDEX_domain,' ',exp,':'
            print '==> ',listing_ens_exp_dict[CORDEX_domain][exp].keys()

# %% cell 10
save_obj = listing_ens_exp_dict.copy()
for elt in listing_ens_exp_dict:
    for eelt in listing_ens_exp_dict[elt]:
        for mem in listing_ens_exp_dict[elt][eelt]:
            tmp_kvp = listing_ens_exp_dict[elt][eelt][mem].kvp
            for key in listing_ens_exp_dict[elt][eelt][mem].kvp:
                tmp_kvp[key] = str(listing_ens_exp_dict[elt][eelt][mem].kvp[key])
            save_obj[elt][eelt][mem] = tmp_kvp


import json
with open('listing_ens_exp_dict.json', 'w') as outfile:
    json.dump(save_obj, outfile, sort_keys=True, indent=4)

# %% cell 11
listing_ens_exp_dict[elt][eelt][mem].kvp

# %% cell 13
import json
with open('listing_ens_exp_dict.json') as json_file:
    listing_ens_exp_dict = json.load(json_file)

# %% cell 14
listing_ens_exp_dict['AFR-22'].keys()

# %% cell 16
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

ens_dict = dict()
#for CORDEX_domain in [listing_ens_exp_dict.keys()[0]]:
for CORDEX_domain in listing_ens_exp_dict.keys():
    
    ens_dict[CORDEX_domain] = dict()
    
    # -- Cat baseline and baseline_ext
    hist_members = listing_ens_exp_dict[CORDEX_domain]['historical'].keys()
    rcp85_members = listing_ens_exp_dict[CORDEX_domain]['rcp85'].keys()
    common_members = list( set(hist_members) & set(rcp85_members) )
    
    # -- Create dict to store the members of the concatenated baseline
    ens_dict[CORDEX_domain]['baseline'] = dict()
    #
    if common_members:
        for member in common_members:
            print CORDEX_domain, '-- cat baseline -- ',member
            # -- Baseline
            ds_baseline_dict     = listing_ens_exp_dict[CORDEX_domain]['historical'][member].copy()
            ds_baseline_dict['period'] = exp_dict_list['baseline']['period']
            dat_baseline = ds(**ds_baseline_dict)
            # -- Baseline ext
            ds_baseline_ext_dict = listing_ens_exp_dict[CORDEX_domain]['rcp85'][member].copy()
            ds_baseline_dict['period'] = exp_dict_list['baseline_ext']['period']
            dat_baseline_ext = ds(**ds_baseline_ext_dict)
            #
            # -- Concat baseline and baseline ext
            dat = ccdo2(dat_baseline, dat_baseline_ext, operator='cat')
            #
            # -- Compute climatology
            clim = clim_average(dat,'ANM')
            try:
                cfile(clim)
                #
                # -- Store in baseline
                ens_dict[CORDEX_domain]['baseline'][member] = clim
            except:
                print 'Error on ',member, dat
    #
    future_periods = ['rcp26_mid','rcp26_far','rcp85_mid','rcp85_far']
    for exp in future_periods:
        ens_dict[CORDEX_domain][exp] = dict()
        #
        experiment = exp_dict_list[exp]['experiment']
        period = exp_dict_list[exp]['period']
        #
        # -- We select the members available for the experiment
        for member in listing_ens_exp_dict[CORDEX_domain][experiment]:
            print CORDEX_domain, '-- ',exp,' -- ',member
            ds_dict = listing_ens_exp_dict[CORDEX_domain][experiment][member].copy()
            ds_dict['period'] = period
            #
            # -- Get dataset
            dat = ds(**ds_dict)
            # -- Compute climatology
            clim = clim_average(dat,'ANM')
            try:
                cfile(clim)
                #
                ens_dict[CORDEX_domain][exp][member] = clim
            except:
                print 'Error on ',member, dat

# %% cell 18
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

# %% cell 19
ens_dict_per_GWL = dict()
list_of_GWLs = ['1.5','2','4']
CORDEX_domains = [
    # -- Africa
    'AFR-44','AFR-22',
    # -- AustralAsia
    'AUS-44','AUS-22',
    # -- Central America
    'CAM-44','CAM-22',
    # -- North America
    'NAM-44','NAM-22',
    # -- South America
    'SAM-44','SAM-22',
    # -- Asia
    'EAS-44','EAS-22',
    'WAS-44','WAS-22',
    'SEA-22',
    # -- Europe
    'EUR-11',
    
]
for CORDEX_domain in CORDEX_domains:
    ens_dict_per_GWL[CORDEX_domain] = dict()
    for GWL in list_of_GWLs:
        ens_dict_per_GWL[CORDEX_domain][GWL] = dict()

#req_dict = dict(project='tx_individual_models_cmip5_ch12')
for CORDEX_domain in CORDEX_domains:
    for scenario in ['26','85']:
        list_of_models = listing_ens_exp_dict[CORDEX_domain]['rcp'+scenario].keys()
        for member in list_of_models:
            wmodel = member.split('_')[0]
            ok = []
            for GCM in GWL_dict.keys():
                if GCM in wmodel:
                    ok.append(GCM)

            if len(ok)==1:
                GWL_model = ok[0]
                print 'We have : ', wmodel,' for',CORDEX_domain
                print GWL_dict[GWL_model]
                for GWL in list_of_GWLs:
                    if scenario=='26': GWL_scenario = GWL+'_rcp26'
                    if scenario=='85': GWL_scenario = GWL+'_rcp85'

                    # --> file nc
                    # --> period
                    central_year = GWL_dict[GWL_model][GWL_scenario]
                    if central_year not in ['NA','9999'] and float(central_year)>=2014:
                        start_year = str( int(central_year)-9 )
                        end_year = str( int(central_year)+10 )
                        #
                        ds_dict = listing_ens_exp_dict[CORDEX_domain]['rcp'+scenario][member].copy()
                        ds_dict['period'] = start_year+'-'+end_year
                        #
                        # -- Get dataset
                        dat = ds(**ds_dict)
                        # -- Compute climatology
                        clim = clim_average(dat,'ANM')
                        try:
                            cfile(clim)

                            ens_dict_per_GWL[CORDEX_domain][GWL][member] = clim
                        except:
                            print 'Error for ',GWL, member, dat
                        #print cfile(ens_dict_per_GWL[GWL][wmodel+'_'+scenario])
            elif len(ok)>1:
                print 'Multiple models? ',ok
            else:
                print 'We dont have GWL info for ',wmodel

# %% cell 22
ens_dict.keys()

# %% cell 23
AR6regions_by_CORDEX_domain = dict(
    AUS = ['NAU','CAU','EAU','SAU','NZ'],
    SEA = ['SEA'],
    WAS = ['ARP','SAS','WCA'],#,'TIB'],
    EAS = ['TIB','ECA','EAS'],#'SAS'
    CAM = ['NSA','SCA','CAR'],
    SAM = ['NWS','NSA','SAM','NES','SWS','SES','SSA'],
    NAM = ['NWN','NEN','WNA','CNA','ENA','NCA'],#,'GAP'],
    EUR = ['MED','WCE','NEU'],
    AFR = ['WAF','SAH','CAF','WSAF','ESAF','MDG','SEAF','NEAF','ARP']
)

# %% cell 24
# -- Get tracking_id
# -- get version
# -- 
#CORDEX.output.EUR-11.CLMcom.CCCma-CanESM2.historical.r1i1p1
import xarray as xr
def get_tracking_id(ncfile):
    nc = xr.open_dataset(ncfile)
    tracking_id = nc.tracking_id
    nc.close()
    return tracking_id
rows = [['DATA_REF_SYNTAX','MODEL_ID','RCM_VERSION_ID','FREQUENCY','VAR_NAME','VERSION_NO','HANDLE','SUBPANEL']]
for CORDEX_domain in ens_dict.keys():
    short_CORDEX_domain = CORDEX_domain[0:3]
    for exp in [ens_dict[CORDEX_domain].keys()[0]]:
        for mem in ens_dict[CORDEX_domain][exp]:
            try:
                dat = ens_dict[CORDEX_domain][exp][mem].operands[0]
                print dat.baseFiles()
            except:
                dat = ens_dict[CORDEX_domain][exp][mem].operands[0].operands[0]
                print dat.baseFiles()
            ds_kvp = dat.explore('resolve').kvp
            ncfile = dat.baseFiles().split(' ')[0]
            regions = ','.join(AR6regions_by_CORDEX_domain[short_CORDEX_domain])
            try:
                tracking_id = get_tracking_id(ncfile)
            except:
                tracking_id = ''
            dataset_descr = 'CORDEX.output.'+CORDEX_domain+'.'+ds_kvp['institute']+'.'+ds_kvp['driving_model']+'.'+ds_kvp['experiment']+'.'+ds_kvp['realization']+','+ds_kvp['model_version']+','+ds_kvp['frequency']+','+ds_kvp['variable']+','+'version_no'+','+tracking_id+','+regions
            print(dataset_descr)
            rows.append([dataset_descr])

# %% cell 25
dat.baseFiles().split(' ')

# %% cell 26
import csv
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.4/CORDEX_mrso_time_periods.csv'

with open(output_metadata_filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in rows:
        writer.writerow(row)

# %% cell 28
#ens_dict_per_GWL[CORDEX_domain][GWL][member]
rows = [['DATA_REF_SYNTAX','MODEL_ID','RCM_VERSION_ID','FREQUENCY','VAR_NAME','VERSION_NO','HANDLE','SUBPANEL']]
for CORDEX_domain in ens_dict_per_GWL.keys():
    short_CORDEX_domain = CORDEX_domain[0:3]
    mems_15 = ens_dict_per_GWL[CORDEX_domain]['1.5'].keys()
    mems_2 = ens_dict_per_GWL[CORDEX_domain]['2'].keys()
    mems_4 = ens_dict_per_GWL[CORDEX_domain]['4'].keys()
    all_mems = set(mems_15 + mems_2 + mems_4)
    for mem in all_mems:
        tmp_GWL_per_mem = ','
        if mem in mems_15:
            tmp_GWL_per_mem += '1.5,'
            GWL = '1.5'
        else:
            tmp_GWL_per_mem += 'none,'
        if mem in mems_2:
            tmp_GWL_per_mem += '2,'
            GWL = '2'
        else:
            tmp_GWL_per_mem += 'none,'
        if mem in mems_4:
            tmp_GWL_per_mem += '4,'
            GWL = '4'
        else:
            tmp_GWL_per_mem += 'none,'
        try:
            dat = ens_dict_per_GWL[CORDEX_domain][GWL][mem].operands[0]
            print dat.baseFiles()
        except:
            dat = ens_dict_per_GWL[CORDEX_domain][GWL][mem].operands[0].operands[0]
            print dat.baseFiles()
        ds_kvp = dat.explore('resolve').kvp
        ncfile = dat.baseFiles().split(' ')[0]
        try:
            tracking_id = get_tracking_id(ncfile)
        except:
            tracking_id = ''
        regions = ','.join(AR6regions_by_CORDEX_domain[short_CORDEX_domain])
        dataset_descr = 'CORDEX.output.'+CORDEX_domain+'.'+ds_kvp['institute']+'.'+ds_kvp['driving_model']+'.'+ds_kvp['experiment']+'.'+ds_kvp['realization']+','+ds_kvp['model_version']+','+ds_kvp['frequency']+','+ds_kvp['variable']+','+'version_no'+','+tracking_id+tmp_GWL_per_mem+','+regions
        print(dataset_descr)
        rows.append([dataset_descr])

# %% cell 29
import csv
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.4/CORDEX_mrso_GWL.csv'

with open(output_metadata_filename, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in rows:
        writer.writerow(row)

# %% cell 30
#ens_dict_per_GWL[CORDEX_domain][GWL][member]
for CORDEX_domain in [ens_dict_per_GWL.keys()[0]]:
    short_CORDEX_domain = CORDEX_domain[0:3]
    for GWL in [ens_dict_per_GWL[CORDEX_domain].keys()[0]]:
        for mem in ens_dict_per_GWL[CORDEX_domain][GWL]:
            try:
                dat = ens_dict_per_GWL[CORDEX_domain][GWL][mem].operands[0]
                print dat.baseFiles()
            except:
                dat = ens_dict_per_GWL[CORDEX_domain][GWL][mem].operands[0].operands[0]
                print dat.baseFiles()
            ds_kvp = dat.explore('resolve').kvp
            ncfile = dat.baseFiles().split(' ')[1]
            regions = ','.join(AR6regions_by_CORDEX_domain[short_CORDEX_domain])
            print 'CORDEX.output.'+CORDEX_domain+'.'+ds_kvp['institute']+'.'+ds_kvp['driving_model']+'.'+ds_kvp['experiment']+'.'+ds_kvp['realization']+','+ds_kvp['model_version']+','+ds_kvp['frequency']+','+ds_kvp['variable']+','+'version_no'+','+get_tracking_id(ncfile)+','+regions

# %% cell 32
import regionmask
import xarray as xr

def weighted_mean(da, weights, dim):
    """Reduce da by a weighted mean along some dimension(s).

    Parameters
    ----------
    da : DataArray
        Object over which the weighted reduction operation is applied.    
    weights : DataArray
        An array of weights associated with the values in this Dataset.
    dim : str or sequence of str, optional
        Dimension(s) over which to apply the weighted `mean`.
        
    Returns
    -------
    weighted_mean : DataArray
        New DataArray with weighted mean applied to its data and
        the indicated dimension(s) removed.
    """

    weighted_sum = (da * weights).sum(dim=dim, skipna=True)
    # need to mask weights where data is not valid
    masked_weights = weights.where(da.notnull())
    sum_of_weights = masked_weights.sum(dim=dim, skipna=True)
    valid_weights = sum_of_weights != 0
    sum_of_weights = sum_of_weights.where(valid_weights)

    return weighted_sum / sum_of_weights

def average_over_AR6_region(filename, variable, region_name):

    # -- AR6 regions
    #ar6_all = regionmask.defined_regions.ar6.all
    # -- Get the regions
    ar6_land = regionmask.defined_regions.ar6.land

    #ax = ar6_all.plot()
    # -- Get land/sea mask (generic)
    land_110 = regionmask.defined_regions.natural_earth.land_110

    # -- Get data
    ds = xr.open_dataset(filename, decode_times=False)
    dat = ds[variable]
    dat.values = np.array(dat.values, dtype=np.float32)

    # -- Mask the data
    mask_3D = ar6_land.mask_3D(dat) # AR6 mask
    land_mask = land_110.mask_3D(dat) # Land sea mask
    mask_lsm = mask_3D * land_mask.squeeze(drop=True) # Combine the two

    weights = np.cos(np.deg2rad(dat.lat))
    
    if region_name=='all':
        tmp = weighted_mean(dat, mask_lsm * weights, ("lon", "lat"))
        tmp['abbrevs'] = mask_3D.abbrevs
        return tmp
    else:
        if isinstance(region_name, list):
            res = list()
            for region in region_name:
                region_mask = mask_lsm.isel(region=list(mask_3D.abbrevs).index(region))
                dat_region = dat.where(region_mask)
                weights_region = weights.where(region_mask)
                res.append( weighted_mean(dat_region, region_mask*weights_region, ("lon","lat")) )
            return res
        else:
            region_mask = mask_lsm.isel(region=list(mask_3D.abbrevs).index(region_name))
            dat_region = dat.where(region_mask)
            weights_region = weights.where(region_mask)            
            return weighted_mean(dat_region, region_mask*weights_region, ("lon","lat"))

# %% cell 34
ens_dict[CORDEX_domain][exp][member] = clim

# %% cell 35
# -- Merge the dictionary with scenarios and the one with the GWLs
#ens_CORDEX = ens_exp_dict_CORDEX.copy()
#ens_CORDEX.update(ens_GWL_dict_CORDEX)

AR6regions_by_CORDEX_domain = dict(
    AUS = ['NAU','CAU','EAU','SAU','NZ'],
    SEA = ['SEA'],
    WAS = ['ARP','SAS','WCA'],#,'TIB'],
    EAS = ['TIB','ECA','EAS'],#'SAS'
    CAM = ['NSA','SCA','CAR'],
    SAM = ['NWS','NSA','SAM','NES','SWS','SES','SSA'],
    NAM = ['NWN','NEN','WNA','CNA','ENA','NCA'],#,'GAP'],
    EUR = ['MED','WCE','NEU'],
    AFR = ['WAF','SAH','CAF','WSAF','ESAF','MDG','SEAF','NEAF','ARP']
)

#ens_dict[CORDEX_domain][exp][member] = clim
#ens_dict_per_GWL[CORDEX_domain][GWL][member]

regional_averages_diff = dict()
#for CORDEX_domain in ['NAM-44','NAM-22','EUR-11']:
for CORDEX_domain in ens_dict.keys():
    
    short_CORDEX_domain = CORDEX_domain[0:3]
    #if short_CORDEX_domain not in regional_averages_diff:
    #    regional_averages_diff[short_CORDEX_domain] = dict()
    
    for ens_CORDEX in [ens_dict[CORDEX_domain], ens_dict_per_GWL[CORDEX_domain]]:
        
        # -- Loop on experiments / horizons
        for clim_period in ens_CORDEX:
            if 'baseline' not in clim_period:
                print clim_period
                #if clim_period not in regional_averages_diff[short_CORDEX_domain]:
                #    regional_averages_diff[short_CORDEX_domain][clim_period] = dict()
                if clim_period not in regional_averages_diff:
                    regional_averages_diff[clim_period] = dict()

                # -- Loop on the members of each ensemble
                for mem in ens_CORDEX[clim_period]:
                    if mem in ens_dict[CORDEX_domain]['baseline']:
                        #if 'CCCma-CanESM2--UCAN-WRF341I' not in mem:
                        print mem
                        # -- Compute the averages for each AR6 region thanks to regionmask
                        # --> We regrid on a 0.25° grid with conservative regridding
                        tmp = average_over_AR6_region(
                                    cfile(regridn(ens_CORDEX[clim_period][mem], cdogrid='r1440x720', option='remapbil')),
                                    'mrso', 'all')
                        tmp_baseline = average_over_AR6_region(
                                    cfile(regridn(ens_dict[CORDEX_domain]['baseline'][mem], cdogrid='r1440x720', option='remapbil')),
                                    'mrso', 'all')
                        region_names = tmp.abbrevs
                        for region_name in AR6regions_by_CORDEX_domain[short_CORDEX_domain]:
                            print region_name
                            region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name))[0].values)
                            region_value_baseline = float(tmp_baseline.sel(region=list(tmp.abbrevs).index(region_name))[0].values)
                            if region_value_baseline==0:
                                if region_value==0:
                                    perc_val = 0
                                else:
                                    perc_val = float('nan')
                            else:
                                perc_val = 100*(region_value - region_value_baseline)/region_value_baseline
                            #if region_name not in regional_averages_diff[short_CORDEX_domain][clim_period]:
                            #    regional_averages_diff[short_CORDEX_domain][clim_period][region_name] = [perc_val]
                            #else:
                            #    regional_averages_diff[short_CORDEX_domain][clim_period][region_name].append(perc_val)
                            if region_name not in regional_averages_diff[clim_period]:
                                regional_averages_diff[clim_period][region_name] = [perc_val]
                            else:
                                regional_averages_diff[clim_period][region_name].append(perc_val)

# %% cell 36
ens_dict['NAM-44']

# %% cell 37
regional_averages_diff['1.5']

# %% cell 38
quantiles_dict = dict()
for clim_period in regional_averages_diff:
    if clim_period not in quantiles_dict:
        quantiles_dict[clim_period] = dict()
    for region_name in regional_averages_diff[clim_period]:
        print clim_period, region_name
        #quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages_diff[clim_period][region_name])
        wdat = dat[~np.isnan(dat)]
        if len(wdat)>=5:
            q10 = np.quantile(wdat, 0.1)
            q50 = np.quantile(wdat, 0.5)
            q90 = np.quantile(wdat, 0.9)
            quantiles_dict[clim_period][region_name] = [q10, q50, q90]
        else:
            quantiles_dict[clim_period][region_name] = [-99999, -99999, -99999]

# %% cell 39
import json
ensemble = 'CORDEX'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.4/'+ensemble+'_SM_diff_perc2020_AR6_regional_averages.json'
print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 40
float('nan')

# %% cell 41
# Merge -22 et -44

regional_averages_CORDEX = dict()
ens_exp_dict_CORDEX = dict()
for short_CORDEX_domain in AR6regions_by_CORDEX_domain:
    if short_CORDEX_domain=='EUR':
        regional_averages_CORDEX[short_CORDEX_domain] = regional_averages_diff['EUR-11'].copy()
    else:
        regional_averages_CORDEX[short_CORDEX_domain] = dict()
        if short_CORDEX_domain+'-22' in regional_averages_diff and short_CORDEX_domain+'-44' in regional_averages_diff :
            for clim_period in regional_averages_diff[short_CORDEX_domain+'-22']:
                regional_averages_CORDEX[short_CORDEX_domain][clim_period] = dict()
                for region_name in regional_averages_diff[short_CORDEX_domain+'-22'][clim_period]:
                    regional_averages_CORDEX[short_CORDEX_domain][clim_period][region_name] = regional_averages_diff[short_CORDEX_domain+'-22'][clim_period][region_name] + regional_averages_diff[short_CORDEX_domain+'-44'][clim_period][region_name]
        else:
            if short_CORDEX_domain+'-22' in regional_averages_diff:
                regional_averages_CORDEX[short_CORDEX_domain] = regional_averages_diff[short_CORDEX_domain+'-22'].copy()
            if short_CORDEX_domain+'-44' in regional_averages_diff:
                regional_averages_CORDEX[short_CORDEX_domain] = regional_averages_diff[short_CORDEX_domain+'-44'].copy()

# %% cell 42
regional_averages_CORDEX = region_averages_diff

# %% cell 43
quantiles_dict = dict()
for short_CORDEX_domain in regional_averages_CORDEX:
    for clim_period in regional_averages_CORDEX[short_CORDEX_domain]:
        if clim_period not in quantiles_dict:
            quantiles_dict[clim_period] = dict()
        for region_name in regional_averages_CORDEX[short_CORDEX_domain][clim_period]:
            print clim_period, region_name
            #quantiles_dict[clim_period][region_name] = dict()
            dat = np.array(regional_averages_CORDEX[short_CORDEX_domain][clim_period][region_name])
            wdat = dat[~np.isnan(dat)]
            q10 = np.quantile(wdat, 0.1)
            q50 = np.quantile(wdat, 0.5)
            q90 = np.quantile(wdat, 0.9)
            quantiles_dict[clim_period][region_name] = [q10, q50, q90]

# %% cell 44
import json
ensemble = 'CORDEX'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.4/'+ensemble+'_SM_diff_AR6_regional_averages.json'
print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 48
iplot_members(diff, proj='Robinson', N=3, color='MPL_BrBg',
              min=-0.3, max=0.3, delta=0.05, focus='land')

# %% cell 54
import regionmask
import xarray as xr

def weighted_mean(da, weights, dim):
    """Reduce da by a weighted mean along some dimension(s).

    Parameters
    ----------
    da : DataArray
        Object over which the weighted reduction operation is applied.    
    weights : DataArray
        An array of weights associated with the values in this Dataset.
    dim : str or sequence of str, optional
        Dimension(s) over which to apply the weighted `mean`.
        
    Returns
    -------
    weighted_mean : DataArray
        New DataArray with weighted mean applied to its data and
        the indicated dimension(s) removed.
    """

    weighted_sum = (da * weights).sum(dim=dim, skipna=True)
    # need to mask weights where data is not valid
    masked_weights = weights.where(da.notnull())
    sum_of_weights = masked_weights.sum(dim=dim, skipna=True)
    valid_weights = sum_of_weights != 0
    sum_of_weights = sum_of_weights.where(valid_weights)

    return weighted_sum / sum_of_weights

def average_over_AR6_region_back(filename, variable, region_name):

    # -- AR6 regions
    #ar6_all = regionmask.defined_regions.ar6.all
    # -- Get the regions
    ar6_land = regionmask.defined_regions.ar6.land

    #ax = ar6_all.plot()
    # -- Get land/sea mask (generic)
    land_110 = regionmask.defined_regions.natural_earth.land_110

    # -- Get data
    ds = xr.open_dataset(filename, decode_times=False)
    dat = ds[variable]
    dat.values = np.array(dat.values, dtype=np.float32)

    # -- Mask the data
    mask_3D = ar6_land.mask_3D(dat) # AR6 mask
    land_mask = land_110.mask_3D(dat) # Land sea mask
    mask_lsm = mask_3D * land_mask.squeeze(drop=True) # Combine the two

    weights = np.cos(np.deg2rad(dat.lat))
    
    if region_name=='all':
        return weighted_mean(dat, mask_lsm * weights, ("lon", "lat"))
    else:
        if isinstance(region_name, list):
            res = list()
            for region in region_name:
                region_mask = mask_lsm.isel(region=list(mask_3D.abbrevs).index(region))
                dat_region = dat.where(region_mask)
                weights_region = weights.where(region_mask)
                res.append( weighted_mean(dat_region, region_mask*weights_region, ("lon","lat")) )
            return res
        else:
            region_mask = mask_lsm.isel(region=list(mask_3D.abbrevs).index(region_name))
            dat_region = dat.where(region_mask)
            weights_region = weights.where(region_mask)            
            return weighted_mean(dat_region, region_mask*weights_region, ("lon","lat"))
    
def average_over_AR6_region(filename, variable, region_name):

    # -- AR6 regions
    #ar6_all = regionmask.defined_regions.ar6.all
    # -- Get the regions
    ar6_land = regionmask.defined_regions.ar6.land

    #ax = ar6_all.plot()
    # -- Get land/sea mask (generic)
    land_110 = regionmask.defined_regions.natural_earth.land_110

    # -- Get data
    ds = xr.open_dataset(filename, decode_times=False)
    dat = ds[variable]
    dat.values = np.array(dat.values, dtype=np.float32)

    # -- Mask the data
    mask_3D = ar6_land.mask_3D(dat) # AR6 mask
    land_mask = land_110.mask_3D(dat) # Land sea mask
    mask_lsm = mask_3D * land_mask.squeeze(drop=True) # Combine the two
    
    # -- Compute weights
    if dat.lat.shape == dat.shape:
        weights = np.cos(np.deg2rad(dat.lat))
    else:
        # -- Case dat is has time dim
        if 'time' in dat.dims:
            matlat = np.mean(dat.values, axis=dat.dims.index('time')) * 0
        else:
            matlat = dat.values * 0

        if dat.dims.index('lat')<dat.dims.index('lon'):
            for i in range(0,dat.shape[dat.dims.index('lon')]):
                matlat[:,i] = dat.lat
        else:
            for i in range(0,dat.shape[dat.dims.index('lon')]):
                matlat[i,:] = dat.lat
    
        weights = np.cos(np.deg2rad(matlat))
    
    if region_name=='all':
        return weighted_mean(dat, mask_lsm * weights, ("lon", "lat"))
    else:
        if isinstance(region_name, list):
            res = list()
            for region in region_name:
                region_mask = mask_lsm.isel(region=list(mask_3D.abbrevs).index(region))
                dat_region = dat.where(region_mask)
                weights_region = np.where(region_mask, weights, float("nan"))
                #weights_region = weights.where(region_mask)
                res.append( weighted_mean(dat_region, region_mask*weights_region, ("lon","lat")) )
            return res
        else:
            region_mask = mask_lsm.isel(region=list(mask_3D.abbrevs).index(region_name))
            dat_region = dat.where(region_mask)
            weights_region = np.where(region_mask, weights, float("nan"))
            #weights_region = weights.where(region_mask)            
            return weighted_mean(dat_region, region_mask*weights_region, ("lon","lat"))
#
def regions_contained(lon, lat, regions):

    # determine if the longitude needs to be wrapped
    regions_is_180 = regions.lon_180
    grid_is_180 = regionmask.core.utils._is_180(lon.min(), lon.max())

    wrap_lon = not regions_is_180 == grid_is_180

    lon_orig = lon.copy()
    if wrap_lon:
        lon = regionmask.core.utils._wrapAngle(lon, wrap_lon)

    lon = np.asarray(lon).squeeze()
    lat = np.asarray(lat).squeeze()

    if lon.ndim == 1 and lat.ndim == 1:
        poly = shapely.geometry.box(lon.min(), lat.min(), lon.max(), lat.max())

    # convex_hull is not really what we need
    # https://gist.github.com/dwyerk/10561690
    #     elif lon.ndim == 2 and lat.ndim == 2:
    #         # get the convex hull from all points
    #         lonlat = np.stack([lon.ravel(), lat.ravel()], axis=1)
    #         multipoint = shapely.geometry.MultiPoint(lonlat)
    #         poly = multipoint.convex_hull
    else:
        raise ValueError("Cannot currently handle 2D coordinates")

    fully_contained = list()
    for region_poly in regions.polygons:
        res = poly.contains(region_poly)

        fully_contained.append(res)

    return xr.DataArray(
        fully_contained, dims=["region"], coords=dict(region=regions.numbers)
    )

if None:
    region_name = "all"
    variable = 'tx35'
    filename = "/data/jservon/IPCC/tx35/individual_models/CMIP6_ssp585_tx35_2100_NorESM2-LM_r1i1p1f1.nc"

    tmp = average_over_AR6_region(filename, variable, region_name)
    tmp

# %% cell 56
if None:
    regional_averages_CMIP5 = dict()

    # -- Loop on experiments / horizons
    #wind_ens_clim_exp_dict[exp]
    for ens_exp in ens_clim_exp_dict:
        print ens_exp
        regional_averages_CMIP5[ens_exp] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_clim_exp_dict[ens_exp]:
            print mem
            # -- Compute the averages for each AR6 region thanks to regionmask
            tmp = average_over_AR6_region(cfile(ens_clim_exp_dict[ens_exp][mem]), 'mrso', 'all')
            region_names = tmp.abbrevs
            for tmp_region_name in region_names:
                region_name = str(tmp_region_name.values)
                #print region_name
                region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                if region_name not in regional_averages_CMIP5[ens_exp]:
                    regional_averages_CMIP5[ens_exp][region_name] = [region_value]
                else:
                    regional_averages_CMIP5[ens_exp][region_name].append(region_value)
    #
regional_averages_CMIP5 = dict()

# -- Loop on experiments / horizons
for ens_exp in ens_clim_exp_dict:
    print ens_exp
    regional_averages_CMIP5[ens_exp] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_clim_exp_dict[ens_exp]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        tmp = average_over_AR6_region(cfile(ens_clim_exp_dict[ens_exp][mem]), 'mrso', 'all')
        region_names = list(tmp.abbrevs)
        ttmp = average_over_AR6_region(cfile(ens_clim_exp_dict[ens_exp][mem]), 'mrso', region_names)
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            region_value = float(ttmp[list(tmp.abbrevs).index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages_CMIP5[ens_exp]:
                regional_averages_CMIP5[ens_exp][region_name] = [region_value]
            else:
                regional_averages_CMIP5[ens_exp][region_name].append(region_value)
#

# %% cell 57
ens_clim_exp_dict[ens_exp].keys()

# %% cell 58
CMCC-CMS 77
MIROC-ESM 2600


ACCESS1-0
ACCESS1-3
FGOALS-g2
CMCC-CMS
MIROC-ESM
HadGEM2-ES
CMCC-CM
FGOALS-s2
MPI-ESM-MR
CSIRO-Mk3-6-0
CESM1-BGC
HadGEM2-AO
inmcm4
CanESM2
GISS-E2-R-CC
BNU-ESM
IPSL-CM5B-LR
GFDL-ESM2G
MRI-CGCM3
GFDL-ESM2M
CCSM4
NorESM1-M
IPSL-CM5A-MR
IPSL-CM5A-LR
GFDL-CM3
CNRM-CM5
GISS-E2-H
MIROC-ESM-CHEM
MRI-ESM1
NorESM1-ME
MIROC5
GISS-E2-R
HadGEM2-CC
GISS-E2-H-CC
CMCC-CESM
bcc-csm1-1-m
MPI-ESM-LR
bcc-csm1-1
CESM1-CAM5

# %% cell 61
ens_baseline_dict.keys()

# %% cell 62
regional_averages_diff_CMIP5 = dict()
# -- Loop on experiments / horizons
#wind_ens_clim_exp_dict[exp]
for ens_exp in ens_clim_exp_dict:
    if ens_exp not in ['baseline']:
        print ens_exp
        regional_averages_diff_CMIP5[ens_exp] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_clim_exp_dict[ens_exp]:
            if mem.split('_')[0] in ens_baseline_dict:
                print mem
                # -- Compute the averages for each AR6 region thanks to regionmask
                tmp = average_over_AR6_region(cfile(ens_clim_exp_dict[ens_exp][mem]), 'mrso', 'all')
                region_names = list(tmp.abbrevs)
                ttmp = average_over_AR6_region(cfile(ens_clim_exp_dict[ens_exp][mem]), 'mrso', region_names)
                ttmp_baseline = average_over_AR6_region(cfile(ens_clim_exp_dict['baseline'][mem]), 'mrso', region_names)
                for tmp_region_name in region_names:
                    region_name = str(tmp_region_name.values)
                    region_value = float(ttmp[list(tmp.abbrevs).index(region_name)])
                    region_value_baseline = float(ttmp_baseline[list(tmp.abbrevs).index(region_name)])
                    if region_value_baseline==0:
                        if region_value==0:
                            perc_val = 0
                        else:
                            perc_val = -99999
                    else:
                        perc_val = 100*(region_value - region_value_baseline)/region_value_baseline
                    if region_name not in regional_averages_diff_CMIP5[ens_exp]:
                        regional_averages_diff_CMIP5[ens_exp][region_name] = [perc_val]
                    else:
                        regional_averages_diff_CMIP5[ens_exp][region_name].append(perc_val)
#
if None:
    regional_averages_diff_CMIP5 = dict()
    # -- Loop on experiments / horizons
    #wind_ens_clim_exp_dict[exp]
    for ens_exp in ens_clim_exp_dict:
        if ens_exp not in ['baseline']:
            print ens_exp
            regional_averages_diff_CMIP5[ens_exp] = dict()
            # -- Loop on the members of each ensemble
            for mem in ens_clim_exp_dict[ens_exp]:
                if mem.split('_')[0] in ens_baseline_dict:
                    print mem
                    # -- Compute the averages for each AR6 region thanks to regionmask
                    tmp = average_over_AR6_region(cfile(ens_clim_exp_dict[ens_exp][mem]), 'mrso', 'all')
                    tmp_baseline = average_over_AR6_region(cfile(ens_clim_exp_dict['baseline'][mem]), 'mrso', 'all')
                    region_names = tmp.abbrevs
                    for tmp_region_name in region_names:
                        region_name = str(tmp_region_name.values)
                        #print region_name
                        region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                        region_value_baseline = float(tmp_baseline.sel(region=list(tmp.abbrevs).index(region_name)).values)
                        if region_value_baseline==0:
                            if region_value==0:
                                perc_val = 0
                            else:
                                perc_val = -99999
                        else:
                            perc_val = 100*(region_value - region_value_baseline)/region_value_baseline
                        if region_name not in regional_averages_diff_CMIP5[ens_exp]:
                            regional_averages_diff_CMIP5[ens_exp][region_name] = [perc_val]
                        else:
                            regional_averages_diff_CMIP5[ens_exp][region_name].append(perc_val)
            #

# %% cell 64
if None:
    for GWL in ens_dict_per_GWL :
        print GWL
        regional_averages_CMIP5[GWL] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_dict_per_GWL[GWL]:
            print mem
            # -- Compute the averages for each AR6 region thanks to regionmask
            tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'mrso', 'all')
            region_names = list(tmp.abbrevs)
            ttmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'mrso', region_names)
            for tmp_region_name in region_names:
                region_name = str(tmp_region_name.values)
                region_value = float(ttmp[list(tmp.abbrevs).index(region_name)])
                print region_name, region_value
                if region_name not in regional_averages_CMIP5[GWL]:
                    regional_averages_CMIP5[GWL][region_name] = [region_value]
                else:
                    regional_averages_CMIP5[GWL][region_name].append(region_value)

if None:
    for GWL in ens_dict_per_GWL:
        print GWL
        regional_averages_CMIP5[GWL] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_dict_per_GWL[GWL]:
            print mem
            # -- Compute the averages for each AR6 region thanks to regionmask
            tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'mrso', 'all')
            region_names = tmp.abbrevs
            for tmp_region_name in region_names:
                region_name = str(tmp_region_name.values)
                #print region_name
                region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                if region_name not in regional_averages_CMIP5[GWL]:
                    regional_averages_CMIP5[GWL][region_name] = [region_value]
                else:
                    regional_averages_CMIP5[GWL][region_name].append(region_value)

# %% cell 66
for GWL in ens_dict_per_GWL:
    print GWL
    regional_averages_diff_CMIP5[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_dict_per_GWL[GWL]:
        wmem = mem.replace('_26','').replace('_85','')
        print wmem
        if wmem in ens_baseline_dict:
            print mem
            tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'mrso', 'all')
            region_names = list(tmp.abbrevs)
            ttmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'mrso', region_names)
            ttmp_baseline = average_over_AR6_region(cfile(ens_clim_exp_dict['baseline'][wmem]), 'mrso', region_names)
            for tmp_region_name in region_names:
                region_name = str(tmp_region_name.values)
                region_value = float(ttmp[region_names.index(region_name)])
                region_value_baseline = float(ttmp_baseline[region_names.index(region_name)])
                if region_value_baseline==0:
                    if region_value==0:
                        perc_val = 0
                    else:
                        perc_val = -99999
                else:
                    perc_val = 100*(region_value - region_value_baseline)/region_value_baseline
                if region_name not in regional_averages_diff_CMIP5[GWL]:
                    regional_averages_diff_CMIP5[GWL][region_name] = [perc_val]
                else:
                    regional_averages_diff_CMIP5[GWL][region_name].append(perc_val)


if None:
    for GWL in ens_dict_per_GWL:
        print GWL
        regional_averages_diff_CMIP5[GWL] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_dict_per_GWL[GWL]:
            wmem = mem.replace('_26','').replace('_85','')
            print wmem
            if wmem in ens_baseline_dict:
                print mem
                # -- Compute the averages for each AR6 region thanks to regionmask
                tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'mrso', 'all')
                tmp_baseline = average_over_AR6_region(cfile(ens_clim_exp_dict['baseline'][wmem]), 'mrso', 'all')
                region_names = tmp.abbrevs
                for tmp_region_name in region_names:
                    region_name = str(tmp_region_name.values)
                    #print region_name
                    region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                    region_value_baseline = float(tmp_baseline.sel(region=list(tmp.abbrevs).index(region_name)).values)
                    if region_value_baseline==0:
                        if region_value==0:
                            perc_val = 0
                        else:
                            perc_val = -99999
                    else:
                        perc_val = 100*(region_value - region_value_baseline)/region_value_baseline
                    if region_name not in regional_averages_diff_CMIP5[GWL]:
                        regional_averages_diff_CMIP5[GWL][region_name] = [perc_val]
                    else:
                        regional_averages_diff_CMIP5[GWL][region_name].append(perc_val)

# %% cell 68
quantiles_dict = dict()
for clim_period in regional_averages_CMIP5:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages_CMIP5[clim_period]:
        print clim_period, region_name
        quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages_CMIP5[clim_period][region_name])
        q10 = np.quantile(dat, 0.1)
        q50 = np.quantile(dat, 0.5)
        q90 = np.quantile(dat, 0.9)
        quantiles_dict[clim_period][region_name] = [q10, q50, q90]

import json
ensemble = 'CMIP5'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.4/'+ensemble+'_SM_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 69
quantiles_dict = dict()
for clim_period in regional_averages_diff_CMIP5:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages_diff_CMIP5[clim_period]:
        print clim_period, region_name
        quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages_diff_CMIP5[clim_period][region_name])
        q10 = np.quantile(dat, 0.1)
        q50 = np.quantile(dat, 0.5)
        q90 = np.quantile(dat, 0.9)
        quantiles_dict[clim_period][region_name] = [q10, q50, q90]

import json
ensemble = 'CMIP5'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.4/'+ensemble+'_SM_diff_perc2020_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)
