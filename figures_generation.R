# Charger les bibliothèques nécessaires
library(ggplot2)
library(tidyr)
library(dplyr)
library(grid)
library(gridExtra)
library(cowplot)
library(VennDiagram)
# Données combinées
data <- data.frame(
  Species = rep(c("T. cornetzi", "T. septentrionalis", "T. zeteki"), each = 5),
  Category = rep(
    c("Gènes non-supportés (loci)", 
      "Gènes non-supportés (tracking)", 
      "Exons manquants", 
      "Erreurs de bornes", 
      "Transcrits manquants"), 3
  ),
  GCF = c(
    15.97, 25.75, 11.37, 39.40, 42.33,   # T. cornetzi
    10.58, 17.75, 7.69, 30.70, 33.04,    # T. septentrionalis
    13.43, 17.05, 11.16, 36.60, 39.01    # T. zeteki
  ),
  GCA = c(
    34.40, 31.10, 28.19, 71.30, 76.62,   # T. cornetzi
    27.11, 25.14, 23.48, 66.00, 70.37,   # T. septentrionalis
    29.41, 29.31, 25.06, 68.10, 72.64    # T. zeteki
  )
)

# Transformer les données en format long
data_long <- pivot_longer(data, cols = c(GCF, GCA), names_to = "Annotation", values_to = "Percentage")

# Exclure "Gènes non-supportés (tracking)"
data_long <- data_long[data_long$Category != "Gènes non-supportés (tracking)", ]


#Figure 1
ggplot(data_long, aes(x = Category, y = Percentage, fill = Annotation)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8)) +
  geom_text(aes(label = paste0(round(Percentage, 1), "%")), 
            position = position_dodge(width = 0.8), 
            vjust = -0.3, size = 3) +
  scale_fill_manual(values = c("GCF" = "#4a90e2", "GCA" = "#f5a623")) +
  facet_wrap(~Species, ncol = 1, scales = "free_y") +
  labs(
    x = NULL,
    y = "Pourcentage (%)",
    fill = "Type d'annotation"
  ) +
  ylim(0, 110) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 30, hjust = 1),
    strip.text = element_text(face = "bold", size = 12),
    legend.position = "top",
    plot.margin = margin(15, 15, 10, 15)
  )

# Figure 2
# Données combinées pour les trois espèces
data <- data.frame(
  Species = c(
    rep("T. septentrionalis", 8), 
    rep("T. zeteki", 8), 
    rep("T. cornetzi", 8)
  ),
  Type = rep(c("Aligned (=)", "Unsupported (u)", "Partial (p)", "Ambiguous (other)"), times = 6),  # Légende explicite
  Annotation = rep(c("GCA", "GCF"), each = 4, times = 3),  # Répéter GCA et GCF pour chaque espèce
  Count = c(
    # T. septentrionalis
    4510, 4586, 2185, 22552, # GCA
    14598, 2832, 2110, 14357, # GCF
    # T. zeteki
    4011, 5284, 2136, 19791, # GCA
    12121, 2634, 2142, 13169, # GCF
    # T. cornetzi
    4379, 6819, 2319, 23345, # GCA
    13162, 4942, 2203, 15319  # GCF
  )
)

# Transformer les données en format long et calculer les proportions
data_long <- data %>%
  group_by(Species, Annotation) %>%
  mutate(Percentage = (Count / sum(Count)) * 100)

ggplot(data_long, aes(x = Annotation, y = Percentage, fill = Type)) +
  geom_bar(stat = "identity", width = 0.7) +
  geom_text(aes(label = ifelse(Percentage > 2, sprintf("%.1f%%", Percentage), "")), 
            position = position_stack(vjust = 0.5), size = 3) +  # Masque les valeurs < 2%
  scale_fill_manual(
    values = c(
      "Aligned (=)" = "#66c2a5", 
      "Unsupported (u)" = "#fc8d62", 
      "Partial (p)" = "#8da0cb", 
      "Ambiguous (other)" = "#e78ac3"
    ),
    name = "Type de correspondance"
  ) +
  facet_wrap(~Species, ncol = 1) + 
  labs(
    x = "Type d'annotation",
    y = "Pourcentage (%)"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 30, hjust = 1),
    strip.text = element_text(face = "bold", size = 12),
    plot.margin = margin(15, 15, 10, 15),
    legend.position = "top"  # Place la légende en haut pour optimiser l'espace
  )


