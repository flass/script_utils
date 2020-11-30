#!/usr/bin/env python3
from Bio import SeqIO
import os, sys, getopt

blasttabfields = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']

def usage():
	s = sys.argv[0]+" --inblast blast+.output.outfmt6or7.file --outblast ACT.crunch.formated.file [query.sequence.chrom1.{gff|gbk|fasta}, [query.sequence.chrom2.{gff|gbk|fasta}], ...]"
	return s

opts, args = getopt.getopt(sys.argv[1:], "h", ['inblast=','outblast=', 'help'])
dopt = dict(opts)
if (('-h' in dopt) or ('--help' in dopt)):
	print(usage())
	sys.exit(0)

if not (('--inblast' in dopt) and ('--outblast' in dopt)):
	print("Error: missing operands:")
	print(usage())
	sys.exit(1)
	
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