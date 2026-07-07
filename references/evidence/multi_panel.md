# multi_panel Evidence Pack

- Candidate skill: `ipcc-multipanel-figure`
- Matching chunks: 772
- Matching repositories: 93
- Matching files: 526

## Representative Sources

### 1. Atlas / `Atlas\datasets-aggregated-regionally\scripts\computeFigures.R`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `ed29da33d38ae767d19caafd4cde06042cbe00f4`
- Tags: `multi_panel, scatter, time_series`

```text
a1i <- c(WLp10.cmip5[1],WLp10.cordex[1],WLp10.cmip6[1]) a2i <- c(WLp10.cmip5[2],WLp10.cordex[2],WLp10.cmip6[2]) a3i <- c(WLp10.cmip5[3],WLp10.cordex[3],WLp10.cmip6[3]) a4i <- c(WLp10.cmip5[4],WLp10.cordex[4],WLp10.cmip6[4]) ai <- c(p10.cmip5[1], p10.cordex[1], p10.cmip6[1], p10.cmip5[3], p10.cordex[3], p10.cmip6[3],p10.cmip5[5], p10.cordex[5], p10.cmip6[5]) bi <- c(p10.cmip5[2], p10.cordex[2], p10.cmip6[2], p10.cmip5[4], p10.cordex[4], p10.cmip6[4],p10.cmip5[6], p10.cordex[6], p10.cmip6[6]) # di <- c(p10.cmip5[3], p10.cordex[3], p10.cmip6[3], p10.cmip5[6], p10.cordex[6], p10.cmip6[6],p10.cmip5[9], p10.cordex[9], p10.cmip6[9]) dfi <- data.frame("term" = x, "value" = unname(do.call("c", list(ai, bi, a1i, a2i, a3i, a4i)))[ind]) dfi.sub <- dfi dfi.sub$value <- dfi.sub$value * NA dfi.sub[seq(2, nrow(dfi), by = 3), "value"] <- c(p10.cmip5.sub[seq(1, 6, 2)], p10.cmip5.sub[seq(2, 6, 2)], WLp10.c
```

### 2. Box_TS4_Fig1 / `Box_TS4_Fig1\PanelA_Timeseries\Plot_GMSL.m`

- Chunk type: `code`
- Language: `R`
- Commit: `6a7832877157aa79a6cfcec5c4c278267858e94d`
- Tags: `distribution, multi_panel, raster_stripes, time_series`

```text
%% IPCC AR6 Chapter 9: Figure 9.27 (Sea level scenarios) % % Code used to plot pre-processed sea level scenarios % % Plotting code written by Bob Kopp % Processed data provided by Bob Kopp % Other datasets cited in report/caption clear all addpath ../../../Functions/ %savefile='AR6_GMSL_Models_v3.xlsx' fontsize=15; width = 3; start_year=1900; end_year=2150; % Colors updated to match updated SPM colors color_SSP119 = [0 173 207]/255; color_SSP126 = [23 60 102]/255; color_SSP245 = [247 148 32]/255; color_SSP370 = [231 29 37]/255; color_SSP585 = [149 27 30]/255; %% clear hs; fig1=figure('Position', [10 10 800 500]); dw=.6; hs(1)=subplot(2,2,1); hs(2)=subplot(2,2,2); %hs(3)=subplot(2,2,3); %hs(4)=subplot(2,2,4); pos=get(hs,'position'); pos0=pos; dw2=dw-pos{1}(3); pos{2}(1)=pos{2}(1)+dw2-.09; pos{2}(3)=pos{2}(3)-dw2; pos{1}(3)=dw; %pos{3}(3)=pos{1}(3); %pos{4}([1 3])=pos{2}([1 3]); for sss=1:
```

### 3. Chapter-11 / `Chapter-11\code\data_tables.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `d1a3a99f242a568fb4cefc36a038c888a90b9d37`
- Tags: `multi_panel`

```text
import pandas as pd import xarray as xr import yaml import conf def save_simulation_info_raw( fN, da, iav=None, panel="", add_historical=True, add_tas=True, override=None, ): """save raw simulation info from da Parameters ---------- fN : str File name to save the raw data table to da : xr.DataArray DataArray containing all plotted model data and their metadata as non-dimension coordinates. See ``utils.computation.concat_xarray_with_metadata`` iav : xr.DataArray, default: None DataArray containing all interannual variability data. Not used. See ``utils.iav``. panel : str, default: "" Panel where the data appears, e.g. "a" add_historical : bool, default: True If the historical simulation should be added for each projection. The exp="historical" information is lost for the concatenated simulations. add_tas : bool, default: True Add varn="tas" for each simulation (also adds historical simula
```

