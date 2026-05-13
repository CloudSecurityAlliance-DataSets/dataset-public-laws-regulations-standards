#!/usr/bin/env python3

import os
import re
import argparse
from markdownify import markdownify as md

def convert_html_to_md(html_content):
    # Customize markdownify options here
    return md(html_content, heading_style="ATX")  # Example: ATX heading style

def strip_content_before_h1_and_after_div(html_content):
    # Use regex to find the first <h1> tag and ignore everything before it
    h1_match = re.search(r'<h1.*?>', html_content, re.IGNORECASE)
    if h1_match:
        # Start from the position of the <h1> tag
        html_content = html_content[h1_match.start():]
    else:
        # No <h1> found, return the whole content
        print("Warning: No <h1> tag found, processing the whole file.")
    
    # Use regex to find the <div class="devsite-content-data"> tag and ignore everything after it
    div_match = re.search(r'<div class="devsite-content-data".*?>', html_content, re.IGNORECASE)
    if div_match:
        # Trim the content up to the start of the div
        html_content = html_content[:div_match.start()]

    return html_content

def process_directory(input_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            input_file = os.path.join(root, file)

            try:
                # Try reading the file with UTF-8 encoding
                with open(input_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            except UnicodeDecodeError:
                # If there's an error, try reading with 'latin-1' encoding as fallback
                print(f"Warning: {input_file} contains invalid UTF-8 characters, attempting fallback encoding.")
                with open(input_file, 'r', encoding='latin-1') as f:
                    html_content = f.read()

            # Ignore content before the first <h1> tag and after <div class="devsite-content-data">
            stripped_content = strip_content_before_h1_and_after_div(html_content)

            # Convert the remaining content to Markdown
            markdown_content = convert_html_to_md(stripped_content)

            # Create the corresponding markdown file path
            output_file = os.path.join(root, file + ".md")

            # Write the markdown content to the file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            print(f"Converted {input_file} to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert files to Markdown")
    parser.add_argument("input_directory", help="Directory containing files")

    args = parser.parse_args()
    input_directory = args.input_directory

    if os.path.exists(input_directory):
        process_directory(input_directory)
    else:
        print(f"Error: Directory {input_directory} does not exist")
