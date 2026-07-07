# Script “getmisr.ksh”
#!/bin/ksh
# NASA LARC FTP repository for annual-average aerosol retrievals
#ftp=ftp://l5ftl01.larc.nasa.gov/misrl2l3/MISR/MIL3YAEN.004
ftp=https://opendap.larc.nasa.gov/opendap/MISR/MIL3YAEN.004/

# Download data
y=2000
while [ $y -le 2019 ];do
    let y1=$y+1 # in file name year plus one
    f=MISR_AM1_CGAS_${y1}_F15_0032.nc
    echo $y $f
    #wget $ftp/$y.12.01/$f
    ncatted -agrid_mapping,,d,, $f
    /opt/nco/bin/ncks -3 -O -g Aerosol_Parameter_Average -v Aerosol_Optical_Depth,Small_Mode_Aerosol_Optical_Depth -dOptical_Depth_Range,0 $f 1.nc
    ncwa -O -a Optical_Depth_Range 1.nc misr_$y1.nc
    \rm 1.nc
    let y=$y+1
done

ncecat -O misr_20??.nc misr_2000-2019.nc
