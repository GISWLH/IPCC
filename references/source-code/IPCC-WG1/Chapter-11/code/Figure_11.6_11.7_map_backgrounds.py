# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/Figure_11.6_11.7_map_backgrounds.ipynb

# %% cell 2
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import mplotutils as mpu
import regionmask

import conf

# %% cell 3
FIGURE_FODER = "Figure_11.6_11.7_map_backgrounds"

# %% cell 5
light_blue = "#f2f8fa"
dark_blue = "#bde0ef"

dark_red = "#ffd7a0"
light_red = "#fff3df"

# %% cell 6
def plot_map_colored(color_light, color_dark):

    f, ax = plt.subplots(1, 1, subplot_kw=dict(projection=ccrs.Robinson()))

    regionmask.defined_regions.ar6.land.plot(
        ax=ax,
        add_label=False,
        add_land=True,
        land_kws=dict(color=color_dark, zorder=0.9),
        add_ocean=True,
        ocean_kws=dict(color=color_light, zorder=0.9),
        line_kws=dict(lw=1),
    )

    ax.set_global()
    mpu.set_map_layout(ax)

    side = 0.0125
    plt.subplots_adjust(wspace=0.075, left=side, right=1 - side, bottom=0.05, top=0.95)

# %% cell 7
plot_map_colored(light_red, dark_red)

fN = conf.cmip6.figure_filename("Figure_11.7_ar6_regions_red", FIGURE_FODER)
plt.savefig(fN + ".pdf", dpi=300)
plt.savefig(fN + ".png", dpi=300)

# %% cell 8
plot_map_colored(light_blue, dark_blue)
fN = conf.cmip6.figure_filename("Figure_11.7_ar6_regions_blue", FIGURE_FODER)
plt.savefig(fN + ".pdf", dpi=300)
plt.savefig(fN + ".png", dpi=300)
