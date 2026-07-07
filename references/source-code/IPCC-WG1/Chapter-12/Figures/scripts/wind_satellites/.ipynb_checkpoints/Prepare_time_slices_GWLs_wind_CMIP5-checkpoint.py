# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/wind_satellites/.ipynb_checkpoints/Prepare_time_slices_GWLs_wind_CMIP5-checkpoint.ipynb

# %% cell 4
from climaf.api import *

# %% cell 5
csync(True)

# %% cell 7
lom_per_exp = dict()

# %% cell 8
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
             #variable = 'tas',
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
        #if not check_time_consistency_CMIP(req_test):
        #        print model+' not fully covered'
        #else:
        #        print model+' is fine'
        ok_models.append(model)
        ens_exp_dict[exp][model] = req_test.explore('resolve')

    lom_per_exp[exp] = ok_models

# %% cell 10
lom_baseline     = lom_per_exp['baseline']
lom_baseline_ext = lom_per_exp['rcp26_mid']
#lom_baseline_ext = lom_per_exp['baseline_ext']
print 'Models not in both sets:'
print set(lom_baseline) ^ set(lom_baseline_ext)
print 'Models in common:'
common_lom_baseline = list( set(lom_baseline) & set(lom_baseline_ext) )
print sorted(common_lom_baseline)

# %% cell 11
lom_baseline_ext

# %% cell 13
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

# %% cell 16
ens_baseline_dict = dict()
for model in common_lom_baseline:
    
    # -- Cat baseline and ext
    ens_baseline_dict[model] = ccdo2(ens_baseline_hist[model], ens_baseline_ext[model], operator='cat')
    print(model)
    
    print(cfile(ens_baseline_dict[model]))

# %% cell 18
wind_ens_clim_exp_dict = dict()

for exp in ['rcp26_mid','rcp26_far','rcp85_mid','rcp85_far']:    
    print '--> '+exp
    wind_ens_clim_exp_dict[exp] = clim_average(cens(ens_exp_dict[exp]), 'ANM')

# %% cell 20
ens_baseline = cens(ens_baseline_dict)
wind_ens_clim_exp_dict['baseline'] = clim_average(ens_baseline, 'ANM')

# %% cell 21
wind_ens_clim_exp_dict['baseline'].keys()

# %% cell 23
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

# %% cell 24
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
                if central_year not in ['NA','9999']:
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

# %% cell 25
ens_dict_per_GWL[GWL]

# %% cell 26
#We dont have GWL info for  GISS-E2-H
#We dont have GWL info for  GISS-E2-R
#We dont have GWL info for  GISS-E2-H-CC
#We dont have GWL info for  GISS-E2-R-CC
#We dont have GWL info for  HadGEM2-AO
#We dont have GWL info for  CMCC-CESM
#We dont have GWL info for  MRI-ESM1

# %% cell 29
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

# %% cell 31
if None:
    regional_averages_CMIP5 = dict()

    # -- Loop on experiments / horizons
    #wind_ens_clim_exp_dict[exp]
    for ens_exp in wind_ens_clim_exp_dict:
        print ens_exp
        regional_averages_CMIP5[ens_exp] = dict()
        # -- Loop on the members of each ensemble
        for mem in wind_ens_clim_exp_dict[ens_exp]:
            print mem
            # -- Compute the averages for each AR6 region thanks to regionmask
            tmp = average_over_AR6_region(cfile(wind_ens_clim_exp_dict[ens_exp][mem]), 'sfcWind', 'all')
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

# %% cell 33
ens_baseline_dict.keys()

