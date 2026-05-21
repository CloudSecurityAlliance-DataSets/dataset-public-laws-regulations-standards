#!/usr/bin/env python3
"""Extract NIST CSRC Glossary into structured term/definition data.

Uses the pre-downloaded glossary-export.json from csrc.nist.gov/glossary
(the "Export" / JSON download endpoint).

For each parent term, emits one row per definition source. Terms without
definitions (e.g., abbreviation-only entries) are emitted with a notes
field indicating they are reference-only.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "glossary-export.json"
DIRNAME = "csrc-glossary"

OUT_MD = HERE / f"{DIRNAME}.md"
OUT_CSV = HERE / f"{DIRNAME}-terms.csv"
OUT_JSON = HERE / f"{DIRNAME}-terms.json"


def normalize(s: str) -> str:
    if s is None:
        return ""
    return " ".join(s.split()).strip()


def main() -> None:
    data = json.load(SRC.open(encoding="utf-8-sig"))
    parents = data["parentTerms"]
    rows: list[dict] = []

    for entry in parents:
        term = normalize(entry.get("term", ""))
        if not term:
            continue
        link = entry.get("link") or ""
        abbr_syn = entry.get("abbrSyn") or []
        abbr_text = "; ".join(normalize(a.get("text", "")) for a in abbr_syn if a.get("text"))
        defs = entry.get("definitions") or []

        if not defs:
            # abbreviation/synonym-only entry
            note_parts = []
            if abbr_text:
                note_parts.append(f"abbr/syn: {abbr_text}")
            note_parts.append("no definition listed")
            rows.append({
                "term": term,
                "definition": "",
                "source_anchor": link,
                "notes": "; ".join(note_parts),
            })
            continue

        for d in defs:
            definition = normalize(d.get("text", ""))
            sources = d.get("sources") or []
            src_texts = "; ".join(normalize(s.get("text", "")) for s in sources if s.get("text"))
            note_parts = []
            if abbr_text:
                note_parts.append(f"abbr/syn: {abbr_text}")
            if src_texts:
                note_parts.append(f"source: {src_texts}")
            rows.append({
                "term": term,
                "definition": definition,
                "source_anchor": link,
                "notes": "; ".join(note_parts),
            })

    # Write JSON
    OUT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Write CSV
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["term", "definition", "source_anchor", "notes"])
        w.writeheader()
        w.writerows(rows)

    # Write Markdown
    with OUT_MD.open("w", encoding="utf-8") as fh:
        fh.write("# NIST CSRC Glossary\n\n")
        fh.write(f"Total entries: {len(rows)} (from {len(parents)} parent terms)\n\n")
        fh.write(f"Source: {data.get('comment', '').strip()}\n\n")
        # Group by term so multiple definitions render under one heading
        from collections import OrderedDict
        grouped: OrderedDict[str, list[dict]] = OrderedDict()
        for r in rows:
            grouped.setdefault(r["term"], []).append(r)
        for term, entries in grouped.items():
            fh.write(f"## {term}\n\n")
            for e in entries:
                if e["definition"]:
                    fh.write(f"{e['definition']}\n\n")
                    if e["notes"]:
                        fh.write(f"*{e['notes']}*\n\n")
                else:
                    if e["notes"]:
                        fh.write(f"*{e['notes']}*\n\n")

    print(f"Wrote {len(rows)} rows to {OUT_CSV.name}, {OUT_JSON.name}, {OUT_MD.name}")


if __name__ == "__main__":
    main()
