#!/usr/bin/env python3
"""Parse the Colorado AI Act (SB 24-205) marker markdown into structured CSV/JSON.

The bill adds Part 17 to Article 1 of Title 6 of the Colorado Revised
Statutes, creating sections 6-1-1701 through 6-1-1707. Each CRS section
becomes one row.

Output:
  ai-act-sections.{csv,json}  — one row per CRS section (6-1-1701, ...)
"""
import csv
import json
import re


# Match "6-1-1701. Definitions." style headers (numeric IDs with periods)
CRS_RE = re.compile(
    r"^[\-\s]*(6-1-\d{4})\.\s+([^.\n]+?)\.\s",
    re.MULTILINE,
)


def main():
    md = open("ai-act.md", encoding="utf-8").read()
    # Strip page markers
    md = re.sub(r"\{\d+\}-+", "", md)
    matches = list(CRS_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        section_id = m.group(1)
        name = m.group(2).strip()
        # Content: from end of header to start of next CRS section header
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        rows.append({
            "section": section_id,
            "name": name,
            "content": body,
        })
    # Dedupe — TOC at the top may produce duplicate IDs; keep the longest body
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section"]] = r
    final = sorted(by_id.values(), key=lambda r: r["section"])

    fields = ["section", "name", "content"]
    with open("ai-act-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("ai-act-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"CRS sections: {len(final)}")
    for r in final:
        print(f"  {r['section']}: {r['name'][:60]}")


if __name__ == "__main__":
    main()
