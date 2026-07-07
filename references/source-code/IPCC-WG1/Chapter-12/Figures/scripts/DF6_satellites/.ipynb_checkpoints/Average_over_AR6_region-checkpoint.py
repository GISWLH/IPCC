# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/DF6_satellites/.ipynb_checkpoints/Average_over_AR6_region-checkpoint.ipynb

# %% cell 2
import regionmask
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import json
import glob

# %% cell 4
from climaf.api import *

# %% cell 5
# -- Function to split a multi-member file in individual files
# -- Uses Xarray
def split_ensemble_file(ensemble_file, output_pattern, variable='spell'):
    if not os.path.isdir(os.path.dirname(output_pattern)):
        os.makedirs(os.path.dirname(output_pattern))
    import xarray as xr
    dat = xr.open_dataset(ensemble_file, decode_times=False)[variable]
    i = 0
    for member in dat.time:
        print i
        outfilename = output_pattern+'model'+str(i)+'.nc'
        if not os.path.isfile(outfilename):
            print 'Save '+outfilename
            member_dat = dat[i,:,:]
            wfile = outfilename.replace('.nc','tmp.nc')    
            member_dat.to_netcdf(wfile)
            cmd = 'cdo -b 32 setmissval,1e+20 -copy '+wfile+' '+outfilename+' ; ncrename -v spell,DF6 '+outfilename+' ; rm -f '+wfile
            print cmd
            cmd2 = 'ncatted -O -a coordinates,DF6,o,c,"lat lon" -a units,DF6,o,c,"Droughts" -a long_name,DF6,o,c,"Number of droughts per decade (DF6 index)" '+outfilename
            print cmd2
            os.system(cmd)
            os.system(cmd2)
        else:
            print outfilename+' already exists'
        i = i + 1

# %% cell 7
variable='DF6'
CMIP = 'CMIP6'

# -- Compute the annual sums
exp_list = [
    #dict(experiment='ssp585',
    #     clim_period = 'hist'),
    #dict(experiment='ssp585',
    #     clim_period = 'farfut'),
    #dict(experiment='ssp585',
    #     clim_period='midfut'),
    dict(experiment='ssp126',
         clim_period = 'midfut'),
    #dict(experiment='ssp126',
    #     clim_period = 'farfut'),
    #dict(experiment='ssp126',
    #     clim_period = 'hist'),
    #dict(experiment='ssp585',
    #     clim_period = 'farch'),
    #dict(experiment='ssp585',
    #     clim_period='midch'),
    #dict(experiment='ssp126',
    #     clim_period = 'farch'),
    #dict(experiment='ssp126',
    #     clim_period = 'GWL1.5'),
    #dict(experiment='ssp126',
    #     clim_period = 'GWL2.0'),
    #dict(experiment='ssp585',
    #     clim_period = 'GWL1.5'),
    #dict(experiment='ssp585',
    #     clim_period = 'GWL2.0'),
    #dict(experiment='ssp585',
    #     clim_period = 'GWL3.0'),
    #dict(experiment='ssp585',
    #     clim_period = 'GWL4.0'),
]

for exp_dict in exp_list:
    clim_period = exp_dict['clim_period']
    experiment = exp_dict['experiment']
    wfile = '/data/jservon/IPCC/DF/CMIP6/CMIP6_'+experiment+'-DF6-'+clim_period+'.nc'
    output_pattern = '/data/jservon/IPCC/DF/individual_models/CMIP6/CMIP6_'+experiment+'_DF6_'+clim_period+'_'
    split_ensemble_file(wfile, output_pattern)

# %% cell 9
variable='DF6'
CMIP = 'CMIP5'

