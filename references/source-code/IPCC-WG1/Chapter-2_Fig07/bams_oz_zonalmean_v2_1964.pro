pro read_cmi,fle,yy,cmi_ozone
read_fle,fle,dta,header=1
ncol=2 ; 1 model mean, 2 model median
yy=reform(dta(0,*))
nr=where(yy ge 1998 and  yy le 2008,nrt)
toz_mean=total(dta(ncol,nr))/nrt
dta(ncol,*)=dta(ncol,*)-toz_mean
cmi_ozone=reform(dta(ncol,*))
return
end

function triangular,dta,nsmooth
    ns=fix(nsmooth/2.)*2+1
    res=dta
    if nsmooth ge 3 then begin
     res=smooth(smooth(dta,ns,/edge_truncate),ns,/edge_truncate)
    endif
return,res
end

pro annual_mean,fyr,oz,fyra,oza
y0=fix(min(fyr))
y1=fix(max(fyr))
oza=fltarr(y1-y0+1)*0.
fyra=oza
for iy=y0,y1 do begin
    i=iy-y0
    nr=where(fyr ge iy and fyr le iy+1,nrt)
    if nrt gt 11 then oza(i)=total(oz(nr))/nrt
    fyra(i)=iy
endfor
nr=where(oza gt 0)
fyra=fyra(nr)
oza=oza(nr)
end

pro annual_mean_anomaly,yy,oz,oza,y0,y1,mn
nr=where(yy ge y0 and yy le y1 and oz gt 0,nrt)
oza=oz
mn=1.
if nrt gt 0 then begin
	mn=total(oz(nr))/nrt
	oza=oz-mn
endif
end

pro zm_anomaly,fle,fyr,mo,oz_mean,lat,y0,y1
  close,2
  openr,2,fle
  yy=y0+indgen(y1-y0+1)
  n3=n_elements(yy)
  dummy1=''
  dummy2=''
  n1=14 & n2=36
  ;----------mm,lat,yr
  ozmat=fltarr(12,n2,n3)*0.
  mtrx=fltarr(n1,n2)*0.
  nc=-1
  while not(eof(2)) do begin
    readf,2,dummy1
    readf,2,dummy2
    readf,2,mtrx
    nc=nc+1
    ozmat(*,*,nc)=mtrx(2+indgen(12),*)
  endwhile
  n1=12
  close,2


  lat=-87.5+findgen(36)*5.
  n=12*(y1-y0+1)
  fyr=y0+(findgen(n)+.5d0)/12.d0
  mo=fyr*0+(indgen(n) mod 12) +1
  ozm=fltarr(n,n2)
  k=-1
  for j=0,n3-1 do begin
  for i=0,n1-1 do begin
    k=k+1
    ozm(k,*)=ozmat(i,*,j)
  endfor
  endfor
  o3_ref=fltarr(n1,n2)*0.
  for i=1,12 do begin
    nr=where(fyr ge y0 and fyr le y1 and mo eq i+1,nrt)
    for j=0,n2-1 do begin
     arr=ozm(nr,j)
     mr=where(arr ne 0, mrt)
     o3_ref(i-1,j)=total(arr(mr))/(mrt+0.)
  endfor
  endfor
  for i=0,n-1 do begin
    ozm(i,j)=ozm(i,j)-o3_ref(mo(i)-1,j)
  endfor
  end

pro read_o3_zm,fle,y0,y1,fyr,mo,oz,latmin,latmax,month0,month1
nfrac=0.7
close,2
openr,2,fle
;yy=y0+indgen(y1-y0+1)
n3=60
dummy1=''
dummy2=''
n1=14 & n2=36
ozm=fltarr(12,n2,n3)*0.
mtrx=fltarr(n1,n2)*0.
nc=-1
ymin=2100
ymax=1900
ymax=1
while not(eof(2)) do begin
 readf,2,yy
 if yy ge ymax then ymax=yy
 if yy le ymin then ymin=yy
 readf,2,dummy2
 readf,2,mtrx
 nc=nc+1
 ozm(*,*,nc)=mtrx(2+indgen(12),*)
endwhile
yy=ymin+indgen(ymax-ymin+1)
y0=ymin
y1=ymax
n3=n_elements(yy)
;yy=yy(indgen(nc+1))
;nr=where(yy lt 1978)
;ozm(*,*,nr)=0.
;n3=nc+1
n1=12
close,2

lat=-87.5+findgen(36)*5.
n=12*(y1-y0+1)
fyr=y0+(findgen(n)+.5d0)/12.d0
mo=fyr*0+(indgen(n) mod 12) +1
nl=where (lat ge latmin and lat le latmax,nrt)
wts=cos(!dtor*lat(nl))
nc=-1
oz=fltarr(n)*0.
for iy=y0,y1 do begin
    i=iy-y0
    for im=0,11 do begin
       nc=nc+1
       toz=ozm( (im mod 12),nl,i)
       nr=where(toz gt 0,nrt)
;       if nrt gt 0. then oz(nc)=total(toz(nr)*wts(nr))/total(wts(nr))
       if nrt gt 0 then begin
           latfrac=total(wts(nr))/total(wts)
           if latfrac ge .7 then oz(nc)=total(toz(nr)*wts(nr))/total(wts(nr))
       endif
    endfor
endfor
nr=where(oz gt 0,nrt)
fyr=fyr(nr)
mo=mo(nr)
oz=oz(nr)

nm=max(fix(fyr))-min(fix(fyr))+1
ozm=fltarr(nm)*0
fyrm=min(fix(fyr))+indgen(nm)
for iy=min(fyrm),max(fyrm) do begin
    i=iy-min(fyrm)
    nr=where( fix(fyr) eq iy and mo ge month0 and mo le month1,nrt)
    if nrt gt fix(nfrac*(month1-month0+1)) then ozm(i)=total(oz(nr))/nrt
endfor
nr=where(ozm gt 0,nrt)
fyr=fyrm(nr)
oz=ozm(nr)
end

pro read_o3_zm_sbuvnoaa,fle,y0,y1,fyr,mo,oz,latmin,latmax,month0,month1
dummy1=''
dummy2=''
close,2
openr,2,fle
readf,2,dummy1
nlat=33
oz=0.*findgen(nlat+2)
lat=-80+indgen(nlat)*5.
ntot=50*12
mat=fltarr(nlat,ntot)
yy=fltarr(ntot)*0.
mm=fltarr(ntot)*0.
nc=-1
while not eof(2) do begin
    readf,2,oz
    nc=nc+1
    ;print,nc,oz
    yy(nc)=oz(1)
    mm(nc)=oz(0)
    mat(*,nc)=oz(2+indgen(nlat))
endwhile
close,2

oz_threshold=80
yy=yy(indgen(nc))
mm=mm(indgen(nc))
mat=mat(*,indgen(nc))
ntot=nc

y0=min(yy)
y1=max(yy)
yr=y0+indgen(y1-y0+1)
n=(y1-y0+1)
fyr=yr+( (month1+month0)*0.5-.5 )/12.
mo=fix(yr)

