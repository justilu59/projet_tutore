import re
import argparse

def extract_data(gffcompare_summary_file):
    data = {
        'missed_loci': None,
        'total_loci': None,
        'missed_exons': None,
        'total_exons': None,
        'missed_introns': None,
        'total_introns': None,
        'boundary_errors': None,
        'total_transcripts': None,
        'matching_transcripts': None,
    }

    with open(gffcompare_summary_file, 'r') as file:
        for line in file:
            # Ignore lines starting with #
            if line.startswith('#'):
                line = line.lstrip("#").strip()

            # Extract missed loci
            if 'Missed loci' in line:
                match = re.search(r'Missed loci:\s+(\d+)/(\d+)', line)
                if match:
                    data['missed_loci'] = int(match.group(1))
                    data['total_loci'] = int(match.group(2))
                    #print(f"Loci manquants: {data['missed_loci']} / {data['total_loci']}")  # Debug print

            # Extract missed exons
            if 'Missed exons' in line:
                match = re.search(r'Missed exons:\s+(\d+)/(\d+)', line)
                if match:
                    data['missed_exons'] = int(match.group(1))
                    data['total_exons'] = int(match.group(2))
                    #print(f"Exons manquants: {data['missed_exons']} / {data['total_exons']}")  # Debug print

            # Extract total and matching transcripts
            if 'Reference mRNAs' in line:
                match = re.search(r'Reference mRNAs\s*:\s*(\d+)', line)  # Adjusted regex to capture only the number
                if match:
                    data['total_transcripts'] = int(match.group(1))
                    #print(f"Transcrits total: {data['total_transcripts']}")  # Debug print
                else:
                    print(f"Could not extract Reference mRNAs from line: {line}")  # Debugging

            if 'Matching transcripts' in line:
                match = re.search(r'Matching transcripts:\s+(\d+)', line)
                if match:
                    data['matching_transcripts'] = int(match.group(1))
                    #print(f"Transcrits matchés: {data['matching_transcripts']}")  # Debug print
                
            # Extract boundary errors (from intron chain sensitivity)
            if 'Intron chain level' in line:
                match = re.search(r'Intron chain level:\s+(\d+.\d+)\s+\|\s+(\d+.\d+)', line)
                if match:
                    sensitivity = float(match.group(1))
                    data['boundary_errors'] = 100 - sensitivity
                    #print(f"Erreurs de bornes: {data['boundary_errors']}%")  # Debug print

    return data

def generate_report(data):
    report = {}

    # Calculate unsupported genes (missed loci)
    if data['missed_loci'] is not None and data['total_loci'] is not None:
        report['unsupported_genes'] = (data['missed_loci'] / data['total_loci']) * 100

    # Calculate missing exons
    if data['missed_exons'] is not None and data['total_exons'] is not None:
        report['missing_exons'] = (data['missed_exons'] / data['total_exons']) * 100

    # Calculate boundary errors
    if data['boundary_errors'] is not None:
        report['boundary_errors'] = data['boundary_errors']

    # Calculate missing transcripts
    if data['total_transcripts'] is not None and data['matching_transcripts'] is not None:
        missing_transcripts = data['total_transcripts'] - data['matching_transcripts']
        report['missing_transcripts'] = (missing_transcripts / data['total_transcripts']) * 100

    return report

def print_report(report):
    unsupported_genes = report.get('unsupported_genes', 'N/A')
    missing_exons = report.get('missing_exons', 'N/A')
    boundary_errors = report.get('boundary_errors', 'N/A')
    missing_transcripts = report.get('missing_transcripts', 'N/A')

    # Handle numeric values separately from "N/A"
    if isinstance(unsupported_genes, (int, float)):
        print(f"Gènes non-supportés (approximation basée sur les loci) : {unsupported_genes:.2f}%")
    else:
        print(f"Gènes non-supportés : {unsupported_genes}")

    if isinstance(missing_exons, (int, float)):
        print(f"Exons manquants : {missing_exons:.2f}%")
    else:
        print(f"Exons manquants : {missing_exons}")

    if isinstance(boundary_errors, (int, float)):
        print(f"Erreurs de bornes : {boundary_errors:.2f}%")
    else:
        print(f"Erreurs de bornes : {boundary_errors}")

    if isinstance(missing_transcripts, (int, float)):
        print(f"Transcrits manquants : {missing_transcripts:.2f}%")
    else:
        print(f"Transcrits manquants : {missing_transcripts}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Analyse un fichier GFFCompare summary")
    parser.add_argument("gffcompare_summary_file", type=str, help="Chemin vers le fichier summary de GFFCompare")
    args = parser.parse_args()

    # Extraction des données
    data = extract_data(args.gffcompare_summary_file)

    # Génération du rapport
    report = generate_report(data)

    # Affichage du rapport
    print_report(report)
#python script.py /path/to/comparison_output.stats
