#!/usr/bin/env python3
"""
Compare EU AI Act YAML and JSON files to ensure content equivalence.
"""

import yaml
import json
import argparse
from typing import Dict, List, Tuple

def load_yaml(filepath: str) -> dict:
    """Load YAML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_json(filepath: str) -> list:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def flatten_yaml_to_articles(yaml_data: dict) -> List[Dict]:
    """Convert nested YAML structure to flat list of articles."""
    articles = []

    for chapter in yaml_data.get('chapters', []):
        chapter_num = chapter.get('chapter', '')
        chapter_name = chapter.get('name', '')

        for section in chapter.get('sections', []):
            section_num = section.get('section', '')
            section_name = section.get('name', '')

            for article in section.get('articles', []):
                articles.append({
                    'CHAPTER': chapter_num,
                    'CHAPTER_NAME': chapter_name,
                    'SECTION': section_num,
                    'SECTION_NAME': section_name,
                    'ARTICLE': article.get('number', ''),
                    'ARTICLE_NAME': article.get('name', ''),
                    'ARTICLE_CONTENT': article.get('content', '')
                })

    return articles

def normalize_text(text: str) -> str:
    """Normalize text for comparison by removing extra whitespace."""
    return ' '.join(text.split())

def compare_articles(yaml_articles: List[Dict], json_articles: List[Dict]) -> Tuple[bool, List[str]]:
    """Compare flattened article lists for equivalence."""
    differences = []

    # Check counts
    if len(yaml_articles) != len(json_articles):
        differences.append(f"Article count mismatch: YAML has {len(yaml_articles)}, JSON has {len(json_articles)}")

    # Compare each article
    max_len = max(len(yaml_articles), len(json_articles))

    for i in range(max_len):
        yaml_art = yaml_articles[i] if i < len(yaml_articles) else None
        json_art = json_articles[i] if i < len(json_articles) else None

        if yaml_art is None:
            differences.append(f"Article {i+1}: Missing in YAML")
            continue
        if json_art is None:
            differences.append(f"Article {i+1}: Missing in JSON")
            continue

        # Compare each field
        for field in ['CHAPTER', 'CHAPTER_NAME', 'SECTION', 'SECTION_NAME', 'ARTICLE', 'ARTICLE_NAME']:
            yaml_val = yaml_art.get(field, '')
            json_val = json_art.get(field, '')

            if yaml_val != json_val:
                differences.append(
                    f"Article {yaml_art.get('ARTICLE', i+1)} - {field} mismatch:\n"
                    f"  YAML: '{yaml_val}'\n"
                    f"  JSON: '{json_val}'"
                )

        # Compare content (normalized)
        yaml_content = normalize_text(yaml_art.get('ARTICLE_CONTENT', ''))
        json_content = normalize_text(json_art.get('ARTICLE_CONTENT', ''))

        if yaml_content != json_content:
            differences.append(
                f"Article {yaml_art.get('ARTICLE', i+1)} ({yaml_art.get('ARTICLE_NAME', '')}) - CONTENT mismatch:\n"
                f"  YAML length: {len(yaml_content)} chars\n"
                f"  JSON length: {len(json_content)} chars"
            )

            # Show first difference location
            for idx, (c1, c2) in enumerate(zip(yaml_content, json_content)):
                if c1 != c2:
                    start = max(0, idx - 50)
                    end = min(len(yaml_content), idx + 50)
                    differences.append(
                        f"  First diff at char {idx}:\n"
                        f"    YAML: ...{yaml_content[start:end]}...\n"
                        f"    JSON: ...{json_content[start:end]}..."
                    )
                    break

    return len(differences) == 0, differences

def main():
    parser = argparse.ArgumentParser(
        description='Compare EU AI Act YAML and JSON files to ensure content equivalence.'
    )
    parser.add_argument(
        '--yaml',
        required=True,
        help='Path to the YAML file'
    )
    parser.add_argument(
        '--json',
        required=True,
        help='Path to the JSON file'
    )

    args = parser.parse_args()

    print(f"Loading files...")
    print(f"  YAML: {args.yaml}")
    print(f"  JSON: {args.json}")

    yaml_data = load_yaml(args.yaml)
    json_data = load_json(args.json)

    print("Flattening YAML structure...")
    yaml_articles = flatten_yaml_to_articles(yaml_data)

    print(f"YAML: {len(yaml_articles)} articles")
    print(f"JSON: {len(json_data)} articles")

    print("\nComparing content...")
    is_equivalent, differences = compare_articles(yaml_articles, json_data)

    if is_equivalent:
        print("\n✅ SUCCESS: Files are equivalent!")
    else:
        print(f"\n❌ DIFFERENCES FOUND: {len(differences)} issues\n")
        for diff in differences[:20]:  # Show first 20 differences
            print(diff)
            print("-" * 80)

        if len(differences) > 20:
            print(f"\n... and {len(differences) - 20} more differences")

    return 0 if is_equivalent else 1

if __name__ == '__main__':
    exit(main())
