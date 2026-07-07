# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/070_chapter7_ozone_emissions_to_forcing.ipynb

# %% cell 2
import fair
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
from fair.constants import molwt
from fair.forcing.ozone_tr import stevenson
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import copy

from ar6.forcing.ozone import eesc
from ar6.constants.gases import rcmip_to_ghg_names

# %% cell 4
good_models = ['BCC-ESM1', 'CESM2(WACCM6)', 'GFDL-ESM4', 'GISS-E2-1-H', 'MRI-ESM2-0', 'OsloCTM3']
skeie_trop = pd.read_csv('../data_input/Skeie_et_al_npj_2020/skeie_ozone_trop.csv', index_col=0)
skeie_trop = skeie_trop.loc[good_models]
skeie_trop.insert(0, 1850, 0)
skeie_trop.columns = pd.to_numeric(skeie_trop.columns)
skeie_trop.interpolate(axis=1, method='values', limit_area='inside', inplace=True)

# %% cell 5
skeie_trop

# %% cell 6
skeie_strat = pd.read_csv('../data_input/Skeie_et_al_npj_2020/skeie_ozone_strat.csv', index_col=0)
skeie_strat = skeie_strat.loc[good_models]
skeie_strat.insert(0, 1850, 0)
skeie_strat.columns = pd.to_numeric(skeie_strat.columns)
skeie_strat.interpolate(axis=1, method='values', limit_area='inside', inplace=True)
skeie_strat

# %% cell 7
skeie_total = skeie_trop + skeie_strat
#skeie_total.drop([2014,2017,2020], inplace=True, axis=1)
skeie_total

# %% cell 8
skeie_trop_est = skeie_trop.mean()
skeie_trop_est[1750] = -0.03
skeie_trop_est.sort_index(inplace=True)
skeie_trop_est = skeie_trop_est + 0.03
skeie_trop_est.drop([2014,2017,2020], inplace=True)
skeie_trop_est = skeie_trop_est.append(skeie_trop.loc['OsloCTM3',2014:]-skeie_trop.loc['OsloCTM3',2010]+skeie_trop_est[2010])         
f = interp1d(skeie_trop_est.index, skeie_trop_est, bounds_error=False, fill_value='extrapolate')
years = np.arange(1750,2021)
o3trop = f(years)
pl.plot(years, o3trop)
print("2014-1750 trop. ozone ERF from Skeie:", o3trop[264])
print("2019-1750 trop. ozone ERF from Skeie:", o3trop[269])

# %% cell 9
skeie_strat_est = skeie_strat.mean()
skeie_strat_est_min = skeie_strat.min()
skeie_strat_est_max = skeie_strat.max()
skeie_strat_est[1750] = 0.00
skeie_strat_est_min[1750] = 0.00
skeie_strat_est_max[1750] = 0.00
skeie_strat_est.sort_index(inplace=True)
skeie_strat_est_min.sort_index(inplace=True)
skeie_strat_est_max.sort_index(inplace=True)
skeie_strat_est.drop([2014,2017,2020], inplace=True)
skeie_strat_est_min.drop([2014,2017,2020], inplace=True)
skeie_strat_est_max.drop([2014,2017,2020], inplace=True)

years = np.arange(1750,2021)
skeie_strat_est = skeie_strat_est.append(skeie_strat.loc['OsloCTM3',2014:]-skeie_strat.loc['OsloCTM3',2010]+skeie_strat_est[2010])         
f = interp1d(skeie_strat_est.index, skeie_strat_est, bounds_error=False, fill_value='extrapolate')
o3strat = f(years)

skeie_strat_est_min = skeie_strat_est_min.append(skeie_strat.loc['OsloCTM3',2014:]-skeie_strat.loc['OsloCTM3',2010]+skeie_strat_est_min[2010])         
f = interp1d(skeie_strat_est_min.index, skeie_strat_est_min, bounds_error=False, fill_value='extrapolate')
o3strat_min = f(years)

skeie_strat_est_max = skeie_strat_est_max.append(skeie_strat.loc['OsloCTM3',2014:]-skeie_strat.loc['OsloCTM3',2010]+skeie_strat_est_max[2010])         
f = interp1d(skeie_strat_est_max.index, skeie_strat_est_max, bounds_error=False, fill_value='extrapolate')
o3strat_max = f(years)

pl.fill_between(years, o3strat_min, o3strat_max)
pl.plot(years, o3strat, color='k')
print("2014-1750 strat. ozone ERF from Skeie:", o3strat[264])
print("2019-1750 strat. ozone ERF from Skeie:", o3strat[269])

