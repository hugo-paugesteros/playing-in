Questions :
1. L'ouverture a-t-elle eu un effet sur le Klimke ?
1. L'ouverture a-t-elle eu un effet sur la violoniste test ?

Question : L'ouverture a-t-elle eu un effet significatif sur le violon test ("Klimke") ?


1. Faut-il normaliser les notes (par ex., z-scores) ?
    - Peut-être utile pour l'ANOVA ou le t-test afin de réduire la variance inter-juges
    - Peut-être inutile pour le LMM qui modélise directement chaque personne via un random effect
    - Inutile pour les tests de Wilcoxon / Friedman qui utilisent les rangs

2. Quel test statistique ?
    A. Comparaison à 2 niveaux (S1 vs S3, S2 vs S3, (S1+S2)/2 vs S3)
        - si distrib normale : paired t-test
        - sinon : Wilcoxon

    B. Comparaison à 3 niveaux (S1 vs S2 vs S3)
        - si distrib normale : One-way Repeated Measures ANOVA
        - sinon : Friedman
        - nécessite de faire des tests post-hoc si significatif

    C. Modélisation
        - Linear Mixed Model pour modéliser les notes : `Ratings ~ Violin * Session + (1|Player)`