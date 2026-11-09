"""Shared extractor for Cloudflare developer-docs glossaries.

Used by per-product extract scripts under reference/cloudflare.com/<slug>-glossary/.

Two parser strategies, auto-selected from the source markdown:

  table mode    The doc contains a markdown table with "Term" in its header
                row. We pull each row's Term, Definition, and optional Product
                column. Most Cloudflare product glossaries use this format.

  headings mode No glossary table; instead, each term is a "## Term Name" h2
                heading followed by paragraph(s) of definition. Used by Radar
                (and potentially other product glossaries).

All extractors emit the canonical four-file set with the term/definition/
source_anchor/notes schema documented in PROCESSING-GLOSSARIES.md.
"""

import csv
import json
import re
from pathlib import Path

import requests

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)


def _squish(s):
    return re.sub(r"\s+", " ", s).strip()


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _fetch(md_url):
    r = requests.get(
        md_url,
        timeout=30,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
    )
    r.raise_for_status()
    return r.text


def _strip_markdown_links(text):
    """Replace [label](url) with just label, drop emoji arrows."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("↗", "").replace("​", "")
    return _squish(text)


def _parse_table(md):
    """Look for a markdown table with 'Term' in its header. Return list or None."""
    terms = []
    in_table = False
    header_cells = None
    for line in md.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table:
                break
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if header_cells is None:
            if not any("term" in c.lower() for c in cells):
                continue
            header_cells = cells
            continue
        if all(re.match(r"^[\s\-:]+$", c) for c in cells):
            in_table = True
            continue
        if not in_table or len(cells) < 2:
            continue
        term = _strip_markdown_links(cells[0])
        definition = _strip_markdown_links(cells[1])
        if not term or not definition:
            continue
        notes = ""
        if len(cells) >= 3 and cells[2].strip():
            product = _strip_markdown_links(cells[2])
            if product:
                notes = f"product: {product}"
        terms.append({"term": term, "definition": definition, "notes": notes})
    return terms if header_cells else None


def _parse_headings(md):
    """Heading-based: collect ## H2 + paragraph(s) until next ## or document end."""
    # Strip fenced code blocks (such as trailing JSON-LD BreadcrumbList metadata) and HTML comments.
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    # Strip frontmatter / leading metadata before the first ## section.
    # Walk line-by-line, accumulating definition lines under the current h2.
    terms = []
    current_term = None
    current_lines = []
    seen_first_h1 = False
    for line in md.splitlines():
        if line.startswith("# ") and not seen_first_h1:
            seen_first_h1 = True
            continue
        if line.startswith("## "):
            # Flush previous term.
            if current_term:
                definition = _strip_markdown_links(" ".join(current_lines)).strip()
                if definition:
                    terms.append({
                        "term": current_term,
                        "definition": definition,
                        "notes": "",
                    })
            current_term = _strip_markdown_links(line[3:])
            current_lines = []
        elif current_term is not None:
            # Skip blank lines that are entirely whitespace; keep substantive content.
            if line.strip():
                # Drop image-only lines, pure markup, or JSON-LD breadcrumb lines.
                if not re.match(r"^\s*!\[", line) and "BreadcrumbList" not in line and '"@context"' not in line:
                    current_lines.append(line.strip())
    # Flush last.
    if current_term:
        definition = _strip_markdown_links(" ".join(current_lines)).strip()
        if definition:
            terms.append({
                "term": current_term,
                "definition": definition,
                "notes": "",
            })
    return terms


def _annotate_anchors(terms, source_url):
    for t in terms:
        t["source_anchor"] = f"{source_url}#{_slug(t['term'])}"
    return terms


def _dedupe_sorted(terms):
    by_term = {}
    for t in terms:
        key = (t["term"].lower(), t.get("notes", "").lower())
        existing = by_term.get(key)
        if existing is None or len(t["definition"]) > len(existing["definition"]):
            by_term[key] = t
    return sorted(by_term.values(), key=lambda x: (x["term"].lower(), x.get("notes", "").lower()))


def parse(md, source_url):
    table_terms = _parse_table(md)
    if table_terms:
        return _dedupe_sorted(_annotate_anchors(table_terms, source_url))
    heading_terms = _parse_headings(md)
    return _dedupe_sorted(_annotate_anchors(heading_terms, source_url))


def write_outputs(terms, out_dir, prefix, title, source_url, md_url):
    out_dir = Path(out_dir)
    md_path = out_dir / f"{prefix}.md"
    with open(md_path, "w") as f:
        f.write(f"# {title}\n\n")
        f.write(f"Source: {source_url}\n")
        f.write(f"Markdown alternate (used by the extractor): {md_url}\n\n")
        f.write("License: LicenseRef-Vendor-Copyright (Cloudflare, Inc.; internal CSA use only — not redistributable).\n\n")
        f.write(f"Extracted: {len(terms)} terms.\n\n---\n\n")
        for t in terms:
            f.write(f"## {t['term']}\n\n{t['definition']}\n\n")
            if t["notes"]:
                f.write(f"_{t['notes']}_\n\n")
    csv_path = out_dir / f"{prefix}-terms.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(terms)
    json_path = out_dir / f"{prefix}-terms.json"
    with open(json_path, "w") as f:
        json.dump(terms, f, indent=2, ensure_ascii=False)
    return md_path, csv_path, json_path


def run(source_url, md_url, out_dir, prefix, title):
    md = _fetch(md_url)
    terms = parse(md, source_url)
    write_outputs(terms, out_dir, prefix, title, source_url, md_url)
    return len(terms)
