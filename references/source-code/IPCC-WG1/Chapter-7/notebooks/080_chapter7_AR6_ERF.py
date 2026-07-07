# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/080_chapter7_AR6_ERF.ipynb

# %% cell 2
import fair
import json
import numpy as np
from fair.constants import molwt
from fair.forcing.bc_snow import linear
from fair.forcing.landuse import cumulative
from fair.forcing.ghg import etminan, meinshausen
from fair.tools.magicc import scen_open
from scipy.interpolate import interp1d
import scipy.stats as st
import pandas as pd

import matplotlib.pyplot as pl
from tqdm.notebook import tqdm
from ar6.utils.h5 import save_dict_to_hdf5
from ar6.forcing.aerosol import aerocom_n, ghan
from ar6.forcing.ozone import eesc
from ar6.constants.gases import rcmip_to_ghg_names, ods_species, radeff
from ar6.constants import NINETY_TO_ONESIGMA

# %% cell 3
forcing = {}
scenario = 'ssp245'  # for where decisions are scenario-dependent
samples = 100000
with open('../data_input/random_seeds.json', 'r') as filehandle:
    SEEDS = json.load(filehandle)

# %% cell 4
emissions = pd.read_csv('../data_input_large/rcmip-emissions-annual-means-v5-1-0.csv')
df_emissions = pd.concat([emissions.loc[(
        (emissions.Variable=='Emissions|BC')|
        (emissions.Variable=='Emissions|OC')|
        (emissions.Variable=='Emissions|Sulfur')|
        (emissions.Variable=='Emissions|NOx')|
        (emissions.Variable=='Emissions|NH3')|
        (emissions.Variable=='Emissions|VOC')|
        (emissions.Variable=='Emissions|CO')
    ) & (emissions.Scenario=='ssp245') & (emissions.Region=='World'), 'Variable'], emissions.loc[(
        (emissions.Variable=='Emissions|BC')|
        (emissions.Variable=='Emissions|OC')|
        (emissions.Variable=='Emissions|Sulfur')|
        (emissions.Variable=='Emissions|NOx')|
        (emissions.Variable=='Emissions|NH3')|
        (emissions.Variable=='Emissions|VOC')|
        (emissions.Variable=='Emissions|CO')
    ) & (emissions.Scenario=='ssp245') & (emissions.Region=='World'), '1750':'2100']], axis=1)#.interpolate(axis=1).T
df_emissions.set_index('Variable', inplace=True)
df_emissions = df_emissions.interpolate(axis=1).T
df_emissions.rename(
    columns={
        'Emissions|BC': 'BC',
        'Emissions|OC': 'OC',
        'Emissions|Sulfur': 'SO2',
        'Emissions|NOx': 'NOx',
        'Emissions|NH3': 'NH3',
        'Emissions|VOC': 'VOC',
        'Emissions|CO': 'CO'
    }, inplace=True
)
# only keep cols we want
emissions = df_emissions[['SO2', 'BC', 'OC', 'NH3', 'NOx', 'VOC', 'CO']]
emissions.index = emissions.index.astype('int')
emissions.index.name='year'
emissions.columns.name=None

emissions_ceds_update = emissions.copy()

emissions_old = pd.read_csv('../data_input_large/rcmip-emissions-annual-means-v5-1-0.csv')
df_emissions = pd.concat([emissions_old.loc[(
        (emissions_old.Variable=='Emissions|BC|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|OC|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|Sulfur|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|NOx|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|NH3|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|VOC|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|CO|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|BC|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|OC|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|Sulfur|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|NOx|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|NH3|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|VOC|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|CO|MAGICC AFOLU|Agriculture')
    ) & (emissions_old.Scenario=='ssp245') & (emissions_old.Region=='World'), 'Variable'], emissions_old.loc[(
        (emissions_old.Variable=='Emissions|BC|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|OC|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|Sulfur|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|NOx|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|NH3|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|VOC|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|CO|MAGICC Fossil and Industrial')|
        (emissions_old.Variable=='Emissions|BC|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|OC|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|Sulfur|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|NOx|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|NH3|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|VOC|MAGICC AFOLU|Agriculture')|
        (emissions_old.Variable=='Emissions|CO|MAGICC AFOLU|Agriculture')
    ) & (emissions_old.Scenario=='ssp245') & (emissions_old.Region=='World'), '1750':'2100']], axis=1)#.interpolate(axis=1).T
df_emissions.set_index('Variable', inplace=True)
df_emissions = df_emissions.interpolate(axis=1).T
for species in ['BC', 'OC', 'Sulfur', 'NOx', 'NH3', 'VOC', 'CO']:
    df_emissions[species] = df_emissions['Emissions|{}|MAGICC Fossil and Industrial'.format(species)] + df_emissions['Emissions|{}|MAGICC AFOLU|Agriculture'.format(species)]
df_emissions.rename(columns = {'Sulfur': 'SO2'}, inplace=True)
df_emissions.drop(columns=[
        'Emissions|BC|MAGICC Fossil and Industrial',
        'Emissions|OC|MAGICC Fossil and Industrial',
        'Emissions|Sulfur|MAGICC Fossil and Industrial',
        'Emissions|NOx|MAGICC Fossil and Industrial',
        'Emissions|NH3|MAGICC Fossil and Industrial',
        'Emissions|VOC|MAGICC Fossil and Industrial',
        'Emissions|CO|MAGICC Fossil and Industrial',
        'Emissions|BC|MAGICC AFOLU|Agriculture',
        'Emissions|OC|MAGICC AFOLU|Agriculture',
        'Emissions|Sulfur|MAGICC AFOLU|Agriculture',
        'Emissions|NOx|MAGICC AFOLU|Agriculture',
        'Emissions|NH3|MAGICC AFOLU|Agriculture',
        'Emissions|VOC|MAGICC AFOLU|Agriculture',
        'Emissions|CO|MAGICC AFOLU|Agriculture',
    ],
    inplace=True
)
df_emissions.index = emissions.index.astype('int')
df_emissions.index.name='year'
df_emissions.columns.name=None

