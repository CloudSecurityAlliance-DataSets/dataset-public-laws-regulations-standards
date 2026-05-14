#!/usr/bin/env python3
"""Parse PIPEDA from Justice Canada XML into per-section CSV/JSON.

Justice Canada publishes consolidated federal statutes in a structured XML
format (see https://laws-lois.justice.gc.ca/eng/XML/P-8.6.xml). Each
<Section> element has a <Label> (the section number) and a <MarginalNote>
(the section title), with body content in <Text> and nested <Subsection>
elements. This XML preserves the section structure perfectly — far better
than re-extracting the bilingual PDF via marker.

Output:
  pipeda-sections.{csv,json}  — one row per section, with subsections inlined
"""
import csv
import json
import re
import xml.etree.ElementTree as ET


def text_of(el):
    """Recursive text extraction that ignores marker/anchor elements but keeps
    all natural-language content (including text inside Subsection, Definition,
    XRefExternal etc.)."""
    parts = []
    if el.text:
        parts.append(el.text)
    for child in el:
        parts.append(text_of(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def main():
    tree = ET.parse("pipeda.xml")
    root = tree.getroot()
    rows = []
    for section in root.iter("Section"):
        label = section.find("Label")
        if label is None or not (label.text or "").strip():
            continue
        sec_num = label.text.strip()
        margin = section.find("MarginalNote")
        title = (text_of(margin).strip() if margin is not None else "")
        body = text_of(section)
        # The Label text is included by text_of — strip it from the body prefix.
        body = body.strip()
        if body.startswith(title):
            body = body[len(title):].strip()
        if body.startswith(sec_num):
            body = body[len(sec_num):].strip()
        body = re.sub(r"\s+", " ", body)
        try:
            sec_sort = int(re.match(r"^(\d+)", sec_num).group(1))
        except (AttributeError, ValueError):
            sec_sort = 999
        rows.append({
            "section": sec_num,
            "_sort": sec_sort,
            "title": title,
            "content": body,
        })

    rows.sort(key=lambda r: (r["_sort"], r["section"]))
    for r in rows:
        del r["_sort"]

    fields = ["section", "title", "content"]
    with open("pipeda-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("pipeda-sections.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(rows)}")
    if rows:
        print(f"  First: § {rows[0]['section']} — {rows[0]['title']}")
        print(f"  Last:  § {rows[-1]['section']} — {rows[-1]['title']}")


if __name__ == "__main__":
    main()
