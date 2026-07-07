# time_series Evidence Pack

- Candidate skill: `ipcc-timeseries-plot`
- Matching chunks: 692
- Matching repositories: 90
- Matching files: 414

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

### 3. Chapter-11 / `Chapter-11\code\hadex3.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `d1a3a99f242a568fb4cefc36a038c888a90b9d37`
- Tags: `bar_hist_density, color_style, map, multi_panel, time_series, uncertainty`

```text
da_valid = find_valid_gridpoints_dunn( da, time=time, last_timestep=last_timestep, minimum_valid=minimum_valid ) return theil_ufunc(da_valid, dim="time", alpha=alpha) def plot_theilslope( theil_slope, theil_sign, ax, title=None, add_colorbar=True, colorbar_kwargs=None, stippling_label="Non-significant", **kwargs, ): """plot theil slope and significance""" no_data_color = "0.8" land_kws = dict(fc=no_data_color, ec="none") if colorbar_kwargs is None: colorbar_kwargs = {} # coastline_kws = dict(color="0.1", lw=1, zorder=1.2) # ax.coastlines(**coastline_kws) # # ax.add_feature(cfeatures.LAND, fc=no_data_color, ec="none") # h = ().plot( # ax=ax, transform=ccrs.PlateCarree(), add_colorbar=False, **kwargs # ) h = plot.one_map_flat( theil_slope * 10, ax=ax, mask_ocean=True, ocean_kws=None, add_coastlines=True, coastline_kws=None, add_land=True, land_kws=land_kws, **kwargs, ) lh1 = plot.text_lege
```

### 4. Chapter-12 / `Chapter-12\Figures\scripts\Coastal_recession_by_AR6_region\Compute_averages_AR6_regions_Coastal_recession.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `358a09813f5b29ea064a0629c26b030d60c1f972`
- Tags: `time_series`

```text
#for i in np.arange(0,500000,100): # -- Retrieve coastal recession data # ----------------------------------------------------------------- print 'Reading coastal recession data for ',scenario,horizon coastal_data = [] median_list = [] q5_list = [] q95_list = [] points_list = [] lons_list = [] lats_list = [] with open(filename) as csvfile: spamreader = csv.reader(csvfile, delimiter=',') i = 0 for row in spamreader: print i lon = float(row[1] lat = float(row[0] lons_list.append(lon) lats_list.append(lat) points_list.append( Point(lon, lat) ) median_list.append( float(row[5]) ) q5_list.append( float(row[3]) ) q95_list.append( float(row[7]) ) ##for subregion in regions.keys(): ## found_domain = False ## if is_in_AR6_region(lon,lat,regions[subregion]): ## found_domain = True ## regions_values[subregion]['median'].append(float(row[5])) ## regions_values[subregion]['q5'].append(float(row[3])) 
```

### 5. Chapter-2_Fig02 / `Chapter-2_Fig02\IPCC_Ch2_plot_volc_solar_RF_Final.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `19a2e1599f6e5aee540e4ac33d79f034a17ef49a`
- Tags: `color_style, multi_panel, time_series`

```text
% IPCC Ch 2 plot volcanic and solar ERF % Author: Matthew Toohey % Created February 2019-June 2021 %% definitions data_dir='C:\Users\mat897\work\Projects\IPCC'; fig_save_dir='C:\Users\mat897\work\Projects\IPCC\'; volc_file=[data_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls']; solar_tsi_file=[data_dir 'IPCC_AR6_solar_TSI_v3.xls']; % colors ipcc=[127 68 170; 48 79 191; 54 156 232; 36 147 126; 236 209 81; 237 128 55; 204 64 74]./255; cmip=[204 35 35; 37 81 204]./255; orange = [0.8500 0.3250 0.0980]; blue = [ 0 0.4470 0.7410]; %% load data from saved xls files % all data are global mean annual mean values [cm6_ndata, cm6_text, cm6_alldata] = xlsread(volc_file,'CMIP6_hist'); cm6_year=cm6_ndata(:,1); cm6_aod=cm6_ndata(:,2); [evo_ndata, evo_text, evo_alldata] = xlsread(volc_file,'eVolv2k'); evo_year=evo_ndata(:,1); evo_aod=evo_ndata(:,2); [sato_ndata, sato_text, sato_alldata] = xlsread(volc_file,'Sato_2
```

### 6. Chapter-2_Fig07 / `Chapter-2_Fig07\bams_oz_zonalmean_v2_1964.pro`

- Chunk type: `code`
- Language: `IDL`
- Commit: `dd511f09d7f94476434c5c2c919fd3e1509baeca`
- Tags: `color_style, time_series`

