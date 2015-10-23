#!/usr/bin/python

#-----------------------------------------------------
# python script.py Basic_Statistics_of_Sequencing_Quality.txt Statistics_of_Filtered_Reads.txt output.txt
#-----------------------------------------------------

import sys
import os
if len(sys.argv) != 4:
    print "python script.py Basic_Statistics_of_Sequencing_Quality.txt Statistics_of_Filtered_Reads.txt output.txt"
    sys.exit()

with open(sys.argv[1]) as handle:
    basic = handle.readlines()

with open(sys.argv[2]) as handle:
    statics = handle.readlines()

clean_reads = int(basic[2].split('\t')[3].split(' ')[0])
N_bases = int(statics[6].split('\t')[1]) /2
low_quality = int(statics[3].split('\t')[1])/2
adapters = int(statics[2].split('\t')[1])/2

result = 'Clean Reads\t%s\nContaining N\t%s\nLow Quality\t%s\nContaining Adaptor\t%s\n' % (clean_reads,N_bases,low_quality,adapters)

with open(sys.argv[3],'w') as handle:
    handle.write(result)

cmd = '/nfs2/pipe/RNA/soft/R-3.1.2/bin/Rscript /nfs/pipe/RNA/RNA-ref/version1/filter/plot_RawReadsClass.R ' + sys.argv[3]
os.system(cmd)

#print clean_reads,N_bases,low_quality,adapters
