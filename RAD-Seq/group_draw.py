import sys

from reportlab.lib.units import cm
from Bio.Graphics import BasicChromosome
from reportlab.lib import colors


def group2features(infile):
    features = []
    with open(infile) as handle:
        for f in handle:
            if f.startswith(';'):
                continue

            tmplist = f.split()
            tmp_feature = ( float(tmplist[1]) * 1000, 
                            float(tmplist[1]) * 1000, 
                            '0', 
                            tmplist[1] + ' : ' + tmplist[0],
                            'black')
            features.append(tmp_feature)
    return features


if __name__ == "__main__":
    max_length = float(sys.argv[2]) * 1000
    telomere_length = 10000

    chr_diagram = BasicChromosome.Organism()
    chr_diagram.page_size = (15*cm, 30*cm)

    features = group2features(sys.argv[1])
    group = BasicChromosome.Chromosome(sys.argv[3])
    group.scale_num = max_length + 2 * telomere_length

    start = BasicChromosome.TelomereSegment()
    start.scale = telomere_length
    group.add(start)
    
    body = BasicChromosome.AnnotatedChromosomeSegment(max_length, features)
    body.scale = max_length
    group.add(body)

    end = BasicChromosome.TelomereSegment(inverted=True)
    end.scale = telomere_length
    group.add(end)
    
    chr_diagram.add(group)
    chr_diagram.draw(sys.argv[4], "Group for Joinmap")

