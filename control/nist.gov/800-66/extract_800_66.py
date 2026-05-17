#!/usr/bin/env python3
"""Parse NIST SP 800-66 r2 (HIPAA Security Rule implementation guidance) into CSV/JSON.

800-66 r2 walks each HIPAA Security Rule citation (45 CFR §§ 164.30x)
and provides implementation guidance. The markdown structure is:

  ## **5.1.1. Security Management Process (§ 164.308(a)(1))**
  ## **5.1.2. Assigned Security Responsibility (§ 164.308(a)(2))**
  ## **5.2.1. Facility Access Controls (§ 164.310(a))**
  ## **5.3.1. Access Control (§ 164.312(a))**

Where 5.1.x = Administrative Safeguards (164.308), 5.2.x = Physical
Safeguards (164.310), 5.3.x = Technical Safeguards (164.312), and 5.4.x
= Organizational Requirements (164.314).

Output:
  800-66-r2-safeguards.{csv,json}  — one row per Security Rule standard
"""
import csv
import json
import re


SAFEGUARD_SECTIONS = {
    "5.1": "Administrative Safeguards (45 CFR § 164.308)",
    "5.2": "Physical Safeguards (45 CFR § 164.310)",
    "5.3": "Technical Safeguards (45 CFR § 164.312)",
    "5.4": "Organizational Requirements (45 CFR § 164.314)",
}


HEAD_RE = re.compile(
    r"^#+\s+(?:<span[^>]*></span>\s*)?\*\*(?P<sec>5\.\d+\.\d+)\.\s+"
    r"(?P<title>[^*(]+?)\s*\(§\s*(?P<hipaa>164\.\d+(?:\([^)]+\))*)\)"
    r"(?:\[\d+\][^)]*\))?\*\*",
    re.MULTILINE,
)


def main():
    md = open("800-66.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)

    matches = list(HEAD_RE.finditer(md))
    rows = []
    for i, m in enumerate(matches):
        sec = m.group("sec")
        title = re.sub(r"\s+", " ", m.group("title")).strip()
        hipaa = m.group("hipaa")
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        # Strip footnote refs like [53](#page-...)
        body = re.sub(r"\[\d+\]\(#page-[^)]+\)", "", body).strip()
        category = ".".join(sec.split(".")[:2])  # "5.1.1" -> "5.1"
        rows.append({
            "guidance_id": sec,
            "title": title,
            "hipaa_citation": f"§ {hipaa}",
            "safeguard_category": SAFEGUARD_SECTIONS.get(category, ""),
            "content": body,
        })

    def sort_key(r):
        parts = r["guidance_id"].split(".")
        return tuple(int(p) for p in parts)

    rows.sort(key=sort_key)
    fields = ["guidance_id", "title", "hipaa_citation", "safeguard_category", "content"]
    with open("800-66-r2-safeguards.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    with open("800-66-r2-safeguards.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Safeguards: {len(rows)}")
    for cat_id, cat_name in SAFEGUARD_SECTIONS.items():
        cnt = sum(1 for r in rows if r["guidance_id"].startswith(cat_id + "."))
        print(f"  {cat_id} ({cnt}): {cat_name}")


if __name__ == "__main__":
    main()
