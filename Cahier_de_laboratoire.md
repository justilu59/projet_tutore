# Projet_tutore

Dans le cadre de notre projet tutoré, nous étudions les génomes de référence de trois espèces de fourmis : T. septentrionalis, T. cornetzi et T. zeteki. Justine se consacre à l'analyse de T. septentrionalis, Mina à celle de T. cornetzi, et Dilara à celle de T. zeteki.

**03/10/2024** Justine

**Importation des données des génomes de référence des 3 espèces de fourmis T.septentrionalis, T.cornetzi et T.zeteki avec l'outil ncbi-datasets-cli version 16.31.0**:

datasets download genome accession GCF_001594115.1 --include gff3,rna,cds,protein,genome,seq-report

datasets download genome accession GCF_001594075.2 --include gff3,rna,cds,protein,genome,seq-report

datasets download genome accession GCF_001594055.1 --include gff3,rna,cds,protein,genome,seq-report

Les mêmes commandes sont exécutées pour l'annotation gca.

**Importation des données de RNA-seq avec l'outil sra-tools version 3.1.1**:

fastq-dump --split-files --gzip SRR3270634

fastq-dump --split-files --gzip SRR3270378

fastq-dump --split-files --gzip SRR3270377

**04/10/2024** Justine

**Génération du rapport de qualité des reads forward et reverse de T.cornetzi et de T.septentrionalis avec l'outil Fastqc version 0.11.9 et application des commandes**:

fastqc -o quality_reports/T_cornetzi raw_reads/T_cornetzi/SRR3270378_1.fastq.gz raw_reads/T_cornetzi/SRR3270378_2.fastq.gz 

fastqc -o quality_reports/T_septentrionalis raw_reads/T_septentrionalis/SRR3270634_1.fastq.gz raw_reads/T_septentrionalis/SRR3270634_2.fastq.gz

**06/10/2024** Justine

**Analyse de qualité des reads SRR3270634_1 et SRR3270634_2 de T.septentrionalis** : 
- reads de longueur 90 pb 
- 42% GC
- per base sequence content : on oberve une distribution non uniforme pour les 10-15 nucléotides, ce qui est normal en RNA-seq
- sequence duplication level : on a un certain nombre de reads qui sont présents plusieurs fois, il est attendu d'avoir des reads dupliqués pour les transcrits de forte abondance
- overrepresented sequence : il y a présence de séquence qui correspond à un adaptateur Truseq dans SRR3270634_1

**Elimination de la séquence correspondant à l'adaptateur avec l'outil cutadapt version 4.9 et la commande** :

cutadapt -a GATCGGAAGAGCACACGTCTGAACTCCAGTCACTTAACCGGATCTCGTAT -o SRR3270634_1_trimmed.fastq.gz -z raw_reads/T_septentrionalis/SRR3270634_1.fastq.gz

**Génération de l'index des génomes gcf et gca de T.septentrionalis avec l'outil STAR version 2.7.11b et les commandes** :

STAR --runMode genomeGenerate --genomeDir index_genomes/index_gcf/T_septentrionalis --genomeFastaFiles genomes/gcf_genomes/T_septentrionalis/ncbi_dataset/data/GCF_001594115.1/GCF_001594115.1_Tsep1.0_genomic.fna --runThreadN 4 --genomeSAindexNbases 13

STAR --runMode genomeGenerate --genomeDir index_genomes/index_gca/T_septentrionalis --genomeFastaFiles genomes/gca_genomes/T_septentrionalis/ncbi_dataset/data/GCA_001594115.1/GCA_001594115.1_Tsep1.0_genomic.fna --runThreadN 4 --genomeSAindexNbases 13


**8/10/2024** Justine

Le trimming a induit des incohérences dans la longueur des séquences et qualité associées à SRR3270634_trimmed_1 donc utilisation des reads non trimmés pour le mapping.

**Mapping des reads SRR3270634_1.fastq et SRR3270634_2.fastq de T.septentrionalis sur les génomes de références gca et gcf de T.septentrionalis avec l'outil STAR version 2.7.11b et les commandes** :

STAR --genomeDir index_genomes/index_gcf/T_septentrionalis \
--sjdbGTFfile genomes/gcf_genomes/T_septentrionalis/ncbi_dataset/data/GCF_001594115.1/genomic.gff \
--readFilesIn raw_reads/T_septentrionalis/SRR3270634_1.fastq raw_reads/T_septentrionalis/SRR3270634_2.fastq \
--runThreadN 4 \
--outFileNamePrefix mapping/map_gcf/T_septentrionalis/SRR3270634_gcf_

STAR --genomeDir index_genomes/index_gca/T_septentrionalis \
--sjdbGTFfile genomes/gca_genomes/T_septentrionalis/ncbi_dataset/data/GCA_001594115.1/genomic.gff \
--readFilesIn raw_reads/T_septentrionalis/SRR3270634_1.fastq.gz raw_reads/T_septentrionalis/SRR3270634_2.fastq.gz \
--runThreadN 4 \
--outFileNamePrefix mapping/map_gca/T_septentrionalis/SRR3270634_gca_ \
--readFilesCommand zcat

**9/10/2024** Justine

**Génération du rapport de qualité du mapping des reads SRR3270634 sur le génome de référence gcf et gca de T.septentrionalis avec l'outil multiqc version  1.25.1**:

multiqc /data/projet1/projet_tutore/mapping/map_gcf/T_septentrionalis -o /data/projet1/projet_tutore/mapping_quality_reports/map_qual_gcf/T_septentrionalis

