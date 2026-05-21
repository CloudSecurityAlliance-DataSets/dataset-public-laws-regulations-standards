#!/usr/bin/env python3
"""Extract OAIC Chapter B (Key Concepts) for Australian Privacy Principles.

Source: https://www.oaic.gov.au/privacy/australian-privacy-principles/
        australian-privacy-principles-guidelines/chapter-b-key-concepts

Structure: each key concept is an <h3>, followed by numbered <p>
paragraphs (B.2, B.3, ...) and optional <ul>, <h4> sub-sections until
the next <h3> or <h2>. The page also has section headers ("Key concepts
A to D", "Enforcement related activities through Purpose", ...) as <h2>
which we treat as boundaries but not as terms.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

SRC_URL = ("https://www.oaic.gov.au/privacy/australian-privacy-principles/"
           "australian-privacy-principles-guidelines/chapter-b-key-concepts")
HERE = Path(__file__).resolve().parent
DIRNAME = HERE.name  # "app-key-concepts"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Section headers that aren't concepts themselves.
SKIP_HEADINGS = {
    "key concepts a to d",
    "key concepts e to p",
    "key concepts q to z",
    "enforcement related activities through purpose",
    "reasonable through use",
    "on this page",
}


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def slugify(term: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
    return s[:64]


def collect_body(h3: Tag) -> str:
    """Walk siblings after `h3` until the next h2/h3."""
    parts: list[str] = []
    for sib in h3.next_siblings:
        if isinstance(sib, NavigableString):
            continue
        if not isinstance(sib, Tag):
            continue
        if sib.name in {"h1", "h2", "h3"}:
            break
        if sib.name in {"h4", "h5", "h6"}:
            parts.append(f"\n[{normalize(sib.get_text(' ', strip=True))}]")
            continue
        if sib.name in {"p", "ul", "ol", "blockquote", "pre", "table"}:
            parts.append(normalize(sib.get_text(" ", strip=True)))
    return "\n\n".join(p for p in parts if p)


def extract():
    r = requests.get(SRC_URL, timeout=60, headers={"User-Agent": UA})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    rows = []
    seen = set()
    # Only operate within the main content article if present.
    container = soup.find("main") or soup.find("article") or soup
    for h3 in container.find_all("h3"):
        term = normalize(h3.get_text(" ", strip=True))
        if not term:
            continue
        if term.lower() in SKIP_HEADINGS:
            continue
        if term in seen:
            continue
        body = collect_body(h3)
        if not body:
            continue
        seen.add(term)
        anchor = h3.get("id") or slugify(term)
        rows.append({
            "term": term,
            "definition": body,
            "source_anchor": f"{SRC_URL}#{anchor}",
            "notes": "Australian Privacy Principles guidelines, Chapter B",
        })
    return rows


def write_outputs(rows):
    base = HERE / DIRNAME
    md_path = base.with_suffix(".md")
    csv_path = HERE / f"{DIRNAME}-terms.csv"
    json_path = HERE / f"{DIRNAME}-terms.json"

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# OAIC Australian Privacy Principles - Chapter B: Key Concepts\n\n")
        f.write(f"Source: {SRC_URL}\n\n")
        for row in rows:
            f.write(f"## {row['term']}\n{row['definition']}\n\n")

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        for row in rows:
            w.writerow(row)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(rows)} terms")
    print(f"  {md_path}")
    print(f"  {csv_path}")
    print(f"  {json_path}")


if __name__ == "__main__":
    rows = extract()
    if len(rows) < 10:
        print(f"WARN: only {len(rows)} terms extracted", file=sys.stderr)
    write_outputs(rows)
