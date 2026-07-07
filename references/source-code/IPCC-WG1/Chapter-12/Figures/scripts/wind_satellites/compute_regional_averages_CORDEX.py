import regionmask
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import json
import glob

CWD = os.getcwd()


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

GWL_csv = CWD+'/../../scripts/ATLAS/warming-levels/CMIP5_Atlas_WarmingLevels.csv'


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
#

# -- Add EUR
# ----------------------------------------------------------
clog('critical')
pattern = '/data/jservon/IPCC/WSPD/${experiment}/sfcWind.${member}.${clim_period}.nc'
cproject('wind_individual_models_EURO_cordex_ch12',('CORDEX_domain','EUR'),'experiment',('period','fx'),'clim_period','member',('variable','sfcWind'), ensemble=['member'], separator='%')
dataloc(project='wind_individual_models_EURO_cordex_ch12', url=pattern)    

# -- Clim periods
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

# -- GWLs
all_CORDEX_domains_ens_dict_per_GWL['EUR'] = dict()

for gwl in ['1.5', '2', '4']:    
    req = ds(project = 'wind_individual_models_EURO_cordex_ch12',
              clim_period = 'gwl'+gwl.replace('.',''),
              member = '*',
              experiment = '*'
             )
    all_CORDEX_domains_ens_dict_per_GWL['EUR'][gwl] = req.explore('ensemble')


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


#
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
    if dat.lat.shape == dat.shape or region_name=='all':
        weights = np.cos(np.deg2rad(dat.lat))
        tmp = weighted_mean(dat, mask_lsm * weights, ("lon", "lat"))
        tmp['abbrevs'] = mask_3D.abbrevs
        return tmp
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

regional_averages_diff = dict()
for CORDEX_domain in all_CORDEX_domains_ens_exp_dict.keys():
    
    short_CORDEX_domain = CORDEX_domain[0:3]
    
    for ens_CORDEX in [all_CORDEX_domains_ens_exp_dict[CORDEX_domain],
                       all_CORDEX_domains_ens_dict_per_GWL[CORDEX_domain]]:
                
        # -- Loop on experiments / horizons
        for clim_period in ens_CORDEX:
            if 'baseline' not in clim_period:
                print clim_period
                if clim_period not in regional_averages_diff:
                    regional_averages_diff[clim_period] = dict()

                # -- Loop on the members of each ensemble
                for mem in ens_CORDEX[clim_period]:
                    wmem = mem.replace('_85','').replace('_26','')
                    if wmem in all_CORDEX_domains_ens_exp_dict[CORDEX_domain]['baseline']:
                        if CORDEX_domain == 'EUR':
                            variable = 'sfcWind'
                        else:
                            variable = 'wind'
                        print wmem, CORDEX_domain
                        # -- Compute the averages for each AR6 region thanks to regionmask
                        # --> We regrid on a 0.25 grid with conservative regridding
                        tmp = average_over_AR6_region(
                                    cfile(regridn(ens_CORDEX[clim_period][mem], cdogrid='r1440x720', option='remapbil')),
                                    variable, 'all')
                        tmp_baseline = average_over_AR6_region(
                                    cfile(regridn(all_CORDEX_domains_ens_exp_dict[CORDEX_domain]['baseline'][wmem], cdogrid='r1440x720', option='remapbil')),
                                    variable, 'all')
                        region_names = tmp.abbrevs
                        for region_name in AR6regions_by_CORDEX_domain[short_CORDEX_domain]:
                            print region_name
                            region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name))[0].values)
                            region_value_baseline = float(tmp_baseline.sel(region=list(tmp.abbrevs).index(region_name))[0].values)
                            print region_value, region_value_baseline
                            if region_value_baseline==0:
                                if region_value==0:
                                    perc_val = 0
                                else:
                                    perc_val = float('nan')
                            else:
                                perc_val = 100*(region_value - region_value_baseline)/region_value_baseline
                            if region_name not in regional_averages_diff[clim_period]:
                                regional_averages_diff[clim_period][region_name] = [perc_val]
                            else:
                                regional_averages_diff[clim_period][region_name].append(perc_val)

                        
                        
quantiles_dict = dict()
for clim_period in regional_averages_diff:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages_diff[clim_period]:
        print clim_period, region_name
        quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages_diff[clim_period][region_name])
        wdat = dat[~np.isnan(dat)]
        if len(wdat)>=5:
            q10 = np.quantile(wdat, 0.1)
            q50 = np.quantile(wdat, 0.5)
            q90 = np.quantile(wdat, 0.9)
            quantiles_dict[clim_period][region_name] = [q10, q50, q90]
        else:
            quantiles_dict[clim_period][region_name] = [-99999, -99999, -99999]

import json

ensemble = 'CORDEX'
outfilename = CWD+'/../../data/Figure_S12.5/'+ensemble+'_sfcWind_diff-perc-baseline_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)
