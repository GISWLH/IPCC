;---------------------------------------------
;; Plots AR6 Ch6 Figure GSAT response to emissions on 10 and 100 year
;; time horizons
;; Written by m.t.lund@cicero.oslo.no
;; Last edits:
;; January 2021, adding long country/sector names
;; February 2021, adding HFCs, changes sector names and plott 2sigma error
;; March/April, adding error bars to sector/regions, modification to label names
;; Needs subroute AL_legend.pro
;------------------------------------------. 

PRO plot_temp

plotpath = '/div/pdo/mariantl/analysis/IDL_SVN/AR6/Figs/FIG_dTpulse/'

;----------------------------------
;---------- Sector data --------------------------
sector = ['AGR','ENE_C','ENE_P','IND','TRA','RES_FF','RES_BF','WST','SHP','BB']
;sector_long = ['Agriculture','Fossil fuel combustion for energy','Fossil fuel production and distribution','Industry','Transport*', $
;               'Residential and commercial fossil fuel use','Residential and commercial biofuel use','Waste management, incl. open trash burning','Shipping','Open biomass burning, incl. agricultural waste burning']
sector_long = ['Agriculture','Fossil fuel combustion for energy','Fossil fuel production and distribution','Industry','Land transportation', $
               'Residential and commercial','Residential and commercial (biofuel use only)','Waste management','Shipping','Open biomass burning']


avia = ['AVIA']
avia_long =['Aviation']
nsect = n_elements(sector)

component=['CO!I2!N','CH!I4!N','N!I2!NO','BC','OC','SO!I2!N','NOx','CO','VOC','NH!I3!N','Avia-contrail','Avia-stratH!I2!NO','HFCs']
ncomp=n_elements(component)


;----------- Read dT10 CEDS ---------------
indata='/div/pdo/mariantl/analysis/IDL_SVN/AR6/Input/dT10_CEDS_sectors_v2_wHFCs_v210214.txt'
data = read_ascii(indata, COUNT=nr,data_start=1)
HELP, /STRUCTURE, data

dT_10 = data.field01[1:13,0:9]/1000  
dT_10_avia = data.field01[1:13,10]/1000 

;----------- Read dT100 CEDS ---------------
indata='/div/pdo/mariantl/analysis/IDL_SVN/AR6/Input/dT100_CEDS_sectors_v2_wHFCs_v210214.txt'
data = read_ascii(indata, COUNT=nr,data_start=1,header=sector_name)
HELP, /STRUCTURE, data

dT_100 = data.field01[1:13,0:9]/1000
dT_100_avia = data.field01[1:13,10]/1000

;----------- Read dT100 CEDS ---------------
indata='/div/pdo/mariantl/analysis/IDL_SVN/AR6/Input/dT10_100_CEDS_total_v2_wHFCs_v210214.txt'
data = read_ascii(indata, COUNT=nr,data_start=1,header=sector_name)
HELP, /STRUCTURE, data

dT_10_tot = data.field01[1:13,0]/1000
dT_100_tot = data.field01[1:13,1]/1000


;-------- Read errorbar ------------
indata='/div/pdo/mariantl/analysis/IDL_SVN/AR6/Input/errorbar_dT10_sectors.txt'
data = read_ascii(indata, COUNT=nr,data_start=1)
HELP, /STRUCTURE, data
errlow_sector_10 = data.field1[1,0:9]
errupp_sector_10 = data.field1[3,0:9]
errlow_avia_10 = data.field1[1,10]
errupp_avia_10 = data.field1[3,10]
err_sector_10 = (errupp_sector_10 - errlow_sector_10)/2.
err_avia_10 = (errupp_avia_10 - errlow_avia_10)/2.


indata='/div/pdo/mariantl/analysis/IDL_SVN/AR6/Input/errorbar_dT100_sectors.txt'
data = read_ascii(indata, COUNT=nr,data_start=1)
HELP, /STRUCTURE, data
errlow_sector_100 = data.field1[1,0:9]
errupp_sector_100 = data.field1[3,0:9]
errlow_avia_100 = data.field1[1,10]
errupp_avia_100 = data.field1[3,10]
err_sector_100 = (errupp_sector_100 - errlow_sector_100)/2.
err_avia_100 = (errupp_avia_100 - errlow_avia_100)/2.



