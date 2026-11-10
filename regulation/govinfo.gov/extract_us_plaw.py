#!/usr/bin/env python3
"""Parse US Public Law / U.S. Code markdown (from govinfo.gov PDFs) into sections.

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
    r'^(?:#{1,6}\s*)?(?:\*+)?(?:["\'`]+)?(SEC\.|Sec\.|SECTION|§)\s*(\d{1,6}[A-Za-z]?)\.?\s+(.+?)$',
    re.MULTILINE,
)
TITLE_RE = re.compile(r"^(?:#{1,6}\s*)?(?:\*+)?TITLE\s+([IVX]+)[-—](.+?)$", re.MULTILINE)
SUBTITLE_RE = re.compile(r"^(?:#{1,6}\s*)?(?:\*+)?Subtitle\s+([A-Z])[-—](.+?)$", re.MULTILINE)

# Out-of-scope trailing sections present on shared PDF pages
EXCLUDED_SECTIONS = {
    "coppa": {"6551"},  # Chapter 91A (15 U.S.C. 6551) follows Chapter 91 (COPPA, 6501-6506)
    "cfaa": {"1031"},   # 18 U.S.C. 1031 follows 18 U.S.C. 1030 (CFAA)
}


def clean(s):
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def parse_md(md_path, slug=""):
    md = open(md_path, encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    def _is_clerical_toc(m):
        raw_line = m.group(0).strip()
        kw = m.group(1)
        rest = m.group(3).strip()
        if re.search(r"(?:''|\")\.$", rest):
            return True
        if kw == "Sec." and not raw_line.startswith("#") and "**" not in raw_line:
            if "—" not in rest and "--" not in rest and not rest.startswith("(") and len(rest) < 120:
                return True
        return False

    sec_matches = [m for m in SEC_RE.finditer(md) if not _is_clerical_toc(m)]
    title_matches = [(m.start(), "title", m.group(1), clean(m.group(2))) for m in TITLE_RE.finditer(md)]
    subtitle_matches = [(m.start(), "subtitle", m.group(1), clean(m.group(2))) for m in SUBTITLE_RE.finditer(md)]
    nav = sorted(title_matches + subtitle_matches, key=lambda x: x[0])

    # If the document has TITLE I, any section between Sec. 1 (Table of Contents)
    # and the start of TITLE I is an inline Table of Contents entry.
    first_title_offset = title_matches[0][0] if title_matches else None

    rows = []
    current_title = ""
    current_title_name = ""
    current_subtitle = ""
    current_subtitle_name = ""

    nav_idx = 0
    for i, m in enumerate(sec_matches):
        if first_title_offset is not None and i > 0 and m.start() < first_title_offset:
            continue
        while nav_idx < len(nav) and nav[nav_idx][0] < m.start():
            offset, kind, num, name = nav[nav_idx]
            if kind == "title":
                current_title, current_title_name = num, name
                current_subtitle, current_subtitle_name = "", ""
            else:
                current_subtitle, current_subtitle_name = num, name
            nav_idx += 1
        sec_num = m.group(2)
        if sec_num in EXCLUDED_SECTIONS.get(slug, set()):
            continue
        sec_title = clean(m.group(3)).rstrip("*").strip()
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

    # Deduplicate TOC stubs vs body sections (keep the longer body entry)
    by_sec = {}
    order = []
    for r in rows:
        s = r["section"]
        if s not in by_sec:
            by_sec[s] = r
            order.append(s)
        elif len(r["content"]) > len(by_sec[s]["content"]):
            by_sec[s] = r
    return [by_sec[s] for s in order]


def main():
    if len(sys.argv) != 3:
        print("usage: extract_us_plaw.py <input.md> <slug>", file=sys.stderr)
        sys.exit(2)
    md_path, slug = sys.argv[1], sys.argv[2]
    rows = parse_md(md_path, slug=slug)
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
        f.write("\n")
    from collections import Counter
    by_title = Counter(r["title_roman"] for r in rows if r["title_roman"])
    print(f"{slug}: Sections: {len(rows)}")
    if by_title:
        for t, n in sorted(by_title.items()):
            print(f"  Title {t}: {n} sections")


if __name__ == "__main__":
    main()
