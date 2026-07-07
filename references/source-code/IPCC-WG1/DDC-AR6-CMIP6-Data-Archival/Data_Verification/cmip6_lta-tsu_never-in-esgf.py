# Code-only export from IPCC-WG1 notebook.
# Source: DDC-AR6-CMIP6-Data-Archival/Data_Verification/cmip6_lta-tsu_never-in-esgf.ipynb

# %% cell 2
import json
import pandas as pd
import tqdm
import uuid
with open("cmip6_list_2022-07-11.json") as f:
    cmip6_list=json.load(f)

# %% cell 3
cmip6_requested_drs_list_idx=[]
cmip6_requested_drs_list=[]
cmip6_requested_pids_list=[]
for dset in cmip6_list[0]:
    cmip6_requested_drs_list_idx.append(tuple(dset["data_ref_syntax"].split('.')[1:]))
    cmip6_requested_drs_list.append('.'.join(dset["data_ref_syntax"].split('.')[1:]))
    cmip6_requested_pids_list.append(dset["tracking_id_nc"])

# %% cell 4
len(cmip6_requested_pids_list)

# %% cell 5
from pyhandle.handleclient import PyHandleClient
client = PyHandleClient('rest')

# %% cell 6
pids_not_solvable={}
pids_no_url_orig_data={}
pids_not_available=[]
created_pids={}
drs_wrong=[]
new_drs={}
li=0
for pids,drs in tqdm.tqdm(zip(cmip6_requested_pids_list, cmip6_requested_drs_list),total=len(cmip6_requested_drs_list)):
    check_drs='CMIP6.'+drs
    pid_drs='CMIP6.'+'.'.join(drs.split('.')[:-1])+".v"+drs.split('.')[-1]
        #if check_drs not in cmip6_notinpool_notinesgf :
        #continue
    if not pids :
        pids_not_available.append(drs)
        uuid_ds = str(uuid.uuid3(uuid.NAMESPACE_URL, pid_drs))
        pids = ['21.14100/'+uuid_ds ]
        if not client.retrieve_handle_record(pids[0]):
            drs_wrong.append(pid_drs)
            continue
        else:
            created_pids[drs]=pids[0]
#        continue
    else:
        if not client.retrieve_handle_record(pids[0]):
            pids_not_solvable[drs]=pids[0]        
            continue
    try:
        url_orig_data=client.retrieve_handle_record(pids[0])["URL_ORIGINAL_DATA"]
        if check_drs in cmip6_notinpool_notinesgf:
            pid_drs='.'.join(url_orig_data.split('CMIP6')[1].split('/')[1:9])+'.'+url_orig_data.split('CMIP6')[1].split('/')[9].split('v')[1]
            print(pid_drs)
            if pid_drs != check_drs:
                new_drs[drs]=pid_drs
    except:
        pids_no_url_orig_data[drs]=pids[0]

# %% cell 7
drs_wrong=['.'.join(k.split('.')[0:-1])+'.'+k.split('.')[-1].split('v')[1] for k in drs_wrong]

# %% cell 8
drs_wrong

# %% cell 9
with open ("cmip6_list_data_ref_syntax_wrong-drs-by-pids.txt", 'w') as f:
    f.write("data_ref_syntax\n")
    for dset in drs_wrong :
        #f.write
        f.write('.'.join(dset.split('.')[1:])+"\n")

# %% cell 10
len(drs_wrong)
