; Script “plotmimoanf.ncl”

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
begin
  fine=0
  if ( fine.eq.1 ) then
    wks = gsn_open_wks("pdf","mimoanf")           ; open a pdf file
    ;wks = gsn_open_wks("eps","mimoanf")           ; open a pdf file
  else
    wks = gsn_open_wks("pdf","mimoan")           ; open a pdf file
    ;wks = gsn_open_wks("eps","mimoan")           ; open a pdf file
  end if
  a = addfile("mimof.nc","r")
  if ( fine.eq.1 )then
    tmm = a->tmf
    smm = a->smf
  else
    tmm = a->tmm
    smm = a->smm
  end if
  ;gsn_define_colormap(wks,"BrownBlue12")
  ;gsn_define_colormap(wks,"CBR_coldhot")
  ;gsn_define_colormap(wks,"AR6_Temp_10")
  gsn_define_colormap(wks,"chem_div")
  ;gsn_define_colormap(wks,"GreenMagenta16")
  ;gsn_define_colormap(wks,"BlueDarkRed18")
  ;
  txres = True
  ;txres@txFont=12
  txres@txFontHeightF = 0.03                    ; font smaller. default big
  txres@txJust="CenterCenter"
  gsn_text_ndc(wks,"% yr~S~-1~N~",0.5,0.2,txres)
  ;gsn_text_ndc(wks,"-71",0.272,0.305,txres)
  res                   = True
  res@gsnDraw = False
  res@gsnFrame = False
  res@mpProjection      = "Robinson"       ; choose projection
  res@mpGridAndLimbOn   = True              ; turn on lat/lon lines
  res@mpGridLineColor = 0.
  res@mpPerimOn         = False             ; turn off box around plot
  res@mpGridLatSpacingF = 30.               ; spacing for lat lines
  res@mpGridLonSpacingF = 30.               ; spacing for lon lines
  res@mpGridLineDashPattern = 2
  res@mpGeophysicalLineThicknessF = 2
  res@mpLimbLineDashPattern=0
  res@mpLimitMode       = "LatLon"
  res@mpMinLatF         = -70.
  res@mpMaxLatF         = 70.
  res@mpFillOn          = False
  res@cnFillOn          = True              ; color plot desired
  res@txFontHeightF     = 0.015
  res@cnFillMode     = "CellFill"
  res@cnLinesOn      = False              ; turn off contour lines
  res@cnLineLabelsOn = False
  res@cnLevelSelectionMode = "ExplicitLevels"
  ;colors=(/3*16,4*16,5*16,6*16,7*16,0*16,8*16,9*16,10*16,11*16,12*16/)
  colors=(/3,3+21,3+21*2,3+4*21,3+5*21,3+6*21,0,3+7*21,3+8*21,3+9*21,3+10*21,3+12*21/)
  res@cnFillColors = colors
  ;res@cnLevels           = (/-2,-1.8,-1.6,-1.4,-1.2,-1,-.8,-.6,-.4,-.2,0,.2,.4,.6,.8,1,1.2,1.4,1.6,1.8,2.0/)
  ;res@cnLevels           = (/-1.8,-1.2,-.6,0,.6,1.2,1.8/)
  res@cnLevels           = (/-20,-1.6,-1.2,-0.8,-0.4,0,0.4,0.8,1.2,1.6,20/)
  res@pmLabelBarDisplayMode = "Conditional"
  res@pmLabelBarOrthogonalPosF = -0.01          ; move farther to plot
  res@pmLabelBarParallelPosF = 0.5
  res@lbOrientation        = "horizontal"       ; vertical label bars
                                ;res@lbLabelAlignment = "ExternalEdges"
  ;res@cnMaxDataValueFormat = "*+.2^sg"
  ;res@cnLabelBarEndStyle = "IncludeMinMaxLabels"
  res@pmLabelBarHeightF = 0.06
  res@pmLabelBarWidthF = 0.4
  res@lbLabelFontHeightF = 0.015         ; Decrease font size.

    res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill)
    ;res@cnMissingValFillColor   = "(/0.75,0.75,0.75/)"
    res@cnMissingValFillColor   = "grey" ; should be darkgrey
                                ;
    res@tiMainString = ""
    if ( fine.eq.1 ) then
      res@gsnLeftString = "(d)"
      res@gsnCenterString = " Trend in fine-mode aerosol optical depth (2000 - 2019)" ; don't use the variable long_name
    else
      res@gsnLeftString = "(c)"
      res@gsnCenterString = "Trend in aerosol optical depth (2000 - 2019)" ; don't use the variable long_name
    end if
  res@gsnRightString = "" ; don't use the variable units
  res@gsnPaperOrientation = "Landscape"
  res@gsnMaximize = True

  ;cmap_data = read_colormap_file("chem_div")
  ;res@cnFillPalette       = cmap_data(::-1,:)
  contour = gsn_csm_contour_map(wks,tmm,res)  ; create the plot


  ; www.ncl.ucar.edu/Applications/Scripts/scatter_6.ncl
  a = addfile("../aeronet/antrend.nc","r")
  if ( fine.eq.1 ) then
    tanet = a->taodf
    sanet = a->saodf
  else
    tanet = a->taod
    sanet = a->saod

  end if
  tanet=mask(tanet,sanet,0.1)
  xlon = a->xlon
  ylat = a->xlat
  an=ndtooned(tanet)
