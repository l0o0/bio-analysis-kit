#!/bin/env python
# linxzh 2015-12-10


import sys


# home: 1/1, 0/0, hete: 0/1


type_dict = {"1/1":1, "0/0":0, "0/1":-1}


def CalRate(inlist):
    miss = inlist.count(0)
    home = inlist.count(1)
    hete = inlist.count(-1)
    all = float(len(inlist))
    return "%s\t%.2f\t%s\t%.2f\t%s\t%.2f\n" % (home, home/all, hete, hete/all, miss, miss/all)

def PopSNP(infile, sampleNum):
    snp_dict = dict((k,[]) for k in range(1,sampleNum + 1))
    for i in open(infile):
        if i.startswith('#'):
            continue
        tmplist = i.strip().split('\t')[9:]
        tmptype = [type_dict[x.split(':')[0]] for x in tmplist]

        for m,n in enumerate(tmptype):
            snp_dict[m+1].append(n)
    return snp_dict


if __name__ == "__main__":
    snp_dict = PopSNP(sys.argv[1],int(sys.argv[2]))
    out = ['Sample\tHome\tHome-rate\tHete\tHete-rate\tMiss\tMiss-rate\n']
    for k in snp_dict:
        ratio = CalRate(snp_dict[k])
        out.append('%s\t%s' % (k, ratio))

    with open(sys.argv[3], 'w') as handle:
        handle.writelines(out)



