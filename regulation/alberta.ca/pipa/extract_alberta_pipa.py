#!/usr/bin/env python3
"""Parse Alberta Personal Information Protection Act (SA 2003 c P-6.5) into CSV/JSON.

Marker emits section bodies with the section's first subsection inline as
"**N(1)**". A section without subsections is emitted as "**N**" followed
by the body. Both forms are list-prefixed ("- "). Section titles appear
as level-1 markdown headings ("# **Title**") immediately before the
first subsection marker.

Output:
  alberta-pipa-sections.{csv,json}  — one row per section
"""
import csv
import json
import re


# Section start: optional list dash, then either
#   **N(1)** ...    (section with numbered subsections)
#   **N** Capital   (single-paragraph section — N followed by a capital letter)
# In both cases N may be "13.1" etc. for sub-numbered amendments.
SEC_RE = re.compile(
    r"^[-\s]*\*\*(\d+(?:\.\d+)?)(?:\((?:\*?1\*?|i)\))?\*\*\s+(?=[A-Z])",
    re.MULTILINE,
)


def main():
    md = open("pipa.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)  # strip page-break markers

    # Find all section starts and grab the preceding "# **Title**" heading
    matches = list(SEC_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        sec_num = m.group(1)
        # Title heading appears in the ~300 chars before this match
        prefix = md[max(0, m.start() - 600):m.start()]
        title_match = re.findall(
            r"^#+\s+\*\*([^*\n]+?)\*\*\s*$",
            prefix,
            re.MULTILINE,
        )
        title = title_match[-1].strip() if title_match else ""
        body_start = m.start()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        rows.append({
            "section": sec_num,
            "title": title,
            "content": body,
        })

    # Dedupe — TOC entries near top of file may produce duplicate IDs; keep longest
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
    with open("alberta-pipa-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("alberta-pipa-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(final)}")
    for r in final[:3]:
        print(f"  § {r['section']}: {r['title'][:60]}")
    if len(final) > 6:
        print(f"  ...")
        for r in final[-3:]:
            print(f"  § {r['section']}: {r['title'][:60]}")


if __name__ == "__main__":
    main()
