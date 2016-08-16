# Writing for Tang
# Linxzh 2016-06-21
# Find out genes belong to a Gene Ontology ID.

args = commandArgs(T)
if (length(args) != 3) {
    print('USAGE: Rscript GO.R GO_Mapping GO_ID Ontology')
    print('Ontology: BP for Biological Process')
    print('CC for Cellular Component')
    print('MF for Molecular Function')
    quit(save='no')
}

tryCatch({
    library(topGO)
}, error = function(e) {
    print("You need to install topGO package from bioconductor.")
    print("You can find help from https://bioconductor.org/packages/release/bioc/html/topGO.html.")
    quit(save='no')
})

library(topGO)

geneID2GO = readMappings(file=args[1])
geneNames = names(geneID2GO)
tmpgene = geneNames[1:100]
geneList = factor(as.integer(geneNames %in% tmpgene))
names(geneList) = geneNames

GOdata = new('topGOdata', ontology=args[3], allGenes=geneList, annot=annFUN.gene2GO, gene2GO = geneID2GO)

ann.genes = genesInTerm(GOdata, args[2])
write.table(ann.genes, file=paste(args[3], '_',args[2],'.txt', sep=''), sep='\t', quote=F)
