#!/usr/bin/python
import json
import sys
import os
#~ dirbusted = os.environ['busteddir']
try:
	dirbusted = sys.argv[1]
except IndexError:
	print "Usage: %s /path/to/dir_of_BUSTED_result_files"%sys.argv[0]
	sys.exit(2)

nfout = "%s_summary.tab"%(dirbusted)
fout = open(nfout, 'w')
fout.write("gene.locus\tlikelihood.ratio\tp.value\n")
for nfbusted in os.listdir(dirbusted):
	genename = nfbusted.split('.')[0]
	if nfbusted.endswith('.BUSTED.json'):
		with open("%s/%s"%(dirbusted, nfbusted), 'r') as fbusted:
			bustedout = json.load(fbusted)
			res = bustedout["test results"]
			fout.write("%s\t%g\t%g\n"%(genename, res["LR"], res["p"]))

fout.close()
sys.exit(0)
