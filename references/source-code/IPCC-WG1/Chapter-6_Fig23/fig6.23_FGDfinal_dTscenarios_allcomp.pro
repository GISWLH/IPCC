;---------------------------------------------
;; Plots AR6 Ch6 Figure GSAT response to change in SLCF emissions under SSPs 
;; Written by m.t.lund@cicero.oslo.no
;; Last edit Feburary 2021, adding long country names and all species
;; Needs subroutine AL_legend.pro
;------------------------------------------

PRO plot_temp

plotpath = '/div/pdo/mariantl/analysis/IDL_SVN/AR6/Figs/FIG_dTscenarios/'


reg_new=['NAM','EUR','SAS','EAS','SEA','PAN','AFR','MDE','LAM','CAS']
reg_new_long = ['North America','Europe','Southern Asia','Eastern Asia', $
                'South-East Asia and Developing Pacific','Asia-Pacific Developed', $
                'Africa','Middle East','Latin America and Caribbean','Eurasia']
nreg_new=n_elements(reg_new)

comp=['BC','CH4','CO','NH3','NMVOC','NOx','OC','SO2']
ncomp=n_elements(comp)

scen_name = ['SSP1-2.6','SSP2-4.5','SSP3-7.0','SSP5-8.5']
nscen=n_elements(scen_name)


temp_2040 = fltarr(ncomp,nreg_new,4)
temp_2100 = fltarr(ncomp,nreg_new,4)

;------------------ read data ---------------------------------------
id = NCDF_OPEN(plotpath+'FIG_AR6_dTscenarios_allcomp_data.nc')

for c=0,ncomp-1 do begin 
   NCDF_VARGET,id,'dT_2040_'+comp[c],field
   temp_2040[c,*,*] = field

   NCDF_VARGET,id,'dT_2100_'+comp[c],field2
   temp_2100[c,*,*] = field2

endfor

NCDF_CLOSE,id



doPlot=1
if (doPlot) then begin 

;----------------- Version long region names--------------------------------
;---------------------------------------------------
PS_START, file=plotpath+"FIG_AR6_dTscenarios_allcomp_v210210.eps",/NOMATCH,xsize=35,ysize=27,/ENCAPSULATE


;System variables
!p.title='!5'
!p.thick=5.0
!x.thick=5.0
!y.thick=5.0
!p.charthick=2.0
!p.charsize=3.5
!p.font=0
device, /helvetica


;Set up window
nrows = 2.0
yposmax = 0.85
yposmin = 0.08
posdy = (yposmax-yposmin)/nrows

ncols = 4.0
xposmax = 0.97
xposmin = 0.17
posdx = (xposmax-xposmin)/ncols


SSPs = [0,1,2,3]
REGs = [0,1,2,3,4,5,6,7,8,9];,10,11,12,13]         

plotcomps=['BC','CH4','CO','NH3','NMVOC','NOx','OC','SO2']
nplotcomps=n_elements(plotcomps)

title_plot=['SSP1-2.6','SSP2-4.5','SSP3-7.0','SSP5-8.5']

LOADCT, 39
; From https://wg1.ipcc.ch/AR6/documents/ipcc_visual-identity_guidelines.pdf
;tvlct,131, 60, 11,1  ;BC brown
;tvlct,245, 119, 42,2 ; CH4 dark orange
;tvlct,51, 34, 136,3    ;dark blue
;tvlct,102, 153, 204,4  ;steel blue
;compcolors=[1,2,3,4]

tvlct, 245,245,245, 15          ; grey 
tvlct, 255,248,220, 16          ; corn silk 
tvlct,0,0,0,0


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

;'BC','CH4','CO','NH3','NMVOC','NOx','OC','SO2'
compcolors=[3,5,9,10,7,6,8,11]

xmin = -0.10
xmax = 0.10;0.32

;Plot title
DEVICE, /helvetica,/bold
xyouts,0.02,0.97,'Contribution from changes in anthropogenic regional emissions of SLCFs to GSAT changes',/normal,color=0,charsize=4.0
device, /helvetica

;----- 2040 -----
row=0
col=0

for s=0,3 do begin 

!P.POSITION=[xposmin + col*posdx,yposmax-(row+1)*posdy+0.05,xposmin+(col+1)*posdx,yposmax-(row)*posdy*posdy]
print, [xposmin + col*posdx,yposmax-(row+1)*posdy+0.03,xposmin+(col+1)*posdx,yposmax-(row)*posdy*posdy-0.03]

nbars = nreg_new

if s lt 3 then xtickvals=[-0.1,-0.05,0.0,0.05] else xtickvals=[-0.1,-0.05,0.0,0.05,0.1]
xnticks = N_Elements(xtickvals)

