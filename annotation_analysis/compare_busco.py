#!/usr/bin/env python3

import pandas as pd
import argparse

def main():
    # Configurer l'analyse des arguments
    parser = argparse.ArgumentParser(description="Compare two BUSCO full_table.tsv files and identifies differences in status.")
    parser.add_argument("--gca", required=True, help="Path to the GCA full_table.tsv file")
    parser.add_argument("--gcf", required=True, help="Path to the GCF full_table.tsv file")
    parser.add_argument("--output", default="busco_differences.csv", help="Path to save the output CSV file (default: busco_differences.csv)")
    args = parser.parse_args()

    # Charger les fichiers BUSCO
    gca_busco = pd.read_csv(args.gca, sep="\t", comment="#", header=None,
                            names=["BUSCO_group", "Status", "Sequence", "Start", "End", "Score", "Length"])
    gcf_busco = pd.read_csv(args.gcf, sep="\t", comment="#", header=None,
                            names=["BUSCO_group", "Status", "Sequence", "Start", "End", "Score", "Length"])

    # Comparer les BUSCO IDs
    comparison = pd.merge(gca_busco, gcf_busco, on="BUSCO_group", suffixes=("_GCA", "_GCF"))

    # Identifier les différences dans le statut
    diff_status = comparison[comparison["Status_GCA"] != comparison["Status_GCF"]]

    # Exporter les résultats
    diff_status.to_csv(args.output, index=False)
    print(f"Differences saved to {args.output}")

if __name__ == "__main__":
    main()