;----------------------------------------
;--------------- Region data ---------------
region = ['LAM','SAS','AFR','EUR','CAS','MDE','SEA','PAN','NAM','EAS']
region_long = ['Latin America and Caribbean','Southern Asia','Africa','Europe','Eurasia','Middle East', $
               'South-East Asia and Developing Pacific','Asia-Pacific Developed','North America','Eastern Asia']
nreg = n_elements(region)

;------
indata='/div/pdo/mariantl/analysis/IDL_SVN/AR6/Input/dT10_CEDS_regions_v2_wHFCs_v210214.txt'
data = read_ascii(indata, COUNT=nr,data_start=1)
HELP, /STRUCTURE, data

dT_10_reg = data.field01[1:13,*] /1000 

;--------
indata='/div/pdo/mariantl/analysis/IDL_SVN/AR6/Input/dT100_CEDS_regions_v2_wHFCs_v210214.txt'
data = read_ascii(indata, COUNT=nr,data_start=1)
HELP, /STRUCTURE, data

dT_100_reg = data.field01[1:13,*]/1000  


;-------- Read errorbar ------------
indata='/div/pdo/mariantl/analysis/IDL_SVN/AR6/Input/errorbar_dT10_regions.txt'
data = read_ascii(indata, COUNT=nr,data_start=1)
HELP, /STRUCTURE, data
errlow_region_10 = data.field1[1,*]
errupp_region_10 = data.field1[3,*]
err_region_10 = (errupp_region_10 - errlow_region_10)/2.


indata='/div/pdo/mariantl/analysis/IDL_SVN/AR6/Input/errorbar_dT100_regions.txt'
data = read_ascii(indata, COUNT=nr,data_start=1)
HELP, /STRUCTURE, data
errlow_region_100 = data.field1[1,*]
errupp_region_100 = data.field1[3,*]
err_region_100 = (errupp_region_100 - errlow_region_100)/2.



doPlot=1
if (doPlot) then begin
;-------------- Version with long label names, data from October 2020 ---------------------
;---------- ---------------- HFCs added -----------------------------------
PS_START, file=plotpath+"FIG_AR6_Ch6_dT_H10v100_v210407.eps",/NOMATCH,xsize=35,ysize=20,/ENCAPSULATE

noofcolors=20
LOADCT, 72, NCOLORS=noofcolors


;IPCC SOD colors
;Red-yellow cat
tvlct,196, 42, 51,1  ;red
tvlct,241, 197, 53,2 ;yellow
tvlct,131, 60, 11,3  ;brown
tvlct,221, 79, 97,4  ;dark salmon
tvlct,245, 119, 42,5 ;dark orange

;green-blue cat
tvlct,51, 34, 136,6    ;dark blue
tvlct,17, 119, 51,7    ;teal
tvlct,136, 204, 238,8  ;ligh blue
tvlct,153, 153, 51,9   ;kakhi
tvlct,68, 170, 153,10   ;green 
tvlct,102, 153, 204,11  ;steel blue

tvlct,128,54,168,12 ;purple
tvlct,159, 0, 159,13 ;dark purple
tvlct,124,130,130,14            ;grey
 
;'CO2','CH4','N2O','BC','OC','SO2','NOx','CO','VOC','NH3','H2O','AIC','HFC'
compcolors=[2,5,1,3,8,11,6,9,7,10,12,13,14]


;other colors
tvlct,192,192,192,17            ; gray 46 
tvlct, 255,255,224, 15          ; Faded yellow BG
tvlct, 245,245,245, 15          ; Faded yellow BG
tvlct,0,0,0,0                   ; black 
tvlct,255,255,255,20            ; white

;System variables
!p.title='!5'
!p.thick=5.0
!x.thick=5.0
!y.thick=5.0
!p.charthick=2.0
!p.charsize=3.5
!p.font=0
device, /helvetica

tcharsize=2.0

;Sub-plot variables
nrows = 1.0
yposmax = 0.70
yposmin = 0.07
posdy = (yposmax-yposmin)/nrows

ncols = 2.0
xposmax = 0.87
xposmin = 0.03
posdx = (xposmax-xposmin)/ncols


