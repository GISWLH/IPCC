# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/340_chapter7_table7.SM.7.ipynb

# %% cell 2
import pandas as pd
import numpy as np
import copy
import urllib
from urllib.error import HTTPError
import time

from ar6.utils.numerical import significance

pd.set_option('display.max_rows', None)

# %% cell 3
df_supp = pd.read_csv('../data_input/ghg_properties/metrics_supplement.csv')

# %% cell 4
#df_supp.index.name = "Name"

# %% cell 5
# strip whitespace and hashes
df = df_supp.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df = df.apply(lambda x: x.str.strip('#') if x.dtype == "object" else x)

# %% cell 6
# replace "nan" with np.nan
df.replace(to_replace="nan", value=np.nan, inplace=True)

# %% cell 7
df

# %% cell 8
# fill in REs
df.loc[0, 'Radiative_efficiency'] = 1.33E-05
df.loc[1, 'Radiative_efficiency'] = 0.000388
df.loc[2, 'Radiative_efficiency'] = 0.0032

# resolve typos and omissions in CASRN
df.loc[71, 'CASRN'] = '29118-24-9'
df.loc[73, 'CASRN'] = '66711-86-2'
df.loc[182, 'CASRN'] = '163702-05-4'

# consistency with acronyms
df.loc[76, 'Acronym'] = 'HFO-1345zfc'
df.loc[182, 'Acronym'] = 'HFE-569sf2'
df.loc[107, 'Acronym'] = 'Halon-2311'
df.loc[148, 'Acronym'] = 'HCFE-235ca2'
df.loc[149, 'Acronym'] = 'HCFE-235da2'
df.loc[150, 'Acronym'] = 'HFE-236ea2'   # This was erroneously HCFE-236ea2 in the first edition
df.loc[163, 'Acronym'] = 'HFE-347mmz1'
df.loc[164, 'Acronym'] = 'HFE-347mcc3'
df.loc[178, 'Acronym'] = 'HFE-43-10pccc124'
df.loc[179, 'Acronym'] = 'HFE-449s1'  # or "sl". Jury is out!
df.loc[186, 'Acronym'] = 'HFE-236ca12'
df.loc[187, 'Acronym'] = 'HFE-338pcc13'
df.loc[202, 'Acronym'] = 'PFPMIE'
df.loc[218, 'Acronym'] = ''
df.loc[225, 'Acronym'] = ''

# %% cell 9
df.rename(
    columns = {
        '# Name' : 'Name',
        'Radiative_efficiency' : 'Radiative efficiency (W m-2 ppb-1)',
        'Lifetime' : 'Lifetime (yr)',
        'CASRN': 'CAS',
        'AGWP20': 'AGWP20 (W m-2 yr kg-1)',
        'AGWP100': 'AGWP100 (W m-2 yr kg-1)',
        'AGWP500': 'AGWP500 (W m-2 yr kg-1)',
        'AGTP50': 'AGTP50 (K kg-1)',
        'AGTP100': 'AGTP100 (K kg-1)',
        'CGTP50': 'CGTP50 (yr)',
        'CGTP100': 'CGTP100 (yr)'
    },
    inplace=True
)
df

# %% cell 10
# get IUPAC names from API where they are truncated, ambigious, wrong, have colons instead of commas...
# easier to specifiy which compounds are correct

good_idx = [0,1,2,3,4,5,17,18,19,39,40,41,49,65,67,90,91,92,93,94,98,99,100,101,102,103,104,105,110,111,112,114,115,
            116,117,118,119,120,121,122,124,125,126,127,128,129,130,131,132,133,134,135,142,143,204,220,228,229,230,
            232,234,235,236,237,240,241,242,243,244,245,246,247,248]
    
# #iupac_list = []
for i, cas in enumerate(df['CAS']):
    if cas == '':
        continue
    if i not in good_idx:
        url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/property/IUPACName/TXT" % cas
        try:
            file = urllib.request.urlopen(url)
            for line in file:
                iupac_name = line.decode('utf-8').strip()
                break
            print(cas, iupac_name)
            df.loc[i, 'Name'] = iupac_name.capitalize()
        #    iupac_list.append(iupac_name)
        except HTTPError:
            print('\n*** no entry found for %s\n' % cas)
        time.sleep(0.25)  # web server requests no more than 5 requests per second
    else:
        df.loc[i, 'Name'] = df.loc[i, 'Name'].capitalize()

# %% cell 11
# all values to 3 SF
for col in ['Lifetime (yr)', 'Radiative efficiency (W m-2 ppb-1)', 'AGWP20 (W m-2 yr kg-1)', 'GWP20', 'AGWP100 (W m-2 yr kg-1)',
            'GWP100', 'AGWP500 (W m-2 yr kg-1)', 'GWP500', 'AGTP50 (K kg-1)', 'GTP50', 'AGTP100 (K kg-1)', 'GTP100',
            'CGTP50 (yr)', 'CGTP100 (yr)']:
    df.loc[:,col] = pd.to_numeric(df.loc[:,col])
    df.loc[df[col] == 0,col] = 0
    df.loc[df[col] > 0,col] = df.loc[df[col] > 0,col].apply(significance, args=(3,))

# %% cell 12
# stop excel interpreting CAS numbers as dates
for i, row in df.iterrows():
    df.loc[i,'CAS'] = '="'+df.loc[i,'CAS']+'"'

# %% cell 13
df

# %% cell 14
# hand-edit what's left
df.loc[87, 'Name'] = '1,3,3,4,4-pentafluorocyclobutene'
df.loc[160, 'Name'] = '1,1,1,2,2-pentafluoro-2-(1,1,2,2-tetrafluoroethoxy)ethane'
df.loc[165, 'Name'] = '1-(2,2-difluoroethoxy)-1,1,2,2,2-pentafluoroethane'
df.loc[170, 'Name'] = '1-(2,2-difluoroethoxy)-1,1,2,2-tetrafluoroethane'
df.loc[181, 'Name'] = '2-(difluoromethoxymethyl)-1,1,1,2,3,3,3-heptafluoropropane'
df.loc[190, 'Name'] = '1,1,3,3,4,4,6,6,7,7,9,9,10,10,12,12-hexadecafluoro-2,5,8,11-tetraoxadodecane'
df.loc[192, 'Name'] = '2-ethoxy-3,3,4,4,5-pentafluorotetrahydro-2,5-bis[1,2,2,2-tetrafluoro-1-(trifluoromethyl)ethyl]-furan'
df.loc[195, 'Name'] = '1,1,2,2-Tetrafluoro-1-methoxyethane'
df.loc[202, 'Name'] = '1‐(difluoro(trifluoromethoxy)methoxy)‐1,1,2,3,3,3‐hexafluoro‐2‐(trifluoromethoxy)propane'
df.loc[223, 'Name'] = ''

# %% cell 15
df.to_csv('../data_output/7sm/metrics_supplement_cleaned.csv', index=False)
