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
print "input:"
print '\n'.join(lnfalnin)
print "output:"
print nfalnout

lfinhandles = [open(nfalnin, 'r') for nfalnin in lnfalnin]
fout = open(nfalnout, 'w')

currlabel = None

def iterOneLabel(lfinhandles, fout, currlabel):
	if not (currlabel is None):
		fout.write(currlabel)
	for i, fin in enumerate(lfinhandles):
#		print fin
		for line in fin:
#			print line[0:min(12, len(line))]
			if line.startswith('>'):
				if i==0:
					currlabel = line
#					print 'here'
				else:
					if line != currlabel:
						print line
						print currlabel
						raise IndexError, "labels (fasta headers) are not orderred the same in input files"
#					print 'there'
				break # 'for line in fin' loop
			else:
				fout.write(line)
#				print 'la'
	fout.flush()
	return currlabel

nextlabel = iterOneLabel(lfinhandles, fout, currlabel)
n = 1
#print ""
while nextlabel != currlabel:
	currlabel = nextlabel
	nextlabel = iterOneLabel(lfinhandles, fout, currlabel)
	sys.stdout.write("\r%d %s"%(n, nextlabel.rstrip('\n')))
#	print ""
	n += 1
#	if n == 4: break

for fin in lfinhandles:
	fin.close()

fout.close()
print " done."

	

				