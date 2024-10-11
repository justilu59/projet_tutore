# projet_tutore
**03/10**

**Importation des données des génomes de référence des 3 espèces de fourmis T.septentrionalis, T.cornetzi et T.zeteki avec l'outil ncbi-datasets-cli version 16.31.0**:

datasets download genome accession GCF_001594115.1 --include gff3,rna,cds,protein,genome,seq-report

datasets download genome accession GCF_001594075.2 --include gff3,rna,cds,protein,genome,seq-report

datasets download genome accession GCF_001594055.1 --include gff3,rna,cds,protein,genome,seq-report

Les mêmes commandes sont exécutées pour l'annotation gca.

**Importation des données de RNA-seq avec l'outil sra-tools version 3.1.1**:

fastq-dump --split-files --gzip SRR3270634

fastq-dump --split-files --gzip SRR3270378

fastq-dump --split-files --gzip SRR3270377

**04/10** 

**Génération du rapport de qualité des reads forward et reverse de T.cornetzi et de T.septentrionalis avec l'outil Fastqc version 0.11.9 et application des commandes**:

fastqc -o quality_reports/T_cornetzi raw_reads/T_cornetzi/SRR3270378_1.fastq.gz raw_reads/T_cornetzi/SRR3270378_2.fastq.gz 

fastqc -o quality_reports/T_septentrionalis raw_reads/T_septentrionalis/SRR3270634_1.fastq.gz raw_reads/T_septentrionalis/SRR3270634_2.fastq.gz

**06/10** 

**Analyse de qualité des reads SRR3270634_1 et SRR3270634_2 de T.septentrionalis** : 
- reads de longueur 90 pb et 
- 42% GC, 
- per base sequence content : on oberve une distribution non uniforme pour les 10-15 nucléotides, ce qui est normal en RNA-seq
- sequence duplication level : on a un certain nombre de reads qui sont présents plusieurs fois, il est attendu d'avoir des reads dupliqués pour les transcrits de forte abondance
- overrepresented sequence : il y a présence de séquence qui correspond à un adaptateur Truseq dans SRR3270634_1

**Elimination de la séquence correspondant à l'adaptateur avec l'outil cutadapt version 4.9 et la commande** :

cutadapt -a GATCGGAAGAGCACACGTCTGAACTCCAGTCACTTAACCGGATCTCGTAT -o SRR3270634_1_trimmed.fastq.gz -z raw_reads/T_septentrionalis/SRR3270634_1.fastq.gz

**Génération de l'index des génomes gcf et gca de T.septentrionalis ave l'outil STAR version 2.7.11b et les commandes** :

STAR --runMode genomeGenerate --genomeDir index_genomes/index_gcf/T_septentrionalis --genomeFastaFiles genomes/gcf_genomes/T_septentrionalis/ncbi_dataset/data/GCF_001594115.1/GCF_001594115.1_Tsep1.0_genomic.fna --runThreadN 4 --genomeSAindexNbases 13

STAR --runMode genomeGenerate --genomeDir index_genomes/index_gca/T_septentrionalis --genomeFastaFiles genomes/gca_genomes/T_septentrionalis/ncbi_dataset/data/GCA_001594115.1/GCA_001594115.1_Tsep1.0_genomic.fna --runThreadN 4 --genomeSAindexNbases 13


**8/10**

Le trimming a induit des incohérences dans la longueur des séquences et qualité associées à SRR3270634_trimmed_1 donc utilisation des reads non trimmés pour le mapping.

**Mapping des reads SRR3270634_1.fastq et SRR3270634_2.fastq de T.septentrionalis sur les génomes de références gca et gcf de T.septentrionalis avec l'outil STAR version 2.7.11b et les commandes** :

STAR --genomeDir index_genomes/index_gcf/T_septentrionalis \
--sjdbGTFfile genomes/gcf_genomes/T_septentrionalis/ncbi_dataset/data/GCF_001594115.1/genomic.gff \
--readFilesIn raw_reads/T_septentrionalis/SRR3270634_1.fastq raw_reads/T_septentrionalis/SRR3270634_2.fastq \
--runThreadN 4 \
--outFileNamePrefix mapping/map_gcf/T_septentrionalis/SRR3270634_gcf_

STAR --genomeDir index_genomes/index_gca/T_septentrionalis \
--sjdbGTFfile genomes/gca_genomes/T_septentrionalis/ncbi_dataset/data/GCA_001594115.1/genomic.gff \
--readFilesIn raw_reads/T_septentrionalis/SRR3270634_1.fastq raw_reads/T_septentrionalis/SRR3270634_2.fastq \
--runThreadN 4 \
--outFileNamePrefix mapping/map_gca/T_septentrionalis/SRR3270634_gca_

**9/10**

**Génération du rapport de qualité du mapping des reads SRR3270634 sur le génome de référence gcf et gca de T.septentrionalis avec l'outil multiqc version  1.25.1**:

multiqc /data/projet1/projet_tutore/mapping/map_gcf/T_septentrionalis -o /data/projet1/projet_tutore/mapping_quality_reports/map_qual_gcf/T_septentrionalis

multiqc /data/projet1/projet_tutore/mapping/map_gca/T_septentrionalis -o /data/projet1/projet_tutore/mapping_quality_reports/map_qual_gca/T_septentrionalis


**10/10**

**Analyse de la qualité du mapping des reads SRR3270634 sur le génome gcf de T.septentrionalis**

- 94,2 % des lectures se sont alignés donc la grande majorité des lectures se sont correctement alignées.
- 92,6 % des lectures s'alignent à un endroit unique sur le génome, donc la majorité des lectures ont une correspondance claire et non ambigüe avec une région sur le génome de référence.
La longueur moyenne des lectures mappée est de 178.5 bp, ce qui est correct pour des lectures paired end de 90 bp

**Assemblage des reads à l'aide de l'annotation gcf avec l'outil stringtie version 2.2.3**:

en premier lieu, on a transformer le ficher d'alignement sam généré par star en fichier bam et on a trié ce fichier bam avec l'outil samtools version 1.21

samtools view -S -b SRR3270634_gcf_Aligned.out.sam > SRR3270634_gcf_Aligned.out.bam

samtools sort SRR3270634_gcf_Aligned.out.bam -o SRR3270634_gcf_sorted.bam

On a transformé l'annotation de référence .gff en fichier .gtf avec l'outil gffread version 0.12.7
gffread genomic.gff -T -o genomic.gtf

stringtie mapping/map_gcf/T_septentrionalis/SRR3270634_gcf_sorted.bam -G genomes/gcf_genomes/T_septentrionalis/ncbi_dataset/data/GCF_001594115.1/genomic.gtf -o transcripts_assembly/gcf_assembly/T_septentrionalis/assembled_transcripts.gtf






