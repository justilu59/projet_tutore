README - Dossier des génomes GCF

Ce dossier contient les données génomiques associées aux espèces étudiées dans le cadre du projet tutoré. Les données sont organisées par espèces, avec des sous-dossiers contenant les fichiers génomiques nécessaires à l'analyse.
Structure du dossier

    T_cornetzi/ : Données pour l'espèce Trachymyrmex cornetzi.
    
    T_septentrionalis/ : Données pour l'espèce Trachymyrmex septentrionalis.
    
    T_zeteki/ : Données pour l'espèce Trachymyrmex zeteki.

Chaque sous-dossier contient les fichiers téléchargés depuis NCBI ou une source équivalente et est organisé comme suit :

Exemple de structure d'un sous-dossier (T_septentrionalis/ncbi_dataset/data/GCF_001594115.1) :

    GCF_001594115.1_Tsep1.0_genomic.fna : Séquences génomiques au format FASTA.
    
    genomic.gff : Fichier d'annotation génomique au format GFF.
    
    genomic.gtf : Fichier d'annotation génomique au format GTF.
    
    protein.faa : Séquences protéiques prédictes au format FASTA.
    
    rna.fna : Séquences ARN au format FASTA.
    
    cds_from_genomic.fna : Séquences des CDS (Codant DNA Sequences) extraites du génome.
    
    sequence_report.jsonl : Rapport JSON détaillant les métadonnées de l'ensemble de données génomiques.

Objectif

Ces données sont utilisées pour :

    Comparer et évaluer la qualité de deux annotations génomiques (GCA et GCF).
    
    Analyser les transcriptomes alignés pour valider ou améliorer les annotations existantes.
    
    Explorer les caractéristiques spécifiques des génomes des différentes espèces étudiées.

Notes supplémentaires

    Les noms des dossiers et fichiers suivent les conventions standard de NCBI pour faciliter la traçabilité.

