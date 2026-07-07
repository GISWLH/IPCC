# bar_hist_density Evidence Pack

- Candidate skill: `ipcc-bars-density`
- Matching chunks: 305
- Matching repositories: 39
- Matching files: 190

## Representative Sources

### 1. Atlas / `Atlas\datasets-interactive-atlas\04_map_figures.R`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `ed29da33d38ae767d19caafd4cde06042cbe00f4`
- Tags: `bar_hist_density, time_series, uncertainty`

```text
# The intermediate object can be optionally stored as a R data object: # save(delta, file = paste0(out.dir, "delta_", AtlasIndex, "_", scenario, "_", paste(season, collapse = "-"),".rda")) # load(paste0(out.dir, "delta_", AtlasIndex, "_", scenario, "_", paste(season, collapse = "-"),".rda"), verbose = TRUE) # CALCULATE UNCERTAINTY AND PRODUCE HATCHING --------------------------------------------------- # Next uncertainty is calculated (check "../datasets-interactive-atlas/hatching-functions/hatching-functions.R" # for further details on the uncertainty calculation). The outputs are binary C4R grids (0 = uncertain, 1 = certain) # run e.g. spatialPlot(uncer2) to check the uncertainty areas. # (1) signal signal.grid <- signal(hist.s, delta) uncer1 <- aggregateGrid(signal.grid, aggr.mem = list(FUN = signal.ens, th = 66)) # (2) agreement uncer2 <- aggregateGrid(delta, aggr.mem = list(FUN = ag
```

### 2. Box_TS4_Fig1 / `Box_TS4_Fig1\PanelC_milestone\super_legend.r`

- Chunk type: `code`
- Language: `R`
- Commit: `6a7832877157aa79a6cfcec5c4c278267858e94d`
- Tags: `bar_hist_density, color_style`

```text
LEGEND <- function (x, y = NULL, legend, fill = NULL, col = par("col"), pt.col=col, line.col=col, border = "black", lty, lwd, pch, angle = 45, density = NULL, bty = "o", bg = par("bg"), box.lwd = par("lwd"), box.lty = par("lty"), box.col = par("fg"), pt.bg = NA, cex = 1, pt.cex = cex, pt.lwd = lwd, xjust = 0, yjust = 1, x.intersp = 1, y.intersp = 1, adj = c(0, 0.5), text.width = NULL, text.col = par("col"), text.font = NULL, merge = do.lines && has.pch, trace = FALSE, plot = TRUE, ncol = 1, horiz = FALSE, title = NULL, inset = 0, xpd, title.col = text.col, title.adj = 0.5, seg.len = 2) { if (missing(legend) && !missing(y) && (is.character(y) || is.expression(y))) { legend <- y y <- NULL } mfill <- !missing(fill) || !missing(density) if (!missing(xpd)) { op <- par("xpd") on.exit(par(xpd = op)) par(xpd = xpd) } title <- as.graphicsAnnot(title) if (length(title) > 1) stop("invalid 'title'")
```

### 3. Chapter-11 / `Chapter-11\code\hadex3.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `d1a3a99f242a568fb4cefc36a038c888a90b9d37`
- Tags: `bar_hist_density, color_style, map, multi_panel, time_series, uncertainty`

```text
da_valid = find_valid_gridpoints_dunn( da, time=time, last_timestep=last_timestep, minimum_valid=minimum_valid ) return theil_ufunc(da_valid, dim="time", alpha=alpha) def plot_theilslope( theil_slope, theil_sign, ax, title=None, add_colorbar=True, colorbar_kwargs=None, stippling_label="Non-significant", **kwargs, ): """plot theil slope and significance""" no_data_color = "0.8" land_kws = dict(fc=no_data_color, ec="none") if colorbar_kwargs is None: colorbar_kwargs = {} # coastline_kws = dict(color="0.1", lw=1, zorder=1.2) # ax.coastlines(**coastline_kws) # # ax.add_feature(cfeatures.LAND, fc=no_data_color, ec="none") # h = ().plot( # ax=ax, transform=ccrs.PlateCarree(), add_colorbar=False, **kwargs # ) h = plot.one_map_flat( theil_slope * 10, ax=ax, mask_ocean=True, ocean_kws=None, add_coastlines=True, coastline_kws=None, add_land=True, land_kws=land_kws, **kwargs, ) lh1 = plot.text_lege
```

