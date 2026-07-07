# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/212_SPM_projections_AR6.ipynb

# %% cell 2
import fair
import json
import sys
import os
import random
import numpy as np
import scipy.stats as st       # v1.4+ needed
import matplotlib.pyplot as pl
import pandas as pd
from multiprocessing import Pool

from ar6.utils.h5 import *
from ar6.forcing.aerosol import aerocom_n, ghan
from ar6.twolayermodel import TwoLayerModel
from ar6.constants import NINETY_TO_ONESIGMA

from netCDF4 import Dataset
from tqdm import tqdm_notebook
from scipy.interpolate import interp1d

from tqdm.notebook import tqdm

# %% cell 4
with open('../data_input/random_seeds.json', 'r') as filehandle:
    SEEDS = json.load(filehandle)

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
    global_total[species] = df.sum(axis=0).values[3:].astype(float) / 1000 
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

# %% cell 8
# ozone
ozone_feedback = np.load('../data_input_large/fair-samples/ozone_feedback_unconstrained.npy')
beta_ch4 = np.load('../data_input_large/fair-samples/beta_ch4_unconstrained.npy')
beta_n2o = np.load('../data_input_large/fair-samples/beta_n2o_unconstrained.npy')
beta_ods = np.load('../data_input_large/fair-samples/beta_ods_unconstrained.npy')
beta_co = np.load('../data_input_large/fair-samples/beta_co_unconstrained.npy')
beta_voc = np.load('../data_input_large/fair-samples/beta_voc_unconstrained.npy')
beta_nox = np.load('../data_input_large/fair-samples/beta_nox_unconstrained.npy')

# carbon cycle
r0 = np.load('../data_input_large/fair-samples/r0_unconstrained.npy')
rC = np.load('../data_input_large/fair-samples/rC_unconstrained.npy')
rT = np.load('../data_input_large/fair-samples/rT_unconstrained.npy')
pre_ind_co2 = np.load('../data_input_large/fair-samples/pre_ind_co2_unconstrained.npy')

# aerosol
beta_so2 = np.load('../data_input_large/fair-samples/beta_so2_unconstrained.npy')
beta_bc = np.load('../data_input_large/fair-samples/beta_bc_unconstrained.npy')
beta_oc = np.load('../data_input_large/fair-samples/beta_oc_unconstrained.npy')
beta_nh3 = np.load('../data_input_large/fair-samples/beta_nh3_unconstrained.npy')
beta = np.load('../data_input_large/fair-samples/beta_unconstrained.npy')
aci_coeffs = np.load('../data_input_large/fair-samples/aci_coeffs.npy')

# forcing
scale_normals = np.load('../data_input_large/fair-samples/scale_normals.npy')
trend_solar = np.load('../data_input_large/fair-samples/scale_trend_solar.npy')

# climate response
geoff_sample_df = pd.read_csv('../data_output_large/geoff_sample.csv', index_col=0)
f2x = np.load('../data_input_large/fair-samples/f2x_unconstrained.npy')
ecs = np.load('../data_input_large/fair-samples/ecs_unconstrained.npy')
tcr = np.load('../data_input_large/fair-samples/tcr_unconstrained.npy')

# accepted ensemble
accept_inds = np.loadtxt('../data_output_large/fair-samples/accept_inds.csv', dtype=int)

# %% cell 10
accept_inds

# %% cell 11
geoff_sample_df.loc[accept_inds]

# %% cell 12
# ozone
ozone_feedback = ozone_feedback[accept_inds]
beta_ch4 = beta_ch4[accept_inds]
beta_n2o = beta_n2o[accept_inds]
beta_ods = beta_ods[accept_inds]
beta_co = beta_co[accept_inds]
beta_voc = beta_voc[accept_inds]
beta_nox = beta_nox[accept_inds]

# carbon cycle
pre_ind_co2 = pre_ind_co2[accept_inds]
r0 = r0[accept_inds]
rC = rC[accept_inds]
rT = rT[accept_inds]

# aerosol
beta_so2 = beta_so2[accept_inds]
beta_bc = beta_bc[accept_inds]
beta_oc = beta_oc[accept_inds]
beta_nh3 = beta_nh3[accept_inds]
beta = beta[accept_inds]
aci_coeffs = aci_coeffs[accept_inds]

