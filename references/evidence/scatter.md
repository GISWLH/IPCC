# scatter Evidence Pack

- Candidate skill: `ipcc-scatter-relationship`
- Matching chunks: 109
- Matching repositories: 14
- Matching files: 48

## Representative Sources

### 1. Atlas / `Atlas\datasets-aggregated-regionally\scripts\computeFigures.R`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `ed29da33d38ae767d19caafd4cde06042cbe00f4`
- Tags: `distribution, raster_stripes, scatter`

```text
# computeFigures.R # # Copyright (C) 2021 Santander Meteorology Group (http://meteo.unican.es) # # This work is licensed under a Creative Commons Attribution 4.0 International # License (CC BY 4.0 - http://creativecommons.org/licenses/by/4.0) #' @title Scatter and boxplots of temperature and precipitation changes #' @description Compute scatterplots and boxplots of temperature and precipitation changes from data #' files of this repository (datasets-aggregated-regionally). #' @details Functions computeDeltas (computeDeltas.R) and computeOffset (computeOffset.R) #' are internally used. #' @author M. Iturbide computeFigures <- function(regions, cordex.domain = NULL, area, ref.period, scatter.seasons, xlim = NULL, ylim = NULL) { library(lattice) library(latticeExtra) # select warming levels and list future periods, e.g. list(c(2021, 2040), c(2041, 2060), c(2081, 2100)) WL <- c("1.5", "2", "
```

### 2. Chapter-2_Fig12 / `Chapter-2_Fig12\vertical.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `beff84dd7a5e081eb6bfc07985b767a1881f3261`
- Tags: `color_style, scatter, uncertainty`

```text
# -*- coding: utf-8 -*- """ Author: Florian Ladstädter © Copyright 2021 [ Wegener Center && IGAM ] / UniGraz """ # Standard Library import logging import os import time from collections import Counter # Third party import click import matplotlib as mpl import matplotlib.pyplot as plt import numpy as np import pandas as pd import xarray as xr from matplotlib.ticker import FixedLocator, MultipleLocator, ScalarFormatter from scipy.interpolate import interp1d # First party import atmoplots.ipcc_colors as ipcc_colors from atmoplots.plotconfig import PlotConfig from atmoplots.pressure_mapping import pressure_mapping # Local imports from . import common logger = logging.getLogger(__name__) mpl.rcParams["hatch.color"] = "black" mpl.rcParams["hatch.linewidth"] = 0.1 mpl.rc("lines", markersize=3) # markersize scatterplots plot_style = { "ipcc": { "xtick.direction": "out", "ytick.direction": "out",
```

### 3. Chapter-3_Fig02b / `Chapter-3_Fig02b\ch03_fig2b_code.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `ee22b6221c6535f81a33c1b033a4183621df0b23`
- Tags: `multi_panel, scatter`

```text
# ch03_fig2b.py # Description # Generates Figure 3.2 panel b in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 3 # Creator: Anni Zhao (anni.zhao.16@ucl.ac.uk) # Creator: Chris Brierley (c.brierley@ucl.ac.uk) # Creation Date: 1 Mar 2021 # Import packages import matplotlib.pyplot as plt import numpy as np import pandas as pd import matplotlib # Define markers for CMIP indicidual models: markers = {'CMIP6':['o'], 'CMIP5':['x'], 'nonCMIP':['+']} # Define markers for CMIP multi-model means: avemarkers = {'CMIP6':['s'], 'CMIP5':['X'], 'nonCMIP':['P']} # Define colors for experiments: colors = {'LGM':['blue'], 'LIG':['lightblue'], 'MH':['lightsalmon'], 'mPWP':['red'], 'EECO':['darkred'], '1pctCO2':['limegreen'], 'abrupt4xCO2':['violet']} # Define experiment names expt_names = {'LGM':['Last Glacial Maximum'], 'LIG':['Last Inter Glacial'], 'MH':['mid-Holocene'], 'mP
```

### 4. Chapter-6_Fig12_22_24 / `Chapter-6_Fig12_22_24\ar6_ch6_rcmipfigs\notebooks\fig6_12_and_ts15_spm2\utils_hist_att\attribution_1750_2019_newBC_smb.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `cd6393f61459534bf60374c757e8af0f6f1553a7`
- Tags: `scatter`

