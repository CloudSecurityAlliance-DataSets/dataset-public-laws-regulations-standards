#!/usr/bin/env python3
"""Extract the CISA NICCS Cybersecurity Glossary.

Source: https://niccs.cisa.gov/resources/glossary

The glossary lives on a single static HTML page (~500 terms). Terms are
grouped into alphabetic sections (``<div class="letter-X termset">``), and
each term is a USWDS accordion under that letter. The page also exposes
an authoritative CSV download at ``/rest/vocab/export-csv`` with these
columns (the first 7 are machine field IDs and are empty; the last 6 are
the human-labelled fields):

    Term,
    field_acronym_expansion, field_definition, field_extended_definition,
    field_related_term_s_, field_synonym_s_, field_from,
    Acronym Expansion, Definition, Extended Definition,
    Related Term(s), Synonym(s), From

This extractor uses the official CSV as the canonical source of term data
and supplements it with the HTML page only to discover each term's letter
section (used to build the ``source_anchor`` URL fragment, e.g.
``#letter-a``).

Outputs:
  - niccs-glossary.md             - human-readable A-Z markdown
  - niccs-glossary-terms.csv      - {term, definition, source_anchor, notes}
  - niccs-glossary-terms.json     - rich record per term (all fields)
"""
from __future__ import annotations

import csv
import html as html_lib
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIRNAME = "niccs-glossary"

SOURCE_PAGE = "https://niccs.cisa.gov/resources/glossary"
CSV_URL = "https://niccs.cisa.gov/rest/vocab/export-csv"

OUT_MD = HERE / f"{DIRNAME}.md"
OUT_CSV = HERE / f"{DIRNAME}-terms.csv"
OUT_JSON = HERE / f"{DIRNAME}-terms.json"
CACHE_DIR = HERE / "_source_pages"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch(url: str, cache_name: str) -> str:
    CACHE_DIR.mkdir(exist_ok=True)
    cache = CACHE_DIR / cache_name
    if cache.exists():
        return cache.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
        body = resp.read().decode("utf-8")
    cache.write_text(body, encoding="utf-8")
    return body


def slugify(s: str) -> str:
    """Approximate the Drupal slug used in element ids.

    Drupal's pathauto produces ``access-and-identity-management`` from
    ``Access and Identity Management``. The accordion ids follow that
    pattern: ``<slug>-accordion``. We do not actually rely on slug
    matching for term content (the CSV is authoritative), only to build
    a stable source_anchor URL.
    """
    s = s.lower()
    # Replace anything that's not a-z/0-9 with a hyphen, collapse runs.
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def parse_letter_sections(html: str) -> dict[str, str]:
    """Map term (lowercased, normalized) -> letter ('a'..'z').

    Walks each ``<div class="letter-X termset">`` block and grabs the
    visible heading text from each accordion button
    (``<div class="text">...</div>``).
    """
    term_to_letter: dict[str, str] = {}
    # A section runs until the next ``letter-X termset`` opens or until the
    # end of the document — the page has no explicit terminator class after
    # the last letter section (letter-x).
    section_re = re.compile(
        r'<div class="letter-([a-z])\s+termset">(.*?)(?=<div class="letter-[a-z]\s+termset">|\Z)',
        re.DOTALL,
    )
    button_re = re.compile(
        r'<button[^>]*class="usa-accordion__button"[^>]*>.*?<div class="text">(.*?)</div>',
        re.DOTALL,
    )
    for sec in section_re.finditer(html):
        letter = sec.group(1)
        block = sec.group(2)
        for btn in button_re.finditer(block):
            term = re.sub(r"\s+", " ", btn.group(1)).strip()
            # Strip any HTML that snuck in, then decode entities (&amp;, &nbsp;, ...)
            term = re.sub(r"<[^>]+>", "", term)
            term = html_lib.unescape(term)
            if term:
                term_to_letter[term.casefold()] = letter
    return term_to_letter


def load_csv(text: str) -> list[dict]:
    rdr = csv.DictReader(io.StringIO(text))
    rows = []
    for row in rdr:
        term = (row.get("Term") or "").strip()
        if not term:
            continue
        rows.append(
            {
                "term": term,
                "acronym_expansion": (row.get("Acronym Expansion") or "").strip(),
                "definition": (row.get("Definition") or "").strip(),
                "extended_definition": (row.get("Extended Definition") or "").strip(),
                "related_terms": (row.get("Related Term(s)") or "").strip(),
                "synonyms": (row.get("Synonym(s)") or "").strip(),
                "from": (row.get("From") or "").strip(),
            }
        )
    return rows


