# Script “prepaeronet.ksh”
#!/bin/ksh
touch stations
for i in SDA/SDA20/MONTHLY/19930101_202*_lev20;do
    stat=`echo $i|sed -e 's/SDA\/SDA20\/MONTHLY\/19930101\_20190105\_//g'|sed -e 's/.ONEILL\_lev20//g'`
    y=`tail -1 $i |awk -F"," '{print $39}'`
    x=`tail -1 $i |awk -F"," '{print $40}'`
    nt=`wc -l $i|awk -F" " '{print $1}'`
    let nt=$nt-7
    echo $stat >> stations
    echo $nt > $stat
    echo $x >> $stat
    echo $y >> $stat
    cat $i|awk 'BEGIN { FS = "," } ; { printf "%12.6f%12.6f\n", $2, $3}' >> $stat
done
