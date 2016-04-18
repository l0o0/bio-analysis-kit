#!/bin/env python

import sys
import xlwt
import xlrd


def row_writer(idx,rowline,ws, style):
    '''idx = row index
       rowline = value list
       ws = worksheet object'''

    for i,v in enumerate(rowline):
        try:
            ws.write(idx,i,v, style)
        except ValueError:
            print "The max column number of xls format is 256!\nPlease check your file or use xlsx instead."
            sys.exit(0)
    return ws


def transfer(infile, style):
    sheetname ='sheet1' 
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(sheetname)
    with open(infile) as handle:
        for idx, rowline in enumerate(handle):
            rowline = rowline.strip().split('\t')
            if len(rowline) > 256:
                print "Maximun colmun num reached!\nPlease check your file or use xlsx instead."
                sys.exit(0)
            worksheet = row_writer(idx, rowline, worksheet, style)

    return workbook


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "USAGE: python excel.py infile outfile"
        sys.exit(0)
    filename = sys.argv[1]
    outfile = sys.argv[2]



    fontname='Times New Roman'
    font = xlwt.Font()
    font.name = fontname
    style = xlwt.XFStyle()
    style.font= font
    workbook = transfer(filename, style)
    workbook.save(outfile)


