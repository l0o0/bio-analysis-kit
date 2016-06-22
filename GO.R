# Writing for Tang
# Linxzh 2016-06-21
# Find out genes belong to a Gene Ontology ID.

tryCatch({
    library(topGO)
}, error = function(e) {
    print("You need to install topGO package from bioconductor.")
    print("You can find help from https://bioconductor.org/packages/release/bioc/html/topGO.html.")
    quit(save='no')
})

library(topGO)

args = commandArgs(T)

geneID2GO = readMappings(file=args[1])
geneNames = names(geneID2GO)
tmpgene = geneNames[1:100]
geneList = factor(as.integer(geneNames %in% tmpgene))
names(geneList) = geneNames


