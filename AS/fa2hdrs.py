
import sys
from Bio import SeqIO

def hdrs(fasta, organism):
    fa = SeqIO.parse(fasta, 'fasta')
    tmp = []
    for f in fa:
        chrom = f.id
        chrom_length = len(f)
        chrom_length_noN = chrom_length - f.seq.count('N') - f.seq.count('n')
        tmpline = '>%s /len=%s /nonNlen=%s /org=%s\n' % (chrom,
                    chrom_length, chrom_length_noN, organism)
        tmp.append(tmpline)
    return tmp


if __name__ == "__main__":
    chrinfo = hdrs(sys.argv[1], sys.argv[2])
    with open(sys.argv[3], 'w') as handle:
        handle.writelines(chrinfo)
