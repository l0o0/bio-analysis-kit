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
                pos = [ int(x) for x in f.split()[3:] ]
                i += 1
            elif f.startswith('Multiallelic'):
                marker_t = marker_trans(marker)
                D[i] = dict(zip(pos, marker_t))
                marker = []
            else:
                marker.append(f.split()[0])
    return D


# draw block
def draw_block(dwg, D, Allpos, distlog, ministep, y, barsize = 0.5):
    y1 = y
    y2 = y + 0.5
    dwg.add(dwg.rect(insert=(2 * cm, y1 * cm), size=(14 * cm, 0.5 * cm), fill='none', stroke='black', stroke_width=0.5))
    for block in D:
        pos = D[block]
        maxidx = Allpos.index(max(pos))
        minidx = Allpos.index(min(pos))
        if minidx == 0:
            blockposX = 2 + ((maxidx + sum(distlog[:maxidx - 1])))/2 * ministep
        else:
            blockposX = 2 + ((maxidx + sum(distlog[:maxidx - 1])) + (minidx + sum(distlog[:minidx - 1])))/2 * ministep
        dwg.add(dwg.line(start=(blockposX*cm, y1*cm), end=(blockposX*cm,y2*cm), stroke='red', stroke_width=0.5))
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


if __name__ == '__main__':
    with open(sys.argv[1]) as handle:
        headregion = handle.readlines()[0].strip()
        tmp = headregion.split()
        region = [int(tmp[1]), int(tmp[2])]

    D1 = read_data('/nfs3/onegene/user/group1/linxingzhong/workspace/8-7/Gk/trace.chr02.Gk.genotype.ped.GABRIELblocks')
    D2 = read_data('/nfs3/onegene/user/group1/linxingzhong/workspace/8-7/Gs_r2/chr02.Gs28_r2.genotype.ped.GABRIELblocks')
    D3 = read_data('/nfs3/onegene/user/group1/linxingzhong/workspace/8-7/Gs_r3/chr02.Gs28_r3.genotype.ped.GABRIELblocks')
    D4 = read_data('/nfs3/onegene/user/group1/linxingzhong/workspace/8-7/Gs_r4/chr02.Gs28_r4.genotype.ped.GABRIELblocks')
    
#    dwg = svgwrite.Drawing(filename='Test.svg', size=(18 * cm, 8 * cm))
    
#    region = [23712760, 26917128]
    D1 = filter_pos(D1, region)
    D2 = filter_pos(D2, region)
    D3 = filter_pos(D3, region)
    D4 = filter_pos(D4, region)
#    print len(D1), len(D2) 
    pos1 = subdict_keys(D1)
    pos2 = subdict_keys(D2)
    pos3 = subdict_keys(D3)
    pos4 = subdict_keys(D4)

    Allpos = sorted(list(set(pos1) | set(pos2) | set(pos3) | set(pos4)))
    distlog = map(lambda x: log(Allpos[x + 1] - Allpos[x], 10), range(len(Allpos) - 1))
#    print len(Allpos), len(distlog)


    if len(Allpos) > 5000:
        barsize = 0.5
    elif len(Allpos) > 1000:
        barsize = 1
    else:
        barsize = 2

    if Allpos:
        dwg = svgwrite.Drawing(filename=sys.argv[2], size=(18 * cm, 12 * cm))
        ministep = round(14.0 / (int(sum(distlog)) + len(Allpos)), 6)
        dwg = draw_block(dwg, D1, Allpos, distlog, ministep, 2, barsize)
        dwg = draw_block(dwg, D2, Allpos, distlog, ministep, 4.5, barsize)
        dwg = draw_block(dwg, D3, Allpos, distlog, ministep, 7, barsize)
        dwg = draw_block(dwg, D4, Allpos, distlog, ministep, 9.5, barsize)
        dwg.add(dwg.text('Gk', insert=(0.5*cm, 2.25*cm)))
        dwg.add(dwg.text('Gs_r2', insert=(0.5*cm, 4.75*cm)))
        dwg.add(dwg.text('Gs_r3', insert=(0.5*cm, 7.25*cm)))
        dwg.add(dwg.text('Gs_r4', insert=(0.5*cm, 9.75*cm)))
        dwg.add(dwg.text(headregion, insert=(7*cm, 0.5*cm)))
        dwg.save()
    else:
        print '%s has no marker in this region:%s' % (sys.argv[1], headregion)
