# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/Figure_11.15_Rx1day_intensity_Li_et_al.ipynb

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
Rx1day = li_etal_events.read_data("Rx1day")

# %% cell 7
li_etal_events.plot_boxstats(Rx1day, "Extremely high precipitation event", "%")

fN = conf.figure_filename(
    "Figure_11.15_Rx1day_intensity_Li_et_al",
    "Figure_11.15_Rx1day_intensity_Li_et_al",
)
plt.savefig(fN + ".png", facecolor="w", dpi=400)
plt.savefig(fN + ".pdf")
