#!/usr/bin/env python3
"""Parse CCPA/CPRA from California leginfo HTML into structured CSV/JSON.

CCPA/CPRA is codified at California Civil Code §§1798.100-1798.199.100.
The leginfo.legislature.ca.gov HTML uses simple <div> tags; section
boundaries are marked by text starting "1798.NNN."

Output:
  ccpa-cpra-sections.{csv,json}  one row per CCC section
"""
import csv
import json
import re
from bs4 import BeautifulSoup


SECTION_RE = re.compile(r"^(1798\.\d+(?:\.\d+)?)\s*\.\s*(.+?)$", re.MULTILINE)


def main():
    html = open("ccpa-cpra.html", encoding="utf-8").read()
    # Extract all text content; California's HTML is mostly flat
    soup = BeautifulSoup(html, "html.parser")
    # Remove navigation/script/style noise
    for el in soup(["script", "style", "nav", "header", "footer"]):
        el.decompose()
    text = soup.get_text("\n", strip=True)
    # Normalize whitespace within lines
    text = re.sub(r"[\xa0]", " ", text)

    # Find all section starts
    matches = list(SECTION_RE.finditer(text))
    rows = []
    for i, m in enumerate(matches):
        sec_id = m.group(1)
        title_and_body = m.group(2).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        # Section title is the first line before the body proper.
        # In CCPA the first sentence is usually the title (e.g., "General Duties of Businesses...")
        # followed by lettered subsections (a), (b), etc.
        # Use a heuristic: title is the part before the first "(a)" subsection marker.
        full_section = title_and_body + " " + text[body_start:body_end]
        full_section = re.sub(r"\s+", " ", full_section).strip()
        m2 = re.search(r"\s+\(a\)\s+", full_section)
        if m2:
            title = full_section[: m2.start()].strip()
            body = full_section[m2.start():].strip()
        else:
            # No subsections — entire content is the section
            title = title_and_body.split(". ", 1)[0] if ". " in title_and_body else ""
            body = full_section
        rows.append({
            "section": sec_id,
            "title": title[:300],
            "content": body,
        })
    # Dedupe — TOC entries near top of file create duplicates; keep longest
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section"]] = r
    sorted_rows = sorted(by_id.values(), key=lambda r: tuple(int(x) for x in r["section"].split(".")))

    fields = ["section", "title", "content"]
    with open("ccpa-cpra-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(sorted_rows)
    with open("ccpa-cpra-sections.json", "w", encoding="utf-8") as f:
        json.dump(sorted_rows, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(sorted_rows)}")
    for r in sorted_rows[:3]:
        print(f"  {r['section']}: {r['title'][:60]}")
    if sorted_rows:
        print(f"  ...")
        print(f"  {sorted_rows[-1]['section']}: {sorted_rows[-1]['title'][:60]}")


if __name__ == "__main__":
    main()
