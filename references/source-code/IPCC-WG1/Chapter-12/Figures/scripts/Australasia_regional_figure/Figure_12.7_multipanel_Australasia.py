# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/Australasia_regional_figure/Figure_12.7_multipanel_Australasia.ipynb

# %% cell 3
import os
from IPython.display import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# %% cell 5
region = 'Australasia'
outdir = os.getcwd()+'/../../figs/Figure_12.7/'
outfilename = outdir +region+'_regional_figure_12.7.png'

# %% cell 7
# -- Q100 Boxplot
Q100_boxplot_fig = mpimg.imread(outdir + 'panel_c_'+region+'_Q100_boxplot.png')

# -- CR map
CR_map_fig = mpimg.imread(outdir + 'panel_b_'+region+'_CoastalRecession_map_RCP85_2100.png')
# -- CR boxplot
CR_boxplot_fig = mpimg.imread(outdir + 'panel_d_'+region+'_CoastalRecession_boxplot_RCP85_2100.png')

# %% cell 9
# -- Open figure device
plt.figure(1, figsize=[22,27],dpi=200).patch.set_facecolor('white')
fontsizeunit=17

# -- Split the device in multipanels
mapheight = 1  # Relative height of maps
boxplotheight = 1.6
grid = plt.GridSpec(2, 2, hspace=0, wspace=0.05, height_ratios=[mapheight,boxplotheight])#, wspace=0.1

# -- Q100
# -----------------------------------------------------
# -- Boxplot
plt.subplot(grid[1,0]).axis('off')
plt.imshow(Q100_boxplot_fig)
#plt.text(-30, 10, '(c)', fontsize=25)
#plt.text(-20, 100, r"Recent past value ($m^3s^{-1}km^{-2}$)", rotation=90, fontsize=fontsizeunit)
#plt.text(880, 80, r"Change r.t. recent past ($m^3s^{-1}km^{-2}$)", rotation=-90, fontsize=fontsizeunit)
plt.text(-20, 70, r"1:100yr river discharge per unit catchment area (Q100, $m^3s^{-1}km^{-2}$)", rotation=90, fontsize=fontsizeunit)
plt.text(885, 200, r"Change in Q100 r.t. recent past ($m^3s^{-1}km^{-2}$)", rotation=-90, fontsize=fontsizeunit)

# -- Coastal Recession
# -----------------------------------------------------
# -- Map
plt.subplot(grid[0,1]).axis('off')
plt.imshow(CR_map_fig)
#plt.text(-30, 40, '(b)', fontsize=25)
#plt.text(600, 570, 'm', fontsize=25)

# -- Boxplot
plt.subplot(grid[1,1]).axis('off')
plt.imshow(CR_boxplot_fig)
#plt.text(-30, 30, '(d)', fontsize=25)
#plt.text(-30, 80, 'Average shoreline position change (m)', rotation=90, fontsize=fontsizeunit)
plt.text(30, 290, 'Shoreline position change ($m$)', rotation=90, fontsize=fontsizeunit)
plt.text(490, 290, 'Shoreline position change ($m$)', rotation=90, fontsize=fontsizeunit)


plt.savefig(outfilename, transparent=True, bbox_inches='tight', pad_inches=0)
