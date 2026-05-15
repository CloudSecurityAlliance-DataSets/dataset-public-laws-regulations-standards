#!/usr/bin/env python3
"""Parse NIST SP 800-161 r1 (Cybersecurity Supply Chain Risk Management
Practices for Systems and Organizations) C-SCRM control augmentations into CSV/JSON.

800-161 r1 layers C-SCRM-specific guidance on top of NIST SP 800-53 r5
controls. In Appendix A the document walks every 800-53 r5 control family
and provides "Supplemental C-SCRM Guidance:" plus level applicability
(Level(s): 1, 2, 3) for each base control, optionally followed by
"Control Enhancement(s):" with per-enhancement guidance.

Each control appears as a level-3 or level-4 markdown heading:

  #### **AC-1 POLICY AND PROCEDURES**

  Supplemental C-SCRM Guidance: ...

  Level(s): ...

  #### Control Enhancement(s):
  - *AC-1(1)*
    ...

Output:
  800-161-r1-controls.{csv,json}  — one row per C-SCRM-augmented base control
"""
import csv
import json
import re


CONTROL_RE = re.compile(
    r"^#{2,4}\s+\*\*([A-Z]{2,3})-(\d+)\s+([A-Z][A-Z\s,\(\)\-\/]+?)\*\*\s*$",
    re.MULTILINE,
)

FAMILY_NAMES = {
    "AC": "Access Control",
    "AT": "Awareness and Training",
    "AU": "Audit and Accountability",
    "CA": "Assessment, Authorization, and Monitoring",
    "CM": "Configuration Management",
    "CP": "Contingency Planning",
    "IA": "Identification and Authentication",
    "IR": "Incident Response",
    "MA": "Maintenance",
    "MP": "Media Protection",
    "PE": "Physical and Environmental Protection",
    "PL": "Planning",
    "PM": "Program Management",
    "PS": "Personnel Security",
    "PT": "Personally Identifiable Information Processing and Transparency",
    "RA": "Risk Assessment",
    "SA": "System and Services Acquisition",
    "SC": "System and Communications Protection",
    "SI": "System and Information Integrity",
    "SR": "Supply Chain Risk Management",
}


def main():
    md = open("800-161-r1.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)

    matches = list(CONTROL_RE.finditer(md))
    # Each base control may appear multiple times (TOC summary, body, appendix
    # cross-references). The body occurrence is the longest — dedupe by
    # (family, number) keeping longest content.
    by_id = {}
    for i, m in enumerate(matches):
        family = m.group(1)
        # Skip unknown families — these are likely false positives like
        # "ABSTRACT" or random acronyms that happen to match.
        if family not in FAMILY_NAMES:
            continue
        num = int(m.group(2))
        title = re.sub(r"\s+", " ", m.group(3)).strip().title()
        cid = f"{family}-{num}"
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        existing = by_id.get(cid)
        if not existing or len(body) > len(existing["content"]):
            # Pull Level(s) marker if present
            levels_m = re.search(r"Level\(s\):\s*([0-9, ]+)", body)
            levels = levels_m.group(1).strip() if levels_m else ""
            by_id[cid] = {
                "control_id": cid,
                "family": family,
                "family_name": FAMILY_NAMES[family],
                "title": title,
                "levels": levels,
                "content": body,
            }

    def sort_key(r):
        family_order = list(FAMILY_NAMES.keys())
        return (family_order.index(r["family"]) if r["family"] in family_order else 999,
                int(r["control_id"].split("-")[1]))

    final = sorted(by_id.values(), key=sort_key)
    fields = ["control_id", "family", "family_name", "title", "levels", "content"]
    with open("800-161-r1-controls.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("800-161-r1-controls.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Controls: {len(final)}")
    families_seen = sorted({r["family"] for r in final}, key=lambda f: list(FAMILY_NAMES.keys()).index(f) if f in FAMILY_NAMES else 999)
    for fam in families_seen:
        cnt = sum(1 for r in final if r["family"] == fam)
        print(f"  {fam} ({cnt}): {FAMILY_NAMES.get(fam, '')}")


if __name__ == "__main__":
    main()
