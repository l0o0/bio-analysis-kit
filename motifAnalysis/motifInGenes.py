#!/bin/env python
# 2014-12-14	Linxzh

import argparse
import re
import sys

parse = argparse.ArgumentParser()
parse.add_argument('-i', type=argparse.FileType('r'), help='input file')
#parse.add_argument('-o', type=argparse.FileType('w'), help='output file')
args = parse.parse_args()

def motif_genes(infile):
	fl = infile.readlines()
	head = 85 * '_' + '\n'
	tail = 43 * '-' + '\n'

	try:
		start = fl.index(head)
		end = fl.index(tail)
	except ValueError:
		print infile
		sys.exit()

	pattern = re.compile(r'Csa([0-9]|UN)M[0-9]+')
	startLine = fl.index(head) + 1
	endLine = fl.index(tail) - 3
	
	for x in fl[:startLine]:
		out = pattern.search(x)
		if out:
			gene = out.group()

	motifList = []
	for i in fl[startLine:endLine]:
		il = i.split()
		motif = il[4]
		motifList.append(motif)
	motifList = list(set(motifList))	
	wl = '%s\t%s\n' % (gene,','.join(motifList))

	return wl

if __name__ == '__main__':
	outList = motif_genes(args.i)
	print outList
