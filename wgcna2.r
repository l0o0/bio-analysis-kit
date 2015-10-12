# load expression data
load('datExpr.RData')

# environment
library(WGCNA)
options(stringsAsFactors=FALSE)
enableWGCNAThreads(6)

# softpower
softPower = 6

# unsigned type
adjacency = adjacency(datExpr, power = softPower)
TOM = TOMsimilarity(adjacency)
dissTOM = 1 - TOM
save(file='dissTOM.RData', dissTOM)
#load('dissTOM.RData')
geneTree = hclust(as.dist(dissTOM), method='average')
minModuleSize = 30

dynamicMods = cutreeDynamic(dendro = geneTree, distM = dissTOM, deepSplit = 4,
pamRespectsDendro = FALSE, minClusterSize = minModuleSize) 

dynamicColors = labels2colors(dynamicMods)

MEList = moduleEigengenes(datExpr, colors = dynamicColors)
MEs = MEList$eigengenes
MEDiss = 1 - cor(MEs)
METree = hclust(as.dist(MEDiss), method = 'average')

# plot genetree cluster
#pdf(file = 'GeneTreeCluster.pdf', wi=12, he=9)
#plot(METree, main= 'Clustering of module eigengenes', xlab = '', sub = '', cex.lab = 0.6, cex.axis = 0.8)
#dev.off()

# plot module eigengenes cluster
MEDissThres = 0.25
#pdf(file = 'ClusterModuleEigengenes.pdf', wi=12, he=9)
#plot(METree, main='Clustering of module eigengenes', xlab = '', sub = '')
#abline(h=MEDissThres, col = 'red')
#dev.off()

# module merge
merge = mergeCloseModules(datExpr, dynamicColors, cutHeight = MEDissThres , verbose = 3)
mergedColors = merge$colors
mergedMEs = merge$newMEs
pdf(file = 'BeforeAndAfterMerge.pdf', wi=12, he=9)
plotDendroAndColors(geneTree, cbind(dynamicColors, mergedColors), dendroLabels
= FALSE, hang = 0.03, addGuide = TRUE, guideHang = 0.05)
dev.off()

moduleColors = mergedColors
colorOrder = c('grey', standardColors(100))
moduleLabels = match(moduleColors, colorOrder) - 1
MEs = mergedMEs
save(file='dynamic_merged_networkdata.RData', MEs, moduleLabels, moduleColors,
geneTree, dynamicMods)

# output module genes and rpkm values, export network to cytoscape
dir.create('moduleGenes', showWarnings = FALSE)
colors = names(table(moduleColors))
data = t(datExpr)
genes = names(datExpr)

for (c in colors) {
    selected = moduleColors == c
    tmpdata = data[selected,]
    outfilename = paste('moduleGenes/', c,'.xls', sep='')
    write.table(file=outfilename, tmpdata, quote=F, sep='\t')

    modGenes = genes[selected]
    modTom = TOM[selected,selected]
    dimnames(modTOM) = list(modGenes, modGenes)
    exportNetworkToCytoscape(modTOM, 
      edgeFile = paste("moduleGenes/cyt-edge_", c, ".txt", sep=""),
      nodeFile = paste("moduleGenes/cyt-nodes-", c, ".txt", sep=""),
      weighted = TRUE,
      threshold = 0.02,
      nodeNames = modGeness,
      altNodeNames = modGenes,
      nodeAttr = moduleColors[selected])
}

