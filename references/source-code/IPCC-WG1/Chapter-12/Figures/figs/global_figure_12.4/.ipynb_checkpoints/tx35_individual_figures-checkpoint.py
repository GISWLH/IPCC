# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/figs/global_figure_12.4/.ipynb_checkpoints/tx35_individual_figures-checkpoint.ipynb

# %% cell 3
# -- Preparing the files

# -- Select the periods by scenario
# -- Compute annual sums
# -- Split the annual files
# -- Using CliMAF:
# --   - compute the individual differences
# --   - compute the ensemble statistics
# --   - start the plot of the ensemble median
# --   - code model agreement

# %% cell 4
import os, glob
import xarray as xr
from IPython.display import Image
import PIL

# %% cell 6
# WBGT = /data/ciles/IPCC/FGD/WBGT_FGD/CMIP6_share/
# SPI = /data/ciles/IPCC/SOD/SPI/CMIP6/CMIP6Amon-DF6-ALLfar-mask.nc

# %% cell 7
!ls /data/ciles/IPCC/FGD/WBGT_FGD/CMIP6_share/*/

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
variable='tx35'

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

for exp_dict in exp_list:
    years = exp_dict['years']
    experiment = exp_dict['experiment']
    for year in years:
        wfile = '/data/jservon/IPCC/'+variable+'/CMIP6_'+experiment+'_'+variable+'_'+str(year)+'.nc4'
        output_pattern = '/data/jservon/IPCC/'+variable+'/individual_models/CMIP6_'+experiment+'_'+variable+'_'+str(year)+'_'
        split_ensemble_file(wfile, output_pattern, variable)
#

# %% cell 12
from climaf.api import *

# %% cell 14
pattern = '/data/jservon/IPCC/${variable}/individual_models/CMIP6_${experiment}_${variable}_${period}_${member}.nc'
cproject('tx_individual_models_cmip6_ch12','experiment','period','member',('variable','tx35'), ensemble=['member'], separator='%')
dataloc(project='tx_individual_models_cmip6_ch12', url=pattern)

# %% cell 16
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
    ens_diff[experiment+'_'+period] = diff_exp_baseline

# %% cell 17
pp_colorbar = dict(proj   = 'Robinson',
                   colors = '-250 -150 -80 -40 -15 -5 5 15 40 80 150 250',
                   color  = 'temp_diff_18lev',#NCV_blu_red',
                   mpCenterLonF = 0,
                   contours = 1,
                   focus = 'land',
                   tiMainFontHeightF=0.03,
                   gsnStringFontHeightF=0.02,
                   gsnRightString='', gsnLeftString=''
                  )

# %% cell 19
pp = pp_colorbar.copy()
pp.update(
    dict(options='gsnAddCyclic=True|lbLabelBarOn=False|lbBoxEndCapStyle=TriangleBothEnds')
)

# %% cell 20
# -- Plot the individual models
wfuture = 'ssp585_2081-2100'
iplot_members(ens_diff[wfuture], N=1, **pp)

# %% cell 21
iplot_members(ens_diff[wfuture], N=2, **pp)

# %% cell 22
# -- Colorbar
def extract_labelbar(figure_file,labelbar_file) :
    import PIL
    im = PIL.Image.open(figure_file)
    #box=(left, upper, right, lower).
    im_crop = im.crop((55, 550, 930, 642))
    im_crop.save(labelbar_file, quality=95)

# -- Base plot for the colorbar
plot_4colorbar = plot(ens_diff[wfuture][ens_diff[wfuture].keys()[0]],
                      options='lbOrientation=horizontal|lbLabelFontHeightF=0.015|lbBoxEndCapStyle=TriangleBothEnds',
                      **pp_colorbar)

# -- color bar file
colorbar_file = '/home/jservon/Chapter12_IPCC/figs/global_figure_1/'+variable+'_colorbar.png'

# -- Extract the colorbar
extract_labelbar(cfile(plot_4colorbar),colorbar_file)

Image(colorbar_file)

# %% cell 24
pp['tiMainFontHeightF'] = 0.025

wfuture = 'ssp585_2041-2060'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
p1 = plot(ensmedian_field,
          title = '(a) Change in # days Tx>35~F34~0~F~C 2041-2060, SSP5-8.5',
          **pp
         )

wfuture = 'ssp585_2081-2100'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
p2 = plot(ensmedian_field,
          title = '(b) 2081-2100, SSP5-8.5',
          **pp
         )

wfuture = 'ssp126_2081-2100'
ensmedian_field = ccdo_ens(ens_diff[wfuture], operator='enspctl,50')
p3 = plot(ensmedian_field,
          title = '(c) 2081-2100, SSP1-2.6',
          **pp
         )

mp = cpage(fig_lines=[[p1,p2,p3]],
            insert=colorbar_file,
            insert_width=400, page_width=1200
          )
iplot(mp)

# %% cell 25
# -- For the three figures, prepare:

# -- Ensemble Median
ensmedian_field
# -- Hatching
hatching_field
# -- Stippling
stippling_field

# %% cell 26
wfuture = 'ssp126_2081-2100'

mask_pos_dict = dict()
mask_neg_dict = dict()

for mem in ens_diff[wfuture]:
    mask_pos_dict[mem] = ccdo(ens_diff[wfuture][mem], operator='gtc,0')
    mask_neg_dict[mem] = ccdo(ens_diff[wfuture][mem], operator='ltc,0')
ens_mask_pos = cens(mask_pos_dict)
ens_mask_neg = cens(mask_neg_dict)

perc_ens_pos = fmul( fdiv( ccdo_ens(ens_mask_pos, operator='enssum'), len(ens_diff[wfuture]) ), 100 )
perc_ens_neg = fmul( fdiv( ccdo_ens(ens_mask_neg, operator='enssum'), len(ens_diff[wfuture]) ), 100 )

mask_inf90_pos = ccdo(perc_ens_pos, operator='ltc,90')
mask_inf90_neg = ccdo(perc_ens_neg, operator='ltc,90')

# %% cell 27
# Trouver un moyen de mettre la mediane commme condition de base

# %% cell 28
iplot( plot(perc_ens_pos, perc_ens_pos, shade_below=90, focus='land',
            proj='Robinson',
            shading_options='gsnShadeLow=3|gsnShadeFillScales=0.3|cnMonoLineThickness=True|cnLineThicknessF=3.0') )

# %% cell 29
len(ens_diff[wfuture])