;--- Figure title --------------------
DEVICE, /helvetica,/bold
xyouts,0.01,0.97,'Effect of a one year pulse of present-day emissions on global surface temperature',/normal,color=0,charsize=4.0
device, /helvetica

;--- Totals --------
!P.POSITION=[xposmin-0.02,0.80,0.95,0.93] 
xmin = -0.06
xmax = 0.07
nbars = 1

plot,[0,0],[1,1], xrange=[xmin,xmax], yrange=[0.5,nbars+0.5], ytitle=' ',/nodata, COLOR = 0, xstyle=8, ystyle=1,YTICKFORMAT="(A1)", xtitle='Change in GSAT due to total anthropogenic emissions (!Uo!NC)', $
     yticks=1, yminor=1,xtickinterval=0.01,xticklen=0.1,/noerase

axis, xaxis=1, xstyle=1,xticks=1, xminor=1,XTICKFORMAT="(A1)",color=0 

dy = 0.20

;--- H=10 -----
for bar=0,0 do begin     
   y=(nbars-bar)
   data=reform(dT_10_tot(*,bar))    ;data for plotting the bars
   xhiP=0
   xloN=0
   for comp=0,ncomp-1 do begin
      if finite(data(comp)) ne 1 then continue
      if data(comp) gt 0 then begin ;put positive (P) component-temp-effects on top of the previous positive one
         xloP=xhiP
         xhiP=data(comp)+xhiP
         xhi=xhiP
         xlo=xloP
      endif else begin          ;put negative (N) component-temp-effects on the negative side
         xhiN=xloN
         xloN=data(comp)+xloN
         xhi=xloN
         xlo=xhiN
      end
      polyfill, [xlo,xlo,xhi,xhi], [y-dy,y+dy,y+dy,y-dy]+dy, color=compcolors(comp)                 ;the component part of the bar
      plots,  [xlo,xlo,xhi,xhi,xlo],[y-dy,y+dy,y+dy,y-dy,y-dy]+dy, color=0, linestyle=0, thick=4    ;with a black outline
   end             ;end going through components   

   xlo=0
   xhi=total(data,/NAN)
   
   xerr=(11.5/1000)*1.645
   yerr=0
   oploterror, [xhi,1000,1000],[y+0.2,1000,1000], xerr,yerr,errthick=12

   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000],psym=symcat(16),color=0,symsize=5.5
   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000],psym=symcat(16),color=17,symsize=5.2

   
   if bar eq 0 then begin 
      ypos=y+0.18
      xpos=xmin+0.001
      xyouts,xpos,ypos,"Response after 10 years (H=10)",/data,color=0,charsize=3.2
   endif


endfor


;--- H=100 ---
for bar=0,0 do begin      
   y=(nbars-bar)
   data=reform(dT_100_tot(*,bar))  ;data for plotting the bars
   xhiP=0
   xloN=0
   for comp=0,ncomp-1 do begin
      if finite(data(comp)) ne 1 then continue
      if data(comp) gt 0 then begin ;put positive (P) component-temp-effects on top of the previous positive one
         xloP=xhiP
         xhiP=data(comp)+xhiP
         xhi=xhiP
         xlo=xloP
      endif else begin          ;put negative (N) component-temp-effects on the negative side
         xhiN=xloN
         xloN=data(comp)+xloN
         xhi=xloN
         xlo=xhiN
      end
      polyfill, [xlo,xlo,xhi,xhi], [y-dy,y+dy,y+dy,y-dy]-dy, color=compcolors(comp)                 ;the component part of the bar
      plots,  [xlo,xlo,xhi,xhi,xlo],[y-dy,y+dy,y+dy,y-dy,y-dy]-dy, color=0, linestyle=0, thick=4    ;with a black outline
   end             ;end going through components                                                         

   xlo=0
   xhi=total(data,/NAN)
   
   xerr=(1.2/1000.)*1.645
   yerr=0
   oploterror, [xhi,1000,1000],[y+0.2,1000,1000]-dy-0.2, xerr,yerr,errthick=12

   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000]-dy-0.2,psym=symcat(16),color=0,symsize=5.5
   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000]-dy-0.2,psym=symcat(16),color=17,symsize=5.2

   if bar eq 0 then begin
      ypos=y-0.25
      xpos=xmin+0.001
      xyouts,xpos,ypos,"Response after 100 years (H=100)",/data,color=0,charsize=3.2
   endif
        
