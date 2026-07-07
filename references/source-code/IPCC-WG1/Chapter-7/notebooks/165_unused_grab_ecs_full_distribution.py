# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/165_unused_grab_ecs_full_distribution.ipynb

# %% cell 2
import json

import numpy as np
import matplotlib.pyplot as pl
import pandas as pd
import scipy.stats as st

# %% cell 3
ecs = np.load('../data_input_large/fair-samples/ecs_unconstrained.npy')
accept_inds = np.loadtxt('../data_output_large/fair-samples/accept_inds.csv').astype(int)

# %% cell 4
ecs[accept_inds]

# %% cell 5
pl.hist(ecs[accept_inds], bins=np.arange(1.6,12.0,0.2), density=True, alpha=0.5);
pl.hist(ecs[accept_inds][:600], bins=np.arange(1.6,12.0,0.2), density=True, alpha=0.5);

# %% cell 6
np.savetxt('../data_output_large/fair-samples/ecs.csv', ecs[accept_inds], fmt='%f')

# %% cell 7
with open('../data_input/random_seeds.json', 'r') as filehandle:
    SEEDS = json.load(filehandle)

# %% cell 8
SAMPLES=1000000

# %% cell 9
with open("../data_input/tunings/cmip6_twolayer_tuning_params.json", "r") as read_file:
    params = json.load(read_file)
cmip6_models = list(params['q4x']['model_data']['EBM-epsilon'].keys())
cmip6_models
NMODELS = len(cmip6_models)

geoff_data = np.zeros((NMODELS, 6))
for im, model in enumerate(cmip6_models):
    geoff_data[im,0] = params['q4x']['model_data']['EBM-epsilon'][model]
    geoff_data[im,1] = params['lamg']['model_data']['EBM-epsilon'][model]
    geoff_data[im,2] = params['cmix']['model_data']['EBM-epsilon'][model]
    geoff_data[im,3] = params['cdeep']['model_data']['EBM-epsilon'][model]
    geoff_data[im,4] = params['gamma_2l']['model_data']['EBM-epsilon'][model]
    geoff_data[im,5] = params['eff']['model_data']['EBM-epsilon'][model]

geoff_df = pd.DataFrame(geoff_data, columns=['q4x','lamg','cmix','cdeep','gamma_2l','eff'], index=cmip6_models)
kde = st.gaussian_kde(geoff_df.T)
geoff_sample = kde.resample(size=int(SAMPLES*1.25), seed = SEEDS[15])

# remove unphysical combinations
geoff_sample[:,geoff_sample[0,:] <= 0] = np.nan
#geoff_sample[:,geoff_sample[1,:] >= -0.6] = np.nan
geoff_sample[1, :] = st.truncnorm.rvs(-2, 2, loc=-4/3, scale=0.5, size=int(SAMPLES*1.25), random_state=SEEDS[16])
geoff_sample[:,geoff_sample[2,:] <= 0] = np.nan
geoff_sample[:,geoff_sample[3,:] <= 0] = np.nan
geoff_sample[:,geoff_sample[4,:] <= 0] = np.nan
geoff_sample[:,geoff_sample[5,:] <= 0] = np.nan

mask = np.all(np.isnan(geoff_sample), axis=0)
geoff_sample = geoff_sample[:,~mask][:,:SAMPLES]
geoff_sample_df=pd.DataFrame(data=geoff_sample.T, columns=['q4x','lamg','cmix','cdeep','gamma_2l','eff']).loc[accept_inds]
geoff_sample_df.to_csv('../data_output/geoff_sample_constrained.csv')
geoff_sample_df
