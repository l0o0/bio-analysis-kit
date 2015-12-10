#!/bin/bash 

if [ $# -ne 2 ]; then
    echo "USAGE: sh check_summary.sh checkfile"
    exit 0
fi


read bases length <<< `sed -n '1p' $1 | awk -F '[ ,: ]' '{print $14,$20}'`
read qc1 q201 <<< `sed -n '$p' $1 | cut -f 2,3`
read qc2 q202 <<< `sed -n '$p' $2 | cut -f 2,3`
QC=`echo "scale=2;($qc1 + $qc2)/2" | bc`
Q20=`echo "scale=2; ($q201 + $q202)/2" | bc`
echo -e "${1%_*}\t$length\t$bases\t$Q20\t$QC"



