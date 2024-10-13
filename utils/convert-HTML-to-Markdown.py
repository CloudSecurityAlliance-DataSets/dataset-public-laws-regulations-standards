#!/usr/bin/env python3

import argparse
import html2text
from bs4 import BeautifulSoup

def convert_html_to_markdown(input_file: str, output_file: str):
    # Read the HTML file
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Convert HTML to Markdown using html2text
    h = html2text.HTML2Text()
    h.ignore_links = False  # Set to True if you want to skip converting links
    markdown_text = h.handle(str(soup))
    
    # Write the Markdown to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_text)
    
    print(f"Converted {input_file} to {output_file} in Markdown format.")

def main():
    parser = argparse.ArgumentParser(description="Convert HTML file to Markdown.")
    parser.add_argument('input_file', type=str, help="Path to the HTML file.")
    parser.add_argument('output_file', type=str, help="Path to save the output Markdown file.")
    
    args = parser.parse_args()
    
    # Convert HTML to Markdown
    convert_html_to_markdown(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
