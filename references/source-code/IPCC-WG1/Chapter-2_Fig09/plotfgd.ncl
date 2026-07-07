; Script “plotfgd.ncl”

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
begin


var="su"
;var="bc"



wks = gsn_open_wks ("eps","icesod"+var)
;wks = gsn_open_wks ("pdf","icesod"+var)
gsn_define_colormap(wks,"AR6_Line_Shade")
wks@wkOrientation = "landscape"
res = True
res@vpHeightF= 0.4                    ; change aspect ratio of plot
res@vpWidthF = 0.7
res@gsnDraw = False
res@gsnFrame = False
res@tmYRBorderOn = False
res@tmXTBorderOn = False
res@tmYROn = False
res@tmXTOn = False
res@tmXBLabelFont=12
res@tmYLLabelFont=12
res@txFontHeightF     = 0.015
if ( var.eq."su" ) then
  res@gsnLeftString   = "(a) Non-sea salt sulfate"
  res@tiYAxisString = "(ng g~S~-1~N~)"
else
  res@gsnLeftString   = "(b) Refractory black carbon"
  res@tiYAxisString = "(ng g~S~-1~N~)"
end if
res@tiYAxisFont=12
res@trXMaxF = 2020.
res@trYMinF = 0.
res@trXMinF = 1700
if ( var.eq."su" ) then
  res@trYMaxF = 999 ; sulfate
else
  res@trYMaxF = 14.99 ; bc
end if
;res@tmYLPrecision = 1
res@tiMainFont = 12
res@xyLineThicknessF=6.
res@gsnMaximize           = True
;res@gsnYRefLine                 = 0.

txres               = True                      ; text mods desired
txres@txJust        = "CenterLeft"              ; Default is "CenterCenter".

if ( var.eq."su" ) then
  f = addfile("su.nc","r")
else
  f = addfile("bc.nc","r")
end if
europe = f->europe
russia = f->russia
arctic = f->arctic
southamerica = f->southamerica
antarctica = f->antarctica
if ( var.eq."bc" ) then
  elbrus = f->elbrus
  greenland = f->greenland
end if
res@xyLineColor="(/0.031,0.180,0.445/)"
plot = gsn_csm_xy(wks,europe&time,europe,res)
res@xyLineColor="(/0.207,0.645,0.770/)"
p1 = gsn_csm_xy(wks,europe&time,russia,res)
overlay(plot,p1)
res@xyLineColor="(/0.863,0.328,0.180/)"
p2 = gsn_csm_xy(wks,europe&time,arctic,res)
overlay(plot,p2)
res@xyLineColor="(/0.922,0.609,0.180/)"
p3 = gsn_csm_xy(wks,europe&time,southamerica,res)
overlay(plot,p3)
res@xyLineColor="(/0.195,0.496,0.316/)"
p4 = gsn_csm_xy(wks,europe&time,antarctica,res)
overlay(plot,p4)

if ( var.eq."bc" ) then
  res@xyLineColor="(/0.664,0.094,0.094/)"
  p5 = gsn_csm_xy(wks,europe&time,elbrus,res)
  overlay(plot,p5)
  res@xyLineColor="(/0.129,0.203,0.855/)"
  p6 = gsn_csm_xy(wks,europe&time,greenland,res)
  overlay(plot,p6)
end if

if ( var.eq."su" ) then
  txres@txFontHeightF = 0.02                     ; text font height
  txres@txFontColor="(/0.863,0.328,0.180/)"
  gsn_text_ndc(wks,"Arctic",.19,.72,txres)
  txres@txFontColor="(/0.207,0.645,0.770/)"
  gsn_text_ndc(wks,"Russia",.19,.69,txres)
  txres@txFontColor="(/0.031,0.190,0.445/)"
  gsn_text_ndc(wks,"Europe",.19,.66,txres)
  txres@txFontColor="(/0.922,0.609,0.190/)"
  gsn_text_ndc(wks,"South America",.19,.63,txres)
  txres@txFontColor="(/0.195,0.496,0.316/)"
  gsn_text_ndc(wks,"Antarctica",.19,.60,txres)
else
  txres@txFontHeightF = 0.02                     ; text font height
  txres@txFontColor="(/0.863,0.328,0.190/)"
  gsn_text_ndc(wks,"Arctic",.19,.72,txres)
  txres@txFontColor="(/0.129,0.203,0.855/)"
  gsn_text_ndc(wks,"Greenland",.19,.69,txres)
  txres@txFontColor="(/0.207,0.645,0.770/)"
  gsn_text_ndc(wks,"Russia",.19,.66,txres)
  txres@txFontColor="(/0.664,0.094,0.094/)"
  gsn_text_ndc(wks,"Eastern Europe",.19,.63,txres)
  txres@txFontColor="(/0.031,0.190,0.445/)"
  gsn_text_ndc(wks,"Europe",.19,.60,txres)
  txres@txFontColor="(/0.922,0.609,0.190/)"
  gsn_text_ndc(wks,"South America",.19,.57,txres)
  txres@txFontColor="(/0.195,0.496,0.316/)"
  gsn_text_ndc(wks,"Antarctica",.19,.54,txres)
end if

draw(plot)
frame(wks)
end
