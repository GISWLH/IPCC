# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/160_WG3_constrain_fair_samples.ipynb

# %% cell 2
import errno
import fair
import json
import sys
import os
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

# %% cell 4
fair.__version__

# %% cell 6
xl = pd.read_excel('../data_input/observations/AR6 FGD assessment time series - GMST and GSAT.xlsx', skiprows=1, skipfooter=28)
temp_gmst=xl['4-set mean'].values
temp_year=xl['Unnamed: 0'].values
pl.plot(temp_year, temp_gmst)

temp_gmst[-1]

# %% cell 7
OHC_df = pd.read_csv("../data_input/observations/AR6_OHC_ensemble_FGDprelim.csv", skiprows=1)
OHC_df

# %% cell 8
OHUobs = OHC_df['Central Estimate Full-depth'].values
OHUyears = OHC_df['Year'].values

# %% cell 9
OHU90 = OHC_df['Full-depth Uncertainty (1-sigma)'].values

# %% cell 11
with open('../data_input/random_seeds.json', 'r') as filehandle:
    SEEDS = json.load(filehandle)

# %% cell 12
SAMPLES = 1000000
F2XCO2_MEAN = 4.00
F2XCO2_NINETY = 0.48

# %% cell 14
geoff_sample_df = pd.read_csv('../data_output_large/geoff_sample.csv', index_col=0)
geoff_sample_df

# %% cell 15
ecs = np.load('../data_input_large/fair-samples/ecs_unconstrained.npy')
tcr = np.load('../data_input_large/fair-samples/tcr_unconstrained.npy')
f2x = np.load('../data_input_large/fair-samples/f2x_unconstrained.npy')

# %% cell 17
r0 = np.load('../data_input_large/fair-samples/r0_unconstrained.npy')
rC = np.load('../data_input_large/fair-samples/rC_unconstrained.npy')
rT = np.load('../data_input_large/fair-samples/rT_unconstrained.npy')
pre_ind_co2 = np.load('../data_input_large/fair-samples/pre_ind_co2_unconstrained.npy')

# %% cell 19
C_CO2 = np.load('../data_output_large/fair-samples/C_CO2_unconstrained.npy')
F_O3 = np.load('../data_output_large/fair-samples/F_O3_unconstrained.npy')
F_dir = np.load('../data_output_large/fair-samples/F_ERFari_unconstrained.npy')
F_ind = np.load('../data_output_large/fair-samples/F_ERFaci_unconstrained.npy')
F_ant = np.load('../data_output_large/fair-samples/F_anthro_unconstrained.npy')
F_tot = np.load('../data_output_large/fair-samples/F_total_unconstrained.npy')
T = np.load('../data_output_large/fair-samples/T_unconstrained.npy')
OHU = np.load('../data_output_large/fair-samples/OHU_unconstrained.npy')
AF = np.load('../data_output_large/fair-samples/AF_unconstrained.npy')

# %% cell 20
F_O3.shape

# %% cell 21
def rmse(obs, mod):
    return np.sqrt(np.sum((obs-mod)**2)/len(obs))

# %% cell 23
## simple criterion: RMSE of temperature 1850-2014 < 0.135
rmse_temp = np.zeros((SAMPLES))
for i in range(SAMPLES):
    rmse_temp[i] = rmse(temp_gmst[:165], (T[100:265,i]-np.mean(T[100:151,i], axis=0)))
accept_temp=(rmse_temp<0.135)
print(np.sum(accept_temp))
valid_temp = np.arange(SAMPLES, dtype=int)[accept_temp]

# %% cell 24
# accept_temp = np.logical_and(
#     T[245:265].mean(axis=0)-T[100:151].mean(axis=0) < 0.98,
#     0.67 < T[245:265].mean(axis=0)-T[100:151].mean(axis=0)
# )
# valid_temp = np.arange(SAMPLES, dtype=int)[accept_temp]
# print(np.sum(accept_temp))

# %% cell 25
pl.hist(T[245:265,accept_temp].mean(axis=0) - T[100:151,accept_temp].mean(axis=0))

# %% cell 26
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

# %% cell 27
# GMST target 0.67 0.85 0.98
print(np.percentile(np.mean(T[245:265,accept_temp], axis=0)-np.mean(T[100:151,accept_temp], axis=0), (5, 16, 50, 84, 95)))

