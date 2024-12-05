README - Analyse des annotations génomiques

Ce dossier contient les fichiers, scripts et résultats liés à l'analyse des annotations génomiques pour évaluer la qualité et la pertinence des annotations GCA et GCF.

Structure du dossier

Fichiers principaux

    analysis_tracking_file.py : Script Python pour analyser les fichiers .tracking et générer des rapports sur les correspondances des annotations.
    
    report_annotation.py : Script Python pour générer un rapport global à partir des analyses effectuées.

    compare_busco.py : Script Python pour comparer les résultats des analyses BUSCO entre les annotations GCA et GCF.

Sous-dossiers

    annotation_gca/ : Contient les résultats d'analyse des annotations basées sur les génomes GCA.
        
        Organisation par espèce : T_cornetzi/, T_septentrionalis/, T_zeteki/
    
    annotation_gcf/ : Contient les résultats d'analyse des annotations basées sur les génomes GCF.
        
        Organisation par espèce : T_cornetzi/, T_septentrionalis/, T_zeteki/

Exemple de contenu des sous-dossiers (annotation_gcf/T_zeteki)

    busco_output/ : Contient les résultats détaillés de l'analyse BUSCO pour l'espèce.

    comparison_output.annotated.gtf : Fichier GTF annoté après comparaison avec la référence.
    
    comparison_output.tracking : Fichier de correspondance détaillant les relations entre les annotations assemblées et les annotations de référence.
    
    comparison_output.loci : Informations sur les loci annotés.
    
    comparison_output.stats : Statistiques générales issues de l'annotation.
    
    report_gcf_T_zeteki.txt : Rapport global pour l'annotation GCF de l'espèce T. zeteki.
    
    tracking_analysis_report.txt : Rapport d'analyse des correspondances basé sur le fichier .tracking.

Résultats BUSCO :

Dans chaque sous-dossier d'espèce (exemple : annotation_gca/T_zeteki/ ou annotation_gcf/T_zeteki/) :

    busco_output/ : Sous-dossier contenant les fichiers produits par BUSCO.
    
    Exemple de fichiers dans ce sous-dossier :
        
        full_table.tsv : Résumé complet des gènes évalués.
        
        short_summary.txt : Résumé succinct des résultats BUSCO.

Autres fichiers à la racine

    busco_differences_Tcornetzi.csv : Comparaison des résultats BUSCO pour T. cornetzi entre GCA et GCF.
    
    busco_differences_Tseptentrionalis.csv : Comparaison des résultats BUSCO pour T. septentrionalis entre GCA et GCF.
    
    busco_differences_Tzeteki.csv : Comparaison des résultats BUSCO pour T. zeteki entre GCA et GCF.

Objectif

L'objectif de ce dossier est de comparer et d'évaluer la qualité des annotations génomiques GCA et GCF pour les trois espèces étudiées :

    Identifier les gènes bien pris en charge, partiels, ou non pris en charge.
    
    Mettre en évidence les correspondances avec les loci et les catégories spécifiques (e.g., exonic, intergenic).
    
    Produire des rapports détaillés pour guider l'amélioration ou la validation des annotations.

Notes supplémentaires

    Les rapports générés dans chaque sous-dossier incluent des statistiques détaillées pour chaque espèce.
    
    Les fichiers .tracking sont essentiels pour identifier les correspondances entre les annotations assemblées et les annotations de référence.

    Les résultats BUSCO sont cruciaux pour évaluer la complétude des génomes annotés et permettent de comparer les annotations GCA et GCF.
