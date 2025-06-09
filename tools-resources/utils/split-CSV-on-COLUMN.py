#!/usr/bin/env python3

import csv
import os
import argparse

def split_csv_by_column(input_file, column_index=0):
    # Extract the filename without extension for output prefix
    output_prefix = os.path.splitext(os.path.basename(input_file))[0]

    # Create a dictionary to hold file handles and writers for each group
    group_files = {}

    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read the header row

            for row in reader:
                if len(row) <= column_index:
                    continue  # Skip rows that don't have enough columns

                group = row[column_index].strip()

                # Ensure a valid filename
                sanitized_group = group.replace(" ", "_").replace("/", "-")
                output_file = f"{output_prefix}-{sanitized_group}.csv"

                if sanitized_group not in group_files:
                    outfile = open(output_file, "w", encoding="utf-8", newline="")
                    writer = csv.writer(outfile)
                    writer.writerow(header)  # Write the header row
                    group_files[sanitized_group] = (outfile, writer)

                # Write the current row to the appropriate file
                group_files[sanitized_group][1].writerow(row)
    
    finally:
        # Close all file handles
        for outfile, _ in group_files.values():
            outfile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a CSV file into smaller files based on a specific column.")
    parser.add_argument("--input", required=True, help="Input CSV file.")
    parser.add_argument("--column-index", type=int, default=0, help="Index of the column to split on (default: 0).")

    args = parser.parse_args()

    split_csv_by_column(args.input, args.column_index)

