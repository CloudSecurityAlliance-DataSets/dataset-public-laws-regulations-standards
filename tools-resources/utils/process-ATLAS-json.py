#!/usr/bin/env python3

import json
import os

# Load the JSON file
with open('ATLAS.json', 'r') as file:
    data = json.load(file)

# Create a directory to store the individual files
output_dir = 'output_files'
os.makedirs(output_dir, exist_ok=True)

# Define the keys that contain lists of items with unique IDs
list_keys = ['tactics', 'techniques', 'another_list_key']

# Iterate through each matrix in the 'matrices' list
for matrix in data.get('matrices', []):
    for key in list_keys:
        if key in matrix:
            for item in matrix[key]:
                item_id = item.get('id')
                if item_id:
                    # Define the filename based on the item ID
                    filename = f"ATLAS-{item_id}.json"
                    filepath = os.path.join(output_dir, filename)
                    
                    # Write the item to the individual file
                    with open(filepath, 'w') as outfile:
                        json.dump(item, outfile, indent=4)

print("Individual files have been created successfully.")