wts=cos(!dtor*lat)
nc=-1
oz=fltarr(n)*0.
for iy=y0,y1 do begin
    i=iy-y0
    nc=nc+1
    nd=where(yy eq iy and mm ge month0 and mm le month1,nmt)
    nl=where (lat ge latmin and lat le latmax,nlt)
    oz(nc)=0.
    ;if iy eq 1978 then stop
    if nmt gt 0 and nlt gt 0 then begin
     mwts=fltarr(nlt,nmt)*0.
     moz=mwts*0.
     nom=0
     for k=0,nmt-1 do begin
       if (max(mat(nl,nd(k))) gt oz_threshold)  then nom=nom+1
        mwts(*,k)=wts(nl)
        moz(*,k)=mat(nl,nd(k))
     endfor
     nr=where(moz le oz_threshold,nrt)
     if nrt gt 0. then begin
            mwts(nr)=0.
            moz(nr)=0.
     endif
     oz(nc)=total(mwts*moz)/total(mwts)
     if (nom+0.)/(month1-month0+1.) le 0.8 then oz(nc)=0.
     print,iy,(nom+0.)/(month1-month0+1.),oz(nc)
    endif
endfor
nr=where(oz gt 0,nrt)
fyr=fyr(nr)
mo=mo(nr)
oz=oz(nr)
end


pro read_modv8annual,fle,yr,toz
read_fle,fle,dta,header=4
n=n_elements(dta(0,*))
toz=fltarr(4,n)
yr=fix(reform(dta(0,*)))
toz(0,*)=dta(1,*)
toz(1,*)=dta(4,*)
toz(2,*)=dta(3,*)
toz(3,*)=dta(2,*)
return
end

pro reform_array,fs,ys,ms,smean
nr=where(smean gt 0,nrt)
fs=fs(nr)
ys=ys(nr)
ms=ms(nr)
smean=smean(nr)
end



;*********************************************
;
; define zonal bands
;
;*********************************************
latmin=-60
latmax=60
nsmooth=3

cmicol=8
msrcol=233
woudccol=155;232
tomscol=72;231
noaacol=154;226
gomecol=222
gtocol=151;228

msrcol=201
msrcol=235
woudccol=233
tomscol=234;231
noaacol=238;226
gomecol=232
gtocol=236;228

eesccol=205;212
s80color=124
s86color=122

y0ref=1998
y1ref=2008
y0g=1995
y1g=2020
y0w=1964
y1w=2020
y0t=1970
y1t=2020
y0m=1970
y1m=2020
y0d=1995
y1d=2020
y0o=1970
y1o=2012
y0n=1978
y1n=2020
plot_y0=1963
plot_y1=2022
ymin=1964
ymax=y1g>y1d>y1t>y1n>y1w>y1m
;ymax=ymax+1
yr_range=digits2string(ymin,0)+'-'+digits2string(ymax,0)

sx_letter=plot_y0+(plot_y1-plot_y0)*.03
sx_legend=plot_y0+(plot_y1-plot_y0)*.45
sx_color=plot_y0+(plot_y1-plot_y0)*.03

cmi_path='C:\Users\weber\000mydocuments\GOME_SCIA\CCM\'

pthg='C:\Users\weber\000mydocuments\GOME_SCIA\GOMESCIA_monthly\montlymeanzonalmean\'
fleg=pthg+'GSG_merged_zonalmean.dat'
flew='../WOUDC/gb_1964-2020_za_final.txt'
flen='C:\Users\weber\000mydocuments\GOME_SCIA\TOMSSBUV\noaa\2020\total_o3_7820.dat'
flet='../TOMSSBUV/SBUV/2020/sbuv.v87.mod_v12.70-20.za.txt'
fled=pthg+'GTO-ECV_CCI_OMI_ext.zonalmean.1995-2020.dat'
flem='../MSR/toc_zonal_monthly_mean_1970_2020_msr2.txt'





yrnow=2017
yrnowbar=.5

;*********************************************



title='total ozone timeseries '+yr_range

fle='../TOMSSBUV/MOD_V8_ann_mean.1970-2012.txt'
read_modv8annual,fle,yr80,toz80
fle='../TOMSSBUV/MOD_V8.6_ann_mean.1970-2011.txt'
read_modv8annual,fle,yr86,toz86

n=2011-1964+1
yr_eesc=1964+findgen(n)
read_fle,'C:\Users\weber\000mydocuments\manuscripts\BAMS_CLIMATE\bams_2012\EESC_S30-S60.dat',eesc_sh,header=3
read_fle,'C:\Users\weber\000mydocuments\manuscripts\BAMS_CLIMATE\bams_2012\EESC_N30-N60.dat',eesc_nh,header=3
read_fle,'C:\Users\weber\000mydocuments\manuscripts\BAMS_CLIMATE\bams_2012\EESC_S25-N25.dat',eesc_tr,header=3


set_plot,'PS'
fle='plot_o3timeseries_global'+ digits2string(ymin,0)+'_'+$
                          digits2string(ymax,0)+'.ps'
;digits2string(latmin,0)+'_'+digits2string(latmax,0)+'_'+$

device,file=fle,$
         /color,/portrait,xoffset=2.5,yoffset=0,xsize=13,ysize=30
tek_color_modify
!P.thick=5
!y.thick=4
!x.thick=4
!P.font=3
!P.charsize=2.5
!P.multi=[0,1,5]
!y.minor=0
pos=fltarr(5,4)
pwidth=0.3




pos(0,*)=[0.2,.746,0.99,.900]
pos(1,*)=[0.2,.500,0.99,.746]
pos(2,*)=[0.2,.346,0.99,.500]
pos(3,*)=[0.2,.100,0.99,.346]

pos(0,*)=[0.2,.8,0.99,.9]
pos(1,*)=[0.2,.64,0.99,.8]
pos(2,*)=[0.2,.54,0.99,.64]
pos(3,*)=[0.2,.38,0.99,.54]
pos(4,*)=[0.2,.1,0.99,.38]

;------------------------------ plot 1 (global)
latmin=-60 & latmax=60
month0=1 & month1=12


read_o3_zm,fleg,y0g,y1g,fyrg,mog,ozg,latmin,latmax,month0,month1
read_o3_zm,flew,y0w,y1w,fyrw,mow,ozw,latmin,latmax,month0,month1
read_o3_zm,flen,y0n,y1n,fyrn,mon,ozn,latmin,latmax,month0,month1
read_o3_zm,flet,y0t,y1t,fyrt,mot,ozt,latmin,latmax,month0,month1
read_o3_zm,fled,y0d,y1d,fyrd,modi,ozd,latmin,latmax,month0,month1
read_o3_zm,flem,y0m,y1m,fyrm,mom,ozm,latmin,latmax,month0,month1
nr=where(fyrm lt 1979)
ozm(nr)=0.
;read_o3_zm,fleo,y0o,y1o,fyro,moo,ozo,latmin,latmax,month0,month1
annual_mean_anomaly,fyrg,ozg,ozga,y0ref,y1ref,offg
annual_mean_anomaly,fyrw,ozw,ozwa,y0ref,y1ref,offw
annual_mean_anomaly,fyrn,ozn,ozna,y0ref,y1ref,offn
annual_mean_anomaly,fyrt,ozt,ozta,y0ref,y1ref,offt
annual_mean_anomaly,fyrd,ozd,ozda,y0ref,y1ref,offd
annual_mean_anomaly,fyrm,ozm,ozma,y0ref,y1ref,offm
toz_mean=(offg+offw+offn+offt+offd+offm)/6.
ozg=ozg-offg+toz_mean
ozw=ozw-offw+toz_mean
ozn=ozn-offn+toz_mean
ozt=ozt-offt+toz_mean
ozd=ozd-offd+toz_mean
ozm=ozm-offm+toz_mean

fle=cmi_path+'CCMI_refc2_toz_stats_60s60n.dat'
read_cmi,fle,cmi_yy,cmi_ozone
cmi_ozone=toz_mean*(1+cmi_ozone/100.)

