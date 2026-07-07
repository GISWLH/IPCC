# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/170_WG3_verify_constrained_output.ipynb

# %% cell 2
import os.path
import copy
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyam
from fair.forward import fair_scm
from scmdata import ScmRun, run_append
from tqdm import tqdm_notebook

import openscm_runner
from openscm_runner.run import run
from openscm_runner.adapters import FAIR

# %% cell 3
openscm_runner.__version__

# %% cell 4
fair = FAIR()
fair.get_version()

# %% cell 5
with open('../data_output_large/fair-samples/fair-1.6.2-wg3-params.json') as f:
    config_list = json.load(f)

# %% cell 6
species = [
'Emissions|BC',
'Emissions|CH4',
'Emissions|CO',
'Emissions|CO2|MAGICC AFOLU',
'Emissions|CO2|MAGICC Fossil and Industrial',
'Emissions|F-Gases|HFC|HFC125',
'Emissions|F-Gases|HFC|HFC134a',
'Emissions|F-Gases|HFC|HFC143a',
'Emissions|F-Gases|HFC|HFC227ea',
'Emissions|F-Gases|HFC|HFC23',
'Emissions|F-Gases|HFC|HFC245fa',
'Emissions|F-Gases|HFC|HFC32',
'Emissions|F-Gases|HFC|HFC4310mee',
'Emissions|F-Gases|PFC|C2F6',
'Emissions|F-Gases|PFC|C6F14',
'Emissions|F-Gases|PFC|CF4',
'Emissions|F-Gases|SF6',
'Emissions|Montreal Gases|CCl4',
'Emissions|Montreal Gases|CFC|CFC11',
'Emissions|Montreal Gases|CFC|CFC113',
'Emissions|Montreal Gases|CFC|CFC114',
'Emissions|Montreal Gases|CFC|CFC115',
'Emissions|Montreal Gases|CFC|CFC12',
'Emissions|Montreal Gases|CH3Br',
'Emissions|Montreal Gases|CH3CCl3',
'Emissions|Montreal Gases|CH3Cl',
'Emissions|Montreal Gases|HCFC141b',
'Emissions|Montreal Gases|HCFC142b',
'Emissions|Montreal Gases|HCFC22',
'Emissions|Montreal Gases|Halon1202',
'Emissions|Montreal Gases|Halon1211',
'Emissions|Montreal Gases|Halon1301',
'Emissions|Montreal Gases|Halon2402',
'Emissions|N2O',
'Emissions|NH3',
'Emissions|NOx',
'Emissions|OC',
'Emissions|Sulfur',
'Emissions|VOC']

# %% cell 7
df_fair = ScmRun('../data_input_large/rcmip-emissions-annual-means-v5-1-0.csv', lowercase_cols=True)
df_fair.filter(
    scenario=['ssp245'], 
#    year=range(2015,2301),
    year=range(2015,2101),
    variable=species,
    region='World', 
    inplace=True
)
print(len(df_fair))
#df_fair.head(50)

# %% cell 8
nt = df_fair.time_points.years()[-1] - 1750 + 1
nt

# %% cell 9
# drop beyond 2100
updated_config = copy.copy(config_list)
for i in range(len(config_list)):
    updated_config[i]['F_solar'] = updated_config[i]['F_solar'][:nt]
    updated_config[i]['F_volcanic'] = updated_config[i]['F_volcanic'][:nt]
    updated_config[i]['natural'] = updated_config[i]['natural'][:nt]

# %% cell 10
# need parallel FaIR in openscm-runner

