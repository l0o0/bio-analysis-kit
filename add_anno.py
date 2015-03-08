#! /bin/env python
#Date: 2013-10-31, last edit: 2014-11-21
#Author: Linxzh version = 0.1.3
#add the annotation

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-i", help = 'input a non annotation file',\
		type= argparse.FileType('r'))
parser.add_argument("-a", \
		help = "input an annotation file, default value is 1234.txt, support multi annotation file, -a anno1 -a anno2",\
		default = "/share/fg3/Linxzh/Data/Annotation/1234.txt")
parser.add_argument('-o', help = 'the output file', \
		type = argparse.FileType('w'))
parser.add_argument('-m',default = 1,\
		help='gene id col number of non annotation file, default is 1',\
		type=int)
parser.add_argument('-n',default = 1,\
		help='gene id col number of annotation file, default is 1',\
		type=int)
parser.add_argument('-s', default = '| ', type = str, help='seperate symbol')
args=parser.parse_args()


# creat a annotation dict
def an_2_dict(anno):
	'''convert the annotation list into a dict, gene id as key, anno as value'''

	anno_dict = {}
	annof = open(anno)
	for x in annof:

		if '#' in x:
			anno_dict['header'] = x

		xl = x.split('\t')
		gene_id = xl[args.n -1]

		if '.' in gene_id:
			gene_id = xl[args.n -1].split('.')[0]

		gene_id = re.sub('[PM]', 'G', gene_id)
		anno_dict[gene_id] = x.strip()

	if 'header' not in anno_dict:
		print 'You need a header line!'

	return anno_dict

# gene_id corresponding to the annotation
def add_anno(infile, anno_dict, sep, m):
	'''for every item of the input list, add the annotation at the end of the line'''
	
	def match_gene(add, gene, anno_dict, tmpD, sep):
		if gene in anno_dict:
			add = add + sep + anno_dict[gene]
		else:
			add = add + sep + 'None\n'

		tmpD[gene] = add
		return tmpD
	
	tmpD = {}
	
	if isinstance(infile,file):		# infile is a file
		for x in infile:
			add = ''
			if x=='\n':
				continue
			elif '#' in x:						# add header
				add = x.replace('\n', '\t') + anno_dict['header']
				tmpD['header'] = add
				continue

			gene = x.split()[m-1]
			gene = re.sub('[MP]', 'G', gene)
			gene = gene.split('.')[0]
			tmp = match_gene(add,gene, anno_dict, tmpD, sep)
	elif isinstance(infile, dict):		# infile is a dict
		print 'dict'
		for k,v in infile.items():
			tmpD = match_gene(v,k, anno_dict, tmpD, sep)

	return tmpD

def write_dict(tmpD, outfile):
	wl = ['%s\t%s\n' % (k,v.strip()) for k,v in tmpD.items()]
	outfile.writelines(wl)


if __name__ == '__main__':
	print type(args.a)
	print args.a
	if isinstance(args.a, str):
		anno1 = an_2_dict(args.a)
		all_D = add_anno(args.i, anno1, args.s, args.m)
	else:
		anno1 = an_2_dict(args.a[0])
		all_D = add_anno(args.i, anno1, args.s, args.m)
		for i in args.a[1:]:
			annoi = an_2_dict(i)
			all_D = add_anno(all_D, annoi, args.s, args.m)

	write_dict(all_D, args.o)
