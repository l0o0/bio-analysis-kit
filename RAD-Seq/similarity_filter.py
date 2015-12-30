#!/usr/bin/python
# created by linxzh 2015 10-22
# filter output result of genotype of stacks workflow

import sys

if len(sys.argv) != 4:
    print "USAGE: python script.py inputfile outfile similarity(float)"
    sys.exit(0)


def similarity(s, l1, l2, simi=0.99):
    thresh_num = int((len(l1) -s) * (1-simi) + 1)
    n = 0
    for a1,b1 in zip(l1,l2):
        if a1 != b1:
            n += 1
        if n >= thresh_num:
            return False
    return True


if __name__ == '__main__':
    with open(sys.argv[1]) as handle:
        filelist = handle.readlines()

    start_col = 2
    tmplist = [filelist[0].strip().split('\t')]
    out = []
    n = len(filelist)
    for i in range(n):
        flag = 1
        for j in range(i+1,n):
            if similarity(start_col, filelist[i], filelist[j], float(sys.argv[3])):
                flag = 0
                break
        if flag:
           out.append(filelist[i])

#    print len(out)
    with open(sys.argv[2], 'w') as handle:
        handle.writelines(out)