slat0=strarr(4)
slat1=strarr(4)
if latmin lt 0 then begin
  slatmin=digits2string(-latmin,0)+textoidl('\circS')
  endif else begin
  slatmin=digits2string(latmin,0)+textoidl('\circN')
endelse

if latmax lt 0 then begin
  slatmax=digits2string(-latmax,0)+textoidl('\circS')
  endif else begin
  slatmax=digits2string(latmax,0)+textoidl('\circN')
endelse

slat0(0)=slatmin
slat1(0)=slatmax
!x.minor=5
!y.minor=2

plot,fyrw,ozw,/nodata,title=title,ytitle='DU',xstyle=1,ystyle=1,$
    position=reform(pos(0,*)),yrange=[275.01,299.9],xrange=[plot_y0,plot_y1], xtickname=replicate(' ',20)
;nr=where(fyrw le (yrnow-1))
oplot,cmi_yy,cmi_ozone,color=cmicol,thick=10
;nr=where(fyrw gt 1970 and fyrw le 1979,nwt)
nr=where(fyrw gt 1964 and fyrw le 1980,nwt)
pre_o3=total(ozw(nr))/(nwt+0.)
oplot,[1900,2100],[pre_o3,pre_o3],color=140,thick=1,line=1

nr=where(fyrw le 2100)
plot_segment,fyrw(nr),ozw(nr),1.5,thick=2,line=0,color=woudccol
;nr=where(fyrw ge (yrnow-1))
;oplot,fyrw(nr),ozw(nr),thick=2,line=0,color=woudccol
plot_segment,fix(fyrt),ozt,1.5,thick=2,line=0,color=tomscol,pwidth=.25
;oplot,fix(fyrt),ozt,psym=1,symsize=.05,color=tomscol
plot_segment,fix(fyrn),ozn,1.5,thick=2,line=0,color=noaacol
plot_segment,fix(fyrg),ozg,1.5,thick=2,line=0,color=gomecol
plot_segment,fix(fyrd),ozd,1.5,thick=2,line=0,color=gtocol
plot_segment,fix(fyrm),ozm,1.5,thick=2,line=0,color=msrcol
;plot_segment,fix(fyro),ozo,1.5,thick=2,line=1,color=tomscol

xyouts,sx_legend-7,295,'near global ('+slat0(0)+'-'+slat1(0)+')',charsize=1.1
xyouts,sx_letter,277,'(a)',charsize=1.5

openw,33,'gsg_'+slatmin+'_'+slatmax+'.dat'
for i=0,n_elements(fyrg)-1 do begin
    printf,33,format='(1x,i4,1x,f5.1)',fyrg(i),ozg(i)
endfor
close,33


;-------------------------------------plot 2 (NH mid)
latmin=35 & latmax=60
;month0=1 & month1=4
month0=1 & month1=12
!x.minor=5
!y.minor=5
if latmin lt 0 then begin
  slatmin=digits2string(-latmin,0)+textoidl('\circS')
  endif else begin
  slatmin=digits2string(latmin,0)+textoidl('\circN')
endelse

if latmax lt 0 then begin
  slatmax=digits2string(-latmax,0)+textoidl('\circS')
  endif else begin
  slatmax=digits2string(latmax,0)+textoidl('\circN')
endelse
slat0(1)=slatmin
slat1(1)=slatmax
read_o3_zm,fleg,y0g,y1g,fyrg,mog,ozg,latmin,latmax,month0,month1
read_o3_zm,flew,y0w,y1w,fyrw,mow,ozw,latmin,latmax,month0,month1
read_o3_zm,flen,y0n,y1n,fyrn,mon,ozn,latmin,latmax,month0,month1
read_o3_zm,flet,y0t,y1t,fyrt,mot,ozt,latmin,latmax,month0,month1
read_o3_zm,fled,y0d,y1d,fyrd,modi,ozd,latmin,latmax,month0,month1
read_o3_zm,flem,y0m,y1m,fyrm,mom,ozm,latmin,latmax,month0,month1
nr=where(fyrm lt 1979)
ozm(nr)=0.
;read_o3_zm,fleo,y0o,y1o,fyro,moo,ozo,latmin,latmax,month0,month1
annual_mean_anomaly,fyrg,ozg,ozga,y0ref,y1ref,offg
annual_mean_anomaly,fyrw,ozw,ozwa,y0ref,y1ref,offw
annual_mean_anomaly,fyrn,ozn,ozna,y0ref,y1ref,offn
annual_mean_anomaly,fyrt,ozt,ozta,y0ref,y1ref,offt
annual_mean_anomaly,fyrd,ozd,ozda,y0ref,y1ref,offd
annual_mean_anomaly,fyrm,ozm,ozma,y0ref,y1ref,offm
toz_mean=(offg+offw+offn+offt+offd+offm)/6.
ozg=ozg-offg+toz_mean
ozw=ozw-offw+toz_mean
ozn=ozn-offn+toz_mean
ozt=ozt-offt+toz_mean
ozd=ozd-offd+toz_mean
ozm=ozm-offm+toz_mean

fle=cmi_path+'CCMI_refc2_toz_stats_35n60n.dat'
read_cmi,fle,cmi_yy,cmi_ozone
cmi_ozone=toz_mean*(1+cmi_ozone/100.)


; polar: 150,520
; midlats: 300,420
plot,fyrw,ozw,/nodata,title='',ytitle='DU',xstyle=1,ystyle=1,$
    position=reform(pos(1,*)),xrange=[plot_y0,plot_y1], xtickname=replicate(' ',20),$
    yrange=[315.01,354.99]
;plot_segment,fix(fyrw),ozw,1.5,thick=8,line=0,color=woudccol
;oplot,cmi_yy,cmi_ozone,color=cmicol,thick=10
;nr=where(fyrw gt 1970 and fyrw le 1979,nwt)
nr=where(fyrw gt 1964 and fyrw le 1980,nwt)
pre_o3=total(ozw(nr))/(nwt+0.)
oplot,[1900,2100],[pre_o3,pre_o3],color=140,thick=1,line=1



;nr=where(fyrw le (yrnow-1))
nr=where(fyrw le 2100)
plot_segment,fyrw(nr),ozw(nr),1.5,thick=2,line=0,color=woudccol
;nr=where(fyrw ge (yrnow-1))
;oplot,fyrw(nr),ozw(nr),thick=2,line=0,color=woudccol;color=woudcpre
plot_segment,fix(fyrt),ozt,1.5,thick=2,line=0,color=tomscol,pwidth=.25
;oplot,fix(fyrt),ozt,psym=1,symsize=.05,color=tomscol
plot_segment,fix(fyrn),ozn,1.5,thick=2,line=0,color=noaacol
plot_segment,fix(fyrg),ozg,1.5,thick=2,line=0,color=gomecol
plot_segment,fix(fyrd),ozd,1.5,thick=2,line=0,color=gtocol
plot_segment,fix(fyrm),ozm,1.5,thick=2,line=0,color=msrcol
;plot_segment,fix(fyro),ozo,1.5,thick=2,line=1,color=tomscol

;nr=where(fyrw eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozw(nr),ozw(nr)],thick=4,line=0,color=woudccol

