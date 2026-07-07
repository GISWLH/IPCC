# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/220_chapter7_fig7.7.ipynb

# %% cell 2
import numpy as np
import scipy.stats as st
import pandas as pd
import matplotlib.pyplot as pl
import os
from matplotlib import gridspec, rc
from matplotlib.lines import Line2D
import matplotlib.patches as mp
from netCDF4 import Dataset
import warnings

from ar6.utils.h5 import *

# %% cell 3
# TODO - sort out figure sizing

pl.rcParams['figure.figsize'] = (18/2.54, 11/2.54)
pl.rcParams['font.size'] = 11
pl.rcParams['font.family'] = 'Arial'
pl.rcParams['xtick.direction'] = 'out'
pl.rcParams['xtick.minor.visible'] = True
pl.rcParams['ytick.major.left'] = True
pl.rcParams['ytick.major.size'] = 0
pl.rcParams['xtick.top'] = True

# %% cell 4
results = load_dict_from_hdf5('../data_output_large/twolayer_AR6-historical.h5')

# %% cell 5
results.keys()

# %% cell 6
results['AR6-historical']['surface_temperature'].shape

# %% cell 7
results['AR6-historical']['surface_temperature'][0].mean()

# %% cell 8
# 1750 values

forcings = ['co2', 'ch4', 'n2o', 'other_wmghg', 'o3', 'h2o_stratospheric',
            'contrails', 'aerosol-radiation_interactions', 'aerosol-cloud_interactions', 
            'bc_on_snow', 'land_use', 'volcanic', 'solar', 'wmghgs', 'aerosol', 'albedo', 'anthro', 'natural']
for forcing in forcings:
    print(forcing, results['remove_%s' % forcing]['surface_temperature'][0,:].mean())

# %% cell 9
pl.plot(results['AR6-historical_climuncert']['surface_temperature']);

# %% cell 10
AR6_forc = {}
AR6_ecsforc = {}
forcings = ['co2', 'ch4', 'n2o', 'other_wmghg', 'o3', 'h2o_stratospheric',
            'contrails', 'aerosol-radiation_interactions', 'aerosol-cloud_interactions', 
            'bc_on_snow', 'land_use', 'volcanic', 'solar', 'wmghgs', 'aerosol', 'albedo', 'anthro', 'natural']

for forcing in forcings:
    AR6_forc[forcing] = np.zeros(5)
    AR6_forc[forcing] = np.percentile(
        (results['AR6-historical']['surface_temperature'][-1,:] - results['AR6-historical']['surface_temperature'][0,:])-
        (results['remove_%s' % forcing]['surface_temperature'][-1,:] - results['remove_%s' % forcing]['surface_temperature'][0,:]), (5,16,50,84,95)
    )
    AR6_ecsforc[forcing] = np.zeros(5)
    AR6_ecsforc[forcing] = np.percentile(
        (results['AR6-historical_climuncert']['surface_temperature'][-1,:] - results['AR6-historical_climuncert']['surface_temperature'][0,:])-
        (results['remove_%s_climuncert' % forcing]['surface_temperature'][-1,:] - results['remove_%s_climuncert' % forcing]['surface_temperature'][0,:]), (5,16,50,84,95)
    )

