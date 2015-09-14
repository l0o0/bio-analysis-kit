# coding: utf-8

# 每个循环只提交一个序列，每个序列产生一个HTML文件，再从HTML结果中
# 整理得到结果


import urllib2
import re
import os
import argparse
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

parser = argparse.ArgumentParser()
parser.add_argument('-fa', help='promoter seq file', 
        type=argparse.FileType='r')
parser.add_argument('-outdir', help='output dir', type=str, default='htmlresult')
args = parser.parse_args()


def upload_analysis(fa, outdir):
    os.path.exists(outdir) and pass or os.mkdir(outdir)
    register_openers()
    f = openfa.readlines()
#    sepline = '____________________________________________________________________________'
    url = 'https://sogo.dna.affrc.go.jp/cgi-bin/sogo.cgi?sid=&lang=en&pj=640&action=page&page=newplace'
    
    for i in range(0, len(f), 2):
        query_id = f[i]
        result_html = '%s/%s.html' % (outdir, query_id)   
        data = {'query_seq':'\n'.join(f[i:i+2]), 'action':'newplace', 'sid':'', 'pj':'640',"style":'html'}
        datagen, header = multipart_encode(data)
        request = urllib2.Request(url, datagen, header)
        htmltext = urllib2.urlopen(request).read()
# write analysis result in html
        with open(result_html) as handle:
            handle.write(htmltext)
            
#        htmllines = htmltext.split('\n')
#        targetlines = htmllines[htmllines.index(sepline)+1:-6]

if __name__ == '__main__':
    upload_analysis(args.fa, args.outdir)
