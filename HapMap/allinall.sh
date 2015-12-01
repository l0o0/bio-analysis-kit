#!/bin/bash

source /nfs3/onegene/user/group1/linxingzhong/workspace/bio2.7.10/bin/activate

read -p "Please input chromosome number(int): " chrNum
echo $chrNum

for i in $(seq 1 ${chrNum})
do  
    i=`printf "%02d" ${i}`
    printf "chr%s starts...\n" $i 
    echo -e "chr${i}\tchr${i}\t1\t1000000000" >> region.txt
    echo -e "chr${i}:1:1000000000" >> chr${i}_sample.txt
    for j in $(ls *chr${i}.filter.block)
    do
        echo -e "${j%%.*}\t${j}" >> chr${i}_sample.txt
    done
    printf "chr%s drawing...\n" $i
    python /nfs3/onegene/user/group1/linxingzhong/scripts/bio/HapMap/draw.py chr${i}_sample.txt region.txt chr${i}.svg
    printf "chr%s done.\n" $i
done

deactivate
