# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/global_figure_12.4/.ipynb_checkpoints/tx35_individual_figures-checkpoint.ipynb

# %% cell 4
import os, glob
import xarray as xr
from IPython.display import Image
from PIL import Image as PILImage

# %% cell 5
CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/tx35'
outfigdir = CWD + '/../../figs/global_figure_12.4'

root_inputdatadir = '/data/jservon/IPCC'

# %% cell 8
# -- Function to split a multi-member file in individual files
# -- Uses Xarray
def split_ensemble_file(ensemble_file, output_pattern, variable):
    if not os.path.isdir(os.path.dirname(output_pattern)):
        os.makedirs(os.path.dirname(output_pattern))
    import xarray as xr
    dat = xr.open_dataset(ensemble_file)[variable]
    for member in dat.member:
        member_name = str(member.values)
        print member_name
        outfilename = output_pattern+member_name+'.nc'
        if not os.path.isfile(outfilename):
            print 'Save '+outfilename
            member_dat = dat.loc[:,member_name,:,:]
            member_dat.to_netcdf(outfilename)
        else:
            print outfilename+' already exists'

# %% cell 9
variable='tx35'

# -- Compute the annual sums
exp_list = [
    dict(experiment='ssp126',
         years = range(2015,2101)),
    dict(experiment='ssp585',
         years = range(2015,2101)),
]

# %% cell 10
variable='tx35isimip'
for exp_dict in exp_list:
    years = exp_dict['years']
    experiment = exp_dict['experiment']
    for year in years:
        wfile = root_inputdatadir+'/tx35/bias_corrected/CMIP6_'+experiment+'_'+variable+'/CMIP6_'+experiment+'_'+variable+'_'+str(year)+'.nc4'
        output_pattern = root_inputdatadir+'/tx35/bias_corrected/individual_models/CMIP6_'+experiment+'_'+variable+'_'+str(year)+'_'
        split_ensemble_file(wfile, output_pattern, variable)
#

# %% cell 13
from climaf.api import *

# %% cell 15
pattern = root_inputdatadir+'/tx35/bias_corrected/individual_models/CMIP6_${experiment}_${variable}_${period}_${member}.nc'
cproject('tx_individual_models_cmip6_ch12','experiment','period','member',('variable','tx35isimip'), ensemble=['member'], separator='%')
dataloc(project='tx_individual_models_cmip6_ch12', url=pattern)

# %% cell 17
req_baseline = ds(project='tx_individual_models_cmip6_ch12',
                  experiment = 'historical',
                  period = '*',
                  member = '*'
                 )
req_baseline.explore('choices')

# %% cell 18
exp_list = [
    dict(experiment='ssp585',
         period = '2041-2060'),
    dict(experiment='ssp585',
         period = '2081-2100'),
    dict(experiment='ssp126',
         period = '2081-2100'),
]

# -- Create ensemble for historical baseline
req_baseline = ds(project='tx_individual_models_cmip6_ch12',
                  experiment = 'historical',
                  period = '1995-2014',
                  member = '*'
                 )
ens_baseline = req_baseline.explore('ensemble')

# -- Loop on the scenarios
ens_diff = dict()
for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    period = exp['period']
    
    # -- Create ensemble object for the scenario
    req_exp = ds(project='tx_individual_models_cmip6_ch12',
                 experiment = experiment,
                 period = period,
                 member = '*'
                )
    ens_exp = req_exp.explore('ensemble')
    
    # -- Extract common members
    wens_baseline, wens_exp = ensemble_intersection([ens_baseline, ens_exp])
    #
    # -- Compute annual sums
    yearsum_baseline = ccdo(wens_baseline, operator='yearsum')
    yearsum_exp      = ccdo(wens_exp, operator='yearsum')
    
    # -- Climatologies
    clim_baseline = clim_average(yearsum_baseline, 'ANM')
    clim_exp      = clim_average(yearsum_exp, 'ANM')
    
    # -- Changes = Scenario minus baselines
    diff_exp_baseline = fsub(clim_exp, clim_baseline)
    diff_exp_baseline.pop('EC-Earth3-Veg_r1i1p1f1')
    ens_diff[experiment+'_'+period] = diff_exp_baseline

# %% cell 20
pp_colorbar = dict(proj   = 'Robinson',
                   colors = '-15 -5 -1 1 5 15 30 45 60 75 100 150 200',
                   color  = 'HI_palette',
                   mpCenterLonF = 0,
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString='',
                  )

pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|mpGridAndLimbOn=True|mpGridLineColor=-1')
)

# %% cell 21
# -- Plot the individual models
wfuture = 'ssp585_2081-2100'
iplot_members(ens_diff[wfuture], plot_script=plot_ipcc, N=1, **pp)

# %% cell 22
iplot_members(ens_diff[wfuture], plot_script=plot_ipcc, N=2, **pp)

# %% cell 23
iplot_members(ens_diff[wfuture], plot_script=plot_ipcc, N=3, **pp)

# %% cell 26
perc_agreement = '80'

