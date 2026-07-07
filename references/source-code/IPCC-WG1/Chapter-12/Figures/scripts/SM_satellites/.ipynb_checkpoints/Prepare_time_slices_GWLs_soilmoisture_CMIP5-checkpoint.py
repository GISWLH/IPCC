# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/SM_satellites/.ipynb_checkpoints/Prepare_time_slices_GWLs_soilmoisture_CMIP5-checkpoint.ipynb

# %% cell 4
from climaf.api import *

# %% cell 6
lom_per_exp = dict()

# %% cell 7
req_dict = dict(project='CMIP5',
                frequency='monthly',
                table = 'Lmon',
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
             variable = 'mrso',
             **wreq
            )
    models = req.explore('choices')['model']
    ok_models = []
    for model in models:
        req_test = ds(model=model,
                     variable = 'mrso',
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
                        variable = 'mrso',
                        **wreq_dict
                       )

wreq_dict = req_dict.copy()
wreq_dict.update(exp_dict_list['baseline_ext'])
ens_baseline_ext = eds(model=common_lom_baseline,
                       variable = 'mrso',
                       **wreq_dict
                      )

# %% cell 13
csync(True)

# %% cell 14
ens_baseline_dict = dict()
for model in common_lom_baseline:
    
    # -- Cat baseline and ext
    ens_baseline_dict[model] = ccdo2(ens_baseline_hist[model], ens_baseline_ext[model], operator='cat')
    print(model)
    
    print(cfile(ens_baseline_dict[model]))

# %% cell 16
ens_clim_exp_dict = dict()

for exp in ['rcp26_mid','rcp26_far','rcp85_mid','rcp85_far']:    
    print '--> '+exp
    ens_clim_exp_dict[exp] = clim_average(cens(ens_exp_dict[exp]), 'ANM')

# %% cell 18
for exp in ens_exp_dict:
    for mem in ens_exp_dict[exp]:
        print ens_exp_dict[exp][mem]

# %% cell 19
ds('CMIP5%%mrso%2006-2015%global%/bdd%CESM1-CAM5%Lmon%rcp85%r1i1p1%monthly%land%latest').baseFiles()

# %% cell 20
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

# %% cell 21
new_rows = []
for row in rows:
    if (len(row)==1):
        print row[0].split(',')
        new_rows.append(row[0].split(','))
    else:
        print row
        new_rows.append(row)

# %% cell 22
import csv
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.4/CMIP5_mrso_time_periods.csv'

with open(output_metadata_filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|')
    for row in new_rows:
        writer.writerow(row)

# %% cell 26
ens_baseline = cens(ens_baseline_dict)
ens_clim_exp_dict['baseline'] = clim_average(ens_baseline, 'ANM')

# %% cell 27
ens_clim_exp_dict['baseline'].keys()

# %% cell 28
diff = fdiv(fsub(cens(ens_clim_exp_dict['rcp85_far']), cens(ens_clim_exp_dict['baseline'])),cens(ens_clim_exp_dict['baseline']))

# %% cell 29
iplot_members(diff, proj='Robinson', N=1, color='MPL_BrBg',
              min=-0.3, max=0.3, delta=0.05, focus='land')

# %% cell 30
iplot_members(diff, proj='Robinson', N=2, color='MPL_BrBg',
              min=-0.3, max=0.3, delta=0.05, focus='land')

# %% cell 31
iplot_members(diff, proj='Robinson', N=3, color='MPL_BrBg',
              min=-0.3, max=0.3, delta=0.05, focus='land')

# %% cell 32
iplot_members(diff, proj='Robinson', N=4, color='MPL_BrBg',
              min=-0.3, max=0.3, delta=0.05, focus='land')

# %% cell 34
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

# %% cell 35
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
                             variable = 'mrso',
                             **req_dict
                             )
                    ens_dict_per_GWL[GWL][wmodel+'_'+scenario] = clim_average(dat, 'ANM')
                    print cfile(ens_dict_per_GWL[GWL][wmodel+'_'+scenario])
        else:
            print 'We dont have GWL info for ',wmodel

# %% cell 36
ens_dict_per_GWL[GWL]

# %% cell 37
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

# %% cell 38
import csv
output_metadata_filename = '/home/jservon/Chapter12_IPCC/data/Figure_S12.4/CMIP5_mrso_gwl.csv'

with open(output_metadata_filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|')
    for row in rows:
        writer.writerow(row)

# %% cell 39
rows

# %% cell 40
#We dont have GWL info for  GISS-E2-H
#We dont have GWL info for  GISS-E2-R
#We dont have GWL info for  GISS-E2-H-CC
#We dont have GWL info for  GISS-E2-R-CC
#We dont have GWL info for  HadGEM2-AO
#We dont have GWL info for  CMCC-CESM
#We dont have GWL info for  MRI-ESM1

# %% cell 43
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

# %% cell 45
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

# %% cell 46
ens_clim_exp_dict[ens_exp].keys()

# %% cell 47
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

# %% cell 50
ens_baseline_dict.keys()

# %% cell 51
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

# %% cell 53
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

# %% cell 55
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

# %% cell 57
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

# %% cell 58
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
