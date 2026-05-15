#!/usr/bin/env python3
"""Parse Executive Order 14028 (Improving the Nation's Cybersecurity) into per-section CSV/JSON.

EO 14028 was issued 2021-05-12. Marker's markdown output preserves the
EO's section structure: "Section 1" for the first section, then "Sec. 2"
through "Sec. 11" for the remainder, with each marker italicized and
list-prefixed in the markdown ("- *Sec. 2*. *Title*. (a)...").

Output:
  eo-14028-sections.{csv,json}  — one row per section
"""
import csv
import json
import re


SEC_RE = re.compile(
    r"^\s*-?\s*\*(?:Section|Sec\.)\s+(\d+)\*\.\s*\*([^*]+?)\*\.\s*",
    re.MULTILINE,
)


def main():
    md = open("eo-14028.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    matches = list(SEC_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        sec_num = int(m.group(1))
        title = m.group(2).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        rows.append({
            "section": sec_num,
            "title": title,
            "content": body,
        })
    rows.sort(key=lambda r: r["section"])
    fields = ["section", "title", "content"]
    with open("eo-14028-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("eo-14028-sections.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(rows)}")
    for r in rows:
        print(f"  Sec {r['section']}: {r['title'][:60]}")


if __name__ == "__main__":
    main()
