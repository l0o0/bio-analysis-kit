#!/usr/bin/python

import sys


if len(sys.argv) != 5:
    print "USAGE: python filter.py input.loc output.loc missingRate(float) ProSampleNum(int)"
    sys.exit(0)

sample= int(sys.argv[4])
missnum = int(sample * float(sys.argv[3])) + 1
with open(sys.argv[1]) as handle:
    filelist = handle.readlines()
#    markerlist = filelist[5:-(sample+1)]
    markerlist = [x for x in filelist if not x.startswith('#')]

out = [x for x in markerlist if x.count('--') < missnum and x.strip()]
print len(out)
print out[0]
D={}
for l in out:
    llist = l.split('\t')
    k='\t'.join(llist[2:])
    v='\t'.join(llist[:2])
    D[k] = v
print D.items()[0]

with open(sys.argv[2], 'w') as handle:
    for k,v in D.items():
        s = '%s\t%s' % (v,k)
        handle.write(s)

