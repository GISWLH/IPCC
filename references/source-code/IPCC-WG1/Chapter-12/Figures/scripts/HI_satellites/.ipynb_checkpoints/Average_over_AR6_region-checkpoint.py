# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/HI_satellites/.ipynb_checkpoints/Average_over_AR6_region-checkpoint.ipynb

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

# %% cell 7
lof = glob.glob('/data/ciles/IPCC/FGD/WBGT_FGD/CMIP6_share/*/*_*-*_QDM_HI.nc')
outdir = '/data/jservon/IPCC/WBGT/CMIP6/'
for wfile in lof:
    #print wfile
    # -- Get model, realization, and threshold
    dumsplit = wfile.split('/')[-1].split('_')
    thres = dumsplit[1]
    model = dumsplit[2]
    scenario = dumsplit[3]
    realization = dumsplit[4]
    period = dumsplit[5]
    if '.' not in period:
        #print model, realization, thres, scenario, period
        target = outdir+model+'_'+realization+'_'+thres+'_'+scenario+'_'+period+'.nc'
        cmd = 'cdo -b 32 setmissval,1e+20 -copy '+wfile+' '+target
        print cmd
        cmd2 = 'ncatted -O -a coordinates,WBGTindoor,o,c,"time lat lon" -a units,WBGTindoor,o,c,days -a long_name,WBGTindoor,o,c,"Number of days per year with wet-bulb temperature above '+thres+' degC" '+target
        os.system(cmd)
        os.system(cmd2)
    # -- Add coordinates attribute
    # -- set FillValue

# %% cell 9
lof = glob.glob('/data/ciles/IPCC/FGD/HI_NOAA/CMIP6/*/*_*-*_QDM_HI.nc')
outdir = '/data/jservon/IPCC/HI_NOAA/CMIP6/'
for wfile in lof:
    #print wfile
    # -- Get model, realization, and threshold
    dumsplit = wfile.split('/')[-1].split('_')
    thres = dumsplit[1]
    model = dumsplit[2]
    scenario = dumsplit[3]
    realization = dumsplit[4]
    period = dumsplit[5]
    #if '.' not in period:
    #print model, realization, thres, scenario, period
    target = outdir+model+'_'+realization+'_'+thres+'_'+scenario+'_'+period+'.nc'
    cmd = 'cdo -b 32 setmissval,1e+20 -copy '+wfile+' '+target
    print cmd
    cmd2 = 'ncatted -O -a coordinates,HI,o,c,"time lat lon" -a units,HI,o,c,days -a long_name,HI,o,c,"Number of days per year with HI temperature above '+thres+' degC" '+target
    os.system(cmd)
    os.system(cmd2)
    # -- Add coordinates attribute
    # -- set FillValue

# %% cell 11
lof = glob.glob('/data/ciles/IPCC/FGD/HI_NOAA/CMIP5/*/*_*-*_QDM_HI.nc')
outdir = '/data/jservon/IPCC/HI_NOAA/CMIP5/'
for wfile in lof:
    #print wfile
    # -- Get model, realization, and threshold
    dumsplit = wfile.split('/')[-1].split('_')
    thres = dumsplit[1]
    model = dumsplit[2]
    scenario = dumsplit[3]
    realization = dumsplit[4]
    period = dumsplit[5]
    #if '.' not in period:
    #print model, realization, thres, scenario, period
    target = outdir+model+'_'+realization+'_'+thres+'_'+scenario+'_'+period+'.nc'
    cmd = 'cdo -b 32 setmissval,1e+20 -copy '+wfile+' '+target
    print cmd
    cmd2 = 'ncatted -O -a coordinates,HI,o,c,"time lat lon" -a units,HI,o,c,days -a long_name,HI,o,c,"Number of days per year with HI temperature above '+thres+' degC" '+target
    os.system(cmd)
    os.system(cmd2)
    # -- Add coordinates attribute
    # -- set FillValue

