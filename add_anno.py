#! /bin/env python
#Date: 2013-10-31, last edit: 2014-11-21
#Author: Linxzh version = 0.1.3
#add the annotation

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-i", help = 'input a non annotation file',\
		type= argparse.FileType('r'))
parser.add_argument("-a", help = "input an annotation file, default value is 1234.txt", type = argparse.FileType('r'),\
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
def an_2_dic(anno):
	'''convert the annotation list into a dict, gene id as key, anno as value'''

	anno_dict = {}

	for x in anno:

		if '#' in x:
			anno_dict['header'] = x

		xl = x.split('\t')
		gene_id = xl[args.n -1]

		if '.' in gene_id:
			gene_id = xl[args.n -1].split('.')[0]

		gene_id = re.sub('[PM]', 'G', gene_id)
		anno_dict[gene_id] = x

	if 'header' not in anno_dict:
		print 'You need a header line!'

	return anno_dict

# gene_id corresponding to the annotation
def add_anno(infile, outfile, anno, sep, m):
	'''for every item of the input list, add the annotation at the end of the line'''

	anno_dict = an_2_dic(anno)		# anno file to dict
	tmp = []

	for x in infile:
		add = ''
		
		if x=='\n':
			continue
		elif '#' in x:						# add header
			add = x.replace('\n', '\t') + anno_dict['header']
			tmp.append(add)
			continue

		gene = x.split()[m-1]
		gene = re.sub('[MP]', 'G', gene)

		if '.' in gene:
			gene = gene[:-2]

		if gene in anno_dict:			# add anno if gene in an-dict
			add = add + sep + anno_dict[gene]
		else:
			add = add + sep + 'None\n'

		add = '%s\t%s' % (x[:-1], add)
		tmp.append(add)
		add = ''
	
	outfile.writelines(tmp)

if __name__ == '__main__':
	add_anno(args.i, args.o, args.a, args.s, args.m)
	args.o.close()
	args.i.close()
	args.a.close()
