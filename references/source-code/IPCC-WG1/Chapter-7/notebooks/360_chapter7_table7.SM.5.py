# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/360_chapter7_table7.SM.5.ipynb

# %% cell 2
import json
import pandas as pd

# %% cell 3
with open('../data_input/Zelinka_et_al_2020/cmip56_feedbacks_AR6.json') as file:
    z20 = json.load(file)

# %% cell 4
df5 = pd.DataFrame(z20['cmip5'])
df5['mip'] = 'CMIP5'
df5

# %% cell 5
df6 = pd.DataFrame(z20['cmip6'])
df6['mip'] = 'CMIP6'
df6

# %% cell 6
df = pd.concat([df5, df6])
df

# %% cell 7
df = df[['mip', 'models', 'NET_fbk', 'PL_fbk', 'WVLR_fbk', 'ALB_fbk', 'CLD_fbk', 'resid_fbk']]
df

# %% cell 8
df.to_csv('../data_output/7sm/feedbacks_supplement.csv', index=False)

# %% cell 9
df6.mean()
