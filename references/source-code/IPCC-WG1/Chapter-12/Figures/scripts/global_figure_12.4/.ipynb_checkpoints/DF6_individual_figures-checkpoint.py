# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/global_figure_12.4/.ipynb_checkpoints/DF6_individual_figures-checkpoint.ipynb

# %% cell 4
import os, glob
import xarray as xr
from IPython.display import Image
from PIL import Image as PILImage

# %% cell 5
CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/DF6'
outfigdir = CWD + '/../../figs/global_figure_12.4'

root_inputdatadir = '/data/jservon/IPCC'

# %% cell 8
# -- Function to split a multi-member file in individual files
# -- Uses Xarray
def split_ensemble_file(ensemble_file, output_pattern, variable='spell'):
    if not os.path.isdir(os.path.dirname(output_pattern)):
        os.makedirs(os.path.dirname(output_pattern))
    import xarray as xr
    dat = xr.open_dataset(ensemble_file, decode_times=False)[variable]
    i = 0
    for member in dat.time:
        print i
        outfilename = output_pattern+'model'+str(i)+'.nc'
        if not os.path.isfile(outfilename):
            print 'Save '+outfilename
            member_dat = dat[i,:,:]
            wfile = outfilename.replace('.nc','tmp.nc')    
            member_dat.to_netcdf(wfile)
            cmd = 'cdo -b 32 setmissval,1e+20 -copy '+wfile+' '+outfilename+' ; ncrename -v spell,DF6 '+outfilename+' ; rm -f '+wfile
            print cmd
            cmd2 = 'ncatted -O -a coordinates,DF6,o,c,"lat lon" -a units,DF6,o,c,"Droughts" -a long_name,DF6,o,c,"Number of droughts per decade (DF6 index)" '+outfilename
            print cmd2
            os.system(cmd)
            os.system(cmd2)
        else:
            print outfilename+' already exists'
        i = i + 1

# %% cell 9
variable='DF6'
CMIP = 'CMIP6'

# %% cell 10
# -- Compute the annual sums
exp_list = [
    dict(experiment='ssp585',
         clim_period = 'hist'),
    dict(experiment='ssp585',
         clim_period = 'farfut'),
    dict(experiment='ssp585',
         clim_period='midfut'),
    dict(experiment='ssp126',
         clim_period = 'farfut'),
    dict(experiment='ssp126',
         clim_period = 'hist'),
    dict(experiment='ssp585',
         clim_period = 'farch'),
    dict(experiment='ssp585',
         clim_period='midch'),
    dict(experiment='ssp126',
         clim_period = 'farch'),
]

for exp_dict in exp_list:
    clim_period = exp_dict['clim_period']
    experiment = exp_dict['experiment']
    wfile = '/data/jservon/IPCC/DF/CMIP6/CMIP6_'+experiment+'-DF6-'+clim_period+'.nc'
    output_pattern = '/data/jservon/IPCC/DF/individual_models/CMIP6/CMIP6_'+experiment+'_DF6_'+clim_period+'_'
    split_ensemble_file(wfile, output_pattern)

# %% cell 13
from climaf.api import *

# %% cell 15
variable='DF6'
CMIP = 'CMIP6'
pattern = root_inputdatadir+'/DF/individual_models/'+CMIP+'/'+CMIP+'_${experiment}_${variable}_${clim_period}_${member}.nc'
cproject('DF6_individual_models_cmip6_ch12','experiment','clim_period','member',('variable',variable),('period','fx'), ensemble=['member'], separator='%')
dataloc(project='DF6_individual_models_cmip6_ch12', url=pattern)

# %% cell 17
exp_list = [
    dict(experiment='ssp585',
         clim_period = 'farch'),
    dict(experiment='ssp585',
         clim_period='midch'),
    dict(experiment='ssp126',
         clim_period = 'farch'),
]


# -- Loop on the scenarios
ens_diff = dict()
for exp in exp_list:
    #
    # -- Experiment and period
    experiment = exp['experiment']
    clim_period = exp['clim_period']
       
    # -- Changes = Scenario minus baselines
    req_exp = ds(project='DF6_individual_models_cmip6_ch12',
                 experiment = experiment,
                 clim_period = clim_period,
                 member = '*'
                )
    diff_exp_baseline = req_exp.explore('ensemble')
    ens_diff[experiment+'_'+clim_period] = diff_exp_baseline

# %% cell 18
pp_colorbar = dict(proj   = 'Robinson',
                   colors = '-3.5 -2.5 -2 -1.5 -1 -0.25 0.25 1 1.5 2 2.5 3.5',
                   color  = 'dfpalette',
                   mpCenterLonF = 0,
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString=''
                  )
pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|lbBoxEndCapStyle=TriangleBothEnds|mpGridAndLimbOn=True|mpGridLineColor=-1')
)

# %% cell 19
crm(pattern='dfpalette')

# %% cell 20
# -- Plot the individual models
wfuture = 'ssp585_farch'
iplot_members(ens_diff[wfuture], plot_script=plot_ipcc, N=1, **pp)

# %% cell 21
iplot_members(ens_diff[wfuture], plot_script=plot_ipcc, N=2, **pp)

# %% cell 22
iplot_members(ens_diff[wfuture], plot_script=plot_ipcc, N=3, **pp)

# %% cell 25
perc_agreement = '80'

