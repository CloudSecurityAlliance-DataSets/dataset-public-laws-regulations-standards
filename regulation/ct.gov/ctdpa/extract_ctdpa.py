#!/usr/bin/env python3
"""Parse Connecticut Data Privacy Act (CTDPA, PA 22-15) into per-section CSV/JSON.

CTDPA is structured as Sections 1 through 12 of Public Act 22-15. Marker
sometimes emits these as ordinary lines and sometimes as markdown list
items (- prefix), so the section regex must tolerate both.

Output:
  ctdpa-sections.{csv,json}
"""
import csv
import json
import re


SEC_RE = re.compile(
    r"^[-\s]*(?:Section|Sec\.)\s+(\d+)\.\s*(?:\(NEW\)\s*)?(?:\(\*Effective[^)]*\*\)\s*)?",
    re.MULTILINE,
)


def main():
    md = open("ctdpa.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    matches = list(SEC_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        sec = m.group(1)
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        rows.append({"section": int(sec), "content": body})
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section"]] = r
    final = sorted(by_id.values(), key=lambda r: r["section"])
    fields = ["section", "content"]
    with open("ctdpa-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("ctdpa-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(final)}")
    for r in final:
        print(f"  Sec {r['section']}: {r['content'][:80]}...")


if __name__ == "__main__":
    main()