plot,[0,0],[1,1], xrange=[xmin,xmax], yrange=[0.5,nbars+0.5],title='',$
     ytitle=' ',/nodata, COLOR = 0, xstyle=1, ystyle=1,YTICKFORMAT="(A1)",$
     XTICKS=xnticks-1,XTICKV=xtickvals,XMINOR=5, $;xtickformat="(A1)", $
     yticks=1,yminor=1,/noerase


dy = 0.40

xpos=!p.position(0)+0.05
ypos=!p.position(3)+0.02
polyfill, [xpos-0.01,xpos-0.01,xpos+0.08,xpos+0.08] ,[ypos+0.025,ypos-0.01,ypos-0.01,ypos+0.025], /normal,color=16
xyouts,xpos,ypos,title_plot[s],/normal,color=0,charsize=3.5


;Plot shading for every other bar      
for bar=0,nbars-1 do begin
   if not bar then begin
      polyfill,[!x.crange(0),!x.crange(0),!x.crange(1),!x.crange(1)], [nbars-bar-0.5+0.02,nbars-bar+0.5-0.02,nbars-bar+0.5,nbars-bar-0.5] ,color=15
   end
end


;--- Sort high-to-low ------
;datatots=total(dT_10_reg,1,/NAN)                ;totals per sector
barnames=reg_new_long

;---- H=10 ---
datas=temp_2040[*,*,s]; comp, reg, scen, dT_10_reg(*,reverse(sort(datatots)))    ;sort sectors by total-component temp change
for bar=0,nbars-1 do begin
   y=(nbars-bar)
   data=reform(datas(*,bar)) 
   xhiP=0
   xloN=0
   for comp=0,nplotcomps-1 do begin
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
      polyfill, [xlo,xlo,xhi,xhi], [y-dy,y+dy,y+dy,y-dy], color=compcolors(comp)                 ;the component part of the bar
      plots,  [xlo,xlo,xhi,xhi,xlo],[y-dy,y+dy,y+dy,y-dy,y-dy], color=0, linestyle=0, thick=4    ;with a black outline
   end             ;end going through components   

if s eq 1 then begin 
   xpos=!p.position(2)-0.04
   ypos=!p.position(1)-0.055
   xyouts,xpos,ypos,Greek('Delta')+'GSAT (!Uo!NC)',/normal,color=0
endif 
 
if s eq 0 then begin 
   
   DEVICE, /helvetica,/bold
   xpos=!p.position(0)-0.16
   ypos=!p.position(3)+0.01
   xyouts,xpos,ypos,Greek('Delta')+'GSAT(2040-2020)',/normal,color=0,charsize=3.3
   device, /helvetica

   ypos=y-0.1
   xpos=xmin-0.16
   if bar eq 0 or bar eq 2 or bar eq 4 or bar eq 6 or bar eq 8 then $
      polyfill, [xpos,xpos+0.16,xpos+0.16,xpos] ,[y-1.2*dy,y-1.2*dy,y+1.2*dy,y+1.2*dy], color=15
   
   if barnames[bar] eq 'South-East Asia and Developing Pacific' then begin  
      xyouts,xpos,ypos+0.21,'Southeast Asia and',/data,color=0,charsize=3.0
      xyouts,xpos,ypos-0.31,'Developing Pacific',/data,color=0,charsize=3.0
   endif else if barnames[bar] eq 'Latin America and Caribbean' then begin  
      xyouts,xpos,ypos+0.21,'Latin America and',/data,color=0,charsize=3.0
      xyouts,xpos,ypos-0.31,'Caribbean',/data,color=0,charsize=3.0
   endif else begin 
      xyouts,xpos,ypos,barnames[bar],/data,color=0,charsize=3.0
   endelse 
endif

endfor

;re-plot axes after adding boxes 
axis, yaxis=1, ystyle=1,yticks=1, yminor=1,YTICKFORMAT="(A1)",color=0    
axis, yaxis=0, ystyle=1,yticks=1, yminor=1,YTICKFORMAT="(A1)",color=0

oplot, [0,0],!y.crange(), line=0, color=0, thick=12

col=col+1

endfor  ;end scenarios




;----- 2100 -----
xmin = -0.12
xmax = 0.35

row=1
col=0

for s=0,3 do begin 

!P.POSITION=[xposmin + col*posdx,yposmax-(row+1)*posdy,xposmin+(col+1)*posdx,yposmax-(row)*posdy*posdy-0.26]
print, [xposmin + col*posdx,yposmax-(row+1)*posdy,xposmin+(col+1)*posdx,yposmax-(row)*posdy*posdy-0.33]

