#!/usr/bin/env python3
"""Merge the three MITRE CWE view CSVs into a unified weakness catalog.

CWE publishes per-view CSV exports — each view (1000 Research, 699 Software
Development, 1194 Hardware Design) ships its own CSV that includes every
weakness reachable from the view root, plus the relationship data scoped
to that view.

A given CWE-ID can appear in multiple views (e.g., CWE-79 XSS appears in
both 1000 and 699). The non-relationship columns (Name, Description,
Common Consequences, etc.) are identical across views — only the
relationship columns differ. This script merges by CWE-ID and tracks
which views each entry appears in.

Input: CWE-Research-Concepts-1000.csv
       CWE-Software-Development-699.csv
       CWE-Hardware-Design-1194.csv

Output: cwe-4.19.1-all.csv
        cwe-4.19.1-all.json

Each output row has:
  - cwe_id              numeric (e.g., 79)
  - cwe_identifier      "CWE-79"
  - name
  - weakness_abstraction (Pillar/Class/Base/Variant/Compound/View/Category)
  - status              (Draft/Incomplete/Stable/Deprecated)
  - description
  - extended_description
  - views               list of view IDs ("1000", "699", "1194")
  - related_weaknesses_by_view  dict view_id -> raw relationship string
  - applicable_platforms
  - modes_of_introduction
  - common_consequences
  - detection_methods
  - potential_mitigations
  - observed_examples
  - taxonomy_mappings
  - related_attack_patterns
"""
import csv
import json
import re
from collections import defaultdict

VIEW_FILES = [
    ("1000", "CWE-Research-Concepts-1000.csv"),
    ("699", "CWE-Software-Development-699.csv"),
    ("1194", "CWE-Hardware-Design-1194.csv"),
]


def parse_capec(s):
    """'::13::146::176::' -> ['13','146','176']"""
    if not s:
        return []
    return [x for x in s.split("::") if x.strip()]


def main():
    by_id = {}
    for view_id, fn in VIEW_FILES:
        with open(fn, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cwe_id_raw = row.get("CWE-ID", "").strip()
                if not cwe_id_raw or not cwe_id_raw.isdigit():
                    continue
                cwe_id = int(cwe_id_raw)
                entry = by_id.get(cwe_id)
                if not entry:
                    entry = {
                        "cwe_id": cwe_id,
                        "cwe_identifier": f"CWE-{cwe_id}",
                        "name": row.get("Name", "").strip(),
                        "weakness_abstraction": row.get("Weakness Abstraction", "").strip(),
                        "status": row.get("Status", "").strip(),
                        "description": row.get("Description", "").strip(),
                        "extended_description": row.get("Extended Description", "").strip(),
                        "views": [],
                        "related_weaknesses_by_view": {},
                        "applicable_platforms": row.get("Applicable Platforms", "").strip(),
                        "modes_of_introduction": row.get("Modes Of Introduction", "").strip(),
                        "common_consequences": row.get("Common Consequences", "").strip(),
                        "detection_methods": row.get("Detection Methods", "").strip(),
                        "potential_mitigations": row.get("Potential Mitigations", "").strip(),
                        "observed_examples": row.get("Observed Examples", "").strip(),
                        "taxonomy_mappings": row.get("Taxonomy Mappings", "").strip(),
                        "related_attack_patterns": parse_capec(row.get("Related Attack Patterns", "")),
                        "likelihood_of_exploit": row.get("Likelihood of Exploit", "").strip(),
                    }
                    by_id[cwe_id] = entry
                # Record view membership and per-view relationships
                if view_id not in entry["views"]:
                    entry["views"].append(view_id)
                rels = row.get("Related Weaknesses", "").strip()
                if rels:
                    entry["related_weaknesses_by_view"][view_id] = rels

    # Sort by CWE ID
    sorted_entries = sorted(by_id.values(), key=lambda x: x["cwe_id"])

    # Write JSON (rich)
    with open("cwe-4.19.1-all.json", "w", encoding="utf-8") as f:
        json.dump(sorted_entries, f, indent=2, ensure_ascii=False)

    # Write CSV (flattened — views list joined, related_weaknesses_by_view JSON-encoded)
    fields = [
        "cwe_id", "cwe_identifier", "name", "weakness_abstraction", "status",
        "description", "extended_description", "views",
        "related_weaknesses_by_view",
        "applicable_platforms", "modes_of_introduction", "common_consequences",
        "detection_methods", "potential_mitigations", "observed_examples",
        "taxonomy_mappings", "related_attack_patterns", "likelihood_of_exploit",
    ]
    with open("cwe-4.19.1-all.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for e in sorted_entries:
            r = dict(e)
            r["views"] = ",".join(e["views"])
            r["related_weaknesses_by_view"] = json.dumps(e["related_weaknesses_by_view"], ensure_ascii=False)
            r["related_attack_patterns"] = ",".join(e["related_attack_patterns"])
            w.writerow(r)

    # Summary
    from collections import Counter
    by_view = Counter()
    multi_view = 0
    abstractions = Counter()
    for e in sorted_entries:
        abstractions[e["weakness_abstraction"]] += 1
        if len(e["views"]) > 1:
            multi_view += 1
        for v in e["views"]:
            by_view[v] += 1
    print(f"Distinct CWE entries: {len(sorted_entries)}")
    print(f"  Multi-view (in 2+ views): {multi_view}")
    print(f"  Per view:")
    for v, n in by_view.most_common():
        print(f"    View {v}: {n}")
    print(f"  By abstraction:")
    for a, n in abstractions.most_common():
        print(f"    {a or '(none)'}: {n}")


if __name__ == "__main__":
    main()
