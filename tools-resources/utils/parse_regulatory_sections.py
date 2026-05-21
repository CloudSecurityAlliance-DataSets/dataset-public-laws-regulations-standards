#!/usr/bin/env python3
"""Generic per-section extractor for hierarchical regulatory documents.

Walks a markdown file for `#`-level headings, captures each as a row with:
  - section_id     (numeric/textual identifier pulled from the heading)
  - section_name   (heading title, with the id stripped)
  - depth          (heading level)
  - parent_id      (derived from hierarchical numbering, or empty)
  - body           (prose under the heading until the next heading)

Identifier patterns are heuristic: tries to match common shapes like
"1.1", "22757.10", "Pillar I", "SECTION 2". If no recognizable identifier
prefixes the heading, section_id is left empty (rows still emitted).

Usage:
    python3 parse_regulatory_sections.py <doc-dir> [--out-stem PREFIX]

Output: <doc-dir>/<PREFIX>-sections.{csv,json}
  PREFIX defaults to the dir name.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#+)\s+(.+?)\s*$", re.MULTILINE)

# Identifier patterns tried in order. First match wins. Each returns the id
# string from the heading text.
ID_PATTERNS = [
    # SB-53 style: "22757.10. Short Title" or "22757.10 Short Title"
    (re.compile(r"^(\d{4,5}\.\d+(?:\.\d+)?)\.?\s+(.+)$"), "statute"),
    # SECTION 1 / SECTION 2: "SECTION 1. Legislative Findings and Declarations"
    (re.compile(r"^(SECTION\s+\d+)\.?\s+(.+)$", re.IGNORECASE), "section_word"),
    # Pillar I / Pillar II: "Pillar I: AI Use Restrictions ..."
    (re.compile(r"^(Pillar\s+[IVX]+)[:\.]?\s+(.+)$", re.IGNORECASE), "pillar"),
    # CHAPTER 25.1: "CHAPTER 25.1. Transparency in ..."
    (re.compile(r"^(CHAPTER\s+\d+(?:\.\d+)?)\.?\s+(.+)$", re.IGNORECASE), "chapter"),
    # Plain hierarchical numbering "1.1 Title" / "1.1. Title" / "2.3.1 Title"
    (re.compile(r"^(\d+(?:\.\d+){0,3})\.?\s+(.+)$"), "numbered"),
]


def clean_heading_text(s: str) -> str:
    """Strip markdown bold/italic + anchor tags + leading numbering punctuation."""
    s = re.sub(r"<a id=\"[^\"]*\"></a>", "", s)
    s = re.sub(r"<span[^>]*>([^<]*)</span>", r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"\\([_*\[\]\(\)])", r"\1", s)
    return s.strip()


def parse_heading(text: str):
    """Return (section_id, section_name, id_kind) for a heading text. If no id
    pattern matches, section_id and id_kind are empty strings."""
    cleaned = clean_heading_text(text)
    for pat, kind in ID_PATTERNS:
        m = pat.match(cleaned)
        if m:
            return m.group(1), m.group(2).strip(), kind
    return "", cleaned, ""


def derive_parent_id(section_id: str) -> str:
    """For numeric ids like '1.2.3' or '22757.10', return the parent ('1.2',
    '22757'). For non-numeric ids return empty."""
    parts = section_id.split(".")
    if len(parts) > 1 and all(re.match(r"^\d+$", p) for p in parts):
        return ".".join(parts[:-1])
    return ""


def normalize_body(s: str) -> str:
    s = re.sub(r"\\([_*\[\]\(\)\-\.])", r"\1", s)
    s = re.sub(r"<a id=\"[^\"]*\"></a>", "", s)
    s = re.sub(r"<span[^>]*>([^<]*)</span>", r"\1", s)
    s = re.sub(r"\{\d+\}-+", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc_dir", help="Document directory containing the .md file")
    ap.add_argument("--out-stem", default=None,
                    help="Output filename prefix (default: dir name)")
    args = ap.parse_args()

    doc_dir = Path(args.doc_dir).resolve()
    if not doc_dir.is_dir():
        raise SystemExit(f"Not a directory: {doc_dir}")

    md_files = [p for p in doc_dir.glob("*.md")
                if not p.name.endswith("-metadata.md")
                and not p.name.startswith("README")]
    if not md_files:
        raise SystemExit(f"No source markdown in {doc_dir}")
    md = md_files[0].read_text(encoding="utf-8")

    headings = list(HEADING_RE.finditer(md))
    rows = []
    for i, m in enumerate(headings):
        depth = len(m.group(1))
        section_id, section_name, id_kind = parse_heading(m.group(2))
        body_start = m.end()
        body_end = headings[i + 1].start() if i + 1 < len(headings) else len(md)
        body = normalize_body(md[body_start:body_end])
        rows.append({
            "depth": depth,
            "section_id": section_id,
            "section_name": section_name,
            "id_kind": id_kind,
            "parent_id": derive_parent_id(section_id) if section_id else "",
            "body": body,
        })

    stem = args.out_stem or doc_dir.name
    csv_path = doc_dir / f"{stem}-sections.csv"
    json_path = doc_dir / f"{stem}-sections.json"
    fields = ["depth", "section_id", "section_name", "id_kind", "parent_id", "body"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    n_id = sum(1 for r in rows if r["section_id"])
    print(f"Sections: {len(rows)}  ({n_id} with identifier, {len(rows) - n_id} headings without)")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    main()
