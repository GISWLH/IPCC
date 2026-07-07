# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/162_unused_reconstrain_fair_samples.ipynb

# %% cell 2
import json
import random
import numpy as np
import scipy.stats as st       # v1.4+ needed
import matplotlib.pyplot as pl
import pandas as pd
import pickle
import warnings
from multiprocessing import Pool

from netCDF4 import Dataset
from tqdm.notebook import tqdm
from scipy.interpolate import interp1d
from scipy.optimize import root
from fair.constants import molwt
from fair.ancil import natural, cmip6_volcanic, cmip6_solar
from fair.forward import fair_scm
from fair.inverse import inverse_fair_scm
from fair.constants.general import ppm_gtc, EARTH_RADIUS, SECONDS_PER_YEAR
NTOA_ZJ = 4 * np.pi * EARTH_RADIUS**2 * SECONDS_PER_YEAR * 1e-21

# %% cell 3
pl.rcParams['figure.figsize'] = (12/2.54, 9/2.54)
pl.rcParams['font.size'] = 14
pl.rcParams['font.family'] = 'Arial'
pl.rcParams['xtick.direction'] = 'out'
pl.rcParams['xtick.minor.visible'] = True
pl.rcParams['ytick.minor.visible'] = True
pl.rcParams['ytick.right'] = True
pl.rcParams['xtick.top'] = True
pl.rcParams['figure.dpi'] = 96

# %% cell 5
xl = pd.read_excel('../data_input/observations/AR6 FGD assessment time series - GMST and GSAT.xlsx', skiprows=1, skipfooter=28)
temp_gmst=xl['4-set mean'].values
temp_year=xl['Unnamed: 0'].values
pl.plot(temp_year, temp_gmst)

temp_gmst[-1]

# %% cell 6
OHC_df = pd.read_csv("../data_input/observations/AR6_OHC_ensemble_FGDprelim.csv", skiprows=1)
OHC_df

# %% cell 7
OHUobs = OHC_df['Central Estimate Full-depth'].values
OHUyears = OHC_df['Year'].values

# %% cell 8
OHU90 = OHC_df['Full-depth Uncertainty (1-sigma)'].values

# %% cell 10
with open('../data_input/random_seeds.json', 'r') as filehandle:
    SEEDS = json.load(filehandle)

# %% cell 11
SAMPLES = 1000000
F2XCO2_MEAN = 4.00
F2XCO2_NINETY = 0.48

# %% cell 13
geoff_sample_df = pd.read_csv('../data_output_large/geoff_sample.csv', index_col=0)
geoff_sample_df

# %% cell 14
ecs = np.load('../data_input_large/fair-samples/ecs_unconstrained.npy')
tcr = np.load('../data_input_large/fair-samples/tcr_unconstrained.npy')
f2x = np.load('../data_input_large/fair-samples/f2x_unconstrained.npy')

# %% cell 16
r0 = np.load('../data_input_large/fair-samples/r0_unconstrained.npy')
rC = np.load('../data_input_large/fair-samples/rC_unconstrained.npy')
rT = np.load('../data_input_large/fair-samples/rT_unconstrained.npy')
pre_ind_co2 = np.load('../data_input_large/fair-samples/pre_ind_co2_unconstrained.npy')

# %% cell 18
C_CO2 = np.load('../data_output_large/fair-samples/C_CO2_unconstrained.npy')
F_O3 = np.load('../data_output_large/fair-samples/F_O3_unconstrained.npy')
F_dir = np.load('../data_output_large/fair-samples/F_ERFari_unconstrained.npy')
F_ind = np.load('../data_output_large/fair-samples/F_ERFaci_unconstrained.npy')
F_ant = np.load('../data_output_large/fair-samples/F_anthro_unconstrained.npy')
F_tot = np.load('../data_output_large/fair-samples/F_total_unconstrained.npy')
T = np.load('../data_output_large/fair-samples/T_unconstrained.npy')
OHU = np.load('../data_output_large/fair-samples/OHU_unconstrained.npy')
AF = np.load('../data_output_large/fair-samples/AF_unconstrained.npy')

# %% cell 19
F_O3.shape

# %% cell 20
def rmse(obs, mod):
    return np.sqrt(np.sum((obs-mod)**2)/len(obs))

