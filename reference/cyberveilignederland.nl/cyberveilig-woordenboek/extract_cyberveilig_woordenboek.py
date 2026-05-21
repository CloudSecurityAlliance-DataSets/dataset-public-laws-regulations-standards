#!/usr/bin/env python3
"""Extract the Cyberveilig Woordenboek (Dutch Cybersecurity Dictionary) into CSV/JSON.

Source PDF: https://www.cyberveilignederland.nl/download/file/Cyberveilig_Woordenboek2024.pdf
License: CC-BY-4.0 (explicit in PDF colophon: "Copyright: Creative Commons
Naamsvermelding 4.0 Internationaal (CC BY 4.0)").

The PDF is a Dutch security dictionary published by Cyberveilig Nederland in
cooperation with ECP (Platform voor de Informatiesamenleving). 4th edition,
November 2024, ~800 terms with cross-references.

The original 3-column page layout (BEGRIP | BETEKENIS | ZIE OOK) is too complex
for pdftotext. We use the marker GPU pipeline to render to markdown, which
emits clean pipe-delimited tables. This script parses those tables.

Reproduction recipe:
  1. curl -o /tmp/cyberveilig.pdf <SOURCE_URL>
  2. tools-resources/utils/pdf_to_md_via_gpu.sh \\
       --output-dir reference/cyberveilignederland.nl/cyberveilig-woordenboek/_marker/ \\
       /tmp/cyberveilig.pdf
  3. python3 extract_cyberveilig_woordenboek.py

Marker output lives at _marker/cyberveilig/cyberveilig.md.

Produces:
  cyberveilig-woordenboek.md
  cyberveilig-woordenboek-terms.csv  (term,definition,source_anchor,notes)
  cyberveilig-woordenboek-terms.json
"""

import csv
import json
import re
from pathlib import Path

OUT_DIR = Path(__file__).parent
PREFIX = "cyberveilig-woordenboek"
MARKER_MD = OUT_DIR / "_marker" / "cyberveilig" / "cyberveilig.md"
SOURCE_URL = "https://www.cyberveilignederland.nl/download/file/Cyberveilig_Woordenboek2024.pdf"


def slugify(term):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", term.lower().encode("ascii", "ignore").decode())
    return s.strip("-")


def clean_cell(text):
    """Collapse marker's <br>-as-newline and column-wrap whitespace into a single string."""
    # Strip markdown formatting markers but preserve content
    text = text.strip()
    # Replace multiple spaces / newlines with single space
    text = re.sub(r"\s+", " ", text)
    return text


def parse_marker(text):
    lines = text.splitlines()
    in_table = False
    current_row_cells = None  # When set, we're inside a multi-line row
    rows = []

    # Marker tables look like:
    #   | term      | definition spans multiple lines<br>continuing here | see-also |
    # In the .md output marker often renders cells one per line:
    #   | Term name |
    #   | Definition body continuing<br>more body | See also refs |
    # Easier path: identify each `| ... |` row and split on `|`.

    for raw in lines:
        # Skip table-separator rows like |---|---|---|
        if re.match(r"^\s*\|[\s\-:|]+\|\s*$", raw):
            in_table = True
            continue
        if not raw.strip().startswith("|"):
            in_table = False
            continue
        in_table = True
        # Split into cells; the leading and trailing | produce empty strings
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if not cells:
            continue
        # If exactly 3 cells, that's the BEGRIP | BETEKENIS | ZIE OOK shape.
        # Skip header rows.
        if cells and cells[0].lower() in {"begrip", "term"}:
            continue
        if len(cells) >= 3:
            term = cells[0]
            definition = " ".join(cells[1:-1])
            see_also = cells[-1]
        elif len(cells) == 2:
            term = cells[0]
            definition = cells[1]
            see_also = ""
        else:
            continue
        if not term:
            continue
        rows.append({
            "term": term,
            "definition": clean_cell(definition),
            "see_also": clean_cell(see_also),
        })

    # Some marker tables wrap a single term across multiple table rows by leaving
    # the term column empty in continuation rows. Merge them.
    merged = []
    for r in rows:
        if r["term"]:
            merged.append(r)
        elif merged:
            merged[-1]["definition"] = (merged[-1]["definition"] + " " + r["definition"]).strip()
            if r.get("see_also") and not merged[-1]["see_also"]:
                merged[-1]["see_also"] = r["see_also"]

    # Convert to standard schema
    out = []
    for r in merged:
        term = r["term"].strip()
        definition = r["definition"].strip()
        if not term or not definition:
            continue
        # Skip page-number / cover-banner artifacts
        if re.match(r"^\d+$", term):
            continue
        if re.search(r"^\s*Cybersecurity Woordenboek", term):
            continue
        out.append({
            "term": term,
            "definition": definition,
            "source_anchor": f"{SOURCE_URL}#{slugify(term)}",
            "notes": f"see also: {r['see_also']}" if r["see_also"] else "",
        })
    # Dedupe by term, keep longest definition
    by_term = {}
    for r in out:
        existing = by_term.get(r["term"])
        if existing is None or len(r["definition"]) > len(existing["definition"]):
            by_term[r["term"]] = r
    return sorted(by_term.values(), key=lambda x: x["term"].lower())


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# Cyberveilig Woordenboek 2024\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: CC-BY-4.0 (Cyberveilig Nederland i.s.m. ECP).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
            if t["notes"]:
                f.write(f"*{t['notes']}*\n\n")
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
    if not MARKER_MD.exists():
        raise SystemExit(
            f"Missing marker output at {MARKER_MD}. Run pdf_to_md_via_gpu.sh first "
            "(see this file's docstring)."
        )
    text = MARKER_MD.read_text()
    terms = parse_marker(text)
    md = write_md(terms)
    csv_path = write_csv(terms)
    json_path = write_json(terms)
    print(f"Extracted {len(terms)} terms")
    print(f"  {md}")
    print(f"  {csv_path}")
    print(f"  {json_path}")


if __name__ == "__main__":
    main()
