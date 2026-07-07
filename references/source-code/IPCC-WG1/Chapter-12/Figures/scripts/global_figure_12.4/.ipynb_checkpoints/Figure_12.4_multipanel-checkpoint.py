# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/global_figure_12.4/.ipynb_checkpoints/Figure_12.4_multipanel-checkpoint.ipynb

# %% cell 3
import os
from IPython.display import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# %% cell 5
perc_agreement = '80'
HI_thres = '41'

# %% cell 6
outdir = os.getcwd()+'/../../figs/global_figure_12.4/'
outfilename = outdir + 'figure_12.4.png'

# %% cell 8
# -- tx35
variable = 'tx35'
wfuture = 'ssp585_2041-2060'
tx35_20412060_ssp585_fig = mpimg.imread(outdir + 'panel_b_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
#tx35_20412060_ssp585_fig = mpimg.imread(outdir + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp585_2081-2100'
tx35_20812100_ssp585_fig = mpimg.imread(outdir + 'panel_c_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp126_2081-2100'
tx35_20812100_ssp126_fig = mpimg.imread(outdir + 'panel_a_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
tx35_colorbar = mpimg.imread(outdir + variable+'_colorbar.png')

# -- HI
variable = 'HI'
wfuture = 'ssp585_2041-2060'
HI_20412060_ssp585_fig = mpimg.imread(outdir + 'panel_e_' + variable.upper()+HI_thres+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp585_2081-2100'
HI_20812100_ssp585_fig = mpimg.imread(outdir + 'panel_f_' + variable.upper()+HI_thres+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp126_2081-2100'
HI_20812100_ssp126_fig = mpimg.imread(outdir + 'panel_d_' + variable.upper()+HI_thres+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
HI_colorbar = mpimg.imread(outdir + variable.upper()+HI_thres+'_colorbar.png')

# -- DF6
variable = 'DF6'
wfuture = 'ssp585_midch'
DF6_20412060_ssp585_fig = mpimg.imread(outdir + 'panel_h_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp585_farch'
DF6_20812100_ssp585_fig = mpimg.imread(outdir + 'panel_i_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp126_farch'
DF6_20812100_ssp126_fig = mpimg.imread(outdir + 'panel_g_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
DF6_colorbar = mpimg.imread(outdir + variable+'_colorbar.png')

# -- Soil moisture
variable = 'mrso'
wfuture = 'ssp585_2041-2060'
sm_20412060_ssp585_fig = mpimg.imread(outdir + 'panel_k_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp585_2081-2100'
sm_20812100_ssp585_fig = mpimg.imread(outdir + 'panel_l_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp126_2081-2100'
sm_20812100_ssp126_fig = mpimg.imread(outdir + 'panel_j_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
sm_colorbar = mpimg.imread(outdir + variable+'_colorbar.png')

# -- Wind
variable = 'wind'
wfuture = 'ssp585_2041-2060'
wind_20412060_ssp585_fig = mpimg.imread(outdir + 'panel_n_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp585_2081-2100'
wind_20812100_ssp585_fig = mpimg.imread(outdir + 'panel_o_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wfuture = 'ssp126_2081-2100'
wind_20812100_ssp126_fig = mpimg.imread(outdir + 'panel_m_' + variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
wind_colorbar = mpimg.imread(outdir + variable+'_perc-baseline_colorbar.png')

# -- Extreme Total Water Level
variable = 'ESL'
wfuture = '2050_RCP85'
esl_20412060_ssp585_fig = mpimg.imread(outdir + 'panel_q_' + variable+'_'+wfuture+'-final.png')
wfuture = '2100_RCP85'
esl_20812100_ssp585_fig = mpimg.imread(outdir + 'panel_r_' + variable+'_'+wfuture+'-final.png')
wfuture = '2100_RCP45'
esl_20812100_ssp126_fig = mpimg.imread(outdir + 'panel_p_' + variable+'_'+wfuture+'-final.png')
esl_colorbar = mpimg.imread(outdir + variable+'_colorbar.png')

# %% cell 10
# -- Open figure device
#plt.figure(1, figsize=[21,30],dpi=500)
plt.figure(1, figsize=[18,30],dpi=200).patch.set_facecolor('white')
fontsizeunit=16

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

fontsize_label = 20

# -- tx35
# -----------------------------------------------------
wline = 1
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(tx35_20812100_ssp126_fig)
plt.text(-30, 120, '(a)', fontsize=fontsize_label)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(tx35_20412060_ssp585_fig)
plt.text(-30, 120, '(b)', fontsize=fontsize_label)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(tx35_20812100_ssp585_fig)
plt.text(-30, 120, '(c)', fontsize=fontsize_label)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(tx35_colorbar)
plt.text(900, 35, r"$days.yr^{-1}$", fontsize=fontsizeunit)

# -- HI
# -----------------------------------------------------
wline = 2
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(HI_20812100_ssp126_fig)
plt.text(-30, 120, '(d)', fontsize=fontsize_label)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(HI_20412060_ssp585_fig)
plt.text(-30, 120, '(e)', fontsize=fontsize_label)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(HI_20812100_ssp585_fig)
plt.text(-30, 120, '(f)', fontsize=fontsize_label)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(HI_colorbar)
plt.text(900, 38, r"$days.yr^{-1}$", fontsize=fontsizeunit)

# -- SPI
# -----------------------------------------------------
wline = 3
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(DF6_20812100_ssp126_fig)
plt.text(-30, 120, '(g)', fontsize=fontsize_label)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(DF6_20412060_ssp585_fig)
plt.text(-30, 120, '(h)', fontsize=fontsize_label)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(DF6_20812100_ssp585_fig)
plt.text(-30, 120, '(i)', fontsize=fontsize_label)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(DF6_colorbar)
plt.text(900, 38, r"$events.decade^{-1}$", fontsize=fontsizeunit)

# -- Soil Moisture
# -----------------------------------------------------
wline = 4
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(sm_20812100_ssp126_fig)
plt.text(-30, 120, '(j)', fontsize=fontsize_label)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(sm_20412060_ssp585_fig)
plt.text(-30, 120, '(k)', fontsize=fontsize_label)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(sm_20812100_ssp585_fig)
plt.text(-30, 120, '(l)', fontsize=fontsize_label)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(sm_colorbar)
plt.text(900, 35, '%', fontsize=fontsizeunit+0.03)

# -- Wind
# -----------------------------------------------------
wline = 5
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(wind_20812100_ssp126_fig)
plt.text(-30, 120, '(m)', fontsize=fontsize_label)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(wind_20412060_ssp585_fig)
plt.text(-30, 120, '(n)', fontsize=fontsize_label)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(wind_20812100_ssp585_fig)
plt.text(-30, 120, '(o)', fontsize=fontsize_label)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(wind_colorbar)
plt.text(900, 37, '%', fontsize=fontsizeunit)

# -- Extreme Sea Level
# -----------------------------------------------------
wline = 6
# -- 20412060_ssp585
plt.subplot(grid[wline*2-2,0:4]).axis('off')
plt.imshow(esl_20812100_ssp126_fig)
plt.text(-30, 120, '(p)', fontsize=fontsize_label)
# -- 208121O0_ssp585
plt.subplot(grid[wline*2-2,4:8]).axis('off')
plt.imshow(esl_20412060_ssp585_fig)
plt.text(-30, 120, '(q)', fontsize=fontsize_label)
# -- 20812100_ssp126
plt.subplot(grid[wline*2-2,8:12]).axis('off')
plt.imshow(esl_20812100_ssp585_fig)
plt.text(-30, 120, '(r)', fontsize=fontsize_label)
# -- Colorbar
plt.subplot(grid[wline*2-1,4:8]).axis('off')
plt.imshow(esl_colorbar)
plt.text(650, 33, 'm', fontsize=fontsizeunit)#, bbox=dict(facecolor='red', alpha=0.5))

#plt.show()

plt.savefig(outfilename, transparent=True, bbox_inches='tight', pad_inches=0)
