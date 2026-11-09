#!/usr/bin/env python3
"""Extract the Cisco Security Glossary into structured CSV/JSON.

Source:  https://www.cisco.com/c/en/us/td/docs/security/glossary/b_security_glossary_terms.html
License: LicenseRef-Vendor-Copyright (Cisco Systems, Inc.; internal CSA use only).

Page structure: DITA-style. Each term is wrapped in <article class="glossentry"
id="term-id"> with:
  h3.glossterm        -> term name
  div.glossdef        -> contains a table with metadata rows; we pull the row
                        whose label cell is "Definition" and read its value cell.
                        Other label rows seen: "Products", "Synonym(s)".
                        We capture Synonym(s) into the notes field when present.

Produces:
  security-glossary.md
  security-glossary-terms.csv   (header: term,definition,source_anchor,notes)
  security-glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOURCE_URL = (
    "https://www.cisco.com/c/en/us/td/docs/security/glossary/"
    "b_security_glossary_terms.html"
)
OUT_DIR = Path(__file__).parent
PREFIX = "security-glossary"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)


def fetch():
    r = requests.get(
        SOURCE_URL,
        timeout=30,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
    )
    r.raise_for_status()
    return r.text


def squish(s):
    return re.sub(r"\s+", " ", s).strip()


def parse_glossdef_table(glossdef):
    """Walk the metadata table inside .glossdef; return (definition, synonyms_str)."""
    definition = ""
    synonyms = ""
    for row in glossdef.select("tr"):
        cells = row.find_all("td")
        if len(cells) != 2:
            continue
        label = squish(cells[0].get_text(" ", strip=True)).lower().rstrip(":")
        value = squish(cells[1].get_text(" ", strip=True))
        if label == "definition":
            definition = value
        elif label in {"synonym", "synonyms", "synonym(s)"}:
            synonyms = value
    # Fall back to all glossdef text if no Definition row found.
    if not definition:
        definition = squish(glossdef.get_text(" ", strip=True))
    return definition, synonyms


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    terms = []
    for entry in soup.select(".glossentry"):
        term_el = entry.select_one(".glossterm")
        if not term_el:
            continue
        term = squish(term_el.get_text(" ", strip=True))
        if not term:
            continue

        glossdef = entry.select_one(".glossdef")
        if not glossdef:
            continue
        definition, synonyms = parse_glossdef_table(glossdef)
        if not definition:
            continue

        anchor_id = entry.get("id", "")
        source_anchor = f"{SOURCE_URL}#{anchor_id}" if anchor_id else SOURCE_URL

        notes = f"synonyms: {synonyms}" if synonyms else ""

        terms.append(
            {
                "term": term,
                "definition": definition,
                "source_anchor": source_anchor,
                "notes": notes,
            }
        )

    # Dedupe by case-insensitive term, keep longest definition.
    by_term = {}
    for t in terms:
        key = t["term"].lower()
        existing = by_term.get(key)
        if existing is None or len(t["definition"]) > len(existing["definition"]):
            by_term[key] = t
    return sorted(by_term.values(), key=lambda x: x["term"].lower())


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# Cisco Security Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (Cisco Systems, Inc.; internal CSA use only — not redistributable).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
            if t["notes"]:
                f.write(f"_{t['notes']}_\n\n")
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
