# uncertainty Evidence Pack

- Candidate skill: `ipcc-uncertainty-hatching`
- Matching chunks: 455
- Matching repositories: 60
- Matching files: 320

## Representative Sources

### 1. Atlas / `Atlas\datasets-aggregated-regionally\scripts\calculate_regional_means.R`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `ed29da33d38ae767d19caafd4cde06042cbe00f4`
- Tags: `uncertainty`

```text
# calculate_regional_means.R # # Copyright (C) 2021 Santander Meteorology Group (http://meteo.unican.es) # # This work is licensed under a Creative Commons Attribution 4.0 International # License (CC BY 4.0 - http://creativecommons.org/licenses/by/4.0) #' @title Monthly regional area-weighted means for the reference regions #' @description #' This script computes monthly regional area-weighted means for the #' IPCC AR6 reference regions, for each model run in a given CMIP project, #' scenario and variable. Regional means are computed for all grid-points #' (landsea) in the region, and also separately for land and sea grid-points. #' @author M. Iturbide library(sp) library(loadeR) library(transformeR) library(geoprocessoR) # # 1. Set parameters # project <- "CMIP5" scenario <- "historical" # or "rcp45", "rcp85", etc. var <- "tas" vari <- "tas" # NetCDF variable name (usually, vari = var) 
```

### 2. Box_TS4_Fig1 / `Box_TS4_Fig1\PanelA_Timeseries\Plot_GMSL.m`

- Chunk type: `code`
- Language: `R`
- Commit: `6a7832877157aa79a6cfcec5c4c278267858e94d`
- Tags: `time_series, uncertainty`

```text
%Plot the low-confidence process ranges ppp=[]; clear hp hpb; %hplc(1) = patch(Time_Conf_Bounds,Conf_BoundsLCvl,color_SSP585, 'EdgeColor', 'none', 'FaceAlpha', 0.03); hold on; %hplc(2) = patch(Time_Conf_Bounds,Conf_BoundsLCl,color_SSP585, 'EdgeColor', 'none', 'FaceAlpha', 0.03); hold on; collabs={'A','G','L','Q','V','AA','AF'}; %writematrix('Change in global mean sea level (GMSL) in meters compared to 1995-2014 average - FACTS Probabilistic Emulator Product',savefile,'Range','A1'); year=[2005; Time_Conf_Bounds(1:12)]; verylikely_ubound_m=[0; Conf_BoundsLCvl(1:12)]; verylikely_lbound_m=[0; Conf_BoundsLCvl(end-1:-1:end-12)]; likely_ubound_m=[0; Conf_BoundsLCl(1:12)]; likely_lbound_m=[0; Conf_BoundsLCl(end-1:-1:end-12)]; T = table(year,likely_lbound_m,likely_ubound_m,verylikely_lbound_m,verylikely_ubound_m); %writematrix('SSP5-8.5 Low Confidence Processes',savefile,'Range',[cell2mat(collabs
```

### 3. Chapter-11 / `Chapter-11\code\hadex3.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `d1a3a99f242a568fb4cefc36a038c888a90b9d37`
- Tags: `bar_hist_density, color_style, map, multi_panel, time_series, uncertainty`

```text
da_valid = find_valid_gridpoints_dunn( da, time=time, last_timestep=last_timestep, minimum_valid=minimum_valid ) return theil_ufunc(da_valid, dim="time", alpha=alpha) def plot_theilslope( theil_slope, theil_sign, ax, title=None, add_colorbar=True, colorbar_kwargs=None, stippling_label="Non-significant", **kwargs, ): """plot theil slope and significance""" no_data_color = "0.8" land_kws = dict(fc=no_data_color, ec="none") if colorbar_kwargs is None: colorbar_kwargs = {} # coastline_kws = dict(color="0.1", lw=1, zorder=1.2) # ax.coastlines(**coastline_kws) # # ax.add_feature(cfeatures.LAND, fc=no_data_color, ec="none") # h = ().plot( # ax=ax, transform=ccrs.PlateCarree(), add_colorbar=False, **kwargs # ) h = plot.one_map_flat( theil_slope * 10, ax=ax, mask_ocean=True, ocean_kws=None, add_coastlines=True, coastline_kws=None, add_land=True, land_kws=land_kws, **kwargs, ) lh1 = plot.text_lege
```

### 4. Chapter-12 / `Chapter-12\Figures\scripts\CID\CID_AR6regions.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `358a09813f5b29ea064a0629c26b030d60c1f972`
- Tags: `map, uncertainty`

