function decadal_averages,inarr,inyears,decade_starts,decade_ends

  n = n_elements(decade_starts)
  outarr = fltarr(n)
  for i = 0, n-1 do begin
     index = where(inyears ge decade_starts[i] and inyears le decade_ends[i])
     outarr[i] = avg(inarr[index])
  endfor

  return, outarr

end

waveon

final_year = 2020

data = read_csv('GMST_IPCC_Feb_2021.csv')

years = data.field1
ncdc = data.field3
;had = data.field2
cw = data.field5
berk = data.field4
kadow = data.field6
vaccaro = data.field7



ind = where(years mod 10 eq 1)
decade_starts = years[ind]
decade_ends = decade_starts + 9
ndecades = n_elements(decade_starts)

had5ts = fltarr(171,200)
had5tsdec = fltarr(ndecades,200)
had5cov = fltarr(171)
y = findgen(171)+1850

haddir = '$HadCRUTDIR/'

for i = 1,200 do begin
   had5file = haddir+'/HadCRUT5/analysis/diagnostics/global/HadCRUT.5.0.1.0.analysis.anomalies.global.annual.'+nicenumber(i)+'.nc'

   handle = NCDF_OPEN(had5file,/NOWRITE)
   varid = NCDF_VARID(handle, 'tas')
   NCDF_VARGET, handle, Varid, had5ts_member
   NCDF_CLOSE,handle

   had5ts_member = had5ts_member - avg(had5ts_member[where(y ge 1850 and y le 1900)])

   had5ts[*,i-1] = had5ts_member[0:170]
   had5tsdec[*,i-1] = decadal_averages(had5ts_member[0:170], years, decade_starts, decade_ends)
endfor

had5covfile = haddir+'/HadCRUT5/analysis/diagnostics/global/HadCRUT.5.0.1.0.analysis.coverage.global.annual.nc'
handle = NCDF_OPEN(had5covfile,/NOWRITE)
varid = NCDF_VARID(handle, 'coverage_unc')
NCDF_VARGET, handle, Varid, had5ts_cov
NCDF_CLOSE,handle

had5ts_summary = fltarr(171, 3)
had5tsdec_summary = fltarr(ndecades, 3)

for i = 0,170 do begin

   had5ts_summary[i,0] = avg(had5ts[i,*])
   unc = 1.96 * sqrt(stdev(had5ts[i,*])^2 + had5ts_cov[i]^2)

   had5ts_summary[i,1] = had5ts_summary[i,0] - unc
   had5ts_summary[i,2] = had5ts_summary[i,0] + unc

endfor

for i = 0, ndecades-1 do begin

   ; use the coverage uncertainty from the first year of the decade
   covindex = where(years eq decade_starts[i])

   had5tsdec_summary[i,0] = avg(had5tsdec[i,*])
   unc = 1.96 * sqrt(stdev(had5tsdec[i,*])^2 + had5ts_cov[covindex]^2)

   had5tsdec_summary[i,1] = had5tsdec_summary[i,0] - unc
   had5tsdec_summary[i,2] = had5tsdec_summary[i,0] + unc

endfor

had5tslo = had5ts_summary[*,1]
had5tshi = had5ts_summary[*,2]
had5ts = had5ts_summary[*,0]

had5tsdeclo = had5tsdec_summary[*,1]
had5tsdechi = had5tsdec_summary[*,2]
had5tsdec = had5tsdec_summary[*,0]




pr,/ps,/color,/encapsulated,/land,file='Figure_1_IPCC_shared.eps'
!p.font=0
device,/helvetica
!x.thick=4
!y.thick=4
tek_color
!p.multi=[0,1,2,0,0]

lo = 0.075
hi = 0.88
delta = 0.02

set_viewport,0.12,0.95,delta + hi-(hi-lo)/2,hi


plot,years,had,xrange=[1845,final_year+4],xstyle=5,/nodata,charsize=1.5, xtitle='' $
  ,ytitle='!Eo!NC',yrange=[-0.5,1.35],ystyle=9,yminor=1,xminor=1,yticklen=0.005