global_total = {}
for species in ['BC', 'OC', 'SO2', 'NH3', 'NOx', 'NMVOC', 'CO']:
    df = pd.read_csv('../data_input_large/CEDS_v_2020_09_11_emissions/{}_global_CEDS_emissions_by_sector_2020_09_11.csv'.format(species))
    global_total[species] = df.sum(axis=0).values[3:].astype(float) / 1000 # yes could get openscm on this
    #unit = df.units[0]
    #print(unit)
global_total['VOC'] = global_total.pop('NMVOC')
new_ceds = pd.DataFrame(global_total)
new_ceds.index = np.arange(1750,2020)
new_ceds.index = new_ceds.index.astype('int')
new_ceds.index.name='year'
new_ceds.columns.name=None
emissions_ceds_update = new_ceds.loc[1750:2020] + emissions - df_emissions
emissions_ceds_update.drop(index=range(2020,2101), inplace=True)
emissions_ceds_update

# %% cell 5
emissions_ceds_update.loc[1980:]

# %% cell 6
emissions_ceds_update.to_csv('../data_output/emissions_ceds_update_plus_bb.csv')

# %% cell 7
seed    = 36572 

# to do move to module

# these are standard deviations of the scale factor for normally distributed forcings (mean = 1). The list below is expressed in terms of 5-95% ranges.
unc_ranges = np.array([
    0.12,      # CO2
    0.20,      # CH4: updated value from etminan 2016
    0.14,      # N2O
    0.19,      # other WMGHGs
    0.50,      # Total ozone
    1.00,      # stratospheric WV from CH4
    0.70,      # contrails approx - half-normal
    1.25,      # bc on snow - half-normal
    0.50,      # land use change
    5.0/20.0,  # volcanic
    0.50,      # solar (amplitude)
])/NINETY_TO_ONESIGMA

scale = st.norm.rvs(size=(samples,11), loc=np.ones((samples,11)), scale=np.ones((samples, 11)) * unc_ranges[None,:], random_state=seed)
#scale[:,8] = st.lognorm.rvs(0.5, size=samples, random_state=seed+1)
# refine this calc and maybe half normal it

# here's a half normal
## bc snow is asymmetric Gaussian. We can just scale the half of the distribution above/below best estimate
scale[scale[:,7]<1,7] = 0.08/0.1*(scale[scale[:,7]<1,7]-1) + 1

## so is contrails - the benefits of doing this are tiny :)
scale[scale[:,6]<1,6] = 0.0384/0.0406*(scale[scale[:,6]<1,6]-1) + 1

trend_solar = st.norm.rvs(size=samples, loc=+0.01, scale=0.07/NINETY_TO_ONESIGMA, random_state=138294)
#trend_solar[trend_solar>-0.01] = 11/4 * (trend_solar[trend_solar>-0.01]+0.01)-0.01

scale_df = pd.DataFrame(
    data = scale,
    columns = ['co2','ch4','n2o','other_wmghg','o3','h2o_stratospheric','contrails','bc_on_snow','land_use','volcanic','solar']
)

# %% cell 9
pl.hist(trend_solar)
np.percentile(trend_solar,(5,50,95))

# %% cell 10
# get solar forcing from CMIP6 TSI time series
df = pd.read_csv('../data_output/solar_erf.csv', index_col='year')
forcing['solar'] = np.zeros((270, samples))
forcing['solar'] = df.solar_erf.loc[1750:2019]

# %% cell 12
df = pd.read_csv('../data_output/volcanic_erf.csv', index_col='year')
forcing['volcanic'] = df.volcanic_erf.loc[1750:2019]

# %% cell 15
df = pd.read_csv('../data_input_large/ERFaci_samples.csv')
aci_coeffs = np.exp(df.values)

NINETY_TO_ONESIGMA = st.norm.ppf(0.95)

# SCALE TO ASSESSMENT
ERFari_scale = st.norm.rvs(loc=-0.30, scale=0.30/NINETY_TO_ONESIGMA, size=samples, random_state=786418)
ERFaci_scale = st.norm.rvs(loc=-1.00, scale=0.70/NINETY_TO_ONESIGMA, size=samples, random_state=31318990)

ERFari = np.zeros((270,samples))
ERFaci = np.zeros((270,samples))
    
bc = emissions_ceds_update['BC'].values.squeeze()
oc = emissions_ceds_update['OC'].values.squeeze()
so2 = emissions_ceds_update['SO2'].values.squeeze()
nh3 = emissions_ceds_update['NH3'].values.squeeze()

for i in tqdm(range(samples), leave=False):
    ts2010 = np.mean(
        ghan(
            [
                so2[255:265],
                    bc[255:265]+
                    oc[255:265],
            ], 1.11, aci_coeffs[i,0], aci_coeffs[i,1]
        )
    )
    ts1750 = ghan(
        [
            so2[0],
                bc[0]+
                oc[0],
        ], 1.11, aci_coeffs[i,0], aci_coeffs[i,1]
    )
    ERFaci[:,i] = (
        ghan([so2, bc+oc], 1.11, aci_coeffs[i,0], aci_coeffs[i,1])
    - ts1750)/(ts2010-ts1750)*ERFaci_scale[i]

