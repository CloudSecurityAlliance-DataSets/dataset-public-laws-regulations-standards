#!/usr/bin/env python3

import argparse
import html2text
from bs4 import BeautifulSoup
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def convert_html_to_markdown(input_file: str, output_file: str, ignore_links: bool = False, skip_images: bool = False):
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            logging.error(f"Input file '{input_file}' does not exist.")
            return

        # Read the HTML file
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Convert HTML to Markdown using html2text
        h = html2text.HTML2Text()
        h.ignore_links = ignore_links
        h.skip_internal_links = False
        h.ignore_images = skip_images  # Skip images if specified
        markdown_text = h.handle(str(soup))

        # Write the Markdown to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_text)

        logging.info(f"Converted '{input_file}' to '{output_file}' in Markdown format.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert an HTML file to Markdown format.")
    parser.add_argument('--input', type=str, required=True, help="Path to the input HTML file.")
    parser.add_argument('--output', type=str, required=True, help="Path to save the output Markdown file.")
    parser.add_argument('--ignore-links', action='store_true', help="Ignore converting links in the HTML.")
    parser.add_argument('--skip-images', action='store_true', help="Skip converting images in the HTML.")

    args = parser.parse_args()

    # Convert HTML to Markdown
    convert_html_to_markdown(args.input, args.output, args.ignore_links, args.skip_images)

if __name__ == "__main__":
    main()

    