xyouts,0.04,0.95,'Global Temperature anomalies (1850-'+nicenumber(final_year)+')',/normal,charsize=2.2
xyouts,0.04,0.91,'annual average and decadal averages relative to 1850-1900',/normal,charsize=1.5

;plot HadCRUT4 uncertainty range.
polyfill,[years,reverse(years)],[had5tshi,reverse(had5tslo)],color=200

;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
oplot,years,berk,color=13,thick=4,/noclip
oplot,years,kadow,thick=4,color=8,/noclip
oplot,years,ncdc,color=27,thick=4,/noclip
oplot,years,had5ts,color=0,thick=4,/noclip
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

csize=1.4
step=0.17
shift=0.44
xyouts,1850,shift+0.8,'HadCRUT.5.0',color=0,charsize=csize
xyouts,1850,shift+0.8-step,'Kadow et al.',color=8,charsize=csize
xyouts,1850,shift+0.8-2*step,'NOAAGlobalTemp',color=27,charsize=csize
xyouts,1850,shift+0.8-3*step,'Berkeley Earth',color=13,charsize=csize

;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@                           @@@@
;@@@   DECADAL PLOT            @@@@
;@@@                           @@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
set_viewport,0.12,0.95,lo,hi-(hi-lo)/2 - delta

plot,years,had,xrange=[1845,final_year+4],xstyle=9,/nodata,charsize=1.5, xtitle='' $
  ,ytitle='!Eo!NC',yrange=!y.crange,ystyle=9,yminor=1,xminor=1,yticklen=0.005

n_decades = floor(n_elements(years)/10)
ind = where(years mod 10 eq 1)
decade_starts = years[ind]
decade_ends = decade_starts + 9

f=read_ascii('hadcrut4_decadal_ns_avg_x1x0.txt')
anoms2 = f.field01(1:*,*) 
years2 = reform(f.field01(0,*),n_elements(f.field01(0,*)))
u = reform(anoms2(9,*),n_elements(anoms2(9,*)))
l = reform(anoms2(10,*),n_elements(anoms2(10,*)))
b = reform(anoms2(0,*),n_elements(anoms2(0,*)))
n_decades2  = n_elements(years2)



for i = 0,n_decades2-1 do begin
   ds = decade_starts[i]
   de = decade_ends[i]
   polyfill,[de, ds, ds, de],[had5tsdeclo[i],had5tsdeclo[i],had5tsdechi[i],had5tsdechi[i]],color=200
endfor

runberk = decadal_averages(berk, years, decade_starts, decade_ends)
runcw = decadal_averages(cw, years, decade_starts, decade_ends)
runncdc = decadal_averages(ncdc, years, decade_starts, decade_ends)
runkadow = decadal_averages(kadow, years, decade_starts, decade_ends)
runvaccaro = decadal_averages(vaccaro, years, decade_starts, decade_ends)
for i = 0,n_elements(runberk)-1 do begin
   print,decade_starts[i],decade_ends[i]

   plots,[decade_starts[i], decade_ends[i]],[runberk[i],runberk[i]],color=13,thick=4
   plots,[decade_starts[i], decade_ends[i]],[runncdc[i],runncdc[i]],color=27,thick=4
   plots,[decade_starts[i], decade_ends[i]],[runkadow[i],runkadow[i]],color=8,thick=4
endfor

for i = 0,n_decades2-1 do begin

   plots,[decade_starts[i], decade_ends[i]], [had5tsdec[i], had5tsdec[i]], thick=4

endfor

polyfill,[1849.8,1849.8,1845.951,1845.951],[-0.4,-0.5218,-0.5218,-0.4],color=255

prend,/keep,/view,/noprint


spawn,'convert -antialias -density 300 -flatten Figure_1_IPCC_shared.eps Figure_1_IPCC_shared.png'





end
