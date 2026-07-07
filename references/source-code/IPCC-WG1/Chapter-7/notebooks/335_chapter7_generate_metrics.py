# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/335_chapter7_generate_metrics.ipynb

# %% cell 2
from fair.forcing.ghg import meinshausen

from tqdm.notebook import tqdm
import pandas as pd
import numpy as np

from ar6.metrics.halogen_generic import halogen_analytical
from ar6.metrics.co2 import co2_analytical
from ar6.metrics.ch4 import ch4_analytical
from ar6.metrics.n2o import n2o_analytical
from ar6.metrics.gasser import carbon_cycle_adjustment

# %% cell 4
# Input data file
# note, this is a file that has been cleaned up and standardised by Bill Collins
# original file is from Hodnebrog et al. 2020, Reviews of Geophysics
# https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019RG000691
# supplementary table S1
halo_file = "../data_input/Hodnebrog_et_al_2020_revgeo/hodnebrog20.csv"

# %% cell 5
# extract raw data
halo = np.genfromtxt(
    halo_file,
    delimiter=',',
    comments='£', # seemed to work better than None
    names=True,
    dtype="U30, U20, U20, U30, f8, f8, f8",
    usecols = (0, 1, 2, 3, 4, 5, 6)
)

# %% cell 6
# Allocate output table
num_halo = np.size(halo)
names = ['Name', 'CASRN', 'Acronym', 'Formula', 'Lifetime',
         'Radiative_efficiency', 'AGWP20', 'GWP20', 'AGWP100', 'GWP100', 'AGWP500', 'GWP500',
         'AGTP50', 'GTP50', 'AGTP100', 'GTP100', 'CGTP50', 'CGTP100']
formats = np.concatenate((np.repeat('U30',4), np.repeat('f8', 14)))
table = np.zeros(
    num_halo+3,
    dtype={
        'names': names,
        'formats': formats
    }
)

# %% cell 8
co2 = 409.9
ch4 = 1866.3
n2o = 332.1

# %% cell 10
ts_per_year = 10
H_max = 500  # years

# %% cell 12
rf_co2, agwp_co2, agtp_co2, iagtp_co2 = co2_analytical(
    np.linspace(0, H_max, H_max * ts_per_year + 1),
    d=np.array([3.424102092311, 285.003477841911]),
    #q=np.array([0.443767728883447, 0.319591049742508]),    # this is what is in Zeb's file sent 25 Feb
    q = np.array([0.443767728883447, 0.313998206372015]),   # this is what Bill used
    co2=co2, n2o=n2o,
    a=np.array([0.2173, 0.2240, 0.2824, 0.2763]),
    alpha_co2=np.array([0, 394.4, 36.54, 4.304]),
    co2_ra = 0.05
)

# %% cell 13
# Save to first row of output
table[0]['Name'] = 'Carbon dioxide'
table[0]['Formula'] = 'CO2'
table[0]['Lifetime'] = np.nan
table[0]['Radiative_efficiency'] = meinshausen(np.array([co2+0.001, 1866.3, n2o]), np.array([co2, 1866.3, n2o]), scale_F2x=False)[0] * 1.05
table[0]['AGWP20'] = agwp_co2[20 * ts_per_year]
table[0]['GWP20'] = 1.
table[0]['AGWP100'] = agwp_co2[100 * ts_per_year]
table[0]['GWP100'] = 1.
table[0]['AGWP500'] = agwp_co2[500 * ts_per_year]
table[0]['GWP500'] = 1.
table[0]['AGTP50'] = agtp_co2[50 * ts_per_year]
table[0]['GTP50'] = 1.
table[0]['AGTP100'] = agtp_co2[100 * ts_per_year]
table[0]['GTP100'] = 1.
table[0]

