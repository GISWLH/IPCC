# map Evidence Pack

- Candidate skill: `ipcc-regional-map`
- Matching chunks: 263
- Matching repositories: 27
- Matching files: 171

## Representative Sources

### 1. Atlas / `Atlas\datasets-interactive-atlas\04_map_figures.R`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `ed29da33d38ae767d19caafd4cde06042cbe00f4`
- Tags: `color_style, map, uncertainty`

```text
# 04_map_figures.R # # Copyright (C) 2021 Santander Meteorology Group (http://meteo.unican.es) # # This work is licensed under a Creative Commons Attribution 4.0 International # License (CC BY 4.0 - http://creativecommons.org/licenses/by/4.0) #' @title Generate map figures from ensemble NcMLs #' @description Generate map figures from the NcMLs created #' using 03_ensemble_building.R, for Atlas Product Reproducibility. #' @author M. Iturbide # This script builds on the climate4R framework # https://github.com/SantanderMetGroup/climate4R # Climate4R package for data loading library(loadeR) # Climate4R package for data visualization # <https://doi.org/10.1016/j.envsoft.2017.09.008> library(visualizeR) # climate 4R package for geoprocessing library(geoprocessoR) # Other utilities for spatial data handling and geoprocessing: library(sp) library(rgdal) # Dev utilities used for source_url libra
```

### 2. Chapter-11 / `Chapter-11\code\hadex3.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `d1a3a99f242a568fb4cefc36a038c888a90b9d37`
- Tags: `map`

```text
import warnings import cartopy.crs as ccrs import cartopy.feature as cfeatures import matplotlib.patches as mpatches import matplotlib.pyplot as plt import mplotutils as mpu import xarray as xr import filefinder as ff from utils import plot from utils.statistics import theil_ufunc # we would get 13 warnings when reading HadEX3 data warnings.filterwarnings("ignore", message="variable '.*' has multiple fill values") CURRENT_VERSION = "3.0.2" class HadEx3_cls: """docstring for HadEx3_cls.""" def __init__(self): self._files_raw = ff.FileFinder( path_pattern="../data/HadEX3/v{version}/raw/", file_pattern="HadEX3_{varn}_{year_from}-{year_to}_ADW_{climatology}_1.25x1.875deg.nc", ) self._files_post = ff.FileFinder( path_pattern="../data/HadEX3/v{version}/{postprocess}/", file_pattern="{postprocess}_HadEX3_{varn}_ADW_{climatology}.{ending}", ) self._all_files_raw = None self.map_abbrevs = dict( T
```

### 3. Chapter-12 / `Chapter-12\Figures\scripts\CID\CID_AR6regions.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `358a09813f5b29ea064a0629c26b030d60c1f972`
- Tags: `map, uncertainty`

```text
import Ngl, Nio import os, numpy, csv, json from IPython.display import Image from shapely.geometry import Polygon, Point import geopandas import sys region_name = sys.argv[1] # -- Create empty map over region # -- test with and without gray fill over continent #---------------------------------------------------------------------- # Create map of southern tip of South America #---------------------------------------------------------------------- def create_map(wks, region_dict, mpOutlineOn=True): #---Map resources res = Ngl.Resources() # map resources res.nglDraw = False # don't draw map res.nglFrame = False # don't advance frame res.nglMaximize = False res.mpDataBaseVersion = "MediumRes" # better map outlines #res.mpCenterLonF = 145 #res.mpCenterLatF = 0 #res.mpLimitMode = "MaximalArea" if 'Robinson' in region_dict: res.mpProjection = "Robinson" #res.mpEllipticalBoundary = True else: 
```

### 4. Chapter-2_Fig09 / `Chapter-2_Fig09\plotfgd.ncl`

- Chunk type: `code`
- Language: `Fortran`
- Commit: `4413efb5552423d7e0e4330387b0cdf593dd3638`
- Tags: `color_style, map`