# %% cell 29
((OHUobs[-1]-OHUobs[0]) - np.sqrt(OHU90[0]**2+OHU90[-1]**2))

# %% cell 30
accept_ohu = np.logical_and(
    ((OHUobs[-1]-OHUobs[0]) - np.sqrt(OHU90[0]**2+OHU90[-1]**2)) < 0.90*(OHU[268,:]-OHU[221,:])*1e-21,
    0.90*(OHU[268,:]-OHU[221,:])*1e-21 < ((OHUobs[-1]-OHUobs[0]) + np.sqrt(OHU90[0]**2+OHU90[-1]**2))
)
valid_ohu = np.arange(SAMPLES, dtype=int)[accept_ohu]
print(np.sum(accept_ohu))

# %% cell 31
pl.fill_between(OHUyears, OHUobs-OHU90, OHUobs+OHU90, color='blue', lw=0, alpha=0.5)
pl.plot(OHUyears, OHUobs, color='blue')
pl.fill_between(np.arange(1750.5, 2019), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept_ohu]-OHU[268,accept_ohu]), 5, axis=1), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept_ohu]-OHU[268,accept_ohu]), 95, axis=1), color='gray', lw=0, alpha=0.5)
pl.plot(np.arange(1750.5,2019), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept_ohu]-OHU[268,accept_ohu]), 50, axis=1), color='k')
pl.title('Historically constrained - ocean heat')
pl.xlim(1971,2019)
pl.ylim(-100,440)
pl.ylabel('ZJ')
pl.tight_layout()

# %% cell 33
conc_all = pd.read_csv('../data_input_large/rcmip-concentrations-annual-means-v5-1-0.csv')
co2_obs = conc_all[(conc_all['Scenario']=='ssp245')&(conc_all['Region']=='World')&(conc_all.Variable.str.endswith('CO2'))].loc[:,'1750':'2018'].values.squeeze()
co2_obs.shape

# %% cell 34
pl.hist(C_CO2[0,:])

# %% cell 35
C_CO2.shape

# %% cell 36
accept_co2 = np.logical_and( (co2_obs[264] - 0.36) < C_CO2[264], C_CO2[264] < (co2_obs[264] + 0.36) )
print(np.sum(accept_co2))
valid_co2 = np.arange(SAMPLES, dtype=int)[accept_co2]

# %% cell 37
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

# %% cell 38
pl.hist(rC[accept_co2])

# %% cell 40
accept_ssp245 = accept_temp * accept_ohu * accept_co2
accept_inds = (np.arange(len(accept_ssp245), dtype=int))[accept_ssp245]
accept_inds

# %% cell 41
conc_subset = conc_all[(conc_all['Model']=='unspecified')&(conc_all['Scenario']=='1pctCO2')&(conc_all['Region']=='World')]
gases=['CO2','CH4','N2O','CF4','C2F6','C6F14','HFC23','HFC32','HFC4310mee','HFC125','HFC134a','HFC143a',
       'HFC227ea','HFC245fa','SF6','CFC11','CFC12','CFC113','CFC114','CFC115','CCl4','CH3CCl3','HCFC22',
       'HCFC141b','HCFC142b','Halon1211','Halon1202','Halon1301','Halon2402','CH3Br','CH3Cl']
conc = np.zeros((151,31))
for ig, gas in enumerate(gases):
    try:
        conc[:,ig] = conc_subset[conc_subset.Variable.str.endswith(gas)].loc[:,'1850':'2000'].values
    except:
        conc[:,ig] = 0

results = np.empty((151,0))
expt = '1pctCO2'