# -- Compute the annual sums
exp_list = [
    #dict(experiment='rcp85',
    #     clim_period = 'hist'),
    #dict(experiment='rcp85',
    #     clim_period = 'farfut'),
    #dict(experiment='rcp85',
    #     clim_period='midfut'),
    dict(experiment='rcp26',
         clim_period = 'midfut'),
    #dict(experiment='rcp26',
    #     clim_period = 'farfut'),
    #dict(experiment='rcp26',
    #     clim_period = 'hist'),
    #dict(experiment='rcp85',
    #     clim_period = 'farch'),
    #dict(experiment='rcp85',
    #     clim_period='midch'),
    #dict(experiment='rcp26',
    #     clim_period = 'farch'),
    #dict(experiment='rcp26',
    #     clim_period = 'GWL1.5'),
    #dict(experiment='rcp26',
    #     clim_period = 'GWL2.0'),
    #dict(experiment='rcp85',
    #     clim_period = 'GWL1.5'),
    #dict(experiment='rcp85',
    #     clim_period = 'GWL2.0'),
    #dict(experiment='rcp85',
    #     clim_period = 'GWL3.0'),
    #dict(experiment='rcp85',
    #     clim_period = 'GWL4.0'),

]

for exp_dict in exp_list:
    clim_period = exp_dict['clim_period']
    experiment = exp_dict['experiment']
    wfile = '/data/jservon/IPCC/DF/DF-CMIP5/CMIP5_'+experiment+'-DF6-'+clim_period+'.nc'
    output_pattern = '/data/jservon/IPCC/DF/individual_models/CMIP5/CMIP5_'+experiment+'_DF6_'+clim_period+'_'
    split_ensemble_file(wfile, output_pattern)

# %% cell 11
variable='DF6'
CMIP = 'CMIP6'

CORDEX_domains = [
    'AFR',
    'AUS',
    'CAM',
    'EAS',
    'NAM',
    'SAM',
    'SEA',
    'WAS'
    # -- Asia
    #'EAS-22','EAS-44',
    #'WAS-22','WAS-44',
    #'SEA-22',
    # -- Europe
    #'EUR-11',
    
]
#AFR  AUS  CAM  EAS  EUR-11  NAM  SAM  SEA  WAS


variable='DF6'
CMIP = 'CORDEX'

# -- Compute the annual sums
exp_list = [
    dict(experiment='rcp85',
         clim_period = 'hist'),
    dict(experiment='rcp85',
         clim_period = 'farfut'),
    dict(experiment='rcp85',
         clim_period='midfut'),
    dict(experiment='rcp26',
         clim_period = 'farfut'),
    dict(experiment='rcp26',
         clim_period = 'hist'),
    dict(experiment='rcp26',
         clim_period = 'midfut'),
    
    dict(experiment='rcp26',
         clim_period = 'GWL1.5'),
    #dict(experiment='rcp26',
    #     clim_period = 'GWL2.0'),
    dict(experiment='rcp85',
         clim_period = 'GWL1.5'),
    dict(experiment='rcp85',
         clim_period = 'GWL2.0'),
    dict(experiment='rcp85',
         clim_period = 'GWL3.0'),
    dict(experiment='rcp85',
         clim_period = 'GWL4.0'),
]

for CORDEX_domain in CORDEX_domains:
    for exp_dict in exp_list:
        clim_period = exp_dict['clim_period']
        experiment = exp_dict['experiment']
        wCORDEX_domain = CORDEX_domain
        if '-' not in CORDEX_domain:
            wCORDEX_domain = CORDEX_domain+'-22'
        wfile = '/data/jservon/IPCC/DF/DF-CORDEX/'+CORDEX_domain+'/'+wCORDEX_domain+'_'+experiment+'-DF6-'+clim_period+'.nc'
        outdir = '/data/jservon/IPCC/DF/individual_models/CORDEX/'+CORDEX_domain
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        output_pattern = '/data/jservon/IPCC/DF/individual_models/CORDEX/'+wCORDEX_domain+'/'+wCORDEX_domain+'_'+experiment+'_DF6_'+clim_period+'_'
        split_ensemble_file(wfile, output_pattern)

# %% cell 12
CORDEX_domain = 'EUR-11'

exp_list = [
    #dict(experiment='rcp85',
    #     clim_period = 'ref'),
    #dict(experiment='rcp85',
    #     clim_period = 'far'),
    #dict(experiment='rcp85',
    #     clim_period='mid'),
    #dict(experiment='rcp26',
    #     clim_period = 'far'),
    #dict(experiment='rcp26',
    #     clim_period = 'ref'),
    dict(experiment='rcp26',
         clim_period = 'mid'),
    
    #dict(experiment='GWLs',
    #     clim_period = '1.5deg'),
    #dict(experiment='GWLs',
    #     clim_period = '2.0deg'),
    #dict(experiment='GWLs',
    #     clim_period = '4.0deg'),
]


