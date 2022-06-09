A script to collect genome metadata and database cross-references from the NCBI based on a heterogeneous list of query genome accessions.

```sh
get_NCBI_metadata_from_dataset_table.py [options] intable outtable
 intable     file_path  input tab-delimited table file, with a header line for field/column names.
                        the following fields are required :
                          'Isolate_name', 'NCBI_accession'.
 outdir      file_path  output folder.
 Options:
   --email   string     email address of user for registration on using the NCBI Entrez API.
   --ignore_bioproj     skip recording specified Bioproject records; defaults to excluding large umbrella projects:
                         `{'608517', '514245', '248064', '224116'}`.
   --keep_xml          write the full XML records for the various database entries that were accessed in respective folders
                       named '[db]_xml/', where db is one of:
                         'pubmed', 'bioproject', 'biosample', 'assembly'. (option not yet functional)

```