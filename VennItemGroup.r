#!/bin/env Rscript
# Created by Linxingzhong at 2015-7-24
# get items in the intersection of venn plot

library('tools')
library('VennDiagram')


args = commandArgs(TRUE)
options(stringsAsFactors=F)
#-----------------------------------------------------
#               USAGE
# Rscript VennItemGroup.r <outdir> <file1> <file2> <file3> ...
#
#----------------------------------------------------


# read input file as a list
File2List = function(args) {
    tmpList = list()
        for (arg in args) {
            name = basename(file_path_sans_ext(arg))
            geneList = read.table(arg, header=T, sep='\t', fill=TRUE, quote="", stringsAsFactors=F)[,1]
            tmpList[[name]] = geneList
        }
    return(tmpList)
    }


# redefined function of set analyis, add the sample names to the result
Intersection = function(...) {
    out = Reduce(intersect, list(...))
    return(out)

}

Union = function(...) {
    out = Reduce(union, list(...))
    return(out)
}



# get intersection and write them to file
InterItems = function(datalist) {
    if (class(datalist) != "list") 
        stop("Please make sure the input data is in list! ")
    
    m = length(datalist)    # sample number
    Names = names(datalist) # sample names 
    outlist = list()
    
    if (m == 1) {
        outlist = datalist
    }
    else if (m == 2) {
        cross = Intersection(datalist[[1]], datalist[[2]])
        outlist[[paste(Names, collapse="@")]] = cross
        a12 = setdiff(datalist[[1]], cross)
        outlist[[paste(Names, collapse="-")]] = a12
        a21 = setdiff(datalist[[2]], cross)
        outlist[[paste(rev(Names), collapse="-")]] = a21

    }
    else if (m == 3) {
        n12 = intersect(datalist[[1]], datalist[[2]])
        n13 = intersect(datalist[[1]], datalist[[3]])
        n23 = intersect(datalist[[2]], datalist[[3]])
        n123 = Intersection(n13, n12, n23)

        a1 = setdiff(datalist[[1]], union(n12,n13))
        a2 = setdiff(n12, n123)
        a3 = setdiff(datalist[[2]], union(n12, n23))
        a4 = setdiff(n13, n123)
        a5 = n123
        a6 = setdiff(n23, n123)
        a7 = setdiff(datalist[[3]], union(n13, n23))

        outlist[['a1']] = a1
        outlist[['a2']] = a2
        outlist[['a3']] = a3
        outlist[['a4']] = a4
        outlist[['a5']] = a5
        outlist[['a6']] = a6
        outlist[['a7']] = a7

    }
    else if (m == 4) {
        n12 = intersect(datalist[[1]], datalist[[2]])
        n13 = intersect(datalist[[1]], datalist[[3]])
        n14 = intersect(datalist[[1]], datalist[[4]])
        n23 = intersect(datalist[[2]], datalist[[3]])
        n24 = intersect(datalist[[2]], datalist[[4]])
        n34 = intersect(datalist[[3]], datalist[[4]])

        n123 = intersect(n12, datalist[[3]])
        n124 = intersect(n12, datalist[[4]])
        n134 = intersect(n13, datalist[[4]])
        n234 = intersect(n23, datalist[[4]])

        n1234 = intersect(n123, datalist[[4]])

        a6  = n1234
        a12 = setdiff(n123, a6)
        a11 = setdiff(n124, a6)
        a5  = setdiff(n134, a6)
        a7  = setdiff(n234, a6)
        a15 = setdiff(n12, Union(a6, a11, a12))
        a4  = setdiff(n13, Union(a6, a5, a12))
        a10 = setdiff(n14, Union(a6, a5, a11))
        a13 = setdiff(n23, Union(a6, a7, a12))
        a8  = setdiff(n24, Union(a6, a7, a11))
        a2  = setdiff(n34, Union(a6, a5, a7))
        a9  = setdiff(datalist[[1]], Union(a4, a5, a6, a10, a11, a12, a15))
        a14 = setdiff(datalist[[2]], Union(a6, a7, a8, a11, a12, a13, a15))
        a1  = setdiff(datalist[[3]], Union(a2, a4, a5, a6, a7, a12, a13))
        a3  = setdiff(datalist[[4]], Union(a2, a5, a6, a7, a8, a10, a11))
        
        outlist[['a1']] = a1
        outlist[['a2']] = a2
        outlist[['a3']] = a3
        outlist[['a4']] = a4
        outlist[['a5']] = a5
        outlist[['a6']] = a6
        outlist[['a7']] = a7
        outlist[['a8']] = a8
        outlist[['a9']] = a9
        outlist[['a10']] = a10
        outlist[['a11']] = a11
        outlist[['a12']] = a12
        outlist[['a13']] = a13
        outlist[['a14']] = a14
        outlist[['a15']] = a15


        }
    else if (m == 5) {
        n12 = intersect(datalist[[1]], datalist[[2]])
        n13 = intersect(datalist[[1]], datalist[[3]])
        n14 = intersect(datalist[[1]], datalist[[4]])
        n15 = intersect(datalist[[1]], datalist[[5]])
        n23 = intersect(datalist[[2]], datalist[[3]])
        n24 = intersect(datalist[[2]], datalist[[4]])
        n25 = intersect(datalist[[2]], datalist[[5]])
        n34 = intersect(datalist[[3]], datalist[[4]])
        n35 = intersect(datalist[[3]], datalist[[5]])
        n45 = intersect(datalist[[4]], datalist[[5]])


        n123 = intersect(n12, datalist[[3]])
        n124 = intersect(n12, datalist[[4]])
        n125 = intersect(n12, datalist[[5]])
        n134 = intersect(n13, datalist[[4]])
        n135 = intersect(n13, datalist[[5]])
        n145 = intersect(n14, datalist[[5]])
        n234 = intersect(n23, datalist[[4]])
        n235 = intersect(n23, datalist[[5]])
        n245 = intersect(n24, datalist[[5]])
        n345 = intersect(n34, datalist[[5]])

        n1234 = intersect(n123, datalist[[4]])
        n1235 = intersect(n123, datalist[[5]])
        n1245 = intersect(n124, datalist[[5]])
        n1345 = intersect(n134, datalist[[5]])
        n2345 = intersect(n234, datalist[[5]])

        n12345 = intersect(n1234, datalist[[5]])

        a31 = n12345
        a30 = setdiff(n1234, a31)
        a29 = setdiff(n1235, a31)
        a28 = setdiff(n1245, a31)
        a27 = setdiff(n1345, a31)
        a26 = setdiff(n2345, a31)
        a25 = setdiff(n245, Union(a26, a28, a31))
        a24 = setdiff(n234, Union(a26, a30, a31))
        a23 = setdiff(n134, Union(a27, a30, a31))
        a22 = setdiff(n123, Union(a29, a30, a31))
        a21 = setdiff(n235, Union(a26, a29, a31))
        a20 = setdiff(n125, Union(a28, a29, a31))
        a19 = setdiff(n124, Union(a28, a30, a31))
        a18 = setdiff(n145, Union(a27, a28, a31))
        a17 = setdiff(n135, Union(a27, a29, a31))
        a16 = setdiff(n345, Union(a26, a27, a31))
        a15 = setdiff(n45, Union(a18, a25, a16, a28, a27, a26, a31))
        a14 = setdiff(n24, Union(a19, a24, a25, a30, a28, a26, a31))
        a13 = setdiff(n34, Union(a16, a23, a24, a26, a27, a30, a31))
        a12 = setdiff(n13, Union(a17, a22, a23, a27, a29, a30, a31))
        a11 = setdiff(n23, Union(a21, a22, a24, a26, a29, a30, a31))
        a10 = setdiff(n25, Union(a20, a21, a25, a26, a28, a29, a31))
        a9  = setdiff(n12, Union(a19, a20, a22, a28, a29, a30, a31))
        a8  = setdiff(n14, Union(a18, a19, a23, a27, a28, a30, a31))
        a7  = setdiff(n15, Union(a17, a18, a20, a27, a28, a29, a31))
        a6  = setdiff(n35, Union(a16, a17, a21, a26, a27, a29, a31))
        a5 = setdiff(datalist[[5]], Union(a6, a7, a15, a16, a17, a18, a25, a26, a27, a28, a31, a20, a29, a21, a10))
        a4 = setdiff(datalist[[4]], Union(a13, a14, a15, a16, a23, a24, a25, a26, a27, a28, a31, a18, a19, a8, a30))
        a3 = setdiff(datalist[[3]], Union(a21, a11, a12, a13, a29, a22, a23, a24, a30, a31, a26, a27, a16, a6, a17))
        a2 = setdiff(datalist[[2]], Union(a9, a10, a19, a20, a21, a11, a28, a29, a31, a22, a30, a26, a25, a24, a14))
        a1 = setdiff(datalist[[1]], Union(a7, a8, a18, a17, a19, a9, a27, a28, a31, a20, a30, a29, a22, a23, a12))

        outlist[['a1']] = a1
        outlist[['a2']] = a2
        outlist[['a3']] = a3
        outlist[['a4']] = a4
        outlist[['a5']] = a5
        outlist[['a6']] = a6
        outlist[['a7']] = a7
        outlist[['a8']] = a8
        outlist[['a9']] = a9
        outlist[['a10']] = a10
        outlist[['a11']] = a11
        outlist[['a12']] = a12
        outlist[['a13']] = a13
        outlist[['a14']] = a14
        outlist[['a15']] = a15
        outlist[['a16']] = a16
        outlist[['a17']] = a17
        outlist[['a18']] = a18
        outlist[['a19']] = a19
        outlist[['a20']] = a20
        outlist[['a21']] = a21
        outlist[['a22']] = a22
        outlist[['a23']] = a23
        outlist[['a24']] = a24
        outlist[['a25']] = a25
        outlist[['a26']] = a26
        outlist[['a27']] = a27
        outlist[['a28']] = a28
        outlist[['a29']] = a29
        outlist[['a30']] = a30
        outlist[['a31']] = a31

    }
        
    return(outlist)

}



