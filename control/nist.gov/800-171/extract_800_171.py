#!/usr/bin/env python3
"""Parse NIST SP 800-171 r3 security requirements into per-requirement CSV/JSON.

NIST SP 800-171 r3 (May 2024) consolidates the security requirements for
protecting Controlled Unclassified Information (CUI) in nonfederal
systems. Revision 3 introduces a new requirement-ID format using
two-digit zero-padding: `03.NN.MM` (with optional letter suffix for
withdrawn requirements). The 17 requirement families align with NIST SP
800-53 r5.

Marker emits each requirement as a level-3 or level-4 markdown heading:

  ## **03.01.01 Account Management**
  #### **03.13.11 Cryptographic Protection**

A subset of requirements are explicitly marked "Withdrawn" — kept in
the output with `status='withdrawn'` so downstream consumers can
identify them.

Output:
  800-171-requirements.{csv,json}  — one row per requirement
"""
import csv
import json
import re


REQ_RE = re.compile(
    r"^#{2,4}\s+(?:<span[^>]*></span>\s*)?\*\*(?P<id>0?3\.\d{1,2}\.\d{1,2}[a-z]?)\s+(?P<title>[^*]+?)\*\*\s*$",
    re.MULTILINE,
)

FAMILY_NAMES = {
    "03.01": "Access Control",
    "03.02": "Awareness and Training",
    "03.03": "Audit and Accountability",
    "03.04": "Configuration Management",
    "03.05": "Identification and Authentication",
    "03.06": "Incident Response",
    "03.07": "Maintenance",
    "03.08": "Media Protection",
    "03.09": "Personnel Security",
    "03.10": "Physical Protection",
    "03.11": "Risk Assessment",
    "03.12": "Security Assessment and Monitoring",
    "03.13": "System and Communications Protection",
    "03.14": "System and Information Integrity",
    "03.15": "Planning",
    "03.16": "System and Services Acquisition",
    "03.17": "Supply Chain Risk Management",
}


def main():
    md = open("800-171.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    matches = list(REQ_RE.finditer(md))
    by_id = {}
    for i, m in enumerate(matches):
        rid = m.group("id")
        # Normalize "3.X.Y" -> "03.0X.0Y" for consistency (some headings drop the leading zero)
        parts = rid.split(".")
        norm = f"{int(parts[0]):02d}.{int(parts[1]):02d}.{parts[2]}"
        title = re.sub(r"\s+", " ", m.group("title")).strip()
        status = "withdrawn" if title.lower() == "withdrawn" else "active"
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
        family = ".".join(norm.split(".")[:2])  # "03.01.01" -> "03.01"
        existing = by_id.get(norm)
        if not existing or len(body) > len(existing["content"]):
            by_id[norm] = {
                "requirement_id": norm,
                "family": family,
                "family_name": FAMILY_NAMES.get(family, ""),
                "title": title,
                "status": status,
                "content": body,
            }

    def sort_key(r):
        parts = r["requirement_id"].split(".")
        return (int(parts[0]), int(parts[1]), parts[2])

    final = sorted(by_id.values(), key=sort_key)
    fields = ["requirement_id", "family", "family_name", "title", "status", "content"]
    with open("800-171-requirements.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("800-171-requirements.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Requirements: {len(final)} (incl withdrawn)")
    active = [r for r in final if r["status"] == "active"]
    withdrawn = [r for r in final if r["status"] == "withdrawn"]
    print(f"  active:    {len(active)}")
    print(f"  withdrawn: {len(withdrawn)}")
    families_seen = sorted({r["family"] for r in final},
                           key=lambda f: int(f.split(".")[1]))
    for fam in families_seen:
        cnt = sum(1 for r in active if r["family"] == fam)
        print(f"  {fam} ({cnt} active): {FAMILY_NAMES.get(fam, '')}")


if __name__ == "__main__":
    main()
