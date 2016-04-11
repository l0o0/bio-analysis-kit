library(pheatmap)
args = commandArgs(T)

agene = read.table(args[1], header=T)
#bgene = read.table(args[2], header=T)
#intergene = intersect(agene[,1], bgene[,1])

allexp = read.table(args[2], header=T, row.names = 1)
prefix = args[3]
inter_gene_exp = allexp[rownames(allexp)%in%agene[,1],]
pdf(paste(prefix,'.pdf',sep=''))

# 在进行聚类的时候，一般选择的基因数目不能太多，最好别超过250个
# 有时基因数目太多，需要设置下右边基因ID字体的大小（参数 fontsize_row）
pheatmap(log10(data.matrix(inter_gene_exp)+1), fontsize_row = 8)
dev.off()

png(filename=paste(prefix, '.png', sep=''))
pheatmap(log10(data.matrix(inter_gene_exp)+1), fontsize_row = 8)
dev.off()
write.table(file=paste(prefix, '_exp.xls', sep=''), inter_gene_exp, sep='\t', quote=F)
