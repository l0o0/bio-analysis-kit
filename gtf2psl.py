#!/usr/bin/env python

import sys


def fun(gtf):
    D = {}
    with open(gtf) as handle:
        for l in handle:
            if l.startswith('#') or l.startswith('\n'):
                continue
            tmplist = l.split('\t')
            qStart = int(tmplist[3])
            qEnd = int(tmplist[4])
            items = tmplist[8].split(';')
#            qName = items[1][5:]
            tName = tmplist[0]
            strand = tmplist[6]
            blockSize = qEnd - qStart + 1
            if tmplist[2] == 'gene':
                transcript = ''
            elif 'mRNA' == tmplist[2]:
                transcript = items[0][3:]
                D[transcript] = [strand, transcript, tName, [], [], [], (qStart,qEnd)]
            elif 'CDS' == tmplist[2] and transcript:
                D[transcript][3].append(qStart)
                D[transcript][4].append(qEnd)
                D[transcript][5].append(blockSize)

    return D

def write_lines(D, psl):
    out = open(psl, 'w')
    for t in D:
        line = '0\t0\t0\t0\t0\t0\t0\t0\t%s\t%s\t%s\t0\t%s\t%s\t0\t%s\t%s\t%s\t%s\t%s\t%s\n' % (D[t][0], 
                 D[t][1],
                 D[t][-1][1] + 1 - D[t][-1][0],
                 D[t][-1][1] - D[t][-1][0],
                 D[t][2],
                 D[t][-1][0] -1,
                 D[t][-1][1],
                 len(D[t][5]),
                 ''.join([str(x)+',' for x in D[t][5]]),
                 '0,' * len(D[t][5]),
                 ''.join([str(x-1)+',' for x in D[t][3]]))
        out.write(line)
    out.close()

if __name__ == '__main__':
    D = fun(sys.argv[1])
    print len(D)
    write_lines(D, sys.argv[2])