```text
# CH4 forcing rfch4 = np.zeros(nspec) rfch4_sd = np.zeros(nspec) for ispec in np.arange(nspec): rfch4[ispec] = \ ch4_forcing_AR6(ch4[ispec], ch4_2014, n2o_2014) * \ (1 + ch4_ra) rfch4_sd[ispec] = \ ch4_forcing_AR6(ch4[ispec] + ch4_sd[ispec], ch4_2014, n2o_2014) * \ (1 + ch4_ra) - rfch4[ispec] # rfch4 due to ch4 is minus sum of non-ch4 terms # - ensures total sum of rfch4 changes is zero rfch4[i_ch4] = -np.sum(rfch4[i_non_ch4]) rfch4_sd[i_ch4] = np.sqrt(np.sum(np.square(rfch4_sd[[i_non_ch4]]))) # Add in 14% spectral uncertainty rfch4_sd = np.sqrt((rfch4 * 0.14) ** 2 + (rfch4_sd) ** 2) em_co2 = np.zeros(nspec) em_co2[[i_ch4, i_hc, i_voc]] = [6.6, 0.02, 26.] # From MAGICC input files # CH4 HC VOC, CO CO2 scalings applied of 75%, 100%, 50%, 100% # Assume 88% of CH4 emitted oxidised (12% remains as CH4) # Assume can attributed present day CO2 change by scaling cumulative emissions co2 = (em_c
```

### 5. Chapter-7 / `Chapter-7\contributed\faq7.3_fig1\Redo_Grose_figure.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `2f948c862dbc158182ba47b863395ec1a4aa7998`
- Tags: `color_style, multi_panel, scatter, time_series`

```text
import matplotlib.pyplot as plt from matplotlib.patches import Rectangle import numpy as np import pandas as pd from netCDF4 import Dataset import os.path df = pd.read_excel (r'ecs_for_faq.xlsx') dt = pd.read_excel (r'tcr_for_faq.xlsx') nCMIP5 = df[df['project'] == "CMIP5"]['dataset'].size nCMIP6 = df[df['project'] == "CMIP6"]['dataset'].size iCMIP5 = df['project'] == "CMIP5" iCMIP6 = df['project'] == "CMIP6" nTCR = dt[dt['project'] == "CMIP6"]['dataset'].size # CMIP5: for i in np.arange(nCMIP5): model = df[df['project'] == "CMIP5"]['dataset'][i] filename = "CMIP5_means/dtas_"+model+".nc" if os.path.isfile(filename): f = Dataset(filename, "r") df['dT'][i] = f.variables['tas'][0,0,0].data # g = Dataset("CMIP5_means/tas_"+model+"_rcp85.nc") # h = Dataset("CMIP5_means/tas_"+model+"_piControl.nc") # plt.figure() # plt.plot(g.variables['time'][:].data, g.variables['tas'][:,0,0].data) # plt.pl
```

### 6. Chapter-7_Fig10 / `Chapter-7_Fig10\AR6_fbk_violin_plot.py`

- Chunk type: `code`
- Language: ``
- Commit: `c1023c9d30eedab63e7399fc5a6e45738edecfec`
- Tags: `color_style, distribution, multi_panel, raster_stripes, scatter, time_series, uncertainty`

```text
# Code to generate the CMIP5, CMIP6, and AR6 assessed feedback "violin plot" import matplotlib.pyplot as plt import numpy as np import json # IPCC COLORBAR # https://github.com/IPCC-WG1/colormaps/blob/master/categorical_colors_rgb_0-255/rcp_cat.txt red = (153/255, 0/255, 2/255) orange = (196/255, 121/255, 0/255) lt_blue = (112/255, 160/255, 205/255) def legend_without_duplicate_labels(ax): handles, labels = ax.get_legend_handles_labels() unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]] ax.legend(*zip(*unique)) names4=['NET_fbk','PL_fbk','WVLR_fbk','ALB_fbk','CLD_fbk','resid_fbk'] ################################################################################## # AR6 expert-assessed values provided by Masa on 1/27/21: Masa_names = ['Net', 'Planck', 'WV+LR','Albedo','Cloud','Other'] AR6 = np.array([-1.16081, -3.22, 1.30, 0.35, 0.42, -0.01081]) AR6p
```

