# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/090_chapter7_table7.5.ipynb

# %% cell 2
from fair.forcing.ghg import meinshausen
import numpy as np
import scipy.stats as st
import pandas as pd

from ar6.constants.gases import radeff

# %% cell 4
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
ghg_obs

# %% cell 5
forcing_minor_1750 = pd.read_csv('../data_output/AR6_ERF_minorGHGs_1750-2019.csv', index_col=0)
list_signif_0005 = ['CO2', 'CH4', 'N2O'] + forcing_minor_1750.loc[:,forcing_minor_1750.loc[2019,:]>0.0005].columns.tolist()
list_signif_0010 = ['CO2', 'CH4', 'N2O'] + forcing_minor_1750.loc[:,forcing_minor_1750.loc[2019,:]>=0.001].columns.tolist()
print(list_signif_0005)
print(list_signif_0010)

# %% cell 6
list_signif = [   # from table 2.3 - not the same as ERF > 0.001
    'CO2',
    'CH4',
    'N2O',
    'CFC-11',
    'CFC-12',
    'CFC-113',
    'CFC-114',
    'CFC-115',
    'CCl4',
    'Halon-1211',
    'Halon-1301',
    'HCFC-22',
    'HCFC-141b',
    'HCFC-142b',
    'HFC-23',
    'HFC-32',
    'HFC-125',
    'HFC-134a',
    'HFC-143a',
    'CF4',
    'C2F6',
    'SF6',
]

# %% cell 7
gases = ghg_obs.columns.to_list()
gases.remove('YYYY')

# %% cell 8
ghg_obs.loc[[2019, 2011, 1850, 1750],list_signif_0010].round(
    {
        'CO2':1,
        'CH4':0,
        'N2O':1,
        'CFC-11':0,
        'CFC-12':0,
        'CFC-113':1,
        'CFC-114':1,
        'CFC-115':2,
        'CCl4':1,
        'Halon-1211':2,
        'Halon-1301':2,
        'HCFC-22':0,
        'HCFC-141b':1,
        'HCFC-142b':1,
        'HFC-23':1,
        'HFC-32':1,
        'HFC-125':1,
        'HFC-134a':1,
        'HFC-143a':1,
        'CF4':1,
        'C2F6':2,
        'SF6':2,
    }
).T.style.format('{0:g}')

# %% cell 9
forcing1750 = {}
co2base1750 = np.zeros(270)
ch4base1750 = np.zeros(270)
n2obase1750 = np.zeros(270)
forcing1850 = {}
co2base1850 = np.zeros(270)
ch4base1850 = np.zeros(270)
n2obase1850 = np.zeros(270)
c = np.array([ghg_obs['CO2'].values, ghg_obs['CH4'].values, ghg_obs['N2O'].values])
for i, year in enumerate(range(1750,2020)):
    co2base1750[i], ch4base1750[i], n2obase1750[i] = meinshausen(c[:,i], [ghg_obs.loc[1750,'CO2'], ghg_obs.loc[1750,'CH4'], ghg_obs.loc[1750,'N2O']], scale_F2x=False)
    co2base1850[i], ch4base1850[i], n2obase1850[i] = meinshausen(c[:,i], [ghg_obs.loc[1850,'CO2'], ghg_obs.loc[1850,'CH4'], ghg_obs.loc[1850,'N2O']], scale_F2x=False)

# include rapid adjustments for CO2, CH4 and N2O
forcing1750['CO2'] = 1.05 * co2base1750
forcing1750['CH4'] = 0.86 * ch4base1750
forcing1750['N2O'] = 1.07 * n2obase1750
forcing1850['CO2'] = 1.05 * co2base1850
forcing1850['CH4'] = 0.86 * ch4base1850
forcing1850['N2O'] = 1.07 * n2obase1850

# %% cell 10
forcing1850['CO2'][269]

# %% cell 11
trop_adjustment_scale = radeff.copy()
for key in trop_adjustment_scale.keys():
    trop_adjustment_scale[key] = 1
trop_adjustment_scale['CFC-11'] = 1.13
trop_adjustment_scale['CFC-12'] = 1.12

for gas in gases[3:]:
    forcing1750[gas] = (ghg_obs.loc[:,gas] - ghg_obs.loc[1750,gas]).values * radeff[gas] * 0.001 * trop_adjustment_scale[gas]
    forcing1850[gas] = (ghg_obs.loc[:,gas] - ghg_obs.loc[1850,gas]).values * radeff[gas] * 0.001 * trop_adjustment_scale[gas]

# %% cell 12
forcing1750

# %% cell 13
gases

