#!/bin/bash
# created by linxzh, 2015-10-24
# script for sample raw data renaming, converting quality,filtering


#-----------------------------------------------------------------------
# $1 == index2sample.txt
# $2 == index of index
# $3 == raw data path 
# $4 == working dir 
# $5 == reads length
# $6 == data size
# sh quality.sh index2sample.txt <index num> <rawdata path> <working dir> <read length> <data size in Gb>
#------------------------------------------------------------------------

#echo $1,$2,$3,$4

if [ $# -lt 4 ]; then
    echo "sh quality.sh index2sample.txt <index num> <rawdata path> <working dir> <readlength> <datasize(G)>"
    echo "index2sample.list : index1<tab>sample1"
    echo "index is seperated by '_-'"
    exit 0 
fi

mkdir $4/ph64
mkdir $4/filter

declare -A index2sample
declare -A old2new

# read index and sample file
while read line
do
    read a b <<< `echo $line | awk '{print $1"\t"$2}'`
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
        ln -s $i $4/$new
        echo -e "$old\t$new" >> old2new.txt
        echo -e "/nfs/onegene/user/1gene/charles/bin/phred33to64 ../$new $new" > $4/ph64/${new%%.*}.sh
        # fqpath for configure file        
        if [[ "$new" =~ _R1\.fastq.gz ]];then
            echo "KeyName=${new%%_R1*}" >> $4/ph64/fqpath.txt
            echo "length=You need change here" >> $4/ph64/fqpath.txt
            echo "insert=200" >> $4/ph64/fqpath.txt
            echo "q1=$4/ph64/$new" >> $4/ph64/fqpath.txt
            echo "q2=$4/ph64/${new/_R1./_R2.}" >> $4/ph64/fqpath.txt
            echo >> $4/ph64/fqpath.txt
        fi
    fi
done

# for filtering
G=$6
if [ $G -eq 0 ]; then
    G=''
fi

mkdir $4/cut
for j in ${index2sample[*]}
do
    mkdir $4/filter/$j
    echo -e "/nfs/pipe/RNA/RNA-ref/version1/filter/SOAPnuke1.3.0 filter -1 $4/ph64/${j}_R1.fastq.gz -2 $4/ph64/${j}_R2.fastq.gz -r AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA -f GATCGGAAGAGCACACGTCTGAACTCCAGTCAC -l 20 -q 0.3 -n 0.02 -i -c 0 -o $4/filter/$j -C ${j}_R1.fq.gz -D ${j}_R2.fq.gz" > $4/filter/$j.sh
    echo -e "perl /nfs/pipe/RNA/RNA-ref/version1/filter/PlotfilterResult_GC-PE_Forsoapnuke.pl $j/Base_distributions_by_read_position_1.txt $j/Base_distributions_by_read_position_2.txt -k $j -o $j" >> $4/filter/$j.sh
    echo -e "perl /nfs/pipe/RNA/RNA-ref/version1/filter/PlotfilterResult_GC-PE_Forsoapnuke.pl $j/Base_distributions_by_read_position_1.txt $j/Base_distributions_by_read_position_2.txt -k $j -o $j" >> $4/filter/$j.sh
	echo -e "perl /nfs/pipe/RNA/RNA-ref/version1/cutFq2.pl $4/filter/${j}_R1.fq.gz $4/filter/${j}/${j}_R2.fq.gz $5 ${j} $6" > $4/cut/$j.sh
    # fqpath for configure file in cut
    echo "KeyName=$j" >> $4/cut/fqpath.txt
    echo "length=$5,$5" >> $4/cut/fqpath.txt
    echo "insert=200" >> $4/cut/fqpath.txt
    echo "q1=$4/cut/${j}_R1.fq.gz" >> $4/cut/fqpath.txt
    echo "q2=$4/cut/${j}_R2.fq.gz" >> $4/cut/fqpath.txt
    echo >> $4/cut/fqpath.txt

done
    
