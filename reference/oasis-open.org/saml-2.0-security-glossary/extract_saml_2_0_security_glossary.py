#!/usr/bin/env python3
"""Extract the OASIS SAML V2.0 Security Glossary into CSV/JSON.

Source PDF: https://docs.oasis-open.org/security/saml/v2.0/saml-glossary-2.0-os.pdf
License: OASIS IPR boilerplate — "This document and translations of it may be
copied and furnished to others, and derivative works that comment on or
otherwise explain it or assist in its implementation may be prepared, copied,
published and distributed, in whole or in part, without restriction of any
kind, provided that the above copyright notice and this paragraph are included
on all such copies and derivative works."

The PDF presents a Term/Definition two-column table on pages 4–13. Terms start
in a left column at character offset ~8 (after a line-number column), and
definitions are in a right column starting at offset ~55. Continuation lines
have an empty term column.

Reproduction recipe:
  1. curl -o /tmp/oasis-saml.pdf <SOURCE_URL>
  2. python3 extract_saml_2_0_security_glossary.py /tmp/oasis-saml.pdf

Produces:
  saml-2.0-security-glossary.md
  saml-2.0-security-glossary-terms.csv  (term,definition,source_anchor,notes)
  saml-2.0-security-glossary-terms.json
"""

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

OUT_DIR = Path(__file__).parent
PREFIX = "saml-2.0-security-glossary"
SOURCE_URL = "https://docs.oasis-open.org/security/saml/v2.0/saml-glossary-2.0-os.pdf"


def pdftotext(pdf_path):
    return subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True, check=True,
    ).stdout


# Column boundaries observed in the PDF rendering:
#   - line number ends around col 5
#   - term column spans roughly cols 7–48
#   - definition column starts around col 50
TERM_LINE_RE = re.compile(r"^\s*\d+\s+(\S.{0,42})\s{2,}(\S.+)$")
CONT_LINE_RE = re.compile(r"^\s*\d+\s{6,}(\S.+)$")
# Lines that aren't part of the table — page footer, section headers, etc.
SKIP_RE = re.compile(
    r"^\s*(saml-glossary-2\.0-os|Copyright ©|Page \d+ of|15 March 2005|"
    r"Term\s+Definition|This normative document|Some definitions|"
    r"Following are|\d+ Glossary|\d+ References)"
)


def parse(text):
    blocks = []  # list of {term, definition_lines}
    current = None
    in_glossary = False
    for raw in text.splitlines():
        # Track entering the glossary section. Match only the section heading
        # itself (e.g. " 63   1       Glossary"), not the TOC entry that has
        # trailing dot-leaders.
        if re.match(r"^\s*\d+\s+1\s+Glossary\s*$", raw):
            in_glossary = True
            continue
        if re.match(r"^\s*\d+\s+2\s+References\s*$", raw):
            in_glossary = False
            break
        if not in_glossary:
            continue
        if SKIP_RE.match(raw):
            continue
        # New term line: number + left-col term + right-col body
        m = TERM_LINE_RE.match(raw)
        if m:
            term = m.group(1).strip()
            body = m.group(2).strip()
            # Filter out lines that are clearly section sub-headers or
            # cross-references (term column is all-uppercase short, etc.)
            if len(term) < 2 or term.lower() == "term":
                continue
            if current:
                blocks.append(current)
            current = {"term": term, "lines": [body]}
            continue
        # Continuation: number + right-col body only
        m = CONT_LINE_RE.match(raw)
        if m and current is not None:
            current["lines"].append(m.group(1).strip())
            continue
        # Blank or other lines reset current paragraph but stay within the same term
        if not raw.strip():
            continue
    if current:
        blocks.append(current)

    out = []
    for b in blocks:
        if not b["term"] or not b["lines"]:
            continue
        definition = " ".join(b["lines"]).strip()
        # Pull out citation tags like [RFC2828], [X.812], etc.
        cites = re.findall(r"\[([^\]]+)\]", definition)
        notes = ""
        if cites:
            notes = "references: " + ", ".join(sorted(set(cites)))
        out.append({
            "term": b["term"],
            "definition": definition,
            "source_anchor": SOURCE_URL,
            "notes": notes,
        })
    return out


def write_md(terms):
    path = OUT_DIR / f"{PREFIX}.md"
    with open(path, "w") as f:
        f.write("# OASIS SAML V2.0 Security Glossary\n\n")
        f.write(f"Source: {SOURCE_URL}\n\n")
        f.write("License: OASIS IPR boilerplate — verbatim copy and explanatory derivative works permitted with attribution.\n\n")
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
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/phase4d/oasis-saml.pdf"
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
