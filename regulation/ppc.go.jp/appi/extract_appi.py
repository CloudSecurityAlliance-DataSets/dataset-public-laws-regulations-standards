#!/usr/bin/env python3
"""Parse Japan's Act on Protection of Personal Information (APPI) into per-article CSV/JSON.

Fixes vs. the original extract_appi.py:
- Article titles are parenthetical headings that precede "Article N" in the
  source (e.g. "(Purpose)" then "Article 1 ..."), not text following it on
  the same line. The original regex looked in the wrong place, producing a
  meaningless truncated first-line "title" and a content field misaligned
  by one line.
- "Article 2" (Definitions) never appears as literal text in the marker
  PDF extraction (a source-extraction/OCR gap in appi.md, not a parsing
  bug) even though its content and preceding "(Definition)" heading are
  present. Recovered by manual insertion: Chapter I's table of contents
  states it covers "Articles 1 to 3", article 1 is Purpose and article 3
  is Overall Vision (both present), so the (Definition) block between them
  is Article 2 by elimination. A synthetic "Article 2" marker is inserted
  before "(Definition)" with this reasoning recorded in the metadata.
"""
import csv
import json
import re

MD_PATH = "appi.md"

ART_RE = re.compile(r"^(?:#{1,6}\s*)?(?:[-*]\s*)?\*{0,2}Article\s+(\d+(?:-\d+)?)\b\.?\*{0,2}\s*", re.MULTILINE)
TITLE_RE = re.compile(r"^\(([^)]+)\)\s*$", re.MULTILINE)


def main():
    md = open(MD_PATH, encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+\n?", "", md)  # strip marker page-break artifacts

    # Manual correction: recover the missing "Article 2" marker (see docstring).
    if not re.search(r"^Article\s+2\s*$", md, re.MULTILINE):
        md = md.replace("(Definition)", "(Definition)\n\nArticle 2", 1)

    matches = list(ART_RE.finditer(md))
    if not matches:
        raise SystemExit("No 'Article N' markers found — source format changed?")

    rows = []
    for i, m in enumerate(matches):
        art = m.group(1)
        content_start = m.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        content = md[content_start:content_end]

        # Look backward from this marker (up to the previous marker) for the
        # nearest "(...)" heading line — that is this article's title.
        search_start = matches[i - 1].end() if i > 0 else 0
        preceding = md[search_start:m.start()]
        title_matches = list(TITLE_RE.finditer(preceding))
        title = title_matches[-1].group(1).strip() if title_matches else None

        content = re.sub(r"\s+", " ", content).strip()
        rows.append({"article": art, "title": title, "content": content})

    by_id = {}
    for r in rows:
        existing = by_id.get(r["article"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["article"]] = r

    def sort_key(r):
        parts = r["article"].split("-")
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)

    final = sorted(by_id.values(), key=sort_key)

    fields = ["article", "title", "content"]
    with open("appi-articles.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("appi-articles.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)

    print(f"Articles: {len(final)}")
    print(f"  First: Article {final[0]['article']} ({final[0]['title']})")
    print(f"  Last:  Article {final[-1]['article']} ({final[-1]['title']})")
    missing_titles = [r["article"] for r in final if not r["title"]]
    print(f"  Missing titles: {missing_titles}")


if __name__ == "__main__":
    main()