endfor                                                                                           ;end going through sectors


oplot, [0,0],!y.crange(), line=0, color=0, thick=12



;------------------------------
;--- Sectors ----------
row=0
col=0
!P.POSITION=[xposmin + col*posdx+0.11,yposmax-(row+1)*posdy+0.01,xposmin+(col+1)*posdx-0.015,yposmax-(row)*posdy*posdy]
xmin = -12./1000
xmax = 15./1000
nbars = nsect+1

plot,[0,0],[1,1], xrange=[xmin,xmax], yrange=[0.5,nbars+0.5], $
     ytitle=' ', xtitle='Change in GSAT by sector (!Uo!NC)',/nodata, COLOR = 0, xstyle=1, ystyle=1,YTICKFORMAT="(A1)",$
     yticks=1, yminor=1, /noerase

dy = 0.20

;plot shading for every other bar      
for bar=0,nbars-1 do begin
   if not bar then begin
      if bar le 8 then polyfill,[!x.crange(0),!x.crange(0),!x.crange(1),!x.crange(1)], [nbars-bar-0.5+0.02,nbars-bar+0.5-0.02,nbars-bar+0.5,nbars-bar-0.5] ,color=15 else polyfill,[!x.crange(0),!x.crange(0),!x.crange(1),!x.crange(1)], [nbars-bar-0.4+0.02,nbars-bar+0.5-0.02,nbars-bar+0.5,nbars-bar-0.4] ,color=15

   end
end



;--- Sort high-to-low ------
datatots=total(dT_10,1,/NAN)                ;totals per sector
barnames=sector_long(reverse(sort(datatots)))
barnames_avia=avia_long

;--- H=10 -----
datas=dT_10(*,reverse(sort(datatots)))    ;sort sectors by total-component temp change
datas_avia=dT_10_avia
errbar=err_sector_10(reverse(sort(datatots)))
errbar_avia=err_avia_10
for bar=0,nbars-1 do begin     
   y=(nbars-bar)
   if bar le 9 then data=reform(datas(*,bar)) else data=reform(datas_avia(*,0))  
   xhiP=0
   xloN=0
   for comp=0,ncomp-1 do begin
      if finite(data(comp)) ne 1 then continue
      if data(comp) gt 0 then begin ;put positive (P) component-temp-effects on top of the previous positive one
         xloP=xhiP
         xhiP=data(comp)+xhiP
         xhi=xhiP
         xlo=xloP
      endif else begin          ;put negative (N) component-temp-effects on the negative side
         xhiN=xloN
         xloN=data(comp)+xloN
         xhi=xloN
         xlo=xhiN
      end
      polyfill, [xlo,xlo,xhi,xhi], [y-dy,y+dy,y+dy,y-dy]+dy, color=compcolors(comp)                 ;the component part of the bar
      plots,  [xlo,xlo,xhi,xhi,xlo],[y-dy,y+dy,y+dy,y-dy,y-dy]+dy, color=0, linestyle=0, thick=4    ;with a black outline
   end             ;end going through components   

   xlo=0
   xhi=total(data,/NAN)

   if bar le 9 then xerr=errbar[bar]*1.645 else xerr=errbar_avia*1.645
   yerr=0
   oploterror, [xhi,1000,1000],[y+0.2,1000,1000], xerr,yerr,errthick=6,errcolor=0,hatlength=300.
  
   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000],psym=symcat(16),color=0,symsize=2.5
   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000],psym=symcat(16),color=17,symsize=2.2

     
   if bar eq 0 then begin 
      ypos=y+0.07
      xpos=xmin+0.0005
      xyouts,xpos,ypos,"H=10",/data,color=0,charsize=3.0
   endif

endfor


;--- H=100 ---
datas=dT_100(*,reverse(sort(datatots))) ;sort sectors by total-component temp change
datas_avia=dT_100_avia
errbar=err_sector_100(reverse(sort(datatots)))
errbar_avia=err_avia_100

