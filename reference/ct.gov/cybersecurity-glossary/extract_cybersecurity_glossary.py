#!/usr/bin/env python3
"""
Extract Connecticut General Assembly Office of Legislative Research (CGA OLR)
Cybersecurity Glossary (report 2016-R-0267) into structured form.

Source: https://www.cga.ct.gov/2016/rpt/2016-R-0267.htm

Output:
- cybersecurity-glossary.md
- cybersecurity-glossary-terms.csv  (header: term,definition,source_anchor,notes)
- cybersecurity-glossary-terms.json

The source page is a Word-exported HTML with one or more <table> blocks whose
data rows contain three <td> cells: Term/Acronym, Definition/Explanation,
Relevant Links. Header rows ("Term or Acronym", "Definition or Explanation",
etc.) and continuation/title rows ("Table 1 (continued)") are filtered out.

Standalone, no third-party deps. Run from this directory.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import urllib.request
import ssl
from html.parser import HTMLParser
from pathlib import Path

SOURCE_URL = "https://www.cga.ct.gov/2016/rpt/2016-R-0267.htm"
HERE = Path(__file__).resolve().parent
LOCAL_HTML = HERE / "_source.html"


def fetch_source() -> str:
    """Download the report HTML, caching on disk."""
    if LOCAL_HTML.exists() and LOCAL_HTML.stat().st_size > 1000:
        return LOCAL_HTML.read_text(encoding="windows-1252")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0 (extractor; CSA dataset)"},
    )
    with urllib.request.urlopen(req, context=ctx) as resp:  # noqa: S310
        raw = resp.read()
    text = raw.decode("windows-1252", errors="replace")
    LOCAL_HTML.write_text(text, encoding="windows-1252")
    return text


# ----------------------------- HTML parsing ----------------------------------

class TableExtractor(HTMLParser):
    """Pull (term, definition, links_html) triples from the report tables.

    State machine:
    - track depth of <table>/<tr>/<td>
    - within a <td>, capture text and <a href> URLs
    - on </tr>, emit row if it has 3 cells
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_table = 0
        self.in_tr = False
        self.in_td = False
        self.cells: list[dict] = []  # current row's cells
        self.cur_text_parts: list[str] = []
        self.cur_links: list[tuple[str, str]] = []  # (href, text)
        self.cur_link_href: str | None = None
        self.cur_link_text_parts: list[str] = []
        self.rows: list[list[dict]] = []

    def handle_starttag(self, tag: str, attrs):
        t = tag.lower()
        if t == "table":
            self.in_table += 1
        elif t == "tr" and self.in_table:
            self.in_tr = True
            self.cells = []
        elif t == "td" and self.in_tr:
            self.in_td = True
            self.cur_text_parts = []
            self.cur_links = []
            self.cur_link_href = None
            self.cur_link_text_parts = []
        elif t == "a" and self.in_td:
            href = dict(attrs).get("href", "")
            self.cur_link_href = href
            self.cur_link_text_parts = []
        elif t in ("br", "p") and self.in_td:
            # newline boundary inside cell — represent as space
            self.cur_text_parts.append(" ")

    def handle_endtag(self, tag: str):
        t = tag.lower()
        if t == "a" and self.in_td and self.cur_link_href is not None:
            link_text = clean_text("".join(self.cur_link_text_parts))
            self.cur_links.append((self.cur_link_href, link_text))
            self.cur_link_href = None
            self.cur_link_text_parts = []
        elif t == "td" and self.in_td:
            text = "".join(self.cur_text_parts)
            self.cells.append({
                "text": clean_text(text),
                "links": list(self.cur_links),
            })
            self.in_td = False
        elif t == "tr" and self.in_tr:
            if len(self.cells) >= 2:
                self.rows.append(self.cells)
            self.in_tr = False
            self.cells = []
        elif t == "table" and self.in_table:
            self.in_table -= 1

    def handle_data(self, data: str):
        if self.in_td:
            self.cur_text_parts.append(data)
            if self.cur_link_href is not None:
                self.cur_link_text_parts.append(data)


def clean_text(s: str) -> str:
    # collapse whitespace, normalize curly quotes / non-breaking spaces
    s = s.replace("\xa0", " ").replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    # Windows-1252 char 0x92 etc. already decoded by codec; the unicode replacements
    # above handle the canonical forms.
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# ----------------------------- Filtering -------------------------------------

