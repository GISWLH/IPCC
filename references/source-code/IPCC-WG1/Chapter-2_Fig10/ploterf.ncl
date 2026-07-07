; Script “ploterf.ncl”

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
begin

;wks = gsn_open_wks ("pdf","erf")
;wks = gsn_open_wks ("eps","erf")
wks = gsn_open_wks ("ps","erf")
gsn_define_colormap(wks,"AR6_Line_Shade")


wks@wkOrientation = "landscape"
res = True
res@vpHeightF= 0.6                    ; change aspect ratio of plot
res@vpWidthF = 0.7
res@gsnDraw = False
res@gsnFrame = False
res@tmXBLabelFont=12
res@tmYLLabelFont=12
res@tiYAxisString = "(W m~S~-2~N~)"
res@tiYAxisFont=12
res@trXMinF = 1750
res@trXMaxF = 2020.
res@trYMinF = -4.9
res@trYMaxF = 2.99
res@tmYRBorderOn = False
res@tmXTBorderOn = False
res@tmYROn = False
res@tmXTOn = False
res@tmYLPrecision = 1
res@tiMainFont = 12
res@xyLineThicknessF=3.
;res@gsnMaximize           = True
res@gsnYRefLine                 = 0.
res@gsnYRefLineDashPattern =2 ; dotted
res@gsnLeftString   = "Effective radiative forcings"
txres               = True                      ; text mods desired
txres@txFontHeightF = 0.017                     ; text font height
txres@txJust        = "CenterLeft"              ; Default is "CenterCenter".

f = addfile("erf.nc","r")
co2 = f->CO2
ch4 = f->CH4
n2o = f->N2O
halo = f->Halogens
o3 = f->O3
aer = f->aerosol
luc = f->LUC
swv = f->H2O_Strat
bcsnow = f->BC_Snow
contrails = f->Contrails
volc = f->Volcano
tsi = f->Solar
total=f->Total
anthr=f->Total_Anthropogenic
f = addfile("erfpc05.nc","r")
co205 = f->CO2
ch405 = f->CH4
n2o05 = f->N2O
halo05 = f->Halogens
o305 = f->O3
aer05 = f->aerosol
luc05 = f->LUC
swv05 = f->H2O_Strat
bcsnow05 = f->BC_Snow
contrails05 = f->Contrails
volc05 = f->Volcano
tsi05 = f->Solar

f = addfile("erfpc95.nc","r")
co295 = f->CO2
ch495 = f->CH4
n2o95 = f->N2O
halo95 = f->Halogens
o395 = f->O3
aer95 = f->aerosol
luc95 = f->LUC
swv95 = f->H2O_Strat
bcsnow95 = f->BC_Snow
contrails95 = f->Contrails
volc95 = f->Volcano
tsi95 = f->Solar


nn=dimsizes(co2&time)
;************************************************
; define a polygon centered with width of 2 sigma
;************************************************
 xp    = new( (/2*nn/), float )
 yp    = new( (/2*nn/), float )


res@xyLineColor="(/0.496,0,0.535/)"
plot = gsn_csm_xy(wks,co2&time,co2,res)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Carbon dioxide (CO~B~2~N~)",.21,.78,txres)
do k=0,nn-1
  yp(k)          = co205(k)
  xp(k)          = co2&time(k)
  xp(2*nn-1-k) = co2&time(k)
  yp(2*nn-1-k) =  co295(k)
end do
gsres                   = True                        ; poly res
gsres@tfPolyDrawOrder   = "Predraw"                   ; draw this first
gsres@gsFillColor       = res@xyLineColor                 ; color chosen
gsres@gsFillOpacityF = 0.1
dummy = gsn_add_polygon (wks,plot,xp,yp,gsres)

res@xyLineColor="(/0.676,0.367,0./)"
p1 = gsn_csm_xy(wks,co2&time,ch4,res)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Methane (CH~B~4~N~)",.21,.755,txres)
overlay(plot,p1)
do k=0,nn-1
   yp(k)          = ch405(k)
   xp(k)          = co2&time(k)
   xp(2*nn-1-k) = co2&time(k)
   yp(2*nn-1-k) =  ch495(k)
