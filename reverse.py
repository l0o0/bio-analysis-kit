#! /bin/env python
#Date: 2013-11-3
#Author: Linxzh
# reverse the sequence

from Bio.Seq import reverse_complement 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", help='input file',type=argparse.FileType('r'))
parser.add_argument("-o", help='output file',type=argparse.FileType('w'))
args = parser.parse_args()

n = 0

for l in args.i:
    if n == 0:
        n = 1
        tmp_id = l        
    elif n ==1:
        n = 0
        if '-' in tmp_id:
            seq = reverse_complement(l[:-1]) + '\n'
        else:
            seq = l
        args.o.write(tmp_id,seq)

args.i.close()
args.o.close()
