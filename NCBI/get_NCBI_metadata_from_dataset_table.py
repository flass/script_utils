#!/usr/bin/env python3

import sys, os
import getopt
import re
from Bio import Entrez
#from io import BytesIO

ncbi_dbs = ['pubmed', 'bioproject', 'biosample', 'assembly']

isolfield = 'Isolate_name'
ncbiaccfield = 'NCBI_accession'
required_input_fields = [isolfield, ncbiaccfield]

ignore_bioprojects_default = {'514245', '224116', '608517', '248064'} # Umbrella NCBI projects to ignore
# include of  and RefSeq collection
#PRJNA514245	assembly of 150k prokaryotic SRA short read sets with SKESA
#PRJNA224116	RefSeq genome assembly collection
#PRJNA608517	Bactopia pipeline (spurious record association with 250k assemblies)
#PRJNA248064	Whole genome sequencing data from Public Health England (Umbrella project)

bioprojdocsum_pathto_projecttype = "['DocumentSummarySet']['DocumentSummary'][0]['Project_Type']"
exclude_umbrealla = (bioprojdocsum_pathto_projecttype, 'Umbrella project')

srapat = re.compile('[SDE]RR')
asspat = re.compile('GC[AF]_')
sampat = re.compile('SAM|[SDE]RS')

def getDatabaseLink(initid, fromdb, todb, biosamid=None, verbose=False):
	fromdbname = fromdb[0].upper()+fromdb[1:]
	todbname = todb[0].upper()+todb[1:]
	dblink = Entrez.read(Entrez.elink(dbfrom=fromdb, db=todb, id=initid))
	if dblink[0]['LinkSetDb']:
		if verbose: print('  obtained {} links straight from initial database ({}) record {}'.format(todbname, fromdbname, initid))
	else:
		if biosamid:
			dblink = Entrez.read(Entrez.elink(dbfrom='biosample', db='assembly', id=biosamid))
			if verbose: print('  obtained {} links from linked BioSample record {}'.format(todbname, biosamid))
	return dblink
	
def getUIDsFromDatabaseLink(dblink, db, ignoreset=None, verbose=False, exclude_on_docsum_property=None):
	# ignoreset: a set of id strings to be excluded
	# exclude_on_docsum_property: a tuple providing:
	#   in [0], a string to be passed to eval() so to access the Documment Summary element to test
	#   in [1], a string for the vaue that if matched leaads to exclude the entry
	dbids = set([])
	dbaccs = []
	dbname = db[0].upper()+db[1:]
	for k, dblinkelt in enumerate(dblink[0]['LinkSetDb']):
		if verbose: print('  Linked {} record #{}'.format(dbname, k))
		dbids |= set([bpe['Id'] for bpe in dblinkelt["Link"]])
		if ignoreset: dbids -= ignoreset
		if exclude_on_docsum_property:
			exclids = []
			for dbid in dbids:
				docsum = Entrez.read(Entrez.efetch(db=db, id=dbid, rettype='docsum'))
				eltval = eva('docsum'+exclude_on_docsum_property[0])
				if eltval == exclude_on_docsum_property[1]:
					exclids.append(eltval)
			dbids -= set(exclids)
	if verbose: print("    Collected {} UIDs: {}".format(dbname, repr(dbids)))
	return list(dbids)

def getAccFromUIDs(dbids, db, acckey, outxmlprefix=None, verbose=False):
	dbaccs = []
	for dbid in dbids:
		dbhandle = Entrez.efetch(db=db, id=dbid, rettype='docsum')
#		if outxmlprefix:
#			# experimental / not working yet
#			streamio = BytesIO()
#			streamio.write(dbhandle.read())
#			with open(os.path.join(outxmlprefix+"_linked_{}.xml".format(db)), 'w') as foutxml:
#				foutxml.write(str(streamio.read()))
#			streamio.seek(0, 0)
#			dbhandle = streamio
		dbacc = Entrez.read(dbhandle)['DocumentSummarySet']['DocumentSummary'][0][acckey]
		dbaccs.append(dbacc.strip())
	return list(set(dbaccs))

def parseDatabaseLink(dblink, db, acckey, ignoreset={}, verbose=False):
	dbids = getUIDsFromDatabaseLink(dblink, db, ignoreset=ignoreset, verbose=verbose)
	dbaccs = getAccFromUIDs(dbids, db, acckey, verbose=verbose)
	return dbaccs

def parsePubMedLink(dblink, verbose=False):
	dois = []
	shortcits = []
	pmids = getUIDsFromDatabaseLink(dblink, 'pubmed', verbose=verbose)
	for pmid in pmids:
		pmrecord = Entrez.read(Entrez.efetch(db='pubmed', id=pmid, rettype='full'))
		for idrec in pmrecord['PubmedArticle'][0]['PubmedData']['ArticleIdList']:
			if idrec.attributes['IdType'] == 'doi':
				dois.append(str(idrec))
		firstauthlastname = pmrecord['PubmedArticle'][0]['MedlineCitation']['Article']['AuthorList'][0]['LastName']
		if verbose: print('    First author\'s last name: '+firstauthlastname)