# %% cell 34
#
regional_averages_diff_CMIP5 = dict()
# -- Loop on experiments / horizons
#wind_ens_clim_exp_dict[exp]
for ens_exp in wind_ens_clim_exp_dict:
    if ens_exp not in ['baseline']:
        print ens_exp
        regional_averages_diff_CMIP5[ens_exp] = dict()
        # -- Loop on the members of each ensemble
        for mem in wind_ens_clim_exp_dict[ens_exp]:
            if mem.split('_')[0] in ens_baseline_dict:
                print mem
                # -- Compute the averages for each AR6 region thanks to regionmask
                tmp = average_over_AR6_region(cfile(wind_ens_clim_exp_dict[ens_exp][mem]), 'sfcWind', 'all')
                region_names = list(tmp.abbrevs)
                ttmp = average_over_AR6_region(cfile(wind_ens_clim_exp_dict[ens_exp][mem]), 'sfcWind', region_names)
                ttmp_baseline = average_over_AR6_region(cfile(wind_ens_clim_exp_dict['baseline'][mem]), 'sfcWind', region_names)
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
    for ens_exp in wind_ens_clim_exp_dict:
        if ens_exp not in ['baseline']:
            print ens_exp
            regional_averages_diff_CMIP5[ens_exp] = dict()
            # -- Loop on the members of each ensemble
            for mem in wind_ens_clim_exp_dict[ens_exp]:
                if mem.split('_')[0] in ens_baseline_dict:
                    print mem
                    # -- Compute the averages for each AR6 region thanks to regionmask
                    tmp = average_over_AR6_region(cfile(wind_ens_clim_exp_dict[ens_exp][mem]), 'sfcWind', 'all')
                    tmp_baseline = average_over_AR6_region(cfile(wind_ens_clim_exp_dict['baseline'][mem]), 'sfcWind', 'all')
                    region_names = tmp.abbrevs
                    for tmp_region_name in region_names:
                        region_name = str(tmp_region_name.values)
                        #print region_name
                        region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                        region_value_baseline = float(tmp_baseline.sel(region=list(tmp.abbrevs).index(region_name)).values)
                        tmpval = 100 * (region_value - region_value_baseline) / region_value_baseline
                        if region_name not in regional_averages_diff_CMIP5[ens_exp]:
                            regional_averages_diff_CMIP5[ens_exp][region_name] = [tmpval]
                        else:
                            regional_averages_diff_CMIP5[ens_exp][region_name].append(tmpval)
            #

# %% cell 36
if None:
    for GWL in ens_dict_per_GWL:
        print GWL
        regional_averages_CMIP5[GWL] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_dict_per_GWL[GWL]:
            print mem
            # -- Compute the averages for each AR6 region thanks to regionmask
            tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'sfcWind', 'all')
            region_names = tmp.abbrevs
            for tmp_region_name in region_names:
                region_name = str(tmp_region_name.values)
                #print region_name
                region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                if region_name not in regional_averages_CMIP5[GWL]:
                    regional_averages_CMIP5[GWL][region_name] = [region_value]
                else:
                    regional_averages_CMIP5[GWL][region_name].append(region_value)

# %% cell 38
for GWL in ens_dict_per_GWL:
    print GWL
    regional_averages_diff_CMIP5[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_dict_per_GWL[GWL]:
        wmem = mem.replace('_26','').replace('_85','')
        print wmem
        if wmem in ens_baseline_dict:
            print mem
            tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'sfcWind', 'all')
            region_names = list(tmp.abbrevs)
            ttmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'sfcWind', region_names)
            ttmp_baseline = average_over_AR6_region(cfile(wind_ens_clim_exp_dict['baseline'][wmem]), 'sfcWind', region_names)
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
                tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'sfcWind', 'all')
                tmp_baseline = average_over_AR6_region(cfile(wind_ens_clim_exp_dict['baseline'][wmem]), 'sfcWind', 'all')
                region_names = tmp.abbrevs
                for tmp_region_name in region_names:
                    region_name = str(tmp_region_name.values)
                    #print region_name
                    region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                    region_value_baseline = float(tmp_baseline.sel(region=list(tmp.abbrevs).index(region_name)).values)
                    tmpval = 100 * (region_value - region_value_baseline) / region_value_baseline
                    if region_name not in regional_averages_diff_CMIP5[GWL]:
                        regional_averages_diff_CMIP5[GWL][region_name] = [tmpval]
                    else:
                        regional_averages_diff_CMIP5[GWL][region_name].append(tmpval)

# %% cell 40
if None:
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
    outfilename = '/home/jservon/Chapter12_IPCC/data/wind_satellites/'+ensemble+'_sfcWind_AR6_regional_averages.json'
    #print outfilename
    with open(outfilename, 'w') as fp:
        json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 41
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
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.5/'+ensemble+'_sfcWind_diff-perc-baseline_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 42
# -- Get the list of models that have both uas and vas
# -- create the ensemble and compute sfcWind

# -- historical 1995_2014 (cat historical and rcp85)
# -- rcp85 2041-2060 and 2081-2100
# -- rcp26 2041-2060 and 2081-2100
# -- GWLs => use the file

# %% cell 44
from climaf.api import *