```text
import Ngl, Nio import os, numpy, csv, json from IPython.display import Image from shapely.geometry import Polygon, Point import geopandas import sys region_name = sys.argv[1] # -- Create empty map over region # -- test with and without gray fill over continent #---------------------------------------------------------------------- # Create map of southern tip of South America #---------------------------------------------------------------------- def create_map(wks, region_dict, mpOutlineOn=True): #---Map resources res = Ngl.Resources() # map resources res.nglDraw = False # don't draw map res.nglFrame = False # don't advance frame res.nglMaximize = False res.mpDataBaseVersion = "MediumRes" # better map outlines #res.mpCenterLonF = 145 #res.mpCenterLatF = 0 #res.mpLimitMode = "MaximalArea" if 'Robinson' in region_dict: res.mpProjection = "Robinson" #res.mpEllipticalBoundary = True else: 
```

### 5. Chapter-2_Fig03 / `Chapter-2_Fig03\CO2_IPCC_colours_clean.R`

- Chunk type: `code`
- Language: `R`
- Commit: `5078755d5bf97653ae498f204bc55aeaf13b1671`
- Tags: `multi_panel, uncertainty`

```text
#GF 11/11/2020 #Code for Figure 2.3 setwd("") #Data input #gas ice<-read.table (file="ice_core.txt", header=TRUE) #boron sos<-read.table (file="Sosdian.txt", header=TRUE) #from Sosdian et al. 2018 Eleni<-read.table (file ="Anagnostou.txt", header = TRUE)# from Anagnostou et al. 2020 PP<-read.table (file="Plio_Pleisto_Final.txt", header=TRUE) #compiled from De la Vega et al., 2020, Bartoli et al., 2011; Chalk et al. 2017; Hoenisch et al. 2009; Dyez et al., 2018; Raitzsch et al. 2018 #d13C Stoll<-read.table (file="Stoll.txt", header=TRUE) wit<-read.table (file="wit.txt", header=TRUE) AlkComp<-read.table (file="Alkenone compilation.txt", header=TRUE) #other Phan<-read.table (file="PhanCO2F.txt", header=TRUE) # no PSol <200 ppm; taken from Royer compilation June 2015. if no age error = 4% if land, = 0.001 if marine. PhanCO2sm<-read.table (file="PhanCO2sm.exp.txt", header=TRUE) #geological 4 
```

### 6. Chapter-2_Fig10 / `Chapter-2_Fig10\ploterf.ncl`

- Chunk type: `code`
- Language: `NCL`
- Commit: `c02680421212f290bbf2682860608da84ac7075e`
- Tags: `color_style, map, uncertainty`

```text
; Script “ploterf.ncl” load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl" begin ;wks = gsn_open_wks ("pdf","erf") ;wks = gsn_open_wks ("eps","erf") wks = gsn_open_wks ("ps","erf") gsn_define_colormap(wks,"AR6_Line_Shade") wks@wkOrientation = "landscape" res = True res@vpHeightF= 0.6 ; change aspect ratio of plot res@vpWidthF = 0.7 res@gsnDraw = False res@gsnFrame = False res@tmXBLabelFont=12 res@tmYLLabelFont=12 res@tiYAxisString = "(W m~S~-2~N~)" res@tiYAxisFont=12 res@trXMinF = 1750 res@trXMaxF = 2020. res@trYMinF = -4.9 res@trYMaxF = 2.99 res@tmYRBorderOn = False res@tmXTBorderOn = False res@tmYROn = False res@tmXTOn = False res@tmYLPrecision = 1 res@tiMainFont = 12 res@xyLineThicknessF=3. ;res@gsnMaximize =
```

### 7. Chapter-2_Fig12 / `Chapter-2_Fig12\atmoplots.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `beff84dd7a5e081eb6bfc07985b767a1881f3261`
- Tags: `color_style, uncertainty`

```text
@atmoplots.command() @click.option( "--data", multiple=True, type=click.Tuple([str, click.Path(exists=True)]), help="Label and filepath of data to plot.", ) @click.option( "--var-to-plot", required=True, help="Base variable name to plot, e.g. 'dry_temperature_anomalies'", ) @click.option( "--vertical-dim", default="altitude", show_default=True, type=click.Choice(["altitude", "pressure", "impact_altitude"]), help="The coordinate to be used as y-axis.", ) @click.option( "--vertical-limits", nargs=2, type=float, default=(0, 30000), show_default=True, help="Specify lower and upper limit for vertical dimension. " "In (m) for altitude and (Pa) for pressure vertical dim. " "Example: '0 30000' (m) or '100000 1000' (Pa).", ) @click.option( "--xlim", nargs=2, type=float, help="Overrule x-limits for horizontal axis.", ) @click.option( "--mask-below", type=float, default=None, help="Specify below wh
```

