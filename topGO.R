library(topGO)
library(multtest)

geneID2GO = readMappings(file='/share/fg3/Linxzh/Tmp/GO/2014-10-6_cucumber_gene2go.map')
geneNames = names(geneID2GO)

args = commandArgs(TRUE)
infile = args[1]
outfile = paste(sep='', strsplit(infile, '.', fixed=T)[[1]][1], '_topGO.txt')
outgene = paste(sep='', strsplit(infile, '.', fixed=T)[[1]][1], '_topGOgenes.txt')
ingene = read.table(infile, header=F)
Ingene = as.character(ingene[,1])

geneList = factor(as.integer(geneNames %in% Ingene))
names(geneList) = geneNames

GOdata = new('topGOdata', ontology='BP', allGenes=geneList, annot=annFUN.gene2GO, gene2GO = geneID2GO)

resultFis = runTest(GOdata, algorithm='classic', statistic='fisher')
sigNum = sum(resultFis@score <0.05)
Res = GenTable(GOdata,classic=resultFis,orderBy='classic',ranksOf = 'classic', numChar=1000, topNodes=sigNum + 1)

# FDR Running
raw_p = as.numeric(Res$classic)
res = mt.rawp2adjp(raw_p,"BH")
adjp = res$adjp[order(res$index), ]

ResOut = cbind(Res,data.frame(adjp))

write.table(ResOut, file=outfile, quote=F,row.names=F, sep='\t')

# write out gene in every goterm
goID = Res$GO.ID

for (go in goID) {
	write.table(go, file=outgene, quote=F,row.names=F, sep='\t', append=T, col.names=F)
	genesInAll = genesInTerm(GOdata, go)[[1]]
	genesInSample = intersect(genesInAll, Ingene)
	write.table(t(data.frame(genesInAll)), file=outgene, quote=F,row.names=F, sep='\t', append=T, col.names=F)
	write.table(t(data.frame(genesInSample)), file=outgene, quote=F,row.names=F, sep='\t', append=T, col.names=F)
}
