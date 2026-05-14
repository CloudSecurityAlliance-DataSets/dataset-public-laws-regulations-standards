#!/usr/bin/env python3
"""Parse India Digital Personal Data Protection Act, 2023 (DPDP) into per-section CSV/JSON.

DPDP has 44 sections in 9 chapters. Marker emits section headers as
"**N.**" at line start sometimes and as "- **N.**" (list-prefixed)
elsewhere; tolerate both. Subclause markers like "**N.** (*1*)"
should be matched as section N, not section N-subclause.

Output:
  dpdp-sections.{csv,json}
"""
import csv
import json
import re


SEC_RE = re.compile(
    r"^[-\s]*(?:\*\*)?(\d+)\.(?:\*\*)?\s+(?:\(\*?\d+\*?\)|[A-Z])",
    re.MULTILINE,
)


def main():
    md = open("dpdp.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    matches = list(SEC_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        sec = int(m.group(1))
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        rows.append({"section": sec, "content": body})
    # Dedupe; keep longest body
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section"]] = r
    final = sorted(by_id.values(), key=lambda r: r["section"])
    fields = ["section", "content"]
    with open("dpdp-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("dpdp-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(final)}")
    print(f"  First section: {final[0]['section']}")
    print(f"  Last section: {final[-1]['section']}")
    sec_ids = [r["section"] for r in final]
    expected = set(range(1, 45))
    missing = sorted(expected - set(sec_ids))
    if missing:
        print(f"  Missing: {missing}")


if __name__ == "__main__":
    main()
