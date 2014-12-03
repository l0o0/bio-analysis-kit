#!/bin/env python
# 2014-5-6	Linxzh

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help = 'input file', type = argparse.FileType('r'))
parser.add_argument('-o', help = 'output file', type = argparse.FileType('w'))
args = parser.parse_args()


# fpkm line cache
def fpkm_line(in_file, out_file):
	for l in in_file:
		llist = l.split()
		frag = llist[2]
		fpkm = llist[13][1:-4]
		id = llist[11][1:-4].replace('M','G')
		
		if frag == 'transcript' and 'Csa' in l:
			out_file.write(id + '\t' + fpkm + '\n')


if __name__ == '__main__':
	fpkm_line(args.i, args.o)