;nr=where(fyrt eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozt(nr),ozt(nr)],thick=4,line=0,color=tomscol
;plot_segment,fix(fyrn),ozn,1.5,thick=6,line=0,color=noaacol
;nr=where(fix(fyrn) eq 2011,nrt)
;;oplot,yrnow+[0.,yrnowbar],[ozn(nr),ozn(nr)],thick=4,line=0,color=noaacol
;plot_segment,fix(fyro),ozo,1.5,thick=6,line=0,color=omicol
;plot_segment,fix(fyrg),ozg,1.5,thick=6,line=0,color=gomecol
;nr=where(fyrg eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozg(nr),ozg(nr)],thick=4,line=0,color=gomecol
nr80=where(toz80(1,*) lt 1000.)
nr86=where(toz86(1,*) lt 1000.)
y80=yr80(nr80)
t80=reform(toz80(1,nr80))
y86=yr86(nr86)
t86=reform(toz86(1,nr86))
;synchronise,x1,y1,x2,y2,x,z1,z2,i1,i2,tolerance
synchronise,y80,t80,y86,t86,x,z1,z2,i
cc=linfit(z1,z2)
nr=where(y80 eq 2012)
y86=[y86,2012]
t86=[t86,cc(0)+cc(1)*t80(nr)]
;plot_segment,yr80(nr80),toz80(1,nr80),1.5,thick=6,line=0,color=s80color
;plot_segment,yr86(nr86),toz86(1,nr86),1.5,thick=6,line=0,color=s86color
;plot_segment,y86,t86,1.5,thick=6,line=0,color=tomscol,pwidth=pwidth

;nr=where(fyrg eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozg(nr),ozg(nr)],thick=4,line=0,color=gomecol

;oplot,yr_eesc,eesc_nh,color=eesccol




xyouts,sx_legend,349,'NH ('+slat0(1)+'-'+slat1(1)+')',charsize=1.1
;xyouts,sx_color,330,'WOUDC',color=woudccol,charsize=.9
;xyouts,sx_color,328,'SBUV V8.7 NASA',color=tomscol,charsize=.9
;xyouts,sx_color,326,'SBUV V8.7 NOAA',color=noaacol,charsize=.9
;xyouts,sx_color,324,'GOME/SCIA GSG',color=gomecol,charsize=.9
;xyouts,sx_color,322,'GOME/SCIA GTO',color=gtocol,charsize=.9
;xyouts,sx_color,320,'MSR2',color=msrcol,charsize=.9
;xyouts,sx_color,318,'  preliminary WOUDC data in 2012',color=woudcpre,charsize=.9
;xyouts,sx_color,321,'EESC fit (1970-2012)',color=eesccol,charsize=.9

;xyouts,1971.12,311,'OMI (OMTO3)',color=omicol,charsize=.9
xyouts,sx_letter,317,'(b)',charsize=1.5
;device,/close

openw,33,'gsg_'+slatmin+'_'+slatmax+'.dat'
for i=0,n_elements(fyrg)-1 do begin
    printf,33,format='(1x,i4,1x,f5.1)',fyrg(i),ozg(i)
endfor
close,33



;------------------------------ plot 3 (tropics)
latmin=-20 & latmax=20
month0=1 & month1=12
!x.minor=5
!y.minor=2
 if latmin lt 0 then begin
  slatmin=digits2string(-latmin,0)+textoidl('\circS')
  endif else begin
  slatmin=digits2string(latmin,0)+textoidl('\circN')
endelse

if latmax lt 0 then begin
  slatmax=digits2string(-latmax,0)+textoidl('\circS')
  endif else begin
  slatmax=digits2string(latmax,0)+textoidl('\circN')
endelse
slat0(3)=slatmin
slat1(3)=slatmax


read_o3_zm,fleg,y0g,y1g,fyrg,mog,ozg,latmin,latmax,month0,month1
read_o3_zm,flew,y0w,y1w,fyrw,mow,ozw,latmin,latmax,month0,month1
read_o3_zm,flen,y0n,y1n,fyrn,mon,ozn,latmin,latmax,month0,month1
read_o3_zm,flet,y0t,y1t,fyrt,mot,ozt,latmin,latmax,month0,month1
;read_o3_zm,fleo,y0o,y1o,fyro,moo,ozo,latmin,latmax,month0,month1
read_o3_zm,fled,y0d,y1d,fyrd,modi,ozd,latmin,latmax,month0,month1
read_o3_zm,flem,y0m,y1m,fyrm,mom,ozm,latmin,latmax,month0,month1
nr=where(fyrm lt 1979)
ozm(nr)=0.
annual_mean_anomaly,fyrg,ozg,ozga,y0ref,y1ref,offg
annual_mean_anomaly,fyrw,ozw,ozwa,y0ref,y1ref,offw
annual_mean_anomaly,fyrn,ozn,ozna,y0ref,y1ref,offn
annual_mean_anomaly,fyrt,ozt,ozta,y0ref,y1ref,offt
annual_mean_anomaly,fyrd,ozd,ozda,y0ref,y1ref,offd
annual_mean_anomaly,fyrm,ozm,ozma,y0ref,y1ref,offm
toz_mean=(offg+offw+offn+offt+offd+offm)/6.
ozg=ozg-offg+toz_mean
ozw=ozw-offw+toz_mean
ozn=ozn-offn+toz_mean
ozt=ozt-offt+toz_mean
ozd=ozd-offd+toz_mean
ozm=ozm-offm+toz_mean


fle=cmi_path+'CCMI_refc2_toz_stats_20s20n.dat'
read_cmi,fle,cmi_yy,cmi_ozone
cmi_ozone=toz_mean*(1+cmi_ozone/100.)


;!y.ticklen=.006
;!x.ticklen=.06


plot,fyrw,ozw,/nodata,title='',ytitle='DU',xstyle=1,ystyle=1,$
    position=reform(pos(2,*)),yrange=[250.01,274.99],xrange=[plot_y0,plot_y1], $
    xtickname=replicate(' ',20)
xyouts,sx_legend-3,270,'tropics ('+slat0(3)+'-'+slat1(3)+')',charsize=1.1
;oplot,cmi_yy,cmi_ozone,color=cmicol,thick=10
;nr=where(fyrw gt 1970 and fyrw le 1979,nwt)
nr=where(fyrw gt 1964 and fyrw le 1980,nwt)
pre_o3=total(ozw(nr))/(nwt+0.)
oplot,[1900,2100],[pre_o3,pre_o3],color=140,thick=1,line=1



