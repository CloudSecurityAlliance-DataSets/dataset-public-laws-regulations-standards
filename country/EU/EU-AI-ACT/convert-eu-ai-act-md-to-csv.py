#!/usr/bin/env python3

import argparse
import re
import csv

def clean_quotes_and_dashes(text):
    """Replace non-ASCII quotes and dashes with normal ASCII quotes and dashes."""
    replacements = {
        'â€˜': '"',  # Opening single quote
        'â€™': '"',  # Closing single quote
        'â€œ': '"',  # Opening double quote
        'â€�': '"',  # Closing double quote
        '‘': '"',    # Curly single quote
        '’': '"',    # Curly single quote
        '“': '"',    # Curly double quote
        '”': '"',    # Curly double quote
        '–': '-',    # En dash
        '—': '-',    # Em dash
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

def process_markdown_with_escaping_quotes_and_dashes(input_file, output_file):
    # Regular expressions to match chapters, sections, and articles
    chapter_regex = r'^CHAPTER ([IVXLCDM]+)$'
    section_regex = r'^SECTION (\d+)$'
    article_regex = r'^Article (\d+)$'
    blank_line_regex = r'^\s*$'

    # Variables to hold the current chapter, section, and article details
    current_chapter = ""
    current_chapter_name = ""
    current_section = ""
    current_section_name = ""
    current_article = ""
    current_article_name = ""
    current_article_content = []

    data = []

    # Process the markdown file line by line
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Match Chapter
            chapter_match = re.match(chapter_regex, line)
            if chapter_match:
                if current_article:
                    # Append the last article data
                    article_text = clean_quotes_and_dashes("\n".join(current_article_content).replace('"', '""'))
                    data.append([current_chapter, current_chapter_name, current_section, current_section_name,
                                 current_article, current_article_name, article_text])
                
                # Reset section and article details when a new chapter is found
                current_article = ""
                current_article_name = ""
                current_article_content = []
                current_section = ""
                current_section_name = ""

                current_chapter = chapter_match.group(1)
                current_chapter_name = lines[i + 2].strip()  # Skip a blank line and get the chapter name
                i += 3
                continue

            # Match Section
            section_match = re.match(section_regex, line)
            if section_match:
                if current_article:
                    # Append the last article data
                    article_text = clean_quotes_and_dashes("\n".join(current_article_content).replace('"', '""'))
                    data.append([current_chapter, current_chapter_name, current_section, current_section_name,
                                 current_article, current_article_name, article_text])
                
                # Reset article details when a new section is found
                current_article = ""
                current_article_name = ""
                current_article_content = []

                current_section = section_match.group(1)
                current_section_name = lines[i + 2].strip()  # Skip a blank line and get the section name
                i += 3
                continue

            # Match Article
            article_match = re.match(article_regex, line)
            if article_match:
                if current_article:
                    # Append the last article data
                    article_text = clean_quotes_and_dashes("\n".join(current_article_content).replace('"', '""'))
                    data.append([current_chapter, current_chapter_name, current_section, current_section_name,
                                 current_article, current_article_name, article_text])
                    current_article_content = []

                current_article = article_match.group(1)
                current_article_name = lines[i + 2].strip()  # Skip a blank line and get the article name
                i += 3
                continue

            # Append content to the current article
            if current_article and not re.match(blank_line_regex, line):
                current_article_content.append(line)

            i += 1

    # Add the last article to the data
    if current_article:
        article_text = clean_quotes_and_dashes("\n".join(current_article_content).replace('"', '""'))
        data.append([current_chapter, current_chapter_name, current_section, current_section_name,
                     current_article, current_article_name, article_text])

    # Write data to CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CHAPTER', 'CHAPTER_NAME', 'SECTION', 'SECTION_NAME', 'ARTICLE', 'ARTICLE_NAME', 'ARTICLE_CONTENT'])
        writer.writerows(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a markdown file of the EU AI Act and output a CSV file.")
    parser.add_argument('--input', type=str, required=True, help="Input markdown file path")
    parser.add_argument('--output', type=str, required=True, help="Output CSV file path")

    args = parser.parse_args()

    process_markdown_with_escaping_quotes_and_dashes(args.input, args.output)

    
