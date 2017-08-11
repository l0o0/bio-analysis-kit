#!/usr/bin/python


import sys
from Bio import Entrez

# get gene id list
with open(sys.argv[1]) as handle:
    idlist = handle.readlines()
    idlist = [x.strip().split('\t') for x in idlist]

Entrez.email = 'linxzh1989@gmail.com'

out = open(sys.argv[2],'a') 
for i in idlist:
#    term = "(%s[Protein Name]) AND %s[Organism]" % (i[0], i[1])
    term = "((%s[Gene Name]) OR %s[Properties]) AND %s[Organism]" % ((i[0], i[0], i[1]))
    handle = Entrez.esearch(db='protein', term=term, usehistory='y')
    rec = Entrez.read(handle)
    webenv = rec["WebEnv"]
    query_key = rec["QueryKey"]

    if len(rec['IdList']) == 0:
        print "%s\t%s missing." % (i[0], i[1])
        continue

    handle = Entrez.efetch(db='protein', rettype='fasta', retmode='text',
                            retstart=0, retmax=int(rec['Count']),
                            webenv=webenv, query_key=query_key)
    fa = handle.read()
    print "%s\t%s, %s sequences  downloaded." % (i[0], rec['Count'], i[1])
    out.write(fa)

out.close()


