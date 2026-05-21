#!/usr/bin/env python3
"""Extract the central AWS Glossary Reference into structured CSV/JSON.

Source: https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.html
License: AWS docs (generally CC-BY-SA-4.0 for documentation — verify per page).

Page structure: 25 <dl> elements (alphabet sections A-Z plus 'Numbers');
each <dl> contains alternating <dt>term</dt><dd>definition</dd> pairs.

Produces in the same directory:
  aws-glossary.md
  aws-glossary-terms.csv  (header: term,definition,source_anchor,notes)
  aws-glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.html"
OUT_DIR = Path(__file__).parent
PREFIX = "aws-glossary"


def fetch():
    r = requests.get(SOURCE_URL, timeout=30)
    r.raise_for_status()
    return r.text


def slugify(term):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", term.lower()).strip("-")
    return s


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    terms = []
    for dl in soup.select("dl"):
        children = list(dl.children)
        current_term = None
        for c in children:
            name = getattr(c, "name", None)
            if name == "dt":
                current_term = c.get_text(" ", strip=True)
            elif name == "dd" and current_term:
                definition = c.get_text(" ", strip=True)
                definition = re.sub(r"\s+", " ", definition).strip()
                anchor = f"{SOURCE_URL}#{slugify(current_term)}"
                terms.append(
                    {
                        "term": current_term,
                        "definition": definition,
                        "source_anchor": anchor,
                        "notes": "",
                    }
                )
                current_term = None
    # Dedupe by term (some terms may appear in multiple <dl>); keep longest definition
    by_term = {}
    for t in terms:
        existing = by_term.get(t["term"])
        if existing is None or len(t["definition"]) > len(existing["definition"]):
            by_term[t["term"]] = t
    return sorted(by_term.values(), key=lambda x: x["term"].lower())


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# AWS Glossary Reference\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: AWS documentation (CC-BY-SA-4.0 for documentation generally; verify per page).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
    return path


def write_csv(terms):
    path = OUT_DIR / f"{PREFIX}-terms.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["term", "definition", "source_anchor", "notes"]
        )
        w.writeheader()
        w.writerows(terms)
    return path


def write_json(terms):
    path = OUT_DIR / f"{PREFIX}-terms.json"
    with open(path, "w") as f:
        json.dump(terms, f, indent=2, ensure_ascii=False)
    return path


def main():
    html = fetch()
    terms = parse(html)
    md = write_md(terms)
    csv_path = write_csv(terms)
    json_path = write_json(terms)
    print(f"Extracted {len(terms)} terms")
    print(f"  {md}")
    print(f"  {csv_path}")
    print(f"  {json_path}")


if __name__ == "__main__":
    main()
