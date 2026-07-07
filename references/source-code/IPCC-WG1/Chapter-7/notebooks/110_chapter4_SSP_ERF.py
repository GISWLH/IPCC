# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/110_chapter4_SSP_ERF.ipynb

# %% cell 2
import json
import numpy as np
from fair.constants import molwt
from fair.forcing.ghg import etminan, meinshausen
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import scipy.stats as st
import random
import pandas as pd
from tqdm.notebook import tqdm
import random
import os
import copy

from ar6.utils import check_and_download, mkdir_p
from ar6.utils.statistics import weighted_percentile
from ar6.utils.h5 import *
from ar6.forcing.aerosol import ghan, aerocom_n
from ar6.forcing.ozone import eesc
from ar6.constants.gases import rcmip_to_ghg_names, ghg_to_rcmip_names, ods_species, radeff
from ar6.constants import NINETY_TO_ONESIGMA

from ar6.twolayermodel import TwoLayerModel

import datetime as dt
import scmdata
import matplotlib.pyplot as pl
import json

# %% cell 3
forcing = {}

check_and_download(
    '../data_input_large/rcmip-emissions-annual-means-v5-1-0.csv',
    'https://rcmip-protocols-au.s3-ap-southeast-2.amazonaws.com/v5.1.0/rcmip-emissions-annual-means-v5-1-0.csv'
)

check_and_download(
    '../data_input_large/rcmip-concentrations-annual-means-v5-1-0.csv',
    'https://rcmip-protocols-au.s3-ap-southeast-2.amazonaws.com/v5.1.0/rcmip-concentrations-annual-means-v5-1-0.csv'
)
    
emissions = pd.read_csv('../data_input_large/rcmip-emissions-annual-means-v5-1-0.csv')
concentrations = pd.read_csv('../data_input_large/rcmip-concentrations-annual-means-v5-1-0.csv')

with open('../data_input/random_seeds.json', 'r') as filehandle:
    SEEDS = json.load(filehandle)

# %% cell 4
scenarios = ['ssp119','ssp126','ssp245','ssp370','ssp370-lowNTCF-aerchemmip','ssp434','ssp460','ssp534-over','ssp585']
scenarios_full = scenarios + ['ssp334', 'ssp370-lowNTCFCH4']
for scenario in scenarios_full:
    forcing[scenario] = {}

# %% cell 5
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
global_total['VOC'] = global_total['NMVOC']
new_ceds = pd.DataFrame(global_total)
new_ceds.index = np.arange(1750,2020)
new_ceds.index = new_ceds.index.astype('int')
new_ceds.index.name='year'
new_ceds.columns.name=None
emissions_ceds_update = new_ceds.loc[1750:2020] + emissions - df_emissions
emissions_ceds_update.drop(index=range(2020,2101), inplace=True)
emissions_ceds_update
#new_ceds

emissions = pd.read_csv('../data_input_large/rcmip-emissions-annual-means-v5-1-0.csv')
new_emissions = {}
for scenario in tqdm(scenarios):
    bc = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|BC'),'1750':'2500'].interpolate(axis=1, pad=True).values.squeeze()
    oc = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|OC'),'1750':'2500'].interpolate(axis=1, pad=True).values.squeeze()
    so2 = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|Sulfur'),'1750':'2500'].interpolate(axis=1, pad=True).values.squeeze()
    nh3 = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|NH3'),'1750':'2500'].interpolate(axis=1, pad=True).values.squeeze()
    nox = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|NOx'),'1750':'2500'].interpolate(axis=1, pad=True).values.squeeze()
    nmvoc = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|VOC'),'1750':'2500'].interpolate(axis=1, pad=True).values.squeeze()
    co = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|CO'),'1750':'2500'].interpolate(axis=1, pad=True).values.squeeze()
    bc[:265] = emissions_ceds_update.loc[1750:2014,'BC'].values
    oc[:265] = emissions_ceds_update.loc[1750:2014,'OC'].values
    so2[:265] = emissions_ceds_update.loc[1750:2014,'SO2'].values
    nh3[:265] = emissions_ceds_update.loc[1750:2014,'NH3'].values
    nox[:265] = emissions_ceds_update.loc[1750:2014,'NOx'].values
    nmvoc[:265] = emissions_ceds_update.loc[1750:2014,'VOC'].values
    co[:265] = emissions_ceds_update.loc[1750:2014,'CO'].values
    bc[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'BC'].values + np.linspace(0,0.8,5) * bc[265:270]
    oc[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'OC'].values + np.linspace(0,0.8,5) * oc[265:270]
    so2[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'SO2'].values + np.linspace(0,0.8,5) * so2[265:270]
    nh3[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'NH3'].values + np.linspace(0,0.8,5) * nh3[265:270]
    nox[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'NOx'].values + np.linspace(0,0.8,5) * nox[265:270]
    nmvoc[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'VOC'].values + np.linspace(0,0.8,5) * nmvoc[265:270]
    co[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'CO'].values + np.linspace(0,0.8,5) * co[265:270]
    
    new_emissions[scenario] = pd.DataFrame(
    {
        'BC': bc,
        'OC': oc,
        'SO2': so2,
        'NH3': nh3,
        'NOx': nox,
        'VOC': nmvoc,
        'CO': co
    })

# %% cell 6
for scenario in scenarios:
    pl.plot(np.arange(1750,2501), new_emissions[scenario]['BC'])

# %% cell 8
new_emissions['ssp370-lowNTCFCH4'] = copy.copy(new_emissions['ssp370-lowNTCF-aerchemmip'])

# %% cell 10
df = pd.read_csv('../data_input/IIASA_SSP_Scenario_Database/AIM-CGE_ssp334.csv')

bc = np.ones(751) * np.nan
oc = np.ones(751) * np.nan
co = np.ones(751) * np.nan
so2 = np.ones(751) * np.nan
nox = np.ones(751) * np.nan
nmvoc = np.ones(751) * np.nan
nh3 = np.ones(751) * np.nan

bc[:265] = emissions_ceds_update.loc[1750:2014,'BC'].values
f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Emissions|BC"), "2005":"2100"].squeeze().values)
bc[265:351] = f(np.arange(2015,2101))
bc[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'BC'].values + np.linspace(0,0.8,5) * bc[265:270]

oc[:265] = emissions_ceds_update.loc[1750:2014,'OC'].values
f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Emissions|OC"), "2005":"2100"].squeeze().values)
oc[265:351] = f(np.arange(2015,2101))
oc[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'OC'].values + np.linspace(0,0.8,5) * oc[265:270]

co[:265] = emissions_ceds_update.loc[1750:2014,'CO'].values
f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Emissions|CO"), "2005":"2100"].squeeze().values)
co[265:351] = f(np.arange(2015,2101))
co[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'CO'].values + np.linspace(0,0.8,5) * co[265:270]

nmvoc[:265] = emissions_ceds_update.loc[1750:2014,'VOC'].values
f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Emissions|VOC"), "2005":"2100"].squeeze().values)
nmvoc[265:351] = f(np.arange(2015,2101))
nmvoc[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'VOC'].values + np.linspace(0,0.8,5) * nmvoc[265:270]

so2[:265] = emissions_ceds_update.loc[1750:2014,'SO2'].values
f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Emissions|Sulfur"), "2005":"2100"].squeeze().values)
so2[265:351] = f(np.arange(2015,2101))
so2[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'SO2'].values + np.linspace(0,0.8,5) * so2[265:270]

nh3[:265] = emissions_ceds_update.loc[1750:2014,'NH3'].values
f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Emissions|NH3"), "2005":"2100"].squeeze().values)
nh3[265:351] = f(np.arange(2015,2101))
nh3[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'NH3'].values + np.linspace(0,0.8,5) * nh3[265:270]

nox[:265] = emissions_ceds_update.loc[1750:2014,'NOx'].values
f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Emissions|NOx"), "2005":"2100"].squeeze().values)
nox[265:351] = f(np.arange(2015,2101))
nox[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'NOx'].values + np.linspace(0,0.8,5) * nox[265:270]

new_emissions['ssp334'] = pd.DataFrame(
    {
        'BC': bc,
        'OC': oc,
        'SO2': so2,
        'NH3': nh3,
        'NOx': nox,
        'VOC': nmvoc,
        'CO': co
    }
)

