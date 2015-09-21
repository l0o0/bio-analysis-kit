#!/usr/bin/python
# 2015-9-18, created by Linxzh


import sys
import svgwrite
from svgwrite import cm, mm
from math import log

#global W = 18; H=15; SAMPLE_STEP=2

def marker_trans(marker):
    '''
    ['TTG','CCA','CCG','CTG'] => ['TCCC','TCCT','GAGG']
    '''
    f = lambda x, y: [ ''.join(i) for i in zip(x, y) ]
    marker_t = reduce(f, marker)
    return marker_t

def read_data(infile):
    '''
    transcform input data into a dict:
    {blockid:{pos1:markers1,pos2:markers2, ..., 'frequency':(f1,f2,...)}, ...}
    '''
    D = {}
    marker = []; freq = []
    i = 0
    with open(infile) as handle:
        for f in handle:
            if f.startswith('BLOCK'):
                if marker:
                    marker_t = marker_trans(marker)
                    D[i] = dict(zip(pos, marker_t))
                    D[i]['frequency'] = freq
                    marker = []; freq = []
                pos = [int(x) for x in f.split()[3:]]
                i += 1
            elif f.startswith('Multiallelic'):
                continue
            else:
                flist = f.split()
                marker.append(flist[0])
                freq.append(float(flist[1][1:-1]))
    marker_t = marker_trans(marker)
    D[i] = dict(zip(pos, marker_t))
    D[i]['frequency'] = freq

    return D

# read gene positions information
def read_gene(geneinfo):
    '''return dict {chrom:{gene1:[start, end], ...}, ...}'''
    gene_dict = {}
    with open(geneinfo) as handle:
        for f in handle:
            flist = f.split()
            if flist[0] not in gene_dict:
                gene_dict[flist[0]] = {flist[1]:[int(flist[2]), int(flist[3])]}
            else:
                gene_dict[flist[0]][flist[1]] = [int(flist[2]), int(flist[3])]
    return gene_dict

# draw block
def draw_block(dwg, D, Allpos, distlog, ministep, y, barsize = 0.5):
    y1 = y
    y2 = y + 0.5
    step_list = [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1]
 # draw rect region from 2 ~ 16
    dwg.add(dwg.line(start=(2*cm, y1*cm), end=(16*cm,y1*cm), stroke='black', stroke_width=0.25))
    dwg.add(dwg.line(start=(2*cm, y2*cm), end=(16*cm,y2*cm), stroke='black', stroke_width=0.25))
#    dwg.add(dwg.rect(insert=(2 * cm, y1 * cm), size=(14 * cm, 0.5 * cm), 
#        fill='none', stroke='black', stroke_width=0.5))
# draw y-xaxis from 0 ~ 1 indicate grequence
    dwg.add(dwg.line(start=(1.975*cm, y1*cm), end=(1.975*cm,(y1-1)*cm), stroke='black', stroke_width=0.5))
# ticks for y-axis, 0.25,0.5,0.75
    dwg.add(dwg.text('Frequency', insert=(0.9*cm, (y1-1.1)*cm),style="font-size:6px; font-family:Arial"))
    for t in (0,0.25,0.5,0.75,1):
        dwg.add(dwg.line(start=(1.95*cm, (y1-t)*cm), end=(1.975*cm,(y1-t)*cm), stroke='black', stroke_width=0.5))
        dwg.add(dwg.text(str(t), insert=(1.75*cm, (y1-t)*cm),style="font-size:3px; font-family:Arial"))
# draw blocks and marker from here        
#    blocks = D.keys()
    for block in D.keys():              # block id is int
        pos_and_freq_dict = D[block]
        pos = pos_and_freq_dict.keys()
        pos.remove('frequency')
        frequency = D[block]['frequency']
        maxidx = Allpos.index(max(pos))
        minidx = Allpos.index(min(pos))

        if minidx == 0:
            blockposX = [2, 2 + ((maxidx + sum(distlog[:maxidx - 1]))) * ministep]
        else:
            blockposX = [2 + (maxidx + sum(distlog[:maxidx - 1])) * ministep, 
                    2+ (minidx + sum(distlog[:minidx - 1])) * ministep]

        step_index = block % 17
        dwg.add(dwg.line(start=(blockposX[0]*cm, 
                (step_list[step_index]* 0.05 + y1)*cm), 
                end=(blockposX[1]*cm, (step_list[step_index]* 0.05 + y1)*cm), 
                stroke="grey", stroke_width=0.5))

        for p in pos:
            if p in Allpos:
                idx = Allpos.index(p)
                if idx == 0:
                    x1 = 2
                else:
                    x1 = 2 + (idx + sum(distlog[:idx - 1])) * ministep
                common_marker = max(set(list(pos_and_freq_dict[p])), key=list(pos_and_freq_dict[p]).count)
                
                for i, c in enumerate(pos_and_freq_dict[p]):
                    if c == common_marker:
                        c='#0a67a3'
                    else:
                        c = '#ff8e00'
                    dwg.add(dwg.line(start=(x1 * cm, (y1 - frequency[i]-0.025) * cm), 
                            end=(x1 * cm, (y1 - frequency[i]+0.025) * cm), 
                            stroke=c, stroke_width=barsize))
