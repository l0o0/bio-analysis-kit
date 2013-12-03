#!/bin/bash
#2013-12-2    Linxzh    version:0.01
#work flow for call snps

#you must build an index first
#bwa index -a bwtsw reference.fa

#short name
ref=/share/fg1/Linxzh/Data/Mutant/Ref/domestic_Chr_20101102.fa
#specify the working dicrectory by $3
cd $3

#$1 = 1.fq.gz, $2 = 2.fq.gz, SA coordinates
bwa aln -t 3 $ref $1 > leftRead.sai
bwa aln -t 3 $ref $2 > rightRead.sai

#sam 
bwa sampe -f pair-end.sam $ref leftRead.sai rightRead.sai $1 $2

#sam to bam
samtools view -bS pair-end.sam > pair-end.bam

#sort
samtools sort pair-end.bam pair-end.sorted

#index
samtools faidx $ref

#rm duplication
samtools rmdup -S pair-end.sorted.bam pair-end.sorted.rmdup.bam

#index the bam
samtools index pair-end.sorted.rmdup.bam

#call snps
samtools mpileup -u -f  $ref  pair-end.sorted.rmdup.bam | bcftools view -cg - >  pair-end.raw.cg

