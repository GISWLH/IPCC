pro IPCC_TEMIS_NO2_timeseries_v5

;---------------------------------------------------------------------------------------------------------------------------------------
;This code reads the IPCC_TEMIS_NO2_trends.dat file and plots the annual trop. NO2 values relative to 2016 for various subregions. 
;The self-consistent GOME, SCIAMACHY, and GOME-2 dataset from Georgoulias et al. (2019) (available on http://www.temis.nl) is used. 
;---------------------------------------------------------------------------------------------------------------------------------------
;The code was created by Dr. Aristeidis K. Georgoulias (ageor@auth.gr), Dept. of Meteorology and Climatology, AUTH, Thessaloniki, Greece
;for the needs of the IPCC Working Group I (WGI) Sixth Assessment Report (Chapter 6).
;---------------------------------------------------------------------------------------------------------------------------------------

dir='C:\IPCC\'

pattern=dir+'IPCC_TEMIS_NO2_trends.dat'
filenames=file_search(pattern)
num_files=n_elements(filenames)
if num_files eq 0 then begin
 print, 'ERROR: no files found'
 return
endif

print, num_files

minx=1996
maxx=2016
miny=0
maxy=5
vertick=10
hortick=10

for j=0L,num_files-1 do begin

;open device for ploting
 orig_device=!d.name

;set_plot,'ps'
Set_Plot, 'PS'

!P.FONT=1

;set_plot,'PS', /copy

device, filename=dir+strmid(filenames(j),8,strlen(filenames)-12)+'_trends_v5.ps', COLOR=1, BITS_PER_PIXEL=8,$
 /INCHES, Set_Font='Arial'

cc=strarr(365)

dummy=''
reversal=''
record=''

yemonth=fltarr(1000000)
data1=fltarr(1000000)
data2=fltarr(1000000)
data3=fltarr(1000000)
data4=fltarr(1000000)
data5=fltarr(1000000)
data6=fltarr(1000000)
data7=fltarr(1000000)
data8=fltarr(1000000)
data9=fltarr(1000000)
data10=fltarr(1000000)
data11=fltarr(1000000)
data12=fltarr(1000000)
data13=fltarr(1000000)
data14=fltarr(1000000)
data15=fltarr(1000000)
data16=fltarr(1000000)

openr, in1, filenames(j), /get_lun
count=0L

for i=0,3 do begin
readf, in1, dummy
endfor

for i=4,4 do begin
readf, in1, reversal
record1=strsplit(reversal, /extract)
endfor

while (not eof(in1)) do begin
readf, in1, record

record2=strsplit(record, /extract,count=ct1)

if record2(0) ge 1996 and record2(0) lt 2017 then begin

yemonth(count)=record2(0)
data1(count)=record2(1)
data2(count)=record2(2)
data3(count)=record2(3)
data4(count)=record2(4)
data5(count)=record2(5)
data6(count)=record2(6)
data7(count)=record2(7)
data8(count)=record2(8)
data9(count)=record2(9)
data10(count)=record2(10)
data11(count)=record2(11)
data12(count)=record2(12)
data13(count)=record2(13)
data14(count)=record2(14)
data15(count)=record2(15)
data16(count)=record2(16)

count=count+1

endif

endwhile

yemonth=yemonth(0:count-1)
data1=data1(0:count-1)
data2=data2(0:count-1)
data3=data3(0:count-1)
data4=data4(0:count-1)
data5=data5(0:count-1)
data6=data6(0:count-1)
data7=data7(0:count-1)
data8=data8(0:count-1)
data9=data9(0:count-1)
data10=data10(0:count-1)
data11=data11(0:count-1)
data12=data12(0:count-1)
data13=data13(0:count-1)
data14=data14(0:count-1)
data15=data15(0:count-1)
data16=data16(0:count-1)

close, in1 & free_lun, in1

loadct, 0

A = FINDGEN(17)*(!PI*2/16.)   ;Make a vector of 16 points, A[i] = 2pi/16.
USERSYM, COS(A), SIN(A), thick=1, color=0  ;Define the symbol to be a unit circle with 16 points. Set the filled flag.

plot,A(*), position = [0.10, 0.15, 0.90, 0.86], PSYM=8, color=1 ,thick=1 ,symsize=1, xrange=[minx,maxx], yrange=[miny,maxy],$
xstyle=1,ystyle=1,xticks=hortick,yticks=vertick,xticklen=-0.02,yticklen=-0.01,xminor=2,/nodata,charsize=1.2

axis, minx,miny, yrange = [miny,maxy], yaxis = 0, ystyle=1, color = 0, $
     yticks=vertick, yminor=5,yticklen=-0.01,charsize=1.2
     ; yaxis = 0 => left axis
axis, maxx,miny, yrange = [miny,maxy], yaxis = 1, ystyle=1, color = 0,  $
     yticks=vertick, xticks=hortick, yminor=5,yticklen=-0.01,charsize=1.2,ytickformat='(A1)'
     ; yaxis = 1 => rhight axis
axis, minx,miny, xrange = [minx,maxx], xaxis = 0, xstyle=1, color = 0 , $
     xticks =hortick,  xminor=2, xticklen=-0.02,charsize=1.2

loadct,0

tvlct,[[0],[50],[172]],1
tvlct,[[0],[127],[237]],2
tvlct,[[49],[84],[33]],3
tvlct,[[105],[147],[46]],4
tvlct,[[165],[190],[114]],5

tvlct,[[117],[0],[0]],6
tvlct,[[255],[0],[0]],7
tvlct,[[219],[12],[101]],8
tvlct,[[252],[63],[184]],9
tvlct,[[252],[188],[242]],10

tvlct,[[255],[161],[0]],11
tvlct,[[0],[220],[255]],12
tvlct,[[0],[255],[199]],13
tvlct,[[87],[0],[110]],14
tvlct,[[111],[111],[221]],15

tvlct,[[252],[239],[0]],16

xyouts, .11 , 0.83, '1: Western U.S.', charsize = 0.9, charthick=3, /normal, color=1, orientation=0
xyouts, .11 , 0.80, '2: Eastern U.S.', charsize = 0.9, charthick=3, /normal, color=2, orientation=0
xyouts, .11 , 0.77, '3: Western Europe', charsize = 0.9, charthick=3, /normal, color=3, orientation=0
xyouts, .11 , 0.74, '4: Middle East', charsize = 0.9, charthick=3, /normal, color=4, orientation=0
xyouts, .11 , 0.71, '5: Northwestern China', charsize = 0.9, charthick=3, /normal, color=6, orientation=0
xyouts, .11 , 0.68, '6: Eastern China', charsize = 0.9, charthick=3, /normal, color=7, orientation=0
xyouts, .11 , 0.65, '7: Japan', charsize = 0.9, charthick=3, /normal, color=9, orientation=0
xyouts, .11 , 0.62, '8: Eastern India', charsize = 0.9, charthick=3, /normal, color=10, orientation=0
xyouts, .11 , 0.59, '9: Southeastern America', charsize = 0.9, charthick=3, /normal, color=13, orientation=0
xyouts, .11 , 0.56, '10: Southern Africa', charsize = 0.9, charthick=3, /normal, color=11, orientation=0

oplot,[2003.5,2003.5],[miny,maxy],color=100, linestyle=1, thick=10
oplot,[2012.25,2012.25],[miny,maxy],color=100, linestyle=1, thick=10

xyouts,1999,0.15,'GOME',/DATA, alignment=0,charsize=1.2, color=100, charthick=3
xyouts,2006.5,0.15,'SCIAMACHY',/DATA, alignment=0,charsize=1.2, color=100, charthick=3
xyouts,2012.62,0.15,'GOME-2A/2B',/DATA, alignment=0,charsize=1.2, color=100, charthick=3

oplot,  yemonth(0:count-1), data1(0:count-1),  color=1,  thick=3.0

oplot,  yemonth(0:count-1), data2(0:count-1),  color=2,  thick=3.0

oplot,  yemonth(0:count-1), data4(0:count-1),  color=3,  thick=3.0

oplot,  yemonth(0:count-1), data6(0:count-1),  color=6,  thick=3.0

oplot,  yemonth(0:count-1), data7(0:count-1),  color=7,  thick=3.0

oplot,  yemonth(0:count-1), data9(0:count-1),  color=9,  thick=3.0

oplot,  yemonth(0:count-1), data10(0:count-1),  color=10,  thick=3.0

oplot,  yemonth(0:count-1), data11(0:count-1),  color=4,  thick=3.0

oplot,  yemonth(0:count-1), data13(0:count-1),  color=13,  thick=3.0

oplot,  yemonth(0:count-1), data15(0:count-1),  color=11,  thick=3.0

xyouts, .04 , 0.5,'Tropospheric NO!D2!N normalized to 1996', charsize = 1.4, charthick=1.0, /normal, color=0, orientation=90, alignment=0.5
xyouts, .5 , 0.042,'Year', charsize = 1.4, charthick=1.0, /normal, color=0, orientation=0, alignment=0.5

xyouts, .11 , 0.175, '(b)', charsize = 1.7, charthick=1.5, /normal, color=0,orientation=0,alignment=0

; close device for ploting
device, /close_file
set_plot, orig_device

endfor

end




















