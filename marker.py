#!/usr/bin/env python 

import math
import sys


def chi_test(alist, tlist):
    if len(alist) == 2:
        f = lambda i : pow((abs(float(alist[i])-tlist[i])-0.5),2) / tlist[i]
        chi = f(0) + f(1)
        if chi >= 3.841:
            s = 'sig'
        else:
            s = 'No sig'
        return chi, 1, s
    else:
        f = lambda i : pow((float(alist[i])-tlist[i]),2) / tlist[i]
        chi = sum([f(j) for j in range(len(alist))])
        if chi >= 5.991:
            s = 'sig'
        else:
            s = 'No sig'
        return chi, 2, s


def segregation(seg, sampleNum):
    seg = seg.split('x')
    sega = seg[0][1:]
    segb = seg[1][:-1]
    seglist = [''.join(sorted(i + j)) for i in sega for j in segb]
    segfeq = [float(seglist.count(i))/len(seglist) * sampleNum for i in set(seglist)]
    return set(seglist), segfeq

if __name__ == '__main__':
    with open(sys.argv[1]) as handle:
        fl = handle.readlines()
        out = []
        for f in fl:
            flist = f.strip().split()
            marker = flist[0]
            seg = flist[1]
            seglist, segfeq = segregation(seg, 148)
            afeq = [flist[2:].count(i) for i in seglist]
            chi, df, sig = chi_test(afeq, segfeq)
            out.append('%s\t%5g\t%s\t%s\n' % (marker, chi, df, sig))

    with open(sys.argv[2], 'w') as handle:
        handle.writelines(out)


    
