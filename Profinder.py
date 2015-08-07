#!/usr/bin/env python
#Created: 2013-11-4
#Modified: 2014-7-16
#Author: Linxzh
#retrive promoter sequence before ATG start codon

import time
import argparse
from Bio.Seq import reverse_complement
from Bio import SeqIO


#specify the arguments
parser = argparse.ArgumentParser(description='Find the promoter sequence',
        prog='Promoter Finder', usage='PROG [options]')
parser.add_argument('-l',help='sequence length, default is 2000bp', type=int, default=2000)
parser.add_argument('-i',help='input a gene id list',
        type=argparse.FileType('r'))
parser.add_argument('-g', help='gff3 file', type=argparse.FileType('r'))
parser.add_argument('-f', help="genome sequence file",type=str)
parser.add_argument('-c', type=int, default=1,
        help='specify the col number of input gene list,default is 1')
parser.add_argument('-o', help='output file name(fasta format by default',
        type=argparse.FileType('w'))
parser.add_argument('-r', help='''reverse_complement of the sequence if
        the strand is '-',default is false, valid parameter is T or F''',
        default='F', choices=['T','F'])
#parser.add_argument('-feature', help='GFF file feature needs to get', type=str)
args=parser.parse_args()

start = time.clock()        #start a clock

# transfer the fasta file in a dict
def fa_to_dict(fa_file):
    fa_dict = SeqIO.to_dict(SeqIO.parse(fa_file,'fasta'))
    print 'Chromesome read complete!'
    return fa_dict

#select gene id by col number
def select_gene(inputfile,gene_col):            #file input and gene col nm
    gene_list = []

    for x in inputfile:
        if x == '\n':
            continue
        x = x.split()[args.c -1]
        gene_list.append(x)

    print '%s genes input.' % (len(gene_list))
    return gene_list

# creat a dict,gene id as key, position as value
# input gff3 file
def pos(gff3):
    '''get CDS'''
    D = {}
    for x in gff3:

        if x.startswith('#'):
            continue
        elif 'CDS' in x:
            xlist = x.split()
            start = int(xlist[3])
            end = int(xlist[4])
            strand = xlist[6]
            gene_id = xlist[8].split('=')[1].split(';')[0]
            chr_id = xlist[0]

            if gene_id in D:
                D[gene_id][0].append(start)
                D[gene_id][0].append(end)
            else:
                D[gene_id] = [[start,end],strand,chr_id]

    print 'GFF3 file parse complete!'
    return D

# find 2000 bp before the ATG
def promoter(chr_dict, pos_dict, reverse, output, gene_list, length):
    n = 0
    outputList = []
    for gene in gene_list:
        positions = sorted(pos_dict[gene][0])
        gene_strand = pos_dict[gene][1]
        chrome = chr_dict[pos_dict[gene][2]]

        print positions

        if gene_strand == '+':
            gene_start = positions[0]
            pro_start = gene_start-length

            if pro_start < 0:        # gene start pos less than length
                gene_seq = chrome[:gene_start].seq
            else:
                gene_seq = chrome[gene_start-length:gene_start].seq

        elif gene_strand == '-':
            gene_start = positions[-1]
            print gene_start
            # sequence of + strand
            gene_seq = chrome[gene_start :gene_start + length].seq
            print gene_start, gene_start + length
            
            if reverse == 'T':
                gene_strand += ' reverse_complement'
            else:
                gene_seq = gene_seq.reverse_complement()

        n+=1
        wl = '>%s|%s\n%s\n' % (gene,gene_strand,str(gene_seq))
        outputList.append(wl)

    output.writelines(outputList)
    print "%s genes found!" % n

    output.close()

if __name__ == '__main__':
    chr_dict = fa_to_dict(args.f)
    pos_dict = pos(args.g)
    gene_list = select_gene(args.i, args.c)
    promoter(chr_dict, pos_dict, args.r, args.o, gene_list, args.l)

    t = time.clock() - start        #time comsumed
    print 'Time: ' ,t                #print time consumed
