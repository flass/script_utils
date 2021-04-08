## script_utils: some miscellaneous bioinformatics scripts

There is lots of stuff in here, please feel free to use! In particular, you can find the following thematic folders:

- `misc/` gathers... miscelaneous scripts, including for automated download of genome asemblies from the NCBI FTP service, translating NCBI accession ids from Nuleotide to Assembly databases, splitting multi-record GenBank flat files, or simply efficiently generating a list of file full paths.   
- `HyPhy/` includes submission scripts for running application from the HyPhy phylogenetic analysis package, in particular for those that requie a MPI environment
- `AMR_search/` includes submission scripts for systematic search of AMR genes using a variety of mainstream tool (RGI, ABRICATE, Resfinder)
- `phylogenetics/` includes submission scripts for a variety of tree building programs RAxML and MrBayes (typically used on many gene trees of a same dataset) and for gene tree/species tree reconcilation programs ALE, ecceTERA and GeneRax
- `LSFcluster_SangerInstitute/` includes susbmission scripts generally fit for job sumission on a **LSF computer cluster** system (using `bsub` command), with some specific reference to the environment of the Sanger Insitute farm
- `PBScluster_ImperialCollege/` includes susbmission scripts generally fit for job sumission on a **PBS computer cluster** system (using `bsub` command), with some specific reference to the environment of the Imperial College cluster
- `SGEcluster_UCL-CS/` includes susbmission scripts generally fit for job sumission on a **SGE computer cluster** system (using `qsub` command), with some specific reference to the environment of the UCL Computer Science Department cluster
- `R/` gathers miscelaneous `R` scripts, including one to generate metadata dataset files for iTOL phylogenetic tree annotation, or a list of countries in each UN subregion.
`*_array.[bq]sub` scripts are designed for the submission of *array* jobs on these respective systems, with the general syntax:
```
xsub [submission command options] script_array.xsub tasklist [other arguments]
```
where `tasklist` is the path to a file containing a list of files (their FULL paths) or arguments which will be used as specific input for each subjob of the array job.

An example of this syntax:
```sh
# create the task list file (here listing contig files)
ls $PWD/contigs/*.fa > contiglist
# create folder for the output and logs, respectively
mkdir -p AMR/abricate/ logs/abricate/
# count the number of tasks to submit to the array job
Njobs=$(wc -l contiglist | cut -d' ' -f1)
# define other arguments, here the reference databases to search with ABRICATE
abdbs='ncbi,card,plasmidfinder,argannot,vfdb,resfinder'
# submit the array job
bsub -J abricate-muldb[1-${Njobs}]%50 -R "select[mem>4000] rusage[mem=4000]" -M4000 -q normal \
-e logs/abricate/abricate-muldb.%J.%I.log -o logs/abricate/abricate-muldb.%J.%I.log \
scripts_utils/AMR_search/abricate_multipledb_array.bsub contiglist AMR/abricate/ "${abdbs}"
```
