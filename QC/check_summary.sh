#!/bin/bash 

if [ $# -ne 2 ]; then
    echo "USAGE: sh check_summary.sh checkfile1 checkfile2"
    exit 0
fi

#echo -e "Sample\tLength\tReads\tBases\tGC(%)\tQ20(%)\tQ30(%)"

read readsNum bases length <<< `sed -n '1p' $1 | awk -F '[ ,: ]' '{print $11,$14,$20}'`
read gc1 q201 q301<<< `sed -n '$p' $1 | cut -f 2,3,4`
read gc2 q202 q302<<< `sed -n '$p' $2 | cut -f 2,3,4`
GC=`echo "scale=2;($gc1 + $gc2)/2" | bc`
Q20=`echo "scale=2; ($q201 + $q202)/2" | bc`
Q30=`echo "scale=2; ($q301 + $q302)/2" | bc`
Bases=`echo "$bases * 2" | bc`
Reads=`echo "$readsNum * 2" | bc`
echo -e "${1%_*}\t$length\t$Reads\t$Bases\t$GC\t$Q20\t$Q30"



