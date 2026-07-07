
% ch2_fig18.m
%
% Description
% Generates Figure 2.18 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 2
%
% Creator: Daoyi Gong (gdy@bnu.edu.cn)
% Creating Date: 19 December 2020
%
% computing U wind trend for ERA5
%
% Assume a confidence level for computing confidence intervals
%
pconf=0.9;
cn=-1.5; cx=1.5;
  load BuDRd_18.dat;
  C=BuDRd_18(:,1:3);


mon_str={'01','02','03','04','05','06','07','08','09','10','11','12'};
mon_name={'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'};

for mon_num=1:12;
mon_name{mon_num}
eval(['load u' mon_str{mon_num}])
end % next mon

clf
figure
% title('Zonal wind trend')

for isea=1:4
%[wkdat=u01]; 
% eval(['wkdat=u' mon_str{mon_num} ';']);
% eval(['u_cli=u' mon_str{mon_num} '_cli;']);

% DJF;
if (isea ==1 )  wkdat=(u12(1:end-1,:,:)+u01(2:end,:,:)+u02(2:end,:,:))/3; u_cli=(u12_cli+u01_cli+u02_cli)/3; ssea={'DJF'};end

% MAM 
if (isea ==2 ) wkdat=(u03+u04+u05)/3; u_cli=(u03_cli+u04_cli+u05_cli)/3; ssea={'MAM'};end
% JJA 
if (isea ==3 ) wkdat=(u06+u07+u08)/3; u_cli=(u06_cli+u07_cli+u08_cli)/3;ssea={'JJA'};end
% SON 
if (isea ==4 ) wkdat=(u09+u10+u11)/3; u_cli=(u09_cli+u10_cli+u11_cli)/3;ssea={'SON'};end

clear utrd utrdsig;
 for ilat=1:length(plat)
     for ilvl=1:length(plvl)
         clear y; y=wkdat(:,ilvl,ilat); 
         % computing trend  
 % call ltr_OLSdofrNaN() function:
   clear b cinthw sig DOFr rho pval;
   [b,cinthw,sig,DOFr,rho,pval]=ltr_OLSdofrNaN(pyr(1:length(y(:)))/10,y(:),pconf);
        utrd(ilvl,ilat)=b;utrdsig(ilvl,ilat)=pval;
     end
 end   
 
     
z95=100*(1-utrdsig);
z95(z95 < pconf)=NaN; z95=z95 * 0;
 
% report trends and confidence intervals: 
% fprintf('   %10s :%6.3f+-%5.3f, p-value=%7.5f\n','utrend',b,cinthw,pval)

fprintf('Max. tred %5.2f  min. trend %5.2f\n',max(utrd(:)),min(utrd(:)));
 
 kk=(log(1000.0)-log(double(plvl)))*8*5;
 clear XX YY;
 [XX,YY]=meshgrid(plat(1:12:end),min(kk):3:max(kk));
 [X0,Y0]=meshgrid(plat,kk);
 
[ZZ]=griddata(double(X0),Y0,u_cli,double(XX),YY);
 
  % figure;
  % axes('position',[.1  .1  .4  .6])
 % subplot(2,2,isea);
 if (isea == 1); axes('position',[.1  .53  .33  .31]); end
 if (isea == 2); axes('position',[.5  .53  .33  .31]); end
 if (isea == 3); axes('position',[.1  .15   .33  .31]); end
 if (isea == 4); axes('position',[.5  .15   .33  .31]); end
 
 %contourf(plat,kk,u_cli);
 trd_trim=utrd; %trd_trim(1,:)=NaN; trd_trim(end,:)=NaN;trd_trim(:,1)=NaN;trd_trim(:,end)=NaN;   
 pcolor(plat,kk,trd_trim);colormap(C); shading flat; % colorbar;
 hold on; caxis([cn cx]);
 

