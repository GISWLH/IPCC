# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-6_Fig12_22_24/ar6_ch6_rcmipfigs/notebooks/convert2badc_csv/convert2badc_csv.ipynb

# %% cell 1
from ar6_ch6_rcmipfigs.utils.badc_csv import redo_SSPs_to_badc_csv, write_badc_header, make_badc_csvs_for_slcf_warming_ranges

# %% cell 2
from pathlib import Path

# %% cell 3
from ar6_ch6_rcmipfigs.constants import BASE_DIR

# %% cell 4
path_in =  Path(BASE_DIR) / 'data_in/SSPs/'
path_out =  Path(BASE_DIR) / 'data_in_badc_csv/SSPs/'
redo_SSPs_to_badc_csv(path_in, path_out)

# %% cell 5
make_badc_csvs_for_slcf_warming_ranges()

# %% cell 6
from ar6_ch6_rcmipfigs.utils.badc_csv import path_FaIR_hist_header_general_info

# %% cell 7
# %%
## Write AR6 files:
fp_orig = BASE_DIR /'data_in/AR6_ERF_1750-2019.csv'
fp_out =  BASE_DIR /'data_in_badc_csv/AR6_ERF_1750-2019.csv'
path_header = path_FaIR_hist_header_general_info
add_global_info = [['comments','G',f'Time period: 1750-2019'],]
#
# %%

write_badc_header(
    fp_orig,
    fp_out,
    add_global_info,
    #variable_dic,
    #read_csv_kwargs=None,
    fp_global_default = path_header,
    fp_var_default = path_header
)
# %%
fp_orig = BASE_DIR /'data_in/AR6_ERF_minorGHGs_1750-2019.csv'
fp_out =  BASE_DIR /'data_in_badc_csv/AR6_ERF_minorGHGs_1750-2019.csv'
#

write_badc_header(
    fp_orig,
    fp_out,
    add_global_info,
    #variable_dic,
    #read_csv_kwargs=None,
    fp_global_default = path_header,
    fp_var_default = path_header
)
