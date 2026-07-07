# Script “tx2nc.ksh”

#!/bin/ksh
cat > su.txt <<EOF
netcdf rf {
dimensions:
        time = 27 ;
variables:
        float time(time) ;
                time:units = "year" ;
EOF
agents="europe russia arctic southamerica antarctica"
for i in $agents;do
    cat >> su.txt <<EOF
    	float ${i}(time) ;
	      ${i}:units = "ppb";
	      ${i}:missing_value = -999.f;
EOF
done
echo "data:" >> su.txt

line=`cat su.csv |awk 'BEGIN { FS = "," } ; { printf"%9.3f, ", $1 }'`
cat >> su.txt <<EOF
time = $line;
EOF
i=2
while [ $i -le 6 ];do
    line=`cat su.csv |awk -v i="$i" 'BEGIN { FS = "," } ; { printf"%9.3f, ", $i }'`
    let j=$i-1
    var=`echo $agents | awk -v j="$j" '{print $j}'`
    echo $var
    cat >> su.txt <<EOF
$var = $line;
EOF
    let i=$i+1
done
echo "}" >> su.txt

sed -e 's/\,\ \;/\;/g' su.txt > 1.txt
mv -f 1.txt su.txt
cat su.txt | ncgen -o su.nc


cat > bc.txt <<EOF
netcdf rf {
dimensions:
        time = 32 ;
variables:
        float time(time) ;
                time:units = "year" ;
EOF
agents="europe russia arctic southamerica southasia elbrus greenland antarctica"
for i in $agents;do
    cat >> bc.txt <<EOF
    	float ${i}(time) ;
	      ${i}:units = "ppb";
	      ${i}:missing_value = -999.f;
EOF
done
echo "data:" >> bc.txt

line=`cat bc.csv |awk 'BEGIN { FS = "," } ; { printf"%9.3f, ", $1 }'`
cat >> bc.txt <<EOF
time = $line;
EOF
i=2
while [ $i -le 9 ];do
    line=`cat bc.csv |awk -v i="$i" 'BEGIN { FS = "," } ; { printf"%9.3f, ", $i }'`
    let j=$i-1
    var=`echo $agents | awk -v j="$j" '{print $j}'`
    echo $var
    cat >> bc.txt <<EOF
$var = $line;
EOF
    let i=$i+1
done
echo "}" >> bc.txt

sed -e 's/\,\ \;/\;/g' bc.txt > 1.txt
mv -f 1.txt bc.txt
cat bc.txt | ncgen -o bc.nc
