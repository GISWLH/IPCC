# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/AFRICA_regional_figure/.ipynb_checkpoints/Figure_12.5_multipanel_AFRICA-checkpoint.ipynb

# %% cell 3
import os
from IPython.display import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# %% cell 5
outdir = os.getcwd()+'/../../figs/Figure_12.5/'
outfilename = outdir + 'AFRICA_regional_figure_12.5.png'

# %% cell 7
region='AFRICA'
# -- Q100 Boxplot
Q100_boxplot_fig = mpimg.imread(outdir + 'panel_c_'+region+'_Q100_boxplot.png')


# -- CR map
CR_map_fig = mpimg.imread(outdir + 'panel_b_AFRICA_CoastalRecession_map_RCP85_2100.png')
# -- CR boxplot
CR_boxplot_fig = mpimg.imread(outdir + 'panel_d_AFRICA_CoastalRecession_boxplot_RCP85_2100.png')

# %% cell 9
# -- Open figure device
plt.figure(1, figsize=[20,30],dpi=300).patch.set_facecolor('white')

# -- Split the device in multipanels
mapheight = 1  # Relative height of maps
boxplotheight = 1.4
grid = plt.GridSpec(2, 2, hspace=0.025, wspace=0, height_ratios=[mapheight,boxplotheight])#, wspace=0.1

# -- Q100
# -----------------------------------------------------
# -- Boxplot
plt.subplot(grid[1,0]).axis('off')
plt.imshow(Q100_boxplot_fig)
#plt.text(-30, 10, '(c)', fontsize=25)
fontsizeunit = 17
plt.text(-30, 200, r"1:100yr river discharge per unit catchment area (Q100, $m^3s^{-1}km^{-2}$)", rotation=90, fontsize=fontsizeunit)
plt.text(885, 350, r"Change in Q100 r.t. recent past ($m^3s^{-1}km^{-2}$)", rotation=-90, fontsize=fontsizeunit)

# -- Coastal Recession
# -----------------------------------------------------
# -- Map
plt.subplot(grid[0,1]).axis('off')
plt.imshow(CR_map_fig)
#plt.text(-20, 50, '(b)', fontsize=25)

# -- Boxplot
plt.subplot(grid[1,1]).axis('off')
plt.imshow(CR_boxplot_fig)
#plt.text(-20, 10, '(d)', fontsize=25)
plt.text(30, 490, 'Shoreline position change ($m$)', rotation=90, fontsize=fontsizeunit)
plt.text(490, 490, 'Shoreline position change ($m$)', rotation=90, fontsize=fontsizeunit)

plt.savefig(outfilename, transparent=True, bbox_inches='tight', pad_inches=0)
