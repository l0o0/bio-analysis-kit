#!/usr/local/bin/python
# 2014-12-2	Linxzh

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input file')
parser.add_argument('-o', help='output file')
parser.add_argument('-d', help='distance * kb', type=int, default=10)
args = parser.parse_args()

# read gene-id from module 
def read_gene(infile):
	'''input file format:
	moduleName1
	Gene1 Gene2...
	moduleName2
	GeneA GeneB...'''

	D = {}
	
	with open(infile) as f:
		fl = f.readlines()

	for i in range(0,len(fl),2):
		genes = [x for x in fl[i+1].split() if 'UN' not in x] 	# fliter CsaUNxx
		D[fl[i]] = genes

	return D

# read gene--pos dictionary
def read_pos(infile):
	posD = {}

	with open(infile) as f:
		for line in f:
			lineList = line.split() 
			posD[lineList[3]] = int(lineList[1])

	return posD

# positional cluster
def cluster(D, posD, outfile, dist=10):
	'''D: input gene, {moduleName: gene1 gene2 ...}
	   posD: {geneID: start pos}'''

# cluster the genes by chromosome
	def genes_in_chrom(l):		# input genes list
		tmpD = {'1':[], '2':[], '3':[], '4':[], '5':[], '6':[], '7':[]}
		
		for i in l:
			tmpD[i[3]].append(i)

		return tmpD
# cluster the gene with '-', sep by ' | '
	def find_cluster(tmpD, posD):
		outList = []
		for k in tmpD.keys():
			geneList = tmpD[k]
			geneList = sorted(geneList, key=lambda g:posD[g])
			if not geneList:
				continue

			Marker=[]
			for i in range(len(geneList)-1):

				d = posD[geneList[i+1]] - posD[geneList[i]]
				
				if d <= dist * 1000:
					geneList[i] += '-'
				else:
					geneList[i] += ' | '

			newline = ''.join(geneList) + '\n'

			if '-' in newline:			# only need cluster genes
				outList.append(newline)


		return outList
	
	wl = []
	for (m,l) in D.items():
		tmpD = genes_in_chrom(l)
		outList = find_cluster(tmpD, posD)

		if outList:					# fliter empty out list
			wl.append(m)
			wl += outList

	with open(outfile,'w') as f:
		f.writelines(wl)

if __name__ == '__main__':
	D = read_gene(args.i)
	posD = read_pos('/share/fg3/Linxzh/Data/Cucumber_ref/genes_pos.txt')
	cluster(D, posD, args.o, args.d)			