# %% cell 10
df = pd.DataFrame(
    np.array([o3strat_min, o3strat, o3strat_max]).T,
    columns=['min','mean','max'],
    index=np.arange(1750,2021)
)
df.index.name = 'year'
df.to_csv('../data_output/o3strat_erf.csv')

# %% cell 11
skeie_ssp245 = skeie_total.mean()
skeie_ssp245[1750] = -0.03
skeie_ssp245.sort_index(inplace=True)
skeie_ssp245 = skeie_ssp245 + 0.03
skeie_ssp245.drop([2014,2017,2020], inplace=True)
skeie_ssp245 = skeie_ssp245.append(skeie_total.loc['OsloCTM3',2014:]-skeie_total.loc['OsloCTM3',2010]+skeie_ssp245[2010])
skeie_ssp245

# %% cell 12
f = interp1d(skeie_ssp245.index, skeie_ssp245, bounds_error=False, fill_value='extrapolate')
years = np.arange(1750,2021)
o3total = f(years)
pl.plot(years, o3total)
print("2014-1750 ozone ERF from Skeie:", o3total[264])
print("2019-1750 ozone ERF from Skeie:", o3total[269])

# %% cell 13
df = pd.DataFrame(np.array([o3total, o3trop, o3strat]).T, columns=['o3_erf','o3_trop','o3_strat'], index=np.arange(1750,2021))
df.index.name = 'year'
df.to_csv('../data_output/o3_erf.csv')

# %% cell 16
emissions = pd.read_csv('../data_input_large/rcmip-emissions-annual-means-v5-1-0.csv')
concentrations = pd.read_csv('../data_input_large/rcmip-concentrations-annual-means-v5-1-0.csv')

scenario = 'ssp245'
ch4 = concentrations.loc[(concentrations['Scenario']==scenario)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|CH4')),'1750':'2020'].values.squeeze()
n2o = concentrations.loc[(concentrations['Scenario']==scenario)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|N2O')),'1750':'2020'].values.squeeze()
ods = {}
ods_species = [
    'CCl4',
    'CFC11',
    'CFC113',
    'CFC114',
    'CFC115',
    'CFC12',
    'CH2Cl2',
    'CH3Br',
    'CH3CCl3',
    'CH3Cl',
    'CHCl3',
    'HCFC141b',
    'HCFC142b',
    'HCFC22',
    'Halon1211',
    'Halon1301',
    'Halon2402',
]
for specie in ods_species:
    ods[specie] = concentrations.loc[(concentrations['Scenario']==scenario)&(concentrations['Region']=='World')&(concentrations.Variable.str.endswith('|%s' % specie)),'1750':'2020'].values.squeeze()

co  = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions.Variable.str.endswith('|CO')),'1750':'2020'].interpolate(axis=1).values.squeeze()
nox = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions.Variable.str.endswith('|NOx')),'1750':'2020'].interpolate(axis=1).values.squeeze()
voc = emissions.loc[(emissions['Scenario']==scenario)&(emissions['Region']=='World')&(emissions.Variable.str.endswith('|VOC')),'1750':'2020'].interpolate(axis=1).values.squeeze()

# %% cell 17
pl.plot(voc)
nox.shape

# %% cell 18
eesc_total = np.zeros((271))
for specie in ods_species:
    eesc_total = eesc_total + eesc(ods[specie], specie)

# %% cell 19
pl.plot(np.arange(1750,2021), eesc_total)

# %% cell 20
delta_Cch4 = ch4[264] - ch4[0]
delta_Cn2o = n2o[264] - n2o[0]
delta_Cods = eesc_total[264] - eesc_total[0]
delta_Eco  = co[264] - co[0]
delta_Evoc = voc[264] - voc[0]
delta_Enox = nox[264] - nox[0]

# %% cell 21
# best estimate radiative efficienices from 2014 - 1850

radeff_ch4 = 0.14/delta_Cch4
radeff_n2o = 0.03/delta_Cn2o
radeff_ods = -0.11/delta_Cods
radeff_co  = 0.067/delta_Eco    # stevenson rescaled
radeff_voc = 0.043/delta_Evoc   # stevenson rescaled
radeff_nox = 0.20/delta_Enox

# %% cell 22
fac_cmip6_skeie = (
    (
    radeff_ch4 * delta_Cch4 +
    radeff_n2o * delta_Cn2o +
    radeff_ods * delta_Cods +
    radeff_co  * delta_Eco +
    radeff_voc * delta_Evoc +
    radeff_nox * delta_Enox 
    ) / (o3total[264]-o3total[0])
)
ts = np.vstack((ch4, n2o, eesc_total, co, voc, nox)).T

