#!/usr/bin/env python

import sys


def fun(gtf):
    D = {}
    with open(gtf) as handle:
        for l in handle:
            tmplist = l.split('\t')
            items = tmplist[8].split('"')
            transcript = items[1]
            qStart = int(tmplist[3])
            qEnd = int(tmplist[4])
            blockSize = qEnd - qStart + 1
            if transcript not in D:
                qName = items[3]
                tName = tmplist[0]
                strand = tmplist[6]
                D[transcript] = [strand, qName, tName, [qStart], [qEnd], [blockSize]]
            else:
                D[transcript][3].append(qStart)
                D[transcript][4].append(qEnd)
                D[transcript][5].append(blockSize)
    return D

def write_lines(D, psl):
    out = open(psl, 'w')
    for t in D:
        line = '0\t0\t0\t0\t0\t0\t0\t0\t%s\t%s\t%s\t0\t%s\t%s\t0\t%s\t%s\t%s\t%s\t%s\t%s\n' % (D[t][0], 
                 D[t][1],
                 max(D[t][4]) - min(D[t][3]) + 1,
                 max(D[t][4]) - min(D[t][3]),
                 D[t][2],
                 min(D[t][3])-1,
                 max(D[t][4]),
                 len(D[t][5]),
                 ''.join([str(x)+',' for x in D[t][5]]),
                 '0,' * len(D[t][5]),
                 ''.join([str(x-1)+',' for x in D[t][3]]))
        out.write(line)
    out.close()

if __name__ == '__main__':
    D = fun(sys.argv[1])
    write_lines(D, sys.argv[2])
