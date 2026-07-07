# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/global_figure_12.4/HI_NOAA_individual_figures.ipynb

# %% cell 3
import os, glob
import xarray as xr
from IPython.display import Image
from PIL import Image as PILImage

# %% cell 4
CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/HI41'
outfigdir = CWD + '/../../figs/global_figure_12.4'

root_inputdatadir = '/data/jservon/IPCC'

# %% cell 7
lof = glob.glob('/data/ciles/IPCC/FGD/HI_NOAA/CMIP6/*/*_*-*_QDM_HI.nc')
outdir = root_inputdatadir+'/HI_NOAA/CMIP6/'
for wfile in lof:
    #print wfile
    # -- Get model, realization, and threshold
    dumsplit = wfile.split('/')[-1].split('_')
    thres = dumsplit[1]
    model = dumsplit[2]
    scenario = dumsplit[3]
    realization = dumsplit[4]
    period = dumsplit[5]
    if '.' not in period:
        #print model, realization, thres, scenario, period
        target = outdir+model+'_'+realization+'_'+thres+'_'+scenario+'_'+period+'.nc'
        cmd = 'cdo -b 32 setmissval,1e+20 -copy '+wfile+' '+target
        print cmd
        cmd2 = 'ncatted -O -a coordinates,HI,o,c,"time lat lon" -a units,HI,o,c,days -a long_name,HI,o,c,"Number of days per year with HI temperature above '+thres+' degC" '+target
        os.system(cmd)
        os.system(cmd2)
    # -- Add coordinates attribute
    # -- set FillValue

# %% cell 10
from climaf.api import *

# %% cell 11
climaf.cache.stamping=False

# %% cell 13
pattern = root_inputdatadir+'/HI_NOAA/CMIP6/${member}_${thres}_${experiment}_${period}.nc'
cproject('HI_cmip6_ch12','experiment','period','member','thres', ('variable','HI'), ensemble=['member'], separator='%')
dataloc(project='HI_cmip6_ch12', url=pattern)

# %% cell 15
wthres = '41'
thres = 'Exceed'+wthres
variable = 'HI'

exp_list = [
    dict(experiment='ssp585',
         period = '2041-2060'),
    dict(experiment='ssp585',
         period = '2081-2100'),
    dict(experiment='ssp126',
         period = '2081-2100'),
]

# -- Create ensemble for historical baseline
req_baseline = ds(project='HI_cmip6_ch12',
                  experiment = 'ssp585',
                  period = '1995-2014',
                  member = '*',
                  thres = thres
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
    req_exp = ds(project='HI_cmip6_ch12',
                 experiment = experiment,
                 period = period,
                 member = '*',
                 thres = thres
                )
    ens_exp = req_exp.explore('ensemble')
    
    # -- Extract common members
    wens_baseline, wens_exp = ensemble_intersection([ens_baseline, ens_exp])
    #    
    # -- Climatologies
    clim_baseline = clim_average(wens_baseline, 'ANM')
    clim_exp      = clim_average(wens_exp, 'ANM')
    
    # -- Changes = Scenario minus baselines
    diff_exp_baseline = fsub(clim_exp, clim_baseline)
    ens_diff[experiment+'_'+period] = diff_exp_baseline

# %% cell 16
pp_colorbar = dict(proj   = 'Robinson',
                   colors = '-15 -5 -1 1 5 15 30 45 60 75 100 150 200',
                   color  = 'HI_palette',
                   mpCenterLonF = 0,
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString=''
                  )

# %% cell 17
pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|mpGridAndLimbOn=True|mpGridLineColor=-1')
)

# %% cell 18
# -- Plot the individual models
wfuture = 'ssp585_2081-2100'
iplot_members(ens_diff[wfuture], plot_script=plot_ipcc, N=1, **pp)

# %% cell 19
iplot_members(ens_diff[wfuture], plot_script=plot_ipcc, N=2, **pp)

# %% cell 20
iplot_members(ens_diff[wfuture], plot_script=plot_ipcc, N=3, **pp)

