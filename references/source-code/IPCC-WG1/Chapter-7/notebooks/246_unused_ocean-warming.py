# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/246_unused_ocean-warming.ipynb

# %% cell 2
from ar6.utils.h5 import *
import numpy as np
import matplotlib.pyplot as pl
import pandas as pd

# %% cell 3
results = load_dict_from_hdf5('../data_output_large/chapter9/twolayer_historical-AR6.h5')

# %% cell 4
results['historical-AR6'].keys()

# %% cell 5
pl.plot(results['historical-AR6']['deep_ocean_temperature']);

# %% cell 6
tocean2015 = results['historical-AR6']['deep_ocean_temperature'][260:270, :].mean(axis=0) - results['historical-AR6']['deep_ocean_temperature'][100:151, :].mean(axis=0)

# %% cell 7
pl.hist(tocean2015)

# %% cell 8
print(np.mean(tocean2015))
print(np.median(tocean2015))

# %% cell 9
df = pd.DataFrame(tocean2015, columns=['deep_ocean_warming_2015'])

# %% cell 10
df.to_csv('../data_output/tlm_lower_layer_warming_2015v1850-1900.csv', index=False)
