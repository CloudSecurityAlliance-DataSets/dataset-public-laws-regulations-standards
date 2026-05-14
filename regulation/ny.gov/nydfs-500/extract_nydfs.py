#!/usr/bin/env python3
"""Parse 23 NYCRR Part 500 (NYDFS Cybersecurity Regulation) into per-section CSV/JSON.

Source: nydfs-500-consolidated.md (marker-extracted from dfs.ny.gov 2023-03 PDF).
Each section is marked "Section 500.N Title."

Output:
  nydfs-500-sections.{csv,json}
"""
import csv
import json
import re


SEC_RE = re.compile(
    r"^(?:#{1,6}\s*)?(?:\*+)?Section\s+(500\.\d+)\s+(.+?)\.\s*(?:\*+)?$",
    re.MULTILINE,
)


def main():
    md = open("nydfs-500-consolidated.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)  # strip marker page-break tags
    matches = list(SEC_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        sec = m.group(1)
        title = m.group(2).strip().rstrip(".").rstrip("*").strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        rows.append({"section": sec, "title": title, "content": body})
    # Sort by section number
    rows.sort(key=lambda r: tuple(int(x) for x in r["section"].split(".")))
    fields = ["section", "title", "content"]
    with open("nydfs-500-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("nydfs-500-sections.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(rows)}")
    for r in rows:
        print(f"  {r['section']}: {r['title']}")


if __name__ == "__main__":
    main()
