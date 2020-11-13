#!/usr/bin/env python2.7

import json
import sys, os

def parse_resfinder_json(nfjson, dsamplefoundres={}, dsamplepheno={}):
	orgtag = '[organism='
	phenotag = ' resistance'
	sample = os.path.basename(nfjson).rsplit('.json', 1)[0]
	if sample=='data_resfinder':
		sample = os.path.basename(os.path.dirname(nfjson))
	with open (nfjson) as fjson:
		rf = json.load(fjson)
	for Ab, res in rf['resfinder']['results'].iteritems():
		ab = str(Ab.lower())
		dresab = res[ab]
		if dresab=='No hit found':
			restag = 'S'
		else:
			restag = 'R'
			for hit in dresab:
				resab = dresab[hit]
				# parse phenotype
				prph = resab.get('predicted_phenotype')
				if prph.startswith('Warning'):
					print "sample '%s', antibiotic '%s': %s"%(sample, ab, str(prph))
				elif prph is None:
					raise ValueError, "unexpected absence of 'predicted_phenotype' element in sample '%s', antibiotic '%s':\n'%s'"%(sample, ab, str(resab))
				else:
					prph0 = prph.rsplit(phenotag, 1)
					if prph0[1].strip():
						print "sample '%s', antibiotic '%s': '%s'"%(sample, ab, prph0[1].strip())
				prph12 = prph0[0].rsplit(' and ', 1)
				if len(prph12)==1:
					lpheno = prph12
				else:
					lpheno = prph12[0].split(', ') + [prph12[1]]
				dsamplepheno.setdefault(sample, set([])).update(lpheno)
				# parse genotype
				resgene = resab.get('resistance_gene', '')
				reshitid = resab.get('hit_id', '')
				rescontig = resab.get('contig_name', '')
				if orgtag in reshitid:
					hitorg = reshitid.split(orgtag, 1)[1].split(']', 1)[0].replace(' ', '_')
				elif orgtag in rescontig:
					hitorg = rescontig.split(orgtag, 1)[1].split(']', 1)[0].replace(' ', '_')
				else:
					hitorg = ''
				restag += ':%s-%s'%(resgene, hitorg)
		dsamplefoundres.setdefault(sample, {}).setdefault(ab, restag)
	return dsamplefoundres

if __name__ == '__main__':

	nflnfin = sys.argv[1]
	nfout = sys.argv[2]

	dsamplefoundres = {}
	dsamplepheno = {}
	with open(nflnfin, 'r') as flnfin:
		for line in flnfin:
			nfin = line.strip('\n')
			parse_resfinder_json(nfin, dsamplefoundres, dsamplepheno)
	
	sab = set([])
	for sample, d in dsamplefoundres.iteritems():
		sab.update(d.keys())
	lab = sorted(sab)
	
	ftabout = open(nfout+'.tab', 'w')
	fdetout = open(nfout+'.details', 'w')
	header = '\t'.join(['sequence_id', 'res_phenotype']+lab)+'\n'
	ftabout.write(header)
	lsamples = sorted(dsamplefoundres.keys())
	for sample in lsamples:
		pheno = ', '.join(sorted(dsamplepheno.get(sample, '')))
		foundres = dsamplefoundres[sample]
		resprofile = [(ab, foundres.get(ab, '')) for ab in lab]
		ftabout.write('\t'.join([sample, pheno]+[res.split(':', 1)[0] for ab, res in resprofile])+'\n')
		fdetout.write('\n'.join(['\t'.join([sample, ab, res]) for ab, res in resprofile if (res!='S')])+'\n')
	
	ftabout.close()
	fdetout.close()