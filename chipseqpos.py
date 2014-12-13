#!/bin/env python
# 2014-12-11 Linxzh

import argparse
import time
import re
import sys

parse = argparse.ArgumentParser()
parse.add_argument('-i', help='input')
parse.add_argument('-o', help='output')
args = parse.parse_args()

# read feature pos from gff file
def pos_D(posfile):
	D = {}
	f = open(posfile)
	for x in f:

		if 'mRNA' in x or 'CDS' in x or x =='\n':
			continue

		xl = x.split()
		chrom = xl[0]
		start = int(xl[3])
		end = int(xl[4])

		values = re.split('\t|\.|=|,|;', xl[8])
		gene = values[1].replace('M','G')
		if chrom not in D:
			D[chrom] = {}
		
		if gene not in D[chrom]:
			D[chrom][gene] = {}

		if 'gene' in x:
			D[chrom][gene]['gene'] = (start, end)
			D[chrom][gene]['Up3k'] = (start-3000, start -1)
			continue

		feature = values[3]
		D[chrom][gene][feature] = (start, end)
	
	return D

# detect the features in the peak pos
def det_fea(peak_pos, geneD):
	'''peak_pos = [int(start), int(end)]
	   geneD ={'gene':(intS,intE), 'exon1':(intS,intE)...}'''
	out = {}
	
	for gene,feaD in geneD.items():
	
		for fea,pos in feaD.items():
			if pos[0] < peak_pos[0] < pos[1] or pos[0] < peak_pos[1] < pos[1]:

				if gene not in out:
					out[gene] = []
				
				out[gene].append(fea)

	return out

# read the peak file
def locate(infile, outfile):
	D = pos_D('/share/fg3/Linxzh/Data/Cucumber_ref/Cucumber_20101104.gff3')

	f = open(infile)
	o = open(outfile,'w')
	tmp = []
	for x in f:
		
		if x.startswith('#') or x.startswith('"') or not x.strip():
			continue
		elif 'fold_enrichment' in x:
			wl = x.replace('#NAME?','-10*LOG10(pvalue)')
			wl = '#%s\t%s\t%s\n' % (wl.strip(), 'gene','features')
			tmp.append(wl)
			continue

		xl = x.split()
		st = int(xl[1])
		ed = int(xl[2])
		chrom = xl[0]

		try:
			geneD = D[chrom]
			res = det_fea([st, ed], geneD)
			if res:
#				print res
				for gene in res:
					wl =  '%s\t%s\t%s\n' % (x.strip(), gene, '+'.join(res[gene]))
					tmp.append(wl)
		except KeyError:
			print chrom
	
	o.writelines(tmp)

if __name__ == '__main__':
	a = time.time()
	tmp = locate(args.i, args.o)
	b = time.time()
	print b-a	
