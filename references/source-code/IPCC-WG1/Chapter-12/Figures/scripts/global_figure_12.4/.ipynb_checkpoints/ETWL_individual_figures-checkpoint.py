# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/scripts/global_figure_12.4/.ipynb_checkpoints/ETWL_individual_figures-checkpoint.ipynb

# %% cell 1
import os, numpy
from IPython.display import Image

# %% cell 2
CWD = os.getcwd()
outdatadir = CWD + '/../../data/Figure_12.4/ETWL'
outfigdir = CWD + '/../../figs/global_figure_12.4'

# %% cell 3
plot_script = CWD + '/../../scripts/global_figure_12.4/ETWL_plot.py'

# %% cell 5
rcp = 'RCP85'
horizon = 2050
baseline = outdatadir+'/globalTWL_baseline.nc'
future = outdatadir+'/globalTWL_'+rcp+'.nc'
title = '"'+str(horizon)+', RCP8.5"'
label = '"(p)"'
trim_figure_base = outfigdir+'/panel_q_ESL_'+str(horizon)+'_'+rcp+'-final.'

figformat='pdf'
trim_figure = trim_figure_base + figformat
cmd = 'rm -f '+trim_figure+' ; python '+plot_script+' '+baseline+' '+future+' '+str(horizon)+' '+rcp+' '+title+' '+label+' '+trim_figure+' '+figformat
print(cmd)
os.system(cmd)


figformat='png'
trim_figure = trim_figure_base + figformat
cmd = 'rm -f '+trim_figure+' ; python '+plot_script+' '+baseline+' '+future+' '+str(horizon)+' '+rcp+' '+title+' '+label+' '+trim_figure+' '+figformat
print(cmd)
os.system(cmd)

Image(trim_figure)

# %% cell 7
Image(outfigdir+'/ESL_colorbar.png')

# %% cell 10
rcp = 'RCP85'
horizon = 2100
baseline = outdatadir+'/globalTWL_baseline.nc'
future = outdatadir+'/globalTWL_'+rcp+'.nc'
title = '"'+str(horizon)+', RCP8.5"'
label = '"(q)"'
trim_figure_base = outfigdir+'/panel_r_ESL_'+str(horizon)+'_'+rcp+'-final.'

figformat='pdf'
trim_figure = trim_figure_base + figformat
cmd = 'rm -f '+trim_figure+' ; python '+plot_script+' '+baseline+' '+future+' '+str(horizon)+' '+rcp+' '+title+' '+label+' '+trim_figure+' '+figformat
print(cmd)
os.system(cmd)


figformat='png'
trim_figure = trim_figure_base + figformat
cmd = 'rm -f '+trim_figure+' ; python '+plot_script+' '+baseline+' '+future+' '+str(horizon)+' '+rcp+' '+title+' '+label+' '+trim_figure+' '+figformat
print(cmd)
os.system(cmd)


Image(trim_figure)

# %% cell 12
rcp = 'RCP45'
horizon = 2100
baseline = outdatadir+'/globalTWL_baseline.nc'
future = outdatadir+'/globalTWL_'+rcp+'.nc'
title = '"'+str(horizon)+', RCP4.5"'
label = '"(r)"'
trim_figure_base = outfigdir+'/panel_p_ESL_'+str(horizon)+'_'+rcp+'-final.'

figformat='pdf'
trim_figure = trim_figure_base + figformat
cmd = 'rm -f '+trim_figure+' ; python '+plot_script+' '+baseline+' '+future+' '+str(horizon)+' '+rcp+' '+title+' '+label+' '+trim_figure+' '+figformat
print(cmd)
os.system(cmd)


figformat='png'
trim_figure = trim_figure_base + figformat
cmd = 'rm -f '+trim_figure+' ; python '+plot_script+' '+baseline+' '+future+' '+str(horizon)+' '+rcp+' '+title+' '+label+' '+trim_figure+' '+figformat
print(cmd)
os.system(cmd)

Image(trim_figure)
