library(ggplot2)
library(grid)

args = commandArgs(T)
infile = args[1]

d <- read.table(infile, sep = "\t",stringsAsFactor=F,header=T)


draw = function(indexA, indexB, d) {
    colA = colnames(d)[indexA]
    colB = colnames(d)[indexB]
    title = sprintf("Gene Expression between %s and %s", colA,colB)
    pdffile = sprintf("%s_vs_%s.cor.pdf", colA,colB)
    pngfile = sprintf("%s_vs_%s.cor.png", colA,colB)
    B <- cor(d[,colA], d[,colB], method = c("spearman"), use="pairwise.complete.obs")
    C <- cor(d[,colA], d[,colB], method = c("pearson"), use="pairwise.complete.obs")
    print('cor')
    linefit <-lm(d[,colA] ~ d[,colB])
    B=round(B,4)
    C=round(C,4)
    linefit$coefficients[[2]]=sprintf("%.4f",linefit$coefficients[[2]])
    print('darwing')
    #pdf(pdffile)
    p = ggplot(data = d, mapping = aes(x = log10(get(colA)), y = log10(get(colB)))) 
    p1 = p + geom_point(colour="#B1639F",size=1)
    p2 = p1 + xlab(sprintf("log10(%s)",colA))+ylab(sprintf("log10(%s)",colB)) + ggtitle(title)
    p3 = p2+ theme(axis.text=element_text(size=10),axis.title = element_text(size =13), plot.title=element_text(size=16),legend.title=element_text(size=14,face="plain"),legend.title.align=0,legend.key=element_blank(),legend.text=element_blank(),legend.position=c(0.18,0.92),legend.key.size=unit(0,"cm"))
    p4 = p3 + geom_text(data=NULL, x=-1, y=3.5,label=paste(paste(" slope k = ",linefit$coefficients[[2]],"\n"),paste("spearman r = ",B,"\n"),paste("pearson r = ",C)),size=3)
#    p5 = p4 + stat_abline(colour="#A2A3A4",linetype="dashed",lw=0.6)
    ggsave(p4, file=pdffile)
    ggsave(p4, file=pngfile)
}


pick = function(idx, m, d) {
    choices = combn(idx, m)
    for (i in seq(1, ncol(choices))) {
        draw(choices[1,i], choices[2,i], d)
    }
}


# for 0 5 9
#for (i in c(0,5,9)) {
#    pattern = paste('^[Cc].*', i, sep='')
#    controls = grep(pattern, colnames(d))
#    print(controls)
#    pick(controls, 2, d)
#}

# for 5 9 
for (i in c(5,9)) {
    pattern = paste('^ABA.*', i, sep='')
    treats = grep(pattern, colnames(d))
    pick(treats, 2, d)

    pattern = paste('^NDGA.*', i, sep='')
    treats = grep(pattern, colnames(d))
    pick(treats, 2, d)
    
    pattern = paste('^control.*', i, sep='')
    treats = grep(pattern, colnames(d))
    pick(treats, 2, d)
}
