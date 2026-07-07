# distribution Evidence Pack

- Candidate skill: `ipcc-ensemble-distribution`
- Matching chunks: 386
- Matching repositories: 41
- Matching files: 235

## Representative Sources

### 1. Atlas / `Atlas\datasets-aggregated-regionally\scripts\computeFigures.R`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `ed29da33d38ae767d19caafd4cde06042cbe00f4`
- Tags: `distribution, raster_stripes, scatter`

```text
# computeFigures.R # # Copyright (C) 2021 Santander Meteorology Group (http://meteo.unican.es) # # This work is licensed under a Creative Commons Attribution 4.0 International # License (CC BY 4.0 - http://creativecommons.org/licenses/by/4.0) #' @title Scatter and boxplots of temperature and precipitation changes #' @description Compute scatterplots and boxplots of temperature and precipitation changes from data #' files of this repository (datasets-aggregated-regionally). #' @details Functions computeDeltas (computeDeltas.R) and computeOffset (computeOffset.R) #' are internally used. #' @author M. Iturbide computeFigures <- function(regions, cordex.domain = NULL, area, ref.period, scatter.seasons, xlim = NULL, ylim = NULL) { library(lattice) library(latticeExtra) # select warming levels and list future periods, e.g. list(c(2021, 2040), c(2041, 2060), c(2081, 2100)) WL <- c("1.5", "2", "
```

### 2. Box_TS4_Fig1 / `Box_TS4_Fig1\PanelA_Timeseries\Plot_GMSL.m`

- Chunk type: `code`
- Language: `R`
- Commit: `6a7832877157aa79a6cfcec5c4c278267858e94d`
- Tags: `distribution, multi_panel, raster_stripes, time_series`

```text
%% IPCC AR6 Chapter 9: Figure 9.27 (Sea level scenarios) % % Code used to plot pre-processed sea level scenarios % % Plotting code written by Bob Kopp % Processed data provided by Bob Kopp % Other datasets cited in report/caption clear all addpath ../../../Functions/ %savefile='AR6_GMSL_Models_v3.xlsx' fontsize=15; width = 3; start_year=1900; end_year=2150; % Colors updated to match updated SPM colors color_SSP119 = [0 173 207]/255; color_SSP126 = [23 60 102]/255; color_SSP245 = [247 148 32]/255; color_SSP370 = [231 29 37]/255; color_SSP585 = [149 27 30]/255; %% clear hs; fig1=figure('Position', [10 10 800 500]); dw=.6; hs(1)=subplot(2,2,1); hs(2)=subplot(2,2,2); %hs(3)=subplot(2,2,3); %hs(4)=subplot(2,2,4); pos=get(hs,'position'); pos0=pos; dw2=dw-pos{1}(3); pos{2}(1)=pos{2}(1)+dw2-.09; pos{2}(3)=pos{2}(3)-dw2; pos{1}(3)=dw; %pos{3}(3)=pos{1}(3); %pos{4}([1 3])=pos{2}([1 3]); for sss=1:
```

### 3. Chapter-11 / `Chapter-11\code\process.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `d1a3a99f242a568fb4cefc36a038c888a90b9d37`
- Tags: `distribution, raster_stripes`

```text
import logging import docopt import regionmask import conf from utils import postprocess logger = logging.getLogger(__name__) ar6_land = regionmask.defined_regions.ar6.land # ============================================================================= # postprocess.GlobalMeanFromOrig(self.conf_cmip) # postprocess.NoTransformFromOrig(self.conf_cmip) # postprocess.SelectGridpointFromOrig(self.conf_cmip) # postprocess.SelectRegionFromOrig(self.conf_cmip) # postprocess.CDDFromOrig(self.conf_cmip) # postprocess.RxNdayFromOrig(self.conf_cmip) # postprocess.TxDaysAboveFromOrig(self.conf_cmip) # postprocess.ResampleAnnualFromOrig(self.conf_cmip) # postprocess.ResampleMonthlyFromOrig(self.conf_cmip) # postprocess.ResampleAnnualQuantileFromOrig(self.conf_cmip) # postprocess.RegionAverageFromOrig(self.conf_cmip) # postprocess.RegridFromPost(self.conf_cmip) # postprocess.RegionAverageFromPost(self.
```

