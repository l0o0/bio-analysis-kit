#!/usr/local/bin/python
# 2014-12-2    Linxzh

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input file')
parser.add_argument('-o', help='output file')
parser.add_argument('-p', help='Positional file')
parser.add_argument('-d', help='distance * kb', type=int, default=10000)
parser.add_argument('-f', help='fliter the uncluster genes', type=str, default='True', choices=['True','False'])
args = parser.parse_args()

# read gene-id from module, args.i -- input file
def read_gene(infile):
    '''input file format:
    moduleName1
    Gene1 Gene2...
    moduleName2
    GeneA GeneB...'''

    D = {}

    with open(infile) as f:
        fl = f.readlines()

    for i in range(0,len(fl),2):
        genes = [x for x in fl[i+1].split()]
        D[fl[i]] = genes

    return D

# read gene--pos dictionary
def read_pos(infile):
    posD = {}
    chrom_genes = {}
    with open(infile) as f:
        for line in f:
            lineList = line.split()
            posD[lineList[3]] = int(lineList[1])
            if lineList[0] not in chrom_genes:
                chrom_genes[lineList[0]] = [lineList[3]]
            else:
                chrom_genes[lineList[0]].append(lineList[3])

    return posD, chrom_genes

# remove unclustered gene from the result line
def remove_uncluster(outstring):
    outlist = outstring.split(' | ')
    outlist = [x for x in outlist if '-' in x]
    outstr = ' | '.join(outlist)
    return outstr

# positional cluster
def cluster(D, posD, chrom_genes, outfile, dist=10000, f='True'):
    '''D: input gene, {moduleName: gene1 gene2 ...}
       posD: {geneID: start pos}'''

# cluster the gene with '-', sep by ' | '
    def find_cluster(chrom_genes, posD, inputgenes):
        outList = []
        for k in chrom_genes.keys():
            geneList = chrom_genes[k]
            geneList = list(set(geneList).intersection(set(inputgenes)))
            geneList = sorted(geneList, key=lambda g:posD[g])
            if not geneList:
                continue

            for i in range(len(geneList)-1):

                d = posD[geneList[i+1]] - posD[geneList[i]]

                if d <= dist :
                    geneList[i] += '<->'
                else:
                    geneList[i] += ' | '

            newline = ''.join(geneList)

            if '-' in newline:            # only need cluster genes
                if f == 'True':
                    newline = remove_uncluster(newline)
                    newline = k + '\t' + newline +  '\n'
                outList.append(newline)

        return outList

    wl = []
    for (m,l) in D.items():
        outList = find_cluster(chrom_genes, posD, l)
        if outList:                    # fliter empty out list
            wl.append(m)               # add module number
            wl += outList

    with open(outfile,'w') as f:
        print len(wl)
        f.writelines(wl)

if __name__ == '__main__':
    D = read_gene(args.i)

    for sca in D:
        print sca, len(D[sca])

    posD, chrom_genes = read_pos(args.p)
    cluster(D, posD, chrom_genes, args.o, args.d, args.f)
