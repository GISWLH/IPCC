# Code-only export from IPCC-WG1 notebook.
# Source: DDC-AR6-CMIP6-Data-Archival/Data_Verification/cmip6_lta-tsu_finalize.ipynb

# %% cell 1
import json
import os
with open("cmip6_list_2022-07-11.json") as f1:
    tsul=json.load(f1)
with open("cmip6_list_data_ref_syntax_drs-candidates-by-version_2022-08-17.json") as f2:
    updl=json.load(f2)

# %% cell 2
len(tsul[0])

# %% cell 3
li=1
lk=1
for k in updl.keys():
    vers=updl[k]
    versk=vers.split(',')  
    ejson=next((x for x in tsul[0] if x['data_ref_syntax'] == 'CMIP6.'+k), None)
    if ejson!=None:
        li=1;
        for v in versk:
            if li==1:  
                ejson['data_ref_syntax']='CMIP6.'+v
                #print(li,k,',',ejson['data_ref_syntax'])
            else:
                ejson2=ejson.copy()
                ejson2['data_ref_syntax']='CMIP6.'+v
                #print(li,ejson2)
                tsul[0].append(ejson2)
            li=li+1

# %% cell 4
len(tsul[0])

# %% cell 5
with open("cmip6_list_2022-08-17.json", 'w') as f:
    json.dump(tsul,f,indent=4, sort_keys=False)
