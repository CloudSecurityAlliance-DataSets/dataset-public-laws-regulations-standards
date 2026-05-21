#!/usr/bin/env python3
"""Extract GitLab Application Security terminology glossary.

Source: https://docs.gitlab.com/user/application_security/terminology/

Structure: <h2> headings for each term, followed by one or more <p>
paragraphs and other content until the next <h2>. The page also has a
top-level <h1> for the page title and a leading "On this page" TOC we
must skip.
"""
from __future__ import annotations

import csv
import html
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

SRC_URL = "https://docs.gitlab.com/user/application_security/terminology/"
HERE = Path(__file__).resolve().parent
DIRNAME = HERE.name  # "security-glossary"


def text_of(node: Tag) -> str:
    s = node.get_text(" ", strip=True)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def slug_of(h2: Tag) -> str:
    # GitLab Hugo headings use an `id` attribute. Fall back to the slugified
    # text if absent.
    if h2.get("id"):
        return h2["id"]
    return re.sub(r"[^a-z0-9]+", "-", text_of(h2).lower()).strip("-")


def collect_definition(h2: Tag) -> str:
    """Walk siblings after `h2` until the next h2 (or higher heading)."""
    parts: list[str] = []
    for sib in h2.next_siblings:
        if isinstance(sib, NavigableString):
            continue
        if not isinstance(sib, Tag):
            continue
        if sib.name in {"h1", "h2"}:
            break
        if sib.name in {"h3", "h4", "h5", "h6"}:
            # Treat sub-headings as part of the definition; render inline.
            parts.append(f"[{text_of(sib)}]")
            continue
        if sib.name in {"p", "ul", "ol", "blockquote", "pre", "table"}:
            parts.append(text_of(sib))
    return "\n\n".join(p for p in parts if p)


def extract():
    r = requests.get(SRC_URL, timeout=60, headers={"User-Agent": "csa-dataset-extractor/1.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    # The main content lives under <main>.
    main = soup.find("main") or soup
    h2s = main.find_all("h2")
    rows = []
    seen = set()
    for h2 in h2s:
        term = text_of(h2)
        if not term:
            continue
        # Skip non-term headings like "On this page".
        low = term.lower()
        if low in {"on this page", "table of contents", "feedback"}:
            continue
        if term in seen:
            continue
        seen.add(term)
        definition = collect_definition(h2)
        if not definition:
            continue
        anchor = slug_of(h2)
        rows.append({
            "term": term,
            "definition": definition,
            "source_anchor": f"{SRC_URL}#{anchor}" if anchor else SRC_URL,
            "notes": "",
        })
    return rows


def write_outputs(rows):
    base = HERE / DIRNAME
    md_path = base.with_suffix(".md")
    csv_path = HERE / f"{DIRNAME}-terms.csv"
    json_path = HERE / f"{DIRNAME}-terms.json"

    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# GitLab Application Security Terminology\n\n")
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