#exp_list = [
#    dict(experiment='rcp85',
#         clim_period = 'far'),
#    dict(experiment='GWLs',
#         clim_period = '1.5deg'),
#]

def prepare_EUR_files(wfile, outfilename, variable='spell'):
    if not os.path.isfile(outfilename):
        cmd = 'cdo -b 32 setmissval,1e+20 -copy '+wfile+' '+outfilename+' ; ncrename -v spell,DF6 '+outfilename
        print cmd
        cmd2 = 'ncatted -O -a coordinates,DF6,o,c,"lat lon" -a units,DF6,o,c,"Droughts" -a long_name,DF6,o,c,"Number of droughts per decade (DF6 index)" '+outfilename
        print cmd2
        os.system(cmd)
        os.system(cmd2)
    else:
        print outfilename+' already exists'
#
for exp in exp_list:
    experiment  = exp['experiment']
    clim_period = exp['clim_period']
    
    if experiment=='GWLs':
        file_pattern = '/data/jservon/IPCC/DF/DF-CORDEX/'+CORDEX_domain+'/'+experiment+'/pr_mon_*_OK_SPI6_sel*_SPELL_'+clim_period+'.nc'
        wclim_period = 'GWL'+clim_period.replace('deg','')
        output_pattern = '/data/jservon/IPCC/DF/individual_models/CORDEX/'+CORDEX_domain+'/'+CORDEX_domain+'_rcptarget_DF6_'+wclim_period+'_'
    else:
        if clim_period not in ['ref']:
            wclim_period = clim_period+'fut'
        else:
            wclim_period = 'hist'
        file_pattern = '/data/jservon/IPCC/DF/DF-CORDEX/'+CORDEX_domain+'/'+experiment+'/pr_mon_*_OK_SPI6_sel_SPELL_'+clim_period+'.nc'
        output_pattern = '/data/jservon/IPCC/DF/individual_models/CORDEX/'+CORDEX_domain+'/'+CORDEX_domain+'_'+experiment+'_DF6_'+wclim_period+'_'
    
    lof = glob.glob(file_pattern)
    i = 0
    for wfile in lof:
        wexperiment = os.path.basename(wfile).split('_')[5]
        outfilename = output_pattern.replace('rcptarget',wexperiment)+'model'+str(i)+'.nc'
        if not os.path.isdir(os.path.dirname(outfilename)):
            os.makedirs(os.path.dirname(outfilename))
            print 'creating '+os.path.dirname(outfilename)
        print '--> '+experiment+' '+clim_period
        prepare_EUR_files(wfile, outfilename)
        i = i + 1

# %% cell 13
lof

# %% cell 15
pattern = '/data/jservon/IPCC/DF/individual_models/CMIP6/CMIP6_${experiment}_DF6_${clim_period}_${member}.nc'
#pattern = '/data/jservon/IPCC/DF/CMIP6/CMIP6_${experiment}_DF6_${clim_period}_${member}.nc'
cproject('DF_cmip6_ch12','experiment','clim_period',('period','fx'),'member', ('variable','DF6'), ensemble=['member'], separator='%')
dataloc(project='DF_cmip6_ch12', url=pattern)

pattern = '/data/jservon/IPCC/DF/individual_models/CMIP6/CMIP6_${experiment}_DF6_${GWL}_${member}.nc'
cproject('DF_cmip6_GWL_ch12','experiment','GWL',('period','fx'),'member', ('variable','DF6'), ensemble=['member'], separator='%')
dataloc(project='DF_cmip6_GWL_ch12', url=pattern)

# %% cell 16
pattern = '/data/jservon/IPCC/DF/individual_models/CMIP5/CMIP5_${experiment}_DF6_${clim_period}_${member}.nc'
cproject('DF_cmip5_ch12','experiment','clim_period',('period','fx'),'member', ('variable','DF6'), ensemble=['member'], separator='%')
dataloc(project='DF_cmip5_ch12', url=pattern)

