library(multtest)

args = commandArgs(TRUE)

infile = args[1]
outfile = paste(sep='', strsplit(infile, '_', fixed=T)[[1]][1], "_IPRout.txt")

D = read.delim(infile, sep='\t')
n = seq(1:nrow(D))
fisher = rep('NA',nrow(D))
FDR = rep('NA',nrow(D))

for (i in n) {
	a = D[i,2] - D[i,3] 
	b = D[i,3]
	c = D[i,4] - D[i,5]
	d =D[i,5]
	m = matrix(c(a,b,c,d),nrow=2)
	
	p = fisher.test(m)$p.value
	fisher[i] = p
}

res = mt.rawp2adjp(as.numeric(fisher),"BH")
adjp = res$adjp[order(res$index), ]
M = cbind(data.frame(adjp), D, all=T)
colnames(M) = c('raw-p_value','FDR', 'IPR-id','Gene_num','Genes_in_ipr_num','Sample_gene_num','Sample_Genes_in_ipr_num','IPR_term')
write.table(M,file=outfile, row.names=F,quote=F,sep='\t')
