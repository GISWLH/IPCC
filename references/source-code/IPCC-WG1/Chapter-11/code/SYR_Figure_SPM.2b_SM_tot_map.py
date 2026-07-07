# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/SYR_Figure_SPM.2b_SM_tot_map.ipynb

# %% cell 2
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import conf
from utils import computation, plot, save_figuredata, syr_colors

mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['font.sans-serif'] = "Liberation Sans Narrow"
mpl.rcParams['font.sans-serif'] = "Arial"

# %% cell 3
warnings.filterwarnings("ignore", message="invalid value encountered in reduce")

# %% cell 4
FIGURE_FOLDER = "SYR_Figure_SPM.2b_SM_tot_map"

plot.create_figure_folders(FIGURE_FOLDER, conf.cmip6)

# %% cell 6
c6_tas = conf.cmip6.load_post_all_concat(
    varn="tas",
    postprocess="global_mean"
)

# %% cell 8
c6_mrso = conf.cmip6.load_post_all_concat(
    varn="mrso",
    postprocess="sm_annmean_regrid",
    anomaly="no_anom"
)

# %% cell 10
warming_levels_4 = [1.5, 2.0, 3.0, 4.0]

c6_mrso_norm = computation.process_datalist(
    computation.calc_anomaly, c6_mrso, start=1850, end=1900, how="norm"
)

c6_at_warming_mrso_norm_4 = computation.at_warming_levels_list(
    c6_tas, c6_mrso_norm, warming_levels=warming_levels_4
)

# %% cell 12
def plot_levels(levels, data, unit="Change (σ)", hatch_simple=None, cmap="BrBG"):

    if len(data) == 3:
        func = plot.at_warming_level_one
    elif len(data) == 4:
        func = plot.at_warming_level_one_4
    else:
        raise ValueError()

    return func(
        data,
        unit,
        "Soil moisture (total column)",
        levels=levels,
        average="median",
        mask_ocean=True,
        colorbar=True,
        robust=True,
        cmap=cmap,
        skipna=True,
        plotfunc="contourf",
        add_coastlines=False,
        coastline_kws=dict(lw=0.1, color="k"),
        ocean_kws=dict(facecolor="w", edgecolor="k", zorder=1.1, lw=0.1),
        colorbar_kwargs=dict(extendfrac="auto"),
        hatch_simple=hatch_simple,
    )

# %% cell 13
levels = np.arange(-1.5, 1.6, 0.25)
cbar = plot_levels(levels, c6_at_warming_mrso_norm_4, cmap=syr_colors.cmap)
cbar.set_ticks(levels[::2])

f = plt.gcf()
axes = f.axes[:4]

axes[0].set_title("", fontsize=9, pad=4, loc="left")
axes[1].set_title("", fontsize=9, pad=4, loc="left")
axes[2].set_title("", fontsize=9, pad=4, loc="left")
axes[3].set_title("", fontsize=9, pad=4, loc="left")

fN = conf.cmip6.figure_filename(
    "SYR_Figure_SPM.2b_cmip6_SM_tot", FIGURE_FOLDER, add_prefix=False
)
plt.savefig(fN + ".pdf", dpi=300)
plt.savefig(fN + ".svg", dpi=300)
plt.savefig(fN + ".eps", dpi=300)
plt.savefig(fN + ".png", dpi=300, transparent=False, facecolor="w")

# ============================================

# # save figure data

sfd = save_figuredata.SaveFiguredata(
    chapter="SYR",
    figure="SPM.2b",
    units="std",
    varn=None,
)

for i, warming_level in enumerate([1.5, 2.0, 3.0, 4.0]):

    fN = conf.cmip6.figure_filename(
        f"SYR_Figure_SPM.2b_cmip6_SM_tot_change_at_{warming_level:0.1f}C.nc",
        FIGURE_FOLDER,
        "figure_data",
        add_prefix=False,
    )

    da = c6_at_warming_mrso_norm_4[i]
    da.attrs["long_name"] = "Total Soil Moisture Content"
    da.attrs["comment"] = "anomaly wrt 1850-1900"

    ds = sfd.map_panel(
        da=da,
        average="median",
        panel="b",
        warming_level=warming_level,
    )
    ds.to_netcdf(fN)