multiqc /data/projet1/projet_tutore/mapping/map_gca/T_septentrionalis -o /data/projet1/projet_tutore/mapping_quality_reports/map_qual_gca/T_septentrionalis


**10/10/2024** Justine

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

**12/10/2024** Justine

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

gffread transcripts_assembly/gcf_assembly/T_septentrionalis/assembled_transcripts.gtf -g genomes/gcf_genomes/T_septentrionalis/ncbi_dataset/data/GCF_001594115.1/GCF_001594115.1_Tsep1.0_genomic.fna -w transcripts_assembly/gcf_assembly/T_septentrionalis/assembled_transcripts.fasta

busco -i transcripts_assembly/gcf_assembly/T_septentrionalis/assembled_transcripts.fasta -l insecta_odb10 -o annotation_analysis/annotation_gcf/T_septentrionalis/busco_output -m transcriptome -f

L'analyse révèle que 1355 gènes complets ont été retrouvés sur 1367.
- 656 ont été trouvés en une seule copie et 699 ont été trouvés dupliqués.
- 4 gènes sont fragmentés et 8 sont manquants.

**13/10/2024** Justine

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

**14/10/2024** Justine

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

**20/10/2024** Dilara, Mina

**Génération du rapport de qualité des reads forward et reverse de T.zeteki avec l'outil Fastqc version 0.11.9 :**

fastqc -o quality_reports/T_zeteki raw_reads/T_zeteki/SRR3270377_1.fastq.gz raw_reads/T_zeteki/SRR3270377_2.fastq.gz



**Analyse de qualité des reads SRR3270378_1 et SRR3270378_2 de T.cornetzi avec FastQC v.0.11.9 pour verifier la qualité des séquences avant le mapping**

Longueur des reads : 90 pb avec un contenu GC de 44 %.

Duplication des séquences : 30,35 % des séquences étaient uniques après la suppression des duplicats, ce qui est conforme aux attentes pour des transcrits de forte abondance.

Séquences surreprésentées : Aucune contamination par des séquences d'adaptateurs n’a été détectée. C'est bien.

**21/10/2024** Mina

**Génération de l'index du génomes gcf de T.cornetzi avec l'outil STAR version 2.7.11b pour permettre le mapping des reads** :

STAR --runMode genomeGenerate --genomeDir index_genomes/index_gcf/T_cornetzi --genomeFastaFiles genomes/gcf_genomes/T_cornetzi/ncbi_dataset/data/GCF_001594075.2/GCF_001594075.2_Tcor1.1_genomic.fna --runThreadN 4 --genomeSAindexNbases 13

**Mapping des reads SRR3270378_1 et SRR3270378_2 de T.cornetzi sur le génome de référence gcf vec l'outil STAR version 2.7.11b pour aligner les reads aux sequences de ref et permettre l'assemblage des transcrits** :

STAR --genomeDir index_genomes/index_gcf/T_cornetzi --sjdbGTFfile genomes/gcf_genomes/T_cornetzi/ncbi_dataset/data/GCF_001594075.2/genomic.gff --readFilesIn raw_reads/T_cornetzi/SRR3270378_1.fastq.gz raw_reads/T_cornetzi/SRR3270378_2.fastq.gz --runThreadN 4 --outFileNamePrefix mapping/map_gcf/T_cornetzi/SRR3270378_gcf_ --readFilesCommand zcat

**Resultats et évaluation du mapping des transcrits:**

Transcrits assemblés (Query) : 35,626 transcrits dans 20,731 loci.
Transcrits de référence (Reference) : 22,823 transcrits dans 13,690 loci.
En moyenne, il y a 1.7 transcrits par locus dans l'assemblage.


Niveau	                   Sensibilité           	Précision
Base                         	87.5 %	              67.5 %
Exon                         	79.3 %              	73.5 %
Intron	                       83.6 %	              89.2 %
Transcript	                   57.7 %              	36.9 %
Locus	                        63.3 %              	41.3 %

Analyse des Exons et Introns: 
Exons manqués : 11,199 sur 98,458 (11.4 %).
Nouveaux exons : 11,842 sur 108,502 (10.9 %).
Introns manqués : 9,215 sur 82,509 (11.2 %).
Nouveaux introns : 1,680 sur 77,351 (2.2 %).
Loci manqués : 2,186 sur 13,690 (16.0 %).
Nouveaux loci : 8,001 sur 20,731 (38.6 %).

Ces résultats montrent que l’assemblage offre une couverture incomplète de certains éléments de la référence (exons, introns, et loci). Il révèle aussi des nouveautés au niveau des exons et des loci, ce qui pourrait suggérer la présence de nouveaux gènes, isoformes, ou régulations d'épissage non encore documentés.

**27/10/2024** Justine

**Développement d'un script report_annotation.py pour l'analyse du fichier summary de GFFcompare**

Ce script extrait des informations spécifiques telles que les loci manquants, les exons manquants, les transcrits matchés, et les erreurs de bornes, et génère un rapport permettant d'estimer les gènes non supportés (approximation basée sur les loci manquants), les exons manquants, les transcrits manquants, et les erreurs de bornes.

Le script utilise le module re pour la recherche de motifs dans le texte et argparse pour la gestion des arguments en ligne de commande.

