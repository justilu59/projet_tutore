README - Dossier d'assemblage des transcrits

Ce dossier contient les résultats de l'assemblage des transcrits alignés sur les génomes de référence GCA, ainsi que des fichiers de comparaison pour évaluer la qualité des annotations.

Structure du dossier

Organisation générale

    T_cornetzi/ : Résultats d'assemblage pour l'espèce Trachymyrmex cornetzi.
    
    T_septentrionalis/ : Résultats d'assemblage pour l'espèce Trachymyrmex septentrionalis.
    
    T_zeteki/ : Résultats d'assemblage pour l'espèce Trachymyrmex zeteki.

Chaque sous-dossier contient les fichiers générés après l'assemblage des transcrits et la comparaison avec les annotations génomiques de référence.

Exemple de contenu d'un sous-dossier (T_zeteki/)

    assembled_transcripts.gtf : Fichier GTF contenant les transcrits assemblés par StringTie ou un autre outil d'assemblage.

    assembled_transcripts.fasta : Fichier FASTA contenant les séquences nucléotidiques des transcrits assemblés. Utilisé pour l'analyse BUSCO afin d'évaluer la complétude des transcrits.
    
    comparison_output.assembled_transcripts.gtf.tmap : Fichier TMAP contenant les correspondances entre les transcrits assemblés et les transcrits de référence.
    
    comparison_output.assembled_transcripts.gtf.refmap : Fichier REFMAP contenant les correspondances détaillées entre les transcrits assemblés et les transcrits de référence.

Objectif

L'assemblage des transcrits permet :

    D'identifier et de quantifier les transcrits exprimés dans chaque échantillon.
    
    De comparer les transcrits assemblés aux annotations génomiques de référence pour évaluer leur qualité ou identifier des transcrits non annotés.

Notes techniques

    Outil utilisé : StringTie (ou équivalent).
    
    Commandes StringTie : Les assemblages ont été réalisés avec les options suivantes (à adapter selon vos paramètres réels) :

    stringtie <aligned_bam_file> -G <reference_annotation> -o <output_gtf> -A <gene_abundance_output>

Notes supplémentaires

    Le fichier assembled_transcripts.gtf peut être utilisé pour des analyses downstream, comme l'identification des gènes exprimés ou l'amélioration des annotations.

    Le fichier assembled_transcripts.fasta est crucial pour l'évaluation de la complétude des transcrits assemblés à l'aide de BUSCO.
    
    Les fichiers .tmap et .refmap sont particulièrement utiles pour repérer les transcrits non annotés, les exons manquants ou les erreurs de limites dans les annotations de référence.