arglist=[]
for ens in tqdm(accept_inds, desc='parameters'):
    C_pi=np.zeros(31)
    C_pi[0] = pre_ind_co2[ens]
    C_pi[1]=731.406
    C_pi[2]=273.8651
    C_pi[3]=34.05
    C_pi[4] = 32.28077001
    C_pi[25]=0.00434894
    C_pi[29]=8.75191031
    C_pi[30]=755.7838942
    arglist.append(
        {
            'emissions_driven':False,
            'C_pi': C_pi,
            'C': conc,
            'F_volcanic': 0,
            'F_solar': 0,
            'F2x': f2x[ens],
            'ariaci_out': True,
            'efficacy': np.ones(13),
            'temperature_function': 'Geoffroy',
            'lambda_global': -geoff_sample_df.loc[ens, 'lamg'],  # this and the below only used in two-layer model
            'ocean_heat_capacity': np.array([geoff_sample_df.loc[ens, 'cmix'], geoff_sample_df.loc[ens, 'cdeep']]),
            'ocean_heat_exchange': geoff_sample_df.loc[ens, 'gamma_2l'],
            'deep_ocean_efficacy': geoff_sample_df.loc[ens, 'eff'],
            'r0': r0[ens],
            'rt': rT[ens],
            'rc': rC[ens],
        }
    )

def run_fair(args):
    Ctemp, Ftemp, Ttemp, _, _, _, heatfluxtemp = fair.forward.fair_scm(
        emissions_driven = args['emissions_driven'],
        C_pi = args['C_pi'],
        C = args['C'],
        F_volcanic = args['F_volcanic'],
        F_solar = args['F_solar'],
        F2x = args['F2x'],
        ariaci_out = args['ariaci_out'],
        efficacy = args['efficacy'],
        temperature_function = args['temperature_function'],
        lambda_global = args['lambda_global'],
        ocean_heat_capacity = args['ocean_heat_capacity'],
        ocean_heat_exchange = args['ocean_heat_exchange'],
        deep_ocean_efficacy = args['deep_ocean_efficacy'],
    )
    Etemp, Fetemp, Tetemp, _, _, _, aftemp = inverse_fair_scm(
        C = args['C'][:,0],
        F2x = args['F2x'],
        C_pi = args['C'][0,0],
        r0 = args['r0'],
        rt = args['rt'],
        rc = args['rc'],
        F_in = np.sum(Ftemp, axis=1),
        temperature_function = args['temperature_function'],
        lambda_global = args['lambda_global'],
        ocean_heat_capacity = args['ocean_heat_capacity'],
        ocean_heat_exchange = args['ocean_heat_exchange'],
        deep_ocean_efficacy = args['deep_ocean_efficacy'],
    )
    nt = len(Ttemp)
    cumE = np.cumsum(Etemp) * molwt.CO2/molwt.C*1000.
    Catmpool = Ctemp[:,0]*ppm_gtc*molwt.CO2/molwt.C*1000.
    Cburden = (Ctemp[:,0]-Ctemp[0,0])*ppm_gtc*molwt.CO2/molwt.C*1000.

    return (Ttemp, np.sum(Ftemp, axis=1), heatfluxtemp*NTOA_ZJ,
        aftemp, cumE, Ttemp/cumE)

if __name__ == '__main__':
    with Pool(16) as pool, warnings.catch_warnings():
        warnings.simplefilter('ignore')
        results = list(tqdm(pool.imap(run_fair, arglist), total=len(accept_inds), desc='climate model'))
        
    results = np.array(results).transpose(1,2,0)

# %% cell 42
results.shape

# %% cell 43
len(accept_inds)

# %% cell 44
af140 = results[3,140,:]
af70 = results[3,70,:]
tcre70_unscale = results[5,70,:]
accept_prob = st.uniform.rvs(loc=0, scale=1, size=SAMPLES, random_state=SEEDS[79])
accept_af = np.zeros(len(accept_inds), dtype=bool)
for i in range(len(accept_inds)):
    likelihood = st.norm.pdf(af140[i], loc=.597, scale=.049)/st.norm.pdf(.597, loc=.597, scale=.049)
    if likelihood>=accept_prob[i]:
        accept_af[i] = True
    #print(likelihood)
np.sum(accept_af)

# %% cell 45
valid = np.arange(SAMPLES, dtype=int)[accept_ssp245][accept_af]
accept_ssp245 = np.zeros(SAMPLES, dtype=bool)
accept_ssp245[valid] = True

# %% cell 46
valid

# %% cell 48
accept = accept_ssp245
print(np.sum(accept))
valid = np.arange(SAMPLES, dtype=int)[accept]

# %% cell 49
pl.hist(rC[accept])

# %% cell 50
pl.hist(rT[accept])

# %% cell 51
pl.hist(r0[accept], density=True)

