# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/NORTH-AMERICA_regional_figure/Figure_12.10_multipanel_NORTH-AMERICA.ipynb

# %% cell 3
import os
from IPython.display import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# %% cell 5
region = 'NORTH-AMERICA'
outdir = os.getcwd()+'/../../figs/Figure_12.10/'
outfilename = outdir +region+'_regional_figure_12.10.png'

# %% cell 7
# -- Q100 Boxplot
Q100_boxplot_fig = mpimg.imread(outdir + 'panel_c_'+region+'_Q100_boxplot.png')

# -- SWE map
SWE_map_fig = mpimg.imread(outdir + 'panel_b_SWE_map_RCP85_2050.png')
# -- SWE boxplot
SWE_boxplot_fig = mpimg.imread(outdir + 'panel_d_'+region+'_SWE_mask14_boxplot.png')

# %% cell 9
# -- Open figure device
plt.figure(1, figsize=[32,23],dpi=200).patch.set_facecolor('white')
fontsizeunit=18

# -- Split the device in multipanels
mapheight = 1  # Relative height of maps
boxplotheight = 1.6
grid = plt.GridSpec(2, 3, hspace=0, wspace=0.1, height_ratios=[mapheight,boxplotheight])#, wspace=0.1

# -- Q100
# -----------------------------------------------------
# -- Boxplot
plt.subplot(grid[1,0]).axis('off')
plt.imshow(Q100_boxplot_fig)
#plt.text(-50, 50, '(c)', fontsize=25)
plt.text(-30, 100, r"1:100yr river discharge per unit catchment area (Q100, $m^3s^{-1}km^{-2}$)", rotation=90, fontsize=fontsizeunit)
plt.text(885, 250, r"Change in Q100 r.t. recent past ($m^3s^{-1}km^{-2}$)", rotation=-90, fontsize=fontsizeunit)


# -- SWE
# -----------------------------------------------------
# -- Map
plt.subplot(grid[0,1]).axis('off')
plt.imshow(SWE_map_fig)
#plt.text(550, 580, r"$days.yr^{-1}$", fontsize=16)
#plt.text(-40, 40, '(b)', fontsize=25)

# -- Boxplot
plt.subplot(grid[1,1]).axis('off')
plt.imshow(SWE_boxplot_fig)
#plt.text(-60, 40, '(d)', fontsize=25)
plt.text(-30, 190, r"Days with SWE>100mm ($days.yr^{-1}$)", rotation=90, fontsize=fontsizeunit)



plt.savefig(outfilename, transparent=True, bbox_inches='tight', pad_inches=0)
