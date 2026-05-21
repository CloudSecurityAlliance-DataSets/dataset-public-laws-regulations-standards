#!/usr/bin/env python3
"""Extract the CERT-AGID glossary (https://cert-agid.gov.it/glossario/) into
structured term/definition outputs.

The glossary is published as an index page that links to one HTML page per
term. Each per-term page uses an <h2> for the term label and a series of <h3>
subsections (e.g. "Che cos'e?", "Cos'e tecnicamente?", "Perche e rilevante?",
"Come mi difendo?" / "Come si rimedia?") followed by <p>/<ul> content.

Outputs (written next to this script):
    cert-agid-glossario.md
    cert-agid-glossario-terms.csv  (term,definition,source_anchor,notes)
    cert-agid-glossario-terms.json

Italian definitions are preserved verbatim.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

BASE_URL = "https://cert-agid.gov.it/glossario/"
HEADERS = {
    "User-Agent": (
        "CSA-DataSets/1.0 (+https://github.com/CloudSecurityAlliance-DataSets) "
        "python-requests"
    ),
    "Accept-Language": "it,en;q=0.7",
}
REQUEST_PAUSE_SECONDS = 1.0
SCRIPT_DIR = Path(__file__).resolve().parent


def fetch(url: str) -> str:
    """GET url with a polite UA, raising on HTTP error."""
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    # cert-agid serves UTF-8; be explicit.
    resp.encoding = resp.apparent_encoding or "utf-8"
    return resp.text


def discover_term_urls(index_html: str) -> list[tuple[str, str]]:
    """From the glossary index, return [(label, absolute_url)] for each term.

    Excludes the index URL itself; deduplicates while preserving order.
    """
    soup = BeautifulSoup(index_html, "html.parser")
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        abs_url = urljoin(BASE_URL, href)
        # We want links whose path is /glossario/<slug>/, not the index itself
        # and not a fragment on the same page.
        m = re.match(r"https?://cert-agid\.gov\.it/glossario/([^/?#]+)/?$", abs_url)
        if not m:
            continue
        slug = m.group(1)
        if not slug:
            continue
        # Skip pagination or feed-like slugs that look like numbers.
        normalized = abs_url.rstrip("/") + "/"
        if normalized in seen:
            continue
        label = a.get_text(strip=True)
        if not label:
            # Sometimes a link wraps an image; fall back to slug.
            label = slug
        # Skip obvious non-term links that happen to match the pattern
        # (none observed; defensive).
        if label.lower() in {"glossario"}:
            continue
        seen.add(normalized)
        pairs.append((label, normalized))
    return pairs


def _text_with_lists(node: Tag) -> str:
    """Render a content node (p, ul, ol) to plain text, preserving bullets."""
    if node.name in {"ul", "ol"}:
        lines = []
        for li in node.find_all("li", recursive=False):
            lines.append(f"- {li.get_text(' ', strip=True)}")
        return "\n".join(lines)
    # paragraphs and generic blocks
    return node.get_text(" ", strip=True)


def _find_content_section(soup: BeautifulSoup) -> Tag | None:
    """Locate the main content container on a CERT-AGID glossary term page.

    The site theme places body content inside
        <section class="... Page-text ... hentry">
    with an <h1 class="WP-Title"> term label followed by <h3>/<p>/<ul> blocks.
    Fall back to <main> or <article> if the class-based hook ever changes.
    """
    sec = soup.find("section", class_=lambda c: bool(c) and "Page-text" in c.split())
    if sec is not None:
        return sec
    for tag_name in ("article", "main"):
        node = soup.find(tag_name)
        if node is not None:
            return node
    return None


def parse_term_page(html: str, fallback_label: str) -> tuple[str, dict[str, str], str]:
    """Return (term, sections_dict, combined_definition_text).

    sections_dict preserves order using insertion order.
    combined_definition_text concatenates section bodies (without section
    headings) with double newlines, suitable for a flat CSV "definition" cell.
    """
    soup = BeautifulSoup(html, "html.parser")
    container = _find_content_section(soup) or soup

    # Term label: first <h1 class="WP-Title"> inside the container; fall back
    # to any h1, then to the index label.
    term_node = container.find("h1", class_=lambda c: bool(c) and "WP-Title" in c.split())
    if term_node is None:
        term_node = container.find("h1")
    term = term_node.get_text(" ", strip=True) if term_node else fallback_label

    sections: dict[str, list[str]] = {}
    current_section: str = "__intro__"
    sections[current_section] = []

    # Iterate top-level children of the content container so we don't descend
    # into <ul><li><p>...</p></li></ul> twice.
    children = list(container.descendants) if term_node is None else []
    if term_node is not None:
        # Walk siblings after the term heading. The CERT-AGID layout keeps
        # h3/p/ul as siblings of the h1 inside the section.
        node = term_node
        while True:
            node = node.find_next_sibling()
            if node is None:
                break
            if not isinstance(node, Tag):
                continue
            if node.name == "h1":
                # Defensive: a new h1 would mean a new term.
                break
            if node.name == "h3":
                current_section = node.get_text(" ", strip=True)
                sections.setdefault(current_section, [])
                continue
            if node.name in {"p", "ul", "ol"}:
                text = _text_with_lists(node)
                if text:
                    sections.setdefault(current_section, []).append(text)
                continue
            # Other tags (div wrappers etc.): dig in for nested p/ul/ol/h3.
            for inner in node.find_all(["h3", "p", "ul", "ol"], recursive=True):
                if inner.name == "h3":
                    current_section = inner.get_text(" ", strip=True)
                    sections.setdefault(current_section, [])
                    continue
                # Skip lists nested inside paragraphs/lis we'll also visit.
                if inner.name in {"p", "ul", "ol"} and any(
                    p.name in {"li"} for p in inner.parents
                ):
                    continue
                text = _text_with_lists(inner)
                if text:
                    sections.setdefault(current_section, []).append(text)
    else:
        # No headings found; dump container text as the intro.
        body_text = container.get_text(" ", strip=True) if hasattr(container, "get_text") else ""
        if body_text:
            sections[current_section].append(body_text)
    # children variable kept only for the no-h1 path; not used further.
    del children

    # Drop empty sections and the intro placeholder if empty.
    cleaned: dict[str, str] = {}
    for name, parts in sections.items():
        joined = "\n".join(p for p in parts if p).strip()
        if not joined:
            continue
        display_name = "" if name == "__intro__" else name
        cleaned[display_name] = joined

    # Flat definition: concatenate section bodies (with section labels if
    # present) so the CSV row carries the full text.
    flat_parts: list[str] = []
    for name, body in cleaned.items():
        if name:
            flat_parts.append(f"{name}\n{body}")
        else:
            flat_parts.append(body)
    flat_definition = "\n\n".join(flat_parts).strip()

    return term, cleaned, flat_definition


def main() -> int:
    print(f"[1/3] Fetching index: {BASE_URL}", file=sys.stderr)
    index_html = fetch(BASE_URL)
    term_links = discover_term_urls(index_html)
    if not term_links:
        print("ERROR: no term links discovered from index page", file=sys.stderr)
        return 1
    print(f"      discovered {len(term_links)} term link(s)", file=sys.stderr)

    records: list[dict] = []
    md_chunks: list[str] = [
        "# CERT-AGID Glossario",
        "",
        f"Source: {BASE_URL}",
        "",
        "Italian definitions preserved verbatim from cert-agid.gov.it.",
        "",
    ]

    for i, (label, url) in enumerate(term_links, 1):
        print(f"[2/3] ({i}/{len(term_links)}) {label} <- {url}", file=sys.stderr)
        try:
            html = fetch(url)
        except requests.HTTPError as exc:
            print(f"      HTTP error for {url}: {exc}", file=sys.stderr)
            continue
        term, sections, flat_definition = parse_term_page(html, fallback_label=label)
        notes_bits: list[str] = []
        if not flat_definition:
            notes_bits.append("empty definition extracted")
        if term.lower() != label.lower():
            notes_bits.append(f"index label: {label}")
        notes = "; ".join(notes_bits)

        records.append(
            {
                "term": term,
                "definition": flat_definition,
                "source_anchor": url,
                "notes": notes,
            }
        )

        # Markdown: ## Term, then sections as ### subheads if present.
        md_chunks.append(f"## {term}")
        md_chunks.append("")
        md_chunks.append(f"Source: {url}")
        md_chunks.append("")
        for sname, body in sections.items():
            if sname:
                md_chunks.append(f"### {sname}")
                md_chunks.append("")
            md_chunks.append(body)
            md_chunks.append("")

        time.sleep(REQUEST_PAUSE_SECONDS)

    md_path = SCRIPT_DIR / "cert-agid-glossario.md"
    csv_path = SCRIPT_DIR / "cert-agid-glossario-terms.csv"
    json_path = SCRIPT_DIR / "cert-agid-glossario-terms.json"

    print(f"[3/3] Writing {md_path.name}, {csv_path.name}, {json_path.name}", file=sys.stderr)

    md_path.write_text("\n".join(md_chunks).rstrip() + "\n", encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["term", "definition", "source_anchor", "notes"],
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)

    json_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"DONE: {len(records)} terms written", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
