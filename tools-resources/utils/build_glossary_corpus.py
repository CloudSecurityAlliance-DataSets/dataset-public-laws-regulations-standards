#!/usr/bin/env python3
"""Aggregate every `subtype: ["glossary"]` entry's extracted terms into a single
cross-source corpus, and generate a side-by-side comparison view of terms that
appear in 2+ sources.

Inputs walked:
  reference/{namespace}/{candidate-dir}/{candidate-dir}-metadata.json
  reference/{namespace}/{candidate-dir}/{candidate-dir}-terms.json

Outputs (written under tools-resources/glossary-corpus/):
  corpus.csv          one row per (source, term)
  corpus.json         same data as JSON list
  cross-source.csv    one row per term appearing in 2+ sources, side-by-side
  cross-source.json   same data as JSON
  stats.md            term counts by source + corpus-wide stats

Usage: python3 tools-resources/utils/build_glossary_corpus.py
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
REFERENCE = REPO / "reference"
OUT_DIR = REPO / "tools-resources" / "glossary-corpus"


def find_glossary_dirs():
    """Yield (metadata_dict, metadata_path) for every reference entry tagged subtype=glossary."""
    for meta_file in REFERENCE.glob("*/*/*-metadata.json"):
        try:
            with open(meta_file) as f:
                meta = json.load(f)
        except Exception:
            continue
        if "glossary" in (meta.get("subtype") or []):
            yield meta, meta_file


def normalize_term(t):
    """Lowercase, collapse whitespace, strip punctuation tails for cross-source matching."""
    s = t.lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = s.strip(".,;:!?()[]{}\"'")
    # Drop parenthetical acronyms in the term text, e.g. "Two-Factor Authentication (2FA)" → "two-factor authentication"
    s = re.sub(r"\s*\([^)]*\)\s*$", "", s).strip()
    return s


def build_corpus():
    rows = []
    source_counts = {}
    for meta, meta_path in find_glossary_dirs():
        dirname = meta_path.parent.name
        terms_file = meta_path.parent / f"{dirname}-terms.json"
        secid = meta.get("secid", "")
        source_name = meta.get("name", dirname)
        license_spdx = meta.get("license", {}).get("spdx", "NOASSERTION")
        redistributable = meta.get("license", {}).get("publicly_redistributable", False)
        source_url = meta.get("links", {}).get("source", "")
        if not terms_file.exists():
            source_counts[secid] = {
                "source_name": source_name,
                "term_count": 0,
                "license_spdx": license_spdx,
                "publicly_redistributable": redistributable,
                "source_url": source_url,
                "state": "metadata-only",
            }
            continue
        try:
            with open(terms_file) as f:
                terms = json.load(f)
        except Exception:
            continue
        n = 0
        for t in terms:
            term = (t.get("term") or "").strip()
            definition = (t.get("definition") or "").strip()
            anchor = (t.get("source_anchor") or "").strip()
            notes = (t.get("notes") or "").strip()
            if not term or not definition:
                continue
            rows.append({
                "source_secid": secid,
                "source_name": source_name,
                "license_spdx": license_spdx,
                "publicly_redistributable": redistributable,
                "term": term,
                "normalized_term": normalize_term(term),
                "definition": definition,
                "source_anchor": anchor,
                "notes": notes,
            })
            n += 1
        source_counts[secid] = {
            "source_name": source_name,
            "term_count": n,
            "license_spdx": license_spdx,
            "publicly_redistributable": redistributable,
            "source_url": source_url,
            "state": "structured" if n > 0 else "extracted",
        }
    return rows, source_counts


def build_cross_source(rows):
    """For each normalized_term appearing in 2+ sources, group definitions."""
    by_norm = defaultdict(list)
    for r in rows:
        by_norm[r["normalized_term"]].append(r)
    crossed = []
    for norm, items in by_norm.items():
        sources = {i["source_secid"] for i in items}
        if len(sources) < 2:
            continue
        crossed.append({
            "normalized_term": norm,
            "source_count": len(sources),
            "row_count": len(items),
            "sources": sorted(sources),
            "definitions": [
                {
                    "source_secid": i["source_secid"],
                    "source_name": i["source_name"],
                    "term": i["term"],
                    "definition": i["definition"],
                    "source_anchor": i["source_anchor"],
                }
                for i in items
            ],
        })
    crossed.sort(key=lambda x: (-x["source_count"], x["normalized_term"]))
    return crossed


def write_corpus(rows):
    csv_path = OUT_DIR / "corpus.csv"
    with open(csv_path, "w", newline="") as f:
        fieldnames = [
            "source_secid",
            "source_name",
            "license_spdx",
            "publicly_redistributable",
            "term",
            "normalized_term",
            "definition",
            "source_anchor",
            "notes",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    json_path = OUT_DIR / "corpus.json"
    with open(json_path, "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    return csv_path, json_path


def write_cross_source(crossed):
    csv_path = OUT_DIR / "cross-source.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["normalized_term", "source_count", "source_secid", "source_name", "term", "definition", "source_anchor"])
        for c in crossed:
            for d in c["definitions"]:
                w.writerow([
                    c["normalized_term"],
                    c["source_count"],
                    d["source_secid"],
                    d["source_name"],
                    d["term"],
                    d["definition"],
                    d["source_anchor"],
                ])
    json_path = OUT_DIR / "cross-source.json"
    with open(json_path, "w") as f:
        json.dump(crossed, f, indent=2, ensure_ascii=False)
    return csv_path, json_path


def write_stats(rows, crossed, source_counts):
    path = OUT_DIR / "stats.md"
    total_rows = len(rows)
    total_unique_norms = len({r["normalized_term"] for r in rows})
    cross_terms = len(crossed)
    redistributable_sources = sum(1 for s in source_counts.values() if s["publicly_redistributable"] and s["term_count"] > 0)
    metadata_only_sources = sum(1 for s in source_counts.values() if s["term_count"] == 0)

    with open(path, "w") as f:
        f.write("# Glossary corpus statistics\n\n")
        f.write("Generated by `tools-resources/utils/build_glossary_corpus.py`.\n\n")
        f.write("## Corpus-wide\n\n")
        f.write(f"- Total term-rows (one per source per term): **{total_rows:,}**\n")
        f.write(f"- Unique normalized terms: **{total_unique_norms:,}**\n")
        f.write(f"- Cross-source overlaps (terms in 2+ sources): **{cross_terms:,}**\n")
        f.write(f"- Fully-extracted glossaries: **{redistributable_sources}**\n")
        f.write(f"- Metadata-only glossary stubs: **{metadata_only_sources}**\n\n")

        f.write("## Per-source term counts (extracted)\n\n")
        f.write("| Source | Terms | License |\n|---|---:|---|\n")
        for secid, info in sorted(source_counts.items(), key=lambda x: (-x[1]["term_count"], x[0])):
            if info["term_count"] == 0:
                continue
            f.write(f"| `{secid}` | {info['term_count']:,} | {info['license_spdx']} |\n")

        f.write("\n## Top cross-source terms (most sources)\n\n")
        f.write("| Normalized term | Sources | Source SecIDs |\n|---|---:|---|\n")
        for c in crossed[:25]:
            f.write(f"| {c['normalized_term']} | {c['source_count']} | {', '.join(s.replace('secid:reference/', '') for s in c['sources'])} |\n")

        f.write("\n## Metadata-only stubs (no extracted terms)\n\n")
        f.write(f"Total: {metadata_only_sources}. These are glossary entries whose source is either license-restricted or pending extraction.\n\n")
    return path


def write_readme():
    path = OUT_DIR / "README.md"
    with open(path, "w") as f:
        f.write("""# Glossary corpus

