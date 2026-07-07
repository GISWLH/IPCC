begin

  yrStrt = 1950
  yrLast = 2019
  xlabel = ispan(yrStrt,yrLast,1)
  print(xlabel)

  f      = addfile ("BMI.nc", "r")
  bmi    = f->bmi(:,{yrStrt:yrLast})
  printVarSummary(bmi)       ; variable overview
  bmi = dtrend_msg_n(bmi&year,bmi,True,False,1)

  delete(f)

  f      = addfile ("IOD.nc", "r")
  iod    = f->iod(:,{yrStrt:yrLast})
  printVarSummary(iod)       ; variable overview
  iod = dtrend_msg_n(iod&year,iod,True,False,1)

  delete(f)

  f      = addfile ("NINO34.nc", "r")
  amv    = f->nino34(:,{yrStrt:yrLast})
  printVarSummary(amv)       ; variable overview
  delete(f)

  f      = addfile ("AMM.nc", "r")
  amm    = f->amm(:,{yrStrt:yrLast})
  printVarSummary(amm)       ; variable overview
  amm = dtrend_msg_n(amm&year,amm,True,False,1)
  delete(f)

  f      = addfile ("AZM.nc", "r")
  atl    = f->atl(:,{yrStrt:yrLast})
  printVarSummary(atl)       ; variable overview
  atl = dtrend_msg_n(atl&year,atl,True,False,1)
  delete(f)
;************************************************
; create plots  
;************************************************
  plot = new(6,graphic)
  wtype          = "eps"
  wks = gsn_open_wks(wtype ,"interannual_climate_indices_hyacinth")                 
  res                       = True          ; plot mods desired
  res@gsnDraw               = False
  res@gsnFrame              = False
  res@vpWidthF              = 0.95       ; change aspect ratio of plot
  res@vpHeightF             = 0.20
  res@trXMinF               = yrStrt - 5
  res@trXMaxF               = yrLast + 5
  res@xyLineColors        = (/"blue","red","deepskyblue","seagreen3","yellow3"/)
  res@xyLineThicknessF      = 1.      ; for higher quality large image
  res@xyDashPatterns       = 0                   ; dashed line for 2nd
  res@tiYAxisString         = "IOB (~S~o~N~C)"                  
  res@tiYAxisFontHeightF    = 0.05
  res@tfPolyDrawOrder       = "PreDraw"    ; Draw any attached primitives
  res@tmXBOn                = False
  res@tmYLLabelFontHeightF  = 0.01      ; resize tick labels
  res@tmYROn               = False   ; Turn off left tickmarks
 ;---For higher quality large images
  res@tiYAxisFontThicknessF  = 1.
  res@tmXBMajorThicknessF    = 1.
  res@tmXBMinorThicknessF    = 1.
  res@tmYLMajorThicknessF    = 1.
  res@tmYLMinorThicknessF    = 1.
  res@tmYLLabelFontThicknessF= 1.
  res@tmBorderThicknessF     = 1.
  res@tmYLFormat 	 = "@*+^sg"	; use "e" symbol, don't force 0's (see documentation)
  res@tmXBMajorOutwardLengthF = 0.0               ; draw tickmarks inward
  res@tmXBMinorOutwardLengthF = 0.0               ; draw minor ticsk inward
  res@tmYLMajorOutwardLengthF = 0.0               ; draw tickmarks inward
  res@tmYLMinorOutwardLengthF = 0.0               ; draw minor ticsk inward
  res@tmXTMajorOutwardLengthF = 0.0               ; draw tickmarks inward
  res@tmXTMinorOutwardLengthF = 0.0               ; draw minor ticsk inward
  res@tmYRMajorOutwardLengthF = 0.0               ; draw tickmarks inward
  res@tmYRMinorOutwardLengthF = 0.0               ; draw minor ticsk inward
;
  res1                      = True
  res1@tmYLFormat 	 = "@*+^sg"	; use "e" symbol, don't force 0's (see documentation)
  res1@gsnDraw              = False
  res1@gsnFrame             = False
  res1@vpWidthF             = 0.90          ; change aspect ratio of plot
  res1@vpHeightF            = 0.25
  res1@trXMinF              = res@trXMinF
  res1@trXMaxF              = res@trXMaxF
  res1@xyDashPatterns       = 0                   ; dashed line for 2nd
  res1@xyLineColors          = res@xyLineColors  ; 3 different colors
  res1@xyLineThicknessF     = 1.0
  res1@tiYAxisFontHeightF   = 0.05
  res1@tiYAxisSide          = "Right"	
  res1@tiYAxisString        = "IOD (~S~o~N~C)"       
