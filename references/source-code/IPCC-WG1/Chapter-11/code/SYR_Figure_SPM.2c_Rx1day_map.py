# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/SYR_Figure_SPM.2c_Rx1day_map.ipynb

# %% cell 2
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import conf
from utils import computation, plot, save_figuredata, syr_colors

mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['font.sans-serif'] = "Liberation Sans Narrow"
mpl.rcParams['font.sans-serif'] = "Arial"

# %% cell 3
FIGURE_FOLDER = "SYR_Figure_SPM.2c_Rx1day_map"

plot.create_figure_folders(FIGURE_FOLDER, conf.cmip6)

# %% cell 5
c6_tas = conf.cmip6.load_post_all_concat(
    varn="tas",
    postprocess="global_mean"
)

# %% cell 6
c6_rx1day = conf.cmip6.load_post_all_concat(
    varn="pr", postprocess="rx1day_regrid", anomaly="no_anom"
)

# %% cell 7
c6_rx1day_rel = computation.process_datalist(
    computation.calc_anomaly, c6_rx1day, start=1850, end=1900, how="relative"
)

# %% cell 8
warming_levels_4 = [1.5, 2.0, 3.0, 4.0]

c6_at_warming_rx1day_rel_4 = computation.at_warming_levels_list(
    c6_tas, c6_rx1day_rel, warming_levels=warming_levels_4
)

# %% cell 10
levels = np.arange(-40, 41, 10)
varn = "Rx1day"

# levels = None
cbar = plot.at_warming_level_one_4(
    c6_at_warming_rx1day_rel_4,
    "Change (%)",
    "Annual maximum daily precipitation change (Rx1day)",
    levels=levels,
    average="median",
    colorbar=True,
    robust=True,
    cmap=syr_colors.cmap,
    skipna=False,
    add_legend=False,
    hatch_simple=None,
    plotfunc="contourf",
    #     mask_ocean=True,
)

fN = conf.cmip6.figure_filename(
    f"SYR_Figure_SPM.2c_cmip6_{varn}", FIGURE_FOLDER, add_prefix=False
)
plt.savefig(fN + ".pdf", dpi=300)
plt.savefig(fN + ".svg", dpi=300)
plt.savefig(fN + ".eps", dpi=300)
plt.savefig(fN + ".png", dpi=300, transparent=False, facecolor="w")

# ================================

# save figure data

sfd = save_figuredata.SaveFiguredata(
    figure="SYR_Figure_SPM.2c",
    units="%",
    varn=varn,
)

for i, warming_level in enumerate([1.5, 2.0, 3.0, 4.0]):

    fN = conf.cmip6.figure_filename(
        f"SYR_Figure_SPM.2c_cmip6_{varn}_change_at_{warming_level:0.1f}C.nc",
        FIGURE_FOLDER,
        "figure_data",
        add_prefix=False,
    )

    da = c6_at_warming_rx1day_rel_4[i]
    da.attrs["long_name"] = "Annual maximum 1-day precipitation"
    da.attrs["comment"] = "anomaly wrt 1850-1900"

    ds = sfd.map_panel(
        da=da,
        average="median",
        panel="c",
        warming_level=warming_level,
    )
    ds.to_netcdf(fN)