[cc,ch]=contour(XX,YY,ZZ,(-1500:10:-10),'k--','linewidth',1.2);set(ch,'ShowText','on','TextStep',get(ch,'LevelStep')*2);
[cc,ch]=contour(XX,YY,ZZ,(10:10:1500),'k-','linewidth',1.2);set(ch,'ShowText','on','TextStep',get(ch,'LevelStep')*2);

 
 
%axis([-14 14 min(kk) max(kk)-0.5]);
if (isea == 1); ylabel('Pressure(hPa)'); end
if (isea == 3); ylabel('Pressure(hPa)'); end


% title([mon_name{mon_num}])
title([ssea])

set(gca,'linewidth',1.2);
axis([-91.5 91.5 min(kk)-1 max(kk)+1]);

set(gca,'YTick',flipud(kk));
ylbl=num2str(flipud(plvl(:)));ylbl(2:6,:)=' ';ylbl(8:11,:)=' ';ylbl(13,:)=' ';ylbl(15,:)=' ';ylbl(17,:)=' ';
ylbl(19,:)=' ';ylbl(21:22,:)=' ';ylbl(24,:)=' ';ylbl(26,:)=' ';
set(gca,'XTick',[-90:30:90]);set(gca,'XTickLabel',{'90S','60S','30S','0','30N','60N','90N'});
set(gca,'YTickLabel',ylbl);



z95=100*(1-utrdsig);
%z95(z95 < pconf)=NaN; z95=z95 * 0;
 clear XS YS ZS X0 Y0;
 [XS,YS]=meshgrid(plat(1:12:end),min(kk):3:max(kk));
 [X0,Y0]=meshgrid(plat,kk);
 
[ZS]=griddata(double(X0),Y0,z95,double(XS),YS);

% [XS,YS]=meshgrid(plat,kk);

% Non-sig grids
 XS=XS(:);YS=YS(:);ZS=ZS(:); ZS(ZS >= 100*pconf)=NaN; % ZS=ZS * 0;
 k=find(ZS < 100*pconf); XS=XS(k);YS=YS(k);ZS=ZS(k);

% sig. grids
%XS=XS(:);YS=YS(:);ZS=ZS(:); ZS(ZS < 100*pconf)=NaN; % ZS=ZS * 0;
%k=find(ZS >= 100*pconf); XS=XS(k);YS=YS(k);ZS=ZS(k);

%hold on;plot(XS(1:2:end),YS(1:2:end),'+', 'MarkerEdgeColor','k',...
%                'MarkerFaceColor','k',...
%                'MarkerSize',1.5);
hold on;plot(XS(1:1:end),YS(1:1:end),'x', 'MarkerEdgeColor','k',...
                'MarkerFaceColor','k',...
                'MarkerSize',3.1);

end % next        
        
         set(gcf,'Renderer','painters');
        % eval(['hgsave(''uwind_trd'')']);  eval(['print -depsc2 -r600 uwind_trd.eps']);    

       %  plotting legend
       %  figure;
       %  clf    
         
axes('position',[.21  .13  .5  .08])         
%xlabelstr='Linear trend slope (ms^{-1}decade^{-1})';
xlabelstr='Trend (ms^{-1} per decade)';
fontsizenum=13;
printformstr='-depsc';
foutstr='Uwind_Trend';
colormap(C)
hc=colorbar('southoutside')
caxis([cn cx])
set(gca,'Visible','off','Box','off')
  set(gca,'FontSize',12)
  set(get(hc,'XLabel'),'String',xlabelstr,'FontSize',fontsizenum,'Visible','on')
  %pbaspect([1 0.1 1])
%print(foutstr,printformstr)

text(0.30,9.6,'Zonal wind trend','FontSize',14);

     set(gcf,'Renderer','painters');
         
         eval(['hgsave(''uwind_trd_sig'')']);
         eval(['print -depsc2 -r600 uwind_trd_sig.eps']);  
         
