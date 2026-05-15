#!/usr/bin/env python3
"""Parse California SB-327 (Security of Connected Devices) into per-section CSV/JSON.

SB-327, codified at California Civil Code §§ 1798.91.04 through .06,
is titled "Security of Connected Devices". The leginfo.legislature.ca.gov
page requires JavaScript rendering to populate the text (fetched via
Playwright into sb-327.html).

The 3 sections are:
  1798.91.04 — Reasonable security feature requirement (the operative requirement)
  1798.91.05 — Definitions
  1798.91.06 — Limitations / exemptions

Output:
  sb-327-sections.{csv,json}
"""
import csv
import json
import re
from bs4 import BeautifulSoup


SEC_RE = re.compile(r"(1798\.91\.\d+)\.\s+", re.DOTALL)


def main():
    html = open("sb-327.html", encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)

    matches = list(SEC_RE.finditer(text))
    rows = []
    for i, m in enumerate(matches):
        sec_id = m.group(1)
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        rows.append({"section": sec_id, "content": body})

    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section"]] = r

    final = sorted(by_id.values(), key=lambda r: r["section"])
    fields = ["section", "content"]
    with open("sb-327-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("sb-327-sections.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(final)}")
    for r in final:
        print(f"  § {r['section']}: {r['content'][:100]}")


if __name__ == "__main__":
    main()