### 7. Chapter-9 / `Chapter-9\Functions\hatchfill2.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `79abd70a0c9db81573e6892967958c23ac2a311b`
- Tags: `raster_stripes, scatter, uncertainty`

```text
% Idea here appears to be to rotate everthing so lines will be % horizontal, and scaled so we go in integer steps in 'y' with % 'points' being the units in x. % Center it for "good behavior". % rotate first about (0,0) ca = cosd(angle); sa = sind(angle); u = [ca sa]*xydata; % Rotation v = [-sa ca]*xydata; % translate to the grid point nearest to the centroid u0 = round(mean(u)/step)*step; v0 = round(mean(v)/step)*step; x = (u-u0); y = (v-v0)/step+offset; % plus scaling and offsetting % Compute the coordinates of the hatch line ............... yi = ceil(y); yd = [diff(yi) 0]; % when diff~=0 we are crossing an integer fnd = find(yd); % indices of crossings dm = max(abs(yd)); % max possible #of integers between points % This is going to be pretty space-inefficient if the line segments % going in have very different lengths. We have one column per line % interval and one row per hatch line w
```

### 8. PMIP_for_AR6_Interactive_Atlas / `PMIP_for_AR6_Interactive_Atlas\figures\AR6WG1_Fig3.2b\ch03_fig2b_code.py`

- Chunk type: `code`
- Language: `NCL`
- Commit: `3c30218f5db1eac2bfc3f66066f90253f3a2fcb1`
- Tags: `multi_panel, scatter`

```text
# ch03_fig2b.py # Description # Generates Figure 3.2 panel b in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 3 # Creator: Anni Zhao (anni.zhao.16@ucl.ac.uk) # Creator: Chris Brierley (c.brierley@ucl.ac.uk) # Creation Date: 1 Mar 2021 # Import packages import matplotlib.pyplot as plt import numpy as np import pandas as pd import matplotlib # Define markers for CMIP indicidual models: markers = {'CMIP6':['o'], 'CMIP5':['x'], 'nonCMIP':['+']} # Define markers for CMIP multi-model means: avemarkers = {'CMIP6':['s'], 'CMIP5':['X'], 'nonCMIP':['P']} # Define colors for experiments: colors = {'LGM':['blue'], 'LIG':['lightblue'], 'MH':['lightsalmon'], 'mPWP':['red'], 'EECO':['darkred'], '1pctCO2':['limegreen'], 'abrupt4xCO2':['violet']} # Define experiment names expt_names = {'LGM':['Last Glacial Maximum'], 'LIG':['Last Inter Glacial'], 'MH':['mid-Holocene'], 'mP
```

### 9. PMIP_for_AR6_Interactive_Atlas / `PMIP_for_AR6_Interactive_Atlas\figures\AR6WG1_Fig3.2b\ch03_fig2b_code.py`

- Chunk type: `code`
- Language: `NCL`
- Commit: `3c30218f5db1eac2bfc3f66066f90253f3a2fcb1`
- Tags: `bar_hist_density, scatter, uncertainty`

```text
def ch03_fig2b_function4(expt): # load data # Define the filename according to the input exoeriment name fname = 'fig3.2b_%s_CMIP6_ensemble_mean.csv' %expt DATA = pd.read_csv(fname,header=18) Tsea = np.array(DATA['1'][0:len(DATA['1'])-1]).astype(float) Tland = np.array(DATA['2'][0:len(DATA['1'])-1]).astype(float) fig = plt.scatter(Tsea,Tland,marker="s",s=75,color=colors[expt][0],linewidths=1,facecolors='none',edgecolors=colors[expt][0],label=expt) return fig # Function that loads and plots the ensemble mean of land and ocean temperature contrast in the CMIP5 # Syntax # [output] = ch03_fig2b_function5(input) # Input arguments # input - experiment name # Output argument # output - Plots the right CMIP5 data point in right color and marker according to the experiment name def ch03_fig2b_function5(expt): # load data # Define the filename according to the input exoeriment name fname = 'fig3.2
```

