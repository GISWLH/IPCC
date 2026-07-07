# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/225_SPM_attributed-warming-by-emissions.ipynb

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
results = load_dict_from_hdf5('../data_output_large/twolayer_AR6-historical-emissions-based.h5')

# %% cell 4
results.keys()

# %% cell 5
results['AR6-anthro_climuncert']['surface_temperature'].shape

# %% cell 6
results['AR6-anthro_climuncert']['surface_temperature'][0].mean()

# %% cell 7
forcings = list(results.keys())
forcings.remove('AR6-anthro_climuncert')
forcings

# %% cell 8
AR6_ecsforc = {}

for forcing in forcings:
    AR6_ecsforc[forcing[7:14]] = np.zeros(5)
    AR6_ecsforc[forcing[7:14]] = np.percentile(
        (results['AR6-anthro_climuncert']['surface_temperature'][-1] - results['AR6-anthro_climuncert']['surface_temperature'][0])-
        (results[forcing]['surface_temperature'][-1] - results[forcing]['surface_temperature'][0]), (5,16,50,84,95)
    )

# %% cell 9
AR6_ecsforc.keys()

# %% cell 10
print(AR6_ecsforc['ch4_co2'])

# %% cell 11
emissions = ['co2', 'ch4', 'n2o', 'oth', 'nox', 'voc', 'so2', 'blc', 'orc', 'nh3', 'con', 'luc']
forc = ['co2', 'ch4', 'n2o', 'oth', 'ozo', 'h2o', 'ari', 'aci', 'bcs', 'con', 'luc']

emissions_full = ['CO2', 'CH4', 'N2O', 'Halocarbons', 'NOx', 'VOC', 'SO2', 'BC', 'OC', 'NH3', 'Contrails', 'Land use']
forcings_full = ['CO2', 'CH4', 'N2O', 'Halocarbons', 'O3', 'Stratospheric H2O', 'Aerosol-radiation', 'Aerosol-cloud', 'BC on snow', 'Contrails', 'Land use']

results = np.zeros((len(emissions), len(forc)))

for i, em in enumerate(emissions):
    for j, fo in enumerate(forc):
        combo = '%s_%s' % (em, fo)
        if combo in AR6_ecsforc.keys():
            #print(AR6_ecsforc[combo][2])
            results[i, j] = AR6_ecsforc[combo][2]

# %% cell 12
df50 = pd.DataFrame(results, index=emissions_full, columns=forcings_full)
df50.to_csv('../data_output/GSAT_by_emissions.csv')
