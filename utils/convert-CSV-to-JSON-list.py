#!/usr/bin/env python3

import csv
import json
import argparse

def csv_to_json(csv_file_path, json_file_path):
    data = []

    # Open the CSV file, handle BOM if present
    with open(csv_file_path, mode='r', newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Just append the row as-is, let json.dump handle line returns
            data.append(row)

    # Write the JSON file with proper encoding and formatting
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Convert CSV file to JSON format with Unicode, BOM, and line return handling.')
    parser.add_argument('--input', required=True, help='Path to the input CSV file.')
    parser.add_argument('--output', required=True, help='Path to the output JSON file.')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert CSV to JSON
    csv_to_json(args.input, args.output)

if __name__ == "__main__":
    main()

    