# %% cell 23
ts

# %% cell 24
def fit_precursors(x, rch4, rn2o, rods, rco, rvoc, rnox):
    return rch4*x[0] + rn2o*x[1] + rods*x[2] + rco*x[3] + rvoc*x[4] + rnox*x[5]

p, cov = curve_fit(
    fit_precursors, 
    ts[:271,:].T - ts[0:1, :].T,
    o3total[:271]-o3total[0],
    bounds=(
        (
            0.09/delta_Cch4/fac_cmip6_skeie,
            0.01/delta_Cn2o/fac_cmip6_skeie,
            -0.21/delta_Cods/fac_cmip6_skeie,
            0.010/delta_Eco/fac_cmip6_skeie,
            0/delta_Evoc/fac_cmip6_skeie,
            0.09/delta_Enox/fac_cmip6_skeie
        ), (
            0.19/delta_Cch4/fac_cmip6_skeie, 
            0.05/delta_Cn2o/fac_cmip6_skeie, 
            -0.01/delta_Cods/fac_cmip6_skeie, 
            0.124/delta_Eco/fac_cmip6_skeie, 
            0.086/delta_Evoc/fac_cmip6_skeie, 
            0.31/delta_Enox/fac_cmip6_skeie
        )
    )
)

forcing = (
    p[0] * (ch4 - ch4[0]) +
    p[1] * (n2o - n2o[0]) +
    p[2] * (eesc_total - eesc_total[0]) +
    p[3] * (co  - co[0]) +
    p[4] * (voc  - voc[0]) +
    p[5] * (nox  - nox[0])
)

pl.plot(np.arange(1750,2021), forcing)

# %% cell 25
pl.plot(np.arange(1750,2021), forcing, label='Precursor fit')
pl.plot(np.arange(1750,2021), o3total, label='Skeie et al. 2020 mean')
pl.legend()

# %% cell 26
print(p)  # these coefficients we export to the ERF time series
print(radeff_ch4, radeff_n2o, radeff_ods, radeff_co, radeff_voc, radeff_nox)

# %% cell 28
xl = pd.read_excel('../data_input/observations/AR6 FGD assessment time series - GMST and GSAT.xlsx', skiprows=1, skipfooter=28)
Tobs=xl['4-set mean'].values
years=xl['Unnamed: 0'].values

# %% cell 29
pl.plot(years, Tobs)

# %% cell 30
Tobs[:51].mean()  # already normalised to 1850-1900 anyway - from plot above, looks stable

# %% cell 31
Tobs[161:171].mean() # 2011-2020 mean

# %% cell 32
delta_gmst = pd.DataFrame(
{
    1850: 0,
    1920: Tobs[65:76].mean(),
    1930: Tobs[75:86].mean(),
    1940: Tobs[85:96].mean(),
    1950: Tobs[95:106].mean(),
    1960: Tobs[105:116].mean(),
    1970: Tobs[115:126].mean(),
    1980: Tobs[125:136].mean(),
    1990: Tobs[135:146].mean(),
    2000: Tobs[145:156].mean(),
    2007: Tobs[152:163].mean(),
    2010: Tobs[155:166].mean(),
    2014: Tobs[159:170].mean(),
    2017: Tobs[167],   # we don't use this
    2020: Tobs[168]    # or this
}, index=[0])
delta_gmst

delta_gmst=[
    0,
    Tobs[65:76].mean(),
    Tobs[75:86].mean(),
    Tobs[85:96].mean(),
    Tobs[95:106].mean(),
    Tobs[105:116].mean(),
    Tobs[115:126].mean(),
    Tobs[125:136].mean(),
    Tobs[135:146].mean(),
    Tobs[145:156].mean(),
    Tobs[152:163].mean(),
    Tobs[155:166].mean(),
    Tobs[159:170].mean(),
    Tobs[167],   # we don't use this
    Tobs[168]
]
delta_gmst

# %% cell 33
warming_pi_pd = Tobs[159:170].mean()

