# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/global_figure_12.4/.ipynb_checkpoints/wind_perc-baseline_individual_figures-checkpoint.ipynb

# %% cell 4
import os, glob
import xarray as xr
from IPython.display import Image
from PIL import Image as PILImage
from natsort import natsorted

# %% cell 5
CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/sfcWind'
outfigdir = CWD + '/../../figs/global_figure_12.4'

root_inputdatadir = '/data/jservon/IPCC'

# %% cell 6
variable = 'wind'

# %% cell 9
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

# %% cell 10
# -- Compute the annual sums
exp_list = [
    dict(experiment='historical',
         years = range(1971,2014)),
    dict(experiment='ssp585',
         years = range(2041,2061)),
    dict(experiment='ssp585',
         years = range(2081,2101)),
    dict(experiment='ssp126',
         years = range(2081,2101)),
]

# %% cell 11
for exp_dict in exp_list:
    years = exp_dict['years']
    experiment = exp_dict['experiment']
    for year in years:
        wfile = '/data/jservon/IPCC/'+variable+'/CMIP6_'+variable+'/CMIP6Amon_'+experiment+'_'+variable+'_'+str(year)+'.nc4'
        output_pattern = '/data/jservon/IPCC/'+variable+'/individual_models/CMIP6_'+experiment+'_'+variable+'_'+str(year)+'_'
        split_ensemble_file(wfile, output_pattern, variable)
#

# %% cell 14
from climaf.api import *

# %% cell 15
pattern = root_inputdatadir+'/${variable}/individual_models/CMIP6_${experiment}_${variable}_${period}_${member}.nc'
cproject('wind_individual_models_cmip6_ch12','experiment','period','member',('variable','wind'), ensemble=['member'], separator='%')
dataloc(project='wind_individual_models_cmip6_ch12', url=pattern)

# %% cell 17
exp_list = [
    dict(experiment='ssp585',
         period = '2041-2060'),
    dict(experiment='ssp585',
         period = '2081-2100'),
    dict(experiment='ssp126',
         period = '2081-2100'),
]

# -- Create ensemble for historical baseline
req_baseline = ds(project='wind_individual_models_cmip6_ch12',
                  experiment = 'historical',
                  period = '1971-2010',
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
    req_exp = ds(project='wind_individual_models_cmip6_ch12',
                 experiment = experiment,
                 period = period,
                 member = '*'
                )
    ens_exp = req_exp.explore('ensemble')
    
    # -- Extract common members
    wens_baseline, wens_exp = ensemble_intersection([ens_baseline, ens_exp])
    #
    # -- Climatologies
    clim_baseline = clim_average(wens_baseline, 'ANM')
    clim_exp      = clim_average(wens_exp, 'ANM')
    
    # -- Changes = Scenario minus baselines
    #diff_exp_baseline = fsub(clim_exp, clim_baseline)
    diff_exp_baseline = fmul( fdiv(fsub(clim_exp, clim_baseline), clim_baseline), 100)
    ens_diff[experiment+'_'+period] = diff_exp_baseline

# %% cell 19
pp_colorbar = dict(proj   = 'Robinson',
                   colors = '-10 -5.0 -2.5 -1.0 1.0 2.5 5.0 10',
                   color  = 'wind', #NCV_blu_red',
                   mpCenterLonF = 0,
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString=''
                  )

# %% cell 20
pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|mpGridAndLimbOn=True|mpGridLineColor=-1')
)

# %% cell 21
# -- Plot the individual models
wfuture = 'ssp126_2081-2100'
iplot_members(ens_diff[wfuture], N=1, plot_script=plot_ipcc, **pp)

# %% cell 22
iplot_members(ens_diff[wfuture], N=2, plot_script=plot_ipcc, **pp)

