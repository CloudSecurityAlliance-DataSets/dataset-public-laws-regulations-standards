#!/usr/bin/env python3
"""Parse CIRCIA NPRM (Federal Register XML) into per-section CSV/JSON.

Source: circia-nprm.xml — the Federal Register XML of CISA's Notice of
Proposed Rulemaking implementing the Cyber Incident Reporting for
Critical Infrastructure Act of 2022 (CIRCIA). Published 2024-04-04,
Docket CISA-2022-0010, RIN 1670-AA04. The proposed rule adds 6 CFR
Part 226 with 20 sections (§ 226.1 through § 226.20).

The Federal Register XML uses <SECTION> wrappers with <SECTNO> (section
number) and <SUBJECT> (title) plus prose <P> elements. We extract one
row per § section.

Output:
  circia-sections.{csv,json}  — one row per proposed rule section
"""
import csv
import json
import re
import xml.etree.ElementTree as ET


def text_of(el):
    if el is None:
        return ""
    parts = []
    if el.text:
        parts.append(el.text)
    for child in el:
        parts.append(text_of(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def main():
    tree = ET.parse("circia-nprm.xml")
    root = tree.getroot()
    rows = []
    for sec in root.iter("SECTION"):
        secno_el = sec.find("SECTNO")
        subj_el = sec.find("SUBJECT")
        secno = (text_of(secno_el).strip() if secno_el is not None else "").replace("§", "").strip()
        title = text_of(subj_el).strip().rstrip(".") if subj_el is not None else ""
        # Body: all <P> after <SUBJECT>
        body_parts = []
        for child in sec:
            if child.tag in ("SECTNO", "SUBJECT"):
                continue
            t = text_of(child)
            if t.strip():
                body_parts.append(t)
        body = re.sub(r"\s+", " ", " ".join(body_parts)).strip()
        if not secno:
            continue
        # Extract section ID — e.g., "226.1" from "§ 226.1"
        m = re.search(r"(\d+\.\d+(?:\(\w+\))?)", secno)
        sec_id = m.group(1) if m else secno
        rows.append({
            "section": sec_id,
            "title": title,
            "content": body,
        })

    def sort_key(r):
        parts = r["section"].split(".")
        try:
            return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
        except ValueError:
            return (999, 0)

    rows.sort(key=sort_key)
    fields = ["section", "title", "content"]
    with open("circia-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("circia-sections.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Sections: {len(rows)}")
    for r in rows:
        print(f"  § {r['section']}: {r['title']}")


if __name__ == "__main__":
    main()
