#!/usr/bin/env python3

import pandas as pd
import json
import argparse
import sys
from pathlib import Path

def convert_csv_to_json(csv_file_path, output_file_path):
    # Validate input file exists
    if not Path(csv_file_path).is_file():
        raise FileNotFoundError(f"Input file not found: {csv_file_path}")
    
    # Read the CSV file without headers first to get the groupings
    df_groups = pd.read_csv(csv_file_path, nrows=1, header=None)
    
    # Read the CSV file again, using the second row as headers
    df = pd.read_csv(csv_file_path, skiprows=[0])
    
    # Get the column groups from the first row
    column_groups = df_groups.iloc[0].tolist()
    
    # Create a mapping of columns to their groups
    column_to_group = {}
    for idx, group in enumerate(column_groups):
        if pd.notna(group):
            column_to_group[df.columns[idx]] = group
    
    # Initialize the list to store all JSON objects
    json_data = []
    
    # Process each row
    for _, row in df.iterrows():
        json_obj = {}
        
        # First handle the first 5 columns that stand alone
        standalone_columns = list(df.columns[:5])
        for col in standalone_columns:
            json_obj[col] = row[col] if pd.notna(row[col]) else None
        
        # Now handle the grouped columns
        current_group = None
        grouped_data = {}
        
        for col in df.columns[5:]:
            group = column_to_group.get(col)
            if group and pd.notna(group):
                if group != current_group:
                    current_group = group
                    if current_group not in grouped_data:
                        grouped_data[current_group] = {}
                
                # Add the value to the appropriate group
                value = row[col] if pd.notna(row[col]) else None
                if value is not None:
                    # Clean the column name by removing the group prefix if it exists
                    clean_col = col.replace(f"{group} ", "").strip()
                    grouped_data[current_group][clean_col] = value
        
        # Add grouped data to the main JSON object
        json_obj.update(grouped_data)
        
        # Add this object to the main list
        json_data.append(json_obj)
    
    # Create output directory if it doesn't exist
    output_path = Path(output_file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the JSON to a file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    
    return json_data

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Convert AICM CSV file to JSON with grouped columns.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add arguments
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Path to the input CSV file'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Path for the output JSON file'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Convert the file
        json_data = convert_csv_to_json(args.input, args.output)
        print(f"Successfully converted CSV to JSON. Output saved to {args.output}")
        print(f"Processed {len(json_data)} records")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
