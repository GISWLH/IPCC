coast=load('coast');

load BuDOd_18_2.dat;
C=BuDOd_18_2(:,1:3);
cx=60;
cn=-60;

yba=[1901];
yea=[2019];

np=length(yba);

p=0.90;

nmonmin = 8;
ptot = 0.7;
plenbe = 0.1;
pbe = 0.25;

dx=2.5;
dy=2.5;
Xo = (0:dx:357.5)';
Y = (-88.75:dy:88.75)';

nx=length(Xo);
ny=length(Y);
nxny=nx*ny;

ixs180=[nx/2+1:nx 1:nx/2];
X=Xo(ixs180);
X(1:nx/2)=X(1:nx/2)-360;

tyrs=1901:2019;
nt=length(tyrs);
ntm=nt*12;

t=zeros(ntm,1);

prec = NaN(ntm,nxny);

amiss = -999.9;
fname='../data/cru_masked_2019_2.nc';
prec=ncread('cru_masked_2019_2.nc', 'pre');
prec=permute(prec,[3,1,2]);

inav=find(prec <= amiss);
prec(inav) = NaN;

precann=zeros(nt,nx,ny);

for ixy=1:nx,
    for iyy=1:ny
        panom=prec(:,ixy,iyy);
        pann = monanom2ann(panom,nmonmin);
        precann(:,ixy,iyy)=pann;
    end
end
w0=precann;

w=w0(:,ixs180,:);

% Loop over periods
for ip = 1:np,

sper = [num2str(yba(ip)) '-' num2str(yea(ip))];

its=find(tyrs>=yba(ip) & tyrs<=yea(ip));
ts=tyrs(its);

tr=NaN(nx,ny);
pv=tr;

isig=0;
ysig=zeros(nxny,1);
xsig=zeros(nxny,1);

for iy=1:ny,
for ix=1:nx,

w1=w(its,ix,iy);

if isenough4trend(w1,ptot,plenbe,pbe),
[b,cinthw,sig,DOFr,rho,pval,irrc,N,a,Na,Nc]=ltr_OLSdofrNaN(ts/10,w1,p);
tr(ix,iy)=b;
pv(ix,iy)=pval;
if pval >= 1-p,
     isig = isig + 1; 
     xsig(isig)=X(ix);
     ysig(isig)=Y(iy);
end
end

end
end

nsig=isig;
xsig=xsig(1:nsig);
ysig=ysig(1:nsig);

Xs=[X(1)-dx/2 X'+dx/2];     
Ys=[Y(1)-dy/2 Y'+dy/2];     

figure(ip)
clf
axesm('robinson', 'maplonlimit', [-178.75 178.75], 'maplatlimit',[-80 80],'frame','on')

hpcm=pcolorm(-Ys,Xs,flip(tr'*10));
set(hpcm,'FaceColor','Flat')
colormap(flip(C));
caxis([cn cx])

hp=plotm(ysig,xsig,'xk','MarkerSize',7)

geoshow(coast.lat,coast.long,'LineWidth',1,'Color',[0 0 0])
plotm(coast.lat,coast.long,'-w','LineWidth',1)
set(gca,'Box','off')
set(gca,'Visible','off')
set(gca,'LineWidth',1)

print(['MLOST_tr_CRU_msklow' sper '.eps'], '-depsc')

fido = fopen(['trends' sper '.asc'],'w')
for i=1:ny
	fprintf(fido,'%10.6f',tr(:,i))
	fprintf(fido,'\n')
end
fclose(fido)

fido = fopen(['pvals' sper '.asc'],'w')
for i=1:ny
	fprintf(fido,'%10.6f',pv(:,i))
	fprintf(fido,'\n')
end
fclose(fido)


end

	figure(ip+1)
clf
xlabelstr='Trend (mm yr^-^1 per decade)';
fontsizenum=24;
printformstr='-depsc';
foutstr='cbhor_SurfPrec_Trend';
colormap(flip(C))
hc=colorbar('southoutside');
caxis([cn cx])
set(gca,'Visible','off','Box','off')
  set(gca,'FontSize',24)
  set(get(hc,'XLabel'),'String',xlabelstr,'FontSize',fontsizenum,'Visible','on')
  pbaspect([1 1 1])
print(foutstr,printformstr)
