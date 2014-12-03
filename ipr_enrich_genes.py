#!/bin/python
# 2014-11-3	Linxzh

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input file')
parser.add_argument('-p', help='ipr enrich output')
parser.add_argument('-o', help='output file')
args=parser.parse_args()

def to_set(infile):
	with open(infile,'r') as f:
		fl = f.readlines()
		fl = [x.strip() for x in fl]
		fl_set = set(fl)
		return fl_set


def sel_ipr(infile):
	ipr_list = []
	with open(infile) as f:
		for fl in f:

			if 'IPR-id' in fl:
				continue
			
			fls = fl.split('\t')
			ipr = fls[0]
			
			if float(fls[6]) <= 0.05:
				ipr_list.append(ipr)

		return ipr_list

def ipr_dict(infile):
	D = {}
	with open(infile) as f:
		for fl in f:
			fl_list = fl.split('\t')
			gene = fl_list[0][:-2].replace('P','G')
			tmp = fl_list[1].split()
			iprs = [x for x in tmp if 'IPR' in x]
			
			for ipr in iprs:
				if ipr not in D:
					D[ipr] = [gene]
				else:
					D[ipr].append(gene)

		return D


def final_step(ipr_list, D, sample_set, outfile):
	out = open(outfile,'w')

	for ipr in ipr_list:
		ipr_genes_set = set(D[ipr])
		g_set_ipr = '\t'.join(D[ipr])
		s_set_ipr = '\t'.join(ipr_genes_set & sample_set)

		out.write(ipr + '\n')
		out.write(g_set_ipr + '\n')
		out.write(s_set_ipr + '\n')
	out.close()

if __name__ == '__main__':

	M_set = to_set(args.i)
	M_sel_ipr = sel_ipr(args.p)
	D = ipr_dict('/share/fg3/Linxzh/Data/Annotation/domestic.ipr.txt')

	final_step(M_sel_ipr, D, M_set, args.o)





