#!/usr/bin/env python3

import json
import os

# Load the large JSON file
with open('CWE-Research-Concepts-1000.json', 'r') as file:
    data = json.load(file)

# Create a directory to store the individual files
output_dir = 'output_files'
os.makedirs(output_dir, exist_ok=True)

# Iterate through each item in the JSON data
for item in data:
    cwe_id = item.get("CWE-ID")
    if cwe_id:
        # Define the filename based on CWE-ID
        filename = f"CWE-{cwe_id}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Write the item to the individual file
        with open(filepath, 'w') as outfile:
            json.dump(item, outfile, indent=2)

print("Individual files have been created successfully.")

