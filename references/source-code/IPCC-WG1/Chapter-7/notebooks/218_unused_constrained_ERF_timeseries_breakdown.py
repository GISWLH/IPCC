# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/218_unused_constrained_ERF_timeseries_breakdown.ipynb

# %% cell 2
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl

from ar6.utils.h5 import *

# %% cell 3
results = load_dict_from_hdf5('../data_output_large/twolayer_AR6-historical.h5')

# %% cell 4
results.keys()

# %% cell 5
results['AR6-historical_climuncert']['effective_radiative_forcing'].shape

# %% cell 6
pl.plot(np.arange(1750,2020), results['AR6-historical_climuncert']['effective_radiative_forcing']);

# %% cell 7
pl.plot(np.arange(1750,2020), 
        results['AR6-historical_climuncert']['effective_radiative_forcing'] - results['remove_aerosol_climuncert']['effective_radiative_forcing']);

# %% cell 8
np.percentile(
    (
        results['AR6-historical_climuncert']['effective_radiative_forcing'][255:265,:] -
        results['remove_aerosol_climuncert']['effective_radiative_forcing'][255:265,:]
    ).mean(axis=0),
(5, 50, 95))

# %% cell 9
# aerosols
df = pd.DataFrame(
    results['AR6-historical_climuncert']['effective_radiative_forcing'] -
    results['remove_aerosol_climuncert']['effective_radiative_forcing'], 
    index=range(1750, 2020)
)
df
df.to_csv('../data_output_large/WG1_constrained_ERF_ensemble_aerosol.csv')

# %% cell 10
# co2
df = pd.DataFrame(
    results['AR6-historical_climuncert']['effective_radiative_forcing'] -
    results['remove_co2_climuncert']['effective_radiative_forcing'], 
    index=range(1750, 2020)
)
df
df.to_csv('../data_output_large/WG1_constrained_ERF_ensemble_co2.csv')

# %% cell 11
# other anthro = anthro - co2 - aerosol
df = pd.DataFrame(
    results['AR6-historical_climuncert']['effective_radiative_forcing'] -
    results['remove_anthro_climuncert']['effective_radiative_forcing'] -
    
    (results['AR6-historical_climuncert']['effective_radiative_forcing'] -
    results['remove_co2_climuncert']['effective_radiative_forcing']) -
    
    (results['AR6-historical_climuncert']['effective_radiative_forcing'] -
    results['remove_aerosol_climuncert']['effective_radiative_forcing']) 
    , 
    index=range(1750, 2020)
)
df
df.to_csv('../data_output_large/WG1_constrained_ERF_ensemble_non-co2-non-aerosol-anthro.csv')

# %% cell 12
# volcanic
df = pd.DataFrame(
    results['AR6-historical_climuncert']['effective_radiative_forcing'] -
    results['remove_volcanic_climuncert']['effective_radiative_forcing'], 
    index=range(1750, 2020)
)
df
df.to_csv('../data_output_large/WG1_constrained_ERF_ensemble_volcanic.csv')

# %% cell 13
# solar
df = pd.DataFrame(
    results['AR6-historical_climuncert']['effective_radiative_forcing'] -
    results['remove_solar_climuncert']['effective_radiative_forcing'], 
    index=range(1750, 2020)
)
df
df.to_csv('../data_output_large/WG1_constrained_ERF_ensemble_solar.csv')
