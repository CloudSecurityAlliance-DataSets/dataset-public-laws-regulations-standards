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
    # SECTION 1 / SECTION 2 / Section (1): "SECTION 1. Legislative Findings and Declarations"
    (re.compile(r"^(SECTION\s+(?:\d+(?:\.\d+)*|\(\d+\)|\([ivxlcdm]+\)|[IVXLCDM]+))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "section_word"),
    # Pillar I / Pillar 1 / Pillar (i) / Pillar One: "Pillar I: AI Use Restrictions ..."
    (re.compile(r"^(Pillar\s+(?:[IVXLCDM]+|\([ivxlcdm]+\)|\d+|\(\d+\)|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "pillar"),
    # Part I / Part 1 / Part (1) / Part One: "Part I: ..."
    (re.compile(r"^(Part\s+(?:[IVXLCDM]+|\([ivxlcdm]+\)|\d+|\(\d+\)|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "part"),
    # CHAPTER 25.1 / Chapter 1 / Chapter One: "CHAPTER 25.1. Transparency in ..."
    (re.compile(r"^(CHAPTER\s+(?:\d+(?:\.\d+)?|\(\d+\)|[IVXLCDM]+|\([ivxlcdm]+\)|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "chapter"),
    # Strategic Objective 1.1 / Objective 1.1 / Objective 2a / Implementation 6.1
    (re.compile(r"^((?:Strategic\s+)?Objective\s+\d+[a-z]?(?:\.\d+)*|Implementation\s+\d+(?:\.\d+)*)\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "objective"),
    # Initiative 1.1.1: Title
    (re.compile(r"^(Initiative\s+\d+(?:\.\d+)+)\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "initiative"),
    # Goal 1 / Priority 1 / Principle 1 / Recommendation 1 / Finding 1: Title
    (re.compile(r"^((?:Goal|Priority|Principle|Recommendation|Finding)\s+\d+(?:\.\d+)*)\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "goal"),
    # Annex / Appendix / Schedule A / 1 / I: Title
    (re.compile(r"^((?:Annex|Appendix|Schedule)\s+(?:[A-Z]|\d+|[IVXLCDM]+))\s*[:\.\-–—]?\s+(.+)$", re.IGNORECASE), "annex"),
    # Standalone identifiers without trailing title (e.g., "Principle 1", "Appendix A", "Part One.")
    (re.compile(r"^((?:Pillar|Part|Chapter|Section|Annex|Appendix|Schedule|Principle|Goal|Objective|Finding|Recommendation)\s+(?:[IVXLCDM]+|\([ivxlcdm]+\)|\d+[a-z]?|\(\d+\)|[A-Z]|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten))\.?$", re.IGNORECASE), "standalone_id"),
    # Roman numeral section: "I. Introduction" / "II. Our Vision"
    (re.compile(r"^([IVX]+)\.\s+(.+)$"), "roman"),
    # Plain hierarchical numbering "1.1 Title" / "1.1. Title" / "2.3.1 Title"
    (re.compile(r"^(\d+(?:\.\d+){0,3})\s*[:\.\-–—]?\s+(.+)$"), "numbered"),
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
            if m.lastindex and m.lastindex >= 2:
                return m.group(1).rstrip("."), m.group(2).strip(), kind
            return m.group(1).rstrip("."), m.group(1).rstrip("."), kind
    return "", cleaned, ""


def derive_parent_id(section_id: str, existing_ids: set[str] | None = None) -> str:
    """For numeric ids like '1.2.3' or '22757.10', return the parent ('1.2',
    '22757'). For 'Initiative X.Y.Z' return 'Strategic Objective X.Y' (or
    'Implementation X.Y' if present)."""
    parts = section_id.split(".")
    if len(parts) > 1 and all(re.match(r"^\d+$", p) for p in parts):
        return ".".join(parts[:-1])
    m = re.match(r"^Initiative\s+(\d+\.\d+)\.\d+$", section_id, re.IGNORECASE)
    if m:
        xy = m.group(1)
        if existing_ids and f"Implementation {xy}" in existing_ids:
            return f"Implementation {xy}"
        return f"Strategic Objective {xy}"
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
    seen_ids: set[str] = set()
    for i, m in enumerate(headings):
        depth = len(m.group(1))
        section_id, section_name, id_kind = parse_heading(m.group(2))
        if section_id:
            seen_ids.add(section_id)
        body_start = m.end()
        body_end = headings[i + 1].start() if i + 1 < len(headings) else len(md)
        body = normalize_body(md[body_start:body_end])
        rows.append({
            "depth": depth,
            "section_id": section_id,
            "section_name": section_name,
            "id_kind": id_kind,
            "parent_id": derive_parent_id(section_id, seen_ids) if section_id else "",
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
