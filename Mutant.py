#!/bin/env python
# 2014-3-18 created by Linxzh
# SNP mutation detection

from Bio import SeqIO
from Bio.Alphabet import IUPAC
from Bio.Seq import MutableSeq


# handle the record id 
def get_accession(record):
	parts = record.id.split()
	return parts[0]

# converse the gff file into a dict
def Gff_dict(infile):
	D = {}
	for x in infile:

		if 'Scaffold' in x:
			continue
		elif 'gene' in x:
			xlist = x.split()
			gid = xlist[8].split('=')[1][:-1]
			key = xlist[0] + '-' + gid 
			value = [int(xlist[3]),int(xlist[4]),xlist[6], gid]
			D[key] = value

	return D

# find the sym
def Mutant(chrom,start, end, strand, base, pos,fa_dict,snp):
	'''we need to read the corresponding gene location by SNP
	position in the GFF file'''
	if strand == '+':
		step = (pos - start)/3
		p = (pos - start)% 3
		code = fa_dict[chrom][start-1+3*step:start-1+3*(1+step)]
		asnp_code = bsnp_code = code.seq.tostring()
		asnp_code = asnp_code[1:p] + base + asnp_code[1+p:]
		ap = asnp_code.toseq().translate().to
		bsnp_code[p] = snp
		bp = asnp_code.toseq().translate().tostring()
	elif strand == '-':
		step = (end -pos)/3
		code = fa_dict[chrom][end-3*(1+step):end-3*step]
		p = (end-pos)%3
		asnp_code = bsnp_code = code.seq.tomutable()
		bsnp_code[2-p]=snp
		asnp_code[2-p]=base
		ap = asnp_code.reverse_complement().toseq().translate().tostring()
		bp = bsnp_code.reverse_complement().toseq().translate().tostring()
	print asnp_code,bsnp_code,base,snp,p	
	if ap == bp:
		sym = 'yes'
	else:
		sym = 'no'

	wl = '%s%s%s\t%s%s%s\t%s\n' % (asnp_code,chr(26),bsnp_code,ap,chr(26),bp,sym)
	return wl

def SNP_in_GID(gffdict, infile, outfile):
	
	cucu_fa = SeqIO.to_dict(SeqIO.parse(\
			'/share/fg3/Linxzh/Data/Cucumber_ref/domestic_Chr_20101102.fa',\
			'fasta'),key_function=get_accession)
	for x in infile:
		if '#' in x:
			wl = '%s\t%s\t%s\t%s\t%s\t%s\n' % (x[:-1],'start','end','pos',\
					'strand','gid')
			outfile.write(wl)
			continue
		xlist = x.split()
		pos = int(xlist[1])
		chrom = xlist[0]
		base = xlist[2]
		snp = xlist[3]
		for k in gffdict:
			if xlist[0] in k:
				start = gffdict[k][0]
				end = gffdict[k][1]
				strand = gffdict[k][2]
				if pos >= start and pos <= end:
					mut_line = Mutant(chrom,start,end,strand,base,pos,cucu_fa,snp)
					wl = '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (x[:-1],start,end,\
							pos,strand,gffdict[k][3],mut_line)
					outfile.write(wl)




if __name__ == '__main__':
	gfffile = open('/share/fg3/Linxzh/Data/Cucumber_ref/Cucumber_20101104.gff3')
	snpfile = open('rare_snp.txt')
	outfile = open('tmp_file.txt','w')
	gffdict = Gff_dict(gfffile)
	SNP_in_GID(gffdict, snpfile, outfile)
	outfile.close()
	snpfile.close()

	

