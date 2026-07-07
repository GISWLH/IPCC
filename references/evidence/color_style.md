# color_style Evidence Pack

- Candidate skill: `ipcc-colormap-style`
- Matching chunks: 929
- Matching repositories: 70
- Matching files: 686

## Representative Sources

### 1. Atlas / `Atlas\datasets-aggregated-regionally\scripts\computeStripes.R`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `ed29da33d38ae767d19caafd4cde06042cbe00f4`
- Tags: `color_style, raster_stripes`

```text
# computeStripes.R # # Copyright (C) 2021 Santander Meteorology Group (http://meteo.unican.es) # # This work is licensed under a Creative Commons Attribution 4.0 International # License (CC BY 4.0 - http://creativecommons.org/licenses/by/4.0) #' @title Compute temperature and precipitation stripes plots #' @description Compute temperature and precipitation stripes plots from #' files of this repository (datasets-aggregated-regionally). Use argument #' ... for additional graphical arguments of the levelplot function #' (library lattice). #' @param project Choices are: CMIP6, CMIP5 and CORDEX. #' @param var Choices are: tas and pr. #' @param experiment Depending of the chosen projects, experiment choices are: #' rcp26, rcp45, rcp85, "ssp126", "ssp245", "ssp370", "ssp585". #' @param season Numeric indicating seasons (e.g. 1:12 is for annual data). Use c(12, 1, 2) #' for winter. #' @param ar
```

### 2. Box_TS4_Fig1 / `Box_TS4_Fig1\PanelA_Timeseries\Plot_GMSL.m`

- Chunk type: `code`
- Language: `R`
- Commit: `6a7832877157aa79a6cfcec5c4c278267858e94d`
- Tags: `color_style, distribution, raster_stripes, time_series, uncertainty`

```text
%Plot the medium-confidence process scenarios pp=[]; for sss=[2 4] pp(sss)=plot([2005 ; timec],[0 ; SL_quantc{sss}(:,3)/1000],'Color',scencolors(sss,:),'LineStyle','-', 'LineWidth', width); hold on end hplc(1) = plot(Time_Conf_Bounds(1:end/2),Conf_BoundsLCvl(1:end/2),'Color',color_SSP585, ... 'LineStyle',':','LineWidth',width/4); hold on; hplc(2) = plot(Time_Conf_Bounds(1:end/2),Conf_BoundsLCl(1:end/2),'Color',color_SSP585, ... 'LineStyle','--','LineWidth',width/4); hold on; % outstruct.historical_time=historical.t(:); % outstruct.historical=historical.y(:)/1000; % outstruct.historical_boundstime=historicalextrap.t(:); % outstruct.historical_Likely_lbound=(historical.y(:)-historical.dy(:))/1000; % outstruct.historical_Likely_ubound=(historical.y(:)+historical.dy(:))/1000; % % %Plot the historical data and extrapolation %ph=plot(historical.t,historical.y/1000,'k', 'LineWidth', width); %ph
```

### 3. Chapter-11 / `Chapter-11\code\conf.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `d1a3a99f242a568fb4cefc36a038c888a90b9d37`
- Tags: `color_style`

```text
import os.path as path import numpy as np import fixes from filefinder import FileFinder from utils.cmip_conf import _cmip_conf # CONFIGURATION FILE # ============================================================================= # Folders for the postprocessed data and figures # ============================================================================= root_folder_postprocessed_data = "../data/" root_folder_figures = "../figures/" def figure_filename(name, *subfolders): """create filenames for figures Parameters ---------- name : str File name of the figure *subfolders : list of str Folders of the figure. """ folders = (root_folder_figures,) + subfolders return path.join(*folders, name) # ============================================================================= # Reference Period # ============================================================================= ANOMALY_YR_START = 185
```

### 4. Chapter-12 / `Chapter-12\Figures\scripts\global_figure_12.4\ETWL_plot.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `358a09813f5b29ea064a0629c26b030d60c1f972`
- Tags: `color_style, map`