#                    dwg.add(dwg.circle(center=(x1 * cm, (y1 - frequency[i]) * cm), r=0.025*cm, fill=c))
    return dwg


#  
def filter_pos(D, r):
    keys = D.keys()
    for k in keys:
        Max = max(D[k])
        Min = min(D[k])
        if Max < r[0] or Min > r[1]:
            del D[k]
    return D


def subdict_keys(D):
    keys = []
    for i in D:
        keys += D[i].keys()
    return keys

# read sample info from file
def read_sample(sampleinfo):
    out = {}
    with open(sampleinfo) as handle:
       filelist = handle.readlines()
       positions = filelist[0].split(':')
    region = [positions[0], int(positions[1]), int(positions[2])]

    for l in filelist[1:]:
        names = l.split()
        if len(names) >1:
            out[names[0]] = filter_pos(read_data(names[1]), region[1:])
        else:
            out[names[0]] = {}
    return out, region 

# draw gene region
def draw_gene(chrome, Allpos, distlog, gene_dict, sample_data, dwg, ministep):
    samples = sorted(sample_data.keys())
    samples_step = [samples.index(x) for x in samples if sample_data[x]]
    genes = gene_dict[chrome]

    def get_xaxis(pos, Allpos, ministep):
        if pos <= min(Allpos):
            pos = 2
        elif pos >= max(Allpos):
            pos = 16
        else:
            newpos = sorted(set(Allpos+ [pos]))
            pos = (2 + (newpos.index(pos)-1 + sum(distlog[:(newpos.index(pos) - 2)])) + log(pos-newpos[newpos.index(pos)-1],10)) * ministep
        return pos

    for g in genes:
        x_axis = [get_xaxis(genes[g][0], Allpos, ministep), get_xaxis(genes[g][1], Allpos, ministep)]
        print g, x_axis
        tmpcolor = {0:'red',1:'blue'}
        for i in samples_step:
            dwg.add(dwg.line(start=(x_axis[0]*cm, (2.5+2*i)*cm), end=(x_axis[1]*cm, (2.5+2*i)*cm), stroke=tmpcolor[genes.keys().index(g)%2], stroke_width=1))
            dwg.add(dwg.text(g, insert=((sum(x_axis)/2)*cm, (2.7+2*i)*cm), style="font-size:8px; font-family:Arial; font-style:italic"))
    return dwg
        

if __name__ == '__main__':
    sample_data, region  = read_sample(sys.argv[1])
    dwg = svgwrite.Drawing(filename=sys.argv[3], size=(18 * cm, 15 * cm))
    if len(sample_data) > 1:
        Allpos = sorted(reduce(lambda x,y : set(x) | set(subdict_keys(y)), 
            sample_data.values()[1:], subdict_keys(sample_data.values()[0])))
    else:
        Allpos = sorted(set(subdict_keys(sample_data.values()[0])))
#    print Allpos
    Allpos.remove('frequency')      # remove frequency item for calc
    print "Number of markers:%s, min:%s, max:%s\n" % (len(Allpos), min(Allpos), max(Allpos))
    dwg.add(dwg.text('%s:%s-%s, distance between blocks is converted in log10' % (region[0], min(Allpos), max(Allpos)), 
            insert=(0.1*cm, 13.5*cm), style="font-size:8px; font-family:Arial"))
    distlog = map(lambda x: log(Allpos[x + 1] - Allpos[x], 10), range(len(Allpos) - 1))
    ministep = round(14.0 / (int(sum(distlog)) + len(Allpos)), 6)

    if len(Allpos) > 10000:
        barsize = 0.5
    elif len(Allpos) > 5000:
        barsize = 1
    else:
        barsize = 2
    for i,j in enumerate(sorted(sample_data.keys())):
        print '%s, BLOCKS: %s' % (j, len(sample_data[j]))
# add empty chromosome 
        if sample_data[j]:
            dwg = draw_block(dwg, sample_data[j], Allpos, distlog, ministep, 2+i*2, barsize)
        else:
            dwg.add(dwg.rect(insert=(2 * cm, (2+i*2) * cm), 
                    size=(14 * cm, 0.5 * cm), fill='none', 
                    stroke='black', stroke_width=0.5))

        dwg.add(dwg.text(j, insert=(0.5*cm, (2.25+i*2)*cm), style="font-size:8px"))
# add gene positions here
    gene_dict = read_gene(sys.argv[2])
    dwg = draw_gene(region[0], Allpos, distlog, gene_dict, sample_data, dwg, ministep)
    dwg.save()