Aggregate index of every `subtype: ["glossary"]` entry in this repo, with terms merged into a single corpus and a cross-source comparison view.

## Files

- `corpus.csv` / `corpus.json` — one row per (source, term). The full unified dataset.
- `cross-source.csv` / `cross-source.json` — every term that appears in 2+ sources, with each source's definition side-by-side. Useful for answering "what does NIST vs IETF vs OWASP say about X?".
- `stats.md` — generated counts (terms per source, top cross-source overlaps, etc.).

## How it's built

`python3 tools-resources/utils/build_glossary_corpus.py` walks every `reference/*/*/*-metadata.json` carrying `subtype: ["glossary"]`, loads the sibling `*-terms.json`, and aggregates. Re-run the script after adding or refreshing any source's extraction.

## Schema

`corpus.csv` columns:

| Column | Type | Notes |
|---|---|---|
| `source_secid` | string | The glossary's full SecID (e.g., `secid:reference/nist.gov/csrc-glossary`) |
| `source_name` | string | Human-friendly source name from the entry's metadata |
| `license_spdx` | string | SPDX license identifier (or `NOASSERTION` if unknown) |
| `publicly_redistributable` | bool | Whether definitions in this source can be redistributed |
| `term` | string | The term name as published |
| `normalized_term` | string | Lowercased + punctuation-stripped form used for cross-source matching |
| `definition` | string | The definition body |
| `source_anchor` | URL | Direct link back to the term page (or section anchor) |
| `notes` | string | Per-source notes (categories, "see also" links, source citation, etc.) |

`cross-source.csv` is the same schema repeated for every term that appears in multiple sources, with an additional `source_count` column.

## Why a normalized term

The `normalized_term` column collapses surface variation so that:
- `"Two-Factor Authentication"`, `"two-factor authentication"`, `"Two-factor authentication (2FA)"` all match.
- Trailing acronyms in parentheses are dropped (the corpus still preserves the original term in `term`).
- Whitespace and punctuation are normalized.

This is best-effort; it doesn't catch semantic variants (`"2FA"` vs `"two-factor authentication"`). For deeper de-dup the `notes` field often carries acronym/alias info from the source.
""")
    return path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows, source_counts = build_corpus()
    crossed = build_cross_source(rows)
    csv_path, json_path = write_corpus(rows)
    cross_csv, cross_json = write_cross_source(crossed)
    stats_path = write_stats(rows, crossed, source_counts)
    readme_path = write_readme()
    print(f"Wrote {len(rows):,} term-rows from {sum(1 for s in source_counts.values() if s['term_count']>0)} sources")
    print(f"Cross-source overlaps: {len(crossed):,} terms")
    print(f"  {csv_path}")
    print(f"  {json_path}")
    print(f"  {cross_csv}")
    print(f"  {cross_json}")
    print(f"  {stats_path}")
    print(f"  {readme_path}")


if __name__ == "__main__":
    main()
