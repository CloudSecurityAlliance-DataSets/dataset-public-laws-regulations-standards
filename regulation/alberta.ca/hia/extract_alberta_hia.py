#!/usr/bin/env python3
"""Parse Alberta Health Information Act (RSA 2000 c H-5) into CSV/JSON.

Uses the same section-marker convention as Alberta PIPA: marker emits
"**N(1)**" or "**N**" + Capital-letter body, optionally prefixed with a
list dash. Section titles appear as level-1 markdown headings
("# **Title**") immediately before the section's first marker.

Output:
  alberta-hia-sections.{csv,json}  — one row per section
"""
import csv
import json
import re


SEC_RE = re.compile(
    r"^[-\s]*\*\*(\d+(?:\.\d+)?)(?:\((?:\*?1\*?|i)\))?\*\*\s+(?=[A-Z])",
    re.MULTILINE,
)


def main():
    md = open("hia.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    matches = list(SEC_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        sec_num = m.group(1)
        prefix = md[max(0, m.start() - 600):m.start()]
        title_match = re.findall(r"^#+\s+\*\*([^*\n]+?)\*\*\s*$", prefix, re.MULTILINE)
        title = title_match[-1].strip() if title_match else ""
        body_start = m.start()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        rows.append({"section": sec_num, "title": title, "content": body})

    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section"]] = r

    def sort_key(r):
        parts = r["section"].split(".")
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)

    final = sorted(by_id.values(), key=sort_key)
    fields = ["section", "title", "content"]
    with open("alberta-hia-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("alberta-hia-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(final)}")
    print(f"  First: § {final[0]['section']} — {final[0]['title'][:60]}")
    print(f"  Last:  § {final[-1]['section']} — {final[-1]['title'][:60]}")


if __name__ == "__main__":
    main()
