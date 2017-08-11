import sys
import time


if len(sys.argv) != 4:
    print "USAGE: python sys.argv[0] links.txt SigDiff.txt out_prefix"
    sys.exit(0)


score = 750

start = time.time()
links = []
with open(sys.argv[1]) as handle:
    tmplist = handle.readlines()
    links = [tuple(sorted(x.split()[:2])) for x in tmplist if int(x.split()[2])>score]
    links = list(set(links))
print time.time() - start
start = time.time()

diffgenes = []
log2 = ['GeneID\tlog2\n']
with open(sys.argv[2]) as handle:
    for f in handle:
        if f.startswith('GeneID'):
            continue
        tmplist = f.split()
        gene = tmplist[0]
        log = tmplist[-3]
        log2.append('%s\t%s\n' % (gene, log))
        diffgenes.append(gene)
print time.time() - start
start = time.time()
D = {}
for gene in diffgenes:
    tmpgene = [x for x in links if gene in x]
    D[gene] = tmpgene
print time.time() - start
start = time.time()


all_links_diff = set(reduce(lambda x,y:x+y, D.values()))
all_links_diff = ['\t'.join(x)+'\n' for x in all_links_diff]
all_links_diff = ['fromNode\ttoNode\n'] + all_links_diff
print time.time() - start

topGenes = sorted(D.keys(), key=lambda x: len(D[x]), reverse=True)
outlinks = [['fromNode','toNode']]
outlinks += D[topGenes[0]][:100]
outlinks += D[topGenes[1]][:50]
outlinks += D[topGenes[2]][:50]
outlinks += D[topGenes[3]][:50]

allout = sys.argv[3] + '_all.txt'
topout = sys.argv[3] + '_top250.txt'
log2file = sys.argv[3] + '_log2.txt'
with open(topout, 'w') as handle:
    handle.writelines(['\t'.join(x) + '\n' for x in outlinks])

with open(allout, 'w') as handle:
    handle.writelines(all_links_diff)

with open(log2file, 'w') as handle:
    handle.writelines(log2)
