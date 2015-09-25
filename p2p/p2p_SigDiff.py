#!/usr/bin/python
# get proteion-proteion interaction according genes
# expressing differently(significantly)

import os
import re
import gzip
import sys

def read_pp(infile):
    if infile.endswith('gz'):
        handle = gzip.open(infile, 'rb')
    else:
        handle = open(infile)
    pplist = handle.readlines()
    outlist = ['\t'.join(f.split()[:2])+'\n' for f in pplist]
    
    return outlist


def read_dge(infile):
    with open(infile) as handle:
        flist = handle.readlines()
    return [x.split()[0] for x in flist[1:]]


# gene name to string id 
def name_stringid(stringname):
    with open(stringname) as handle:
        handlist = handle.readlines()
        tmp = [(x.split('\t')[1],x.split('\t')[6].strip()) for x in handlist]
        f = lambda x:x[::-1]
    return dict(tmp),dict(map(f, tmp))


def pick_out(pplist, genes, stringids, dgelist):
    out = []
    for gene in dgelist:
        if gene in genes:
            out += [x for x in pplist if stringids[genes.index(gene)] in x]
    return out

def add_name(link, dge, id2name):
    pps = link.split()

    if pps[0] in id2name:
        p1name = id2name[pps[0]]
    else:
        p1name = pps[0]
    if pps[1] in id2name:
        p2name = id2name[pps[1]]
    else:
        p2name = pps[1]

    if p1name in dge:
        p1dge = dge[p1name]
    else:
        p1dge = 'None'
    if p2name in dge:
        p2dge = dge[p2name]
    else:
        p2dge = 'None'
    newline = '%s\t%s\t%s\t%s\t%s' % (p1name, p2name, p1dge, p2dge,link)
    return newline


def read_updown(infile):
    D = {}
    with open(infile) as handle:
        for f in handle:
            flist = f.split('\t')
            D[flist[0]] = flist[7]
    return D


if __name__ == "__main__":
    pp = read_pp('9606__protein_links.tsv')
    id2name, name2id = name_stringid('9606__proteins.tsv')
    updown = read_updown(sys.argv[1])
#    dge = read_dge(sys.argv[1])
#    print updown.keys()[:10]
#    print updown.values()[:5]
    dge = updown.keys()
    with open('tmp.txt','w') as handle:
        header = 'fromName\ttoName\tF\tT' + 'protein1 protein2 neighborhood neighborhood_transferred fusion cooccurence homology coexpression coexpression_transferred experiments experiments_transferred database database_transferred textmining textmining_transferred combined_score\n'.replace(' ','\t')
        handle.write(header)
        tmplist = []
        for genename in dge:
            if genename in name2id:
                stringid = name2id[genename]
                for link in pp:
                    if stringid+'\t' in link or stringid+'\n' in link:
                        newlink = add_name(link, updown, id2name)
                        tmplist.append(newlink)
        tmplist = list(set(tmplist))
        handle.writelines(tmplist)
              
