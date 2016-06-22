library(WGCNA)
options(stringsAsFactors=F)

args = commandArgs(T)

if (length(args) != 3) {
  print("USAGE: Rscript wgcna3.r datExpr.RData dynamic_merged_networkdata.RData dissTOM.RData")
  quit(save='no')
}

#load("datExpr.RData")
#load("dynamic_merged_networkdata.RData")
#load('dissTOM.RData')

load(args[1])
load(args[2])
load(args[3])

TOM = 1 - dissTOM

dir.create('moduleGenes', showWarnings = FALSE)
colors = names(table(moduleColors))
data = t(datExpr)
genes = colnames(datExpr)

# Module Membership(Kme) and Module Membership p-value
dir.create('moduleMembership', showWarnings = FALSE)
geneModuleMembership = as.data.frame(cor(datExpr, MEs, use="p"))
MMpvalue = as.data.frame(corPvalueStudent(as.matrix(geneModuleMembership), dim(datExpr)[1]))
 
write.table(geneModuleMembership, file='moduleMembership/All_ModuleMembership.xls',quote=F, sep='\t', col.names=NA)
write.table(MMpvalue, file='moduleMembership/All_ModuleMembershipPvalue.xls',quote=F, sep='\t', col.names=NA)

# output data
for (c in colors) {
    if (c == 'grey'){
        next
    }

    selected = moduleColors == c
    tmpdata = data[selected,]
    outfilename = paste('moduleGenes/', c,'.xls', sep='')
    write.table(file=outfilename, tmpdata, quote=F, sep='\t',col.names=NA)

    modGenes = genes[selected]
    modTOM = TOM[selected,selected]
    dimnames(modTOM) = list(modGenes, modGenes)
    exportNetworkToCytoscape(modTOM, 
      edgeFile = paste("moduleGenes/cyt-edge_", c, ".txt", sep=""),
      nodeFile = paste("moduleGenes/cyt-nodes-", c, ".txt", sep=""),
      weighted = TRUE,
      threshold = 0.02,
      nodeNames = modGenes,
      altNodeNames = modGenes,
      nodeAttr = moduleColors[selected])

    tmpMM = paste('moduleMembership/', c,'_MM.xls', sep='')
    tmpMMp = paste('moduleMembership/', c,'_MMp.xls', sep='')
    write.table(geneModuleMembership[selected,], file=tmpMM, quote=F, sep='\t', col.names=NA)
    write.table(MMpvalue[selected,], file=tmpMMp, quote=F, sep='\t', col.names=NA)
}