# %% cell 52
pl.fill_between(
    np.arange(1750, 2101),
    np.percentile(C_CO2[:,accept], 5, axis=1),
    np.percentile(C_CO2[:,accept], 95, axis=1), 
    color='gray', lw=0, alpha=0.5
)
pl.plot(
    np.arange(1750, 2101), 
    np.percentile(C_CO2[:,accept], 50, axis=1),
    color='k'
)
pl.plot(np.arange(1750, 2019), co2_obs, color='blue')
pl.title('Historically constrained - CO2')

# %% cell 53
pl.fill_between(
    np.arange(1850, 2021),
    np.percentile(T[100:271,accept]-np.mean(T[100:151,accept], axis=0), 5, axis=1),
    np.percentile(T[100:271,accept]-np.mean(T[100:151,accept], axis=0), 95, axis=1), 
    color='gray', lw=0, alpha=0.5
)
pl.plot(
    np.arange(1850, 2021), 
    np.percentile(T[100:271,accept]-np.mean(T[100:151,accept], axis=0), 50, axis=1),
    color='k'
)
pl.plot(np.arange(1850, 2021), temp_gmst, color='blue')
pl.title('Historically constrained - temperature')

# %% cell 54
# target 0.67 0.85 0.98 GMST
#print(np.percentile((np.mean(T[245:265,accept], axis=0)-np.mean(T[100:151,accept], axis=0))/1.04, (5, 16, 50, 84, 95)))
print(np.percentile(np.mean(T[245:265,accept], axis=0)-np.mean(T[100:151,accept], axis=0), (5, 16, 50, 84, 95)))

# %% cell 55
pl.fill_between(OHUyears, OHUobs-OHU90, OHUobs+OHU90, color='blue', lw=0, alpha=0.5)
pl.plot(OHUyears, OHUobs, color='blue')
pl.fill_between(np.arange(1750.5, 2019), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept]-OHU[268,accept]), 5, axis=1), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept]-OHU[268,accept]), 95, axis=1), color='gray', lw=0, alpha=0.5)
pl.plot(np.arange(1750.5,2019), OHUobs[-1]+1e-21*np.percentile(0.90*(OHU[:269,accept]-OHU[268,accept]), 50, axis=1), color='k')
pl.title('Historically constrained - ocean heat')
pl.xlim(1971,2019)
pl.ylim(-100,440)
pl.ylabel('ZJ')
pl.tight_layout()

# %% cell 56
# target 0.67 0.85 0.98 GMST
np.percentile(np.mean(T[245:265,accept],axis=0)-np.mean(T[100:151,accept],axis=0), (5,16,50,84,95))

# %% cell 57
pl.hist(ecs[accept], bins=np.arange(1.6,8.8,0.4), density=True)
# target 2.0 2.5 3.0 4.0 5.0
pl.xlabel('K')
pl.title('ECS: constrained')
pl.tight_layout()
np.percentile(ecs[accept], (5,16,50,84,95))

# %% cell 58
pl.hist(tcr[accept], bins=np.arange(0.8,3.2,0.2), density=True)
# target 1.2 1.4 1.8 2.2 2.4
pl.xlabel('K')
pl.title('TCR: constrained')
pl.tight_layout()
np.percentile(tcr[accept], (5,16,50,84,95))

# %% cell 59
# target -0.6 -0.3 -0.0
pl.hist(np.mean(F_dir[255:265,accept], axis=0), bins=np.arange(-0.8,0.2,0.1));
pl.title('aerosol ERFari')
np.percentile(np.mean(F_dir[255:265,accept], axis=0), (5,16,50,84,95))

# %% cell 60
# target -1.7 -1.0 -0.3
pl.hist(np.mean(F_ind[255:265,accept], axis=0), bins=np.arange(-2.0,0.2,0.1));
pl.title('aerosol ERFaci')
np.percentile(np.mean(F_ind[255:265,accept], axis=0), (5,16,50,84,95))

# %% cell 61
# target -2 -1.3 -0.6
pl.hist(np.mean(F_dir[255:265,accept], axis=0)+np.mean(F_ind[255:265,accept], axis=0), bins=np.arange(-2.2,0.2,0.1), density=True);
pl.title('Aerosol ERF: 1750-2010')
pl.xlabel('W m$^{-2}$')
pl.tight_layout()
np.percentile(np.mean(F_dir[255:265,accept], axis=0)+np.mean(F_ind[255:265,accept], axis=0), (5,16,50,84,95))