# %% cell 13
CORDEX_domains = [
    # -- Africa
    #'AFR-22','AFR-44',
    # -- AustralAsia
    'AUS-22','AUS-44',
    # -- Central America
    'CAM-22','CAM-44',
    # -- North America
    'NAM-22','NAM-44',
    # -- South America
    'SAM-22',
    'SAM-44',
    # -- Asia
    'EAS-22','EAS-44',
    'WAS-22','WAS-44',
    'SEA-22',
    # -- Europe
    'EUR-11',
    
]
for CORDEX_domain in CORDEX_domains:
    lof = glob.glob('/data/ciles/IPCC/FGD/HI_NOAA/CORDEX-'+CORDEX_domain+'/*/*_QDM_HI.nc')
    outdir = '/data/jservon/IPCC/HI_NOAA/CORDEX/'+CORDEX_domain+'/'
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    for wfile in lof:
        #print wfile
        # -- Get model, realization, and threshold
        dumsplit = wfile.split('/')[-1].split('_')
        thres = dumsplit[1]
        GCM = dumsplit[2]
        RCM = dumsplit[3]
        scenario = dumsplit[4]
        realization = dumsplit[5]
        period = dumsplit[6]
        #print model, realization, thres, scenario, period
        target = outdir+GCM+'--'+RCM+'_'+realization+'_'+thres+'_'+scenario+'_'+period+'.nc'
        cmd = 'cdo -b 32 setmissval,1e+20 -copy '+wfile+' '+target
        print cmd
        cmd2 = 'ncatted -O -a coordinates,HI,o,c,"time lat lon" -a units,HI,o,c,days -a long_name,HI,o,c,"Number of days per year with HI NOAA index above '+thres+' degC" '+target
        print cmd2
        os.system(cmd)
        os.system(cmd2)
        # -- Add coordinates attribute
        # -- set FillValue

# %% cell 16
pattern = '/data/jservon/IPCC/HI_NOAA/CMIP6/${member}_${thres}_${experiment}_${clim_period}.nc'
cproject('HI_cmip6_ch12','experiment','clim_period','member',('period','fx'),('thres','Exceed41'), ('variable','HI'), ensemble=['member'], separator='%')
dataloc(project='HI_cmip6_ch12', url=pattern)

# %% cell 17
pattern = '/data/jservon/IPCC/HI_NOAA/CORDEX/${CORDEX_domain}/${member}_${thres}_${experiment}_${period}.nc'
cproject('HI_cordex_ch12','experiment','period','CORDEX_domain','member','thres', ('variable','HI'), ensemble=['member'], separator='%')
dataloc(project='HI_cordex_ch12', url=pattern) 
pattern_gwl = '/data/jservon/IPCC/HI_NOAA/CORDEX/${CORDEX_domain}/${member}_${thres}_${experiment}_${GWL}.nc'
cproject('HI_cordex_GWL_ch12','experiment','CORDEX_domain',('period','fx'),'GWL','member','thres', ('variable','HI'), ensemble=['member'], separator='%')
dataloc(project='HI_cordex_GWL_ch12', url=pattern_gwl)

# %% cell 18
pattern = '/data/jservon/IPCC/HI_NOAA/CORDEX/${CORDEX_domain}/${member}_${thres}_${experiment}_${clim_period}.nc'
cproject('HI_cordex_ch12_test','experiment',('period','fx'),'clim_period','CORDEX_domain','member','thres', ('variable','HI'), ensemble=['member'], separator='%')
dataloc(project='HI_cordex_ch12_test', url=pattern)

# %% cell 20
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

# %% cell 22
wthres = '41'
thres = 'Exceed'+wthres

# %% cell 23
thres = 'Exceed'+wthres

exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='ssp585',
         clim_period = '1995-2014'),    
    # -- Mid term
    dict(experiment='ssp585',
         clim_period = '2041-2060'),
    dict(experiment='ssp126',
         clim_period = '2041-2060'),
    # -- Late term
    dict(experiment='ssp585',
         clim_period = '2081-2100'),
    dict(experiment='ssp126',
         clim_period = '2081-2100'),
]

# -- Loop on the scenarios
ens_exp_dict = dict()
for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    clim_period = exp['clim_period']
    
    # -- Create ensemble object for the scenario
    req_exp = ds(project='HI_cmip6_ch12',
                 experiment = experiment,
                 clim_period = clim_period,
                 member = '*',
                 #thres = thres
                )
    ens_exp = req_exp.explore('ensemble')
    
    # -- Climatologies
    ens_exp_dict[experiment+'_'+clim_period] = clim_average(ens_exp, 'ANM')

# %% cell 25

thres = 'Exceed'+wthres
variable = 'wbgt'

