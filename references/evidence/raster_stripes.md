# raster_stripes Evidence Pack

- Candidate skill: `ipcc-raster-stripes`
- Matching chunks: 424
- Matching repositories: 51
- Matching files: 242

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

### 5. Chapter-2_Fig13 / `Chapter-2_Fig13\trendmap_q.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `7c8cc2dcd1d860076832c34b90e3c3ae2e292521`
- Tags: `bar_hist_density, color_style, map, raster_stripes`

```text
coast=load('coast'); load BuDOd_18.dat; C=BuDOd_18(:,1:3); cx=0.5; cn=-0.5; yba=[1973]; yea=[2019]; np=length(yba); p=0.90; nmonmin = 8; ptot = 0.7; plenbe = 0.1; pbe = 0.25; dx=5; dy=5; Xo = (-177.5:dx:177.5)'; Y = (-87.5:dy:87.5)'; nx=length(Xo); ny=length(Y); nxny=nx*ny; ixs180=[nx/2+1:nx 1:nx/2]; X=Xo(ixs180); X(1:nx/2)=X(1:nx/2)-360; tyrs=1973:2019; nt=length(tyrs); ntm=nt*12; t=zeros(ntm,1); q = NaN(ntm,nxny); amiss = -999.9; fname='../data/HadISDH.blendq.1.0.0.2019f.nc'; q=ncread('HadISDH.blendq.1.0.0.2019f.nc', 'q_abs'); q=permute(q,[3,1,2]); inav=find(q <= amiss); q(inav) = NaN; precann=zeros(nt,nx,ny); for ixy=1:nx, for iyy=1:ny panom=q(:,ixy,iyy); pann = monanom2ann(panom,nmonmin); precann(:,ixy,iyy) = pann; end end w0=precann; w=w0(:,ixs180,:); % Loop over periods for ip = 1:np, sper = [num2str(yba(ip)) '-' num2str(yea(ip))]; its=find(tyrs>=yba(ip) & tyrs<=yea(ip)); ts=tyrs(i
```

### 6. Chapter-2_Fig15 / `Chapter-2_Fig15\trendmap_cru25_404_19012019.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `df6adbb8b8c99a7824691d3e2538841112102f98`
- Tags: `bar_hist_density, color_style, map, raster_stripes`

```text
coast=load('coast'); load BuDOd_18_2.dat; C=BuDOd_18_2(:,1:3); cx=60; cn=-60; yba=[1901]; yea=[2019]; np=length(yba); p=0.90; nmonmin = 8; ptot = 0.7; plenbe = 0.1; pbe = 0.25; dx=2.5; dy=2.5; Xo = (0:dx:357.5)'; Y = (-88.75:dy:88.75)'; nx=length(Xo); ny=length(Y); nxny=nx*ny; ixs180=[nx/2+1:nx 1:nx/2]; X=Xo(ixs180); X(1:nx/2)=X(1:nx/2)-360; tyrs=1901:2019; nt=length(tyrs); ntm=nt*12; t=zeros(ntm,1); prec = NaN(ntm,nxny); amiss = -999.9; fname='../data/cru_masked_2019_2.nc'; prec=ncread('cru_masked_2019_2.nc', 'pre'); prec=permute(prec,[3,1,2]); inav=find(prec <= amiss); prec(inav) = NaN; precann=zeros(nt,nx,ny); for ixy=1:nx, for iyy=1:ny panom=prec(:,ixy,iyy); pann = monanom2ann(panom,nmonmin); precann(:,ixy,iyy)=pann; end end w0=precann; w=w0(:,ixs180,:); % Loop over periods for ip = 1:np, sper = [num2str(yba(ip)) '-' num2str(yea(ip))]; its=find(tyrs>=yba(ip) & tyrs<=yea(ip)); ts=tyrs
```

### 7. Chapter-2_Fig16 / `Chapter-2_Fig16\trendmap_pme_era5_19802019.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `78455e26834be3ca60c9b1752925932a1487f7ee`
- Tags: `bar_hist_density, color_style, map, raster_stripes`