pattern = '/data/jservon/IPCC/DF/individual_models/CMIP5/CMIP5_${experiment}_DF6_${GWL}_${member}.nc'
cproject('DF_cmip5_GWL_ch12','experiment','GWL',('period','fx'),'member', ('variable','DF6'), ensemble=['member'], separator='%')
dataloc(project='DF_cmip5_GWL_ch12', url=pattern)

# %% cell 17
pattern = '/data/jservon/IPCC/DF/individual_models/CORDEX/${CORDEX_domain}/${CORDEX_domain}_${experiment}_DF6_${clim_period}_${member}.nc'
pattern_EUR = '/data/jservon/IPCC/DF/CORDEX/${CORDEX_domain}/${experiment}/pr_mon_${member}_OK_SPI6_sel_SPELL_${clim_period}.nc'
cproject('DF_cordex_ch12','experiment','clim_period',('period','fx'),'CORDEX_domain','member', ('variable','DF6'), ensemble=['member'], separator='%')
dataloc(project='DF_cordex_ch12', url=[pattern,pattern_EUR])

pattern_GWL = '/data/jservon/IPCC/DF/individual_models/CORDEX/${CORDEX_domain}/${CORDEX_domain}_${experiment}_DF6_${clim_period}_${member}.nc'
pattern_EUR_GWL = '/data/jservon/IPCC/DF/CORDEX/${CORDEX_domain}/GWLs/pr_mon_${member}_OK_SPI6_sel_SPELL_${GWL}deg.nc'
cproject('DF_cordex_GWL_ch12','experiment','clim_period',('period','fx'),'CORDEX_domain','member', ('variable','DF6'), ensemble=['member'], separator='%')
dataloc(project='DF_cordex_GWL_ch12', url=[pattern_GWL,pattern_EUR_GWL])

# %% cell 18
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
#
def average_over_AR6_region_new(filename, variable, region_name):

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

# %% cell 19
!ls /data/jservon/IPCC/DF/individual_models/CMIP6

# %% cell 21
exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='ssp585',
         clim_period = 'hist'),    
    # -- Mid term
    dict(experiment='ssp585',
         clim_period = 'midfut'),
    dict(experiment='ssp126',
         clim_period = 'midfut'),
    # -- Late term
    dict(experiment='ssp585',
         clim_period = 'farfut'),
    dict(experiment='ssp126',
         clim_period = 'farfut'),
]

# -- Loop on the scenarios
ens_exp_dict = dict()
clog('critical')
for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    clim_period = exp['clim_period']
    
    # -- Create ensemble object for the scenario
    req_exp = ds(project='DF_cmip6_ch12',
                 experiment = experiment,
                 clim_period = clim_period,
                 member = '*'
                )
    ens_exp = req_exp.explore('ensemble')
    
    # -- Climatologies
    ens_exp_dict[experiment+'_'+clim_period] = clim_average(ens_exp, 'ANM')

# %% cell 23
# -- Loop on the scenarios
ens_GWL_dict = dict()
for GWL in ['GWL1.5','GWL2.0','GWL3.0','GWL4.0']:
    #
    if GWL in ['GWL1.5','GWL2.0']:
        # -- Create ensemble object for the scenario
        req_ssp126 = ds(project='DF_cmip6_GWL_ch12',
                     experiment = 'ssp126',
                     GWL = GWL,
                     member = '*'
                    )
        ens_ssp126 = req_ssp126.explore('ensemble')

        # -- Create ensemble object for the scenario
        req_ssp585 = ds(project='DF_cmip6_GWL_ch12',
                     experiment = 'ssp585',
                     GWL = GWL,
                     member = '*'
                    )
        ens_ssp585 = req_ssp585.explore('ensemble')
        #
        # -- Merge ensembles
        GWL_ens = merge_climaf_ensembles([add_prefix_suffix_to_ens_req(ens_ssp126,suffix='_ssp126'),
                                          add_prefix_suffix_to_ens_req(ens_ssp585,suffix='_ssp585')])
    else:
        # -- Create ensemble object for the scenario
        req_ssp585 = ds(project='DF_cmip6_GWL_ch12',
                     experiment = 'ssp585',
                     GWL = GWL,
                     member = '*'
                    )
        GWL_ens = req_ssp585.explore('ensemble')
        
    # -- Climatologies
    ens_GWL_dict[GWL] = clim_average(GWL_ens, 'ANM')