# %% cell 16
bc_20101750 = st.norm.rvs(loc=0.3, scale=0.2/NINETY_TO_ONESIGMA, size=samples, random_state=SEEDS[95])
oc_20101750 = st.norm.rvs(loc=-0.09, scale=0.07/NINETY_TO_ONESIGMA, size=samples, random_state=SEEDS[96])
so2_20101750 = st.norm.rvs(loc=-0.4, scale=0.2/NINETY_TO_ONESIGMA, size=samples, random_state=SEEDS[97])
nh3_20101750 = st.norm.rvs(loc=-0.11, scale=0.05/NINETY_TO_ONESIGMA, size=samples, random_state=SEEDS[98])

beta_bc = bc_20101750/(np.mean(emissions_ceds_update.loc[2005:2014,'BC'])-emissions_ceds_update.loc[1750,'BC'])
beta_oc = oc_20101750/(np.mean(emissions_ceds_update.loc[2005:2014,'OC'])-emissions_ceds_update.loc[1750,'OC'])
beta_so2 = so2_20101750/(np.mean(emissions_ceds_update.loc[2005:2014,'SO2'])-emissions_ceds_update.loc[1750,'SO2'])
beta_nh3 = nh3_20101750/(np.mean(emissions_ceds_update.loc[2005:2014,'NH3'])-emissions_ceds_update.loc[1750,'NH3'])

ERFari = np.zeros((270, samples))
for i in tqdm(range(samples)):
    ERFari[:, i] = (
        (emissions_ceds_update.loc[:,'SO2']-emissions_ceds_update.loc[1750,'SO2']) * beta_so2[i] +
        (emissions_ceds_update.loc[:,'BC']-emissions_ceds_update.loc[1750,'BC']) * beta_bc[i] +
        (emissions_ceds_update.loc[:,'OC']-emissions_ceds_update.loc[1750,'OC']) * beta_oc[i] +
        (emissions_ceds_update.loc[:,'NH3']-emissions_ceds_update.loc[1750,'NH3']) * beta_nh3[i]
    )

# %% cell 17
beta_bc = 0.3/(np.mean(emissions_ceds_update.loc[2005:2014,'BC'])-emissions_ceds_update.loc[1750,'BC'])
beta_oc = -0.09/(np.mean(emissions_ceds_update.loc[2005:2014,'OC'])-emissions_ceds_update.loc[1750,'OC'])
beta_so2 = -0.4/(np.mean(emissions_ceds_update.loc[2005:2014,'SO2'])-emissions_ceds_update.loc[1750,'SO2'])
beta_nh3 = -0.11/(np.mean(emissions_ceds_update.loc[2005:2014,'NH3'])-emissions_ceds_update.loc[1750,'NH3'])

print(beta_bc, beta_oc, beta_so2, beta_nh3)

ERFari_median = (
        (emissions_ceds_update.loc[:,'SO2']-emissions_ceds_update.loc[1750,'SO2']) * beta_so2 +
        (emissions_ceds_update.loc[:,'BC']-emissions_ceds_update.loc[1750,'BC']) * beta_bc +
        (emissions_ceds_update.loc[:,'OC']-emissions_ceds_update.loc[1750,'OC']) * beta_oc +
        (emissions_ceds_update.loc[:,'NH3']-emissions_ceds_update.loc[1750,'NH3']) * beta_nh3 
    )

# %% cell 18
ERFaci_median = np.percentile(ERFaci, 50, axis=1) * (-1.0)/(np.percentile(ERFaci, 50, axis=1)[255:265].mean())

# %% cell 19
ERFari_median[-15:-5].mean()

# %% cell 20
ERFaci_median[-15:-5].mean()

# %% cell 21
pl.fill_between(np.arange(1750, 2020), np.percentile(ERFari, 5, axis=1), np.percentile(ERFari, 95, axis=1), color='k', alpha=0.5)
pl.plot(np.arange(1750,2020), np.percentile(ERFari, 50, axis=1), color='k')

# %% cell 22
pl.fill_between(np.arange(1750, 2020), np.percentile(ERFaci, 5, axis=1), np.percentile(ERFaci, 95, axis=1), color='k', alpha=0.5)
pl.plot(np.arange(1750,2020), np.percentile(ERFaci, 50, axis=1), color='k')

# %% cell 23
pl.fill_between(np.arange(1750, 2020), np.percentile(ERFari+ERFaci, 5, axis=1), np.percentile(ERFari+ERFaci, 95, axis=1), color='k', alpha=0.5)
pl.plot(np.arange(1750,2020), np.percentile(ERFari+ERFaci, 50, axis=1), color='k')

# %% cell 24
forcing['aerosol-radiation_interactions'] = ERFari_median
forcing['aerosol-cloud_interactions'] = ERFaci_median
forcing['aerosol'] = forcing['aerosol-radiation_interactions'] + forcing['aerosol-cloud_interactions']
print(forcing['aerosol'][255:265].mean())
pl.plot(forcing['aerosol'])

# %% cell 25
forcing['aerosol'][-15:]

# %% cell 27
df = pd.read_csv('../data_input_large/CEDS_v_2020_09_11_emissions/NOx_global_CEDS_emissions_by_sector_2020_09_11.csv')
avi_nox_hist = df[df.sector.str.endswith("aviation")].loc[:,'X1750':'X2019']
avi_nox_hist

# %% cell 28
avi_nox_1750_2019 = (avi_nox_hist.sum(axis=0)/1000.).values
contrail_forcing_2018 = 0.0574
forcing['contrails'] = (avi_nox_1750_2019/avi_nox_1750_2019[268] * contrail_forcing_2018)#[:,None] * scale_df['contrails'][None,:]
#pl.plot(np.arange(1750,2020), np.percentile(forcing['contrails'], 95, axis=1))
#pl.plot(np.arange(1750,2020), np.median(forcing['contrails'], axis=1))
#pl.plot(np.arange(1750,2020), np.percentile(forcing['contrails'], 5, axis=1))
forcing['contrails'][-1]

