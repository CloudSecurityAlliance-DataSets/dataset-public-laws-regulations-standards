#!/usr/bin/env python3
"""Parse UK legislation.gov.uk CLML XML into structured CSV/JSON.

UK legislation uses Crown Legislation Markup Language (CLML):
  <Legislation>
    <Primary> or <Secondary> or <EuropeanUnionRetained>
      <Body>
        <Part NumberOfPart="1">
          <Chapter>
            <P1 id="section-1">      Section
              <Pnumber>1</Pnumber>
              <Title>Heading</Title>
              <P1para>
                <P2 id="section-1-1">  Subsection
                  <Pnumber>1</Pnumber>
                  <P2para><Text>...</Text></P2para>

For each section (P1), emit:
  - section          number (e.g., "1")
  - id               "section-1"
  - title            section heading (from <Title> or <Heading>)
  - part             Part number context
  - chapter          Chapter number context
  - content          full text of all subsections joined

Usage (from a UK reg dir):
  python3 ../extract_uk_legislation.py <input.xml> <slug>
"""
import csv
import json
import re
import sys
from lxml import etree

NS = "{http://www.legislation.gov.uk/namespaces/legislation}"


def all_text(el):
    """Get all text content of an element, joining with spaces."""
    if el is None:
        return ""
    text = etree.tostring(el, method="text", encoding="unicode")
    return re.sub(r"\s+", " ", text).strip()


def find_title(el):
    """UK CLML stores section titles either:
    - directly on the section (rare), in <Title> or <Heading>, OR
    - on a containing <Pblock>/<Group>/<PsubBlock> wrapper (common)
    Walk up the ancestor chain looking for the nearest title.
    """
    for tag in ("Title", "Heading"):
        sub = el.find(f"{NS}{tag}")
        if sub is not None:
            return all_text(sub)
    # Walk parents looking for a wrapper with a Title child
    for anc in el.iterancestors():
        anc_tag = anc.tag.split("}")[-1]
        if anc_tag in ("Pblock", "PsubBlock", "Group", "Part", "Chapter",
                       "P1group", "P2group",  # retained-EU UK wrappers
                       "EUChapter", "EUSection"):
            for tag in ("Title", "Heading"):
                sub = anc.find(f"{NS}{tag}")
                if sub is not None:
                    return all_text(sub)
        if anc_tag == "Body":
            break  # don't go above the legislation body
    return ""


def parse_sections(root):
    rows = []
    # Top-level sections live under Body/Part or Body/Group — NOT inside Schedule.
    # Filter P1 elements whose id starts with "section-" (not "schedule-N-paragraph-...")
    # and whose ancestors don't include a Schedule.
    for sec in root.iter(f"{NS}P1"):
        sec_id = sec.get("id", "")
        if not sec_id.startswith("section-") and not sec_id.startswith("regulation-") and not sec_id.startswith("article-"):
            continue
        # Skip if inside a Schedule
        if any(a.tag == f"{NS}Schedule" for a in sec.iterancestors()):
            continue
        m = re.match(r"^(?:section|regulation|article)-(.+)$", sec_id)
        sec_num = m.group(1) if m else ""
        # Pnumber and Title
        pnum_el = sec.find(f"{NS}Pnumber")
        if pnum_el is not None and not sec_num:
            sec_num = all_text(pnum_el)
        title = find_title(sec)
        # Locate ancestors for part/chapter context
        part = ""
        chapter = ""
        for anc in sec.iterancestors():
            tag = anc.tag.split("}")[-1]
            if tag == "Part" and not part:
                part = anc.get("NumberOfPart", "")
                if not part:
                    n = anc.find(f"{NS}Number")
                    if n is None: n = anc.find(f"{NS}Pnumber")
                    if n is not None: part = all_text(n)
            elif tag == "Chapter" and not chapter:
                chapter = anc.get("NumberOfChapter", "")
                if not chapter:
                    n = anc.find(f"{NS}Number")
                    if n is None: n = anc.find(f"{NS}Pnumber")
                    if n is not None: chapter = all_text(n)
        # Content: everything inside, minus the Pnumber/Title elements
        content_parts = []
        for child in sec:
            tag = child.tag.split("}")[-1]
            if tag in ("Pnumber", "Title", "Heading", "Number"):
                continue
            content_parts.append(all_text(child))
        content = " ".join(p for p in content_parts if p)
        rows.append({
            "section": sec_num,
            "id": sec_id,
            "title": title,
            "part": part,
            "chapter": chapter,
            "content": content,
        })
    # Stable sort by id (UK uses string-based section numbers like "1", "1A", "2", ...)
    def sort_key(r):
        m = re.match(r"^section-(\d+)([A-Z]*)$", r["id"])
        if m:
            return (int(m.group(1)), m.group(2))
        return (10**9, r["id"])
    rows.sort(key=sort_key)
    return rows


def parse_schedules(root):
    """UK statutes often have Schedules (akin to annexes)."""
    rows = []
    for sched in root.iter(f"{NS}Schedule"):
        num = sched.get("NumberOfSchedule", "")
        title = find_title(sched)
        text = all_text(sched)
        rows.append({"schedule": num, "title": title, "content": text[:200000]})
    return rows


def write(rows, fields, base):
    if not rows:
        return 0
    with open(f"{base}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open(f"{base}.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    return len(rows)


def main():
    if len(sys.argv) != 3:
        print("usage: extract_uk_legislation.py <input.xml> <slug>", file=sys.stderr)
        sys.exit(2)
    xml_path, slug = sys.argv[1], sys.argv[2]
    tree = etree.parse(xml_path)
    root = tree.getroot()

    sections = parse_sections(root)
    schedules = parse_schedules(root)

    n_s = write(sections, ["section", "id", "title", "part", "chapter", "content"], f"{slug}-sections")
    n_sch = write(schedules, ["schedule", "title", "content"], f"{slug}-schedules")

    print(f"Sections:  {n_s}")
    print(f"Schedules: {n_sch}")


if __name__ == "__main__":
    main()
