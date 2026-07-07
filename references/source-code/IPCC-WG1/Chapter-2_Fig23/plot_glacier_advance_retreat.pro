PRO plot_glacier_advance_retreat

years=[0]
values=[-999]
read_in=INTARR(2)

OPENR,1,'2k_glacier_advances.prn'
  WHILE NOT EOF(1) DO BEGIN
    READF,1,read_in,FORMAT='(2(I10))'
    years=[years,read_in[0]]
    values=[values,read_in[1]]
  ENDWHILE
CLOSE,1

years=[years,2000]
values=[values,-999]

xtick_vals=[0,250,500,750,1000,1250,1500,1750,2000]
years_out=INDGEN(42)*50

SET_PLOT,'PS'
Device,file='/Users/pthorne/Desktop/glacier_series.ps',/color,/helvetica,/landscape
dummy=[0.]
PLOT,years,dummy,min_value=0.,xtickv=xtickvals,title='Number of glaciers advancing through the last 2 ka',$
  ytitle='Number of glaciers advancing',yrange=[0,130],xrange=[0,2000],xstyle=9,ystyle=9,thick=5
FOR y=0,39 DO BEGIN
  OPLOT,[years_out[y],years_out[y+1]],[values[y+1],values[y+1]],thick=5
  IF y NE 39 THEN OPLOT,[years_out[y+1],years_out[y+1]],[values[y+1],values[y+2]]
ENDFOR

DEVICE,/close_file
SET_PLOT,'X'

RETURN

END