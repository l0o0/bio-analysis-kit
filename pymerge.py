#!/usr/bin/python
# create by linxzh at 2014-8-19

import argparse
import re
import sys

parser = argparse.ArgumentParser('pymerge')
parser.add_argument('-A', type=argparse.FileType('r'))
parser.add_argument('-B', type=argparse.FileType('r'))
parser.add_argument('-Aby', type=int, default=1, 
        help='key col of -A file, default is 1')
parser.add_argument('-Bby', type=int, default=1, 
        help='key col of -B file, default is 1')
parser.add_argument('-Acol', type=str, help ='to be merged cols')
parser.add_argument('-Bcol', type=str, help ='to be merged cols')
parser.add_argument('-s', type=str, choices=['all','a','b','ab'],
        default='all', help ="all = union, a = by -A items,\
        b = by -B items, ab = a intersect with b, default is \
        all(union). None exits field is filled with '--'")
parser.add_argument('-Out', type=argparse.FileType('w'))
parser.add_argument('-Sep', type=str, default='\t', 
        help='field delimiter, default is TAB')
parser.add_argument('-H', type=int, default=1, 
        help='line num of head line, default is 1')
parser.add_argument('-F', type=argparse.FileType('r'), 
        help='file contains a filelist to be merged')
args=parser.parse_args()


def get_col(flist, cols):
    colslist = re.split(',|-', cols)
    if '' in colslist:
        out = flist[int(colslist[0])-1:]
    elif '-' in cols:
        out = flist[int(colslist[0])-1:int(colslist[1])]
    else:
        out = [flist[int(x)-1] for x in colslist]
    return out

# read data to dict
def read_data(infile, bycol, cols, sep, h):
    '''bycol is the arg specified by -Aby / -Bby
        cols specified by -Acol / -Bcol
        return a dict:
        {bycol : [target cols] ... }'''
    if isinstance(infile, str):
        infile = open(infile)
    D = {}
    c = 1

    for f in infile:
        flist = f.strip().split(sep)
        k = flist[bycol-1]
        v = get_col(flist, cols)

        if c == h:
            hk = 'header'
            D[hk] = v       
        else:
            D[k] = v

        c += 1

    return D


# 
def merge_dict(D1, D2, s):
    '''D1 as primary'''
    D = {}
    D1len = len(D1[D1.keys()[0]])
    D2len = len(D2[D2.keys()[0]])

    if s == 'all':
        kset = set(D1.keys()) | set(D2.keys())
    elif s == 'a':
        kset = D1.keys()
    elif s == 'b':
        kset = D2.keys()
    elif s == 'ab':
        kset = set(D1.keys()) & set(D2.keys())

    for k in kset:
        if k in D1 and k in D2 and k != 'header':
            v = D1[k] + D2[k]
        elif k in D1 and k not in D2:
            empty = ['--']*D2len
            v = D1[k] + empty
        elif k not in D1 and k in D2:
            empty = ['--'] * D1len
            v = empty + D2[k]
        D[k] = v

    D['header'] = D1['header'] + D2['header']
    return D


# 
def reduce_merge_dict(F, bycol, cols, sep, h, s):
    filelist = F.readlines()
    filelist = [x.strip() for x in filelist]
    tmp = map(lambda x : read_data(x, bycol, cols, sep, h), filelist)
    D = reduce(lambda x, y : merge_dict(x, y, s), tmp)
    return D

if __name__ == '__main__':
   
    if args.F:
        D = reduce_merge_dict(args.F, args.Aby, args.Acol, args.Sep, args.H, args.s)
    else:
        D1 = read_data(args.A, args.Aby, args.Acol, args.Sep, args.H)
        D2 = read_data(args.B, args.Bby, args.Bcol, args.Sep, args.H)
        D = merge_dict(D1,D2, args.s)

    outline = []
    header = 'Name\t%s\n' %  ('\t'.join(D['header']))
    outline.append(header)
    del D['header']
    for k in D:
        line = '%s\t%s\n' % (k, '\t'.join(D[k]))
        outline.append(line)
    args.Out.writelines(outline)
