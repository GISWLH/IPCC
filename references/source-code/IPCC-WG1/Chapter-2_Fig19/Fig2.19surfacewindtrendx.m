% ch2_fig19.m
%
% Description
% Generates Figure 2.19 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 2
%
% Creator: Daoyi Gong (gdy@bnu.edu.cn)
% Creating Date: 19 December 2020
%
% make a single figure
% make a single figure  x-non-significant point
clc,clear
%cd data
clf
fontsizenum=14;
LW=0.5; % coast line width
CZ=2.1; % Cross size

%%%%


figure
for myfig=1:4;

if  ( myfig == 1 ); load HadISD; end
if  ( myfig == 2 ); load ERA5; end
if  ( myfig == 3 ); load CCMP; end
if  ( myfig == 4 ); load OAFlux;end

wind=wind(:,:,find(year>=1988 & year<=2017));
year=year(find(year>=1988 & year<=2017));
% 1.CCMP 2.OAFlux 3.BSW 4.ERA-Interim 5.ERA5 6.NNR 7.WASind 8.HadISD
%cd ..
clear glat glon ;
[glat,glon]=meshgrat(nlat,nlon);

%%%%

%% trend
clear tr pv xlat xlon;
p=0.9;
for i=1:length(nlat)
    for j=1:length(nlon)
        [b,cinthw,sig,DOFr,rho,pval,irrc,N,a,Na,Nc]=ltr_OLSdofrNaN(year/10,squeeze(wind(i,j,:)),p);
        tr(i,j)=b;
        pv(i,j)=pval; 
    end
end

p=1;
for i=1:length(nlat)
    for j=1:length(nlon)

        if  pv(i,j) > 0.1 & abs(glat(i,j))<78 & tr(i,j) > -90 & tr(i,j) < 90 
            xlat(p)=glat(i,j);
            xlon(p)=glon(i,j);
            p=p+1;
        end        
        
    end
end



% clf
if ( myfig == 1 );
axes('Position',[.13  .43  .45  .35 ])
axesm('robinson', 'maplonlimit', [-180,180], 'maplatlimit',[-80 80],'frame','on')
hpcm=pcolorm(glat,glon,tr);
set(hpcm,'FaceColor','Flat')
load BuDRd_18.dat;
C=BuDRd_18(:,1:3);
colormap(C);
cx=0.45;
cn=-0.45;
caxis([cn cx])
 
hp=plotm(xlat+2,xlon+2,'xk','MarkerSize',CZ);
coast=load('coast');
geoshow(coast.lat,coast.long,'LineWidth',LW,'Color',[0 0 0])
set(gca,'Box','off')
set(gca,'Visible','off')
set(gca,'LineWidth',1)
text(-.8,1.5,'a) HadISD','FontSize',fontsizenum); 
%setm(gca,'FFaceColor','cyan')
% setm(gca,'FEdgeColor','r');
setm(gca,'FLineWidth',.9);
end

if ( myfig == 2 );
axes('Position',[.5  .43  .45  .35 ])
axesm('robinson', 'maplonlimit', [-180,180], 'maplatlimit',[-80 80],'frame','on')
hpcm=pcolorm(glat,glon,tr);
set(hpcm,'FaceColor','Flat')
load BuDRd_18.dat;
C=BuDRd_18(:,1:3);
colormap(C);
cx=0.45;
cn=-0.45;
caxis([cn cx])
 
hp=plotm(xlat+2,xlon+2,'xk','MarkerSize',CZ);
coast=load('coast');
geoshow(coast.lat,coast.long,'LineWidth',LW,'Color',[0 0 0])
set(gca,'Box','off')
set(gca,'Visible','off')
set(gca,'LineWidth',1)
text(-.8,1.5,'b) ERA5','FontSize',fontsizenum); 
setm(gca,'FLineWidth',1.3);
end
%ttl=title('(d) HadISD','Visible','on','FontSize',24,'FontWeight','bold');

if ( myfig == 3 );
axes('Position',[.13  .15  .45  .35 ])
axesm('robinson', 'maplonlimit', [-180,180], 'maplatlimit',[-80 80],'frame','on')
hpcm=pcolorm(glat,glon,tr);
set(hpcm,'FaceColor','Flat')
load BuDRd_18.dat;
C=BuDRd_18(:,1:3);
colormap(C);
cx=0.45;
cn=-0.45;
caxis([cn cx])
 
hp=plotm(xlat+2,xlon+2,'xk','MarkerSize',CZ);
coast=load('coast');
geoshow(coast.lat,coast.long,'LineWidth',LW,'Color',[0 0 0])
set(gca,'Box','off')
set(gca,'Visible','off')
set(gca,'LineWidth',1)
text(-.8,1.5,'c) CCMP','FontSize',fontsizenum); 
setm(gca,'FLineWidth',1.3);
end

if ( myfig == 4 );
axes('Position',[.5  .15  .45  .35 ])
axesm('robinson', 'maplonlimit', [-180,180], 'maplatlimit',[-80 80],'frame','on')
hpcm=pcolorm(glat,glon,tr);
set(hpcm,'FaceColor','Flat')
load BuDRd_18.dat;
C=BuDRd_18(:,1:3);
colormap(C);
cx=0.45;
cn=-0.45;
caxis([cn cx])
 
hp=plotm(xlat+2,xlon+2,'xk','MarkerSize',CZ);
coast=load('coast');
geoshow(coast.lat,coast.long,'LineWidth',LW,'Color',[0 0 0])
set(gca,'Box','off')
set(gca,'Visible','off')
set(gca,'LineWidth',1)
text(-.8,1.5,'d) OAFlux','FontSize',fontsizenum); 
setm(gca,'FLineWidth',1.3);
end

end % nex sub-fig

axes('Position',[.29  .2  .5  .1 ])
xlabelstr='Trend (m s^{-1}decade^{-1})';

printformstr='-depsc';

colormap(C)
hc=colorbar('southoutside')
caxis([cn cx])
set(gca,'Visible','off','Box','off')
set(gca,'FontSize',14)
set(get(hc,'XLabel'),'String',xlabelstr,'FontSize',fontsizenum,'Visible','on')
pbaspect([1 0.1 1])

xlabelstr='Wind speed trend';

 text(.29,8.5,xlabelstr,'FontSize',fontsizenum+1);
 foutstr='figOne_1X';

print(foutstr,printformstr)


 


 

