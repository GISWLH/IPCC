addpath /Users/shaynem/MATLAB_SCRIPTS/

ls_mask=ncread('T63GR15_jan_surf.nc','SLF');
ls_mask=abs(ceil(ls_mask)-1);
[ii]=find(ls_mask==0);
ls_mask(ii)=NaN;
ls_mask(:,1:15)=ls_mask(:,1:15).*NaN;
ls_mask(:,end-14:end)=ls_mask(:,end-14:end).*NaN;


temp2=ncread('ts_Amon_MPI-ESM_rcp85_r001i2005p3_200601-209912.nc','ts');
temp=ncread('ts_Amon_MPI-ESM_historical_r001i1850p3_185001-200512.nc','ts');
time2=(1850:0.083333:2099.92);
[m,n,o]=size(temp);
for i=1:o
temp(:,:,i)=temp(:,:,i).* ls_mask;
end
[m,n,o]=size(temp2);
for i=1:o
temp2(:,:,i)=temp2(:,:,i).* ls_mask;
end
ts1=squeeze(nanmean(nanmean(temp-273.15)));
ts2=squeeze(nanmean(nanmean(temp2-273.15)));
ts(:,1)=[ts1;ts2];

temp2=ncread('ts_Amon_MPI-ESM_rcp85_r003i2005p3_200601-209912.nc','ts');
temp=ncread('ts_Amon_MPI-ESM_historical_r003i1850p3_185001-200512.nc','ts');
[m,n,o]=size(temp);
for i=1:o
temp(:,:,i)=temp(:,:,i).* ls_mask;
end
[m,n,o]=size(temp2);
for i=1:o
temp2(:,:,i)=temp2(:,:,i).* ls_mask;
end
ts1=squeeze(nanmean(nanmean(temp-273.15)));
ts2=squeeze(nanmean(nanmean(temp2-273.15)));
ts(:,2)=[ts1;ts2];

temp2=ncread('ts_Amon_MPI-ESM_rcp85_r012i2005p3_200601-209912.nc','ts');
temp=ncread('ts_Amon_MPI-ESM_historical_r012i1850p3_185001-200512.nc','ts');
[m,n,o]=size(temp);
for i=1:o
temp(:,:,i)=temp(:,:,i).* ls_mask;
end
[m,n,o]=size(temp2);
for i=1:o
temp2(:,:,i)=temp2(:,:,i).* ls_mask;
end
ts1=squeeze(nanmean(nanmean(temp-273.15)));
ts2=squeeze(nanmean(nanmean(temp2-273.15)));
ts(:,3)=[ts1;ts2];

[ee,statt2]=min(abs(time2-1950));
% filter the data with 3 different length filters.
for i=1:3,
x=ts(statt2:end,i);
lpf=1/(12*1.3);
y2=ctana_lowpass(x,lpf);
ts_1yrLP_2(:,i)=y2-mean(y2(1:120));
end

for i=1:3,
x=ts_1yrLP_2(:,i);
lpf=1/(12*10);
y=ctana_lowpass(x,lpf);
ts_10yrLP_2(:,i)=y;
end

for i=1:3,
x=ts_1yrLP_2(:,i);
lpf=1/(12*30);
y=ctana_lowpass(x,lpf);
ts_30yrLP_2(:,i)=y;
end

% estimate forced signal
P = polyfit(time2(statt2:end)',mean(ts_1yrLP_2,2),2);
ts_1yrLP_2_Qfit_signal=polyval(P,time2(statt2:end)');


% find start and end dates for plotting plus the offset.
time=(1940:0.08333:2099.92);
[ee,startt]=min(abs(time-1950));
[ee,endtt]=min(abs(time-2019));
[ee,reftt]=min(abs(time-1990));

time2=time2(statt2:end);
[ee,statt2]=min(abs(time2-1950));
[ee,endtt2]=min(abs(time2-2019));
[ee,reftt2]=min(abs(time2-1990));

% plot the figure
figure
subplot(131)
plot(time(1:endtt),ts_1yrLP_2_Qfit_signal(1:endtt)-ts_1yrLP_2_Qfit_signal(reftt),'k','linewidth',[3])
hold on
plot(time2(statt2:endtt2),ts_1yrLP_2(statt2:endtt2,1)-ts_1yrLP_2_Qfit_signal(reftt),'r-','linewidth',[1.5])
plot(time2(statt2:endtt2),ts_1yrLP_2(statt2:endtt2,2)-ts_1yrLP_2_Qfit_signal(reftt),'g--','linewidth',[1.5])
plot(time2(statt2:endtt2),ts_1yrLP_2(statt2:endtt2,3)-ts_1yrLP_2_Qfit_signal(reftt),'b-.','linewidth',[1.5])
set(gca,'fontsize',[14])
xlabel('Year')
ylabel('Global mean surface temperature')
title('Annual variations')
axis([1950 2020 -.6 0.8])
grid

subplot(132)
plot(time(1:endtt),ts_1yrLP_2_Qfit_signal(1:endtt)-ts_1yrLP_2_Qfit_signal(reftt),'k','linewidth',[3])
hold on
plot(time2(statt2:endtt2),ts_10yrLP_2(statt2:endtt2,1)-ts_1yrLP_2_Qfit_signal(reftt),'r-','linewidth',[1.5])
plot(time2(statt2:endtt2),ts_10yrLP_2(statt2:endtt2,2)-ts_1yrLP_2_Qfit_signal(reftt),'g--','linewidth',[1.5])
plot(time2(statt2:endtt2),ts_10yrLP_2(statt2:endtt2,3)-ts_1yrLP_2_Qfit_signal(reftt),'b-.','linewidth',[1.5])
set(gca,'fontsize',[14])
xlabel('Year')
ylabel('Global mean surface temperature')
title('Annual variations')
axis([1950 2020 -.6 0.8])
grid

subplot(133)
plot(time(1:endtt),ts_1yrLP_2_Qfit_signal(1:endtt)-ts_1yrLP_2_Qfit_signal(reftt),'k','linewidth',[3])
hold on
plot(time2(statt2:endtt2),ts_30yrLP_2(statt2:endtt2,1)-ts_1yrLP_2_Qfit_signal(reftt),'r-','linewidth',[1.5])
plot(time2(statt2:endtt2),ts_30yrLP_2(statt2:endtt2,2)-ts_1yrLP_2_Qfit_signal(reftt),'g--','linewidth',[1.5])
plot(time2(statt2:endtt2),ts_30yrLP_2(statt2:endtt2,3)-ts_1yrLP_2_Qfit_signal(reftt),'b-.','linewidth',[1.5])
set(gca,'fontsize',[14])
xlabel('Year')
ylabel('Global mean surface temperature')
title('Annual variations')
axis([1950 2020 -.6 0.8])
grid






