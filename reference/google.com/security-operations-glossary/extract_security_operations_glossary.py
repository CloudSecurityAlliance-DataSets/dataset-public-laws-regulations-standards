#!/usr/bin/env python3
"""Extract the Google Chronicle / Security Operations Glossary into structured form.

Source: https://docs.cloud.google.com/chronicle/docs/glossary
License: Creative Commons Attribution 4.0 (CC-BY-4.0) per Google Cloud docs site.

The page uses a flat list of <p> elements inside the article body, each of the
form "Term: Definition". This script:

  1. Downloads the page.
  2. Parses the article body and extracts each "Term: Definition" pair.
  3. Emits three sibling files in this directory:
       - security-operations-glossary.md
       - security-operations-glossary-terms.csv  (term,definition,source_anchor,notes)
       - security-operations-glossary-terms.json

The page does not assign anchor IDs to individual terms, so source_anchor is
left empty (the column is preserved so downstream consumers have a stable
schema if anchors are added later).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

URL = "https://docs.cloud.google.com/chronicle/docs/glossary"
HERE = Path(__file__).resolve().parent
SLUG = "security-operations-glossary"


def fetch_html(url: str) -> str:
    resp = requests.get(url, timeout=60, headers={
        "User-Agent": "CSA-DataSets-extractor/1.0 (+https://github.com/CloudSecurityAlliance-DataSets)"
    })
    resp.raise_for_status()
    return resp.text


def parse_terms(html: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    article = (
        soup.find("div", class_="devsite-article-body")
        or soup.find("article")
        or soup.find("main")
    )
    if article is None:
        raise RuntimeError("Could not locate article body in glossary HTML")

    terms: List[Dict[str, str]] = []
    for p in article.find_all("p"):
        text = p.get_text(" ", strip=True)
        # Collapse internal whitespace (the source has double-spaces in a few entries)
        text = re.sub(r"\s+", " ", text)
        if ":" not in text:
            continue
        term, _, definition = text.partition(":")
        term = term.strip()
        definition = definition.strip()
        if not term or not definition:
            continue
        # Skip obvious non-glossary paragraphs (boilerplate, feedback links).
        if term.lower() in {"send feedback", "note", "caution", "warning"}:
            continue
        terms.append({
            "term": term,
            "definition": definition,
            "source_anchor": "",  # page does not expose per-term anchors
            "notes": "",
        })
    return terms


def write_csv(rows: List[Dict[str, str]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["term", "definition", "source_anchor", "notes"]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(rows: List[Dict[str, str]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_markdown(rows: List[Dict[str, str]], path: Path) -> None:
    lines: List[str] = []
    lines.append("# Google Security Operations - Glossary of Terms")
    lines.append("")
    lines.append(f"Source: <{URL}>")
    lines.append("")
    lines.append("Licensed under Creative Commons Attribution 4.0 (CC-BY-4.0).")
    lines.append("")
    lines.append(f"Total terms: {len(rows)}")
    lines.append("")
    for row in rows:
        lines.append(f"- **{row['term']}**: {row['definition']}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    html = fetch_html(URL)
    rows = parse_terms(html)
    if not rows:
        print("ERROR: no terms extracted", file=sys.stderr)
        return 1

    write_markdown(rows, HERE / f"{SLUG}.md")
    write_csv(rows, HERE / f"{SLUG}-terms.csv")
    write_json(rows, HERE / f"{SLUG}-terms.json")
    print(f"Extracted {len(rows)} terms to {HERE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