;nr=where(fyrw le (yrnow-1))
nr=where(fyrw le 2100)
plot_segment,fyrw(nr),ozw(nr),1.5,thick=2,line=0,color=woudccol
nr=where(fyrw ge (yrnow-1))
;oplot,fyrw(nr),ozw(nr),thick=4,line=0,color=woudccol;color=woudcpre
;nr=where(fyrw ge (yrnow-1))
;oplot,fyrw(nr),ozw(nr),thick=10,line=0,color=woudccol
;nr=where(fyrw eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozw(nr),ozw(nr)],thick=4,line=0,color=woudccol
plot_segment,fix(fyrt),ozt,1.5,thick=2,line=0,color=tomscol,pwidth=.25
;oplot,fix(fyrt),ozt,psym=1,symsize=.05,color=tomscol
plot_segment,fix(fyrn),ozn,1.5,thick=2,line=0,color=noaacol
plot_segment,fix(fyrg),ozg,1.5,thick=2,line=0,color=gomecol
plot_segment,fix(fyrd),ozd,1.5,thick=2,line=0,color=gtocol
plot_segment,fix(fyrm),ozm,1.5,thick=2,line=0,color=msrcol
;plot_segment,fix(fyro),ozo,1.5,thick=2,line=1,color=tomscol
;nr=where(fyrt eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozt(nr),ozt(nr)],thick=4,line=0,color=tomscol
;plot_segment,fix(fyrn),ozn,1.5,thick=6,line=0,color=noaacol
;nr=where(fix(fyrn) eq 2011,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozn(nr),ozn(nr)],thick=4,line=0,color=noaacol
;plot_segment,fix(fyro),ozo,1.5,thick=6,line=0,color=omicol
nr80=where(toz80(2,*) lt 1000.)
nr86=where(toz86(2,*) lt 1000.)
y80=yr80(nr80)
t80=reform(toz80(2,nr80))
y86=yr86(nr86)
t86=reform(toz86(2,nr86))
;synchronise,x1,y1,x2,y2,x,z1,z2,i1,i2,tolerance
synchronise,y80,t80,y86,t86,x,z1,z2,i
cc=linfit(z1,z2)
nr=where(y80 eq 2012)
y86=[y86,2012]
t86=[t86,cc(0)+cc(1)*t80(nr)]
;plot_segment,yr80(nr80),toz80(1,nr80),1.5,thick=6,line=0,color=s80color
;plot_segment,yr86(nr86),toz86(1,nr86),1.5,thick=6,line=0,color=s86color
;plot_segment,y86,t86,1.5,thick=6,line=0,color=tomscol,pwidth=pwidth
;nr=where(fyrg eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozg(nr),ozg(nr)],thick=4,line=0,color=gomecol
;oplot,yr_eesc,eesc_tr,color=eesccol

xyouts,sx_letter,252.5,'(c)',charsize=1.5

openw,33,'gsg_'+slatmin+'_'+slatmax+'.dat'
for i=0,n_elements(fyrg)-1 do begin
    printf,33,format='(1x,i4,1x,f5.1)',fyrg(i),ozg(i)
endfor
close,33


;------------------------------ plot 4 (SH mid)
latmin=-60 & latmax=-35
month0=8 & month1=10
month0=1 & month1=12
!x.minor=5
!y.minor=5
if latmin lt 0 then begin
  slatmin=digits2string(-latmin,0)+textoidl('\circS')
  endif else begin
  slatmin=digits2string(latmin,0)+textoidl('\circN')
endelse

if latmax lt 0 then begin
  slatmax=digits2string(-latmax,0)+textoidl('\circS')
  endif else begin
  slatmax=digits2string(latmax,0)+textoidl('\circN')
endelse
slat0(2)=slatmin
slat1(2)=slatmax


read_o3_zm,fleg,y0g,y1g,fyrg,mog,ozg,latmin,latmax,month0,month1
read_o3_zm,flew,y0w,y1w,fyrw,mow,ozw,latmin,latmax,month0,month1
read_o3_zm,flen,y0n,y1n,fyrn,mon,ozn,latmin,latmax,month0,month1
read_o3_zm,flet,y0t,y1t,fyrt,mot,ozt,latmin,latmax,month0,month1
;read_o3_zm,fleo,y0o,y1o,fyro,moo,ozo,latmin,latmax,month0,month1
read_o3_zm,fled,y0d,y1d,fyrd,modi,ozd,latmin,latmax,month0,month1
read_o3_zm,flem,y0m,y1m,fyrm,mom,ozm,latmin,latmax,month0,month1
nr=where(fyrm lt 1979)
ozm(nr)=0.
annual_mean_anomaly,fyrg,ozg,ozga,y0ref,y1ref,offg
annual_mean_anomaly,fyrw,ozw,ozwa,y0ref,y1ref,offw
annual_mean_anomaly,fyrn,ozn,ozna,y0ref,y1ref,offn
annual_mean_anomaly,fyrt,ozt,ozta,y0ref,y1ref,offt
annual_mean_anomaly,fyrd,ozd,ozda,y0ref,y1ref,offd
annual_mean_anomaly,fyrm,ozm,ozma,y0ref,y1ref,offm
toz_mean=(offg+offw+offn+offt+offd+offm)/6.
ozg=ozg-offg+toz_mean
ozw=ozw-offw+toz_mean
ozn=ozn-offn+toz_mean
ozt=ozt-offt+toz_mean
ozd=ozd-offd+toz_mean
ozm=ozm-offm+toz_mean

fle=cmi_path+'CCMI_refc2_toz_stats_60s35s.dat'
read_cmi,fle,cmi_yy,cmi_ozone
cmi_ozone=toz_mean*(1+cmi_ozone/100.)


plot,fyrw,ozw,/nodata,title='',ytitle='DU',xstyle=1,ystyle=1,$
    position=reform(pos(3,*)),yrange=[293.01,331.99],xrange=[plot_y0,plot_y1],$
    xtickname=replicate(' ',20)
xyouts,sx_legend,320,'SH ('+slat1(2)+'-'+slat0(2)+')',charsize=1.1
;oplot,cmi_yy,cmi_ozone,color=cmicol,thick=10
;nr=where(fyrw gt 1970 and fyrw le 1979,nwt)
nr=where(fyrw gt 1964 and fyrw le 1980,nwt)
pre_o3=total(ozw(nr))/(nwt+0.)
oplot,[1900,2100],[pre_o3,pre_o3],color=140,thick=1,line=1
xyouts,2007,pre_o3+1,'1964-1980',color=140,charsize=.6


nr=where(fyrw le (yrnow-1))
nr=where(fyrw le 2100)
plot_segment,fyrw(nr),ozw(nr),1.5,thick=2,line=0,color=woudccol
;nr=where(fyrw ge (yrnow-1))
;oplot,fyrw(nr),ozw(nr),thick=4,line=0,color=woudccol;color=woudcpre
plot_segment,fix(fyrt),ozt,1.5,thick=2,line=0,color=tomscol,pwidth=.25
plot_segment,fix(fyrn),ozn,1.5,thick=2,line=0,color=noaacol
plot_segment,fix(fyrg),ozg,1.5,thick=2,line=0,color=gomecol
plot_segment,fix(fyrd),ozd,1.5,thick=2,line=0,color=gtocol
plot_segment,fix(fyrm),ozm,1.5,thick=2,line=0,color=msrcol
;plot_segment,fix(fyro),ozo,1.5,thick=2,line=1,color=tomscol
;nr=where(fyrw ge (yrnow-1))
;oplot,fyrw(nr),ozw(nr),thick=10,line=0,color=woudccol
;nr=where(fyrw eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozw(nr),ozw(nr)],thick=4,line=0,color=woudccol
;nr=where(fyrt eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozt(nr),ozt(nr)],thick=4,line=0,color=tomscol
;plot_segment,fix(fyrn),ozn,1.5,thick=6,line=0,color=noaacol
;nr=where(fix(fyrn) eq 2011,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozn(nr),ozn(nr)],thick=4,line=0,color=noaacol
;plot_segment,fix(fyro),ozo,1.5,thick=6,line=0,color=omicol
nr80=where(toz80(3,*) lt 1000.)
nr86=where(toz86(3,*) lt 1000.)
y80=yr80(nr80)
t80=reform(toz80(3,nr80))
y86=yr86(nr86)
t86=reform(toz86(3,nr86))
;synchronise,x1,y1,x2,y2,x,z1,z2,i1,i2,tolerance
synchronise,y80,t80,y86,t86,x,z1,z2,i
cc=linfit(z1,z2)
nr=where(y80 eq 2012)
y86=[y86,2012]
t86=[t86,cc(0)+cc(1)*t80(nr)]
;plot_segment,yr80(nr80),toz80(1,nr80),1.5,thick=6,line=0,color=s80color
;plot_segment,yr86(nr86),toz86(1,nr86),1.5,thick=6,line=0,color=s86color
;plot_segment,y86,t86,1.5,thick=6,line=0,color=tomscol,pwidth=pwidthl
;nr=where(fyrg eq yrnow,nrt)
;oplot,yrnow+[0.,yrnowbar],[ozg(nr),ozg(nr)],thick=4,line=0,color=gomecol

