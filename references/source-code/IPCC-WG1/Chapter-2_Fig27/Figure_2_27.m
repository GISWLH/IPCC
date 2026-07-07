clear all, close all, clc

cd('/Users/boeiradi/Documents/SL_AR6_work/Chap2')

addpath('/Users/boeiradi/Documents/SL_AR6_work/Chap2/m_map')

addpath('/Users/boeiradi/Library/Application Support/MathWorks/MATLAB Add-Ons/Toolboxes/stipple')

%% define colormap

jetmean = [ 84 48 5
110 68 15
137 88 25
164 108 35
191 129 44
200 148 79
210 169 113
220 189 147
229 209 180
239 228 215
248 248 247
216 232 231
183 216 213
151 200 195
118 183 178
85 167 160
53 151 143
39 128 119
26 105 95
13 82 71
0 60 48];
            
jetmean=jetmean(end:-1:1,:)/256;
jeterror=jetmean;

%% read DW2010 file and variables: 
DW10 = ('DurackandWijffels_GlobalOceanChanges_19500101-20191231__210122-205355_beta.nc');
time = ncread(DW10,'time');
depth = ncread(DW10,'depth');
lon = ncread(DW10,'longitude');
lat = ncread(DW10,'latitude');

salt_mean = ncread(DW10,'salinity_mean');
salt_change = ncread(DW10,'salinity_change')/7; % change unit from PSU/50yars to PSY
salt_error = ncread(DW10,'salinity_change_error')/7;

[Lat,Lon] = meshgrid(lat,lon+lon(11));
% swith center of salt maps for plotting:
saltchg = cat(1,squeeze(salt_change(12:end,:,1)),squeeze(salt_change(1:11,:,1)));
saltmean = cat(1,squeeze(salt_mean(12:end,:,1)),squeeze(salt_mean(1:11,:,1)));
salterr = 1.09*1.64485*cat(1,squeeze(salt_error(12:end,:,1)),squeeze(salt_error(1:11,:,1)));

%% Process global zonal mean
schg_dw10_glo   = squeeze(nanmean(salt_change,1));
smean_dw10_glo  = squeeze(nanmean(salt_mean,1));
serr_dw10_glo   = 1.09*1.64485*squeeze(nanmean(salt_error,1));

% dw vertical section
labxy = [-63 1800]; 
labtxy = [-40 1825];

depth1 = 45; depth2 = 66;
[Dep1,Lat1] = meshgrid(depth(1:depth1),lat);
[Dep2,Lat2] = meshgrid(depth(depth1:depth2),lat);

%% mask  for hatching: 
% where salt_change_error in CI is < than 90%
mask_map = salterr>abs(saltchg);
mask_sec1 = serr_dw10_glo(:,1:depth1)>abs(schg_dw10_glo(:,1:depth1));
mask_sec2 = serr_dw10_glo(:,depth1:depth2)>abs(schg_dw10_glo(:,depth1:depth2));

%% Create dimensions with higher resolution for the stippling

Dep1_more = cat(2,[0:5:10],[10:16:500]);
[Dep1i,Lat1i] = meshgrid(Dep1_more,lat);

Dep2_more = cat(2,[500:50:2000]);
[Dep2i,Lat2i] = meshgrid(Dep2_more,lat);

% interpolate mask for hashing
serr_dw10_glo_dep1i = griddata(Lat1,Dep1,serr_dw10_glo(:,1:depth1),Lat1i,Dep1i);
schg_dw10_glo_dep1i = griddata(Lat1,Dep1,schg_dw10_glo(:,1:depth1),Lat1i,Dep1i);

serr_dw10_glo_dep2i = griddata(Lat2,Dep2,serr_dw10_glo(:,depth1:depth2),Lat2i,Dep2i);
schg_dw10_glo_dep2i = griddata(Lat2,Dep2,schg_dw10_glo(:,depth1:depth2),Lat2i,Dep2i);

mask_sec1i = serr_dw10_glo_dep1i>abs(schg_dw10_glo_dep1i);
mask_sec2i = serr_dw10_glo_dep2i>abs(schg_dw10_glo_dep2i);

%% Final fig w/ 2 colorbars

scale1 = [-.05 .05 .01 .05];
scale2 = [-.03 .03 .01 .05];
fonts = 10; fonts_lab1 = 16; fonts_lab2 = 12; fonts_ax = 8; fonts_c = 6;
labxy = [100 30]; 
labtxy = [55 100];
close all, handle = figure('units','centimeters','visible','off','color','w'); set(0,'CurrentFigure',handle);% clmap(27);