# -- Loop on the scenarios
ens_GWL_dict = dict()
for GWL in ['1.5K','2.0K','3.0K','4.0K']:
    #
    if GWL in ['1.5K','2.0K']:
        # -- Create ensemble object for the scenario
        req_ssp126 = ds(project='HI_cmip6_ch12',
                     experiment = 'ssp126',
                     clim_period = GWL,
                     member = '*'
                     )
        ens_ssp126 = req_ssp126.explore('ensemble')

        # -- Create ensemble object for the scenario
        req_ssp585 = ds(project='HI_cmip6_ch12',
                     experiment = 'ssp585',
                     clim_period = GWL,
                     member = '*',
                    )
        ens_ssp585 = req_ssp585.explore('ensemble')
        #
        # -- Merge ensembles
        GWL_ens = merge_climaf_ensembles([add_prefix_suffix_to_ens_req(ens_ssp126,suffix='_ssp126'),
                                          add_prefix_suffix_to_ens_req(ens_ssp585,suffix='_ssp585')])
    else:
        # -- Create ensemble object for the scenario
        req_ssp585 = ds(project='HI_cmip6_ch12',
                     experiment = 'ssp585',
                     clim_period = GWL,
                     member = '*',
                    )
        GWL_ens = req_ssp585.explore('ensemble')
        
    # -- Climatologies
    ens_GWL_dict[GWL] = clim_average(GWL_ens, 'ANM')

# %% cell 26
ens_GWL_dict['1.5K'].keys()

# %% cell 27
ens_exp_dict.keys()

# %% cell 28
regional_averages = dict()

# -- Loop on experiments / horizons
for ens_exp in ens_exp_dict:
    print ens_exp
    regional_averages[ens_exp] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_exp_dict[ens_exp]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'HI', 'all')
        region_names = tmp.abbrevs
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            print region_name
            region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name))[0].values)
            if region_name not in regional_averages[ens_exp]:
                regional_averages[ens_exp][region_name] = [region_value]
            else:
                regional_averages[ens_exp][region_name].append(region_value)

# %% cell 29
for GWL in ens_GWL_dict :
    print GWL
    regional_averages[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_GWL_dict[GWL]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        tmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]), 'HI', 'all')
        region_names = tmp.abbrevs
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            print region_name
            region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name))[0].values)
            if region_name not in regional_averages[GWL]:
                regional_averages[GWL][region_name] = [region_value]
            else:
                regional_averages[GWL][region_name].append(region_value)

# %% cell 31
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

# %% cell 32
import json
ensemble = 'CMIP6'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.2/'+ensemble+'_HI'+wthres+'_AR6_regional_averages.json'
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 34
regional_averages_diff = dict()

# -- Loop on experiments / horizons
#wind_ens_clim_exp_dict[exp]
for ens_exp in ens_exp_dict:
    if ens_exp not in ['ssp585_1995-2014']:
        print ens_exp
        regional_averages_diff[ens_exp] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_exp_dict[ens_exp]:
            if mem in ens_exp_dict['ssp585_1995-2014']:
                print mem
                # -- Compute the averages for each AR6 region thanks to regionmask
                tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'HI', 'all')
                tmp_baseline = average_over_AR6_region(cfile(ens_exp_dict['ssp585_1995-2014'][mem]), 'HI', 'all')
                region_names = tmp.abbrevs
                for tmp_region_name in region_names:
                    region_name = str(tmp_region_name.values)
                    region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                    region_value_baseline = float(tmp_baseline.sel(region=list(tmp.abbrevs).index(region_name)).values)
                    if region_name not in regional_averages_diff[ens_exp]:
                        regional_averages_diff[ens_exp][region_name] = [region_value - region_value_baseline]
                    else:
                        regional_averages_diff[ens_exp][region_name].append(region_value - region_value_baseline)
        #

# %% cell 35
for GWL in ens_GWL_dict:
    print GWL
    regional_averages_diff[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_GWL_dict[GWL]:
        wmem = mem.replace('_ssp585','').replace('_ssp126','')
        if wmem in ens_exp_dict['ssp585_1995-2014']:
            print wmem
            # -- Compute the averages for each AR6 region thanks to regionmask
            tmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]), 'HI', 'all')
            tmp_baseline = average_over_AR6_region(cfile(ens_exp_dict['ssp585_1995-2014'][wmem]), 'HI', 'all')
            region_names = tmp.abbrevs
            for tmp_region_name in region_names:
                region_name = str(tmp_region_name.values)
                region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                region_value_baseline = float(tmp_baseline.sel(region=list(tmp_baseline.abbrevs).index(region_name)).values)
                if region_name not in regional_averages_diff[GWL]:
                    regional_averages_diff[GWL][region_name] = [region_value - region_value_baseline]
                else:
                    regional_averages_diff[GWL][region_name].append(region_value - region_value_baseline)

