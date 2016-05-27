#!/usr/bin/python 

import sys
import svgwrite
from svgwrite import cm,mm


# Parse the blast output file by query id. Each query id is one setction.
def query_section(infile):
    with open(infile) as handle:
        filelist = handle.readlines()

    section_dict = {}
    for fline in filelist:
        if fline.startswith('#') or not fline.strip():
            continue
        tmplist = fline.split()
        query_id = tmplist[0]
        subject_id = tmplist[1]
        query_region = map(int,tmplist[6:8])
        subject_region = map(int, tmplist[8:10])

        if query_id not in section_dict:
            section_dict[query_id] = {subject_id:[(query_region, subject_region)]}
        else:
            if subject_id not in section_dict[query_id]:
                section_dict[query_id][subject_id] = [(query_region, subject_region)]
            else:
                section_dict[query_id][subject_id].append((query_region, subject_region))
    print "Blast result was parsed."        
    return section_dict


# One subject one plot.
def plot_subject(dwg, query_dict, subject_id, y):

    cbPalette = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]
    # add query id
    dwg.add(dwg.text(subject_id, insert=(0.2*cm, (y+0.5)*cm), style='font-size:12px; font-family:Arial'))

    query_max = max(reduce(lambda x,y : x+y, [pos[0] for pos in query_dict[subject_id]]))
    query_min = min(reduce(lambda x,y : x+y, [pos[0] for pos in query_dict[subject_id]]))
    subject_max = max(reduce(lambda x,y : x+y, [pos[1] for pos in query_dict[subject_id]]))
    subject_min = min(reduce(lambda x,y : x+y, [pos[1] for pos in query_dict[subject_id]]))
    
    if (subject_max - subject_min) > (query_max - query_min):
        scale = 16.0 / (subject_max - subject_min)
    else:
        scale = 16.0 / (query_max - query_min)
    
    print scale
    query_start = 2 + 8 - (query_max-query_min)/2 * scale
    query_end = 2 + 8 + (query_max-query_min)/2 * scale
    subject_start = 2 + 8 - (subject_max-subject_min)/2 * scale
    subject_end = 2 + 8 + (subject_max-subject_min)/2 * scale

    # Query line and subject line.
    print query_start,query_end,subject_start,subject_end
    dwg.add(dwg.line(start=(query_start * cm, (y+1)*cm), end=(query_end * cm, (y+1)*cm),
                     stroke='black', stroke_width=1))
    dwg.add(dwg.line(start=(subject_start * cm, (y+5)*cm), end=(subject_end * cm, (y+5)*cm),
                     stroke='black', stroke_width=1))

    
    for idx, match in enumerate(query_dict[subject_id]):
        qmatch = match[0]
        smatch = match[1]
        
        line1start = (qmatch[0] - query_min) * scale + query_start
        line1end = (smatch[0] - subject_min) * scale + subject_start
        line2start = (qmatch[1] - query_min) * scale + query_start
        line2end = (smatch[1] - subject_min) * scale + subject_start

        dwg.add(dwg.line(start=(line1start * cm, (y+1) *cm), end=(line1end * cm, (y+5) *cm),
                stroke=cbPalette[idx%8], stroke_width=0.5))
        dwg.add(dwg.line(start=(line2start * cm, (y+1) *cm), end=(line2end * cm, (y+5) *cm),
                stroke=cbPalette[idx%8], stroke_width=0.5))
        dwg.add(dwg.rect(insert=(line1start*cm, (y+1-(idx%2+1) *0.1)*cm), 
                size=((line2start-line1start)*cm, 0.5*mm),
                fill=cbPalette[idx%8], stroke=cbPalette[idx%8], stroke_width=0.5))
        dwg.add(dwg.rect(insert=(line1end*cm, (y+5+(idx%2+1)*0.1)*cm),
                size=((line2start-line1start)*cm, 0.5*mm),
                fill=cbPalette[idx%8], stroke=cbPalette[idx%8], stroke_width=0.5))
        
    return dwg






# Main plot function
def ploter(section_dict):
    if not section_dict:
        print "There is no result!"
        return None
    

    for query_id in section_dict:
        high = len(section_dict[query_id]) * 6
        dwg = svgwrite.Drawing(filename=("%s.svg" % query_id), size=(18*cm, high *cm))
        for y, subject_id in enumerate(section_dict[query_id].keys()):
            dwg = plot_subject(dwg, section_dict[query_id], subject_id, y*6)
        dwg.save()

    print 'OK!'



if __name__ == '__main__':
    section_dict = query_section(sys.argv[1])
    ploter(section_dict)

