#!/usr/bin/env python3
"""Extract the MITRE CWE Glossary into structured term/definition CSV/JSON.

Source: https://cwe.mitre.org/documents/glossary/
License: MITRE CWE Terms of Use (royalty-free use with attribution)

The page lists CWE-specific terminology (e.g. "Weakness", "Vulnerability",
"View", "Category", "Mapping_Notes") as a sequence of <h3> headings, each
followed by paragraph(s) of definition text and a "Back to top" link, and
then an <hr/> separator.

Each term has an <a name="..."></a> anchor (either inside the <h3> or
adjacent to it) whose name attribute matches the term itself (spaces
preserved). The fragment href on this page therefore uses the term name
as the anchor.

Outputs (written next to this script):
  - cwe-glossary.md
  - cwe-glossary-terms.csv  (header: term,definition,source_anchor,notes)
  - cwe-glossary-terms.json
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

SOURCE_URL = "https://cwe.mitre.org/documents/glossary/"
HERE = Path(__file__).resolve().parent


def fetch(url: str) -> str:
    resp = requests.get(url, timeout=60, headers={"User-Agent": "CSA-DataSets/1.0 (+https://cloudsecurityalliance.org)"})
    resp.raise_for_status()
    return resp.text


def _anchor_for(h3: Tag) -> str:
    """Return the anchor name for a term heading.

    Strategy: look for an <a name="..."> inside the <h3>, then adjacent
    in the previous sibling if not present. Fall back to the heading text.
    """
    a = h3.find("a", attrs={"name": True})
    if a and a.get("name"):
        return a["name"].strip()
    # try previous sibling
    prev = h3.find_previous_sibling()
    if isinstance(prev, Tag):
        a = prev.find("a", attrs={"name": True}) if prev.name != "a" else prev
        if isinstance(a, Tag) and a.get("name"):
            return a["name"].strip()
    return h3.get_text(strip=True)


def _term_text(h3: Tag) -> str:
    txt = h3.get_text(" ", strip=True)
    # strip "Back to top" if it leaked in (shouldn't, but defensive)
    txt = re.sub(r"\s*Back to top\s*$", "", txt, flags=re.IGNORECASE)
    return txt.strip()


def _collect_definition(h3: Tag) -> str:
    """Walk siblings after the <h3> until the next <h3> or <hr>, collecting text."""
    parts: list[str] = []
    for sib in h3.next_siblings:
        if isinstance(sib, NavigableString):
            s = str(sib).strip()
            if s:
                parts.append(s)
            continue
        if not isinstance(sib, Tag):
            continue
        name = sib.name.lower()
        if name == "h3":
            break
        if name == "hr":
            break
        # skip the "Back to top" navigation paragraph
        if name == "p":
            txt = sib.get_text(" ", strip=True).lower()
            if txt == "back to top":
                continue
        text = sib.get_text(" ", strip=True)
        # strip stray trailing "Back to top" inside the text
        text = re.sub(r"\s*Back to top\s*$", "", text, flags=re.IGNORECASE).strip()
        if text:
            parts.append(text)
    # collapse whitespace
    out = "\n\n".join(p for p in (re.sub(r"\s+", " ", x).strip() for x in parts) if p)
    return out.strip()


def parse(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    terms: list[dict] = []
    seen: set[str] = set()
    for h3 in soup.find_all("h3"):
        term = _term_text(h3)
        if not term:
            continue
        # skip page-header noise like a possible "Glossary" heading without body
        anchor = _anchor_for(h3)
        definition = _collect_definition(h3)
        if not definition:
            # likely a section header, not a glossary entry
            continue
        key = term.lower()
        if key in seen:
            continue
        seen.add(key)
        terms.append(
            {
                "term": term,
                "definition": definition,
                "source_anchor": f"{SOURCE_URL}#{quote(anchor, safe='')}",
                "notes": "",
            }
        )
    return terms


def write_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_json(rows: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def write_md(rows: list[dict], path: Path) -> None:
    lines: list[str] = []
    lines.append("# MITRE CWE Glossary")
    lines.append("")
    lines.append(f"Source: <{SOURCE_URL}>")
    lines.append("")
    lines.append(f"License: MITRE CWE Terms of Use (royalty-free use with attribution).")
    lines.append("")
    lines.append(f"Total terms: **{len(rows)}**")
    lines.append("")
    lines.append("---")
    lines.append("")
    for r in rows:
        lines.append(f"## {r['term']}")
        lines.append("")
        for para in r["definition"].split("\n\n"):
            lines.append(para)
            lines.append("")
        lines.append(f"Source: <{r['source_anchor']}>")
        lines.append("")
        lines.append("---")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    html = fetch(SOURCE_URL)
    rows = parse(html)
    if not rows:
        print("ERROR: no terms parsed", file=sys.stderr)
        return 1
    write_csv(rows, HERE / "cwe-glossary-terms.csv")
    write_json(rows, HERE / "cwe-glossary-terms.json")
    write_md(rows, HERE / "cwe-glossary.md")
    print(f"Extracted {len(rows)} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