for bar=0,nbars-1 do begin      ;either sectors or regions
   y=(nbars-bar)
   if bar le 9 then data=reform(datas(*,bar)) else data=reform(datas_avia(*,0))  
   xhiP=0
   xloN=0
   for comp=0,ncomp-1 do begin
      if finite(data(comp)) ne 1 then continue
      if data(comp) gt 0 then begin ;put positive (P) component-temp-effects on top of the previous positive one
         xloP=xhiP
         xhiP=data(comp)+xhiP
         xhi=xhiP
         xlo=xloP
      endif else begin          ;put negative (N) component-temp-effects on the negative side
         xhiN=xloN
         xloN=data(comp)+xloN
         xhi=xloN
         xlo=xhiN
      end
      polyfill, [xlo,xlo,xhi,xhi], [y-dy,y+dy,y+dy,y-dy]-dy, color=compcolors(comp)                 ;the component part of the bar
      plots,  [xlo,xlo,xhi,xhi,xlo],[y-dy,y+dy,y+dy,y-dy,y-dy]-dy, color=0, linestyle=0, thick=4    ;with a black outline
   end             ;end going through components                                                         
    
   ;overplot zero-line
   oplot, [0,0],!y.crange(), line=0, color=0, thick=8

   ;Add net and errorbar
   ;xlo=0
   xhi=total(data,/NAN)
   
   if bar le 9 then xerr=errbar[bar]*1.645 else xerr=errbar_avia*1.645
   yerr=0
   oploterror, [xhi,1000,1000],[y+0.2,1000,1000]-dy-0.2, xerr,yerr,errthick=6,errcol=0,hatlength=300.

   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000]-dy-0.2,psym=symcat(16),color=0,symsize=2.5
   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000]-dy-0.2,psym=symcat(16),color=17,symsize=2.2
        
   if bar eq 0 then begin
      ypos=y-0.3
      xpos=xmin+0.0005
      xyouts,xpos,ypos,"H=100",/data,color=0,charsize=3.0
   endif

      
   ;Add labels
   ypos=y-0.05
   xpos=xmin-0.012   
   if bar eq 0 or bar eq 2 or bar eq 4 or bar eq 6 or bar eq 8 then $
      polyfill, [xpos,xpos+0.012,xpos+0.012,xpos] ,[y-2.5*dy,y-2.5*dy,y+2.5*dy,y+2.5*dy], color=15
   if bar eq 10 then polyfill, [xpos,xpos+0.012,xpos+0.012,xpos] ,[y-2.2*dy,y-2.2*dy,y+2.5*dy,y+2.5*dy], color=15
   
   if bar le 9 then begin 
      if barnames[bar] eq 'Fossil fuel production and distribution' then begin  
         xyouts,xpos,ypos+0.14,'Fossil fuel production',/data,color=0,charsize=3.0
         xyouts,xpos,ypos-0.24,'and distribution',/data,color=0,charsize=3.0
      endif else if barnames[bar] eq 'Residential and commercial' then begin  
         xyouts,xpos,ypos+0.14,'Residential and com-',/data,color=0,charsize=3.0
         xyouts,xpos,ypos-0.24,'mercial',/data,color=0,charsize=3.0
      endif else if barnames[bar] eq 'Fossil fuel combustion for energy' then begin  
         xyouts,xpos,ypos+0.14,'Fossil fuel combustion',/data,color=0,charsize=3.0
         xyouts,xpos,ypos-0.24,'for energy',/data,color=0,charsize=3.0
      endif else if barnames[bar] eq 'Residential and commercial (biofuel use only)' then begin  
         xyouts,xpos,ypos+0.14,'Residential and com-',/data,color=0,charsize=3.0
         xyouts,xpos,ypos-0.24,'mercial (biofuel use only)',/data,color=0,charsize=3.0
      endif else begin 
         xyouts,xpos,ypos,barnames[bar],/data,color=0,charsize=3.0
      endelse 
   endif else begin 
      xyouts,xpos,ypos,barnames_avia,/data,color=0,charsize=3.0
   endelse

   ;re-plot axes after adding boxes 
   axis, yaxis=1, ystyle=1,yticks=1, yminor=1,YTICKFORMAT="(A1)",color=0   
   axis, yaxis=0, ystyle=1,yticks=1, yminor=1,YTICKFORMAT="(A1)",color=0
   axis, xaxis=0, xstyle=1,xticks=1, xminor=1,XTICKFORMAT="(A1)",color=0

