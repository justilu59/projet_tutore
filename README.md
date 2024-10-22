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

Ensuite, le mapping est effectué et les fichiers SAM générés sont stockés dans le dossier mapping