#				articledate = pmrecord['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleDate'][0]
		articledate = pmrecord['PubmedArticle'][0]['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']
		articleyear = articledate['Year']
		if verbose: print('    Article year: '+articleyear)
		shortcits.append(firstauthlastname+' et al., '+articleyear)
	return (pmids, dois, shortcits)

def usage():
	s =  "get_NCBI_metadata_from_dataset_table.py [options] intable outtable\n"
	s += " intable     file_path  input tab-delimited table file, with a header line for field/column names.\n"
	s += "                        the following fields are required :\n"
	s += "                          '{}'.\n".format("', '".join(required_input_fields))
	s += " outdir      file_path  output folder.\n"
	s += " Options:\n"
	s += "   --email   string     email address of user for registration on using the NCBI Entrez API.\n"
	s += "   --ignore_bioproj     skip recording specified Bioproject records; defaults to excluding large umbrella projects:\n"
	s += "                         \`{}\`.\n".format(repr(ignore_bioprojects_default))
	s += "   --keep_xml          write the full XML records for the various database entries that were accessed in respective folders\n"
	s += "                       named '[db]_xml/', where db is one of:\n"
	s += "                         '{}'.\n".format("', '".join(ncbi_dbs))
	return s

def main():
	opts, args = getopt.getopt(sys.argv[1:], 'hvx', ['email=', 'ignore_bioproj=', 'verbose', 'keep_xml', 'help'])
	dopt = dict(opts)
	if ('-h' in dopt) or ('--help' in dopt):
		print(usage())
		sys.exit(0)
	
	if len(args)<2:
		print(usage())
		sys.exit(1)
	
	nfintable = args[0]
	dirout = args[1]
	
	verbose = ('-v' in dopt) or ('--verbose' in dopt)
	keepxml = ('-x' in dopt) or ('--keep_xml' in dopt)
	myemail = dopt.get('--email')
	strigbioproj = dopt.get('--ignore_bioproj')
	
	if strigbioproj:
		eval("ignore_bioprojects = "+strigbioproj)
	else:
		ignore_bioprojects = ignore_bioprojects_default
	
	if not myemail:
		myemail = 'me@myself.org'
		print("NCBI Entrez API requires an email address to access; will use "+myemail+" as a placeholder; please edit it as required")
	
	if not os.path.isdir(dirout):
		os.mkdir(dirout)
	
	nfouttable = os.path.join(dirout, 'combined_ncbi_metadata_from-'+os.path.basename(nfintable))

	Entrez.email = myemail
	Entrez.max_tries = 5
	Entrez.sleep_between_tries = 10
	
	if keepxml:
		ddbsubdir = {}
		for ndb in ncbi_dbs:
			subd = os.path.join(dirout, ndb+'_xml')
			if not os.path.isdir(subd):
				os.mkdir(subd)
				ddbsubdir[ndb] = subd
	
	fintable = open(nfintable, 'r')
	tableheader = fintable.readline().rstrip('\r\n').split('\t')
	for reqf in required_input_fields:
		if not (reqf in tableheader):
			raise ValueError("required field '{}' is missing in input table {}.\n Please see \`get_NCBI_metadata_from_dataset_table.py -h\` for list of required fields.".format(reqf, nfintable))
	
	isolfi = tableheader.index('Isolate_name')
	accfi = tableheader.index('NCBI_accession')
	
	fout = open(nfouttable, 'w')
	fout.write('\t'.join(['Isolate_name', 'query_NCBI_accession', 'Biosample_accessions', 'Assembly_accessions', 'Bioproject_accessions', 'Citations_direct_PubMed_link', 'PMIDs_direct_PubMed_link', 'DOIs_direct_PubMed_link', 'Citations_Biosample_PubMed_link', 'PMIDs_Biosample_PubMed_link', 'DOIs_Biosample_PubMed_link',  'Citations_Bioproject_PubMed_link', 'PMIDs_Bioproject_PubMed_link', 'DOIs_Bioproject_PubMed_link'])+'\n')
	
	# iterate over each table line / genome entry
	for line in fintable:
		lsp = line.rstrip('\r\n').split('\t')
		isolate = lsp[isolfi]
		ncbiacc = lsp[accfi]
		
		print('# # # # # #')
		if not ncbiacc:
			print(isolate+": no initial NCBI accession; skip fetching metadata.")
			continue
		else:
			print(isolate+": fetching NCBI metadata using initial accession "+ncbiacc+".")

		# output variables; initiate with empty values
		biosamid = ''
		biosamaccs = []
		biosamacc = ''
		assmbid = ''
		assmbaccs = []
		bioproids = []
		bioproaccs = []
		pmids = []
		dois = []
		shortcits = []
		
    	# devise what NCBI database is referred to
		if srapat.match(ncbiacc): oridb='sra'
		elif asspat.match(ncbiacc): oridb='assembly'
		elif sampat.match(ncbiacc): oridb='biosample'
		else: oridb='nucleotide' # here assume that Nucleotide db is the only alternative
		
		ncbiaccsearch = Entrez.read(Entrez.esearch(db=oridb, term=ncbiacc))
		ncbiaccuid = ncbiaccsearch['IdList'][0]
		
		# search for associated Biosamples
		biosamlink = getDatabaseLink(ncbiaccuid, oridb, 'biosample', verbose=verbose)
		if biosamlink[0]['LinkSetDb']:
			biosamids = getUIDsFromDatabaseLink(biosamlink, 'biosample', verbose=verbose)
			biosamaccs = getAccFromUIDs(biosamids, 'biosample', 'Accession', verbose=verbose)
		# select the Biosample record provided as input or the first linked one for further searches
		if oridb == 'biosample':
			biosamid = ncbiaccuid
			biosamacc = ncbiacc
		else:
			biosamid = biosamids[0]
			biosamacc = biosamaccs[0]
