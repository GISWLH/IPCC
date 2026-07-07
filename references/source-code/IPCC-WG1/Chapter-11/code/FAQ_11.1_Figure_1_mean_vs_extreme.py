# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/FAQ_11.1_Figure_1_mean_vs_extreme.ipynb

# %% cell 2
import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplotutils as mpu
import numpy as np

import conf
import data_tables
from utils import computation, plot, transform, save_figuredata

# %% cell 3
mpl.rcParams["font.sans-serif"] = "Arial"
mpl.rc("font", size=9)

# %% cell 4
FIGURE_FOLDER = "FAQ_11.1_Figure_1"

plot.create_figure_folders(FIGURE_FOLDER, conf.cmip6)

# %% cell 6
c6_tas = conf.cmip6.load_post_all_concat(varn="tas", postprocess="global_mean")

# %% cell 7
c6_txx = conf.cmip6.load_post_all_concat(varn="tasmax", postprocess="txx_regrid")

# %% cell 8
c6_rx1day_abs = conf.cmip6.load_post_all_concat(
    varn="pr", postprocess="rx1day_regrid", anomaly="no_anom"
)

# %% cell 9
c6_tas_monthly = conf.cmip6.load_post_all_concat(
    varn="tas",
    postprocess="monthly_regrid",
    exp=None,
    anomaly="no_anom",
    year_mean=False,
)

# %% cell 10
c6_pr_monthly = conf.cmip6.load_post_all_concat(
    varn="pr",
    postprocess="monthly_regrid",
    exp=None,
    anomaly="no_anom",
    year_mean=False,
)

# %% cell 12
c6_rx1day = computation.process_datalist(
    computation.calc_anomaly, c6_rx1day_abs, start=1850, end=1900, how="absolute"
)

c6_rx1day_rel = computation.process_datalist(
    computation.calc_anomaly, c6_rx1day_abs, start=1850, end=1900, how="relative"
)

# %% cell 14
trans = transform.ConsecutiveMonthsClim("tas", how="max", clim=slice("1850", "1900"))

summer_months = computation.process_datalist(trans, c6_tas_monthly)

# %% cell 16
d = summer_months[9][0]

f, ax = plot.map_subplots()

h = plot.one_map_flat(
    d.central_month, ax, levels=np.arange(0.5, 12.6, 1), cmap="Paired"
)

cbar = mpu.colorbar(h, ax, orientation="horizontal", extend="neither")
cbar.set_ticks(range(1, 13))

mpu.set_map_layout(ax)

# %% cell 17
ds = c6_tas_monthly[0][0]

ds_s = summer_months[0][0]

# %% cell 18
g = ds.tas.groupby("time.month")

d = g.where(ds_s.month_mask)

# %% cell 19
def calc_summer_months_mean(ds, meta, summer_months_list):
    """calculate the mean over summer means
    
    Parameters
    ----------
    ds : xr.Dataset
        Dataset to calculate the summer months for.
    meta : metadata
        Metadata belonging to ds.
    summer_month_list : datalist
        Datalist with the summer months data, to be selected
        for ds (via meta).    
    """

    select_by = ("model", "exp", "ens")
    attributes = {key: meta[key] for key in select_by}

    # try to find the index
    summer_months = computation.select_by_metadata(summer_months_list, **attributes)

    # make sure only one dataset is found in index_list
    if len(summer_months) > 1:
        raise ValueError("Found more than one dataset:\n", meta)
    elif len(summer_months) == 0:
        print("skipped")
        return []

    # unpack list
    summer_months = summer_months[0]
    # unpack ds, meta
    summer_months = summer_months[0]

    # set non-summer months to <NA>
    ds = ds.groupby("time.month").where(summer_months.month_mask)

    # do a rolling mean so we don't combine JF......D from one year
    # but calculate DJF over 2 years, assigning it to the year of J
    # then do a annual mean
    return ds.rolling(time=3, center=True).mean().groupby("time.year").mean("time")

# %% cell 20
c6_tas_summer = computation.process_datalist(
    calc_summer_months_mean,
    c6_tas_monthly,
    pass_meta=True,
    summer_months_list=summer_months,
)

# %% cell 21
c6_pr_summer = computation.process_datalist(
    calc_summer_months_mean,
    c6_pr_monthly,
    pass_meta=True,
    summer_months_list=summer_months,
)

# %% cell 23
c6_tas_summer_abs = computation.process_datalist(
    computation.calc_anomaly, c6_tas_summer, start=1850, end=1900, how="absolute"
)


c6_pr_summer_rel = computation.process_datalist(
    computation.calc_anomaly, c6_pr_summer, start=1850, end=1900, how="relative"
)

# %% cell 25
warming_levels = [1.5, 2.0, 4.0]

c6_txx_at_warming = computation.at_warming_levels_list(c6_tas, c6_txx, warming_levels)