# create some new aggregated categories
non_co2_ghgs = (
    (
        (results['AR6-historical']['surface_temperature'][-1] - results['AR6-historical']['surface_temperature'][0]) -
        (results['remove_ch4']['surface_temperature'][-1] - results['remove_ch4']['surface_temperature'][0])
    ) +
    (
        (results['AR6-historical']['surface_temperature'][-1] - results['AR6-historical']['surface_temperature'][0]) -
        (results['remove_n2o']['surface_temperature'][-1] - results['remove_n2o']['surface_temperature'][0])
    ) +
    (
        (results['AR6-historical']['surface_temperature'][-1] - results['AR6-historical']['surface_temperature'][0]) -
        (results['remove_other_wmghg']['surface_temperature'][-1] - results['remove_other_wmghg']['surface_temperature'][0])
    )
)
AR6_forc['ch4+n2o+cfc'] = np.percentile(non_co2_ghgs, (5,16,50,84,95))
non_co2_ghgs = (
    (
        (results['AR6-historical_climuncert']['surface_temperature'][-1] - results['AR6-historical_climuncert']['surface_temperature'][0]) -
        (results['remove_ch4_climuncert']['surface_temperature'][-1] - results['remove_ch4_climuncert']['surface_temperature'][0])
    ) +
    (
        (results['AR6-historical_climuncert']['surface_temperature'][-1] - results['AR6-historical_climuncert']['surface_temperature'][0]) -
        (results['remove_n2o_climuncert']['surface_temperature'][-1] - results['remove_n2o_climuncert']['surface_temperature'][0])
    ) +
    (
        (results['AR6-historical_climuncert']['surface_temperature'][-1] - results['AR6-historical_climuncert']['surface_temperature'][0]) -
        (results['remove_other_wmghg_climuncert']['surface_temperature'][-1] - results['remove_other_wmghg_climuncert']['surface_temperature'][0])
    )
)
AR6_ecsforc['ch4+n2o+cfc'] = np.percentile(non_co2_ghgs, (5,16,50,84,95))

AR6_forc['total'] = np.percentile(results['AR6-historical']['surface_temperature'][-1] - results['AR6-historical']['surface_temperature'][0], (5,16,50,84,95))
AR6_ecsforc['total'] = np.percentile(results['AR6-historical_climuncert']['surface_temperature'][-1] - results['AR6-historical_climuncert']['surface_temperature'][0], (5,16,50,84,95))

# %% cell 11
AR6_forc['total'].shape

# %% cell 12
print(AR6_ecsforc['natural'])
print(AR6_ecsforc['anthro'])
print(AR6_ecsforc['total'])

# %% cell 13
fig, ax = pl.subplots()

gs = gridspec.GridSpec(1,2, width_ratios=[5,1])
ax = pl.subplot(gs[0,0])
# errorbar for owmghg is going to be a mess so pre-calculate it

#hot = ['#f03b20','#feb24c','#feeda0']
#hot = ['#de2d26','#fc9274','#fee0d2']
#cool=['#3182bd','#9ecae1']

hot = ['#cc404a','#ed8037','#ecd151']
cool=['#304fbf','#369ce8']

