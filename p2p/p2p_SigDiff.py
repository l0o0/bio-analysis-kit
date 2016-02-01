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
    pplist = [re.sub('\.\d', '', x).split() for x in pplist]
#    outlist = ['\t'.join(f.split()[:2])+'\n' for f in pplist]
    
    return pplist


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
            D[flist[0]] = flist[5]
    return D


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "python script.py stringdb_links sig_deg"
        sys.exit(0)

    pplinks = read_pp(sys.argv[1])
    print len(pplinks)
#    id2name, name2id = name_stringid('9606__proteins.tsv')
    updown = read_updown(sys.argv[2])
    print len(updown)
    dge = updown.keys()
    outsif = []
    outdiff = []

    for links in pplinks:
        if links[0] in dge or links[1] in dge:
            linksline = '\t'.join(links) + '\n'
            outsif.append(linksline)
    
            outdiff += [gene + '\t'+ updown[gene]+'\n' for gene in links[:2] if gene in updown]

    outsif = list(set(outsif))
    prefix = sys.argv[3]
    with open(prefix + '.sif','w') as handle:
        handle.writelines(outsif)

    with open(prefix + '.data','w') as handle:
        handle.writelines(outdiff)
