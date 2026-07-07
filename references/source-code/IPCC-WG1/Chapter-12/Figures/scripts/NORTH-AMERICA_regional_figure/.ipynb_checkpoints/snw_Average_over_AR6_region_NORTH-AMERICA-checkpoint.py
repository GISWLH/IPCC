# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/NORTH-AMERICA_regional_figure/.ipynb_checkpoints/snw_Average_over_AR6_region_NORTH-AMERICA-checkpoint.ipynb

# %% cell 2
import regionmask
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import json
import glob

CWD = os.getcwd()

# %% cell 4
ndays = '14'

# %% cell 6
from climaf.api import *

# %% cell 8
pattern = '/data/ciles/IPCC/FGD/snow/final/cmip6/time_periods/${model}_${experiment}_snw100seas_${clim_period}_MEAN.1deg.nc'
cproject('snw_cmip6_ch12','experiment',('period','fx'), 'model', 'clim_period', ('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='snw_cmip6_ch12', url=pattern)
pattern_gwl = '/data/ciles/IPCC/FGD/snow/final/cmip6/GWLs/${model}_${GWL}.nc'
cproject('snw_cmip6_GWL_ch12','model',('period','fx'),'GWL',('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='snw_cmip6_GWL_ch12', url=pattern_gwl)

# %% cell 9
# -- CMIP5
pattern = '/data/ciles/IPCC/FGD/snow/final/cmip5/time_periods/${model}_${experiment}_snw100seas_${clim_period}_MEAN.2deg.nc'
cproject('snw_cmip5_ch12','experiment',('period','fx'), 'model', 'clim_period', ('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='snw_cmip5_ch12', url=pattern)
pattern_gwl = '/data/ciles/IPCC/FGD/snow/final/cmip5/GWLs/${model}_${GWL}.nc'
cproject('snw_cmip5_GWL_ch12','model',('period','fx'),'GWL',('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='snw_cmip5_GWL_ch12', url=pattern_gwl)

# %% cell 10
# -- CORDEX
pattern = '/data/ciles/IPCC/FGD/snow/final/NA_CORDEX/time_periods/NAM-22_${model}_${experiment}_snw100seas_${clim_period}_remo22grid.nc'
cproject('snw_NAM-22_cordex_ch12','experiment',('period','fx'),'clim_period','model','thres', ('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='snw_NAM-22_cordex_ch12', url=pattern) 
pattern_gwl = '/data/ciles/IPCC/FGD/snow/final/NA_CORDEX/GWLs/NAM-22_${model}_GWL${GWL}_snw100seas_remo22grid.nc'
cproject('snw_NAM-22_cordex_GWL_ch12',('period','fx'),'model','GWL', ('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='snw_NAM-22_cordex_GWL_ch12', url=pattern_gwl)

# %% cell 11
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

    # -- Get the regions
    ar6_land = regionmask.defined_regions.ar6.land

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
        return weighted_mean(dat, mask_3D * weights, ("lon", "lat"))
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
    
def average_over_AR6_region(filename, mask_sup30, variable, region_name):

    # -- Get the regions
    ar6_land = regionmask.defined_regions.ar6.land

    # -- Get land/sea mask (generic)
    land_110 = regionmask.defined_regions.natural_earth.land_110

    # -- Get data
    ds = xr.open_dataset(filename, decode_times=False)
    dat = ds[variable]
    dat.values = np.array(dat.values, dtype=np.float32)

    # -- Get the mask of values > 30
    mask_ds = xr.open_dataset(mask_sup30, decode_times=False)
    mask = mask_ds[variable]
    mask.values = np.array(mask.values, dtype=np.float32)
    #
    # -- Mask the data
    dat.values = dat.values * mask.values

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
        return weighted_mean(dat, mask_3D * weights, ("lon", "lat"))
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
    else:
        raise ValueError("Cannot currently handle 2D coordinates")

    fully_contained = list()
    for region_poly in regions.polygons:
        res = poly.contains(region_poly)

        fully_contained.append(res)

    return xr.DataArray(
        fully_contained, dims=["region"], coords=dict(region=regions.numbers)
    )

# %% cell 13
# -- Do a mask using baseline = keep only the grid points with more than ndays with snow

# %% cell 14
exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='85',
         clim_period = '1995_2014'),    
    # -- Mid term
    dict(experiment='85',
         clim_period = '2041_2060'),
    dict(experiment='26',
         clim_period = '2041_2060'),
    # -- Late term
    dict(experiment='85',
         clim_period = '2081_2099'),
    dict(experiment='26',
         clim_period = '2081_2099'),
]

# -- Loop on the scenarios
ens_exp_dict = dict()
for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    clim_period = exp['clim_period']
    
    # -- Create ensemble object for the scenario
    req_exp = ds(project='snw_cmip6_ch12',
                 experiment = experiment,
                 clim_period = clim_period,
                 model = '*',
                )
    ens_exp = req_exp.explore('ensemble')
    
    # -- Climatologies
    ens_exp_dict[experiment+'_'+clim_period] = clim_average(ens_exp, 'ANM')

# %% cell 15
# -- Make a mask with baseline to keep only the grid points with more than 30 days
mask_dict = dict()
for mem in ens_exp_dict['85_1995_2014']:
    mask_dict[mem] = ccdo(ens_exp_dict['85_1995_2014'][mem], operator='setctomiss,0 -gtc,'+ndays)

# %% cell 16
iplot_members(ccdo(llbox(cens(mask_dict), lonmin=-175, lonmax=-40, latmin=0, latmax=90), operator='setmisstoc,0'),
              N=1, focus='land')

# %% cell 17
iplot_members(ccdo(llbox(cens(mask_dict), lonmin=-175, lonmax=-40, latmin=0, latmax=90), operator='setmisstoc,0'),
              N=2, focus='land')

# %% cell 19
# -- Loop on the scenarios
ens_GWL_dict = dict()
for GWL in ['1.5','2','3','4']:
    #
    req_GWL = ds(project='snw_cmip6_GWL_ch12',
                 GWL = GWL,
                 model = '*',
                )
    GWL_ens = req_GWL.explore('ensemble')
    # -- Climatologies
    ens_GWL_dict[GWL] = GWL_ens

# %% cell 20
ens_GWL_dict['1.5'].keys()

# %% cell 21
ens_exp_dict.keys()

# %% cell 22
regional_averages = dict()

NAM_regions = ['NWN','NEN','WNA','CNA','ENA']

# -- Loop on experiments / horizons
for ens_exp in ens_exp_dict:
    print ens_exp
    regional_averages[ens_exp] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_exp_dict[ens_exp]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        ttmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]),
                                       cfile(mask_dict[mem]),
                                       'snw', NAM_regions)

        for region_name in NAM_regions:
            region_value = float(ttmp[NAM_regions.index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[ens_exp]:
                regional_averages[ens_exp][region_name] = [region_value]
            else:
                regional_averages[ens_exp][region_name].append(region_value)

# %% cell 23
len(regional_averages['85_1995_2014']['CNA'])

# %% cell 24
regional_averages['85_1995_2014']['CNA']

# %% cell 25
NAM_regions = ['NWN','NEN','WNA','CNA','ENA']

# -- Loop on experiments / horizons
for GWL in ens_GWL_dict :
    print GWL
    regional_averages[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_GWL_dict[GWL]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        ttmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]),
                                      cfile(mask_dict[mem.replace('_85','').replace('_26','')]),
                                      'snw', NAM_regions)
        for region_name in NAM_regions:
            region_value = float(ttmp[NAM_regions.index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[GWL]:
                regional_averages[GWL][region_name] = [region_value]
            else:
                regional_averages[GWL][region_name].append(region_value)

# %% cell 27
quantiles_dict = dict()
nmodels_with_snow_in_baseline = dict()

for clim_period in regional_averages:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages[clim_period]:
        print clim_period, region_name
        quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages[clim_period][region_name])
        wdat = dat[np.where(np.isnan(dat)==False)]
        if clim_period=='85_1995_2014':
            nmodels_with_snow_in_baseline[region_name] = len(wdat)
        if len(wdat)>5:        
            q10 = np.quantile(wdat, 0.1)
            q50 = np.quantile(wdat, 0.5)
            q90 = np.quantile(wdat, 0.9)
        else:
            q10 = -99999
            q50 = -99999
            q90 = -99999
        print [q10, q50, q90]
        quantiles_dict[clim_period][region_name] = [q10, q50, q90]

import json
ensemble = 'CMIP6'
outfilename = CWD+'/../../data/Figure_12.10/'+ensemble+'_NORTH-AMERICA_snw_mask'+ndays+'_AR6_regional_averages.json'
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 28
nmodels_with_snow_in_baseline

# %% cell 30
NAM_regions = ['NWN','NEN','WNA','CNA','ENA','NCA']


exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='85',
         clim_period = '1995_2014'),    
    # -- Mid term
    dict(experiment='85',
         clim_period = '2041_2060'),
    dict(experiment='26',
         clim_period = '2041_2060'),
    # -- Late term
    dict(experiment='85',
         clim_period = '2081_2099'),
    dict(experiment='26',
         clim_period = '2081_2099'),
]

# -- Loop on the scenarios
ens_exp_dict = dict()
for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    clim_period = exp['clim_period']
    
    # -- Create ensemble object for the scenario
    req_exp = ds(project='snw_cmip5_ch12',
                 experiment = experiment,
                 clim_period = clim_period,
                 model = '*'
                )
    ens_exp = req_exp.explore('ensemble')
    
    # -- Climatologies
    ens_exp_dict[experiment+'_'+clim_period] = clim_average(ens_exp, 'ANM')

ens_GWL_dict = dict()
for GWL in ['1.5','2','3','4']:
    #
    req_GWL = ds(project='snw_cmip5_GWL_ch12',
                 GWL = GWL,
                 model = '*'
                )
    GWL_ens = req_GWL.explore('ensemble')
    # -- Climatologies
    ens_GWL_dict[GWL] = GWL_ens

# %% cell 31
# -- Make a mask with baseline to keep only the grid points with more than 30 days
mask_dict = dict()
for mem in ens_exp_dict['85_1995_2014']:
    mask_dict[mem] = ccdo(ens_exp_dict['85_1995_2014'][mem], operator='setctomiss,0 -gtc,'+ndays)

# %% cell 32
regional_averages = dict()

NAM_regions = ['NWN','NEN','WNA','CNA','ENA','NCA']

# -- Loop on experiments / horizons
for ens_exp in ens_exp_dict:
    print ens_exp
    regional_averages[ens_exp] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_exp_dict[ens_exp]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        ttmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]),
                                       cfile(mask_dict[mem]),
                                       'snw', NAM_regions)

        for region_name in NAM_regions:
            region_value = float(ttmp[NAM_regions.index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[ens_exp]:
                regional_averages[ens_exp][region_name] = [region_value]
            else:
                regional_averages[ens_exp][region_name].append(region_value)

# %% cell 33
# -- Loop on experiments / horizons
for GWL in ens_GWL_dict :
    print GWL
    regional_averages[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_GWL_dict[GWL]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        ttmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]),
                                      cfile(mask_dict[mem.replace('_85','').replace('_26','')]),
                                      'snw', NAM_regions)
        for region_name in NAM_regions:
            region_value = float(ttmp[NAM_regions.index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[GWL]:
                regional_averages[GWL][region_name] = [region_value]
            else:
                regional_averages[GWL][region_name].append(region_value)

# %% cell 34
import numpy
quantiles_dict = dict()
nmodels_with_snow_in_baseline = dict()
for clim_period in regional_averages:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages[clim_period]:
        print clim_period, region_name
        quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages[clim_period][region_name])
        wdat = dat[np.where(np.isnan(dat)==False)]
        if clim_period=='85_1995_2014':
            nmodels_with_snow_in_baseline[region_name] = len(wdat)
        if len(wdat)>5:        
            q10 = np.quantile(wdat, 0.1)
            q50 = np.quantile(wdat, 0.5)
            q90 = np.quantile(wdat, 0.9)
        else:
            q10 = -99999
            q50 = -99999
            q90 = -99999
        quantiles_dict[clim_period][region_name] = [q10, q50, q90]

import json
ensemble = 'CMIP5'
outfilename = CWD+'/../../data/Figure_12.10/'+ensemble+'_NORTH-AMERICA_snw_mask'+ndays+'_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 35
nmodels_with_snow_in_baseline

# %% cell 37
# -- CORDEX
pattern = '/data/ciles/IPCC/FGD/snow/final/NA_CORDEX/time_periods/NAM-22_${model}_${experiment}_snw100seas_${clim_period}_remo22grid.nc'
cproject('snw_NAM-22_cordex_ch12','experiment',('period','fx'),'clim_period','model','thres', ('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='snw_NAM-22_cordex_ch12', url=pattern) 
pattern_gwl = '/data/ciles/IPCC/FGD/snow/final/NA_CORDEX/GWLs/NAM-22_${model}_GWL${GWL}_snw100seas_remo22grid.nc'
cproject('snw_NAM-22_cordex_GWL_ch12',('period','fx'),'model','GWL', ('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='snw_NAM-22_cordex_GWL_ch12', url=pattern_gwl)

clog('critical')

exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='85',
         clim_period = '1995_2014'),    
    # -- Mid term
    dict(experiment='85',
         clim_period = '2041_2060'),
    dict(experiment='26',
         clim_period = '2041_2060'),
    # -- Late term
    dict(experiment='85',
         clim_period = '2081_209*'),
    dict(experiment='26',
         clim_period = '2081_209*'),
]

ens_exp_dict = dict()
ens_GWL_dict = dict()

for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    clim_period = exp['clim_period']

    # -- Create ensemble object for the scenario
    req_dict = dict(project='snw_NAM-22_cordex_ch12',
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
    

ens_GWL_dict = dict()
for GWL in ['1.5','2','3','4']:
    #
    req_GWL = ds(project='snw_NAM-22_cordex_GWL_ch12',
                 GWL = GWL,
                 model = '*',
                )
    GWL_ens = req_GWL.explore('ensemble')
    # -- Climatologies
    ens_GWL_dict[GWL] = GWL_ens

# %% cell 38
# -- Make a mask with baseline to keep only the grid points with more than 30 days
mask_dict = dict()
for mem in ens_exp_dict['85_1995_2014']:
    mask_dict[mem] = ccdo(ens_exp_dict['85_1995_2014'][mem], operator='setctomiss,0 -gtc,'+ndays)

# %% cell 39
regional_averages = dict()

NAM_regions = ['NWN','NEN','WNA','CNA','ENA']

# -- Loop on experiments / horizons
for ens_exp in ens_exp_dict:
    print ens_exp
    regional_averages[ens_exp] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_exp_dict[ens_exp]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        ttmp = average_over_AR6_region(cfile(regridn(ens_exp_dict[ens_exp][mem], cdogrid='r1440x720')),
                                       cfile(regridn(mask_dict[mem.replace('_85','').replace('_26','')], cdogrid='r1440x720', option='remapnn')),
                                       'snw', NAM_regions)

        for region_name in NAM_regions:
            region_value = float(ttmp[NAM_regions.index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[ens_exp]:
                regional_averages[ens_exp][region_name] = [region_value]
            else:
                regional_averages[ens_exp][region_name].append(region_value)

# %% cell 40
wmask_dict = dict()
for elt in mask_dict:
    wmask_dict[elt.replace('MOHC_','').replace('MPI-M_','').replace('NOAA_GFDL-','').replace('NCC_','')] = mask_dict[elt]

# -- Loop on experiments / horizons
for GWL in ens_GWL_dict :
    print GWL
    regional_averages[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_GWL_dict[GWL]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        ttmp = average_over_AR6_region(cfile(regridn(ens_GWL_dict[GWL][mem], cdogrid='r1440x720')),
                                      cfile(regridn(wmask_dict[mem.replace('_85','').replace('_26','')], cdogrid='r1440x720', option='remapnn')),
                                      'snw', NAM_regions)
        for region_name in NAM_regions:
            region_value = float(ttmp[NAM_regions.index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[GWL]:
                regional_averages[GWL][region_name] = [region_value]
            else:
                regional_averages[GWL][region_name].append(region_value)

# %% cell 41
import numpy
nmodels_with_snow_in_baseline = dict()
quantiles_dict = dict()
for clim_period in regional_averages:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages[clim_period]:
        print clim_period, region_name
        quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages[clim_period][region_name])
        wdat = dat[np.where(np.isnan(dat)==False)]
        if clim_period=='85_1995_2014':
            nmodels_with_snow_in_baseline[region_name] = len(wdat)
        if len(wdat)>=3:        
            q10 = np.quantile(wdat, 0.1)
            q50 = np.quantile(wdat, 0.5)
            q90 = np.quantile(wdat, 0.9)
        else:
            q10 = -99999
            q50 = -99999
            q90 = -99999
        quantiles_dict[clim_period][region_name] = [q10, q50, q90]

import json
ensemble = 'NAM-22_CORDEX'
outfilename = CWD+'/../../data/Figure_12.10/'+ensemble+'_NORTH-AMERICA_snw_mask'+ndays+'_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 42
nmodels_with_snow_in_baseline