```text
y0=min(yy) y1=max(yy) yr=y0+indgen(y1-y0+1) n=(y1-y0+1) fyr=yr+( (month1+month0)*0.5-.5 )/12. mo=fix(yr) wts=cos(!dtor*lat) nc=-1 oz=fltarr(n)*0. for iy=y0,y1 do begin i=iy-y0 nc=nc+1 nd=where(yy eq iy and mm ge month0 and mm le month1,nmt) nl=where (lat ge latmin and lat le latmax,nlt) oz(nc)=0. ;if iy eq 1978 then stop if nmt gt 0 and nlt gt 0 then begin mwts=fltarr(nlt,nmt)*0. moz=mwts*0. nom=0 for k=0,nmt-1 do begin if (max(mat(nl,nd(k))) gt oz_threshold) then nom=nom+1 mwts(*,k)=wts(nl) moz(*,k)=mat(nl,nd(k)) endfor nr=where(moz le oz_threshold,nrt) if nrt gt 0. then begin mwts(nr)=0. moz(nr)=0. endif oz(nc)=total(mwts*moz)/total(mwts) if (nom+0.)/(month1-month0+1.) le 0.8 then oz(nc)=0. print,iy,(nom+0.)/(month1-month0+1.),oz(nc) endif endfor nr=where(oz gt 0,nrt) fyr=fyr(nr) mo=mo(nr) oz=oz(nr) end pro read_modv8annual,fle,yr,toz read_fle,fle,dta,header=4 n=n_elements(dta(0,*)) to
```

### 7. Chapter-2_Fig08 / `Chapter-2_Fig08\ch02_fig8_plotting_code.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `6d1050b8e871c9910f457818eee4a9c1ffce2551`
- Tags: `color_style, multi_panel, time_series`

```text
%%% Data for panel (b) %%% List the decadal ozone trends for the 7 %%% IAGOS regions in the upper troposphere, from Cohen et al. [2018] %%% %%% Cohen, Y., et al. (2018), Climatology and long-term evolution of ozone and carbon monoxide %%% in the upper troposphere-lower stratosphere (UTLS) at northern midlatitudes, as seen by IAGOS %%% from 1995 to 2013, Atmos. Chem. Phys., 18, 5415-5453, https://doi.org/10.5194/acp-18-5415-2018, 2018. %%% Eastern USA %%% North Atlantic %%% Europe %%% Western Mediterranean %%% Middle East %%% Siberia %%% Northeast Asia %%% latitude, longitude, altitude map_site_info_uppertrop =[ 43 -75 12000 55 -35 12000 50 0 12000 40 5 12000 40 40 12000 58 80 12000 40 125 12000 ]; iagos_uppertrop_slope_decade=[ 3.4 %% p=0.01 2.4 %% p=0.07, personal communication from lead-author Y. Cohen on December 19, 2019 3.1 %% p<0.01 4.2 %% p<0.01 2.5 %% p=0.04 3.7 %% p<0.01 4.5 %% 
```

### 8. Chapter-2_Fig12 / `Chapter-2_Fig12\vertical.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `beff84dd7a5e081eb6bfc07985b767a1881f3261`
- Tags: `bar_hist_density, color_style, scatter, time_series, uncertainty`

```text
if "scatter" in pconf and pconf["scatter"]: ax.plot( regr_params["regr"].values, regr_params["regr"][v_dim].values * v_factor, label=key, color=color, alpha=0.5, marker="o", ) else: ax.plot( regr_params["regr"].values, regr_params["regr"][v_dim].values * v_factor, label=key, color=color, alpha=0.9, **pconf["plot_kwargs"] if "plot_kwargs" in pconf else {}, ) if errorbar: ax.errorbar( regr_params["regr"].values, regr_params["regr"][v_dim].values * v_factor, # label='95% conf. interval', xerr=regr_params["conf_interv_95"], color=color, alpha=0.4, ) idx += 1 if add_title: titles = list(set(title_l)) if len(titles) > 1: title_cnt = Counter(title_l) title_mostcommon = title_cnt.most_common(1) title = title_mostcommon[0][0] logger.debug( f"Could not uniquely determine title string, found: {titles}; " f"use the most common one: {title}" ) else: title = titles[0] ax.set_title(title) hh, ll = ax.g
```

### 9. Chapter-2_Fig13 / `Chapter-2_Fig13\time_series_global_ave_q_rh.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `7c8cc2dcd1d860076832c34b90e3c3ae2e292521`
- Tags: `color_style, time_series`

