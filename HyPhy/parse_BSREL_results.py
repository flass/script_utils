#!/usr/bin/python
import json
import sys
import os
#~ dirbsrel = os.environ['bsreldir']
#~ nfout = "%s_summary.tab"%(dirbsrel)import sys
try:
	dirbsrel = sys.argv[1]
except IndexError:
	print "Usage: %s /path/to/dir_of_BSREL_result_files"%sys.argv[0]
	sys.exit(2)

nfout = "%s_summary.tab"%(dirbsrel)
fout = open(nfout, 'w')
fout.write("gene.locus\tbranch.or.sequence\tlikelihood.ratio\tp.value\n")
for nfbsrel in os.listdir(dirbsrel):
	genename = nfbsrel.split('.')[0]
	if nfbsrel.endswith('.BSREL_out.json'):
		with open("%s/%s"%(dirbsrel, nfbsrel), 'r') as fbsrel:
			bsrelout = json.load(fbsrel)
			res = bsrelout["test results"]
			for branchorseq, dtest in res.iteritems():
				if not dtest["LRT"]=='test not run':
					fout.write("%s\t%s\t%g\t%g\n"%(genename, branchorseq, dtest["LRT"], dtest["p"]))

fout.close()

exit()