# %% cell 15
rf_ch4, agwp_ch4, agtp_ch4, iagtp_ch4 = ch4_analytical(
    np.linspace(0, H_max, H_max * ts_per_year + 1),
    d=np.array([3.424102092311, 285.003477841911]),
    #q=np.array([0.443767728883447, 0.319591049742508]),    # this is what is in Zeb's file sent 25 Feb
    q = np.array([0.443767728883447, 0.313998206372015]),   # this is what Bill used
    co2=co2, ch4=ch4, n2o=n2o,
    ch4_ra = -0.14,
    alpha_ch4 = 11.8,
    ch4_o3=1.4e-4,
    ch4_h2o=0.00004
)

# %% cell 17
rf_cc, agwp_cc, agtp_cc = carbon_cycle_adjustment(
    np.linspace(0, H_max, H_max * ts_per_year + 1),
    agtp_ch4,
    co2=co2,
    n2o=n2o,
    co2_ra = 0.05,
    d = np.array([3.424102092311, 285.003477841911]),
    #q=np.array([0.443767728883447, 0.319591049742508]),    # this is what is in Zeb's file sent 25 Feb
    q = np.array([0.443767728883447, 0.313998206372015]),   # this is what Bill used
)

# %% cell 18
# Save to second row of output
table[1]['Name'] = 'Methane'
table[1]['Formula'] = 'CH4'
table[1]['Lifetime'] = 11.8
table[1]['Radiative_efficiency'] = meinshausen(np.array([co2, ch4+1, n2o]), np.array([co2, ch4, n2o]), scale_F2x=False)[1] * 0.86
table[1]['AGWP20'] = agwp_ch4[20 * ts_per_year] + agwp_cc[20 * ts_per_year]
table[1]['GWP20'] = (agwp_ch4[20 * ts_per_year]+agwp_cc[20 * ts_per_year])/agwp_co2[20 * ts_per_year]
table[1]['AGWP100'] = agwp_ch4[100 * ts_per_year] + agwp_cc[100 * ts_per_year]
table[1]['GWP100'] = (agwp_ch4[100 * ts_per_year]+agwp_cc[100 * ts_per_year])/agwp_co2[100 * ts_per_year]
table[1]['AGWP500'] = agwp_ch4[500 * ts_per_year] + agwp_cc[500 * ts_per_year]
table[1]['GWP500'] = (agwp_ch4[500 * ts_per_year]+agwp_cc[500 * ts_per_year])/agwp_co2[500 * ts_per_year]
table[1]['AGTP50'] = agtp_ch4[50 * ts_per_year] + agtp_cc[50 * ts_per_year]
table[1]['GTP50'] = (agtp_ch4[50 * ts_per_year]+agtp_cc[50 * ts_per_year])/agtp_co2[50 * ts_per_year]
table[1]['AGTP100'] = agtp_ch4[100 * ts_per_year] + agtp_cc[100 * ts_per_year]
table[1]['GTP100'] = (agtp_ch4[100 * ts_per_year]+agtp_cc[100 * ts_per_year])/agtp_co2[100 * ts_per_year]
### and also CGTP for methane
rf_cc, agwp_cc, agtp_cc = carbon_cycle_adjustment(
    np.linspace(0, H_max, H_max * ts_per_year + 1),
    iagtp_ch4,
    co2=co2,
    n2o=n2o,
    co2_ra = 0.05,
    d = np.array([3.424102092311, 285.003477841911]),
    #q=np.array([0.443767728883447, 0.319591049742508]),    # this is what is in Zeb's file sent 25 Feb
    q = np.array([0.443767728883447, 0.313998206372015]),   # this is what Bill used
)
table[1]['CGTP50'] = (iagtp_ch4[50 * ts_per_year]+agtp_cc[50 * ts_per_year])/agtp_co2[50 * ts_per_year]
table[1]['CGTP100'] = (iagtp_ch4[100 * ts_per_year]+agtp_cc[100 * ts_per_year])/agtp_co2[100 * ts_per_year]
table[1]