# %% cell 34
skeie_trop = pd.read_csv('../data_input/Skeie_et_al_npj_2020/skeie_ozone_trop.csv', index_col=0)
skeie_trop = skeie_trop.loc[good_models]
skeie_trop.insert(0, 1850, 0)
skeie_trop.columns = pd.to_numeric(skeie_trop.columns)
skeie_trop.interpolate(axis=1, method='values', limit_area='inside', inplace=True)
skeie_strat = pd.read_csv('../data_input/Skeie_et_al_npj_2020/skeie_ozone_strat.csv', index_col=0)
skeie_strat = skeie_strat.loc[good_models]
skeie_strat.insert(0, 1850, 0)
skeie_strat.columns = pd.to_numeric(skeie_strat.columns)
skeie_strat.interpolate(axis=1, method='values', limit_area='inside', inplace=True)
skeie_total = skeie_strat + skeie_trop
skeie_total
coupled_models = copy.deepcopy(good_models)
coupled_models.remove('OsloCTM3')
skeie_total.loc[coupled_models] = skeie_total.loc[coupled_models] - (-0.037) * np.array(delta_gmst)
skeie_ssp245 = skeie_total.mean()
skeie_ssp245[1750] = -0.03
skeie_ssp245.sort_index(inplace=True)
skeie_ssp245 = skeie_ssp245 + 0.03
skeie_ssp245.drop([2014,2017,2020], inplace=True)
skeie_ssp245 = skeie_ssp245.append(skeie_total.loc['OsloCTM3',2014:]-skeie_total.loc['OsloCTM3',2010]+skeie_ssp245[2010])
skeie_ssp245   # this is what the ozone forcing would be, in the absence of any feedbacks

# %% cell 35
f = interp1d(skeie_ssp245.index, skeie_ssp245, bounds_error=False, fill_value='extrapolate')
years = np.arange(1750,2021)
o3total = f(years)
pl.plot(years, o3total)
print("2014-1750 ozone ERF from Skeie:", o3total[264])
print("2019-1750 ozone ERF from Skeie:", o3total[269])
print("2014-1850 ozone ERF from Skeie:", o3total[264] - o3total[100])

# %% cell 36
# best estimate radiative efficienices from 2014 - 1850

radeff_ch4 = 0.14/delta_Cch4
radeff_n2o = 0.03/delta_Cn2o
radeff_ods = -0.11/delta_Cods
radeff_co  = 0.067/delta_Eco    # stevenson rescaled
radeff_voc = 0.043/delta_Evoc   # stevenson rescaled
radeff_nox = 0.20/delta_Enox

# %% cell 37
fac_cmip6_skeie = (
    (
    radeff_ch4 * delta_Cch4 +
    radeff_n2o * delta_Cn2o +
    radeff_ods * delta_Cods +
    radeff_co  * delta_Eco +
    radeff_voc * delta_Evoc +
    radeff_nox * delta_Enox 
    ) / (o3total[264]-o3total[0])
)
ts = np.vstack((ch4, n2o, eesc_total, co, voc, nox)).T

# %% cell 38
def fit_precursors(x, rch4, rn2o, rods, rco, rvoc, rnox):
    return rch4*x[0] + rn2o*x[1] + rods*x[2] + rco*x[3] + rvoc*x[4] + rnox*x[5]

p, cov = curve_fit(
    fit_precursors, 
    ts[:271,:].T - ts[0:1, :].T,
    o3total[:271]-o3total[0],
    bounds=(
        (
            0.09/delta_Cch4/fac_cmip6_skeie,
            0.01/delta_Cn2o/fac_cmip6_skeie,
            -0.21/delta_Cods/fac_cmip6_skeie,
            0.010/delta_Eco/fac_cmip6_skeie,
            0/delta_Evoc/fac_cmip6_skeie,
            0.09/delta_Enox/fac_cmip6_skeie
        ), (
            0.19/delta_Cch4/fac_cmip6_skeie, 
            0.05/delta_Cn2o/fac_cmip6_skeie, 
            -0.01/delta_Cods/fac_cmip6_skeie, 
            0.124/delta_Eco/fac_cmip6_skeie, 
            0.086/delta_Evoc/fac_cmip6_skeie, 
            0.31/delta_Enox/fac_cmip6_skeie
        )
    )
)

forcing = (
    p[0] * (ch4 - ch4[0]) +
    p[1] * (n2o - n2o[0]) +
    p[2] * (eesc_total - eesc_total[0]) +
    p[3] * (co  - co[0]) +
    p[4] * (voc  - voc[0]) +
    p[5] * (nox  - nox[0])
)

pl.plot(np.arange(1750,2021), forcing)

# %% cell 39
o3_aerchemmip = (
    radeff_ch4 * (ch4 - ch4[0]) +
    radeff_n2o * (n2o - n2o[0]) +
    radeff_ods * (eesc_total - eesc_total[0]) +
    radeff_co * (co - co[0]) +
    radeff_voc * (voc - voc[0]) +
    radeff_nox * (nox - nox[0])
)

