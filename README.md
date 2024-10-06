# projet_tutore
**04/10** 

Analyse de la qualité des reads forward et reverse de T.cornetzi et de T.septentrionalis avec l'outil Fastqc version 0.11.9 et application de la commande fastqc -o quality_reports/T_cornetzi raw_reads/T_cornetzi/SRR3270378_1.fastq.gz raw_reads/T_cornetzi/SRR3270378_2.fastq.gz et fastqc -o quality_reports/T_septentrionalis raw_reads/T_septentrionalis/SRR3270634_1.fastq.gz raw_reads/T_septentrionalis/SRR3270634_2.fastq.gz

**06/10** 

Analyse de qualité des reads SRR3270634_1 et SRR3270634_2 de T.septentrionalis : 
- reads de longueur 90 pb et 
- 42% GC, 
- per base sequence content : on oberve une distribution non uniforme pour les 10-15 nucléotides, ce qui est normal en RNA-seq
- sequence duplication level : on a un certain nombre de reads qui sont présents plusieurs fois, il est attendu d'avoir des reads dupliqués pour les transcrits de forte abondance
- overrepresented sequence : il y a présence de séquence qui correspond à un adaptateur Truseq dans SRR3270634_1