x = run(
    climate_models_cfgs={
        "FAIR": updated_config,
    },
    scenarios=df_fair,
    output_variables=(
        "Surface Air Temperature Change",
        "Atmospheric Concentrations|CO2",
        "Atmospheric Concentrations|CH4",
        "Atmospheric Concentrations|N2O",
        "Effective Radiative Forcing",
        "Effective Radiative Forcing|CO2",
        "Effective Radiative Forcing|CH4",
        "Effective Radiative Forcing|N2O",
        "Effective Radiative Forcing|Greenhouse Gases",
        "Effective Radiative Forcing|Tropospheric Ozone",
        "Effective Radiative Forcing|CH4 Oxidation Stratospheric H2O",
        "Effective Radiative Forcing|Contrails",
        "Effective Radiative Forcing|Aerosols",
        "Effective Radiative Forcing|Aerosols|Direct Effect|BC",
        "Effective Radiative Forcing|Aerosols|Direct Effect|OC",
        "Effective Radiative Forcing|Aerosols|Direct Effect|SOx",
        "Effective Radiative Forcing|Aerosols|Direct Effect|Nitrate",
        "Effective Radiative Forcing|Aerosols|Direct Effect",
        "Effective Radiative Forcing|Aerosols|Indirect Effect",
        "Effective Radiative Forcing|Black Carbon on Snow",
        "Effective Radiative Forcing|Land-use Change"
    ),
)

# %% cell 11
# convert to ScmRun for better plotting functionality
x = ScmRun(x.timeseries())

# %% cell 12
x.tail()

# %% cell 13
# co2 409.9
np.percentile(x.filter(variable="Atmospheric Concentrations|CO2", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 14
# ch4 1866.3
np.percentile(x.filter(variable="Atmospheric Concentrations|CH4", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 15
# n2o 332.1
np.percentile(x.filter(variable="Atmospheric Concentrations|N2O", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 16
# co2 1.90 2.16 2.41
# any differences to GHG forcing is as likely to be with the pre-industrial concentration as it is with FaIR itself
np.percentile(x.filter(variable="Effective Radiative Forcing|CO2", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 17
# ch4 0.43 0.54 0.65
np.percentile(x.filter(variable="Effective Radiative Forcing|CH4", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 18
# n2o 0.18 0.21 0.24
np.percentile(x.filter(variable="Effective Radiative Forcing|N2O", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 19
# other wmghg 0.33 0.41 0.49
np.percentile(
    (
        x.filter(variable="Effective Radiative Forcing|Greenhouse Gases", scenario='ssp245', year=2019).timeseries().values.squeeze() - 
        x.filter(variable="Effective Radiative Forcing|CO2", scenario='ssp245', year=2019).timeseries().values.squeeze() -
        x.filter(variable="Effective Radiative Forcing|CH4", scenario='ssp245', year=2019).timeseries().values.squeeze() -
        x.filter(variable="Effective Radiative Forcing|N2O", scenario='ssp245', year=2019).timeseries().values.squeeze()
    )
, (5, 50, 95))

# %% cell 20
x.filter(variable="Effective Radiative Forcing|N2O", scenario='ssp245', year=2019).timeseries()

# %% cell 21
# n2o 0.18 0.21 0.24
np.percentile(x.filter(variable="Effective Radiative Forcing|N2O", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 22
# o3 0.24 0.47 0.71
np.percentile(x.filter(variable="Effective Radiative Forcing|Tropospheric Ozone", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 23
# h2o 0 0.05 0.10
np.percentile(x.filter(variable="Effective Radiative Forcing|CH4 Oxidation Stratospheric H2O", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 24
# ERFaer -0.6 -0.3 -0.0
np.percentile(x.filter(variable="Effective Radiative Forcing|Aerosols|Direct Effect", scenario='ssp245', year=np.arange(2005,2015)).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 25
# ERFaci -1.7 -1.0 -0.3   - very hard to get
np.percentile(x.filter(variable="Effective Radiative Forcing|Aerosols|Indirect Effect", scenario='ssp245', year=np.arange(2005,2015)).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 26
# BC Snow 0.02 0.08 0.18
np.percentile(x.filter(variable="Effective Radiative Forcing|Black Carbon on Snow", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 27
# Land use -0.30 -0.20 -0.10
np.percentile(x.filter(variable="Effective Radiative Forcing|Land-use Change", scenario='ssp245', year=2019).timeseries().values.squeeze(), (5, 50, 95))

# %% cell 28
config_list[0]['scale']

# %% cell 29
scale_normals = np.load('../data_input_large/fair-samples/scale_normals.npy')
scale_normals[838]