# %% cell 36
quantiles_dict = dict()
for clim_period in regional_averages_diff:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages_diff[clim_period]:
        print clim_period, region_name
        quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages_diff[clim_period][region_name])
        q10 = np.quantile(dat, 0.1)
        q50 = np.quantile(dat, 0.5)
        q90 = np.quantile(dat, 0.9)
        quantiles_dict[clim_period][region_name] = [q10, q50, q90]

import json

ensemble = 'CMIP6'
outfilename = '/home/jservon/Chapter12_IPCC/data/HI_satellites/'+ensemble+'_HI'+wthres+'_diff_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 38
pattern = '/data/jservon/IPCC/HI_NOAA/CMIP5/${member}_${thres}_${experiment}_${clim_period}.nc'
cproject('HI_cmip5_ch12','experiment','clim_period','member',('period','fx'),('thres','Exceed41'), ('variable','HI'), ensemble=['member'], separator='%')
dataloc(project='HI_cmip5_ch12', url=pattern)

# %% cell 39
thres = 'Exceed'+wthres
# -- Scenarios - timelines
# ---------------------------------------------------------------------------

exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='rcp85',
         clim_period = '1995-2014'),    
    # -- Mid term
    dict(experiment='rcp85',
         clim_period = '2041-2060'),
    dict(experiment='rcp26',
         clim_period = '2041-2060'),
    # -- Late term
    dict(experiment='rcp85',
         clim_period = '2081-2100'),
    dict(experiment='rcp26',
         clim_period = '2081-2100'),
]

# -- Loop on the scenarios
ens_exp_dict = dict()
for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    clim_period = exp['clim_period']
    
    # -- Create ensemble object for the scenario
    req_exp = ds(project='HI_cmip5_ch12',
                 experiment = experiment,
                 clim_period = clim_period,
                 member = '*',
                )
    ens_exp = req_exp.explore('ensemble')
    
    # -- Climatologies
    ens_exp_dict[experiment+'_'+clim_period] = clim_average(ens_exp, 'ANM')
#

# %% cell 40
# -- Global Warming Levels
# ---------------------------------------------------------------------------
ens_GWL_dict = dict()

# -- Loop on the GWLs
for GWL in ['1.5K','2.0K','3.0K','4.0K']:
    #
    if GWL in ['1.5K','2.0K']:
        # -- Create ensemble object for the scenario
        req_rcp26 = ds(project='HI_cmip5_ch12',
                     experiment = 'rcp26',
                     clim_period = GWL,
                     member = '*',
                    )
        ens_rcp26 = req_rcp26.explore('ensemble')

        # -- Create ensemble object for the scenario
        req_rcp85 = ds(project='HI_cmip5_ch12',
                     experiment = 'rcp85',
                     clim_period = GWL,
                     member = '*',
                    )
        ens_rcp85 = req_rcp85.explore('ensemble')
        #
        # -- Merge ensembles
        GWL_ens = merge_climaf_ensembles([add_prefix_suffix_to_ens_req(ens_rcp26,suffix='_rcp26'),
                                          add_prefix_suffix_to_ens_req(ens_rcp85,suffix='_rcp85')])
    else:
        # -- Create ensemble object for the scenario
        req_rcp85 = ds(project='HI_cmip5_ch12',
                     experiment = 'rcp85',
                     clim_period = GWL,
                     member = '*',
                    )
        GWL_ens = req_rcp85.explore('ensemble')
        
    # -- Climatologies
    ens_GWL_dict[GWL] = clim_average(GWL_ens, 'ANM')

# %% cell 41
ens_GWL_dict

# %% cell 42
regional_averages_CMIP5 = dict()

# -- Loop on experiments / horizons
for ens_exp in ens_exp_dict:
    print ens_exp
    regional_averages_CMIP5[ens_exp] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_exp_dict[ens_exp]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'HI', 'all')
        region_names = tmp.abbrevs
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            #print region_name
            region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name))[0].values)
            if region_name not in regional_averages_CMIP5[ens_exp]:
                regional_averages_CMIP5[ens_exp][region_name] = [region_value]
            else:
                regional_averages_CMIP5[ens_exp][region_name].append(region_value)

