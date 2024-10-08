# projet_tutore
**04/10** 

Analyse de la qualité des reads forward et reverse de T.cornetzi et de T.septentrionalis avec l'outil Fastqc version 0.11.9 et application des commandes 

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
Mapping des reads SRR3270634_1.fastq et SRR3270634_2.fastq de T.septentrionalis sur les génomes de références gca et gcf de T.septentrionalis avec l'outil STAR version 2.7.11b et les commandes :

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




