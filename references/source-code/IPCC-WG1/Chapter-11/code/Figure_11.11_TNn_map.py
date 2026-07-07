# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/Figure_11.11_TNn_map.ipynb

# %% cell 2
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import regionmask

import conf
from utils import computation, plot, save_figuredata
import data_tables


mpl.rcParams["figure.dpi"] = 200

# %% cell 3
FIGURE_FOLDER = "Figure_11.11_TNn_map"

plot.create_figure_folders(FIGURE_FOLDER, conf.cmip6)

# %% cell 5
c6_tas = conf.cmip6.load_post_all_concat(varn="tas", postprocess="global_mean")

# %% cell 6
c6_tnn = conf.cmip6.load_post_all_concat(
    varn="tasmin",
    postprocess="tnn_regrid",
)

# %% cell 7
warming_levels = [1.5, 2.0, 4.0]

c6_at_warming_tnn = computation.at_warming_levels_list(
    c6_tas, c6_tnn, warming_levels=warming_levels
)

# %% cell 8
levels = np.arange(0, 8.1, 0.5)

# levels = None
cbar = plot.at_warming_level_one(
    c6_at_warming_tnn,
    "Change (°C)",
    "Annual minimum temperature (TNn)",
    levels=levels,
    average="median",
    colorbar=True,
    robust=True,
    cmap="Reds",
    extend="max",
    skipna=False,
    add_legend=True,
    hatch_simple=0.8,
    plotfunc="contourf",
)

f = plt.gcf()
axes = f.axes[:3]

axes[0].set_title("(d)", fontsize=9, pad=4, loc="left")
axes[1].set_title("(e)", fontsize=9, pad=4, loc="left")
axes[2].set_title("(f)", fontsize=9, pad=4, loc="left")

fN = conf.cmip6.figure_filename("TNn_at_w_simple_hatch", FIGURE_FOLDER)
plt.savefig(fN + ".pdf", dpi=300)
plt.savefig(fN + ".png", dpi=300, transparent=False, facecolor="w")


# data tables
fN = conf.cmip6.figure_filename("TNn_at_w_simple_hatch", FIGURE_FOLDER, "data_tables")

dta_ = c6_at_warming_tnn
data_tables.save_simulation_info_raw(fN + "_1.5_md_raw", dta_[0], panel="d")
data_tables.save_simulation_info_raw(fN + "_2.0_md_raw", dta_[1], panel="e")
data_tables.save_simulation_info_raw(fN + "_4.0_md_raw", dta_[2], panel="f")


# save figure data

varn = "TNn"
sfd = save_figuredata.SaveFiguredata(
    figure="Figure 11.11",
    units="°C",
    varn=varn,
)


panels = ["d", "e", "f"]
for i, warming_level in enumerate([1.5, 2.0, 4.0]):

    panel = panels[i]
    fN = conf.cmip6.figure_filename(
        f"Figure_11.11{panel}_cmip6_{varn}_change_at_{warming_level:0.1f}C.nc",
        FIGURE_FOLDER,
        "figure_data",
        add_prefix=False,
    )

    da = dta_[i]
    da.attrs["long_name"] = "Annual minimum temperature"
    da.attrs["comment"] = "anomaly wrt 1850-1900"

    ds = sfd.map_panel(
        da=da,
        average="median",
        panel=panel,
        warming_level=warming_level,
        hatch_simple=0.8,
    )
    ds.to_netcdf(fN)
