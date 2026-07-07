# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7_Fig04/270_chapter7_fig7.4.ipynb

# %% cell 2
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.gridspec as gridspec
import pandas as pd
from matplotlib import rc
from netCDF4 import Dataset
import scipy.stats as st
import warnings
from fair.forcing.ghg import meinshausen, etminan

from ar6.constants import NINETY_TO_ONESIGMA

# %% cell 3
pl.rcParams['figure.figsize'] = (9/2.54, 9/2.54)
pl.rcParams['font.size'] = 9
pl.rcParams['font.family'] = 'Arial'
pl.rcParams['ytick.direction'] = 'out'
pl.rcParams['ytick.minor.visible'] = True
pl.rcParams['ytick.major.right'] = True
pl.rcParams['ytick.right'] = True
pl.rcParams['xtick.bottom'] = False
pl.rcParams['axes.spines.top'] = False
pl.rcParams['axes.spines.bottom'] = False
pl.rcParams['xtick.labelbottom'] = False
pl.rcParams['figure.dpi'] = 150
#pl.rcParams['ytick.major.size'] = 0
#pl.rcParams['xtick.top'] = True

# %% cell 4
expt_names = {
    '10xBC': 'Black\ncarbon',
    '3xCH4': 'Methane',
    '2xCO2': 'Carbon\ndioxide',
    'Solar': 'Solar',
    '5xSO4': 'Sulphate',
    'aer': 'Aerosol',
    '9xCFC12': 'CFC-12',
    '8xCFC11': 'CFC-11',
    '3xN2O': 'Nitrous\noxide',
    'Volcanic': 'Volcanic'
}

# 10 models, 4 kernels, 8 experiments and 7 adjustments
# do adjust[model, kernel, exp]
n_mod = 10; n_ker = 6; n_exp=9

flux = {}
flux_u90 = {}
valid_count = {}

# %% cell 6
indirs = ['../data_input/Smith_et_al_GRL_2018/pdrmip_kernel_ryan_kramer/', 
          '../data_input/Smith_et_al_GRL_2018/pdrmip_kernel_ryan_kramer/', 
          '../data_input/Smith_et_al_GRL_2018/pdrmip_kernel_ryan_kramer/', 
          '../data_input/Smith_et_al_GRL_2018/pdrmip_kernel_ryan_kramer/', 
          '../data_input/Smith_et_al_GRL_2018/pdrmip_kernel_ryan_kramer/', 
          '../data_input/Smith_et_al_GRL_2018/pdrmip_kernel_ECMWF-Oslo_gunnar_myhre/']
models = ['CanESM2', 'ECHAM-HAM', 'GISS-E2-R', 'HadGEM2', 'HadGEM3', 'IPSL-CM5A', 'MIROC-SPRINTARS', 'MPI-ESM', 'NCAR-CESM1-CAM4', 'NCAR-CESM1-CAM5', 'NorESM1']
kernels = ['HadGEM2', 'GFDL', 'BMRC', 'CCSM4', 'CESM', 'Oslo']
vars = ['ERF_SW','IRF_SW','tas_SW','ta_trop_SW','ta_strat_SW','hus_SW','alb_SW','cloud_SW','ERF_LW','IRF_LW','tas_LW','ta_trop_LW','ta_strat_LW','hus_LW','alb_LW','cloud_LW']

flux_data = []

#for var in vars:
#    flux[var] = np.ones((n_mod, n_ker, n_exp)) * np.nan
#    flux_u90[var] = np.ones((n_mod, n_ker, n_exp)) * np.nan
for i_mod,model in enumerate(models):
    for i_ker,kernel in enumerate(kernels):
        nc = Dataset(indirs[i_ker]+'%s_K%s_LWSW_TOA.nc' % (model, kernel))
#            flux[var][i_mod,i_ker,:5]    = nc.variables[var][:]
        for var in ['ERF', 'IRF', 'tas', 'ta_trop', 'ta_strat', 'hus', 'alb', 'cloud']:
            aco2, ach4, asol, abc, aso4 = nc.variables[var + '_SW'][:] + nc.variables[var + '_LW'][:]
            flux_data.append([var, model, kernel, aco2, ach4, asol, abc, aso4])
        nc.close()
            
## replace MPI 10xBC with ECHAM.
#for var in vars:
#    for i_ker,kernel in enumerate(kernels[:]):
#        nc = Dataset(indirs[i_ker]+'ECHAM-HAM_K%s_LWSW_TOA.nc' % kernel)
#        flux[var][6,i_ker,3]    = nc.variables[var][3]
#        nc.close()

