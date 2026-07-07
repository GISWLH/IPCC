# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/155_WG3_double-check-unconstrained-forcing.ipynb

# %% cell 2
import matplotlib.pyplot as pl
import numpy as np

# %% cell 3
F_dir = np.load('../data_output_large/fair-samples/F_ERFari_unconstrained.npy')
F_ind = np.load('../data_output_large/fair-samples/F_ERFaci_unconstrained.npy')

# %% cell 4
F_dir.shape

# %% cell 5
pl.fill_between(np.arange(1750,2101), np.percentile(F_dir, 5, axis=1), np.percentile(F_dir, 95, axis=1))
pl.plot(np.arange(1750,2101), np.percentile(F_dir, 50, axis=1), color='k');
pl.plot(np.arange(2005,2015), -0.3*np.ones(10), color='r')
pl.grid()

# %% cell 6
pl.fill_between(np.arange(1750,2101), np.percentile(F_ind, 5, axis=1), np.percentile(F_ind, 95, axis=1))
pl.plot(np.arange(1750,2101), np.percentile(F_ind, 50, axis=1), color='k');
pl.plot(np.arange(2005,2015), -1.0*np.ones(10), color='r')
pl.grid()
