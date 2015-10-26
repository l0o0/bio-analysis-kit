#!/usr/bin/env python 

import math
import sys



def chi_test(alist, tlist, pvalue):
    
    chi_values = {'0.05':[3.84,5.99], '0.01': [6.63,9.21], '0.005':[7.88,10.6],
                  '0.1':[2.71,4.61], '0.25':[1.32,2.77]}

    if len(alist) == 2:
        f = lambda i : pow((abs(float(alist[i])-tlist[i])-0.5),2) / tlist[i]
        chi = f(0) + f(1)
        if chi >= chi_values[pvalue][0]:
            s = 'sig'
        else:
            s = 'No sig'
        return chi, 1, s
    else:
        f = lambda i : pow((float(alist[i])-tlist[i]),2) / tlist[i]
        chi = sum([f(j) for j in range(len(alist))])
        if chi >= chi_values[pvalue][1]:
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
    sample_num = 148
    with open(sys.argv[1]) as handle:
        fl = handle.readlines()
        out = []
        filtered = []
        for f in fl[5:(len(fl)-sample_num -2)]:
            flist = f.strip().split()
            marker = flist[0]
            seg = flist[1]
            seglist, segfeq = segregation(seg, 148)
            afeq = [flist[2:].count(i) for i in seglist]
            chi, df, sig = chi_test(afeq, segfeq, sys.argv[4])
            if sig == 'No sig':
                filtered.append(f)
            out.append('%s\t%5g\t%s\t%s\n' % (marker, chi, df, sig))

    with open(sys.argv[2], 'w') as handle:
        handle.writelines(out)
    with open(sys.argv[3], 'w') as handle:
        handle.writelines(filtered)

    
