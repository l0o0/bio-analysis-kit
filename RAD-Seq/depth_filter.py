#!/usr/bin/python
# create by linxzh, 2015-10-27
# according input marker locus, get stacks depth at this locus.


import os
import sys 
import gzip
import operator


if len(sys.argv) != 4:
    print 'USAGE: python depth_filter.py indir marker_locus output.txt'
    sys.exit(0)



# files' suffix with 'gz'
def filter_files(indir):
    files = os.listdir(indir)
    files = [x for x in files if x.endswith('gz')]
    return files


# 
def stacks_depth(marker_locus, infile):
    D = dict(zip(marker_locus, ["--"] * len(marker_locus))) 
    handle = gzip.open(infile)
    for f in handle:
        flist = f.split()
        locus = flist[2]
        if locus in marker_locus:
            depth = int(flist[-2])
            if D[locus] == "-":
                D[locus] = depth
            else:
                D[locus] = D[locus] + depth
    sorted_items = sorted(D.items(), key=operator.itemgetter(0))
    depth_list = [x[1] for x in sorted_items]
    return depth_list


if __name__ == '__main__':
    gzfiles = filter_files(sys.argv[1])

    with open(sys.argv[2]) as handle:
        marker_locus = handle.readlines()
        marker_locus = [x.strip() for x in marker_locus]
    
    sample_list = ['locus']
    tmp_depth = []

    for gzfile in gzfiles:
        print 'parsing %s' % gzfile
        sample = gzfile.split('_')[0]
        sample_list.append(sample)
        infile = sys.argv[1] + '/' + gzfile
        depth_list = stacks_depth(marker_locus, infile)
        tmp_depth.append(depth_list)
    
    sorted_locus = sorted(marker_locus, key=lambda x:int(x))
    out_list = []

    for i in range(len(marker_locus)):
        tmp = [str(x[i]) for x in tmp_depth]
        out_list.append(sorted_locus[i] + '\t' + '\t'.join(tmp) + '\n')

    with open(sys.argv[3], 'w') as handle:
        handle.write('\t'.join(sample_list)+'\n')
        handle.writelines(out_list)
