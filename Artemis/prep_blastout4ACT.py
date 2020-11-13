#!/usr/bin/env python3
from Bio import SeqIO
from BCBio import GFF
import os, sys, getopt

blasttabfields = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']


opts, args = getopt.getopt(sys.argv[1:], "", ['inblast=','outblast='])
dopt = dict(opts)

nfinblasttab = dopt['--inblast']
nfoutblasttab = dopt['--outblast']

lnfseqrec = args

dcontigconcatcoord = {}

for nfseqrec in lnfseqrec:
	nfext = os.path.basename(nfseqrec).rsplit('.', 1)[1]
	if nfext=='gff':
		seqrecs = GFF.parse(nfseqrec)
	elif nfext in ['gbk', 'gbff']:
		seqrecs = SeqIO.parse(nfseqrec, format='genbank')
	elif nfext in ['fna', 'fsa', 'fasta', 'fa']:
		seqrecs = SeqIO.parse(nfseqrec, format='fasta')
	else:
		raise ValueError("unknown file format")
	cumseqlen = 0
	for seqrec in seqrecs:
		dcontigconcatcoord[seqrec.id] = cumseqlen
		cumseqlen += len(seqrec)

fout = open(nfoutblasttab, 'w')

with open(nfinblasttab, 'r') as fin:
	for line in fin:
		if line.startswith('#'):
			continue
		lsp = line.rstrip('\n').split('\t')
		dhit = dict(zip(blasttabfields, lsp))
#		print(dhit)
		for fcoord, fseqid in [('qstart', 'qseqid'), ('qend', 'qseqid'), ('sstart', 'sseqid'), ('send', 'sseqid')]:
#			print(fcoord)
#			print(fseqid)
			dhit[fcoord] = str(int(dhit[fcoord]) + dcontigconcatcoord[dhit[fseqid]])
		fout.write('\t'.join([dhit[f] for f in blasttabfields])+'\n')
		
fout.close()