ax.barh(0, AR6_ecsforc['co2'][2], color=hot[0], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['co2'][2], 0.18, xerr=np.array([AR6_forc['co2'][2]-AR6_forc['co2'][0],AR6_forc['co2'][4]-AR6_forc['co2'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['co2'][2], -0.18, xerr=np.array([AR6_ecsforc['co2'][2]-AR6_ecsforc['co2'][0],AR6_ecsforc['co2'][4]-AR6_ecsforc['co2'][2]]).reshape((2,1)), capsize=3, color='k')

ax.barh(-1, AR6_ecsforc['ch4'][2], color=hot[0], lw=1, edgecolor='k')
ax.barh(-1, AR6_ecsforc['n2o'][2], color=hot[1], left=AR6_ecsforc['ch4'][2], lw=1, edgecolor='k')
ax.barh(-1, AR6_ecsforc['other_wmghg'][2], color=hot[2], left=AR6_ecsforc['ch4'][2]+AR6_ecsforc['n2o'][2], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['ch4+n2o+cfc'][2], -0.82, xerr=np.array([AR6_forc['ch4+n2o+cfc'][2]-AR6_forc['ch4+n2o+cfc'][0],AR6_forc['ch4+n2o+cfc'][4]-AR6_forc['ch4+n2o+cfc'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['ch4+n2o+cfc'][2], -1.18, xerr=np.array([AR6_ecsforc['ch4+n2o+cfc'][2]-AR6_ecsforc['ch4+n2o+cfc'][0],AR6_ecsforc['ch4+n2o+cfc'][4]-AR6_ecsforc['ch4+n2o+cfc'][2]]).reshape((2,1)), capsize=3, color='k')

ax.barh(-2, AR6_ecsforc['o3'][2], color=hot[0], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['o3'][2], -1.82, xerr=np.array([AR6_forc['o3'][2]-AR6_forc['o3'][0],AR6_forc['o3'][4]-AR6_forc['o3'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['o3'][2], -2.18, xerr=np.array([AR6_ecsforc['o3'][2]-AR6_ecsforc['o3'][0],AR6_ecsforc['o3'][4]-AR6_ecsforc['o3'][2]]).reshape((2,1)), capsize=3, color='k')

ax.barh(-3, AR6_ecsforc['h2o_stratospheric'][2], color=hot[0], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['h2o_stratospheric'][2], -2.82, xerr=np.array([AR6_forc['h2o_stratospheric'][2]-AR6_forc['h2o_stratospheric'][0],AR6_forc['h2o_stratospheric'][4]-AR6_forc['h2o_stratospheric'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['h2o_stratospheric'][2], -3.18, xerr=np.array([AR6_ecsforc['h2o_stratospheric'][2]-AR6_ecsforc['h2o_stratospheric'][0],AR6_ecsforc['h2o_stratospheric'][4]-AR6_ecsforc['h2o_stratospheric'][2]]).reshape((2,1)), capsize=3, color='k')

ax.barh(-4, AR6_ecsforc['land_use'][2], color=cool[0], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['land_use'][2], -3.82, xerr=np.array([AR6_forc['land_use'][2]-AR6_forc['land_use'][0],AR6_forc['land_use'][4]-AR6_forc['land_use'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['land_use'][2], -4.18, xerr=np.array([AR6_ecsforc['land_use'][2]-AR6_ecsforc['land_use'][0],AR6_ecsforc['land_use'][4]-AR6_ecsforc['land_use'][2]]).reshape((2,1)), capsize=3, color='k')

ax.barh(-4, AR6_ecsforc['bc_on_snow'][2], color=hot[0], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['bc_on_snow'][2], -3.82, xerr=np.array([AR6_forc['bc_on_snow'][2]-AR6_forc['bc_on_snow'][0],AR6_forc['bc_on_snow'][4]-AR6_forc['bc_on_snow'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['bc_on_snow'][2], -4.18, xerr=np.array([AR6_ecsforc['bc_on_snow'][2]-AR6_ecsforc['bc_on_snow'][0],AR6_ecsforc['bc_on_snow'][4]-AR6_ecsforc['bc_on_snow'][2]]).reshape((2,1)), capsize=3, color='k')

ax.barh(-5, AR6_ecsforc['contrails'][2], color=hot[0], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['contrails'][2], -4.82, xerr=np.array([AR6_forc['contrails'][2]-AR6_forc['contrails'][0],AR6_forc['contrails'][4]-AR6_forc['contrails'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['contrails'][2], -5.18, xerr=np.array([AR6_ecsforc['contrails'][2]-AR6_ecsforc['contrails'][0],AR6_ecsforc['contrails'][4]-AR6_ecsforc['contrails'][2]]).reshape((2,1)), capsize=3, color='k')

ax.barh(-6, AR6_ecsforc['aerosol-radiation_interactions'][2], color=cool[0], lw=1, edgecolor='k')
ax.barh(-6, AR6_ecsforc['aerosol-cloud_interactions'][2], color=cool[1], left=AR6_ecsforc['aerosol-radiation_interactions'][2], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['aerosol'][2], -5.82, xerr=np.array([AR6_forc['aerosol'][2]-AR6_forc['aerosol'][0],AR6_forc['aerosol'][4]-AR6_forc['aerosol'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['aerosol'][2], -6.18, xerr=np.array([AR6_ecsforc['aerosol'][2]-AR6_ecsforc['aerosol'][0],AR6_ecsforc['aerosol'][4]-AR6_ecsforc['aerosol'][2]]).reshape((2,1)), capsize=3, color='k')

ax.barh(-7, AR6_ecsforc['solar'][2], color=cool[0], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['solar'][2], -6.82, xerr=np.array([AR6_forc['solar'][2]-AR6_forc['solar'][0],AR6_forc['solar'][4]-AR6_forc['solar'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['solar'][2], -7.18, xerr=np.array([AR6_ecsforc['solar'][2]-AR6_ecsforc['solar'][0],AR6_ecsforc['solar'][4]-AR6_ecsforc['solar'][2]]).reshape((2,1)), capsize=3, color='k')

ax.barh(-8, AR6_ecsforc['volcanic'][2], color=cool[0], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['volcanic'][2], -7.82, xerr=np.array([AR6_forc['volcanic'][2]-AR6_forc['volcanic'][0],AR6_forc['volcanic'][4]-AR6_forc['volcanic'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['volcanic'][2], -8.18, xerr=np.array([AR6_ecsforc['volcanic'][2]-AR6_ecsforc['volcanic'][0],AR6_ecsforc['volcanic'][4]-AR6_ecsforc['volcanic'][2]]).reshape((2,1)), capsize=3, color='k')

#ax.barh(-9, AR6_ecsforc['anthro'][2], color=hot[0], lw=1, edgecolor='k')
#ax.barh(-9, AR6_ecsforc['natural'][2], color=cool[0], lw=1, edgecolor='k')
ax.barh(-9, AR6_ecsforc['total'][2], color=hot[0], lw=1, edgecolor='k')
eb = ax.errorbar(AR6_forc['total'][2], -8.82, xerr=np.array([AR6_forc['total'][2]-AR6_forc['total'][0],AR6_forc['total'][4]-AR6_forc['total'][2]]).reshape((2,1)), capsize=3, color='k')
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(AR6_ecsforc['total'][2], -9.18, xerr=np.array([AR6_ecsforc['total'][2]-AR6_ecsforc['total'][0],AR6_ecsforc['total'][4]-AR6_ecsforc['total'][2]]).reshape((2,1)), capsize=3, color='k')

# labels and prettiness
ax.text(1.0, -1, 'CH$_4$',ha='center',va='center', color=hot[0], size=9)
ax.text(1.28, -1,'N$_2$O',ha='center',va='center', color=hot[1], size=9)
ax.text(1.45, -1, 'Halogens', va='center', color=hot[2], size=9)
#ax.text(1.1, -2, 'Stratospheric', va='center', ha='left', color=hot[1])
#ax.text(0.5, -2, 'Tropospheric', va='center', ha='left', color=hot[0])
ax.text(-0.23,-4, 'Land use', va='center', ha='right', color=cool[0], size=9)
ax.text(0.16, -4, 'Light absorbing particles\non snow and ice', va='center', ha='left', color=hot[0], size=9)
ax.text(0.05, -6, 'Aerosol-cloud', va='center', ha='left', color=cool[1], size=9)
ax.text(0.7, -6, 'Aerosol-radiation', va='center', ha='left', color=cool[0], size=9)
#ax.text(-0.75, -9, 'Anthropogenic', va='center', ha='center', color=hot[0], size=9)
#ax.text(-0.2, -9, 'Natural', va='center', ha='center', color=hot[1], size=9)

ax.text(1.91, -3, 'Anthropogenic', va='center', ha='center', rotation=270)
ax.text(1.91, -7.5, 'Natural', va='center', ha='center', rotation=270)

ax.set_ylim(-9.5,0.5)
ax.set_xlim(-1.2,2.0)
ax.axvline(0, color='k', lw=0.6)
ax.axhline(-6.5, color='k', lw=0.6)
ax.axhline(-8.5, color='k', lw=0.6)
ax.set_yticks(np.arange(-9,1));
ax.set_xlabel('$^{\circ}$C')
ax.set_title('')
ax.set_yticklabels(['Carbon dioxide','Other well-mixed\ngreenhouse gases','Ozone','Stratospheric\nwater vapour', 'Albedo', 'Contrails & aviation-\ninduced cirrus', 'Aerosol', 'Solar', 'Volcanic', 'Total'][::-1]);
ax.set_title('Simulated temperature contributions in 2019 relative to 1750', size=11)

# legend
eb = ax.errorbar(0.5, -7.2, xerr=0.1, color='k', capsize=2, lw=0.8)
eb[-1][0].set_linestyle(':')
eb = ax.errorbar(0.5, -7.75, xerr=0.1, color='k', capsize=2, lw=0.8)
ax.text(0.68, -7.185, 'Forcing uncertainty', va='center', fontsize=8);
ax.text(0.68, -7.735, 'Forcing + climate \nsensitivity uncertainty', va='center', fontsize=8);

rect = mp.Rectangle((0.35, -8.17), 1.3, 1.28, facecolor='None', edgecolor='k', lw=0.5)
ax.add_patch(rect)

# values
ax_values = pl.subplot(gs[0,1])
ax_values.text(0.5,0,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['co2'][2], AR6_ecsforc['co2'][0], AR6_ecsforc['co2'][4]), ha='center', va='center', size=9)
ax_values.text(0.5,-0.6,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['ch4'][2], AR6_ecsforc['ch4'][0], AR6_ecsforc['ch4'][4]), ha='center', va='center', size=9, color=hot[0])
ax_values.text(0.5,-1.0,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['n2o'][2], AR6_ecsforc['n2o'][0], AR6_ecsforc['n2o'][4]), ha='center', va='center', size=9, color=hot[1])
ax_values.text(0.5,-1.4,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['other_wmghg'][2], AR6_ecsforc['other_wmghg'][0], AR6_ecsforc['other_wmghg'][4]), ha='center', va='center', size=9, color=hot[2])
ax_values.text(0.5,-2,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['o3'][2], AR6_ecsforc['o3'][0], AR6_ecsforc['o3'][4]), ha='center', va='center', size=9)
ax_values.text(
    0.5,-3,'{:.2f} [{:.2f} to {:.2f}]'.format(
        AR6_ecsforc['h2o_stratospheric'][2],
        AR6_ecsforc['h2o_stratospheric'][0] if abs(AR6_ecsforc['h2o_stratospheric'][0]) >= 0.005 else abs(AR6_ecsforc['h2o_stratospheric'][0]),
        AR6_ecsforc['h2o_stratospheric'][4]), ha='center', va='center', size=9
)
ax_values.text(0.5,-3.8,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['land_use'][2], AR6_ecsforc['land_use'][0], AR6_ecsforc['land_use'][4]), ha='center', va='center', size=9, color=cool[0])
ax_values.text(
    0.5,-4.2,'{:.2f} [{:.2f} to {:.2f}]'.format(
        AR6_ecsforc['bc_on_snow'][2], 
        AR6_ecsforc['bc_on_snow'][0] if abs(AR6_ecsforc['bc_on_snow'][0]) >= 0.005 else abs(AR6_ecsforc['bc_on_snow'][0]), 
        AR6_ecsforc['bc_on_snow'][4]), ha='center', va='center', size=9, color=hot[0]
)
ax_values.text(0.5,-5,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['contrails'][2], AR6_ecsforc['contrails'][0], AR6_ecsforc['contrails'][4]), ha='center', va='center', size=9)
ax_values.text(0.5,-5.8,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['aerosol-radiation_interactions'][2], AR6_ecsforc['aerosol-radiation_interactions'][0], AR6_ecsforc['aerosol-radiation_interactions'][4]), ha='center', va='center', size=9, color=cool[0])
ax_values.text(0.5,-6.2,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['aerosol-cloud_interactions'][2], AR6_ecsforc['aerosol-cloud_interactions'][0], AR6_ecsforc['aerosol-cloud_interactions'][4]), ha='center', va='center', size=9, color=cool[1])
ax_values.text(
    0.5,-7,'{:.2f} [{:.2f} to {:.2f}]'.format(
        AR6_ecsforc['solar'][2] if abs(AR6_ecsforc['solar'][2]) >= 0.005 else abs(AR6_ecsforc['solar'][2]),
        AR6_ecsforc['solar'][0] if abs(AR6_ecsforc['solar'][0]) >= 0.005 else abs(AR6_ecsforc['solar'][0]), 
        AR6_ecsforc['solar'][4] if abs(AR6_ecsforc['solar'][4]) >= 0.005 else abs(AR6_ecsforc['solar'][4]),
    ), ha='center', va='center', size=9)
ax_values.text(0.5,-8,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['volcanic'][2], AR6_ecsforc['volcanic'][0], AR6_ecsforc['volcanic'][4]), ha='center', va='center', size=9)
ax_values.text(0.5,-9,'{:.2f} [{:.2f} to {:.2f}]'.format(AR6_ecsforc['total'][2], AR6_ecsforc['total'][0], AR6_ecsforc['total'][4]), ha='center', va='center', size=9)
ax_values.set_title('$^{\circ}$C', size=9)

ax_values.set_xlim(0,1)
ax_values.set_ylim(-9.5, 0.5)
ax_values.spines['left'].set_visible(False)
ax_values.spines['right'].set_visible(False)
ax_values.spines['bottom'].set_visible(False)
ax_values.spines['top'].set_visible(False)
ax_values.set_yticklabels([])
ax_values.set_xticks([])

# Create the figure
fig.subplots_adjust(left=0.2)
pl.tight_layout()
pl.savefig('../figures/fig7.7.png', dpi=300)
pl.savefig('../figures/fig7.7.pdf')

# %% cell 14
rebased_climuncert = results['AR6-historical_climuncert']['surface_temperature'] - np.mean(results['AR6-historical_climuncert']['surface_temperature'][100:151,:], axis=0)
rebased = results['AR6-historical']['surface_temperature'] - np.mean(results['AR6-historical']['surface_temperature'][100:151,:], axis=0)


pl.fill_between(np.arange(1750,2020),
                np.percentile(rebased_climuncert, 5, axis=1),
                np.percentile(rebased_climuncert, 95, axis=1),
                alpha=0.3)
pl.plot(np.arange(1750,2020),np.median(rebased_climuncert, axis=1), label='emulated - climuncert');

pl.fill_between(np.arange(1750,2020),
                np.percentile(rebased, 5, axis=1),
                np.percentile(rebased, 95, axis=1),
                alpha=0.3)
pl.plot(np.arange(1750,2020),np.median(rebased, axis=1), label='emulated - forcing only');

xl = pd.read_excel('../data_input/observations/AR6 FGD assessment time series - GMST and GSAT.xlsx', skiprows=1, skipfooter=28)
temp_gmst=xl['4-set mean'].values
temp_year=xl['Unnamed: 0'].values
pl.plot(temp_year, temp_gmst, label='chapter 2 GMST')
pl.legend()

temp_gmst[-1]

# %% cell 15
rebased_climuncert = results['AR6-historical_climuncert']['surface_temperature'] - results['remove_volcanic_climuncert']['surface_temperature']
rebased = results['AR6-historical']['surface_temperature'] - results['remove_volcanic']['surface_temperature']


pl.fill_between(np.arange(1750,2020),
                np.percentile(rebased_climuncert-rebased_climuncert[0,:], 5, axis=1),
                np.percentile(rebased_climuncert-rebased_climuncert[0,:], 95, axis=1),
                alpha=0.3)
pl.plot(np.arange(1750,2020),np.median(rebased_climuncert-rebased_climuncert[0,:], axis=1), label='emulated - climuncert');

pl.fill_between(np.arange(1750,2020),
                np.percentile(rebased-rebased[0,:], 5, axis=1),
                np.percentile(rebased-rebased[0,:], 95, axis=1),
                alpha=0.3)
pl.plot(np.arange(1750,2020),np.median(rebased-rebased[0,:], axis=1), label='emulated - climuncert');

np.median(rebased_climuncert[-1,:]-rebased_climuncert[0,:])
pl.axhline(0, ls=':', color='k')

# %% cell 16
AR6_forc['total'], AR6_ecsforc['total']

# %% cell 18
AR6_ecsforc['anthro'][[0,2,4]]

# %% cell 19
AR6_ecsforc['total'][[0,2,4]]

# %% cell 20
AR6_ecsforc['wmghgs'][[0,2,4]]

# %% cell 21
AR6_ecsforc['o3'][[0,2,4]]

# %% cell 22
AR6_ecsforc['aerosol'][[0,2,4]]

# %% cell 23
AR6_ecsforc['albedo'][[0,2,4]]

# %% cell 24
AR6_ecsforc['natural'][[0,2,4]]

# %% cell 26
np.percentile(
    (results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][0])-
    (results['remove_anthro_climuncert']['surface_temperature'][100:151].mean(axis=0) - results['remove_anthro_climuncert']['surface_temperature'][0]), (5,16,50,84,95)
)
