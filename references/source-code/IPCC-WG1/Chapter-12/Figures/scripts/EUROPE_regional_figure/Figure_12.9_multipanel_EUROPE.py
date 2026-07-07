# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/EUROPE_regional_figure/Figure_12.9_multipanel_EUROPE.ipynb

# %% cell 3
import os
from IPython.display import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# %% cell 5
region = 'EUROPE'
outdir = os.getcwd()+'/../../figs/Figure_12.9/'
outfilename = outdir +region+'_regional_figure_12.9.png'

# %% cell 7
# -- Q100
# -------------------------
# -- Boxplot
Q100_boxplot_fig = mpimg.imread(outdir +'panel_c_'+ region+'_Q100_boxplot.png')

# -- Snow
# -------------------------
# -- map
SWE_map_fig = mpimg.imread(outdir + 'panel_b_SWE_map_RCP85_2050.png')
# -- Boxplot
SWE_boxplot_fig = mpimg.imread(outdir + 'panel_d_'+region+'_SWE_mask14_boxplot.png')

# -- Legend boxplot
Legend_boxplot_fig = mpimg.imread(outdir+'/Legend_boxplot.png')

# %% cell 9
# -- Open figure device
plt.figure(1, figsize=[22,20],dpi=200).patch.set_facecolor('white')
fontsizeunit=18

# -- Split the device in multipanels
mapheight = 1.2  # Relative height of maps
boxplotheight = 1
legendheight = 0.25
grid = plt.GridSpec(3, 2, hspace=0.05, wspace=0.05, height_ratios=[mapheight,boxplotheight,legendheight])#, wspace=0.1

# -- Q100
# -----------------------------------------------------
# -- Boxplot
plt.subplot(grid[1,0]).axis('off')
plt.imshow(Q100_boxplot_fig)
#plt.text(0, 10, '(c)', fontsize=25)
plt.text(-20, 80, r"Recent past Q100 ($m^3s^{-1}km^{-2}$)", rotation=90, fontsize=fontsizeunit)
plt.text(875, 20, r"Change in Q100 r.t. recent past ($m^3s^{-1}km^{-2}$)", rotation=-90, fontsize=fontsizeunit)


# -- SWE
# -----------------------------------------------------
# -- Map
plt.subplot(grid[0,1]).axis('off')
plt.imshow(SWE_map_fig)
#plt.text(-40, 50, '(b)', fontsize=25)

# -- Boxplot
plt.subplot(grid[1,1]).axis('off')
plt.imshow(SWE_boxplot_fig)
#plt.text(-20, 20, '(d)', fontsize=25)
plt.text(-20, 80, r"# days with SWE>100mm ($days.yr^{-1}$)", rotation=90, fontsize=fontsizeunit)


# -- Legend
# -----------------------------------------------------
plt.subplot(grid[2,:]).axis('off')
plt.imshow(Legend_boxplot_fig)


plt.savefig(outfilename, transparent=True, bbox_inches='tight', pad_inches=0)