Plusieurs fonctions ont été définies :
- **extract_data** qui parcourt le fichier summary de GFFCompare pour extraire les informations clés en utilisant des expressions régulières.
- **generate_report** qui utilise les données extraites pour calculer les pourcentages de gènes non supportés, d'exons manquants, d'erreurs de bornes et de transcrits manquants.
- **print_report** qui affiche les résultats en format clair et compréhensible.

L'exécution du script se fait par la commande python script.py /chemin/comparison_output.stats

 **29/10/2024** Dilara

**Analyse de qualité des reads de T. Zeteki, SRR3270377_1 et SRR3270377_2 avant le mapping :**

Longueur des reads : 90 pb
GC Content : 42 %
Contenu par position de séquence : Distribution non uniforme observée sur les 15 premiers nucléotides, ce qui est attendu en RNA-seq
Niveau de duplication des séquences : Un certain nombre de reads sont présents en plusieurs copies. La duplication de reads est attendue pour les transcrits de forte abondance
Séquences surreprésentées : Présence d'une séquence d'adaptateur TruSeq dans SRR3270377_1


**Génération de l'index des génomes gcf et gca de T. zeteki avec l'outil STAR version 2.7.11b pour le mapping :**

STAR --runMode genomeGenerate --genomeDir index_genomes/index_gcf/T_zeteki --genomeFastaFiles genomes/gcf_genomes/T_zeteki/ncbi_dataset/data/GCF_001594055.1/GCF_001594055.1_Tzet1.0_genomic.fna --runThreadN 4 --genomeSAindexNbases 13

STAR --runMode genomeGenerate --genomeDir index_genomes/index_gca/T_zeteki --genomeFastaFiles genomes/gca_genomes/T_zeteki/ncbi_dataset/data/GCA_001594055.1/GCA_001594055.1_Tzet1.0_genomic.fna --runThreadN 4 --genomeSAindexNbases 13


 
**Pour le génome de T. cornetzi** Mina

**Génération du rapport de qualité du mapping des reads SRR3270634 sur le génome de référence gcf et gca de T.cornetzi avec l'outil multiqc version 1.25.1:**

multiqc /data/projet1/projet_tutore/mapping/map_gcf/T_cornetzi -o /data/projet1/projet_tutore/mapping_quality_reports/map_qual_gcf/T_cornetzi

**1. Assemblage des transcrits sur l'annotation gcf avec l'outil stringtie version 2.2.3**

On utilise l'Outil StringTie pour assembler les transcrits de T. cornetzi en utilisant les fichiers BAM produits lors du mapping avec STAR.

*Conversion des fichiers SAM en BAM, tri et assemblage avec outil samtools version 1.21 *

samtools view -S -b mapping/map_gcf/T_cornetzi/SRR3270378_gcf_Aligned.out.sam > SRR3270378_gcf_Aligned.out.bam

samtools sort SRR3270378_gcf_Aligned.out.bam -o SRR3270378_gcf_sorted.bam

On transforme l'annotation de référence .gff en fichier .gtf avec l'outil gffread version 0.12.7 gffread genomic.gff -T -o genomic.gtf

stringtie mapping/map_gcf/T_cornetzi/SRR3270378_gcf_sorted.bam -G genomes/gcf_genomes/T_cornetzi/ncbi_dataset/data/GCF_001594075.2/genomic.gtf -o transcripts_assembly/gcf_assembly/T_cornetzi/assembled_transcripts.gtf

 
**Évaluation de l'annotation des transcrits**
On Utilise GFFcompare pour évaluer l'assemblage obtenu par rapport à l'annotation de référence. Cette étape permet de valider la qualité de l’assemblage en comparant les transcrits assemblés aux transcrits annotés avec l'outil gffcompare version v0.12.6.

   gffcompare -r genomes/gcf_genomes/T_cornetzi/ncbi_dataset/data/GCF_001594075.2/genomic.gtf -o annotation_analysis/annotation_gcf/T_cornetzi/comparison_output transcripts_assembly/gcf_assembly/T_cornetzi/assembled_transcripts.gtf
 
**Analyse de la complétude de l'assemblage des transcrits**
 On utilise BUSCO pour évaluer la complétude de l'assemblage en comparant les transcrits assemblés avec un jeu de gènes universel.

   - Convertir le fichier d’assemblage `.gtf` en format `.fasta` :

     gffread transcripts_assembly/gcf_assembly/T_cornetzi/assembled_transcripts.gtf -g reference_genome.fasta -w assembled_transcripts.fasta

*Ayant des problemes avec BUSCO je passe cette étape* 

 **Validation et analyse du rapport d'annotation**
 
Utilisation du script `report_annotation.py` pour analyser le fichier `.stats` généré par GFFcompare. Cette étape nous permet d’identifier les loci, exons et transcrits manquants, ainsi que les erreurs de bornes pour affiner l'annotation.

python report_annotation.py annotation_analysis/annotation_gcf/T_cornetzi/comparison_output.stats
cat comparison_output.stats


**30/10/2024** Dilara

contrôle qualité du mapping, puis analyse et annotation de GCF

**Mapping des reads SRR3270377_1.fastq et SRR3270377_2.fastq de T.zeteki sur les génomes de références gca et gcf de T.zeteki avec l'outil STAR version 2.7.11b :**