# %% cell 14
uncert = {}
uncert['CO2'] = 0.12
uncert['CH4'] = 0.20
uncert['N2O'] = 0.15
uncert['Halogens'] = 0.19

# %% cell 15
gases_cfcs = ['CFC-12', 'CFC-11', 'CFC-113', 'CFC-114', 'CFC-115', 'CFC-13']
gases_hcfcs= ['HCFC-22', 'HCFC-141b', 'HCFC-142b', 'HCFC-133a', 'HCFC-31', 'HCFC-124']
gases_hfcs = ['HFC-134a', 'HFC-23', 'HFC-32', 'HFC-125', 'HFC-143a', 'HFC-152a', 'HFC-227ea', 'HFC-236fa', 'HFC-245fa', 'HFC-365mfc', 'HFC-43-10mee',]
gases_halo = gases[3:]

# %% cell 17
gases_montreal = [
    'CFC-12',
    'CFC-11',
    'CFC-113',
    'CFC-114',
    'CFC-115',
    'CFC-13',
    'HCFC-22',
    'HCFC-141b',
    'HCFC-142b',
    'CH3CCl3',
    'CCl4',  # yes
    'CH3Cl',  # no
    'CH3Br',  # yes
    'CH2Cl2',  # no!
    'CHCl3',  # no
    'Halon-1211',
    'Halon-1301',
    'Halon-2402',
    'CFC-112',
    'CFC-112a',
    'CFC-113a',
    'CFC-114a',
    'HCFC-133a',
    'HCFC-31',
    'HCFC-124'
]
gases_pfc = [
    'CF4',
    'C2F6',
    'C3F8',
    'c-C4F8',
    'n-C4F10',
    'n-C5F12',
    'n-C6F14',
    'i-C6F14',
    'C7F16',
    'C8F18',
]

# %% cell 19
forcing1750['CFCs'] = np.zeros(270)
forcing1750['HCFCs'] = np.zeros(270)
forcing1750['HFCs'] = np.zeros(270)
forcing1750['Halogens'] = np.zeros(270)
forcing1850['CFCs'] = np.zeros(270)
forcing1850['HCFCs'] = np.zeros(270)
forcing1850['HFCs'] = np.zeros(270)
forcing1850['Halogens'] = np.zeros(270)

# new categories in SPM approval
forcing1750['Montreal'] = np.zeros(270)
forcing1750['PFCs'] = np.zeros(270)
forcing1850['Montreal'] = np.zeros(270)
forcing1850['PFCs'] = np.zeros(270)

for gas in gases_cfcs:
    forcing1750['CFCs'] = forcing1750['CFCs'] + forcing1750[gas]
    forcing1850['CFCs'] = forcing1850['CFCs'] + forcing1750[gas]
for gas in gases_hcfcs:
    forcing1750['HCFCs'] = forcing1750['HCFCs'] + forcing1750[gas]
    forcing1850['HCFCs'] = forcing1850['HCFCs'] + forcing1750[gas]
for gas in gases_hfcs:
    forcing1750['HFCs'] = forcing1750['HFCs'] + forcing1750[gas]
    forcing1850['HFCs'] = forcing1850['HFCs'] + forcing1750[gas]
for gas in gases_halo:
    forcing1750['Halogens'] = forcing1750['Halogens'] + forcing1750[gas]
    forcing1850['Halogens'] = forcing1850['Halogens'] + forcing1750[gas]
for gas in gases_montreal:
    forcing1750['Montreal'] = forcing1750['Montreal'] + forcing1750[gas]
    forcing1850['Montreal'] = forcing1850['Montreal'] + forcing1750[gas]
for gas in gases_pfc:
    forcing1750['PFCs'] = forcing1750['PFCs'] + forcing1750[gas]
    forcing1850['PFCs'] = forcing1850['PFCs'] + forcing1750[gas]
forcing1750['Total'] = forcing1750['CO2'] + forcing1750['CH4'] + forcing1750['N2O'] + forcing1750['Halogens']
forcing1850['Total'] = forcing1850['CO2'] + forcing1850['CH4'] + forcing1850['N2O'] + forcing1850['Halogens']

# %% cell 20
forcing1750 = pd.DataFrame(forcing1750)
forcing1850 = pd.DataFrame(forcing1850)

# %% cell 21
list_signif_plus = list_signif_0010 + ['Montreal', 'PFCs', 'HFCs', 'Halogens', 'Total']

