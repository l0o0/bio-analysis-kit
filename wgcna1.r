library(WGCNA)
options(stringsAsFactors = FALSE)
enableWGCNAThreads()

args = commandArgs(trailingOnly=TRUE)

#***********************************step1 cluster Sample*************************************
prefix = strsplit(args[1], '.', fixed=TRUE)[[1]][1]
d=read.table(args[1],sep="\t",header=T,check.names=F, row.names=1)
#d=d[1:10000,]
datExpr = t(d)

gsg = goodSamplesGenes(datExpr, verbose = 3)
if (!gsg$allOK)
{
if (sum(!gsg$goodGenes)>0)
	printFlush(paste("Removing genes:", paste(names(datExpr)[!gsg$goodGenes], collapse = ", ")))
if (sum(!gsg$goodSamples)>0)
	printFlush(paste("Removing samples:", paste(rownames(datExpr)[!gsg$goodSamples], collapse = ", ")))
	datExpr = datExpr[gsg$goodSamples, gsg$goodGenes]
}
#write.table(names(datExpr)[!gsg$goodGenes], file="removeGene.xls", row.names=FALSE, col.names=FALSE, quote=FALSE)
#write.table(names(datExpr)[!gsg$goodSamples], file="removeSample.xls", row.names=FALSE, col.names=FALSE, quote=FALSE)




sampleTree = hclust(dist(datExpr), method = "average")
pdf(file = paste(prefix,"sampleClustering.pdf", sep='_'), width = 12, height = 9)
par(cex = 0.6)
par(mar = c(0,4,2,0))
plot(sampleTree, main = "Sample clustering", sub="", xlab="", cex.lab = 1.5, cex.axis = 1.5, cex.main = 2)
dev.off()


#***********************************step2  Choosing the soft threshold beta via scale free topology*************************************


powers = c(c(1:10), seq(from = 12, to=20, by=2))
#sft = pickSoftThreshold(datExpr, powerVector = powers, verbose = 5)
sft=pickSoftThreshold(datExpr,dataIsExpr = TRUE,powerVector = powers,corFnc = cor,corOptions = list(use = 'p'),networkType = "unsigned")

pdf(file=paste(prefix,'pickSoftThreshold.pdf', sep='_'), wi=12, he=9)
par(mfrow = c(1,2))
cex1 = 0.9
# Plot the results:
par(mfrow = c(1, 2))
# SFT index as a function of different powers
plot(sft$fitIndices[,1], -sign(sft$fitIndices[, 3])*sft$fitIndices[, 2], xlab = "Soft Threshold (power)", ylab = "Scale Free Topology Model Fit, signed R^2", type = "n", main = paste("Scale independence"))
text(sft$fitIndices[, 1], -sign(sft$fitIndices[, 3]) * sft$fitIndices[, 2], labels = powers, col = "red")
# this line corresponds to using an R^2 cut-off of h
abline(h = 0.9, col = "red")
# Mean connectivity as a function of different powers
plot(sft$fitIndices[, 1], sft$fitIndices[, 5], type = "n", xlab = "Soft Threshold (power)", ylab = "Mean Connectivity", main = paste("Mean connectivity"))
text(sft$fitIndices[, 1], sft$fitIndices[, 5], labels = powers, col = "red") 

dev.off()
save(datExpr, file='datExpr.RData')
