%######################################################################################################################
% ---------------------------------------------------------------------------------------------------------------------
% This is Matlab code to produce IPCC AR6 WGI Cross Chapter Box 4.1 Fig 1  
% Creator: Ingo Bethke, University of Bergen 
% Contact: ingo.bethke@uib.no
% Last updated on: May 16th, 2023
% ---------------------------------------------------------------------------------------------------------------------
%
% - Code functionality: This script plots a modified version of Figure 2 in Bethke et al., 2017 
% (https://doi.org/10.1038/nclimate3394). It shows the simulated 21st Century evolutions of effective radiative forcing 
% and surface temperature from an Earth system model that is driven with synthetic future volcanic forcing variability. 
% - Input data: Model output from Bethke et al. (2017) provided in AR6_Chapter4_CCBOX41_Fig1_ERFvolc.txt,
% AR6_Chapter4_CCBOX41_Fig1_GMSTvolc.txt, AR6_Chapter4_CCBOX41_Fig1_GMSTzero.txt. 
% - Output variables: The code plots the figure as in the report.
%
% ---------------------------------------------------------------------------------------------------------------------
% Information on the software used
% - Software Version: R2014b (8.4.0.150421) 64-bit (glnxa64)
% - Landing page to access the software: https://matlab.mathworks.com
% - Operating System: GNU/Linux 4.18.0-348.23.1.el8_5.x86_64 #1 SMP Wed Apr 27 15:32:52 UTC 2022
% - Environment required to compile and run: OpenJDK Runtime Environment (build 1.8.0_362-b09)
%  --------------------------------------------------------------------------------------------------------------------
%
%  License: Apache 2.0
% ---------------------------------------------------------------------------------------------------------------------
%######################################################################################################################

% read ERF data
ERF=load('AR6_Chapter2_CCBOX41_Fig1_ERFvolc.txt');
time_ERF=ERF(:,1)';
ERF=(ERF(:,2)-0.2); % remove 0.2 W/m2 ERF from non-volcanic aerosols

% read GMST data and compute anomalies relative to piControl
CLIM_PICONTROL=12.7046; % piControl climatological of GMST of NorESM1 
data_zero=load('AR6_Chapter2_CCBOX41_Fig1_GMSTzero.txt');
data_volc=load('AR6_Chapter2_CCBOX41_Fig1_GMSTvolc.txt');
gmst_zero=data_zero(:,2:end)-CLIM_PICONTROL;
gmst_volc=data_volc(:,2:end)-CLIM_PICONTROL;

% compute 5 and 95 percentiles along ensemble dimensions 
gmst_zero95=quantile(gmst_zero,0.95,2); 
gmst_zero05=quantile(gmst_zero,0.05,2); 
gmst_volc95=quantile(gmst_volc,0.95,2); 
gmst_volc05=quantile(gmst_volc,0.05,2); 
gmst_isec95=min(gmst_zero95,gmst_volc95);
gmst_isec05=max(gmst_zero05,gmst_volc05);

% interpolate annual values to monthly resolution 
YEAR1=data_volc(1,1);
YEARN=data_volc(end,1);
time_ann=data_volc(:,1)+0.5;
time_mon=[(YEAR1+0.5/12):(1/12):(YEARN+11.5/12)];
gmst_zero_mon=interp1(time_ann,gmst_zero,time_mon,'pchip',nan);
gmst_zero95_mon=interp1(time_ann,gmst_zero95,time_mon,'pchip',nan);
gmst_zero05_mon=interp1(time_ann,gmst_zero05,time_mon,'pchip',nan);
gmst_volc_mon=interp1(time_ann,gmst_volc,time_mon,'pchip',nan);
gmst_volc95_mon=interp1(time_ann,gmst_volc95,time_mon,'pchip',nan);
gmst_volc05_mon=interp1(time_ann,gmst_volc05,time_mon,'pchip',nan);
gmst_isec95_mon=interp1(time_ann,gmst_isec95,time_mon,'pchip',nan);
gmst_isec05_mon=interp1(time_ann,gmst_isec05,time_mon,'pchip',nan);

% prepare figure 
figure(1);
clf;
set(gcf,'paperunits','inches','papersize',[11 15],'paperposition',[0 0 9 9],...
    'renderer','painters','color',[1 1 1],'InvertHardcopy','off')
set(gca,'outerposition',[0 0 1 1],'position',[0.1 0.3 0.8 0.45])
set(gca,'fontsize',12,'fontweight','bold','xlim',[2006 2100],'ylim',[0 3.8]); 
hold on

% set colors
c1=[1 0.6 0.4]; % zero spread
c2=[0.4 0.6 1]; % volc spread
c12=(c1+c2)/2; % intersection 

% plot GMST ensemble spreads as filled patches  
ind=find(~isnan(gmst_zero95_mon));
h_spread_zero=patch([time_mon(ind) fliplr(time_mon(ind))],...
                    [gmst_zero95_mon(ind) fliplr(gmst_zero05_mon(ind))],...
                    c1,'edgecolor','none');
h_spread_volc=patch([time_mon(ind) fliplr(time_mon(ind))],...
                    [gmst_volc95_mon(ind) fliplr(gmst_volc05_mon(ind))],...
                    c2,'edgecolor','none');
h_spread_isec=patch([time_mon(ind) fliplr(time_mon(ind))],...
                    [gmst_isec95_mon(ind) fliplr(gmst_isec05_mon(ind))],...
                    c12,'edgecolor','none');

% plot GMST ensemble minmax values as dots
h_minmax_zero=plot(time_ann,max(gmst_zero,[],2),'.','color',c1*0.85,'linewidth',1,'markersize',8);
h_minmax_zero=plot(time_ann,min(gmst_zero,[],2),'.','color',c1*0.85,'linewidth',1,'markersize',8);
h_minmax_volc=plot(time_ann,max(gmst_volc,[],2),'.','color',c2*0.85,'linewidth',1,'markersize',8);
h_minmax_volc=plot(time_ann,min(gmst_volc,[],2),'.','color',c2*0.85,'linewidth',1,'markersize',8);

% plot GMST ensemble means and member 45 as solid lines 
plot(time_mon,gmst_volc_mon(:,45),'color',[0.1 0.1 0.1],'linewidth',1)
h_ensave_zero=plot(time_mon,mean(gmst_zero_mon,2),'color',[0.8 0 0],'linewidth',1.5);
h_ensave_volc=plot(time_mon,mean(gmst_volc_mon,2),'color',[0 0 0.8],'linewidth',1.5);

% plot GMST axis manually 
set(gca,'ycolor','w','ytick',[],'hittest','off','visible','off')
xtick=2010:10:2100;
ytick=[0:0.5:3];
xref=2006.1;
yref=0.001;
xlim=get(gca,'xlim');
ylim=get(gca,'ylim');
plot([2006 2100],[yref yref],'k','linewidth',1.5);
plot([xref xref],[ylim(1) ytick(end)],'-k','linewidth',1.5);
for n=1:length(xtick)
  plot([xtick(n) xtick(n)],[yref yref+0.025],'k','linewidth',1);
  text(xtick(n),yref-0.03,int2str(xtick(n)),'horiz','center',...
       'vert','top','fontweight','bold','fontsize',12);
end
for n=1:length(ytick)
  plot([xref+0.5 xref],[ytick(n) ytick(n)],'-k','linewidth',1)
  text(xref-0.7,ytick(n),sprintf('%3.1f',ytick(n)),...
       'horiz','right','fontweight','bold','fontsize',12);
end
text(xref-6.2,mean(ytick),'Temperature above PI (K)',...
     'horiz','center','vert','bottom','rotation',90,'fontweight','bold','fontsize',12);

% plot GMST legend 
legend([h_ensave_zero,h_spread_zero,h_minmax_zero,h_ensave_volc,h_spread_volc,h_minmax_volc],... 
       'RCP4.5^{no volc} mean','RCP4.5^{no volc} 5-95%','RCP4.5^{no volc} min/max',...
       'RCP4.5^{volc} mean','RCP4.5^{volc} 5-95%','RCP4.5^{volc} min/max','location','southeast');
legend boxoff

% plot GMST title
str=['Impact of eruptions upon 21st Century GSAT projections'];
text(xlim(1)-(xlim(2)-xlim(1))*0.042,3+(ylim(2)-ylim(1))*0.05,'(b)',...
     'fontname','Helvetica','fontweight','normal','fontsize',16,...
     'horiz','left','vert','bottom','color',c2)
text(xlim(1)-(xlim(2)-xlim(1))*0.0,3+(ylim(2)-ylim(1))*0.05,str,...
     'fontname','Helvetica','fontweight','normal','fontsize',16,...
     'horiz','left','vert','bottom','color',c2)

% create ERF axis
axes('position',[0.1 0.14 0.8 0.75],'color','none','yaxislocation','right');
xlim=[2006 2100]; ylim=[-200/3 0];
set(gca,'xlim',xlim,'ylim',ylim,'visible','off')
hold on

% plot ERF as patch 
patch([time_ERF,fliplr(time_ERF)],[ERF;ERF*0]',[0.2 0.2 0.2],'edgecolor',[0.2 0.2 0.2]);

% plot ERF axis manually
ytick=[0 -4 -8 -12];
xref=2006.1;
plot([time_ERF(1) time_ERF(end)],[0 0],'-k','linewidth',1.0);
plot([xref xref],[ytick(1) ytick(end)],'-k','linewidth',1.0);
dtick=0.5;
for n=1:length(ytick)
  plot([xref+0.5 xref],[ytick(n) ytick(n)],'-k','linewidth',1)
  text(xref-0.7,ytick(n),int2str(ytick(n)),'horiz','right','fontweight','bold','fontsize',12);
end
text(xref-6.2,mean(ytick),'ERF (W m^{-2})',...
     'horiz','center','vert','bottom','rotation',90,'fontweight','bold','fontsize',12);

% plot ERF title
str=['Potential low likelihood high impact 21st Century volcanic future'];
text(xlim(1)-(xlim(2)-xlim(1))*0.042,0+(ylim(2)-ylim(1))*0.03,'(a)',...
     'fontname','Helvetica','fontweight','normal','fontsize',16,...
     'horiz','left','vert','bottom','color',c2)
text(xlim(1)-(xlim(2)-xlim(1))*0.0,0+(ylim(2)-ylim(1))*0.03,str,...
     'fontname','Helvetica','fontweight','normal','fontsize',16,...
     'horiz','left','vert','bottom','color',c2)

% save to file
print(gcf,'-depsc2','AR6_Chapter2_CCBOX41_Fig1.eps')