nbars = nreg_new

if s lt 3 then xtickvals=[-0.10,0.0,0.10,0.20,0.30] else xtickvals=[-0.10,0.0,0.10,0.20,0.30]
xnticks = N_Elements(xtickvals)

plot,[0,0],[1,1], xrange=[xmin,xmax], yrange=[0.5,nbars+0.5],title=' ',$
     ytitle=' ',/nodata, COLOR = 0, xstyle=1, ystyle=1,YTICKFORMAT="(A1)",$
     XTICKS=xnticks-1,XTICKV=xtickvals,XMINOR=5, $
     yticks=1,yminor=1,/noerase,charsize=3.2

dy = 0.40

;Plot shading for every other bar      
for bar=0,nbars-1 do begin
   if not bar then begin
      polyfill,[!x.crange(0),!x.crange(0),!x.crange(1),!x.crange(1)], [nbars-bar-0.5+0.02,nbars-bar+0.5-0.02,nbars-bar+0.5,nbars-bar-0.5] ,color=15
   end
end

if s eq 1 then begin 
   xpos=!p.position(2)-0.04
   ypos=!p.position(1)-0.055
   xyouts,xpos,ypos,Greek('Delta')+'GSAT (!Uo!NC)',/normal,color=0
endif 

;--- Sort high-to-low ------
;datatots=total(dT_10_reg,1,/NAN)                ;totals per sector
barnames=reg_new_long;region_long(reverse(sort(datatots)))

;---- H=10 ---
datas=temp_2100[*,*,s]   ;sort sectors by total-component temp change

for bar=0,nbars-1 do begin
   y=(nbars-bar)
   data=reform(datas(*,bar)) 
   xhiP=0
   xloN=0
   for comp=0,nplotcomps-1 do begin
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
      polyfill, [xlo,xlo,xhi,xhi], [y-dy,y+dy,y+dy,y-dy], color=compcolors(comp)                 ;the component part of the bar
      plots,  [xlo,xlo,xhi,xhi,xlo],[y-dy,y+dy,y+dy,y-dy,y-dy], color=0, linestyle=0, thick=4    ;with a black outline
   end             ;end going through components   

 
if s eq 0 then begin 
   
   DEVICE, /helvetica,/bold
   xpos=!p.position(0)-0.16
   ypos=!p.position(3)+0.01
   xyouts,xpos,ypos,Greek('Delta')+'GSAT(2100-2020)',/normal,color=0,charsize=3.3
   device, /helvetica

   ypos=y-0.1
   xpos=xmin-0.374
   if bar eq 0 or bar eq 2 or bar eq 4 or bar eq 6 or bar eq 8 then $
      polyfill, [xpos,xpos+0.374,xpos+0.374,xpos] ,[y-1.2*dy,y-1.2*dy,y+1.2*dy,y+1.2*dy], color=15

   if barnames[bar] eq 'South-East Asia and Developing Pacific' then begin  
      xyouts,xpos,ypos+0.21,'Southeast Asia and',/data,color=0,charsize=3.0
      xyouts,xpos,ypos-0.31,'Developing Pacific',/data,color=0,charsize=3.0
   endif else if barnames[bar] eq 'Latin America and Caribbean' then begin  
      xyouts,xpos,ypos+0.21,'Latin America and',/data,color=0,charsize=3.0
      xyouts,xpos,ypos-0.31,'Caribbean',/data,color=0,charsize=3.0
   endif else begin 
      xyouts,xpos,ypos,barnames[bar],/data,color=0,charsize=3.0
   endelse 
endif

endfor

;re-plot axes after adding boxes 
axis, yaxis=1, ystyle=1,yticks=1, yminor=1,YTICKFORMAT="(A1)",color=0    
axis, yaxis=0, ystyle=1,yticks=1, yminor=1,YTICKFORMAT="(A1)",color=0

oplot, [0,0],!y.crange(), line=0, color=0, thick=12

col=col+1

endfor  ;end scenarios



;;;;;;;;;;;;;;;;;;;;;;;
  ;; Legend
  ;;;;;;;;;;;;;;;;;;;;;;;

items = ['CH!I4!N','BC','OC','SO!I2!N','NOx','CO','NMVOC','NH!I3!N']
colors=[5,3,8,11,6,9,7,10]
thick = fltarr(n_elements(items))
thick[*] = 100.
lines = fltarr(n_elements(items))
lines[*]=0.
colors=colors
al_legend,items,linestyle=lines,colors=colors,linsize=0.2, thick=thick, $
          position=[0.15,0.95],/norm,box=0,/horizontal,charsize=3.2




PS_END,/PNG

endif 


END
