# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/050_chapter2_solar_ERF.ipynb

# %% cell 2
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as pl
from ar6.utils import check_and_download
import pandas as pd

# %% cell 3
check_and_download(
    '../data_input_large/SSI_14C_cycle_yearly_cmip_v20160613_fc.nc',
    'https://sharebox.lsce.ipsl.fr/index.php/s/LpiCUCkSmx0P6bb/download?path=%2F&files=SSI_14C_cycle_yearly_cmip_v20160613_fc.nc'
)

check_and_download(
    '../data_input_large/solarforcing-ref-mon_input4MIPs_solar_CMIP_SOLARIS-HEPPA-3-2_gn_185001-229912.nc',
    'http://aims3.llnl.gov/thredds/fileServer/user_pub_work/input4MIPs/CMIP6/CMIP/SOLARIS-HEPPA/SOLARIS-HEPPA-3-2/atmos/mon/multiple/gm/v20170103/solarforcing-ref-mon_input4MIPs_solar_CMIP_SOLARIS-HEPPA-3-2_gn_185001-229912.nc'
)

# %% cell 4
solar_df = pd.DataFrame(index=np.arange(-6755,2300))
solar_df.index.name = 'Year'
#solar_df

# %% cell 6
ar5_df = pd.read_csv('../data_input/AR5/solar_TSI_AR5.csv', index_col=0)
#ar5_df
solar_df = solar_df.join(ar5_df)
solar_df.rename(columns={'TSI': 'AR5'}, inplace=True)

# %% cell 7
solmin_1745=ar5_df.loc[1742:1748,'TSI'].mean()
solmin_2008=ar5_df.loc[2005:2011,'TSI'].mean()
0.25 * 0.70 * 0.78 * (solmin_2008-solmin_1745)   # correct!

# %% cell 10
nc = Dataset('../data_input_large/SSI_14C_cycle_yearly_cmip_v20160613_fc.nc')
wl_bin = nc.variables['wavelength_bin'][:]
time   = nc.variables['time'][:]
ssi    = nc.variables['ssi'][:]
nc.close()

# %% cell 11
nc_future = Dataset('../data_input_large/solarforcing-ref-mon_input4MIPs_solar_CMIP_SOLARIS-HEPPA-3-2_gn_185001-229912.nc')
tsi_future = nc_future.variables['tsi'][:]
nc_future.close()

# %% cell 12
years = np.arange(1850, 2016, dtype=int)
steps = np.ones(166, dtype=int) * 365
steps[np.logical_and(years%4==0, np.logical_or(years%100!=0, years%400==0))] = 366
idx_1850 = np.argmin(time<1850)
idx_yearend = idx_1850+np.cumsum(steps)
idx_yearstart = np.insert(idx_yearend, 0, [idx_1850])[:-1] 
print (idx_yearstart[:10], idx_yearend[:10])
years_future = np.arange(2016, 2300)
isleap = np.zeros(284)
isleap[np.logical_and(years_future%4==0, np.logical_or(years_future%100!=0, years_future%400==0))] = 1

# %% cell 13
years = np.arange(-6755, 2300)
iyear = 0
tsi = np.ones(2300+6755) * np.nan
for idx in range(idx_1850):
    tsi[iyear] = np.sum(ssi[idx,:]*wl_bin)
    iyear = iyear+1
for i, idx in enumerate(idx_yearstart):
    tsi[iyear] = np.sum(np.mean(ssi[idx_yearstart[i]:idx_yearend[i],:], axis=0)*wl_bin)
    iyear = iyear+1
for i, year in enumerate(years_future):
    weights = [31,28+isleap[i],31,30,31,30,31,31,30,31,30,31]
    tsi[iyear] = np.average(tsi_future[(166+i)*12:(167+i)*12], weights=weights)
    iyear = iyear+1
    #print (np.mean(ssi[idx_yearstart[i]:idx_yearend[i]]))

# %% cell 14
satirem14c_cmip6_df = pd.DataFrame({'Year': years, 'TSI': tsi})
satirem14c_cmip6_df.set_index('Year', inplace=True)
satirem14c_cmip6_df
solar_df = solar_df.join(satirem14c_cmip6_df)
solar_df.rename(columns={'TSI': 'SATIRE-M 14C CMIP6'}, inplace=True)

# %% cell 15
solar_df.loc[1900]

# %% cell 17
check_and_download(
    '../data_input_large/SSI_14C_cycle_yearly_cmip_v20160613_nfc.nc',
    'https://sharebox.lsce.ipsl.fr/index.php/s/LpiCUCkSmx0P6bb/download?path=%2F&files=SSI_14C_cycle_yearly_cmip_v20160613_nfc.nc'
)

