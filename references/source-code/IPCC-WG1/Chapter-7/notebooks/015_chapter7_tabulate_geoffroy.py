# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/015_chapter7_tabulate_geoffroy.ipynb

# %% cell 2
import json
import pandas as pd
import numpy as np

# %% cell 3
with open('../data_input/tunings/cmip6_twolayer_tuning_params.json') as file:
    geoff = json.load(file)

# %% cell 4
geoff.keys()

# %% cell 5
data_dict = {}
for key in geoff.keys():
    data_dict[key] = geoff[key]['model_data']['EBM-epsilon']

df = pd.DataFrame(data_dict)

# %% cell 6
df['kappa'] = df['eff'] * df['gamma_2l']

# %% cell 7
def _calculate_geoffroy_helper_parameters(
    cmix, cdeep, lambda0, efficacy, eta
):

    b_pt1 = (lambda0 + efficacy * eta) / cmix
    b_pt2 = eta / cdeep
    b = b_pt1 + b_pt2
    b_star = b_pt1 - b_pt2
    delta = b ** 2 - (4 * lambda0 * eta) / (cmix * cdeep)

    taucoeff = cmix * cdeep / (2 * lambda0 * eta)
    d1 = taucoeff * (b - delta ** 0.5)
    d2 = taucoeff * (b + delta ** 0.5)

    phicoeff = cmix / (2 * efficacy * eta)
    phi1 = phicoeff * (b_star - delta ** 0.5)
    phi2 = phicoeff * (b_star + delta ** 0.5)

    adenom = cmix * (phi2 - phi1)
    a1 = d1 * phi2 * lambda0 / adenom
    a2 = -d2 * phi1 * lambda0 / adenom

    qdenom = cmix * (phi2 - phi1)
    q1 = d1 * phi2 / qdenom
    q2 = -d2 * phi1 / qdenom

    out = {
        "d1": d1,
        "d2": d2,
        "q1": q1,
        "q2": q2,
        "efficacy": efficacy,
        "a1": a1,
        "a2": a2
    }
    return out

# %% cell 8
output = []
for i, row in df.iterrows():
    gh = _calculate_geoffroy_helper_parameters(df.loc[i,'cmix'], df.loc[i,'cdeep'], -df.loc[i,'lamg'], df.loc[i,'eff'], df.loc[i,'gamma_2l'])
    output.append([gh['d1'], gh['d2'], gh['a1'], gh['a2']])
df_a = pd.DataFrame(output, columns=['tau1', 'tau2', 'a1', 'a2'], index=df.index)
df_a

# %% cell 9
df

# %% cell 10
df = pd.concat([df, df_a], axis=1)

# %% cell 11
mean = df.mean()
mean.name = 'Mean'
df = df.append(mean)

# %% cell 12
std = df.std()
std.name = 'StDev'
df = df.append(std)

# %% cell 13
df.to_csv('../data_output/cmip6_twolayer_tuning_params.csv')

# %% cell 14
df

# %% cell 17
def geoff_eq14(f2x, lam, t, tau_f, a_f, tau_s, a_s):
    #return -f2x/lam + f2x / t / lam * tau_f * a_f * (1 - np.exp(-t/tau_f)) + f2x / t / lam * tau_s * a_s * (1 - np.exp(-t/tau_s))
    ecs = -f2x/lam
    
    return ecs * (1 - 1/t * (tau_f * a_f * (1 - np.exp(-t/tau_f)) + tau_s * a_s * (1 - np.exp(-t/tau_s))))

# %% cell 18
# TCR for F2x = 3.9 and CMIP6 mean tunings
geoff_eq14(f2x=3.9, lam=-1.06, t=70, tau_f=4.6, a_f=0.54, tau_s=333, a_s=0.46)