STAR --genomeDir index_genomes/index_gcf/T_zeteki --sjdbGTFfile genomes/gcf_genomes/T_zeteki/ncbi_dataset/data/GCF_001594055.1/genomic.gff --readFilesIn raw_reads/T_zeteki/SRR3270377_1.fastq.gz raw_reads/T_zeteki/SRR3270377_2.fastq.gz --runThreadN 4 --outFileNamePrefix mapping/map_gcf/T_zeteki/SRR3270377_gcf_ --readFilesCommand zcat

STAR --genomeDir index_genomes/index_gca/T_zeteki --sjdbGTFfile genomes/gca_genomes/T_zeteki/ncbi_dataset/data/GCA_001594055.1/genomic.gff --readFilesIn raw_reads/T_zeteki/SRR3270377_1.fastq.gz raw_reads/T_zeteki/SRR3270377_2.fastq.gz --runThreadN 4 --outFileNamePrefix mapping/map_gca/T_zeteki/SRR3270377_gca_ --readFilesCommand zcat


**01/11/2024** Mina

**Mapping des reads de T.cornetzi sur les génomes de références gca.**

On suit les memes etapes vu pour GCF mais avec les noms de fichier GCA : 

Génération de l'index du génomes gca de T.cornetzi avec l'outil STAR version 2.7.11b pour permettre le mapping des reads :


STAR --runMode genomeGenerate --genomeDir index_genomes/index_gca/T_cornetzi --genomeFastaFiles genomes/gca_genomes/T_cornetzi/ncbi_dataset/data/GCA_001594075.2/GCA_001594075.1_Tcor1.1_genomic.fna --runThreadN 4 --genomeSAindexNbases 13

STAR --runMode genomeGenerate --genomeDir index_genomes/index_gca/T_cornetzi --genomeFastaFiles genomes/gca_genomes/T_cornetzi/ncbi_dataset/data/GCA_001594075.2/GCA_001594075.2_Tcor1.1_genomic.fna --runThreadN 4 --genomeSAindexNbases 13

Mapping des reads SRR3270378_1 et SRR3270378_2 de T.cornetzi sur le génome de référence gca vec l'outil STAR version 2.7.11b pour aligner les reads aux sequences de ref et permettre l'assemblage des transcrits :

STAR --genomeDir index_genomes/index_gcf/T_cornetzi --sjdbGTFfile genomes/gca_genomes/T_cornetzi/ncbi_dataset/data/GCA_001594075.2/genomic.gff --readFilesIn raw_reads/T_cornetzi/SRR3270378_1.fastq.gz raw_reads/T_cornetzi/SRR3270378_2.fastq.gz --runThreadN 4 --outFileNamePrefix mapping/map_gcf/T_cornetzi/SRR3270378_gca_ --readFilesCommand zcat

Génération du rapport de qualité du mapping des reads SRR3270378 sur le génome de référence gca de T.cornetzi avec l'outil multiqc version 1.25.1:

multiqc /data/projet1/projet_tutore/mapping/map_gca/T_cornetzi -o /data/projet1/projet_tutore/mapping_quality_reports/map_qual_gca/T_cornetzi

Comme pour l'annotation gcf, on transforme le ficher d'alignement sam généré par star en fichier bam et on a trié ce fichier bam avec l'outil samtools version 1.21

samtools view -S -b SRR3270634_gca_Aligned.out.sam > SRR3270378_gca_Aligned.out.bam


samtools sort SRR3270378_gca_Aligned.out.bam -o SRR3270378_gca_sorted.bam


On a transformé l'annotation de référence .gff en fichier .gtf avec l'outil gffread version 0.12.7 gffread genomic.gff -T -o genomic.gtf


stringtie mapping/map_gca/T_cornetzi/SRR3270378_gca_sorted.bam -G genomes/gca_genomes/T_cornetzi/ncbi_dataset/data/GCA_001594075.1/genomic.gtf -o transcripts_assembly/gca_assembly/T_cornetzi/assembled_transcripts.gtf


gffcompare -r genomes/gca_genomes/T_cornetzi/ncbi_dataset/data/GCA_001594075.1/genomic.gtf -o annotation_analysis/annotation_gca/T_cornetzi/comparison_output transcripts_assembly/gca_assembly/T_cornetzi/assembled_transcripts.gtf


python report_annotation.py annotation_analysis/annotation_gca/T_cornetzi/comparison_output.stats cat comparison_output.stats


Dilara
**Génération du rapport de qualité du mapping des reads SRR3270377 sur le génome de référence gcf et gca de T.zeteki avec l'outil multiqc version 1.25.1:** 

multiqc /data/projet1/projet_tutore/mapping/map_gcf/T_zeteki -o /data/projet1/projet_tutore/mapping_quality_reports/map_qual_gcf/T_zeteki

multiqc /data/projet1/projet_tutore/mapping/map_gca/T_zeteki -o /data/projet1/projet_tutore/mapping_quality_reports/map_qual_gca/T_zeteki

**Analyse de la qualité du mapping des reads SRR3270377 sur le génome gcf de T.zeteki :**

Le mapping des lectures SRR3270377 sur le génome de T. zeteki montre une bonne qualité. 
Environ 88,8 % des lectures se sont alignées, dont 87,35 % de manière unique, suggérant un alignement précis. 
La longueur moyenne des lectures alignées (178,17 nucléotides) est très proche de la longueur moyenne initiale, montrant peu de perte de données. La plupart des jonctions suivent le motif canonique GT/AG, avec des taux d’erreurs, de délétions et d'insertions très faibles (tous inférieurs à 0,4 %), ce qui atteste de la fidélité du mapping.

**05/11/2024** Dilara

