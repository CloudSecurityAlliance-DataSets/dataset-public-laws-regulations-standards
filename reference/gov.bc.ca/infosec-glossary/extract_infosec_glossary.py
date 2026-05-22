#!/usr/bin/env python3
"""Parse the BC Government Information Security Glossary into per-term rows.

Source: https://www2.gov.bc.ca/gov/content/governments/services-for-government/
            information-management-technology/information-security/
            information-security-awareness/information-security-glossary

As of the extraction date the live BC URL refuses HTTP requests with empty
responses; the markdown was captured via the Internet Archive (Wayback
Machine snapshot, 2025-04-03).

Markdown structure (after HTML→markdown conversion):

    Each term-definition lives in a single paragraph that opens with a bold
    term label followed by a colon, then the definition prose. Patterns
    observed:

        **Term:** definition prose ...
        **Term****:** ...   (double-bold artifact from the source markup)
        **Term**(verb)**:** ...  (annotation between bold runs)

    Multi-line definitions are wrapped onto subsequent lines; a blank line
    separates entries.

Output: infosec-glossary-terms.{csv,json}
"""
import csv
import json
import re
from pathlib import Path


SOURCE_URL = ("https://www2.gov.bc.ca/gov/content/governments/services-for-government/"
              "information-management-technology/information-security/"
              "information-security-awareness/information-security-glossary")
HERE = Path(__file__).resolve().parent
MD_PATH = HERE / "infosec-glossary.md"

# Match "**Term:**" or "**Term****:**" or "**Term** (qualifier)**:**" at the
# start of a paragraph. The term itself is whatever sits between the leading
# `**` and the colon, with stray `**`/`*` markers cleaned out afterward.
TERM_RE = re.compile(
    r"^\*\*(?P<term>[^*\n][^\n]*?):\*\*\s*",
)
# Alternate: **Term****:** (closing `**` then opening `**` then colon)
TERM_RE_ALT = re.compile(
    r"^\*\*(?P<term>[^\n]+?)\*\*\*\*:\*\*\s*",
)


def normalize_term(s: str) -> str:
    # Strip stray ** and *(qualifier)* artifacts
    s = re.sub(r"\*\*+", "", s)
    s = re.sub(r"\\(.)", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    # Trailing/leading punctuation cleanup
    s = s.strip(":")
    return s.strip()


def normalize_definition(s: str) -> str:
    s = re.sub(r"\\(.)", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def main():
    md = MD_PATH.read_text(encoding="utf-8")
    # Split into paragraphs at blank lines.
    paragraphs = re.split(r"\n\s*\n", md)
    rows = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # Multiple terms can sit in one paragraph block separated by blank
        # lines that the wayback HTML serializer collapsed; try to split on
        # `\n\n\n` or on lines starting with **Term: but join the wrap.
        text = re.sub(r"\n(?!\*\*)", " ", para)
        text = re.sub(r"\s+", " ", text).strip()
        # Now `text` is one logical paragraph. It may contain multiple
        # term-definition pairs separated by `\n\n` in the original; after
        # collapsing they're all on one line. Split by the term-pattern.
        for chunk in re.split(r"(?=\*\*[^*\n][^\n]*?:\*\*)", text):
            chunk = chunk.strip()
            if not chunk:
                continue
            m = TERM_RE_ALT.match(chunk) or TERM_RE.match(chunk)
            if not m:
                continue
            term = normalize_term(m.group("term"))
            definition = normalize_definition(chunk[m.end():])
            if not term or not definition:
                continue
            # Filter out probable non-glossary captures (very short or
            # paragraph-fragment terms)
            if len(term) > 120 or len(definition) < 5:
                continue
            rows.append({
                "term": term,
                "definition": definition,
                "source_anchor": SOURCE_URL,
                "notes": "",
            })

    # Deduplicate by (term, definition)
    seen = set()
    unique = []
    for r in rows:
        key = (r["term"], r["definition"][:60])
        if key in seen: continue
        seen.add(key)
        unique.append(r)
    rows = unique

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
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    main()