```text
coast=load('coast'); load BuDOd_18.dat; C=BuDOd_18(:,1:3); cx=250; cn=-250; yba=[1980]; yea=[2019]; np=length(yba); p=0.90; nmonmin = 8; ptot = 0.7; plenbe = 0.1; pbe = 0.25; dx=2.5; dy=2.5; Xo = (0:dx:357.5)'; Y = (-88.75:dy:88.75)'; nx=length(Xo); ny=length(Y); nxny=nx*ny; ixs180=[nx/2+1:nx 1:nx/2]; X=Xo(ixs180); X(1:nx/2)=X(1:nx/2)-360; tyrs=1979:2019; nt=length(tyrs); ntm=nt*12; t=zeros(ntm,1); prec = NaN(ntm,nxny); amiss = -999.9; fname1='../data/era5_tp_2.nc'; fname2='../data/era5_evap_2.nc'; pre=ncread('era5_tp_2.nc', 'tp'); evap=ncread('era5_evap_2.nc', 'evap'); prec=pre-evap; prec=permute(prec,[3,1,2]); inav=find(prec <= amiss); prec(inav) = NaN; pmeann=zeros(nt,nx,ny); for ixy=1:nx, for iyy=1:ny panom=prec(:,ixy,iyy); pann = monanom2ann(panom,nmonmin); pmeann(:,ixy,iyy)=pann; end end w0=pmeann; % Loop over periods for ip = 1:np, sper = [num2str(yba(ip)) '-' num2str(yea(ip))]; i
```

### 8. Chapter-2_Fig18 / `Chapter-2_Fig18\Fig2.18ERA5uwindtrendx.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `6e2ec059c07b2f82ce5c54b88209617ba9a08b8e`
- Tags: `color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
% ch2_fig18.m % % Description % Generates Figure 2.18 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 2 % % Creator: Daoyi Gong (gdy@bnu.edu.cn) % Creating Date: 19 December 2020 % % computing U wind trend for ERA5 % % Assume a confidence level for computing confidence intervals % pconf=0.9; cn=-1.5; cx=1.5; load BuDRd_18.dat; C=BuDRd_18(:,1:3); mon_str={'01','02','03','04','05','06','07','08','09','10','11','12'}; mon_name={'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'}; for mon_num=1:12; mon_name{mon_num} eval(['load u' mon_str{mon_num}]) end % next mon clf figure % title('Zonal wind trend') for isea=1:4 %[wkdat=u01]; % eval(['wkdat=u' mon_str{mon_num} ';']); % eval(['u_cli=u' mon_str{mon_num} '_cli;']); % DJF; if (isea ==1 ) wkdat=(u12(1:end-1,:,:)+u01(2:end,:,:)+u02(2:end,:,:))/3; u_cli=(u12_cli+u01_cli+u02_cli)/3; ssea={'DJF
```

### 9. Chapter-2_Fig19 / `Chapter-2_Fig19\Fig2.19surfacewindtrendx.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `4a2030b27987bf32157057ad760fcc5f1c29c627`
- Tags: `bar_hist_density, color_style, map, raster_stripes`

```text
% ch2_fig19.m % % Description % Generates Figure 2.19 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 2 % % Creator: Daoyi Gong (gdy@bnu.edu.cn) % Creating Date: 19 December 2020 % % make a single figure % make a single figure x-non-significant point clc,clear %cd data clf fontsizenum=14; LW=0.5; % coast line width CZ=2.1; % Cross size %%%% figure for myfig=1:4; if ( myfig == 1 ); load HadISD; end if ( myfig == 2 ); load ERA5; end if ( myfig == 3 ); load CCMP; end if ( myfig == 4 ); load OAFlux;end wind=wind(:,:,find(year>=1988 & year<=2017)); year=year(find(year>=1988 & year<=2017)); % 1.CCMP 2.OAFlux 3.BSW 4.ERA-Interim 5.ERA5 6.NNR 7.WASind 8.HadISD %cd .. clear glat glon ; [glat,glon]=meshgrat(nlat,nlon); %%%% %% trend clear tr pv xlat xlon; p=0.9; for i=1:length(nlat) for j=1:length(nlon) [b,cinthw,sig,DOFr,rho,pval,irrc,N,a,Na,Nc]=ltr_OLSdofrNaN(yea
```

