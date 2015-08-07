#!/bin/env python

import svgwrite


# read markers' positions from input file
def read_data(infile):
    kaiguang = 0
    with open(infile) as handle:
        for f in handle:
            if f.startswith('BLOCK'):
                kaiguang = 1
                pos = [int(x) for x in f.split(' ')[3:]]
            elif f.startswith('Multiallelic'):


