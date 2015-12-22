#!/usr/bin/python

import sys
import numpy as np

base_dict = {'A':'A', "T":'T', 'C':'C', 'G':'G',
             'R':'AG', 'Y':'CT', 'M':'AC', 'K':'GT',
             'S':'GC', 'W':'AT', 'H':'ATC', 'B':'GTC',
             'V':'GAC', 'D':'GAT', 'N':'ATCG'}

def settest():
    baseA = base_dict['A']
    baseB = base_dict['R']
    if set(list(baseA)).intersection(set(list(baseB))):
        pass

def difftest():
    baseA = base_dict['A']
    baseB = base_dict['R']
    if difflib.SequenceMatcher(None, baseA, baseB).ratio():
        pass

def parseGT(infile):
    matrix = []
    with open(infile) as handle:
        for f in handle:
            tmplist = f.split()
            matrix.append(tmplist[3:])
    return matrix


def simi(inlist, acol, bcol):
    M = 0; m = 0
#            if f.startswith('#'):
#                continue
    for snp_list in inlist:
       baseA = base_dict[snp_list[acol]]
       baseB = base_dict[snp_list[bcol]]
       if set(list(baseA)).intersection(set(list(baseB))):
           m += 1
       M += 1
#            print baseA,baseB, M,m
    return float(m)/M

def simiMatrix(gt_matrix, sample_num):
    similarity_m = np.zeros(sample_num * sample_num).reshape(sample_num, sample_num)
    
    for i in range(sample_num):
        for j in range(i+1, sample_num):
            similarity_m[i][j] = simi(gt_matrix, i, j)
    return similarity_m
    
if __name__ == '__main__':
    gt_matrix = parseGT(sys.argv[1])
    simi_matrix = simiMatrix(gt_matrix, int(sys.argv[2]))
    print simi_matrix
 