# %% cell 20
rf_n2o, agwp_n2o, agtp_n2o, iagtp_n2o = n2o_analytical(
    np.linspace(0, H_max, H_max * ts_per_year + 1),
    d=np.array([3.424102092311, 285.003477841911]),
    #q=np.array([0.443767728883447, 0.319591049742508]),    # this is what is in Zeb's file sent 25 Feb
    q = np.array([0.443767728883447, 0.313998206372015]),   # this is what Bill used
    co2=co2, ch4=ch4, n2o=n2o
)
rf_cc, agwp_cc, agtp_cc = carbon_cycle_adjustment(
    np.linspace(0, H_max, H_max * ts_per_year + 1),
    agtp_n2o,
    co2=co2,
    n2o=n2o,
    co2_ra = 0.05,
    d = np.array([3.424102092311, 285.003477841911]),
    #q=np.array([0.443767728883447, 0.319591049742508]),    # this is what is in Zeb's file sent 25 Feb
    q = np.array([0.443767728883447, 0.313998206372015]),   # this is what Bill used
)

# %% cell 21
rf_n2o, agwp_n2o, agtp_n2o, iagtp_n2o

# %% cell 22
# Save to third row of output
table[2]['Name'] = 'Nitrous oxide'
table[2]['Formula'] = 'N2O'
table[2]['Lifetime'] = 109
table[2]['Radiative_efficiency'] = meinshausen(np.array([co2, ch4, n2o+1]), np.array([co2, ch4, n2o]), scale_F2x=False)[2] * 1.07
table[2]['AGWP20'] = agwp_n2o[20 * ts_per_year] + agwp_cc[20 * ts_per_year]
table[2]['GWP20'] = (agwp_n2o[20 * ts_per_year]+agwp_cc[20 * ts_per_year])/agwp_co2[20 * ts_per_year]
table[2]['AGWP100'] = agwp_n2o[100 * ts_per_year] + agwp_cc[100 * ts_per_year]
table[2]['GWP100'] = (agwp_n2o[100 * ts_per_year]+agwp_cc[100 * ts_per_year])/agwp_co2[100 * ts_per_year]
table[2]['AGWP500'] = agwp_n2o[500 * ts_per_year] + agwp_cc[500 * ts_per_year]
table[2]['GWP500'] = (agwp_n2o[500 * ts_per_year]+agwp_cc[500 * ts_per_year])/agwp_co2[500 * ts_per_year]
table[2]['AGTP50'] = agtp_n2o[50 * ts_per_year] + agtp_cc[50 * ts_per_year]
table[2]['GTP50'] = (agtp_n2o[50 * ts_per_year]+agtp_cc[50 * ts_per_year])/agtp_co2[50 * ts_per_year]
table[2]['AGTP100'] = agtp_n2o[100 * ts_per_year] + agtp_cc[100 * ts_per_year]
table[2]['GTP100'] = (agtp_n2o[100 * ts_per_year]+agtp_cc[100 * ts_per_year])/agtp_co2[100 * ts_per_year]
table[2]

# %% cell 25
i_out=3
for ispec in tqdm(np.arange(0, num_halo)):
    name = halo[ispec]['Name']
    alpha = halo[ispec]['Lifetime_yr']
    re = halo[ispec]['RE_W_m2_ppb1']
    if (halo[ispec]['Acronym']=='CFC-11' or halo[ispec]['Acronym'] == 'CFC-12'):
        cfc_ra = 0.12
    else:
        cfc_ra = 0
    mass = halo[ispec]['Molar_mass']
    print(name)
    table[i_out]['Name'] = name
    table[i_out]['CASRN'] = halo[ispec]['CASRN']
    table[i_out]['Acronym'] = halo[ispec]['Acronym']
    table[i_out]['Formula'] = halo[ispec]['Formula']
    table[i_out]['Lifetime'] = alpha
    table[i_out]['Radiative_efficiency'] = re * (1 + cfc_ra)
    if not np.isnan(alpha):
