#!/usr/bin/python


import sys
from Bio import Entrez

# get gene id list
with open(sys.argv[1]) as handle:
    idlist = handle.readlines()
    idlist = [x.strip() for x in idlist]


Entrez.email = 'linxzh1989@gmail.com'

for i in idlist:
    handle = Entrez.esearch(db='nucleotide', term=i)
    rec = Entrez.read(handle)
    fetchid = rec['IdList']

    if len(fetchid) == 1:
        fetchid = [fetchid]

    for rid in fetchid:
        handle = Entrez.efetch(db='nucleotide', id=rid, rettype='fasta')
        fa = handle.read()
        print fa



