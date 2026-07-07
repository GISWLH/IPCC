%  IPCC Ch 2 plot volcanic and solar ERF
%  Author: Matthew Toohey
%  Created February 2019-June 2021

%% definitions
data_dir='C:\Users\mat897\work\Projects\IPCC';
fig_save_dir='C:\Users\mat897\work\Projects\IPCC\';

volc_file=[data_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'];
solar_tsi_file=[data_dir 'IPCC_AR6_solar_TSI_v3.xls'];

% colors
ipcc=[127 68 170;
48 79 191;
54 156 232;
36 147 126;
236 209 81;
237 128 55;
204 64 74]./255;

cmip=[204 35 35;
37 81 204]./255;

orange = [0.8500    0.3250    0.0980];
blue   = [     0    0.4470    0.7410];


%% load data from saved xls files
%  all data are global mean annual mean values

[cm6_ndata, cm6_text, cm6_alldata] = xlsread(volc_file,'CMIP6_hist');
cm6_year=cm6_ndata(:,1);
cm6_aod=cm6_ndata(:,2);

[evo_ndata, evo_text, evo_alldata] = xlsread(volc_file,'eVolv2k');
evo_year=evo_ndata(:,1);
evo_aod=evo_ndata(:,2);

[sato_ndata, sato_text, sato_alldata] = xlsread(volc_file,'Sato_2002');
sato_year=sato_ndata(:,1);
sato_aod=sato_ndata(:,2);

[pmip_ndata, pmip_text, pmip_alldata] = xlsread(solar_tsi_file,'C14_TSI_PMIP4');
pmip_year=pmip_ndata(:,1);
pmip_tsi=pmip_ndata(:,2);
pmip_tsi_10yrm=pmip_ndata(:,3);

[cm6_solar_ndata, cm6_solar_text, cm6_solar_alldata] = xlsread(solar_tsi_file,'CMIP6_TSI');
cm6_solar_year=cm6_solar_ndata(:,1);
cm6_solar_tsi=cm6_solar_ndata(:,2);
cm6_solar_tsi_10yrm=cm6_solar_ndata(:,3);

[cm5_solar_ndata, cm5_solar_text, cm5_solar_alldata] = xlsread(solar_tsi_file,'CMIP5_TSI');
cm5_solar_year=cm5_solar_ndata(:,1);
cm5_solar_tsi=cm5_solar_ndata(:,2);
cm5_solar_tsi_10yrm=cm5_solar_ndata(:,3);

[cm6u_solar_ndata, cm6u_solar_text, cm6u_solar_alldata] = xlsread(solar_tsi_file,'CMIP6update_TSI');
cm6u_solar_year=cm6u_solar_ndata(:,1);
cm6u_solar_tsi=cm6u_solar_ndata(:,2);
cm6u_solar_dtsi=cm6u_solar_ndata(:,3);
ind=find(cm6_solar_year==1979);
adj=(cm6_solar_tsi(ind)-cm6u_solar_tsi(1));
cm6_solar_tsi_adj=cm6_solar_tsi-adj;
cm6_solar_tsi_10yrm_adj=cm6_solar_tsi_10yrm-adj;
pmip_tsi_10yrm_adj=pmip_tsi_10yrm-adj;
pmip_tsi_adj=pmip_tsi-adj;

%% Figure 1, 10 yr running means, reformat with solar ERF, volca AOD/ERF switched and new scaling for volc AOD

ind=find(cm6_solar_year<2015); % only solar data before 2015 is based on observations

panel_width=0.32;
panel_height=0.36;

gap_in_solar=(0.5838-0.11-panel_height)*(1362.25-1360)/panel_height;
mean_solar=mean(pmip_tsi(find(pmip_year>=1745 & pmip_year<=1765))); 

solmax=1362.75;
solmin=1360.45;

figure

% Solar -500 to present
ax1= axes('Position',[0.1100    0.5838    panel_width    panel_height]);

pind=find(pmip_year>-500);
[AX,H1,~]=plotyy(pmip_year(pind),pmip_tsi_10yrm_adj(pind),0,0);
set(H1,'Color',ipcc(1,:))
hold on
plot(AX(1),cm6_solar_year(ind),cm6_solar_tsi_10yrm_adj(ind),'Color',cmip(2,:))
xlim(AX,[-500 2020])
ylim(AX(1),[solmin solmax])
set(AX(1),'YTick',[1360:0.5:1365],'YColor',[0 0 0])
ylim(AX(2),0.1278*([solmin solmax]-mean_solar))
set(AX(2),'YTick',[-0.1:.05:0.2],'YColor',[0 0 0])
ylabel(AX(2),'Solar ERF (W m^{ -2})')
ylabel(AX(1),'Total Solar Irradiance (W m^{ -2})')
xlabel(AX(1),'Year')
subplot_label('a',0.15);
box(AX(1),'off')
set(AX(2),'xaxisloc','top','xticklabel',[]);
AX(2).XAxis.Visible = 'on';

AX(1).XMinorTick='on';
AX(1).XAxis.MinorTickValues = -500:100:2020;
AX(2).XMinorTick='on';
AX(2).XAxis.MinorTickValues = -500:100:2020;
AX(1).YMinorTick='on';
AX(1).YAxis.MinorTickValues = 1360:0.25:1362.5;
%AX(2).YMinorTick='on';

set(gca,'Clipping','Off')
plot([2020 2020],[solmin solmin-gap_in_solar],'k:')
plot([1850 -500],[solmin solmin-gap_in_solar],'k:')
set(AX(1), 'TickDir', 'out')
set(AX(2), 'TickDir', 'out')
legend({'Jungclaus et al. (2017)' 'Matthes et al. (2017)'},'Location','NorthWest')

% Solar historical (1850-2014)
ax2= axes('Position',[0.1100    0.1100    panel_width    panel_height]);

[AX,a2H1,a2H2]=plotyy(cm5_solar_year,cm5_solar_tsi-5-adj,0,0);
hold on
a2h3=plot(AX(1),cm5_solar_year,cm5_solar_tsi-5-adj,'Color',cmip(1,:));
a2h4=plot(AX(1),cm6_solar_year(ind),cm6_solar_tsi_adj(ind),'Color',cmip(2,:));
plot(AX(1),cm6u_solar_year,cm6u_solar_tsi,'Color',ipcc(2,:))
fill(AX(1),[cm6_solar_year; flipud(cm6_solar_year)],[cm6_solar_tsi_adj-cm6u_solar_dtsi(1); flipud(cm6_solar_tsi_adj+cm6u_solar_dtsi(1))],cmip(2,:),'FaceAlpha',0.2,'EdgeColor','none')
fill(AX(1),[cm6u_solar_year; flipud(cm6u_solar_year)],[cm6u_solar_tsi-cm6u_solar_dtsi; flipud(cm6u_solar_tsi+cm6u_solar_dtsi)], ipcc(6,:),'FaceAlpha',0.2,'EdgeColor','none')

plot(AX(1),cm6_solar_year(ind),cm6_solar_tsi_adj(ind),'Color',cmip(2,:))
plot(AX(1),cm5_solar_year,cm5_solar_tsi-5-adj,'Color',cmip(1,:))
a2h5=plot(AX(1),cm6u_solar_year,cm6u_solar_tsi,'Color',ipcc(6,:));

xlim(AX,[1850 2020])
ylim(AX(1),[solmin solmax])
set(AX(1),'YTick',[1360:0.5:1365],'YColor',[0 0 0])
ylabel(AX(1),'Total Solar Irradiance (W m^{ -2})')
xlabel(AX(1),'Year')
ylim(AX(2),0.1278*([solmin solmax]-mean_solar))
set(AX(2),'YTick',[-0.1:.05:0.2],'YColor',[0 0 0])
ylabel(AX(2),'Solar ERF (W m^{ -2})')
box(AX(1),'off')
set(AX(2),'xaxisloc','top','xticklabel',[]);
AX(2).XAxis.Visible = 'on';

subplot_label('b',0.15);

AX(1).XMinorTick='on';
AX(1).XAxis.MinorTickValues = 1850:10:2020;
AX(2).XMinorTick='on';
AX(2).XAxis.MinorTickValues = 1850:10:2020;
AX(1).TickLength=[0.02 0.05];
AX(2).TickLength=[0.02 0.05];
AX(1).YMinorTick='on';
AX(1).YAxis.MinorTickValues = 1360:0.25:1362.5;
set(AX(1), 'TickDir', 'out')
set(AX(2), 'TickDir', 'out')

set(AX(1),'layer','top')
legend({'CMIP5' 'Matthes et al (2017)' 'CMIP6 Update'},'Location','NorthWest')

% Volcanic -500 to present

gap_in_volc=(0.5838-0.11-panel_height)*(0.62)/panel_height;

ax3= axes('Position',[0.55    0.5838    panel_width    panel_height]);

[AX,H1,~]=plotyy(evo_year,evo_aod,0,0);
set(H1,'Color',ipcc(4,:))
%set(H2,'Color',[0 0 0])
hold(AX(1));
hold(AX(2));
plot(AX(1),cm6_year,cm6_aod,'Color',cmip(2,:))
plot(AX(2),[1650 1650],[7 8],'k')
plot(AX(2),[1650 1680],[7 7],'k')
plot(AX(2),[1650 1680],[8 8],'k')
txt1=text(AX(2),1660,7,'1 Wm^{-2}  ','VerticalAlignment','Bottom','HorizontalAlignment','left');
xlim(AX,[-500 2020])
set(AX(1),'YColor',[0 0 0],'YTick',[0:0.1:0.5])
ylabel('Stratospheric AOD')
ylim(AX(1),[-0.02 0.6])
ylim(AX(2),20*[-0.02 0.6]-0.2644)
set(AX(2),'YTick',[0:2:10],'YTickLabel',[0:-2:-10],'YColor',[0 0 0])
ylabel(AX(2),'Volcanic ERF (W m^{ -2})')
box(AX(1),'off')
set(AX(2),'xaxisloc','top','xticklabel',[]);
AX(2).XAxis.Visible = 'on';
xlabel('Year')
subplot_label('c',0.15);
ax3.XMinorTick='on';
ax3.XAxis.MinorTickValues = -500:100:2020;
AX(2).XMinorTick='on';
AX(2).XAxis.MinorTickValues=-500:100:2020;
AX(1).YMinorTick='on';
AX(1).YAxis.MinorTickValues=0:0.025:0.6;
AX(2).YMinorTick='on';
AX(2).YAxis.MinorTickValues=-0.5:0.5:10;
set(gca,'Clipping','Off')
plot([2020 2020],[-0.02 -0.02-gap_in_volc],'k:')
plot([1850 -500],[-0.02 -0.02-gap_in_volc],'k:')
legend({'Toohey and Sigl, 2017', 'CMIP6'},'Location','North')
set(AX(1), 'TickDir', 'out')
set(AX(2), 'TickDir', 'out')

% Volcanic historical (1850-2016)
ax4= axes('Position',[0.55    0.1100    panel_width    panel_height]);

[AX,H1,H2]=plotyy(sato_year,sato_aod,[-500 -499],[0 0]);
set(H1,'Color',cmip(1,:));
set(H2,'Color',ipcc(4,:));
hold(AX(1));
hold(AX(2));
h3=plot(AX(1),cm6_year,cm6_aod,'Color',cmip(2,:));
plot(AX(2),[1996 1996],[1.5 2.5],'k')
plot(AX(2),[1996 2001],[1.5 1.5],'k')
plot(AX(2),[1996 2001],[2.5 2.5],'k')

xlim(AX(1),[1850 2020]);
xlim(AX(2),[1850 2020]);
set(AX(1),'YColor',[0 0 0],'YTick',[0:0.05:0.15])
ylabel(AX(1),'Stratospheric AOD')
ylim(AX(1),[-.01 0.15]);
ylim(AX(2),20*[-0.01 0.15]-0.2644)
set(AX(2),'YTick',[0:0.5:3],'YTickLabel',[0:-0.5:-3],'YColor',[0 0 0])
ylabel(AX(2),'Volcanic ERF (W m^{ -2})')
box(AX(1),'off')
set(AX(2),'xaxisloc','top','xticklabel',[]);
AX(2).XAxis.Visible = 'on';
xlabel('Year')
%plot(AX(2),[0 2000],[0.1 0.05])
%plot(AX(2),[2007 2007],[2.85 1.85])
%plot(AX(2),[2004 2007],[2.85 2.85],'k')
%plot(AX(2),[2004 2007],[1.85 1.85],'k')
txt2=text(AX(2),1996.5,2,'1 Wm^{-2}  ','VerticalAlignment','Middle','HorizontalAlignment','Left');

subplot_label('d',0.15);
ax4.XMinorTick='on';
ax4.XAxis.MinorTickValues = 1850:10:2020;
AX(2).XMinorTick='on';
AX(2).XAxis.MinorTickValues = 1850:10:2020;
AX(1).TickLength=[0.02 0.05];
AX(2).TickLength=[0.02 0.05];
AX(1).YMinorTick='on';
AX(1).YAxis.MinorTickValues=0.01:0.01:0.14;
AX(2).YMinorTick='on';
AX(2).YAxis.MinorTickValues=-0.25:0.25:2.5;
set(AX(1), 'TickDir', 'out')
set(AX(2), 'TickDir', 'out')
leg=legend(ax4,[H2 h3 H1],{'Toohey and Sigl (2017)', 'CMIP6', 'Sato et al. (1999)'},'Location','North');

set(findall(gcf,'-property','FontSize'),'FontSize',7)
legend(ax1,{'Jungclaus et al. (2017)' 'Matthes et al. (2017)'},'Location','NorthWest','FontSize',6)
legend(ax2,[a2h3 a2h4 a2h5],{'Lean (2000)' 'Matthes et al. (2017)' 'Matthes et al. updated'},'Location','NorthWest','FontSize',6)
leg3=legend(ax3,{'Toohey and Sigl (2017)', 'Luo (2018)'},'Location','North','FontSize',6);
leg3p=get(leg3,'Position');
set(leg3,'Position',[leg3p(1)-0.045 leg3p(2:4)])
leg=legend(ax4,[h3 H1],{'Luo (2018)', 'Sato et al. (1993)'},'Location','North','FontSize',6);
set(txt1,'FontSize',6)
set(txt2,'FontSize',6)

set(gcf,'WindowStyle','normal','paperUnits','centimeters','PaperPosition',[0 0 18 8])
print(gcf,'-r200','-dpng',[fig_save_dir 'Forcing_figure_4panel_Final']);

print(gcf,'-depsc2',[fig_save_dir 'Forcing_figure_4panel_Final']);

function [x y]= subplot_label(text_in,xshift)
% subplot_label

x0=get(gca,'XLim');
y0=get(gca,'YLim');

x=x0(1)-(x0(2)-x0(1))*xshift;
y=y0(2);

text(x,y,text_in,'FontWeight','bold','VerticalAlignment','Middle')
end