;oplot,yr_eesc,eesc_sh,color=eesccol

xyouts,sx_letter,296,'(d)',charsize=1.5

openw,33,'gsg_'+slatmin+'_'+slatmax+'.dat'
for i=0,n_elements(fyrg)-1 do begin
    printf,33,format='(1x,i4,1x,f5.1)',fyrg(i),ozg(i)
endfor
close,33

;------------------------------plot 5 (polar)
latmin=-90 & latmax=-60

if latmin lt 0 then begin
  slatmin=digits2string(-latmin,0)+textoidl('\circS')
  endif else begin
  slatmin=digits2string(latmin,0)+textoidl('\circN')
endelse

if latmax lt 0 then begin
  slatmax=digits2string(-latmax,0)+textoidl('\circS')
  endif else begin
  slatmax=digits2string(latmax,0)+textoidl('\circN')
endelse
slat0(2)=slatmin
slat1(2)=slatmax
month0=10 & month1=10

read_o3_zm,fleg,y0g,y1g,fyrg,mog,ozg,latmin,latmax,month0,month1
read_o3_zm,flew,y0w,y1w,fyrw,mow,ozw,latmin,latmax,month0,month1
read_o3_zm,flet,y0t,y1t,fyrt,mot,ozt,latmin,latmax,month0,month1
read_o3_zm,flen,y0n,y1n,fyrn,mon,ozn,latmin,latmax,month0,month1
;read_o3_zm,fleo,y0o,y1o,fyro,moo,ozo,latmin,latmax,month0,month1
read_o3_zm,fled,y0d,y1d,fyrd,modi,ozd,latmin,latmax,month0,month1
read_o3_zm,flem,y0m,y1m,fyrm,mom,ozm,latmin,latmax,month0,month1
nr=where(fyrm lt 1979)
ozm(nr)=0.
annual_mean_anomaly,fyrg,ozg,ozga,y0ref,y1ref,offg
annual_mean_anomaly,fyrw,ozw,ozwa,y0ref,y1ref,offw
annual_mean_anomaly,fyrn,ozn,ozna,y0ref,y1ref,offn
annual_mean_anomaly,fyrt,ozt,ozta,y0ref,y1ref,offt
annual_mean_anomaly,fyrd,ozd,ozda,y0ref,y1ref,offd
annual_mean_anomaly,fyrm,ozm,ozma,y0ref,y1ref,offm
toz_mean=(offg+offw+offn+offt+offd+offm)/6.
ozg=ozg-offg+toz_mean
ozw=ozw-offw+toz_mean
ozn=ozn-offn+toz_mean
ozt=ozt-offt+toz_mean
ozd=ozd-offd+toz_mean
ozm=ozm-offm+toz_mean

