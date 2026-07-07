%  IPCC Ch 2, load and save volcanic and solar forcing data
%  Author: Matthew Toohey
%  Created February 2019-June 2021

data_save_dir='C:\Users\mat897\work\Projects\IPCC';

erf_factor=[-20 0.2644];

%% colors
red=     [204 37 41]/255;
blue   = [0 0.4470 0.7410];
purple = [0.4940    0.1840    0.5560];
orange = [0.8500    0.3250    0.0980];
yellow=  [0.9290    0.6940    0.1250];
lblue = [0.3010    0.7450    0.9330];
green = [0.4660    0.6740    0.1880];

%% data, volcanic

% load EVA/eVolv2k file
% https://cera-www.dkrz.de/WDCC/ui/cerasearch/entry?acronym=eVolv2k_v3
eva_file='C:\Users\mat897\Data\eVolv2k\eVolv2k_v3_EVA_AOD_-500_1900_1.nc';

eva_lat=ncread(eva_file,'lat');
eva_time=ncread(eva_file,'time');
eva_AOD_2D=ncread(eva_file,'aod550');
eva_AOD_gm=area_mean(eva_AOD_2D',eva_lat,[-90 90]); % see function included at end of script
eva_time_am=-500:1900;
eva_aod_gm_res=reshape(eva_AOD_gm,12,[]);
eva_aod_gm_am=mean(eva_aod_gm_res,1);

% load CMIP6
% ftp://iacftp.ethz.ch/pub_read/luo/CMIP6
cmip6_ext=ncread('C:\Users\mat897\Data\AOD_reconstructions\CMIP6_ETH\CMIP_1850_2014_extinction_550nm_strat_only_v3.nc','ext550');
cmip6_lat=ncread('C:\Users\mat897\Data\AOD_reconstructions\CMIP6_ETH\CMIP_1850_2014_extinction_550nm_strat_only_v3.nc','latitude');

cmip6_aod=squeeze(sum(0.5*cmip6_ext,2));
cmip6_aod_gm=area_mean(cmip6_aod,cmip6_lat,[-90 90]);
cmip6_aod_gm_am=mean(reshape(cmip6_aod_gm,12,[]),1);
cmip6_year=reshape(repmat(1850:2014,12,1),[],1);
cmip6_month=reshape(repmat(1:12',1,length(cmip6_year)/12),[],1);
cmip6_time=cmip6_year+(cmip6_month-1)/12;
cmip6_time_am=cmip6_time(1):1:floor(cmip6_time(end));

% Sato
% https://data.giss.nasa.gov/modelforce/strataer/
[sato_time, sato_lat, sato_aod]=read_sato(); % see function included at end of script
sato_aod_gm=area_mean(sato_aod,sato_lat,[-90 90]);
sato_aod_gm_am=mean(reshape(sato_aod_gm,12,[]),1);
sato_years=1850:2012;

[sato02_time, sato02_lat, sato02_aod]=read_sato02(); % see function included at end of script
sato02_aod_gm=area_mean(sato02_aod,sato02_lat,[-90 90]);
sato02_aod_gm_am=mean(reshape(sato02_aod_gm,12,[]),1);
sato02_aod_gm_am=[sato02_aod_gm_am 0.0001*ones(1,13) ];
sato02_years=1850:2012;

%% Volc RF calculations

eva_erf=erf_factor(1)*eva_aod_gm_am+erf_factor(2);
cmip6_erf=erf_factor(1)*cmip6_aod_gm_am+erf_factor(2);
sato_erf=erf_factor(1)*sato_aod_gm_am+erf_factor(2);
sato02_erf=erf_factor(1)*sato02_aod_gm_am+erf_factor(2);

%% Solar data

% PMIP4
% https://pmip4.lsce.ipsl.fr/doku.php/data:solar_satire
C14_file='C:\Users\mat897\Data\Solar\PMIP\SSI_14C_cycle_yearly_cmip_v20160613_fc.nc';
C14_dwl=ncread(C14_file,'wavelength_bin');
C14_ssi=ncread(C14_file,'ssi');
C14_time=ncread(C14_file,'time');
C14_tsi=sum(C14_dwl.*C14_ssi,1);
C14_time_am=floor(min(C14_time)):2016;
C14_tsi_am=NaN*ones(size(C14_time_am));
year_length=NaN*ones(size(C14_time_am));
for i=1:length(C14_time_am)
    ind=find(C14_time>=C14_time_am(i) & C14_time<C14_time_am(i)+1);
    year_length(i)=length(ind);
    C14_tsi_am(i)=mean(C14_tsi(ind));
end

% CMIP6
% http://solarisheppa.geomar.de/cmip6

cm6_file='C:\Users\mat897\Data\Solar\CMIP6\solarforcing-ref-mon_input4MIPs_solar_CMIP_SOLARIS-HEPPA-3-2_gn_18500101-22991231.nc';
cm6_tsi=ncread(cm6_file,'tsi');
cm6_year=ncread(cm6_file,'calyear');
cm6_month=ncread(cm6_file,'calmonth');
cm6_day=ncread(cm6_file,'calday');
cm6_time=cm6_year+(cm6_month-1)/12;

cm6_uyear=unique(cm6_year);
for i=1:length(cm6_uyear)
    cm6_tsi_am(i)=mean(cm6_tsi(find(cm6_year==cm6_uyear(i))));
end

% update
x=xlsread('C:\Users\mat897\Data\Solar\CMIP6_update\TSI_Composite.xlsx');
jday=x(:,1);
cm6u_tsi=x(:,2);
cm6u_dtsi=x(:,3);
t=datetime(jday,'Convertfrom','juliandate');
cm6u_yr=year(t);
cm6u_mo=month(t);
uyear=unique(cm6u_yr);
for i=1:length(uyear)
    ind=find(cm6u_yr==uyear(i));
    cm6u_tsi_am(i)=mean(cm6u_tsi(ind));
    %cm6u_dtsi_am(i)=(1/length(ind))*sqrt(sum(cm6u_dtsi(ind).^2));
    cm6u_dtsi_am(i)=mean(cm6u_dtsi(ind));
end
% first and last years are incomplete
cm6u_yr=uyear(2:end-1);
cm6u_tsi_am=cm6u_tsi_am(2:end-1);
cm6u_dtsi_am=cm6u_dtsi_am(2:end-1);

% CMIP5
% http://solarisheppa.geomar.de/cmip5
 
cm5=dlmread('C:\Users\mat897\Data\Solar\CMIP5\TSI_WLS_mon_1882_2008_clean.txt');
cm5_year=cm5(:,1);
cm5_time=cm5(:,1)+(cm5(:,2)-1)/12;
cm5_tsi=cm5(:,4);

cm5_uyear=unique(cm5(:,1));
for i=1:length(cm5_uyear)
    cm5_tsi_am(i)=mean(cm5_tsi(find(cm5_year==cm5_uyear(i))));
end

%% Solar 10 yr running means
C14_tsi_10yrm=movmean(C14_tsi_am,10);
cm6_tsi_10yrm=movmean(cm6_tsi_am,10);
cm5_tsi_10yrm=movmean(cm5_tsi_am,10);


%% save data volc

eva_mat=double([eva_time_am(:) eva_aod_gm_am(:) eva_erf(:)]);
save([data_save_dir 'eVolv2k_ERF.txt'],'eva_mat','-ascii');
cmip6_mat=double([cmip6_time_am(:) cmip6_aod_gm_am(:) cmip6_erf(:)]);
save([data_save_dir 'cmip6_ERF.txt'],'cmip6_mat','-ascii');

sato_mat=double([sato_years(:) sato_aod_gm_am(:) sato_erf(:)]);
sato02_mat=double([sato02_years(:) sato02_aod_gm_am(:) sato02_erf(:)]);

meta_data={'Volcanic Forcing Data for IPCC AR6 Chapter 2' ...
    'Compiled by Matthew Toohey, February 2019' ...
    'Sources: (1) Toohey, M. and Sigl, M.: Volcanic stratospheric sulfur injections and aerosol optical depth from 500 BCE to 1900 CE, Earth Syst. Sci. Data, 9(2), 809–831, doi:10.5194/essd-9-809-2017, 2017. download: https://cera-www.dkrz.de/WDCC/ui/cerasearch/entry?acronym=eVolv2k_v3' ...
    ' (2) CMIP6: ftp://iacftp.ethz.ch/pub_read/luo/CMIP6_SAD_radForcing_v4.0.0/' ...
    ' (3) Sato, M., Hansen, J. E., McCormick, M. P. and Pollack, J. B.: Stratospheric Aerosol Optical Depths, 1850–1990, J. Geophys. Res., 98(D12), 22987–22994, doi:10.1029/93JD02553, 1993. and updates from https://data.giss.nasa.gov/modelforce/strataer/' ...
    ' ' ...
    ' Each sheet contains annual mean global mean stratospheric aerosol optical depth (SAOD) at 550 nm, effective radiative forcing (ERF, units: W m**-2)' ...
    ' Effective radiative forcing is computed as -20*SAOD+0.2644'
    }';
    
xlswrite([data_save_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'],meta_data,'Readme');
xlswrite([data_save_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'],{'Year' 'SAOD' 'ERF (W m**-2)'},'CMIP6_hist','A1');
xlswrite([data_save_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'],cmip6_mat,'CMIP6_hist','A2');

xlswrite([data_save_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'],{'Year' 'SAOD' 'ERF (W m**-2)'},'eVolv2k','A1');
xlswrite([data_save_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'],eva_mat,'eVolv2k','A2');

xlswrite([data_save_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'],{'Year' 'SAOD' 'ERF (W m**-2)'},'Sato_2012','A1');
xlswrite([data_save_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'],sato_mat,'Sato_2012','A2');

xlswrite([data_save_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'],{'Year' 'SAOD' 'ERF (W m**-2)'},'Sato_2002','A1');
xlswrite([data_save_dir 'IPCC_AR6_volcanic_SAOD_ERF.xls'],sato02_mat,'Sato_2002','A2');


%% save solar data

solar_mat=double([C14_time_am' C14_tsi_am' C14_tsi_10yrm']);
ind=find(cm6_uyear<2015);
cmip6_solar_mat=double([cm6_uyear(ind) cm6_tsi_am(ind)' cm6_tsi_10yrm(ind)']);
cmip5_solar_mat=double([cm5_uyear(:) cm5_tsi_am(:) cm5_tsi_10yrm(:)]);
cmip6u_solar_mat=double([cm6u_yr(:) cm6u_tsi_am(:) cm6u_dtsi_am(:)]);

meta_data={'Solar Forcing Data for IPCC AR6' ...
    'Compiled by Matthew Toohey, February 2019' ...
    'Sources: file: SSI_14C_cycle_yearly_cmip_v20160613_fc.nc available from https://pmip4.lsce.ipsl.fr/doku.php/data:solar_satire' ...
    ' file: solarforcing-ref-mon_input4MIPs_solar_CMIP_SOLARIS-HEPPA-3-2_gn_18500101-22991231.nc from http://solarisheppa.geomar.de/cmip6' ...
    ' file: TSI_WLS_mon_1882_2008.txt from http://solarisheppa.geomar.de/cmip5' ...
    ' file: TSI_Composite.xlsx'
    }';
    
xlswrite([data_save_dir 'IPCC_AR6_solar_TSI_v3.xls'],meta_data,'Readme');
xlswrite([data_save_dir 'IPCC_AR6_solar_TSI_v3.xls'],{'Year' 'TSI' '10y mean'},'C14_TSI_PMIP4','A1');
xlswrite([data_save_dir 'IPCC_AR6_solar_TSI_v3.xls'],solar_mat,'C14_TSI_PMIP4','A2');
xlswrite([data_save_dir 'IPCC_AR6_solar_TSI_v3.xls'],{'Year' 'TSI' '10y mean'},'CMIP6_TSI','A1');
xlswrite([data_save_dir 'IPCC_AR6_solar_TSI_v3.xls'],cmip6_solar_mat,'CMIP6_TSI','A2');
xlswrite([data_save_dir 'IPCC_AR6_solar_TSI_v3.xls'],{'Year' 'TSI' '10y mean'},'CMIP5_TSI','A1');
xlswrite([data_save_dir 'IPCC_AR6_solar_TSI_v3.xls'],cmip5_solar_mat,'CMIP5_TSI','A2');
xlswrite([data_save_dir 'IPCC_AR6_solar_TSI_v3.xls'],{'Year' 'TSI' 'dTSI'},'CMIP6update_TSI','A1');
xlswrite([data_save_dir 'IPCC_AR6_solar_TSI_v3.xls'],cmip6u_solar_mat,'CMIP6update_TSI','A2');

%% functions

function m=area_mean(x,lat,lat_bounds)

% x is size time x lat (i.e. zonal means)

rlat=(pi/180)*lat;
ind=find(lat>=lat_bounds(1) & lat<=lat_bounds(2));

w=cos(rlat(ind))'./sum(cos(rlat(ind)));

for i=1:size(x,3)
    m(:,i)=nansum(x(:,ind,i).*(ones(size(x,1),1)*w),2);
end

end

function [sato_time, sato_lat, sato_aod]=read_sato()

sato_dir='C:\Users\mat897\Data\AOD_reconstructions\Sato\';
f1=fopen([sato_dir 'tau.map_2012.12b.txt']);

sato_years=1850:2012;
sato_aod=NaN*ones(24,13,length(sato_years),4);

for i=1:4 % for altitude regions
    for j=1:2
        garbage=fgetl(f1);
    end
    for j=1:length(sato_years)
        j;
        temp1=cell2mat(textscan(f1,'%n%n%n%n%n%n%n%n%n%n%n%n%n%n',1));
        sato_aod(1,:,j,i)=temp1(2:end);
        temp2=cell2mat(textscan(f1,'%n%n%n%n%n%n%n%n%n%n%n%n%n',23));
        sato_aod(2:end,:,j,i)=temp2;
    end
    garbage=fgetl(f1);
end
fclose(f1);

sato_lat=sato_aod(:,1,1,1);
sato_aod(:,1,:,:)=[];

sato_aod=sum(sato_aod,4);
sato_aod=reshape(sato_aod,24,[])';
ty=[];
tm=ty;
for i=1:length(sato_years)
    ty=[ty sato_years(i)*ones(1,12)];
    tm=[tm 1 2 3 4 5 6 7 8 9 10 11 12];
end
tdate=datenum(ty,tm,15);
sato_time=ty+(tm-1)/12;
sato_ty=ty;

end

function [sato02_time, sato02_lat, sato02_aod]=read_sato02()

sato02_dir='C:\Users\mat897\Data\AOD_reconstructions\Sato\';
f1=fopen([sato02_dir 'tau.map_2002.txt']);

sato02_years=1850:1999;
sato02_aod=NaN*ones(24,13,length(sato02_years));
sato02_aod_gm=NaN*ones(12,length(sato02_years));
sato02_aod_nh=NaN*ones(12,length(sato02_years));
sato02_aod_sh=NaN*ones(12,length(sato02_years));


for j=1:2
    garbage=fgetl(f1);
end
for j=1:length(sato02_years)
    j;
    temp1=textscan(f1,'%n%s%n%n%n%n%n%n%n%n%n%n%n%n',1);
    sato02_aod_gm(:,j)=cell2mat(temp1(3:end))';
    temp2=textscan(f1,'%s%n%n%n%n%n%n%n%n%n%n%n%n',1);
    sato02_aod_nh(:,j)=cell2mat(temp2(2:end))';
    temp3=textscan(f1,'%s%n%n%n%n%n%n%n%n%n%n%n%n',1);
    sato02_aod_sh(:,j)=cell2mat(temp3(2:end))';
    temp4=cell2mat(textscan(f1,'%n%n%n%n%n%n%n%n%n%n%n%n%n',24));
    sato02_aod(:,:,j)=temp4;
end
fclose(f1);

sato02_lat=sato02_aod(:,1,1);
sato02_aod(:,1,:)=[];

sato02_aod_gm_am=mean(sato02_aod_gm,1);

sato02_aod=sato02_aod/10000;
sato02_aod_gm=sato02_aod_gm(:)/10000;
sato02_aod_nh=sato02_aod_nh(:)/10000;
sato02_aod_sh=sato02_aod_sh(:)/10000;

sato02_aod=reshape(sato02_aod,24,[])';
ty=[];
tm=ty;
for i=1:length(sato02_years)
    ty=[ty sato02_years(i)*ones(1,12)];
    tm=[tm 1 2 3 4 5 6 7 8 9 10 11 12];
end
tdate=datenum(ty,tm,15);
sato02_time=ty+(tm-1)/12;
sato02_ty=ty;

end
