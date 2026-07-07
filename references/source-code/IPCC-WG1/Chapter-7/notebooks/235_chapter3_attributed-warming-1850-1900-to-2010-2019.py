# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/235_chapter3_attributed-warming-1850-1900-to-2010-2019.ipynb

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
AR6_forc = {}
forcings = ['co2', 'ch4', 'n2o', 'other_wmghg', 'o3', 'h2o_stratospheric',
            'contrails', 'aerosol-radiation_interactions', 'aerosol-cloud_interactions', 
            'bc_on_snow', 'land_use', 'volcanic', 'solar', 'aerosol', 'anthro', 'natural', 'wmghgs']
for forcing in forcings:
    AR6_forc[forcing] = np.zeros(5)
    AR6_forc[forcing] = np.percentile(        
        (results['AR6-historical_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0))-
        (results['remove_%s_climuncert' % forcing]['surface_temperature'][260:270].mean(axis=0) - results['remove_%s_climuncert' % forcing]['surface_temperature'][100:151].mean(axis=0)),
        (5,16,50,84,95)
    )    
# aggregated categories
other_anth_chapter3 = (
    (
        (results['AR6-historical_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0))-
        (results['remove_o3_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['remove_o3_climuncert']['surface_temperature'][100:151].mean(axis=0))
    ) +
    (
        (results['AR6-historical_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0))-
        (results['remove_h2o_stratospheric_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['remove_h2o_stratospheric_climuncert']['surface_temperature'][100:151].mean(axis=0))
    ) +
    (
        (results['AR6-historical_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0))-
        (results['remove_contrails_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['remove_contrails_climuncert']['surface_temperature'][100:151].mean(axis=0))
    ) +
    (
        (results['AR6-historical_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0))-
        (results['remove_aerosol_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['remove_aerosol_climuncert']['surface_temperature'][100:151].mean(axis=0))
    ) +
    (
        (results['AR6-historical_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0))-
        (results['remove_land_use_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['remove_land_use_climuncert']['surface_temperature'][100:151].mean(axis=0))
    ) +
    (
        (results['AR6-historical_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0))-
        (results['remove_bc_on_snow_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['remove_bc_on_snow_climuncert']['surface_temperature'][100:151].mean(axis=0))
    )
)
AR6_forc['aerosols_o3_luc_other_anth'] = np.percentile(other_anth_chapter3, (5,16,50,84,95))

AR6_forc['total'] = np.percentile(results['AR6-historical_climuncert']['surface_temperature'][260:270].mean(axis=0) - results['AR6-historical_climuncert']['surface_temperature'][100:151].mean(axis=0), (5,16,50,84,95))

# %% cell 6
data_output = []
for species in ['anthro','natural','wmghgs','aerosols_o3_luc_other_anth']:
    data_output.append([
        species,
        AR6_forc[species][0],
        AR6_forc[species][2],
        AR6_forc[species][4]
    ])

# %% cell 7
df = pd.DataFrame(data_output, columns=['Species', 'pc05', 'pc50', 'pc95'])
df.set_index('Species', inplace=True)
df.to_csv('../data_output/fig3.7_data.csv')
df

# %% cell 8
data_output = []
for species in ['co2', 'ch4', 'n2o', 'other_wmghg', 'o3', 'h2o_stratospheric',
            'contrails', 'aerosol-radiation_interactions', 'aerosol-cloud_interactions', 
            'bc_on_snow', 'land_use', 'volcanic', 'solar']:
    data_output.append([
        species,
        AR6_forc[species][0],
        AR6_forc[species][2],
        AR6_forc[species][4]
    ])
df = pd.DataFrame(data_output, columns=['Species', 'pc05', 'pc50', 'pc95'])
df.set_index('Species', inplace=True)
df.to_csv('../data_output/figSPM_A_data.csv')
df