# %% cell 45
# -- Function to split a multi-member file in individual files
# -- Uses Xarray
def split_ensemble_file(ensemble_file, output_pattern, variable):
    if not os.path.isdir(os.path.dirname(output_pattern)):
        os.makedirs(os.path.dirname(output_pattern))
    import xarray as xr
    dat = xr.open_dataset(ensemble_file)[variable]
    for member in dat.member:
        member_name = str(member.values)
        print member_name
        outfilename = output_pattern+member_name+'.nc'
        if not os.path.isfile(outfilename):
            print 'Save '+outfilename
            member_dat = dat.loc[:,member_name,:,:]
            member_dat.to_netcdf(outfilename)
        else:
            print outfilename+' already exists'

variable='wind'
exp_list = [
    #dict(experiment='historical',
    #     period = '1995-2014'),
    #dict(experiment='ssp585',
    #     period = '2041-2060'),
    #dict(experiment='ssp585',
    #     period = '2081-2100'),
    #dict(experiment='ssp126',
    #     period = '2081-2100'),
    dict(experiment='ssp126',
         years = range(2041,2061)),
]
for exp_dict in exp_list:
    years = exp_dict['years']
    experiment = exp_dict['experiment']
    for year in years:
        wfile = '/data/jservon/IPCC/wind/CMIP6_wind/CMIP6Amon_'+experiment+'_'+variable+'_'+str(year)+'.nc4'
        output_pattern = '/data/jservon/IPCC/wind/individual_models/CMIP6_'+experiment+'_'+variable+'_'+str(year)+'_'
        split_ensemble_file(wfile, output_pattern, variable)
#

# %% cell 46
pattern = '/data/jservon/IPCC/${variable}/individual_models/CMIP6_${experiment}_${variable}_${period}_${member}.nc'
cproject('wind_individual_models_cmip6_ch12','experiment','period','member',('variable','wind'), ensemble=['member'], separator='%')
dataloc(project='wind_individual_models_cmip6_ch12', url=pattern)

# %% cell 48
## Baseline + GWL + time slices = ok...

# %% cell 49
req_dict = dict(project='wind_individual_models_cmip6_ch12')

req = ds(experiment='historical', period='1995-2014', member='*',project='wind_individual_models_cmip6_ch12')
req.explore('choices')

# %% cell 50
exp_list = [
    dict(experiment='historical',
         period = '1995-2014'),
    dict(experiment='ssp585',
         period = '2041-2060'),
    dict(experiment='ssp585',
         period = '2081-2100'),
    dict(experiment='ssp126',
         period = '2081-2100'),
    dict(experiment='ssp126',
         period = '2041-2060'),
]

ens_exp_dict = dict()
for exp in exp_list:
        experiment = exp['experiment']
        period = exp['period']
        
        req = ds(experiment=experiment,
                 period=period,
                 member='*',
                 project='wind_individual_models_cmip6_ch12')

        ens_exp = req.explore('ensemble')
        #
        # -- Climatologies
        clim_exp      = clim_average(ens_exp, 'ANM')

        # -- Changes = Scenario minus baselines
        ens_exp_dict[experiment+'_'+period] = clim_exp

# %% cell 51
if None:
    regional_averages = dict()

    # -- Loop on experiments / horizons
    #wind_ens_clim_exp_dict[exp]
    for ens_exp in ens_exp_dict:
        print ens_exp
        regional_averages[ens_exp] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_exp_dict[ens_exp]:
            print mem
            # -- Compute the averages for each AR6 region thanks to regionmask
            #cmd = 'ncrename -v .uas,wind -v .vas,wind -v .sfcWind,wind '+cfile(ens_exp_dict[ens_exp][mem])
            #os.system(cmd)
            tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'wind', 'all')
            region_names = tmp.abbrevs
            for tmp_region_name in region_names:
                region_name = str(tmp_region_name.values)
                #print region_name
                region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                if region_name not in regional_averages[ens_exp]:
                    regional_averages[ens_exp][region_name] = [region_value]
                else:
                    regional_averages[ens_exp][region_name].append(region_value)
    #

# %% cell 52
regional_averages_diff = dict()