```text
; Script “plotfgd.ncl” load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl" begin var="su" ;var="bc" wks = gsn_open_wks ("eps","icesod"+var) ;wks = gsn_open_wks ("pdf","icesod"+var) gsn_define_colormap(wks,"AR6_Line_Shade") wks@wkOrientation = "landscape" res = True res@vpHeightF= 0.4 ; change aspect ratio of plot res@vpWidthF = 0.7 res@gsnDraw = False res@gsnFrame = False res@tmYRBorderOn = False res@tmXTBorderOn = False res@tmYROn = False res@tmXTOn = False res@tmXBLabelFont=12 res@tmYLLabelFont=12 res@txFontHeightF = 0.015 if ( var.eq."su" ) then res@gsnLeftString = "(a) Non-sea salt sulfate" res@tiYAxisString = "(ng g~S~-1~N~)" else res@gsnLeftString = "(b) Refractory black carbon" res@tiYAxisString = "(ng g~
```

### 5. Chapter-2_Fig10 / `Chapter-2_Fig10\ploterf.ncl`

- Chunk type: `code`
- Language: `NCL`
- Commit: `c02680421212f290bbf2682860608da84ac7075e`
- Tags: `color_style, map, uncertainty`

```text
; Script “ploterf.ncl” load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl" begin ;wks = gsn_open_wks ("pdf","erf") ;wks = gsn_open_wks ("eps","erf") wks = gsn_open_wks ("ps","erf") gsn_define_colormap(wks,"AR6_Line_Shade") wks@wkOrientation = "landscape" res = True res@vpHeightF= 0.6 ; change aspect ratio of plot res@vpWidthF = 0.7 res@gsnDraw = False res@gsnFrame = False res@tmXBLabelFont=12 res@tmYLLabelFont=12 res@tiYAxisString = "(W m~S~-2~N~)" res@tiYAxisFont=12 res@trXMinF = 1750 res@trXMaxF = 2020. res@trYMinF = -4.9 res@trYMaxF = 2.99 res@tmYRBorderOn = False res@tmXTBorderOn = False res@tmYROn = False res@tmXTOn = False res@tmYLPrecision = 1 res@tiMainFont = 12 res@xyLineThicknessF=3. ;res@gsnMaximize =
```

### 6. Chapter-2_Fig13 / `Chapter-2_Fig13\trendmap_q.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `7c8cc2dcd1d860076832c34b90e3c3ae2e292521`
- Tags: `bar_hist_density, color_style, map, raster_stripes`

```text
coast=load('coast'); load BuDOd_18.dat; C=BuDOd_18(:,1:3); cx=0.5; cn=-0.5; yba=[1973]; yea=[2019]; np=length(yba); p=0.90; nmonmin = 8; ptot = 0.7; plenbe = 0.1; pbe = 0.25; dx=5; dy=5; Xo = (-177.5:dx:177.5)'; Y = (-87.5:dy:87.5)'; nx=length(Xo); ny=length(Y); nxny=nx*ny; ixs180=[nx/2+1:nx 1:nx/2]; X=Xo(ixs180); X(1:nx/2)=X(1:nx/2)-360; tyrs=1973:2019; nt=length(tyrs); ntm=nt*12; t=zeros(ntm,1); q = NaN(ntm,nxny); amiss = -999.9; fname='../data/HadISDH.blendq.1.0.0.2019f.nc'; q=ncread('HadISDH.blendq.1.0.0.2019f.nc', 'q_abs'); q=permute(q,[3,1,2]); inav=find(q <= amiss); q(inav) = NaN; precann=zeros(nt,nx,ny); for ixy=1:nx, for iyy=1:ny panom=q(:,ixy,iyy); pann = monanom2ann(panom,nmonmin); precann(:,ixy,iyy) = pann; end end w0=precann; w=w0(:,ixs180,:); % Loop over periods for ip = 1:np, sper = [num2str(yba(ip)) '-' num2str(yea(ip))]; its=find(tyrs>=yba(ip) & tyrs<=yea(ip)); ts=tyrs(i
```

### 7. Chapter-2_Fig15 / `Chapter-2_Fig15\trendmap_cru25_404_19012019.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `df6adbb8b8c99a7824691d3e2538841112102f98`
- Tags: `bar_hist_density, color_style, map, raster_stripes`

