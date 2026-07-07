# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/global_figure_12.4/.ipynb_checkpoints/Figure_1_multipanel-checkpoint.ipynb

# %% cell 3
import os
from IPython.display import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# %% cell 5
outdir = '/home/jservon/Chapter12_IPCC/figs/global_figure_1/'
outfilename = outdir + 'final_figure_1.png'

# %% cell 7
# -- tx35
variable = 'tx35'
wfuture = 'ssp585_2041-2060'
tx35_20412060_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = 'ssp585_2081-2100'
tx35_20812100_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = 'ssp126_2081-2100'
tx35_20812100_ssp126_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
tx35_colorbar = mpimg.imread(outdir + variable+'_colorbar.png')

# -- WBGT
variable = 'wbgt'
wfuture = 'ssp585_2041-2060'
wbgt_20412060_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = 'ssp585_2081-2100'
wbgt_20812100_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = 'ssp126_2081-2100'
wbgt_20812100_ssp126_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wbgt_colorbar = mpimg.imread(outdir + variable+'_colorbar.png')

# -- SPI
variable = 'spi6'
wfuture = 'ssp585_2041-2060'
wfuture = 'rcp85_2041-2060'
spi_20412060_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = 'ssp585_2081-2100'
wfuture = 'rcp85_2081-2100'
spi_20812100_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = 'ssp126_2081-2100'
wfuture = 'rcp26_2081-2100'
spi_20812100_ssp126_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
spi_colorbar = mpimg.imread(outdir + variable+'_colorbar.png')

# -- Soil moisture
sm_20412060_ssp585_fig = mpimg.imread('/home/jservon/colorbar_temp_penalty.png')
sm_20812100_ssp585_fig = mpimg.imread('/home/jservon/colorbar_temp_penalty.png')
sm_20812100_ssp126_fig = mpimg.imread('/home/jservon/colorbar_temp_penalty.png')
sm_colorbar = mpimg.imread('/home/jservon/colorbar_temp_penalty_perc_diffhorizon2020.png')

# -- Wind
variable = 'sfcWind'
wfuture = 'ssp585_2041-2060'
wind_20412060_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = 'ssp585_2081-2100'
wind_20812100_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = 'ssp126_2081-2100'
wind_20812100_ssp126_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wind_colorbar = mpimg.imread(outdir + variable+'_colorbar.png')

# -- Extreme Sea Level
variable = 'ESL'
wfuture = '2050_RCP85'
esl_20412060_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = '2100_RCP85'
esl_20812100_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
wfuture = '2100_RCP45'
esl_20812100_ssp126_fig = mpimg.imread(outdir + variable+'_'+wfuture+'.png')
esl_colorbar = mpimg.imread(outdir + variable+'_colorbar.png')

# %% cell 9
# -- Open figure device
plt.figure(1, figsize=[21,30])#,dpi=500)
fontsizeunit=12

# -- Split the device in multipanels
mapheight = 3  # Relative height of maps
colorbarheight = 1  # Relative height of colorbar
grid = plt.GridSpec(12, 12, wspace=0.1, hspace=0, height_ratios=[mapheight,colorbarheight,
                                                                 mapheight,colorbarheight,
                                                                 mapheight,colorbarheight,
                                                                 mapheight,colorbarheight,
                                                                 mapheight,colorbarheight,
                                                                 mapheight,colorbarheight
                                                                ])

# -- tx35
# -----------------------------------------------------
wline = 1
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(tx35_20412060_ssp585_fig)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(tx35_20812100_ssp585_fig)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(tx35_20812100_ssp126_fig)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(tx35_colorbar)
plt.text(900, 30, 'days/year', fontsize=fontsizeunit)

# -- WBGT
# -----------------------------------------------------
wline = 2
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(wbgt_20412060_ssp585_fig)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(wbgt_20812100_ssp585_fig)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(wbgt_20812100_ssp126_fig)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(wbgt_colorbar)
plt.text(900, 30, 'days/year', fontsize=fontsizeunit)

# -- SPI
# -----------------------------------------------------
wline = 3
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(spi_20412060_ssp585_fig)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(spi_20812100_ssp585_fig)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(spi_20812100_ssp126_fig)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(spi_colorbar)
plt.text(900, 30, 'events/year', fontsize=fontsizeunit)

# -- Soil Moisture
# -----------------------------------------------------
wline = 4
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(sm_20412060_ssp585_fig)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(sm_20812100_ssp585_fig)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(sm_20812100_ssp126_fig)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(sm_colorbar)
#plt.text(900, 30, 'days/year', fontsize=fontsizeunit)

# -- Wind
# -----------------------------------------------------
wline = 5
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(wind_20412060_ssp585_fig)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(wind_20812100_ssp585_fig)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(wind_20812100_ssp126_fig)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(wind_colorbar)
plt.text(900, 30, 'km/h', fontsize=fontsizeunit)

# -- Extreme Sea Level
# -----------------------------------------------------
wline = 6
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(esl_20412060_ssp585_fig)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(esl_20812100_ssp585_fig)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(esl_20812100_ssp126_fig)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(esl_colorbar)
plt.text(900, 30, 'm', fontsize=fontsizeunit)#, bbox=dict(facecolor='red', alpha=0.5))

#plt.show()

plt.savefig(outfilename, transparent=True, bbox_inches='tight', pad_inches=0)

# %% cell 10
Image(outfilename)