**Assemblage des transcrits de T.zeteki basé sur l'annotation gcf avec l'outil stringtie version 2.2.3:**

On va d'abord transformé le ficher d'alignement sam généré par star en fichier bam : 


samtools view -S -b SRR3270377_gcf_Aligned.out.sam > SRR3270377_gcf_Aligned.out.bam

et on va trié ce fichier bam avec l'outil samtools version 1.21 : 

samtools sort SRR3270377_gcf_Aligned.out.bam -o SRR3270377_gcf_sorted.bam


**On a ensuite transformé l'annotation de référence .gff en fichier .gtf avec l'outil gffread version 0.12.7 :** 

gffread genomic.gff -T -o genomic.gtf

stringtie mapping/map_gcf/T_zeteki/SRR3270377_gcf_sorted.bam -G genomes/gcf_genomes/T_zeteki/ncbi_dataset/data/GCF_001594055.1/genomic.gtf -o transcripts_assembly/gcf_assembly/T_zeteki/assembled_transcripts.gtf

**Evaluation de l'annotation de l'assemblage des transcrits de T.zeteki par rapport à l'annotation de référence gcf avec l'outil gffcompare version v0.12.6 :**

gffcompare -r genomes/gcf_genomes/T_zeteki/ncbi_dataset/data/GCF_001594055.1/genomic.gtf -o annotation_analysis/annotation_gcf/T_zeteki/comparison_output transcripts_assembly/gcf_assembly/T_zeteki/assembled_transcripts.gtf

**Analyse du rapport généré par gffcompare concernant l'assemblage des transcrits de T.zeteki basé sur l'annotation gcf** : 

Le rapport de gffcompare pour l'assemblage des transcrits de T. zeteki montre que cet assemblage contient 30 066 transcrits répartis sur 16 697 loci, alors que l'annotation de référence GCF en inclut 19 870 transcrits et 11 927 loci. 

Parmi les transcrits de l'assemblage, 12 119 correspondent exactement aux transcrits de la référence, et 7 906 loci correspondent parfaitement à ceux annotés dans GCF.

On observe également une proportion significative de nouveaux éléments dans l'assemblage : 32,3 % des loci et 8,9 % des exons sont nouveaux, ce qui pourrait indiquer des transcrits ou loci propres à T. zeteki. Par ailleurs, 11,2 % des exons et 13,4 % des loci annotés dans GCF sont absents dans cet assemblage.
Les scores de sensibilité et de précision varient selon les niveaux d’analyse. 

Par exemple, la sensibilité et précision sont relativement élevées au niveau des exons (80,4 % et 76,3 % respectivement), mais elles diminuent pour les chaînes d'introns (sensibilité de 63,4 % et précision de 50,6 %) et les transcrits (sensibilité de 61 % et précision de 40,3 %). 

Ces différences pourraient indiquer des variantes d’épissage ou des erreurs d'assemblage.

**Amélioration du code report_annotation.py pour la prise en compte des gènes non supportés** :

Modification du script report_annotation.py pour intégrer l'analyse des gènes non supportés (non alignés) en extrayant ces informations du fichier .tracking. 

En ajoutant une fonction de comptage des gènes non supportés, basée sur les transcrits de type 'u' dans le fichier .tracking, le rapport final génère désormais également un comptage précis des gènes non supportés.

Ajout d'une fonction count_unsupported_genes pour compter et extraire les gènes non supportés du fichier .tracking.

**Génération d'un fichier de rapport .txt contenant un résumé complet des gènes et transcrits analysés, y compris les gènes non supportés pour T_septentrionalis** :

python report_annotation.py annotation_gcf/T_septentrionalis/comparison_output.stats annotation_gcf/T_septentrionalis/comparison_output.tracking annotation_gcf/T_septentrionalis/report_gcf_T_septentrionalis.txt

python report_annotation.py annotation_gca/T_septentrionalis/comparison_output.stats annotation_gca/T_septentrionalis/comparison_output.tracking annotation_gca/T_septentrionalis/report_gca_T_septentrionalis.txt

**Pour l'annotation gcf de T.septentrionalis, les résultats obtenus sont** :

Gènes non-supportés (approximés sur les loci) : 1262 sur 11929 (10.58%)

Nombre total de gènes non supportés (fichier .tracking) : 2832

Exons manquants : 7205 sur 93707 (7.69%)

Erreurs de bornes : 30.70%

Transcrits manquants : 7202 sur 21800 (33.04%)

**Pour l'annotation gca de T.septentrionalis, les résultats obtenus sont** :

Gènes non-supportés (approximés sur les loci) : 4127 sur 15221 (27.11%)

Nombre total de gènes non supportés (fichier .tracking) : 4583

Exons manquants : 20277 sur 86362 (23.48%)

Erreurs de bornes : 66.00%

Transcrits manquants : 10711 sur 15221 (70.37%)

En conclusion,l'annotation gcf semble offrir être plus robuste, avec moins de gènes et d’exons manquants, une meilleure précision des bornes introniques, et une meilleure correspondance des transcrits avec les données d’expression.

Il pourrait être intéressant d’explorer davantage les transcrits non appariés notamment en intégrant de nouvelles informations issues du fichier .tmap généré par StringTie. 

Le fichier .tmap contient des codes de correspondance détaillés (u pour les transcrits non appariés, p pour les correspondances partielles) qui peuvent compléter l’analyse.

