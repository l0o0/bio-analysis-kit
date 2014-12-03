#!/bin/python
# 2014-11-4	Linxzh
# retrive gene seq for genome seq by gene id

import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description='Retrive gene sequence by gene id', prog='SeqGeter', usage='PROG [options]')

parser.add_argument('-i', help='file contains gene ids')
parser.add_argument('-o', help='output file in fasta format', type=argparse.FileType('w'))
parser.add_argument('-c', help='column of gene id, default is 1', type=int, default=1)
parser.add_argument('-g', help="format gene id as 'Csa1G000111', default is FALSE'", default='F', choices=['T', 'F'])
args = parser.parse_args()


def pos_dict(infile):
	D={}
	with open(infile) as f:
		for fl in f:
			if 'gene' in fl:
				fl_list = fl.split()
				chrom = fl_list[0]
				geneid = fl_list[8].split(';')[0][3:]
				start = int(fl_list[3]) - 1 
				end = int(fl_list[4])
				D[geneid] = [chrom, start, end]

	return D


def read_id(infile, c=1, g='F'):
	gene_list = []
	with open(infile) as f:
		for fl in f:
			if '#' in fl:
				continue
			elif 'Csa' not in fl:
				continue
			elif fl == '\n':
				continue

			fl_list = fl.split()
			gene = fl_list[c-1]

			if g == 'T':
				gene = gene.split('.')[0]
				gene = gene.replace('P','G')
				gene = gene.replace('M','G')
			
			gene_list.append(gene)
	
	return gene_list


def get_seq(gene_list, outfile):
	D = pos_dict('/share/fg3/Linxzh/Data/Cucumber_ref/Cucumber_20101104.gff3')
	fa_dict = SeqIO.to_dict(SeqIO.parse('/share/fg3/Linxzh/Data/Cucumber_ref/whole_genome/origin/domestic_Chr_20101102.fa','fasta'))

	for gene in gene_list:
		seq = str(fa_dict[D[gene][0]][D[gene][1]:D[gene][2]].seq)
		wl = '>%s\n%s\n' % (gene, seq)
		outfile.write(wl)

	outfile.close()

if __name__ == '__main__':
	gene_list = read_id(args.i, c = args.c, g = args.g)
	get_seq(gene_list, args.o)