### 10. Chapter-2_Fig27 / `Chapter-2_Fig27\Figure_2_27.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `debdd5d06b7a5002d4437825663a93fc531e72b4`
- Tags: `bar_hist_density, color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
clear all, close all, clc cd('/Users/boeiradi/Documents/SL_AR6_work/Chap2') addpath('/Users/boeiradi/Documents/SL_AR6_work/Chap2/m_map') addpath('/Users/boeiradi/Library/Application Support/MathWorks/MATLAB Add-Ons/Toolboxes/stipple') %% define colormap jetmean = [ 84 48 5 110 68 15 137 88 25 164 108 35 191 129 44 200 148 79 210 169 113 220 189 147 229 209 180 239 228 215 248 248 247 216 232 231 183 216 213 151 200 195 118 183 178 85 167 160 53 151 143 39 128 119 26 105 95 13 82 71 0 60 48]; jetmean=jetmean(end:-1:1,:)/256; jeterror=jetmean; %% read DW2010 file and variables: DW10 = ('DurackandWijffels_GlobalOceanChanges_19500101-20191231__210122-205355_beta.nc'); time = ncread(DW10,'time'); depth = ncread(DW10,'depth'); lon = ncread(DW10,'longitude'); lat = ncread(DW10,'latitude'); salt_mean = ncread(DW10,'salinity_mean'); salt_change = ncread(DW10,'salinity_change')/7; % change unit fr
```

### 11. Chapter-2_Fig27 / `Chapter-2_Fig27\Figure_2_27.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `debdd5d06b7a5002d4437825663a93fc531e72b4`
- Tags: `bar_hist_density, color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
% dw vertical section % changes ax2 = subplot(3,1,2); pcolor(Lat1,Dep1,schg_dw10_glo(:,1:depth1)); shading flat; caxis([scale2(1) scale2(2)]); hold on; axis ij; colormap(ax2,jetmean) contour(Lat1,Dep1,smean_dw10_glo(:,1:depth1),[34.25 34.75 35.25 35.75 36.25 36.75],'k','linewidth',1); [c,h] = contour(Lat1,Dep1,smean_dw10_glo(:,1:depth1),33:.5:37,'k','linewidth',2); stipple(Lat1i,Dep1i,mask_sec1i,'color',0.5*[1 1 1],'marker','x','markersize',3) clabel(c,h,'LabelSpacing',100,'fontsize',fonts_c,'fontweight','bold','color','k') ax3 = subplot(3,1,3); pcolor(Lat2,Dep2,schg_dw10_glo(:,depth1:depth2)); shading flat; caxis([scale2(1) scale2(2)]); hold on; axis ij; colormap(ax3,jetmean) contour(Lat2,Dep2,smean_dw10_glo(:,depth1:depth2),[34.25 34.75 35.25 35.75 36.25 36.75],'k','linewidth',1); [c,h] = contour(Lat2,Dep2,smean_dw10_glo(:,depth1:depth2),33:.5:37,'k','linewidth',2); stipple(Lat2i,Dep2i
```

### 12. Chapter-2_Fig31 / `Chapter-2_Fig31\chl_analysis.py`

- Chunk type: `code`
- Language: ``
- Commit: `56f7e4926f72540330194e2ae91b4f0c09243a8e`
- Tags: `color_style, map, raster_stripes`

```text
import os from pathlib import Path import numpy as np import pylab as pl import pandas as pd import xarray as xr from matplotlib import cm from matplotlib.colors import LogNorm import requests import matplotlib as mpl import projmap import trend_analysis Path("figs").mkdir(parents=True, exist_ok=True) def filename(dtm, ver="4.2", datadir=None): """Generate OC-CCI filenames based on datetime object""" if datadir is None: datadir = "ncfiles/OC-CCI" Path(datadir).mkdir(parents=True, exist_ok=True) dstr = f"{dtm.year}{dtm.month:02}" return (f"{datadir}/ESACCI-OC-L3S-CHLOR_A-MERGED-" + f"1M_MONTHLY_4km_GEO_PML_OCx-{dstr}-fv{ver}.nc") def download(dtm, download_timeout=10): """Download OC-CCI monthly netcdf files""" local_filename = filename(dtm) url = "https://www.oceancolour.org/browser/get.php" params = dict(date=f"{dtm.year}-{dtm.month:02}-{dtm.day:02}", product="chlor_a", period="monthly"
```