# %% cell 22
## simple criterion: RMSE of temperature 1850-2014 < 0.135
rmse_temp = np.zeros((SAMPLES))
for i in range(SAMPLES):
    rmse_temp[i] = rmse(temp_gmst[:165], (T[100:265,i]-np.mean(T[100:151,i], axis=0)))
accept_temp=(rmse_temp<0.135)
print(np.sum(accept_temp))
valid_temp = np.arange(SAMPLES, dtype=int)[accept_temp]

# %% cell 23
# accept_temp = np.logical_and(
#     T[245:265].mean(axis=0)-T[100:151].mean(axis=0) < 0.98,
#     0.67 < T[245:265].mean(axis=0)-T[100:151].mean(axis=0)
# )
# valid_temp = np.arange(SAMPLES, dtype=int)[accept_temp]
# print(np.sum(accept_temp))

# %% cell 24
pl.hist(T[245:265,accept_temp].mean(axis=0) - T[100:151,accept_temp].mean(axis=0))

# %% cell 25
pl.fill_between(
    np.arange(1850, 2021),
    np.percentile(T[100:271,accept_temp]-np.mean(T[100:151,accept_temp], axis=0), 5, axis=1),
    np.percentile(T[100:271,accept_temp]-np.mean(T[100:151,accept_temp], axis=0), 95, axis=1), 
    color='gray', lw=0, alpha=0.5
)
pl.plot(
    np.arange(1850, 2021), 
    np.percentile(T[100:271,accept_temp]-np.mean(T[100:151,accept_temp], axis=0), 50, axis=1),
    color='k'
)
pl.plot(np.arange(1850, 2021), temp_gmst, color='blue')
pl.title('Historically constrained - temperature')
pl.ylabel('K')
pl.tight_layout()

# %% cell 26
# GMST target 0.67 0.85 0.98
print(np.percentile(np.mean(T[245:265,accept_temp], axis=0)-np.mean(T[100:151,accept_temp], axis=0), (5, 16, 50, 84, 95)))

# %% cell 28
((OHUobs[-1]-OHUobs[0]) - np.sqrt(OHU90[0]**2+OHU90[-1]**2))

# %% cell 29
accept_ohu = np.logical_and(
    ((OHUobs[-1]-OHUobs[0]) - np.sqrt(OHU90[0]**2+OHU90[-1]**2)) < 0.90*(OHU[268,:]-OHU[221,:])*1e-21,
    0.90*(OHU[268,:]-OHU[221,:])*1e-21 < ((OHUobs[-1]-OHUobs[0]) + np.sqrt(OHU90[0]**2+OHU90[-1]**2))
)
valid_ohu = np.arange(SAMPLES, dtype=int)[accept_ohu]
print(np.sum(accept_ohu))

# %% cell 30
pl.fill_between(OHUyears, OHUobs-OHU90, OHUobs+OHU90, color='blue', lw=0, alpha=0.5)
pl.plot(OHUyears, OHUobs, color='blue')
pl.fill_between(np.arange(1750.5, 2019), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept_ohu]-OHU[268,accept_ohu]), 5, axis=1), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept_ohu]-OHU[268,accept_ohu]), 95, axis=1), color='gray', lw=0, alpha=0.5)
pl.plot(np.arange(1750.5,2019), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept_ohu]-OHU[268,accept_ohu]), 50, axis=1), color='k')
pl.title('Historically constrained - ocean heat')
pl.xlim(1971,2019)
pl.ylim(-100,440)
pl.ylabel('ZJ')
pl.tight_layout()

# %% cell 32
conc_all = pd.read_csv('../data_input_large/rcmip-concentrations-annual-means-v5-1-0.csv')
co2_obs = conc_all[(conc_all['Scenario']=='ssp245')&(conc_all['Region']=='World')&(conc_all.Variable.str.endswith('CO2'))].loc[:,'1750':'2018'].values.squeeze()
co2_obs.shape

# %% cell 33
pl.hist(C_CO2[0,:])

# %% cell 34
C_CO2.shape

# %% cell 35
accept_co2 = np.logical_and( (co2_obs[264] - 0.36) < C_CO2[264], C_CO2[264] < (co2_obs[264] + 0.36) )
print(np.sum(accept_co2))
valid_co2 = np.arange(SAMPLES, dtype=int)[accept_co2]