if None:
    # -- Loop on experiments / horizons
    #wind_ens_clim_exp_dict[exp]
    for ens_exp in ens_exp_dict:
        if ens_exp not in ['historical_1995-2014']:
            print ens_exp
            regional_averages_diff[ens_exp] = dict()
            # -- Loop on the members of each ensemble
            for mem in ens_exp_dict[ens_exp]:
                if mem in ens_exp_dict['historical_1995-2014']:
                    print mem
                    # -- Compute the averages for each AR6 region thanks to regionmask
                    #print cfile(ens_exp_dict[ens_exp][mem])
                    #cmd = 'ncrename -v .uas,wind -v .vas,wind -v .sfcWind,wind '+cfile(ens_exp_dict[ens_exp][mem])
                    #os.system(cmd)
                    tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'wind', 'all')
                    tmp_baseline = average_over_AR6_region(cfile(ens_exp_dict['historical_1995-2014'][mem]), 'wind', 'all')
                    region_names = tmp.abbrevs
                    for tmp_region_name in region_names:
                        region_name = str(tmp_region_name.values)
                        region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                        region_value_baseline = float(tmp_baseline.sel(region=list(tmp.abbrevs).index(region_name)).values)
                        tmpval = 100 * (region_value - region_value_baseline) / region_value_baseline
                        if region_name not in regional_averages_diff[ens_exp]:
                            regional_averages_diff[ens_exp][region_name] = [tmpval]
                        else:
                            regional_averages_diff[ens_exp][region_name].append(tmpval)
            #
#
for ens_exp in ens_exp_dict:
    if ens_exp not in ['historical_1995-2014']:
        print ens_exp
        regional_averages_diff[ens_exp] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_exp_dict[ens_exp]:
            if mem in ens_exp_dict['historical_1995-2014']:
                print mem
                # -- Compute the averages for each AR6 region thanks to regionmask
                tmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'wind', 'all')
                region_names = list(tmp.abbrevs)
                ttmp = average_over_AR6_region(cfile(ens_exp_dict[ens_exp][mem]), 'wind', region_names)
                ttmp_baseline = average_over_AR6_region(cfile(ens_exp_dict['historical_1995-2014'][mem]), 'wind', region_names)
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
                    if region_name not in regional_averages_diff[ens_exp]:
                        regional_averages_diff[ens_exp][region_name] = [perc_val]
                    else:
                        regional_averages_diff[ens_exp][region_name].append(perc_val)

# %% cell 53
#ssp585_2081-2100
#MIROC6_r1i1p1f1
#/data/jservon/climafcache/e2/3aa8cbaa06d21c19cecd4ac5847e4ed31be105f91dcddbd3f439c7.nc
#SES (EXP,baseline) =  1.83608290053 1.74512893604
#index =  14 14
#EXP obj =  time_average(c_sfcWind(cncks(ds('CMIP6%%uas%2081-2100%global%/bdd%MIROC6%MIROC%ScenarioMIP%Amon%ssp585%r1i1p1f1%gn%latest'),Var='uas'),cncks(ds('CMIP6%%vas%2081-2100%global%/bdd%MIROC6%MIROC%ScenarioMIP%Amon%ssp585%r1i1p1f1%gn%latest'),Var='vas')))
#Baseline obj =  time_average(c_sfcWind(cncks(ds('CMIP6%%uas%1995-2014%global%/bdd%MIROC6%MIROC%CMIP%Amon%historical%r1i1p1f1%gn%latest'),Var='uas'),cncks(ds('CMIP6%%vas%1995-2014%global%/bdd%MIROC6%MIROC%CMIP%Amon%historical%r1i1p1f1%gn%latest'),Var='vas')))
#Baseline file =  /data/jservon/climafcache/89/88b677481ac0958a3f066593a04705e5ee8611f0c16914be3bacf3.nc
#MRI-ESM2-0_r1i1p1f1
#/data/jservon/climafcache/4f/f8d395e93df6891a802dc978f83f993b48760459f93851542a48c6.nc

