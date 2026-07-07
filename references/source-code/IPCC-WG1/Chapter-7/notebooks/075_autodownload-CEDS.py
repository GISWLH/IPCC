# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/075_autodownload-CEDS.ipynb

# %% cell 2
from ar6.utils import check_and_download, mkdir_p
import zipfile
import os

# %% cell 3
mkdir_p('../data_input_large/')

# %% cell 4
check_and_download('../data_input_large/CEDS_v_2020_09_11_emissions.zip', "https://zenodo.org/record/4025316/files/CEDS_v_2020_09_11_emissions.zip")

# %% cell 5
with zipfile.ZipFile('../data_input_large/CEDS_v_2020_09_11_emissions.zip', 'r') as zip_ref:
    zip_ref.extractall('../data_input_large/CEDS_v_2020_09_11_emissions/')

# %% cell 6
os.remove('../data_input_large/CEDS_v_2020_09_11_emissions.zip')