### 4. Chapter-12 / `Chapter-12\Figures\scripts\global_figure_12.4\ETWL_plot.py`

- Chunk type: `code`
- Language: `Jupyter Notebook`
- Commit: `358a09813f5b29ea064a0629c26b030d60c1f972`
- Tags: `bar_hist_density, color_style, map, uncertainty`

```text
# if isinstance(colormap, str): colors = Ngl.read_colormap_file(colormap) else: colors = colormap ninc = len(inc) #len(inc)-1 : n ticks => n-1 colors ; + 2 => left and right colors indcolors = [0] for val in numpy.arange(0, len(colors)-1, float(len(colors)-1)/(ninc+1)).tolist()[1:-1]: indcolors.append(int(val)) indcolors.append(len(colors)-1) cmap = [] for ind in indcolors: cmap.append(colors[ind]) #cmap = colors[indcolors] cmap = colors #print len(cmap), len(inc) #for j in numpy.arange(0,len(lat)-1, 10): for j in range(len(lat)-1): cindex = color_index(TWL[j], inc) mres.gsMarkerColor = cmap[cindex] sid.append(Ngl.add_polymarker(wks,map,lon[j],lat[j],mres)) Ngl.add_polymarker(wks,map,lon[j],lat[j],mres) return def add_labelbar(wks,map,inc,colormap): gsres = Ngl.Resources() # Line resources. txres = Ngl.Resources() # For labeling the label bar. txres.txFontHeightF = 0.015 #txres.txJust = 
```

### 5. Chapter-2_Fig12 / `Chapter-2_Fig12\vertical.py`

- Chunk type: `code`
- Language: `Python`
- Commit: `beff84dd7a5e081eb6bfc07985b767a1881f3261`
- Tags: `bar_hist_density, color_style, multi_panel, uncertainty`

```text
# Build up output filename # Take arbitrary (first) filename to determine order of filename parts one_filename = os.path.basename(data[0][1]) plot_filename = "_".join( [part for part in one_filename[:-3].split("_") if part in common_fn_parts] ) # Remove variable names from filename possible_var_strings = [ "bending_angle", "optimized_bending_angle", "refractivity", "dry_temperature", "dry_pressure", "density", "temperature", "pressure", "specific_humidity", "geopotential_height", ] # Var names might or might not be part of filename for ss in possible_var_strings: plot_filename = plot_filename.replace("_" + ss, "") # Add actual varname now plot_filename = plot_filename + "_" + var_to_plot.replace("_anomalies", "") if any_pres_mapping: plot_filename = plot_filename + "_" + method_pres_to_alt if filename_prefix: plot_filename = f"{filename_prefix}_{plot_filename}" data_types = sorted(list(s
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
- Tags: `bar_hist_density, color_style, map, raster_stripes, time_series, uncertainty`

```text
def plot_chl_trend(ds=None,year1=1998, ver="4.2"): verstr = str(ver.replace(".","")) if ds is None: ds = xr.open_mfdataset("ncfiles/OC-CCI_1998_2018_v42_0000_4320_*") trend = (100 * (ds.slope*12) / (ds.climatology+ds.intercept)).data mask = ds.pvalue.data > 0.05 trend[mask] = np.nan ds["trend"] = (("lat", "lon"), trend) plot_trend(ds) sf_kw = dict(dpi=600, bbox_inches="tight") for ftype in ["png", "pdf", "eps", "svg"]: pl.savefig( f"figs/OC-CCI_Chl_trend_v{verstr}_{year1}-2018.{ftype}", **sf_kw) def plot_hatched_chl_trend(ds=None,year1=1998, ver="4.2", pcut=0.1): verstr = str(ver.replace(".","")) if ds is None: ds = xr.open_mfdataset("ncfiles/OC-CCI_1998_2018_v42_0000_4320_*") trend = (100 * (ds.slope*12) / (ds.climatology+ds.intercept)).data mask = ds.pvalue.data > pcut hatchmask = np.zeros(trend.shape) hatchmask[mask==0] = np.nan #trend[mask] = np.nan ds["trend"] = (("lat", "lon"), tre
```