end do
gsres@gsFillColor       = res@xyLineColor                 ; color chosen
dummy1 = gsn_add_polygon (wks,p1,xp,yp,gsres)

res@xyLineColor="(/0.,0.555,0.512/)"
p11 = gsn_csm_xy(wks,co2&time,n2o,res)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Nitrous oxide (N~B~2~N~O)",.21,.73,txres)
overlay(plot,p11)
do k=0,nn-1
   yp(k)          = n2o05(k)
   xp(k)          = co2&time(k)
   xp(2*nn-1-k) = co2&time(k)
   yp(2*nn-1-k) =  n2o95(k)
end do
gsres@gsFillColor       = res@xyLineColor                 ; color chosen
dummy11 = gsn_add_polygon (wks,p11,xp,yp,gsres)

res@xyLineColor="(/0.,0.438,0.75/)"
p12 = gsn_csm_xy(wks,co2&time,halo,res)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Halogenated gases",.21,.68,txres)
overlay(plot,p12)
do k=0,nn-1
   yp(k)          = halo05(k)
   xp(k)          = co2&time(k)
   xp(2*nn-1-k) = co2&time(k)
   yp(2*nn-1-k) =  halo95(k)
end do
gsres@gsFillColor       = res@xyLineColor                 ; color chosen
dummy12 = gsn_add_polygon (wks,p12,xp,yp,gsres)

res@xyLineColor="(/0.895,0.852,0.277/)"
p2 = gsn_csm_xy(wks,co2&time,o3,res)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Ozone (O~B~3~N~)",.21,.705,txres)
overlay(plot,p2)
do k=0,nn-1
   yp(k)          = o305(k)
   xp(k)          = co2&time(k)
   xp(2*nn-1-k) = co2&time(k)
   yp(2*nn-1-k) =  o395(k)
end do
gsres@gsFillColor       = res@xyLineColor                 ; color chosen
dummy2 = gsn_add_polygon (wks,p2,xp,yp,gsres)

res@xyLineColor="(/0.398,0.398,0.371/)"
p3 = gsn_csm_xy(wks,co2&time,aer,res)
overlay(plot,p3)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Tropospheric aerosol",.48,.78,txres)
do k=0,nn-1
  yp(k)          = aer95(k)
  xp(k)          = co2&time(k)
  xp(2*nn-1-k) = co2&time(k)
  yp(2*nn-1-k) =  aer05(k)
end do
gsres@gsFillColor       = res@xyLineColor                 ; color chosen
dummy3 = gsn_add_polygon (wks,p3,xp,yp,gsres)

res@xyLineColor=13
p4 = gsn_csm_xy(wks,co2&time,swv+luc+bcsnow+contrails,res)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Other anthropogenic",.48,.755,txres)
overlay(plot,p4)
do k=0,nn-1
   yp(k)          = (swv05(k)+luc05(k)+bcsnow05(k)+contrails05(k))
   xp(k)          = co2&time(k)
   xp(2*nn-1-k) = co2&time(k)
   yp(2*nn-1-k) =  (swv95(k)+luc95(k)+bcsnow95(k)+contrails95(k))
end do
gsres@gsFillColor       = res@xyLineColor                 ; color chosen
dummy4 = gsn_add_polygon (wks,p4,xp,yp,gsres)


res@xyLineColor=7
p5 = gsn_csm_xy(wks,co2&time,volc,res)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Volcanic",.48,.730,txres)
overlay(plot,p5)
do k=0,nn-1
   yp(k)          = volc05(k)
   xp(k)          = co2&time(k)
   xp(2*nn-1-k) = co2&time(k)
   yp(2*nn-1-k) =  volc95(k)
end do
gsres@gsFillColor       = res@xyLineColor                 ; color chosen
dummy5 = gsn_add_polygon (wks,p5,xp,yp,gsres)

