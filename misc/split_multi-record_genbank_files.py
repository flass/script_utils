#!/usr/bin/env python2.7

from Bio import SeqIO
import sys, os, gzip, glob

lnfinpat = sys.argv[1:-1]
dirout = sys.argv[-1]

for nfinpat in lnfinpat:
	for nfin in glob.glob(nfinpat):
		if nfin.endswith('.gz'):
			fin = gzip.open(nfin, 'rb')
		else:
			fin = open(nfin, 'r')
		seqrecit = SeqIO.parse(fin, format='genbank')
		for seqrec in seqrecit:
			seqid = seqrec.id
			nfout = seqid+'.gbk'
			with open(os.path.join(dirout, nfout), 'w') as fout:
				SeqIO.write([seqrec], fout, format='genbank')
		fin.close()
