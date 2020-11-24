#/usr/bin/env python2.7
import sys, os

def usage():
	s = "Usage:\n%s input_aln1 input_aln2 [input_alnN, ...] output_aln"%(os.path.basename(sys.argv[0]))
	return s

if len(sys.argv)<2:
	print "Error: missing arguments"
	print usage()
	sys.exit(1)

if sys.argv[1] in ['-h', '--help']:
	print usage()
	sys.exit(0)

lnfalnin = sys.argv[1:-1]
nfalnout = sys.argv[-1]

lfinhandles = [open(nfalnin, 'r') for nfalnin in lnfalnin]

fout = open(nfalnout, 'w')

currlabel = None

def iterOneLabel(lfinhandles, fout, currlabel):
	for i, fin in enumerate(lfinhandles):
		for line in fin:
			if line.startswith('>'):
				if i==0:
					currlabel = line
					fout.write(line)
					break	
				else:
					if line != currlabel:
						print line
						print currlabel
						raise IndexError, "labels (fasta headers) are not orderred the same in input files"
					else:
						break # 'for line in fin' loop
			else:
				if line.rstrip('\n'):
					fout.write(line)
	return currlabel

nextlabel = iterOneLabel(lfinhandles, fout, currlabel)
while nextlabel != currlabel:
	currlabel = nextlabel
	nextlabel = iterOneLabel(lfinhandles, fout, currlabel)
	print nextlabel

for fin in lfinhandles:
	fin.close()

fout.close()

	

				