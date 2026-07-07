# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/005_chapter7_4xCO2_2xCO2_forcing_constant.ipynb

# %% cell 2
from fair.forcing.ghg import meinshausen, etminan
import pandas as pd
import numpy as np

# %% cell 3
ghg_obs = pd.read_excel('../data_input/observations/LLGHG_history_AR6_v9_for_archive.xlsx', skiprows=22, sheet_name="mixing_ratios", index_col=0)
for addyear in range(1751,1850):
    ghg_obs.loc[addyear, 'YYYY'] = np.nan
ghg_obs = ghg_obs.sort_index()
ghg_obs = ghg_obs.interpolate()
ghg_obs

# %% cell 4
co2_pi = ghg_obs.loc[1750,'CO2']
ch4_pi = ghg_obs.loc[1750,'CH4']
n2o_pi = ghg_obs.loc[1750,'N2O']

co2_1850 = ghg_obs.loc[1850,'CO2']
ch4_1850 = ghg_obs.loc[1850,'CH4']
n2o_1850 = ghg_obs.loc[1850,'N2O']

co2_2011 = ghg_obs.loc[2011,'CO2']
ch4_2011 = ghg_obs.loc[2011,'CH4']
n2o_2011 = ghg_obs.loc[2011,'N2O']

co2_2019 = ghg_obs.loc[2019,'CO2']
ch4_2019 = ghg_obs.loc[2019,'CH4']
n2o_2019 = ghg_obs.loc[2019,'N2O']

# %% cell 5
m4x = meinshausen(np.array([4*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)
m2x = meinshausen(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)
m2x[0]/m4x[0]

# %% cell 6
e4x = etminan(np.array([4*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)
e2x = etminan(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)
e2x[0]/e4x[0]

# %% cell 7
e2x[0]

# %% cell 8
m2x[0]

# %% cell 9
etminan(np.array([2*co2_2011, ch4_2011, n2o_2011]), Cpi=np.array([co2_2011, ch4_2011, n2o_2011]), scale_F2x=False)

# %% cell 10
meinshausen(np.array([2*co2_2011, ch4_2011, n2o_2011]), Cpi=np.array([co2_2011, ch4_2011, n2o_2011]), scale_F2x=False)

# %% cell 11
meinshausen(np.array([284.3*2, ch4_pi, n2o_pi]), Cpi=np.array([284.3, ch4_pi, n2o_pi]), scale_F2x=False)

# %% cell 12
etminan(np.array([co2_2019, ch4_2019, n2o_2019]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)

# %% cell 13
meinshausen(np.array([co2_2019, ch4_2019, n2o_2019]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)

# %% cell 14
meinshausen(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False) * np.array([1.05, 0.86, 1.07])

# %% cell 15
meinshausen(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)

# %% cell 16
meinshausen(np.array([2*co2_1850, ch4_1850, n2o_1850]), Cpi=np.array([co2_1850, ch4_1850, n2o_1850]), scale_F2x=False) * np.array([1.05, 0.86, 1.07])

# %% cell 17
etminan(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)

# %% cell 18
etminan(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False) * np.array([1.05, 0.86, 1.07])

# %% cell 19
print(etminan(np.array([700, 1800, 323]), Cpi=np.array([389, 1800, 323]), scale_F2x=False))
print(meinshausen(np.array([700, 1800, 323]), Cpi=np.array([389, 1800, 323]), scale_F2x=False))

# %% cell 20
print(etminan(np.array([389, 1800, 323]), Cpi=np.array([180, 1800, 323]), scale_F2x=False))
print(meinshausen(np.array([389, 1800, 323]), Cpi=np.array([180, 1800, 323]), scale_F2x=False))

# %% cell 21
print(etminan(np.array([700, 1800, 323]), Cpi=np.array([180, 1800, 323]), scale_F2x=False))
print(meinshausen(np.array([700, 1800, 323]), Cpi=np.array([180, 1800, 323]), scale_F2x=False))

# %% cell 22
3.22707066 +4.18614974

# %% cell 23
3.18558871 + 4.12898865

# %% cell 25
print(etminan(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False))
print(etminan(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))

print(meinshausen(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False))
print(meinshausen(np.array([2*co2_pi, ch4_pi, n2o_pi]), Cpi=np.array([co2_pi, ch4_pi, n2o_pi]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))

# %% cell 27
print(etminan(np.array([2*277.15, ch4_pi, 273.87]), Cpi=np.array([277.15, ch4_pi, 273.87]), scale_F2x=False))
print(etminan(np.array([2*277.15, ch4_pi, 273.87]), Cpi=np.array([277.15, ch4_pi, 273.87]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))

print(meinshausen(np.array([2*277.15, ch4_pi, 273.87]), Cpi=np.array([277.15, ch4_pi, 273.87]), scale_F2x=False))
print(meinshausen(np.array([2*277.15, ch4_pi, 273.87]), Cpi=np.array([277.15, ch4_pi, 273.87]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))

# %% cell 29
print(etminan(np.array([2*284.32, ch4_pi, 273.02]), Cpi=np.array([284.32, ch4_pi, 273.02]), scale_F2x=False))
print(etminan(np.array([2*284.32, ch4_pi, 273.02]), Cpi=np.array([284.32, ch4_pi, 273.02]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))

print(meinshausen(np.array([2*284.32, ch4_pi, 273.02]), Cpi=np.array([284.32, ch4_pi, 273.02]), scale_F2x=False))
print(meinshausen(np.array([2*284.32, ch4_pi, 273.02]), Cpi=np.array([284.32, ch4_pi, 273.02]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))

# %% cell 31
print(etminan(np.array([2*389, ch4_pi, 323]), Cpi=np.array([389, ch4_pi, 323]), scale_F2x=False))
print(etminan(np.array([2*389, ch4_pi, 323]), Cpi=np.array([389, ch4_pi, 323]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))

print(meinshausen(np.array([2*389, ch4_pi, 323]), Cpi=np.array([389, ch4_pi, 323]), scale_F2x=False))
print(meinshausen(np.array([2*389, ch4_pi, 323]), Cpi=np.array([389, ch4_pi, 323]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))

# %% cell 33
print(etminan(np.array([2*co2_2019, ch4_2019, n2o_2019]), Cpi=np.array([co2_2019, ch4_2019, n2o_2019]), scale_F2x=False))
print(etminan(np.array([2*co2_2019, ch4_2019, n2o_2019]), Cpi=np.array([co2_2019, ch4_2019, n2o_2019]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))

print(meinshausen(np.array([2*co2_2019, ch4_2019, n2o_2019]), Cpi=np.array([co2_2019, ch4_2019, n2o_2019]), scale_F2x=False))
print(meinshausen(np.array([2*co2_2019, ch4_2019, n2o_2019]), Cpi=np.array([co2_2019, ch4_2019, n2o_2019]), scale_F2x=False)*np.array([1.05, 0.86, 1.07]))