# %% cell 22
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
    ens_mask_pos = regridn(ccdo(ens_diff[wfuture], operator='gtc,0'), cdogrid='r360x180', option='remapnn')
    ens_mask_neg = regridn(ccdo(ens_diff[wfuture], operator='ltc,0'), cdogrid='r360x180', option='remapnn')
    ens_mask_zero = regridn(ccdo(ens_diff[wfuture], operator='eqc,0'), cdogrid='r360x180', option='remapnn')

    perc_ens_pos = fmul( fdiv( ccdo_ens(ens_mask_pos, operator='enssum'), len(ens_diff[wfuture]) ), 100 )
    perc_ens_neg = fmul( fdiv( ccdo_ens(ens_mask_neg, operator='enssum'), len(ens_diff[wfuture]) ), 100 )
    perc_ens_zero = fmul( fdiv( ccdo_ens(ens_mask_zero, operator='enssum'), len(ens_diff[wfuture]) ), 100 )

    # -- Signif90
    model_agreement_pos = ccdo(perc_ens_pos, operator='gtc,'+perc_agreement)
    model_agreement_neg = ccdo(perc_ens_neg, operator='gtc,'+perc_agreement)
    model_agreement_zero = ccdo(perc_ens_zero, operator='gtc,'+perc_agreement)
    model_agreement_dict[wfuture] = fmul( fadd( fadd(model_agreement_pos, model_agreement_neg), model_agreement_zero), -1)
    if wfuture=='ssp126_2081-2100':
        panel = 'panel_d'
    if wfuture=='ssp585_2041-2060':
        panel = 'panel_e'
    if wfuture=='ssp585_2081-2100':
        panel = 'panel_f'
    mask_agreement_name = outdatadir + '/mask_'+perc_agreement+'perc-agreement_HI41_'+panel+'_'+wfuture+'_minus_baseline.nc'
    cfile(model_agreement_dict[wfuture], target=mask_agreement_name)
    cmd = 'ncatted -O -a comment,global,o,c,"This file is used for the hatching of '+panel+' of figure 12.4 - Chapter 12" '+mask_agreement_name
    os.system(cmd)
    

# -- Ensemble medians
# ------------------------------------------------
# -- Panel d
wfuture = 'ssp126_2081-2100'
ensmedian_field = ccdo_ens(regridn(ens_diff[wfuture],cdogrid='r360x180'), operator='enspctl,50')
ensmedian_filename = outdatadir + '/HI41_panel_d_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel d of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel e
wfuture = 'ssp585_2041-2060'
ensmedian_field = ccdo_ens(regridn(ens_diff[wfuture],cdogrid='r360x180'), operator='enspctl,50')
ensmedian_filename = outdatadir + '/HI41_panel_e_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel e of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel f
wfuture = 'ssp585_2081-2100'
ensmedian_field = ccdo_ens(regridn(ens_diff[wfuture],cdogrid='r360x180'), operator='enspctl,50')
ensmedian_filename = outdatadir + '/HI41_panel_f_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel f of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# %% cell 26
from climaf.api import *
import os
from IPython.display import Image
from PIL import Image as PILImage

CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/HI41'
outfigdir = CWD + '/../../figs/global_figure_12.4'

# %% cell 28
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

# %% cell 30
# -- variable
variable = 'HI41'
wthres = '41'

# -- Percentage of model agreement (hatching)
perc_agreement = '80'

# -- Panel d
# --------------------------------------------------
wfuture = 'ssp126_2081-2100'
ensmedian_filename = outdatadir + '/HI41_panel_d_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable='HI')
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_HI41_panel_d_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable='HI')
# -- Save in png
panel_d = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # days HI>'+wthres+'~F34~0~F~C',
                    title = '2081-2100, SSP1-2.6',
                    **pp
                    )
cfile(panel_d, target = outfigdir + '/panel_d_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_d_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # days HI>'+wthres+'~F34~0~F~C',
                        title = '2081-2100, SSP1-2.6',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_d_pdf), target = outfigdir + '/panel_d_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')


# -- Panel e
# --------------------------------------------------
wfuture = 'ssp585_2041-2060'
ensmedian_filename = outdatadir + '/HI41_panel_e_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable='HI')
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_HI41_panel_e_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable='HI')
# -- Save in png
panel_e = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # days HI>'+wthres+'~F34~0~F~C',
                    title = '2041-2060, SSP5-8.5',
                    **pp
                    )
cfile(panel_e, target = outfigdir + '/panel_e_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_e_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # days HI>'+wthres+'~F34~0~F~C',
                        title = '2041-2060, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_e_pdf), target = outfigdir + '/panel_e_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')


# -- Panel f
# --------------------------------------------------
wfuture = 'ssp585_2081-2100'
ensmedian_filename = outdatadir + '/HI41_panel_f_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable='HI')
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_HI41_panel_f_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable='HI')
# -- Save in png
panel_f = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # days HI>'+wthres+'~F34~0~F~C',
                    title = '2081-2100, SSP5-8.5',
                    **pp
                    )
cfile(panel_f, target = outfigdir + '/panel_f_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_f_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # days HI>'+wthres+'~F34~0~F~C',
                        title = '2081-2100, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_f_pdf), target = outfigdir + '/panel_f_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')

# %% cell 32
# -- Colorbar
def extract_labelbar(figure_file,labelbar_file) :
    #import PIL
    im = PILImage.open(figure_file)
    #box=(left, upper, right, lower).
    im_crop = im.crop((55, 564, 930, 642))
    im_crop.save(labelbar_file, quality=95)

# -- Base plot for the colorbar
wfuture = 'ssp585_2081-2100'

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

# %% cell 34
mp = cpage(fig_lines=[[panel_d,panel_e,panel_f]],
            insert=colorbar_file,
            insert_width=400, page_width=1200
          )
iplot(mp)