# %% cell 36
pl.fill_between(
    np.arange(1750, 2019),
    np.percentile(C_CO2[:269,accept_co2], 5, axis=1),
    np.percentile(C_CO2[:269,accept_co2], 95, axis=1), 
    color='gray', lw=0, alpha=0.5
)
pl.plot(
    np.arange(1750, 2019), 
    np.percentile(C_CO2[:269,accept_co2], 50, axis=1),
    color='k'
)
pl.plot(np.arange(1750, 2019), co2_obs, color='blue')
pl.title('Historically constrained - CO2')
pl.ylabel('ppm')
pl.tight_layout()

# %% cell 37
pl.hist(rC[accept_co2])

# %% cell 38
accept_ssp245 = accept_temp * accept_ohu * accept_co2
accept_inds = (np.arange(len(accept_ssp245), dtype=int))[accept_ssp245]
accept_inds

# %% cell 39
len(accept_inds)

# %% cell 40
pl.hist(rC[accept_inds])

# %% cell 41
pl.hist(rT[accept_inds])

# %% cell 42
pl.hist(r0[accept_inds], density=True)

# %% cell 43
pl.fill_between(
    np.arange(1750, 2101),
    np.percentile(C_CO2[:,accept_inds], 5, axis=1),
    np.percentile(C_CO2[:,accept_inds], 95, axis=1), 
    color='gray', lw=0, alpha=0.5
)
pl.plot(
    np.arange(1750, 2101), 
    np.percentile(C_CO2[:,accept_inds], 50, axis=1),
    color='k'
)
pl.plot(np.arange(1750, 2019), co2_obs, color='blue')
pl.title('Historically constrained - CO2')

# %% cell 44
pl.fill_between(
    np.arange(1850, 2021),
    np.percentile(T[100:271,accept_inds]-np.mean(T[100:151,accept_inds], axis=0), 5, axis=1),
    np.percentile(T[100:271,accept_inds]-np.mean(T[100:151,accept_inds], axis=0), 95, axis=1), 
    color='gray', lw=0, alpha=0.5
)
pl.plot(
    np.arange(1850, 2021), 
    np.percentile(T[100:271,accept_inds]-np.mean(T[100:151,accept_inds], axis=0), 50, axis=1),
    color='k'
)
pl.plot(np.arange(1850, 2021), temp_gmst, color='blue')
pl.title('Historically constrained - temperature')

# %% cell 45
# target 0.67 0.85 0.98 GMST
#print(np.percentile((np.mean(T[245:265,accept], axis=0)-np.mean(T[100:151,accept], axis=0))/1.04, (5, 16, 50, 84, 95)))
print(np.percentile(np.mean(T[245:265,accept_inds], axis=0)-np.mean(T[100:151,accept_inds], axis=0), (5, 16, 50, 84, 95)))

# %% cell 46
pl.fill_between(OHUyears, OHUobs-OHU90, OHUobs+OHU90, color='blue', lw=0, alpha=0.5)
pl.plot(OHUyears, OHUobs, color='blue')
pl.fill_between(np.arange(1750.5, 2019), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept_inds]-OHU[268,accept_inds]), 5, axis=1), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept_inds]-OHU[268,accept_inds]), 95, axis=1), color='gray', lw=0, alpha=0.5)
pl.plot(np.arange(1750.5,2019), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept_inds]-OHU[268,accept_inds]), 50, axis=1), color='k')
pl.title('Historically constrained - ocean heat')
pl.xlim(1971,2019)
pl.ylim(-100,440)
pl.ylabel('ZJ')
pl.tight_layout()

# %% cell 47
# target 0.67 0.85 0.98 GMST
np.percentile(np.mean(T[245:265,accept_inds],axis=0)-np.mean(T[100:151,accept_inds],axis=0), (5,16,50,84,95))

# %% cell 48
pl.hist(ecs[accept_inds], bins=np.arange(1.6,8.8,0.4), density=True)
# target 2.0 2.5 3.0 4.0 5.0
pl.xlabel('K')
pl.title('ECS: constrained')
pl.tight_layout()
np.percentile(ecs[accept_inds], (5,16,50,84,95))

# %% cell 49
pl.hist(tcr[accept_inds], bins=np.arange(0.8,3.2,0.2), density=True)
# target 1.2 1.4 1.8 2.2 2.4
pl.xlabel('K')
pl.title('TCR: constrained')
pl.tight_layout()
np.percentile(tcr[accept_inds], (5,16,50,84,95))

