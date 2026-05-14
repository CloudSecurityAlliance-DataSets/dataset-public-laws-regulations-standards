#!/usr/bin/env python3
"""Parse Quebec "Act respecting the protection of personal information in the
private sector" (CQLR c P-39.1, as amended by Law 25 / Bill 64) into CSV/JSON.

Source: loi-25.html fetched via Playwright from
https://www.legisquebec.gouv.qc.ca/en/document/cs/p-39.1 (legisquebec
is CloudFront-WAF-protected — automated curl returns 403).

LégisQuébec renders each section as `<div class="section" id="se:N">`
where N is the section number (e.g., "1", "1_1" for section 1.1, "26_1"
for section 26.1). Each section contains:
  - `<div class="Subsection SubsectionFirst">` with the section number
    and lead text
  - `<div class="Subsection">` for additional unnumbered paragraphs
  - `<div class="HistoricalNote">` with amendment citations

Output:
  loi-25-sections.{csv,json}  — one row per section
"""
import csv
import json
import re
from bs4 import BeautifulSoup


SEC_NUM_RE = re.compile(r"^(\d+(?:\.\d+)*)\s*\.\s*(.*)", re.DOTALL)


def main():
    soup = BeautifulSoup(open("loi-25.html", encoding="utf-8").read(), "html.parser")
    rows = []
    top_secs = [
        s for s in soup.find_all("div", class_="section")
        if s.get("id") and re.fullmatch(r"se:\d+(?:_\d+)*(?:_[a-z0-9]+)?", s.get("id"))
    ]
    for sec in top_secs:
        raw_id = sec.get("id")[3:]  # strip "se:"
        # Convert "1_1" → "1.1"
        sec_id = raw_id.replace("_", ".")

        # Drop HistoricalNote from content
        for hn in sec.find_all("div", class_="HistoricalNote"):
            hn.decompose()
        # Drop NoteInfo (annotations)
        for ni in sec.find_all("div", class_="NoteInfo"):
            ni.decompose()

        text = sec.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text)
        m = SEC_NUM_RE.match(text)
        if m:
            content = m.group(2).strip()
        else:
            content = text

        rows.append({
            "section": sec_id,
            "content": content,
        })

    def sort_key(r):
        parts = r["section"].split(".")
        try:
            return tuple(int(p) for p in parts)
        except ValueError:
            return (999, 0)

    rows.sort(key=sort_key)
    fields = ["section", "content"]
    with open("loi-25-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("loi-25-sections.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(rows)}")
    print(f"  First: § {rows[0]['section']}: {rows[0]['content'][:80]}")
    print(f"  Last:  § {rows[-1]['section']}: {rows[-1]['content'][:80]}")


if __name__ == "__main__":
    main()