# %% cell 30
emissions = pd.read_csv('../data_input_large/rcmip-emissions-annual-means-v5-1-0.csv')
ghimire = pd.read_csv('../data_input/Ghimire_et_al_2014_GRL/ghimire_curve_fit.csv')
landuse_co2 = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|CO2|MAGICC AFOLU'),'1750':'2020'].interpolate(axis=1, pad=True).values

# %% cell 31
lusf2019 = -0.15/np.cumsum(landuse_co2)  # include irrigation of -0.05 in Sherwood et al
landuse_erf = np.cumsum(landuse_co2)*lusf2019
f = interp1d(ghimire['year'], ghimire['flux'], kind='linear', fill_value='extrapolate', bounds_error=False)
lusf2019 = -0.20/(f(2019)-f(1750))
forcing['land_use'] = lusf2019*(f(np.arange(1750,2020))-f(1750))#[:,None] * scale_df['land_use'][None,:]

# %% cell 33
df = pd.read_csv('../data_input_large/CEDS_v_2020_09_11_emissions/BC_global_CEDS_emissions_by_sector_2020_09_11.csv')
bc_hist = df.loc[:,'X1750':'X2019'].sum(axis=0).values/1000.
bc_hist

forcing['bc_on_snow'] = (0.08*(bc_hist[:270]-bc_hist[0])/(bc_hist[269]-bc_hist[0]))#[:,None] * scale_df['bc_on_snow'][None,:]

# %% cell 35
ghg_obs = pd.read_excel('../data_input/observations/LLGHG_history_AR6_v9_for_archive.xlsx', skiprows=22, sheet_name="mixing_ratios", index_col=0)
for addyear in range(1751,1850):
    ghg_obs.loc[addyear, 'YYYY'] = np.nan
ghg_obs = ghg_obs.sort_index()

# For C8F18 there appears to be an error in the spreadsheet where 2015 is entered as zero, presumably 0.09 but treat as missing
ghg_obs.loc[2015, 'C8F18'] = np.nan

# For gases with no observations before the recent past, fill with zeros.
# Unfortunately, this is a bit case-by-case.
# While these gases probably were emitted before the first year they appear in the data, their omission in forcing terms is
# likely to be negligible.
ghg_obs.loc[:1989, 'i-C6F14'] = ghg_obs.loc[:1989, 'i-C6F14'].fillna(0)
ghg_obs.loc[:1977, 'CFC-112'] = ghg_obs.loc[:1977, 'CFC-112'].fillna(0)
ghg_obs.loc[:1998, 'CFC-112a'] = ghg_obs.loc[:1998, 'CFC-112a'].fillna(0)
ghg_obs.loc[:1977, 'CFC-113a'] = ghg_obs.loc[:1977, 'CFC-113a'].fillna(0)
ghg_obs.loc[:1977, 'CFC-114a'] = ghg_obs.loc[:1977, 'CFC-114a'].fillna(0)
ghg_obs.loc[:1979, 'HCFC-133a'] = ghg_obs.loc[:1979, 'HCFC-133a'].fillna(0)
ghg_obs.loc[:1999, 'HCFC-31'] = ghg_obs.loc[:1999, 'HCFC-31'].fillna(0)
ghg_obs.loc[:2003, 'HCFC-124'] = ghg_obs.loc[:2003, 'HCFC-124'].fillna(0)

# For gases with missing observations in the last few years we use the last available year (usually 2015)
ghg_obs = ghg_obs.interpolate()
ghg_obs

# %% cell 36
gases = ghg_obs.columns.to_list()
gases.remove('YYYY')

# %% cell 37
forcing['co2'] = np.zeros((270,samples))
forcing['ch4'] = np.zeros((270,samples))
forcing['n2o'] = np.zeros((270,samples))
co2base = np.zeros(270)
ch4base = np.zeros(270)
n2obase = np.zeros(270)
c = np.array([ghg_obs['CO2'].values, ghg_obs['CH4'].values, ghg_obs['N2O'].values])
for i, year in enumerate(range(1750,2020)):
    co2base[i], ch4base[i], n2obase[i] = meinshausen(c[:,i], [ghg_obs.loc[1750,'CO2'], ghg_obs.loc[1750,'CH4'], ghg_obs.loc[1750,'N2O']], scale_F2x=False)

# include rapid adjustments for CO2 and CH4 (FOD numbers):
forcing['co2'] = 1.05 * co2base
forcing['ch4'] = 0.86 * ch4base
forcing['n2o'] = 1.07 * n2obase

# %% cell 38
trop_adjustment_scale = radeff.copy()
for key in trop_adjustment_scale.keys():
    trop_adjustment_scale[key] = 1
trop_adjustment_scale['CFC-11'] = 1.13
trop_adjustment_scale['CFC-12'] = 1.12

otherghgbase = np.zeros(270)
for gas in gases[3:]:
    forcing[gas] = (ghg_obs.loc[:,gas] - ghg_obs.loc[1750,gas]).values * radeff[gas] * 0.001 * trop_adjustment_scale[gas]
    otherghgbase = otherghgbase + forcing[gas]
forcing['other_wmghg'] = otherghgbase

# %% cell 40
o3_df = pd.read_csv('../data_output/o3_erf.csv')
forcing['o3'] = o3_df['o3_erf'].values[:270]

# %% cell 42
forcing['ch4'].shape

# %% cell 43
sfh2ostrat = 0.05 / forcing['ch4'][269]
#forcing['h2o_strat'] = (forcing['ch4'] * sfh2ostrat[None,:]) * scale_df['h2o_stratospheric'][None,:]
forcing['h2o_stratospheric'] = (forcing['ch4'] * sfh2ostrat)
forcing['h2o_stratospheric'].shape

