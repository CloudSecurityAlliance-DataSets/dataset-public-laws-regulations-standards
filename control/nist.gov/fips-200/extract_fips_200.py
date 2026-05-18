#!/usr/bin/env python3
"""Parse FIPS 200 (Minimum Security Requirements for Federal Information
and Information Systems) into per-section CSV/JSON.

FIPS 200 (March 2006) defines the minimum security requirements for
federal information systems and pairs with FIPS 199's categorization
standard. The publication has:

- Foreword (12 numbered "FIPS template" sections at level-2)
- 4 body sections (level-1):
  1. PURPOSE
  2. INFORMATION SYSTEM IMPACT LEVELS
  3. MINIMUM SECURITY REQUIREMENTS — enumerates 17 control families
     (AC, AT, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PS, RA, SA, SC, SI)
  4. SECURITY CONTROL SELECTION

The 17 control families in §3 are the substantive content; we also
extract those as a separate "control families" output.

Output:
  fips-200-sections.{csv,json}        — per body section
  fips-200-control-families.{csv,json} — the 17 families from §3
"""
import csv
import json
import re


SEC_RE = re.compile(
    r"^#+\s+(?:<span[^>]*></span>\s*)?\*\*(?P<id>\d+(?:\.\d+){0,3})\s+(?P<title>[A-Z][^*]+?)\*\*\s*$",
    re.MULTILINE,
)
FAMILY_RE = re.compile(
    r"\*\*(?P<family>[A-Z][^*]+?)\s+\((?P<code>[A-Z]{2})\):\*\*\s*(?P<text>[^*]+?)"
    r"(?=\s*\*\*[A-Z][^*]+?\([A-Z]{2}\):\*\*|\s*##|\s*\Z)",
    re.DOTALL,
)


def main():
    md = open("fips-200.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)

    # Body sections
    matches = list(SEC_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        sid = m.group("id")
        title = re.sub(r"\s+", " ", m.group("title")).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        body = re.sub(r"\[\d+\]\(#[^)]+\)", "", body)
        body = re.sub(r"!\[\]\([^)]+\)", "", body)
        body = re.sub(r"\s+", " ", body).strip()
        rows.append({"section_id": sid, "title": title, "content": body})
    by_id = {}
    for r in rows:
        existing = by_id.get(r["section_id"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["section_id"]] = r
    sections = sorted(by_id.values(), key=lambda r: tuple(int(p) for p in r["section_id"].split(".")))

    with open("fips-200-sections.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["section_id", "title", "content"], quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(sections)
    with open("fips-200-sections.json", "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

    # Control families — parse Section 3 body for the 17 families
    sec3 = next((r["content"] for r in sections if r["section_id"] == "3"), "")
    families = []
    for m in FAMILY_RE.finditer(sec3):
        text = re.sub(r"\s+", " ", m.group("text")).strip()
        # Trim at the next sentence beginning a new family description
        text = re.split(r"\s+\*\s+[A-Z][a-z]+\s+", text)[0]
        families.append({
            "family_code": m.group("code"),
            "family_name": m.group("family"),
            "minimum_requirement": text,
        })
    with open("fips-200-control-families.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["family_code", "family_name", "minimum_requirement"], quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(families)
    with open("fips-200-control-families.json", "w", encoding="utf-8") as f:
        json.dump(families, f, indent=2, ensure_ascii=False)

    print(f"Sections: {len(sections)}")
    for r in sections:
        print(f"  § {r['section_id']}: {r['title'][:70]}")
    print(f"\nControl families: {len(families)}")
    for fam in families:
        print(f"  {fam['family_code']}: {fam['family_name']}")


if __name__ == "__main__":
    main()