# forcing
scale_normals = scale_normals[accept_inds]
trend_solar = trend_solar[accept_inds]

# climate response
geoff_sample_df = geoff_sample_df.loc[accept_inds]
f2x = f2x[accept_inds]
ecs = ecs[accept_inds]
tcr = tcr[accept_inds]

# %% cell 13
f2x_median = np.median(f2x)
ecs_median = np.median(ecs)
tcr_median = np.median(tcr)

# %% cell 14
kappa = f2x/tcr - f2x/ecs
# kappa = efficacy * eta
pl.hist(kappa)

# %% cell 15
lamg = geoff_sample_df['lamg'].values
eff = geoff_sample_df['eff'].values
gamma_2l = geoff_sample_df['gamma_2l'].values
cdeep = geoff_sample_df['cdeep'].values
cmix = geoff_sample_df['cmix'].values

# %% cell 18
ERFari = np.zeros((270, len(accept_inds)))
ERFaci = np.zeros((270, len(accept_inds)))

so2 = emissions_ceds_update.loc[:,'SO2']
bc = emissions_ceds_update.loc[:,'BC']
oc = emissions_ceds_update.loc[:,'OC']
nh3 = emissions_ceds_update.loc[:,'NH3']

for i in tqdm(range(len(accept_inds))):
    ERFari[:, i] = (
        (emissions_ceds_update.loc[:,'SO2']-emissions_ceds_update.loc[1750,'SO2']) * beta_so2[i] * 32/64 +
        (emissions_ceds_update.loc[:,'BC']-emissions_ceds_update.loc[1750,'BC']) * beta_bc[i] +
        (emissions_ceds_update.loc[:,'OC']-emissions_ceds_update.loc[1750,'OC']) * beta_oc[i] +
        (emissions_ceds_update.loc[:,'NH3']-emissions_ceds_update.loc[1750,'NH3']) * beta_nh3[i]
    )
    
    ERFaci[:,i] = ghan([so2 * 32/64, bc+oc], beta[i], aci_coeffs[i,0], aci_coeffs[i,1]) - ghan([so2[1750] * 32/64, bc[1750]+oc[1750]], beta[i], aci_coeffs[i,0], aci_coeffs[i,1])

# %% cell 19
pl.fill_between(np.arange(1750, 2020), np.percentile(ERFari, 5, axis=1), np.percentile(ERFari, 95, axis=1), color='k', alpha=0.5)
pl.plot(np.arange(1750,2020), np.percentile(ERFari, 50, axis=1), color='k')
pl.grid()

# %% cell 20
pl.fill_between(np.arange(1750, 2020), np.percentile(ERFaci, 5, axis=1), np.percentile(ERFaci, 95, axis=1), color='k', alpha=0.5)
pl.plot(np.arange(1750,2020), np.percentile(ERFaci, 50, axis=1), color='k')
pl.grid()

# %% cell 21
pl.fill_between(np.arange(1750, 2020), np.percentile(ERFari+ERFaci, 5, axis=1), np.percentile(ERFari+ERFaci, 95, axis=1), color='k', alpha=0.5)
pl.plot(np.arange(1750,2020), np.percentile(ERFari+ERFaci, 50, axis=1), color='k')
pl.grid()

# %% cell 23
forcing_by_emissions = pd.read_csv('../data_input/chapter6_emissions_attribution/2019_ERF_est.csv', index_col=0)
forcing_by_emissions.rename(
    columns={
        'CO2': 'co2',
        'CH4_lifetime': 'ch4',
        'Strat_H2O': 'h2o_stratospheric',
        'Aerosol': 'aerosol-radiation_interactions',
        'Cloud': 'aerosol-cloud_interactions',
        'O3': 'o3',
        'HC': 'other_wmghg',
        'N2O': 'n2o'
    },
    index = {
        'CO2': 'co2',
        'CH4': 'ch4',
        'N2O': 'n2o',
        'HC': 'other_wmghg',
    },
    inplace=True
)
forcing_by_emissions.drop(columns='HFCs', inplace=True)
forcing_by_emissions_ratio = forcing_by_emissions / forcing_by_emissions.sum(axis=0)
forcing_by_emissions_ratio

