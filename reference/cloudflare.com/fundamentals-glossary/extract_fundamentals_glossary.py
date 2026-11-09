#!/usr/bin/env python3
"""Extract the Cloudflare Developer Documentation Fundamentals Glossary into CSV/JSON.

Source:        https://developers.cloudflare.com/fundamentals/reference/glossary/
Markdown alt:  https://developers.cloudflare.com/fundamentals/reference/glossary/index.md
License:       LicenseRef-Vendor-Copyright (Cloudflare, Inc.; internal CSA use only).

Page structure: the .md alternate is a single markdown table with three columns —
Term | Definition | Product. The Product column tags each term with the Cloudflare
service it belongs to (Spectrum, Workers, R2, WAF, Zero Trust, etc.); captured in
the notes field as `product: <name>`.

Produces:
  fundamentals-glossary.md
  fundamentals-glossary-terms.csv   (header: term,definition,source_anchor,notes)
  fundamentals-glossary-terms.json
"""

import csv
import json
import re
from pathlib import Path

import requests

SOURCE_URL = "https://developers.cloudflare.com/fundamentals/reference/glossary/"
MD_URL = "https://developers.cloudflare.com/fundamentals/reference/glossary/index.md"
OUT_DIR = Path(__file__).parent
PREFIX = "fundamentals-glossary"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)


def fetch():
    r = requests.get(
        MD_URL,
        timeout=30,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
    )
    r.raise_for_status()
    return r.text


def squish(s):
    return re.sub(r"\s+", " ", s).strip()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def parse(md):
    # Find the first markdown table whose header includes Term / Definition / Product.
    terms = []
    in_table = False
    expected_cols = None
    for line in md.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table:
                # End of table.
                break
            continue
        # Split markdown table row on '|', drop leading/trailing empties.
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if expected_cols is None:
            # Header row.
            if not any("term" in c.lower() for c in cells):
                continue
            expected_cols = cells
            continue
        # Separator row (---|---|---).
        if all(re.match(r"^[\s\-:]+$", c) for c in cells):
            in_table = True
            continue
        if not in_table:
            continue
        if len(cells) < 2:
            continue
        term = squish(cells[0])
        definition = squish(cells[1])
        if not term or not definition:
            continue
        notes = ""
        if len(cells) >= 3 and cells[2]:
            product = squish(cells[2])
            if product:
                notes = f"product: {product}"
        anchor = f"{SOURCE_URL}#{slug(term)}"
        terms.append(
            {
                "term": term,
                "definition": definition,
                "source_anchor": anchor,
                "notes": notes,
            }
        )

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
        f.write("# Cloudflare Developer Documentation Fundamentals Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n")
        f.write(f"Markdown alternate (used by the extractor): {MD_URL}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (Cloudflare, Inc.; internal CSA use only — not redistributable).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
            if t["notes"]:
                f.write(f"_{t['notes']}_\n\n")
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
    md = fetch()
    terms = parse(md)
    write_md(terms)
    write_csv(terms)
    write_json(terms)
    print(f"Extracted {len(terms)} terms")


if __name__ == "__main__":
    main()
