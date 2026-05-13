#!/usr/bin/env python3
"""
HTML to Markdown converter for CWE documents
Provides better conversion than basic regex approach
"""

import sys
import re
import argparse
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

class HTMLToMarkdownConverter(HTMLParser):
    def __init__(self, base_url=""):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
        self.current_tag = None
        self.list_stack = []
        self.table_mode = False
        self.table_headers = []
        self.table_rows = []
        self.current_table_row = []
        self.base_url = base_url
        self.skip_content = False
        self.heading_level = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Skip script, style, and nav content
        if tag in ['script', 'style', 'nav', 'header', 'footer']:
            self.skip_content = True
            return
            
        if self.skip_content:
            return
            
        if tag == 'h1':
            self.text.append('\n# ')
            self.heading_level = 1
        elif tag == 'h2':
            self.text.append('\n## ')
            self.heading_level = 2
        elif tag == 'h3':
            self.text.append('\n### ')
            self.heading_level = 3
        elif tag == 'h4':
            self.text.append('\n#### ')
            self.heading_level = 4
        elif tag == 'h5':
            self.text.append('\n##### ')
            self.heading_level = 5
        elif tag == 'h6':
            self.text.append('\n###### ')
            self.heading_level = 6
        elif tag == 'p':
            self.text.append('\n\n')
        elif tag == 'br':
            self.text.append('  \n')
        elif tag == 'strong' or tag == 'b':
            self.text.append('**')
        elif tag == 'em' or tag == 'i':
            self.text.append('*')
        elif tag == 'code':
            self.text.append('`')
        elif tag == 'pre':
            self.text.append('\n```\n')
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            if href:
                if self.base_url and not href.startswith(('http://', 'https://', 'mailto:')):
                    href = urljoin(self.base_url, href)
                self.text.append('[')
            else:
                self.text.append('[')
        elif tag == 'ul':
            self.list_stack.append('ul')
            self.text.append('\n')
        elif tag == 'ol':
            self.list_stack.append('ol')
            self.text.append('\n')
        elif tag == 'li':
            if self.list_stack:
                indent = '  ' * (len(self.list_stack) - 1)
                if self.list_stack[-1] == 'ul':
                    self.text.append(f'{indent}- ')
                else:  # ol
                    self.text.append(f'{indent}1. ')
        elif tag == 'blockquote':
            self.text.append('\n> ')
        elif tag == 'hr':
            self.text.append('\n---\n')
        elif tag == 'table':
            self.table_mode = True
            self.table_headers = []
            self.table_rows = []
        elif tag == 'tr' and self.table_mode:
            self.current_table_row = []
        elif tag == 'div':
            self.text.append('\n')
            
        self.current_tag = tag
        
    def handle_endtag(self, tag):
        if tag in ['script', 'style', 'nav', 'header', 'footer']:
            self.skip_content = False
            return
            
        if self.skip_content:
            return
            
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.text.append('\n')
            self.heading_level = 0
        elif tag == 'p':
            self.text.append('\n')
        elif tag == 'strong' or tag == 'b':
            self.text.append('**')
        elif tag == 'em' or tag == 'i':
            self.text.append('*')
        elif tag == 'code':
            self.text.append('`')
        elif tag == 'pre':
            self.text.append('\n```\n')
        elif tag == 'a':
            # This is simplified - ideally we'd store the href
            self.text.append(']()')
        elif tag == 'ul' or tag == 'ol':
            if self.list_stack:
                self.list_stack.pop()
            self.text.append('\n')
        elif tag == 'li':
            self.text.append('\n')
        elif tag == 'blockquote':
            self.text.append('\n')
        elif tag == 'table':
            self.table_mode = False
            if self.table_headers:
                # Add table headers
                self.text.append('\n| ')
                self.text.append(' | '.join(self.table_headers))
                self.text.append(' |\n|')
                self.text.append('|'.join(['---' for _ in self.table_headers]))
                self.text.append('|\n')
                
                # Add table rows
                for row in self.table_rows:
                    self.text.append('| ')
                    self.text.append(' | '.join(row))
                    self.text.append(' |\n')
                self.text.append('\n')
        elif tag == 'tr' and self.table_mode:
            if not self.table_headers and self.current_table_row:
                self.table_headers = self.current_table_row[:]
            else:
                self.table_rows.append(self.current_table_row[:])
            self.current_table_row = []
            
        self.current_tag = None
        
    def handle_data(self, data):
        if self.skip_content:
            return
            
        # Clean up whitespace but preserve intentional spacing
        if self.current_tag in ['pre', 'code']:
            self.text.append(data)
        elif self.table_mode and self.current_tag in ['td', 'th']:
            self.current_table_row.append(data.strip())
        else:
            # Normalize whitespace but preserve paragraph breaks
            cleaned_data = re.sub(r'\s+', ' ', data.strip())
            if cleaned_data:
                self.text.append(cleaned_data)
                
    def get_markdown(self):
        result = ''.join(self.text)
        
        # Clean up multiple newlines
        result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)
        
        # Clean up spaces before newlines
        result = re.sub(r' +\n', '\n', result)
        
        # Clean up multiple spaces
        result = re.sub(r'  +', ' ', result)
        
        return result.strip()

def convert_html_to_markdown(html_content, base_url=""):
    """Convert HTML content to Markdown"""
    converter = HTMLToMarkdownConverter(base_url)
    converter.feed(html_content)
    return converter.get_markdown()

def main():
    parser = argparse.ArgumentParser(description='Convert HTML to Markdown')
    parser.add_argument('input_file', help='Input HTML file')
    parser.add_argument('output_file', help='Output Markdown file')
    parser.add_argument('--base-url', default='', help='Base URL for relative links')
    parser.add_argument('--title', help='Document title to add as header')
    
    args = parser.parse_args()
    
    try:
        # Read HTML file
        with open(args.input_file, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        
        # Convert to markdown
        markdown_content = convert_html_to_markdown(html_content, args.base_url)
        
        # Add title if provided
        if args.title:
            markdown_content = f"# {args.title}\n\n{markdown_content}"
        elif not markdown_content.startswith('#'):
            # Add default title based on filename
            title = Path(args.input_file).stem.replace('_', ' ').replace('-', ' ').title()
            markdown_content = f"# {title}\n\n{markdown_content}"
        
        # Write markdown file
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✓ Converted {args.input_file} to {args.output_file}")
        
    except Exception as e:
        print(f"✗ Error converting {args.input_file}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()