# %% cell 25
scale_normals.shape

# %% cell 26
df = pd.read_csv('../data_output/AR6_ERF_1750-2019.csv')
forcing_ensemble = {}
#for cat in ['co2', 'ch4', 'n2o', 'other_wmghg', 'o3', 'h2o_stratospheric', 'contrails', 'aerosol-radiation_interactions',
##           'aerosol-cloud_interactions', 'bc_on_snow', 'land_use', 'solar', 'volcanic', 'wmghgs', 'aerosol', 'albedo',
#           'anthro', 'natural']:
#    forcing_ensemble[cat] = np.zeros((270, len(accept_inds)))
    
# naming convention: emissions_resulting-forcing
forcing_ensemble['co2_co2'] = df['co2'].values[:,None] * scale_normals[:,0] * forcing_by_emissions_ratio.loc['co2', 'co2']
forcing_ensemble['ch4_co2'] = df['co2'].values[:,None] * scale_normals[:,0] * forcing_by_emissions_ratio.loc['ch4', 'co2']
forcing_ensemble['oth_co2'] = df['co2'].values[:,None] * scale_normals[:,0] * forcing_by_emissions_ratio.loc['other_wmghg', 'co2']
forcing_ensemble['voc_co2'] = df['co2'].values[:,None] * scale_normals[:,0] * forcing_by_emissions_ratio.loc['VOC', 'co2']

forcing_ensemble['ch4_ch4'] = df['ch4'].values[:,None] * scale_normals[:,1] * forcing_by_emissions_ratio.loc['ch4', 'ch4']
forcing_ensemble['n2o_ch4'] = df['ch4'].values[:,None] * scale_normals[:,1] * forcing_by_emissions_ratio.loc['n2o', 'ch4']
forcing_ensemble['oth_ch4'] = df['ch4'].values[:,None] * scale_normals[:,1] * forcing_by_emissions_ratio.loc['other_wmghg', 'ch4']
forcing_ensemble['nox_ch4'] = df['ch4'].values[:,None] * scale_normals[:,1] * forcing_by_emissions_ratio.loc['NOx', 'ch4']
forcing_ensemble['voc_ch4'] = df['ch4'].values[:,None] * scale_normals[:,1] * forcing_by_emissions_ratio.loc['VOC', 'ch4']

forcing_ensemble['n2o_n2o'] = df['n2o'].values[:,None] * scale_normals[:,2]

forcing_ensemble['oth_oth'] = df['other_wmghg'].values[:,None] * scale_normals[:,3]

forcing_ensemble['ch4_ozo'] = df['o3'].values[:,None] * scale_normals[:,4] * forcing_by_emissions_ratio.loc['ch4', 'o3']
forcing_ensemble['n2o_ozo'] = df['o3'].values[:,None] * scale_normals[:,4] * forcing_by_emissions_ratio.loc['n2o', 'o3']
forcing_ensemble['oth_ozo'] = df['o3'].values[:,None] * scale_normals[:,4] * forcing_by_emissions_ratio.loc['other_wmghg', 'o3']
forcing_ensemble['nox_ozo'] = df['o3'].values[:,None] * scale_normals[:,4] * forcing_by_emissions_ratio.loc['NOx', 'o3']
forcing_ensemble['voc_ozo'] = df['o3'].values[:,None] * scale_normals[:,4] * forcing_by_emissions_ratio.loc['VOC', 'o3']

forcing_ensemble['ch4_h2o'] = df['h2o_stratospheric'].values[:,None] * scale_normals[:,5]

forcing_ensemble['con_con'] = df['contrails'].values[:,None] * scale_normals[:,6]

