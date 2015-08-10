#!/bin/env python

import sys
import svgwrite
import svgwrite
from svgwrite import cm, mm

NUM2BASE = {'1':'green','2':'yellow', '4':'red', '3':'blue' }

# read markers' positions from input file
def read_data(infile):
    kaiguang = 0
    D = {}
    marker = []
    i = 0
    with open(infile) as handle:
        for f in handle:
            if f.startswith('BLOCK'):
                kaiguang = 1
                pos = [int(x) for x in f.split(' ')[3:]]
                i += 1
            elif f.startswith('Multiallelic'):
                D[i] = dict(zip(pos, marker))
                marker = []
            else:
                marker.append(f.split()[0])
    return D


if __name__ == '__main__':
    markerD = read_data(sys.argv[1])


