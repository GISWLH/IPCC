# Code-only export from IPCC-WG1 notebook.
# Source: Atlas/notebooks/reference-regions_Python.ipynb

# %% cell 3
import regionmask
regionmask.__version__

# %% cell 5
import xarray as xr
xr.set_options(display_style="text")
xr.__version__

# %% cell 7
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(edgeitems=2)

# %% cell 9
regionmask.defined_regions.ar6

# %% cell 11
ar6_all = regionmask.defined_regions.ar6.all
ar6_all

# %% cell 13
ax = ar6_all.plot()

# %% cell 15
f, ax = plt.subplots(subplot_kw=dict(projection=ccrs.Robinson()))

text_kws = dict(color="#67000d", fontsize=8, bbox=dict(pad=0.2, color="w"))

ax = ar6_all.plot(
    ax=ax,
    add_ocean=False,
    line_kws=dict(linewidth=1),
    coastlines=False,
    text_kws=text_kws,
)

ax.coastlines(color="0.5", lw=0.5);

# %% cell 17
new_zealand = ar6_all[[43]]
new_zealand

# %% cell 19
projection = ccrs.PlateCarree(central_longitude=180)

ax = new_zealand.plot(proj=projection, label="abbrev", add_ocean=True)

ax.set_extent([120, 185, -20, -60], ccrs.PlateCarree())

# %% cell 21
australasia = ar6_all[["NZ", "SEA", "NAU", "C.Australia", "SAU"]]

ax = australasia.plot(proj=projection, label="abbrev", add_ocean=True)

# %% cell 23
fN = ("auxiliary-material/CMIP6Amon_tas_CanESM5_r1i1p1f1_historical_gn_185001-201412.nc") 

ds = xr.open_dataset(fN)

tas = ds.tas

# calculate annual mean
tas = tas.groupby("time.year").mean("time")
tas = tas.rename(year="time")

# %% cell 24
# convert to celsius
tas = tas - 273.15

tas

# %% cell 26
proj = ccrs.Robinson()

f, ax = plt.subplots(subplot_kw=dict(projection=proj))

h = tas.isel(time=0).plot.pcolormesh(
    ax=ax, transform=ccrs.PlateCarree(), robust=True, center=0
)

ax.coastlines();

# %% cell 28
ar6_land = regionmask.defined_regions.ar6.land

# %% cell 30
mask_2D = ar6_land.mask(tas)

# %% cell 32
proj = ccrs.Robinson()
f, ax = plt.subplots(subplot_kw=dict(projection=proj))

h = mask_2D.plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(), add_colorbar=False)

ax.coastlines()

ar6_land.plot_regions(line_kws=dict(lw=0.5), add_label=False);

# %% cell 34
mask_3D = ar6_land.mask_3D(tas)
mask_3D

# %% cell 36
from matplotlib import colors as mplc

cmap1 = mplc.ListedColormap(["none", "#9ecae1"])

fg = mask_3D.isel(region=slice(2)).plot(
    subplot_kws=dict(projection=ccrs.PlateCarree()),
    col="region",
    col_wrap=2,
    transform=ccrs.PlateCarree(),
    add_colorbar=False,
    aspect=1.5,
    cmap=cmap1,
)

for ax in fg.axes.flatten():
    ax.coastlines(lw=0.5, color="0.5")

fg.fig.subplots_adjust(hspace=0, wspace=0.1);

# %% cell 38
# 1) by the index of the region:
r1 = mask_3D.sel(region=2)

# 2) with the abbreviation
r2 = mask_3D.isel(region=(mask_3D.abbrevs == "CNA"))

# 3) with the long name:
r3 = mask_3D.isel(region=(mask_3D.names == "C.North-America"))

# %% cell 40
tas_CNA = tas.where(r1)

proj = ccrs.Robinson()

ax = plt.subplot(111, projection=proj)

tas_CNA.isel(time=0).plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree())

ax.set_title("Central North America")

ax.coastlines();

# %% cell 42
weights = np.cos(np.deg2rad(tas.lat))

tas_regional = tas.weighted(mask_3D * weights).mean(dim=("lat", "lon"))

# %% cell 44
tas_regional

# %% cell 46
tas_regional.isel(region=slice(6)).plot(col="region", col_wrap=3, sharey=False);

# %% cell 48
land_110 = regionmask.defined_regions.natural_earth.land_110

land_mask = land_110.mask_3D(tas)

# add a plot
ax = plt.axes(projection=ccrs.Robinson())
land_mask.plot(ax=ax, transform=ccrs.PlateCarree(), add_colorbar=False);

# %% cell 50
mask_lsm = mask_3D * land_mask.squeeze(drop=True)

# %% cell 52
ar6_land.plot(add_label=False, line_kws=dict(lw=1), proj=ccrs.Robinson())

regionmask.plot_3D_mask(mask_lsm, transform=ccrs.PlateCarree(), add_colorbar=False);

# %% cell 54
tas_regional_land = tas.weighted(mask_lsm * weights).mean(dim=("lat", "lon"))

# %% cell 56
f, axes = plt.subplots(2, 3, sharex=True, figsize=(9, 6))
axes = axes.flatten()

for i, ax in enumerate(axes):

    ds = tas_regional.isel(region=i)
    ds.plot(ax=ax, label="Land + Ocean")

    ds = tas_regional_land.isel(region=i)
    ds.plot(ax=ax, label="Land only")

    ax.set_title(ds.names.values)
    if i < 3:
        ax.set_xlabel("")

axes[2].legend()
plt.tight_layout()

# %% cell 59
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
