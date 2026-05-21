#!/usr/bin/env python3
"""Extract RFC 4949 Internet Security Glossary v2 into structured CSV/JSON/MD.

Source: https://www.rfc-editor.org/rfc/rfc4949.txt (plain text RFC)

Term entries look like:

       $ Term name
          (I)  Definition body, possibly multiple paragraphs and lines.
               Continues with hanging indent.
       $ Next term
          (D)  ...

The (I)/(D)/(O)/(N) tag at the start of the body identifies the
recommendation type:
  (I) Recommended definition of first choice
  (N) Recommended only as a non-Internet definition
  (O) Other definition - additional information without recommendation
  (D) Deprecated - SHOULD NOT be used

Section 4 ("Definitions") contains the dictionary; section 5+ is back matter.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import urllib.request
from pathlib import Path

RFC_URL = "https://www.rfc-editor.org/rfc/rfc4949.txt"
HERE = Path(__file__).resolve().parent
BASENAME = "rfc4949-internet-security-glossary"

# Pattern for page-break footer / header lines that appear every ~58 lines.
# Footer: "Shirey                       Informational                      [Page N]"
# Header: "RFC 4949         Internet Security Glossary, Version 2       August 2007"
PAGE_FOOTER_RE = re.compile(r"^\s*Shirey\s+Informational\s+\[Page\s+\d+\]\s*$")
PAGE_HEADER_RE = re.compile(r"^RFC 4949\s+Internet Security Glossary, Version 2\s+August 2007\s*$")

# Lines that mark a new term begin with three spaces then "$ " then the term.
TERM_RE = re.compile(r"^   \$ (.+)$")

# Recommendation-tag prefix on a definition body.
TAG_RE = re.compile(r"^\s*\(([INDO])\)\s*")


def fetch_source(cache: Path) -> str:
    if cache.exists():
        return cache.read_text(encoding="utf-8", errors="replace")
    with urllib.request.urlopen(RFC_URL) as resp:
        data = resp.read().decode("utf-8", errors="replace")
    cache.write_text(data, encoding="utf-8")
    return data


def strip_page_breaks(lines: list[str]) -> list[str]:
    """Remove RFC page footers/headers and the blank lines that surround them.

    A page break looks like:
        <blank>
        <blank>
        <blank>
        Shirey                       Informational                      [Page N]
        <form-feed or blank>
        RFC 4949 ... August 2007
        <blank>
        <blank>
    """
    out: list[str] = []
    for line in lines:
        # Form-feed character if present
        line = line.replace("\f", "")
        if PAGE_FOOTER_RE.match(line) or PAGE_HEADER_RE.match(line):
            continue
        out.append(line)
    return out


def slice_definitions(lines: list[str]) -> list[str]:
    """Return only the lines inside section 4 ("Definitions"), exclusive of sec 5+."""
    start = end = None
    for i, line in enumerate(lines):
        if line.startswith("4. Definitions"):
            start = i + 1
        elif start is not None and line.startswith("5. Security Considerations"):
            end = i
            break
    if start is None or end is None:
        raise RuntimeError("Could not locate section 4/5 boundaries")
    return lines[start:end]


def parse_terms(lines: list[str]) -> list[dict]:
    terms: list[dict] = []
    current_term: str | None = None
    current_body: list[str] = []

    def flush():
        if current_term is None:
            return
        # Strip leading 6-space hanging indent from every body line, then
        # collapse trailing whitespace and excess blank lines.
        body_lines = []
        for bl in current_body:
            if bl.startswith("      "):
                body_lines.append(bl[6:])
            else:
                body_lines.append(bl.lstrip())
        # Collapse runs of blank lines.
        cleaned: list[str] = []
        prev_blank = False
        for bl in body_lines:
            is_blank = not bl.strip()
            if is_blank and prev_blank:
                continue
            cleaned.append(bl.rstrip())
            prev_blank = is_blank
        while cleaned and not cleaned[0].strip():
            cleaned.pop(0)
        while cleaned and not cleaned[-1].strip():
            cleaned.pop()

        raw = "\n".join(cleaned).strip()

        # Identify the recommendation tag if present.
        tag = ""
        m = TAG_RE.match(raw)
        if m:
            tag = m.group(1)  # I, N, D, or O

        # The definition keeps the tag inline (it carries semantic weight),
        # but we also surface it in the notes field for filtering.
        notes_bits: list[str] = []
        if tag:
            tag_label = {
                "I": "Recommended (Internet)",
                "N": "Recommended (Non-Internet)",
                "O": "Other (non-recommendation)",
                "D": "Deprecated",
            }.get(tag, tag)
            notes_bits.append(f"tag=({tag}) {tag_label}")

        anchor = "rfc4949-section-4-" + re.sub(r"[^a-z0-9]+", "-", current_term.lower()).strip("-")
        terms.append({
            "term": current_term,
            "definition": raw,
            "source_anchor": anchor,
            "notes": "; ".join(notes_bits),
        })

    for line in lines:
        m = TERM_RE.match(line)
        if m:
            flush()
            raw_term = m.group(1).strip()
            # Pattern: "$ accounting See: COMSEC accounting." — the body is on
            # the same line as the term. Split it into term + inline definition.
            inline = re.match(r"^(.+?)\s+(See:\s+.+\.)$", raw_term)
            if inline:
                current_term = inline.group(1).strip()
                current_body = ["      " + inline.group(2)]
            else:
                current_term = raw_term
                current_body = []
        else:
            if current_term is not None:
                current_body.append(line)
    flush()

    # Pattern: paired sibling terms like
    #   $ Diffie-Hellman
    #   $ Diffie-Hellman-Merkle
    #     (N) A key-agreement algorithm...
    # The first term ends up with an empty body; copy the next term's body and
    # annotate the notes field.
    for i, t in enumerate(terms):
        if t["definition"] or i + 1 >= len(terms):
            continue
        next_t = terms[i + 1]
        if not next_t["definition"]:
            continue
        t["definition"] = next_t["definition"]
        sibling_note = f"shared definition with \"{next_t['term']}\""
        t["notes"] = "; ".join(filter(None, [t["notes"], sibling_note]))
        next_sibling_note = f"shared definition with \"{t['term']}\""
        next_t["notes"] = "; ".join(filter(None, [next_t["notes"], next_sibling_note]))

    return terms


def write_outputs(terms: list[dict]) -> None:
    # CSV
    csv_path = HERE / f"{BASENAME}-terms.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        for t in terms:
            w.writerow(t)

    # JSON
    json_path = HERE / f"{BASENAME}-terms.json"
    json_path.write_text(json.dumps(terms, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Markdown
    md_path = HERE / f"{BASENAME}.md"
    lines: list[str] = []
    lines.append("# RFC 4949 - Internet Security Glossary, Version 2")
    lines.append("")
    lines.append("Source: https://www.rfc-editor.org/rfc/rfc4949.txt")
    lines.append("")
    lines.append(f"Total terms extracted: {len(terms)}")
    lines.append("")
    lines.append("Recommendation tags used by the RFC:")
    lines.append("")
    lines.append("- `(I)` Recommended definition of first choice (Internet)")
    lines.append("- `(N)` Recommended only as a non-Internet definition")
    lines.append("- `(O)` Other definition - background information without a recommendation")
    lines.append("- `(D)` Deprecated - SHOULD NOT be used")
    lines.append("")
    lines.append("## Terms")
    lines.append("")
    for t in terms:
        lines.append(f"### {t['term']}")
        lines.append("")
        lines.append(t["definition"])
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    cache = HERE / "rfc4949.txt"
    raw = fetch_source(cache)
    all_lines = raw.splitlines()
    cleaned = strip_page_breaks(all_lines)
    section_lines = slice_definitions(cleaned)
    terms = parse_terms(section_lines)

    # Sanity check.
    if len(terms) < 100:
        raise RuntimeError(f"Parsed only {len(terms)} terms; structure likely misidentified.")
    if any(not t["definition"] for t in terms):
        empties = [t["term"] for t in terms if not t["definition"]]
        raise RuntimeError(f"Empty definitions for: {empties[:5]} ({len(empties)} total)")

    write_outputs(terms)
    print(f"Extracted {len(terms)} terms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
