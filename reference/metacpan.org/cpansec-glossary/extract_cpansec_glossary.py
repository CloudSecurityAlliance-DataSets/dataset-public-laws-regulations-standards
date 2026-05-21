#!/usr/bin/env python3
"""Extract the CPAN Security Group (CPANSec) Glossary into structured form.

Source: https://security.metacpan.org/docs/glossary.html
License: CC-BY-SA-4.0 (declared on the source page)

The page is Jekyll-rendered. Glossary terms live between the
``<h2 id="glossary">`` and ``<h2 id="references-and-terms">`` anchors.
Each term is an ``<h3>`` (main term) or ``<h4>`` (subtype) with an ``id``
attribute. The body of a term entry is the run of sibling elements that
follows it until the next ``<h2>``/``<h3>``/``<h4>``. Definitions are
typically inside an ``<ol>``; additional commentary may live in a
``<div class="markdown-alert">`` (notes/warnings) or a trailing ``<p>``
with a ``(Ref: ...)`` citation.

Outputs (in this directory):
    cpansec-glossary.md
    cpansec-glossary-terms.csv  (header: term,definition,source_anchor,notes)
    cpansec-glossary-terms.json
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

SOURCE_URL = "https://security.metacpan.org/docs/glossary.html"
OUT_DIR = Path(__file__).resolve().parent

TERM_TAGS = {"h3", "h4"}
STOP_TAGS = {"h1", "h2", "h3", "h4"}


def fetch_html() -> str:
    resp = requests.get(SOURCE_URL, timeout=60)
    resp.raise_for_status()
    return resp.text


def clean_text(s: str) -> str:
    """Collapse whitespace and trim."""
    return re.sub(r"\s+", " ", s).strip()


def term_name(heading: Tag) -> str:
    """Term name with marker emojis (warning/edit) stripped."""
    raw = heading.get_text(" ", strip=True)
    # Strip the two annotation glyphs used by the page (warning, draft).
    raw = raw.replace("⚠️", "").replace("✍️", "")
    return clean_text(raw)


def collect_body(heading: Tag) -> list[Tag]:
    """Return the run of sibling elements that follow ``heading`` until
    the next heading at h1-h4 level.
    """
    body: list[Tag] = []
    for sib in heading.next_siblings:
        if isinstance(sib, NavigableString):
            continue
        if not isinstance(sib, Tag):
            continue
        if sib.name in STOP_TAGS:
            break
        body.append(sib)
    return body


def render_definition(body: list[Tag]) -> str:
    """Build a single text blob containing all numbered definitions from
    the ``<ol>`` blocks within the body. Sub-bullets are inlined.
    """
    parts: list[str] = []
    for el in body:
        if el.name != "ol":
            continue
        for li in el.find_all("li", recursive=False):
            parts.append(clean_text(li.get_text(" ", strip=True)))
    return " | ".join(parts) if parts else ""


def render_notes(body: list[Tag]) -> str:
    """Concatenate markdown-alert notes/warnings, See-also lists, and the
    trailing ``(Ref: ...)`` line into one ``notes`` field.
    """
    chunks: list[str] = []
    for el in body:
        cls = " ".join(el.get("class", []))
        if el.name == "div" and "markdown-alert" in cls:
            # Drop the SVG icon text; keep the body text.
            text = clean_text(el.get_text(" ", strip=True))
            if text:
                chunks.append(text)
        elif el.name == "ul":
            text = clean_text(el.get_text(" ", strip=True))
            if text:
                chunks.append(text)
        elif el.name == "p":
            text = clean_text(el.get_text(" ", strip=True))
            if text:
                chunks.append(text)
    return " || ".join(chunks)


def render_markdown_entry(name: str, anchor: str, level: int,
                          definition: str, notes: str) -> str:
    hashes = "#" * level  # h3 -> ###, h4 -> ####
    md = [f"{hashes} {name}", f"<a id=\"{anchor}\"></a>", ""]
    if definition:
        md.append(definition)
        md.append("")
    if notes:
        md.append(f"_Notes:_ {notes}")
        md.append("")
    return "\n".join(md)


def main() -> int:
    html = fetch_html()
    soup = BeautifulSoup(html, "html.parser")

    glossary_anchor = soup.find("h2", id="glossary")
    end_anchor = soup.find("h2", id="references-and-terms")
    if glossary_anchor is None or end_anchor is None:
        raise RuntimeError("Could not locate glossary section bounds in source page.")

    # Walk siblings from glossary_anchor to end_anchor in document order.
    rows: list[dict] = []
    md_blocks: list[str] = ["# CPAN Security Group (CPANSec) Glossary",
                            "",
                            f"Source: {SOURCE_URL}",
                            "License: CC-BY-SA-4.0",
                            ""]

    # Use find_all_next on the glossary_anchor to enumerate every h3/h4
    # between the two h2 anchors.
    for heading in glossary_anchor.find_all_next(["h2", "h3", "h4"]):
        if heading is end_anchor:
            break
        if heading.name == "h2":
            continue
        anchor = heading.get("id")
        if not anchor:
            continue
        name = term_name(heading)
        body = collect_body(heading)
        definition = render_definition(body)
        notes = render_notes(body)
        level = 3 if heading.name == "h3" else 4
        rows.append({
            "term": name,
            "definition": definition,
            "source_anchor": f"{SOURCE_URL}#{anchor}",
            "notes": notes,
        })
        md_blocks.append(render_markdown_entry(name, anchor, level, definition, notes))

    # Write CSV.
    csv_path = OUT_DIR / "cpansec-glossary-terms.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["term", "definition", "source_anchor", "notes"],
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        writer.writerows(rows)

    # Write JSON.
    json_path = OUT_DIR / "cpansec-glossary-terms.json"
    with json_path.open("w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    # Write Markdown.
    md_path = OUT_DIR / "cpansec-glossary.md"
    md_path.write_text("\n".join(md_blocks) + "\n", encoding="utf-8")

    print(f"Extracted {len(rows)} terms")
    print(f"  CSV:  {csv_path}")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