% dw10 global surface map
figure
ax1 = subplot(3,1,1); 
m_proj('robinson','lon',[0+lon(11) 360+lon(11)])
% changes
m_pcolor(Lon,Lat,saltchg),shading flat, caxis([-1 1]*scale1(2)); hold on; colormap(ax1,jetmean)
m_contour(Lon,Lat,saltmean,[31.5 32.5 33.5 34.5 35.5 36.5 37.5 38.5],'k','linewidth',0.5); hold on
m_contour(Lon,Lat,saltmean,32:1:38,'k','linewidth',1); 
[x,y]=m_ll2xy(Lon,Lat);
stipple(x,y,mask_map,'color',0.5*[1 1 1],'marker','x','markersize',3)
m_coast('patch',[.8 .8 .8],'edgecolor','k');
lab1t = m_text(labtxy(1),labtxy(1),'(a)', 'fontsize',14);
m_grid('tickdir','out','fontsize',fonts_ax-1.5,'xtick',[-180:60:360],...
                 'ytick',[-90:20:90])  
width1 = 0.46; height1 = 0.38;
col1 = 0.04; 
row3 = 0.6;
set(handle,'Units','centimeters','Position',[0 0 9 8])
set(ax1,'Position',[col1 row3 width1 height1]);
cc1 = colorbar('southoutside','fontsize',8)
xlabel(cc1,'Changes in salinity (1950-2019), PSS-78 per decade','fontsize',10)
set(cc1,'YTick',[scale1(1):scale1(3):scale1(2)])

% dw vertical section
% changes
ax2 = subplot(3,1,2);
pcolor(Lat1,Dep1,schg_dw10_glo(:,1:depth1)); shading flat;  caxis([scale2(1) scale2(2)]); hold on; axis ij; colormap(ax2,jetmean)
contour(Lat1,Dep1,smean_dw10_glo(:,1:depth1),[34.25 34.75 35.25 35.75 36.25 36.75],'k','linewidth',1);
[c,h] = contour(Lat1,Dep1,smean_dw10_glo(:,1:depth1),33:.5:37,'k','linewidth',2);
stipple(Lat1i,Dep1i,mask_sec1i,'color',0.5*[1 1 1],'marker','x','markersize',3)
clabel(c,h,'LabelSpacing',100,'fontsize',fonts_c,'fontweight','bold','color','k')
ax3 = subplot(3,1,3);
pcolor(Lat2,Dep2,schg_dw10_glo(:,depth1:depth2)); shading flat; caxis([scale2(1) scale2(2)]); hold on; axis ij; colormap(ax3,jetmean)
contour(Lat2,Dep2,smean_dw10_glo(:,depth1:depth2),[34.25 34.75 35.25 35.75 36.25 36.75],'k','linewidth',1);
[c,h] = contour(Lat2,Dep2,smean_dw10_glo(:,depth1:depth2),33:.5:37,'k','linewidth',2);
stipple(Lat2i,Dep2i,mask_sec2i,'color',0.5*[1 1 1],'marker','x','markersize',3)
clabel(c,h,'LabelSpacing',100,'fontsize',fonts_c,'fontweight','bold','color','k')
hold on, text(-68,1750,'(b)', 'fontsize',14);
% Resize into canvas
width = .4; height1 = .22; height2 = .35; %include cbar
row1 = .37; row2 = .01;
col1 = .07; 
set(handle,'Units','centimeters','Position',[0 0 9 8]) % Full page width (175mm (17) width x 83mm (8) height) - Back to 16.5 x 6 for proportion
set(ax2,'Position',[col1 row1 width height1]);
set(ax2,'Tickdir','out','fontsize',fonts_ax,'layer','top','box','on', ...
    'ylim',[0 500],'ytick',0:50:500,'yticklabel',{'0','','100','','200','','300','','400','','500'},'yminort','on', ...
    'xlim',[-70 70],'xtick',-70:20:70,'xticklabel',{''},'xminort','on')
set(ax3,'Position',[col1 row2 width height2]);
set(ax3,'Tickdir','out','fontsize',fonts_ax,'layer','top','box','on', ...
    'ylim',[500 2000],'ytick',500:250:2000,'yticklabel',{'','750','1000','1250','1500','1750','2000'},'yminort','on', ...
    'xlim',[-70 70],'xtick',-70:20:70,'xticklabel',{'70S','50S','30S','10S','10N','30N','50N','70N'},'xminort','on')
cc2 = colorbar('southoutside')
xlabel(cc2,'Changes in salinity (1950-2019), PSS-78 per decade','fontsize',10)
set(cc2,'YTick',[scale2(1):scale2(3):scale2(2)])

% subplot ylabel
p1=get(ax2,'position');
p2=get(ax3,'position');
height=p1(2)+p1(4)-p2(2);
ax4=axes('position',[p2(1) p2(2) p2(3) height],'visible','off');
ylab2=ylabel('Pressure/Depth (dbar/m)','visible','on');

f=gcf;
print(gcf, 'Fig_DW10_salt_changes_1950-2019_r600_v2_test.png', '-dpng', '-r600');
print(gcf, 'Fig_DW10_salt_changes_1950-2019_r600_v2_test.eps', '-depsc', '-r600');
