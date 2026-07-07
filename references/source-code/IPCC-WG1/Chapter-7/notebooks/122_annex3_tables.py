# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/122_annex3_tables.ipynb

# %% cell 2
import numpy as np
import pandas as pd
from ar6.utils import mkdir_p

# %% cell 3
mkdir_p('../data_output/annex5/')

# %% cell 4
years = [2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2200, 2300, 2400, 2500]
years_hist = [1750, 1850, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2015, 2019]

# %% cell 5
scenarios_ssp = ['ssp119','ssp126','ssp245','ssp370','ssp370-lowNTCFCH4','ssp370-lowNTCF','ssp434','ssp460','ssp534-over','ssp585']
scenarios_rcp = ['rcp26', 'rcp45', 'rcp60', 'rcp85']
erf = {}
erf95 = {}
erf05 = {}
for scenario in scenarios_ssp:
    erf[scenario] = pd.read_csv('../data_output/SSPs/ERF_%s_1750-2500.csv' % scenario, index_col=0)
    erf[scenario].loc[years,:].to_csv('../data_output/annex5/ERF_%s_2020-2500.csv' % scenario, float_format='%.2f')
    erf05[scenario] = pd.read_csv('../data_output/SSPs/ERF_%s_1750-2500_pc05.csv' % scenario, index_col=0)
    erf95[scenario] = pd.read_csv('../data_output/SSPs/ERF_%s_1750-2500_pc95.csv' % scenario, index_col=0)
for scenario in scenarios_rcp:
    erf[scenario] = pd.read_csv('../data_output/RCPs/ERF_%s_1750-2500.csv' % scenario, index_col=0)
    erf05[scenario] = pd.read_csv('../data_output/RCPs/ERF_%s_1750-2500_pc05.csv' % scenario, index_col=0)
    erf95[scenario] = pd.read_csv('../data_output/RCPs/ERF_%s_1750-2500_pc95.csv' % scenario, index_col=0)
erf['historical'] = pd.read_csv('../data_output/AR6_ERF_1750-2019.csv', index_col=0)
erf['historical'].drop(columns=['nonco2_wmghg','aerosol','chapter2_other_anthro'], inplace=True)
pd.options.display.float_format = "{:,.2f}".format

# %% cell 6
erf['historical'].loc[years_hist,:]

# %% cell 7
erf['ssp119'].loc[years,:]

# %% cell 8
scenarios = scenarios_rcp + scenarios_ssp

# %% cell 9
data_output = []
for scenario in scenarios:
    data_output.append([
        scenario,
        '%.2f' % erf[scenario].loc[2030,'total_anthropogenic'],
        '%.2f' % erf[scenario].loc[2030,'total_natural'],
        '%.2f (%.2f-%.2f)' % (erf[scenario].loc[2030,'total'], erf05[scenario].loc[2030,'total'], erf95[scenario].loc[2030,'total']),
        '%.2f' % erf[scenario].loc[2050,'total_anthropogenic'],
        '%.2f' % erf[scenario].loc[2050,'total_natural'],
        '%.2f (%.2f-%.2f)' % (erf[scenario].loc[2050,'total'], erf05[scenario].loc[2050,'total'], erf95[scenario].loc[2050,'total']),
        '%.2f' % erf[scenario].loc[2090,'total_anthropogenic'],
        '%.2f' % erf[scenario].loc[2090,'total_natural'],
        '%.2f (%.2f-%.2f)' % (erf[scenario].loc[2090,'total'], erf05[scenario].loc[2090,'total'], erf95[scenario].loc[2090,'total']),
    ])
df = pd.DataFrame(data_output, columns = ['scenario','2030a','2030n','2030','2050a','2050n','2050','2090a','2090n','2090'])
df.set_index('scenario',inplace=True)
df.to_csv('../data_output/annex5/comparison.csv')

# %% cell 10
df
