# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/Figure_11.3_TXx_scaling.ipynb

# %% cell 2
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import conf
from utils import computation, plot, scaling_plot, save_figuredata
import data_tables

mpl.rcParams["figure.dpi"] = 200
mpl.rcParams["font.sans-serif"] = "Arial"

# %% cell 3
FIGURE_FOLDER = "Figure_11.3_TXx_scaling"

plot.create_figure_folders(FIGURE_FOLDER, conf.cmip6)

# %% cell 5
c6_tas = conf.cmip6.load_post_all_concat(
    varn="tas",
    postprocess="global_mean"
)

# %% cell 6
c6_txx_reg_no_anom = conf.cmip6.load_post_all_concat(
    varn="tasmax",
    postprocess="txx_reg_ave_ar6",
    anomaly="no_anom"
)

# %% cell 7
c6_txx_reg = computation.process_datalist(
    computation.calc_anomaly, c6_txx_reg_no_anom, start=1850, end=1900, how="absolute"
)

# %% cell 9
warming_levels = np.arange(0.1, 5.1, 0.1)

c6_at_warming_txx_ = computation.at_warming_levels_list(
    c6_tas, c6_txx_reg, warming_levels=warming_levels
)

# %% cell 11
c6_at_warming_txx = scaling_plot.concat_for_scaling(c6_at_warming_txx_, warming_levels)

# %% cell 13
colors = sns.color_palette("Paired", 12)

# %% cell 14
scaling_plot.plot_region_groups()

fN = conf.cmip6.figure_filename("scaling_region_groups", "Figure_11.3_TXx_scaling")

plt.savefig(fN + ".pdf")
plt.savefig(fN + ".png", dpi=300, facecolor="w")

# %% cell 16
colors = sns.color_palette("colorblind", 5)


scaling_plot.plot_scaling(
    c6_at_warming_txx,
    title="Scaling of regional annual maximum temperature (TXx)",
    conf_cmip=conf.cmip6,
    ylabel="TXx change (°C)",
)


fN = conf.cmip6.figure_filename(
    "Figure_11.3_TXx_scaling", FIGURE_FOLDER, add_prefix=False
)

plt.savefig(fN + ".pdf")
plt.savefig(fN + ".png", dpi=300, facecolor="w")


# data tables
fN = conf.cmip6.figure_filename(
    "Figure_11.3_TXx_scaling", FIGURE_FOLDER, "data_tables", add_prefix=False
)

# use the non-concatenated data
data_tables.save_simulation_info_raw(fN + "_md_raw", c6_at_warming_txx_[0], panel="a-l")

# %% cell 17
# save figure data
varn = "TXx"
sfd = save_figuredata.SaveFiguredata(
    figure="Figure 11.3",
    units="°C",
    varn=varn,
)

fN = conf.cmip6.figure_filename(
    f"Figure_11.3_cmip6_{varn}_scaling.nc",
    FIGURE_FOLDER,
    "figure_data",
    add_prefix=False,
)

c6_at_warming_txx.attrs["long_name"] = "Annual maximum temperature"
c6_at_warming_txx.attrs["comment"] = "anomaly wrt 1850-1900"

ds = sfd.scaling(
    da=c6_at_warming_txx,
    panels="(a) to (l)",
)
ds.to_netcdf(fN)