#ssp585_2081-2100
#MRI-ESM2-0_r1i1p1f1
#/data/jservon/climafcache/4f/f8d395e93df6891a802dc978f83f993b48760459f93851542a48c6.nc
#SES (EXP,baseline) =  1.90005605827 1.85712259389
#index =  14 14
#EXP obj =  time_average(c_sfcWind(cncks(ds('CMIP6%%uas%2081-2100%global%/bdd%MRI-ESM2-0%MRI%ScenarioMIP%Amon%ssp585%r1i1p1f1%gn%latest'),Var='uas'),cncks(ds('CMIP6%%vas%2081-2100%global%/bdd%MRI-ESM2-0%MRI%ScenarioMIP%Amon%ssp585%r1i1p1f1%gn%latest'),Var='vas')))
#EXP file =  time_average(c_sfcWind(cncks(ds('CMIP6%%uas%2081-2100%global%/bdd%MRI-ESM2-0%MRI%ScenarioMIP%Amon%ssp585%r1i1p1f1%gn%latest'),Var='uas'),cncks(ds('CMIP6%%vas%2081-2100%global%/bdd%MRI-ESM2-0%MRI%ScenarioMIP%Amon%ssp585%r1i1p1f1%gn%latest'),Var='vas')))
#Baseline obj =  time_average(c_sfcWind(cncks(ds('CMIP6%%uas%1995-2014%global%/bdd%MRI-ESM2-0%MRI%CMIP%Amon%historical%r1i1p1f1%gn%latest'),Var='uas'),cncks(ds('CMIP6%%vas%1995-2014%global%/bdd%MRI-ESM2-0%MRI%CMIP%Amon%historical%r1i1p1f1%gn%latest'),Var='vas')))
#Baseline file =  /data/jservon/climafcache/5f/dbb0242c5a3872ed87826a8919abcde87e63b892673fb983470e38.nc

# %% cell 55
import csv
GWL_csv = '/home/jservon/Chapter12_IPCC/scripts/ATLAS/warming-levels/CMIP6_Atlas_WarmingLevels.csv'

GWL_dict = dict()
i = 0
with open(GWL_csv) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')#, quotechar='|')
    for row in spamreader:
        print row
        model = row[0]#.split('_')[0]
        print model
        GWL_dict[model] = dict()
        if i==0:
            colnames = row
        j = 1
        for elt in row[1:len(row)]:
            print elt
            GWL_dict[model][colnames[j]] = row[j]
            j = j + 1
        i = i + 1

# %% cell 56
clog('critical')
ens_dict_per_GWL = dict()
list_of_GWLs = ['1.5','2','3','4']
for GWL in list_of_GWLs:
    ens_dict_per_GWL[GWL] = dict()


for scenario in ['26','85']:
    
    if scenario=='26': req_scenario = 'ssp126'
    if scenario=='85': req_scenario = 'ssp585'
    list_of_models = ens_exp_dict[req_scenario+'_2041-2060'].keys()
    for wmodel_realization in GWL_dict:
        if wmodel_realization:
            print wmodel_realization
            wmodel = wmodel_realization.split('_')[0]
            realization = wmodel_realization.split('_')[1]
            print wmodel
            print 'We have : ', wmodel_realization
            for GWL in list_of_GWLs:
                if scenario=='26': GWL_scenario = GWL+'_ssp126'
                if scenario=='85': GWL_scenario = GWL+'_ssp585'

                # --> file nc
                # --> period
                central_year = GWL_dict[wmodel_realization][GWL_scenario]
                if central_year not in ['NA','9999'] and int(central_year)>2025:
                    print 'central_year = ',central_year
                    start_year = str( int(central_year)-9 )
                    end_year = str( int(central_year)+10 )

                    dat_wind = ds(experiment=experiment,
                                 period=period,
                                 member=wmodel_realization,
                                 project='wind_individual_models_cmip6_ch12')

                    try:
                        #ens_dict_per_GWL[GWL][wmodel+'_'+scenario] = clim_average(c_sfcWind(dat_uas, dat_vas), 'ANM')
                        print cfile(clim_average(dat_wind, 'ANM'))
                        ens_dict_per_GWL[GWL][wmodel_realization+'_'+scenario] = clim_average(dat_wind, 'ANM')
                    except:
                        print 'An error occured for ',wmodel+'_'+scenario, GWL
        else:
            print 'We dont have GWL info for ',wmodel_realization

# %% cell 58
if None:
    # -- Loop on experiments / horizons
    for GWL in ens_dict_per_GWL:
        print GWL
        regional_averages[GWL] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_dict_per_GWL[GWL]:
            print mem
            # -- Compute the averages for each AR6 region thanks to regionmask
            cmd = 'ncrename -v .uas,wind -v .vas,wind -v .sfcWind,wind '+cfile(ens_dict_per_GWL[GWL][mem])
            os.system(cmd)
            tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'wind', 'all')
            region_names = tmp.abbrevs
            for tmp_region_name in region_names:
                region_name = str(tmp_region_name.values)
                #print region_name
                region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                if region_name not in regional_averages[GWL]:
                    regional_averages[GWL][region_name] = [region_value]
                else:
                    regional_averages[GWL][region_name].append(region_value)

