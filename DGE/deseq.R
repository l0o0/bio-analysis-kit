library(DESeq)
countsTable <- read.delim("readsCount.txt",header=TRUE,stringsAsFactors=TRUE, row.names="GeneID")
#countsTable <-countsTable[rowSums(countsTable) >=16, ]
conds <- factor(c("CK1","CK2","CK3","Con1","Con2","Con3"))
cds <- newCountDataSet( countsTable, conds )
cdsAB <- cds[,c("CK","Con")]
cdsAB <- estimateSizeFactors( cdsAB )
cdsAB <- estimateDispersions(cdsAB,method="blind",sharingMode ="fit-only",fitType="local")
resAB <- nbinomTest(cdsAB,"CK","Con")
write.table(resAB,"out.DESeq.Result.xls",sep = "\t",row.names = F,quote=F)
