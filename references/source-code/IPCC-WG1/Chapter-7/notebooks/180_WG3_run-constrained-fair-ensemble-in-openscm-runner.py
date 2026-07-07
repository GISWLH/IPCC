# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/180_WG3_run-constrained-fair-ensemble-in-openscm-runner.ipynb

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
from scmdata.plotting import RCMIP_SCENARIO_COLOURS

# %% cell 3
openscm_runner.__version__

# %% cell 4
fair = FAIR()
fair.get_version()

# %% cell 5
with open('../data_output_large/fair-samples/fair-1.6.2-wg3-params.json') as f:
    config_list = json.load(f)

# %% cell 6
# what a pain

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
    scenario=['ssp119','ssp126','ssp245','ssp370','ssp434','ssp460','ssp534-over','ssp585'], 
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
# # add in natural emissions and natural forcing
# ch4_n2o_df = pd.read_csv('../data/cmip6_natural_ch4_n2o.csv')
# ch4_n2o = ch4_n2o_df.values[:nt,1:]
# sol_vol_df = pd.read_csv('../data/cmip6_natural_forcing.csv')
# solar_forcing = sol_vol_df.values[:nt,1]
# volcanic_forcing = sol_vol_df.values[:nt,2]

# %% cell 10
#config_list[0]

# %% cell 11
# drop beyond 2100
updated_config = copy.copy(config_list)
for i in range(len(config_list)):
    updated_config[i]['F_solar'] = updated_config[i]['F_solar'][:nt]
    updated_config[i]['F_volcanic'] = updated_config[i]['F_volcanic'][:nt]
    updated_config[i]['natural'] = updated_config[i]['natural'][:nt]

# %% cell 12
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
        "Effective Radiative Forcing|Aerosols",
        "Effective Radiative Forcing|Aerosols|Direct Effect|BC",
        "Effective Radiative Forcing|Aerosols|Direct Effect|OC",
        "Effective Radiative Forcing|Aerosols|Direct Effect|SOx",
        "Effective Radiative Forcing|Aerosols|Direct Effect|Nitrate",
        "Effective Radiative Forcing|Aerosols|Direct Effect",
        "Effective Radiative Forcing|Aerosols|Indirect Effect",
        "Heat Uptake",
        "Heat Uptake|Ocean",
        "Airborne Fraction",
    ),
)

# %% cell 13
# convert to ScmRun for better plotting functionality
x = ScmRun(x.timeseries())

# %% cell 14
x.tail()

# %% cell 15
def new_timeseries(
    n=100,
    count=1,
    model="example",
    scenario="ssp119",
    variable="Surface Temperature",
    unit="K",
    region="World",
    cls=ScmRun,
    **kwargs,
):
    data = np.random.rand(n, count) * np.arange(n)[:, np.newaxis]
    index = 2000 + np.arange(n)
    return cls(
        data,
        columns={
            "model": model,
            "scenario": scenario,
            "variable": variable,
            "region": region,
            "unit": unit,
            **kwargs,
        },
        index=index,
    )

# %% cell 16
# save output to netCDF
x.to_nc('../data_output_large/fair-samples/ssp_emissions_driven_runs.nc', dimensions=["run_id", "scenario", "model"])

# %% cell 17
x = ScmRun.from_nc('../data_output_large/fair-samples/ssp_emissions_driven_runs.nc')

# %% cell 18
plt.rcParams['font.size'] = 14
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
# x.filter(variable="Surface Temperature").relative_to_ref_period_mean(year=range(1985,2005)).lineplot(
#     hue="scenario", style="model", ax=ax, time_axis="year", palette=RCMIP_SCENARIO_COLOURS,
#     hue_order=RCMIP_SCENARIO_COLOURS.keys(),
# )
x.filter(variable="Surface Air Temperature Change").relative_to_ref_period_mean(year=range(1850,1900)).lineplot(
    hue="scenario",
    ax=ax,
    time_axis="year",
    palette=RCMIP_SCENARIO_COLOURS,
    hue_order=RCMIP_SCENARIO_COLOURS.keys(),
)
ax.set_xlim(1850,2100)
#ax.axhline(0, color='k', ls=':')
ax.grid()
ax.set_title('SSP projections with FaIR: 1850-2100')
plt.tight_layout()

# %% cell 19
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Effective Radiative Forcing|Aerosols").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 20
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Effective Radiative Forcing|Aerosols|Direct Effect|BC").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 21
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Effective Radiative Forcing|Aerosols|Direct Effect|OC").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 22
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Effective Radiative Forcing|Aerosols|Direct Effect|SOx").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 23
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Effective Radiative Forcing|Aerosols|Direct Effect|Nitrate").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 24
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Effective Radiative Forcing|Aerosols|Direct Effect").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 25
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Effective Radiative Forcing|Aerosols|Indirect Effect").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 26
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Atmospheric Concentrations|CO2").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 27
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Atmospheric Concentrations|CH4").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 28
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Atmospheric Concentrations|N2O").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 29
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Heat Uptake").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 30
ax = plt.figure(figsize=(12, 7)).add_subplot(111)
x.filter(variable="Airborne Fraction").lineplot(
    hue="scenario", style="model", ax=ax, time_axis="year"
)

# %% cell 31
x.filter(scenario='ssp119', variable="Atmospheric Concentrations|CO2").timeseries()

# %% cell 32
x.filter(variable="Atmospheric Concentrations|N2O", scenario='ssp119', run_id=0).timeseries().values.squeeze()[264]

# %% cell 33
x.filter(variable="Atmospheric Concentrations|CH4", scenario='ssp119', run_id=0).timeseries().values.squeeze()[264]