```text
coast=load('coast'); load BuDOd_18_2.dat; C=BuDOd_18_2(:,1:3); cx=60; cn=-60; yba=[1901]; yea=[2019]; np=length(yba); p=0.90; nmonmin = 8; ptot = 0.7; plenbe = 0.1; pbe = 0.25; dx=2.5; dy=2.5; Xo = (0:dx:357.5)'; Y = (-88.75:dy:88.75)'; nx=length(Xo); ny=length(Y); nxny=nx*ny; ixs180=[nx/2+1:nx 1:nx/2]; X=Xo(ixs180); X(1:nx/2)=X(1:nx/2)-360; tyrs=1901:2019; nt=length(tyrs); ntm=nt*12; t=zeros(ntm,1); prec = NaN(ntm,nxny); amiss = -999.9; fname='../data/cru_masked_2019_2.nc'; prec=ncread('cru_masked_2019_2.nc', 'pre'); prec=permute(prec,[3,1,2]); inav=find(prec <= amiss); prec(inav) = NaN; precann=zeros(nt,nx,ny); for ixy=1:nx, for iyy=1:ny panom=prec(:,ixy,iyy); pann = monanom2ann(panom,nmonmin); precann(:,ixy,iyy)=pann; end end w0=precann; w=w0(:,ixs180,:); % Loop over periods for ip = 1:np, sper = [num2str(yba(ip)) '-' num2str(yea(ip))]; its=find(tyrs>=yba(ip) & tyrs<=yea(ip)); ts=tyrs
```

### 8. Chapter-2_Fig16 / `Chapter-2_Fig16\trendmap_pme_era5_19802019.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `78455e26834be3ca60c9b1752925932a1487f7ee`
- Tags: `bar_hist_density, color_style, map, raster_stripes`

```text
coast=load('coast'); load BuDOd_18.dat; C=BuDOd_18(:,1:3); cx=250; cn=-250; yba=[1980]; yea=[2019]; np=length(yba); p=0.90; nmonmin = 8; ptot = 0.7; plenbe = 0.1; pbe = 0.25; dx=2.5; dy=2.5; Xo = (0:dx:357.5)'; Y = (-88.75:dy:88.75)'; nx=length(Xo); ny=length(Y); nxny=nx*ny; ixs180=[nx/2+1:nx 1:nx/2]; X=Xo(ixs180); X(1:nx/2)=X(1:nx/2)-360; tyrs=1979:2019; nt=length(tyrs); ntm=nt*12; t=zeros(ntm,1); prec = NaN(ntm,nxny); amiss = -999.9; fname1='../data/era5_tp_2.nc'; fname2='../data/era5_evap_2.nc'; pre=ncread('era5_tp_2.nc', 'tp'); evap=ncread('era5_evap_2.nc', 'evap'); prec=pre-evap; prec=permute(prec,[3,1,2]); inav=find(prec <= amiss); prec(inav) = NaN; pmeann=zeros(nt,nx,ny); for ixy=1:nx, for iyy=1:ny panom=prec(:,ixy,iyy); pann = monanom2ann(panom,nmonmin); pmeann(:,ixy,iyy)=pann; end end w0=pmeann; % Loop over periods for ip = 1:np, sper = [num2str(yba(ip)) '-' num2str(yea(ip))]; i
```

### 9. Chapter-2_Fig18 / `Chapter-2_Fig18\Fig2.18ERA5uwindtrendx.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `6e2ec059c07b2f82ce5c54b88209617ba9a08b8e`
- Tags: `color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
% ch2_fig18.m % % Description % Generates Figure 2.18 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 2 % % Creator: Daoyi Gong (gdy@bnu.edu.cn) % Creating Date: 19 December 2020 % % computing U wind trend for ERA5 % % Assume a confidence level for computing confidence intervals % pconf=0.9; cn=-1.5; cx=1.5; load BuDRd_18.dat; C=BuDRd_18(:,1:3); mon_str={'01','02','03','04','05','06','07','08','09','10','11','12'}; mon_name={'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'}; for mon_num=1:12; mon_name{mon_num} eval(['load u' mon_str{mon_num}]) end % next mon clf figure % title('Zonal wind trend') for isea=1:4 %[wkdat=u01]; % eval(['wkdat=u' mon_str{mon_num} ';']); % eval(['u_cli=u' mon_str{mon_num} '_cli;']); % DJF; if (isea ==1 ) wkdat=(u12(1:end-1,:,:)+u01(2:end,:,:)+u02(2:end,:,:))/3; u_cli=(u12_cli+u01_cli+u02_cli)/3; ssea={'DJF
```

### 10. Chapter-2_Fig19 / `Chapter-2_Fig19\Fig2.19surfacewindtrendx.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `4a2030b27987bf32157057ad760fcc5f1c29c627`
- Tags: `bar_hist_density, color_style, map, raster_stripes`