# %% cell 24
regional_averages = dict()

# -- Loop on experiments / horizons
for ens_exp in ens_exp_dict:
    print ens_exp
    regional_averages[ens_exp] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_exp_dict[ens_exp]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        #tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'DF6', 'all')
        #region_names = tmp.abbrevs
        #for tmp_region_name in region_names:
        #    region_name = str(tmp_region_name.values)
        #    print region_name
        #    region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
        #    if region_name not in regional_averages[ens_exp]:
        #        regional_averages[ens_exp][region_name] = [region_value]
        #    else:
        #        regional_averages[ens_exp][region_name].append(region_value)
        tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'DF6', 'all')
        region_names = list(tmp.abbrevs)
        ttmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'DF6', region_names)
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            region_value = float(ttmp[list(tmp.abbrevs).index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[ens_exp]:
                regional_averages[ens_exp][region_name] = [region_value]
            else:
                regional_averages[ens_exp][region_name].append(region_value)

# %% cell 25
for GWL in ens_GWL_dict :
    print GWL
    regional_averages[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_GWL_dict[GWL]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        #tmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]), 'DF6', 'all')
        #region_names = tmp.abbrevs
        #for tmp_region_name in region_names:
        #    region_name = str(tmp_region_name.values)
        #    print region_name
        #    region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
        #    if region_name not in regional_averages[GWL]:
        #        regional_averages[GWL][region_name] = [region_value]
        #    else:
        #        regional_averages[GWL][region_name].append(region_value)
        tmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]), 'DF6', 'all')
        region_names = list(tmp.abbrevs)
        ttmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]), 'DF6', region_names)
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            region_value = float(ttmp[list(tmp.abbrevs).index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages[GWL]:
                regional_averages[GWL][region_name] = [region_value]
            else:
                regional_averages[GWL][region_name].append(region_value)

# %% cell 27
import numpy
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

# %% cell 28
quantiles_dict[clim_period][region_name]

# %% cell 30
import json
ensemble = 'CMIP6'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.3/'+ensemble+'_DF6_AR6_regional_averages.json'
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 32
# -- Scenarios - timelines
# ---------------------------------------------------------------------------

exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='rcp85',
         clim_period = 'hist'),    
    # -- Mid term
    dict(experiment='rcp85',
         clim_period = 'midfut'),
    dict(experiment='rcp26',
         clim_period = 'midfut'),
    # -- Late term
    dict(experiment='rcp85',
         clim_period = 'farfut'),
    dict(experiment='rcp26',
         clim_period = 'farfut'),
]

# -- Loop on the scenarios
ens_exp_dict = dict()
for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    clim_period = exp['clim_period']
    
    # -- Create ensemble object for the scenario
    req_exp = ds(project='DF_cmip5_ch12',
                 experiment = experiment,
                 clim_period = clim_period,
                 member = '*'
                )
    ens_exp = req_exp.explore('ensemble')
    
    # -- Climatologies
    ens_exp_dict[experiment+'_'+clim_period] = ens_exp
#


# -- Global Warming Levels
# ---------------------------------------------------------------------------
ens_GWL_dict = dict()

# -- Loop on the GWLs
for GWL in ['GWL1.5','GWL2.0','GWL3.0','GWL4.0']:
    #
    if GWL in ['GWL1.5','GWL2.0']:
        # -- Create ensemble object for the scenario
        req_rcp26 = ds(project='DF_cmip5_GWL_ch12',
                     experiment = 'rcp26',
                     GWL = GWL,
                     member = '*'
                    )
        ens_rcp26 = req_rcp26.explore('ensemble')

        # -- Create ensemble object for the scenario
        req_rcp85 = ds(project='DF_cmip5_GWL_ch12',
                     experiment = 'rcp85',
                     GWL = GWL,
                     member = '*'
                    )
        ens_rcp85 = req_rcp85.explore('ensemble')
        #
        # -- Merge ensembles
        GWL_ens = merge_climaf_ensembles([add_prefix_suffix_to_ens_req(ens_rcp26,suffix='_rcp26'),
                                          add_prefix_suffix_to_ens_req(ens_rcp85,suffix='_rcp85')])
    else:
        # -- Create ensemble object for the scenario
        req_rcp85 = ds(project='DF_cmip5_GWL_ch12',
                     experiment = 'rcp85',
                     GWL = GWL,
                     member = '*'
                    )
        GWL_ens = req_rcp85.explore('ensemble')
        
    # -- Climatologies
    ens_GWL_dict[GWL] = GWL_ens