# %% cell 60
for GWL in ens_dict_per_GWL:
    print GWL
    regional_averages_diff[GWL] = dict()
    # -- Loop on the members of each ensemble
    for mem in ens_dict_per_GWL[GWL]:
        wmem = mem.replace('_26','').replace('_85','')
        print wmem
        if wmem in ens_exp_dict['historical_1995-2014']:
            print mem
            tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'wind', 'all')
            region_names = list(tmp.abbrevs)
            ttmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'wind', region_names)
            ttmp_baseline = average_over_AR6_region(cfile(ens_exp_dict['historical_1995-2014'][wmem]), 'wind', region_names)
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
                if region_name not in regional_averages_diff[GWL]:
                    regional_averages_diff[GWL][region_name] = [perc_val]
                else:
                    regional_averages_diff[GWL][region_name].append(perc_val)

if None:
    #regional_averages = dict()
    # -- Loop on experiments / horizons
    for GWL in ens_dict_per_GWL:
        print GWL
        regional_averages_diff[GWL] = dict()
        # -- Loop on the members of each ensemble
        for mem in ens_dict_per_GWL[GWL]:
            wmem = mem.replace('_85','').replace('_26','')
            #if mem.replace('_85','').replace('_26','') in ens_exp_dict['historical_1995-2014']:
            if wmem in ens_exp_dict['historical_1995-2014']:
                print wmem
                # -- Compute the averages for each AR6 region thanks to regionmask
                cmd = 'ncrename -v .uas,wind -v .vas,wind -v .sfcWind,wind '+cfile(ens_dict_per_GWL[GWL][mem])
                #os.system(cmd)
                tmp = average_over_AR6_region(cfile(ens_dict_per_GWL[GWL][mem]), 'wind', 'all')
                tmp_baseline = average_over_AR6_region(cfile(ens_exp_dict['historical_1995-2014'][wmem]), 'wind', 'all')
                region_names = tmp.abbrevs
                for tmp_region_name in region_names:
                    region_name = str(tmp_region_name.values)
                    #print region_name
                    region_value = float(tmp.sel(region=list(tmp.abbrevs).index(region_name)).values)
                    region_value_baseline = float(tmp_baseline.sel(region=list(tmp_baseline.abbrevs).index(region_name)).values)
                    tmpval = 100 * (region_value - region_value_baseline) / region_value_baseline
                    if region_name not in regional_averages_diff[GWL]:
                        regional_averages_diff[GWL][region_name] = [tmpval]
                    else:
                        regional_averages_diff[GWL][region_name].append(tmpval)

# %% cell 62
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

ensemble = 'CMIP6'
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.5/'+ensemble+'_sfcWind_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 63
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
outfilename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.5/'+ensemble+'_sfcWind_diff-perc-baseline_AR6_regional_averages.json'
#print outfilename
with open(outfilename, 'w') as fp:
    json.dump(quantiles_dict, fp, sort_keys=True, indent=4)

# %% cell 64
#EC-Earth3-Veg_r1i1p1f1 ==> Archive a trous!
#An error occured for  EC-Earth3-Veg_85 1.5
#An error occured for  EC-Earth3-Veg_26 1.5

#NorESM2-LM_r1i1p1f1 ==> ni uas, ni vas, ni sfcWind
#An error occured for  NorESM2-LM_85 3

#NorESM2-MM_r1i1p1f1 ==> Archive a trous!
#NorESM2-MM_85 1.5

#UKESM1-0-LL_r1i1p1f2 ==> grids do not match
#An error occured for  UKESM1-0-LL_85 1.5
#An error occured for  UKESM1-0-LL_85 2
#An error occured for  UKESM1-0-LL_85 3
#An error occured for  UKESM1-0-LL_85 4

#FGOALS-g3_r1i1p1f1 ==> Archive a trous!
#An error occured for  FGOALS-g3_85 3

#KACE-1-0-G_r2i1p1f1 ==> grids do not match
#An error occured for  KACE-1-0-G_85 1.5
#An error occured for  KACE-1-0-G_85 2
#An error occured for  KACE-1-0-G_85 3
#An error occured for  KACE-1-0-G_85 4

#HadGEM3-GC31-LL_r1i1p1f3 ==> uas, mais pas vas!!!
#An error occured for  HadGEM3-GC31-LL_85 1.5
#An error occured for  HadGEM3-GC31-LL_85 2