```text
function createfigure(X1, YMatrix1) %CREATEFIGURE(X1, YMatrix1) % X1: vector of x data % YMATRIX1: matrix of y data % Create figure figure1 = figure('PaperUnits','centimeters','PaperSize',[150 100],... 'Color',[1 1 1]); % Create axes axes1 = axes('Parent',figure1,... 'Position',[0.13 0.2 0.78 0.7]); hold(axes1,'on'); ax = gca; ax.LineWidth = 2; set(gcf,'Position',[200,200,1000,600],'PaperPositionMode','Auto') load('qrh2.mat'); t=qrh(:,1); % Create multiple lines using matrix input to plot plot1 = plot(t,qrh(:,[2:6]),'LineWidth',3,'Parent',axes1); set(plot1(1),'LineWidth',3,'Color',[0.3294 0.5725 0.8039],'DisplayName','JRA55'); set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0],'DisplayName','ERA5'); set(plot1(3),'LineWidth',3,'Color',[0 0.2039 0.4000],'DisplayName','20CRv3'); set(plot1(4),'LineWidth',3,'Color',[0 0 0],'DisplayName','HadISDH'); set(plot1(5),'LineWidth',1,'LineStyle','--
```

### 10. Chapter-2_Fig15 / `Chapter-2_Fig15\time_series_global_ave_precip_decadal.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `df6adbb8b8c99a7824691d3e2538841112102f98`
- Tags: `time_series`

```text
load('precipglobalavedata2019_4.mat'); t=precipglobalaverage([2 11],1); % Create multiple lines using matrix input to plot plot1 = plot(t,precipglobalaverage([2 11],[6:10]),'LineWidth',3,'Parent',axes1); set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020],'DisplayName',''); set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0],'DisplayName','GPCC V2020'); set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039],'DisplayName','CRU TS 4.04'); set(plot1(4),'LineWidth',3,'Color',[0 0 0],'DisplayName','GHCN V4'); set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0],'DisplayName','GPCP V2.3'); hold on t=precipglobalaverage([12 21],1); plot1 = plot(t,precipglobalaverage([12 21],[6:10]),'LineWidth',3,'Parent',axes1); set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020],'DisplayName',''); set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0],
```

### 11. Chapter-2_Fig18 / `Chapter-2_Fig18\Fig2.18ERA5uwindtrendx.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `6e2ec059c07b2f82ce5c54b88209617ba9a08b8e`
- Tags: `color_style, map, multi_panel, raster_stripes, time_series, uncertainty`

```text
% ch2_fig18.m % % Description % Generates Figure 2.18 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 2 % % Creator: Daoyi Gong (gdy@bnu.edu.cn) % Creating Date: 19 December 2020 % % computing U wind trend for ERA5 % % Assume a confidence level for computing confidence intervals % pconf=0.9; cn=-1.5; cx=1.5; load BuDRd_18.dat; C=BuDRd_18(:,1:3); mon_str={'01','02','03','04','05','06','07','08','09','10','11','12'}; mon_name={'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'}; for mon_num=1:12; mon_name{mon_num} eval(['load u' mon_str{mon_num}]) end % next mon clf figure % title('Zonal wind trend') for isea=1:4 %[wkdat=u01]; % eval(['wkdat=u' mon_str{mon_num} ';']); % eval(['u_cli=u' mon_str{mon_num} '_cli;']); % DJF; if (isea ==1 ) wkdat=(u12(1:end-1,:,:)+u01(2:end,:,:)+u02(2:end,:,:))/3; u_cli=(u12_cli+u01_cli+u02_cli)/3; ssea={'DJF
```

### 12. Chapter-2_Fig23 / `Chapter-2_Fig23\2.23b_MB_figure_FGD__chapter2_jun_28_2021.m`

- Chunk type: `code`
- Language: `MATLAB`
- Commit: `e9c02396ba94f46e70e0a77dd265fe8e59403903`
- Tags: `time_series, uncertainty`

```text
clear all clc format long g %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %% Description % Script to generate the annual and decadal global glacier mass change (Gt yr-1) from 1961 until 2018 % for Figure 2.23. I % Includes the global annual mass balance from Zemp et al. (2019/2020), global mass balance between 2002-2016 % from Wouters et al. (2019), global mass balance between 2006-2015 from SROCC and decadal (2000-2010 and 2010-2020) % global mass balance from Hugonnet et al. (2021) %Ranges show the 90% confidence interval. % script create by Lucas Ruiz (LA chapter 9) for Chapter 2 of AR6 WGI. % Files you need: % IPCC color scheme = 'colorscheme.mat' % Global results of Zemp et al (2019) = 'Zemp_etal_results_global.csv' % Global results of Wouters et al (2019) = 'annual_MB_Gtyr.mat' % File preparated by Romain Hugonnet for Chapter 9 = 'table_hugonnet_regions_10yr_ar6period.xlsx' % shade
```
