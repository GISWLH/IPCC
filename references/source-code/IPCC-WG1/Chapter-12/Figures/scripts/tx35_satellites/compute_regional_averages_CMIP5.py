import regionmask
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import json
import glob

CWD = os.getcwd()

from climaf.api import *

pattern = '/data/jservon/IPCC/tx35/bias_corrected/individual_models/CMIP5_${experiment}_${variable}_${period}_${member}.nc'
cproject('tx_individual_models_cmip5_ch12','experiment','period','member',('variable','tx35isimip'), ensemble=['member'], separator='%')
dataloc(project='tx_individual_models_cmip5_ch12', url=pattern)    

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


ens_exp_dict = dict()
lom_per_exp = dict()
for exp in exp_dict_list:
    print exp
    
    experiment = exp_dict_list[exp]['experiment']
    period = exp_dict_list[exp]['period']

    req = ds(experiment=experiment,
             period=period,
             member='*',
             project='tx_individual_models_cmip5_ch12')

    ens_exp = req.explore('ensemble')
    #
    # -- Climatologies
    clim_exp      = clim_average(ccdo(ens_exp, operator='yearsum'), 'ANM')
    
    lom_per_exp[exp] = clim_exp.keys()

    # -- Changes = Scenario minus baselines
    ens_exp_dict[exp] = clim_exp

    
lom_baseline     = lom_per_exp['baseline']
lom_baseline_ext = lom_per_exp['baseline_ext']
print 'Models not in both sets:'
print set(lom_baseline) ^ set(lom_baseline_ext)
print 'Models in common:'
common_lom_baseline = list( set(lom_baseline) & set(lom_baseline_ext) )
print common_lom_baseline



req_dict = dict(project='tx_individual_models_cmip5_ch12')
wreq_dict = req_dict.copy()
wreq_dict.update(exp_dict_list['baseline'])
ens_baseline_hist = eds(member=common_lom_baseline,
                        **wreq_dict
                       )

wreq_dict = req_dict.copy()
wreq_dict.update(exp_dict_list['baseline_ext'])
ens_baseline_ext = eds(member=common_lom_baseline,
                       **wreq_dict
                      )
ens_baseline_dict = dict()
for mem in ens_baseline_hist:
    ens_baseline_dict[mem] = ccdo2(ens_baseline_hist[mem], ens_baseline_ext[mem], operator='cat')

# -- Add to the list of ensembles
ens_baseline = cens(ens_baseline_dict)
ens_exp_dict['baseline'] = clim_average(ccdo(ens_baseline, operator='yearsum'), 'ANM')

ens_exp_dict.pop('baseline_ext')


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
ens_dict_per_GWL = dict()
list_of_GWLs = ['1.5','2','3','4']

for GWL in list_of_GWLs:
    ens_dict_per_GWL[GWL] = dict()

req_dict = dict(project='tx_individual_models_cmip5_ch12')

for scenario in ['26','85']:
    list_of_models = ens_exp_dict['rcp'+scenario+'_far'].keys()
    for wmodel_realization in list_of_models:
        wmodel = wmodel_realization.split('_')[0]
        if wmodel in GWL_dict:
            print 'We have : ', wmodel
            print GWL_dict[wmodel]
            for GWL in list_of_GWLs:
                if scenario=='26': GWL_scenario = GWL+'_rcp26'
                if scenario=='85': GWL_scenario = GWL+'_rcp85'

                # --> file nc
                # --> period
                central_year = GWL_dict[wmodel][GWL_scenario]
                if central_year not in ['NA','9999'] and float(central_year)>=2024:
                    start_year = str( int(central_year)-9 )
                    end_year = str( int(central_year)+10 )
                    
                    dat = ds(member = wmodel_realization,
                             experiment = 'rcp'+scenario,
                             period=start_year+'-'+end_year,
                             **req_dict
                             )
                    ens_dict_per_GWL[GWL][wmodel_realization+'_'+scenario] = clim_average(ccdo(dat, operator='yearsum'), 'ANM')
                    print cfile(ens_dict_per_GWL[GWL][wmodel_realization+'_'+scenario])
        else:
            print 'We dont have GWL info for ',wmodel
#



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
    

regional_averages = dict()

# -- Loop on experiments / horizons
for ens_exp in ens_exp_dict:
    print ens_exp
    regional_averages[ens_exp] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_exp_dict[ens_exp]:
        print mem
        tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'tx35isimip', 'all')
        region_names = list(tmp.abbrevs)
        ttmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'tx35isimip', region_names)
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            region_value = float(ttmp[list(tmp.abbrevs).index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[ens_exp]:
                regional_averages[ens_exp][region_name] = [region_value]
            else:
                regional_averages[ens_exp][region_name].append(region_value)


for GWL in ens_dict_per_GWL :
    print GWL
    regional_averages[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_dict_per_GWL[GWL]:
        print mem
        tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'tx35isimip', 'all')
        region_names = list(tmp.abbrevs)
        ttmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'tx35isimip', region_names)
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            region_value = float(ttmp[list(tmp.abbrevs).index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[GWL]:
                regional_averages[GWL][region_name] = [region_value]
            else:
                regional_averages[GWL][region_name].append(region_value)
#




quantiles_dict = dict()
for clim_period in regional_averages:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages[clim_period]:
        print clim_period, region_name
        quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages[clim_period][region_name])
        q10 = np.quantile(dat, 0.1)
        q50 = np.quantile(dat, 0.5)
        q90 = np.quantile(dat, 0.9)
        quantiles_dict[clim_period][region_name] = [q10, q50, q90]

import json

ensemble = 'CMIP5'
outfilename = CWD+'/../../data/Figure_S12.1/'+ensemble+'_tx35isimip_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)
