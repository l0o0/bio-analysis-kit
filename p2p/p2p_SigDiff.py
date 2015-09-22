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
    return pplist


def read_dge(infile):
    with open(infile) as handle:
        flist = handle.readlines()
    return [x.split()[0] for x in flist]


if __name__ == '__main__':
    