On pourrait adapter le script report_annotation.py pour extraire et inclure les informations de transcrits non appariés (u) et partiellement appariés (p) du fichier comparison_output.assembled_transcripts.gtf.tmap. 

En parallèle, on pourrait pousser l'analyse des transcrits non appariés en utilisant un alignement secondaire, par exemple avec Exonerate ou BLAST, pour tenter de caractériser leur origine ou leur fonction potentielle.

Mina
**Interprétation des Résultats de transcrit pour GCA T_cornetzi**

cat comparison_output.stats

Query mRNAs : 36,862 transcrits dans 24,121 loci.
Reference mRNAs : 18,729 transcrits dans 18,729 loci.
Il y a beaucoup plus de transcrits assemblés que de transcrits de référence, mais c'est normal dans les études d'annotation de novo où l'on cherche à capturer la diversité transcriptomique.

*Loci et Transcrits :*

Multi-transcript loci : 6,145, ce qui signifie qu’il y a des loci avec plusieurs transcrits, montrant une complexité d'expression.
Environ 1.5 transcrits par locus en moyenne, ce qui est un indicateur de la diversité des isoformes.

*Sensibilité et Précision :*

Base level : Sensibilité de 73.6 % et précision de 47.2 %. Cela signifie que la majorité des bases sont identifiées correctement par rapport à la référence, mais la précision est inférieure, indiquant que de nombreux transcrits identifiés ne sont pas des correspondances exactes.
Les niveaux d'exon, d'intron, de transcrit et de locus montrent tous des performances similaires, avec des sensibilités plus élevées pour les introns et des précisions plus faibles pour les transcrits.

*Exons et Introns :*

Missed exons : 25,981, ce qui représente 28.2 % des exons manquants par rapport à la référence.
Novel exons : 21,173, ce qui signifie qu’il y a beaucoup d’exons qui n’étaient pas présents dans l'annotation de référence.
Cela montre que l'assemblage a identifié de nombreux nouveaux éléments.

*Loci Manqués et Nouveaux :*

Missed loci : 6,442 (34.4 %), ce qui montre que beaucoup de loci présents dans la référence ne sont pas retrouvés dans l'assemblage.
Novel loci : 10,504, montrant encore une fois une richesse d'annotations qui ne figurent pas dans le génome de référence.

**Rapport d'alignement des transcrits pour T_cornetzi**

python report_annotation.py annotation_gca/T_cornetzi/comparison_output.stats annotation_gca/T_cornetzi/comparison_output.tracking annotation_gca/T_cornetzi/report_gca_T_cornetzi.txt

Gènes non-supportés (approximés sur les loci) : 6442 sur 18729 (34.40%)

Nombre total de gènes non supportés (selon le fichier .tracking) : 6816

Exons manquants : 25981 sur 92170 (28.19%)

Erreurs de bornes : 71.30%

Transcrits manquants : 14350 sur 18729 (76.62%)


**19/11/2024** Dilara

**Assemblage des transcrits de T.zeteki basé sur l'annotation gca avec l'outil stringtie version 2.2.3**

On va reprendre les mêmes étapes que pour GCF, mais avec les fichier GCA : 

Convertir fichier SAM en BAM : 

samtools view -S -b SRR3270377_gca_Aligned.out.sam > SRR3270377_gca_Aligned.out.bam 

Trié fichier BAM avec Samtools version 1.21 : 

samtools sort SRR3270377_gca_Aligned.out.bam -o SRR3270377_gca_sorted.bam

On transforme l'annotation de référence .gff en fichier .gtf avec gffread version 0.12.7 : 
gffread genomic.gff -T -o genomic.gtf

Et enfin, assemblage des transcrits basé sur l'annotation gca avec stringtie version 2.2.3: 

stringtie mapping/map_gca/T_zeteki/SRR3270377_gca_sorted.bam -G genomes/gca_genomes/T_zeteki/ncbi_dataset/data/GCA_001594055.1/genomic.gtf -o transcripts_assembly/gca_assembly/T_zeteki/assembled_transcripts.gtf

**Evaluation de l'annotation de l'assemblage des transcrits de T.zeteki par rapport à annotation de référence gcf avec l'outil gffcompare version v0.12.6**

gffcompare -r genomes/gca_genomes/T_zeteki/ncbi_dataset/data/GCA_001594055.1/genomic.gtf -o annotation_analysis/annotation_gca/T_zeteki/comparison_output transcripts_assembly/gca_assembly/T_zeteki/assembled_transcripts.gtf

**Analyse du rapport généré par gffcompare sur l'assemblage des transcrits de T_zeteki basé sur l'annotation gca** : 

Le rapport de gffcompare pour l'assemblage des transcrits de T. zeteki montre que cet assemblage contient 31 222 transcrits répartis sur 19 877 loci, alors que l'annotation de référence GCA en inclut 14 662 transcrits et 14 662 loci. Parmi les transcrits de l'assemblage, 4 011 correspondent exactement aux transcrits de la référence, et 4 011 loci correspondent parfaitement à ceux annotés dans GCA.

On observe également une proportion significative de nouveaux éléments dans l'assemblage : 42,3 % des loci et 20,0 % des exons sont nouveaux, ce qui pourrait indiquer des transcrits ou loci propres à T. zeteki. Par ailleurs, 25,1 % des exons et 29,4 % des loci annotés dans GCA sont absents dans cet assemblage.

