# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/236_chapter2_attributed_warming.ipynb

# %% cell 2
import numpy as np
import scipy.stats as st
import pandas as pd

from ar6.utils.h5 import *

# %% cell 3
results = load_dict_from_hdf5('../data_output_large/twolayer_AR6-historical.h5')

# %% cell 4
results.keys()

# %% cell 5
AR6_ecsforc = {}
AR6_ecsforc['total'] = np.percentile(results['AR6-historical_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0), (5,16,50,84,95))

AR6_forc = {}
AR6_forc['total'] = np.percentile(results['AR6-historical']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical']['surface_temperature'][100:151].mean(axis=0), (5,16,50,84,95))

# %% cell 6
AR6_ecsforc['total']

# %% cell 7
AR6_forc['total']