close,12
openw,12,'polar_ozone_SH.dat'
printf,12,'# October 60S-90S ozone [DU]'
printf,12,'# WOUDC data'
for i=0,n_elements(fyrw)-1 do begin
	printf,12,fix(fyrw(i)),ozw(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# MSR data'
for i=0,n_elements(fyrm)-1 do begin
	printf,12,fix(fyrm(i)),ozm(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# SBUV V8.7 NASA (MOD)'
for i=0,n_elements(fyrt)-1 do begin
	printf,12,fix(fyrt(i)),ozt(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# SBUV V8.7 NOAA (COH)'
for i=0,n_elements(fyrn)-1 do begin
	printf,12,fix(fyrn(i)),ozn(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# GOME/SCIA GSG'
for i=0,n_elements(fyrg)-1 do begin
	printf,12,fix(fyrg(i)),ozg(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# GOME/SCIA GTO'
for i=0,n_elements(fyrd)-1 do begin
	printf,12,fix(fyrd(i)),ozd(i),format='(1x,i4,1x,f5.1)'
endfor
close,12

;device,/close


;plot_y1=2015
;set_plot,'PS'
;fle='plot_o3timeseries_polar'+ digits2string(plot_y0,0)+'_'+$
;                          digits2string(plot_y1,0)+'.ps'
;device,file=fle,$
;         /color,/portrait,xoffset=2.5,yoffset=0,xsize=13,ysize=25
;tek_color_modify
;P.charsize=3.
;pos(3,*)=[0.2,.100,0.99,.5]
plot,fyrw,ozw,/nodata,title='',ytitle='DU',xstyle=1,ystyle=1,$
    position=reform(pos(4,*)),yrange=[180,500],xrange=[plot_y0,plot_y1]
xyouts,sx_legend-7,328,'SH October ('+slat1(2)+'-'+slat0(2)+')',charsize=1.1

;nr=where(fyrw gt 1970 and fyrw le 1979,nwt)
nr=where(fyrw gt 1964 and fyrw le 1980,nwt)
pre_o3=total(ozw(nr))/(nwt+0.)
oplot,[1900,2100],[pre_o3,pre_o3],color=140,thick=1,line=1

nr=where(fyrw le (yrnow-1))
nr=where(fyrw le 2100)
plot_segment,fyrw(nr),ozw(nr),1.5,thick=2,line=0,color=woudccol
;nr=where(fyrw ge (yrnow-1))
;oplot,fyrw(nr),ozw(nr),thick=4,line=0,color=woudccol;color=woudcpre
plot_segment,fix(fyrt),ozt,1.5,thick=2,line=0,color=tomscol,pwidth=.25
plot_segment,fix(fyrn),ozn,1.5,thick=2,line=0,color=noaacol
plot_segment,fix(fyrd),ozd,1.5,thick=2,line=0,color=gtocol
plot_segment,fix(fyrg),ozg,1.5,thick=2,line=0,color=gomecol
plot_segment,fix(fyrm),ozm,1.5,thick=2,line=0,color=msrcol
;plot_segment,fix(fyro),ozo,1.5,thick=2,line=1,color=tomscol
polar_endyear=2020
ny=polar_endyear-1964+1
ozsh=fltarr(ny)*0.
openw,33,'SH_polar_ozone.txt'
printf,33,'# 60S-90S, October average from NASA SBUV, WOUDC, and GSG'
for iy=1964,polar_endyear do begin
	sum=0.
	nsum=0
	nr=where(fix(fyrt) eq iy,nrt)
	if (nrt gt 0) then begin
		sum=sum+ozt(nr(0))
		nsum=nsum+1
	endif
	nr=where(fix(fyrw) eq iy and fix(fyrw) ne 2014,nrt)
	if (nrt gt 0) then begin
		sum=sum+ozw(nr(0))
		nsum=nsum+1
	endif
	nr=where(fix(fyrg) eq iy,nrt)
	if (nrt gt 0) then begin
		sum=sum+ozg(nr(0))
		nsum=nsum+1
	endif
	if nsum gt 0 then ozsh(iy-1964)=sum/(nsum+0.)
	printf,33,iy,ozsh(iy-1964),nsum,format='(1x,i4,1x,f5.1,1x,i2)'
	print,iy,ozsh(iy-1964),nsum,format='(1x,i4,1x,f5.1,1x,i2)'
endfor
close,33
latmin=60 & latmax=90
if latmin lt 0 then begin
  slatmin=digits2string(-latmin,0)+textoidl('\circS')
  endif else begin
  slatmin=digits2string(latmin,0)+textoidl('\circN')
endelse

if latmax lt 0 then begin
  slatmax=digits2string(-latmax,0)+textoidl('\circS')
  endif else begin
  slatmax=digits2string(latmax,0)+textoidl('\circN')
endelse
slat0(2)=slatmin
slat1(2)=slatmax
month0=3 & month1=3
read_o3_zm,fleg,y0g,y1g,fyrg,mog,ozg,latmin,latmax,month0,month1
read_o3_zm,flew,y0w,y1w,fyrw,mow,ozw,latmin,latmax,month0,month1
read_o3_zm,flet,y0t,y1t,fyrt,mot,ozt,latmin,latmax,month0,month1
read_o3_zm,flen,y0n,y1n,fyrn,mon,ozn,latmin,latmax,month0,month1
;read_o3_zm,fleo,y0o,y1o,fyro,moo,ozo,latmin,latmax,month0,month1
read_o3_zm,fled,y0d,y1d,fyrd,modi,ozd,latmin,latmax,month0,month1
read_o3_zm,flem,y0m,y1m,fyrm,mom,ozm,latmin,latmax,month0,month1
nr=where(fyrm lt 1979)
ozm(nr)=0.
annual_mean_anomaly,fyrg,ozg,ozga,y0ref,y1ref,offg
annual_mean_anomaly,fyrw,ozw,ozwa,y0ref,y1ref,offw
annual_mean_anomaly,fyrn,ozn,ozna,y0ref,y1ref,offn
annual_mean_anomaly,fyrt,ozt,ozta,y0ref,y1ref,offt
annual_mean_anomaly,fyrd,ozd,ozda,y0ref,y1ref,offd
annual_mean_anomaly,fyrm,ozm,ozma,y0ref,y1ref,offm
toz_mean=(offg+offw+offn+offt+offd+offm)/6.
ozg=ozg-offg+toz_mean
ozw=ozw-offw+toz_mean
ozn=ozn-offn+toz_mean
ozt=ozt-offt+toz_mean
ozd=ozd-offd+toz_mean
ozm=ozm-offm+toz_mean

close,12
openw,12,'polar_ozone_NH.dat'
printf,12,'# March 60N-90N ozone [DU]'
printf,12,'# WOUDC data'
for i=0,n_elements(fyrw)-1 do begin
	printf,12,fix(fyrw(i)),ozw(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# MSR data'
for i=0,n_elements(fyrm)-1 do begin
	printf,12,fix(fyrm(i)),ozm(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# SBUV V8.6 NASA (MOD)'
for i=0,n_elements(fyrt)-1 do begin
	printf,12,fix(fyrt(i)),ozt(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# SBUV V8.6 NOAA (COH)'
for i=0,n_elements(fyrn)-1 do begin
	printf,12,fix(fyrn(i)),ozn(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# GOME/SCIA GSG'
for i=0,n_elements(fyrg)-1 do begin
	printf,12,fix(fyrg(i)),ozg(i),format='(1x,i4,1x,f5.1)'
endfor
printf,12,'# GOME/SCIA GTO'
for i=0,n_elements(fyrd)-1 do begin
	printf,12,fix(fyrd(i)),ozd(i),format='(1x,i4,1x,f5.1)'
endfor
close,12

;nr=where(fyrw gt 1970 and fyrw le 1979,nwt)
nr=where(fyrw gt 1964 and fyrw le 1980,nwt)
pre_o3=total(ozw(nr))/(nwt+0.)
oplot,[1900,2100],[pre_o3,pre_o3],color=140,thick=1,line=1



nr=where(fyrw le (yrnow-1))
nr=where(fyrw le 2100)
plot_segment,fyrw(nr),ozw(nr),1.5,thick=2,line=0,color=woudccol
;nr=where(fyrw ge (yrnow-1))

;oplot,fyrw(nr),ozw(nr),thick=4,line=0,color=woudccol;color=woudcpre
plot_segment,fix(fyrt),ozt,1.5,thick=2,line=0,color=tomscol,pwidth=.25
plot_segment,fix(fyrn),ozn,1.5,thick=2,line=0,color=noaacol
plot_segment,fix(fyrd),ozd,1.5,thick=2,line=0,color=gtocol
plot_segment,fix(fyrg),ozg,1.5,thick=2,line=0,color=gomecol
plot_segment,fix(fyrm),ozm,1.5,thick=2,line=0,color=msrcol
;plot_segment,fix(fyro),ozo,1.5,thick=2,line=1,color=tomscol
ny=polar_endyear-1964+1
ozsh=fltarr(ny)*0.
close,33
openw,33,'NH_polar_ozone.txt'
printf,33,'# 60N-90N, March average from NASA SBUV, WOUDC, and GSG'
for iy=1964,polar_endyear do begin
	sum=0.
	nsum=0
	nr=where(fix(fyrt) eq iy,nrt)
	if (nrt gt 0) then begin
		sum=sum+ozt(nr(0))
		nsum=nsum+1
	endif
	nr=where(fix(fyrw) eq iy and fix(fyrw) ne 2014,nrt)
	if (nrt gt 0) then begin
		sum=sum+ozw(nr(0))
		nsum=nsum+1
	endif
	nr=where(fix(fyrg) eq iy,nrt)
	if (nrt gt 0) then begin
		sum=sum+ozg(nr(0))
		nsum=nsum+1
	endif
	if nsum gt 0 then ozsh(iy-1964)=sum/(nsum+0.)
	printf,33,iy,ozsh(iy-1964),nsum,format='(1x,i4,1x,f5.1,1x,i2)'
	print,iy,ozsh(iy-1964),nsum,format='(1x,i4,1x,f5.1,1x,i2)'
endfor
close,33

xyouts,sx_letter,300.,'(e)',charsize=1.5
xyouts,sx_legend-7,472.,'NH March ('+slat0(2)+'-'+slat1(2)+')',charsize=1.1

s0pos=190
dpos=11
xyouts,sx_color,s0pos+0*dpos,'WOUDC',color=woudccol,charsize=.7
xyouts,sx_color,s0pos+1*dpos,'SBUV V8.7/OMPS NASA (MOD)',color=tomscol,charsize=.7
xyouts,sx_color,s0pos+2*dpos,'SBUV V8.7/OMPS NOAA (COH)',color=noaacol,charsize=.7
xyouts,sx_color,s0pos+3*dpos,'GOME/SCIA GSG',color=gomecol,charsize=.7
xyouts,sx_color,s0pos+4*dpos,'GOME/SCIA/OMI GTO',color=gtocol,charsize=.7
xyouts,sx_color,s0pos+5*dpos,'MSR2',color=msrcol,charsize=.7
xyouts,sx_color,s0pos+6*dpos,'median CCMI models',color=cmicol,charsize=.7
;xyouts,sx_color,201,'  preliminary data in 2016',color=woudcpre,charsize=.7
device,/close

;================================================= separate polar plot
;plot_y1=2017

set_plot,'PS'
fle='plot_o3timeseries_polar'+ digits2string(ymin,0)+'_'+$
                          digits2string(ymax,0)+'.ps'
device,file=fle,$
         /color,/portrait,xoffset=2.5,yoffset=0,xsize=13,ysize=25
tek_color_modify
!P.charsize=1.7
!P.font=3



latmin=-90 & latmax=-60

if latmin lt 0 then begin
  slatmin=digits2string(-latmin,0)+textoidl('\circS')
  endif else begin
  slatmin=digits2string(latmin,0)+textoidl('\circN')
endelse

if latmax lt 0 then begin
  slatmax=digits2string(-latmax,0)+textoidl('\circS')
  endif else begin
  slatmax=digits2string(latmax,0)+textoidl('\circN')
endelse
slat0(2)=slatmin
slat1(2)=slatmax
month0=10 & month1=10

read_o3_zm,fleg,y0g,y1g,fyrg,mog,ozg,latmin,latmax,month0,month1
read_o3_zm,flew,y0w,y1w,fyrw,mow,ozw,latmin,latmax,month0,month1
read_o3_zm,flet,y0t,y1t,fyrt,mot,ozt,latmin,latmax,month0,month1
read_o3_zm,flen,y0n,y1n,fyrn,mon,ozn,latmin,latmax,month0,month1
;read_o3_zm,fleo,y0o,y1o,fyro,moo,ozo,latmin,latmax,month0,month1
read_o3_zm,fled,y0d,y1d,fyrd,modi,ozd,latmin,latmax,month0,month1
read_o3_zm,flem,y0m,y1m,fyrm,mom,ozm,latmin,latmax,month0,month1
annual_mean_anomaly,fyrg,ozg,ozga,y0ref,y1ref,offg
annual_mean_anomaly,fyrw,ozw,ozwa,y0ref,y1ref,offw
annual_mean_anomaly,fyrn,ozn,ozna,y0ref,y1ref,offn
annual_mean_anomaly,fyrt,ozt,ozta,y0ref,y1ref,offt
annual_mean_anomaly,fyrd,ozd,ozda,y0ref,y1ref,offd
annual_mean_anomaly,fyrm,ozm,ozma,y0ref,y1ref,offm
toz_mean=(offg+offw+offn+offt+offd+offm)/6.
ozg=ozg-offg+toz_mean
ozw=ozw-offw+toz_mean
ozn=ozn-offn+toz_mean
ozt=ozt-offt+toz_mean
ozd=ozd-offd+toz_mean
ozm=ozm-offm+toz_mean
pos(3,*)=[0.2,.100,0.99,.5]
plot,fyrw,ozw,/nodata,title='polar total ozone',ytitle='DU',xstyle=1,ystyle=1,$
    position=reform(pos(3,*)),yrange=[170,500],xrange=[plot_y0,plot_y1+1]


nr=where(fyrw le (yrnow-1))
nr=where(fyrw le (yrnow))
plot_segment,fyrw(nr),ozw(nr),1.5,thick=2,line=0,color=woudccol
;nr=where(fyrw ge (yrnow-1))
;oplot,fyrw(nr),ozw(nr),thick=4,line=0,color=woudccol;color=woudcpre
plot_segment,fix(fyrt),ozt,1.5,thick=2,line=0,color=tomscol,pwidth=.25
plot_segment,fix(fyrn),ozn,1.5,thick=2,line=0,color=noaacol
plot_segment,fix(fyrg),ozg,1.5,thick=2,line=0,color=gomecol
plot_segment,fix(fyrd),ozd,1.5,thick=2,line=0,color=gtocol
plot_segment,fix(fyrm),ozm,1.5,thick=2,line=0,color=msrcol
;plot_segment,fix(fyro),ozo,1.5,thick=2,line=1,color=tomscol

latmin=60 & latmax=90
if latmin lt 0 then begin
  slatmin=digits2string(-latmin,0)+textoidl('\circS')
  endif else begin
  slatmin=digits2string(latmin,0)+textoidl('\circN')
endelse

if latmax lt 0 then begin
  slatmax=digits2string(-latmax,0)+textoidl('\circS')
  endif else begin
  slatmax=digits2string(latmax,0)+textoidl('\circN')
endelse
slat0(2)=slatmin
slat1(2)=slatmax
month0=3 & month1=3
read_o3_zm,fleg,y0g,y1g,fyrg,mog,ozg,latmin,latmax,month0,month1
read_o3_zm,flew,y0w,y1w,fyrw,mow,ozw,latmin,latmax,month0,month1
read_o3_zm,flet,y0t,y1t,fyrt,mot,ozt,latmin,latmax,month0,month1
read_o3_zm,flen,y0n,y1n,fyrn,mon,ozn,latmin,latmax,month0,month1
;read_o3_zm,fleo,y0o,y1o,fyro,moo,ozo,latmin,latmax,month0,month1
read_o3_zm,fled,y0d,y1d,fyrd,modi,ozd,latmin,latmax,month0,month1
read_o3_zm,flem,y0m,y1m,fyrm,mom,ozm,latmin,latmax,month0,month1
annual_mean_anomaly,fyrg,ozg,ozga,y0ref,y1ref,offg
annual_mean_anomaly,fyrw,ozw,ozwa,y0ref,y1ref,offw
annual_mean_anomaly,fyrn,ozn,ozna,y0ref,y1ref,offn
annual_mean_anomaly,fyrt,ozt,ozta,y0ref,y1ref,offt
annual_mean_anomaly,fyrd,ozd,ozda,y0ref,y1ref,offd
annual_mean_anomaly,fyrm,ozm,ozma,y0ref,y1ref,offm
toz_mean=(offg+offw+offn+offt+offd+offm)/6.
ozg=ozg-offg+toz_mean
ozw=ozw-offw+toz_mean
ozn=ozn-offn+toz_mean
ozt=ozt-offt+toz_mean
ozd=ozd-offd+toz_mean
ozm=ozm-offm+toz_mean




nr=where(fyrw le (yrnow-1))
nr=where(fyrw le (yrnow))
plot_segment,fyrw(nr),ozw(nr),1.5,thick=2,line=0,color=woudccol
;nr=where(fyrw ge (yrnow-1))
;oplot,fyrw(nr),ozw(nr),thick=4,line=0,color=woudccol;color=woudcpre
plot_segment,fix(fyrt),ozt,1.5,thick=2,line=0,color=tomscol,pwidth=.25
plot_segment,fix(fyrn),ozn,1.5,thick=2,line=0,color=noaacol
plot_segment,fix(fyrg),ozg,1.5,thick=2,line=0,color=gomecol
plot_segment,fix(fyrd),ozd,1.5,thick=2,line=0,color=gtocol
plot_segment,fix(fyrm),ozm,1.5,thick=2,line=0,color=msrcol
;plot_segment,fix(fyro),ozo,1.5,thick=2,line=1,color=tomscol


xyouts,sx_legend-5,330,'SH October ('+slat1(2)+'-'+slat0(2)+')',charsize=1.1
xyouts,sx_legend,473,'NH March ('+slat0(2)+'-'+slat1(2)+')',charsize=1.1
s0pos=188
dpos=11
xyouts,sx_color,s0pos+0*dpos,'WOUDC',color=woudccol,charsize=.7
xyouts,sx_color,s0pos+1*dpos,'SBUV V8.6/OMPS NASA (MOD)',color=tomscol,charsize=.7
xyouts,sx_color,s0pos+2*dpos,'SBUV V8.6/OMPS NOAA (COH)',color=noaacol,charsize=.7
xyouts,sx_color,s0pos+3*dpos,'GOME/SCIA GSG',color=gomecol,charsize=.7
xyouts,sx_color,s0pos+4*dpos,'GOME/SCIA/OMI GTO',color=gtocol,charsize=.7
xyouts,sx_color,s0pos+5*dpos,'MSR2',color=msrcol,charsize=.7
;xyouts,sx_color,163,'  preliminary WOUDC data in 2012',color=woudcpre,charsize=.9
device,/close
end
