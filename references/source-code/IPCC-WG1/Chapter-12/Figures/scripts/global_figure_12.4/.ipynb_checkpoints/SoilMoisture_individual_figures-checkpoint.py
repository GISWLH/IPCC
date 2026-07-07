# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/global_figure_12.4/.ipynb_checkpoints/SoilMoisture_individual_figures-checkpoint.ipynb

# %% cell 4
import os, glob
import xarray as xr
from IPython.display import Image
from PIL import Image as PILImage

# %% cell 5
CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/SM'
outfigdir = CWD + '/../../figs/global_figure_12.4'

root_inputdatadir = '/thredds/ipsl/jservon/Chapter12/temporary_data_20210415'

# %% cell 6
variable = 'mrso'

# %% cell 10
from climaf.api import *

# %% cell 12
#pattern = '/data/jservon/IPCC/spi/individual_models/'+CMIP+'/'+CMIP+'_${experiment}_${variable}_${period}_${member}.nc'
pattern = root_inputdatadir+'/mrso/data.iac.ethz.ch/IPCC_AR6/for_ch12/cmip6/mrso/sm_annmean_regrid_g010a/sm_annmean_regrid_g010a_${variable}_Lmon_${model}_${experiment}_${realization}_gn.nc'
cproject('mrso_individual_models_cmip6_ch12','experiment','model','realization',('variable',variable), ensemble=['model'], separator='%')
dataloc(project='mrso_individual_models_cmip6_ch12', url=pattern)

# %% cell 14
exp_list = [
    dict(experiment='ssp585',
         period = '2041-2060'),
    dict(experiment='ssp585',
         period = '2081-2100'),
    dict(experiment='ssp126',
         period = '2081-2100'),
]

# -- Create ensemble for historical baseline
# 1. Initial request to list all the models
req_baseline_dict = dict(project='mrso_individual_models_cmip6_ch12',
                         experiment = 'historical',
                         period = '1995-2004',
                         realization = '*'
                        )
req_baseline = ds(model='*', **req_baseline_dict)
# 2. Build the ensemble by hand to deal with the realizations
ens_baseline_dict = dict()
for model in req_baseline.explore('choices')['model']:
    ens_baseline_dict[model] = ds(model=model, **req_baseline_dict).explore('resolve')
ens_baseline = cens(ens_baseline_dict)

# -- Loop on the scenarios
ens_diff = dict()
for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    period = exp['period']
    
    # -- Create ensemble object for the scenario
    # 1. Initial request to list all the models
    req_exp_dict = dict(project='mrso_individual_models_cmip6_ch12',
                        experiment = experiment,
                        period = period,
                        realization = '*'
                       )
    req_exp = ds(model='*', **req_exp_dict)
    # 2. Build the ensemble by hand to deal with the realizations
    ens_exp_dict = dict()
    for model in req_exp.explore('choices')['model']:
        ens_exp_dict[model] = ds(model=model, **req_exp_dict).explore('resolve')
    ens_exp = cens(ens_exp_dict)
    
    # -- Extract common members
    wens_baseline, wens_exp = ensemble_intersection([ens_baseline, ens_exp])
    #    
    # -- Climatologies
    clim_baseline = clim_average(wens_baseline, 'ANM')
    clim_exp      = clim_average(wens_exp, 'ANM')
    
    # -- Changes = Scenario minus baselines
    diff_exp_baseline = fmul( fdiv(fsub(clim_exp, clim_baseline), clim_baseline), 100)
    ens_diff[experiment+'_'+period] = diff_exp_baseline

# %% cell 16
pp_colorbar = dict(proj   = 'Robinson',
                   min = -5, max=5, delta=0.5,
                   color  = 'MPL_BrBG',#NCV_blu_red',
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString=''
                  )

# %% cell 17
pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|lbBoxEndCapStyle=TriangleBothEnds|mpGridAndLimbOn=True|mpGridLineColor=-1')
)

# %% cell 18
clog('critical')

# %% cell 19
# -- Plot the individual models
wfuture = 'ssp585_2081-2100'
iplot_members(ens_diff[wfuture], N=1, **pp)

# %% cell 20
iplot_members(ens_diff[wfuture], N=2, **pp)

