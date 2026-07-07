% this script was writtne to load in all ENSO proxies
% described in our  review chapter.
%
% Stahle et al. (1998); Cook (2000); Mann et al. (2000); Evans et al. (2001, 2002); Cook et al. (2008); Braganza et al. (2009); McGregor et al. (2010); Wilson et al. (2010); Li et al. (2011); Emile-Geay et al. 2013a,b; Li et al. (2013) and Tierney et al. (2015) (see Table 1). 
%==================================================


time =1150:2000;

[m,n]=size(time);

proxy_data = NaN*ones(19,n);
obs_data=1900:2000;

%--------------------------------------------------------------------------------------------------------

% first load the stahle et al (1998) reconstructed soi data

%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/stahle_et_al_1998_soi.asc
load predefined_ENSO_proxies/raw_ENSO_PROXIES/stahle_et_al_1998_soi.asc

[ee,sp(1)]=min(abs(stahle_et_al_1998_soi(1,1)-time));
[ee,ep(1)]=min(abs(stahle_et_al_1998_soi(end,1)-time));

proxy_data(1,sp(1):ep(1))=stahle_et_al_1998_soi(:,2)/std(stahle_et_al_1998_soi(:,2))*-1;

%--------------------------------------------------------------------------------------------------------

% now load the cook et al (2000) reconstructed n3 data

%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/cook_2000_n3.asc
load predefined_ENSO_proxies/raw_ENSO_PROXIES/cook_2000_n3.asc

[ee,sp(2)]=min(abs(cook_2000_n3(1,1)-time));
[ee,ep(2)]=min(abs(cook_2000_n3(end,1)-time));

proxy_data(2,sp(2):ep(2))=cook_2000_n3(:,2)/std(cook_2000_n3(:,2));

%--------------------------------------------------------------------------------------------------------

% now load the mann et al (2000) reconstructed n3 data

%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/jonesmannrogfig6a.asc
load predefined_ENSO_proxies/raw_ENSO_PROXIES/jonesmannrogfig6a.asc
[ii]=find(jonesmannrogfig6a(:,3)==-99.99);
jonesmannrogfig6a(ii,3)=NaN;

[ee,sp(3)]=min(abs(jonesmannrogfig6a(1,1)-time));
[ee,ep(3)]=min(abs(jonesmannrogfig6a(end,1)-time));

proxy_data(3,sp(3):ep(3))=jonesmannrogfig6a(:,3)/nanstd(jonesmannrogfig6a(:,3))*-1;

%--------------------------------------------------------------------------------------------------

% now load the coral and tree ring based ssta recon data of evans et al. (2002)
% the coral based ssta recon spans 1800 to 1990
% the tree ring based ssta recon spans 1590 to 1990

%fname=['/Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/evans_ssta_proxy_data.cdf'];
fname=['predefined_ENSO_proxies/raw_ENSO_PROXIES/evans_ssta_proxy_data.cdf'];
lon = ncread(fname,'X');
lat = ncread(fname,'Y');
%Latitudes of grid points : 57.5S to 62.5N by 5. N= 25 points
%Longitudes of grid points : 112.5E to 67.5W by 5. N= 37 points

coral_ssta = ncread(fname,'Pac_ssta_coral.ssta');
tree_ring_ssta = ncread(fname,'Pac_ssta_tree.ssta');
[ii]=find(coral_ssta<-9000); coral_ssta(ii)=NaN;
[ii]=find(tree_ring_ssta<-9000); tree_ring_ssta(ii)=NaN;

% now calculate the n3 region ssta

n3_coral = squeeze(nanmean(nanmean(coral_ssta(20:end,11:14,:),1),2));
n3_tree_ring = squeeze(nanmean(nanmean(tree_ring_ssta(20:end,11:14,:),1),2));

%

[ee,coral_sp]=min(abs(1800-time));
[ee,tr_sp]=min(abs(1590-time));
[ee,coral_ep]=min(abs(1990-time));
sp(4)=coral_sp+1;
ep(4)=coral_ep+1;
sp(5)=tr_sp+1;
ep(5)=coral_ep+1;

