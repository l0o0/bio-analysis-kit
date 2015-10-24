#!/bin/bash
# created by linxzh, 2015-10-24
# script for sample raw data renaming, converting quality,filtering


#-----------------------------------------------------------------------
# $1 == index2sample.txt
# $2 == index of index
# $3 == raw data path 
# $4 == working dir 
# sh quality.sh index2sample.txt <index num> <rawdata path> <working dir>
#------------------------------------------------------------------------

#echo $1,$2,$3,$4

if [ $# -lt 4 ]; then
    echo "sh quality.sh index2sample.txt <index num> <rawdata path> <working dir>"
    exit 0 
fi

mkdir $4/ph64
mkdir $4/filter

declare -A index2sample
declare -A old2new

# read index and sample file
while read line
do
    read a b <<< `echo $line | cut -f 1,2`
    index2sample[$a]=$b
done < $1

# for quality converting
for i in $(ls $3/*.gz)
do 
    old=`basename $i`
    tmpindex=`echo $old | awk -F '_|-' '{print $"'$2'"}'`
#    echo $tmpindex,tmpindex
    if [ -n "$tmpindex"  ] && [ -n "${index2sample[$tmpindex]}" ]; then
        suffix=${old##*_}
        new=${index2sample[$tmpindex]}_${suffix}
        old2new[$old]=$new
        ln -s $i $new
        echo -e "$old\t$new" >> old2new.txt
        echo -e "/nfs/onegene/user/1gene/charles/bin/phred33to64 $i $new" > $4/ph64/${new%%.*}.sh
    fi
done

# for filtering
for j in ${index2sample[*]}
do
    mkdir $4/filter/$j
    echo -e "/nfs/pipe/RNA/RNA-ref/version1/filter/SOAPnuke1.3.0 filter -1 $4/ph64/${j}_R1.fastq.gz -2 $4/ph64/${j}_R2.fastq.gz -r AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA -f GATCGGAAGAGCACACGTCTGAACTCCAGTCAC -l 10 -q 0.5 -n 0.05 -i -c 0 -o $4/filter/$j -C ${j}_R1.fq.gz -D ${j}_R2.fq.gz" > $4/filter/$j/$j.sh
done
    
