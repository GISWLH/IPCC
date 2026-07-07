# Code-only export from IPCC-WG1 notebook.
# Source: DDC-AR6-CMIP6-Data-Archival/Data_Verification/cmip6_lta-tsu_sanitize.ipynb

# %% cell 2
import json
import pandas as pd
wrong_drs=pd.read_csv("cmip6_list_data_ref_syntax_wrong-drs-by-pids.txt")

# %% cell 3
drs_keys=['activity_id', 'institution_id', 'source_id', 'experiment_id', 'member_id', 'table_id', 'variable_id', 'grid_label', 'version']
drs_keys_noversion=['activity_id', 'institution_id', 'source_id', 'experiment_id', 'member_id', 'table_id', 'variable_id', 'grid_label']

# %% cell 4
wrong_drs=pd.DataFrame([k.split('.') for k in wrong_drs["data_ref_syntax"]], columns=drs_keys)

# %% cell 6
sort_out=wrong_drs[(wrong_drs["variable_id"].str.contains("\?")) |
          (wrong_drs["variable_id"]=='')]
sort_out.agg('.'.join,axis=1).to_csv("cmip6_list_data_ref_syntax_sortout-varwrong.txt", index=False)

# %% cell 7
wrong_drs=wrong_drs[~wrong_drs.index.isin(sort_out.index)]

# %% cell 9
duplicates=wrong_drs[wrong_drs[drs_keys_noversion].duplicated(keep=False)]
len(duplicates)
duplicates[drs_keys]

# %% cell 10
duplicates[drs_keys].agg('.'.join,axis=1).to_csv(
    "cmip6_list_data_ref_syntax_sortout-versionduplicated.txt", index=False)

# %% cell 12
#wrong_drs=wrong_drs[~wrong_drs[drs_keys_noversion].duplicated()]

# %% cell 14
wrong_drs

# %% cell 15
import intake
cmip6_col = intake.open_esm_datastore("https://gitlab.dkrz.de/data-infrastructure-services/intake-esm/-/raw/master/esm-collections/cloud-access/dkrz_cmip6_disk.json")
cmip6_col.df.head()

# %% cell 16
cmip6_cat=cmip6_col.df[drs_keys]
#df is the dataframe under the catalog
#each dataset consists of many files. by keeping only one we get the list of datasets:
cmip6_cat=cmip6_col.df[drs_keys].drop_duplicates(keep="first").reindex()

# %% cell 18
wrong_drs_idx=wrong_drs.set_index(drs_keys_noversion).index
cmip6_cat_idx=cmip6_cat.set_index(drs_keys_noversion).index

# %% cell 19
cat_candidates_version=cmip6_cat[cmip6_cat_idx.isin(wrong_drs_idx)]

# %% cell 21
cat_candidates_version

# %% cell 22
cat_candidates_version_idx=cat_candidates_version.set_index(drs_keys_noversion).index

# %% cell 23
wrong_drs_candidates_version=wrong_drs[wrong_drs_idx.isin(cat_candidates_version_idx)].reset_index(drop=True)

# %% cell 24
wrong_drs_candidates_version_idx=wrong_drs_candidates_version.set_index(drs_keys_noversion).index

# %% cell 26
wrong_drs_candidates_version.loc[:,"data_ref_syntax"]=wrong_drs_candidates_version.agg('.'.join,axis=1)
cat_candidates_version.loc[:,"data_ref_syntax"]=cat_candidates_version[drs_keys].agg('.'.join,axis=1)

# %% cell 27
for row,idx in enumerate(wrong_drs_candidates_version_idx) :
    wrong_drs_candidates_version.loc[row,"candidate"]=','.join(cat_candidates_version.set_index(drs_keys_noversion).loc[idx,"data_ref_syntax"].values)

# %% cell 28
wrong_drs_candidates_version_dict={}
for i,row in wrong_drs_candidates_version[["data_ref_syntax","candidate"]].iterrows():
    wrong_drs_candidates_version_dict[row["data_ref_syntax"]]=row["candidate"]

# %% cell 29
with open("cmip6_list_data_ref_syntax_drs-candidates-by-version.json", 'w') as f:
    json.dump(wrong_drs_candidates_version_dict,f,indent=4, sort_keys=True)

# %% cell 31
wrong_drs=wrong_drs[~wrong_drs_idx.isin(wrong_drs_candidates_version_idx)]
wrong_drs.agg('.'.join,axis=1).to_csv("cmip6_list_data_ref_syntax_sortout-notfound.txt", index=False)