HEADER_TERMS = {
    "term or acronym",
    "definition or explanation",
    "relevant links",
    "relevant links (if applicable)",
    "(if applicable)",
}

CONTINUED_RE = re.compile(r"^table\s*\d+\s*\(continued\)\s*$", re.I)


def is_skip_row(term: str, definition: str) -> bool:
    tl = term.lower().strip()
    dl = definition.lower().strip()
    if not term and not definition:
        return True
    if CONTINUED_RE.match(tl) or CONTINUED_RE.match(dl):
        return True
    if tl in HEADER_TERMS and dl in HEADER_TERMS:
        return True
    # header-row guard: both cells look like column labels
    if tl in HEADER_TERMS:
        return True
    return False


# ----------------------------- Markdown rendering ----------------------------

def render_markdown(entries: list[dict]) -> str:
    lines = [
        "# Connecticut Cybersecurity Glossary",
        "",
        "Source: Connecticut General Assembly, Office of Legislative Research,",
        f"report 2016-R-0267. <{SOURCE_URL}>",
        "",
        "By Mary Fitzpatrick, Legislative Analyst II.",
        "",
        "This glossary collects acronyms and terms related to cybersecurity in",
        "the utility sector, used in the Connecticut Public Utility Regulatory",
        "Authority (PURA) Cybersecurity Action Plan.",
        "",
        "## Terms",
        "",
    ]
    for e in entries:
        term = e["term"]
        defn = e["definition"]
        links = e.get("links") or []
        lines.append(f"### {term}")
        lines.append("")
        lines.append(defn if defn else "_(no definition provided)_")
        lines.append("")
        if links:
            lines.append("Relevant links:")
            lines.append("")
            for link in links:
                href = link["href"]
                text = link.get("text", "") or href
                lines.append(f"- [{text}]({href})")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ----------------------------- Main ------------------------------------------

def main() -> int:
    html = fetch_source()
    parser = TableExtractor()
    parser.feed(html)

    entries: list[dict] = []
    for row in parser.rows:
        # take first 3 cells; some rows may have colspan'd single cell — skip those
        if len(row) < 2:
            continue
        term = row[0]["text"]
        definition = row[1]["text"] if len(row) > 1 else ""
        links_cell = row[2] if len(row) > 2 else {"text": "", "links": []}

        if is_skip_row(term, definition):
            continue

        # If the row is a section header (1 cell colspan), skip
        if not term or not definition:
            # treat as skip unless one is meaningfully present and the other
            # is a real value — for this source we require both
            continue

        # source_anchor: deterministic slug from term
        anchor = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")

        notes_parts = []
        if links_cell["text"]:
            # any non-URL prose appearing in the links column
            txt = links_cell["text"]
            # avoid duplicating the link anchor text in notes; only keep if it
            # differs materially
            if not all(lt and lt in txt for _, lt in links_cell["links"]):
                notes_parts.append(txt)

        entries.append({
            "term": term,
            "definition": definition,
            "source_anchor": anchor,
            "links": links_cell["links"],
            "notes": "; ".join(notes_parts),
        })

    # CSV
    csv_path = HERE / "cybersecurity-glossary-terms.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["term", "definition", "source_anchor", "notes"])
        for e in entries:
            link_str = "; ".join(
                f"{lt or href}: {href}" for href, lt in e["links"]
            )
            notes = e["notes"]
            if link_str:
                notes = (notes + " | " if notes else "") + f"links: {link_str}"
            w.writerow([e["term"], e["definition"], e["source_anchor"], notes])

    # JSON
    json_path = HERE / "cybersecurity-glossary-terms.json"
    out_json = []
    for e in entries:
        out_json.append({
            "term": e["term"],
            "definition": e["definition"],
            "source_anchor": e["source_anchor"],
            "links": [{"href": h, "text": t} for h, t in e["links"]],
            "notes": e["notes"],
        })
    json_path.write_text(
        json.dumps(out_json, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Markdown
    md_path = HERE / "cybersecurity-glossary.md"
    md_path.write_text(render_markdown(out_json), encoding="utf-8")

    print(f"Extracted {len(entries)} terms")
    print(f"  -> {md_path}")
    print(f"  -> {csv_path}")
    print(f"  -> {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
