#!/usr/bin/env python3
"""Parse Japan's Act on Protection of Personal Information (APPI) into per-article CSV/JSON.

APPI has 88 articles in 7 chapters (English translation from PPC).
Article headers in the marker output appear as "Article N <title>" or
"Article N-M <title>" (hyphenated supplementary articles like "Article 17-2").

Output:
  appi-articles.{csv,json}
"""
import csv
import json
import re


ART_RE = re.compile(
    r"^(?:#{1,6}\s+)?Article\s+(\d+(?:-\d+)?)\s*(.+?)$",
    re.MULTILINE,
)


def main():
    md = open("appi.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    matches = list(ART_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        art = m.group(1)
        title = re.sub(r"\s+", " ", m.group(2)).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        rows.append({
            "article": art,
            "title": title[:200],
            "content": body,
        })
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
    print(f"  First: Article {final[0]['article']}")
    print(f"  Last:  Article {final[-1]['article']}")


if __name__ == "__main__":
    main()
