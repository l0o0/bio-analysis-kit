#! /bin/env python
#Date: 2013-10-31, last edit: 2013-12-20
#Author: Linxzh version = 0.1.2
#add the annotation

import argparse

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
args=parser.parse_args()


# creat a annotation dict
def an_2_dic(anno, point='yes'):
	'''convert the annotation list into a dict, gene id as key, anno as value'''

	anno_dict = {}

	for x in anno:
		xl = x.split('\t')
		if point == 'yes':
			gene_id = xl[args.n -1].replace('P','M')
		elif point =='no':
			gene_id = xl[args.n -1].replace('P','M')[:-2]
		anno_dict[gene_id] = x

	return anno_dict

# gene_id corresponding to the annotation
def add_anno(infile, outfile, anno):
	'''for every item of the input list, add the annotation at the end of the line'''

	non_an = infile.readlines()
	if 'Csa' not in non_an[0]:				# create a header for output
		header = '%s\t%s\n' % (non_an[0][:-1],'Annotation')
		outfile.write(header)
		check_p = non_an[1].split()[0]
		if '.' in check_p:
			point = 'yes'
		else:
			point = 'no'
	else:	
		check_p = non_an[0].split()[0]			# check '.' in gene_id
		if '.' in check_p:
			point = 'yes'
		else:
			point = 'no'

	anno_dict = an_2_dic(anno,point)		# anno file to dict

	for x in non_an:
		add = ''
		if 'Csa' not in x:					# exclude the non-gene row
			continue

		gene_ids = x.split()[args.m-1].split(',')

		for gene in gene_ids:				# if ',' in gene row
			gene = gene.strip()

			if 'M' not in gene:
				a = gene[4]
				gene = gene.replace(a,'M')	# replace 'P' or 'G' to 'M'

			if gene in anno_dict:			# add anno if gene in an-dict
				add = add + ' |' + anno_dict[gene][:-1]
			else:
				add = add + ' |' + 'None'

		add += '\n'
		idx = non_an.index(x)
		non_an[idx] = x.replace('\n','\t') + add
	
	outfile.writelines(non_an[1:])

if __name__ == '__main__':
	add_anno(args.i, args.o, args.a)
	args.o.close()
	args.i.close()
	args.a.close()
