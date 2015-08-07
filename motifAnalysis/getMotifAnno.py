#!/bin/env python

import os
import urllib2
import re
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-p', help='input folder')
parser.add_argument('-o1', help='output file, accession to many genes')
parser.add_argument('-o2', help='output file, gene to many accessions')
args=parser.parse_args()


def get_description(accession):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	userheader = {'User-Agent':user_agent}
	prefix = 'http://www.dna.affrc.go.jp/sigscan/disp.cgi?'
	url = ''.join((prefix,accession))
	req = urllib2.Request(url, None, userheader)
	htmltext = urllib2.urlopen(req, timeout=5).read()
	textlist = htmltext.split('\n')
	textlist = [x.split('   ')[1] for x in textlist if x.startswith('DE')]
	return ' '.join(textlist)

def motif_anno(path, output1, output2):
	files = os.listdir(path)
	files = [f for f in files if f.endswith('html')]
	motif_acD = {}
	gene_acsD = {}
	cwd = os.getcwd()
	acs = []

	for f in files:
		filename = '/'.join((path,f))
		with open(filename) as handle:
			fl = handle.readlines()
		header = 85 * '_' + '\n'
		tail = 43 * '-' + '\n'
		gene = re.split(";|\|", fl[9])[1]

		start = fl.index(header)
		end = fl.index(tail)
		motif_text = fl[start+1:end -3]

		for motifline in motif_text:
			lists = motifline.split()
			motif = lists[4]
			name = lists[0]
			accession = re.search(r'S\d+', lists[-1]).group()
			acs.append(accession)

			if motif not in motif_acD:
				description = get_description(accession)
				wl = [accession, name, motif, description] 
				motif_acD[motif] = wl
#			print wl, gene
			motif_acD[motif].append(gene)

		gene_acsD[gene] = acs
		acs = []

	os.chdir(cwd)

	with open(output1,'w') as handle:
		header = '%s\t%s\t%s\t%s\t%s\n' % ('accession', 'name', 'pattern', 'description', 'genes')
		handle.write(header)
		for l in motif_acD.values():
			line = '%s\t%s\n' % ('\t'.join(l[:4]), ','.join(set(l[4:]))) 
			handle.writelines(line)

	with open(output2, 'w') as handle:
		header = '%s\t%s\n' % ('Gene', 'Accessions')
		handle.write(header)
		lines = ['%s\t%s\n' % (x, ','.join(set(y))) for x, y in gene_acsD.items()]
		handle.writelines(lines)


if __name__ == "__main__":
	motif_anno(args.p, args.o1, args.o2)
