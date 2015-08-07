#!/bin/env python
# 2014-12-28	Linxzh
# Modified: 2015-7-13
# get motif accession html from PLACE

import urllib2
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p', help='output folder')
parser.add_argument('-i', help='input file, accession2genes.txt')
args = parser.parse_args()


def get_html(accession, outpath):
    '''download description from PLACE by accession,
       save it as text.'''

    if not outpath.endswith('/'):
        outpath = outpath + '/'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    userheader = {'User-Agent': user_agent}
    prefix = 'http://www.dna.affrc.go.jp/sigscan/disp.cgi?'
    url = ''.join((prefix, accession))
    req = urllib2.Request(url, None, userheader)
    htmltext = urllib2.urlopen(req, timeout=10).read()
    outhtmlname = ''.join((outpath, accession, '.txt'))
    outhtml = open(outhtmlname, 'w')
    outhtml.write(htmltext)
    outhtml.close()


def get_item(filedir, accession, itemName):
    filename = ''.join((filedir, accession, '.txt'))
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
    if not os.path.exists(args.p):
        os.mkdir(args.p)
        print "Create folder: %s" % args.p

    path = args.p
    infile = args.i
    with open(infile) as handle:
        for f in handle:

            if not f.startswith('S'):
                continue

            flist = f.split('\t')
            accession = flist[0]	# 1st col as accession 
            get_html(accession, path)
