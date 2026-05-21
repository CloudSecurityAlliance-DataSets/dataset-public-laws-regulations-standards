#!/usr/bin/env python3
"""Extract the Kubernetes glossary.

Source: https://kubernetes.io/docs/reference/glossary/

Structure: <ul class="glossary-terms"><li>... each <li> contains
  - <div id="term-{slug}" class="term-anchor">
  - <div class="term-name"><span class="glossary-term-name">Name</span>...</div>
  - <div class="term-definition">
      <span class="preview-text"><p>Short definition</p>...</span>
      <div id="{slug}" class="hide"><p>Long detail</p>...</div>
    </div>
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag

SRC_URL = "https://kubernetes.io/docs/reference/glossary/"
HERE = Path(__file__).resolve().parent
DIRNAME = HERE.name  # "kubernetes-glossary"


def text_of(node) -> str:
    if node is None:
        return ""
    s = node.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", s).strip()


def clean_preview(node: Tag) -> str:
    """preview-text contains the short definition <p>; strip the trailing
    [+] anchor that toggles the long form."""
    if node is None:
        return ""
    # Drop the toggle anchor.
    for a in node.select("a.click-controller, a[href='javascript:void(0)']"):
        a.decompose()
    return text_of(node)


def long_definition(li: Tag) -> str:
    """Long definition is in <div class='hide'> inside term-definition."""
    div = li.select_one("div.term-definition > div.hide")
    if div is None:
        # Sometimes the toggle div is nested differently.
        div = li.select_one("div.term-definition div[id]:not(.term-anchor)")
    if div is None:
        return ""
    return text_of(div)


def extract():
    r = requests.get(SRC_URL, timeout=60, headers={"User-Agent": "csa-dataset-extractor/1.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    lis = soup.select("ul.glossary-terms > li")
    rows = []
    seen = set()
    for li in lis:
        name_node = li.select_one("span.glossary-term-name")
        term = text_of(name_node)
        if not term or term in seen:
            continue
        seen.add(term)
        anchor_div = li.select_one("div.term-anchor[id]")
        anchor_id = anchor_div["id"] if anchor_div and anchor_div.has_attr("id") else ""
        preview = li.select_one("div.term-definition span.preview-text")
        short = clean_preview(preview)
        long_def = long_definition(li)
        # Combine short + long; long often elaborates.
        if long_def and long_def != short:
            definition = short + ("\n\n" + long_def if long_def else "")
        else:
            definition = short
        if not definition.strip():
            continue
        # Capture tags (from li classes like "tag-tool", "tag-security") for notes.
        tags = [c.replace("tag-", "") for c in li.get("class", []) if c.startswith("tag-")]
        notes = "tags: " + ", ".join(sorted(tags)) if tags else ""
        rows.append({
            "term": term,
            "definition": definition.strip(),
            "source_anchor": f"{SRC_URL}#{anchor_id}" if anchor_id else SRC_URL,
            "notes": notes,
        })
    return rows


def write_outputs(rows):
    base = HERE / DIRNAME
    md_path = base.with_suffix(".md")
    csv_path = HERE / f"{DIRNAME}-terms.csv"
    json_path = HERE / f"{DIRNAME}-terms.json"

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Kubernetes Glossary\n\n")
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
