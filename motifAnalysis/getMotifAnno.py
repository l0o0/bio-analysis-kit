#!/bin/env python
# 2014-12-17	Linxzh
#

import os
import urllib2
import re
import time

# get description from PLACE website
def get_description(accession):
	'''accession number plus prefix == website'''
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	userheader = {'User-Agent':user_agent}
	prefix = 'http://www.dna.affrc.go.jp/sigscan/disp.cgi?'
	url = ''.join((prefix,accession))
	req = urllib2.Request(url, None, userheader)
	htmltext = urllib2.urlopen(req, timeout=5).read()
	textlist = htmltext.split('\n')
	textlist = [x.split('   ')[1] for x in textlist if x.startswith('DE')]
	return ' '.join(textlist)

# get the html file
cwd = os.getcwd()
path='/share/fg3/Linxzh/Workspace/subject/dome/FpkmMax5/unmerged/moduleDist/Motif'
files = os.listdir(path)
files = [f for f in files if f.endswith('html')]


motif_acD = {}

for f in files:
	filename = '/'.join((path,f))
	with open(filename) as handle:
		fl = handle.readlines()
	
	header = 85 * '_' + '\n'
	tail = 43 * '-' + '\n'
	try:
		start = fl.index(header)
		end = fl.index(tail)
		motif_text = fl[start+1:end -3]

		for motifline in motif_text:
			lists = motifline.split()
			motif = lists[4]
			name = lists[0]
			if motif not in motif_acD:
				accession = re.search(r'S\d+', lists[-1]).group()
				description = get_description(accession)
				wl = '%s\t%s\t%s\t%s\n' % (motif, name,accession,description)
				motif_acD[motif]=wl
	except ValueError:
		print f
		continue

os.chdir(cwd)
with open('htmlresult.txt','w') as handle:
	handle.writelines(motif_acD.values())	 


	
