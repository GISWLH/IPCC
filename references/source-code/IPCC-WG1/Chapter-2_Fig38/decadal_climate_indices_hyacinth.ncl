;************************************
begin

  yrStrt = 1854
  yrLast = 2019
  xlabel = ispan(yrStrt,yrLast,1)

  f      = addfile("AMV.nc", "r")
  amv    = f->amv
  printVarSummary(amv)       ; variable overview
  amv = dtrend_msg_n(amv&year,amv,True,False,1)

  delete(f)

  f      = addfile("PDV.nc", "r")
  pdv    = f->pdv
  printVarSummary(pdv)       ; variable overview
  pdv = dtrend_msg_n(pdv&year,pdv,True,False,1)

  delete(f)

;************************************************
; create plots  
;************************************************
  plot = new(2,graphic)
  wtype          = "eps"
  wks = gsn_open_wks(wtype ,"decadal_climate_indices_hyacinth")                 ; ps,pdf,x11,png
  res                       = True          ; plot mods desired
  res@gsnDraw               = False
  res@gsnFrame              = False

  res@vpWidthF              = 0.95       ; change aspect ratio of plot
  res@vpHeightF             = 0.45
  res@trYMinF             =  -0.6                 ; manually set lower limit
  res@trYMaxF             =   0.6                 ;   "          upper
  res@trXMinF               = yrStrt - 5
  res@trXMaxF               = yrLast + 5
  res@xyLineColors        = (/"blue","red","deepskyblue","seagreen3","yellow3"/)
  res@xyLineThicknessF      = 1.      ; for higher quality large image
  res@xyDashPatterns       = 0                   ; dashed line for 2nd
  res@tiYAxisString         = "AMV (~S~o~N~C)"                  
  res@tiYAxisFontHeightF    = 0.020
  res@tiXAxisFontHeightF    = 0.020
  res@tmYLLabelFontHeightF  = 0.020      ; resize tick labels
  res@tmXBLabelFontHeightF  = 0.020    
;---For higher quality large images
  res@tiYAxisFontThicknessF  = 1.
  res@tmXBMajorThicknessF    = 1.
  res@tmXBMinorThicknessF    = 1.
  res@tmYLMajorThicknessF    = 1.
  res@tmYLMinorThicknessF    = 1.
  res@tmYLLabelFontThicknessF= 1.
  res@tmBorderThicknessF     = 1.
  res@tmXBMajorOutwardLengthF = 0.0               ; draw tickmarks inward
  res@tmXBMinorOutwardLengthF = 0.0               ; draw minor ticsk inward
  res@tmYLMajorOutwardLengthF = 0.0               ; draw tickmarks inward
  res@tmYLMinorOutwardLengthF = 0.0               ; draw minor ticsk inward
  res@tmXTMajorOutwardLengthF = 0.0               ; draw tickmarks inward
  res@tmXTMinorOutwardLengthF = 0.0               ; draw minor ticsk inward
  res@tmYRMajorOutwardLengthF = 0.0               ; draw tickmarks inward
  res@tmYRMinorOutwardLengthF = 0.0               ; draw minor ticsk inward
  res@tmYLFormat 	 = "@*+^sg"	; use "e" symbol, don't force 0's (see documentation)
  plot(0) = gsn_csm_xy(wks,xlabel,amv,res)
  res@tiYAxisString         = "PDV (~S~o~N~C)"   
  res@trYMinF             =  -0.7                 ; manually set lower limit
  res@trYMaxF             =   0.7                 ;   "          upper            
  plot(1) = gsn_csm_xy(wks,xlabel,pdv,res)
;----------------------------------------------------------------------
; Code for customizing a legend via simple_legend.
;----------------------------------------------------------------------
var_names = (/"COBE","ERSST","HADI","KAPL"/)
printVarSummary(var_names)
print(var_names)
icol = (/"blue","red","deepskyblue","seagreen3"/)

  txres               = True         ; Text resources
  txres@txFontHeightF = 0.013
  txres@txJust        = "CenterLeft"
  txres@txFont                = "Helvetica"
  txres@txAngleF      =  0.

  labels  = var_names
  xpos    = fspan(0.2, 0.70,dimsizes(var_names))

 do i = 0,dimsizes(labels)-1,1
      txres@txFontColor = icol(i)
     gsn_text_ndc(wks,labels(i),xpos(i),0.90,txres)
  end do
delete(i)
delete(txres)
;
;-----------------
  resP                                  = True         ; modify the panel plot
  resP@gsnDraw                          = True      ; don't draw yet
  resP@gsnFrame                         = False        ; don't advance frame yet
  resP@gsnPanelYWhiteSpacePercent      	= 1.0    	; default is 1.0
  resP@gsnPanelXWhiteSpacePercent      	= 1.0   	 ; default is 1.0
  resP@gsnPanelTop                      = 0.99
  resP@gsnPanelBottom                   = 0.01
  resP@gsnPanelLeft                     = 0.01
  resP@gsnPanelRight                    = 0.99
  resP@gsnMaximize                      = True         ; large format
  resP@gsnPaperOrientation              = "portrait"   ; force portrait
;*******************************************
gsn_panel(wks,plot(0:),(/2,1/),resP)     ; now draw as one plot

end


