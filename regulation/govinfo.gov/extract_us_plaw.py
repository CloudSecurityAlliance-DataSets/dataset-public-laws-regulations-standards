#!/usr/bin/env python3
"""Parse US Public Law markdown (from govinfo.gov PLAW PDFs) into sections.

US Public Laws use structure:
  TITLE I—NAME OF TITLE
    Subtitle A—...
      SEC. 101. SHORT TITLE.
        (a) ...
        (b) ...
      SEC. 102. ...

The marker-extracted markdown from the PLAW PDF preserves this structure
but as flat text with newlines. This parser walks the markdown and emits
one row per section.

Output:
  <slug>-sections.{csv,json}

Usage (from a govinfo doc dir):
  python3 ../extract_us_plaw.py <input.md> <slug>
"""
import csv
import json
import re
import sys


SEC_RE = re.compile(
    r"^(?:#{1,6}\s*)?(?:\*+)?(?:''|`)?(?:SEC\.|Sec\.|SECTION|§)\s*(\d{1,4}[A-Z]?)\.?\s*(.+?)$",
    re.MULTILINE,
)
TITLE_RE = re.compile(r"^(?:#{1,6}\s*)?(?:\*+)?TITLE\s+([IVX]+)[-—](.+?)$", re.MULTILINE)
SUBTITLE_RE = re.compile(r"^(?:#{1,6}\s*)?(?:\*+)?Subtitle\s+([A-Z])[-—](.+?)$", re.MULTILINE)


def clean(s):
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def parse_md(md_path):
    md = open(md_path, encoding="utf-8").read()
    # Strip marker page-break markers like {N}---...
    md = re.sub(r"\{\d+\}-+", "", md)
    # Find all section starts
    sec_matches = list(SEC_RE.finditer(md))
    # Find title/subtitle starts — build ordered map of (offset, type, value)
    title_matches = [(m.start(), "title", m.group(1), clean(m.group(2))) for m in TITLE_RE.finditer(md)]
    subtitle_matches = [(m.start(), "subtitle", m.group(1), clean(m.group(2))) for m in SUBTITLE_RE.finditer(md)]
    nav = sorted(title_matches + subtitle_matches, key=lambda x: x[0])

    rows = []
    current_title = ""
    current_title_name = ""
    current_subtitle = ""
    current_subtitle_name = ""

    nav_idx = 0
    for i, m in enumerate(sec_matches):
        # Advance title/subtitle pointers up to this section's start
        while nav_idx < len(nav) and nav[nav_idx][0] < m.start():
            offset, kind, num, name = nav[nav_idx]
            if kind == "title":
                current_title, current_title_name = num, name
                current_subtitle, current_subtitle_name = "", ""
            else:
                current_subtitle, current_subtitle_name = num, name
            nav_idx += 1
        sec_num = m.group(1)
        sec_title = clean(m.group(2))
        # Body: text between this section's start and the next section's start
        body_start = m.end()
        body_end = sec_matches[i + 1].start() if i + 1 < len(sec_matches) else len(md)
        body = clean(md[body_start:body_end])
        rows.append({
            "section": sec_num,
            "title": sec_title,
            "title_roman": current_title,
            "title_name": current_title_name,
            "subtitle_letter": current_subtitle,
            "subtitle_name": current_subtitle_name,
            "content": body,
        })
    return rows


def main():
    if len(sys.argv) != 3:
        print("usage: extract_us_plaw.py <input.md> <slug>", file=sys.stderr)
        sys.exit(2)
    md_path, slug = sys.argv[1], sys.argv[2]
    rows = parse_md(md_path)
    if not rows:
        print("No sections found", file=sys.stderr)
        sys.exit(1)
    fields = ["section", "title", "title_roman", "title_name", "subtitle_letter", "subtitle_name", "content"]
    with open(f"{slug}-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open(f"{slug}-sections.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    # Stats
    from collections import Counter
    by_title = Counter(r["title_roman"] for r in rows if r["title_roman"])
    print(f"Sections: {len(rows)}")
    if by_title:
        for t, n in sorted(by_title.items()):
            print(f"  Title {t}: {n} sections")


if __name__ == "__main__":
    main()