endfor                                                                                           ;end going through sectors



;--------------------------------------
;--------------- Add legend -------------------- 
items = component
colors = compcolors
thick = fltarr(n_elements(items))
thick[*] = 100.
lines = fltarr(n_elements(items))
lines[*]=0.

al_legend,items,linestyle=lines,colors=colors,linsize=0.20, thick=thick, $
          position=[0.85,0.70],/norm,box=0,/vertical,charsize=3.0

items=[' ']
color=[17]
sym=[symcat(16)]
symsize=[5.]
al_legend,items,psym=sym,color=color,symsize=symsize,pos=[0.877,0.32],/norm,box=0,charsize=3.0

xpos=0.865
y=0.30
polyfill, [xpos,xpos+0.05,xpos+0.05,xpos] ,[y-0.001,y-0.001,y+0.001,y+0.001],/normal, color=0
polyfill, [xpos,xpos+0.001,xpos+0.001,xpos] ,[y-0.01,y-0.01,y+0.01,y+0.01],/normal, color=0
xpos=0.915
polyfill, [xpos,xpos+0.001,xpos+0.001,xpos] ,[y-0.01,y-0.01,y+0.01,y+0.01],/normal, color=0

xyouts,0.865,0.32,'Net effect',/normal,color=0,charsize=3.0
xyouts,0.855,0.26,'5% to 95% range',/normal,color=0,charsize=3.0


;------------------------
;--- Regions ----------
row=0
col=1
!P.POSITION=[xposmin + col*posdx+0.105,yposmax-(row+1)*posdy+0.01,xposmin+(col+1)*posdx-0.02,yposmax-(row)*posdy*posdy]

xmin = -12./1000
xmax = 17./1000
nbars = nreg

plot,[0,0],[1,1], xrange=[xmin,xmax], yrange=[0.5,nbars+0.5], $
     ytitle=' ', xtitle='Change in GSAT by sector (!Uo!NC)',/nodata, COLOR = 0, xstyle=1, ystyle=1,YTICKFORMAT="(A1)",$
     yticks=1,yminor=1,/noerase


dy = 0.20

;Plot shading for every other bar      
for bar=0,nbars-1 do begin
   if not bar then begin
      polyfill,[!x.crange(0),!x.crange(0),!x.crange(1),!x.crange(1)], [nbars-bar-0.5+0.02,nbars-bar+0.5-0.02,nbars-bar+0.5,nbars-bar-0.5] ,color=15
   end
end


;--- Sort high-to-low ------
datatots=total(dT_10_reg,1,/NAN)                ;totals per sector
barnames=region_long(reverse(sort(datatots)))

;---- H=10 ---
datas=dT_10_reg(*,reverse(sort(datatots))) ;sort sectors by total-component temp change
errbar=err_region_10(reverse(sort(datatots)))
for bar=0,nbars-1 do begin
   y=(nbars-bar)
   data=reform(datas(*,bar)) 
   xhiP=0
   xloN=0
   for comp=0,ncomp-1 do begin
      if finite(data(comp)) ne 1 then continue
      if data(comp) gt 0 then begin ;put positive (P) component-temp-effects on top of the previous positive one
         xloP=xhiP
         xhiP=data(comp)+xhiP
         xhi=xhiP
         xlo=xloP
      endif else begin          ;put negative (N) component-temp-effects on the negative side
         xhiN=xloN
         xloN=data(comp)+xloN
         xhi=xloN
         xlo=xhiN
      end
      polyfill, [xlo,xlo,xhi,xhi], [y-dy,y+dy,y+dy,y-dy]+dy, color=compcolors(comp)                 ;the component part of the bar
      plots,  [xlo,xlo,xhi,xhi,xlo],[y-dy,y+dy,y+dy,y-dy,y-dy]+dy, color=0, linestyle=0, thick=4    ;with a black outline
   end             ;end going through components   

   ;xlo=0
   xhi=total(data,/NAN)

   xerr=errbar[bar]*1.645
   yerr=0
   oploterror, [xhi,1000,1000],[y+0.2,1000,1000], xerr,yerr,errthick=6,errcolor=0,hatlength=300.
   
   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000],psym=symcat(16),color=0,symsize=2.5
   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000],psym=symcat(16),color=17,symsize=2.2

   if bar eq 0 then begin 
      ypos=y+0.07
      xpos=xmin+0.0005
      xyouts,xpos,ypos,"H=10",/data,color=0,charsize=3.0
   endif

