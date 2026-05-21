#!/usr/bin/env python3
"""Extract the Canadian Centre for Cyber Security (CCCS) Glossary.

Source: https://www.cyber.gc.ca/en/glossary
License: Government of Canada — Open Government Licence - Canada

Page structure: 26 letter-sections, each a <dl class="glossary-term"> containing
alternating <dt>term</dt><dd>definition</dd> pairs.

Produces:
  glossary.md
  glossary-terms.csv  (term,definition,source_anchor,notes)
  glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.cyber.gc.ca/en/glossary"
OUT_DIR = Path(__file__).parent
PREFIX = "glossary"


def fetch():
    r = requests.get(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    return r.text


def slugify(term):
    return re.sub(r"[^a-zA-Z0-9]+", "-", term.lower()).strip("-")


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    terms = []
    # CCCS wraps each term in a <div> inside each <dl class="dl-horizontal">,
    # so dt is not a direct child of dl. Walk all <dt> descendants and pair
    # each with the next-sibling <dd> (within the wrapping div).
    for dt in soup.select("dl dt"):
        term = dt.get_text(" ", strip=True)
        dd = dt.find_next_sibling("dd")
        if dd is None:
            # If the wrapper is a div, the dd lives next to dt inside the div
            parent = dt.parent
            if parent is not None:
                dd = parent.find("dd")
        if dd is None:
            continue
        definition = re.sub(r"\s+", " ", dd.get_text(" ", strip=True)).strip()
        terms.append({
            "term": term,
            "definition": definition,
            "source_anchor": f"{SOURCE_URL}#{slugify(term)}",
            "notes": "",
        })
    # Dedupe (some terms may appear in multiple dl blocks); keep longest
    by_term = {}
    for t in terms:
        cur = by_term.get(t["term"])
        if cur is None or len(t["definition"]) > len(cur["definition"]):
            by_term[t["term"]] = t
    return sorted(by_term.values(), key=lambda x: x["term"].lower())


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# Canadian Centre for Cyber Security Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: Government of Canada — Open Government Licence - Canada.\n\n")
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