### 8. Chapter-2_Fig18 / `Chapter-2_Fig18\Fig2.18ERA5uwindtrendx.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `6e2ec059c07b2f82ce5c54b88209617ba9a08b8e`
- Tags: `color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
% ch2_fig18.m % % Description % Generates Figure 2.18 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 2 % % Creator: Daoyi Gong (gdy@bnu.edu.cn) % Creating Date: 19 December 2020 % % computing U wind trend for ERA5 % % Assume a confidence level for computing confidence intervals % pconf=0.9; cn=-1.5; cx=1.5; load BuDRd_18.dat; C=BuDRd_18(:,1:3); mon_str={'01','02','03','04','05','06','07','08','09','10','11','12'}; mon_name={'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'}; for mon_num=1:12; mon_name{mon_num} eval(['load u' mon_str{mon_num}]) end % next mon clf figure % title('Zonal wind trend') for isea=1:4 %[wkdat=u01]; % eval(['wkdat=u' mon_str{mon_num} ';']); % eval(['u_cli=u' mon_str{mon_num} '_cli;']); % DJF; if (isea ==1 ) wkdat=(u12(1:end-1,:,:)+u01(2:end,:,:)+u02(2:end,:,:))/3; u_cli=(u12_cli+u01_cli+u02_cli)/3; ssea={'DJF
```

### 9. Chapter-2_Fig23 / `Chapter-2_Fig23\2.23b_MB_figure_FGD__chapter2_jun_28_2021.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `e9c02396ba94f46e70e0a77dd265fe8e59403903`
- Tags: `time_series, uncertainty`

```text
clear all clc format long g %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %% Description % Script to generate the annual and decadal global glacier mass change (Gt yr-1) from 1961 until 2018 % for Figure 2.23. I % Includes the global annual mass balance from Zemp et al. (2019/2020), global mass balance between 2002-2016 % from Wouters et al. (2019), global mass balance between 2006-2015 from SROCC and decadal (2000-2010 and 2010-2020) % global mass balance from Hugonnet et al. (2021) %Ranges show the 90% confidence interval. % script create by Lucas Ruiz (LA chapter 9) for Chapter 2 of AR6 WGI. % Files you need: % IPCC color scheme = 'colorscheme.mat' % Global results of Zemp et al (2019) = 'Zemp_etal_results_global.csv' % Global results of Wouters et al (2019) = 'annual_MB_Gtyr.mat' % File preparated by Romain Hugonnet for Chapter 9 = 'table_hugonnet_regions_10yr_ar6period.xlsx' % shade
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

### 12. Chapter-2_Fig29 / `Chapter-2_Fig29\Chapter2_Fig29_code.r`

- Chunk type: `code`
- Language: `R`
- Commit: `19053a5c113e81b49f9564e92f5735a54e08b725`
- Tags: `multi_panel, uncertainty`

```text
#GF 06/01/2021 #script for Figure 2.29 setwd("c:/users/glf1u08/Desktop/RScript/OA IPCC") #files needed Plio.pH<-read.table (file="Plio.pH.txt", header=TRUE) #Pliocene Sos.GR<-read.table (file="Sos.GR.txt", header = TRUE) #Neogene Anag20<-read.table (file="Anag2020.txt", header=TRUE) #Eocene BATS<-read.table (file ="BATS.txt", header = TRUE) #Modern HOTS<-read.table (file = "HOTS.txt", header = TRUE) #Modern modern<-read.table (file="global_modernpH.txt", header=TRUE) #modern averages Shao<-read.table (file="Shao.txt", header =TRUE) #deglacial & Holocene #panel a par (mfrow=c(1,1)) par(mar=c(5,5, 1, 4)) par (oma=c(1,1,1,1)) plot (Sos.GR$Age.myr, Sos.GR$pH50 , yaxt="n", xaxt="n", xlab="", ylab="", cex.axis = 0.8, col="blue", pch=1, las=1, type="n", xlim=c(65,0), ylim=c(7.4, 8.35), cex=0.6) axis (1, at=(seq(0, 65, by=10)),padj=-1, cex.axis=0.8, tck=-0.025) axis (2, at=(seq(7.5, 8.5, by=0.2)
```
