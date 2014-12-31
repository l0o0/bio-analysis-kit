#!/bin/env python
# 2014-12-28	Linxzh
# get motif accession html from PLACE

import urllib2

def get_html(accession, outpath):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	userheader = {'User-Agent':user_agent}
	prefix = 'http://www.dna.affrc.go.jp/sigscan/disp.cgi?'
	url = ''.join((prefix,accession))
	req = urllib2.Request(url, None, userheader)
	htmltext = urllib2.urlopen(req, timeout=10).read()
	outhtmlname = ''.join((outpath,accession,'.txt'))
	outhtml = open(outhtmlname,'w')
	outhtml.write(htmltext)
	outhtml.close()

def get_item(filedir, accession, itemName):
	filename = ''.join((filedir, accession,'.txt'))
	with open(filename) as handle:
		handlelist = handle.readlines()
		targetline = [x for x in handlelist if x.startswith(itemName)]
		if targetline:
			item = targetline[0].split('   ')[1]
			item = item.strip()
		else:
			item = 'None'
	return item


if __name__ == '__main__':
	path = 'MotifAccessionHtml/'
	infile = 'htmlresult.txt'
	with open(infile) as handle:
		for f in handle:

			if f.startswith('#'):
				continue

			flist = f.split('\t')
			accession = flist[2]
			get_html(accession, path)