### 4. Chapter-2_Fig02 / `Chapter-2_Fig02\IPCC_Ch2_plot_volc_solar_RF_Final.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `19a2e1599f6e5aee540e4ac33d79f034a17ef49a`
- Tags: `color_style, multi_panel, time_series`

```text
% IPCC Ch 2 plot volcanic and solar ERF % Author: Matthew Toohey % Created February 2019-June 2021 %% definitions data_dir='C:\Users\mat897\work\Projects\IPCC'; fig_save_dir='C:\Users\mat897\work\Projects\IPCC\'; volc_file=[data_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls']; solar_tsi_file=[data_dir 'IPCC_AR6_solar_TSI_v3.xls']; % colors ipcc=[127 68 170; 48 79 191; 54 156 232; 36 147 126; 236 209 81; 237 128 55; 204 64 74]./255; cmip=[204 35 35; 37 81 204]./255; orange = [0.8500 0.3250 0.0980]; blue = [ 0 0.4470 0.7410]; %% load data from saved xls files % all data are global mean annual mean values [cm6_ndata, cm6_text, cm6_alldata] = xlsread(volc_file,'CMIP6_hist'); cm6_year=cm6_ndata(:,1); cm6_aod=cm6_ndata(:,2); [evo_ndata, evo_text, evo_alldata] = xlsread(volc_file,'eVolv2k'); evo_year=evo_ndata(:,1); evo_aod=evo_ndata(:,2); [sato_ndata, sato_text, sato_alldata] = xlsread(volc_file,'Sato_2
```

### 5. Chapter-2_Fig03 / `Chapter-2_Fig03\CO2_IPCC_colours_clean.R`

- Chunk type: `code`
- Language: `R`
- Commit: `5078755d5bf97653ae498f204bc55aeaf13b1671`
- Tags: `multi_panel, uncertainty`

```text
#GF 11/11/2020 #Code for Figure 2.3 setwd("") #Data input #gas ice<-read.table (file="ice_core.txt", header=TRUE) #boron sos<-read.table (file="Sosdian.txt", header=TRUE) #from Sosdian et al. 2018 Eleni<-read.table (file ="Anagnostou.txt", header = TRUE)# from Anagnostou et al. 2020 PP<-read.table (file="Plio_Pleisto_Final.txt", header=TRUE) #compiled from De la Vega et al., 2020, Bartoli et al., 2011; Chalk et al. 2017; Hoenisch et al. 2009; Dyez et al., 2018; Raitzsch et al. 2018 #d13C Stoll<-read.table (file="Stoll.txt", header=TRUE) wit<-read.table (file="wit.txt", header=TRUE) AlkComp<-read.table (file="Alkenone compilation.txt", header=TRUE) #other Phan<-read.table (file="PhanCO2F.txt", header=TRUE) # no PSol <200 ppm; taken from Royer compilation June 2015. if no age error = 4% if land, = 0.001 if marine. PhanCO2sm<-read.table (file="PhanCO2sm.exp.txt", header=TRUE) #geological 4 
```

### 6. Chapter-2_Fig08 / `Chapter-2_Fig08\ch02_fig8_plotting_code.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `6d1050b8e871c9910f457818eee4a9c1ffce2551`
- Tags: `multi_panel`

```text
%%% Data for panel (a) %%% list decadal ozone trends for the 27 remote surface sites reported by %%% Cooper et al., 2020, including the dry and moist subsets at Mauna Loa %%% %%% Cooper, O. R., M. G. Schultz, S. Schrder, K.-L. Chang, A. Gaudel, G. Carbajal Bentez, E. Cuevas, %%% M. Frhlich, I. E. Galbally, D. Kubistin, X. Lu, A. McClure-Begley, S. Molloy, P. Ndlec, %%% J. OBrien, S. J. Oltmans, I. Petropavlovskikh, L. Ries, I. Senik, K. Sjberg, S. Solberg, %%% T. G. Spain, W. Spangl, M. Steinbacher, D. Tarasick, V. Thouret, X. Xu (2020), Multi-decadal %%% surface ozone trends at globally distributed remote locations, Elem Sci Anth, 8(1), p.23 %%% DOI: http://doi.org/10.1525/elementa.420 %%% %%% site_number latitude longitude elevation slope p-value surface_slope_decade=[ 1 82.5 -62.5 210 -0.5 0.29 %% 'Alert' 2 78.9 11.9 474 0.3 0.52 %% 'Zeppelin' 3 71.3 -156.6 11 0.8 0.08 %% 'Barrow' 4 6
```

