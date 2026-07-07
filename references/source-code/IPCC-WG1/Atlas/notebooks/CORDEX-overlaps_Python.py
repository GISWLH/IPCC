# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/CORDEX-overlaps_Python.ipynb

# %% cell 4
import regionmask
import xarray as xr
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# %% cell 6
ar6_all = regionmask.defined_regions.ar6.all
ar6_all

# %% cell 7
ar6_all.plot()

# %% cell 10
ds = xr.open_dataset("../reference-grids/land_sea_mask_05degree.nc4")
XX_WORLD, YY_WORLD = np.meshgrid(ds.lon, ds.lat)
mask_2d_WORLD = ar6_all.mask(ds.lon, ds.lat)
weights_WORLD = np.cos(np.deg2rad(YY_WORLD))
ds.close()

# %% cell 12
regular_CORDEX_grids = pd.read_csv('auxiliary-material/regular-CORDEX-grids.csv', index_col = 1)

# %% cell 13
regular_CORDEX_grids

# %% cell 15
CORDEX_doms = ['NAM-44i','CAM-44i','SAM-44i','ARC-44i','AFR-44i','EUR-44i','MED-44i',
                  'MNA-44i','SEA-22i','EAS-44i','WAS-44i','CAS-44i','ANT-44i','AUS-44i']

# %% cell 18
Overlaps_CORDEX_ReferenceRegions = pd.DataFrame(index = CORDEX_doms, columns = np.arange(len(ar6_all)))

# %% cell 20
for dom in CORDEX_doms:
    lon = np.arange(regular_CORDEX_grids.loc[dom]['West'], regular_CORDEX_grids.loc[dom]['East']+0.5, 0.5)
    lat = np.arange(regular_CORDEX_grids.loc[dom]['South'], regular_CORDEX_grids.loc[dom]['North']+0.5, 0.5)
    XX, YY = np.meshgrid(lon, lat)
    mask_2d_domain = ar6_all.mask(lon, lat)
    weights_domain = np.cos(np.deg2rad(YY))
    for reg in np.unique(mask_2d_domain.values):
        if not np.isnan(reg):
            pos = np.where(mask_2d_domain.values == reg)
            pos_w = np.where(mask_2d_WORLD.values == reg)
            Overlaps_CORDEX_ReferenceRegions[reg].loc[dom] = np.round(100*np.sum(np.ones_like(pos[0])*weights_domain[pos])/np.sum(np.ones_like(pos_w[0])*weights_WORLD[pos_w]), 2)

# %% cell 22
Overlaps_CORDEX_ReferenceRegions.columns = [ar6_all.regions[n].abbrev for n in Overlaps_CORDEX_ReferenceRegions.columns]
Overlaps_CORDEX_ReferenceRegions = Overlaps_CORDEX_ReferenceRegions.fillna(0).transpose()

# %% cell 24
Overlaps_CORDEX_ReferenceRegions

# %% cell 27
threshold = 80

# %% cell 28
for dom in CORDEX_doms:
    AR6_dom = Overlaps_CORDEX_ReferenceRegions.query(f'`{dom}`>80').index    
    print(dom + ": " + str(AR6_dom.tolist()))

# %% cell 30
!conda list
