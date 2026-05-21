#!/usr/bin/env python3
"""Extract the State of Maryland Cybersecurity & Privacy Glossary into CSV/JSON.

Source PDF: https://doit.maryland.gov/policies/ci/Documents/Cybersecurity-and-Privacy-Glossary.pdf
License: Maryland state government work (Maryland Department of Information
Technology publication; US state records, generally redistributable).

Document structure (from pdftotext):
  "<Term>\n<Definition body, possibly multi-line>\n(Source: <citation>)"

Terms are bare titles (no leading number / bullet) followed by a paragraph
body that ends with "(Source: ...)". Source citations are mostly to NIST CSRC
or NIST SP series.

Reproduction recipe:
  1. curl -o /tmp/maryland.pdf <SOURCE_URL>
  2. python3 extract_cybersecurity_privacy_glossary.py /tmp/maryland.pdf

Produces:
  cybersecurity-privacy-glossary.md
  cybersecurity-privacy-glossary-terms.csv  (term,definition,source_anchor,notes)
  cybersecurity-privacy-glossary-terms.json
"""

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

OUT_DIR = Path(__file__).parent
PREFIX = "cybersecurity-privacy-glossary"
SOURCE_URL = "https://doit.maryland.gov/policies/ci/Documents/Cybersecurity-and-Privacy-Glossary.pdf"


def pdftotext(pdf_path):
    out = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout


def parse(text):
    # Drop the cover/footer artifacts
    lines = text.splitlines()
    # Find start (after "Last Updated" header and title) and end
    # The body begins with the first term entry.
    # Strategy: walk lines, when we see a "(Source: ...)" line, package up the
    # preceding lines into (term, definition body).
    blocks = []
    current_lines = []
    last_term = None
    for line in lines:
        # Drop page-footer artifacts: "<n>" alone, or "Page n of N"
        stripped = line.strip()
        if not stripped:
            current_lines.append("")
            continue
        if re.fullmatch(r"\d+", stripped):
            continue
        if re.match(r"^Page \d+ of \d+", stripped):
            continue
        if "Last Updated" in stripped or "State of Maryland" in stripped:
            continue
        if "Cybersecurity & Privacy Glossary" in stripped:
            continue
        current_lines.append(stripped)
        if re.search(r"\(Source: ", stripped):
            # End of a block. The term is the first non-empty line; the rest is
            # the definition (with the trailing (Source: ...) cite preserved).
            non_empty = [l for l in current_lines if l]
            if len(non_empty) >= 2:
                term = non_empty[0].strip()
                # Skip section-header-ish lines
                if re.match(r"^[A-Z][A-Za-z0-9 ,&\-/().]+$", term) and len(term) < 120:
                    body = " ".join(non_empty[1:]).strip()
                    # Extract the source cite
                    m = re.search(r"\(Source:\s*([^)]+)\)\s*$", body)
                    source_cite = ""
                    if m:
                        source_cite = m.group(1).strip()
                        body = body[: m.start()].strip()
                    blocks.append({
                        "term": term,
                        "definition": body,
                        "notes": f"source: {source_cite}" if source_cite else "",
                    })
            current_lines = []
    # Convert to standard schema
    out = []
    for b in blocks:
        if not b["term"] or not b["definition"]:
            continue
        out.append({
            "term": b["term"],
            "definition": b["definition"],
            "source_anchor": SOURCE_URL,
            "notes": b["notes"],
        })
    # Dedupe by term name; keep first
    seen = set()
    deduped = []
    for r in out:
        if r["term"] in seen:
            continue
        seen.add(r["term"])
        deduped.append(r)
    return deduped


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# State of Maryland Cybersecurity & Privacy Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: Maryland state government work (Maryland DoIT publication).\n\n")
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
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/phase4d/maryland.pdf"
    text = pdftotext(pdf_path)
    terms = parse(text)
    md = write_md(terms)
    csv_path = write_csv(terms)
    json_path = write_json(terms)
    print(f"Extracted {len(terms)} terms")
    print(f"  {md}")
    print(f"  {csv_path}")
    print(f"  {json_path}")


if __name__ == "__main__":
    main()
