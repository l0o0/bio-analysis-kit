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
parser.add_argument('-l',help='sequence length, default is 2kb', type=int, default=2000)
parser.add_argument('-i',help='input a gene id list', 
		type=argparse.FileType('r'))
parser.add_argument('-G', type=argparse.FileType('r'),
		help='a GFF3 annotation file, default is Lin/Data/Cucumber_ref/gff3',
		default='/share/fg3/Linxzh/Data/Cucumber_ref/Cucumber_20101104.gff3')
parser.add_argument('-f', help="genome sequence file,default is /share/fg3/\
		Linxzh/Data/Cucumber_ref/origin/domestic_Chr_20101102.fa",
		default='/share/fg3/Linxzh/Data/Cucumber_ref/whole_genome/origin/domestic_Chr_20101102.fa',\
		type=argparse.FileType('r'))
parser.add_argument('-c', type=int, default=1, 
		help='specify the col number of input gene list,default is 1')
parser.add_argument('-o', help='output file name(fasta format by default',
		type=argparse.FileType('w'),default='output.fa') 
parser.add_argument('-r', help='''reverse_complement of the sequence if
		the strand is '-',default is true, valid parameter is T or F''',
		default='T', choices=['T','F'])
args=parser.parse_args()

start = time.clock()		#start a clock

# transfer the fasta file in a dict
def fa_to_dict(fa_file):
	fa_lists = fa_file.readlines()
	fa_dict = {}
	for i in range(0,len(fa_lists),2):
		key = fa_lists[i].split()[0][1:]
		fa_dict[key] = fa_lists[i+1]
	print 'Chromesome read complete!'	
	return fa_dict

#select gene id by col number
def select_gene(inputfile,gene_col):			#file input and gene col nm
	gene_list = []

	for x in inputfile:
		if 'Csa' not in x or x == '\n':
			continue
		x = x.split()[args.c -1]
		if 'M' not in x:
			x = x.replace('G','M')
			if ',' in x:
				x = x.split(',')
				gene_list += x
			else:
				gene_list.append(x)
		else:	
			gene_list.append(x)
	print '%s genes input.' % (len(gene_list))
	return gene_list		

#creat a dict,gene id as key, position as value
def pos(gff3):							#input gff3 file
	D = {}
	gene_id = 'test'

	for x in gff3:
		if 'CDS' in x and gene_id not in x:
			xlist = x.split()
			start = int(xlist[3])
			end = int(xlist[4])
			strand = xlist[6]
			gene_id = xlist[9].split('=')[1][:-2]
			chr_id = xlist[0]
			
			D[gene_id] = [start,end,strand,chr_id]
	return D

# find 2000 bp before the ATG
def promoter(chr_dict, pos_dict, reverse, output, gene_list, length):	
	n = 0	
	for gene in gene_list:
		start = pos_dict[gene][0]
		end = pos_dict[gene][1]
		gene_strand = pos_dict[gene][2]
		chr = chr_dict[pos_dict[gene][3]]

		if gene_strand == '+':
			gene_start = start
			gene_seq = chr[:-1][gene_start-length:gene_start]
		elif gene_strand == '-':
			gene_start = end
			gene_seq = chr[:-1][gene_start + 1:gene_start + length + 1]
			if reverse == 'T':
				gene_seq = reverse_complement(gene_seq)
				gene_strand += ' reverse_complement'

		n+=1
		output.write('>' + gene +' | ' + gene_strand + '\n' + gene_seq + '\n')
	print "%s genes found!" % n

	output.close()

if __name__ == '__main__':
	chr_dict = fa_to_dict(args.f)
	pos_dict = pos(args.G)
	gene_list = select_gene(args.i, args.c)
	promoter(chr_dict, pos_dict, args.r, args.o, gene_list, args.l)

	t = time.clock() - start		#time comsumed
	print 'Time: ' ,t				#print time consumed