### 4. Chapter-12 / `Chapter-12\Figures\scripts\ETWL_satellites\Kirezci_IPCC_AR6_MatlabCodes\IPCC_ESLs_AR6_Regions_Kirezci.m`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `358a09813f5b29ea064a0629c26b030d60c1f972`
- Tags: `distribution, raster_stripes`

```text
% IPCC_ESLs_AR6_regions_Kirezci.m % Processing code for Figure SM 12.6 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 12 % Computes regional averages of extreme sea level (ESL) for the AR6 regions from the Kirezci et al (2020) dataset (Kirezci, E., Young, I.R., Ranasinghe, R. et al. Projections of global-scale extreme sea levels and resulting episodic coastal flooding over the 21st Century. Sci Rep 10, 11629 (2020). https://doi.org/10.1038/s41598-020-67736-6). ESL data from Kirezci et al (2020) are stored as values per segment of coastline, and here the weighted mean of these coastline lengths per AR6 region is calculated. The 5th (lo), 50th (ce) and 95th (up) percentile estimates of the extreme sea level are available. In chapter 12 we use the the ce estimate as the median value(dots) in Figure S12.6 and the uncertainty bars span from the 5th to 95th pe
```

### 5. Chapter-2_Fig36 / `Chapter-2_Fig36\Fig_2.36_code.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `f7d6a2fc8cff9d9650a9d8587deec5e952306f55`
- Tags: `color_style, distribution, multi_panel, raster_stripes, time_series`

```text
% normalise according to 1900-1970 [ee,sd]=min(abs(time-1900)); [ee,ed]=min(abs(time-1970)); for i=1:17, proxy_data(i,:)=proxy_data(i,:)-nanmean(proxy_data(i,sd:ed)); proxy_data(i,:)=proxy_data(i,:)/nanstd(proxy_data(i,sd:ed)); end % compar with obs SOI % for i =1:17, % cc=corrcoef(proxy_data(i,end-100:end-25),jonesmannrogfig6a(end-100:end-25,2)); % cc0(i)=cc(1,2); % cc=corrcoef(proxy_data(i,end-100:end-25),jonesmannrogfig6a(end-99:end-24,2)); % ccp1(i)=cc(1,2); % cc=corrcoef(proxy_data(i,end-100:end-25),jonesmannrogfig6a(end-101:end-26,2)); % ccm1(i)=cc(1,2); % end k=1; for i=1:length(proxy_data(1,:))-30, proxy_data_std2(:,k)=std(proxy_data(:,i:i+29)'); proxy_data_var2(:,k)=var(proxy_data(:,i:i+29)'); k=k+1; end max_proxy_data_std2=max(proxy_data_std2'); % for i=1:18, % [ii]=find(proxy_data_std2(i,:)==max_proxy_data_std2(i)); % max_time(i)=time(ii+29); % end YMatrix1=proxy_data_var2(1:1
```

### 6. Chapter-3_Figure3.29 / `Chapter-3_Figure3.29\SCRIPT\CodeStep4_plotFinal_1panel_mpl.py.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `8bcf03d38b9e987d86b5f3ed5e0b770b19672008`
- Tags: `distribution, raster_stripes, time_series`

```text
for exp in exp_list: # print ('Experiment :', exp) fout1.write ('Experiment :%s\n' %exp) # lines_to_plot_dict[exp] = {} # mod_list = list(plotDataDict[exp].keys()) # mod_list.sort() N_MODS = len(mod_list) N_RELS = {} # # all_models_rels_weights_list will contain weights for every realization of every model # all_models_rels_weights_list = [] # # all_models_rels_data will contain every realization of every model # all_models_rels_data = [] # # all_models_avg_list will contain the average of all realizations of a single model # all_models_avg_list = [] # # all_models_avg_var_list_to_plot will contain the individual model averages variable for plotting. # all_models_avg_var_list_to_plot = [] # all_rels_all_models_list_to_plot = [] # delta_dict = {} rate_dict = {} # for mod in mod_list: # print ('\tModel :', mod) fout1.write('\tModel :%s\n' %mod) rel_list = plotDataDict[exp][mod].keys() N_RE
```

### 7. Chapter-3_Figure3.2a / `Chapter-3_Figure3.2a\IPCCAR6_WG1_Chapter3_Figs3.2a_3.44.py.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `e6d5e89f5707313a8e276e08cfa4fe9a87c5a40c`
- Tags: `distribution, multi_panel, raster_stripes`