res@xyLineColor=10
p6 = gsn_csm_xy(wks,co2&time,tsi,res)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Solar",.48,.705,txres)
overlay(plot,p6)
do k=0,nn-1
   yp(k)          = tsi05(k)
   xp(k)          = co2&time(k)
   xp(2*nn-1-k) = co2&time(k)
   yp(2*nn-1-k) =  tsi95(k)
end do
gsres@gsFillColor       = res@xyLineColor                 ; color chosen
dummy6 = gsn_add_polygon (wks,p6,xp,yp,gsres)

res@xyLineColor=1
res@xyLineThicknessF=2.
print(total)
p7 = gsn_csm_xy(wks,co2&time,total,res)
txres@txFontColor = res@xyLineColor
gsn_text_ndc(wks,"Total",.48,.680,txres)
overlay(plot,p7)
gsres@gsFillColor       = res@xyLineColor                 ; color chosen


;res@xyDashPattern=2
;res@xyLineThicknessF=1
;p20 = gsn_csm_xy(wks,co2&time,yp(0:nn-1),res)
;p21 = gsn_csm_xy(wks,co2&time,yp(nn:2*nn-1),res)
;overlay(plot,p20)
;overlay(plot,p21)


res1 = True
res1@vpHeightF= 0.175                    ; change aspect ratio of plot
res1@vpWidthF = 0.7
res1@gsnDraw = False
res1@gsnFrame = False
res1@tiYAxisString = "(W m~S~-2~N~ decade~S~-1~N~)"
res1@tiYAxisFont=12
res1@tiYAxisFontHeightF=0.01
res1@trXMinF = 1750
res1@trXMaxF = 2019.
res1@trYMinF = -0.09
res1@trYMaxF = 0.54
res1@tiYAxisSide          = "Right"
res1@tmYLBorderOn = False
res1@tmXBOn            = False
res1@tmYLOn            = False
res1@tmXTBorderOn = False
res1@tmXBBorderOn = False
res1@tmYRLabelsOn         = True
res1@tmYLOn = False
res1@tmYROn = True
res1@tmXTOn = False
res1@tmYLPrecision = 1
res1@xyLineThicknessF=4.
res1@vpYF=0.37
;res1@gsnMaximize           = True
;res1@gsnYRefLine                 = 0.
;res1@gsnYRefLineDashPattern =2 ; dotted


anthr=co2+ch4+n2o+halo+o3+swv+bcsnow+contrails+aer
b1=new( (/15/), float )
time1=new( (/15/), float )

do k=0,14
  b1(k)=regline(co2&time(100+k*10:129+k*10),anthr(100+k*10:129+k*10))*10
  time1(k)=1865+k*10
end do

;print(b1)
;print(time1)
res1@xyMarkLineModes   = "Markers"                ; choose which have markers
res1@xyMarkers         =  16
res1@xyMarkerSizeF = 10
p12 = gsn_csm_xy(wks,time1,b1,res1)
print(b1)
print(time1)
txres@txFontColor = 1
txres@txFontHeightF = 0.017                     ; text font height
;gsn_text_ndc(wks,"Rate of change anthropo-",.47,.345,txres)
;gsn_text_ndc(wks,"genic ERF",.47,.320,txres)
gsn_text_ndc(wks,"Rate of change anthropogenic ERF",.5,.38,txres)

;resp                  = True                      ; polyline mods desired
;resp@gsLineThicknessF = 2.0                       ; thickness of lines
;dum = new(3,graphic)
;ypts = (/ 0.,  0.49,  0.4,   0.41/)
;xpts = (/1850, 1850,  1850, 2019/)
;dum(0)=gsn_add_polyline(wks,p12,(/1850,1850/),(/-0.1,0.54/),resp)
;dum(1)=gsn_add_polyline(wks,p12,(/1850,2019/),(/0.54,0.54/),resp)
;dum(2)=gsn_add_polyline(wks,p12,(/1850,2019/),(/0.,0./),resp)


;draw(plot)
;draw(p12)
;frame(wks)
end