```text
import Ngl, Nio import os, numpy from IPython.display import Image import sys baseline = sys.argv[1] future = sys.argv[2] horizon = int(sys.argv[3]) rcp = sys.argv[4] title = sys.argv[5] label = sys.argv[6] trim_figure = sys.argv[7] figformat = sys.argv[8] #---------------------------------------------------------------------- # nint returns the nearest integer to a given floating value. #---------------------------------------------------------------------- def nint(r): if (abs(int(r)-r) < 0.5): return int(r) else: if (r >= 0.): return int(r)+1 else: return int(r)-1 #---------------------------------------------------------------------- # Create map #---------------------------------------------------------------------- def create_map(wks, mpOutlineOn=False): #---Map resources res = Ngl.Resources() # map resources res.nglDraw = False # don't draw map res.nglFrame = False # don't advance
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

### 8. Chapter-2_Fig09 / `Chapter-2_Fig09\plotfgd.ncl`

- Chunk type: `code`
- Language: `Fortran`
- Commit: `4413efb5552423d7e0e4330387b0cdf593dd3638`
- Tags: `color_style, map`

```text
; Script “plotfgd.ncl” load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl" begin var="su" ;var="bc" wks = gsn_open_wks ("eps","icesod"+var) ;wks = gsn_open_wks ("pdf","icesod"+var) gsn_define_colormap(wks,"AR6_Line_Shade") wks@wkOrientation = "landscape" res = True res@vpHeightF= 0.4 ; change aspect ratio of plot res@vpWidthF = 0.7 res@gsnDraw = False res@gsnFrame = False res@tmYRBorderOn = False res@tmXTBorderOn = False res@tmYROn = False res@tmXTOn = False res@tmXBLabelFont=12 res@tmYLLabelFont=12 res@txFontHeightF = 0.015 if ( var.eq."su" ) then res@gsnLeftString = "(a) Non-sea salt sulfate" res@tiYAxisString = "(ng g~S~-1~N~)" else res@gsnLeftString = "(b) Refractory black carbon" res@tiYAxisString = "(ng g~
```

### 9. Chapter-2_Fig09 / `Chapter-2_Fig09\plotmimoanf.ncl`

- Chunk type: `code`
- Language: `Fortran`
- Commit: `4413efb5552423d7e0e4330387b0cdf593dd3638`
- Tags: `color_style, map`

```text
; Script “plotmimoanf.ncl” load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" begin fine=0 if ( fine.eq.1 ) then wks = gsn_open_wks("pdf","mimoanf") ; open a pdf file ;wks = gsn_open_wks("eps","mimoanf") ; open a pdf file else wks = gsn_open_wks("pdf","mimoan") ; open a pdf file ;wks = gsn_open_wks("eps","mimoan") ; open a pdf file end if a = addfile("mimof.nc","r") if ( fine.eq.1 )then tmm = a->tmf smm = a->smf else tmm = a->tmm smm = a->smm end if ;gsn_define_colormap(wks,"BrownBlue12") ;gsn_define_colormap(wks,"CBR_coldhot") ;gsn_define_colormap(wks,"AR6_Temp_10") gsn_define_colormap(wks,"chem_div") ;gsn_define_colormap(wks,"GreenMagenta16") ;gsn_define_colormap(wks,"BlueDarkRed18") ; txres = True ;txres@txFont=12 txres@txFontHeightF = 0.03 ; font smaller. default big txres@txJust="CenterCenter" gsn_text_ndc(wks,"% yr~S~-1~
```

### 10. Chapter-2_Fig10 / `Chapter-2_Fig10\ploterf.ncl`

- Chunk type: `code`
- Language: `NCL`
- Commit: `c02680421212f290bbf2682860608da84ac7075e`
- Tags: `color_style, map, uncertainty`

```text
; Script “ploterf.ncl” load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl" begin ;wks = gsn_open_wks ("pdf","erf") ;wks = gsn_open_wks ("eps","erf") wks = gsn_open_wks ("ps","erf") gsn_define_colormap(wks,"AR6_Line_Shade") wks@wkOrientation = "landscape" res = True res@vpHeightF= 0.6 ; change aspect ratio of plot res@vpWidthF = 0.7 res@gsnDraw = False res@gsnFrame = False res@tmXBLabelFont=12 res@tmYLLabelFont=12 res@tiYAxisString = "(W m~S~-2~N~)" res@tiYAxisFont=12 res@trXMinF = 1750 res@trXMaxF = 2020. res@trYMinF = -4.9 res@trYMaxF = 2.99 res@tmYRBorderOn = False res@tmXTBorderOn = False res@tmYROn = False res@tmXTOn = False res@tmYLPrecision = 1 res@tiMainFont = 12 res@xyLineThicknessF=3. ;res@gsnMaximize =
```

### 11. Chapter-2_Fig12 / `Chapter-2_Fig12\atmoplots.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `beff84dd7a5e081eb6bfc07985b767a1881f3261`
- Tags: `color_style, uncertainty`

```text
@atmoplots.command() @click.option( "--data", multiple=True, type=click.Tuple([str, click.Path(exists=True)]), help="Label and filepath of data to plot.", ) @click.option( "--var-to-plot", required=True, help="Base variable name to plot, e.g. 'dry_temperature_anomalies'", ) @click.option( "--vertical-dim", default="altitude", show_default=True, type=click.Choice(["altitude", "pressure", "impact_altitude"]), help="The coordinate to be used as y-axis.", ) @click.option( "--vertical-limits", nargs=2, type=float, default=(0, 30000), show_default=True, help="Specify lower and upper limit for vertical dimension. " "In (m) for altitude and (Pa) for pressure vertical dim. " "Example: '0 30000' (m) or '100000 1000' (Pa).", ) @click.option( "--xlim", nargs=2, type=float, help="Overrule x-limits for horizontal axis.", ) @click.option( "--mask-below", type=float, default=None, help="Specify below wh
```

### 12. Chapter-2_Fig12 / `Chapter-2_Fig12\ipcc_colors.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `beff84dd7a5e081eb6bfc07985b767a1881f3261`
- Tags: `color_style`

```text
""" Author: Martin Jury © Copyright 2019 Wegener Center / UniGraz """ # Standard Library import os # Third party import matplotlib.colors as mcolors import numpy as np import pandas as pd from pkg_resources import resource_filename _ipcc_colormaps_dir = resource_filename( __name__, os.path.join("data", "IPCC-WG1-colormaps") ) def load_colors( color_table, Ncolors=256, reverse=False, path_to_ctabels=_ipcc_colormaps_dir ): """ loads IPCC color tables according to color_table (str, also listed under colors_dic discrete_colormaps are of maximum Ncolor=21 categorical_colors are returned as np array """ # for sub in ['categorical_colors_rgb_0-255','continuous_colormaps_rgb_0-255','discrete_colormaps_rgb_0-255']: # files = os.listdir(os.path.join(colors_dir_path, sub)) # files = [f[:-4] for f in files if f[-4:] == '.txt'] # print('{}:{}'.format(sub,files)) colors_dic = { "categorical_colors_rgb
```
