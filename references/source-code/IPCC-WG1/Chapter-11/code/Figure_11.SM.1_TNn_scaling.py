# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/Figure_11.SM.1_TNn_scaling.ipynb

# %% cell 2
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import conf
from utils import computation, scaling_plot, save_figuredata, plot
import data_tables

mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['font.sans-serif'] = "Arial"

# %% cell 3
FIGURE_FOLDER = "Figure_11.SM.1_TNn_scaling"

plot.create_figure_folders(FIGURE_FOLDER, conf.cmip6)

# %% cell 5
c6_tas = conf.cmip6.load_post_all_concat(
    varn="tas",
    postprocess="global_mean"
)

# %% cell 6
c6_tnn_reg_no_anom = conf.cmip6.load_post_all_concat(
    varn="tasmin",
    postprocess="tnn_reg_ave_ar6",
    anomaly="no_anom"
)

# %% cell 7
c6_tnn_reg = computation.process_datalist(
    computation.calc_anomaly, c6_tnn_reg_no_anom, start=1850, end=1900, how="absolute"
)

# %% cell 9
warming_levels = np.arange(0.1, 5.1, 0.1)

c6_at_warming_tnn_ = computation.at_warming_levels_list(
    c6_tas, c6_tnn_reg, warming_levels=warming_levels
)

# %% cell 11
c6_at_warming_tnn = scaling_plot.concat_for_scaling(c6_at_warming_tnn_, warming_levels)

# %% cell 13
scaling_plot.plot_scaling(
    c6_at_warming_tnn,
    title="Scaling of regional annual minimum temperature (TNn)",
    conf_cmip=conf.cmip6,
    ylabel="TNn change (°C)",
)

fN = conf.cmip6.figure_filename(
    "Figure_11.A.1_TNn_scaling", FIGURE_FOLDER, add_prefix=False
)

plt.savefig(fN + ".pdf")
plt.savefig(fN + ".png", dpi=300, facecolor="w")

# data table
# use the non-concatenated data

fN = conf.cmip6.figure_filename(
    "Figure_11.A.1_TNn_scaling", FIGURE_FOLDER, "data_tables", add_prefix=False
)

data_tables.save_simulation_info_raw(fN + "_md_raw", c6_at_warming_tnn_[0], panel="a-l")

# %% cell 14
# save figure data

varn = "TNn"
sfd = save_figuredata.SaveFiguredata(
    figure="Figure 11.A.1",
    units="°C",
    varn=varn,
)


fN = conf.cmip6.figure_filename(
    f"Figure_11.A.1_cmip6_{varn}_scaling.nc",
    FIGURE_FOLDER,
    "figure_data",
    add_prefix=False,
)


c6_at_warming_tnn.attrs["long_name"] = "Annual minimum temperature"
c6_at_warming_tnn.attrs["comment"] = "anomaly wrt 1850-1900"


ds = sfd.scaling(
    da=c6_at_warming_tnn,
    panels="(a) to (l)",
)
ds.to_netcdf(fN)