# %% cell 33
regional_averages_CMIP5 = dict()

# -- Loop on experiments / horizons
for ens_exp in ens_exp_dict:
    print ens_exp
    regional_averages_CMIP5[ens_exp] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_exp_dict[ens_exp]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'DF6', 'all')
        region_names = list(tmp.abbrevs)
        ttmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'DF6', region_names)
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            region_value = float(ttmp[list(tmp.abbrevs).index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages_CMIP5[ens_exp]:
                regional_averages_CMIP5[ens_exp][region_name] = [region_value]
            else:
                regional_averages_CMIP5[ens_exp][region_name].append(region_value)
#

for GWL in ens_GWL_dict :
    print GWL
    regional_averages_CMIP5[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_GWL_dict[GWL]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        tmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]), 'DF6', 'all')
        region_names = list(tmp.abbrevs)
        ttmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]), 'DF6', region_names)
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            region_value = float(ttmp[list(tmp.abbrevs).index(region_name)])
            print region_name, region_value
            if region_name not in regional_averages_CMIP5[GWL]:
                regional_averages_CMIP5[GWL][region_name] = [region_value]
            else:
                regional_averages_CMIP5[GWL][region_name].append(region_value)

# %% cell 34
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

# %% cell 35
import json
ensemble = 'CMIP5'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.3/'+ensemble+'_DF6_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 37
pattern = '/data/jservon/IPCC/DF/individual_models/CORDEX/${CORDEX_domain}/${CORDEX_domain}_${experiment}_DF6_${clim_period}_${member}.nc'
pattern_EUR = '/data/jservon/IPCC/DF/CORDEX/${CORDEX_domain}/${experiment}/pr_mon_${member}_OK_SPI6_sel_SPELL_${clim_period}.nc'
cproject('DF_cordex_ch12','experiment','clim_period',('period','fx'),'CORDEX_domain','member', ('variable','DF6'), ensemble=['member'], separator='%')
dataloc(project='DF_cordex_ch12', url=[pattern,pattern_EUR])

pattern_GWL = '/data/jservon/IPCC/DF/individual_models/CORDEX/${CORDEX_domain}/${CORDEX_domain}_${experiment}_DF6_${clim_period}_${member}.nc'
pattern_EUR_GWL = '/data/jservon/IPCC/DF/CORDEX/${CORDEX_domain}/GWLs/pr_mon_${member}_OK_SPI6_sel_SPELL_${GWL}deg.nc'
cproject('DF_cordex_GWL_ch12','experiment','clim_period',('period','fx'),'CORDEX_domain','member', ('variable','DF6'), ensemble=['member'], separator='%')
dataloc(project='DF_cordex_GWL_ch12', url=[pattern_GWL,pattern_EUR_GWL])

clog('critical')
#thres = 'Exceed'+wthres
# -- Scenarios - timelines
# ---------------------------------------------------------------------------
CORDEX_domains = [
    'AFR-22',
    'AUS-22',
    'CAM-22',
    'EAS-22',
    'EUR-11',
    'NAM-22',
    'SAM-22',
    'SEA-22',
    'WAS-22'
    
]



exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='rcp85',
         clim_period = 'hist'),    
    # -- Mid term
    dict(experiment='rcp85',
         clim_period = 'midfut'),
    dict(experiment='rcp26',
         clim_period = 'midfut'),
    # -- Late term
    dict(experiment='rcp85',
         clim_period = 'farfut'),
    dict(experiment='rcp26',
         clim_period = 'farfut'),
]

ens_exp_dict_CORDEX = dict()
ens_GWL_dict_CORDEX = dict()

