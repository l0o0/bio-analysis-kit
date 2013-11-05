#!/usr/bin/env python
#Date: 2013-11-4
#Author: Linxzh
#splice a sequence before a ATG start codon

import time
import argparse
from Bio.Seq import reverse_complement

#specify the arguments
parser = argparse.ArgumentParser(description='Find the promoter sequence',
		prog='Promoter Finder', usage='PROG [options]')
parser.add_argument('-i',help='input a gene id list', 
		type=argparse.FileType('r'))
parser.add_argument('-G', type=argparse.FileType('r'),
		help='a GFF3 annotation file, default is Lin/Data/Cucumber_ref/gff3',
		default='/share/fg3/Linxzh/Data/Cucumber_ref/Cucumber_20101104.gff3')
parser.add_argument('-f', help="genome sequence file,default is /share/fg3/Linxzh/Data/Cucumber_ref/domestic_Chr_20101102.fa",
		default='/share/fg3/Linxzh/Data/Cucumber_ref/domestic_Chr_20101102.fa',type=argparse.FileType('r'))
parser.add_argument('-c', type=int, default=1, 
		help='specify the col number of input gene list,default is 1')
parser.add_argument('-o', help='output file name(fasta format by default',
		type=argparse.FileType('w'),default='output.fa') 
parser.add_argument('-r', help='''reverse_complement of the sequence if
		the strand is '-',default is false, valid parameter is T or F''',
		default='F', choices=['T','F'])
args=parser.parse_args()

start = time.clock()		#start a clock

# transfer the fasta file in a dict
def fa_to_dict(fa_file):
	fa_lists = fa_file.readlines()
	fa_dict = {}

	for i in range(0,13,2):
		key = fa_lists[i].split('\t')[0][1:]
		print key
		fa_dict[key] = fa_lists[i+1]
	return fa_dict

gen_dict = fa_to_dict(args.f)

#select gene id by col number
gene_list = args.i.readlines()
gene_list = [x.split()[args.c -1] for x in gene_list]		
print gene_list

# find 2000 bp before the ATG
for gff_line in args.G:
	
	for gene in gene_list:
		
		if 'Chr' in gff_line and 'cds1;' in gff_line and gene in gff_line:
#			print gene
			gff_split = gff_line.split('\t')
			chr_id = gff_split[0]
			gene_strand = gff_split[6]
		
			if gene_strand == '+':
				gene_start = int(gff_split[3])
				gene_seq = gen_dict[chr_id][:-1][gene_start-2000:gene_start]
			elif gene_strand == '-':
				gene_start = int(gff_split[4])
				gene_seq = \
				gen_dict[chr_id][:-1][gene_start + 1:gene_start + 2001]
				if args.r == 'T':
					gene_seq = reverse_complement(gene_seq)
					gene_strand += ' reverse'

			gene_id = gff_split[-1].split(';')[0][3:]
			args.o.write('>' + gene +' | ' + gene_strand + '\n' + gene_seq + '\n')

args.o.close()
t = time.clock() - start		#time comsumed
print 'Time: ' ,t				#print time consumed
