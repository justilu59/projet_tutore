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
def count_unsupported_genes(tracking_file):
    unsupported_genes = set()

    with open(tracking_file, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            gene_info = columns[1]
            match_type = columns[3]

            if match_type == 'u':
                unsupported_genes.add(gene_info)

    return len(unsupported_genes)

def generate_report(data, unsupported_genes_count):
    report = {}

    # Calculate unsupported genes (missed loci)
    if data['missed_loci'] is not None and data['total_loci'] is not None:
        report['unsupported_genes_count'] = data['missed_loci']
        report['total_loci'] = data['total_loci']
        report['unsupported_genes_percent'] = (data['missed_loci'] / data['total_loci']) * 100
        
    # Calculate missing exons
    if data['missed_exons'] is not None and data['total_exons'] is not None:
        report['missing_exons_count'] = data['missed_exons']
        report['total_exons'] = data['total_exons']
        report['missing_exons_percent'] = (data['missed_exons'] / data['total_exons']) * 100


    # Calculate boundary errors
    if data['boundary_errors'] is not None:
        report['boundary_errors'] = data['boundary_errors']

    # Calculate missing transcripts
    if data['total_transcripts'] is not None and data['matching_transcripts'] is not None:
        missing_transcripts = data['total_transcripts'] - data['matching_transcripts']
        report['missing_transcripts_count'] = missing_transcripts
        report['total_transcripts'] = data['total_transcripts']
        report['missing_transcripts_percent'] = (missing_transcripts / data['total_transcripts']) * 100
    
    report['unsupported_genes_from_tracking'] = unsupported_genes_count
    return report

def print_report(report):
    unsupported_genes_count = report.get('unsupported_genes_count', 'N/A')
    unsupported_genes_percent = report.get('unsupported_genes_percent', 'N/A')
    missing_exons_count = report.get('missing_exons_count', 'N/A')
    missing_exons_percent = report.get('missing_exons_percent', 'N/A')
    boundary_errors = report.get('boundary_errors', 'N/A')
    missing_transcripts_count = report.get('missing_transcripts_count', 'N/A')
    missing_transcripts_percent = report.get('missing_transcripts_percent', 'N/A')


    print("Rapport d'alignement des transcrits:")
    if isinstance(unsupported_genes_count, int):
        print(f"Gènes non-supportés (approximés sur les loci) : {unsupported_genes_count} sur {report['total_loci']} ({unsupported_genes_percent:.2f}%)")
    else:
        print(f"Gènes non-supportés (approximés sur les loci) : {unsupported_genes_count}")
    print(f"Nombre total de gènes non supportés (fichier .tracking) : {report['unsupported_genes_from_tracking']}")
    if isinstance(missing_exons_count, int):
        print(f"Exons manquants : {missing_exons_count} sur {report['total_exons']} ({missing_exons_percent:.2f}%)")
    else:
        print(f"Exons manquants : {missing_exons_count}")

    if isinstance(boundary_errors, (int, float)):
        print(f"Erreurs de bornes : {boundary_errors:.2f}%")
    else:
        print(f"Erreurs de bornes : {boundary_errors}")

    if isinstance(missing_transcripts_count, int):
        print(f"Transcrits manquants : {missing_transcripts_count} sur {report['total_transcripts']} ({missing_transcripts_percent:.2f}%)")
    else:
        print(f"Transcrits manquants : {missing_transcripts_count}")

def write_report_to_file(report, output_file):
    with open(output_file, 'w') as f:
        f.write("Rapport d'alignement des transcrits:\n")
        if 'unsupported_genes_count' in report:
            f.write(f"Gènes non-supportés (approximation basée sur les loci) : {report['unsupported_genes_count']} sur {report['total_loci']} ({report['unsupported_genes_percent']:.2f}%)\n")
        f.write(f"Nombre total de gènes non supportés (fichier .tracking) : {report['unsupported_genes_from_tracking']}\n")
        if 'missing_exons_count' in report:
            f.write(f"Exons manquants : {report['missing_exons_count']} sur {report['total_exons']} ({report['missing_exons_percent']:.2f}%)\n")
        if 'boundary_errors' in report:
            f.write(f"Erreurs de bornes : {report['boundary_errors']:.2f}%\n")
        if 'missing_transcripts_count' in report:
            f.write(f"Transcrits manquants : {report['missing_transcripts_count']} sur {report['total_transcripts']} ({report['missing_transcripts_percent']:.2f}%)\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate transcript alignment report from gffcompare summary and .tracking files.")
    parser.add_argument("gffcompare_summary_file", help="Path to the GFFCompare summary (.stats) file.")
    parser.add_argument("tracking_file", help="Path to the .tracking file.")
    parser.add_argument("output_file", help="Path to save the generated report.")

    args = parser.parse_args()

    data = extract_data(args.gffcompare_summary_file)
    unsupported_genes_count = count_unsupported_genes(args.tracking_file)

    report = generate_report(data, unsupported_genes_count)

    write_report_to_file(report, args.output_file)
    print_report(report)
    print(f"Report has been written to {args.output_file}")
#python report_annotation.py /path/to/comparison_output.stats /path/to/comparison_output.tracking /path/to/output_report.txt
#python report_annotation.py annotation_gcf/T_septentrionalis/comparison_output.s