# %% cell 23
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
        panel = 'panel_j'
    if wfuture=='ssp585_2041-2060':
        panel = 'panel_k'
    if wfuture=='ssp585_2081-2100':
        panel = 'panel_l'
    mask_agreement_name = outdatadir + '/mask_'+perc_agreement+'perc-agreement_SM_'+panel+'_'+wfuture+'_minus_baseline.nc'
    cfile(model_agreement_dict[wfuture], target=mask_agreement_name)
    cmd = 'ncatted -O -a comment,global,o,c,"This file is used for the hatching of '+panel+' of figure 12.4 - Chapter 12" '+mask_agreement_name
    os.system(cmd)
    

# -- Ensemble medians
# ------------------------------------------------
# -- Panel j
wfuture = 'ssp126_2081-2100'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/SM_panel_j_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel j of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel k
wfuture = 'ssp585_2041-2060'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/SM_panel_k_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel k of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel l
wfuture = 'ssp585_2081-2100'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/SM_panel_l_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel l of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# %% cell 27
from climaf.api import *
import os
from IPython.display import Image
from PIL import Image as PILImage

CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/SM'
outfigdir = CWD + '/../../figs/global_figure_12.4'

# %% cell 29
pp_colorbar = dict(proj   = 'Robinson',
                   min = -5, max=5, delta=0.5,
                   color  = 'MPL_BrBG',#NCV_blu_red',
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString=''
                  )
pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|lbBoxEndCapStyle=TriangleBothEnds|mpGridAndLimbOn=True|mpGridLineColor=-1',
         tiMainFontHeightF = 0.032,
         gsnStringFontHeightF = 0.03

        )
)

# %% cell 31
# -- variable
variable = 'mrso'

# -- Percentage of model agreement (hatching)
perc_agreement = '80'

# -- Panel j
# --------------------------------------------------
wfuture = 'ssp126_2081-2100'
ensmedian_filename = outdatadir + '/SM_panel_j_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable=variable)
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_SM_panel_j_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable=variable)
# -- Save in png
panel_j = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in soil moisture',
                    title = '2081-2100, SSP1-2.6',
                    **pp
                    )
cfile(panel_j, target = outfigdir + '/panel_j_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_j_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in soil moisture',
                        title = '2081-2100, SSP1-2.6',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_j_pdf), target = outfigdir + '/panel_j_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')




# -- Panel k
# --------------------------------------------------
wfuture = 'ssp585_2041-2060'
ensmedian_filename = outdatadir + '/SM_panel_k_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable=variable)
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_SM_panel_k_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable=variable)
# -- Save in png
panel_k = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in soil moisture',
                    title = '2041-2060, SSP5-8.5',
                    **pp
                    )
cfile(panel_k, target = outfigdir + '/panel_k_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_k_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in soil moisture',
                        title = '2041-2060, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_k_pdf), target = outfigdir + '/panel_k_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')

# -- Panel l
# --------------------------------------------------
wfuture = 'ssp585_2081-2100'
ensmedian_filename = outdatadir + '/SM_panel_l_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable=variable)
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_SM_panel_l_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable=variable)
# -- Save in png
panel_l = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in soil moisture',
                    title = '2081-2100, SSP5-8.5',
                    **pp
                    )
cfile(panel_l, target = outfigdir + '/panel_l_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_l_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in soil moisture',
                        title = '2081-2100, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_l_pdf), target = outfigdir + '/panel_l_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')

# %% cell 33
# -- Colorbar
def extract_labelbar(figure_file,labelbar_file) :
    #import PIL
    im = PILImage.open(figure_file)
    im_crop = im.crop((55, 563, 930, 641))
    im_crop.save(labelbar_file, quality=95)

# -- pdf
plot_4colorbar = plot_ipcc(ensmedian_field,
                      options='lbOrientation=horizontal|lbLabelFontHeightF=0.015|lbBoxEndCapStyle=TriangleBothEnds',
                           format='pdf',
                      **pp_colorbar)
colorbar_file = outfigdir+'/'+variable+'_colorbar.pdf'
cfile(cpdfcrop(plot_4colorbar), target=colorbar_file)

# -- png
plot_4colorbar = plot_ipcc(ensmedian_field,
                      options='lbOrientation=horizontal|lbLabelFontHeightF=0.015|lbBoxEndCapStyle=TriangleBothEnds',
                      **pp_colorbar)
colorbar_file = outfigdir+'/'+variable+'_colorbar.png'

# -- Extract the colorbar
extract_labelbar(cfile(plot_4colorbar),colorbar_file)

Image(colorbar_file)

# %% cell 35
mp = cpage(fig_lines=[[panel_j,panel_k,panel_l]],
            insert=colorbar_file,
            insert_width=400, page_width=1200
          )
iplot(mp)