# -- Model agreement
# ------------------------------------------------
model_agreement_dict = dict()
for exp in exp_list:
    # -- Experiment and period
    experiment = exp['experiment']
    period = exp['period']
    wfuture = experiment+'_'+period

    # -- Mask of models with
    ens_mask_pos = ccdo(ens_diff[wfuture], operator='gtc,0')
    ens_mask_neg = ccdo(ens_diff[wfuture], operator='ltc,0')
    ens_mask_zero = ccdo(ens_diff[wfuture], operator='eqc,0')

    perc_ens_pos = fmul( fdiv( ccdo_ens(ens_mask_pos, operator='enssum'), len(ens_diff[wfuture]) ), 100 )
    perc_ens_neg = fmul( fdiv( ccdo_ens(ens_mask_neg, operator='enssum'), len(ens_diff[wfuture]) ), 100 )
    perc_ens_zero = fmul( fdiv( ccdo_ens(ens_mask_zero, operator='enssum'), len(ens_diff[wfuture]) ), 100 )

    # -- Signif90
    model_agreement_pos = ccdo(perc_ens_pos, operator='gtc,'+perc_agreement)
    model_agreement_neg = ccdo(perc_ens_neg, operator='gtc,'+perc_agreement)
    model_agreement_zero = ccdo(perc_ens_zero, operator='gtc,'+perc_agreement)
    model_agreement_dict[wfuture] = fmul( fadd( fadd(model_agreement_pos, model_agreement_neg), model_agreement_zero), -1)
    if wfuture=='ssp126_2081-2100':
        panel = 'panel_a'
    if wfuture=='ssp585_2041-2060':
        panel = 'panel_b'
    if wfuture=='ssp585_2081-2100':
        panel = 'panel_c'
    mask_agreement_name = outdatadir + '/mask_'+perc_agreement+'perc-agreement_tx35_'+panel+'_'+wfuture+'_minus_baseline.nc'
    cfile(model_agreement_dict[wfuture], target=mask_agreement_name)
    cmd = 'ncatted -O -a comment,global,o,c,"This file is used for the hatching of '+panel+' of figure 12.4 - Chapter 12" '+mask_agreement_name
    os.system(cmd)
    

# -- Ensemble medians
# ------------------------------------------------
# -- Panel a
wfuture = 'ssp126_2081-2100'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/tx35_panel_a_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel a of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel b
wfuture = 'ssp585_2041-2060'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/tx35_panel_b_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel b of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel c
wfuture = 'ssp585_2081-2100'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/tx35_panel_c_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel c of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# %% cell 30
from climaf.api import *
import os
from IPython.display import Image
from PIL import Image as PILImage

CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/tx35'
outfigdir = CWD + '/../../figs/global_figure_12.4'

# %% cell 32
# -- Just for the colorbar
pp_colorbar = dict(proj   = 'Robinson',
                   colors = '-15 -5 -1 1 5 15 30 45 60 75 100 150 200',
                   color  = 'HI_palette',
                   mpCenterLonF = 0,
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString='',
                  )

# -- Add plot parameters for the maps
pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|mpGridAndLimbOn=True|mpGridLineColor=-1'),
    tiMainFontHeightF = 0.032,
    gsnStringFontHeightF = 0.03
)

# %% cell 34
# -- variable
variable = 'tx35'

# -- Percentage of model agreement (hatching)
perc_agreement = '80'

# -- Panel a
# --------------------------------------------------
wfuture = 'ssp126_2081-2100'
ensmedian_filename = outdatadir + '/tx35_panel_a_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable='tx35isimip')
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_tx35_panel_a_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable='tx35isimip')
# -- Save in png
panel_a = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                    title = '2081-2100, SSP1-2.6',
                    **pp
                    )
cfile(panel_a, target = outfigdir + '/panel_a_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_a_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                        title = '2081-2100, SSP1-2.6',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_a_pdf), target = outfigdir + '/panel_a_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')




# -- Panel b
# --------------------------------------------------
wfuture = 'ssp585_2041-2060'
ensmedian_filename = outdatadir + '/tx35_panel_b_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable='tx35isimip')
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_tx35_panel_b_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable='tx35isimip')
# -- Save in png
panel_b = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                    title = '2041-2060, SSP5-8.5',
                    **pp
                    )
cfile(panel_b, target = outfigdir + '/panel_b_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_b_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                        title = '2041-2060, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_b_pdf), target = outfigdir + '/panel_b_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')

# -- Panel c
# --------------------------------------------------
wfuture = 'ssp585_2081-2100'
ensmedian_filename = outdatadir + '/tx35_panel_c_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable='tx35isimip')
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_tx35_panel_c_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable='tx35isimip')
# -- Save in png
panel_c = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                    title = '2081-2100, SSP5-8.5',
                    **pp
                    )
cfile(panel_c, target = outfigdir + '/panel_c_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_c_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                        title = '2081-2100, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_c_pdf), target = outfigdir + '/panel_c_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')

# %% cell 36
# -- Colorbar
def extract_labelbar(figure_file,labelbar_file) :
    im = PILImage.open(figure_file)
    im_crop = im.crop((55, 564, 930, 642))
    im_crop.save(labelbar_file, quality=95)

# -- pdf
plot_4colorbar = plot_ipcc(ensmedian_field,
                      options='lbOrientation=horizontal|lbLabelFontHeightF=0.015|lbBoxEndCapStyle=TriangleBothEnds',
                           format='pdf',
                      **pp_colorbar)

# -- color bar file
colorbar_file = outfigdir+'/'+variable+'_colorbar.pdf'
cfile(cpdfcrop(plot_4colorbar), target=colorbar_file)

# -- png
plot_4colorbar = plot_ipcc(ensmedian_field,
                      options='lbOrientation=horizontal|lbLabelFontHeightF=0.015|lbBoxEndCapStyle=TriangleBothEnds',
                      **pp_colorbar)

# -- color bar file
colorbar_file = outfigdir+'/'+variable+'_colorbar.png'

# -- Extract the colorbar
extract_labelbar(cfile(plot_4colorbar),colorbar_file)

Image(colorbar_file)

# %% cell 38
mp = cpage(fig_lines=[[panel_a,panel_b,panel_c]],
            insert=colorbar_file,
            insert_width=400, page_width=1200
          )
iplot(mp)
