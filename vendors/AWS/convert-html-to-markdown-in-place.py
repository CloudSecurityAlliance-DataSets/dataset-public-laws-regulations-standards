#!/usr/bin/env python3

import os
import argparse
from markdownify import markdownify as md

def convert_html_to_md(html_content):
    # Customize markdownify options here
    return md(html_content, heading_style="ATX")  # Example: ATX heading style

def process_directory(input_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".html"):
                input_file = os.path.join(root, file)

                # Read the HTML file
                with open(input_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()

                # Convert HTML to Markdown
                markdown_content = convert_html_to_md(html_content)

                # Create the corresponding markdown file path
                output_file = os.path.join(root, file.replace(".html", ".md"))

                # Write the markdown content to the file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                print(f"Converted {input_file} to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert HTML files to Markdown")
    parser.add_argument("input_directory", help="Directory containing HTML files")

    args = parser.parse_args()
    input_directory = args.input_directory

    if os.path.exists(input_directory):
        process_directory(input_directory)
    else:
        print(f"Error: Directory {input_directory} does not exist")