# %% cell 50
# target -0.6 -0.3 -0.0
pl.hist(np.mean(F_dir[255:265,accept_inds], axis=0), bins=np.arange(-0.8,0.2,0.1));
pl.title('aerosol ERFari')
np.percentile(np.mean(F_dir[255:265,accept_inds], axis=0), (5,16,50,84,95))

# %% cell 51
# target -1.7 -1.0 -0.3
pl.hist(np.mean(F_ind[255:265,accept_inds], axis=0), bins=np.arange(-2.0,0.2,0.1));
pl.title('aerosol ERFaci')
np.percentile(np.mean(F_ind[255:265,accept_inds], axis=0), (5,16,50,84,95))

# %% cell 52
# target -2 -1.3 -0.6
pl.hist(np.mean(F_dir[255:265,accept_inds], axis=0)+np.mean(F_ind[255:265,accept_inds], axis=0), bins=np.arange(-2.2,0.2,0.1), density=True);
pl.title('Aerosol ERF: 1750-2010')
pl.xlabel('W m$^{-2}$')
pl.tight_layout()
np.percentile(np.mean(F_dir[255:265,accept_inds], axis=0)+np.mean(F_ind[255:265,accept_inds], axis=0), (5,16,50,84,95))

# %% cell 53
pl.scatter(ecs[accept_inds], np.mean(F_dir[255:265,accept_inds], axis=0)+np.mean(F_ind[255:265,accept_inds], axis=0))

# %% cell 54
pl.scatter(ecs[accept_inds], tcr[accept_inds])

# %% cell 56
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
geoff_sample_df = pd.read_csv('../data_output_large/geoff_sample.csv')
f2x = np.load('../data_input_large/fair-samples/f2x_unconstrained.npy')

# add in natural emissions and natural forcing: go to 2110 for WG3
ch4_n2o_df = pd.read_csv('../data_output/fair_wg3_natural_ch4_n2o.csv')
ch4_n2o = ch4_n2o_df.values[:361,1:]

df = pd.read_csv('../data_output/solar_erf.csv', index_col='year')
solar_forcing = df.solar_erf.loc[1750:2110].values

df = pd.read_csv('../data_output/volcanic_erf.csv', index_col='year')
volcanic_forcing = np.zeros((361))
volcanic_forcing[:269] = df.volcanic_erf.loc[1750:2018].values
# ramp down last 10 years to zero according to https://www.geosci-model-dev.net/9/3461/2016/gmd-9-3461-2016.html
volcanic_forcing[268:279] = volcanic_forcing[268] * np.linspace(1,0,11)
volcanic_forcing[279:] = 0.

# %% cell 57
config_list = []
for ens in accept_inds:
    scale = np.ones(9)
    scale[0] = scale_normals[ens,1] * 0.86 # methane adjustment
    scale[1] = scale_normals[ens,2] * 1.07
    scale[2] = scale_normals[ens,3]
    scale[3:5] = scale_normals[ens,5:7]
    scale[5:9] = scale_normals[ens,7:11]
    fair_params = {
        'scale': scale.tolist(),
        'trend_solar': trend_solar[ens],
        'C_pi_CO2': pre_ind_co2[ens],
        'F2x' : f2x[ens],
        'r0'  : r0[ens],
        'rt'  : rT[ens],
        'rc'  : rC[ens],
        'lambda_global': -geoff_sample_df.loc[ens, 'lamg'],
        'ocean_heat_capacity':[geoff_sample_df.loc[ens, 'cmix'], geoff_sample_df.loc[ens, 'cdeep']],
        'ocean_heat_exchange':geoff_sample_df.loc[ens, 'gamma_2l'],
        'deep_ocean_efficacy':geoff_sample_df.loc[ens,'eff'],
        'b_aero': [beta_so2[ens], beta_bc[ens], beta_oc[ens], beta_nh3[ens]],
        'ghan_params':[beta[ens], aci_coeffs[ens,0], aci_coeffs[ens, 1]],
        'b_tro3': [beta_ch4[ens], beta_n2o[ens], beta_ods[ens], beta_co[ens], beta_voc[ens], beta_nox[ens]],
        'ozone_feedback': ozone_feedback[ens],

    }
    config_list.append(fair_params)
with open('../data_output_large/fair-samples/fair-1.6.2-wg3-params-slim-reconstrained.json', 'w') as filehandle:
    json.dump(config_list, filehandle)

# %% cell 58
len(config_list)