# write inter items to file 
WriteInter = function(outlist, outdir) {
    for (i in 1:length(outlist)) {
        outfile = paste(outdir, '/', names(outlist[i]), '_', length(outlist[[i]]), '.txt', sep = '')
        names(outlist[[i]]) = names(outlist[i])
        write.table(outlist[[i]], file= outfile, row.names=FALSE, sep='\t', quote=F)
#        print(outfile)
    }
}


# draw plot
DrawVenn = function(datalist, outdir) {
    venn.plot=venn.diagram(datalist,filename=NULL,col = "#222222",lty = 1,
    lwd = 1,fill = rainbow(length(datalist)),alpha = 0.40,cex = 1,
    fontfamily = "serif",fontface = "bold",cat.col = "black",
    cat.cex =1.3,cat.fontfamily = "serif",cat.default.pos = "outer",
    margin=0.12,cat.dist=rep(0.06,length(datalist)))

    picname = paste(outdir, '/', paste(names(datalist), collapse='--'), 
    '_venn.png', sep='')

    png(picname, 540, 540)
    grid.draw(venn.plot)
    dev.off()
}


# check outdir otherwise create
dir.create(args[1], showWarnings = FALSE)

filenames = args[-1]
tmpList = File2List(filenames)
DrawVenn(tmpList, args[1])
outlist = InterItems(tmpList)
WriteInter(outlist, args[1])