# %% cell 7
adjustments_smith18_df = pd.DataFrame(flux_data, columns=['variable','model','kernel','2xCO2','3xCH4','Solar','10xBC','5xSO4'])
pd.options.display.max_rows = 999

# oslo is zero for missing data instead of NaN
for expt in ['2xCO2','3xCH4','5xSO4','Solar']:
    adjustments_smith18_df.loc[(adjustments_smith18_df['model']=='ECHAM-HAM') & (adjustments_smith18_df['kernel']=='Oslo'), expt] = np.nan

for expt in ['10xBC', '5xSO4']:
    adjustments_smith18_df.loc[(adjustments_smith18_df['model']=='MPI-ESM') & (adjustments_smith18_df['kernel']=='Oslo'), expt] = np.nan

for expt in ['2xCO2','3xCH4','10xBC','5xSO4','Solar']:
    adjustments_smith18_df.loc[(adjustments_smith18_df['model']=='NCAR-CESM1-CAM5') & (adjustments_smith18_df['variable']=='cloud') & (adjustments_smith18_df['kernel']=='Oslo'), expt] = np.nan
    
# For all kernels except Oslo, remove SO4 clouds and IRF for all except CAM4 as they are not correct (in GISS)
# or contain some component of IRF (in SPRINTARS or HadGEM2)
for model in ['CanESM2', 'ECHAM-HAM', 'GISS-E2-R', 'HadGEM2', 'HadGEM3', 'IPSL-CM5A', 'MIROC-SPRINTARS', 'MPI-ESM', 'NCAR-CESM1-CAM5', 'NorESM1']:
    for kernel in ['HadGEM2', 'GFDL', 'BMRC', 'CCSM4', 'CESM']:
        adjustments_smith18_df.loc[
            (adjustments_smith18_df['model']==model) & (adjustments_smith18_df['variable']=='cloud') & (adjustments_smith18_df['kernel']==kernel),
        '5xSO4'] = np.nan        

# # make solar 22% of IRF from Gray et al 2009
for model in ['CanESM2', 'ECHAM-HAM', 'GISS-E2-R', 'HadGEM2', 'HadGEM3', 'IPSL-CM5A', 'MIROC-SPRINTARS', 'MPI-ESM', 'NCAR-CESM1-CAM4', 'NCAR-CESM1-CAM5', 'NorESM1']:
    for kernel in ['HadGEM2', 'GFDL', 'BMRC', 'CCSM4', 'CESM', 'Oslo']:
#         print(adjustments_smith18_df.loc[
#             (adjustments_smith18_df['model']==model) & (adjustments_smith18_df['variable']=='IRF') & (adjustments_smith18_df['kernel']==kernel),
#         'Solar'].values[0] * 0.22)
        adjustments_smith18_df.loc[
            (adjustments_smith18_df['model']==model) & (adjustments_smith18_df['variable']=='ta_strat') & (adjustments_smith18_df['kernel']==kernel),
        'Solar'] = (adjustments_smith18_df.loc[
            (adjustments_smith18_df['model']==model) & (adjustments_smith18_df['variable']=='IRF') & (adjustments_smith18_df['kernel']==kernel),
        'Solar'].values[0] * -0.22)

        
# For AR6, remove methane where SW absorption not included.
for model in models:
    if model not in ['CanESM2', 'MIROC-SPRINTARS', 'MPI-ESM', 'NCAR-CESM1-CAM5']:
        adjustments_smith18_df.loc[adjustments_smith18_df['model']==model, '3xCH4'] = np.nan

adjustments_smith18_df

# %% cell 8
flux_data = []
for model in models:
    for var in ['ERF', 'IRF', 'tas', 'ta_trop', 'ta_strat', 'hus', 'alb', 'cloud']:
        aco2, ach4, asol, abc, aso4 = adjustments_smith18_df.loc[(adjustments_smith18_df['model']==model) & (adjustments_smith18_df['variable']==var)].mean()
        flux_data.append([var, model, aco2, ach4, asol, abc, aso4])

smith18_new_df = pd.DataFrame(flux_data, columns=['variable','model','2xCO2','3xCH4','Solar','10xBC','5xSO4'])
smith18_new_df.set_index(['variable','model'], inplace=True)
smith18_new_df

# %% cell 10
adjustments_smith20_co2_df = pd.read_csv('../data_input/Smith_et_al_ACP_2020/ERF_IRF_RA_4xCO2.csv')
adjustments_smith20_co2_df

# %% cell 11
adjustments_smith20_aer_df = pd.read_csv('../data_input/Smith_et_al_ACP_2020/ERF_IRF_RA_aer.csv')
adjustments_smith20_aer_df

