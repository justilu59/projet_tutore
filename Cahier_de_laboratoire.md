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

**Génération de l'index des génomes gcf et gca de T.septentrionalis avec l'outil STAR version 2.7.11b et les commandes** :

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
La longueur moyenne des lectures mappée est de 178.5 bp, ce qui est correct pour des lectures paired end de 90 bp.

**Assemblage des transcrits de T.septentrionalis basé sur l'annotation gcf avec l'outil stringtie version 2.2.3**:

en premier lieu, on a transformé le ficher d'alignement sam généré par star en fichier bam et on a trié ce fichier bam avec l'outil samtools version 1.21

samtools view -S -b SRR3270634_gcf_Aligned.out.sam > SRR3270634_gcf_Aligned.out.bam

samtools sort SRR3270634_gcf_Aligned.out.bam -o SRR3270634_gcf_sorted.bam

On a transformé l'annotation de référence .gff en fichier .gtf avec l'outil gffread version 0.12.7
gffread genomic.gff -T -o genomic.gtf

stringtie mapping/map_gcf/T_septentrionalis/SRR3270634_gcf_sorted.bam -G genomes/gcf_genomes/T_septentrionalis/ncbi_dataset/data/GCF_001594115.1/genomic.gtf -o transcripts_assembly/gcf_assembly/T_septentrionalis/assembled_transcripts.gtf

**12/10**

**Evaluation de l'annotation de l'assemblage des transcrits de T.septentrionalis par rapport à annotation de référence gcf avec l'outil gffcompare version v0.12.6** 

gffcompare -r genomes/gcf_genomes/T_septentrionalis/ncbi_dataset/data/GCF_001594115.1/genomic.gtf -o annotation_analysis/annotation_gcf/T_septentrionalis/comparison_output transcripts_assembly/gcf_assembly/T_septentrionalis/assembled_transcripts.gtf

**Analyse du rapport généré par gffcompare concernant l'assemblage des transcrits de T.septentrionalis basé sur annotation gcf**

- Il y a 33 897 transcrits dans l'assemblage au total.
- 14 598 transcrits correspondent parfaitement à l'annotation de référence gcf.
- 8690 loci correspondent à ceux de l'annotation gcf.
- 7,7 % des exons annotés manquent dans l'assemblage (7205 exons manquants sur 93707)
- 9,3% des exons détectés dans l'assemblage n'étaient pas présent dans l'annotation de référence (9907 nouveaux exons sur 107041).
- 7,2 % des introns annotés sont manquants.
- 2,3 % des introns de l'assemblage sont nouveaux.
- 10,6 % des loci annotés sont absents de l'assemblage.
- 33,2 % des loci trouvés dans l'assemblage sont nouveaux, ce qui est assez élevé et pourrait indiquer la découverte de nouveaux loci non annotés.

**Evaluation de la complétude de l'assemblage des transcrits de T.septentrionalis basé sur annotation gcf avec l'outil BUSCO version 5.7.1**

au préalable on transforme l'assemblage des transcrits .gtf en .fasta

gffread assembled_transcripts.gtf -g reference_genome.fasta -w assembled_transcripts.fasta

busco -i transcripts_assembly/gcf_assembly/T_septentrionalis/assembled_transcripts.fasta -l insecta_odb10 -o annotation_analysis/annotation_gcf/T_septentrionalis/busco_output -m transcriptome -f

L'analyse révèle que 1355 gènes complets ont été retrouvés sur 1367.
- 656 ont été trouvés en une seule copie et 699 ont été trouvés dupliqués.
- 4 gènes sont fragmentés et 8 sont manquants.

**13/10**

**Analyse de la qualité du mapping des reads SRR3270634 sur le génome gca de T.septentrionalis**

- 94,2 % des lectures se sont alignés donc la grande majorité des lectures se sont correctement alignées.
- 92,5 % des lectures s'alignent à un endroit unique sur le génome, donc la majorité des lectures ont une correspondance claire et non ambigüe avec une région sur le génome de référence.
La longueur moyenne des lectures mappée est de 178.2 bp, ce qui est correct pour des lectures paired end de 90 bp.

Donc ces valeurs se rapprochent fortement de celles obtenus pour le mapping sur le génome gcf de T.septentrionalis.

**Assemblage des transcrits de T.septentrionalis basé sur l'annotation gca avec l'outil stringtie version 2.2.3**

