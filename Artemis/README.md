The Python script `prep_blastout4ACT.py` allows you to provide blast-based genome comparisons to ACT (Artemis Comparison Tool) in the right format.
This script can be used on standard output from `blastn` (from Blast+ package) in the tabular format, with commented header or not (`-outfmt` `6` or `7`)
The script requires Python 3, BioPython, and you'll need Blast+ for the intiatial similarity search; this can be set up using an Anaconda environment such as defined below:

```sh
# create the environment - only run once!
conda create -n prep4ACT -c bioconda biopython blast
# activate it
conda activate prep4ACT
```
Here is an example how to use the script:
```sh
## produce standard blast output format, with commented header
# strain O395 vs. strain N16961
blastn -query GCF_000016245.1_ASM1624v1_genomic.O395.fna -subject GCF_900205735.1_N16961_v2_genomic.fna -evalue 1e-05 -outfmt 7 > O395_vs_N16961.blastout
python prep_blastout4ACT.py --inblast O395_vs_N16961.blastout --outblast O395_vs_N16961.blastout.act --queryref GCF_000016245.1_ASM1624v1_genomic.O395.gbff --subjectref GCF_900205735.1_N16961_v2_genomic.gbff
# strain N16961 vs. 48853_G01 (O139)
blastn -query GCF_900205735.1_N16961_v2_genomic.fna -subject 48853_G01.pacbio.fna -evalue 1e-05 -outfmt 7 > N16961_vs_48853_G01.blastout
python prep_blastout4ACT.py --inblast N16961_vs_48853_G01.blastout --outblast N16961_vs_48853_G01.blastout.act --queryref GCF_900205735.1_N16961_v2_genomic.fna --subjectref 48853_G01.pacbio.fna
```