# %% cell 13
concentrations = pd.read_csv('../data_input_large/rcmip-concentrations-annual-means-v5-1-0.csv')
pi_conc = {}
for species in ['CO2','CH4','N2O']:
    pi_conc[species] = concentrations.loc[
        (concentrations['Variable']=='Atmospheric Concentrations|%s' % species)&
        (concentrations['Region']=='World')&
        (concentrations['Scenario']=='historical'),
    '1850'].values[0]

# %% cell 14
m4x = meinshausen(np.array([4*pi_conc['CO2'], pi_conc['CH4'], pi_conc['N2O']]), Cpi=np.array([pi_conc['CO2'], pi_conc['CH4'], pi_conc['N2O']]), scale_F2x=False)
m2x = meinshausen(np.array([2*pi_conc['CO2'], pi_conc['CH4'], pi_conc['N2O']]), Cpi=np.array([pi_conc['CO2'], pi_conc['CH4'], pi_conc['N2O']]), scale_F2x=False)
detune = m2x[0]/m4x[0]
print(detune)

# %% cell 15
mapping = {
    'ERF' : 'ERF',
    'IRF' : 'IRF',
    'ts' : 'tas',
    'tatr' : 'ta_trop',
    'tast' : 'ta_strat',
    'hus': 'hus',
    'alb': 'alb',
    'cl': 'cloud'
}

flux_data = []

for model in adjustments_smith20_co2_df.Model.unique():
    for var in ['ERF', 'ts', 'tatr', 'tast', 'hus', 'alb', 'cl']:
        model_results = adjustments_smith20_co2_df.loc[adjustments_smith20_co2_df['Model']==model, var].mean() * detune
        flux_data.append([mapping[var], model, model_results])

# %% cell 16
smith20_co2_new_df = pd.DataFrame(flux_data, columns=['variable', 'model', '2xCO2_sm20'])
smith20_co2_new_df.set_index(['variable','model'], inplace=True)
smith20_co2_new_df

# %% cell 17
flux_data = []

for model in adjustments_smith20_aer_df.Model.unique():
    for var in ['ERF', 'IRF', 'ts', 'tatr', 'tast', 'hus', 'alb', 'cl']:
        model_results = adjustments_smith20_aer_df.loc[adjustments_smith20_aer_df['Model']==model, var].mean()
        flux_data.append([mapping[var], model, model_results])

smith20_aer_new_df = pd.DataFrame(flux_data, columns=['variable', 'model', 'aer'])
smith20_aer_new_df.set_index(['variable','model'], inplace=True)
smith20_aer_new_df

# %% cell 19
df_hod = pd.read_csv('../data_input/Hodnebrog_et_al_2020_npj/Hodnebrog_et_al_2020_adjustments.csv')
display(df_hod)

# %% cell 20
df_hod.Model.unique()

# %% cell 21
# rearrange to get in the same format
flux_data = []
standard_name = ['8xCFC11', '9xCFC12', '3xN2O']

mapping = {
    'ERF' : 'ERF',
    'IRF' : 'IRF',
    'Ts' : 'tas',
    'Ttrop' : 'ta_trop',
    'Tstrat' : 'ta_strat',
    'WV': 'hus',
    'alpha': 'alb',
    'Clouds': 'cloud'
}

#for ie, expt in enumerate(['CFC11x8', 'CFC12x9', 'N2Ox3']):
for model in models:
    for var in ['ERF', 'IRF', 'Ts', 'Ttrop', 'Tstrat', 'WV', 'alpha', 'Clouds']:
        try:
            cfc11 = df_hod.loc[(df_hod['Model']==model) & (df_hod['Experiment']=='CFC11x8'), var].values[0]
        except:
            cfc11 = np.nan
        try:
            cfc12 = df_hod.loc[(df_hod['Model']==model) & (df_hod['Experiment']=='CFC12x9'), var].values[0]
        except:
            cfc12 = np.nan
        try:
            n2o = df_hod.loc[(df_hod['Model']==model) & (df_hod['Experiment']=='N2Ox3'), var].values[0]
        except:
            n2o = np.nan

        flux_data.append([mapping[var], model, cfc11, cfc12, n2o])

hod_new_df = pd.DataFrame(flux_data, columns=['variable', 'model', '8xCFC11', '9xCFC12', '3xN2O'])
hod_new_df.set_index(['variable','model'], inplace=True)

# %% cell 23
df_lauren = pd.read_csv('../data_input/Marshall_et_al_2020_GRL/albedo.csv')
df_lauren

