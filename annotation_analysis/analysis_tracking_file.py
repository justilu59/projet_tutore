import re
import argparse
import os

# Description des catégories "other"
OTHER_DESCRIPTIONS = {
    'e': "Exonic overlap with reference, but no intron match",
    'm': "Match to mitochondrial genome",
    'o': "Generic exonic overlap with reference on the opposite strand",
    'x': "Exonic overlap with reference at the boundary of a locus",
    'i': "Contained within a reference intron",
    'k': "Match with multiple reference loci",
    'j': "Exact match of intron chain",
    'n': "No match, intergenic region",
    'c': "Contained within a reference locus"
}

# Fonction pour analyser le fichier `.tracking`
def analyze_tracking_file(tracking_file):
    gene_counts = {
        '=': 0,  # Aligned
        'u': 0,  # Unsupported
        'p': 0,  # Partial
        'other': 0  # Any other type
    }
    genes = set()

    with open(tracking_file, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                columns = line.strip().split('\t')
                gene_info = columns[1]  # Gene name or identifier
                match_type = columns[3]  # Correspondence type
                genes.add(gene_info)

                if match_type in gene_counts:
                    gene_counts[match_type] += 1
                else:
                    gene_counts['other'] += 1

    return gene_counts, len(genes)

# Fonction pour analyser les gènes marqués comme "other" dans `.tracking`
def analyze_other_genes(tracking_file):
    other_genes = []

    with open(tracking_file, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            match_type = columns[3]
            if match_type not in ('=', 'u', 'p'):
                other_genes.append(match_type)

    return set(other_genes)

# Fonction pour compter les types "other"
def count_other_types(tracking_file):
    other_counts = {}

    with open(tracking_file, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            match_type = columns[3]
            if match_type not in ('=', 'u', 'p'):
                if match_type not in other_counts:
                    other_counts[match_type] = 0
                other_counts[match_type] += 1

    return other_counts

# Fonction pour écrire les résultats dans un fichier
def write_results_to_file(results, output_file):
    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + '\n')

# Fonction pour ajouter les descriptions des catégories "other"
def describe_other_categories(other_counts):
    descriptions = []
    for category, count in other_counts.items():
        description = OTHER_DESCRIPTIONS.get(category, "Unknown category")
        descriptions.append(f"{category}: {count} ({description})")
    return descriptions

# Main
if __name__ == "__main__":
    # Configuration d'argparse pour les arguments
    parser = argparse.ArgumentParser(description="Analyze .tracking and output results.")
    parser.add_argument("tracking_file", help="Path to the .tracking file")
    parser.add_argument("output_file", help="Path to save the output results")

    args = parser.parse_args()

    # Validation que le fichier existe
    if not os.path.exists(args.tracking_file):
        print(f"Error: The file {args.tracking_file} does not exist.")
        exit(1)

    # Analyse des fichiers
    tracking_file_path = args.tracking_file
    output_file_path = args.output_file

    gene_counts, total_genes = analyze_tracking_file(tracking_file_path)
    other_types = analyze_other_genes(tracking_file_path)
    other_type_counts = count_other_types(tracking_file_path)

    # Ajouter des descriptions aux catégories "other"
    other_descriptions = describe_other_categories(other_type_counts)

    # Préparer les résultats à afficher et écrire dans le fichier
    results = []
    results.append(f"Gene counts by type: {gene_counts}")
    results.append(f"Total unique genes: {total_genes}")
    results.append(f"Unique match types in 'other': {other_types}")
    results.append(f"Counts for other types: {other_type_counts}")
    results.append("Descriptions for 'other' categories:")
    results.extend(other_descriptions)

    # Imprimer les résultats dans le terminal
    for result in results:
        print(result)

    # Écrire les résultats dans le fichier
    write_results_to_file(results, output_file_path)
    print(f"Results have been written to {output_file_path}")
