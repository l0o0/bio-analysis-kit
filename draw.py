# Embedded file name: draw.py
import sys
import svgwrite
from svgwrite import cm, mm
from math import log



def marker_trans(marker):
    f = lambda x, y: [ ''.join(i) for i in zip(x, y) ]
    marker_t = reduce(f, marker)
    return marker_t


def read_data(infile):
    D = {}
    marker = []
    i = 0
    with open(infile) as handle:
        for f in handle:
            if f.startswith('BLOCK'):
                if marker:
                    marker_t = marker_trans(marker)
                    D[i] = dict(zip(pos, marker_t))
                    marker = []
                pos = [int(x) for x in f.split()[3:]]
                i += 1
            elif f.startswith('Multiallelic'):
                continue
            else:
                marker.append(f.split()[0])
    marker_t = marker_trans(marker)
    D[i] = dict(zip(pos, marker_t))

    return D




# draw block
def draw_block(dwg, D, Allpos, distlog, ministep, y, barsize = 0.5):
    y1 = y
    y2 = y + 0.5
    step_list = [1,2,3,4,5,4,3,2,1]
    dwg.add(dwg.rect(insert=(2 * cm, y1 * cm), size=(14 * cm, 0.5 * cm), fill='none', stroke='black', stroke_width=0.5))
    blocks = D.keys()
    for block_index, block in enumerate(blocks):
        pos = D[block]
        maxidx = Allpos.index(max(pos))
        minidx = Allpos.index(min(pos))

        if minidx == 0:
            blockposX = [2, 2 + ((maxidx + sum(distlog[:maxidx - 1]))) * ministep]
        else:
            blockposX = [2 + (maxidx + sum(distlog[:maxidx - 1])) * ministep, 2+ (minidx + sum(distlog[:minidx - 1])) * ministep]

        step_index = block_index % 9
        dwg.add(dwg.line(start=(blockposX[0]*cm, (step_list[step_index]* 0.1 - 0.05 + y1)*cm), end=(blockposX[1]*cm,
               (step_list[step_index]* 0.1 - 0.05 + y1)*cm), stroke="rgb(0,82,156)", stroke_width=1))

        for p in pos:
            if p in Allpos:
                idx = Allpos.index(p)
                if idx == 0:
                    x1 = 2
                else:
                    x1 = 2 + (idx + sum(distlog[:idx - 1])) * ministep
                common_marker = max(set(list(pos[p])), key=list(pos[p]).count)
                for i, c in enumerate(pos[p]):
                    if c == common_marker:
                        c='green'
                    else:
                        c = 'yellow'
                    dwg.add(dwg.line(start=(x1 * cm, (y1 - i*0.05) * cm), end=(x1 * cm, (y1 - (i+1)*0.05) * cm), stroke=c, stroke_width=barsize))
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
    region = [int(x.strip()) for x in filelist[0].split(':')]

    for l in filelist[1:]:
        names = l.split()
        out[names[0]] = filter_pos(read_data(names[1]), region)
    return out, region 


if __name__ == '__main__':
    sample_data, region  = read_sample(sys.argv[1])
    dwg = svgwrite.Drawing(filename=sys.argv[2], size=(18 * cm, 15 * cm))
    print len(sample_data)
    if len(sample_data) > 1:
        Allpos = sorted(reduce(lambda x,y : set(x) | set(subdict_keys(y)), sample_data.values()[1:], subdict_keys(sample_data.values()[0])))
    else:
        Allpos = sorted(set(subdict_keys(sample_data.values()[0])))
#    print Allpos
    print "Number of markers:%s, max:%s, min:%s\n" % (len(Allpos), max(Allpos), min(Allpos))
    dwg.add(dwg.text('Pos: %s - %s' % (min(Allpos), max(Allpos)), insert=(0.1*cm, 0.5*cm), style="font-size:10px; font-family:Arial"))
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
        dwg = draw_block(dwg, sample_data[j], Allpos, distlog, ministep, 2+i*2.5, barsize)
        dwg.add(dwg.text(j, insert=(0.5*cm, (2.25+i*2.5)*cm), style="font-size:10px"))
    dwg.save()