pl.plot(np.arange(2005, 2101), new_emissions['ssp334']['NOx'][255:351])
pl.plot(np.arange(2005, 2101), new_emissions['ssp434']['NOx'][255:351])

# %% cell 11
new_emissions['ssp334']

# %% cell 12
pl.plot(new_emissions['ssp334'])
pl.xlim(250,280)

# %% cell 14
# get solar forcing from CMIP6 TSI time series
df = pd.read_csv('../data_output/solar_erf.csv', index_col='year')
solar_erf = np.zeros((751))
solar_erf[:550] = df.solar_erf.loc[1750:2299].values
for scenario in scenarios_full:
    forcing[scenario]['solar']=np.copy(solar_erf)

# %% cell 16
df = pd.read_csv('../data_output/volcanic_erf.csv', index_col='year')
volcanic_erf = np.zeros((751))
volcanic_erf[:265] = df.volcanic_erf.loc[1750:2014].values
# ramp down last 10 years to zero according to https://www.geosci-model-dev.net/9/3461/2016/gmd-9-3461-2016.html
volcanic_erf[264:275] = volcanic_erf[264] * np.linspace(1,0,11)
volcanic_erf[275:] = 0.
pl.plot(np.arange(1750,2501), volcanic_erf[:])
#emissions = np.loadtxt('../data/SSP460_INTERIM_EMISSIONS.csv', skiprows=3, delimiter=',')

for scenario in scenarios_full:
    forcing[scenario]['volcanic']=np.copy(volcanic_erf)

# %% cell 18
df = pd.read_csv('../data_input_large/ERFaci_samples.csv')
aci_coeffs = np.exp(df.values)

samples = 100000

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

# %% cell 19
# SCALE TO ASSESSMENT
ERFari_scale = st.norm.rvs(loc=-0.30, scale=0.30/NINETY_TO_ONESIGMA, size=samples, random_state=786418)
ERFaci_scale = st.norm.rvs(loc=-1.00, scale=0.70/NINETY_TO_ONESIGMA, size=samples, random_state=31318990)

# %% cell 20
fig,ax = pl.subplots(1,2, figsize=(27/2.54,12/2.54))
ax[0].hist(ERFari_scale, bins=np.arange(-1.2,0.3,0.05), density=True);
ax[0].set_title('ERFari prior');
ax[1].hist(ERFaci_scale, bins=np.arange(-4,0.5,0.2), density=True);
ax[1].set_title('ERFaci prior');
np.percentile(ERFari_scale+ERFaci_scale, (5,16,50,84,95))

# %% cell 21
ERFari = {}
ERFaci = {}

bc_20101750 = st.norm.rvs(loc=0.3, scale=0.2/NINETY_TO_ONESIGMA, size=samples, random_state=SEEDS[95])
oc_20101750 = st.norm.rvs(loc=-0.09, scale=0.07/NINETY_TO_ONESIGMA, size=samples, random_state=SEEDS[96])
so2_20101750 = st.norm.rvs(loc=-0.4, scale=0.2/NINETY_TO_ONESIGMA, size=samples, random_state=SEEDS[97])
nh3_20101750 = st.norm.rvs(loc=-0.11, scale=0.05/NINETY_TO_ONESIGMA, size=samples, random_state=SEEDS[98])

beta_bc = bc_20101750/(np.mean(emissions_ceds_update.loc[2005:2014,'BC'])-emissions_ceds_update.loc[1750,'BC'])
beta_oc = oc_20101750/(np.mean(emissions_ceds_update.loc[2005:2014,'OC'])-emissions_ceds_update.loc[1750,'OC'])
beta_so2 = so2_20101750/(np.mean(emissions_ceds_update.loc[2005:2014,'SO2'])-emissions_ceds_update.loc[1750,'SO2'])
beta_nh3 = nh3_20101750/(np.mean(emissions_ceds_update.loc[2005:2014,'NH3'])-emissions_ceds_update.loc[1750,'NH3'])

for scenario in tqdm(scenarios_full):
    ERFari[scenario] = np.ones((751,samples)) * np.nan
    ERFaci[scenario] = np.ones((751,samples)) * np.nan
    
    bc = new_emissions[scenario]['BC'].values.squeeze()
    oc = new_emissions[scenario]['OC'].values.squeeze()
    so2 = new_emissions[scenario]['SO2'].values.squeeze()
    nh3 = new_emissions[scenario]['NH3'].values.squeeze()
    
    for i in tqdm(range(samples), leave=False):
        ERFari[scenario][:, i] = (
            (so2-so2[0]) * beta_so2[i] +
            (bc-bc[0]) * beta_bc[i] +
            (oc-oc[0]) * beta_oc[i] +
            (nh3-nh3[0]) * beta_nh3[i]
        )
    
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
        ERFaci[scenario][:,i] = (
            ghan([so2, bc+oc], 1.11, aci_coeffs[i,0], aci_coeffs[i,1])
        - ts1750)/(ts2010-ts1750)*ERFaci_scale[i]

# %% cell 22
ERFari_median = {}
ERFaci_median = {}

for scenario in tqdm(scenarios_full):
    bc = new_emissions[scenario]['BC'].values.squeeze()
    oc = new_emissions[scenario]['OC'].values.squeeze()
    so2 = new_emissions[scenario]['SO2'].values.squeeze()
    nh3 = new_emissions[scenario]['NH3'].values.squeeze()
    
    beta_bc = 0.3/(np.mean(bc[255:265])-bc[0])
    beta_oc = -0.09/(np.mean(oc[255:265])-oc[0])
    beta_so2 = -0.4/(np.mean(so2[255:265])-so2[0])
    beta_nh3 = -0.11/(np.mean(nh3[255:265])-nh3[0])
    ERFaci_median[scenario] = np.percentile(ERFaci[scenario], 50, axis=1) * (-1.0)/(np.percentile(ERFaci[scenario], 50, axis=1)[255:265].mean())
    ERFari_median[scenario] = (
        (so2-so2[0]) * beta_so2 +
        (bc-bc[0]) * beta_bc +
        (oc-oc[0]) * beta_oc +
        (nh3-nh3[0]) * beta_nh3
    )

# %% cell 23
for scenario in tqdm(scenarios_full):   
    forcing[scenario]['aerosol-radiation_interactions'] = ERFari_median[scenario]
    forcing[scenario]['aerosol-cloud_interactions'] = ERFaci_median[scenario]
print(forcing['ssp334']['aerosol-cloud_interactions'].shape)

# %% cell 25
df = pd.read_csv('../data_input_large/CEDS_v_2020_09_11_emissions/BC_global_CEDS_emissions_by_sector_2020_09_11.csv')
bc_hist = df.loc[:,'X1750':'X2019'].sum(axis=0).values/1000.

df = pd.read_csv('../data_output/AR6_ERF_1750-2019.csv')
bc_ar6_forc = df.loc[:,'bc_on_snow']

# %% cell 26
for scenario in scenarios_full:
    bc = new_emissions[scenario]['BC'].values.squeeze()
    forcing[scenario]['bc_on_snow'] = (bc-bc[0])/(bc_hist[264]-bc_hist[0])*bc_ar6_forc[264]
    pl.plot(forcing[scenario]['bc_on_snow'])

# %% cell 28
df = pd.read_csv('../data_input_large/CEDS_v_2020_09_11_emissions/NOx_global_CEDS_emissions_by_sector_2020_09_11.csv')
avi_nox_hist = df[df.sector.str.endswith("aviation")].loc[:,'X1750':'X2019'].sum(axis=0).values/1000.
df = pd.read_csv('../data_output/AR6_ERF_1750-2019.csv')
bc_ar6_forc = df.loc[:,'contrails']
for scenario in scenarios:
    avi_nox = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|NOx|MAGICC Fossil and Industrial|Aircraft'),'1750':'2500'].interpolate(axis=1, pad=True).values.squeeze()
    avi_nox[:265] = avi_nox_hist[:265]
    avi_nox[265:270] = np.linspace(1,0.2,5) * avi_nox_hist[265:270] + np.linspace(0,0.8,5) * avi_nox[265:270]
    contrail_forcing_2014 = bc_ar6_forc[264]
    forcing[scenario]['contrails'] = avi_nox/avi_nox_hist[264] * contrail_forcing_2014
    pl.plot(np.arange(1750,2501), forcing[scenario]['contrails'])
