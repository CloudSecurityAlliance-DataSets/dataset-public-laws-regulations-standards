#!/usr/bin/env python3
"""Extract MITRE ATLAS into structured CSV/JSON.

Input: ATLAS.yaml from https://github.com/mitre-atlas/atlas-data/raw/main/dist/ATLAS.yaml

ATLAS structure:
  - 1 matrix (the ATLAS matrix)
  - tactics:    adversary objectives (Reconnaissance, Exfiltration, etc.)
  - techniques: how the adversary achieves a tactic
  - mitigations: defensive measures
  - case-studies: real-world incident summaries

Output:
  - atlas-tactics.{csv,json}
  - atlas-techniques.{csv,json}
  - atlas-mitigations.{csv,json}
  - atlas-case-studies.{csv,json}
  - atlas-all.json   (full bundle, version-aware)
"""
import csv
import json
import yaml


def csv_list(v):
    if v is None: return ""
    if isinstance(v, list): return "; ".join(str(x) for x in v)
    return str(v)


def to_str(v):
    if v is None: return ""
    return str(v)


def main():
    d = yaml.safe_load(open("ATLAS.yaml"))
    version = d.get("version", "")
    matrix = d["matrices"][0]

    # ---- tactics ----
    tactics = []
    for t in matrix.get("tactics", []):
        tactics.append({
            "id": t.get("id", ""),
            "name": t.get("name", ""),
            "description": to_str(t.get("description", "")),
            "attack_reference": csv_list(t.get("ATT&CK-reference", "")),
            "created_date": to_str(t.get("created_date", "")),
            "modified_date": to_str(t.get("modified_date", "")),
        })
    tactics.sort(key=lambda x: x["id"])

    # ---- techniques ----
    techniques = []
    for t in matrix.get("techniques", []):
        techniques.append({
            "id": t.get("id", ""),
            "name": t.get("name", ""),
            "description": to_str(t.get("description", "")),
            "tactics": csv_list(t.get("tactics", [])),
            "subtechnique_of": t.get("subtechnique-of", ""),
            "attack_reference": csv_list(t.get("ATT&CK-reference", "")),
            "maturity": to_str(t.get("maturity", "")),
            "created_date": to_str(t.get("created_date", "")),
            "modified_date": to_str(t.get("modified_date", "")),
        })
    techniques.sort(key=lambda x: x["id"])

    # ---- mitigations ----
    mitigations = []
    for m in matrix.get("mitigations", []):
        mitigations.append({
            "id": m.get("id", ""),
            "name": m.get("name", ""),
            "description": to_str(m.get("description", "")),
            "techniques": csv_list(m.get("techniques", [])),
            "ml_lifecycle": csv_list(m.get("ml-lifecycle", [])),
            "category": csv_list(m.get("category", [])),
            "created_date": to_str(m.get("created_date", "")),
            "modified_date": to_str(m.get("modified_date", "")),
        })
    mitigations.sort(key=lambda x: x["id"])

    # ---- case-studies ----
    case_studies = []
    for c in d.get("case-studies", []):
        case_studies.append({
            "id": c.get("id", ""),
            "name": c.get("name", ""),
            "summary": to_str(c.get("summary", "")),
            "incident_date": to_str(c.get("incident-date", "")),
            "incident_date_granularity": to_str(c.get("incident-date-granularity", "")),
            "case_study_type": to_str(c.get("case-study-type", "")),
            "target": csv_list(c.get("target", "")),
            "actor": csv_list(c.get("actor", "")),
            "n_procedure_steps": len(c.get("procedure", []) or []),
            "n_references": len(c.get("references", []) or []),
        })
    case_studies.sort(key=lambda x: x["id"])

    # Write per-type CSV/JSON
    sets = [
        ("atlas-tactics", tactics),
        ("atlas-techniques", techniques),
        ("atlas-mitigations", mitigations),
        ("atlas-case-studies", case_studies),
    ]
    for name, rows in sets:
        if not rows: continue
        fields = list(rows[0].keys())
        with open(f"{name}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
            w.writeheader()
            w.writerows(rows)
        with open(f"{name}.json", "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)

    # Bundle JSON
    bundle = {
        "version": version,
        "tactics": tactics,
        "techniques": techniques,
        "mitigations": mitigations,
        "case_studies": case_studies,
    }
    with open("atlas-all.json", "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"ATLAS version: {version}")
    print(f"  Tactics:      {len(tactics)}")
    print(f"  Techniques:   {len(techniques)}")
    print(f"  Mitigations:  {len(mitigations)}")
    print(f"  Case studies: {len(case_studies)}")
    # Maturity / subtechnique stats
    from collections import Counter
    by_maturity = Counter(t["maturity"] for t in techniques)
    subtech = sum(1 for t in techniques if t["subtechnique_of"])
    print(f"  Technique maturity: {dict(by_maturity)}")
    print(f"  Sub-techniques (have subtechnique_of): {subtech}")


if __name__ == "__main__":
    main()