forcing_ensemble['ch4_ari'] = ERFari * forcing_by_emissions_ratio.loc['ch4', 'aerosol-radiation_interactions']
forcing_ensemble['n2o_ari'] = ERFari * forcing_by_emissions_ratio.loc['n2o', 'aerosol-radiation_interactions']
forcing_ensemble['oth_ari'] = ERFari * forcing_by_emissions_ratio.loc['other_wmghg', 'aerosol-radiation_interactions']
forcing_ensemble['nox_ari'] = ERFari * forcing_by_emissions_ratio.loc['NOx', 'aerosol-radiation_interactions']
forcing_ensemble['voc_ari'] = ERFari * forcing_by_emissions_ratio.loc['VOC', 'aerosol-radiation_interactions']
forcing_ensemble['so2_ari'] = ERFari * forcing_by_emissions_ratio.loc['SO2', 'aerosol-radiation_interactions']
forcing_ensemble['blc_ari'] = ERFari * forcing_by_emissions_ratio.loc['BC', 'aerosol-radiation_interactions']
forcing_ensemble['orc_ari'] = ERFari * forcing_by_emissions_ratio.loc['OC', 'aerosol-radiation_interactions']
forcing_ensemble['nh3_ari'] = ERFari * forcing_by_emissions_ratio.loc['NH3', 'aerosol-radiation_interactions']

forcing_ensemble['ch4_aci'] = ERFaci * forcing_by_emissions_ratio.loc['ch4', 'aerosol-cloud_interactions']
forcing_ensemble['n2o_aci'] = ERFaci * forcing_by_emissions_ratio.loc['n2o', 'aerosol-cloud_interactions']
forcing_ensemble['oth_aci'] = ERFaci * forcing_by_emissions_ratio.loc['other_wmghg', 'aerosol-cloud_interactions']
forcing_ensemble['nox_aci'] = ERFaci * forcing_by_emissions_ratio.loc['NOx', 'aerosol-cloud_interactions']
forcing_ensemble['voc_aci'] = ERFaci * forcing_by_emissions_ratio.loc['VOC', 'aerosol-cloud_interactions']
forcing_ensemble['so2_aci'] = ERFaci * forcing_by_emissions_ratio.loc['SO2', 'aerosol-cloud_interactions']
forcing_ensemble['blc_aci'] = ERFaci * forcing_by_emissions_ratio.loc['BC', 'aerosol-cloud_interactions']
forcing_ensemble['orc_aci'] = ERFaci * forcing_by_emissions_ratio.loc['OC', 'aerosol-cloud_interactions']

forcing_ensemble['blc_bcs'] = df['bc_on_snow'].values[:,None] * scale_normals[:,7]

forcing_ensemble['luc_luc'] = df['land_use'].values[:,None] * scale_normals[:,8]

forcing_ensemble['anthro'] = (
    forcing_ensemble['co2_co2'] +
    forcing_ensemble['ch4_co2'] +
    forcing_ensemble['oth_co2'] +
    forcing_ensemble['voc_co2'] +
    forcing_ensemble['ch4_ch4'] +
    forcing_ensemble['n2o_ch4'] +
    forcing_ensemble['oth_ch4'] +
    forcing_ensemble['nox_ch4'] +
    forcing_ensemble['voc_ch4'] +
    forcing_ensemble['n2o_n2o'] +
    forcing_ensemble['oth_oth'] +
    forcing_ensemble['ch4_ozo'] +
    forcing_ensemble['n2o_ozo'] +
    forcing_ensemble['oth_ozo'] +
    forcing_ensemble['nox_ozo'] +
    forcing_ensemble['voc_ozo'] +
    forcing_ensemble['ch4_h2o'] +
    forcing_ensemble['con_con'] +
    forcing_ensemble['ch4_ari'] +
    forcing_ensemble['n2o_ari'] +
    forcing_ensemble['oth_ari'] +
    forcing_ensemble['nox_ari'] +
    forcing_ensemble['voc_ari'] +
    forcing_ensemble['so2_ari'] +
    forcing_ensemble['blc_ari'] +
    forcing_ensemble['orc_ari'] +
    forcing_ensemble['nh3_ari'] +
    forcing_ensemble['ch4_aci'] +
    forcing_ensemble['n2o_aci'] +
    forcing_ensemble['oth_aci'] +
    forcing_ensemble['nox_aci'] +
    forcing_ensemble['voc_aci'] +
    forcing_ensemble['so2_aci'] +
    forcing_ensemble['blc_aci'] +
    forcing_ensemble['orc_aci'] +
    forcing_ensemble['blc_bcs'] +
    forcing_ensemble['luc_luc']
)

# %% cell 27
forcing_ensemble['anthro'].shape