# %% cell 44
# solar forcing will use the averages of the solar cycles from 1745 to 1765 as the baseline: this is a different treatment to CMIP6
fig, ax = pl.subplots(4,4, figsize=(16,16),squeeze=True)
ax[0,0].plot(np.arange(1750,2020),forcing['co2'])
ax[0,0].set_title('CO2')
ax[0,1].plot(np.arange(1750,2020),forcing['ch4'])
ax[0,1].set_title('CH4')
ax[0,2].plot(np.arange(1750,2020),forcing['n2o'])
ax[0,2].set_title('N2O')
ax[0,3].plot(np.arange(1750,2020),forcing['other_wmghg'])
ax[0,3].set_title('Other WMGHGs')
ax[1,0].plot(np.arange(1750,2020),forcing['o3'])
ax[1,0].set_title('O3')
ax[1,1].plot(np.arange(1750,2020),forcing['h2o_stratospheric'])
ax[1,1].set_title('H2O stratospheric')
ax[1,2].plot(np.arange(1750,2020),forcing['contrails'])
ax[1,2].set_title('contrails')
ax[1,3].plot(np.arange(1750,2020),forcing['aerosol-radiation_interactions'])
ax[1,3].set_title('ERFari')
ax[2,0].plot(np.arange(1750,2020),forcing['aerosol-cloud_interactions'])
ax[2,0].set_title('ERFaci')
ax[2,1].plot(np.arange(1750,2020),forcing['bc_on_snow'])
ax[2,1].set_title('BC on snow')
ax[2,2].plot(np.arange(1750,2020),forcing['land_use'])
ax[2,2].set_title('land use')
ax[2,3].plot(np.arange(1750,2020),forcing['volcanic'])
ax[2,3].set_title('volcanic')
ax[3,0].plot(np.arange(1750,2020),forcing['solar'])
ax[3,0].set_title('solar')

# %% cell 45
forcing['nonco2_wmghg'] = forcing['ch4'] + forcing['n2o'] + forcing['other_wmghg']
forcing['aerosol'] = forcing['aerosol-radiation_interactions'] + forcing['aerosol-cloud_interactions']
forcing['chapter2_other_anthro'] = ( 
                  forcing['h2o_stratospheric'] + 
                  forcing['contrails'] + 
                  forcing['bc_on_snow'] +
                  forcing['land_use']
)
forcing['total_anthropogenic']=forcing['co2']+forcing['ch4']+forcing['n2o']+\
    forcing['other_wmghg']+\
    forcing['o3']+forcing['h2o_stratospheric']+forcing['contrails']+\
    forcing['aerosol-radiation_interactions']+forcing['aerosol-cloud_interactions']+forcing['bc_on_snow']+forcing['land_use']
forcing['total_natural']=forcing['volcanic']+forcing['solar']
forcing['total']=forcing['total_anthropogenic']+forcing['total_natural']

# %% cell 46
pl.figure(figsize=(16,9))
pl.plot(np.arange(1750,2020), forcing['total'])
pl.yticks(np.arange(-4,3))
pl.xticks(np.arange(1750,2020,50))
pl.ylim(-4,3)
pl.xlim(1750,2020)
pl.grid()

# %% cell 47
#np.percentile(forcing['total'][-1,:],(5,50,95))
#np.percentile(forcing['total_anthropogenic'][-1,:],(5,50,95))

# %% cell 48
df = pd.DataFrame(data=forcing, index=np.arange(1750,2020))
df.index.name = 'year'
df=df[['co2','ch4','n2o','other_wmghg','o3','h2o_stratospheric','contrails','aerosol-radiation_interactions','aerosol-cloud_interactions','bc_on_snow','land_use',
  'volcanic','solar','nonco2_wmghg','aerosol','chapter2_other_anthro',
'total_anthropogenic','total_natural','total']]
df.to_csv('../data_output/AR6_ERF_1750-2019.csv')
df

# %% cell 49
df.loc[2000:2020]

# %% cell 50
df = pd.DataFrame(data=forcing, index=np.arange(1750,2020))
df.index.name='year'
df=df[gases[3:]]
df.to_csv('../data_output/AR6_ERF_minorGHGs_1750-2019.csv')
df

# %% cell 52
forcing_ensemble = {}
df = pd.DataFrame(data=forcing, index=np.arange(1750,2020))
df.index.name = 'year'
df=df[['co2','ch4','n2o','other_wmghg','o3','h2o_stratospheric','contrails','aerosol-radiation_interactions','aerosol-cloud_interactions','bc_on_snow','land_use',
  'volcanic','solar','total_anthropogenic','total_natural','total']]

forcing_ensemble['co2'] = df['co2'].values[:,None] * scale_df['co2'].values[None,:]
forcing_ensemble['ch4'] = df['ch4'].values[:,None] * scale_df['ch4'].values[None,:]
forcing_ensemble['n2o'] = df['n2o'].values[:,None] * scale_df['n2o'].values[None,:]
forcing_ensemble['other_wmghg'] = df['other_wmghg'].values[:,None] * scale_df['other_wmghg'].values[None,:]
forcing_ensemble['o3'] = df['o3'].values[:,None] * scale_df['o3'].values[None,:]
forcing_ensemble['h2o_stratospheric'] = df['h2o_stratospheric'].values[:,None] * scale_df['h2o_stratospheric'].values[None,:]
forcing_ensemble['contrails'] = df['contrails'].values[:,None] * scale_df['contrails'].values[None,:]
forcing_ensemble['aerosol-radiation_interactions'] = ERFari
forcing_ensemble['aerosol-cloud_interactions'] = ERFaci
forcing_ensemble['bc_on_snow'] = df['bc_on_snow'].values[:,None] * scale_df['bc_on_snow'].values[None,:]
forcing_ensemble['land_use'] = df['land_use'].values[:,None] * scale_df['land_use'].values[None,:]
forcing_ensemble['volcanic'] = df['volcanic'].values[:,None] * scale_df['volcanic'].values[None,:]
forcing_ensemble['solar'] = np.linspace(0, trend_solar, 270) + df['solar'].values[:,None] * scale_df['solar'].values[None,:]

