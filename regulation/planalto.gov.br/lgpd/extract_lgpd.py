#!/usr/bin/env python3
"""Parse LGPD (Brazil Law 13.709/2018) from planalto.gov.br HTML into structured CSV/JSON.

Brazilian federal laws on planalto.gov.br use HTML (windows-1252 encoded
on this URL pattern) with articles marked "Art. NN.º" (Portuguese
ordinal). LGPD has 65 articles.

Output:
  lgpd-articles.{csv,json}
"""
import csv
import json
import re
from bs4 import BeautifulSoup


# Match Article markers like "Art. 1º" or "Art. 65." possibly with º/° ordinal
ART_RE = re.compile(r"\bArt\.\s*(\d+)[º°ºo]?\s*\.?")


def main():
    raw = open("lgpd.html", "rb").read()
    html = raw.decode("windows-1252", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    for el in soup(["script", "style"]):
        el.decompose()
    text = soup.get_text("\n", strip=False)
    # Normalize whitespace but preserve structure
    text = re.sub(r"[\xa0\xc2]", " ", text)
    text = re.sub(r"\n+", "\n", text)

    # Find unique article markers, keeping highest occurrence position
    matches = list(ART_RE.finditer(text))
    by_num = {}
    for m in matches:
        num = int(m.group(1))
        by_num.setdefault(num, []).append((m.start(), m.end()))

    rows = []
    sorted_nums = sorted(by_num)
    for i, num in enumerate(sorted_nums):
        # Use the FIRST occurrence of this article in the body
        # (header references at the top of the HTML are usually summary; first body occurrence is most reliable)
        # Heuristic: take the occurrence that has the longest content before the next article
        candidates = by_num[num]
        # Body end = start of next article (any occurrence)
        next_num = sorted_nums[i + 1] if i + 1 < len(sorted_nums) else None
        if next_num is not None:
            next_starts = [s for s, _ in by_num[next_num]]
        else:
            next_starts = [len(text)]
        best = (0, "", 0)  # (length, content, start)
        for start, end in candidates:
            # find next-article start that is after this article's start
            next_ends = [ns for ns in next_starts if ns > start]
            body_end = min(next_ends) if next_ends else len(text)
            body = text[end:body_end]
            body = re.sub(r"\s+", " ", body).strip()
            # First sentence sometimes restates "Art. N" — strip it
            body = re.sub(r"^[º°ºo\.\s]*", "", body)
            if len(body) > best[0]:
                best = (len(body), body, start)
        rows.append({
            "article": num,
            "content": best[1][:50000],  # cap absurdly large
        })

    fields = ["article", "content"]
    with open("lgpd-articles.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("lgpd-articles.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Articles: {len(rows)}")
    print(f"  Art 1: {rows[0]['content'][:100]!r}")
    if len(rows) > 5:
        print(f"  Art 30 sample: {next((r['content'][:100] for r in rows if r['article']==30), '')!r}")
    print(f"  Art {rows[-1]['article']}: {rows[-1]['content'][:100]!r}")


if __name__ == "__main__":
    main()