#
#		if oridb == 'assembly':
#			assmbaccs.append(ncbiacc)
#		
		# search for associated Assemblies (even if initial db is assembly, to check if secondary assemblies have been made)
		assmblink = getDatabaseLink(ncbiaccuid, oridb, 'assembly', biosamid, verbose=verbose)
		if assmblink[0]['LinkSetDb']:
			assmbaccs = parseDatabaseLink(assmblink, 'assembly', 'AssemblyAccession', verbose=verbose)
			if len(set(assmbaccs))>0:
				print("    Warning: More than one Assembly acession linked to this entry: "+repr(assmbaccs))
		else:
			if verbose: print('  no associated Assembly record')

		# search for associated Bioproject records
		bioprolink = getDatabaseLink(ncbiaccuid, oridb, 'bioproject', biosamid, verbose=verbose)
		if bioprolink[0]['LinkSetDb']:
#			bioproids = getUIDsFromDatabaseLink(bioprolink, 'bioproject', \
#												exclude_on_docsum_property=exclude_umbrella, \
#												ignoreset=ignore_bioprojects, verbose=verbose)
			bioproids = getUIDsFromDatabaseLink(bioprolink, 'bioproject', ignoreset=ignore_bioprojects, verbose=verbose)
			bioproaccs = getAccFromUIDs(bioproids, 'bioproject', 'Project_Acc', verbose=verbose)
		else:
			if verbose: print('  no associated Bioproject record')

		# search for associated PubMed records
		pubmedlink = Entrez.read(Entrez.elink(dbfrom=oridb, db='pubmed', id=ncbiaccuid))
		if pubmedlink[0]['LinkSetDb']:
			if verbose: print('  obtained Pubmed links straight from initial database ({}) record {}'.format(oridb, ncbiacc))
			pmids, dois, shortcits = parsePubMedLink(pubmedlink, verbose=verbose)
		elif verbose: print('  no Pubmed record associated to initial accession')
		# gather PubMed links from associated Biosample record
		bspmids = [] ; bsdois = [] ; bsshortcits = []
		if biosamid:
			bspubmedlink = Entrez.read(Entrez.elink(dbfrom='biosample', db='pubmed', id=biosamid))
			if verbose: print('  obtained Pubmed links from linked BioSample record {}'.format(biosamid))
			if bspubmedlink[0]['LinkSetDb']:
				bspmids, bsdois, bsshortcits = parsePubMedLink(bspubmedlink, verbose=verbose)
			elif verbose: print('  no Pubmed record associated to BioSample record')
		# gather PubMed links from associated Bioproject records
		bppmids = [] ; bpdois = [] ; bpshortcits = []
		for bioproid in bioproids:
			bppubmedlink = Entrez.read(Entrez.elink(dbfrom='bioproject', db='pubmed', id=bioproid))
			if verbose: print('  obtained Pubmed links from linked Bioproject record {}'.format(biosamid))
			if bppubmedlink[0]['LinkSetDb']:
				sbppmids, sbpdois, sbpshortcits = parsePubMedLink(bppubmedlink, verbose=verbose)
				bppmids += sbppmids
				bpdois += sbpdois
				bpshortcits += sbpshortcits
		# write result line to ouput table
		fout.write('\t'.join([isolate, ncbiacc, ';'.join(biosamaccs), ';'.join(assmbaccs), ';'.join(bioproaccs), ';'.join(shortcits), ';'.join(pmids), ';'.join(dois), ';'.join(bsshortcits), ';'.join(bspmids), ';'.join(bsdois), ';'.join(bpshortcits), ';'.join(bppmids), ';'.join(bpdois)])+'\n')
		fout.flush() # ensure regular writing of output, considering the expected slow progress of script as limited by web queries
		
		print(isolate+": done.")

	fintable.close()
	fout.close()


if __name__=='__main__':
	
	main()
