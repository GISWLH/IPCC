# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/260_chapter6_slcf_future_warming_contributions.ipynb

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
forcings = ['ch4', 'hfc', 'o3', 'aerosol', 'bc_on_snow', 'slcf']
scenarios = ['ssp119','ssp126','ssp245','ssp334','ssp370','ssp370-lowNTCF-aerchemmip','ssp370-lowNTCF-gidden','ssp434','ssp460','ssp534-over','ssp585']
for scenario in scenarios:
    for forcing in forcings:
        print(scenario, forcing, (results[scenario]['surface_temperature'][331:351] - results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][331:351]).mean())

# %% cell 9
(results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][331:351] - results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][0]).shape

# %% cell 10
forcings = ['ch4', 'hfc', 'o3', 'aerosol', 'bc_on_snow', 'slcf']

AR6_forc = {}
AR6_ecsforc = {}

base_periods = {
#    '1750': 0,
#    '1850-1900': slice(100,151),
#    '1995-2014': slice(245,265),
#    '2010-2019': slice(260,270),
    '2020'     : slice(270,271)
}

for scenario in scenarios:
    AR6_forc[scenario] = {}
    AR6_ecsforc[scenario] = {}
    for forcing in forcings:
        AR6_forc[scenario][forcing] = {}
        AR6_ecsforc[scenario][forcing] = {}
        for base_period in base_periods:
            AR6_forc[scenario][forcing][base_period] = np.zeros((81,5))
            AR6_ecsforc[scenario][forcing][base_period] = np.zeros((81,5))
            for year in range(270,351):
                AR6_forc[scenario][forcing][base_period][year-270,:] = np.percentile(
                    (
                        (results[scenario]['surface_temperature'][year]- results[scenario]['surface_temperature'][base_periods[base_period]].mean(axis=0))-
                        (results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][year] - results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][base_periods[base_period]].mean(axis=0))
                    ), (5,16,50,84,95)
                )
                AR6_ecsforc[scenario][forcing][base_period][year-270,:] = np.percentile(
                    (
                        (results['%s_climuncert' % scenario]['surface_temperature'][year] - results['%s_climuncert' % scenario]['surface_temperature'][base_periods[base_period]].mean(axis=0))-
                        (results['%s_remove_%s_climuncert' % (scenario, forcing)]['surface_temperature'][year] - results['%s_remove_%s_climuncert' % (scenario, forcing)]['surface_temperature'][base_periods[base_period]].mean(axis=0))
                    ), (5,16,50,84,95)
                )
    AR6_forc[scenario]['anthro'] = {}
    AR6_ecsforc[scenario]['anthro'] = {}
    for base_period in base_periods:
        AR6_forc[scenario]['anthro'][base_period] = np.zeros((81,5))
        AR6_ecsforc[scenario]['anthro'][base_period] = np.zeros((81,5))
        for year in range(270,351):
            AR6_forc[scenario]['anthro'][base_period][year-270,:] = np.percentile(results[scenario]['surface_temperature'][year] - results[scenario]['surface_temperature'][base_periods[base_period]].mean(axis=0), (5,16,50,84,95))
            AR6_ecsforc[scenario]['anthro'][base_period][year-270,:] = np.percentile(results['%s_climuncert' % scenario]['surface_temperature'][year] - results['%s_climuncert' % scenario]['surface_temperature'][base_periods[base_period]].mean(axis=0), (5,16,50,84,95))

# %% cell 11
print(AR6_ecsforc['ssp245']['anthro']['2020'])

# %% cell 12
for scenario in scenarios:
    print(scenario, AR6_ecsforc[scenario]['anthro']['2020'][:,[0,2,4]])

# %% cell 13
output = []
for scenario in scenarios:
    for forcing in ['ch4', 'hfc', 'o3', 'aerosol', 'bc_on_snow', 'slcf', 'anthro']:
        for year in range(270, 351):
            output.append([scenario, forcing, '2020', year+1750,
               AR6_ecsforc[scenario][forcing]['2020'][year-270,0],
               AR6_ecsforc[scenario][forcing]['2020'][year-270,1],
               AR6_ecsforc[scenario][forcing]['2020'][year-270,2],
               AR6_ecsforc[scenario][forcing]['2020'][year-270,3],
               AR6_ecsforc[scenario][forcing]['2020'][year-270,4],
            ])

df = pd.DataFrame(output, columns=['scenario', 'forcing', 'base_period', 'year', 'p05','p16','p50','p84','p95'])
df.to_csv('../data_output/slcf_warming_ranges.csv')
df
