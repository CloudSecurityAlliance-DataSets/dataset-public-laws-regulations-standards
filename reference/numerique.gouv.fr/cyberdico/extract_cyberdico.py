#!/usr/bin/env python3
"""Extract the ANSSI / cyber.gouv.fr CyberDico glossary.

Source: https://cyber.gouv.fr/glossaire

Structure: each term is an <h3> with a French (or English) headword.
Immediately following the h3 is one <h4> giving the translation ("EN :
Local access" or "FR : Logiciel publicitaire") and one or more <p>
paragraphs for the definition. Walk forward until the next h2/h3.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

SRC_URL = "https://cyber.gouv.fr/glossaire"
HERE = Path(__file__).resolve().parent
DIRNAME = HERE.name  # "cyberdico"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def slugify(term: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
    return s[:64]


def collect_for_term(h3: Tag):
    """Return (translation_h4_text, definition_text) by walking siblings
    until the next h2/h3."""
    translation = ""
    parts: list[str] = []
    for sib in h3.next_siblings:
        if isinstance(sib, NavigableString):
            continue
        if not isinstance(sib, Tag):
            continue
        if sib.name in {"h1", "h2", "h3"}:
            break
        if sib.name == "h4" and not translation:
            translation = normalize(sib.get_text(" ", strip=True))
            continue
        if sib.name in {"p", "ul", "ol", "blockquote", "pre", "table"}:
            parts.append(normalize(sib.get_text(" ", strip=True)))
    return translation, "\n\n".join(p for p in parts if p)


def extract():
    r = requests.get(SRC_URL, timeout=60, headers={"User-Agent": UA})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    container = soup.find("main") or soup.find("article") or soup
    rows = []
    seen = set()
    for h3 in container.find_all("h3"):
        term = normalize(h3.get_text(" ", strip=True))
        if not term or term in seen:
            continue
        translation, body = collect_for_term(h3)
        if not body:
            continue
        seen.add(term)
        anchor = h3.get("id") or slugify(term)
        rows.append({
            "term": term,
            "definition": body,
            "source_anchor": f"{SRC_URL}#{anchor}",
            "notes": translation,
        })
    return rows


def write_outputs(rows):
    base = HERE / DIRNAME
    md_path = base.with_suffix(".md")
    csv_path = HERE / f"{DIRNAME}-terms.csv"
    json_path = HERE / f"{DIRNAME}-terms.json"

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# CyberDico - Glossaire (cyber.gouv.fr / ANSSI)\n\n")
        f.write(f"Source: {SRC_URL}\n\n")
        for row in rows:
            f.write(f"## {row['term']}\n")
            if row['notes']:
                f.write(f"*{row['notes']}*\n\n")
            f.write(f"{row['definition']}\n\n")

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