# %% cell 40
delta_Cch4_1850 = ch4[264] - ch4[100]
delta_Cn2o_1850 = n2o[264] - n2o[100]
delta_Cods_1850 = eesc_total[264] - eesc_total[100]
delta_Eco_1850  = co[264] - co[100]
delta_Evoc_1850 = voc[264] - voc[100]
delta_Enox_1850 = nox[264] - nox[100]

radeff_ch4_1850 = 0.14/delta_Cch4_1850
radeff_n2o_1850 = 0.03/delta_Cn2o_1850
radeff_ods_1850 = -0.11/delta_Cods_1850
radeff_co_1850  = 0.067/delta_Eco_1850    # stevenson rescaled
radeff_voc_1850 = 0.043/delta_Evoc_1850   # stevenson rescaled
radeff_nox_1850 = 0.20/delta_Enox_1850

o3_aerchemmip = (
    radeff_ch4_1850 * (ch4 - ch4[0]) +
    radeff_n2o_1850 * (n2o - n2o[0]) +
    radeff_ods_1850 * (eesc_total - eesc_total[0]) +
    radeff_co_1850 * (co - co[0]) +
    radeff_voc_1850 * (voc - voc[0]) +
    radeff_nox_1850 * (nox - nox[0])
)

# %% cell 41
default_to_skeie = forcing[269]/o3_aerchemmip[269]
default_to_skeie

# %% cell 42
default_to_skeie*o3_aerchemmip[269]
#o3total[269]
#forcing[269]

# %% cell 43
# scale everything up to be exactly equal in 2014
#ratio = forcing[170]/(o3total[270]-o3total[100])
ratio=1
print(ratio)
pl.plot(np.arange(1750,2021), forcing/ratio, label='Precursor fit')
pl.plot(np.arange(1750,2021), o3total, label='Skeie et al. 2020 mean')
pl.plot(np.arange(1750,2021), default_to_skeie*o3_aerchemmip, label='Default coefficients')
#pl.xlim(2000,2020)
#pl.ylim(0.4,0.5)
pl.legend()

# %% cell 45
p  # these coefficients we export to the ERF time series
#print(radeff_ch4/ratio, radeff_n2o/ratio, radeff_ods/ratio, radeff_co/ratio, radeff_voc/ratio, radeff_nox/ratio)
mean = np.array([default_to_skeie*radeff_ch4_1850, default_to_skeie*radeff_n2o_1850, default_to_skeie*radeff_ods_1850, default_to_skeie*radeff_co_1850, default_to_skeie*radeff_voc_1850, default_to_skeie*radeff_nox_1850])
unc = np.array([47/37*radeff_ch4_1850*5/14, 47/37*radeff_n2o_1850*2/3, 47/37*radeff_ods_1850*10/11, 47/37*radeff_co_1850*57/67, 47/37*radeff_voc_1850*43/43, 47/37*radeff_nox_1850*11/20])

df = pd.DataFrame(data={'mean': mean, 'u90': unc})
df.index = ['CH4','N2O','ODS','CO','VOC','NOx']
df.index.name='species'
df.to_csv('../data_input/tunings/cmip6_ozone_skeie_fits.csv')
df
#pl.savetxt('../data_input/ozone_coeffici')

# %% cell 46
print(p[0] * (ch4[264] - ch4[100]))
print(p[1] * (n2o[264] - n2o[100]))
print(p[2] * (eesc_total[264] - eesc_total[100]))
print(p[3] * (co[264]  - co[100]))
print(p[4] * (voc[264]  - voc[100]))
print(p[5] * (nox[264]  - nox[100]))

# %% cell 47
print(radeff_ch4 * (ch4[264] - ch4[100]))
print(radeff_n2o * (n2o[264] - n2o[100]))
print(radeff_ods * (eesc_total[264] - eesc_total[100]))
print(radeff_co * (co[264]  - co[100]))
print(radeff_voc * (voc[264]  - voc[100]))
print(radeff_nox * (nox[264]  - nox[100]))

# %% cell 48
47/37*radeff_ch4_1850, 47/37*radeff_n2o_1850, 47/37*radeff_ods_1850, 47/37*radeff_co_1850, 47/37*radeff_voc_1850, 47/37*radeff_nox_1850

# %% cell 49
47/37*radeff_ch4_1850*5/14, 47/37*radeff_n2o_1850*2/3, 47/37*radeff_ods_1850*10/11, 47/37*radeff_co_1850*57/67, 47/37*radeff_voc_1850*43/43, 47/37*radeff_nox_1850*11/20
