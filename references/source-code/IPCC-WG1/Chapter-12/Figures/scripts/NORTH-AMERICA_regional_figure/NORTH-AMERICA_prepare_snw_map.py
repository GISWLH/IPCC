# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/NORTH-AMERICA_regional_figure/NORTH-AMERICA_prepare_snw_map.ipynb

# %% cell 1
from climaf.api import *

# %% cell 2
CWD = os.getcwd()

# %% cell 3
import regionmask
import numpy as np
common_grid_filename = 'NORTH-AMERICA_raw_common_grid.nc'

lats = np.arange(0, 90, 0.2)
lons = np.arange(-175, -40, 0.2)
mask = regionmask.defined_regions.natural_earth.land_110.mask(lons, lats)
mask.to_netcdf(common_grid_filename)


def add_lonlat_variable_attributes(filename, variable):
    import os
    cmd = 'ncrename -v .__xarray_dataarray_variable__,'+variable+' -v .region,'+variable+' '+filename+' ; ncatted -O -a coordinates,'+variable+',o,c,"lon lat" -a units,lon,o,c,degrees_east -a units,lat,o,c,degrees_north -a standard_name,lon,o,c,longitude -a standard_name,lat,o,c,latitude '+filename
    print cmd
    os.system(cmd)
def add_lonlat_variable_attributes(filename, variable):
    import os
    cmd = 'ncrename -v .region,'+variable+' '+filename+' ; ncatted -O -a coordinates,'+variable+',o,c,"lon lat" -a units,lon,o,c,degrees_east -a units,lat,o,c,degrees_north -a standard_name,lon,o,c,longitude -a standard_name,lat,o,c,latitude '+filename
    print cmd
    os.system(cmd)

def mask_common_grid(filename):
    #cmd = 'cdo setctomiss,0 '+filename+' tmp.nc ; mv tmp.nc '+filename
    cmd = 'cdo setmissval,1e+20 -addc,1 '+filename+' tmp.nc ; mv tmp.nc '+filename
    print cmd
    os.system(cmd)

add_lonlat_variable_attributes(common_grid_filename, 'lsmmask')
mask_common_grid(common_grid_filename)

# %% cell 4
clog('critical')
pattern = '/data/ciles/IPCC/FGD/snow/final/NA_CORDEX/time_periods/NAM-22_${model}_${experiment}_snw100seas_${clim_period}_remo22grid.nc'
cproject('NAM-22_snw_chapter12','model','experiment','clim_period',('variable','snw'), ('period','fx'), ensemble=['model'], separator='%')
dataloc(project='NAM-22_snw_chapter12', url=pattern)

test = ds(project='NAM-22_snw_chapter12',
          model = '*',
          experiment='85',
          clim_period='2041_2060'
         )

lom = test.explore("choices")['model']

mid_ens_dict = dict()
for model in lom:
    test = ds(project='NAM-22_snw_chapter12',
              model = model,
              clim_period='2041_2060',
              experiment='85',
             ).explore('resolve')
    mid_ens_dict[model] = test
mid_myens = cens(mid_ens_dict)


baseline_ens_dict = dict()
for model in lom:
    test = ds(project='NAM-22_snw_chapter12',
              model = model,
              clim_period='1995_2014',
              experiment='85'
             ).explore('resolve')
    baseline_ens_dict[model] = test
baseline_myens = cens(baseline_ens_dict)


wbaseline_myens, wmid_myens = ensemble_intersection([baseline_myens, mid_myens])

ens_diff = fsub(wmid_myens, wbaseline_myens)
ensmedian = ccdo_ens(ens_diff, operator='enspctl,50')

outfilename = CWD+'/../../data/Figure_12.10/SWE_panel_b_RCP85_2041-2060_minus_1995-2014.nc'
cfile(regridn(ensmedian, cdogrid=common_grid_filename, option='remapbil'), target=outfilename)
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel b of figure 12.10 - Chapter 12" '+outfilename
os.system(cmd)

# %% cell 5
implot(regridn(ensmedian, cdogrid=common_grid_filename, option='remapbil'))

# %% cell 6
# -- Agreement
perc_agreement = '80'

# -- Mask of models with
ens_mask_pos = ccdo(regridn(ens_diff, cdogrid=common_grid_filename, option='remapbil'), operator='gtc,0')
ens_mask_neg = ccdo(regridn(ens_diff, cdogrid=common_grid_filename, option='remapbil'), operator='ltc,0')
ens_mask_zero = ccdo(regridn(ens_diff, cdogrid=common_grid_filename, option='remapbil'), operator='eqc,0')

perc_ens_pos = fmul( fdiv( ccdo_ens(ens_mask_pos, operator='enssum'), len(ens_diff) ), 100 )
perc_ens_neg = fmul( fdiv( ccdo_ens(ens_mask_neg, operator='enssum'), len(ens_diff) ), 100 )
perc_ens_zero = fmul( fdiv( ccdo_ens(ens_mask_zero, operator='enssum'), len(ens_diff) ), 100 )

# -- Signif90
signif90_pos = ccdo(perc_ens_pos, operator='gtc,'+perc_agreement)
signif90_neg = ccdo(perc_ens_neg, operator='gtc,'+perc_agreement)
signif90_zero = ccdo(perc_ens_zero, operator='gtc,'+perc_agreement)
signif90 = fadd(fadd(signif90_pos, signif90_neg), signif90_zero)

outfilename = CWD+'/../../data/Figure_12.10/mask_'+perc_agreement+'perc-agreement_SWE_panel_b_RCP85_2041-2060_minus_1995-2014.nc'
#regridn(ensmedian, cdogrid=common_grid_filename, option='remapbil')
cfile(regridn(signif90, cdogrid=common_grid_filename, option='remapnn'), target=outfilename)
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for the hatching of panel b of figure 12.10 - Chapter 12" '+outfilename
os.system(cmd)

# %% cell 7
implot(signif90)

# %% cell 8
!cat last.out
