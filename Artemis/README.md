The Python script `prep_blastout4ACT.py` allows you to provide blast-based genome comparisons to ACT (Artemis Comparison Tool) in the right format.
This script can be used on standard output from `blastn` (from Blast+ package) in the tabular format, with commented header or not (`-outfmt` `6` or `7`)
The script requires Python 3, BioPython, and you'll need Blast+ for the intitial similarity search; this can be set up using an Anaconda environment such as defined below:

```sh
# create the environment - only run once!
conda create -n prep4ACT -c bioconda biopython blast
# activate it
conda activate prep4ACT
```
Here is an example how to use the script (here aiming at comparing a trio of _V. cholerae_ strains):
```sh
## produce standard blast output format, with commented header
# strain O395 vs. strain N16961
blastn -query GCF_000016245.1_ASM1624v1_genomic.O395.fna -subject GCF_900205735.1_N16961_v2_genomic.fna -evalue 1e-05 -outfmt 7 > O395_vs_N16961.blastout
# strain N16961 vs. 48853_G01 (O139)
blastn -query GCF_900205735.1_N16961_v2_genomic.fna -subject 48853_G01.pacbio.fna -evalue 1e-05 -outfmt 7 > N16961_vs_48853_G01.blastout
## then reformat the output
python prep_blastout4ACT.py --inblast O395_vs_N16961.blastout --outblast O395_vs_N16961.blastout.act GCF_000016245.1_ASM1624v1_genomic.O395.gbff GCF_900205735.1_N16961_v2_genomic.gbff
python prep_blastout4ACT.py --inblast N16961_vs_48853_G01.blastout --outblast N16961_vs_48853_G01.blastout.act GCF_900205735.1_N16961_v2_genomic.fna 48853_G01.pacbio.fna
```

Then here is the best way to load the data into ACT:
- open ACT
- in the `File` tab, choose `Open...`
- for `Sequence File 1`, choose the first reference sequence file - it is best to load a simple fasta file, rather than a annotated sequence file, in this case the one as used in the blast search: `GCF_000016245.1_ASM1624v1_genomic.O395.fna`
- for the `Comparison File 1` choose the first reformated blast output: `O395_vs_N16961.blastout.act`
- for `Sequence File 2`, choose the second reference sequence file in fasta format: `GCF_900205735.1_N16961_v2_genomic.fna`
- then click on `more files...`
- for the `Comparison File 2` choose the first reformated blast output: `N16961_vs_48853_G01.blastout.act`
- for `Sequence File 3`, choose the second reference sequence file in fasta format: `48853_G01.pacbio.fna`
- then click `Apply`; you should get the ACT display of genome comparisons
- finally to load the genome annotations, go to th tab `Entries`, select the first entry `GCF_000016245.1_ASM1624v1_genomic.O395.fna` and click on load an entry
- there you can load a corresponding annotation file; I recommend loading the corresponding GFF file, as would have been obtained from the same NCBI Assembly folder: `GCF_000016245.1_ASM1624v1_genomic.O395.gff`
- repeat this for the other two genomes
