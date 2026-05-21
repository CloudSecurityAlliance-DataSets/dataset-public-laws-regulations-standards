#!/usr/bin/env python3
"""Extract the California SAM 5300 Technical Definitions glossary.

Source: https://www.cdt.ca.gov/security/technical-definitions/

The source page is structured as one <dl> per letter section, each preceded
by an <h5> heading containing the section letter. Within a <dl>, terms appear
as <dt> elements with their definitions in the following <dd>. Some entries
have an extra trailing <dd> with continuation text; we fold any continuation
<dd>s into the preceding term's definition.

Outputs (next to this script):
    sam-5300-definitions.md
    sam-5300-definitions-terms.csv  (term,definition,source_anchor,notes)
    sam-5300-definitions-terms.json
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag

SOURCE_URL = "https://www.cdt.ca.gov/security/technical-definitions/"
USER_AGENT = "CSA-Dataset-Bot/1.0 (+https://cloudsecurityalliance.org)"

HERE = Path(__file__).resolve().parent
MD_OUT = HERE / "sam-5300-definitions.md"
CSV_OUT = HERE / "sam-5300-definitions-terms.csv"
JSON_OUT = HERE / "sam-5300-definitions-terms.json"


def fetch_html(url: str = SOURCE_URL) -> str:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=60)
    resp.raise_for_status()
    return resp.text


def normalize_text(text: str) -> str:
    """Collapse whitespace, normalize curly quotes, trim."""
    text = text.replace(" ", " ")
    # Curly quotes / dashes left as-is (preserve source fidelity), just whitespace cleanup.
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_terms(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    terms: list[dict] = []

    for dl in soup.find_all("dl"):
        # Find the section letter from the nearest preceding heading.
        heading = dl.find_previous(["h1", "h2", "h3", "h4", "h5", "h6"])
        letter = ""
        if heading is not None:
            letter = heading.get_text(strip=True)[:1].upper()

        current: dict | None = None
        for child in dl.children:
            if not isinstance(child, Tag):
                continue
            if child.name == "dt":
                if current is not None:
                    terms.append(current)
                term_text = normalize_text(child.get_text(" ", strip=True))
                # Anchor: SAM 5300 page is a single page with no per-term anchors,
                # so use the letter section.
                anchor = f"{SOURCE_URL}#{letter}" if letter else SOURCE_URL
                current = {
                    "term": term_text,
                    "definition": "",
                    "source_anchor": anchor,
                    "notes": "",
                    "_letter": letter,
                }
            elif child.name == "dd":
                dd_text = normalize_text(child.get_text(" ", strip=True))
                if current is None:
                    # Orphan dd before any dt; skip.
                    continue
                if not dd_text:
                    # Empty trailing dd — ignore.
                    continue
                if current["definition"]:
                    # Continuation paragraph: join with a space (track in notes).
                    current["definition"] = (
                        current["definition"] + " " + dd_text
                    ).strip()
                    note = "multi-paragraph definition"
                    if note not in current["notes"]:
                        current["notes"] = note
                else:
                    current["definition"] = dd_text
        if current is not None:
            terms.append(current)

    return terms


def write_csv(terms: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, quoting=csv.QUOTE_ALL)
        writer.writerow(["term", "definition", "source_anchor", "notes"])
        for t in terms:
            writer.writerow(
                [t["term"], t["definition"], t["source_anchor"], t["notes"]]
            )


def write_json(terms: list[dict], path: Path) -> None:
    payload = [
        {
            "term": t["term"],
            "definition": t["definition"],
            "source_anchor": t["source_anchor"],
            "notes": t["notes"],
        }
        for t in terms
    ]
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def write_md(terms: list[dict], path: Path) -> None:
    lines: list[str] = []
    lines.append("# California SAM 5300 Technical Definitions")
    lines.append("")
    lines.append(f"Source: <{SOURCE_URL}>")
    lines.append("")
    lines.append(
        "Glossary of technical definitions accompanying the State Administrative "
        "Manual (SAM) Sections 5300 et seq., as published by the California "
        "Department of Technology (CDT)."
    )
    lines.append("")
    lines.append(f"Term count: **{len(terms)}**")
    lines.append("")

    current_letter = ""
    for t in terms:
        letter = t.get("_letter", "") or t["term"][:1].upper()
        if letter != current_letter:
            current_letter = letter
            lines.append(f"## {letter}")
            lines.append("")
        lines.append(f"**{t['term']}**")
        lines.append("")
        lines.append(t["definition"])
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    html = fetch_html()
    terms = parse_terms(html)
    if not terms:
        raise RuntimeError("No terms parsed; source structure may have changed.")
    write_md(terms, MD_OUT)
    write_csv(terms, CSV_OUT)
    write_json(terms, JSON_OUT)
    print(f"Extracted {len(terms)} terms")
    print(f"  -> {MD_OUT}")
    print(f"  -> {CSV_OUT}")
    print(f"  -> {JSON_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