#for CORDEX_domain in ['AFR-22']:
for CORDEX_domain in CORDEX_domains:
    #
    # -- We use the first three letters of the CORDEX_domain to identify the region
    short_CORDEX_domain = CORDEX_domain[0:3]

    # -- Loop on the scenarios
    ens_exp_dict_CORDEX[short_CORDEX_domain] = dict()
    for exp in exp_list:
        #
        # -- Experiment and period
        experiment = exp['experiment']
        clim_period = exp['clim_period']

        # -- Create ensemble object for the scenario
        req_exp = ds(project='DF_cordex_ch12',
                     experiment = experiment,
                     #realization='r1i1p1',
                     clim_period = clim_period,
                     CORDEX_domain = CORDEX_domain,
                     member = '*'
                    )
        #try:
        ens_exp = add_prefix_suffix_to_ens_req(req_exp.explore('ensemble'), suffix='_'+CORDEX_domain)
        #
        # -- Climatologies
        # If there is already a short_CORDEX_domain in the results, we merge the results of the new one
        if experiment+'_'+clim_period in ens_exp_dict_CORDEX[short_CORDEX_domain]:
            #res_copy = ens_exp_dict_CORDEX[short_CORDEX_domain][experiment+'_'+period].copy()
            #final_ens = merge_climaf_ensembles([res_copy, clim_average(ens_exp, 'ANM')])
            ens_exp_dict_CORDEX[short_CORDEX_domain][experiment+'_'+clim_period].update( clim_average(ens_exp, 'ANM') )
        else:
            ens_exp_dict_CORDEX[short_CORDEX_domain][experiment+'_'+clim_period] = clim_average(ens_exp, 'ANM')
            #final_ens = clim_average(ens_exp, 'ANM')
        #ens_exp_dict_CORDEX[short_CORDEX_domain][experiment+'_'+period] = final_ens
        #except:
        #print 'no data found for ', req_exp
    #

    # -- Global Warming Levels
    # ---------------------------------------------------------------------------
    ens_GWL_dict_CORDEX[short_CORDEX_domain] = dict()

    # -- Loop on the GWLs
    for GWL in ['GWL1.5','GWL2.0','GWL4.0']:
        #
        if GWL in ['GWL1.5']:
            # -- Create ensemble object for the scenario
            req_rcp26 = ds(project='DF_cordex_ch12',
                         experiment = 'rcp26',
                         clim_period = GWL,
                         CORDEX_domain = CORDEX_domain,
                         member = '*'
                        )
            try:
                ens_rcp26 = req_rcp26.explore('ensemble')
            except:
                print 'No data found for ',req_rcp26
                ens_rcp26 = cens(dict())

            # -- Create ensemble object for the scenario
            req_rcp85 = ds(project='DF_cordex_ch12',
                         experiment = 'rcp85',
                         clim_period = GWL,
                         CORDEX_domain = CORDEX_domain,
                         member = '*'
                        )
            try:
                ens_rcp85 = req_rcp85.explore('ensemble')
            except:
                print 'No data found for ',req_rcp85
                ens_rcp85 = cens(dict())
            #
            # -- Merge ensembles
            GWL_ens = merge_climaf_ensembles([add_prefix_suffix_to_ens_req(ens_rcp26,suffix='_rcp26'),
                                              add_prefix_suffix_to_ens_req(ens_rcp85,suffix='_rcp85')])
        else:
            # -- Create ensemble object for the scenario
            req_rcp85 = ds(project='DF_cordex_ch12',
                         experiment = 'rcp85',
                         #  realization='r1i1p1',
                         clim_period = GWL,
                         CORDEX_domain = CORDEX_domain,
                         member = '*'
                        )
            GWL_ens = req_rcp85.explore('ensemble')
        #
        # -- Rename the members with the CORDEX domain for future merge
        renamed_GWL_ens = add_prefix_suffix_to_ens_req(GWL_ens, suffix='_'+CORDEX_domain)
        #
        # -- if GWL in ens_GWL_dict_CORDEX[short_CORDEX_domain]:
        if GWL in ens_GWL_dict_CORDEX[short_CORDEX_domain]:
            res_copy = ens_GWL_dict_CORDEX[short_CORDEX_domain][GWL].copy()
            final_ens = merge_climaf_ensembles([res_copy, clim_average(renamed_GWL_ens, 'ANM')])
            # We merge the new one with the old one
        else:
            # We just add the new one
            final_ens = clim_average(renamed_GWL_ens, 'ANM')
        #
        # -- Climatologies
        ens_GWL_dict_CORDEX[short_CORDEX_domain][GWL] = final_ens
    #

