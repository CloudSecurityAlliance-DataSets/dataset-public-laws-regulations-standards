#!/usr/bin/env python3
"""Extract glossary terms for the AWS Well-Architected Security Pillar glossary.

Source state (verified 2026-05):
    The AWS Well-Architected Security Pillar glossary page at
    https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/glossary.html
    is now a redirect notice pointing at the unified AWS Glossary Reference. The
    same is true of the glossary section of the AWS Overview Whitepaper
    (https://docs.aws.amazon.com/whitepapers/latest/aws-overview/glossary.html).

    The canonical destination is the unified AWS Glossary, which AWS publishes
    in both HTML and markdown:

        HTML: https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.html
        MD:   https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.md

    This extractor fetches the markdown and parses the per-term blocks.

Markdown structure:

    **term name (acronym)**<a name="anchor"></a>
    Definition prose, possibly multi-line, ending at the next blank line or
    the next **term** entry. Section headers like '### Numbers and symbols'
    delimit alphabetical bands and are skipped.

Output: wellarchitected-security-glossary-terms.{csv,json} — schema:
    term            human-readable term (with parenthesized acronym if present)
    definition      prose definition (whitespace-normalized)
    source_anchor   absolute URL to the anchor on the source page
    notes           empty (kept for schema compatibility)
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

import requests

SOURCE_URL_HTML = "https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.html"
SOURCE_URL_MD = "https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.md"

HERE = Path(__file__).resolve().parent
MD_PATH = HERE / "wellarchitected-security-glossary.md"

TERM_RE = re.compile(
    r"^\*\*(?P<term>.+?)\*\*<a\s+name=\"(?P<anchor>[^\"]+)\">"
)


def fetch_markdown() -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        )
    }
    r = requests.get(SOURCE_URL_MD, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def parse_terms(md_text: str) -> List[Dict[str, str]]:
    lines = md_text.splitlines()
    rows: List[Dict[str, str]] = []
    i = 0
    while i < len(lines):
        m = TERM_RE.match(lines[i])
        if not m:
            i += 1
            continue
        term = m.group("term").strip()
        anchor = m.group("anchor").strip()
        # Collect definition lines until next term/section header.
        defn_lines: List[str] = []
        j = i + 1
        while j < len(lines):
            ln = lines[j]
            stripped = ln.strip()
            if not stripped:
                # Blank line — peek ahead. If next non-blank is a new term or
                # section heading, stop. Otherwise allow the definition to
                # continue across the blank line.
                k = j + 1
                while k < len(lines) and not lines[k].strip():
                    k += 1
                if k >= len(lines):
                    break
                nxt = lines[k]
                if (TERM_RE.match(nxt)
                        or nxt.startswith("### ")
                        or nxt.startswith("# ")):
                    break
                defn_lines.append("")
                j = k
                continue
            if TERM_RE.match(ln):
                break
            if ln.startswith("### ") or ln.startswith("# "):
                break
            defn_lines.append(stripped)
            j += 1

        definition = " ".join(s for s in defn_lines if s)
        definition = re.sub(r"\s+", " ", definition).strip()
        rows.append({
            "term": term,
            "definition": definition,
            "source_anchor": f"{SOURCE_URL_HTML}#{anchor}",
            "notes": "",
        })
        i = j
    return rows


def write_outputs(terms: List[Dict[str, str]]) -> None:
    stem = HERE.name
    csv_path = HERE / f"{stem}-terms.csv"
    json_path = HERE / f"{stem}-terms.json"
    fields = ["term", "definition", "source_anchor", "notes"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(terms)
    json_path.write_text(json.dumps(terms, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {csv_path.name}, {json_path.name}")


def main() -> int:
    # Prefer the local markdown if present (offline-friendly); otherwise fetch.
    if MD_PATH.exists():
        md_text = MD_PATH.read_text(encoding="utf-8")
    else:
        md_text = fetch_markdown()
        MD_PATH.write_text(md_text, encoding="utf-8")
    terms = parse_terms(md_text)
    n_with_def = sum(1 for r in terms if r["definition"])
    print(f"Terms: {len(terms)}  ({n_with_def} with definition text)")
    write_outputs(terms)
    return 0


if __name__ == "__main__":
    sys.exit(main())