;---For higher quality large images
  res1@tiYAxisFontThicknessF   = 1.
  res1@tmXBLabelFontThicknessF = 1.0
  res1@tmYRLabelFontThicknessF = 1.
  res1@tmXBMajorThicknessF     = 1.0
  res1@tmXBMinorThicknessF     = 1.0
  res1@tmYLMajorThicknessF     = 1.0
  res1@tmYLMinorThicknessF     = 1.0
  res1@tmBorderThicknessF      = 1.
  res1@tfPolyDrawOrder       = "PreDraw"    ; Draw any attached primitives
  res1@tmXBOn               = False
  res1@tmXTOn               = False
  res1@tmYLLabelsOn         = False
  res1@tmYRLabelFontHeightF = 0.01      ; resize tick labels
  res1@tmYRLabelsOn         = False
  res1@tmYLOn               = False   ; Turn off left tickmarks
  res1@tmYLFormat 	 = "@*+^sg"	; use "e" symbol, don't force 0's (see documentation)   

  plot(0) = gsn_csm_xy(wks,xlabel,bmi,res)
   res1@tmYRLabelsOn         = True
;----------------------------------------------------------------------
; Code for customizing a legend via simple_legend.
;----------------------------------------------------------------------
;======================================================== 
;========================================================
var_names = (/"COBE","ERSST","HADI","KAPL","OISST"/)
printVarSummary(var_names)
print(var_names)
icol = (/"blue","red","deepskyblue","seagreen3","yellow3"/)

  txres               = True         ; Text resources
  txres@txFontHeightF = 0.013
  txres@txJust        = "CenterLeft"
  txres@txFont                = "Helvetica"
  txres@txAngleF      =  0.

  labels  = var_names
  xpos    = fspan(0.2, 0.70,dimsizes(var_names))

 do i = 0,dimsizes(labels)-1,1
      txres@txFontColor = icol(i)
     gsn_text_ndc(wks,labels(i),xpos(i),0.98,txres)
  end do
delete(i)
delete(txres)
;
  plot(1) = gsn_csm_xy(wks,xlabel,iod,res1)
  res@tmXTOn                = False
  res@tiYAxisString         = "Nino34 (~S~o~N~C)" 
  res@tmYLFormat 	 = "0@*+^sg"	;    
  plot(2) = gsn_csm_xy(wks,xlabel,amv,res)
  res@tmYLFormat 	 = "0@*+^sg"	  
  res1@tmYLFormat 	 = "0@*+^sg"	
  res1@tmXBOn               = True
  res1@tmXBMode             = "Explicit"
  res1@tmXBLabelFontHeightF = 0.02
  res1@tiYAxisString        = "AMM (~S~o~N~C)"       
  plot(3) = gsn_csm_xy(wks,xlabel,amm,res1)
  res@tmXTOn                = False
  res@tiYAxisString         = "AZM (~S~o~N~C)" 
  res@tmXBOn                = False      
  res@tmXBOn               = True
  res@tmXBMode             = "Explicit"
  plot(4) = gsn_csm_xy(wks,xlabel,atl,res)
  res1@tmXBOn               = True
  res1@tmXBMode             = "Explicit"
  res1@tmXBLabelFontHeightF = 0.02
  res1@tiYAxisString        = "PDO (~S~o~N~C)"       
  res1@xyLineColors        = (/"red","red","deepskyblue","seagreen3","yellow3"/)
;;;;;; Attach plots along the X axes
  attachres1                     = True
  attachres1@gsnAttachPlotsXAxis = True  ;; attaches along x-axis
  attachres1@gsnAttachBorderOn   = False ;; No border please
  attachres2                     = True
  attachres2@gsnAttachPlotsXAxis = True  ;; attaches along x-axis
  attachres2@gsnAttachBorderOn   = False ;; No border please
  attachid1  = gsn_attach_plots(plot(0),plot(1:4),attachres1,attachres2)
;;;;;; Maximize output on the page and draw everything
  pres = False               ; No resources needed
  maximize_output(wks,pres)  ; Maximize plot on page
end