# %% cell 38
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

#
# -- Loop on the short CORDEX domains
# -- short_CORDEX_domains = ['AFR','EAS',...]
regional_averages_CORDEX = dict()

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

for ens_CORDEX in [ens_exp_dict_CORDEX, ens_GWL_dict_CORDEX]:
    for short_CORDEX_domain in ens_CORDEX:
        print short_CORDEX_domain
        if short_CORDEX_domain not in regional_averages_CORDEX:
            regional_averages_CORDEX[short_CORDEX_domain] = dict()

        # -- Loop on experiments / horizons
        for ens_exp in ens_CORDEX[short_CORDEX_domain]:
            if ens_exp not in ['3.0K']:
                print ens_exp
                regional_averages_CORDEX[short_CORDEX_domain][ens_exp] = dict()
                # -- Loop on the members of each ensemble
                for mem in ens_CORDEX[short_CORDEX_domain][ens_exp]:
                    #if 'CCCma-CanESM2--UCAN-WRF341I' not in mem:
                    print mem
                    # -- Compute the averages for each AR6 region thanks to regionmask
                    # --> We regrid on a 0.25° grid with conservative regridding
                    tmp = average_over_AR6_region(
                                cfile(regridn(ens_CORDEX[short_CORDEX_domain][ens_exp][mem], cdogrid='r1440x720', option='remapbil')),
                                'DF6', 'all')
                    region_names = tmp.abbrevs
                    #for tmp_region_name in region_names:
                    for tmp_region_name in AR6regions_by_CORDEX_domain[short_CORDEX_domain]:
                        #region_name = str(tmp_region_name.values)
                        region_name = tmp_region_name
                        print region_name
                        region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                        region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                        if region_name not in regional_averages_CORDEX[short_CORDEX_domain][ens_exp]:
                            regional_averages_CORDEX[short_CORDEX_domain][ens_exp][region_name] = [region_value]
                        else:
                            regional_averages_CORDEX[short_CORDEX_domain][ens_exp][region_name].append(region_value)

# %% cell 39
float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)

# %% cell 40
ens_exp_dict_CORDEX['SEA'].keys()# ens_GWL_dict_CORDEX

# %% cell 41
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

# %% cell 42
quantiles_dict

# %% cell 43
import json
ensemble = 'CORDEX'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.3/'+ensemble+'_DF6_AR6_regional_averages.json'
print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 44
# Creer une grille lon/lat pour chaque CORDEX domain
# regriller sur cette grille
# missing values outside the domain
#   => ok to retrieve the regions
#   => not ok to check if the region is completely covered
#   => check by hand?
#   => if CORDEX_domain = ... ; then subregions = [...]
#   => if partially covered => No!
# AFR, 3 domains for America, Aus = ok, 3 domains over Asia, 1 over Europe =
#   8 domains = feasable
# AFR, et Asia = ok; need Europe, and the Americas

# %% cell 45
# Prendre un champ de chaque domain, faire un plot avec toutes les regions
# Selectionner a la main

# Si on prend les regions partiellement couvertes:
#  - on regrille CMIP6 et CMIP5 sur tous les domains CORDEX
#  - en multipliant par un mask pour mettre des missing

# %% cell 46
ncdump(ens_CORDEX[short_CORDEX_domain][ens_exp][mem])

# %% cell 47
# If region is not entireley covered => 0
# Do the map with regions on top and hatching
# Start the barplot:
# - retrieve values from json file
# - do the plot for one region
# Start to build the multiplot
#

# %% cell 49
regionmask.defined_regions.ar6.all.abbrevs.index('CAR')

# %% cell 50
ar6_land = regionmask.defined_regions.ar6.land
ar6_land

# %% cell 51
ar6_land.abbrevs

# %% cell 52
ar6_land.names
