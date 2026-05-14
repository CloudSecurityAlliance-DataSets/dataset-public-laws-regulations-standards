#!/usr/bin/env python3
"""Parse Singapore Personal Data Protection Act 2012 (PDPA) into per-section CSV/JSON.

Source: pdpa-wholedoc.html — fetched via Playwright from
https://sso.agc.gov.sg/Act/PDPA2012?WholeDoc=1 (the ?WholeDoc=1 query
expands lazy-loaded provisions into a single document; the default view
only renders ~11 provisions for the current part).

Singapore Statutes Online structures each section as a `div.prov1`
containing two tables:
  1. Header table with `td.prov1Hdr id="prN-"` — the marginal-note title
  2. Body table — a leading "N." section-number marker followed by text

Parts wrap groups of sections in `td.part id="P1N-"` containers.

Output:
  pdpa-sections.{csv,json}  — one row per section with part / title / content
"""
import csv
import json
import re
from bs4 import BeautifulSoup


SECTION_NUM_RE = re.compile(r"^(\d+[A-Z]*)\.\s*")


def main():
    soup = BeautifulSoup(
        open("pdpa-wholedoc.html", encoding="utf-8").read(),
        "html.parser",
    )

    # Map each Part container to (part_number, part_name) — name is in
    # the first heading-style element inside the part header td.
    part_map = []
    for p in soup.find_all("td", class_="part"):
        pno = p.find(class_="partNo")
        pname = p.find(class_=re.compile(r"(partName|partHd|partTitle)"))
        if not pname:
            # Fall back to first sibling text after partNo
            all_text = p.get_text(" ", strip=True)
            after = all_text[len(pno.get_text(strip=True)):].strip() if pno else all_text
            pname_text = after.split("Division")[0].strip()
        else:
            pname_text = pname.get_text(" ", strip=True)
        part_map.append({
            "el": p,
            "number": pno.get_text(strip=True) if pno else "",
            "name": pname_text[:200],
        })

    def part_for(el):
        """Return (number, name) for the closest enclosing part."""
        cur = el
        while cur is not None:
            for pm in part_map:
                if pm["el"] is cur:
                    return pm["number"], pm["name"]
            cur = cur.parent
        return "", ""

    rows = []
    for prov in soup.find_all("div", class_="prov1"):
        hdr = prov.find("td", class_="prov1Hdr")
        title = hdr.get_text(" ", strip=True) if hdr else ""
        # Body is the rest of the div minus the header table
        body_text = prov.get_text(" ", strip=True)
        if title:
            body_text = body_text[len(title):].strip()
        m = SECTION_NUM_RE.match(body_text)
        if m:
            sec_num = m.group(1)
            content = body_text[m.end():].strip()
        else:
            sec_num = ""
            content = body_text
        part_no, part_name = part_for(prov)
        rows.append({
            "section": sec_num,
            "title": title[:300],
            "part": part_no,
            "part_name": part_name,
            "content": re.sub(r"\s+", " ", content),
        })

    fields = ["section", "title", "part", "part_name", "content"]
    with open("pdpa-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("pdpa-sections.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(rows)}")
    parts_seen = sorted({(r["part"], r["part_name"]) for r in rows if r["part"]})
    print(f"Parts covered: {len(parts_seen)}")
    for p, n in parts_seen[:5]:
        cnt = sum(1 for r in rows if r["part"] == p)
        print(f"  {p}: {cnt} sections — {n[:60]}")
    if rows:
        print(f"First section: § {rows[0]['section']} — {rows[0]['title']}")
        print(f"Last section:  § {rows[-1]['section']} — {rows[-1]['title']}")


if __name__ == "__main__":
    main()
