# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7_Fig06/055_chapter7_table7.6.ipynb

# %% cell 2
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as pl
import pandas as pd
from matplotlib import gridspec, rc
from matplotlib.lines import Line2D
from netCDF4 import Dataset
import warnings

from ar6.constants import NINETY_TO_ONESIGMA

# %% cell 3
# # # add models from Zelinka 14
z14_data = np.array([
    [-0.66, 0.28, -0.24, -0.01, 0.15, 0.01, -0.22], #'IPSL-CM5A-LR'
    [-0.58, 0.17, -0.51, 0.01, -0.01, 0.11, -0.04], #'CanESM2'
    [-0.63, 0.29, -0.80, 0.03, 0.18, 0.13, -0.17], #'NorESM1-M'
    [-1.13, 0.49, -0.76, 0.08, 0.00, -0.02, -0.21], #'CSIRO-Mk3-6-0'
    [-0.53, 0.26, -1.00, 0.06, -0.13, 0.14, -0.05], #'HadGEM2-A'
    [-0.91, 0.41, -0.99, -0.03, -0.13, 0.11, 0.02], #'GFDL-CM3'
    [-0.66, 0.16, -0.93, -0.01, -0.28, 0.22, 0.27], #'MIROC5'
    [-0.11, 0.12, -1.77, -0.09, -0.23, 0.00, 0.95], #'MRI-CGCM3'
    [-0.33, 0.21, -1.93, 0.06, -0.11, 0.17, 0.57], #'CESM1-CAM5'
])
print(z14_data[:,0])
ERFariCMIP5 = z14_data[:,0]+z14_data[:,1]+z14_data[:,5]
ERFaciCMIP5 = z14_data[:,2]+z14_data[:,3]+z14_data[:,4]+z14_data[:,6]
ERFCMIP5 = ERFariCMIP5+ERFaciCMIP5
print(ERFCMIP5)

# %% cell 4
df = pd.read_csv('../data_input/Smith_et_al_ACP_2020/aprp_aer_20200211.csv')
# treat GISS p1 and GISS p3 as separate models
df.loc[(df['Model']=='GISS-E2-1-G') & (df['Run']=='r1i1p1f1'),'Model'] = 'GISS-E2-1-G p1'
df.loc[(df['Model']=='GISS-E2-1-G') & (df['Run']=='r1i1p1f1'),'Model'] = 'GISS-E2-1-G p3'
df

# %% cell 5
data = []
erfari = []
erfaci = []
total = []

for model in df.Model.unique():
    erfari.append(1.05 * df.ERFari[df.Model==model].mean())
    erfaci.append(1.05 * df.ERFaci[df.Model==model].mean())
    total.append(1.05 * df.ERFari[df.Model==model].mean() + 1.05 * df.ERFaci[df.Model==model].mean())
    data.append([model, erfari[-1], erfaci[-1], total[-1]])
erfari = np.array(erfari)
erfaci = np.array(erfaci)
total = np.array(total)
data.append(['CMIP6 mean', np.nanmean(erfari), np.nanmean(erfaci), np.nanmean(total)])
data.append(
    [
        'CMIP6 range',
        NINETY_TO_ONESIGMA * np.nanstd(erfari, ddof=1), 
        NINETY_TO_ONESIGMA * np.nanstd(erfaci, ddof=1),
        NINETY_TO_ONESIGMA * np.nanstd(total, ddof=1)
    ]
) # use sample stdev and inflate to 5-95%
data.append(['CMIP5 mean', np.mean(1.05 * ERFariCMIP5), np.mean(1.05 * ERFaciCMIP5), np.mean(1.05 * ERFCMIP5)])
data.append(
    [
        'CMIP5 range',
        NINETY_TO_ONESIGMA * np.nanstd(1.05 * ERFariCMIP5),
        NINETY_TO_ONESIGMA * np.nanstd(1.05 * ERFaciCMIP5),
        NINETY_TO_ONESIGMA * np.nanstd(1.05 * ERFCMIP5)
    ]
)

# %% cell 6
df = pd.DataFrame(data, columns = ['Model', 'ERFari', 'ERFaci', 'ERFari+aci'])

# %% cell 7
df

# %% cell 8
df.to_csv('../data_output/table7.6.csv', index=False)