### 7. Chapter-2_Fig12 / `Chapter-2_Fig12\vertical.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `beff84dd7a5e081eb6bfc07985b767a1881f3261`
- Tags: `bar_hist_density, color_style, multi_panel, uncertainty`

```text
# Build up output filename # Take arbitrary (first) filename to determine order of filename parts one_filename = os.path.basename(data[0][1]) plot_filename = "_".join( [part for part in one_filename[:-3].split("_") if part in common_fn_parts] ) # Remove variable names from filename possible_var_strings = [ "bending_angle", "optimized_bending_angle", "refractivity", "dry_temperature", "dry_pressure", "density", "temperature", "pressure", "specific_humidity", "geopotential_height", ] # Var names might or might not be part of filename for ss in possible_var_strings: plot_filename = plot_filename.replace("_" + ss, "") # Add actual varname now plot_filename = plot_filename + "_" + var_to_plot.replace("_anomalies", "") if any_pres_mapping: plot_filename = plot_filename + "_" + method_pres_to_alt if filename_prefix: plot_filename = f"{filename_prefix}_{plot_filename}" data_types = sorted(list(s
```

### 8. Chapter-2_Fig18 / `Chapter-2_Fig18\Fig2.18ERA5uwindtrendx.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `6e2ec059c07b2f82ce5c54b88209617ba9a08b8e`
- Tags: `color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
% ch2_fig18.m % % Description % Generates Figure 2.18 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 2 % % Creator: Daoyi Gong (gdy@bnu.edu.cn) % Creating Date: 19 December 2020 % % computing U wind trend for ERA5 % % Assume a confidence level for computing confidence intervals % pconf=0.9; cn=-1.5; cx=1.5; load BuDRd_18.dat; C=BuDRd_18(:,1:3); mon_str={'01','02','03','04','05','06','07','08','09','10','11','12'}; mon_name={'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'}; for mon_num=1:12; mon_name{mon_num} eval(['load u' mon_str{mon_num}]) end % next mon clf figure % title('Zonal wind trend') for isea=1:4 %[wkdat=u01]; % eval(['wkdat=u' mon_str{mon_num} ';']); % eval(['u_cli=u' mon_str{mon_num} '_cli;']); % DJF; if (isea ==1 ) wkdat=(u12(1:end-1,:,:)+u01(2:end,:,:)+u02(2:end,:,:))/3; u_cli=(u12_cli+u01_cli+u02_cli)/3; ssea={'DJF
```

### 9. Chapter-2_Fig27 / `Chapter-2_Fig27\Figure_2_27.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `debdd5d06b7a5002d4437825663a93fc531e72b4`
- Tags: `bar_hist_density, color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
clear all, close all, clc cd('/Users/boeiradi/Documents/SL_AR6_work/Chap2') addpath('/Users/boeiradi/Documents/SL_AR6_work/Chap2/m_map') addpath('/Users/boeiradi/Library/Application Support/MathWorks/MATLAB Add-Ons/Toolboxes/stipple') %% define colormap jetmean = [ 84 48 5 110 68 15 137 88 25 164 108 35 191 129 44 200 148 79 210 169 113 220 189 147 229 209 180 239 228 215 248 248 247 216 232 231 183 216 213 151 200 195 118 183 178 85 167 160 53 151 143 39 128 119 26 105 95 13 82 71 0 60 48]; jetmean=jetmean(end:-1:1,:)/256; jeterror=jetmean; %% read DW2010 file and variables: DW10 = ('DurackandWijffels_GlobalOceanChanges_19500101-20191231__210122-205355_beta.nc'); time = ncread(DW10,'time'); depth = ncread(DW10,'depth'); lon = ncread(DW10,'longitude'); lat = ncread(DW10,'latitude'); salt_mean = ncread(DW10,'salinity_mean'); salt_change = ncread(DW10,'salinity_change')/7; % change unit fr
```

