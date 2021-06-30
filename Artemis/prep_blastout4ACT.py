#!/usr/bin/env python3
from Bio import SeqIO
import os, sys, getopt
from BCBio import GFF

blasttabfields = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']

def usage():
	s = sys.argv[0]+" --inblast blast+.output.outfmt6or7.file --outblast ACT.crunch.formated.file [--queryref=query.sequence.{gff|gbk|fasta}] [--subjectref=subject.sequence.{gff|gbk|fasta}]\n"
	s += "  options '--queryref' and '--subjectref' allow to provide reference sequence\n"
	s += "  in multi-fasta, multi-genbank flat file or GFF format."
	s += "  This allows to correct the coordinates in case there are several records\n"
	s += "  (molecules, contigs) in the query and/or subject genomes.\n"
	s += "  Genome sequences (and their partition in multiple records need to be\n"
	s += "  the same as in Blast input query/subject, but they can be annotatted\n"
	s += "  differently, for instance with different ids.\n"
	return s

opts, args = getopt.getopt(sys.argv[1:], "h", ['inblast=','outblast=', 'queryref=', 'subjectref=', 'help'])
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

dnfseqrec = {}
if '--subjectref' in dopt:
	dnfseqrec['s'] = dopt['--subjectref']
if '--queryref' in dopt:
	dnfseqrec['q'] = dopt['--queryref']

dcontigconcatcoord = {}
drefqsseqid = {}

for refkey, nfseqrec in dnfseqrec.items():
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
		drefqsseqid.setdefault(refkey, []).append(seqrec.id) # ordered list of encountered sequence ids for query and subject as in reference sequence files
		cumseqlen += len(seqrec)

fout = open(nfoutblasttab, 'w')

with open(nfinblasttab, 'r') as fin:
	for line in fin:
		if line.startswith('#'):
			continue
		lsp = line.rstrip('\n').split('\t')
		dhit = dict(zip(blasttabfields, lsp))
#		print(dhit)
		dblaqsseqid = {'s':[], 'q':[]} # ordered list of encountered sequence ids for query and subject as in files used in blast search
		for fcoord, fseqid in [('qstart', 'qseqid'), ('qend', 'qseqid'), ('sstart', 'sseqid'), ('send', 'sseqid')]:
#			print(fcoord)
#			print(fseqid)
			seqid = dhit[fseqid]
			fk = fcoord[0]
			if not seqid in dblaqsseqid.get(fk, []):
				dblaqsseqid[fk].append(seqid)
			iseq = dblaqsseqid[fk].index(seqid)
			hitcoord = int(dhit[fcoord])
			if drefqsseqid:
				if seqid in dcontigconcatcoord:
					hitcoord += dcontigconcatcoord[seqid]
				else:
					hitcoord += dcontigconcatcoord[drefqsseqid[fk][iseq]]
			dhit[fcoord] = str(hitcoord)
		fout.write('\t'.join([dhit[f] for f in blasttabfields])+'\n')
		
fout.close()