# %% cell 53
# solar forcing_ensemble will use the averages of the solar cycles from 1745 to 1765 as the baseline: this is a different treatment to CMIP6
fig, ax = pl.subplots(4,4, figsize=(16,16),squeeze=True)
ax[0,0].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['co2'],5,axis=1),np.percentile(forcing_ensemble['co2'],95,axis=1), alpha=0.3)
ax[0,0].plot(np.arange(1750,2020),np.median(forcing_ensemble['co2'],axis=1))
ax[0,0].set_title('CO2')
ax[0,1].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['ch4'],5,axis=1),np.percentile(forcing_ensemble['ch4'],95,axis=1), alpha=0.3)
ax[0,1].plot(np.arange(1750,2020),np.median(forcing_ensemble['ch4'],axis=1))
ax[0,1].set_title('CH4')
ax[0,2].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['n2o'],5,axis=1),np.percentile(forcing_ensemble['n2o'],95,axis=1), alpha=0.3)
ax[0,2].plot(np.arange(1750,2020),np.median(forcing_ensemble['n2o'],axis=1))
ax[0,2].set_title('N2O')
ax[0,3].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['other_wmghg'],5,axis=1),np.percentile(forcing_ensemble['other_wmghg'],95,axis=1), alpha=0.3)
ax[0,3].plot(np.arange(1750,2020),np.median(forcing_ensemble['other_wmghg'],axis=1))
ax[0,3].set_title('Other WMGHGs')
ax[1,0].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['o3'],5,axis=1),np.percentile(forcing_ensemble['o3'],95,axis=1), alpha=0.3)
ax[1,0].plot(np.arange(1750,2020),np.median(forcing_ensemble['o3'],axis=1))
ax[1,0].set_title('O3')
ax[1,1].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['h2o_stratospheric'],5,axis=1),np.percentile(forcing_ensemble['h2o_stratospheric'],95,axis=1), alpha=0.3)
ax[1,1].plot(np.arange(1750,2020),np.median(forcing_ensemble['h2o_stratospheric'],axis=1))
ax[1,1].set_title('H2O stratospheric')
ax[1,2].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['contrails'],5,axis=1),np.percentile(forcing_ensemble['contrails'],95,axis=1), alpha=0.3)
ax[1,2].plot(np.arange(1750,2020),np.median(forcing_ensemble['contrails'],axis=1))
ax[1,2].set_title('contrails')
ax[1,3].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['aerosol-radiation_interactions'],5,axis=1),np.percentile(forcing_ensemble['aerosol-radiation_interactions'],95,axis=1), alpha=0.3)
ax[1,3].plot(np.arange(1750,2020),forcing['aerosol-radiation_interactions'])
ax[1,3].set_title('ERFari')
ax[2,0].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['aerosol-cloud_interactions'],5,axis=1),np.percentile(forcing_ensemble['aerosol-cloud_interactions'],95,axis=1), alpha=0.3)
ax[2,0].plot(np.arange(1750,2020),forcing['aerosol-cloud_interactions'])
ax[2,0].set_title('ERFaci')
ax[2,1].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['bc_on_snow'],5,axis=1),np.percentile(forcing_ensemble['bc_on_snow'],95,axis=1), alpha=0.3)
ax[2,1].plot(np.arange(1750,2020),np.median(forcing_ensemble['bc_on_snow'],axis=1))
ax[2,1].set_title('BC on snow')
ax[2,2].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['land_use'],5,axis=1),np.percentile(forcing_ensemble['land_use'],95,axis=1), alpha=0.3)
ax[2,2].plot(np.arange(1750,2020),np.median(forcing_ensemble['land_use'],axis=1))
ax[2,2].set_title('land use')
ax[2,3].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['volcanic'],5,axis=1),np.percentile(forcing_ensemble['volcanic'],95,axis=1), alpha=0.3)
ax[2,3].plot(np.arange(1750,2020),np.median(forcing_ensemble['volcanic'],axis=1))
ax[2,3].set_title('volcanic')
ax[3,0].fill_between(np.arange(1750,2020),np.percentile(forcing_ensemble['solar'],5,axis=1),np.percentile(forcing_ensemble['solar'],95,axis=1), alpha=0.3)
ax[3,0].plot(np.arange(1750,2020),np.median(forcing_ensemble['solar'],axis=1))
ax[3,0].set_title('solar')

# %% cell 54
print(np.percentile(forcing_ensemble['aerosol-radiation_interactions'],5,axis=1)[255:265].mean())
print(np.percentile(forcing_ensemble['aerosol-radiation_interactions'],95,axis=1)[255:265].mean())
print(np.percentile(forcing_ensemble['aerosol-cloud_interactions'],5,axis=1)[255:265].mean())
print(np.percentile(forcing_ensemble['aerosol-cloud_interactions'],95,axis=1)[255:265].mean())

forcing_ensemble['total']=(forcing_ensemble['co2'] +
                  forcing_ensemble['ch4'] +
                  forcing_ensemble['n2o'] +
                  forcing_ensemble['other_wmghg'] +
                  forcing_ensemble['o3'] +
                  forcing_ensemble['h2o_stratospheric'] + 
                  forcing_ensemble['contrails'] + 
                  forcing_ensemble['bc_on_snow'] +
                  forcing_ensemble['land_use'] +
                  forcing_ensemble['aerosol-radiation_interactions'] + 
                  forcing_ensemble['aerosol-cloud_interactions'] +
                  forcing_ensemble['solar'] +
                  forcing_ensemble['volcanic'])
