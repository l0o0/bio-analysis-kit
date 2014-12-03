#!/bin/bash
# 2014-10-10	Linxzh

AllNum=24274
SampleNum=`cat $1 | wc -l`				# sample gene number
item=`echo $1 | cut -d . -f 1`

# generate the sample gene to ipr mapping file(*.map), $2
while read line
do
	grep ${line/G/P}.1 /share/fg3/Linxzh/Tmp/ipr/gene2ipr.map >> ${item}.map
done < $1
echo $item.map "Done"

# all ipr ids mapping to sample genes(ipr to gene)(uni_ipr), $4 
awk '{for (i=2;i<=NF;i++) {print $i}}' $item.map > tmp
sort tmp | uniq > ${item}_uni_ipr.txt
rm tmp
echo ${item}_uni_ipr.txt "Done"

# count the frequency of occurrence of each ipr id, $3 
while read line
do
	IprNum=`grep $line /share/fg3/Linxzh/Data/Annotation/domestic.ipr.txt | wc -l`
	IprSamNum=`grep $line $item.map | wc -l`
	printf $line"\t"${AllNum}"\t"${IprNum}"\t"${SampleNum}"\t"${IprSamNum}"\n" >> tmp3
	grep $line /share/fg3/Linxzh/Data/Annotation/domestic_ipr_seperate_id.txt >> tmp2
done < ${item}_uni_ipr.txt

paste tmp3 tmp2 > ${item}_num.txt
rm tmp3 tmp2
echo ${item}_num.txt "Done"
