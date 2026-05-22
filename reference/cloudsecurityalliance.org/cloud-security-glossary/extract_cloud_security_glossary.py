#!/usr/bin/env python3
"""Extract the CSA Cloud Security Glossary into structured form.

Source: https://cloudsecurityalliance.org/cloud-security-glossary
License notes: footer reads "© 2009-2026 Cloud Security Alliance. All rights
reserved." Inclusion in this public dataset is authorized by CSA as the
publisher and rights-holder; see the directory-level metadata.json for the
authorization record.

Structure of the page (static HTML, no JS required):
  Each term is wrapped in a single <div class="c-glossary__item"> with:
    <h6 id="..."> TERM </h6>
    <p> DEFINITION </p>
    [optional] <span>Sources</span><p> SOURCE_TEXT </p>
  Items are ordered alphabetically (numerics first, then A-Z).

The script caches the raw HTML to `_source.html` so re-runs work offline; pass
`--refresh` to force a re-download.

Outputs (alongside this script):
  cloud-security-glossary.md             — human-readable A-Z markdown
  cloud-security-glossary-terms.csv      — flat rows (term, definition, sources, source_anchor)
  cloud-security-glossary-terms.json     — list-of-dicts JSON
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

HERE = Path(__file__).parent
SOURCE_URL = "https://cloudsecurityalliance.org/cloud-security-glossary"
SOURCE_CACHE = HERE / "_source.html"
USER_AGENT = "Mozilla/5.0 (compatible; CSA-DatasetBuilder/1.0)"


def download(force_refresh: bool = False) -> str:
    if SOURCE_CACHE.exists() and not force_refresh:
        return SOURCE_CACHE.read_text(encoding="utf-8")
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        html = resp.read().decode("utf-8")
    SOURCE_CACHE.write_text(html, encoding="utf-8")
    return html


def parse(html: str):
    """Yield {term, definition, sources, source_anchor} dicts."""
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div", class_="c-glossary__item"):
        h6 = item.find("h6")
        if not h6:
            continue
        term = " ".join(h6.get_text(strip=True).split())
        if not term:
            continue

        # First <p> after the h6 is the definition.
        paragraphs = item.find_all("p")
        if not paragraphs:
            continue
        definition = " ".join(paragraphs[0].get_text(" ", strip=True).split())

        # The Sources span (if present) introduces a separate "Sources" block.
        # Everything after it (the remaining <p> children) is source info.
        sources = ""
        sources_span = item.find("span", string=lambda s: s and s.strip() == "Sources")
        if sources_span is None:
            # Some entries use a slightly different label; fall back to any
            # span with the gray color class right before extra paragraphs.
            sources_span = item.find("span", class_="u-text-color-gray-300")
        if sources_span and len(paragraphs) > 1:
            source_blocks = []
            # Take every <p> that comes after the Sources span in document order.
            for p in paragraphs[1:]:
                if sources_span in p.find_all_previous():
                    txt = " ".join(p.get_text(" ", strip=True).split())
                    if txt:
                        source_blocks.append(txt)
            sources = " | ".join(source_blocks)

        # The div's id (kebab-case) is the deep-link anchor on the page.
        source_anchor = item.get("id") or ""
        yield {
            "term": term,
            "definition": definition,
            "sources": sources,
            "source_anchor": f"{SOURCE_URL}#{source_anchor}" if source_anchor else SOURCE_URL,
        }


def write_outputs(entries):
    json_path = HERE / "cloud-security-glossary-terms.json"
    csv_path = HERE / "cloud-security-glossary-terms.csv"
    md_path = HERE / "cloud-security-glossary.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "sources", "source_anchor"])
        w.writeheader()
        w.writerows(entries)

    # Markdown — group by first letter
    lines = [
        "# CSA Cloud Security Glossary\n",
        f"Source: <{SOURCE_URL}>",
        "",
        "Extracted via `extract_cloud_security_glossary.py`. Inclusion in this "
        "public dataset is authorized by CSA as the publisher and rights-holder; "
        "see the directory-level metadata.json for the authorization record.",
        "",
        f"**Total terms: {len(entries)}**",
        "",
    ]
    current_letter = None
    for e in entries:
        first = e["term"][0].upper() if e["term"] else "#"
        if not first.isalpha():
            first = "#"
        if first != current_letter:
            lines.append(f"\n## {first}\n")
            current_letter = first
        lines.append(f"### {e['term']}\n")
        lines.append(e["definition"])
        if e["sources"]:
            lines.append(f"\n*Sources:* {e['sources']}")
        lines.append("")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return json_path, csv_path, md_path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true", help="force re-download from CSA site")
    args = ap.parse_args()

    html = download(force_refresh=args.refresh)
    entries = list(parse(html))
    if not entries:
        print("ERROR: parsed zero entries; HTML structure may have changed", file=sys.stderr)
        sys.exit(1)

    json_path, csv_path, md_path = write_outputs(entries)
    print(f"Parsed {len(entries):,} glossary entries")
    print(f"  wrote {json_path}")
    print(f"  wrote {csv_path}")
    print(f"  wrote {md_path}")


if __name__ == "__main__":
    main()
