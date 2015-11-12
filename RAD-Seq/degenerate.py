#!/usr/bin/python

import sys


if len(sys.argv) != 3:
    print "USAGE: python degenerate.py inputfile outputfile"
    sys.exit(0)

DegenerateBase_Dict = {'A':'AA', 'T':'TT', 'C':'CC', 'G':'GG',
                       'R':"AG", 'Y':'CT', 'M':'AC', 'K':'GT', 'S':'GC', 'W':'AT', 
                       'H':'ATC', 'B':'GTC', 'V':'GAC', 'D':'GAT', '-':'--'}

infile = open(sys.argv[1])
out = []
for f in infile:
    if f.startswith('#'):
        out.append(f)
        continue

    flist = f.strip().split('\t')
    bases = map(lambda x : DegenerateBase_Dict[x], flist[1:])
    newline = flist[0] + '\t' + '\t'.join(bases) + '\n'
    out.append(newline)

infile.close()

with open(sys.argv[2], 'w') as handle:
    handle.writelines(out)