endfor 

;--- H=100 ----------
datas=dT_100_reg(*,reverse(sort(datatots))) ;sort sectors by total-component temp change
errbar=err_region_100(reverse(sort(datatots)))
for bar=0,nbars-1 do begin
   y=(nbars-bar)
   data=reform(datas(*,bar)) 
   xhiP=0
   xloN=0
   for comp=0,ncomp-1 do begin
      if finite(data(comp)) ne 1 then continue
      if data(comp) gt 0 then begin ;put positive (P) component-temp-effects on top of the previous positive one
         xloP=xhiP
         xhiP=data(comp)+xhiP
         xhi=xhiP
         xlo=xloP
      endif else begin          ;put negative (N) component-temp-effects on the negative side
         xhiN=xloN
         xloN=data(comp)+xloN
         xhi=xloN
         xlo=xhiN
      end
      polyfill, [xlo,xlo,xhi,xhi], [y-dy,y+dy,y+dy,y-dy]-dy, color=compcolors(comp)                 ;the component part of the bar
      plots,  [xlo,xlo,xhi,xhi,xlo],[y-dy,y+dy,y+dy,y-dy,y-dy]-dy, color=0, linestyle=0, thick=4    ;with a black outline
   end             ;end going through components                                                         

   ;plot zero line
   oplot, [0,0],!y.crange(), line=0, color=0, thick=10
   
   xlo=0
   xhi=total(data,/NAN)

   xerr=errbar[bar]*1.645
   yerr=0
   oploterror, [xhi,1000,1000],[y+0.2,1000,1000]-dy-0.2, xerr,yerr,errthick=6,errcol=0,hatlength=300.
   
   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000]-dy-0.2,psym=symcat(16),color=0,symsize=2.5
   OPLOT,[xhi,1000,1000],[y+0.2,1000,1000]-dy-0.2,psym=symcat(16),color=17,symsize=2.2

   
   if bar eq 0 then begin
      ypos=y-0.3
      xpos=xmin+0.0005
      xyouts,xpos,ypos,"H=100",/data,color=0,charsize=3.0
   endif

   ypos=y-0.05
   xpos=xmin-0.01
   if bar eq 0 or bar eq 2 or bar eq 4 or bar eq 6 or bar eq 8 then $
   polyfill, [xpos,xpos+0.01,xpos+0.01,xpos] ,[y-2.5*dy,y-2.5*dy,y+2.5*dy,y+2.5*dy], color=15

   if barnames[bar] eq 'South-East Asia and Developing Pacific' then begin  
      xyouts,xpos,ypos+0.12,'Southeast Asia and',/data,color=0,charsize=3.0
      xyouts,xpos,ypos-0.22,'Developing Pacific',/data,color=0,charsize=3.0
   endif else if barnames[bar] eq 'Latin America and Caribbean' then begin  
      xyouts,xpos,ypos+0.12,'Latin America and',/data,color=0,charsize=3.0
      xyouts,xpos,ypos-0.22,'Caribbean',/data,color=0,charsize=3.0
   endif else if barnames[bar] eq 'Asia-Pacific Developed' then begin  
      xyouts,xpos,ypos+0.12,'Asia-Pacific',/data,color=0,charsize=3.0
      xyouts,xpos,ypos-0.22,'Developed',/data,color=0,charsize=3.0
   endif else begin 
      xyouts,xpos,ypos,barnames[bar],/data,color=0,charsize=3.0
   endelse 

endfor

;re-plot axes after adding boxes 
axis, yaxis=1, ystyle=1,yticks=1, yminor=1,YTICKFORMAT="(A1)",color=0    
axis, yaxis=0, ystyle=1,yticks=1, yminor=1,YTICKFORMAT="(A1)",color=0


PS_END,/PNG

endif 










END