# %% cell 29
with open('../data_input/tunings/cmip6_twolayer_tuning_params.json', 'r') as filehandle:
    cmip6_models = json.load(filehandle)

# %% cell 30
cmix_mean = cmip6_models['cmix']['mean']['EBM-epsilon']
cdeep_mean = cmip6_models['cdeep']['mean']['EBM-epsilon']
eff_mean = cmip6_models['eff']['mean']['EBM-epsilon']

lamg_median = f2x_median/ecs_median
kappa_median = -(f2x_median/ecs_median - f2x_median/tcr_median)
gamma_2l_median = kappa_median/eff_mean

# %% cell 31
gamma_2l_median, kappa_median, lamg_median, eff_mean, cmix_mean, cdeep_mean

# %% cell 32
results = {}

# %% cell 33
forcing_ensemble.keys()

# %% cell 35
arglist = []

lamg = -geoff_sample_df['lamg'].values
eff = geoff_sample_df['eff'].values
gamma_2l = geoff_sample_df['gamma_2l'].values
cdeep = geoff_sample_df['cdeep'].values
cmix = geoff_sample_df['cmix'].values


for i in range(len(accept_inds)):
    arglist.append(
        {
            'cmix': cmix[i],
            'cdeep': cdeep[i],
            'gamma_2l': gamma_2l[i],
            'lamg': lamg[i],
            'eff': eff[i],
            'in_forcing' : forcing_ensemble['anthro'][:,i],
            'firstyear': 1750
        }
    )

results['AR6-anthro_climuncert'] = {}

def run_tlm(args):
    in_forcing = args['in_forcing']
    driver = TwoLayerModel(
        extforce=in_forcing,
        exttime=np.arange(args['firstyear'],2020),
        tbeg=args['firstyear'],
        tend=2020,
        lamg=args['lamg'],
        t2x=None,
        eff=args['eff'],
        cmix=args['cmix'],
        cdeep=args['cdeep'],
        gamma_2l=args['gamma_2l'],
        outtime=np.arange(1750,2020),
        dt=0.2
    )
    output = driver.run()
    return(output.tg)
    
    
if __name__ == '__main__':
    with Pool(24) as pool:
        result = list(tqdm(pool.imap(run_tlm, arglist), total=len(accept_inds)))
    output = np.array(result).T

results['AR6-anthro_climuncert']['effective_radiative_forcing'] = forcing_ensemble['anthro']
results['AR6-anthro_climuncert']['surface_temperature'] = output

# %% cell 36
results['AR6-anthro_climuncert']['surface_temperature'].shape

# %% cell 37
pl.fill_between(np.arange(1750, 2020),
                np.percentile(results['AR6-anthro_climuncert']['surface_temperature'], 5, axis=1),
                np.percentile(results['AR6-anthro_climuncert']['surface_temperature'], 95, axis=1),
               )
pl.plot(np.arange(1750, 2020), np.median(results['AR6-anthro_climuncert']['surface_temperature'], axis=1), color='k')

# %% cell 39
if __name__ == '__main__':
    for agent in tqdm(list(forcing_ensemble.keys())[:-1], desc='Removing one at a time'):
        arglist = []
        for i in range(len(accept_inds)):
            startindex=0
            firstyear = 1750
            in_forcing = forcing_ensemble['anthro'][startindex:,i] - forcing_ensemble[agent][startindex:,i]
            arglist.append(
                {
                    'in_forcing' : in_forcing,
                    'cmix': cmix[i],
                    'cdeep': cdeep[i],
                    'gamma_2l': gamma_2l[i],
                    'lamg': lamg[i],
                    'eff': eff[i],
                    'firstyear': firstyear
                }
            )
        output = []
        results['remove_%s_climuncert' % agent] = {}
        with Pool(24) as pool:
            result = list(tqdm(pool.imap(run_tlm, arglist), total=len(accept_inds), leave=False))
        output = np.array(result).T

        results['remove_%s_climuncert' % agent]['effective_radiative_forcing'] = forcing_ensemble['anthro'] - forcing_ensemble[agent]
        results['remove_%s_climuncert' % agent]['surface_temperature'] = output

# %% cell 40
save_dict_to_hdf5(results, '../data_output_large/twolayer_AR6-historical-emissions-based.h5')
