#!/bin/env Rscript

args = commandArgs(T)

if (length(args) != 4){
    print('USAGE: Rscript merge.R pattern merge_colname input_dir output_file')
    quit()
}


files = list.files(args[3],pattern = paste(args[1],'$',sep=''))

a <- files[1]
atable <- read.table(a, header=T, check.names=F)
#fpkma <- strsplit(a, '.', fixed=T)[[1]][1]
#names(atable) <- c('gene_id', fpkma)

for (i in files[-1]){
	print (i)
	#i <- toString(flist[i,1])
	#fpkm <- strsplit(i, '.', fixed=T)[[1]][1]
	btable <- read.table(i, header=T, check.names=F)
	print(colnames(btable))
	#names(btable) <- c('gene_id', fpkm)
	atable <- merge(atable, btable, by = args[2], all =TRUE)
}
row.names(atable) = atable[,1]
atable = atable[,-1]
print(colnames(atable))
write.table(atable, sep='\t', file=args[4], col.names=NA,quote=FALSE, na='NA')

