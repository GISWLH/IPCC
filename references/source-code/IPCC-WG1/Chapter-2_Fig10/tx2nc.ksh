# Script “tx2nc.ksh”

#!/bin/ksh
cat > erf.txt <<EOF
netcdf rf {
dimensions:
        time = 271 ;
variables:
        float time(time) ;
                time:units = "year" ;
EOF
agents="CO2 CH4 N2O Halogens O3_Trop O3_Strat H2O_Strat Contrails ARI ACI BC_Snow LUC Volcano Solar Total_Anthropogenic Total_Natural Total"
for i in $agents;do
    cat >> erf.txt <<EOF
    	float ${i}(time) ;
	      ${i}:units = "W m-2";
	      ${i}:missing_values = -9999.f;
EOF
done
echo "data:" >> erf.txt

tail -272 table_A3.3_historical_ERF_1750-2019_best_estimate.csv > 1.csv
line=`cat 1.csv |awk 'BEGIN { FS = "," } ; { printf"%9.3f, ", $1 }'`
cat >> erf.txt <<EOF
time = $line;
EOF
i=2
while [ $i -le 18 ];do
    line=`cat 1.csv |awk -v i="$i" 'BEGIN { FS = "," } ; { printf"%9.3f, ", $i }'`
    let j=$i-1
    var=`echo $agents | awk -v j="$j" '{print $j}'`
    echo $var
    cat >> erf.txt <<EOF
$var = $line;
EOF
    let i=$i+1
done
echo "}" >> erf.txt

\rm 1.csv
sed -e 's/\,\ \;/\;/g' erf.txt > 1.txt
mv -f 1.txt erf.txt
cat erf.txt | ncgen -o erf.nc
