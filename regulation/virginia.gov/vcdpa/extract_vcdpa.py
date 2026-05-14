#!/usr/bin/env python3
"""Parse Virginia VCDPA from law.lis.virginia.gov HTML into structured CSV/JSON.

VCDPA is Virginia Code §§ 59.1-575 through 59.1-585. Each section is
marked by <b>§ 59.1-NNN. Title.</b> followed by paragraphs.

Output:
  vcdpa-sections.{csv,json}
"""
import csv
import json
import re
from bs4 import BeautifulSoup


def main():
    html = open("vcdpa.html", encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    for el in soup(["script", "style", "nav", "header", "footer"]):
        el.decompose()

    # Find all <b> tags that contain a section marker
    sec_pattern = re.compile(r"^§\s*(59\.1-\d+)\.?\s*(?:\(([^)]+)\))?\s*(.+?)\.?$")
    rows = []
    bolds = soup.find_all("b")
    for i, b in enumerate(bolds):
        t = b.get_text(" ", strip=True)
        m = sec_pattern.match(t)
        if not m:
            continue
        sec_id = m.group(1)
        effective = (m.group(2) or "").strip()
        title = (m.group(3) or "").strip()
        # Body: everything after this <b> until the next section <b>
        body_parts = []
        for sib in b.next_siblings:
            if hasattr(sib, "name") and sib.name == "b":
                stext = sib.get_text(" ", strip=True)
                if sec_pattern.match(stext):
                    break
            if hasattr(sib, "get_text"):
                body_parts.append(sib.get_text(" ", strip=True))
            elif isinstance(sib, str):
                body_parts.append(sib.strip())
        body = " ".join(p for p in body_parts if p)
        body = re.sub(r"\s+", " ", body).strip()
        rows.append({
            "section": sec_id,
            "effective": effective,
            "title": title,
            "content": body,
        })

    # Dedupe — if multiple versions of same section, keep the active one (no "Effective until" qualifier)
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section"])
        if not existing:
            by_id[r["section"]] = r
        else:
            # Prefer the one without "Effective until" (which means deprecated)
            cur_deprecated = "until" in existing.get("effective", "").lower()
            new_deprecated = "until" in r.get("effective", "").lower()
            if cur_deprecated and not new_deprecated:
                by_id[r["section"]] = r
            elif len(r["content"]) > len(existing["content"]):
                by_id[r["section"]] = r

    sorted_rows = sorted(by_id.values(), key=lambda r: tuple(int(x) for x in r["section"].split("-")[-1:]))

    fields = ["section", "effective", "title", "content"]
    with open("vcdpa-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(sorted_rows)
    with open("vcdpa-sections.json", "w", encoding="utf-8") as f:
        json.dump(sorted_rows, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(sorted_rows)}")
    for r in sorted_rows:
        print(f"  § {r['section']}: {r['title'][:60]}")


if __name__ == "__main__":
    main()
