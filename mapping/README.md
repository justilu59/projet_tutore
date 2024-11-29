README - Dossier de mapping

Ce dossier contient les résultats de l'étape de mapping des lectures transcriptomiques contre les génomes de référence GCA. 

Les sous-dossiers sont organisés par espèces, et chaque fichier correspond à un échantillon aligné.

Structure du dossier

Organisation générale

    T_cornetzi/ : Résultats de mapping pour l'espèce Trachymyrmex cornetzi.
    
    T_septentrionalis/ : Résultats de mapping pour l'espèce Trachymyrmex septentrionalis.
    
    T_zeteki/ : Résultats de mapping pour l'espèce Trachymyrmex zeteki.

Chaque sous-dossier contient les fichiers de sortie générés pour chaque échantillon lors de l'alignement avec STAR.

Exemple de contenu d'un sous-dossier (T_septentrionalis/)

    SRR3270634_gca_Aligned.out.bam : Fichier BAM contenant les lectures alignées.
    
    SRR3270634_gca_sorted.bam : Fichier BAM trié.
    
    SRR3270634_gca_Log.out : Journal principal généré par STAR pour l'échantillon.
    
    SRR3270634_gca_Log.final.out : Résumé des statistiques d'alignement final.
    
    SRR3270634_gca_Log.progress.out : Journal de progression durant l'exécution.
    
    SRR3270634_gca_SJ.out.tab : Tableau des jonctions splicées détectées.

Objectif

Ces fichiers résultent de l'étape d'alignement des lectures transcriptomiques pour :

    Identifier les régions alignées des séquences RNA sur le génome de référence.
    
    Générer des fichiers BAM nécessaires aux étapes suivantes, comme l'assemblage de transcriptomes et l'analyse des jonctions splicées.

Notes techniques

    Outil utilisé : STAR (Spliced Transcripts Alignment to a Reference).
    
    Commandes STAR : Les alignements ont été réalisés en mode 2-pass avec les options suivantes :

STAR --runThreadN <num_threads> --genomeDir <genome_index_dir> --readFilesIn <input_reads> --outFileNamePrefix <prefix> --outSAMtype BAM SortedByCoordinates

    Fichiers d'entrée : Lectures RNA-seq préalablement contrôlées et éventuellement corrigées.
    
    Fichiers de référence : Génomes de référence.

Notes supplémentaires

    Les fichiers BAM triés (_sorted.bam) peuvent être utilisés directement pour des analyses downstream comme l'assemblage des transcriptomes.
    
    Les fichiers _SJ.out.tab contiennent les jonctions splicées identifiées, utiles pour évaluer la qualité des annotations génomiques.
