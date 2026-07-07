# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-11/code/gather_data_tabels.ipynb

# %% cell 2
import glob

import data_tables
import pandas as pd

import conf

# %% cell 4
name = ("Figure_11.3_TXx_scaling", "Figure_11.3_TXx_scaling", "data_tables")
fN = conf.cmip6.figure_filename(*name, add_prefix=False)

fNs = glob.glob(fN + "_md_raw")
data_tables.save_cmip6_info_post(fNs, fN_out=fN + "_md_cmip6.txt")

# %% cell 6
name = "TXx_at_w_simple_hatch", "Figure_11.11_TXx_map", "data_tables"
fN = conf.cmip6.figure_filename(*name)
fNs = glob.glob(fN + "_*_md_raw")

name = "TNn_at_w_simple_hatch", "Figure_11.11_TNn_map", "data_tables"
fN = conf.cmip6.figure_filename(*name)
fNs += glob.glob(fN + "_*_md_raw")

print(len(fNs))

name = ("Figure_11.11_TXx_TNn", "Figure_11.11_TXx_TNn_combined", "data_tables")
fN = conf.cmip6.figure_filename(*name, add_prefix=False)
data_tables.save_cmip6_info_post(fNs, fN_out=fN + "_md_cmip6.txt")

# %% cell 8
name = "Figure_11.16_Rx1day_at_w_simple", "Figure_11.16_Rx1day_map", "data_tables"
fN = conf.cmip6.figure_filename(*name, add_prefix=False)
fNs = glob.glob(fN + "_*_md_raw")

print(len(fNs))
data_tables.save_cmip6_info_post(fNs, fN_out=fN + "_md_cmip6.txt")

# %% cell 10
name = (
    "Figure_11.18ab_SMDroughtIndex_dpr_intensity_frequency",
    "Figure_11.18_SM_drought_dpr",
    "data_tables",
)
fN = conf.cmip6.figure_filename(*name, add_prefix=False)
fNs = glob.glob(fN + "_all_md_raw")

print(len(fNs))
data_tables.save_cmip6_info_post(fNs, fN_out=fN + "_md_cmip6.txt")

# %% cell 12
fN = conf.cmip6.figure_filename("CDD_at_w_simple", "Figure_11.19_CDD_map", "data_tables")
fNs = glob.glob(fN + "_*_md_raw")

fN = conf.cmip6.figure_filename("SM_tot_at_w_norm_simple_hatch", "Figure_11.19_SM_map", "data_tables")
fNs += glob.glob(fN + "_*_md_raw")

fN = conf.cmip6.figure_filename(
    f"sm_drought_frequency_JJA_wrt_1850_1900", "Figure_11.19_SM_drought_map", "data_tables"
)
fNs += glob.glob(fN + "_*_md_raw")

fN = conf.cmip6.figure_filename(
    f"sm_drought_frequency_DJF_wrt_1850_1900", "Figure_11.19_SM_drought_map", "data_tables"
)
fNs += glob.glob(fN + "_*_md_raw")

print(len(fNs))
fN = conf.cmip6.figure_filename(
    "Figure_11.19_CDD_SM", "Figure_11.19_CDD_SM_combined", "data_tables", add_prefix=False
)
data_tables.save_cmip6_info_post(fNs, fN_out=fN + "_md_cmip6.txt")

# %% cell 14
name = "FAQ_11.1_Figure_1_mean_vs_extreme", "FAQ_11.1_Figure_1", "data_tables"
fN = conf.cmip6.figure_filename(*name, add_prefix=False)
fNs = glob.glob(fN + "_*_md_raw")

print(len(fNs))
data_tables.save_cmip6_info_post(fNs, fN_out=fN + "_md_cmip6.txt")

# %% cell 16
fN = "../../cmip_temperatures/temperatures/cmip5/data_tables/cmip5_temperatures_one_ens_1850_1900"

fNs = glob.glob(fN + "_rcp*_md_raw")
print(len(fNs))
data_tables.save_cmip5_info_post(fNs, fN_out=fN + "_md_cmip5.txt")

# %% cell 18
fN = conf.cmip6.figure_filename(
    "SM_tot_time_ave", "Figure_12.4_S12.4_SM_data_tables", "data_tables"
)

fNs = glob.glob(fN + "_*_md_raw")
print(len(fNs))
data_tables.save_cmip6_info_post(fNs, fN_out=fN + "_md.txt")

# %% cell 19
fN = conf.cmip6.figure_filename(
    "SM_tot_at_w", "Figure_12.4_S12.4_SM_data_tables", "data_tables"
)

fNs = glob.glob(fN + "_*_md_raw")
print(len(fNs))
data_tables.save_cmip6_info_post(fNs, fN_out=fN + "_md.txt")

# %% cell 21
FIGURE_FOLDER = "Figure_11.SM.1_TNn_scaling"

fN = conf.cmip6.figure_filename(
    "Figure_11.A.1_TNn_scaling", FIGURE_FOLDER, "data_tables", add_prefix=False
)

fNs = glob.glob(fN + "_md_raw")
print(len(fNs))
data_tables.save_cmip6_info_post(fNs, fN_out=fN + "_md_cmip6.txt")
