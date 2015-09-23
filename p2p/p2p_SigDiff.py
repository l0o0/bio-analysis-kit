#!/usr/bin/python
# get proteion-proteion interaction according genes
# expressing differently(significantly)

import argparse
import os
import re
import gzip


parser = argparse.ArgumentParser()
parser.add_argument('-indir', type=str, help='output dir of different expressed genes')
parser.add_argument('-p', type=str, help='proteion-proteion interaction file, in gz or text')
parser.add_argument('-outdir', type=str, default='.', help='output dir')
args = parser.parse_args()


def read_pp(infile):
    if infile.endswith('gz'):
        handle = gzip.open(infile, 'rb')
    else:
        handle = open(infile)
    pplist = handle.readlines()
    pp1 = []; pp2 = []

    for p in pplist:
        plist = p.split()
        pp1.append(plist[0])
        pp2.append(plist[1])

    return pplist, pp1, pp2


def read_dge(infile):
    with open(infile) as handle:
        flist = handle.readlines()
    return [x.split()[0] for x in flist]


def pick_out(pplist, pp1, pp2, dgelist):
    allset = set(pp1) | set(pp2) | set(dgelist)

    


if __name__ == '__main__':
    
