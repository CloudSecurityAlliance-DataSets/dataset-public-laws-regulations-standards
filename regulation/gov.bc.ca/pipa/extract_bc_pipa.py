#!/usr/bin/env python3
"""Parse BC Personal Information Protection Act (SBC 2003 c 63) into per-section CSV/JSON.

BC Laws publishes consolidated legislation in XML using its own
namespace (`http://www.gov.bc.ca/2013/legislation/act`) plus the
BC-Legislation child namespace (`http://www.gov.bc.ca/2013/bclegislation`)
for `<bcl:part>`, `<bcl:section>`, etc. The XML preserves structure
explicitly, making per-section extraction straightforward.

Output:
  pipa-sections.{csv,json}  — one row per section with part / title / content
"""
import csv
import json
import re
import xml.etree.ElementTree as ET


NS = {
    "act": "http://www.gov.bc.ca/2013/legislation/act",
    "bcl": "http://www.gov.bc.ca/2013/bclegislation",
}


def text_of(el):
    parts = []
    if el.text:
        parts.append(el.text)
    for child in el:
        parts.append(text_of(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def main():
    tree = ET.parse("pipa.xml")
    root = tree.getroot()
    rows = []
    for part in root.iter(f"{{{NS['bcl']}}}part"):
        # Children: <bcl:num>, <bcl:text> (part title), then <bcl:section>s
        pn_el = part.find(f"{{{NS['bcl']}}}num")
        pt_el = part.find(f"{{{NS['bcl']}}}text")
        part_num = (pn_el.text or "").strip() if pn_el is not None else ""
        part_title = (pt_el.text or "").strip() if pt_el is not None else ""

        for section in part.iter(f"{{{NS['bcl']}}}section"):
            mn = section.find(f"{{{NS['bcl']}}}marginalnote")
            num = section.find(f"{{{NS['bcl']}}}num")
            title = text_of(mn).strip() if mn is not None else ""
            sec_num = (num.text or "").strip() if num is not None else ""
            body = text_of(section).strip()
            # Strip leading marginalnote and section number that text_of() already
            # included in the body
            if body.startswith(title):
                body = body[len(title):].strip()
            if body.startswith(sec_num):
                body = body[len(sec_num):].strip()
            body = re.sub(r"\s+", " ", body)
            rows.append({
                "section": sec_num,
                "title": title,
                "part": part_num,
                "part_name": part_title,
                "content": body,
            })

    fields = ["section", "title", "part", "part_name", "content"]
    with open("pipa-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("pipa-sections.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(rows)}")
    parts_seen = sorted({(r["part"], r["part_name"]) for r in rows if r["part"]},
                        key=lambda kv: int(kv[0]) if kv[0].isdigit() else 999)
    for pno, pname in parts_seen:
        cnt = sum(1 for r in rows if r["part"] == pno)
        print(f"  Part {pno}: {cnt} sections — {pname}")
    if rows:
        print(f"First: § {rows[0]['section']} — {rows[0]['title']}")
        print(f"Last:  § {rows[-1]['section']} — {rows[-1]['title']}")


if __name__ == "__main__":
    main()
