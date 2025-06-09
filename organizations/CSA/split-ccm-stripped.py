#!/usr/bin/env python3.12
import os
import re
import argparse
import pandas as pd

def sanitize(text: str) -> str:
    """
    Replace any character that is not alphanumeric, dash or underscore with an underscore.
    """
    return re.sub(r'[^A-Za-z0-9_-]', '_', text)

def split_csv_by_control_domain(input_path: str):
    # Load the CSV
    df = pd.read_csv(input_path)
    if 'Control Domain' not in df.columns:
        raise KeyError("Column 'Control Domain' not found in input file")

    # Prepare base filename
    base_name, ext = os.path.splitext(os.path.basename(input_path))

    # Group and write
    for domain_value, group in df.groupby('Control Domain'):
        safe_domain = sanitize(str(domain_value))
        output_filename = f"{base_name}-{safe_domain}{ext}"
        group.to_csv(output_filename, index=False)
        print(f"Wrote {len(group)} rows → {output_filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Split a CSV into per-Control-Domain files (keeping headers)."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input CSV (e.g. CCMv4.0.13_Generated-at_2024-10-31_ccm_normalized_stripped.csv)"
    )
    args = parser.parse_args()
    split_csv_by_control_domain(args.input_file)

if __name__ == "__main__":
    main()