Comme pour l'annotation gcf, on a transformé le ficher d'alignement sam généré par star en fichier bam et on a trié ce fichier bam avec l'outil samtools version 1.21

samtools view -S -b SRR3270634_gca_Aligned.out.sam > SRR3270634_gca_Aligned.out.bam

samtools sort SRR3270634_gca_Aligned.out.bam -o SRR3270634_gca_sorted.bam

On a transformé l'annotation de référence .gff en fichier .gtf avec l'outil gffread version 0.12.7
gffread genomic.gff -T -o genomic.gtf

stringtie mapping/map_gca/T_septentrionalis/SRR3270634_gca_sorted.bam -G genomes/gca_genomes/T_septentrionalis/ncbi_dataset/data/GCA_001594115.1/genomic.gtf -o transcripts_assembly/gcf_assembly/T_septentrionalis/assembled_transcripts.gtf

**Evaluation de l'annotation de l'assemblage des transcrits de T.septentrionalis par rapport à annotation de référence gcf avec l'outil gffcompare version v0.12.6** 

gffcompare -r genomes/gca_genomes/T_septentrionalis/ncbi_dataset/data/GCA_001594115.1/genomic.gtf -o annotation_analysis/annotation_gca/T_septentrionalis/comparison_output transcripts_assembly/gca_assembly/T_septentrionalis/assembled_transcripts.gtf

**14/10**

**Analyse du rapport généré par gffcompare concernant l'assemblage des transcrits de T.septentrionalis basé sur annotation gca**

- Il y a 33 833 transcrits dans l'assemblage au total.
- 4510 transcrits correspondent parfaitement à l'annotation de référence gca.
- 4510 loci correspondent à ceux de l'annotation gcf.
- 23,5 % des exons annotés manquent dans l'assemblage.
- 19,9 % des exons détectés dans l'assemblage n'étaient pas présent dans l'annotation de référence.
- 21,2 % des introns annotés sont manquants.
- 10,6 % des introns de l'assemblage sont nouveaux.
- 27,1 % des loci annotés sont absents de l'assemblage.
- 40,1 % des loci trouvés dans l'assemblage sont nouveaux, ce qui est assez élevé et pourrait indiquer la découverte de nouveaux loci non annotés

On constate globalement qu'un faible nombre de transcrits correspondent parfaitement à l'annotation de référence gca comparativement à l'annotaion gcf précedemment étudié.

**Evaluation de la complétude de l'assemblage des transcrits de T.septentrionalis basé sur annotation gca avec l'outil BUSCO version 5.7.1**

au préalable on transforme l'assemblage des transcrits .gtf en .fasta

gffread assembled_transcripts.gtf -g reference_genome.fasta -w assembled_transcripts.fasta

busco -i transcripts_assembly/gca_assembly/T_septentrionalis/assembled_transcripts.fasta -l insecta_odb10 -o annotation_analysis/annotation_gca/T_septentrionalis/busco_output -m transcriptome -f

L'analyse révèle que 1328 gènes complets ont été retrouvés sur 1367.
- 657 ont été trouvés en une seule copie et 671 ont été trouvés dupliqués.
- 17 gènes sont fragmentés et 22 sont manquants.

Donc globalement, l'annotation gca semble moins bonne que l'annotation gcf.

**20/10/2024**

**Analyse de qualité des reads SRR3270378_1 et SRR3270378_2 de T.cornetzi**
- Longueur des reads: 90 pb  
- 44% GC
- per base sequence content : La distribution des 15 premiers nucléotides est non uniforme, ce qui est attendu en RNA-seq.
- sequence duplication level :La courbe rouge montre que seulement 30,35 % des séquences restent uniques après suppression des duplicats, ce qui suggère qu'environ 70 % sont des copies. Un taux de duplication élevé peut indiquer un biais de séquençage, tel qu'une amplification excessive (PCR), ou la présence de régions répétées dans le génome. La courbe bleue montre qu'environ 10 % des séquences apparaissent une ou deux fois, mais des pics de duplication se manifestent à des niveaux plus élevés, notamment autour de 9 et 500, suggérant des séquences sur-représentées. Ces resultats sont attendus avoir des reads dupliqués pour les transcrits de forte abondance
- overrepresented sequence : Le graphique représente le contenu en adapteurs dans les reads, en fonction de leur position le long des séquences. Aucun contenu adaptateur est détecté dans les reads, ce qui signifie qu'il n'y a pas de contamination significative par des séquences d'adapteurs. C'est bien.




