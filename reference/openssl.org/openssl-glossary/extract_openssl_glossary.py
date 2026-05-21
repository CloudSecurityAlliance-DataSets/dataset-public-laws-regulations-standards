#!/usr/bin/env python3
"""Extract the OpenSSL Glossary into structured term/definition form.

Source: https://docs.openssl.org/3.0/man7/openssl-glossary/
License of source content: Apache-2.0

Page structure: the DESCRIPTION section contains a single <ul> whose direct
<li> children are one-glossary-entry each. Within each <li>, the first <p>
holds the term (which can contain commas or parenthesized expansions, e.g.
"DER (\"Distinguished Encoding Rules\")"), and the remaining <p> tags hold
the definition body. Cross-reference links live as <a href=...> inside the
later <p> tags. There is no per-term anchor id in the source HTML -- the only
anchor on the page is #description -- so we synthesize a stable slug from the
term and record it in the `source_anchor` column as `#description-<slug>` to
make round-tripping unambiguous.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

SOURCE_URL = "https://docs.openssl.org/3.0/man7/openssl-glossary/"
OUT_DIR = Path(__file__).resolve().parent
MD_PATH = OUT_DIR / "openssl-glossary.md"
CSV_PATH = OUT_DIR / "openssl-glossary-terms.csv"
JSON_PATH = OUT_DIR / "openssl-glossary-terms.json"


def slugify(term: str) -> str:
    s = term.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def p_to_text(p: Tag) -> str:
    """Flatten a <p> to plain text while preserving link URLs in-line."""
    parts: list[str] = []
    for node in p.descendants:
        if isinstance(node, NavigableString):
            # Skip strings that live inside <a> tags -- handled when we visit
            # the <a> itself, to avoid duplicating the anchor text.
            if node.parent and node.parent.name == "a":
                continue
            parts.append(str(node))
        elif isinstance(node, Tag) and node.name == "a":
            text = node.get_text(" ", strip=True)
            href = node.get("href", "")
            if href and href != text:
                parts.append(f"{text} ({href})")
            else:
                parts.append(text)
    text = "".join(parts)
    return re.sub(r"\s+", " ", text).strip()


def extract_entries(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    desc_h2 = soup.find("h2", id="description")
    if desc_h2 is None:
        raise RuntimeError("Could not find <h2 id=description> on the page")

    # Walk forward to find the <ul> that holds the entries.
    ul = desc_h2.find_next("ul")
    if ul is None:
        raise RuntimeError("Could not find the glossary <ul> after DESCRIPTION")

    entries: list[dict] = []
    for li in ul.find_all("li", recursive=False):
        paragraphs = li.find_all("p", recursive=False)
        if not paragraphs:
            continue
        term = re.sub(r"\s+", " ", paragraphs[0].get_text(" ", strip=True)).strip()
        if not term:
            continue
        body_parts = [p_to_text(p) for p in paragraphs[1:]]
        body_parts = [b for b in body_parts if b]
        definition = "\n\n".join(body_parts)

        # Collect cross-reference links found anywhere after the first <p>.
        notes_links: list[str] = []
        for p in paragraphs[1:]:
            for a in p.find_all("a"):
                href = a.get("href", "")
                if not href:
                    continue
                # Resolve relative man-page links to absolute URLs for notes.
                if href.startswith(("http://", "https://")):
                    notes_links.append(href)
                else:
                    notes_links.append(href)
        notes = "; ".join(dict.fromkeys(notes_links))  # de-dup, keep order

        entries.append(
            {
                "term": term,
                "definition": definition,
                "source_anchor": f"#description-{slugify(term)}",
                "notes": notes,
            }
        )
    return entries


def write_csv(entries: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["term", "definition", "source_anchor", "notes"]
        )
        writer.writeheader()
        for row in entries:
            writer.writerow(row)


def write_json(entries: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_markdown(entries: list[dict], path: Path) -> None:
    lines: list[str] = []
    lines.append("# OpenSSL Glossary")
    lines.append("")
    lines.append(f"Source: {SOURCE_URL}")
    lines.append("")
    lines.append("License of source content: Apache-2.0")
    lines.append("")
    lines.append(f"Term count: {len(entries)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    for e in entries:
        lines.append(f"## {e['term']}")
        lines.append("")
        if e["definition"]:
            lines.append(e["definition"])
            lines.append("")
        if e["notes"]:
            lines.append(f"See also: {e['notes']}")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    resp = requests.get(SOURCE_URL, timeout=30)
    resp.raise_for_status()
    entries = extract_entries(resp.text)
    if not entries:
        raise RuntimeError("No glossary entries extracted")
    write_csv(entries, CSV_PATH)
    write_json(entries, JSON_PATH)
    write_markdown(entries, MD_PATH)
    print(f"Extracted {len(entries)} terms")
    print(f"  CSV:  {CSV_PATH}")
    print(f"  JSON: {JSON_PATH}")
    print(f"  MD:   {MD_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
