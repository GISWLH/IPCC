# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/345_chapter7_verify_GWP.ipynb

# %% cell 2
from fair.tools.gwp import gwp
from fair.constants import molwt
import pandas as pp
import numpy as np

from ar6.metrics.halogen_generic import halogen_analytical
from ar6.metrics.co2 import co2_analytical
from ar6.metrics.ch4 import ch4_analytical

from ar6.constants.gases import lifetimes, radeff

from fair.constants.general import M_ATMOS

# %% cell 4
co2_analytical(20)   # rf, agwp, delT, idelT

# %% cell 5
co2_analytical(50, d=np.array([3.424102092311, 285.003477841911]), q=np.array([0.443767728883447, 0.319591049742508]))

# %% cell 6
co2_analytical(100, d=np.array([3.424102092311, 285.003477841911]), q=np.array([0.443767728883447, 0.319591049742508]), co2=410, ch4=1866, n2o=332, a=np.array([0.2173, 0.2240, 0.2824, 0.2763]), alpha_co2=np.array([0, 394.4, 36.54, 4.304]))

# %% cell 7
co2_analytical(500)

# %% cell 8
rf, agwp, delT, idelT = co2_analytical(np.arange(101))

# %% cell 9
### Bill's Thomas Gasser IRF to move to a new module

# GTP is the ratio of "delT" values between gas of interest and CO2

from fair.constants import molwt

def ccycle_gasser(H, delT):
    dts = H[1]
    rf_co2, agwp_co2, delT_co2, idelT_co2 = co2_analytical(H)
    
    delT_cc = H*0.
    agwp_cc = H*0.
    rf_cc = H*0.
    F_CO2 = H*0.
    a = np.array([0.6368, 0.3322, 0.0310])  # Gasser et al. 2017
    alpha = np.array([2.376, 30.14, 490.1])

    gamma = 3.015*1E12  # kgCO2/yr/K  Gasser et al. 2017
    r_f = H*0.
    r_f[0] = np.sum(a)/dts
    for i in np.arange(0, 3):
        r_f = r_f-(a[i]/alpha[i])*np.exp(-H/alpha[i])

    for j in np.arange(H.size):
        for i in np.arange(j+1):
            F_CO2[j] = F_CO2[j]+delT[i]*gamma*r_f[j-i]*dts
    for j in np.arange(H.size):
        for i in np.arange(j+1):
            rf_cc[j] = rf_cc[j]+F_CO2[i]*rf_co2[j-i]*dts * \
                (molwt.CO2/12)
            agwp_cc[j] = agwp_cc[j]+F_CO2[i]*agwp_co2[j-i]*dts * \
                (molwt.CO2/12)
            delT_cc[j] = delT_cc[j]+F_CO2[i]*delT_co2[j-i]*dts * \
                (molwt.CO2/12)
    return rf_cc, agwp_cc, delT_cc

# %% cell 10
ccycle_gasser(np.arange(101), delT)

# %% cell 11
-3.49675758e-18 + 3.960979480442774e-16

# %% cell 13
lifetimes['CFC-11'], radeff['CFC-11'], molwt.CFC11
halogen_analytical(100, lifetimes['CFC-11'], radeff['CFC-11'], molwt.CFC11, 0.13)

# %% cell 14
halogen_analytical(100, lifetimes['CFC-11'], 0.927*radeff['CFC-11'], molwt.CFC11, 0.13)

# %% cell 15
halogen_analytical(100, 52, 0.25941, 137.36, 0.12)

# %% cell 16
# Raw metrics file from Bill Collins
df = pd.read_csv('../data_input/7sm/metrics_supplement.csv')

# %% cell 17
df

# %% cell 18
lt = df.loc[df['Acronym']=='CFC-11', 'Lifetime (yr)'].values[0]
re = df.loc[df['Acronym']=='CFC-11', 'Radiative efficiency (W m-2 ppb-1)'].values[0]

# %% cell 19
re

# %% cell 20
gwp(100, lt, re, molwt.CFC11)
