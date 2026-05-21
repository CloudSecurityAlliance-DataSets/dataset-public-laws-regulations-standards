#!/usr/bin/env python3
"""Extract the glossary section (Appendix B) from the Government of Canada
Enterprise Cyber Security Strategy page.

Source:
  https://www.canada.ca/en/government/system/digital-government/online-security-privacy/enterprise-cyber-security-strategy.html

The glossary is one section within a larger strategy document. The page is
served as a single HTML document; the glossary lives under
<section><h2 id="app-b">Appendix B: glossary</h2>...</section> as a <dl>
where each <dt> is the term (wrapped in <strong>) and each <dd> contains the
definition followed by a "(Source: ...)" attribution paragraph.

This script:
  1. Downloads the HTML (or reads a local cache).
  2. Slices out the Appendix B <section>.
  3. Parses each <dt>/<dd> pair into a term + definition + source attribution.
  4. Writes:
       - enterprise-cyber-security-strategy-glossary.md
       - enterprise-cyber-security-strategy-glossary-terms.csv
       - enterprise-cyber-security-strategy-glossary-terms.json

Content licence: Open Government Licence - Canada
  https://open.canada.ca/en/open-government-licence-canada
"""

from __future__ import annotations

import csv
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

SOURCE_URL = (
    "https://www.canada.ca/en/government/system/digital-government/"
    "online-security-privacy/enterprise-cyber-security-strategy.html"
)
ANCHOR = "app-b"

HERE = Path(__file__).resolve().parent
SLUG = "enterprise-cyber-security-strategy-glossary"
CACHE_HTML = HERE / "_source.html"
OUT_MD = HERE / f"{SLUG}.md"
OUT_CSV = HERE / f"{SLUG}-terms.csv"
OUT_JSON = HERE / f"{SLUG}-terms.json"


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_html() -> str:
    if CACHE_HTML.exists():
        return CACHE_HTML.read_text(encoding="utf-8")
    req = urllib.request.Request(
        SOURCE_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    CACHE_HTML.write_text(raw, encoding="utf-8")
    return raw


# ---------------------------------------------------------------------------
# Slice + parse
# ---------------------------------------------------------------------------

def slice_glossary_section(doc: str) -> str:
    """Return the inner HTML of the <section> that contains Appendix B."""
    # Find the <section> that opens immediately before the Appendix B h2.
    h2_marker = f'<h2 id="{ANCHOR}"'
    h2_idx = doc.find(h2_marker)
    if h2_idx == -1:
        raise RuntimeError(
            "Could not find the Appendix B glossary anchor in the source HTML."
        )
    # Walk backwards to the nearest <section>.
    sec_open = doc.rfind("<section>", 0, h2_idx)
    if sec_open == -1:
        raise RuntimeError("Could not find <section> opening before Appendix B.")
    sec_close = doc.find("</section>", h2_idx)
    if sec_close == -1:
        raise RuntimeError("Could not find </section> closing for Appendix B.")
    return doc[sec_open : sec_close + len("</section>")]


_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def strip_tags(fragment: str) -> str:
    text = _TAG_RE.sub("", fragment)
    text = html.unescape(text)
    text = text.replace("\xa0", " ")
    text = _WS_RE.sub(" ", text).strip()
    return text


# Matches a <dt>...</dt> <dd>...</dd> pair.
_PAIR_RE = re.compile(
    r"<dt[^>]*>(?P<dt>.*?)</dt>\s*<dd[^>]*>(?P<dd>.*?)</dd>",
    re.DOTALL,
)


def _split_definition_and_source(dd_html: str) -> tuple[str, str]:
    """Return (definition_text, source_text). Handles definitions that contain
    bullet lists and a trailing "(Source: ...)" paragraph."""
    # Identify the last <p> that begins with "(Source:" - that's attribution.
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", dd_html, flags=re.DOTALL)
    lists = re.findall(r"<ul[^>]*>(.*?)</ul>", dd_html, flags=re.DOTALL)

    source = ""
    body_paragraphs: list[str] = []
    for p in paragraphs:
        ptext = strip_tags(p)
        if ptext.startswith("(Source:") and ptext.endswith(")"):
            source = ptext[len("(Source:"):-1].strip()
        else:
            body_paragraphs.append(ptext)

    # Append bullet items inline so the CSV cell stays a single field.
    bullet_items: list[str] = []
    for ul in lists:
        for li in re.findall(r"<li[^>]*>(.*?)</li>", ul, flags=re.DOTALL):
            bullet_items.append(strip_tags(li))

    definition = " ".join(body_paragraphs).strip()
    if bullet_items:
        definition = (definition + " " if definition else "") + "; ".join(
            f"- {item}" for item in bullet_items
        )
    return definition, source


def parse_terms(section_html: str) -> list[dict]:
    # Restrict to the inside of the <dl>.
    dl_match = re.search(r"<dl[^>]*>(.*?)</dl>", section_html, re.DOTALL)
    if not dl_match:
        raise RuntimeError("No <dl> found inside the Appendix B section.")
    dl_inner = dl_match.group(1)

    terms: list[dict] = []
    for m in _PAIR_RE.finditer(dl_inner):
        term = strip_tags(m.group("dt"))
        definition, source = _split_definition_and_source(m.group("dd"))
        anchor_slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
        terms.append(
            {
                "term": term,
                "definition": definition,
                "source_anchor": f"{ANCHOR}#{anchor_slug}",
                "notes": f"Source: {source}" if source else "",
            }
        )
    return terms


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------

def write_markdown(terms: list[dict]) -> None:
    lines: list[str] = []
    lines.append("# Government of Canada - Enterprise Cyber Security Strategy")
    lines.append("")
    lines.append("## Appendix B: Glossary")
    lines.append("")
    lines.append(f"Source: <{SOURCE_URL}#{ANCHOR}>")
    lines.append("")
    lines.append(
        "Content reproduced under the Open Government Licence - Canada "
        "(https://open.canada.ca/en/open-government-licence-canada)."
    )
    lines.append("")
    for entry in terms:
        lines.append(f"### {entry['term']}")
        lines.append("")
        lines.append(entry["definition"])
        lines.append("")
        if entry["notes"]:
            lines.append(f"_{entry['notes']}_")
            lines.append("")
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_csv(terms: list[dict]) -> None:
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["term", "definition", "source_anchor", "notes"]
        )
        writer.writeheader()
        for entry in terms:
            writer.writerow(entry)


def write_json(terms: list[dict]) -> None:
    OUT_JSON.write_text(
        json.dumps(terms, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    doc = fetch_html()
    section = slice_glossary_section(doc)
    terms = parse_terms(section)
    if not terms:
        raise RuntimeError("Parsed 0 glossary terms - check selectors.")
    write_markdown(terms)
    write_csv(terms)
    write_json(terms)
    print(f"Parsed {len(terms)} terms.")
    print(f"  markdown -> {OUT_MD}")
    print(f"  csv      -> {OUT_CSV}")
    print(f"  json     -> {OUT_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
