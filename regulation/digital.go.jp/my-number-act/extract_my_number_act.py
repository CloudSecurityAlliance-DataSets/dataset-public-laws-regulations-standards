#!/usr/bin/env python3
"""Parse Japan's My Number Act into per-article CSV/JSON.

Format: "(Title)" on its own line immediately precedes "Article N" on its
own line; body text follows until the next such pair. Mirrors the fix
applied to APPI's extract_appi.py in this repo.
"""
import csv
import json
import re

ART_RE = re.compile(r"^Article\s+(\d+(?:-\d+)?)\s*$", re.MULTILINE)
TITLE_RE = re.compile(r"^\(([^)]+)\)\s*$", re.MULTILINE)


def main():
    text = open("my-number-act.txt", encoding="utf-8").read()
    # Strip page-number-only lines and form feeds
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

    matches = list(ART_RE.finditer(text))
    rows = []
    for i, m in enumerate(matches):
        art = m.group(1)
        content_start = m.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = re.sub(r"\s+", " ", text[content_start:content_end]).strip()

        search_start = matches[i - 1].end() if i > 0 else 0
        preceding = text[search_start:m.start()]
        title_matches = list(TITLE_RE.finditer(preceding))
        title = title_matches[-1].group(1).strip() if title_matches else None

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
    with open("my-number-act-articles.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("my-number-act-articles.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)

    print(f"Articles: {len(final)}")
    print(f"  First: {final[0]['article']} ({final[0]['title']})")
    print(f"  Last:  {final[-1]['article']} ({final[-1]['title']})")
    missing = [r["article"] for r in final if not r["title"]]
    print(f"  Missing titles: {len(missing)}")


if __name__ == "__main__":
    main()