# %% cell 18
nc = Dataset('../data_input_large/SSI_14C_cycle_yearly_cmip_v20160613_nfc.nc')
wl_bin = nc.variables['wavelength_bin'][:]
time   = nc.variables['time'][:]
ssi    = nc.variables['ssi'][:]
nc.close()

# %% cell 19
years = np.arange(1850, 2016, dtype=int)
steps = np.ones(166, dtype=int) * 365
steps[np.logical_and(years%4==0, np.logical_or(years%100!=0, years%400==0))] = 366
idx_1850 = np.argmin(time<1850)
idx_yearend = idx_1850+np.cumsum(steps)
idx_yearstart = np.insert(idx_yearend, 0, [idx_1850])[:-1] 
print (idx_yearstart[:10], idx_yearend[:10])

# %% cell 20
years = np.arange(-6755, 2016)
iyear = 0
tsi = np.ones(2016+6755) * np.nan
for idx in range(idx_1850):
    tsi[iyear] = np.sum(ssi[idx,:]*wl_bin)
    iyear = iyear+1
for i, idx in enumerate(idx_yearstart):
    tsi[iyear] = np.sum(np.mean(ssi[idx_yearstart[i]:idx_yearend[i],:], axis=0)*wl_bin)
    iyear = iyear+1

# %% cell 21
satirem14c_df = pd.DataFrame({'Year': years, 'TSI': tsi})
satirem14c_df.set_index('Year', inplace=True)
satirem14c_df
solar_df = solar_df.join(satirem14c_df)
solar_df.rename(columns={'TSI': 'SATIRE-M 14C'}, inplace=True)

# %% cell 23
check_and_download(
    '../data_input_large/SSI_10Be_cycle_yearly_cmip_v20160613_fc.nc',
    'https://sharebox.lsce.ipsl.fr/index.php/s/LpiCUCkSmx0P6bb/download?path=%2F&files=SSI_10Be_cycle_yearly_cmip_v20160613_fc.nc'
)

# %% cell 24
nc = Dataset('../data_input_large/SSI_10Be_cycle_yearly_cmip_v20160613_fc.nc')
wl_bin = nc.variables['wavelength_bin'][:]
time   = nc.variables['time'][:]
ssi    = nc.variables['ssi'][:]
nc.close()

# %% cell 25
years = np.arange(1850, 2016, dtype=int)
steps = np.ones(166, dtype=int) * 365
steps[np.logical_and(years%4==0, np.logical_or(years%100!=0, years%400==0))] = 366
idx_1850 = np.argmin(time<1850)
idx_yearend = idx_1850+np.cumsum(steps)
idx_yearstart = np.insert(idx_yearend, 0, [idx_1850])[:-1] 
print (idx_yearstart[:10], idx_yearend[:10])
years_future = np.arange(2016, 2300)
isleap = np.zeros(284)
isleap[np.logical_and(years_future%4==0, np.logical_or(years_future%100!=0, years_future%400==0))] = 1

# %% cell 26
years = np.arange(885, 2300)
iyear = 0
tsi = np.ones(2300-885) * np.nan
for idx in range(idx_1850):
    tsi[iyear] = np.sum(ssi[idx,:]*wl_bin)
    iyear = iyear+1
for i, idx in enumerate(idx_yearstart):
    tsi[iyear] = np.sum(np.mean(ssi[idx_yearstart[i]:idx_yearend[i],:], axis=0)*wl_bin)
    iyear = iyear+1
for i, year in enumerate(years_future):
    weights = [31,28+isleap[i],31,30,31,30,31,31,30,31,30,31]
    tsi[iyear] = np.average(tsi_future[(166+i)*12:(167+i)*12], weights=weights)
    iyear = iyear+1
    #print (np.mean(ssi[idx_yearstart[i]:idx_yearend[i]]))

# %% cell 27
satirem10be_cmip6_df = pd.DataFrame({'Year': years, 'TSI': tsi})
satirem10be_cmip6_df.set_index('Year', inplace=True)
satirem10be_cmip6_df
solar_df = solar_df.join(satirem10be_cmip6_df)
solar_df.rename(columns={'TSI': 'SATIRE-M 10Be CMIP6'}, inplace=True)

# %% cell 29
check_and_download(
    '../data_input_large/SSI_10Be_cycle_yearly_cmip_v20160613_nfc.nc',
    'https://sharebox.lsce.ipsl.fr/index.php/s/LpiCUCkSmx0P6bb/download?path=%2F&files=SSI_10Be_cycle_yearly_cmip_v20160613_nfc.nc'
)

# %% cell 30
nc = Dataset('../data_input_large/SSI_10Be_cycle_yearly_cmip_v20160613_nfc.nc')
wl_bin = nc.variables['wavelength_bin'][:]
time   = nc.variables['time'][:]
ssi    = nc.variables['ssi'][:]
#print(time[:1000])
nc.close()

