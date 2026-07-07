# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/250_SPM_future_warming_contributions.ipynb

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
pl.rcParams['figure.dpi'] = 150

# %% cell 4
results = load_dict_from_hdf5('../data_output_large/twolayer_SSPs.h5')

# %% cell 5
results.keys()

# %% cell 6
results['ssp245']['surface_temperature'].shape

# %% cell 7
results['ssp245']['surface_temperature'][269].mean()

# %% cell 8
forcings = ['co2', 'other_ghg', 'other_anthro']
scenarios = ['ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
for scenario in scenarios:
    for forcing in forcings:
        print(scenario, forcing, (results[scenario]['surface_temperature'][331:351] - results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][331:351]).mean())

# %% cell 9
(results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][331:351] - results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][0]).shape

# %% cell 10
forcings = ['co2', 'other_ghg', 'other_anthro']

AR6_forc = {}
AR6_ecsforc = {}
scenarios = ['ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp585']

base_periods = {
    '1750': 0,
    '1850-1900': slice(100,151),
    '1995-2014': slice(245,265),
    '2010-2019': slice(260,270)
}

for scenario in scenarios:
    AR6_forc[scenario] = {}
    AR6_ecsforc[scenario] = {}
    for forcing in forcings:
        AR6_forc[scenario][forcing] = {}
        AR6_ecsforc[scenario][forcing] = {}
        for base_period in base_periods:
            AR6_forc[scenario][forcing][base_period] = np.zeros(5)
            AR6_forc[scenario][forcing][base_period] = np.percentile(
                (
                    (results[scenario]['surface_temperature'][331:351].mean(axis=0) - results[scenario]['surface_temperature'][base_periods[base_period]].mean(axis=0))-
                    (results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][331:351].mean(axis=0) - results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][base_periods[base_period]].mean(axis=0))
                ), (5,16,50,84,95)
            )
            AR6_ecsforc[scenario][forcing][base_period] = np.zeros(5)
            AR6_ecsforc[scenario][forcing][base_period] = np.percentile(
                (
                    (results['%s_climuncert' % scenario]['surface_temperature'][331:351].mean(axis=0) - results['%s_climuncert' % scenario]['surface_temperature'][base_periods[base_period]].mean(axis=0))-
                    (results['%s_remove_%s_climuncert' % (scenario, forcing)]['surface_temperature'][331:351].mean(axis=0) - results['%s_remove_%s_climuncert' % (scenario, forcing)]['surface_temperature'][base_periods[base_period]].mean(axis=0))
                ), (5,16,50,84,95)
            )
    AR6_forc[scenario]['anthro'] = {}
    AR6_ecsforc[scenario]['anthro'] = {}
    for base_period in base_periods:
        AR6_forc[scenario]['anthro'][base_period] = np.percentile(results[scenario]['surface_temperature'][331:351].mean(axis=0) - results[scenario]['surface_temperature'][base_periods[base_period]].mean(axis=0), (5,16,50,84,95))
        AR6_ecsforc[scenario]['anthro'][base_period] = np.percentile(results['%s_climuncert' % scenario]['surface_temperature'][331:351].mean(axis=0) - results['%s_climuncert' % scenario]['surface_temperature'][base_periods[base_period]].mean(axis=0), (5,16,50,84,95))

# %% cell 11
print(AR6_ecsforc['ssp245']['anthro']['1750'])
print(AR6_ecsforc['ssp245']['co2']['1750'])
print(AR6_ecsforc['ssp245']['other_ghg']['1750'])
print(AR6_ecsforc['ssp245']['other_anthro']['1750'])

# %% cell 12
chapter4_tas = {}
varnames = {
    '05': 'Q05',
    'central': 'mean',
    '95': 'Q95'
}
for scenario in scenarios:
    chapter4_tas[scenario] = {}
    for pc in ['05','central','95']:
        nc = Dataset('../data_input/chapter4_assessed_ranges/assessed_%s_%s.nc' % (scenario, pc))
        chapter4_tas[scenario][pc] = nc.variables[varnames[pc]][:]
        #if pc=='95' and scen=='ssp119':
            #print(nc.variables['time'])
            #print(nc.variables['time'][:])
            #print(chapter4_tas[scen][pc])
        nc.close()
    print(scenario, chapter4_tas[scenario]['05'][-1], chapter4_tas[scenario]['central'][-1], chapter4_tas[scenario]['95'][-1])

# %% cell 13
for scenario in scenarios:
    print(scenario, AR6_ecsforc[scenario]['anthro']['1995-2014'][[0,2,4]])

# %% cell 14
output = []
for scenario in scenarios:
    for base_period in base_periods:
        for forcing in ['co2', 'other_ghg', 'other_anthro', 'anthro']:
            output.append([scenario, forcing, base_period, 
                           AR6_ecsforc[scenario][forcing][base_period][0],
                           AR6_ecsforc[scenario][forcing][base_period][1],
                           AR6_ecsforc[scenario][forcing][base_period][2],
                           AR6_ecsforc[scenario][forcing][base_period][3],
                           AR6_ecsforc[scenario][forcing][base_period][4],
                        ])

    output.append([scenario, 'chapter4', '1995-2014', chapter4_tas[scenario]['05'][-1],
                   np.nan, 
                   chapter4_tas[scenario]['central'][-1],
                   np.nan,
                   chapter4_tas[scenario]['95'][-1]])
df = pd.DataFrame(output, columns=['scenario', 'forcing', 'base_period', 'p05','p16','p50','p84','p95'])
df.to_csv('../data_output/ts_warming_ranges.csv')