```text
% ch2_fig19.m % % Description % Generates Figure 2.19 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 2 % % Creator: Daoyi Gong (gdy@bnu.edu.cn) % Creating Date: 19 December 2020 % % make a single figure % make a single figure x-non-significant point clc,clear %cd data clf fontsizenum=14; LW=0.5; % coast line width CZ=2.1; % Cross size %%%% figure for myfig=1:4; if ( myfig == 1 ); load HadISD; end if ( myfig == 2 ); load ERA5; end if ( myfig == 3 ); load CCMP; end if ( myfig == 4 ); load OAFlux;end wind=wind(:,:,find(year>=1988 & year<=2017)); year=year(find(year>=1988 & year<=2017)); % 1.CCMP 2.OAFlux 3.BSW 4.ERA-Interim 5.ERA5 6.NNR 7.WASind 8.HadISD %cd .. clear glat glon ; [glat,glon]=meshgrat(nlat,nlon); %%%% %% trend clear tr pv xlat xlon; p=0.9; for i=1:length(nlat) for j=1:length(nlon) [b,cinthw,sig,DOFr,rho,pval,irrc,N,a,Na,Nc]=ltr_OLSdofrNaN(yea
```

### 11. Chapter-2_Fig27 / `Chapter-2_Fig27\Figure_2_27.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `debdd5d06b7a5002d4437825663a93fc531e72b4`
- Tags: `bar_hist_density, color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
clear all, close all, clc cd('/Users/boeiradi/Documents/SL_AR6_work/Chap2') addpath('/Users/boeiradi/Documents/SL_AR6_work/Chap2/m_map') addpath('/Users/boeiradi/Library/Application Support/MathWorks/MATLAB Add-Ons/Toolboxes/stipple') %% define colormap jetmean = [ 84 48 5 110 68 15 137 88 25 164 108 35 191 129 44 200 148 79 210 169 113 220 189 147 229 209 180 239 228 215 248 248 247 216 232 231 183 216 213 151 200 195 118 183 178 85 167 160 53 151 143 39 128 119 26 105 95 13 82 71 0 60 48]; jetmean=jetmean(end:-1:1,:)/256; jeterror=jetmean; %% read DW2010 file and variables: DW10 = ('DurackandWijffels_GlobalOceanChanges_19500101-20191231__210122-205355_beta.nc'); time = ncread(DW10,'time'); depth = ncread(DW10,'depth'); lon = ncread(DW10,'longitude'); lat = ncread(DW10,'latitude'); salt_mean = ncread(DW10,'salinity_mean'); salt_change = ncread(DW10,'salinity_change')/7; % change unit fr
```

### 12. Chapter-2_Fig27 / `Chapter-2_Fig27\Figure_2_27.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `debdd5d06b7a5002d4437825663a93fc531e72b4`
- Tags: `bar_hist_density, color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
% dw vertical section % changes ax2 = subplot(3,1,2); pcolor(Lat1,Dep1,schg_dw10_glo(:,1:depth1)); shading flat; caxis([scale2(1) scale2(2)]); hold on; axis ij; colormap(ax2,jetmean) contour(Lat1,Dep1,smean_dw10_glo(:,1:depth1),[34.25 34.75 35.25 35.75 36.25 36.75],'k','linewidth',1); [c,h] = contour(Lat1,Dep1,smean_dw10_glo(:,1:depth1),33:.5:37,'k','linewidth',2); stipple(Lat1i,Dep1i,mask_sec1i,'color',0.5*[1 1 1],'marker','x','markersize',3) clabel(c,h,'LabelSpacing',100,'fontsize',fonts_c,'fontweight','bold','color','k') ax3 = subplot(3,1,3); pcolor(Lat2,Dep2,schg_dw10_glo(:,depth1:depth2)); shading flat; caxis([scale2(1) scale2(2)]); hold on; axis ij; colormap(ax3,jetmean) contour(Lat2,Dep2,smean_dw10_glo(:,depth1:depth2),[34.25 34.75 35.25 35.75 36.25 36.75],'k','linewidth',1); [c,h] = contour(Lat2,Dep2,smean_dw10_glo(:,depth1:depth2),33:.5:37,'k','linewidth',2); stipple(Lat2i,Dep2i
```
