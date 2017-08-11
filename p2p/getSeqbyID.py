#! /usr/bin/python
#! linxingxhong 201606028
# Retrive prptein sequences from StringDB by specie id.

import sys

try:
    from Bio import SeqIO
except ImportError:
    print "Please run the command below:"
    print "source /nfs3/onegene/user/group1/linxingzhong/workspace/bio2.7.10/bin/activate"
    print "Or you can install biopython by yourself."
    sys.exit(0)


def faGet(infile, num):
    prefix = num + '.'
    fa = SeqIO.parse(infile,'fasta')
    out = [f for f in fa if f.id.startswith(prefix)]
    return out


if __name__=='__main__':

    spe_id = sys.argv[1]
    stringdb = sys.argv[2]
    specieFa = sys.argv[3]
    rec = faGet(stringdb, spe_id)
    SeqIO.write(rec, specieFa, 'fasta')