### 10. Chapter-2_Fig27 / `Chapter-2_Fig27\Figure_2_27.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `debdd5d06b7a5002d4437825663a93fc531e72b4`
- Tags: `bar_hist_density, color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
% dw vertical section % changes ax2 = subplot(3,1,2); pcolor(Lat1,Dep1,schg_dw10_glo(:,1:depth1)); shading flat; caxis([scale2(1) scale2(2)]); hold on; axis ij; colormap(ax2,jetmean) contour(Lat1,Dep1,smean_dw10_glo(:,1:depth1),[34.25 34.75 35.25 35.75 36.25 36.75],'k','linewidth',1); [c,h] = contour(Lat1,Dep1,smean_dw10_glo(:,1:depth1),33:.5:37,'k','linewidth',2); stipple(Lat1i,Dep1i,mask_sec1i,'color',0.5*[1 1 1],'marker','x','markersize',3) clabel(c,h,'LabelSpacing',100,'fontsize',fonts_c,'fontweight','bold','color','k') ax3 = subplot(3,1,3); pcolor(Lat2,Dep2,schg_dw10_glo(:,depth1:depth2)); shading flat; caxis([scale2(1) scale2(2)]); hold on; axis ij; colormap(ax3,jetmean) contour(Lat2,Dep2,smean_dw10_glo(:,depth1:depth2),[34.25 34.75 35.25 35.75 36.25 36.75],'k','linewidth',1); [c,h] = contour(Lat2,Dep2,smean_dw10_glo(:,depth1:depth2),33:.5:37,'k','linewidth',2); stipple(Lat2i,Dep2i
```

### 11. Chapter-2_Fig29 / `Chapter-2_Fig29\Chapter2_Fig29_code.r`

- Chunk type: `code`
- Language: `R`
- Commit: `19053a5c113e81b49f9564e92f5735a54e08b725`
- Tags: `multi_panel, uncertainty`

```text
#GF 06/01/2021 #script for Figure 2.29 setwd("c:/users/glf1u08/Desktop/RScript/OA IPCC") #files needed Plio.pH<-read.table (file="Plio.pH.txt", header=TRUE) #Pliocene Sos.GR<-read.table (file="Sos.GR.txt", header = TRUE) #Neogene Anag20<-read.table (file="Anag2020.txt", header=TRUE) #Eocene BATS<-read.table (file ="BATS.txt", header = TRUE) #Modern HOTS<-read.table (file = "HOTS.txt", header = TRUE) #Modern modern<-read.table (file="global_modernpH.txt", header=TRUE) #modern averages Shao<-read.table (file="Shao.txt", header =TRUE) #deglacial & Holocene #panel a par (mfrow=c(1,1)) par(mar=c(5,5, 1, 4)) par (oma=c(1,1,1,1)) plot (Sos.GR$Age.myr, Sos.GR$pH50 , yaxt="n", xaxt="n", xlab="", ylab="", cex.axis = 0.8, col="blue", pch=1, las=1, type="n", xlim=c(65,0), ylim=c(7.4, 8.35), cex=0.6) axis (1, at=(seq(0, 65, by=10)),padj=-1, cex.axis=0.8, tck=-0.025) axis (2, at=(seq(7.5, 8.5, by=0.2)
```

### 12. Chapter-2_Fig36 / `Chapter-2_Fig36\Fig_2.36_code.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `f7d6a2fc8cff9d9650a9d8587deec5e952306f55`
- Tags: `color_style, distribution, multi_panel, raster_stripes, time_series`

```text
% normalise according to 1900-1970 [ee,sd]=min(abs(time-1900)); [ee,ed]=min(abs(time-1970)); for i=1:17, proxy_data(i,:)=proxy_data(i,:)-nanmean(proxy_data(i,sd:ed)); proxy_data(i,:)=proxy_data(i,:)/nanstd(proxy_data(i,sd:ed)); end % compar with obs SOI % for i =1:17, % cc=corrcoef(proxy_data(i,end-100:end-25),jonesmannrogfig6a(end-100:end-25,2)); % cc0(i)=cc(1,2); % cc=corrcoef(proxy_data(i,end-100:end-25),jonesmannrogfig6a(end-99:end-24,2)); % ccp1(i)=cc(1,2); % cc=corrcoef(proxy_data(i,end-100:end-25),jonesmannrogfig6a(end-101:end-26,2)); % ccm1(i)=cc(1,2); % end k=1; for i=1:length(proxy_data(1,:))-30, proxy_data_std2(:,k)=std(proxy_data(:,i:i+29)'); proxy_data_var2(:,k)=var(proxy_data(:,i:i+29)'); k=k+1; end max_proxy_data_std2=max(proxy_data_std2'); % for i=1:18, % [ii]=find(proxy_data_std2(i,:)==max_proxy_data_std2(i)); % max_time(i)=time(ii+29); % end YMatrix1=proxy_data_var2(1:1
```