```text
# for Fig 3.44 panel a. Data provided by Dan Lunt (computed for Chapter 7) # GSAT anomalies # for LIG (Last Interglacial) dic_global_mean_lig = {'ACCESS-ESM1-5':0.33, 'AWI-ESM-1-1-LR':-0.25, 'AWIESM2':-0.20, 'CESM2':-0.11, 'CNRM-CM6-1':0.4, 'EC-Earth3-LR':0.45, 'FGOALS-f3-L':-0.48, 'FGOALS-g3':0.38, 'GISS-E2-1-G':-0.12, 'HadGEM3-GC31':0.56, 'INM-CM4-8':-0.2, 'IPSL-CM6A-LR':-0.29, 'MIROC-ES2L':-0.4, 'MPI-ESM1-2-LR':-0.12, 'NESM3':0.07, 'NorESM1-F':-0.24, 'NorESM2-LM':-0.11, } # for the mid-Pliocene dic_global_mean_plio = {'CCSM4-plio':2.64831, 'CCSM4-UoT': 3.79105, 'CCSM4-Utrecht': 4.67974, 'CESM1.2': 4.03265, 'CESM2': 5.22695, 'COSMOS': 3.32687, 'EC-Earth3-LR': 4.84114, 'GISS-E2-1-G': 2.08071, 'HadCM3': 2.89054, 'IPSL-CM6A-LR': 3.47365, 'IPSLCM5A': 2.29695, 'IPSLCM5A2': 2.16866, 'MIROC4m': 3.13146, 'MRI-CGCM2.3': 2.45558, 'NorESM-L': 2.09194, 'NorESM1-F': 1.73549, 'HadGEM3':5.05506, } # 
```

### 8. Chapter-4_CCBOX4.1_Fig1 / `Chapter-4_CCBOX4.1_Fig1\AR6_Chapter4_CCBOX41_Fig1.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `966b5fc731261d88672bf6fb4905c2e44d136ec3`
- Tags: `distribution, raster_stripes`

```text
%###################################################################################################################### % --------------------------------------------------------------------------------------------------------------------- % This is Matlab code to produce IPCC AR6 WGI Cross Chapter Box 4.1 Fig 1 % Creator: Ingo Bethke, University of Bergen % Contact: ingo.bethke@uib.no % Last updated on: May 16th, 2023 % --------------------------------------------------------------------------------------------------------------------- % % - Code functionality: This script plots a modified version of Figure 2 in Bethke et al., 2017 % (https://doi.org/10.1038/nclimate3394). It shows the simulated 21st Century evolutions of effective radiative forcing % and surface temperature from an Earth system model that is driven with synthetic future volcanic forcing variability. % - Input data: Mod
```

### 9. Chapter-6_Fig09 / `Chapter-6_Fig09\Fig6.9_oh_anomaly.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `5979eb3f5af6fda8628306e78cf90107bf32aed3`
- Tags: `distribution, raster_stripes`

```text
# |-------------------------------------------------------------------------------| # | #-*- coding:utf-8 -*- # | __author__ = "Alcide Zhao" # | __copyright__ = "Copyright 2021, The AerChemMIP Project" # | __maintainer__ = "Alcide Zhao" # | __email__ = "alcide.zhao@reading.ac.uk" # | __status__ = "Production" # | __reference__ = "Stevenson et al. (2020): Trends in global tropospheric # | hydroxyl radical and methane lifetime since 1850 from # | AerChemMIP, Atmos. Chem. Phys. # | https://doi.org/10.5194/acp-20-12905-2020, 2020. " # | # | This script produces the OH anomoly plots for IPCC AR6. # | It was written using Python2.7, but should also wotk with Python 3 # | Inputs: # | All data are under the ./data folder # | Output: # | The plot named 'OHAnomoly_1850-2014_IPCC_AR6.png' saved under working # | directory # | Use: # | change to the working directory and execute # | python oh_anomol
```

### 10. Chapter-6_Fig12_22_24 / `Chapter-6_Fig12_22_24\ar6_ch6_rcmipfigs\notebooks\fig6_12_and_ts15_spm2\01_make_historical_attribution.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `cd6393f61459534bf60374c757e8af0f6f1553a7`
- Tags: `bar_hist_density, color_style, distribution, multi_panel, raster_stripes, uncertainty`

