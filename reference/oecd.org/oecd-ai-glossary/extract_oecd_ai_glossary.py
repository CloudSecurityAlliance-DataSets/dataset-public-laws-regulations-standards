#!/usr/bin/env python3
"""Parse the OECD AI Papers No. 16 ('Defining AI Incidents and Related Terms')
into per-term glossary rows.

Source: https://www.oecd.org/en/publications/defining-ai-incidents-and-related-terms_d1a8d965-en.html
PDF:    https://www.oecd.org/content/dam/oecd/en/publications/.../d1a8d965-en.pdf  (also at the html page)
Local:  defining-ai-incidents-and-related-terms.pdf (kept in S3, gitignored)

This OECD paper is the closest thing OECD publishes to an AI glossary — formal
definitions of:
    - AI incident
    - Serious AI incident
    - AI disaster
    - AI hazard
    - Serious AI hazard

Each definition appears as a "Draft definition of <term>" heading followed by
an indented prose block. The extractor:

    1. Walks every 'Draft definition of <term>' heading
    2. Captures the indented definition block (one or more paragraphs, including
       enumerated harm categories) until the explanatory 'This working definition
       is based on ...' or 'Key clarifications:' break
    3. Emits one row per term

Output: oecd-ai-glossary-terms.{csv,json}
"""
import csv
import json
import re
from pathlib import Path


SOURCE_URL = ("https://www.oecd.org/en/publications/"
              "defining-ai-incidents-and-related-terms_d1a8d965-en.html")
HERE = Path(__file__).resolve().parent
MD_PATH = HERE / "oecd-ai-glossary.md"

HEADING_RE = re.compile(
    r"^Draft definition of (?:an? |a )?(?P<term>.+?)\s*$",
    re.MULTILINE,
)

# Lines that signal end-of-definition (commentary that follows the formal text).
END_MARKERS = (
    "This working definition",
    "Key clarifications:",
    "Serious AI",  # e.g., "Serious AI hazards are a subset of AI hazards."
)


def normalize(text: str) -> str:
    """Collapse whitespace and clean up enumerated lists into a single block."""
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    md = MD_PATH.read_text(encoding="utf-8")
    lines = md.splitlines()

    rows = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line.strip())
        if not m:
            continue
        term = m.group("term").strip()
        # Skip TOC entries which match the same prefix but trail with a
        # page-number column (e.g., 'AI disaster                          11').
        if re.search(r"\s+\d+\s*$", term):
            continue
        # Capture indented body until end-marker or next heading
        body_lines = []
        for j in range(i + 1, len(lines)):
            stripped = lines[j].strip()
            if not stripped:
                continue
            # Stop conditions
            if HEADING_RE.match(stripped):
                break
            if any(stripped.startswith(mk) for mk in END_MARKERS):
                break
            # Skip running headers/footers from the PDF
            if re.match(r"^\d+\s+DEFINING AI INCIDENTS", stripped):
                continue
            if re.match(r"^DEFINING AI INCIDENTS.+\d+$", stripped):
                continue
            if "OECD ARTIFICIAL INTELLIGENCE PAPERS" in stripped:
                continue
            body_lines.append(stripped)
        definition = normalize(" ".join(body_lines))
        if not definition:
            continue
        rows.append({
            "term": term,
            "definition": definition,
            "source_anchor": SOURCE_URL,
            "notes": "OECD AI Papers No. 16 (May 2024) — formal working definition",
        })

    stem = HERE.name
    csv_path = HERE / f"{stem}-terms.csv"
    json_path = HERE / f"{stem}-terms.json"
    fields = ["term", "definition", "source_anchor", "notes"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")

    print(f"Terms: {len(rows)}")
    for r in rows:
        print(f"  - {r['term']}")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    main()