Les scores de sensibilité et de précision varient selon les niveaux d’analyse. Par exemple, la sensibilité et précision sont relativement élevées au niveau des introns (66,0 % et 71,9 % respectivement), mais elles diminuent pour les chaînes d'introns (sensibilité de 31,9 % et précision de 18,9 %) et les transcrits (sensibilité de 27,4 % et précision de 12,8 %). Ces différences pourraient indiquer des variantes d’épissage ou des erreurs d'assemblage.
En conclusion, le nombre de transcrits correspondant parfaitement à l'annotation de référence GCA est relativement faible, ce qui pourrait refléter une couverture partielle de l'assemblage ou des divergences potentielles entre les données assemblées et l'annotation de référence.


**20/11/2024** Dilara

**Génération d’un rapport .txt des gènes et transcrits analysés pour T. zeteki**

**Rapport pour T. zeteki (GCF)**

python report_annotation.py annotation_gcf/T_zeteki/comparison_output.stats annotation_gcf/T_zeteki/comparison_output.tracking annotation_gcf/T_zeteki/report_gcf_T_zeteki.txt

**Rapport d'alignement des transcrits pour l'annotation gcf de T.zeteki :**

- Gènes non-supportés (approximés sur les loci) : 1602 sur 11927 (13.43%)
- Nombre total de gènes non supportés (fichier .tracking) : 2633
- Exons manquants : 10133 sur 90807 (11.16%)
- Erreurs de bornes : 36.60%
- Transcrits manquants : 7751 sur 19870 (39.01%)

**Rapport pour T. zeteki (GCA)**

python report_annotation.py annotation_gca/T_zeteki/comparison_output.stats annotation_gca/T_zeteki/comparison_output.tracking annotation_gca/T_zeteki/report_gca_T_zeteki.txt

**Rapport d'alignement des transcrits pour l'annotation gca de T.zeteki :**

- Gènes non-supportés (approximés sur les loci) : 4312 sur 14662 (29.41%)
- Nombre total de gènes non supportés (fichier .tracking) : 5283
- Exons manquants : 20460 sur 81648 (25.06%)
- Erreurs de bornes : 68.10%
- Transcrits manquants : 10651 sur 14662 (72.64%)

En conclusion, l'annotation GCF apparaît plus fiable pour T_zeteki, présentant moins de gènes et d'exons absents, une délimitation des introns plus précise et une correspondance supérieure des transcrits avec les données d'expression.

**25/11/2024**

**Création du script analysis_tracking_file.py pour l'analyse plus approfondie de la correspondance des transcrits**

L'objectif du script analysis_tracking_file.py est d'analyser les fichiers .tracking générés par GFFCompare pour comprendre la répartition des correspondances des transcrits par catégories (=, u, p, et other). 

Le script permet :

- de calculer le nombre total de transcrits par type (= : alignement exact, u : non supporté, p : partiel, other : catégories supplémentaires comme j, k, etc.).

- de lister et compter les types spécifiques dans la catégorie other.

- de générer un fichier de sortie contenant un résumé des résultats.

- d'afficher les résultats dans le terminal pour une validation rapide.

Le script contient plusieurs fonctions :

- analyze_tracking_file : lit le fichier .tracking et compte le nombre de transcrits par catégorie (=, u, p, other) et retourne un dictionnaire contenant ces comptages ainsi que le nombre total de gènes uniques.

- analyze_other_genes : identifie les types spécifiques dans la catégorie other.

- count_other_types : compte le nombre d'occurrences pour chaque type dans other.

- write_results_to_file : sauvegarde les résultats dans un fichier .txt.

execution du script avec commande : python analysis_tracking_file.py annotation_gcf/T_septentrionalis/comparison_output.tracking annotation_gcf/T_septentrionalis/results_output.txt

**Analyse des différentes correspondances obtenues pour les transcrits pour l'annotation GCA et GCF**

GCF montre généralement une proportion plus élevée de transcrits parfaitement alignés (=) par rapport à GCA. Cela reflète une annotation potentiellement plus stricte ou mieux résolue.

GCA présente davantage de transcrits dans les catégories u (non supportés) et other (ambiguïtés), suggérant une annotation moins spécifique ou une inclusion de transcrits potentiellement erronés.

La catégorie j (Exact match of intron chain) est la plus fréquente dans other pour toutes les espèces et annotations.

Cependant :
        - T. septentrionalis et T. zeteki montrent une proportion plus élevée de j dans GCF par rapport à GCA.
        - T. cornetzi, en revanche, présente une proportion relativement plus faible de j dans GCF (8760 sur 15319) par rapport à GCA (12200 sur 23345), ce qui reflète une complexité ou une variabilité intronique plus importante dans cette espèce.

Une proportion élevée de j dans GCF peut indiquer une annotation intronique mieux définie et plus précise.

GCA, en incluant davantage d'annotations ambiguës (k, n, o), pourrait ne pas capturer autant de correspondances introniques exactes.

Les catégories k (loci multiples) et n (régions intergéniques) sont significativement plus élevées dans GCA pour toutes les espèces :

  - T. septentrionalis :

   k : 3367 (GCA) vs 1142 (GCF).

   n : 1850 (GCA) vs 699 (GCF).

  - T. zeteki :

   k : 2779 (GCA) vs 945 (GCF).

   n : 1977 (GCA) vs 858 (GCF).

  - T. cornetzi :

   k : 3773 (GCA) vs 1149 (GCF).

   n : 1998 (GCA) vs 917 (GCF).

