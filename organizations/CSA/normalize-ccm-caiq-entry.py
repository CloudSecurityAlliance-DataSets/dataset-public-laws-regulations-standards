#!/usr/bin/env python3.12

import pandas as pd
from pathlib import Path
import argparse
from functools import reduce


def find_header_row(df_raw, header_key):
    """
    Locate the row index in df_raw where header_key appears.
    """
    for idx, row in df_raw.iterrows():
        # Convert row values to stripped strings
        if header_key in row.fillna('').astype(str).str.strip().values:
            return idx
    raise ValueError(f"Header row with '{header_key}' not found in sheet")


def load_and_process_sheet(path, sheet_name, header_keys):
    """
    Load an Excel sheet and normalize:
      - Detect and flatten multi-row headers
      - Stop at 'End of Standard'
      - Forward-fill merged cells (including CAIQ spec)
      - Drop true-empty rows and visual separators
      - Prefix non-key columns with sheet name
    """
        # Read raw data without header
    df_raw = pd.read_excel(path, sheet_name=sheet_name, header=None)

    # Find the header row (containing the first key)
    header_idx = find_header_row(df_raw, header_keys[0])

    # Grab the row above header_idx for group labels (always prepend)
    if header_idx > 0:
        group_header = df_raw.iloc[header_idx - 1].fillna('').astype(str).str.strip().tolist()
    else:
        group_header = [''] * len(df_raw.iloc[header_idx])

        # Extract and flatten header row
    raw_row = df_raw.iloc[header_idx]
    raw_header = raw_row.fillna('').astype(str).str.strip().tolist()
    header = [f"{g} {r}".strip() for g, r in zip(group_header, raw_header)]

    # Ensure join key columns are named exactly for merging
    for idx, raw_col in enumerate(raw_header):
        for key in header_keys:
            if raw_col == key:
                header[idx] = key
                break

    # Build DataFrame starting right after the header row
    df = df_raw.iloc[header_idx + 1 :].reset_index(drop=True)
    df.columns = header
    df = df_raw.iloc[header_idx + 1 :].reset_index(drop=True)
    df.columns = header
    df = df_raw.iloc[header_idx + 1 :].reset_index(drop=True)
    df.columns = header

    # Stop at 'End of Standard' if present
    domain_col = header_keys[0]
    if 'End of Standard' in df[domain_col].astype(str).values:
        stop_idx = df[df[domain_col].astype(str) == 'End of Standard'].index[0]
        df = df.iloc[:stop_idx].reset_index(drop=True)

    # Forward-fill merged key columns
    df[header_keys] = df[header_keys].ffill()

    # Drop rows missing a Control ID
    control_id_col = header_keys[2]
    df = df[df[control_id_col].notna()].copy()

        # Drop rows that only have the key columns and no other data
    non_keys = [c for c in df.columns if c not in header_keys]
    if non_keys:
        # Treat empty strings as missing across the sheet
        df.replace('', pd.NA, inplace=True)
        df = df.dropna(subset=non_keys, how='all').reset_index(drop=True)

    # Prefix all non-key columns to avoid collisions
    rename_map = {col: f"{sheet_name}_{col}" for col in df.columns if col not in header_keys}
    df = df.rename(columns=rename_map)

    # For CAIQ, ensure the Control Specification propagates to every question
    if sheet_name == 'CAIQ':
        spec = 'CAIQ_Control Specification'
        if spec in df.columns:
            df[spec] = df[spec].ffill()

    return df


def main():
    parser = argparse.ArgumentParser(description="Normalize CSA CCM+CAIQ Excel to a single CSV")
    parser.add_argument('input', help='Path to CCM+CAIQ Excel file')
    parser.add_argument('-o', '--output', help='CSV output path; defaults to <input_stem>_normalized.csv')
    args = parser.parse_args()

    inp = Path(args.input)
    out = Path(args.output) if args.output else inp.with_name(inp.stem + '_normalized.csv')

    # Merge keys: must exactly match header text
    join_keys = ['Control Domain', 'Control Title', 'Control ID']

    # Sheets contributing control data
    control_sheets = [
        'CCM',
        'Implementation Guidelines',
        'Auditing Guidelines',
        'Scope Applicability (Mappings)',
    ]
    # Load and merge all control sheets
    dfs = [load_and_process_sheet(inp, s, join_keys) for s in control_sheets]
    df_controls = reduce(lambda a, b: pd.merge(a, b, on=join_keys, how='outer'), dfs)

    # Load CAIQ (questions)
    df_caiq = load_and_process_sheet(inp, 'CAIQ', join_keys)

        # One row per question, with control info repeated
    df_final = pd.merge(df_caiq, df_controls, on=join_keys, how='left')

        # Sort for consistent ordering
    df_controls = df_controls.sort_values(by=[join_keys[0], join_keys[2]])
    df_final = df_final.sort_values(by=[join_keys[0], 'CAIQ_Question ID'])

    # Write out two CSVs: CCM-only and CAIQ merged
    stem = inp.stem
    ccm_out = inp.with_name(f"{stem}_ccm_normalized.csv")
    caiq_out = inp.with_name(f"{stem}_caiq_normalized.csv")

    df_controls.to_csv(ccm_out, index=False)
    print(f"Written CCM-only CSV to: {ccm_out}")

    df_final.to_csv(caiq_out, index=False)
    print(f"Written CAIQ-normalized CSV to: {caiq_out}")

if __name__ == '__main__':
    main()

