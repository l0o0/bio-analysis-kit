#!/bin/env python
# 2014-11-28	Linxzh
# according to the gene position in the genome, draw the cluster

import argparse
import svgwrite
from svgwrite import cm,mm

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input file')
parser.add_argument('-o', help='output file')
args = parser.parse_args()

chr_len = {'Chr1':29149675, 'Chr2':23174626, 'Chr3':39782674, 
		'Chr4':23425844, 'Chr5':28023477, 'Chr6':29076228,
		'Chr7':19226500}

# draw 7 chromosome line
def chromesome_line(draw):
	for i in range(1,8):
		chrom = 'Chr' + str(i)
		x1, y1 = 1*cm, (2 + i * 1.5)*cm
		x2, y2 = (1 + chr_len[chrom] / 1000000.0)*cm, y1
		draw.add(draw.line(start=(x1, y1), end=(x2, y2), stroke ='black', stroke_width = 0.25*mm))
	return draw

# read genes pos into dict
def pos_to_dict(infile):
	Chr1 = Chr2 = Chr3 = Chr4 = Chr5 = Chr6 = Chr7 = []
	with open(infile) as f:
		

# draw all genes' start positions
def all_gene(draw):
#	with open('/share/fg3/Linxzh/Tmp/tmp.txt') as f:
#	with open('/share/fg3/Linxzh/Data/Cucumber_ref/genes_pos.txt') as f:
		fl = f.readlines()

	pos = [x.split()[:2] for x in fl]
#	print pos
	for p in pos:
		chrom = int(p[0][-1])
		position = int(p[1])
		x1, y1 = (1 + position / 1000000.0), (2 + chrom * 1.5 - 0.2)
		x2, y2 = x1, (2 + chrom * 1.5 + 0.2)
		draw.add(draw.line(start=(x1*cm, y1*cm), end=(x2*cm, y2*cm), stroke='blue', stroke_width = 0.05 *mm))
#		print position / 1000000.0
	return draw

# draw cluster genes as a single line
def clust_line(draw, pos_list):
	Chr1 = Chr2 = Chr3 = Chr4 = Chr5 = Chr6 = Chr7 = []
	for p in pos_list:


	

if __name__ == '__main__':
	dwg = svgwrite.Drawing(filename='test.svg', size =(45*cm, 15*cm))
	chromesome_line(dwg)
	all_gene(dwg)
	dwg.save()