;  print(an)
  lon=ndtooned(xlon)-6.
  lat=ndtooned(ylat)

  mkres2               = True
  mkres2@gsMarkerIndex = 5
  mkres2@gsMarkerOpacityF = 0.5
  nx=30
  ny=30
  sigmark   = new(nx*ny,graphic)
  sigmark1   = new(nx*ny,graphic)
  do j=0,ny-1
    mkres2@gsMarkerSizeF = 15+30*cos(ylat(0,j)/180*3.141)
    do i=0,nx-1
      if (smm(i,j).lt.0.1) then
        sigmark(i*nx+j)=gsn_add_polymarker(wks,contour,xlon(i,j)-9,ylat(i,j)*-1,mkres2)
        sigmark1(i*nx+j)=gsn_add_polymarker(wks,contour,xlon(i,j)-3.,ylat(i,j)*-1,mkres2)
      end if
    end do
  end do



  mkres               = True
  mkres@mpProjection      = "Robinson"       ; choose projection
  ;---Arrays for attaching two sets of markers
  nlevels=11
  dum_fill   = new(nlevels-1,graphic)
  dum_hollow = new(nlevels-1,graphic)

  mkres@gsMarkerThicknessF = 2.0      ; Twice as thick
  mkres1               = True
  mkres1@gsMarkerThicknessF = 2.0      ; Twice as thick
;
; For each range, gather the data that falls in this range
; and draw the set of markers at those lat/lon locations.
;
  levels=res@cnLevels
  ;colors=(/3,4,5,6,7,0,8,9,10,11,12/)

  ;colors=gsn_retrieve_colormap(wks)
  ;print(colors)
  do i=0,nlevels-2
    ii = ind(levels(i).le.an.and.an.lt.levels(i+1))
    if (.not.ismissing(ii(0))) then
    ;print(i)
    ;print(colors(i))
    ;print(an(ii))
    ;print(lon(ii))
    ;print(lat(ii))
    mkres@gsMarkerIndex = 16          ; Filled dots
    mkres@gsMarkerSizeF = 10
    mkres@gsMarkerColor = colors(i)
    dum_fill(i) = gsn_add_polymarker(wks,contour,lon(ii),lat(ii),mkres)

;---Draw the markers again, only this time hollow, to get an outline.
    mkres1@gsMarkerIndex = 4           ; Hollow dots
    mkres1@gsMarkerSizeF = 10
    mkres1@gsMarkerColor = "black"
    dum_hollow(i) = gsn_add_polymarker(wks,contour,lon(ii),lat(ii),mkres1)
    end if
    delete(ii)
  end do

  draw(contour)
  frame(wks)
end