```text
# %% pycharm={"name": "#%%\n"} from ar6_ch6_rcmipfigs.utils.plot import get_chem_col # %% [markdown] pycharm={"name": "#%% md\n"} # Variables in the rigth order: # %% pycharm={"name": "#%%\n"} varn = ['co2','N2O','HC','ch4','o3','H2O_strat','ari','aci'] var_dir = ['CO2','N2O','HC','CH4_lifetime','O3','Strat_H2O','Aerosol','Cloud'] # %% [markdown] pycharm={"name": "#%% md\n"} # Colors: # %% pycharm={"name": "#%%\n"} cols = [get_chem_col(var) for var in varn] # %% [markdown] pycharm={"name": "#%% md\n"} # ## Uncertainty: # %% [markdown] pycharm={"name": "#%% md\n"} # We have the standard deviation, but would like the use the standard error of the mean AND we would like to calculate the 5-95th percentile. # %% [markdown] pycharm={"name": "#%% md\n"} # We have the standard deviation (as far as I can tell, not the unbiased one) # %% [markdown] pycharm={"name": "#%% md\n"} # $\sigma=\sqrt {\fr
```

### 11. Chapter-6_Fig12_22_24 / `Chapter-6_Fig12_22_24\ar6_ch6_rcmipfigs\notebooks\fig6_12_and_ts15_spm2\03_historical_deltaGSAT.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `cd6393f61459534bf60374c757e8af0f6f1553a7`
- Tags: `distribution, raster_stripes, time_series`

```text
# --- # jupyter: # jupytext: # formats: ipynb,py:percent # text_representation: # extension: .py # format_name: percent # format_version: '1.3' # jupytext_version: 1.11.4 # kernelspec: # display_name: Python 3 (ipykernel) # language: python # name: python3 # --- # %% [markdown] tags=[] # # Compute $\Delta T$ # %% [markdown] # ### Imports # %% import numpy as np # %% import pandas as pd import xarray as xr from IPython.display import clear_output # %% from openscm_twolayermodel import ImpulseResponseModel # pip install openscm-twolayermodel from openscm_units import unit_registry # pip install openscm-units from scmdata import ScmRun # pip install scmdata # %load_ext autoreload # %autoreload 2 from ar6_ch6_rcmipfigs.constants import INPUT_DATA_DIR_BADC # %% from ar6_ch6_rcmipfigs.utils.badc_csv import read_csv_badc # %% [markdown] # ### General about computing $\Delta T$: # %% [markdown] 
```

### 12. Chapter-6_Fig12_22_24 / `Chapter-6_Fig12_22_24\ar6_ch6_rcmipfigs\notebooks\fig6_12_and_ts15_spm2\03_historical_deltaGSAT.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `cd6393f61459534bf60374c757e8af0f6f1553a7`
- Tags: `distribution, raster_stripes, time_series`

```text
# lets define the vars of the ds namevar = name_deltaT # set all values to zero for results dataarray: ds_DT[namevar] = ds_DT[int_var] * 0 # Units Kelvin: ds_DT[namevar].attrs['unit'] = 'K' if 'unit' in ds_DT[namevar].coords: ds_DT[namevar].coords['unit'] = 'K' for i in range(len_time): # da = ds[var] if (i % 20) == 0: print('%s of %s done' % (i, len_time)) integrate_(i, int_var, namevar, ds_sl, ds_DT, irf_cnsts) clear_output() # fn = 'DT_%s-%s.nc' % (from_t, to_t) #fname = OUTPUT_DATA_DIR/ fn#'DT_%s-%s.nc' % (from_t, to_t) # save dataset. #ds_DT.to_netcdf(fname) return ds_DT # %% def calc_dGSAT(var, ds, ds_out, scenario='scenario'): s_y = int(ds.isel(year=0)['year'].values) _erf_tmp = ds['ERF'].sel(variable=var).to_pandas() unit = "W/m^2" driver = ScmRun( data=_erf_tmp, index=s_y + np.arange(len(_erf_tmp)), columns={ "unit": unit, "model": "custom", "scenario": scenario, "region": "Worl
```
