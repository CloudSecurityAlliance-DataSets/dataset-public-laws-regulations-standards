#!/usr/bin/env python3
"""Parse the Utah Consumer Privacy Act (UCPA, SB 227) into per-section CSV/JSON.

UCPA adds Chapter 61 to Title 13 of the Utah Code: sections 13-61-101
through 13-61-405 organized across multiple parts.

Output:
  ucpa-sections.{csv,json}
"""
import csv
import json
import re


SEC_RE = re.compile(
    r"(13-61-\d{3})\.\s+([A-Z][^|\n]+?)\s*(?:\.[\s\*]|\|)",
)


def main():
    md = open("ucpa.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    matches = list(SEC_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        section_id = m.group(1)
        name = m.group(2).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        rows.append({
            "section": section_id,
            "name": name,
            "content": body,
        })
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section"]] = r
    final = sorted(by_id.values(), key=lambda r: r["section"])

    fields = ["section", "name", "content"]
    with open("ucpa-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("ucpa-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Utah Code sections: {len(final)}")
    for r in final:
        print(f"  {r['section']}: {r['name'][:60]}")


if __name__ == "__main__":
    main()