# %% cell 24
volcanic_adj = {}
for adj_type in ['irf', 'erf', 'ts', 'albedo', 'cl_lw', 'cl_sw', 'hus_lw_stratosphere', 'hus_sw_stratosphere', 'hus_lw_troposphere', 'hus_sw_troposphere', 'ta_stratosphere', 'ta_troposphere']:
    print(adj_type)
    df_lauren = pd.read_csv('../data_input/Marshall_et_al_2020_GRL/%s.csv' % adj_type)
    jul = df_lauren.loc[7:30,'xncna':'xncop'].mean()
    jan = df_lauren.loc[1:24,'xnqha':'xnqip'].mean()
    volcanic_adj[adj_type] = np.mean((jul, jan))

# %% cell 25
flux_data = []
flux_data.append(['ERF', 'HadGEM3', volcanic_adj['erf']])
flux_data.append(['IRF', 'HadGEM3', volcanic_adj['irf']])
flux_data.append(['tas', 'HadGEM3', volcanic_adj['ts']])
flux_data.append(['alb', 'HadGEM3', volcanic_adj['albedo']])
flux_data.append(['cloud', 'HadGEM3', volcanic_adj['cl_lw'] + volcanic_adj['cl_sw']])
flux_data.append(['hus', 'HadGEM3', volcanic_adj['hus_lw_stratosphere'] + volcanic_adj['hus_lw_troposphere'] + volcanic_adj['hus_sw_stratosphere'] + volcanic_adj['hus_sw_troposphere']])
flux_data.append(['ta_trop', 'HadGEM3', volcanic_adj['ta_troposphere']])
flux_data.append(['ta_strat', 'HadGEM3', volcanic_adj['ta_stratosphere']])


volcanic_df = pd.DataFrame(flux_data, columns=['variable','model','Volcanic'])
volcanic_df.set_index(['variable','model'], inplace=True)

# %% cell 26
volcanic_adj

# %% cell 28
smith20_co2_new_df

# %% cell 29
adjustments_df = (
    pd.concat([smith18_new_df, smith20_aer_new_df, hod_new_df, volcanic_df], axis=1)
)
#adjustments_df.loc[:,'2xCO2'] = adjustments_df['2xCO2'].fillna(adjustments_df['2xCO2_sm20'])
#adjustments_df.drop(columns=['2xCO2_sm20'], inplace=True)
#.fillna(df['_id'])
#adjustments_df = pd.merge(adjustments_df, smith20_co2_new_df, how='outer', on='2xCO2', left_index=True, right_index=True)
adjustments_df.to_csv('../data_output/fig7.4.csv')
adjustments_df

# %% cell 31
# adjusted ERF
ERF_adj = (adjustments_df.loc['ERF'] - adjustments_df.loc['tas'])

# %% cell 32
# SARF
SARF = (adjustments_df.loc['ERF'] - adjustments_df.loc['tas'] - adjustments_df.loc['ta_trop'] - adjustments_df.loc['hus'] - adjustments_df.loc['alb'] - adjustments_df.loc['cloud'])

# %% cell 33
adjustments_df.loc['ta_strat']/adjustments_df.loc['IRF']

# %% cell 34
# IRF 
# For GHGs, overwrite the IRF values from Ryan
for expt in ['2xCO2','3xCH4','10xBC','5xSO4','8xCFC11','9xCFC12','3xN2O']:
    adjustments_df.loc['IRF',expt] = (adjustments_df.loc['ERF',expt] - adjustments_df.loc['tas',expt] - adjustments_df.loc['ta_trop',expt] - adjustments_df.loc['ta_strat',expt] - adjustments_df.loc['hus',expt] - adjustments_df.loc['alb',expt] - adjustments_df.loc['cloud',expt])

# %% cell 35
IRF = adjustments_df.loc['IRF']
tas = adjustments_df.loc['tas']
ta_trop = adjustments_df.loc['ta_trop']
ta_strat = adjustments_df.loc['ta_strat']
hus = adjustments_df.loc['hus']
cloud = adjustments_df.loc['cloud']
alb = adjustments_df.loc['alb']
RA = ta_trop + ta_strat + hus + cloud + alb
total_trop = ta_trop + hus + cloud + alb

# %% cell 36
(total_trop/SARF).mean()['2xCO2']

# %% cell 37
(adjustments_df.loc['alb']/(adjustments_df.loc['ERF'] - adjustments_df.loc['tas'])).mean()['3xCH4']

# %% cell 38
fig, ax1 = pl.subplots()

