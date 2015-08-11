#!/bin/env python
# 2014-3-25 created by Linxzh


import svgwrite
from svgwrite import cm, mm

lengthD = {'Chr1':29149675,'Chr2':23174626,'Chr3':39782674,'Chr4':23425844,'Chr5':28023477,\
'Chr6':29076228,'Chr7':19226500}

infile = open('eurasian_vs_xsbn.txt').readlines()
posD = {'Chr1':[],'Chr2':[],'Chr3':[],'Chr4':[],'Chr5':[],'Chr6':[],'Chr7':[]}
for i in infile:
    if '#' in i:
        continue
    il = i.split()
    if il[0] in posD:
        posD[il[0]].append(il[1:])

dwg = svgwrite.Drawing(filename = 'lintao2.svg', size = (18*cm, 8*cm))

# draw vline
def draw_tick(x, y, base, draw, l=0.12):
    col = {'T':'red', 'A':'black', 'C':'blue', 'G':'green','W':'brown','S':'brown','K':'brown',\
    'M':'brown','Y':'brown','R':'brown','11':'pink','12':'lightpurple'}
    draw.add(draw.line(start = (x*cm, (y-l/2)*cm), end = (x*cm, (y+l/2)*cm), stroke = col[base],\
    stroke_width = 0.1*mm))
    return draw    
    
    
for i in range(1,8):
    x1 = 1; y1 = 1 + (i-1)
    chrome = 'Chr' + str(i)
    scale = 2350000.0           # scale number
    length = lengthD[chrome]
    pos_set = posD[chrome]
    chr_len = length /scale
#    dwg.add(dwg.line(start = (x1*cm, y1*cm), end = ((x1+chr_len)*cm, y1*cm), stroke = 'lightgrey',\
#        stroke_width = 5*mm))
    dwg.add(dwg.rect(insert = (x1*cm, y1*cm), size = (chr_len*cm, 0.5*cm), fill = 'none', stroke = 'black', stroke_width = 0.5))
    for j in pos_set:
        offset = int(j[0]) / scale
        span = int(j[2]) / scale
        dwg.add(dwg.rect(insert = ((x1+offset)*cm, y1*cm), size = (span*cm, 0.5*cm), fill = 'red', stroke = 'red', stroke_width = 0.5))
        
dwg.save()
