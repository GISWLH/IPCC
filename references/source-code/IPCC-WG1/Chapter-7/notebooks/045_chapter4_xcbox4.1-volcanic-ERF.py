# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/045_chapter4_xcbox4.1-volcanic-ERF.ipynb

# %% cell 2
import numpy as np
import matplotlib.pyplot as pl
import pandas as pd
import scipy.stats as st

# %% cell 3
bethke_data = np.loadtxt('../data_input/Bethke_et_al_2017_NCC/NorESM1_AerosolMass_AODVIS_GMST_2006-2099.txt')

# %% cell 5
bethke_df = pd.DataFrame(data=bethke_data, columns=['year', 'month', 'burden_mem45', 'aod_mem45', 'aod_ctl', 'gmst_mem45', 'gmst_ctl'])

# %% cell 6
bethke_df

# %% cell 7
bethke_df['delta_aod'] = bethke_df['aod_mem45'] - bethke_df['aod_ctl']
bethke_df['delta_gmst'] = bethke_df['gmst_mem45'] - bethke_df['gmst_ctl']

# %% cell 8
bethke_df

# %% cell 9
# I have to admit, I did not expect the burden-sAOD relationship to be this linear :)
reg = st.linregress(bethke_df['burden_mem45'], bethke_df['delta_aod'])
reg

# %% cell 10
pl.scatter(bethke_df['burden_mem45'], bethke_df['delta_aod'])
pl.xlabel('delta stratospheric aerosol burden, Tg')
pl.ylabel('delta AOD')
pl.plot(np.linspace(0,180,100), reg.slope*np.linspace(0,180,100)+reg.intercept, color='r')

# %% cell 11
# conversion to ERF = -21 * regression slope (sAOD/Tg) * burden (Tg) + 0.2
# -21 is the conversion for NorESM2
# +0.2 offset is the quiescent year forcing in the AR6 time series
year = np.arange(2006+1/24, 2100, 1/12)

# %% cell 12
pl.plot(year, -21 * reg.slope * bethke_df['burden_mem45'] + reg.intercept + 0.2)

# %% cell 13
np.mean(-21 * reg.slope * bethke_df['burden_mem45'] + reg.intercept + 0.2)

# %% cell 14
df = pd.DataFrame({'year': year, 'ERF': -21 * reg.slope * bethke_df['burden_mem45'].squeeze() + reg.intercept + 0.2})
df.set_index('year', inplace=True)
df.to_csv('../data_output/xcbox4.1_ERF.csv')

# %% cell 15
df
