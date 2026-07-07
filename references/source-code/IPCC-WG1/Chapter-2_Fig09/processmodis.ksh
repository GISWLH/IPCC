# Script “processmodis.ksh”

#!/bin/ksh
d=/pool/data/ICDC/atmosphere/modis_terra_aerosol/DATA/
f0=MODIS-C6.1__MOD08__daily__aerosol-parameters__
f1=__UHAM-ICDC__fv0.2.nc

y=1999
let y1=$y+1
(cdo -O enspctl,50 $d/$y1/${f0}${y1}0???${f1} $d/$y1/${f0}${y1}1[0-1]??${f1}  $y.nc; cdo selvar,aod_landocean,aod550_ocean_fm_qa $y1.nc modis_$y1.nc; \rm $y1.nc)&
let y=$y+1

while [ $y -le 2002 ];do
    let y1=$y+1
    (cdo -O enspctl,50 $d/$y/${f0}${y}12??${f1} $d/$y1/${f0}${y1}0???${f1} $d/$y1/${f0}${y1}1[0-1]??${f1}  $y.nc; cdo selvar,aod_landocean,aod550_ocean_fm_qa $y1.nc modis_$y1.nc; \rm $y1.nc)&
    let y=$y+1
done

da=/pool/data/ICDC/atmosphere/modis_aqua_aerosol/DATA/
f0a=MODIS-C6.1__MYD08__daily__aerosol-parameters__

while [ $y -le 2018 ];do
    let y1=$y+1
    (cdo -O enspctl,50 $d/$y/${f0}${y}12??${f1} $d/$y1/${f0}${y1}0???${f1} $d/$y1/${f0}${y1}1[0-1]??${f1} $da/$y/${f0a}${y}12??${f1} $da/$y1/${f0a}${y1}0???${f1} $da/$y1/${f0a}${y1}1[0-1]??${f1}  $y.nc; cdo selvar,aod_landocean,aod550_ocean_fm_qa $y1.nc modis_$y1.nc; \rm $y1.nc)&
    let y=$y+1
done
