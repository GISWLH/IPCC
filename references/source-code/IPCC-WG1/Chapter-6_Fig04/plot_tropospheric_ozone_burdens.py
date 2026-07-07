import netCDF4 as nc
from matplotlib import rcParams
import matplotlib.pyplot as plt
import pandas as pd
import pylab as plt
import numpy as np
import xarray as xr

# # MRI-ESM2
MRI_hist_r1 = pd.read_csv('data/burdens_MRI-ESM2-0_historical_1850-2014_pressure_excl_r1.csv', index_col=[0])
MRI_hist_r1.index = pd.to_datetime(MRI_hist_r1.index, format='%Y')
MRI_hist_r1.drop(columns='Year', inplace=True)
MRI_hist_r2_5 = pd.read_csv('data/burdens_MRI-ESM2-0_historical_1850-2014_pressure_excl_r2-r5.csv', index_col=[0])
MRI_hist_r2_5.index = pd.to_datetime(MRI_hist_r2_5.index, format='%Y')
MRI_hist_r2_5.drop(columns='Year',  inplace=True)
MRI_hist = pd.concat([MRI_hist_r1,MRI_hist_r2_5], axis=1)
MRI_hist['mean_MRI'] = MRI_hist[['r1i1p1f1', 'r2i1p1f1', 'r3i1p1f1', 'r4i1p1f1', 'r5i1p1f1']].mean(axis=1)
MRI_hist['std_MRI'] = MRI_hist[['r1i1p1f1','r2i1p1f1', 'r3i1p1f1', 'r4i1p1f1', 'r5i1p1f1']].std(axis=1)
MRI_hist.index = MRI_hist_r1.index
MRI_ssp370 = pd.read_csv('data/burdens_MRI-ESM2-0_ssp370_2015-2099_pressure_excl.csv', index_col=[0])
MRI_ssp370.index = pd.to_datetime(MRI_ssp370.index, format='%Y')
MRI_ssp370['mean_MRI'] = MRI_ssp370[['r2i1p1f1', 'r3i1p1f1', 'r1i1p1f1']].mean(axis=1)
MRI_ssp370['std_MRI'] = MRI_ssp370[['r2i1p1f1', 'r3i1p1f1', 'r1i1p1f1']].std(axis=1)
MRI_ssp370.drop(columns='Year', inplace=True)
MRI=pd.concat([MRI_hist,MRI_ssp370])
MRI = MRI/1e9
MRI = MRI.groupby(MRI.index.year).mean()