forcing_ensemble['aerosol'] = (forcing_ensemble['aerosol-radiation_interactions'] + forcing_ensemble['aerosol-cloud_interactions'])
forcing_ensemble['nonco2_wmghg'] = (forcing_ensemble['ch4'] + forcing_ensemble['n2o'] + forcing_ensemble['other_wmghg'])
forcing_ensemble['chapter2_other_anthro'] = ( 
                  forcing_ensemble['h2o_stratospheric'] + 
                  forcing_ensemble['contrails'] + 
                  forcing_ensemble['bc_on_snow'] +
                  forcing_ensemble['land_use']
)
forcing_ensemble['total_natural'] = forcing_ensemble['solar'] + forcing_ensemble['volcanic']
forcing_ensemble['total_anthropogenic']=(forcing_ensemble['co2'] +
                  forcing_ensemble['ch4'] +
                  forcing_ensemble['n2o'] +
                  forcing_ensemble['other_wmghg'] +
                  forcing_ensemble['o3'] + 
                  forcing_ensemble['h2o_stratospheric'] + 
                  forcing_ensemble['contrails'] + 
                  forcing_ensemble['bc_on_snow'] +
                  forcing_ensemble['land_use'] +
                  forcing_ensemble['aerosol-radiation_interactions'] + 
                  forcing_ensemble['aerosol-cloud_interactions'])

# %% cell 55
df = pd.DataFrame(data=np.array([
    np.percentile(forcing_ensemble['co2'],5,axis=1),
    np.percentile(forcing_ensemble['ch4'],5,axis=1),
    np.percentile(forcing_ensemble['n2o'],5,axis=1),
    np.percentile(forcing_ensemble['other_wmghg'],5,axis=1),
    np.percentile(forcing_ensemble['o3'],5,axis=1),
    np.percentile(forcing_ensemble['h2o_stratospheric'],5,axis=1),
    np.percentile(forcing_ensemble['contrails'],5,axis=1),
    np.percentile(forcing_ensemble['aerosol-radiation_interactions'],5,axis=1),
    np.percentile(forcing_ensemble['aerosol-cloud_interactions'],5,axis=1),
    np.percentile(forcing_ensemble['bc_on_snow'],5,axis=1),
    np.percentile(forcing_ensemble['land_use'],5,axis=1),
    np.percentile(forcing_ensemble['volcanic'],5,axis=1),    
    np.percentile(forcing_ensemble['solar'],5,axis=1),
    np.percentile(forcing_ensemble['nonco2_wmghg'],5,axis=1),
    np.percentile(forcing_ensemble['aerosol'],5,axis=1),
    np.percentile(forcing_ensemble['chapter2_other_anthro'],5,axis=1),
    np.percentile(forcing_ensemble['total_anthropogenic'],5,axis=1),
    np.percentile(forcing_ensemble['total_natural'],5,axis=1),
    np.percentile(forcing_ensemble['total'],5,axis=1)
]).T, index=np.arange(1750,2020))
df.index.name = 'year'
df = df.rename(columns={
    0: 'co2',
    1: 'ch4',
    2: 'n2o',
    3: 'other_wmghg',
    4: 'o3',
    5: 'h2o_stratospheric',
    6: 'contrails',
    7: 'aerosol-radiation_interactions',
    8: 'aerosol-cloud_interactions',
    9:'bc_on_snow',
    10:'land_use',
    11:'volcanic',
    12:'solar',
    13:'nonco2_wmghg',
    14:'aerosol',
    15:'chapter2_other_anthro',
    16:'total_anthropogenic',
    17:'total_natural',
    18:'total'
})
df.to_csv('../data_output/AR6_ERF_1750-2019_pc05.csv')
df

# %% cell 56
df = pd.DataFrame(data=np.array([
    np.percentile(forcing_ensemble['co2'],95,axis=1),
    np.percentile(forcing_ensemble['ch4'],95,axis=1),
    np.percentile(forcing_ensemble['n2o'],95,axis=1),
    np.percentile(forcing_ensemble['other_wmghg'],95,axis=1),
    np.percentile(forcing_ensemble['o3'],95,axis=1),
    np.percentile(forcing_ensemble['h2o_stratospheric'],95,axis=1),
    np.percentile(forcing_ensemble['contrails'],95,axis=1),
    np.percentile(forcing_ensemble['aerosol-radiation_interactions'],95,axis=1),
    np.percentile(forcing_ensemble['aerosol-cloud_interactions'],95,axis=1),
    np.percentile(forcing_ensemble['bc_on_snow'],95,axis=1),
    np.percentile(forcing_ensemble['land_use'],95,axis=1),
    np.percentile(forcing_ensemble['volcanic'],95,axis=1),    
    np.percentile(forcing_ensemble['solar'],95,axis=1),
    np.percentile(forcing_ensemble['nonco2_wmghg'],95,axis=1),
    np.percentile(forcing_ensemble['aerosol'],95,axis=1),
    np.percentile(forcing_ensemble['chapter2_other_anthro'],95,axis=1),
    np.percentile(forcing_ensemble['total_anthropogenic'],95,axis=1),
    np.percentile(forcing_ensemble['total_natural'],95,axis=1),
    np.percentile(forcing_ensemble['total'],95,axis=1)
]).T, index=np.arange(1750,2020))
df.index.name = 'year'
#df=df[['co2','ch4','n2o','other_wmghg','o3_trop','other_anthro','aerosols','volcanic','solar','total']]
df = df.rename(columns={
    0: 'co2',
    1: 'ch4',
    2: 'n2o',
    3: 'other_wmghg',
    4: 'o3',
    5: 'h2o_stratospheric',
    6: 'contrails',
    7: 'aerosol-radiation_interactions',
    8: 'aerosol-cloud_interactions',
    9:'bc_on_snow',
    10:'land_use',
    11:'volcanic',
    12:'solar',
    13:'nonco2_wmghg',
    14:'aerosol',
    15:'chapter2_other_anthro',
    16:'total_anthropogenic',
    17:'total_natural',
    18:'total'
})
df.to_csv('../data_output/AR6_ERF_1750-2019_pc95.csv')
df