# -- Model agreement
# ------------------------------------------------
model_agreement_dict = dict()
for exp in exp_list:
    # -- Experiment and period
    experiment = exp['experiment']
    period = exp['clim_period']
    wfuture = experiment+'_'+clim_period

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
    if wfuture=='ssp126_farch':
        panel = 'panel_g'
    if wfuture=='ssp585_midch':
        panel = 'panel_h'
    if wfuture=='ssp585_farch':
        panel = 'panel_i'
    mask_agreement_name = outdatadir + '/mask_'+perc_agreement+'perc-agreement_DF6_'+panel+'_'+wfuture+'_minus_baseline.nc'
    cfile(model_agreement_dict[wfuture], target=mask_agreement_name)
    cmd = 'ncatted -O -a comment,global,o,c,"This file is used for the hatching of '+panel+' of figure 12.4 - Chapter 12" '+mask_agreement_name
    os.system(cmd)
    

# -- Ensemble medians
# ------------------------------------------------
# -- Panel g
wfuture = 'ssp126_farch'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/DF6_panel_g_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel g of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel h
wfuture = 'ssp585_midch'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/DF6_panel_h_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel h of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# -- Panel i
wfuture = 'ssp585_farch'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
ensmedian_filename = outdatadir + '/DF6_panel_i_'+wfuture+'_minus_baseline.nc'
cmd = 'ncatted -O -a comment,global,o,c,"This file is used for panel i of figure 12.4 - Chapter 12" '+ensmedian_filename
cfile(ensmedian_field, target=ensmedian_filename)
os.system(cmd)

# %% cell 29
from climaf.api import *
import os
from IPython.display import Image
from PIL import Image as PILImage

CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/DF6'
outfigdir = CWD + '/../../figs/global_figure_12.4'

# %% cell 31
pp_colorbar = dict(proj   = 'Robinson',
                   colors = '-3.5 -2.5 -2 -1.5 -1 -0.25 0.25 1 1.5 2 2.5 3.5',
                   color  = 'dfpalette',
                   mpCenterLonF = 0,
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString=''
                  )
pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|lbBoxEndCapStyle=TriangleBothEnds|mpGridAndLimbOn=True|mpGridLineColor=-1',
         tiMainFontHeightF = 0.032,
         gsnStringFontHeightF = 0.03)
)

# %% cell 33
# -- variable
variable = 'DF6'

# -- Percentage of model agreement (hatching)
perc_agreement = '80'

# -- Panel g
# --------------------------------------------------
wfuture = 'ssp126_farch'
ensmedian_filename = outdatadir + '/DF6_panel_g_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable='DF6')
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_DF6_panel_g_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable='DF6')
# -- Save in png
panel_g = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # droughts',
                    title = '2081-2100, SSP1-2.6',
                    **pp
                    )
cdrop(panel_g)
cdrop(panel_h)
cdrop(panel_i)
cfile(panel_g, target = outfigdir + '/panel_g_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_g_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # droughts',
                        title = '2081-2100, SSP1-2.6',
                        format='pdf',
                        **pp
                        )
cdrop(panel_g_pdf)
cdrop(panel_h_pdf)
cdrop(panel_i_pdf)
cfile(cpdfcrop(panel_g_pdf), target = outfigdir + '/panel_g_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')


# -- Panel h
# --------------------------------------------------
wfuture = 'ssp585_midch'
ensmedian_filename = outdatadir + '/DF6_panel_h_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable='DF6')
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_DF6_panel_h_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable='DF6')
# -- Save in png
panel_h = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # droughts',
                    title = '2041-2060, SSP5-8.5',
                    **pp
                    )
cfile(panel_h, target = outfigdir + '/panel_h_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_h_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # droughts',
                        title = '2041-2060, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_h_pdf), target = outfigdir + '/panel_h_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')

# -- Panel i
# --------------------------------------------------
wfuture = 'ssp585_farch'
ensmedian_filename = outdatadir + '/DF6_panel_i_'+wfuture+'_minus_baseline.nc'
ensmedian_field = fds(ensmedian_filename, period='fx', variable='DF6')
model_agreement_filename = outdatadir + '/mask_'+perc_agreement+'perc-agreement_DF6_panel_i_'+wfuture+'_minus_baseline.nc'
model_agreement_field = fds(model_agreement_filename, period='fx', variable='DF6')
# -- Save in png
panel_i = plot_ipcc(ensmedian_field,
                    model_agreement_field,
                    shade_above = -0.99999,
                    shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                    gsnCenterString = 'Change in # droughts',
                    title = '2081-2100, SSP5-8.5',
                    **pp
                    )
cfile(panel_i, target = outfigdir + '/panel_i_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.png')
# -- Save in pdf
panel_i_pdf = plot_ipcc(ensmedian_field,
                        model_agreement_field,
                        shade_above = -0.99999,
                        shading_options='gsnShadeHigh=3|gsnShadeFillScaleF=1.0',
                        gsnCenterString = 'Change in # droughts',
                        title = '2081-2100, SSP5-8.5',
                        format='pdf',
                        **pp
                        )
cfile(cpdfcrop(panel_i_pdf), target = outfigdir + '/panel_i_'+ variable+'_'+wfuture+'_'+perc_agreement+'perc-agreement.pdf')

# %% cell 35
# -- Colorbar
def extract_labelbar(figure_file,labelbar_file) :
    #import PIL
    im = PILImage.open(figure_file)
    #box=(left, upper, right, lower).
    im_crop = im.crop((55, 564, 930, 642))
    im_crop.save(labelbar_file, quality=95)

# -- Base plot for the colorbar
wfuture = 'ssp585_farch'

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

# %% cell 37
mp = cpage(fig_lines=[[panel_g,panel_h,panel_i]],
            insert=colorbar_file,
            insert_width=400, page_width=1200
          )
iplot(mp)