proxy_data(4,sp(4):ep(4))=n3_coral/nanstd(n3_coral);
proxy_data(5,sp(5):ep(5))=n3_tree_ring/nanstd(n3_tree_ring);

%----------------------------------------------------------------
% now load the new cook tr data set

%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/new_cook_tr_proxy_data.txt
load predefined_ENSO_proxies/raw_ENSO_PROXIES/new_cook_tr_proxy_data.txt
[ee,new_cook_sp]=min(abs(new_cook_tr_proxy_data(1,1)-time));
[ee,new_cook_ep]=min(abs(new_cook_tr_proxy_data(:,1)-time(end)));

sp(6)=new_cook_sp;
ep(6)=851;

proxy_data(6,sp(6):ep(6))=new_cook_tr_proxy_data(1:new_cook_ep,3)';

%-------------------------------------------------------------------------------------
% now load the enso proxy of Braganza et al (2009)

%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/braganza_et_al_2009
%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/braganza_et_al_2009_1727
load predefined_ENSO_proxies/raw_ENSO_PROXIES/braganza_et_al_2009
load predefined_ENSO_proxies/raw_ENSO_PROXIES/braganza_et_al_2009_1727
[ee,sp(7)]=min(abs(braganza_et_al_2009_1727(1,1)-time));
[ee,ep(7)]=min(abs(braganza_et_al_2009_1727(end,1)-time));

[ee,sp(8)]=min(abs(braganza_et_al_2009(1,1)-time));
[ee,ep(8)]=min(abs(braganza_et_al_2009(end,1)-time));

proxy_data(7,sp(7):ep(7))=braganza_et_al_2009_1727(:,2)/std(braganza_et_al_2009_1727(:,2))*-1;
proxy_data(8,sp(8):ep(8))=braganza_et_al_2009(:,2)/std(braganza_et_al_2009(:,2))*-1;

%------------------------------------------------------------
% now load in the mcgregor et al. data
%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/Unified_ENSO_Proxy_noheader.dat
load predefined_ENSO_proxies/raw_ENSO_PROXIES/Unified_ENSO_Proxy_noheader.dat
[error,sp(9)]=min(abs(time-Unified_ENSO_Proxy_noheader(1,1)));
[error,ep(9)]=min(abs(time-Unified_ENSO_Proxy_noheader(end,1)));
proxy_data(9,sp(9):ep(9))=Unified_ENSO_Proxy_noheader(:,2)';

%--------------------------------------------------------------
% now add Wilson 2010 data
%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/wilson_et_al_2010.dat
load predefined_ENSO_proxies/raw_ENSO_PROXIES/wilson_et_al_2010.dat
[error,sp(10)]=min(abs(time-wilson_et_al_2010(68,1)));
[error,ep(10)]=min(abs(time-wilson_et_al_2010(end,1)));
proxy_data(10,sp(10):ep(10))=wilson_et_al_2010(68:end,2)';

[error,sp(11)]=min(abs(time-wilson_et_al_2010(1,1)));
[error,ep(11)]=min(abs(time-wilson_et_al_2010(end,1)));
proxy_data(11,sp(11):ep(11))=wilson_et_al_2010(:,3)';

%-----------------------------------------------------------
% now load in the new jinboa tree ring data set

%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/jinbao_enso_2011.dat
load predefined_ENSO_proxies/raw_ENSO_PROXIES/jinbao_enso_2011.dat

ii=find(jinbao_enso_2011(:,1)==time(1));
iii=find(jinbao_enso_2011(:,1)==time(end));
sp(12)=1;
ep(12)=851;

proxy_data(12,:)=jinbao_enso_2011(ii:iii,2)';

%-------------------------------------------------------------
% now load in the emile-geay et al 2013 data

%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/emile-gaey_2013.txt
load predefined_ENSO_proxies/raw_ENSO_PROXIES/emile-gaey_2013.txt

emile_gaey_2013_2=flipud(emile_gaey_2013);

[error,sp(13)]=min(abs(time-emile_gaey_2013_2(1,1)));
[error,ep(13)]=min(abs(time-emile_gaey_2013_2(end,1)));
sp(14)=sp(13);
sp(15)=sp(13);
ep(14)=ep(13);
ep(15)=ep(13);