# c6_rx1day_at_warming = computation.at_warming_levels_list(
#     c6_tas, c6_rx1day, warming_levels, factor=3600*24
# )

c6_rx1day_rel_at_warming = computation.at_warming_levels_list(
    c6_tas, c6_rx1day_rel, warming_levels
)

# %% cell 26
c6_tas_summer_at_warming = computation.at_warming_levels_list(
    c6_tas, c6_tas_summer_abs, warming_levels
)


c6_pr_summer_rel_at_warming = computation.at_warming_levels_list(
    c6_tas, c6_pr_summer_rel, warming_levels
)

# %% cell 29
f, axes = plt.subplots(2, 2, subplot_kw=dict(projection=ccrs.Robinson()))
axes = axes.flatten()

cbar_kwargs = dict(orientation="horizontal", pad=0.05, shrink=0.5)


opt = dict(extend="max", add_n_models=False, plotfunc="contourf")


# ====

ax = axes[0]

levels = np.arange(0, 8.1, 1)

da = c6_tas_summer_at_warming[2]
h, _ = plot.one_map(da, ax, "median", levels=levels, cmap="Reds", **opt)
ax.set_title("Climate average", fontsize=11)

# ====

ax = axes[1]

da = c6_txx_at_warming[2]
h, _ = plot.one_map(da, ax, "median", levels=levels, cmap="Reds", **opt)

ax.set_title("Climate extreme", fontsize=11)

cbar = mpu.colorbar(h, axes[0], axes[1], **cbar_kwargs)
cbar.set_label("°C")

# ====
opt["extend"] = "both"

# ====


ax = axes[2]

levels = np.arange(-40, 41, 10)

da = c6_pr_summer_rel_at_warming[2]
h, _ = plot.one_map(da, ax, "median", levels=levels, cmap="BrBG", **opt)

# ====


ax = axes[3]

da = c6_rx1day_rel_at_warming[2]
h, _ = plot.one_map(da, ax, "median", levels=levels, cmap="BrBG", **opt)

cbar = mpu.colorbar(h, axes[2], axes[3], **cbar_kwargs)
cbar.set_label("%")

# ====

plt.subplots_adjust(
    wspace=0.075, hspace=0.6, left=0.05, right=1 - 0.025, bottom=0.15, top=0.9
)

mpu.set_map_layout(axes)

f.canvas.draw()

fN = conf.cmip6.figure_filename(
    "FAQ_11.1_Figure_1_mean_vs_extreme", "FAQ_11.1_Figure_1", add_prefix=False
)
plt.savefig(fN + ".png", dpi=300, facecolor="w")
plt.savefig(fN + ".pdf", dpi=400)


# data tables
fN = conf.cmip6.figure_filename(
    "FAQ_11.1_Figure_1_mean_vs_extreme", "FAQ_11.1_Figure_1", "data_tables", add_prefix=False
)

data_tables.save_simulation_info_raw(
    fN + "_a_md_raw", c6_tas_summer_at_warming[2], panel="a"
)
data_tables.save_simulation_info_raw(fN + "_b_md_raw", c6_txx_at_warming[2], panel="b")
data_tables.save_simulation_info_raw(
    fN + "_c_md_raw", c6_pr_summer_rel_at_warming[2], panel="c"
)
data_tables.save_simulation_info_raw(
    fN + "_d_md_raw", c6_rx1day_rel_at_warming[2], panel="d"
)


# save figure data
# ================

warming_level = 4.0
figure = "FAQ 11.1 Figure 1"

data = [
    c6_tas_summer_at_warming[2],
    c6_txx_at_warming[2],
    c6_pr_summer_rel_at_warming[2],
    c6_rx1day_rel_at_warming[2],
]

varns = ["summer_temperature", "TXx", "summer_prec", "Rx1day"]
panels = ["a", "b", "c", "d"]
units = ["°C", "°C", "%", "%"]
long_name = [
    "Near-Surface Air Temperature",
    "Annual maximum temperature",
    "Precipitation",
    "Annual maximum 1-day precipitation",
]


for i in range(4):

    dta_ = data[i]
    varn = varns[i]
    panel = panels[i]
    unit = units[i]

    dta_.attrs["long_name"] = long_name[i]
    dta_.attrs["comment"] = "anomaly wrt 1850-1900"

    sfd = save_figuredata.SaveFiguredata(
        figure=figure,
        units=unit,
        varn=varn,
    )

    ds = sfd.map_panel(
        da=dta_,
        average="median",
        panel=panel,
        warming_level=warming_level,
        hatch_simple=None,
    )

    fN = conf.cmip6.figure_filename(
        f"{figure.replace(' ', '_')}{panel}_cmip6_{varn}_change_at_{warming_level:0.1f}C.nc",
        FIGURE_FOLDER,
        "figure_data",
        add_prefix=False,
    )
    ds.to_netcdf(fN)
