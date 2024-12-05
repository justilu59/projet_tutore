# Evaluation de l'annotation des génomes par approche transcriptomique

Ce projet vise à évaluer la qualité des annotations génomiques (GCA et GCF) pour trois espèces de la fourmi Trachymyrmex (T. septentrionalis, T. cornetzi, T. zeteki), en utilisant des données transcriptomiques. 

L'objectif est d'identifier les forces et faiblesses des annotations en comparant les transcrits assemblés aux génomes de référence.

## Etapes du projet

**1.Récupération des données de génomique et de transcriptomique**

    Données transcriptomiques :
        
        Récupérées depuis SRA.
        
        Stockées dans le dossier raw_reads, subdivisé par espèce :
            
            T_septentrionalis/
            
            T_cornetzi/
            
            T_zeteki/

    Données génomiques :
        
        Récupérées depuis NCBI.
        
        Stockées dans le dossier genomes, organisé en deux sous-dossiers :
            
            gca_genomes/ (annotations GCA)
            
            gcf_genomes/ (annotations GCF)
        
        Chaque sous-dossier est subdivisé par espèce, et les fichiers originaux (dossier ncbi_dataset) sont conservés.


**2.Traitement des données brutes**

Contrôle qualité :

    Réalisé avec FastQC, les rapports sont stockés dans reads_quality_reports, subdivisé par espèce.

Trimmage des lectures :

    Si nécessaire, les adaptateurs et bases de mauvaise qualité sont supprimés avec Trimmomatic ou Cutadapt.

**3.Alignement des lectures**

Alignement :

    Les lectures sont alignées sur les génomes de référence avec STAR.

Organisation :

    Les index de génomes sont stockés dans index_genomes, subdivisés en index_gca/ et index_gcf/, avec des sous-dossiers pour chaque espèce.
    
    Les fichiers d'alignement au format SAM sont stockés dans mapping, organisé de manière similaire (map_gca/ et map_gcf/).

**4.Assemblage des transcrits**

Objectif :

    Assembler les transcrits alignés pour évaluer leur concordance avec les annotations GCA et GCF.

Outil utilisé :

    StringTie

Organisation :

    Les fichiers assemblés au format GTF et FASTA sont stockés dans transcripts_assembly, subdivisé en gca_assembly/ et gcf_assembly/, avec des sous-dossiers pour chaque espèce.


**5.Analyse de la Qualité des Annotations**

Comparaison des transcrits assemblés :

    Réalisée avec GFFCompare pour évaluer les concordances, transcrits manquants, exons manquants, et erreurs de bornes.

Organisation :

    Les résultats sont stockés dans annotation_analysis, subdivisé en annotation_gca/ et annotation_gcf/, avec des sous-dossiers pour chaque espèce.

Scripts d'analyse :

    report_annotation.py : Génère un rapport global résumant les loci manquants, exons manquants, transcrits manquants, et erreurs de bornes.
    
    compare_busco.py : Compare les résultats BUSCO entre GCA et GCF pour chaque espèce.

Résultats supplémentaires :

    Les fichiers FASTA des transcrits assemblés sont analysés avec BUSCO pour évaluer leur complétude.


## Organisation des fichiers

/data/projet1/projet_tutore/

├── Cahier_de_laboratoire.md
├── README.md
├── raw_reads/
│   ├── T_septentrionalis/
│   ├── T_cornetzi/
│   ├── T_zeteki/
├── genomes/
│   ├── gca_genomes/
│   │   ├── T_septentrionalis/
│   │   ├── T_cornetzi/
│   │   ├── T_zeteki/
│   ├── gcf_genomes/
├── reads_quality_reports/
│   ├── T_septentrionalis/
│   ├── T_cornetzi/
│   ├── T_zeteki/
├── index_genomes/
│   ├── index_gca/
│   │   ├── T_septentrionalis/
│   │   ├── T_cornetzi/
│   │   ├── T_zeteki/
│   ├── index_gcf/
├── mapping/
│   ├── map_gca/
│   │   ├── T_septentrionalis/
│   │   ├── T_cornetzi/
│   │   ├── T_zeteki/
│   ├── map_gcf/
├── transcripts_assembly/
│   ├── gca_assembly/
│   │   ├── T_septentrionalis/
│   │   ├── T_cornetzi/
│   │   ├── T_zeteki/
│   ├── gcf_assembly/
├── annotation_analysis/
│   ├── annotation_gca/
│   │   ├── T_septentrionalis/
│   │   ├── T_cornetzi/
│   │   ├── T_zeteki/
│   ├── annotation_gcf/

## Outils utilisés

    FastQC (v0.11.9) : Évaluation de la qualité des lectures.
    
    Cutadapt (v3.4) : Nettoyage des lectures.
    
    STAR (v2.7.10a) : Alignement des lectures sur le génome de référence.
    
    StringTie (v2.1.8) : Assemblage des transcrits.
    
    GFFCompare (v0.12.6) : Comparaison des transcrits avec les annotations de référence.
    
    BUSCO (v5.4.3) : Évaluation de la complétude des transcrits assemblés.
    
    Python scripts :
        
        report_annotation.py : Génération de rapports d'analyse.
        
        compare_busco.py : Comparaison des résultats BUSCO.

## Résultats attendus

Pourcentages calculés :

    Gènes non supportés.
    
    Transcrits et exons manquants.
    
    Erreurs de bornes.

Comparaison GCA vs GCF :

    Identifier l'annotation offrant la meilleure couverture et précision pour chaque espèce.