proxy_data(13,sp(13):ep(13))=emile_gaey_2013_2(:,2);
proxy_data(14,sp(14):ep(14))=emile_gaey_2013_2(:,6);
proxy_data(15,sp(15):ep(15))=emile_gaey_2013_2(:,10);

%--------------------------------------------------------------
% now load in Li et al. 2013 data

%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/li_et_al_2013.asc
load predefined_ENSO_proxies/raw_ENSO_PROXIES/li_et_al_2013.asc

[error,sp(16)]=min(abs(time-li_et_al_2013(1,1)));
[error,iii]=min(abs(time(end)-li_et_al_2013(:,1)));
ep(16)=851;

proxy_data(16,sp(16):ep(16))=li_et_al_2013(1:iii,2);

%--------------------------------------------------------------
% now load in the Tierney et al. 2015 data

%load /Users/shaynem/DATA/Paleo/ENSO/predefined_ENSO_proxies/raw_ENSO_PROXIES/tierney_et_al_2015.txt
load predefined_ENSO_proxies/raw_ENSO_PROXIES/tierney_et_al_2015.txt
tierney_et_al_2015_2=flipud(tierney_et_al_2015);

[error,ii]=min(abs(time-tierney_et_al_2015_2(1,1)));
[error,iii]=min(abs(time-tierney_et_al_2015_2(end,1)));
sp(17)=ii+1;
ep(17)=iii+1;

proxy_data(17,sp(17):ep(17))=tierney_et_al_2015_2(:,2);


% normalise according to 1900-1970
[ee,sd]=min(abs(time-1900));
[ee,ed]=min(abs(time-1970));

for i=1:17,
proxy_data(i,:)=proxy_data(i,:)-nanmean(proxy_data(i,sd:ed));
proxy_data(i,:)=proxy_data(i,:)/nanstd(proxy_data(i,sd:ed));
end

% compar with obs SOI
% for i =1:17,
% cc=corrcoef(proxy_data(i,end-100:end-25),jonesmannrogfig6a(end-100:end-25,2));
% cc0(i)=cc(1,2);
% cc=corrcoef(proxy_data(i,end-100:end-25),jonesmannrogfig6a(end-99:end-24,2));
% ccp1(i)=cc(1,2);
% cc=corrcoef(proxy_data(i,end-100:end-25),jonesmannrogfig6a(end-101:end-26,2));
% ccm1(i)=cc(1,2);
% end