# Données combinées pour T. septentrionalis, T. zeteki, et T. cornetzi
data <- data.frame(
  Species = c(
    rep("T. septentrionalis", 18),  # 9 catégories × 2 annotations (GCA, GCF)
    rep("T. zeteki", 18),          # 9 catégories × 2 annotations (GCA, GCF)
    rep("T. cornetzi", 20)         # 10 catégories × 2 annotations (GCA, GCF)
  ),
  Category = c(
    rep(c("j", "m", "k", "o", "n", "c", "i", "e", "x"), 4),  # Pour T. septentrionalis et T. zeteki
    rep(c("j", "m", "k", "o", "n", "c", "i", "e", "x", "y"), 2)  # Pour T. cornetzi
  ),
  Annotation = c(
    rep(c("GCF", "GCA"), each = 9),  # Pour T. septentrionalis
    rep(c("GCF", "GCA"), each = 9),  # Pour T. zeteki
    rep(c("GCF", "GCA"), each = 10)  # Pour T. cornetzi
  ),
  Count = c(
    # T. septentrionalis
    9029, 901, 1142, 412, 699, 1259, 833, 79, 3, # GCF
    12702, 921, 3367, 1149, 1850, 851, 1461, 232, 19, # GCA
    # T. zeteki
    7652, 943, 945, 310, 1613, 858, 735, 107, 6, # GCF
    10748, 970, 2779, 887, 998, 1977, 1178, 238, 16, # GCA
    # T. cornetzi
    8760, 1099, 1149, 411, 917, 1843, 991, 145, 4, 0, # GCF
    12200, 1031, 3773, 1276, 1998, 1168, 1587, 296, 14, 2 # GCA
  )
)

# Transformer les données en format long et calculer les proportions
data_long <- data %>%
  group_by(Species, Annotation) %>%
  mutate(Percentage = (Count / sum(Count)) * 100)


# Remplacer les abréviations par des descriptions dans la légende
data_long$Category <- recode(data_long$Category,
                             "j" = "Alignement exact des introns",
                             "m" = "Alignement mitochondrial",
                             "k" = "Correspond à plusieurs loci",
                             "o" = "Chevauchement sur brin opposé",
                             "n" = "Régions intergéniques",
                             "c" = "Inclus dans un locus de référence",
                             "i" = "Inclus dans un intron de référence",
                             "e" = "Chevauchement exons",
                             "x" = "Limites du locus",
                             "y" = "Catégorie inconnue")


ggplot(data_long, aes(x = Species, y = Percentage, fill = Category)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8)) +  # Graphique groupé
  geom_text(aes(label = ifelse(Percentage > 2, sprintf("%.1f%%", Percentage), "")), 
            position = position_dodge(width = 0.8), vjust = -0.5, size = 3) +  # Annotations
  scale_fill_manual(
    values = c(
      "Alignement exact des introns" = "#66c2a5",
      "Alignement mitochondrial" = "#fc8d62",
      "Correspond à plusieurs loci" = "#8da0cb",
      "Chevauchement sur brin opposé" = "#e78ac3",
      "Régions intergéniques" = "#a6d854",
      "Inclus dans un locus de référence" = "#ffd92f",
      "Inclus dans un intron de référence" = "#e5c494",
      "Chevauchement exons" = "#b3b3b3",
      "Limites du locus" = "#8dd3c7",
      "Catégorie inconnue" = "#fb8072"
    )
  ) +
  facet_wrap(~Annotation, ncol = 2) +  # Une facette par annotation
  labs(
    x = "Espèce",
    y = "Pourcentage (%)",
    fill = "Type de correspondance"
  ) +
  theme_minimal() +
  theme(
    legend.position = "top",  # Place la légende en haut
    axis.text.x = element_text(angle = 0, hjust = 0.5),
    strip.text = element_text(face = "bold", size = 12),
    plot.margin = margin(10, 20, 10, 10)
  )

