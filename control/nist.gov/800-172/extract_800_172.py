#!/usr/bin/env python3
"""Parse NIST SP 800-172 enhanced security requirements into per-requirement CSV/JSON.

NIST SP 800-172 (Enhanced Security Requirements for Protecting Controlled
Unclassified Information) defines 35 enhanced security requirements
organized across 14 families (3.1 through 3.14, with no 3.7/3.8/3.10/3.12/3.13).
Each requirement is identified as 3.X.Ne in the marker markdown:

  **[3.X.Ne](anchor) Requirement statement.**

followed by a discussion paragraph and Protection-Strategy / Adversary-Effects
sub-sections.

Output:
  800-172-requirements.{csv,json}  — one row per enhanced requirement
"""
import csv
import json
import re


# Match a requirement header: optional leading markup, then **[3.X.Ne](anchor) Title.**
REQ_RE = re.compile(
    r"\*\*\[(?P<id>3\.\d+\.\d+e)\](?:\(#[^)]*\))?\s*(?P<title>[^*]+?)\*\*",
)

FAMILY_NAMES = {
    "3.1": "Access Control",
    "3.2": "Awareness and Training",
    "3.3": "Audit and Accountability",
    "3.4": "Configuration Management",
    "3.5": "Identification and Authentication",
    "3.6": "Incident Response",
    "3.7": "Maintenance",
    "3.8": "Media Protection",
    "3.9": "Personnel Security",
    "3.10": "Physical Protection",
    "3.11": "Risk Assessment",
    "3.12": "Security Assessment",
    "3.13": "System and Communications Protection",
    "3.14": "System and Information Integrity",
}


def main():
    md = open("800-172.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)

    matches = list(REQ_RE.finditer(md))
    # Each requirement appears twice — once as section header (chapter 3),
    # once in Appendix C summary table. Pair them by ID and keep the LONGEST
    # body (which is the section header occurrence).
    by_id = {}
    for i, m in enumerate(matches):
        rid = m.group("id")
        title = re.sub(r"\s+", " ", m.group("title")).strip().rstrip(".")
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        family = rid.rsplit(".", 1)[0]  # "3.1.1e" -> "3.1"
        existing = by_id.get(rid)
        if not existing or len(body) > len(existing["content"]):
            by_id[rid] = {
                "requirement_id": rid,
                "family": family,
                "family_name": FAMILY_NAMES.get(family, ""),
                "title": title,
                "content": body,
            }

    def sort_key(r):
        parts = r["requirement_id"].rstrip("e").split(".")
        return tuple(int(p) for p in parts)

    final = sorted(by_id.values(), key=sort_key)
    fields = ["requirement_id", "family", "family_name", "title", "content"]
    with open("800-172-requirements.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("800-172-requirements.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Enhanced requirements: {len(final)}")
    families_seen = sorted({r["family"] for r in final}, key=lambda f: tuple(int(x) for x in f.split(".")))
    for fam in families_seen:
        cnt = sum(1 for r in final if r["family"] == fam)
        print(f"  {fam} ({cnt} reqs): {FAMILY_NAMES.get(fam, '')}")


if __name__ == "__main__":
    main()
