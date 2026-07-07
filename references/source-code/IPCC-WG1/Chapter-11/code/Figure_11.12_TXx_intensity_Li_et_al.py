# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/Figure_11.12_TXx_intensity_Li_et_al.ipynb

# %% cell 2
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import conf
from utils import li_etal_events

# %% cell 3
mpl.rcParams['font.sans-serif'] = "Arial"

# %% cell 5
TXx = li_etal_events.read_data("TXx")

# %% cell 7
li_etal_events.plot_boxstats(TXx, "Extremely high temperature event", "°C")

fN = conf.figure_filename(
    "Figure_11.12_TXx_intensity_Li_et_al",
    "Figure_11.12_TXx_intensity_Li_et_al",
)
plt.savefig(fN + ".png", facecolor="w", dpi=400)
plt.savefig(fN + ".pdf")
