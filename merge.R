#!/bin/env Rscript

setwd('/share/fg3/Linxzh/genes')
flist <- read.table('flist.txt')

a <- toString(flist[1,1])
atable <- read.delim(a)
fpkma <- strsplit(a, '.', fixed=T)[[1]][1]
names(atable) <- c('gene_id', fpkma)

for (i in 2:28){
	print (flist[i,1])
	i <- toString(flist[i,1])
	fpkm <- strsplit(i, '.', fixed=T)[[1]][1]
	btable <- read.table(i)
	names(btable) <- c('gene_id', fpkm)
	atable <- merge(atable, btable, by = 'gene_id', all =TRUE)
}

write.table(atable, sep='\t', file='Genes_Fpkm_Merged.txt', quote=FALSE, row.names=FALSE, na='0.00')

