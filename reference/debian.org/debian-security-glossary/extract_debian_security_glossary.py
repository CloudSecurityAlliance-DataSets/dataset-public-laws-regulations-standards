#!/usr/bin/env python3
"""Extract the Debian Security Team Glossary into structured CSV/JSON.

Source: https://security-team.debian.org/glossary.html
License: Debian web content — conventionally redistributable (MIT-style site
terms; no inline restrictive notice on the page itself).

Tiny glossary (8 entries): acronyms used in Debian Security Advisories.

Produces:
  debian-security-glossary.md
  debian-security-glossary-terms.csv  (term,definition,source_anchor,notes)
  debian-security-glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://security-team.debian.org/glossary.html"
OUT_DIR = Path(__file__).parent
PREFIX = "debian-security-glossary"


def slugify(term):
    return re.sub(r"[^a-zA-Z0-9]+", "-", term.lower()).strip("-")


def fetch():
    r = requests.get(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    return r.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    terms = []
    for dt in soup.select("dl dt"):
        term = dt.get_text(" ", strip=True)
        dd = dt.find_next_sibling("dd")
        if not dd:
            continue
        definition = re.sub(r"\s+", " ", dd.get_text(" ", strip=True)).strip()
        terms.append({
            "term": term,
            "definition": definition,
            "source_anchor": f"{SOURCE_URL}#{slugify(term)}",
            "notes": "",
        })
    return terms


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# Debian Security Team Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: Debian web content (MIT-style site terms).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
    return path


def write_csv(terms):
    path = OUT_DIR / f"{PREFIX}-terms.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
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