for GWL in ens_GWL_dict :
    print GWL
    regional_averages_CMIP5[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_GWL_dict[GWL]:
        print mem
        # -- Compute the averages for each AR6 region thanks to regionmask
        tmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]), 'HI', 'all')
        region_names = tmp.abbrevs
        for tmp_region_name in region_names:
            region_name = str(tmp_region_name.values)
            #print region_name
            region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name))[0].values)
            if region_name not in regional_averages_CMIP5[GWL]:
                regional_averages_CMIP5[GWL][region_name] = [region_value]
            else:
                regional_averages_CMIP5[GWL][region_name].append(region_value)

# %% cell 43
regional_averages

# %% cell 44
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

# %% cell 45
import json
ensemble = 'CMIP5'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.2/'+ensemble+'_HI'+wthres+'_AR6_regional_averages.json'
print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 47
regional_averages_diff = dict()

# -- Loop on experiments / horizons
#wind_ens_clim_exp_dict[exp]
for ens_exp in ens_exp_dict:
    if ens_exp not in ['rcp85_1995-2014']:
        print ens_exp
        regional_averages_diff[ens_exp] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_exp_dict[ens_exp]:
            if mem in ens_exp_dict['rcp85_1995-2014']:
                print mem
                # -- Compute the averages for each AR6 region thanks to regionmask
                tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'HI', 'all')
                tmp_baseline = average_over_AR6_region(cfile(ens_exp_dict['rcp85_1995-2014'][mem]), 'HI', 'all')
                region_names = tmp.abbrevs
                for tmp_region_name in region_names:
                    region_name = str(tmp_region_name.values)
                    region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                    region_value_baseline = float(tmp_baseline.sel(region=list(tmp.abbrevs).index(region_name)).values)
                    if region_name not in regional_averages_diff[ens_exp]:
                        regional_averages_diff[ens_exp][region_name] = [region_value - region_value_baseline]
                    else:
                        regional_averages_diff[ens_exp][region_name].append(region_value - region_value_baseline)
        #