GCA inclut probablement davantage de transcrits ambiguës, soit en raison d'annotations répétées non résolues (k), soit par l'inclusion de transcrits dans des régions intergéniques (n).

Ces ambiguïtés sont moins présentes dans GCF, ce qui suggère une annotation plus ciblée et stricte.

Les annotations mitochondriales (m) sont globalement similaires entre GCA et GCF :

   - T. septentrionalis : 921 (GCA) vs 901 (GCF).

   - T. zeteki : 970 (GCA) vs 943 (GCF).

   - T. cornetzi : 1031 (GCA) vs 1099 (GCF).

Les annotations mitochondriales semblent bien représentées dans les deux bases de données. La légère différence pourrait être liée aux critères de filtration.

La catégorie y apparaît uniquement dans T. cornetzi (GCA) avec 2 occurrences, cela pourrait refléter une anomalie ou une spécificité de l'annotation dans cette espèce.

Globalement :

- Pour T. septentrionalis :

GCF a une proportion nettement plus élevée de transcrits parfaitement alignés (=) : 14598 (GCF) vs 4510 (GCA).

Les ambiguïtés (k, n) sont plus fréquentes dans GCA, suggérant une annotation moins précise.

GCF semble mieux résolue pour cette espèce, avec une dominance des alignements exacts (j et =).

- Pour T. zeteki :

GCA inclut davantage de transcrits dans des régions ambiguës (k, n) et a une proportion plus faible d'alignements exacts (j).

GCF montre une annotation plus stricte et mieux définie, notamment avec une proportion plus élevée de j.

- Pour T. cornetzi :

Les résultats pour T. cornetzi diffèrent légèrement des autres espèces.

GCA montre une proportion plus élevée de j que GCF, contrairement aux autres espèces.

Une proportion notable de k (3773) dans GCA suggère des loci multiples ou des duplications plus fréquents.

La catégorie y apparaît uniquement dans GCA, bien que marginale (2 occurrences).

**01/12/2024**

**Utilisation de l'outil BUSCO version 5.7.1 sur les annotations GCA et GCF pour les éspèces T.cornetzi et T.zeteki**

L'objectif de cette étape est d'évaluer la complétude des annotations de transcrits obtenues pour les trois espèces de Trachymyrmex  en utilisant l'outil BUSCO (Benchmarking Universal Single-Copy Orthologs). 

Cette analyse permet de mesurer la proportion d'orthologues universels présents, fragmentés ou manquants, afin d'évaluer la qualité et la complétude des transcrits annotés pour les bases GCF (RefSeq) et GCA (GenBank).

Pour chaque espèce et chaque annotation (GCF et GCA), BUSCO a été exécuté en mode transcriptome avec la commande suivante :

busco -i [chemin/vers/les/transcrits.fasta] -l insecta_odb10 -o [chemin/de/sortie/busco_output] -m transcriptome -f

Les résultats de BUSCO sont enregistrés dans un fichier texte nommé short_summary.specific.insecta_odb10.busco_output.txt situé dans les dossiers respectifs des sorties, par exemple :

    annotation_analysis/annotation_gcf/T_zeteki/busco_output/short_summary.specific.insecta_odb10.busco_output.txt

Chaque analyse produit un rapport BUSCO contenant :

    - Le pourcentage de gènes complets (C), répartis en gènes simple-copie (S) et dupliqués (D).
    
    - Le pourcentage de gènes fragmentés (F).
    
    - Le pourcentage de gènes manquants (M).
    
    - Le nombre total d'orthologues BUSCO recherchés dans la base insecta_odb10.

Ces résultats permettent de comparer directement la complétude des annotations GCF et GCA pour chaque espèce.

T. zeteki

    Annotation GCA :
        
        93,1 % de gènes complets (47,5 % en copie unique, 45,6 % en copies dupliquées).
        
        4,7 % de gènes fragmentés.
        
        7,2 % de gènes manquants.

    Annotation GCF :
        
        98,6 % de gènes complets (52,9 % en copie unique, 45,7 % en copies dupliquées).
        
        0,7 % de gènes fragmentés.
        
        0,7 % de gènes manquants.

T. cornetzi

    Annotation GCA :
        
        94,1 % de gènes complets (46,8 % en copie unique, 47,3 % en copies dupliquées).
        
        3,8 % de gènes fragmentés.
        
        2,1 % de gènes manquants.

    Annotation GCF :
        
        98,0 % de gènes complets (50,4 % en copie unique, 47,6 % en copies dupliquées).
        
        1,1 % de gènes fragmentés.
        
        0,9 % de gènes manquants.


Les annotations GCF présentent une proportion significativement plus élevée de gènes complets dans toutes les espèces étudiées (entre 98,0 % et 99,1 %) par rapport aux annotations GCA (entre 93,1 % et 97,2 %). Cette tendance est cohérente avec la réputation de RefSeq (GCF) en tant que base de données rigoureusement validée.

Les annotations GCA montrent une proportion plus élevée de gènes fragmentés et manquants par rapport à GCF. Par exemple, pour T. zeteki, les gènes fragmentés représentent 4,7 % dans GCA contre 0,7 % dans GCF, et les gènes manquants 2,2 % contre 0,7 %.

La proportion de gènes dupliqués est légèrement plus élevée dans les annotations GCF pour certaines espèces, notamment T. septentrionalis (51,1 % pour GCF contre 49,1 % pour GCA). Cela pourrait indiquer une meilleure capacité à capturer des duplications dans GCF.



