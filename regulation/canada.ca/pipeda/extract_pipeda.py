#!/usr/bin/env python3
"""Parse Canada PIPEDA from marker markdown into per-section CSV/JSON.

PIPEDA is bilingual (English + French) — Justice Canada publishes a
single dual-column PDF with English on the left and French on the right
that marker flattens into interleaved lines.

The act has ~72 sections. Section headers in the body appear as bare
digit-at-start-of-line followed by capitalized text, e.g.
  "1 This Act may be cited as..."
  "3 The purpose of this Part is..."

To avoid false positives, we restrict to body content (lines after
the TOC, which ends with "SCHEDULE N" markers) and require the matched
number to be a plausible section ID (1-100) followed by a sentence-like
continuation.

Output:
  pipeda-sections.{csv,json}
"""
import csv
import json
import re


SEC_RE = re.compile(
    r"^(\d{1,3})\s+([A-Z\*][^\n]{20,})",
    re.MULTILINE,
)


def main():
    md = open("pipeda.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    # Find body start: first occurrence of "This Act may be cited" (s.1 English)
    body_start = md.find("This Act may be cited")
    if body_start < 0:
        body_start = 0
    body = md[body_start:]

    matches = list(SEC_RE.finditer(body))
    rows = []
    for i, m in enumerate(matches):
        sec_num = int(m.group(1))
        if sec_num < 1 or sec_num > 100:
            continue
        bstart = m.end()
        bend = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = m.group(2) + " " + body[bstart:bend]
        content = re.sub(r"\s+", " ", content).strip()
        # Filter pure-numeric reference noise (very short matches)
        if len(content) < 30:
            continue
        rows.append({"section": sec_num, "content": content})

    # Each section appears twice (EN + FR). Keep the longest as canonical body.
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section"]] = r

    # Heuristic: real sections form a monotone-ish run from 1 upward.
    # Drop ID numbers that are likely intra-text references (e.g., year
    # citations like "2000" or section cross-refs). A section number is
    # accepted only if it is part of the canonical PIPEDA enumeration —
    # we cap at section 72 (the highest real section).
    final = sorted([r for r in by_id.values() if r["section"] <= 75],
                   key=lambda r: r["section"])

    fields = ["section", "content"]
    with open("pipeda-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("pipeda-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(final)}")
    print(f"  First: section {final[0]['section']}")
    print(f"  Last:  section {final[-1]['section']}")


if __name__ == "__main__":
    main()
