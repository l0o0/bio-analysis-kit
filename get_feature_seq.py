#!/usr/bin/python
# linxzh, create at 2015-9-16
# get feature sequence from genome according gff/gtf annotation file

import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='genome fasta file', type=str)
parser.add_argument('-g', help='gff/gtf file', type=argparse.FileType('r'))
parser.add_argument('-t', help='feature type, default is gene', default='gene', type=str)
parser.add_argument('-o', help='output file in fasta', type=str)
args = parser.parse_args()


# read feature position from gff/gtf file
def read_feature_pos(gff, feature):
    pos_dict = {}
    for f in gff:
        if f.startswith('#') or f.startswith('\n'):
            continue
        elif feature in f:
            fl = f.split()
            feature_id = fl[8].split(';')[1].split('=')[1]
            pos_dict[feature_id] = [fl[0], int(fl[3]), int(fl[4])]
    return pos_dict

# retrieve feature sequence from genome
def retrieve_seq(genome, pos_dict, outfasta):
    genome_dict = SeqIO.to_dict(SeqIO.parse(genome, 'fasta'))
    records = []
#    f = lambda x : genome_dict[pos_dict[x][0]][pos_dict[x][1]-1:pos_dict[x][2]]
    for g in pos_dict:
        s = genome_dict[pos_dict[g][0]][pos_dict[g][1]-1:pos_dict[g][2]]
        s.id = g
        s.name = ''
        s.description = ''
        records.append(s)
    SeqIO.write(records, outfasta, 'fasta')

if __name__ == '__main__':
    pos_dict = read_feature_pos(args.g, args.t)
    retrieve_seq(args.f, pos_dict, args.o)
