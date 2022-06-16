#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from os import path
import sys

exclude_criteria = ['fragmented assembly',\
					'genome length too small',\
					'low quality sequence',\
					'many frameshifted proteins',\
					'missing ribosomal protein genes',\
					'RefSeq annotation failed']
#					'derived from metagenome',\
#					'from large multi-isolate project',\
#					'genome length too large',\

def iterGetElt(xmlelt, name):
	for childelt in xmlelt:
		if childelt.tag == name:
			return childelt

def recurseGetElt(xmlelt, namepath=[]):
	if namepath and xmlelt:
		childelt = iterGetElt(xmlelt, namepath[0])
		return recurseGetElt(childelt, namepath[1:])
	else:
		return xmlelt
	
def getAllEltDict(xmlelt, names=None):
	childeltdict = {}
	for childelt in xmlelt:
		if names and (childelt.tag not in names): continue
		childeltdict[childelt.tag] = childelt
	return childeltdict
	
def collectChildrenVals(xmlelt, names=None):
	values = []
	for childelt in xmlelt:
		if names and (childelt.tag not in names): continue
		values.append(childelt.text)
	return values

def usage():
	s =  "parse_Assembly_DocSumXML.py assembly_docsum.xml out_file_prefix"
	s += "\tassembly_docsum.xml\tan XML file as produced by exporting the Document Summary from an NCBI Entrez search for multiple Assembly accessions. Multiple DocumentSummary XML elements should be separated by  an empty newline\n"
	s += "\tout_file_prefix\tprefix for the output files, inlcuding a summary of collected data and a filtered list of assemblies (excluding assemblies tagged with the folowing properties in the 'ExclFromRefSeq' field: {}\n".format(repr(exclude_criteria))
	return s

args = sys.argv[1:]
if len(args)!=2:
	print(usage())
	sys.exit(1)

if args[0] in ('-h', '--help'):
	print(usage())
	sys.exit(0)

nfinxml = args[0]
nfoutprefix = args[1]
fxml = open(nfinxml, 'r')
currxmlelts = ""
xmlelt = None
assacc = ''
nfout = nfoutprefix+"-parsed.txt"
nfoutkeepacc = nfoutprefix+"-filtered_acc_list.txt"
fout = open(nfout, 'w')
foutkeepacc = open(nfoutkeepacc, 'w')
outfields = ['AssemblyAccession', 'Strain', 'ExclFromRefSeq']
fout.write('\t'.join(outfields)+'\n')
#foutkeepacc.write('\t'.join(outfields[:-1])+'\n')

for line in fxml:
	if line!='\n':
		currxmlelts += line
	else:
		xmlelt = ET.fromstring(currxmlelts)
		currxmlelts = ""
		alltopelt = getAllEltDict(xmlelt)
		assacc = alltopelt['AssemblyAccession'].text
		print(assacc)
		biosourceelt = alltopelt['Biosource']
#		strain = iterGetElt(iterGetElt(iterGetElt(biosourceelt, 'InfraspeciesList'), 'Infraspecie'), 'Sub_value').text
		strainelt = recurseGetElt(biosourceelt, ['InfraspeciesList', 'Infraspecie', 'Sub_value'])
		if strainelt: strain = strainelt.text
		else: strain = ''
		exclfromRS = collectChildrenVals(alltopelt['ExclFromRefSeq'])
		fout.write('\t'.join([assacc, strain, ';'.join(exclfromRS)])+'\n')
		if not set(exclfromRS) & set(exclude_criteria):
			foutkeepacc.write(assacc+'\n')

fout.close()
foutkeepacc.close()