# %% cell 62
pl.scatter(ecs[accept], np.mean(F_dir[255:265,accept], axis=0)+np.mean(F_ind[255:265,accept], axis=0))

# %% cell 63
pl.scatter(ecs[accept], tcr[accept])

# %% cell 64
accept_inds = (np.arange(len(accept), dtype=int))[accept]
np.savetxt('../data_output_large/fair-samples/accept_inds.csv', accept_inds, fmt='%d')

# %% cell 66
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

# %% cell 67
config_list = []
for ens in valid:
    scale = np.ones(45)
    scale[1] = scale_normals[ens,1] * 0.86 # methane adjustment
    scale[2] = scale_normals[ens,2] * 1.07
    scale[3:31] = scale_normals[ens,3]
    scale[15] = scale_normals[ens,3] * 1.13 # cfc11 adjustment
    scale[16] = scale_normals[ens,3] * 1.12 # cfc12 adjustment
    #scale[31] = scale_normals[i,4]
    scale[33:35] = scale_normals[ens,5:7]
    scale[41:44] = scale_normals[ens,7:10]
    F_solar = np.zeros(361)
    F_solar[:270] = np.linspace(0,trend_solar[ens],270) + solar_forcing[:270]*scale_normals[ens,10]
    F_solar[270:351] = trend_solar[ens] + solar_forcing[270:351]*scale_normals[ens,10]
    F_solar[351:361] = solar_forcing[351:]
    C_pi=np.zeros(31)
    C_pi[1]=731.406
    C_pi[2]=273.8651
    C_pi[3]=34.05
    C_pi[20] = 0.025
    C_pi[25]=0.004447
    C_pi[29]=5.3
    C_pi[30]=457
    C_pi[0] = pre_ind_co2[ens]
    E_pi=np.zeros(40)
    E_pi[5]=1.22002422
    E_pi[6]=348.527359
    E_pi[7]=60.0218262
    E_pi[8]=3.87593407
    E_pi[9]=2.09777075
    E_pi[10]=15.4476682
    E_pi[11]=6.92769009
    aCO2land = -0.2 / 190
    E_ref_BC = 6.095
    fair_params = {
        'F2x' : f2x[ens],
        'r0'  : r0[ens],
        'rt'  : rT[ens],
        'rc'  : rC[ens],
        'lambda_global': -geoff_sample_df.loc[ens, 'lamg'],  # this and the below only used in two-layer model
        'ocean_heat_capacity':[geoff_sample_df.loc[ens, 'cmix'], geoff_sample_df.loc[ens, 'cdeep']],
        'ocean_heat_exchange':geoff_sample_df.loc[ens, 'gamma_2l'],
        'deep_ocean_efficacy':geoff_sample_df.loc[ens,'eff'],
        'b_aero': [beta_so2[ens], 0.0, 0.0, 0.0, beta_bc[ens], beta_oc[ens], beta_nh3[ens]],
        'ghan_params':[beta[ens], aci_coeffs[ens,0], aci_coeffs[ens, 1]],
        'scale':scale.tolist(),
        'C_pi':C_pi.tolist(),
        'E_pi':E_pi.tolist(),
        'ghg_forcing':'Meinshausen',
        'aCO2land': aCO2land,
        'stwv_from_ch4': 0.079047,
        'F_ref_BC': 0.08,
        'E_ref_BC': E_ref_BC,
        'F_solar':F_solar.tolist(),
        'F_volcanic':volcanic_forcing.tolist(),
        'tropO3_forcing': 'thornhill-skeie',
        'b_tro3': [beta_ch4[ens], beta_n2o[ens], beta_ods[ens], beta_co[ens], beta_voc[ens], beta_nox[ens]],
        'ozone_feedback': ozone_feedback[ens],
        'natural': ch4_n2o.tolist(),
    }
    config_list.append(fair_params)
with open('../data_output_large/fair-samples/fair-1.6.2-wg3-params.json', 'w') as filehandle:
    json.dump(config_list, filehandle)

# %% cell 68
len(config_list)