### 10. PMIP_for_AR6_Interactive_Atlas / `PMIP_for_AR6_Interactive_Atlas\figures\AR6WG1_Fig3.2b\ch03_fig2b_code.py`

- Chunk type: `code`
- Language: `NCL`
- Commit: `3c30218f5db1eac2bfc3f66066f90253f3a2fcb1`
- Tags: `color_style, multi_panel, scatter, time_series`

```text
# Plot the panel b in figure 2 in chapter 3 # Set figure size to 9cm x 12cm # Change the size unit from cm to inch by deviding 2.54 plt.figure(figsize=(9/2.54,12/2.54)) ax = plt.subplot(111) # Setups # Set title plt.title('b) Global temperature change over \nland and ocean for a range of climates',fontsize=9,pad=5,loc='left') # Set labels and ticks of axes plt.xlabel('Temperature change over sea (%sC)'%(chr(176)),fontsize=9) plt.ylabel('Temperature change over land (%sC)'%(chr(176)),fontsize=9) plt.xticks(fontsize=9) plt.yticks(fontsize=9) # Add grey dotted lines to indicate the zero levels plt.axvline(x=0,color='grey',linestyle="dotted",linewidth=0.5) plt.axhline(y=0,color='grey',linestyle="dotted",linewidth=0.5) # Set axes limits plt.xlim([-11,20]) plt.ylim([-15,25]) # Set boundary edges for axis in ['top','bottom','left','right']: ax.spines[axis].set_linewidth(0.5) ax.spines['right'].
```

### 11. TS_Fig12 / `TS_Fig12\Extremes\TS2-Land-Extremes-202110.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `43b20f1bf10a9c345f0bb90812987947651b87ab`
- Tags: `multi_panel, scatter`

```text
#!/usr/bin/env python3 # -*- coding: utf-8 -*- """ Created on Tue Mar 9 17:12:01 2021 @author: gkrinner """ import numpy as np from xlrd import open_workbook import matplotlib.pyplot as plt from matplotlib.font_manager import FontProperties from matplotlib.path import Path from matplotlib.textpath import TextToPath from matplotlib.ticker import (MultipleLocator, AutoMinorLocator) import csv selectlevels = ['1.0', '1.5', '2.0', '3.0', '4.0'] dx = .1 sizeref = 100 size0 = .25*sizeref size1 = 1*sizeref size2 = 1.5*sizeref size3 = 2.25*sizeref large = 2.3*dx def get_positions(dx0,selectlevels): npos = len(selectlevels) retpos = np.empty((npos),np.float) if (False): retpos = np.arange(dx0, np.float(npos)+dx0) else: for i in range(npos): retpos[i] = dx0 + float(selectlevels[i]) return retpos def read_csv(filename): varout = np.empty((nsGWL,nrange),np.float) fields = [] with open(filename, 'r')
```

### 12. TS_Fig12 / `TS_Fig12\Extremes\TS2-Land-Extremes-202110.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `43b20f1bf10a9c345f0bb90812987947651b87ab`
- Tags: `color_style, multi_panel, scatter`

```text
axr = ax.twinx() dx0 = -.5*dx positions = get_positions(dx0,selectlevels) axr.scatter(positions, IntTXx10s[:,i50], marker=get_marker(symbols["thermometer"]), s = size3, c=c10, edgecolors="none", linewidth=2, label="10-year event, intensity") axr.scatter(positions, IntTXx10s[:,iup], marker='1', s = size0, c=c10, edgecolors="none", linewidth=1) axr.scatter(positions, IntTXx10s[:,ilo], marker='2', s = size0, c=c10, edgecolors="none", linewidth=1) dx0 = .5*dx positions = get_positions(dx0,selectlevels) ax.scatter(positions, FreqTXx50s[:,i50], marker=get_marker(symbols["stopwatch"]), s = size2, c=c50, edgecolors="none", linewidth=2, label="50-year event, frequency") ax.scatter(positions, FreqTXx50s[:,iup], marker='1', s = size0, c=c50, edgecolors="none", linewidth=1) ax.scatter(positions, FreqTXx50s[:,ilo], marker='2', s = size0, c=c50, edgecolors="none", linewidth=1) dx0 = 1.5*dx positions =
```