#  Pulse
        rf, agwp, agtp, iagtp = halogen_analytical(
            np.linspace(0, H_max, H_max * ts_per_year + 1),
            alpha,
            re,
            mass,
            d=np.array([3.424102092311, 285.003477841911]),
            #q=np.array([0.443767728883447, 0.319591049742508]),    # this is what is in Zeb's file sent 25 Feb
            q = np.array([0.443767728883447, 0.313998206372015]),   # this is what Bill used
            halogen_ra = cfc_ra
        )
        rf_cc, agwp_cc, agtp_cc = carbon_cycle_adjustment(
            np.linspace(0, H_max, H_max * ts_per_year + 1),
            agtp,
            co2=co2,
            n2o=n2o,
            co2_ra = 0.05,
        d = np.array([3.424102092311, 285.003477841911]),
        #q=np.array([0.443767728883447, 0.319591049742508]),    # this is what is in Zeb's file sent 25 Feb
        q = np.array([0.443767728883447, 0.313998206372015]),   # this is what Bill used
        )
        table[i_out]['AGWP20'] = (agwp[20 * ts_per_year]+agwp_cc[20 * ts_per_year])
        table[i_out]['GWP20'] = (agwp[20 * ts_per_year]+agwp_cc[20 * ts_per_year])/agwp_co2[20 * ts_per_year]
        table[i_out]['AGWP100'] = (agwp[100 * ts_per_year]+agwp_cc[100 * ts_per_year])
        table[i_out]['GWP100'] = (agwp[100 * ts_per_year]+agwp_cc[100 * ts_per_year])/agwp_co2[100 * ts_per_year]
        table[i_out]['AGWP500'] = (agwp[500 * ts_per_year]+agwp_cc[500 * ts_per_year])
        table[i_out]['GWP500'] = (agwp[500 * ts_per_year]+agwp_cc[500 * ts_per_year])/agwp_co2[500 * ts_per_year]
        table[i_out]['AGTP50'] = (agtp[50 * ts_per_year]+agtp_cc[50 * ts_per_year])
        table[i_out]['GTP50'] = (agtp[50 * ts_per_year]+agtp_cc[50 * ts_per_year])/agtp_co2[50 * ts_per_year]
        table[i_out]['AGTP100'] = (agtp[100 * ts_per_year]+agtp_cc[100 * ts_per_year])
        table[i_out]['GTP100'] = (agtp[100 * ts_per_year]+agtp_cc[100 * ts_per_year])/agtp_co2[100 * ts_per_year]
# Step
        if alpha < 20.:
            rf_cc, agwp_cc, agtp_cc = carbon_cycle_adjustment(
                np.linspace(0, H_max, H_max * ts_per_year + 1),
                iagtp,
                co2=co2,
                n2o=n2o,
                co2_ra = 0.05,
                d = np.array([3.424102092311, 285.003477841911]),
                #q=np.array([0.443767728883447, 0.319591049742508]),    # this is what is in Zeb's file sent 25 Feb
                q = np.array([0.443767728883447, 0.313998206372015]),   # this is what Bill used
            )
            table[i_out]['CGTP50'] = (iagtp[50 * ts_per_year]+agtp_cc[50 * ts_per_year])/agtp_co2[50 * ts_per_year]
            table[i_out]['CGTP100'] = (iagtp[100 * ts_per_year]+agtp_cc[100 * ts_per_year])/agtp_co2[100 * ts_per_year]
        else:
            table[i_out]['CGTP50'] = np.nan 
            table[i_out]['CGTP100'] = np.nan
        i_out += 1

# %% cell 27
fmt = '%30s'+', %20s'*2+', %30s'+', %5.3f'*2+ ', %7.5e, %5.3f'*5+', %5.3f, %5.3f'

# %% cell 28
np.savetxt(
    "../data_input/ghg_properties/metrics_supplement.csv",
    table[:i_out],
    delimiter=',',
    fmt=fmt,
    header=','.join(table.dtype.names)
)