colors = ['#cc4049','#ed8037','#ecd151','#369ce8','#24937e','#b0b0b0','black']
labels = ['Surface temperature','Tropospheric temperature','Stratospheric temperature','Water vapour','Albedo','Clouds','Total']
for ie, expt in enumerate(['2xCO2', '3xCH4', '3xN2O', '9xCFC12', 'aer', 'Solar', 'Volcanic']):
    if expt in ['2xCO2', '3xCH4', '3xN2O', '9xCFC12']:
        ax1.bar(0.14+ie, 100*(tas/SARF).mean()[expt], 0.12, color="None", edgecolor=colors[0], lw=1, zorder=4)
        ax1.bar(0.26+ie, 100*(ta_trop/SARF).mean()[expt], 0.12, color=colors[1], zorder=3)
        ax1.bar(0.38+ie, 100*(ta_strat/SARF).mean()[expt], 0.12, color="None", edgecolor=colors[2], zorder=4)
        ax1.bar(0.50+ie, 100*(hus/SARF).mean()[expt], 0.12, color=colors[3], zorder=3)
        ax1.bar(0.62+ie, 100*(alb/SARF).mean()[expt], 0.12, color=colors[4], zorder=3)
        ax1.bar(0.74+ie, 100*(cloud/SARF).mean()[expt], 0.12, color=colors[5], zorder=3)
        ax1.bar(0.86+ie, 100*(total_trop/SARF).mean()[expt], 0.12, color=colors[6], zorder=3)
    elif expt in ['aer', 'Solar', 'Volcanic']:
        ax1.bar(0.14+ie, 100*(tas/IRF).mean()[expt], 0.12, color="None", edgecolor=colors[0], lw=1, zorder=4, label=labels[0] if ie==6 else '')
        ax1.bar(0.26+ie, 100*(ta_trop/IRF).mean()[expt], 0.12, color=colors[1], zorder=3, label=labels[1] if ie==6 else '')
        ax1.bar(0.38+ie, 100*(ta_strat/IRF).mean()[expt], 0.12, color=colors[2], zorder=3, label=labels[2] if ie==6 else '')
        ax1.bar(0.50+ie, 100*(hus/IRF).mean()[expt], 0.12, color=colors[3], zorder=3, label=labels[3] if ie==6 else '')
        ax1.bar(0.62+ie, 100*(alb/IRF).mean()[expt], 0.12, color=colors[4], zorder=3, label=labels[4] if ie==6 else '')
        ax1.bar(0.74+ie, 100*(cloud/IRF).mean()[expt], 0.12, color=colors[5], zorder=3, label=labels[5] if ie==6 else '')
        ax1.bar(0.86+ie, 100*(RA/IRF).mean()[expt], 0.12, color=colors[6], zorder=3, label=labels[6] if ie==6 else '')
    if expt in ['Volcanic', '5xSO4', 'aer']:
        textcolor='#304fbf'
    else:
        textcolor='#cc4049'
    ax1.text(0.5+ie, 44, expt_names[expt], ha='center', va='top', fontsize=7, color=textcolor)

ax1.text(2, -27, 'Greenhouse gases', size=11, va='bottom', ha='center')
#ax1.text(6, -118, 'Aerosols', size=11, va='bottom', ha='center')
ax1.text(6, 30, 'Natural', size=11, va='bottom', ha='center')

ax1.set_ylabel('Percent of SARF or IRF (%)')

ax1.axhline(0, color='k', lw=1, zorder=4)

for x in range(1,8):
    ax1.axvline(x,lw=0.2,color='#d0d0d0')

mn,mx = ax1.get_ylim()
backfill = [0,4,4,5,5,7]
fillind  = [1,1,0,0,1,1]
ax1.fill_between(backfill, -120, 100, where=fillind, color='#f0f0f0', zorder=0.6)
ax1.legend(loc='lower center', framealpha=1, fontsize=7, ncol=2, frameon=True)#, bbox_to_anchor=[0.5,0.02])
ax1.set_ylim(-50,45)
ax1.set_xlim(0,7)
#ax1.grid(axis='y', zorder=-11, lw=0.5)

ax1.set_title('Top-of-atmosphere radiative adjustments')
ax1.text(2.25, 28, '"Total" bars for greenhouse\ngases represent\ntropospheric totals', size=7, ha='center', va='center')


fig.tight_layout()

pl.savefig('../figures/fig7.4.png', dpi=300)
pl.savefig('../figures/fig7.4.pdf')

# %% cell 39
100*(total_trop/SARF).mean()['2xCO2']

# %% cell 40
100*(total_trop/SARF).mean()['3xCH4']

# %% cell 41
100*(total_trop/SARF).mean()['3xN2O']

# %% cell 42
100*(total_trop/SARF).mean()['9xCFC12']

# %% cell 43
100*(total_trop/SARF).mean()['8xCFC11']

# %% cell 44
ta_strat/IRF
