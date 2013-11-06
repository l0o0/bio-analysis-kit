#! /bin/env python
#Date: 2013-10-31
#Author: Linxzh
# add the annotation

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
	header = non_an[0][:-1] + 'Annotation\n'
else:	
	header = non_an[0][:-1] + '\t' + anno[0]

anno_dict = {}

for x in anno:
	xl = x.split('\t')
	id = xl[args.n -1].replace('P','G')[:-2]
	anno_dict[id] = x

for x in non_an:
	if 'Csa' not in x:
		continue
	id = x.split('\t')[args.m-1]
	if id in anno_dict:
		add = anno_dict[id]
	else:
		add = 'None'
	
	idx = non_an.index(x) 
	non_an[idx] = x[:-1] + '\t' + add 

args.o.write(header)
args.o.writelines(non_an[1:])
args.o.close()
args.i.close()
args.a.close()