def build_notes(rec: dict) -> str:
    parts = []
    if rec["acronym_expansion"]:
        parts.append(f"Acronym Expansion: {rec['acronym_expansion']}")
    if rec["extended_definition"]:
        parts.append(f"Extended Definition: {rec['extended_definition']}")
    if rec["related_terms"]:
        parts.append(f"Related Term(s): {rec['related_terms']}")
    if rec["synonyms"]:
        parts.append(f"Synonym(s): {rec['synonyms']}")
    if rec["from"]:
        parts.append(f"From: {rec['from']}")
    return " | ".join(parts)


def main() -> int:
    print(f"Fetching {SOURCE_PAGE}", file=sys.stderr)
    html = fetch(SOURCE_PAGE, "glossary.html")
    print(f"Fetching {CSV_URL}", file=sys.stderr)
    csv_text = fetch(CSV_URL, "glossary.csv")

    term_to_letter = parse_letter_sections(html)
    print(f"Parsed {len(term_to_letter)} terms from HTML letter sections", file=sys.stderr)

    records = load_csv(csv_text)
    print(f"Parsed {len(records)} terms from CSV", file=sys.stderr)

    # Enrich each record with source_anchor and notes
    missing_letter = 0
    for rec in records:
        letter = term_to_letter.get(rec["term"].casefold())
        if letter is None:
            # Fall back to first character of the term
            first = rec["term"][:1].lower()
            letter = first if first.isalpha() else None
            missing_letter += 1
        rec["source_anchor"] = (
            f"{SOURCE_PAGE}#letter-{letter}" if letter else SOURCE_PAGE
        )
        rec["notes"] = build_notes(rec)
    if missing_letter:
        print(
            f"Note: {missing_letter} term(s) not matched to HTML letter section; used first-letter fallback",
            file=sys.stderr,
        )

    # Stable order: by term, case-insensitive
    records.sort(key=lambda r: r["term"].casefold())

    # --- Write CSV (per spec: term, definition, source_anchor, notes) ---
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["term", "definition", "source_anchor", "notes"])
        for rec in records:
            w.writerow(
                [rec["term"], rec["definition"], rec["source_anchor"], rec["notes"]]
            )

    # --- Write JSON (rich) ---
    json_records = []
    for rec in records:
        json_records.append(
            {
                "term": rec["term"],
                "acronym_expansion": rec["acronym_expansion"],
                "definition": rec["definition"],
                "extended_definition": rec["extended_definition"],
                "related_terms": rec["related_terms"],
                "synonyms": rec["synonyms"],
                "from": rec["from"],
                "source_anchor": rec["source_anchor"],
            }
        )
    OUT_JSON.write_text(
        json.dumps(json_records, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # --- Write Markdown ---
    lines: list[str] = []
    lines.append("# NICCS Cybersecurity Glossary (CISA)")
    lines.append("")
    lines.append(f"Source: <{SOURCE_PAGE}>")
    lines.append("")
    lines.append(f"CSV export: <{CSV_URL}>")
    lines.append("")
    lines.append(f"Extracted {len(records)} terms.")
    lines.append("")

    current_letter = None
    for rec in records:
        first = rec["term"][:1].upper()
        if first != current_letter:
            current_letter = first
            lines.append("")
            lines.append(f"## {current_letter}")
            lines.append("")
        lines.append(f"### {rec['term']}")
        lines.append("")
        if rec["acronym_expansion"]:
            lines.append(f"**Acronym Expansion:** {rec['acronym_expansion']}")
            lines.append("")
        if rec["definition"]:
            lines.append(rec["definition"])
            lines.append("")
        if rec["extended_definition"]:
            lines.append(f"**Extended Definition:** {rec['extended_definition']}")
            lines.append("")
        if rec["related_terms"]:
            lines.append(f"**Related Term(s):** {rec['related_terms']}")
            lines.append("")
        if rec["synonyms"]:
            lines.append(f"**Synonym(s):** {rec['synonyms']}")
            lines.append("")
        if rec["from"]:
            lines.append(f"**From:** {rec['from']}")
            lines.append("")

    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(f"Wrote {OUT_MD}", file=sys.stderr)
    print(f"Wrote {OUT_CSV}", file=sys.stderr)
    print(f"Wrote {OUT_JSON}", file=sys.stderr)
    print(f"TERM_COUNT: {len(records)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
