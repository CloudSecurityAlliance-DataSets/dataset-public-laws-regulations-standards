#!/usr/bin/env python3
"""
Convert EU AI Act JSON to hierarchical YAML format.

This script converts a flat JSON array of articles into a hierarchical YAML structure
organized by chapters and sections, while preserving empty section fields.
"""

import argparse
import json
import yaml
from collections import defaultdict


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert EU AI Act JSON to hierarchical YAML format'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input JSON file path'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output YAML file path'
    )
    return parser.parse_args()


def build_hierarchical_structure(json_data):
    """
    Convert flat JSON array to hierarchical structure organized by chapters and sections.

    Args:
        json_data: List of article dictionaries

    Returns:
        Dictionary with hierarchical structure
    """
    chapters = defaultdict(lambda: {
        'name': '',
        'sections': defaultdict(lambda: {
            'name': '',
            'articles': []
        })
    })

    for article in json_data:
        chapter_num = article['CHAPTER']
        chapter_name = article['CHAPTER_NAME']
        section_num = article['SECTION']  # Preserve empty strings
        section_name = article['SECTION_NAME']  # Preserve empty strings

        # Set chapter name
        chapters[chapter_num]['name'] = chapter_name

        # Set section name (preserving empty strings)
        chapters[chapter_num]['sections'][section_num]['name'] = section_name

        # Add article to section
        chapters[chapter_num]['sections'][section_num]['articles'].append({
            'number': article['ARTICLE'],
            'name': article['ARTICLE_NAME'],
            'content': article['ARTICLE_CONTENT']
        })

    # Convert defaultdicts to regular dicts and build final structure
    result = {'chapters': []}

    for chapter_num in sorted(chapters.keys(), key=lambda x: roman_to_int(x) if x else 0):
        chapter_data = {
            'chapter': chapter_num,
            'name': chapters[chapter_num]['name'],
            'sections': []
        }

        for section_num in sorted(chapters[chapter_num]['sections'].keys(),
                                  key=lambda x: int(x) if x and x.isdigit() else -1):
            section_data = {
                'section': section_num,
                'name': chapters[chapter_num]['sections'][section_num]['name'],
                'articles': chapters[chapter_num]['sections'][section_num]['articles']
            }
            chapter_data['sections'].append(section_data)

        result['chapters'].append(chapter_data)

    return result


def roman_to_int(s):
    """Convert Roman numeral to integer for sorting."""
    if not s:
        return 0

    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    total = 0
    prev_value = 0

    for char in reversed(s):
        value = roman_values.get(char, 0)
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total


def main():
    """Main execution function."""
    args = parse_arguments()

    # Read JSON file
    print(f"Reading JSON from: {args.input}")
    with open(args.input, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    print(f"Found {len(json_data)} articles")

    # Build hierarchical structure
    print("Converting to hierarchical structure...")
    hierarchical_data = build_hierarchical_structure(json_data)

    print(f"Organized into {len(hierarchical_data['chapters'])} chapters")

    # Write YAML file
    print(f"Writing YAML to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as f:
        yaml.dump(
            hierarchical_data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=100,
            indent=2
        )

    print("Conversion complete!")


if __name__ == '__main__':
    main()
