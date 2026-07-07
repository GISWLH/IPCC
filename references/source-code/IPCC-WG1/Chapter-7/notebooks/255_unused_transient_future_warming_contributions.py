# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/255_unused_transient_future_warming_contributions.ipynb

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
results['ssp245']['surface_temperature'].shape

# %% cell 6
results['ssp245']['surface_temperature'][269].mean()

# %% cell 7
forcings = ['co2', 'ch4', 'aerosol']
scenarios = ['ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
for scenario in scenarios:
    for forcing in forcings:
        print(scenario, forcing, (results[scenario]['surface_temperature'][331:351] - results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][331:351]).mean())

# %% cell 8
(results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][268:351] - results['%s_remove_%s' % (scenario, forcing)]['surface_temperature'][0]).shape

# %% cell 9
forcings = ['co2', 'ch4', 'aerosol', 'other_ghg', 'other_anthro']

AR6_ecsforc = {}
scenarios = ['ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp585']

base_period = slice(100,151)

for scenario in scenarios:
    AR6_ecsforc[scenario] = {}
    for forcing in forcings:
#        AR6_ecsforc[scenario][forcing] = np.zeros((83, 5))
        AR6_ecsforc[scenario][forcing] = np.percentile(
            (
                (results['%s_climuncert' % scenario]['surface_temperature'][268:351] - results['%s_climuncert' % scenario]['surface_temperature'][base_period].mean(axis=0))-
                (results['%s_remove_%s_climuncert' % (scenario, forcing)]['surface_temperature'][268:351] - results['%s_remove_%s_climuncert' % (scenario, forcing)]['surface_temperature'][base_period].mean(axis=0))
            ), (5,16,50,84,95), axis=1
        )
    AR6_ecsforc[scenario]['anthro'] = np.percentile(results['%s_climuncert' % scenario]['surface_temperature'][268:351] - results['%s_climuncert' % scenario]['surface_temperature'][base_period].mean(axis=0), (5,16,50,84,95), axis=1)

# %% cell 10
output = []
for scenario in scenarios:
    for forcing in ['co2', 'ch4', 'aerosol', 'other_ghg', 'other_anthro', 'anthro']:
        output.append([scenario, forcing]+[i for i in AR6_ecsforc[scenario][forcing][2,:]])

df = pd.DataFrame(output, columns=['scenario', 'forcing'] + list(range(2018,2101)))
df.to_csv('../data_output/spm4_extended_warming_contributions.csv', index=False)
