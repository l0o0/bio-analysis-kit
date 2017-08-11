import re
import sys


def summary(infile):
    with open(infile) as handle:
        infos = handle.readlines()
    if len(infos) != 17:
        raise Exception("Bowtie seems currupt.", infile)
    
    total_reads = re.search('^(\d+) ', infos[0]).group(1)
    uniq = re.search('\s*(\d+).*?([\d\.]+)%.*', infos[3])
    total_map = re.search('^([\d\.]+)%*', infos[14]).group(1)
    #print total_map
    return total_reads, uniq.group(1), uniq.group(2), total_map

if __name__ == "__main__":
    total_reads, uniq_reads, uniq_map, total_map =  summary(sys.argv[1])
    sample = re.search('.*_([\d\-\w]*).sh.e.*', sys.argv[1]).group(1)
    single = float(total_map) - float(uniq_map)
    print "%s\t%s\t%s%%\t%s%%(%s)\t%s%%(%s)" % \
        (sample, format(int(total_reads),','), total_map, uniq_map, format(int(uniq_reads),','), single, format(int(int(total_reads)*single/100),','))
