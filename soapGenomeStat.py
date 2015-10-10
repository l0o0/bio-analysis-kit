#!/usr/bin/python

import sys

with open(sys.argv[1]) as handle:
    lines = handle.readlines()


outlines = ['\t'.join(x.split('\t')[:3])+'\n' for x in lines[:3]]
outlines.append(lines[3])
# total mapped reads

def combine(line):
    l = line.strip().split('\t')
    reads = (int(l[1]) + int(l[4]) + int(l[7]))
    pers = (float(l[2][:-1]) + float(l[5][:-1]) + float(l[8][:-1]))
    return (reads, pers)
    


line5 = 'Total Mapped Reads\t%s\t%s%%\n' % combine(lines[4])
outlines.append(line5)
outlines.append('\n')
line7 = 'perfect match\t%s\t%s%%\n' % combine(lines[6])
outlines.append(line7)
line8 = '<=5bp mismatch\t%s\t%s%%\n' % combine(lines[7])
outlines.append(line8)
outlines.append('\n')
line10 = 'unique match\t%s\t%s%%\n' % combine(lines[9])
line11 = 'multi-position match\t%s\t%s%%\n' % combine(lines[10])
outlines.append(line10)
outlines.append(line11)
outlines.append('\n')
line13 = 'Total Unmapped Reads\t%s\t%s%%\n' % combine(lines[12])
outlines.append(line13)

with open(sys.argv[2], 'w') as handle:
    handle.writelines(outlines)
