# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/EUROPE_regional_figure/snow_map_Europe.ipynb

# %% cell 2
import os, glob
import xarray as xr
from IPython.display import Image
from PIL import Image as PILImage

# %% cell 3
CWD = os.getcwd()

# %% cell 6
from climaf.api import *

# %% cell 8
pattern ='/projsu/cmip-work/rvautard/IPCC/SWE${experiment}/snw100seas.${model}.${clim_period}.meanG.nc'
cproject('SWE_cordex_ch12','experiment',('period','fx'),'clim_period','model', ('variable','snw'), ensemble=['model'], separator='%')
dataloc(project='SWE_cordex_ch12', url=pattern)

# %% cell 10
import regionmask
import numpy as np
common_grid_filename = CWD+'/../../data/Figure_12.9/EUROPE_raw_common_grid.nc'

lats = np.arange(25, 75, 0.1)
lons = np.arange(-15, 65, 0.1)
mask = regionmask.defined_regions.natural_earth.land_110.mask(lons, lats)
mask.to_netcdf(common_grid_filename)


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

# %% cell 11
# -- Create ensemble for historical baseline
req_baseline = ds(project='SWE_cordex_ch12',
                  experiment = 'RCP85',
                  clim_period = 'ref',
                  model = '*',
                 )
ens_baseline = req_baseline.explore('ensemble')

# %% cell 12
ens_baseline

# %% cell 13
# -- Create ensemble object for the scenario
req_exp = ds(project='SWE_cordex_ch12',
             experiment = 'RCP85',
             clim_period = 'mce',
             model = '*',
            )
ens_exp = req_exp.explore('ensemble')

# -- Extract common members
wens_baseline, wens_exp = ensemble_intersection([ens_baseline, ens_exp])

# -- Climatologies
clim_baseline = clim_average(wens_baseline, 'ANM')
clim_exp      = clim_average(wens_exp, 'ANM')

# -- Difference
diff = fsub(clim_exp, clim_baseline)

# -- Ensemble median
ensmedian = ccdo_ens(diff, operator='enspctl,50')

outdatadir = CWD+'/../../data/Figure_12.9/'

# -- Mask of models with
ens_mask_pos = ccdo(diff, operator='gtc,0')
ens_mask_neg = ccdo(diff, operator='ltc,0')
ens_mask_zero = ccdo(diff, operator='eqc,0')

perc_ens_pos = fmul( fdiv( ccdo_ens(ens_mask_pos, operator='enssum'), len(diff) ), 100 )
perc_ens_neg = fmul( fdiv( ccdo_ens(ens_mask_neg, operator='enssum'), len(diff) ), 100 )
perc_ens_zero = fmul( fdiv( ccdo_ens(ens_mask_zero, operator='enssum'), len(diff) ), 100 )

# -- Signif90
perc_agreement = '80'
signif90_pos = ccdo(perc_ens_pos, operator='gtc,'+perc_agreement)
signif90_neg = ccdo(perc_ens_neg, operator='gtc,'+perc_agreement)
signif90_zero = ccdo(perc_ens_zero, operator='gtc,'+perc_agreement)
signif90 = fadd( fadd(signif90_pos, signif90_neg), signif90_zero)

mask_agreement_name = outdatadir + 'mask_'+perc_agreement+'perc-agreement_SWE_panel_b_RCP85_mce_minus_baseline.nc'
cfile(regridn(signif90, cdogrid=common_grid_filename), target=mask_agreement_name)
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for the hatching of panel_b of figure 12.9 - Chapter 12" '+mask_agreement_name
os.system(cmd)

ensmedian_filename = outdatadir + 'SWE_panel_b_RCP85_mce_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel_b of figure 12.9 - Chapter 12" '+ensmedian_filename
cfile(regridn(ensmedian, cdogrid=common_grid_filename), target=ensmedian_filename)
os.system(cmd)

# %% cell 14
implot(regridn(signif90, cdogrid=common_grid_filename))