# %% cell 31
years = np.arange(1850, 2016, dtype=int)
steps = np.ones(166, dtype=int) * 365
steps[np.logical_and(years%4==0, np.logical_or(years%100!=0, years%400==0))] = 366
idx_1850 = np.argmin(time<1850)
idx_yearend = idx_1850+np.cumsum(steps)
idx_yearstart = np.insert(idx_yearend, 0, [idx_1850])[:-1] 
print (idx_yearstart[:10], idx_yearend[:10])

# %% cell 32
years = np.arange(-6755, 2016)
iyear = 0
tsi = np.ones(2016+6755) * np.nan
for idx in range(idx_1850):
    tsi[iyear] = np.sum(ssi[idx,:]*wl_bin)
    iyear = iyear+1
for i, idx in enumerate(idx_yearstart):
    tsi[iyear] = np.sum(np.mean(ssi[idx_yearstart[i]:idx_yearend[i],:], axis=0)*wl_bin)
    iyear = iyear+1

# %% cell 33
satirem10be_df = pd.DataFrame({'Year': years, 'TSI': tsi})
satirem10be_df.set_index('Year', inplace=True)
satirem10be_df
solar_df = solar_df.join(satirem10be_df)
solar_df.rename(columns={'TSI': 'SATIRE-M 10Be'}, inplace=True)

# %% cell 35
lean = np.loadtxt('../data_input/Lean_2018_ESS/Lean_2018_TSI.txt', skiprows=8)
pl.fill_between(lean[:,0], lean[:,1]-lean[:,3], lean[:,1]+lean[:,3])
pl.plot(lean[:,0], lean[:,1], color='k')

years = lean[:,0].astype(int)
lean_df = pd.DataFrame({'Year': years, 'TSI': lean[:,1]})
lean_df.set_index('Year', inplace=True)
solar_df = solar_df.join(lean_df)
solar_df.rename(columns={'TSI': 'NRLTSI2'}, inplace=True)

# %% cell 37
solar_df.loc[1700]

# %% cell 38
solar_df.plot()
pl.xlim(1700,2020)
#pl.legend()

# %% cell 40
solmin_1745=satirem14c_cmip6_df.loc[1742:1748,'TSI'].mean()
solmin_2008=satirem14c_cmip6_df.loc[2005:2011,'TSI'].mean()
solmin_2019=satirem14c_cmip6_df.loc[2016:2022,'TSI'].mean()
0.25 * 0.70 * 0.78 * (solmin_2008-solmin_1745)

# %% cell 42
0.25 * 0.70 * 0.78 * (solmin_2019-solmin_1745)

# %% cell 44
# first, find first minimum. Clearly -6754.
satirem14c_cmip6_df.iloc[:12]

# %% cell 45
# the cycle before 1750 ended 1744
satirem14c_cmip6_df.loc[1740:1750]

# %% cell 46
tsi_baseline = satirem14c_cmip6_df.loc[-6744:1744].mean()
tsi_baseline

# %% cell 47
solar_erf = 0.25 * (satirem14c_cmip6_df-tsi_baseline) * 0.71 * 0.72
# 0.25: geometry
# 0.71: 1-planetary albedo
# 0.72: stratospheric adjustments (22%: Gray) and tropospheric adjustments (6%: Smith)

# %% cell 48
pl.plot(solar_erf.loc[1700:2100])
pl.axhline(0, color='k', ls=':')

# %% cell 50
print(solar_erf.loc[2009:2019].mean())

# %% cell 52
solar_erf.loc[2019]

# %% cell 53
#df = pd.DataFrame(data=solar_erf, index=years, columns=['solar_erf'])
#df.index.name = 'year'
solar_erf.rename(columns={'TSI': 'solar_erf'}, inplace=True)
solar_erf.index.name = 'year'
solar_erf.to_csv('../data_output/solar_erf.csv')
solar_erf

# %% cell 55
solar_df

# %% cell 56
0.25*0.71*0.72*(solar_df.loc[2005:2011,'NRLTSI2'].mean() - solar_df.loc[1742:1748,'NRLTSI2'].mean())

# %% cell 57
0.25*0.71*0.72*(solar_df.loc[2005:2011,'SATIRE-M 10Be CMIP6'].mean() - solar_df.loc[1742:1748,'SATIRE-M 10Be CMIP6'].mean())

# %% cell 58
0.25*0.71*0.72*(solar_df.loc[2005:2011,'SATIRE-M 14C CMIP6'].mean() - solar_df.loc[1742:1748,'SATIRE-M 14C CMIP6'].mean())

# %% cell 60
-0.95 * 0.25*0.71*0.72

# %% cell 61
1.25 * 0.25*0.71*0.72
