#!/usr/bin/python
# created by linxzh 2015 10-22
# filter output result of genotype of stacks workflow

import sys


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
    out = [filelist[0]]

    for f in filelist[1:]:
        flist = f.strip().split('\t')
        flag = 0

        for tmp_item in tmplist:
            if similarity(start_col, flist, tmp_item):
#                print flist[0], tmp_item[0], 'simi'
                break
            else:
                flag += 1
        if flag == len(tmplist):
            tmplist.append(flist)
            out.append(f)
               

#    print len(out)
    with open(sys.argv[2], 'w') as handle:
        handle.writelines(out)



