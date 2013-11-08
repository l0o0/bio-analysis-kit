#! /bin/env python
#Date: 2013-10-31
#Author: Linxzh version = 0.1.1
#add the annotation

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", help = 'input a non annotation file', type= argparse.FileType('r'))
parser.add_argument("-a", help = "input an annotation file", type = argparse.FileType('r'))
parser.add_argument('-o', help = 'the output file', type = argparse.FileType('w'))
parser.add_argument('-m',help='gene id col number of non annotation file',type=int)
parser.add_argument('-n',help='gene id col number of annotation file', type=int)
args=parser.parse_args()

non_an = args.i.readlines()
anno = args.a.readlines()
result = []

#create a header
if 'Csa' in anno[0]:
	header = '%s\t%s\n' % (non_an[0][:-1],'Annotation')
else:	
	header = '%s\t%s\n' % (non_an[0][:-1],anno[0])

#creat a annotation dict
anno_dict = {}

for x in anno:
	xl = x.split('\t')
	gene_id = xl[args.n -1].replace('P','G')[:-2]
	anno_dict[gene_id] = x

#gene_id corresponding to the annotation

for x in non_an:
	add = ''
	if 'Csa' not in x:					#exclude the non-gene row
		continue

	gene_ids = x.split('\t')[args.m-1].split(',')

	for gene in gene_ids:				#if ',' in gene row
		if gene in anno_dict:
			add = add + ' |' + anno_dict[gene][:-1]			
		else:
			add = add + ' |' + 'None'
	add += '\n'		
	idx = non_an.index(x) 
	non_an[idx] = x.replace('\n','\t') + add 

args.o.write(header)
args.o.writelines(non_an[1:])
args.o.close()
args.i.close()
args.a.close()


