# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/SYR_Figure_SPM.2a_TXx_map.ipynb

# %% cell 2
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import conf
from utils import computation, plot, save_figuredata

mpl.rcParams["figure.dpi"] = 200
mpl.rcParams['font.sans-serif'] = "Liberation Sans Narrow"
mpl.rcParams['font.sans-serif'] = "Arial"

# %% cell 3
FIGURE_FOLDER = "SYR_Figure_SPM.2a_TXx_map"

# %% cell 5
c6_tas = conf.cmip6.load_post_all_concat(varn="tas", postprocess="global_mean")

# %% cell 6
c6_txx_reg = conf.cmip6.load_post_all_concat(
    varn="tasmax", postprocess="txx_reg_ave_ar6", anomaly="no_anom"
)

# %% cell 7
c6_txx = conf.cmip6.load_post_all_concat(
    varn="tasmax",
    postprocess="txx_regrid",
)

# %% cell 8
warming_levels = [1.5, 2.0, 4.0]

c6_at_warming_txx = computation.at_warming_levels_list(
    c6_tas, c6_txx, warming_levels=warming_levels
)

# %% cell 9
warming_levels_4 = [1.5, 2.0, 3.0, 4.0]

c6_at_warming_txx_4 = computation.at_warming_levels_list(
    c6_tas, c6_txx, warming_levels=warming_levels_4
)

# %% cell 10
colors = [
    [0.776, 0.859, 0.937],
    [0.998, 0.917, 0.878],
    [0.996, 0.869, 0.811],
    [0.991, 0.791, 0.708],
    [0.988, 0.712, 0.607],
    [0.988, 0.626, 0.508],
    [0.987, 0.541, 0.416],
    [0.985, 0.458, 0.332],
    [0.972, 0.367, 0.259],
    [0.947, 0.268, 0.196],
    [0.890, 0.186, 0.153],
    [0.815, 0.112, 0.122],
    [0.736, 0.080, 0.101],
    [0.657, 0.061, 0.084],
    [0.534, 0.031, 0.068],
    [0.404, 0.000, 0.051],
]

# %% cell 11
levels = np.arange(0, 7.1, 0.5)
varn = "TXx"

# levels = None
cbar = plot.at_warming_level_one_4(
    c6_at_warming_txx_4,
    "Change (°C)",
    "Annual maximum temperature (TXx)",
    levels=levels,
    average="median",
    colorbar=True,
    robust=True,
    colors=colors,
    extend="both",
    skipna=False,
    add_legend=False,
    hatch_simple=None,
    plotfunc="contourf",
)


fN = conf.cmip6.figure_filename(
    f"SYR_Figure_SPM.2a_cmip6_{varn}", FIGURE_FOLDER, add_prefix=False
)

plt.savefig(fN + ".pdf", dpi=300)
plt.savefig(fN + ".svg", dpi=300)
plt.savefig(fN + ".eps", dpi=300)
plt.savefig(fN + ".png", dpi=300, transparent=False, facecolor="w")

# save figure data


sfd = save_figuredata.SaveFiguredata(
    figure="Figure SPM.2a", units="°C", varn=varn, chapter="SYR"
)


for i, warming_level in enumerate([1.5, 2.0, 3.0, 4.0]):

    fN = conf.cmip6.figure_filename(
        f"SYR_Figure_SPM.2a_cmip6_{varn}_change_at_{warming_level:0.1f}C.nc",
        FIGURE_FOLDER,
        "figure_data",
        add_prefix=False,
    )

    da = c6_at_warming_txx_4[i]
    da.attrs["long_name"] = "Annual maximum temperature"
    da.attrs["comment"] = "anomaly wrt 1850-1900"

    ds = sfd.map_panel(
        da=da,
        average="median",
        panel="a",
        warming_level=warming_level,
        hatch_simple=0.8,
    )
    ds.to_netcdf(fN)