k=1;
for i=1:length(proxy_data(1,:))-30,
   proxy_data_std2(:,k)=std(proxy_data(:,i:i+29)');
   proxy_data_var2(:,k)=var(proxy_data(:,i:i+29)');
   k=k+1;
end

max_proxy_data_std2=max(proxy_data_std2');

% for i=1:18,
%    [ii]=find(proxy_data_std2(i,:)==max_proxy_data_std2(i));
%    max_time(i)=time(ii+29);
% end

YMatrix1=proxy_data_var2(1:17,1:end-1);
YMatrix1(18,:)=nanmean(YMatrix1(1:17,:));
YMatrix1(19,:)=prctile(YMatrix1(1:17,:),10);
YMatrix1(20,:)=prctile(YMatrix1(1:17,:),90);
X1=time(31:end-1);

[ee,sp]=min(abs(X1-1600));

figure1 = figure;

axes1 = axes('Parent',figure1,...
    'Position',[0.0690399137001078 0.11 0.553074433656958 0.815]);
hold(axes1,'on');

plot1 = plot(X1,YMatrix1(1:18,:),'Parent',axes1,'LineWidth',0.5);
set(plot1(1),'DisplayName','Stahle et al. (1988)','Color',[0.65 0.65 0.65]);
set(plot1(2),'DisplayName','Cook (2000)','Color',[0.65 0.65 0.65]);
set(plot1(3),'DisplayName','Mann et al. (2000)','Color',[0.65 0.65 0.65]);
set(plot1(4),'DisplayName','Evans et al. (2002)','Color',[0.65 0.65 0.65]);
set(plot1(5),'DisplayName','Evans et al. (2001)','Color',[0.65 0.65 0.65]);
set(plot1(6),'DisplayName','Cook  (2008)','Color',[0.65 0.65 0.65]);
set(plot1(7),'DisplayName','Braganza et al. (2009)','Color',[0.65 0.65 0.65]);
set(plot1(8),'DisplayName','Braganza et al. (2009)','Color',[0.65 0.65 0.65]);
set(plot1(9),'DisplayName','McGregor et al. (2010)','Color',[0.65 0.65 0.65]);
set(plot1(10),'DisplayName','Wilson et al. (2010)','Color',[0.65 0.65 0.65]);
set(plot1(11),'DisplayName','Wilson et al. (2010)','Color',[0.65 0.65 0.65]);
set(plot1(12),'DisplayName','Li et al. (2011)','Color',[0.65 0.65 0.65]);
set(plot1(13),'DisplayName','Emile-Geay et al. (2013)','Color',[0.65 0.65 0.65]);
set(plot1(14),'DisplayName','Emile-Geay et al. (2013)','Color',[0.65 0.65 0.65]);
set(plot1(15),'DisplayName','Emile-Geay et al. (2013)','Color',[0.65 0.65 0.65]);
set(plot1(16),'DisplayName','Li et al. (2013)','Color',[0.65 0.65 0.65]);
set(plot1(17),'DisplayName','Tierney et al. (2015)','Color',[0.65 0.65 0.65]);
set(plot1(18),'DisplayName','mean','LineWidth',3,'Color',[0 0 1]);

plot2=plot(X1(sp:end-5),YMatrix1(19:20,sp:end-5),'Parent',axes1,'LineWidth',0.5,'linestyle','--')
set(plot2(1),'DisplayName','10th percentile','LineWidth',2,'Color',[0 0 0]);
set(plot2(2),'DisplayName','90th percentile','LineWidth',2,'Color',[0 0 0]);

%plot(nanmean(proxy_data_var2(18:19,:)),'m','LineWidth',2,'DisplayName','Line Island Coral')

% Create xlabel
xlabel('Year');

% Create ylabel
ylabel('Variance ratio');
title('(a) ENSO variability - reconstructed')

box(axes1,'on');
grid(axes1,'on');
% Set the remaining axes properties
set(axes1,'FontSize',18);
% Create legend
% legend1 = legend(axes1,'show');
% set(legend1,...
%     'Position',[0.531957928802587 0.306633291614518 0.114347357065804 0.492538631404438],...
%     'FontSize',16);


%load /Users/shaynem/Documents/PANELS/AR6/ch2_paleo_figure/blairs_data.txt
load blairs_data.txt
YMatrix2=blairs_data(:,1:2);
X2=blairs_data(:,3);
[ee,sp]=min(abs(X1-X2(1)));
[ee,ep]=min(abs(X2-X1(end)));
YMatrix2(1:ep,3)=YMatrix1(18,sp:end)
YMatrix2(ep+1:end,3)=YMatrix2(ep+1:end,3)*NaN;

% Create axes
axes2 = axes('Parent',figure1,...
    'Position',[0.701186623516721 0.11 0.253813376483274 0.815]);
hold(axes2,'on');

% Create multiple lines using matrix input to plot
plot3=plot(X2,YMatrix2,'Parent',axes2);
set(plot3(1),'DisplayName','SOI','Color',[1 0 0],'linewidth',[2]);
set(plot3(2),'DisplayName','N34','Color',[0 1 1],'linewidth',[2]);
set(plot3(3),'DisplayName','Proxy','Color',[0 0 1],'linewidth',[2]);

% Uncomment the following line to preserve the Y-limits of the axes
% ylim(axes2,[0.2 1.6]);
box(axes2,'on');
grid(axes2,'on');
% Set the remaining axes properties
set(axes2,'FontSize',18);
ylabel('Variance ratio');
title('(a) ENSO variability - historical')

% how many proxies are used in the reconstruction?
% 
% proxy_data_var2_v2=abs(isnan(proxy_data_var2)-1);
% figure
% subplot(121)
% plot(X1,sum(proxy_data_var2_v2))
% 
% subplot(122)
% plot(X1,sum(proxy_data_var2_v2))
% axis([1900 2000 1 18])


