## script_utils: some miscellaneous bioinformatics scripts

There is lots of stuff in here, please feel free to use! In particular, you can find the following thematic folders:

- `HyPhy/` include submission scripts for running application from the HyPhy phylogenetic analysis package, in particular for those that requie a MPI environment
- `AMR_search/` include submission scripts for systematic search of AMR genes using a variety of mainstream tool (RGI, ABRICATE, Resfinder)

- `LSFcluster_SangerInstitute/` include susbmission scripts generally fit for job sumission on a LSF computer cluster system (using `bsub` command), with some specific reference to the environment of the Sanger Insitute farm
- `SGEcluster_UCL-CS/` include susbmission scripts generally fit for job sumission on a SGE computer cluster system (using `qsub` command), with some specific reference to the environment of the UCL Computer Science Department cluster

`*_array.[bq]sub` scripts are designed for the submission of *array* jobs on these respective systems, with the general syntax:
```sh
xsub [submission command options] script_array.xsub tasklist [other arguments]
```
where `tasklist` is the path to a file containing a list of files (their FULL paths) or arguments which will be used as specific input for each subjob of the array job.

An example of this syntax:
```sh
ls $PWD/contigs/*.fa > contiglist
mkdir -p AMR/abricate/ logs/abricate/
Njobs=$(wc -l contiglist | cut -d' ' -f1)
abdbs='ncbi,card,plasmidfinder,argannot,vfdb,resfinder'

bsub -J abricate-muldb[1-${Njobs}]%50 -R "select[mem>4000] rusage[mem=4000]" -M4000 -q normal \
-e logs/abricate/abricate-muldb.%J.%I.log -o logs/abricate/abricate-muldb.%J.%I.log \
scripts_utils/AMR_search/abricate_multipledb_array.bsub contiglist AMR/abricate/ "${abdbs}"
```
