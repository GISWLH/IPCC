PRO ipcc_temis_no2_map_v5

;---------------------------------------------------------------------------------------------------------------------------------------
;This code reads the GOME_SCIA_GOME2ab_TroposNO2_v2.3_041996-092017_correctedx3_timmean.nc file and plots trop. NO2 patterns (1996-2017).
;The self-consistent GOME, SCIAMACHY, and GOME-2 dataset from Georgoulias et al. (2019) (available on http://www.temis.nl) is used.
;---------------------------------------------------------------------------------------------------------------------------------------
;The code was created by Dr. Aristeidis K. Georgoulias (ageor@auth.gr), Dept. of Meteorology and Climatology, AUTH, Thessaloniki, Greece
;for the needs of the IPCC Working Group I (WGI) Sixth Assessment Report (Chapter 6).
;---------------------------------------------------------------------------------------------------------------------------------------

dir='C:\IPCC\'

;Files to read
pattern=dir+'GOME_SCIA_GOME2ab_TroposNO2_v2.3_041996-092017_correctedx3_timmean.nc'

filenames=file_search(pattern)
num_files=n_elements(filenames)
if num_files eq 0 then begin
 print, 'ERROR: no files found'
 return
endif

;Number of files to read
print, num_files

FOR IFILE=0, num_files-1 do begin

;---
plottype='total';takes values 'total', 'annual', 'monthly', 'seasonal' or 'generic'

;---
parameter='TroposNO2'

;---
Ncolors=24
bottom=3
up=254
range=30
Divisions=12

;---
barmax=12;0.80
barmin=0
latdel=5
londel=5
grid=0.1251

;---
tabletype='mycolors';takes values 'brewer' or 'standard'
tablenumber=78
rever='noreverse';takes values 'reverse' or 'noreverse'

;---Set colortable values
;tvlct,[[249],[246],[193]],1
;tvlct,[[248],[241],[151]],2
;tvlct,[[249],[239],[108]],3
;tvlct,[[251],[228],[62]],4
;tvlct,[[254],[214],[38]],5

;tvlct,[[253],[199],[31]],6
;tvlct,[[251],[182],[27]],7
;tvlct,[[247],[164],[22]],8
;tvlct,[[243],[147],[24]],9
;tvlct,[[240],[130],[19]],10

;tvlct,[[238],[114],[24]],11
;tvlct,[[236],[95],[26]],12
;tvlct,[[232],[68],[30]],13
;tvlct,[[230],[44],[31]],14
;tvlct,[[229],[29],[32]],15

;tvlct,[[229],[16],[22]],16
;tvlct,[[223],[9],[19]],17
;tvlct,[[208],[19],[23]],18
;tvlct,[[207],[21],[24]],19
;tvlct,[[224],[66],[65]],20

;tvlct,[[238],[118],[120]],21
;tvlct,[[246],[176],[178]],22

;---
comment='Long term average and trends in tropospheric NO!D2!N column over 1996-2017';'Trop. NO!D2!N (GOME, SCIAMACHY & GOME-2A/2B)'

;;;EASTERN CHINA
;;;---------------------------------------
lat_min1=30
lat_max1=40
lon_min1=107
lon_max1=122
;;;---------------------------------------

;;;NORTHWESTERN CHINA
;;;---------------------------------------
lat_min2=40
lat_max2=45
lon_min2=82
lon_max2=92
;;;---------------------------------------

;;;WESTERN INDIA
;;;---------------------------------------
lat_min3=20
lat_max3=25
lon_min3=80
lon_max3=90
;;;---------------------------------------

;;;EASTERN US
;;;---------------------------------------
lat_min4=32
lat_max4=42
lon_min4=-90
lon_max4=-75
;;;---------------------------------------

;;;WESTERN EUROPE
;;;---------------------------------------
lat_min5=45
lat_max5=55
lon_min5=-2
lon_max5=13
;;;---------------------------------------

;;;MIDDLE EAST
;;;---------------------------------------
lat_min8=28
lat_max8=38
lon_min8=34
lon_max8=60
;;;---------------------------------------

;;;SOUTH AFRICA
;;;---------------------------------------
lat_min9=-29
lat_max9=-24
lon_min9=24
lon_max9=34
;;;---------------------------------------

;;;WEST COAST US
;;;---------------------------------------
lat_min10=32
lat_max10=42
lon_min10=-123
lon_max10=-115
;;;---------------------------------------

;;;SOUTHEASTERN AMERICA
;;;---------------------------------------
lat_min14=-29
lat_max14=-19
lon_min14=-52
lon_max14=-42
;;;---------------------------------------

;;;JAPANESE ARCHIPELAGO
;;;---------------------------------------
lat_min15=32
lat_max15=37
lon_min15=132
lon_max15=142
;;;---------------------------------------

lat_min=-89.8;GLOBE
lat_max=89.8
lon_min=-180
lon_max=180


month=month

cdfid = ncdf_open(filenames(IFILE),/NOWRITE)

varname1='lon'
varname2='lat'
varname3='time'
varname4=parameter

lon = ncdfread2(filenames(IFILE), varname1)
lat = ncdfread2(filenames(IFILE), varname2)
time = ncdfread2(filenames(IFILE), varname3)
SIS = ncdfread2(filenames(IFILE), varname4)

cenlon=fltarr(size(lon,/N_ELEMENTS),size(lat,/N_ELEMENTS),size(time,/N_ELEMENTS))
cenlat=fltarr(size(lon,/N_ELEMENTS),size(lat,/N_ELEMENTS),size(time,/N_ELEMENTS))
PARAM=fltarr(size(lon,/N_ELEMENTS),size(lat,/N_ELEMENTS),size(time,/N_ELEMENTS))
icol=fltarr(size(lon,/N_ELEMENTS),size(lat,/N_ELEMENTS),size(time,/N_ELEMENTS))
PARAM=SIS

if plottype eq 'total' then begin
step=''
outstep=comment
endif

if plottype eq 'annual' then begin
step=string(indgen(finyear-inityear+1)+inityear,format='(i4)')
outstep=string(indgen(finyear-inityear+1)+inityear,format='(i4)')
endif

if plottype eq 'monthly' then begin
step=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
outstep=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
endif

if plottype eq 'seasonal' then begin
step=['DJF','MAM','JJA','SON']
outstep=['DJF','MAM','JJA','SON']
endif

for t=0,size(time,/N_ELEMENTS)-1 do begin

if plottype eq 'total' then begin
steps=string(step(t))
endif

if plottype ne 'total' then begin
steps='_'+string(step(t))
endif

; open device for ploting
 orig_device=!d.name
 ;dataColors=!P.COLOR

;open device for ploting
 orig_device=!d.name

;set_plot,'ps'
Set_Plot, 'PS'

; set_plot,'PS', /copy

 !P.FONT=1
 
device, filename=dir+strmid(filenames(IFILE),8,strlen(filenames(IFILE))-11)+'_ipcc_v6.ps', COLOR=1, BITS_PER_PIXEL=8,$
 /INCHES, Set_Font='Arial';, xoffset=0,yoffset=0;,/landscape;XSIZE=5, YSIZE=3,

restname=''

loadct, 0

tvlct,[[132],[132],[132]],664

map_set, /robinson,  limit=[lat_min,lon_min,lat_max,lon_max],  position = [0.05, .155, 0.95, 0.88],  $
         /noerase, color=254;, /hires;, /isotropic;, /hires ;, /isotropic

;polyfill, [-179.99,-80,0,0,-179.99,-179.99], [lat_min,lat_min,lat_min,lat_max,lat_max,lat_min], color=132
;polyfill, [0,179.99,179.99,0,0], [lat_min,lat_min,lat_max,lat_max,lat_min], color=132

if tabletype eq 'mycolors' and rever eq 'reverse' then begin
colorFile = Filepath(SUBDIRECTORY=['resource','colors'], 'mycolors.tbl')
CTLOAD, tablenumber, Ncolors=Ncolors, bottom=bottom, clip=[bottom,up], file=colorfile,/reverse
endif

if tabletype eq 'mycolors' and rever eq 'noreverse' then begin
colorFile = Filepath(SUBDIRECTORY=['resource','colors'], 'mycolors.tbl')
CTLOAD, tablenumber, Ncolors=Ncolors, bottom=bottom, clip=[bottom,up], file=colorfile
endif

for x=0, size(lon,/N_ELEMENTS)-1.0 do begin
for y=0, size(lat,/N_ELEMENTS)-1.0 do begin

icol(x,y,t)=fix(((PARAM(x,y,t))-(barmin*1.0))*(Ncolors*1.0)/(barmax*1.0-(barmin*1.0)))+Bottom*1.0

if icol(x,y,t) lt bottom then icol(*,*,t)=bottom
if icol(x,y,t) gt bottom+Ncolors-1 then icol(*,*,t)=bottom+Ncolors-1
if icol(x,y,t) eq -999 then icol(*,*,t)='NaN'

if lat(y) gt lat_min and lat(y) lt lat_max then begin

if finite(PARAM(x,y,t)) eq 1 then begin

polyfill, [lon(x)-grid,lon(x)+grid,lon(x)+grid,lon(x)-grid], [lat(y)-grid,lat(y)-grid,lat(y)+grid,lat(y)+grid], color=icol(x,y,t)

endif

if finite(PARAM(x,y,t)) eq 0 then begin
polyfill, [lon(x)-grid,lon(x)+grid,lon(x)+grid,lon(x)-grid], [lat(y)-grid,lat(y)-grid,lat(y)+grid,lat(y)+grid], color=664

endif

endif

endfor
endfor

ColorBar, Divisions=Divisions, Range=[barmin,barmax], vertical=vertical, Format='(i2)', Bottom=Bottom, Ncolors=Ncolors, tickinterval=0.5, $
   Position = [0.1, 0.06, 0.9, 0.12], Minor=1, ticklen=1, Subticklen=1, Right=right, charsize=1.4, color=0;, Color=!P.Background

CTLOAD, 0

map_continents,/coasts, MLINETHICK=1.0, color=0;, /hires;,/countries; Black Sea

map_grid, /robinson, box_axes=0,/no_grid,latdel=40,londel=40,charsize=1.2,/Horizon

CTLOAD,0

oplot, [lon_min1,lon_min1,lon_max1,lon_max1,lon_min1], [lat_min1,lat_max1,lat_max1,lat_min1,lat_min1], color=0, thick=2.5
oplot, [lon_min2,lon_min2,lon_max2,lon_max2,lon_min2], [lat_min2,lat_max2,lat_max2,lat_min2,lat_min2], color=0, thick=2.5
oplot, [lon_min3,lon_min3,lon_max3,lon_max3,lon_min3], [lat_min3,lat_max3,lat_max3,lat_min3,lat_min3], color=0, thick=2.5
oplot, [lon_min4,lon_min4,lon_max4,lon_max4,lon_min4], [lat_min4,lat_max4,lat_max4,lat_min4,lat_min4], color=0, thick=2.5
oplot, [lon_min5,lon_min5,lon_max5,lon_max5,lon_min5], [lat_min5,lat_max5,lat_max5,lat_min5,lat_min5], color=0, thick=2.5
oplot, [lon_min8,lon_min8,lon_max8,lon_max8,lon_min8], [lat_min8,lat_max8,lat_max8,lat_min8,lat_min8], color=0, thick=2.5
oplot, [lon_min9,lon_min9,lon_max9,lon_max9,lon_min9], [lat_min9,lat_max9,lat_max9,lat_min9,lat_min9], color=0, thick=2.5
oplot, [lon_min10,lon_min10,lon_max10,lon_max10,lon_min10], [lat_min10,lat_max10,lat_max10,lat_min10,lat_min10], color=0, thick=2.5
oplot, [lon_min14,lon_min14,lon_max14,lon_max14,lon_min14], [lat_min14,lat_max14,lat_max14,lat_min14,lat_min14], color=0, thick=2.5
oplot, [lon_min15,lon_min15,lon_max15,lon_max15,lon_min15], [lat_min15,lat_max15,lat_max15,lat_min15,lat_min15], color=0, thick=2.5

xyouts, lon_min1-10,lat_min1, '6',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5
xyouts, lon_min2,lat_min2-8, '5',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5
xyouts, lon_min3+2,lat_min3-8, '8',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5
xyouts, lon_max4+4,lat_min4, '2',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5
xyouts, lon_min5,lat_max5+3, '3',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5
xyouts, lon_min8+6,lat_min8-8, '4',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5
xyouts, lon_max9+2,lat_min9-4, '10',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5
xyouts, lon_min10-8,lat_min10+4, '1',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5
xyouts, lon_max14+2,lat_min14, '9',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5
xyouts, lon_max15+2,lat_min15, '7',/ DATA, alignment=0,charsize=1.2, color=0, charthick=1.5

if plottype ne 'total' then begin
xyouts, .50 , 0.91, outstep(t), charsize = 1.4, charthick=1.5, /normal, color=0,orientation=0,alignment=0.5
endif

if plottype eq 'total' then begin
xyouts, .50 , 0.91, comment, charsize = 1.4, charthick=1.5, /normal, color=0,orientation=0,alignment=0.5
endif

xyouts, .830 , 0.13, '10!E15!N molec. cm!E-2!N', charsize = 1.2, charthick=1.5, /normal, color=0,orientation=0,alignment=0.5
xyouts, .11 , 0.155, '(a)', charsize = 1.7, charthick=1.5, /normal, color=0,orientation=0,alignment=0

endfor

device, /close_file
set_plot, orig_device

ENDFOR

end

function ncdfread2, fname, varname
    ncid = NCDF_OPEN (fname, /NOWRITE)

    variable = -1
    ncdINFO = NCDF_INQUIRE (ncid)
    for varID = 0, ncdINFO.NVARS-1 do begin
        varINFO = NCDF_VARINQ (ncid, varid)
    if (varINFO.NAME eq varname) then begin
            NCDF_VARGET, ncid, varID, variable
            filler = '32766s'
            if (varINFO.DATATYPE eq 'INT')    then filler = -32767
            if (varINFO.DATATYPE eq 'LONG')   then filler = -2147483647L
            if (varINFO.DATATYPE eq 'FLOAT')  then filler = float(9.9692099683868690e+36)
            if (varINFO.DATATYPE eq 'DOUBLE') then filler = double(9.9692099683868690e+36)
            for i = 0, varINFO.NATTS-1 do begin
               r = NCDF_ATTNAME (ncid, varid, i)
          if (r eq '_FillValue') then $
              NCDF_ATTGET, ncid, varid, '_FillValue', filler
            endfor
            idx = where (variable eq filler, cnt)
            if (cnt gt 0) then variable[idx] = !VALUES.F_NAN
            break
    endif
    endfor
    NCDF_CLOSE, ncid
    return, variable
end


;+
; NAME:
;       CTLOAD
;
; PURPOSE:
;
;       This is a drop-in replacement for the ITTVIS-supplied program LOADCT.
;       The same keywords used with LOADCT apply. In addition, a REVERSE keyword
;       is supplied to reverse the color table vectors, and a CLIP keyword is
;       supplied to be able to clip the normal LOADCT color table. This is
;       extremely useful if you wish to use a reduced number of colors. Also,
;       all color table loading is handled silently. (To fix a major pet-peeve
;       of mine.)
;
; NOTE: Program development on CTLOAD has been stopped as of 4 Feb 2011.
;       All future development of this program will occur in cgLoadCT,
;       a program that is part of the Coyote Graphics System.
;
; AUTHOR:
;
;       FANNING SOFTWARE CONSULTING
;       David Fanning, Ph.D.
;       1645 Sheely Drive
;       Fort Collins, CO 80526 USA
;       Phone: 970-221-0438
;       E-mail: david@idlcoyote.com
;       Coyote's Guide to IDL Programming: http://www.idlcoyote.com
;
; CATEGORY:

;       Utilities
;
; CALLING SEQUENCE:
;
;       CTLOAD, table
;
; AUGUMENTS:
;
;       table:         Optional table number to load. Integer from 0 to the number of
;                      tables in the file, minus 1. Default value is 0.
;
; KEYWORDS:
;
;       ADDCMD:        Set this keyword to add the CTLOAD command to the current cgWindow
;                      command list.
;
;       BOTTOM:        The first color table index. Set to 0 by default.
;
;       BREWER:        Set this keyword if you wish to use the Brewer Colors, as
;                      implemented by Mike Galloy in the file brewer.tbl, and implemented
;                      here as fsc_brewer.tbl. See these references:
;
;                      Brewer Colors: http://www.personal.psu.edu/cab38/ColorBrewer/ColorBrewer_intro.html
;                      Mike Galloy Implementation: http://michaelgalloy.com/2007/10/30/colorbrewer.html
;
;                      This program will look first in the $IDL_DIR/resource/colors directory for
;                      the color table file, and failing to find it there will look in the same
;                      directory that the source code of this program is located, then in the IDL path.
;                      Finally, if it still can't find the file, it will ask you to locate it.
;                      If you can't find it, the program will simply return without loading a color table.
;
;                      NOTE: YOU WILL HAVE TO DOWNLOAD THE FSC_BREWER.TBL FILE FROM THE COYOTE LIBRARY AND
;                      PLACE IT IN ONE OF THE THREE PLACES OUTLINED ABOVE:
;
;                      http://www.idlcoyote.com/programs/fsc_brewer.tbl
;
;       CLIP:          A one- or two-element integer array that indicates how to clip
;                      the original color table vectors. This is useful if you are
;                      restricting the number of colors, and do not which to have
;                      black or white (the usual color table end members) in the
;                      loaded color table. CLIP[0] is the lower bound. (A scalar
;                      value of CLIP is treated as CLIP[0].) CLIP[1] is the upper
;                      bound. For example, to load a blue-temperature color bar
;                      with only blue colors, you might type this:
;
;                        IDL> CTLOAD, 1, CLIP=[110,240]
;                        IDL> CINDEX
;
;                     Or, alternatively, if you wanted to include white at the upper
;                     end of the color table:
;
;                        IDL> CTLOAD, 1, CLIP=110
;                        IDL> CINDEX
;
;       RGB_TABLE:    If this keyword is set to a named variable, the color table
;                     is returned as an [NCOLORS,3] array and no colors are loaded
;                     in the display.
;
;       FILE:         The name of a color table file to open. By default colors1.tbl in
;                     the IDL directory.
;
;       GET_NAMES:    If set to a named variable, the names of the color tables are returned
;                     and no colors are loaded in the display. Note that RGB_TABLE cannot be
;                     used concurrently with GET_NAMES. Use two separate calls if you want both.
;
;       NCOLORS:      The number of colors loaded. By default, !D.TABLE_SIZE.
;
;       REVERSE:      If this keyword is set, the color table vectors are reversed.
;
;       ROW:          Set this keyword to indicate you are getting the RGB_TABLE vectors
;                     for use in the IDL's object graphics routines. Whereas TVLCT expects color
;                     tablesto be 256x3 (column vectors), the object graphics routines expect them
;                     to be 3x256 (row vectors). Setting this keyword will transpose the vectors
;                     before they are returned.
;
;       SILENT:       This keyword is provided ONLY for compatibility with LOADCT. *All*
;                     color table manipulations are handled silently.
;
;       WINDOW:       Set this keyword to send the colors to an cgWindow program.
;
;       WINID:        The window index number of an cgWindow to receive the color vectors.
;
; EXAMPLES:
;
;       Suppose you wanted to create a color table that displayed negative values with
;       red-temperature values and positive values with blue-temperature values, and you
;       would like the red-temperature values to be reversed in the color table (so dark
;       colors adjoin in the color table and indicate values near zero). You could do this:
;
;           CTLoad, 0
;           CTLoad, 3, /REVERSE, CLIP=[32,240], BOTTOM=1, NCOLORS=10
;           CTLoad, 1, CLIP=[64, 245], BOTTOM=11, NCOLORS=10
;           cgColorbar, NCOLORS=20, BOTTOM=1, DIV=10, RANGE=[-10,10]
;
;       Here is an example that shows the difference between LOADCT and CTLOAD:
;
;           ERASE, COLOR=cgCOLOR('Charcoal)
;           LoadCT, 5, NCOLORS=8
;           cgColorbar, NCOLORS=8, DIVISIONS=8, POSITION=[0.1, 0.65, 0.9, 0.75], XMINOR=0, XTICKLEN=1
;           CTLoad, 5, NCOLORS=8, CLIP=[16, 240]
;           cgColorbar, NCOLORS=8, DIVISIONS=8, POSITION=[0.1, 0.35, 0.9, 0.45], XMINOR=0, XTICKLEN=1
;
; MODIFICATION HISTORY:
;
;       Written by David W. Fanning, 30 October 2007.
;       Added ability to read Brewer Color Table file, if available, with BREWER keyword. 14 May 2008. DWF.
;       Small change in the way the program looks for the Brewer file. 8 July 2008. DWF.
;       Changed the way the program looks for the Brewer color table file. Now use
;          the Coyote Library routine FIND_RESOURCE_FILE to look for the file. 29 June 2010. DWF.
;       Renamed Colorbar procedure to cgColorbar to avoid conflict with IDL 8 Colorbar function.
;          26 September 2010. DWF.
;       Added ROW keyword to transpose color table vectors for new graphics functions
;          in IDL 8. 23 Nov 2010. DWF.
;       Added WINDOW and WINID keywords. 26 January 2011. DWF.
;       Added ADDCMD keyword. 29 Jan 2011. DWF.
;       Program delevopment ended and code transferred to cgLoadCT as of 4 Feb 2011. DWF.
;-
;******************************************************************************************;
;  Copyright (c) 2008, by Fanning Software Consulting, Inc.                                ;
;  All rights reserved.                                                                    ;
;                                                                                          ;
;  Redistribution and use in source and binary forms, with or without                      ;
;  modification, are permitted provided that the following conditions are met:             ;
;                                                                                          ;
;      * Redistributions of source code must retain the above copyright                    ;
;        notice, this list of conditions and the following disclaimer.                     ;
;      * Redistributions in binary form must reproduce the above copyright                 ;
;        notice, this list of conditions and the following disclaimer in the               ;
;        documentation and/or other materials provided with the distribution.              ;
;      * Neither the name of Fanning Software Consulting, Inc. nor the names of its        ;
;        contributors may be used to endorse or promote products derived from this         ;
;        software without specific prior written permission.                               ;
;                                                                                          ;
;  THIS SOFTWARE IS PROVIDED BY FANNING SOFTWARE CONSULTING, INC. ''AS IS'' AND ANY        ;
;  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES    ;
;  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT     ;
;  SHALL FANNING SOFTWARE CONSULTING, INC. BE LIABLE FOR ANY DIRECT, INDIRECT,             ;
;  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED    ;
;  TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;         ;
;  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND             ;
;  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT              ;
;  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS           ;
;  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                            ;
;******************************************************************************************;
PRO CTLOAD, table, $
   BREWER=brewer, $
   BOTTOM=bottom, $
   CLIP = clip, $
   RGB_TABLE=color_table, $
   FILE=file, $
   GET_NAMES=get_names, $
   NCOLORS=ncolors, $
   REVERSE=reverse, $
   ROW=row, $
   SILENT=silent, $
   WINDOW=window, $
   WINID=winID

   COMMON colors, r_orig, g_orig, b_orig, r_curr, g_curr, b_curr
   Compile_Opt idl2

   ; Error handling.
   Catch, theError
   IF theError NE 0 THEN BEGIN
      Catch, /CANCEL
      Help, LAST_MESSAGE=1, OUTPUT=traceback
      Help, Calls=callStack
      callingRoutine = (StrSplit(StrCompress(callStack[1])," ", /Extract))[0]
      Print,''
      Print, 'Traceback Report from ' + StrUpCase(callingRoutine) + ':'
      Print, ''
      FOR j=0,N_Elements(traceback)-1 DO Print, "     " + traceback[j]
      void = Dialog_Message(traceback[0], /Error, TITLE='Trapped Error')
      IF N_Elements(lun) NE 0 THEN Free_Lun, lun
      RETURN
   ENDIF

    ; Are you adding this command to an cgWindow command list?
    ; Should this be added to a resizeable graphics window?
    IF Keyword_Set(addcmd) AND ((!D.Flags AND 256) NE 0) THEN BEGIN

        windowIDs = cgQuery(COUNT=wincnt)
        IF N_Elements(winid) NE 0 THEN BEGIN
            IF (wincnt GT 0) THEN BEGIN
                index = Where(windowIDs EQ winID)
                IF index[0] NE -1 THEN cgSet, winid
            ENDIF
        ENDIF
        IF wincnt EQ 0 THEN cgWindow
        cgWindow, 'CTLoad', table, $
           BREWER=brewer, $
           BOTTOM=bottom, $
           CLIP = clip, $
           RGB_TABLE=color_table, $
           FILE=file, $
           GET_NAMES=get_names, $
           NCOLORS=ncolors, $
           REVERSE=reverse, $
           ROW=row, $
           SILENT=silent, $
           WINID=winID
           ADDCMD=1
         RETURN
    ENDIF

   ; Check keywords and arguments.
   IF N_Elements(table) EQ 0 THEN table = 0
   IF N_Elements(bottom) EQ 0 THEN bottom = 0 ELSE bottom = 0 > bottom < (!D.TABLE_SIZE-1)
   IF N_Elements(clip) EQ 0 THEN clip = [0,255]
   IF N_Elements(clip) EQ 1 THEN clip = [clip, 255]
   clip = 0 > clip < 255
   IF N_Elements(file) EQ 0 THEN file = Filepath('colors1.tbl', SUBDIRECTORY=['resource', 'colors'])

   ; Try to locate the brewer file.
   IF Keyword_Set(brewer) THEN BEGIN
       brewerfile = Find_Resource_File('fsc_brewer.tbl')
       IF brewerfile EQ "" THEN BEGIN
            Message, 'Cannot find the Brewer color table file "fsc_brewer.tbl."' + $
                     ' Using normal IDL color tables.', /INFORMATIONAL
       ENDIF ELSE file = brewerfile
   ENDIF

   ; Be sure !D.TABLE_SIZE is established.
   IF (!D.NAME EQ 'X') AND (!D.WINDOW EQ -1) THEN BEGIN
      Window, /Free, /Pixmap, XSIZE=10, YSIZE=10
      WDelete, !D.WINDOW
   ENDIF

   IF N_Elements(ncolors) EQ 0 THEN ncolors = !D.TABLE_SIZE
   reverse = KEYWORD_SET(reverse)

   ; Open and read the color table files.
   OPENR, lun, file, /GET_LUN
   ntables = 0B
   READU, lun, ntables

   ; Make sure table number is within range.
   IF (table GE ntables) OR (table LT 0) THEN $
      Message, 'Table number must be from 0 to ' + StrTrim(Fix(ntables)-1,2) + '.'

   ; Read the table names, if required, and return.
   IF Arg_Present(get_names) THEN BEGIN
      get_names = BytArr(32, ntables)
      Point_LUN, lun, ntables * 768L + 1
      READU, lun, get_names
      FREE_LUN, LUN
      get_names = StrTrim(get_names, 2)
      RETURN
   ENDIF

   ; Read the color table.
   theTables = Assoc(lun, BytArr(256), 1)
   r = theTables[table*3]
   g = theTables[table*3+1]
   b = theTables[table*3+2]

   ; Close the file.
   FREE_LUN, lun

   ; Clip the colors.
   r = r[clip[0]:clip[1]]
   g = g[clip[0]:clip[1]]
   b = b[clip[0]:clip[1]]
   nclipcolors = (clip[1]-clip[0]) + 1

   ; Interpolate to the number of colors asked for.
   IF ncolors NE nclipcolors THEN BEGIN
      p = (Lindgen(ncolors) * nclipcolors) / (ncolors-1)
      r = r[p]
      g = g[p]
      b = b[p]
   ENDIF

  ; Need to reverse the colors?
  IF reverse THEN BEGIN
     r = Reverse(r)
     g = Reverse(g)
     b = Reverse(b)
  ENDIF

  ; Load a color_table, if needed. Otherwise, load color vectors.
  IF Arg_Present(color_table) THEN BEGIN
     color_table = [[r], [g], [b]]
     IF Keyword_Set(row) THEN color_table = Transpose(color_table)
  ENDIF ELSE BEGIN
     r_orig = BYTSCL(Indgen(!D.TABLE_SIZE))
     g_orig = r_orig
     b_orig = r_orig
     r_orig[bottom] = r
     g_orig[bottom] = g
     b_orig[bottom] = b
     r_curr = r_orig
     g_curr = g_orig
     b_curr = b_orig
     TVLCT, r, g, b, bottom
  ENDELSE

  ; If the WINDOW keyword is set, send these colors to an cgWindow object.
  IF Keyword_Set(window) THEN BEGIN

      ; Does a window object exist somewhere?
      DefSysV, '!FSC_WINDOW_LIST', EXISTS=exists
      IF exists THEN BEGIN
           theList = !FSC_WINDOW_LIST
           IF Obj_Valid(theList) THEN BEGIN
                structs = theList -> Get_Item(/ALL, /DEREFERENCE)
                IF Size(structs, /TNAME) EQ 'POINTER' THEN RETURN
                IF N_Elements(winID) EQ 0 THEN BEGIN
                    winID = N_Elements(structs) - 1
                ENDIF ELSE BEGIN
                    index = Where(structs.wid[*] EQ winID, count)
                    IF count GT 0 THEN winID = index[0] ELSE BEGIN
                        Message, 'Cannot find an cgWindow with window index ' + StrTrim(winID, 2) + '.'
                    ENDELSE
                ENDELSE
                thisWindowStruct = structs[winID]
                IF Obj_Valid(thisWindowStruct.windowObj) THEN BEGIN
                    thisWindowStruct.windowObj -> LoadColors, r, g, b
                ENDIF
                RETURN
           ENDIF
       ENDIF
  ENDIF
END

;+
; NAME:
;   COLORBAR
;
; PURPOSE:
;
;       The purpose of this routine is to add a color bar to the current
;       graphics window.
;
; AUTHOR:
;
;   FANNING SOFTWARE CONSULTING
;   David Fanning, Ph.D.
;   1645 Sheely Drive
;   Fort Collins, CO 80526 USA
;   Phone: 970-221-0438
;   E-mail: david@idlcoyote.com
;   Coyote's Guide to IDL Programming: http://www.idlcoyote.com/
;
; CATEGORY:
;
;       Graphics, Widgets.
;
; CALLING SEQUENCE:
;
;       COLORBAR
;
; INPUTS:
;
;       None.
;
; KEYWORD PARAMETERS:
;
;       ANNOTATECOLOR: The name of the "annotation color" to use. The names are those for
;                     FSC_COLOR, and using the keyword implies that FSC_COLOR is also in
;                     your !PATH. If this keyword is used, the annotation color is loaded
;                     *after* the color bar is displayed. The color will be represented
;                     as theColor = FSC_COLOR(ANNOTATECOLOR, COLOR). This keyword is provide
;                     to maintain backward compatibility, but also to solve the problem of
;                     and extra line in the color bar when this kind of syntax is used in
;                     conjunction with the indexed (DEVICE, DECOMPOSED=0) model is used:
;
;                          LoadCT, 33
;                          TVImage, image
;                          Colorbar, Color=FSC_Color('firebrick')
;
;                     The proper syntax for device-independent color is like this:
;
;                          LoadCT, 33
;                          TVImage, image
;                          Colorbar, AnnotateColor='firebrick', Color=255
;
;       BOTTOM:       The lowest color index of the colors to be loaded in
;                     the bar.
;
;       CHARSIZE:     The character size of the color bar annotations. Default is !P.Charsize.
;
;       COLOR:        The color index of the bar outline and characters. Default
;                     is !P.Color..
;
;       DIVISIONS:    The number of divisions to divide the bar into. There will
;                     be (divisions + 1) annotations. The default is 6.
;
;       FONT:         Sets the font of the annotation. Hershey: -1, Hardware:0, True-Type: 1.
;
;       FORMAT:       The format of the bar annotations. Default is '(I0)'.
;
;       INVERTCOLORS: Setting this keyword inverts the colors in the color bar.
;
;       MAXRANGE:     The maximum data value for the bar annotation. Default is
;                     NCOLORS.
;
;       MINRANGE:     The minimum data value for the bar annotation. Default is 0.
;
;       MINOR:        The number of minor tick divisions. Default is 2.
;
;       NCOLORS:      This is the number of colors in the color bar.
;
;       NODISPLAY:    COLORBAR uses FSC_COLOR to specify some of it colors. Normally,
;                     FSC_COLOR loads "system" colors as part of its palette of colors.
;                     In order to do so, it has to create an IDL widget, which in turn
;                     has to make a connection to the windowing system. If your program
;                     is being run without a window connection, then this program will
;                     fail. If you can live without the system colors (and most people
;                     don't even know they are there, to tell you the truth), then setting
;                     this keyword will keep them from being loaded, and you can run
;                     COLORBAR without a display.
;
;       POSITION:     A four-element array of normalized coordinates in the same
;                     form as the POSITION keyword on a plot. Default is
;                     [0.88, 0.10, 0.95, 0.90] for a vertical bar and
;                     [0.10, 0.88, 0.90, 0.95] for a horizontal bar.
;
;       RANGE:        A two-element vector of the form [min, max]. Provides an
;                     alternative way of setting the MINRANGE and MAXRANGE keywords.
;
;       REVERSE:      Setting this keyword reverses the colors in the colorbar.
;
;       RIGHT:        This puts the labels on the right-hand side of a vertical
;                     color bar. It applies only to vertical color bars.
;
;       TICKNAMES:    A string array of names or values for the tick marks.
;
;       TITLE:        This is title for the color bar. The default is to have
;                     no title.
;
;       TOP:          This puts the labels on top of the bar rather than under it.
;                     The keyword only applies if a horizontal color bar is rendered.
;
;       VERTICAL:     Setting this keyword give a vertical color bar. The default
;                     is a horizontal color bar.
;
; COMMON BLOCKS:
;
;       None.
;
; SIDE EFFECTS:
;
;       Color bar is drawn in the current graphics window.
;
; RESTRICTIONS:
;
;       The number of colors available on the graphics display device (not the
;       PostScript device) is used unless the NCOLORS keyword is used.
;
;       Requires the FSC_COLOR program from the Coyote Library:
;
;          http://www.idlcoyote.com/programs/fsc_color.pro
;
; EXAMPLE:
;
;       To display a horizontal color bar above a contour plot, type:
;
;       LOADCT, 5, NCOLORS=100
;       CONTOUR, DIST(31,41), POSITION=[0.15, 0.15, 0.95, 0.75], $
;          C_COLORS=INDGEN(25)*4, NLEVELS=25
;       COLORBAR, NCOLORS=100, POSITION=[0.15, 0.85, 0.95, 0.90]
;
; MODIFICATION HISTORY:
;
;       Written by: David W. Fanning, 10 JUNE 96.
;       10/27/96: Added the ability to send output to PostScript. DWF
;       11/4/96: Substantially rewritten to go to screen or PostScript
;           file without having to know much about the PostScript device
;           or even what the current graphics device is. DWF
;       1/27/97: Added the RIGHT and TOP keywords. Also modified the
;            way the TITLE keyword works. DWF
;       7/15/97: Fixed a problem some machines have with plots that have
;            no valid data range in them. DWF
;       12/5/98: Fixed a problem in how the colorbar image is created that
;            seemed to tickle a bug in some versions of IDL. DWF.
;       1/12/99: Fixed a problem caused by RSI fixing a bug in IDL 5.2. Sigh... DWF.
;       3/30/99: Modified a few of the defaults. DWF.
;       3/30/99: Used NORMAL rather than DEVICE coords for positioning bar. DWF.
;       3/30/99: Added the RANGE keyword. DWF.
;       3/30/99: Added FONT keyword. DWF
;       5/6/99: Many modifications to defaults. DWF.
;       5/6/99: Removed PSCOLOR keyword. DWF.
;       5/6/99: Improved error handling on position coordinates. DWF.
;       5/6/99. Added MINOR keyword. DWF.
;       5/6/99: Set Device, Decomposed=0 if necessary. DWF.
;       2/9/99: Fixed a problem caused by setting BOTTOM keyword, but not NCOLORS. DWF.
;       8/17/99. Fixed a problem with ambiguous MIN and MINOR keywords. DWF
;       8/25/99. I think I *finally* got the BOTTOM/NCOLORS thing sorted out. :-( DWF.
;       10/10/99. Modified the program so that current plot and map coordinates are
;            saved and restored after the colorbar is drawn. DWF.
;       3/18/00. Moved a block of code to prevent a problem with color decomposition. DWF.
;       4/28/00. Made !P.Font default value for FONT keyword. DWF.
;       9/26/00. Made the code more general for scalable pixel devices. DWF.
;       1/16/01. Added INVERTCOLORS keyword. DWF.
;       5/11/04. Added TICKNAME keyword. DWF.
;       9/29/05. Added REVERSE keywords, which does the *exact* same thing as
;           INVERTCOLORS, but I can never remember the latter keyword name. DWF.
;       1/2/07. Added ANNOTATECOLOR keyword. DWF.
;       4/14/07. Changed the default FORMAT to I0. DWF.
;       5/1/07. Unexpected consequence of default format change is colorbar annotations
;           no longer match contour plot levels. Changed to explicit formating of
;           colorbar axis labels before PLOT command. DWF.
;       5/25/07. Previous change has unanticipated effect on color bars using
;           logarithmic scaling, which is not really supported, but I have an
;           article on my web page describing how to do it: http://www.idlcoyote.com/graphics_tips/logcb.html.
;           Thus, I've fixed the program to accommodate log scaling, while still not OFFICIALLY
;           supporting it. DWF.
;       10/3/07. Method used to calculate TICKNAMES produces incorrect values in certain cases when
;           the min and max range values are integers. Now force range values to be floats. DWF.
;       10/17/07. Accidentaly use of INTERP keyword in CONGRID results in wrong bar values for
;           low NCOLORS numbers when INVERTCOLORS or REVERSE keyword is used. Removed INTERP keyword. DWF.
;       11/10/07. Finished fixing program to accommodate log scaling in ALL possible permutations. DWF.
;       8 Feb 2008. Added CRONJOB keyword and decided to use month names when I write the date. DWF.
;       8 Feb 2008. Renamed CRONJOB to NODISPLAY to better reflect its purpose. DWF.
;      21 May 2008. Changed the default CHARSIZE to !P.CHARSIZE from 1.0. DWF.
;      30 Oct 2008. Fixed a problem with the FONT keyword not being recognized in certain
;            configurations.
;-     9 Nov 2009. Fixed typo in title of vertical colorbar. DWF.
;******************************************************************************************;
;  Copyright (c) 2008-2009, by Fanning Software Consulting, Inc.                           ;
;  All rights reserved.                                                                    ;
;                                                                                          ;
;  Redistribution and use in source and binary forms, with or without                      ;
;  modification, are permitted provided that the following conditions are met:             ;
;                                                                                          ;
;      * Redistributions of source code must retain the above copyright                    ;
;        notice, this list of conditions and the following disclaimer.                     ;
;      * Redistributions in binary form must reproduce the above copyright                 ;
;        notice, this list of conditions and the following disclaimer in the               ;
;        documentation and/or other materials provided with the distribution.              ;
;      * Neither the name of Fanning Software Consulting, Inc. nor the names of its        ;
;        contributors may be used to endorse or promote products derived from this         ;
;        software without specific prior written permission.                               ;
;                                                                                          ;
;  THIS SOFTWARE IS PROVIDED BY FANNING SOFTWARE CONSULTING, INC. ''AS IS'' AND ANY        ;
;  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES    ;
;  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT     ;
;  SHALL FANNING SOFTWARE CONSULTING, INC. BE LIABLE FOR ANY DIRECT, INDIRECT,             ;
;  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED    ;
;  TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;         ;
;  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND             ;
;  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT              ;
;  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS           ;
;  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                            ;
;******************************************************************************************;
PRO COLORBAR, BOTTOM=bottom, CHARSIZE=charsize, COLOR=color, DIVISIONS=divisions, $
  FORMAT=format, POSITION=position, MAXRANGE=maxrange, MINRANGE=minrange, NCOLORS=ncolors, $
  TITLE=title, VERTICAL=vertical, TOP=top, RIGHT=right, MINOR=minor, $
  RANGE=range, FONT=font, TICKLEN=ticklen, _EXTRA=extra, INVERTCOLORS=invertcolors, $
  TICKNAMES=ticknames, REVERSE=reverse, ANNOTATECOLOR=annotatecolor, XLOG=xlog, YLOG=ylog, $
  NODISPLAY=nodisplay

  compile_opt idl2

  ; Return to caller on error.
  On_Error, 2

  ; Save the current plot state.
  bang_p = !P
  bang_x = !X
  bang_Y = !Y
  bang_Z = !Z
  bang_Map = !Map

  ; Are scalable pixels available on the device?
  IF (!D.Flags AND 1) NE 0 THEN scalablePixels = 1 ELSE scalablePixels = 0

  ; Which release of IDL is this?
  thisRelease = Float(!Version.Release)

  ; Check and define keywords.
  IF N_ELEMENTS(ncolors) EQ 0 THEN BEGIN

    ; Most display devices to not use the 256 colors available to
    ; the PostScript device. This presents a problem when writing
    ; general-purpose programs that can be output to the display or
    ; to the PostScript device. This problem is especially bothersome
    ; if you don't specify the number of colors you are using in the
    ; program. One way to work around this problem is to make the
    ; default number of colors the same for the display device and for
    ; the PostScript device. Then, the colors you see in PostScript are
    ; identical to the colors you see on your display. Here is one way to
    ; do it.

    IF scalablePixels THEN BEGIN
      oldDevice = !D.NAME

      ; What kind of computer are we using? SET_PLOT to appropriate
      ; display device.

      thisOS = !VERSION.OS_FAMILY
      thisOS = STRMID(thisOS, 0, 3)
      thisOS = STRUPCASE(thisOS)
      CASE thisOS of
        'MAC': SET_PLOT, thisOS
        'WIN': SET_PLOT, thisOS
        ELSE: SET_PLOT, 'X'
      ENDCASE

      ; Here is how many colors we should use.
      ncolors = !D.TABLE_SIZE
      SET_PLOT, oldDevice
    ENDIF ELSE ncolors = !D.TABLE_SIZE
  ENDIF
  IF N_ELEMENTS(bottom) EQ 0 THEN bottom = 0B
  IF N_ELEMENTS(charsize) EQ 0 THEN charsize = !P.Charsize
  IF N_ELEMENTS(format) EQ 0 THEN format = '(I0)'
  IF N_ELEMENTS(color) EQ 0 THEN color = !P.Color
  minrange = (N_ELEMENTS(minrange) EQ 0) ? 0. : Float(minrange)
  maxrange = (N_ELEMENTS(maxrange) EQ 0) ? Float(ncolors) : Float(maxrange)
  IF N_ELEMENTS(ticklen) EQ 0 THEN ticklen = 0.2
  IF N_ELEMENTS(minor) EQ 0 THEN minor = 2
  IF N_ELEMENTS(range) NE 0 THEN BEGIN
    minrange = Float(range[0])
    maxrange = Float(range[1])
  ENDIF
  IF N_ELEMENTS(divisions) EQ 0 THEN divisions = 6
  IF N_ELEMENTS(font) EQ 0 THEN font = !P.Font
  IF N_ELEMENTS(title) EQ 0 THEN title = ''
  xlog = Keyword_Set(xlog)
  ylog = Keyword_Set(ylog)

  ; You can't have a format set *and* use ticknames.
  IF N_ELEMENTS(ticknames) NE 0 THEN format = ""

  ; If the format is NOT null, then format the ticknames yourself.
  ; Can't assume minrange is less than maxrange.
  IF (xlog XOR ylog) EQ 0 THEN BEGIN
    IF format NE "" THEN BEGIN
      IF minrange LT maxrange THEN BEGIN
        step = (maxrange - minrange) / divisions
        levels = minrange > (Indgen(divisions+1) * step + minrange) < maxrange
        IF StrPos(StrLowCase(format), 'i') NE -1 THEN levels = Round(levels)
        ticknames = String(levels, Format=format)
        format = "" ; No formats allowed in PLOT call now that we have ticknames.
      ENDIF ELSE BEGIN
        step = (minrange - maxrange) / divisions
        levels = maxrange > (Indgen(divisions+1) * step + maxrange) < minrange
        levels = Reverse(levels)
        IF StrPos(StrLowCase(format), 'i') NE -1 THEN levels = Round(levels)
        ticknames = String(levels, Format=format)
        format = "" ; No formats allowed in PLOT call now that we have ticknames.
      ENDELSE
    ENDIF
  ENDIF

  IF KEYWORD_SET(vertical) THEN BEGIN
    bar = REPLICATE(1B,20) # BINDGEN(ncolors)
    IF Keyword_Set(invertcolors) THEN bar = Reverse(bar, 2)
    IF N_ELEMENTS(position) EQ 0 THEN BEGIN
      position = [0.88, 0.1, 0.95, 0.9]
    ENDIF ELSE BEGIN
      IF position[2]-position[0] GT position[3]-position[1] THEN BEGIN
        position = [position[1], position[0], position[3], position[2]]
      ENDIF
      IF position[0] GE position[2] THEN Message, "Position coordinates can't be reconciled."
      IF position[1] GE position[3] THEN Message, "Position coordinates can't be reconciled."
    ENDELSE
  ENDIF ELSE BEGIN
    bar = BINDGEN(ncolors) # REPLICATE(1B, 20)
    IF Keyword_Set(invertcolors) THEN bar = Reverse(bar, 1)
    IF N_ELEMENTS(position) EQ 0 THEN BEGIN
      position = [0.1, 0.88, 0.9, 0.95]
    ENDIF ELSE BEGIN
      IF position[3]-position[1] GT position[2]-position[0] THEN BEGIN
        position = [position[1], position[0], position[3], position[2]]
      ENDIF
      IF position[0] GE position[2] THEN Message, "Position coordinates can't be reconciled."
      IF position[1] GE position[3] THEN Message, "Position coordinates can't be reconciled."
    ENDELSE
  ENDELSE

  ; Scale the color bar.
  bar = BYTSCL(bar, TOP=(ncolors-1) < (255-bottom)) + bottom

  IF Keyword_Set(reverse) THEN BEGIN
    IF Keyword_Set(vertical) THEN bar = Reverse(bar,2) ELSE bar = Reverse(bar,1)
  ENDIF

  ; Get starting locations in NORMAL coordinates.
  xstart = position[0]
  ystart = position[1]

  ; Get the size of the bar in NORMAL coordinates.
  xsize = (position[2] - position[0])
  ysize = (position[3] - position[1])

  ; Display the color bar in the window. Sizing is
  ; different for PostScript and regular display.
  IF scalablePixels THEN BEGIN

    TV, bar, xstart, ystart, XSIZE=xsize, YSIZE=ysize, /Normal

  ENDIF ELSE BEGIN

    bar = CONGRID(bar, CEIL(xsize*!D.X_VSize), CEIL(ysize*!D.Y_VSize))

    ; Decomposed color off if device supports it.
    CASE  StrUpCase(!D.NAME) OF
      'X': BEGIN
        IF thisRelease GE 5.2 THEN Device, Get_Decomposed=thisDecomposed
        Device, Decomposed=0
      ENDCASE
      'WIN': BEGIN
        IF thisRelease GE 5.2 THEN Device, Get_Decomposed=thisDecomposed
        Device, Decomposed=0
      ENDCASE
      'MAC': BEGIN
        IF thisRelease GE 5.2 THEN Device, Get_Decomposed=thisDecomposed
        Device, Decomposed=0
      ENDCASE
      ELSE:
    ENDCASE

    TV, bar, xstart, ystart, /Normal

    ; Restore Decomposed state if necessary.
    CASE StrUpCase(!D.NAME) OF
      'X': BEGIN
        IF thisRelease GE 5.2 THEN Device, Decomposed=thisDecomposed
      ENDCASE
      'WIN': BEGIN
        IF thisRelease GE 5.2 THEN Device, Decomposed=thisDecomposed
      ENDCASE
      'MAC': BEGIN
        IF thisRelease GE 5.2 THEN Device, Decomposed=thisDecomposed
      ENDCASE
      ELSE:
    ENDCASE

  ENDELSE

  ; Annotate the color bar.
  IF N_Elements(annotateColor) NE 0 THEN $
    color = FSC_Color(annotateColor, color, NODISPLAY=Keyword_Set(nodisplay))

  IF KEYWORD_SET(vertical) THEN BEGIN

    IF KEYWORD_SET(right) THEN BEGIN

      PLOT, [minrange,maxrange], [minrange,maxrange], /NODATA, XTICKS=1, $
        YTICKS=divisions, XSTYLE=1, YSTYLE=9, $
        POSITION=position, COLOR=color, CHARSIZE=charsize, /NOERASE, $
        XTICKFORMAT='(A1)', YTICKFORMAT='(A1)', YMINOR=minor, _EXTRA=extra, $
        YTICKNAME=ticknames, FONT=font, YLOG=ylog

      AXIS, YAXIS=1, YRANGE=[minrange, maxrange], YTICKFORMAT=format, YTICKS=divisions, $
        YTICKLEN=ticklen, YSTYLE=1, COLOR=color, CHARSIZE=charsize, $
        FONT=font, YTITLE=title, _EXTRA=extra, YMINOR=minor, YTICKNAME=ticknames, YLOG=ylog

    ENDIF ELSE BEGIN

      PLOT, [minrange,maxrange], [minrange,maxrange], /NODATA, XTICKS=1,  $
        YTICKS=divisions, YSTYLE=1, XSTYLE=1, YTITLE=title, $
        POSITION=position, COLOR=color, CHARSIZE=charsize, /NOERASE, $
        XTICKFORMAT='(A1)', YTICKFORMAT=format, YMinor=minor, _EXTRA=extra, $
        YTICKNAME=ticknames, YLOG=ylog, YTICKLEN=ticklen, FONT=font

    ENDELSE

  ENDIF ELSE BEGIN

    IF KEYWORD_SET(top) THEN BEGIN

      PLOT, [minrange,maxrange], [minrange,maxrange], /NODATA, XTICKS=divisions, $
        YTICKS=1, XSTYLE=9, YSTYLE=1, $
        POSITION=position, COLOR=color, CHARSIZE=charsize, /NOERASE, $
        YTICKFORMAT='(A1)', XTICKFORMAT='(A1)', XTICKLEN=ticklen, $
        XRANGE=[minrange, maxrange], FONT=font, XMINOR=minor,_EXTRA=extra, $
        XTICKNAME=ticknames, XLOG=xlog

      AXIS, XTICKS=divisions, XSTYLE=1, COLOR=color, CHARSIZE=charsize, $
        XTICKFORMAT=format, XTICKLEN=ticklen, XRANGE=[minrange, maxrange], XAXIS=1, $
        FONT=font, XTITLE=title, _EXTRA=extra, XCHARSIZE=charsize, XMINOR=minor, $
        XTICKNAME=ticknames, XLOG=xlog

    ENDIF ELSE BEGIN

      PLOT, [minrange,maxrange], [minrange,maxrange], /NODATA, XTICKS=divisions, $
        YTICKS=1, XSTYLE=1, YSTYLE=1, TITLE=title, $
        POSITION=position, COLOR=color, CHARSIZE=charsize, /NOERASE, $
        YTICKFORMAT='(A1)', XTICKFORMAT=format, XTICKLEN=ticklen, $
        XRANGE=[minrange, maxrange], FONT=font, XMinor=minor, _EXTRA=extra, $
        XTICKNAME=ticknames, XLOG=xlog

    ENDELSE

  ENDELSE

  ; Restore the previous plot and map system variables.
  !P = bang_p
  !X = bang_x
  !Y = bang_y
  !Z = bang_z
  !Map = bang_map

END








