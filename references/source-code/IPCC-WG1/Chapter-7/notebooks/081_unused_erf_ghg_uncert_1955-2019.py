# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/081_unused_erf_ghg_uncert_1955-2019.ipynb

# %% cell 2
from ar6.utils.h5 import load_dict_from_hdf5
from ar6.constants import NINETY_TO_ONESIGMA
import numpy as np
import pandas as pd

# %% cell 3
forcing_ensemble = load_dict_from_hdf5('../data_output_large/ERF_ensemble.h5')

# %% cell 4
forcing_ensemble['co2'].shape

# %% cell 5
# all WMGHGs
df = pd.DataFrame(
    np.percentile(
        (
            forcing_ensemble['co2'][205:] + 
            forcing_ensemble['ch4'][205:] + 
            forcing_ensemble['n2o'][205:] + 
            forcing_ensemble['other_wmghg'][205:]
        ) - (
            forcing_ensemble['co2'][205] + 
            forcing_ensemble['ch4'][205] + 
            forcing_ensemble['n2o'][205] + 
            forcing_ensemble['other_wmghg'][205]
        ), (5,95), axis=1
    ).T,
    columns=['p05', 'p95'],
    index=range(1955, 2020)
)
df.to_csv('../data_output/AR6_ERF_GHGs_1955-2019.csv')
df

# %% cell 6
# all GHGs and precursors
df = pd.DataFrame(
    np.percentile(
        (
            forcing_ensemble['co2'][205:] + 
            forcing_ensemble['ch4'][205:] + 
            forcing_ensemble['n2o'][205:] + 
            forcing_ensemble['other_wmghg'][205:] +
            forcing_ensemble['o3'][205:] +
            forcing_ensemble['h2o_stratospheric'][205:]
        ) - (
            forcing_ensemble['co2'][205] + 
            forcing_ensemble['ch4'][205] + 
            forcing_ensemble['n2o'][205] + 
            forcing_ensemble['other_wmghg'][205] + 
            forcing_ensemble['o3'][205] +
            forcing_ensemble['h2o_stratospheric'][205]
        ), (5,95), axis=1
    ).T,
    columns=['p05', 'p95'],
    index=range(1955, 2020)
)
df.to_csv('../data_output/AR6_ERF_GHGs_incl_not_well_mixed_1955-2019.csv')
df