# %% cell 22
forcing1750.loc[[269,261],list_signif_plus].round(
    {
        'CO2': 3,
        'CH4': 3,
        'N2O': 3,
        'CFC-11': 3,
        'CFC-12': 3,
        'CFC-113': 3,
        'CFC-114': 3,
        'CFC-115': 3,
        'Halon-1211': 3,
        'Halon-1301': 3,
        'HCFC-22': 3,
        'HCFC-141b': 3,
        'HCFC-142b': 3,
        'HFC-23': 3,
        'HFC-32': 3,
        'HFC-125': 3,
        'HFC-134a': 3,
        'HFC-143a': 3,
        'HFC-152a': 3,
        'SF6': 3,
        'SO2F2': 3,
        'NF3': 3,
        'CF4': 3,
        'C2F6': 3,
        'CH3CCl3': 3,
        'CCl4': 3,
        'CFCs': 3,
        'HCFCs': 3,
        'Montreal': 3,
        'PFCs': 3,
        'HFCs': 3,
        'Halogens': 3,
        'Total': 3
    }
).T.style.format('{0:g}')

# %% cell 23
forcing1850.loc[[269,261],list_signif_plus].round(
    {
        'CO2': 3,
        'CH4': 3,
        'N2O': 3,
        'CFC-11': 3,
        'CFC-12': 3,
        'CFC-113': 3,
        'CFC-114': 3,
        'CFC-115': 3,
        'Halon-1211': 3,
        'Halon-1301': 3,
        'HCFC-22': 3,
        'HCFC-141b': 3,
        'HCFC-142b': 3,
        'HFC-23': 3,
        'HFC-32': 3,
        'HFC-125': 3,
        'HFC-134a': 3,
        'HFC-143a': 3,
        'HFC-152a': 3,
        'SF6': 3,
        'SO2F2': 3,
        'NF3': 3,
        'CF4': 3,
        'C2F6': 3,
        'CH3CCl3': 3,
        'CCl4': 3,
        'CFCs': 3,
        'HCFCs': 3,
        'Montreal': 3,
        'PFCs': 3,
        'HFCs': 3,
        'Halogens': 3,
        'Total': 3,
    }
).T.style.format('{0:g}')

# %% cell 24
df = pd.concat(
    (
        ghg_obs.loc[[2019, 2011, 1850, 1750],list_signif_0010].T, 
        forcing1850.loc[[269,261],list_signif_plus].T,
        forcing1750.loc[[269,261],list_signif_plus].T
    ), axis=1
)
df.columns = ['conc 2019', 'conc 2011', 'conc 1850', 'conc 1750', 'ERF 1850-2019', 'ERF 1850-2011', 'ERF 1750-2019', 'ERF 1750-2011']
df.to_csv('../data_output/table7.5.csv')

# %% cell 25
# We'll assume that uncertainty in halogens is 19%

print("CO2 1850-2019", df.loc['CO2', 'ERF 1850-2019'] * uncert['CO2'])
print("CO2 1750-2019", df.loc['CO2', 'ERF 1750-2019'] * uncert['CO2'])
print("CH4 1850-2019", df.loc['CH4', 'ERF 1850-2019'] * uncert['CH4'])
print("CH4 1750-2019", df.loc['CH4', 'ERF 1750-2019'] * uncert['CH4'])
print("N2O 1850-2019", df.loc['N2O', 'ERF 1850-2019'] * uncert['N2O'])
print("N2O 1750-2019", df.loc['N2O', 'ERF 1750-2019'] * uncert['N2O'])
print("Hal 1850-2019", df.loc['Halogens', 'ERF 1850-2019'] * uncert['Halogens'])
print("Hal 1750-2019", df.loc['Halogens', 'ERF 1750-2019'] * uncert['Halogens'])
print("Sum 1850-2019", np.sqrt((df.loc['CO2', 'ERF 1850-2019'] * uncert['CO2'])**2)+
             ((df.loc['CH4', 'ERF 1850-2019'] * uncert['CH4'])**2)+
             ((df.loc['N2O', 'ERF 1850-2019'] * uncert['N2O'])**2)+
             ((df.loc['Halogens', 'ERF 1850-2019'] * uncert['Halogens'])**2)
     )
print("Sum 1750-2019", np.sqrt((df.loc['CO2', 'ERF 1750-2019'] * uncert['CO2'])**2)+
             ((df.loc['CH4', 'ERF 1750-2019'] * uncert['CH4'])**2)+
             ((df.loc['N2O', 'ERF 1750-2019'] * uncert['N2O'])**2)+
             ((df.loc['Halogens', 'ERF 1750-2019'] * uncert['Halogens'])**2)
     )

# %% cell 26
pfc_hfc134a_eq_2019 = 0
for gas in gases_pfc:
    pfc_hfc134a_eq_2019 = pfc_hfc134a_eq_2019 + (ghg_obs.loc[2019, gas] * radeff[gas] / radeff['CF4'])