# %% cell 23
iplot_members(ens_diff[wfuture], N=3, plot_script=plot_ipcc, **pp)

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
        panel = 'panel_m'
    if wfuture=='ssp585_2041-2060':
        panel = 'panel_n'
    if wfuture=='ssp585_2081-2100':
        panel = 'panel_o'
    mask_agreement_name = outdatadir + '/mask_'+perc_agreement+'perc-agreement_sfcWind_'+panel+'_'+wfuture+'_minus_baseline.nc'
    cfile(model_agreement_dict[wfuture], target=mask_agreement_name)
    cmd = 'ncatted -O -a comment,global,o,c,"This file is used for the hatching of '+panel+' of figure 12.4 - Chapter 12" '+mask_agreement_name
    os.system(cmd)
    

# -- Ensemble medians
# ------------------------------------------------
# -- Panel m
wfuture = 'ssp126_2081-2100'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/sfcWind_panel_m_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel m of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel n
wfuture = 'ssp585_2041-2060'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/sfcWind_panel_n_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel n of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel o
wfuture = 'ssp585_2081-2100'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/sfcWind_panel_o_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel o of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# %% cell 30
from climaf.api import *
import os
from IPython.display import Image
from PIL import Image as PILImage

CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/sfcWind'
outfigdir = CWD + '/../../figs/global_figure_12.4'

# %% cell 32
pp_colorbar = dict(proj   = 'Robinson',
                   colors = '-10 -5.0 -2.5 -1.0 1.0 2.5 5.0 10',
                   color  = 'wind', #NCV_blu_red',
                   mpCenterLonF = 0,
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString=''
                  )

# %% cell 33
# -- Add plot parameters for the maps
pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|mpGridAndLimbOn=True|mpGridLineColor=-1'),
    tiMainFontHeightF = 0.032,
    gsnStringFontHeightF = 0.03
)

# %% cell 35
# -- variable
variable = 'wind'

# -- Percentage of model agreement (hatching)
perc_agreement = '80'

# -- Panel m
# --------------------------------------------------
wfuture = 'ssp126_2081-2100'
ensmedian_filename = outdatadir + '/sfcWind_panel_m_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable=variable)
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_sfcWind_panel_m_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable=variable)
# -- Save in png
panel_m = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                    title = '2081-2100, SSP1-2.6',
                    **pp
                    )
cfile(panel_m, target = outfigdir + '/panel_m_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_m_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                        title = '2081-2100, SSP1-2.6',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_m_pdf), target = outfigdir + '/panel_m_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')




# -- Panel n
# --------------------------------------------------
wfuture = 'ssp585_2041-2060'
ensmedian_filename = outdatadir + '/sfcWind_panel_n_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable=variable)
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_sfcWind_panel_n_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable=variable)
# -- Save in png
panel_n = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                    title = '2041-2060, SSP5-8.5',
                    **pp
                    )
cfile(panel_n, target = outfigdir + '/panel_n_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_n_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                        title = '2041-2060, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_n_pdf), target = outfigdir + '/panel_n_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')

# -- Panel o
# --------------------------------------------------
wfuture = 'ssp585_2081-2100'
ensmedian_filename = outdatadir + '/sfcWind_panel_o_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable=variable)
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_sfcWind_panel_o_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable=variable)
# -- Save in png
panel_o = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                    title = '2081-2100, SSP5-8.5',
                    **pp
                    )
cfile(panel_o, target = outfigdir + '/panel_o_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_o_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # days Tx>35~F34~0~F~C',
                        title = '2081-2100, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_o_pdf), target = outfigdir + '/panel_o_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')

# %% cell 37
# -- Colorbar
def extract_labelbar(figure_file,labelbar_file) :
    #import PIL
    im = PILImage.open(figure_file)
    im_crop = im.crop((52, 561, 930, 642))
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
colorbar_file = outfigdir+'/'+variable+'_perc-baseline_colorbar.png'

# -- Extract the colorbar
extract_labelbar(cfile(plot_4colorbar),colorbar_file)

Image(colorbar_file)

# %% cell 39
mp = cpage(fig_lines=[[panel_m,panel_n,panel_o]],
            insert=colorbar_file,
            insert_width=400, page_width=1200
          )
iplot(mp)
