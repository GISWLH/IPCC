# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-7/notebooks/010_chapter7_test_twolayermodel.ipynb

# %% cell 2
from ar6.twolayermodel import TwoLayerModel
import numpy as np
import matplotlib.pyplot as pl
from tqdm import tqdm

# %% cell 3
for i in tqdm(range(1000)):   # 5x as fast as fair, 10x as fast as openscm-runner
    scm = TwoLayerModel(
        extforce=4.0*np.ones(270),
        exttime=np.arange(270),
        tbeg=1750,
        tend=2020,
        lamg=4.0/3.0,
        t2x=None,
        eff=1.29,
        cmix=6,
        cdeep=75,
        gamma_2l=0.7,
    
        outtime=np.arange(1750.5,2020),
        dt=1
    )
    out = scm.run()

# %% cell 4
pl.plot(out.time, out.tg)