hfc_hfc134a_eq_2019 = 0
for gas in gases_hfcs:
    hfc_hfc134a_eq_2019 = hfc_hfc134a_eq_2019 + (ghg_obs.loc[2019, gas] * radeff[gas] / radeff['HFC-134a'])
montreal_cfc12_eq_2019 = 0
for gas in gases_montreal:
    montreal_cfc12_eq_2019 = montreal_cfc12_eq_2019 + (ghg_obs.loc[2019, gas] * radeff[gas] / radeff['CFC-12'])

# %% cell 27
pfc_hfc134a_eq_2011 = 0
for gas in gases_pfc:
    pfc_hfc134a_eq_2011 = pfc_hfc134a_eq_2011 + (ghg_obs.loc[2011, gas] * radeff[gas] / radeff['CF4'])
hfc_hfc134a_eq_2011 = 0
for gas in gases_hfcs:
    hfc_hfc134a_eq_2011 = hfc_hfc134a_eq_2011 + (ghg_obs.loc[2011, gas] * radeff[gas] / radeff['HFC-134a'])
montreal_cfc12_eq_2011 = 0
for gas in gases_montreal:
    montreal_cfc12_eq_2011 = montreal_cfc12_eq_2011 + (ghg_obs.loc[2011, gas] * radeff[gas] / radeff['CFC-12'])

# %% cell 28
pfc_hfc134a_eq_1850 = 0
for gas in gases_pfc:
    pfc_hfc134a_eq_1850 = pfc_hfc134a_eq_1850 + (ghg_obs.loc[1850, gas] * radeff[gas] / radeff['CF4'])
hfc_hfc134a_eq_1850 = 0
for gas in gases_hfcs:
    hfc_hfc134a_eq_1850 = hfc_hfc134a_eq_1850 + (ghg_obs.loc[1850, gas] * radeff[gas] / radeff['HFC-134a'])
montreal_cfc12_eq_1850 = 0
for gas in gases_montreal:
    montreal_cfc12_eq_1850 = montreal_cfc12_eq_1850 + (ghg_obs.loc[1850, gas] * radeff[gas] / radeff['CFC-12'])

# %% cell 29
pfc_hfc134a_eq_1750 = 0
for gas in gases_pfc:
    pfc_hfc134a_eq_1750 = pfc_hfc134a_eq_1750 + (ghg_obs.loc[1750, gas] * radeff[gas] / radeff['CF4'])
hfc_hfc134a_eq_1750 = 0
for gas in gases_hfcs:
    hfc_hfc134a_eq_1750 = hfc_hfc134a_eq_1750 + (ghg_obs.loc[1750, gas] * radeff[gas] / radeff['HFC-134a'])
montreal_cfc12_eq_1750 = 0
for gas in gases_montreal:
    montreal_cfc12_eq_1750 = montreal_cfc12_eq_1750 + (ghg_obs.loc[1750, gas] * radeff[gas] / radeff['CFC-12'])

# %% cell 30
print(pfc_hfc134a_eq_2019, hfc_hfc134a_eq_2019, montreal_cfc12_eq_2019)
print(pfc_hfc134a_eq_2011, hfc_hfc134a_eq_2011, montreal_cfc12_eq_2011)
print(pfc_hfc134a_eq_1850, hfc_hfc134a_eq_1850, montreal_cfc12_eq_1850)
print(pfc_hfc134a_eq_1750, hfc_hfc134a_eq_1750, montreal_cfc12_eq_1750)

# %% cell 31
print(ghg_obs.loc[2019, 'SF6'], ghg_obs.loc[2011, 'SF6'], ghg_obs.loc[1750, 'SF6'])

# %% cell 32
print(ghg_obs.loc[2019, 'NF3'], ghg_obs.loc[2011, 'NF3'], ghg_obs.loc[1750, 'NF3'])

# %% cell 33
print(ghg_obs.loc[2019, 'CO2'], ghg_obs.loc[2011, 'CO2'], ghg_obs.loc[1850, 'CO2'], ghg_obs.loc[1750, 'CO2'])
print(ghg_obs.loc[2019, 'CH4'], ghg_obs.loc[2011, 'CH4'], ghg_obs.loc[1850, 'CH4'], ghg_obs.loc[1750, 'CH4'])
print(ghg_obs.loc[2019, 'N2O'], ghg_obs.loc[2011, 'N2O'], ghg_obs.loc[1850, 'N2O'], ghg_obs.loc[1750, 'N2O'])
