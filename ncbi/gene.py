#!/usr/bin/python


import sys
from Bio import Entrez

# get gene id list
with open(sys.argv[1]) as handle:


for i in idlist:
    handle = Entrez.search(db='gene', term=i)