# GISS-E2-1-H
GISS_LTM = pd.read_csv('data/GISS.CMIP6.historical.ssp370.csv')
GISS_LTM.set_index(pd.to_datetime(GISS_LTM['year'], format='%Y'), inplace=True)
r1, r2, r3, r4, r5, r6, r7, r8, r9,r10 = 'E212Tomaf10aF40oQ40_2', 'E212Tomaf10bF40oQ40_2',       'E212Tomaf10cF40oQ40_2', 'E212Tomaf10dF40oQ40_2',       'E212Tomaf10eF40oQ40_2', 'E212Tomaf10fF40oQ40_2',       'E212Tomaf10gF40oQ40_2', 'E212Tomaf10hF40oQ40_2',       'E212Tomaf10iF40oQ40_2', 'E212Tomaf10jF40oQ40_2'
r1 = GISS_LTM[(GISS_LTM['ens']==r1) & (GISS_LTM['Tropopause Definition']=='Exclusive')]
GISS_hist = pd.DataFrame(index=pd.to_datetime(r1['year'], format='%Y'))
GISS_hist['r1'] = r1['Burden (Tg)']
GISS_hist['r2'] = GISS_LTM[(GISS_LTM['ens']==r2) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_hist['r3'] = GISS_LTM[(GISS_LTM['ens']==r3) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_hist['r4'] = GISS_LTM[(GISS_LTM['ens']==r4) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_hist['r5'] = GISS_LTM[(GISS_LTM['ens']==r5) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_hist['r6'] = GISS_LTM[(GISS_LTM['ens']==r6) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_hist['r7'] = GISS_LTM[(GISS_LTM['ens']==r7) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_hist['r8'] = GISS_LTM[(GISS_LTM['ens']==r8) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_hist['r9'] = GISS_LTM[(GISS_LTM['ens']==r9) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_hist['r10'] = GISS_LTM[(GISS_LTM['ens']==r10) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_hist['mean_giss'] = GISS_hist[['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10']].mean(axis=1)
GISS_hist['std_giss'] =  GISS_hist[['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10']].std(axis=1)
r11,r12,r13,r14 = 'E212TomaSSP370aF40oQ40', 'E212TomaSSP370bF40oQ40', 'E212TomaSSP370cF40oQ40', 'E212TomaSSP370dF40oQ40'
r11 = GISS_LTM[(GISS_LTM['ens']==r11) & (GISS_LTM['Tropopause Definition']=='Exclusive')]
GISS_ssp370 = pd.DataFrame(index=pd.to_datetime(r11['year'], format='%Y'))
GISS_ssp370['r11'] = r11['Burden (Tg)']
GISS_ssp370['r12'] = GISS_LTM[(GISS_LTM['ens']==r12) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_ssp370['r13'] = GISS_LTM[(GISS_LTM['ens']==r13) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_ssp370['r14'] = GISS_LTM[(GISS_LTM['ens']==r14) & (GISS_LTM['Tropopause Definition']=='Exclusive')]['Burden (Tg)']
GISS_ssp370['mean_giss'] = GISS_ssp370[['r11','r12','r13','r14']].mean(axis=1)
GISS_ssp370['std_giss'] =  GISS_ssp370[['r11','r12','r13','r14']].std(axis=1)
giss = pd.concat([GISS_hist,GISS_ssp370])
giss = giss.groupby(giss.index.year).mean()

# GFDL-ESM4
gfdl_hist = pd.read_csv('data//burdens_GFDL-ESM4_historical_1850-2014_pressure_excl.csv', index_col=[0])
gfdl_hist.index = pd.to_datetime(gfdl_hist.index, format='%Y')
gfdl_ssp370 = pd.read_csv('data//burdens_GFDL-ESM4_ssp370_2015-2099_pressure_excl.csv', index_col=[0])
gfdl_ssp370.index = pd.to_datetime(gfdl_ssp370.index, format='%Y')
gfdl = pd.concat([gfdl_hist,gfdl_ssp370])
gfdl = gfdl/1e9
gfdl = gfdl.groupby(gfdl.index.year).mean()

# CESM2-WACCM
cesm2_waccm_hist = pd.read_csv('data/burdens_CESM2-WACCM_historical_1850-2014_pressure_excl.csv', index_col=[0])
cesm2_waccm_hist.index = pd.to_datetime(cesm2_waccm_hist.index, format="%Y")

cesm2_waccm_ssp370_r1 = pd.read_csv('data/burdens_CESM2-WACCM_ssp370_2015-2099_pressure_excl_r1.csv', index_col=[0])
cesm2_waccm_ssp370_r1.index = pd.to_datetime(cesm2_waccm_ssp370_r1.index, format="%Y")
cesm2_waccm_ssp370_r1 = cesm2_waccm_ssp370_r1.drop(columns='Year')

cesm2_waccm_ssp370_r2_r3 = pd.read_csv('data/burdens_CESM2-WACCM_ssp370_2015-2055_chemopause_r2-r3.csv', index_col=[0])
cesm2_waccm_ssp370_r2_r3.index = pd.to_datetime(cesm2_waccm_ssp370_r2_r3.index, format="%Y")
cesm2_waccm_ssp370_r2_r3 = cesm2_waccm_ssp370_r2_r3.drop(columns='Year')

cesm2_waccm_ssp370_r1['r2']= cesm2_waccm_ssp370_r2_r3['r2i1p1f1']
cesm2_waccm_ssp370_r1['r3']= cesm2_waccm_ssp370_r2_r3['r3i1p1f1']

cesm2_waccm_ssp370 = cesm2_waccm_ssp370_r1

cesm2_waccm=pd.concat([cesm2_waccm_hist,cesm2_waccm_ssp370])
cesm2_waccm = cesm2_waccm/1e9
cesm2_waccm['mean_cesm2_waccm'] = cesm2_waccm[['r2i1p1f1', 'r3i1p1f1', 'r1i1p1f1']].mean(axis=1)
cesm2_waccm['std_cesm2_waccm'] =  cesm2_waccm[['r2i1p1f1', 'r3i1p1f1', 'r1i1p1f1']].std(axis=1)
cesm2_waccm=cesm2_waccm.groupby(cesm2_waccm.index.year).mean()

# UKESM1
ukesm_hist = pd.read_csv('data/burdens_UKESM1-0-LL_historical_1850-2014_pressure_excl.csv', index_col=[0])
ukesm_hist.index = pd.to_datetime(ukesm_hist.index, format="%Y")
ukesm_ssp370 = pd.read_csv('data/burdens_UKESM1-0-LL_ssp370_2015-2099_pressure_excl.csv', index_col=[0])
ukesm_ssp370.index = pd.to_datetime(ukesm_ssp370.index, format="%Y")
ukesm=pd.concat([ukesm_hist,ukesm_ssp370])
ukesm_hist['mean_ukesm'] = ukesm_hist[['r1i1p1f2', 'r11i1p1f2', 'r16i1p1f2', 'r18i1p1f2', 'r1i1p1f2', 'r3i1p1f2',  
                                       'r9i1p1f2', 'r10i1p1f2', 'r12i1p1f2',  'r17i1p1f2','r19i1p1f2','r2i1p1f2', 
                                       'r4i1p1f2', 'r8i1p1f2']].mean(axis=1)
ukesm_hist['std_ukesm'] = ukesm_hist[['r1i1p1f2', 'r11i1p1f2', 'r16i1p1f2', 'r18i1p1f2', 'r1i1p1f2', 'r3i1p1f2', 
                                       'r9i1p1f2', 'r10i1p1f2', 'r12i1p1f2',  'r17i1p1f2','r19i1p1f2','r2i1p1f2', 
                                       'r4i1p1f2', 'r8i1p1f2']].std(axis=1)
ukesm_ssp370['mean_ukesm'] = ukesm_ssp370[['r10i1p1f2', 'r12i1p1f2', 'r17i1p1f2', 'r19i1p1f2', 'r2i1p1f2','r4i1p1f2', 'r8i1p1f2', 
                                           'r11i1p1f2', 'r16i1p1f2', 'r18i1p1f2', 'r1i1p1f2', 'r3i1p1f2', 'r9i1p1f2']].mean(axis=1)
ukesm_ssp370['std_ukesm'] = ukesm_ssp370[['r10i1p1f2', 'r12i1p1f2', 'r17i1p1f2', 'r19i1p1f2', 'r2i1p1f2','r4i1p1f2', 'r8i1p1f2',
                                          'r11i1p1f2', 'r16i1p1f2', 'r18i1p1f2', 'r1i1p1f2', 'r3i1p1f2', 'r9i1p1f2']].std(axis=1)
ukesm=pd.concat([ukesm_hist,ukesm_ssp370])
ukesm = ukesm/1e9
ukesm1=ukesm.groupby(ukesm.index.year).mean()

# group data into mean and std dev
all_means = pd.DataFrame()
all_means_no_UKESM = pd.DataFrame()
all_means['ukesm1'] = ukesm1['mean_ukesm']
all_means['ukesm1_std'] = ukesm1['std_ukesm']
all_means['gfdl'] = gfdl['r1i1p1f1']
all_means['cesm2-waccm'] = cesm2_waccm['mean_cesm2_waccm']
all_means['mri'] = MRI['mean_MRI']
all_means['giss'] = giss['mean_giss']
all_means['MMM'] = all_means[['ukesm1', 'gfdl', 'cesm2-waccm',  'giss', 'mri']].mean(axis=1)
all_means['STD'] = all_means[['ukesm1', 'gfdl', 'cesm2-waccm',  'giss', 'mri']].std(axis=1)
all_means_no_UKESM['MMM'] = all_means[[ 'gfdl', 'cesm2-waccm',  'giss', 'mri']].mean(axis=1)
all_means_no_UKESM['STD'] = all_means[[ 'gfdl', 'cesm2-waccm',  'giss', 'mri']].std(axis=1)
all_means['UL'] = all_means['MMM']+all_means['STD']
all_means['LL'] = all_means['MMM']-all_means['STD']

# TOAR burden
obs=pd.DataFrame()
obs['TOAR'] = [337]
b = pd.date_range(pd.datetime(1999, 1, 1), pd.datetime(2000, 1, 1), freq='Y')
obs.index=b
obs = obs.groupby(obs.index.year).mean()

# TOST data
tost=pd.DataFrame()
tost['TOST'] = [337]
b = pd.date_range(pd.datetime(2005, 1, 1), pd.datetime(2015, 1, 1), freq='10Y')
tost.index=b
tost = tost.groupby(tost.index.year).mean()

# ACCMIP data
accmip_years=np.array([1850, 1930,  1980, 2000 ])
accmip_data =np.array([240, 260, 320, 340])
accmip_ll = np.array([190, 220, 370, 380])
accmip_ul = np.array([270, 290, 290, 310])
accmip=pd.DataFrame()
accmip['Mean'] = accmip_data
accmip['LL'] = accmip_data-accmip_ll
accmip['UL'] = accmip_ul-accmip_data
accmip.index= pd.to_datetime(accmip_years, format='%Y')
accmip = accmip.groupby(accmip.index.year).mean()

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams.update({'font.size': 11})
fig = plt.figure(figsize=(9,6),dpi=300)
ax=plt.subplot(1,1,1)

ax.fill_between(all_means.index[0:165], all_means['UL'][0:165],all_means['LL'][0:165], color='blue', alpha=0.3, label='MMM - HIST')
all_means['MMM'][0:165].plot(color='blue',ax=ax, lw=3, alpha=0.9, label='')
ax.fill_between(all_means.index[165:], all_means['UL'][165:],all_means['LL'][165:], color='red', alpha=0.3, label='MMM - SSP370')
all_means['MMM'][165:].plot(color='red',ax=ax, lw=3, alpha=0.9, label='')
ax.errorbar(x=obs.index, y=[340], yerr=[34], marker='^', color='lightgreen', markersize=8, lw=3, label='TOAR')
ax.errorbar(x=accmip.index, y=accmip['Mean'], yerr=accmip['LL'], fmt='o', color='#004D40', alpha=0.5, markersize=8, lw=3, label='ACCMIP')
ax.errorbar(x=tost.index, y=[339], yerr=[6], marker='s', color='firebrick', markersize=12, alpha=1., lw=3, label='OBS')

leg = plt.legend(loc='upper left',ncol=2)
leg = plt.legend(framealpha = 0, loc = 'best')
cols = ['blue', 'red', 'lightgreen', '#004D40', 'firebrick']
i=0
for text in leg.get_texts():
    plt.setp(text, color = cols[i], fontsize=14)
    i=i+1
plt.grid(False)
plt.title('Tropospheric ozone burden')
ax.vlines(2014.5, ymin=180,ymax=500)
plt.ylim(180,500)
plt.ylabel('Tg')
plt.xlim(1845,2105)
plt.savefig('CH6_fig.png')