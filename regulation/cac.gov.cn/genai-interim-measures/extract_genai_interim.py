#!/usr/bin/env python3
"""Parse the China CAC Interim Measures for the Management of Generative
Artificial Intelligence Services (effective 2023-08-15) into per-article CSV/JSON.

Source: translation-of-web-page.txt — an English translation of the
CAC's official text. The text is organized as 24 articles across 5
chapters; each article is marked "Article N" at line start, chapters as
"Chapter N" (Arabic or Roman numerals).

Output:
  genai-interim-articles.{csv,json}  — one row per article with chapter context
"""
import csv
import json
import re


ART_RE = re.compile(r"^Article\s+(\d+)[:\s]+(.+)$", re.MULTILINE)
CHAPTER_RE = re.compile(r"^Chapter\s+([IVX0-9]+)\s+(.+?)$", re.MULTILINE)


def roman_to_int(s):
    s = s.upper()
    if s.isdigit():
        return int(s)
    vals = {"I": 1, "V": 5, "X": 10}
    out, prev = 0, 0
    for c in reversed(s):
        v = vals.get(c, 0)
        out += -v if v < prev else v
        prev = v
    return out


def main():
    text = open("translation-of-web-page.txt", encoding="utf-8").read()

    # Find all chapter boundaries
    chapters = [(m.start(), roman_to_int(m.group(1)), m.group(2).strip())
                for m in CHAPTER_RE.finditer(text)]
    # Chapter 1 is implicit at start (no header)
    if not chapters or chapters[0][1] != 1:
        chapters.insert(0, (0, 1, "General Provisions"))

    def chapter_for(pos):
        cur = (1, "General Provisions")
        for start, num, name in chapters:
            if start <= pos:
                cur = (num, name)
            else:
                break
        return cur

    # Find all articles
    rows = []
    art_matches = list(ART_RE.finditer(text))
    for i, m in enumerate(art_matches):
        art_num = int(m.group(1))
        body_start = m.end()
        body_end = art_matches[i + 1].start() if i + 1 < len(art_matches) else len(text)
        body = re.sub(r"\s+", " ", text[body_start:body_end]).strip()
        # Strip leading article-number echo
        body = re.sub(r"^\d+\s*\.?\s*", "", body)
        ch_num, ch_name = chapter_for(m.start())
        # Pull a short title from the first ~80 chars of the article body
        first_period = body.find(". ")
        if first_period > 0 and first_period < 100:
            short_title = body[:first_period]
        else:
            short_title = ""
        rows.append({
            "article": art_num,
            "chapter": ch_num,
            "chapter_name": ch_name,
            "short_title": short_title[:120],
            "content": body,
        })

    fields = ["article", "chapter", "chapter_name", "short_title", "content"]
    with open("genai-interim-articles.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("genai-interim-articles.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Articles: {len(rows)}")
    print(f"Chapters: {len(chapters)}")
    for ch_num, ch_name in sorted({(r["chapter"], r["chapter_name"]) for r in rows}):
        cnt = sum(1 for r in rows if r["chapter"] == ch_num)
        print(f"  Ch {ch_num} ({cnt} articles): {ch_name}")


if __name__ == "__main__":
    main()
