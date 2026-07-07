# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/Box_11.4_Figure_1_Sippel_2015.ipynb

# %% cell 2
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import conf

# %% cell 3
mpl.rcParams["font.sans-serif"] = "Arial"

# %% cell 4
fN = "../data/sippel_2015/sippel_2015_fig3.txt"
df = pd.read_csv(fN, sep=",", index_col=0)

# %% cell 5
f, ax = plt.subplots(constrained_layout=True)

f.set_size_inches(9 / 2.54, 6 / 2.54)

df["ts.corrected.2sigma"].plot(ax=ax, label="T > + 2 sigma")
df["ts.corrected.3sigma"].plot(ax=ax, label="T > + 3 sigma")


ax.set_ylabel("Land area (%)", size=9)
ax.set_xlabel("Years", size=9)

ax.set_title("Land area affected by temperature extremes", size=9)

ax.tick_params(axis="both", which="major", labelsize=9)

ax.set_xticks(np.arange(1950, 2011, 10))

ax.legend(fontsize=9)

msg = "JJA, 30°N – 80°N"
ax.text(
    1.02,
    0.005,
    msg,
    ha="left",
    va="bottom",
    rotation="vertical",
    transform=ax.transAxes,
    size=9,
)

fN = conf.figure_filename(
    "Box_11.4_Figure_1_Sippel_2015", "Box_11.4_Figure_1_Sippel_2015"
)
plt.savefig(fN + ".png", facecolor="w", dpi=400)
plt.savefig(fN + ".pdf")
