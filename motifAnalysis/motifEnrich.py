#!/bin/env python
# 2014-12-15	Linxzh
# script for my own article
# motif enrichment analysis for genes in one module

import argparse
from fisher import pvalue

parse = argparse.ArgumentParser()
parse.add_argument('-i', type=argparse.FileType('w'), help='input file')
args = parse.parse_args()

# summary the motif number 
def motif_count(motif_list):
	'''motif count in the input list'''
	D = {}
	uni_list = set(motif_list)

	for motif in uni_list:
		c = motif_list.count(motif)
		D[motif]=c
	
	return D


# fisher exact test 
def fisher_test(countList):
	'''countList = [A,B,C,D]
	  ________________|_ALL_|_Module |___
	  Genes_have_motif|_B___|_D______|___
	  ___not_have_____|_A-B_|_C-D____|___
      ________________|_A___|_C______|___  '''
	
	a = countList[1]
	b = countList[3]
	c = countList[0] - a
	d = countList[2] - b

	p = pvalue(a,b,c,d)
	return p.right_tail
			

# read mapping file 
def read_mapping(infile, dot=False):
	'''gene to motif mapping file to dict:
	gene1	motifA,motifB,...
	gene2	motifA,motifB,motifC,...
	...								
	dict like : {gene1:[motifA,motifB...],
	gene2:[motifA,motifB,motifC...],...'''
	with open(infile) as f:
		fl = f.readlines()

	D = {}
	for i in fl:
		ilist = i.split()
		k = ilist[0]
		v = ilist[1]
		v = v.split(',')
		if dot:
			v = [x.split('.')[0] for x in v]
		D[k] = v
	return D
	
# read module data 
def read_module(tissus_module):
#	tissue_module = '/share/fg3/Linxzh/Workspace/subject/dome/FpkmMax5/unmerged/moduleDist/module_tissue_p65.txt'
	
	tissue_moduleD = {}
	with open(tissus_module) as f:
		for i in f:
			ilist = i.split()

			if ilist[1] not in tissue_moduleD:
				tissue_moduleD[ilist[1]] = []
			
			tissue_moduleD[ilist[1]].append(ilist[3])
	
	return tissue_moduleD

# motif in modules, return a motif list
def motif_in_module(module, module_geneD, D):
	genes = module_geneD[module]
	motif_list = reduce(lambda x,y: x+y, [D[g] for g in genes])
	return motif_list

# write out the result
def writeout(tissue, out):
	outfile = ''.join((tissue,'_motifEnrichment.txt'))
	with open(outfile, 'w') as f:
		f.writelines(out)


# enrichment analysis
def motif_enrich(D, tissue_moduleD, module_geneD):
	all_motif_countD = motif_count(reduce(lambda x,y:x+y,D.values()))
	all = len(D)	# gene num in total

	for t,modules in tissue_moduleD.items():	# every tissue
		out = []
		for m in modules:						# every module in tissue
			out.append(m+'\n')
			sample_motif_countD = motif_count(motif_in_module(m, module_geneD, D))
			sample = len(module_geneD[m])	# gene num in module
			for motif in sample_motif_countD:
				countList = [all,all_motif_countD[motif],sample,sample_motif_countD[motif]]
				p = fisher_test(countList)
				outline = '--%s\t%s\t%s\n' % (motif, ','.join([str(j) for j in countList]), p)
				out.append(outline)
		
		writeout(t, out)
			
if __name__ == '__main__':
	D = read_mapping('/share/fg3/Linxzh/Workspace/subject/dome/FpkmMax5/unmerged/moduleDist/motifsInGenes.txt')
	tissue_moduleD = read_module('/share/fg3/Linxzh/Workspace/subject/dome/FpkmMax5/unmerged/moduleDist/module_tissue_p65.txt')
	module_geneD = read_mapping('/share/fg3/Linxzh/Workspace/subject/dome/FpkmMax5/unmerged/moduleDist/genesInMotif.txt', True)
	motif_enrich(D, tissue_moduleD, module_geneD)
	

	