# Préparer les données
data <- data.frame(
  Species = rep(c("T. septentrionalis", "T. zeteki", "T. cornetzi"), each = 8),
  Annotation = rep(c("GCA", "GCF"), times = 12),
  Category = rep(c("Complete (S)", "Complete (D)", "Fragmented", "Missing"), each = 2, times = 3),
  Percentage = c(
    # T. septentrionalis
    48.1, 48.0, 49.1, 51.1, 1.2, 0.3, 1.6, 0.6,
    # T. zeteki
    47.5, 52.9, 45.6, 45.7, 4.7, 0.7, 2.2, 0.7,
    # T. cornetzi
    46.8, 50.4, 47.3, 47.6, 3.8, 1.1, 2.1, 0.9
  )
)

# Fonction pour créer un camembert sans légende
plot_pie_no_legend <- function(df, species_name, annotation_name) {
  ggplot(df, aes(x = "", y = Percentage, fill = Category)) +
    geom_bar(stat = "identity", width = 1, color = "white") +
    coord_polar(theta = "y") +
    geom_text(
      aes(label = ifelse(Percentage > 5, sprintf("%.1f%%", Percentage), "")),
      position = position_stack(vjust = 0.5), size = 3
    ) +  # Affiche les pourcentages > 5%
    labs(
      title = paste(species_name, "-", annotation_name),
      x = NULL,
      y = NULL
    ) +
    theme_void() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 12, face = "bold"),
      legend.position = "none"  # Supprime la légende individuelle
    )
}

# Créer un graphique factice pour la légende
legend_plot <- ggplot(data, aes(x = "", y = Percentage, fill = Category)) +
  geom_bar(stat = "identity") +
  guides(fill = guide_legend(ncol = 2)) +  # Légende en deux colonnes
  theme_void() +
  theme(
    legend.position = "bottom",
    legend.text = element_text(size = 10),
    legend.title = element_blank()  # Supprime le titre de la légende
  )

plots <- list()
for (species in unique(data$Species)) {
  for (annotation in unique(data$Annotation)) {
    subset_data <- data %>% filter(Species == species, Annotation == annotation)
    plots[[paste(species, annotation)]] <- plot_pie_no_legend(subset_data, species, annotation)
  }
}

# Combiner les graphiques avec une légende commune
final_plot <- grid.arrange(
  grobs = c(plots, list(legend)),  
  layout_matrix = rbind(
    c(1, 2),  # Ligne 1 : Graphiques
    c(3, 4),  # Ligne 2 : Graphiques
    c(5, 6),  # Ligne 3 : Graphiques
    c(7, 7)   
)
)

# Figure supplémentaire
# Générer les trois diagrammes
# Fonction pour générer un diagramme de Venn esthétique

generate_venn <- function(area1, area2, cross_area, species_name) {
  venn <- draw.pairwise.venn(
    area1 = area1,
    area2 = area2,
    cross.area = cross_area,
    category = c("GCF", "GCA"),
    fill = c("#A6CEE3", "#FB9A99"),  # Couleurs pastel harmonisées
    alpha = c(0.6, 0.6),
    cat.pos = c(-30, 30),
    cat.dist = c(0.05, 0.05),
    cex = 1.5,  # Taille des chiffres dans les cercles
    cat.cex = 1.2,  # Taille des labels GCF et GCA
    euler.d = TRUE,
    scaled = TRUE,
    ind = FALSE  # Retourne en tant qu'objet grob
  )
  
  # Ajouter un titre au-dessus du diagramme pour l'espèce
  title_grob <- textGrob(species_name, gp = gpar(fontsize = 14, fontface = "bold"))
  
  # Combiner le titre et le diagramme
  combined_grob <- arrangeGrob(title_grob, venn, ncol = 1, heights = c(0.2, 1))
  
  return(combined_grob)
}

# Générer les diagrammes de Venn pour chaque espèce
venn1 <- generate_venn(area1 = 591, area2 = 562, cross_area = 394, species_name = "T. cornetzi")
venn2 <- generate_venn(area1 = 615, area2 = 580, cross_area = 447, species_name = "T. zeteki")
venn3 <- generate_venn(area1 = 647, area2 = 609, cross_area = 404, species_name = "T. septentrionalis")

# Combiner les diagrammes dans une figure
grid.arrange(
  venn1, venn2, venn3, 
  ncol = 3, 
  top = textGrob(
    "Comparaison des annotations GCA et GCF pour trois espèces de Trachymyrmex", 
    gp = gpar(fontsize = 16, fontface = "bold")
  )
)