forcing['ssp370-lowNTCFCH4']['contrails'] = np.copy(forcing['ssp370-lowNTCF-aerchemmip']['contrails'])
forcing['ssp334']['contrails'] = np.copy(forcing['ssp370-lowNTCF-aerchemmip']['contrails'])

# %% cell 30
ghimire = pd.read_csv('../data_input/Ghimire_et_al_2014_GRL/ghimire_curve_fit.csv')
for scenario in scenarios:
    lusf2019 = -0.20/np.cumsum(emissions.loc[(emissions['Scenario']=='ssp245')&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|CO2|MAGICC AFOLU'),'1750':'2020'].interpolate(axis=1, pad=True).values.squeeze())[269]  # include irrigation of -0.05 in Sherwood et al
    forcing[scenario]['land_use'] = np.cumsum(emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|CO2|MAGICC AFOLU'),'1750':'2500'].interpolate(axis=1, pad=True).values.squeeze())*lusf2019
    f = interp1d(ghimire['year'], ghimire['flux'], kind='linear', fill_value='extrapolate', bounds_error=False)
    lusf2019 = -0.20/(f(2019)-f(1750))
    forcing[scenario]['land_use'][:269] = lusf2019*(f(np.arange(1750,2019))-f(1750))
    pl.plot(np.arange(1750, 2501), forcing[scenario]['land_use'])

lusf2019 = -0.20/np.cumsum(emissions.loc[(emissions['Scenario']=='ssp245')&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|CO2|MAGICC AFOLU'),'1750':'2020'].interpolate(axis=1, pad=True).values.squeeze())[269]  # include irrigation of -0.05 in Sherwood et al
co2 = np.ones(751) * np.nan
df = pd.read_csv('../data_input/IIASA_SSP_Scenario_Database/AIM-CGE_ssp334.csv')
f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Emissions|CO2|Land Use"), "2005":"2100"].squeeze().values)
co2[:265] = emissions.loc[(emissions['Scenario']=='ssp245')&(emissions['Region']=='World')&(emissions['Variable']=='Emissions|CO2|MAGICC AFOLU'),'1750':'2014'].interpolate(axis=1, pad=True).values.squeeze()
co2[265:351] = f(np.arange(2015,2101))
forcing['ssp334']['land_use'] = np.cumsum(co2) * lusf2019
#co2[265:270] = np.linspace(1,0.2,5) * emissions_ceds_update.loc[2015:2019,'BC'].values + np.linspace(0,0.8,5) * bc[265:270]
f = interp1d(ghimire['year'], ghimire['flux'], kind='linear', fill_value='extrapolate', bounds_error=False)
lusf2019 = -0.20/(f(2019)-f(1750))
forcing['ssp334']['land_use'][:269] = lusf2019*(f(np.arange(1750,2019))-f(1750))
forcing['ssp370-lowNTCFCH4']['land_use'] = np.copy(forcing['ssp370-lowNTCF-aerchemmip']['land_use'])
pl.plot(np.arange(1750, 2501), forcing['ssp334']['land_use'])

# %% cell 32
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

gases_obs = ghg_obs.columns.to_list()
gases_obs.remove('YYYY')
print(*(gases_obs))

gases=['CO2','CH4','N2O',
     'HFC125','HFC134a','HFC143a','HFC152a','HFC227ea','HFC23','HFC236fa','HFC245fa','HFC32','HFC365mfc','HFC4310mee',
     'NF3','C2F6','C3F8','C4F10','C5F12','C6F14','C7F16','C8F18','CF4','cC4F8','SF6','SO2F2','CCl4','CFC11','CFC113',
     'CFC114','CFC115','CFC12','CH2Cl2','CH3Br','CH3CCl3','CH3Cl','CHCl3','HCFC141b','HCFC142b','HCFC22','Halon1211',
     'Halon1301','Halon2402']

# %% cell 33
concentrations_out = {}

fig, ax = pl.subplots(1,3,figsize=(16,5))
for scenario in tqdm(scenarios):
    forcing[scenario]['co2'] = np.zeros(751)
    forcing[scenario]['ch4'] = np.zeros(751)
    forcing[scenario]['n2o'] = np.zeros(751)

    concentrations_out[scenario] = {}
    concentrations_out[scenario]['CO2'] = np.zeros(751)
    concentrations_out[scenario]['CH4'] = np.zeros(751)
    concentrations_out[scenario]['N2O'] = np.zeros(751)

    co2 = concentrations.loc[(concentrations['Scenario']==scenario)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|CO2')),'1750':'2500'].values.squeeze()
    ch4 = concentrations.loc[(concentrations['Scenario']==scenario)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|CH4')),'1750':'2500'].values.squeeze()
    n2o = concentrations.loc[(concentrations['Scenario']==scenario)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|N2O')),'1750':'2500'].values.squeeze()
    co2[:265] = ghg_obs['CO2'].values[:265]
    ch4[:265] = ghg_obs['CH4'].values[:265]
    n2o[:265] = ghg_obs['N2O'].values[:265]
    
    co2[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['CO2'].values[264:270] + np.linspace(0,1,6) * co2[264:270]
    ch4[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['CH4'].values[264:270] + np.linspace(0,1,6) * ch4[264:270]
    n2o[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['N2O'].values[264:270] + np.linspace(0,1,6) * n2o[264:270]
    
    concentrations_out[scenario]['CO2'] = co2
    concentrations_out[scenario]['CH4'] = ch4
    concentrations_out[scenario]['N2O'] = n2o
    
    for i, year in enumerate(range(1750,2501)):
        forcing[scenario]['co2'][i], forcing[scenario]['ch4'][i], forcing[scenario]['n2o'][i] = meinshausen( #etminan(
            [co2[i], ch4[i], n2o[i]], 
            [co2[0], ch4[0], n2o[0]], scale_F2x=False)

    # include rapid adjustments for CO2, CH4 and N2O:
    forcing[scenario]['co2'] = 1.05 * forcing[scenario]['co2']
    forcing[scenario]['ch4'] = 0.86 * forcing[scenario]['ch4']
    forcing[scenario]['n2o'] = 1.07 * forcing[scenario]['n2o']
    
    ax[0].plot(np.arange(2000,2051), co2[250:301])
    ax[1].plot(np.arange(2000,2051),ch4[250:301])
    ax[2].plot(np.arange(2000,2051),n2o[250:301])
    

scenario = 'ssp370-lowNTCFCH4'  # modify only methane
concentrations_out[scenario] = {}
concentrations_out[scenario]['CO2'] = np.copy(concentrations_out['ssp370-lowNTCF-aerchemmip']['CO2'])
concentrations_out[scenario]['N2O'] = np.copy(concentrations_out['ssp370-lowNTCF-aerchemmip']['N2O'])
forcing[scenario]['co2'] = np.zeros(751)
forcing[scenario]['ch4'] = np.zeros(751)
forcing[scenario]['n2o'] = np.zeros(751)
co2 = concentrations_out[scenario]['CO2']
ch4 = concentrations.loc[(concentrations['Scenario']=='ssp370-lowNTCF-gidden')&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|CH4')),'1750':'2500'].values.squeeze()
n2o = concentrations_out[scenario]['N2O']
ch4[:265] = ghg_obs['CH4'].values[:265]
ch4[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['CH4'].values[264:270] + np.linspace(0,1,6) * ch4[264:270]
concentrations_out[scenario]['CH4'] = ch4
for i, year in enumerate(range(1750,2501)):
    forcing[scenario]['co2'][i], forcing[scenario]['ch4'][i], forcing[scenario]['n2o'][i] = meinshausen( #etminan(
        [co2[i], ch4[i], n2o[i]], 
        [co2[0], ch4[0], n2o[0]], scale_F2x=False)
# include rapid adjustments for CO2, CH4 and N2O:
forcing[scenario]['co2'] = 1.05 * forcing[scenario]['co2']
forcing[scenario]['ch4'] = 0.86 * forcing[scenario]['ch4']
forcing[scenario]['n2o'] = 1.07 * forcing[scenario]['n2o']




scenario = 'ssp334'
forcing[scenario]['co2'] = np.ones(751) * np.nan
forcing[scenario]['ch4'] = np.ones(751) * np.nan
forcing[scenario]['n2o'] = np.ones(751) * np.nan

df = pd.read_csv('../data_input/IIASA_SSP_Scenario_Database/AIM-CGE_ssp334.csv')

co2 = np.ones(751) * np.nan
ch4 = np.ones(751) * np.nan
n2o = np.ones(751) * np.nan

co2[:265] = ghg_obs['CO2'].values[:265]
ch4[:265] = ghg_obs['CH4'].values[:265]
n2o[:265] = ghg_obs['N2O'].values[:265]

f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Diagnostics|MAGICC6|Concentration|CO2"), "2005":"2100"].squeeze().values)
co2[265:351] = f(np.arange(2015,2101))
co2[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['CO2'].values[264:270] + np.linspace(0,1,6) * co2[264:270]

f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Diagnostics|MAGICC6|Concentration|CH4"), "2005":"2100"].squeeze().values)
ch4[265:351] = f(np.arange(2015,2101))
ch4[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['CH4'].values[264:270] + np.linspace(0,1,6) * ch4[264:270]

f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Diagnostics|MAGICC6|Concentration|N2O"), "2005":"2100"].squeeze().values)
n2o[265:351] = f(np.arange(2015,2101))
n2o[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['N2O'].values[264:270] + np.linspace(0,1,6) * n2o[264:270]
  
for i, year in enumerate(range(1750,2101)):
    forcing[scenario]['co2'][i], forcing[scenario]['ch4'][i], forcing[scenario]['n2o'][i] = meinshausen( #etminan(
        [co2[i], ch4[i], n2o[i]], 
        [co2[0], ch4[0], n2o[0]], scale_F2x=False)

# include rapid adjustments for CO2, CH4 and N2O:
forcing[scenario]['co2'] = 1.05 * forcing[scenario]['co2']
forcing[scenario]['ch4'] = 0.86 * forcing[scenario]['ch4']
forcing[scenario]['n2o'] = 1.07 * forcing[scenario]['n2o']

ax[0].plot(np.arange(2000,2051), co2[250:301])
ax[1].plot(np.arange(2000,2051), ch4[250:301])
ax[2].plot(np.arange(2000,2051), n2o[250:301])

# %% cell 34
gases=['CO2','CH4','N2O',
     'HFC125','HFC134a','HFC143a','HFC152a','HFC227ea','HFC23','HFC236fa','HFC245fa','HFC32','HFC365mfc','HFC4310mee',
     'NF3','C2F6','C3F8','C4F10','C5F12','C6F14','C7F16','C8F18','CF4','cC4F8','SF6','SO2F2','CCl4','CFC11','CFC113',
     'CFC114','CFC115','CFC12','CH2Cl2','CH3Br','CH3CCl3','CH3Cl','CHCl3','HCFC141b','HCFC142b','HCFC22','Halon1211',
     'Halon1301','Halon2402']

trop_adjustment_scale = radeff.copy()
for key in trop_adjustment_scale.keys():
    trop_adjustment_scale[key] = 1
trop_adjustment_scale['CFC-11'] = 1.13
trop_adjustment_scale['CFC-12'] = 1.12

for scenario in scenarios:
    forcing[scenario]['other_wmghg'] = np.zeros(751)
    for gas in gases_obs[3:]:
        meins = concentrations.loc[(concentrations['Scenario']==scenario)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith(ghg_to_rcmip_names[gas])),'1750':'2500'].values.squeeze()
        if meins.shape == (0,751):
            meins = np.zeros(751)
        obs = ghg_obs[gas].values[:270]
        conc = np.zeros(751)
        conc[:265] = obs[:265]
        conc[264:270] = np.linspace(1.0,0.0,6) * obs[264:270] + np.linspace(0,1,6) * meins[264:270]
        conc[270:] = meins[270:]
        concentrations_out[scenario][gas] = conc
        forcing[scenario][gas] = ((conc - conc[0]) * radeff[gas] * 0.001) * trop_adjustment_scale[gas]
        forcing[scenario]['other_wmghg'] = forcing[scenario]['other_wmghg'] + forcing[scenario][gas]
    pl.plot(np.arange(2005,2101), forcing[scenario]['other_wmghg'][255:351])
    
for gas in gases_obs[3:]:
    concentrations_out['ssp370-lowNTCFCH4'][gas] = np.copy(concentrations_out['ssp370-lowNTCF-aerchemmip'][gas])
    forcing['ssp370-lowNTCFCH4'][gas] = np.copy(forcing['ssp370-lowNTCF-aerchemmip'][gas])
forcing['ssp370-lowNTCFCH4']['other_wmghg'] = np.copy(forcing['ssp370-lowNTCF-aerchemmip']['other_wmghg'])

# %% cell 36
forcing['ssp334']['other_wmghg'] = np.copy(forcing['ssp119']['other_wmghg'])

# %% cell 38
forcing_ar6 = pd.read_csv('../data_output/AR6_ERF_1750-2019.csv')

for scenario in scenarios_full:
    forcing[scenario]['h2o_stratospheric'] = forcing[scenario]['ch4']/(forcing_ar6['ch4'].values[269] - forcing_ar6['ch4'].values[0]) * 0.05

# %% cell 40
o3_df = pd.read_csv('../data_output/o3_erf.csv')
skeie_total = o3_df['o3_erf'].values[:270]

o3_coeffs = pd.read_csv('../data_input/tunings/cmip6_ozone_skeie_fits.csv', index_col=0)
ozone_rad_eff = o3_coeffs['mean']

# %% cell 41
for scenario in tqdm(scenarios + ['ssp370-lowNTCFCH4']):
    if scenario=='ssp370-lowNTCFCH4':
        ch4_source='ssp370-lowNTCF-gidden'
        n2o_source='ssp370-lowNTCF-aerchemmip'
    else:
        ch4_source=scenario
        n2o_source=scenario
    ch4 = concentrations.loc[(concentrations['Scenario']==ch4_source)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|CH4')),'1750':'2500'].values.squeeze()
    ch4[:265] = ghg_obs['CH4'].values[:265]
    ch4[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['CH4'].values[264:270] + np.linspace(0,1,6) * ch4[264:270]
    n2o = concentrations.loc[(concentrations['Scenario']==n2o_source)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|N2O')),'1750':'2500'].values.squeeze()
    n2o[:265] = ghg_obs['N2O'].values[:265]
    n2o[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['N2O'].values[264:270] + np.linspace(0,1,6) * n2o[264:270]
    ods = np.zeros((751))
    for specie in ods_species:
        this_ods = concentrations.loc[(concentrations['Scenario']==n2o_source)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith(specie)),'1750':'2500'].values.squeeze()
        this_ods[:265] = ghg_obs.loc[:2014,rcmip_to_ghg_names[specie]].values.squeeze()
        this_ods[264:270] = np.linspace(1.0,0.0,6) * ghg_obs.loc[2014:2019,rcmip_to_ghg_names[specie]].values.squeeze() + np.linspace(0,1,6) * this_ods[264:270]
        ods = ods + (eesc(this_ods, specie))
    co = new_emissions[scenario]['CO']
    nox = new_emissions[scenario]['NOx']
    voc = new_emissions[scenario]['VOC']

    forcing[scenario]['o3'] = np.zeros(751)
    
    forcing[scenario]['o3'][:265] = skeie_total[:265]
    
    forcing[scenario]['o3'][265:] = (
        ozone_rad_eff['CH4'] * (ch4[265:]-ch4[0]) +
        ozone_rad_eff['N2O'] * (n2o[265:]-n2o[0]) +
        ozone_rad_eff['ODS'] * (ods[265:]-ods[0]) +
        ozone_rad_eff['CO'] * (co[265:]-co[0]) +
        ozone_rad_eff['VOC'] * (voc[265:]-voc[0]) +
        ozone_rad_eff['NOx'] * (nox[265:]-nox[0])
    ).values
    
    forcing[scenario]['o3'][264:270] = np.linspace(1.0,0.0,6) * skeie_total[264:270] + np.linspace(0,1,6) * forcing[scenario]['o3'][264:270]
    
    pl.plot(np.arange(1750,2201), forcing[scenario]['o3'][:451], label=scenario)
pl.grid()

# ssp334
df = pd.read_csv('../data_input/IIASA_SSP_Scenario_Database/AIM-CGE_ssp334.csv')

ch4 = np.zeros(751)
n2o = np.zeros(751)

ch4[:265] = ghg_obs['CH4'].values[:265]
n2o[:265] = ghg_obs['N2O'].values[:265]

f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Diagnostics|MAGICC6|Concentration|CH4"), "2005":"2100"].squeeze().values)
ch4[265:351] = f(np.arange(2015,2101))
ch4[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['CH4'].values[264:270] + np.linspace(0,1,6) * ch4[264:270]

f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Diagnostics|MAGICC6|Concentration|N2O"), "2005":"2100"].squeeze().values)
n2o[265:351] = f(np.arange(2015,2101))
n2o[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['N2O'].values[264:270] + np.linspace(0,1,6) * n2o[264:270]

# Terje: use CFCs from SSP434
ods = np.zeros((751))
for specie in ods_species:
    this_ods = concentrations.loc[(concentrations['Scenario']=='ssp434')&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith(specie)),'1750':'2500'].values.squeeze()
    this_ods[:265] = ghg_obs.loc[:2014,rcmip_to_ghg_names[specie]].values.squeeze()
    this_ods[264:270] = np.linspace(1.0,0.0,6) * ghg_obs.loc[2014:2019,rcmip_to_ghg_names[specie]].values.squeeze() + np.linspace(0,1,6) * this_ods[264:270]
    ods = ods + (eesc(this_ods, specie))
co = new_emissions['ssp334']['CO']
nox = new_emissions['ssp334']['NOx']
voc = new_emissions['ssp334']['VOC']

forcing['ssp334']['o3'] = np.zeros(751)

forcing['ssp334']['o3'][:265] = skeie_total[:265]

forcing['ssp334']['o3'][265:] = (
    ozone_rad_eff['CH4'] * (ch4[265:]-ch4[0]) +
    ozone_rad_eff['N2O'] * (n2o[265:]-n2o[0]) +
    ozone_rad_eff['ODS'] * (ods[265:]-ods[0]) +
    ozone_rad_eff['CO'] * (co[265:]-co[0]) +
    ozone_rad_eff['VOC'] * (voc[265:]-voc[0]) +
    ozone_rad_eff['NOx'] * (nox[265:]-nox[0])
).values

forcing['ssp334']['o3'][264:270] = np.linspace(1.0,0.0,6) * skeie_total[264:270] + np.linspace(0,1,6) * forcing['ssp334']['o3'][264:270]

pl.plot(np.arange(1750,2201), forcing['ssp334']['o3'][:451], label='ssp334', color='k')

pl.legend()

# %% cell 42
with open("../data_input/tunings/cmip6_twolayer_tuning_params.json", "r") as read_file:
    cmip6_models = json.load(read_file)

xl = pd.read_excel('../data_input/observations/AR6 FGD assessment time series - GMST and GSAT.xlsx', skiprows=1, skipfooter=28)
Tobs=xl['4-set mean'].values
#years=xl['Unnamed: 0'].values

# %% cell 43
scenario='ssp245'

#dl = cmip6_models['dl']['mean'] * ur(cmip6_models['dl']['units'])
#du = cmip6_models['du']['mean']  * ur(cmip6_models['du']['units'])
#eta = cmip6_models['eta']['mean'] * ur(cmip6_models['eta']['units'])
#lambda0 = 4/3 *  ur(cmip6_models['lambda0']['units'])
#efficacy = cmip6_models['efficacy']['mean'] * ur(cmip6_models['efficacy']['units'])

cmix = cmip6_models['cmix']['mean']['EBM-epsilon']
cdeep = cmip6_models['cdeep']['mean']['EBM-epsilon']
#gamma_2l = cmip6_models['gamma_2l']['mean']['EBM-epsilon']
#lamg = -cmip6_models['lamg']['mean']['EBM-epsilon']
eff = cmip6_models['eff']['mean']['EBM-epsilon']

f2x = 4.0
ecs = 3.0
tcr = 1.8
lamg = f2x/ecs
kappa = -(f2x/ecs - f2x/tcr)
gamma_2l = kappa/eff

# 1. sum up forcing including no-feedback ozone forcing
forcing[scenario]['total_anthropogenic']=forcing[scenario]['co2']+forcing[scenario]['ch4']+forcing[scenario]['n2o']+\
    forcing[scenario]['other_wmghg']+\
    forcing[scenario]['o3']+forcing[scenario]['h2o_stratospheric']+forcing[scenario]['contrails']+\
    forcing[scenario]['aerosol-radiation_interactions']+forcing[scenario]['aerosol-cloud_interactions']+forcing[scenario]['bc_on_snow']+forcing[scenario]['land_use']
forcing[scenario]['total_natural']=forcing[scenario]['volcanic']+forcing[scenario]['solar']
forcing[scenario]['total']=forcing[scenario]['total_anthropogenic']+forcing[scenario]['total_natural']
erf0 = forcing[scenario]['total']

# 2. run two layer model and save temperature results
driver = TwoLayerModel(
    extforce=erf0,
    exttime=np.arange(1750,2501),
    tbeg=1750,
    tend=2500,
    lamg=lamg,
    t2x=None,
    eff=eff,
    cmix=cmix,
    cdeep=cdeep,
    gamma_2l=gamma_2l,
    outtime=np.arange(1750,2501),
    dt=0.2
)
output = driver.run()

temp0 = output.tg

pl.plot(np.arange(1750,2021), -0.037*(temp0[:271]-temp0[100:151].mean()))
pl.plot(np.arange(1850,2021), -0.037*Tobs)

# %% cell 44
for scenario in tqdm(scenarios + ['ssp370-lowNTCFCH4'], desc="Scenarios"):
    if scenario=='ssp370-lowNTCFCH4':
        ch4_source='ssp370-lowNTCF-gidden'
        n2o_source='ssp370-lowNTCF-aerchemmip'
    else:
        ch4_source=scenario
        n2o_source=scenario
    for i in range(10):
        # 1. sum up forcing including no-feedback ozone forcing
        forcing[scenario]['total_anthropogenic']=forcing[scenario]['co2']+forcing[scenario]['ch4']+forcing[scenario]['n2o']+\
            forcing[scenario]['other_wmghg']+\
            forcing[scenario]['o3']+forcing[scenario]['h2o_stratospheric']+forcing[scenario]['contrails']+\
            forcing[scenario]['aerosol-radiation_interactions']+forcing[scenario]['aerosol-cloud_interactions']+forcing[scenario]['bc_on_snow']+forcing[scenario]['land_use']
        forcing[scenario]['total_natural']=forcing[scenario]['volcanic']+forcing[scenario]['solar']
        forcing[scenario]['total']=forcing[scenario]['total_anthropogenic']+forcing[scenario]['total_natural']
        erf0 = forcing[scenario]['total']

        # 2. run two layer model and save temperature results
        driver = TwoLayerModel(
            extforce=erf0,
            exttime=np.arange(1750,2501),
            tbeg=1750,
            tend=2500,
            lamg=lamg,
            t2x=None,
            eff=eff,
            cmix=cmix,
            cdeep=cdeep,
            gamma_2l=gamma_2l,
            outtime=np.arange(1750,2501),
            dt=0.2
        )
        output = driver.run()
        temp0 = output.tg
        ozone_feedback = -0.037 * (temp0-temp0[100:151].mean())

        ch4 = concentrations.loc[(concentrations['Scenario']==ch4_source)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|CH4')),'1750':'2500'].values.squeeze()
        ch4[:265] = ghg_obs['CH4'].values[:265]
        ch4[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['CH4'].values[264:270] + np.linspace(0,1,6) * ch4[264:270]
        n2o = concentrations.loc[(concentrations['Scenario']==n2o_source)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|N2O')),'1750':'2500'].values.squeeze()
        n2o[:265] = ghg_obs['N2O'].values[:265]
        n2o[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['N2O'].values[264:270] + np.linspace(0,1,6) * n2o[264:270]
        ods = np.zeros((751))
        for specie in ods_species:
            this_ods = concentrations.loc[(concentrations['Scenario']==n2o_source)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith(specie)),'1750':'2500'].values.squeeze()
            this_ods[:265] = ghg_obs.loc[:2014,rcmip_to_ghg_names[specie]].values.squeeze()
            this_ods[264:270] = np.linspace(1.0,0.0,6) * ghg_obs.loc[2014:2019,rcmip_to_ghg_names[specie]].values.squeeze() + np.linspace(0,1,6) * this_ods[264:270]
            ods = ods + (eesc(this_ods, specie))
        co = new_emissions[scenario]['CO']
        nox = new_emissions[scenario]['NOx']
        voc = new_emissions[scenario]['VOC']

        forcing[scenario]['o3'][:265] = skeie_total[:265]

        forcing[scenario]['o3'][265:] = (
            ozone_rad_eff['CH4'] * (ch4[265:]-ch4[0]) +
            ozone_rad_eff['N2O'] * (n2o[265:]-n2o[0]) +
            ozone_rad_eff['ODS'] * (ods[265:]-ods[0]) +
            ozone_rad_eff['CO'] * (co[265:]-co[0]) +
            ozone_rad_eff['VOC'] * (voc[265:]-voc[0]) +
            ozone_rad_eff['NOx'] * (nox[265:]-nox[0])
        ).values + ozone_feedback[265:]

        forcing[scenario]['o3'][264:270] = np.linspace(1.0,0.0,6) * skeie_total[264:270] + np.linspace(0,1,6) * forcing[scenario]['o3'][264:270]
        
    pl.plot(np.arange(1750, 2201), forcing[scenario]['o3'][:451], label=scenario)
    
    
scenario = 'ssp334'
for i in range(10):
    # 1. sum up forcing including no-feedback ozone forcing
    forcing[scenario]['total_anthropogenic']=forcing[scenario]['co2']+forcing[scenario]['ch4']+forcing[scenario]['n2o']+\
        forcing[scenario]['other_wmghg']+\
        forcing[scenario]['o3']+forcing[scenario]['h2o_stratospheric']+forcing[scenario]['contrails']+\
        forcing[scenario]['aerosol-radiation_interactions']+forcing[scenario]['aerosol-cloud_interactions']+forcing[scenario]['bc_on_snow']+forcing[scenario]['land_use']
    forcing[scenario]['total_natural']=forcing[scenario]['volcanic']+forcing[scenario]['solar']
    forcing[scenario]['total']=forcing[scenario]['total_anthropogenic']+forcing[scenario]['total_natural']
    erf0 = forcing[scenario]['total']
    erf0[351:] = 0

    # 2. run two layer model and save temperature results
    driver = TwoLayerModel(
        extforce=erf0,
        exttime=np.arange(1750,2501),
        tbeg=1750,
        tend=2500,
        lamg=lamg,
        t2x=None,
        eff=eff,
        cmix=cmix,
        cdeep=cdeep,
        gamma_2l=gamma_2l,
        outtime=np.arange(1750,2501),
        dt=0.2
    )
    output = driver.run()
    temp0 = output.tg
    ozone_feedback = -0.037 * (temp0-temp0[100:151].mean())

    df = pd.read_csv('../data_input/IIASA_SSP_Scenario_Database/AIM-CGE_ssp334.csv')

    ch4 = np.zeros(751)
    n2o = np.zeros(751)

    ch4[:265] = ghg_obs['CH4'].values[:265]
    n2o[:265] = ghg_obs['N2O'].values[:265]

    f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Diagnostics|MAGICC6|Concentration|CH4"), "2005":"2100"].squeeze().values)
    ch4[265:351] = f(np.arange(2015,2101))
    ch4[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['CH4'].values[264:270] + np.linspace(0,1,6) * ch4[264:270]

    f = interp1d([2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100], df.loc[(df['SCENARIO']=='ssp334')&(df['VARIABLE']=="Diagnostics|MAGICC6|Concentration|N2O"), "2005":"2100"].squeeze().values)
    n2o[265:351] = f(np.arange(2015,2101))
    n2o[264:270] = np.linspace(1.0,0.0,6) * ghg_obs['N2O'].values[264:270] + np.linspace(0,1,6) * n2o[264:270]

    ods = np.zeros((751))
    for specie in ods_species:
        this_ods = concentrations.loc[(concentrations['Scenario']=='ssp434')&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith(specie)),'1750':'2500'].values.squeeze()
        this_ods[:265] = ghg_obs.loc[:2014,rcmip_to_ghg_names[specie]].values.squeeze()
        this_ods[264:270] = np.linspace(1.0,0.0,6) * ghg_obs.loc[2014:2019,rcmip_to_ghg_names[specie]].values.squeeze() + np.linspace(0,1,6) * this_ods[264:270]
        ods = ods + (eesc(this_ods, specie))
    co = new_emissions[scenario]['CO']
    nox = new_emissions[scenario]['NOx']
    voc = new_emissions[scenario]['VOC']

    forcing[scenario]['o3'][:265] = skeie_total[:265]

    forcing[scenario]['o3'][265:] = (
        ozone_rad_eff['CH4'] * (ch4[265:]-ch4[0]) +
        ozone_rad_eff['N2O'] * (n2o[265:]-n2o[0]) +
        ozone_rad_eff['ODS'] * (ods[265:]-ods[0]) +
        ozone_rad_eff['CO'] * (co[265:]-co[0]) +
        ozone_rad_eff['VOC'] * (voc[265:]-voc[0]) +
        ozone_rad_eff['NOx'] * (nox[265:]-nox[0])
    ).values + ozone_feedback[265:]

    forcing[scenario]['o3'][264:270] = np.linspace(1.0,0.0,6) * skeie_total[264:270] + np.linspace(0,1,6) * forcing[scenario]['o3'][264:270]

pl.plot(np.arange(1750, 2101), forcing[scenario]['o3'][:351], label=scenario, color='k')
    
pl.grid()
pl.legend()

# %% cell 45
colors = {
    'ssp119': '#1e9583',
    'ssp126': '#1d3354',
    'ssp245': '#e9dc3d',
    'ssp334': '#63bce4', # not standard scenario
    'ssp370': '#f11111',
    'ssp370-lowNTCFCH4': '#f11111', 
    'ssp370-lowNTCF-aerchemmip': '#f11111',
    'ssp434': '#63bce4',
    'ssp460': '#e78731',
    'ssp534-over': '#996dc8',
    'ssp585': '#830b22',
}

ls = {
    'ssp119': '-',
    'ssp126': '-',
    'ssp245': '-', 
    'ssp334': '--',
    'ssp370': '-',
    'ssp370-lowNTCFCH4': '--', 
    'ssp370-lowNTCF-aerchemmip': '-.',
    'ssp434': '-',
    'ssp460': '-',
    'ssp534-over': '-',
    'ssp585': '-',
}

# %% cell 46
# fix 334
for ftype in ['co2','ch4','n2o','other_wmghg','o3','h2o_stratospheric','contrails','aerosol-radiation_interactions','aerosol-cloud_interactions','bc_on_snow','land_use',
      'volcanic','solar','total_anthropogenic','total_natural','total']:
    forcing['ssp334'][ftype][351:] = np.nan

# %% cell 47
fig, ax = pl.subplots(4,4, figsize=(29.7/2.54,21/2.54),squeeze=True)
for scenario in scenarios_full:
    ax[0,0].plot(np.arange(1750,2501),forcing[scenario]['co2'], color=colors[scenario], ls=ls[scenario])
    ax[0,1].plot(np.arange(1750,2501),forcing[scenario]['ch4'], color=colors[scenario], ls=ls[scenario])
    ax[0,2].plot(np.arange(1750,2501),forcing[scenario]['n2o'], color=colors[scenario], ls=ls[scenario])
    ax[0,3].plot(np.arange(1750,2501),forcing[scenario]['other_wmghg'], color=colors[scenario], ls=ls[scenario])
    ax[1,0].plot(np.arange(1750,2501),forcing[scenario]['o3'], color=colors[scenario], ls=ls[scenario])
    ax[1,1].plot(np.arange(1750,2501),forcing[scenario]['h2o_stratospheric'], color=colors[scenario], ls=ls[scenario])
    ax[1,2].plot(np.arange(1750,2501),forcing[scenario]['contrails'], color=colors[scenario], ls=ls[scenario])
    ax[1,3].plot(np.arange(1750,2501),forcing[scenario]['aerosol-radiation_interactions'], color=colors[scenario], ls=ls[scenario])
    ax[2,0].plot(np.arange(1750,2501),forcing[scenario]['aerosol-cloud_interactions'], color=colors[scenario], ls=ls[scenario])
    ax[2,1].plot(np.arange(1750,2501),forcing[scenario]['bc_on_snow'], color=colors[scenario], ls=ls[scenario])
    ax[2,2].plot(np.arange(1750,2501),forcing[scenario]['land_use'], color=colors[scenario], ls=ls[scenario])
    ax[2,3].plot(np.arange(1750,2501),forcing[scenario]['volcanic'], color=colors[scenario], ls=ls[scenario])
    ax[3,0].plot(np.arange(1750,2501),forcing[scenario]['solar'], color=colors[scenario], ls=ls[scenario], label=scenario)

ax[3,1].axis('off')
ax[3,2].axis('off')
ax[3,3].axis('off')
ax[0,0].set_xlim(1750,2500)
ax[0,1].set_xlim(1750,2500)
ax[0,2].set_xlim(1750,2500)
ax[0,3].set_xlim(1750,2500)
ax[1,0].set_xlim(1750,2500)
ax[1,1].set_xlim(1750,2500)
ax[1,2].set_xlim(1750,2500)
ax[1,3].set_xlim(1750,2500)
ax[2,0].set_xlim(1750,2500)
ax[2,1].set_xlim(1750,2500)
ax[2,2].set_xlim(1750,2500)
ax[2,3].set_xlim(1750,2500)
ax[3,0].set_xlim(1750,2500)
ax[0,0].grid()
ax[0,1].grid()
ax[0,2].grid()
ax[0,3].grid()
ax[1,0].grid()
ax[1,1].grid()
ax[1,2].grid()
ax[1,3].grid()
ax[2,0].grid()
ax[2,1].grid()
ax[2,2].grid()
ax[2,3].grid()
ax[3,0].grid()
ax[0,0].set_title('CO2')
ax[0,1].set_title('CH4')
ax[0,2].set_title('N2O')
ax[0,3].set_title('Other WMGHGs')
ax[1,0].set_title('O3')
ax[1,1].set_title('Strat. H2O from CH4')
ax[1,2].set_title('Contrails')
ax[1,3].set_title('Aerosol radiation')
ax[2,0].set_title('Aerosol cloud')
ax[2,1].set_title('BC on snow')
ax[2,2].set_title('Land use change')
ax[2,3].set_title('Volcanic')
ax[3,0].set_title('Solar')
pl.tight_layout()
ax[3,0].legend(bbox_to_anchor=[3.6,0.5], frameon=False, ncol=2, loc='center right')
#pl.savefig('/nfs/see-fs-02_users/mencsm/ssp_erf/components.png')

# %% cell 48
for scenario in scenarios_full:
    forcing[scenario]['total_anthropogenic']=forcing[scenario]['co2']+forcing[scenario]['ch4']+forcing[scenario]['n2o']+\
        forcing[scenario]['other_wmghg']+\
        forcing[scenario]['o3']+forcing[scenario]['h2o_stratospheric']+forcing[scenario]['contrails']+\
        forcing[scenario]['aerosol-radiation_interactions']+forcing[scenario]['aerosol-cloud_interactions']+forcing[scenario]['bc_on_snow']+forcing[scenario]['land_use']
    forcing[scenario]['total_natural']=forcing[scenario]['volcanic']+forcing[scenario]['solar']
    forcing[scenario]['total']=forcing[scenario]['total_anthropogenic']+forcing[scenario]['total_natural']

# %% cell 49
pl.figure(figsize=(16,9))
for scenario in scenarios_full:
    pl.plot(np.arange(1750,2501), forcing[scenario]['o3'], label=scenario)
pl.grid()
pl.legend()

# %% cell 50
pl.figure(figsize=(29.7/2.54,21/2.54))
for scenario in scenarios_full:
    pl.plot(np.arange(1750,2501), forcing[scenario]['total'], label=scenario, color=colors[scenario], ls=ls[scenario])
pl.yticks(np.arange(-4,14))
pl.xticks(np.arange(1750,2501,50))
pl.ylim(-4,14)
pl.xlim(1750,2500)
pl.legend()
pl.grid()
pl.title('Total Effective Radiative Forcing in SSP scenarios, 1750-2500')
pl.ylabel('W m$^{-2}$')
pl.tight_layout()
#pl.savefig('/nfs/see-fs-02_users/mencsm/ssp_erf/total.png')

# %% cell 51
mkdir_p('../data_output/SSPs/')

for scenario in scenarios + ['ssp370-lowNTCFCH4']:
    df = pd.DataFrame(data=forcing[scenario], index=np.arange(1750,2501))
    df.index.name='year'
    df=df[['co2','ch4','n2o','other_wmghg','o3','h2o_stratospheric','contrails','aerosol-radiation_interactions','aerosol-cloud_interactions','bc_on_snow','land_use',
      'volcanic','solar','total_anthropogenic','total_natural','total']]
    outname = scenario
    if scenario=='ssp370-lowNTCF-aerchemmip':
        outname='ssp370-lowNTCF'
    df.to_csv('../data_output/SSPs/ERF_%s_1750-2500.csv' % outname)#
    df = pd.DataFrame(data=forcing[scenario], index=np.arange(1750,2501))
    df.index.name='year'
    df=df[gases_obs[3:]]
    df.to_csv('../data_output/SSPs/ERF_%s_minorGHGs_1750-2500.csv' % outname)
    df = new_emissions[scenario]
    df.index = np.arange(1750,2501)
    df.index.name='year'
    df.to_csv('../data_output_large/SSPs/emissions_%s_1750-2500.csv' % outname)
    df = pd.DataFrame(data=concentrations_out[scenario], index=np.arange(1750,2501))
    df.index.name='year'
    df.to_csv('../data_output_large/SSPs/conc_%s_1750-2500.csv' % outname)
df

# %% cell 52
scenario = 'ssp334'
df = pd.DataFrame(data=forcing[scenario], index=np.arange(1750,2501))
df.index.name='year'
df=df[['co2','ch4','n2o','other_wmghg','o3','h2o_stratospheric','contrails','aerosol-radiation_interactions','aerosol-cloud_interactions','bc_on_snow','land_use',
  'volcanic','solar','total_anthropogenic','total_natural','total']]
outname = scenario
df.to_csv('../data_output/SSPs/ERF_%s_1750-2500.csv' % outname)
df

# %% cell 53
df.loc[2000:2020]

# %% cell 55
# check aerosol ensemble ranges are correct
print(np.percentile(ERFari['ssp245'][255:265,:].mean(axis=0), (5,50,95)))
print(np.percentile(ERFaci['ssp245'][255:265,:].mean(axis=0), (5,50,95)))

# %% cell 56
seed    = 36572 
NINETY_TO_ONESIGMA = st.norm.ppf(0.95)

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

# %% cell 57
forcing_ensemble = {}

for scenario in tqdm(scenarios + ['ssp370-lowNTCFCH4'], desc='scenario'):
    forcing_ensemble[scenario] = {}
    for cat in tqdm(['co2','ch4','n2o','other_wmghg','o3','h2o_stratospheric','contrails','bc_on_snow',
               'land_use','volcanic'], leave=False, desc='category'):
        forcing_ensemble[scenario][cat] = forcing[scenario][cat][:,None] * scale_df['co2'].values[None,:]
    forcing_ensemble[scenario]['aerosol-radiation_interactions'] = ERFari[scenario]
    forcing_ensemble[scenario]['aerosol-cloud_interactions'] = ERFaci[scenario]
    forcing_ensemble[scenario]['solar'] = np.zeros((751, samples))
    forcing_ensemble[scenario]['solar'][:270, :] = np.linspace(0, trend_solar, 270) + solar_erf[:270, None] * scale_df['solar'].values[None,:]
    forcing_ensemble[scenario]['solar'][270:, :] = trend_solar + solar_erf[270:, None] * scale_df['solar'].values[None,:]
    forcing_ensemble[scenario]['total_anthropogenic'] = (
        forcing_ensemble[scenario]['co2'] +
        forcing_ensemble[scenario]['ch4'] +
        forcing_ensemble[scenario]['n2o'] +
        forcing_ensemble[scenario]['other_wmghg'] +
        forcing_ensemble[scenario]['o3'] + 
        forcing_ensemble[scenario]['h2o_stratospheric'] + 
        forcing_ensemble[scenario]['contrails'] + 
        forcing_ensemble[scenario]['bc_on_snow'] +
        forcing_ensemble[scenario]['land_use'] +
        forcing_ensemble[scenario]['aerosol-radiation_interactions'] + 
        forcing_ensemble[scenario]['aerosol-cloud_interactions']
    )
    forcing_ensemble[scenario]['total_natural'] = (
        forcing_ensemble[scenario]['solar'] +
        forcing_ensemble[scenario]['volcanic']
    )
    forcing_ensemble[scenario]['total'] = (
        forcing_ensemble[scenario]['co2'] +
        forcing_ensemble[scenario]['ch4'] +
        forcing_ensemble[scenario]['n2o'] +
        forcing_ensemble[scenario]['other_wmghg'] +
        forcing_ensemble[scenario]['o3'] + 
        forcing_ensemble[scenario]['h2o_stratospheric'] + 
        forcing_ensemble[scenario]['contrails'] + 
        forcing_ensemble[scenario]['bc_on_snow'] +
        forcing_ensemble[scenario]['land_use'] +
        forcing_ensemble[scenario]['aerosol-radiation_interactions'] + 
        forcing_ensemble[scenario]['aerosol-cloud_interactions'] +
        forcing_ensemble[scenario]['solar'] +
        forcing_ensemble[scenario]['volcanic']
    )

# %% cell 58
for scenario in tqdm(scenarios + ['ssp370-lowNTCFCH4']):
    df = pd.DataFrame(data=np.array([
        np.percentile(forcing_ensemble[scenario]['co2'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['ch4'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['n2o'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['other_wmghg'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['o3'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['h2o_stratospheric'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['contrails'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['aerosol-radiation_interactions'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['aerosol-cloud_interactions'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['bc_on_snow'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['land_use'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['volcanic'],5,axis=1),    
        np.percentile(forcing_ensemble[scenario]['solar'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['total_anthropogenic'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['total_natural'],5,axis=1),
        np.percentile(forcing_ensemble[scenario]['total'],5,axis=1)
    ]).T, index=np.arange(1750,2501))
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
        13:'total_anthropogenic',
        14:'total_natural',
        15:'total'
    })
    
    outname = scenario
    if scenario=='ssp370-lowNTCF-aerchemmip':
        outname='ssp370-lowNTCF'
    df.to_csv('../data_output/SSPs/ERF_%s_1750-2500_pc05.csv' % outname)
df

# %% cell 59
for scenario in tqdm(scenarios + ['ssp370-lowNTCFCH4']):
    df = pd.DataFrame(data=np.array([
        np.percentile(forcing_ensemble[scenario]['co2'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['ch4'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['n2o'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['other_wmghg'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['o3'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['h2o_stratospheric'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['contrails'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['aerosol-radiation_interactions'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['aerosol-cloud_interactions'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['bc_on_snow'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['land_use'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['volcanic'],95,axis=1),    
        np.percentile(forcing_ensemble[scenario]['solar'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['total_anthropogenic'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['total_natural'],95,axis=1),
        np.percentile(forcing_ensemble[scenario]['total'],95,axis=1)
    ]).T, index=np.arange(1750,2501))
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
        13:'total_anthropogenic',
        14:'total_natural',
        15:'total'
    })
    
    outname = scenario
    if scenario=='ssp370-lowNTCF-aerchemmip':
        outname='ssp370-lowNTCF'
    df.to_csv('../data_output/SSPs/ERF_%s_1750-2500_pc95.csv' % outname)
df

# %% cell 60
df_obs = pd.read_csv('../data_output/AR6_ERF_1750-2019.csv', index_col=0)

# %% cell 61
pl.rcParams['font.size'] = 16

# %% cell 62
#pl.figure(figsize=(29.7/2.54,21/2.54))
pl.figure(figsize=(16,9))
for scenario in scenarios:
    pl.plot(np.arange(1980,2026), forcing[scenario]['total'][230:276], label=scenario, color=colors[scenario], ls=ls[scenario])
pl.plot(np.arange(1980,2020), df_obs['total'].loc[1980:2020], color='k', label='AR6')
pl.yticks(np.arange(-4,14))
#pl.xticks(np.arange(1750,2501,50))
pl.ylim(-0.5,3.5)
pl.xlim(1980,2025)
pl.legend()
pl.grid()
pl.title('Total Effective Radiative Forcing in SSP scenarios, 1980-2025')
pl.ylabel('W m$^{-2}$')
pl.tight_layout()
#pl.savefig('../plots/total_1980-2025.png')

# %% cell 63
pl.figure(figsize=(16,9))
for scenario in scenarios:
    pl.plot(np.arange(1950,2031), forcing[scenario]['aerosol-radiation_interactions'][200:281]+forcing[scenario]['aerosol-cloud_interactions'][200:281], label=scenario, color=colors[scenario], ls=ls[scenario])
pl.plot(np.arange(1950,2020), df_obs['aerosol-radiation_interactions'].loc[1950:2020]+df_obs['aerosol-cloud_interactions'].loc[1950:2020], color='k', label='AR6')
#pl.yticks(np.arange(-1.5,0.25))
#pl.xticks(np.arange(1750,2501,50))
pl.ylim(-1.5,0)
pl.xlim(1950,2030)
pl.legend()
pl.grid()
pl.title('Total Aerosol Radiative Forcing in SSP scenarios, 1950-2030')
pl.ylabel('W m$^{-2}$')
pl.tight_layout()
#pl.savefig('../plots/total_1980-2025.png')

# %% cell 64
pl.figure(figsize=(16,9))
for scenario in scenarios:
    pl.plot(np.arange(2000,2101), forcing[scenario]['o3'][250:351], label=scenario, color=colors[scenario], ls=ls[scenario])
pl.plot(np.arange(2000,2020), df_obs['o3'].loc[2000:2019], color='k', label='AR6')
#pl.yticks(np.arange(-1.5,0.25))
#pl.xticks(np.arange(1750,2501,50))
pl.ylim(0,1.0)
pl.xlim(2000,2100)
pl.legend(ncol=2)
pl.grid()
pl.title('Total Ozone Radiative Forcing in SSP scenarios, 2000-2100')
pl.ylabel('W m$^{-2}$')
pl.tight_layout()
#pl.savefig('../plots/total_1980-2025.png')

# %% cell 66
forcing_ensemble['year'] = np.arange(1750, 2501)
save_dict_to_hdf5(forcing_ensemble, '../data_output_large/SSP_ERF_ensemble.h5')

# %% cell 68
# climate_model = 'AR6-ERF-v%4d%02d%02d' % (dt.date.today().year, dt.date.today().month, dt.date.today().day)
# model         = 'unspecified'
# region        = 'World'
# variable      = 'Effective Radiative Forcing'
# unit          = 'W/m^2'

# %% cell 69
# mkdir_p('../data_output_large/SSPs/')
# for scenario in scenarios:
#     data = scmdata.ScmRun(
#         forcing_ensemble[scenario]['total'], 
#         columns={
#             "model": [model],
#             "climate_model": [climate_model],
#             "scenario": [scenario],
#             "variable": [variable],
#             "region": [region],
#             "unit": [unit],
#             "ensemble_member": range(100000)
#         },
#         index=range(1750,2501)
#     )
    
#     outfile_path = '../data_output_large/SSPs/figure_4_41_AR6-ERF_%s_effective-radiative-forcing.nc' % scenario
    
#     # fair_data should be an ScmRun with different ensemble members labelled
#     # in an 'ensemble_member' column. 
#     assert set(data.meta.columns.tolist()) == {
#         "climate_model",
#         "ensemble_member",
#         "model",
#         "region",
#         "scenario",
#         "unit",
#         "variable",
#     }

#     for ss in data.groupby(["climate_model", "scenario", "variable"]):
#         climate_model = ss.get_unique_meta("climate_model", True)
#         scenario = ss.get_unique_meta("scenario", True)
#         variable = ss.get_unique_meta("variable", True)
#         ss.to_nc(outfile_path, dimensions=("ensemble_member",))
