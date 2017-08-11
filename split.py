#!/bin/env python
# linxzh    2015012-2
#

import os
import sys
from Bio import SeqIO

if len(sys.argv) != 4:
    print "USAGE: python split.py origin.fa outdir sequenceNum"
    sys.exit(0)

if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])

fa_dict = SeqIO.to_dict(SeqIO.parse(sys.argv[1], 'fasta'))

step =  int(sys.argv[3])
print step
unigenes = fa_dict.keys()
print len(unigenes)
n = 0
for i in range(0,len(unigenes), step):
    genes = unigenes[i:i+step]
    recs = [fa_dict[j] for j in genes]
    outfasta = '%s/unigenes_%s.fa' % (sys.argv[2], i)
    SeqIO.write(recs, outfasta,'fasta')
    n += 1

print n
