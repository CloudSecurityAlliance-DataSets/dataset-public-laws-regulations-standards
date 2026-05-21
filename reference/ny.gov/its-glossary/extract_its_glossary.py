#!/usr/bin/env python3
"""Extract the New York State ITS glossary.

Source: https://its.ny.gov/glossary

Structure: the glossary is a single HTML <table> with two columns
("Term" and "Definition"). Rows where the "Definition" cell is empty are
alphabet section headers (A, B, C, ...) and are skipped. The table
contains ~400 rows; expect ~300 real term entries.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SRC_URL = "https://its.ny.gov/glossary"
HERE = Path(__file__).resolve().parent
DIRNAME = HERE.name  # "its-glossary"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def normalize(s: str) -> str:
    s = re.sub(r"\s+", " ", s or "")
    return s.strip()


def slugify(term: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
    return s[:64]


def extract():
    r = requests.get(SRC_URL, timeout=60, headers={"User-Agent": UA, "Accept": "text/html"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")
    if table is None:
        raise RuntimeError("No <table> found on its.ny.gov/glossary")
    rows = []
    seen = set()
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if len(cells) < 2:
            continue
        term = normalize(cells[0].get_text(" ", strip=True))
        definition = normalize(cells[1].get_text(" ", strip=True))
        if not term or term.lower() == "term":
            continue
        if not definition:
            # Alphabet header row (single letter, no definition).
            continue
        if term in seen:
            continue
        seen.add(term)
        rows.append({
            "term": term,
            "definition": definition,
            "source_anchor": f"{SRC_URL}#{slugify(term)}",
            "notes": "",
        })
    return rows


def write_outputs(rows):
    base = HERE / DIRNAME
    md_path = base.with_suffix(".md")
    csv_path = HERE / f"{DIRNAME}-terms.csv"
    json_path = HERE / f"{DIRNAME}-terms.json"

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# New York State ITS Glossary\n\n")
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
