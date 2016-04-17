#!/bin/env python

import sys
import xlwt
import xlrd


def row_writer(idx,rowline,ws, style):
    '''idx = row index
       rowline = value list
       ws = worksheet object'''

    for i,v in enumerate(rowline):
        ws.write(idx,i,v, style)

    return ws


def transfer(infile, style):
    sheetname = ''.join(filename.split('.')[:-1])
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(sheetname)
    with open(infile) as handle:
        for idx, rowline in enumerate(handle):
            rowline = rowline.strip().split('\t')
            worksheet = row_writer(idx, rowline, worksheet, style)

    return workbook


if __name__ == '__main__':

    filename = sys.argv[1]
    outfile = sys.argv[2]



    fontname='Times New Roman'
    font = xlwt.Font()
    font.name = fontname
    style = xlwt.XFStyle()
    style.font= font
    workbook = transfer(filename, style)
    workbook.save(outfile)


