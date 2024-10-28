# Evaluation de l'annotation des génomes par approche transcriptomique

Le but du projet est d'utiliser des données de transcriptomiques pour évaluer la qualité de deux annotation gca et gcf chez trois génomes de la fourmi Trachymyrmex.

**Récupération des données de génomique et de transcriptomique**

Objectif : Stocker les données dans dossiers dédiés


Les données de transcriptomique ont été récupérés sur SRA et stockées dans le dossier raw_reads qui a été subdivisé en 3 dossiers, un par éspèce différente.

Les données de génomique ont été récupérées sur NCBI et stockées dans le dossier genomes subdivisé en gca_genomes et gcf_genomes, ces 2 dossiers étant eux-mêmes subdivisés en 3, un pour chaque éspèce

**Traitement des données brutes**

Objectif : Nettoyer et préparer les lectures de séquence pour l'analyse


La qualité des lectures est contrôlée par l'utilisation d'outils comme FastQC qui effectue une série de contrôles et génére un rapport. Ces rapports sont stockés dans le dossier reads_qality_reports subdivisé en 3, un pour chaque éspèce

Si nécessaire un trimmage est réalisé pour retirer les adapteurs et les bases de mauvaise qualité avec des outils comme Trimmomatic ou Cutadapt.

**Alignement**

Objectif : Aligner les lectures des séquences sur un génome de référence

L'aligner STAR est utilisé pour mapper les lectures sur le génome de référence.

En première étape, un indexage du génome de référence et réalisé et stocké dans le dossier index_genomes.

Ensuite, le mapping est effectué et les fichiers SAM générés sont stockés dans le dossier mapping.


**Assemblage des transcrits**

Objectif : Assembler les transcrits à partir des lectures alignées pour les comparer avec les annotations génomiques disponibles (GCA et GCF) et évaluer la qualité de ces annotations.

StringTie est utilisé pour assembler les transcrits à partir des fichiers SAM alignés.

Les fichiers de sortie en format GTF sont stockés dans le dossier transcripts_assembly, avec des sous-dossiers pour chaque espèce.


**Analyse de la Qualité des Annotations**

Objectif : Évaluer la précision et la couverture des annotations génomiques GCA et GCF par rapport aux transcrits assemblés.

GFFCompare est utilisé pour comparer les fichiers GTF des transcrits assemblés avec les annotations de référence GCA et GCF.

Différents fichiers de sortie sont créés pour chaque comparaison, fournissant des informations sur les transcrits et exons manquants, les erreurs de borne, etc., stockés dans le dossier annotation_analysis.

Utilisation du script Python pour extraire des statistiques importantes sur les loci manquants, exons manquants, et erreurs de bornes.

Les pourcentages de gènes non supportés, d'exons manquants, de transcrits manquants, et d'erreurs de bornes sont calculés et comparés pour GCA et GCF.

Les résultats sont comparés entre les annotations GCA et GCF pour identifier laquelle offre une couverture et une précision supérieures pour chaque espèce.