# %% cell 48
for GWL in ens_GWL_dict:
    print GWL
    regional_averages_diff[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_GWL_dict[GWL]:
        wmem = mem.replace('_rcp85','').replace('_rcp26','')
        #if mem.replace('_85','').replace('_26','') in ens_exp_dict['historical_1995-2014']:
        if wmem in ens_exp_dict['rcp85_1995-2014']:
            print wmem
            # -- Compute the averages for each AR6 region thanks to regionmask
            tmp = average_over_AR6_region(cfile(ens_GWL_dict[GWL][mem]), 'HI', 'all')
            tmp_baseline = average_over_AR6_region(cfile(ens_exp_dict['rcp85_1995-2014'][wmem]), 'HI', 'all')
            region_names = tmp.abbrevs
            for tmp_region_name in region_names:
                region_name = str(tmp_region_name.values)
                region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                region_value_baseline = float(tmp_baseline.sel(region=list(tmp_baseline.abbrevs).index(region_name)).values)
                if region_name not in regional_averages_diff[GWL]:
                    regional_averages_diff[GWL][region_name] = [region_value - region_value_baseline]
                else:
                    regional_averages_diff[GWL][region_name].append(region_value - region_value_baseline)

# %% cell 49
quantiles_dict = dict()
for clim_period in regional_averages_diff:
    quantiles_dict[clim_period] = dict()
    for region_name in regional_averages_diff[clim_period]:
        print clim_period, region_name
        quantiles_dict[clim_period][region_name] = dict()
        dat = np.array(regional_averages_diff[clim_period][region_name])
        q10 = np.quantile(dat, 0.1)
        q50 = np.quantile(dat, 0.5)
        q90 = np.quantile(dat, 0.9)
        quantiles_dict[clim_period][region_name] = [q10, q50, q90]

import json

ensemble = 'CMIP5'
outfilename = '/home/jservon/Chapter12_IPCC/data/HI_satellites/'+ensemble+'_HI'+wthres+'_diff_AR6_regional_averages.json'
print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 51
clog('critical')
wthres = '41'
thres = 'Exceed'+wthres
# -- Scenarios - timelines
# ---------------------------------------------------------------------------
CORDEX_domains = [
    # -- Africa
    'AFR-22','AFR-44',
    # -- AustralAsia
    'AUS-22','AUS-44',
    # -- Central America
    'CAM-22','CAM-44',
    # -- North America
    'NAM-22','NAM-44',
    # -- South America
    'SAM-22','SAM-44',
    # -- Asia
    'EAS-22','EAS-44',
    'WAS-22','WAS-44',
    'SEA-22',
    # -- Europe
    'EUR-11',    
]

exp_list = [
    # -- Baseline (ssp126 and ssp585 are the same files)
    dict(experiment='rcp85',
         period = '1995-2014'),    
    # -- Mid term
    dict(experiment='rcp85',
         period = '2041-2060'),
    dict(experiment='rcp26',
         period = '2041-2060'),
    # -- Late term
    dict(experiment='rcp85',
         period = '2081-2100'),
    dict(experiment='rcp26',
         period = '2081-2100'),
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
        period = exp['period']

        # -- Create ensemble object for the scenario
        req_exp = ds(project='HI_cordex_ch12_test',
                     experiment = experiment,
                     #realization='r1i1p1',
                     clim_period = period,
                     CORDEX_domain = CORDEX_domain,
                     member = '*',
                     thres = thres
                    )
        try:
            ens_exp = add_prefix_suffix_to_ens_req(req_exp.explore('ensemble'), suffix='_'+CORDEX_domain)
            #
            # -- Climatologies
            # If there is already a short_CORDEX_domain in the results, we merge the results of the new one
            if experiment+'_'+period in ens_exp_dict_CORDEX[short_CORDEX_domain]:
                ens_exp_dict_CORDEX[short_CORDEX_domain][experiment+'_'+period].update( clim_average(ens_exp, 'ANM') )
            else:
                ens_exp_dict_CORDEX[short_CORDEX_domain][experiment+'_'+period] = clim_average(ens_exp, 'ANM')
        except:
            print 'no data found for ', req_exp
    #


    # -- Global Warming Levels
    # ---------------------------------------------------------------------------
    ens_GWL_dict_CORDEX[short_CORDEX_domain] = dict()

    # -- Loop on the GWLs
    for GWL in ['1.5K','2.0K','3.0K','4.0K']:
        #
        if GWL in ['1.5K']:
            # -- Create ensemble object for the scenario
            req_rcp26 = ds(project='HI_cordex_ch12_test',
                         experiment = 'rcp26',
                         #realization='r1i1p1',
                         clim_period = GWL,
                         CORDEX_domain = CORDEX_domain,
                         member = '*',
                         thres = thres
                        )
            try:
                ens_rcp26 = req_rcp26.explore('ensemble')
            except:
                print 'No data found for ',req_rcp26
                ens_rcp26 = cens(dict())

            # -- Create ensemble object for the scenario
            req_rcp85 = ds(project='HI_cordex_ch12_test',
                         experiment = 'rcp85',
                         #  realization='r1i1p1',
                         clim_period = GWL,
                         CORDEX_domain = CORDEX_domain,
                         member = '*',
                         thres = thres
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
            req_rcp85 = ds(project='HI_cordex_ch12_test',
                         experiment = 'rcp85',
                         #  realization='r1i1p1',
                         clim_period = GWL,
                         CORDEX_domain = CORDEX_domain,
                         member = '*',
                         thres = thres
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

# %% cell 52
#
# -- Loop on the short CORDEX domains
# -- short_CORDEX_domains = ['AFR','EAS',...]
regional_averages_CORDEX = dict()

# -- Merge the dictionary with scenarios and the one with the GWLs
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
                                'HI', 'all')
                    region_names = tmp.abbrevs
                    #for tmp_region_name in region_names:
                    for tmp_region_name in AR6regions_by_CORDEX_domain[short_CORDEX_domain]:
                        #region_name = str(tmp_region_name.values)
                        region_name = tmp_region_name
                        print region_name
                        region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name))[0].values)
                        if region_name not in regional_averages_CORDEX[short_CORDEX_domain][ens_exp]:
                            regional_averages_CORDEX[short_CORDEX_domain][ens_exp][region_name] = [region_value]
                        else:
                            regional_averages_CORDEX[short_CORDEX_domain][ens_exp][region_name].append(region_value)

# %% cell 53
regional_averages_CORDEX['EUR']

# %% cell 54
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
            if len(wdat)>=5:
                q10 = np.quantile(wdat, 0.1)
                q50 = np.quantile(wdat, 0.5)
                q90 = np.quantile(wdat, 0.9)
                quantiles_dict[clim_period][region_name] = [q10, q50, q90]
            else:
                print 'Not enough data for ',clim_period, region_name
                quantiles_dict[clim_period][region_name] = [-99999, -99999, -99999]

# %% cell 55
regional_averages_CORDEX[short_CORDEX_domain].keys()

# %% cell 56
import json
ensemble = 'CORDEX'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.2/'+ensemble+'_HI'+wthres+'_AR6_regional_averages.json'
print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)