# %% cell 58
forcing['aerosol'].loc[2005:2014].mean()

# %% cell 59
forcing['total_anthropogenic'][2019] - forcing['aerosol'][2019] + forcing['aerosol'].loc[2005:2014].mean()

# %% cell 60
aerosol_wangle = np.percentile(
    forcing_ensemble['co2'][269]+
    forcing_ensemble['ch4'][269]+
    forcing_ensemble['n2o'][269]+
    forcing_ensemble['other_wmghg'][269]+
    forcing_ensemble['o3'][269]+
    forcing_ensemble['h2o_stratospheric'][269]+
    forcing_ensemble['contrails'][269]+
    forcing_ensemble['bc_on_snow'][269]+
    forcing_ensemble['land_use'][269]+
    forcing_ensemble['aerosol'][255:265,:].mean(axis=0)
,(5,95))
np.savetxt('../data_output/AR6_ERF_1750-PD_pc05pc95_anthro_assessed.csv', aerosol_wangle)
aerosol_wangle

# %% cell 61
forcing['total_anthropogenic'][2019]

# %% cell 62
np.percentile(forcing_ensemble['total_anthropogenic'][269], (5,95))

# %% cell 63
# all WMGHGs
np.percentile(
    forcing_ensemble['co2'][269] + 
    forcing_ensemble['ch4'][269] + 
    forcing_ensemble['n2o'][269] + 
    forcing_ensemble['other_wmghg'][269]
, (5,95))

# %% cell 64
# all GHGs and precursors
np.percentile(
    forcing_ensemble['co2'][269] + 
    forcing_ensemble['ch4'][269] + 
    forcing_ensemble['n2o'][269] + 
    forcing_ensemble['other_wmghg'][269] + 
    forcing_ensemble['o3'][269] +
    forcing_ensemble['h2o_stratospheric'][269]
, (5,95))

# %% cell 66
print('Total 2006-19 minus 1850-1900, 5th', np.percentile(forcing_ensemble['total'][256:270,:].mean(axis=0) - forcing_ensemble['total'][100:151,:].mean(axis=0), 5))
print('Total 2006-19 minus 1850-1900, best', forcing['total'][256:270].mean() - forcing['total'][100:151].mean())
print('Total 2006-19 minus 1850-1900, 50th', np.percentile(forcing_ensemble['total'][256:270,:].mean(axis=0) - forcing_ensemble['total'][100:151,:].mean(axis=0), 50))
print('Total 2006-19 minus 1850-1900, 95th', np.percentile(forcing_ensemble['total'][256:270,:].mean(axis=0) - forcing_ensemble['total'][100:151,:].mean(axis=0), 95))
print()
print('CO2 2006-19 minus 1850-1900, 5th', np.percentile(forcing_ensemble['co2'][256:270,:].mean(axis=0) - forcing_ensemble['co2'][100:151,:].mean(axis=0), 5))
print('CO2 2006-19 minus 1850-1900, best', forcing['co2'][256:270].mean() - forcing['co2'][100:151].mean())
print('CO2 2006-19 minus 1850-1900, 50th', np.percentile(forcing_ensemble['co2'][256:270,:].mean(axis=0) - forcing_ensemble['co2'][100:151,:].mean(axis=0), 50))
print('CO2 2006-19 minus 1850-1900, 95th', np.percentile(forcing_ensemble['co2'][256:270,:].mean(axis=0) - forcing_ensemble['co2'][100:151,:].mean(axis=0), 95))

# %% cell 67
print('Total 2006-19 minus 1850-1900, 5th', np.percentile(forcing_ensemble['total'][256:270,:].mean(axis=0), 5) - np.percentile(forcing_ensemble['total'][100:151,:].mean(axis=0), 5))
print('Total 2006-19 minus 1850-1900, best', forcing['total'][256:270].mean() - forcing['total'][100:151].mean())
print('Total 2006-19 minus 1850-1900, 50th', np.percentile(forcing_ensemble['total'][256:270,:].mean(axis=0), 50) - np.percentile(forcing_ensemble['total'][100:151,:].mean(axis=0), 50))
print('Total 2006-19 minus 1850-1900, 95th', np.percentile(forcing_ensemble['total'][256:270,:].mean(axis=0), 95) - np.percentile(forcing_ensemble['total'][100:151,:].mean(axis=0), 95))
print()
print('CO2 2006-19 minus 1850-1900, 5th', np.percentile(forcing_ensemble['co2'][256:270,:].mean(axis=0), 5) - np.percentile(forcing_ensemble['co2'][100:151,:].mean(axis=0), 5))
print('CO2 2006-19 minus 1850-1900, best', forcing['co2'][256:270].mean() - forcing['co2'][100:151].mean())
print('CO2 2006-19 minus 1850-1900, 50th', np.percentile(forcing_ensemble['co2'][256:270,:].mean(axis=0), 50) - np.percentile(forcing_ensemble['co2'][100:151,:].mean(axis=0), 50))
print('CO2 2006-19 minus 1850-1900, 95th', np.percentile(forcing_ensemble['co2'][256:270,:].mean(axis=0), 95) - np.percentile(forcing_ensemble['co2'][100:151,:].mean(axis=0), 95))

# %% cell 68
forcing_ensemble['total'].shape

# %% cell 70
forcing_ensemble['year'] = np.arange(1750, 2020)
save_dict_to_hdf5(forcing_ensemble, '../data_output_large/ERF_ensemble.h5')
