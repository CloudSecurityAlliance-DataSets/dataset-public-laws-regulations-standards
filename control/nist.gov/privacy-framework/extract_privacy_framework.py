#!/usr/bin/env python3
"""Parse NIST Privacy Framework Core into structured CSV/JSON.

The NIST Privacy Framework Core mirrors NIST CSF's hierarchy with
privacy-specific IDs:
  - 5 Functions: IDENTIFY-P, GOVERN-P, CONTROL-P, COMMUNICATE-P, PROTECT-P
  - Categories: e.g., ID.BE-P (Business Environment), CM.AW-P (Awareness)
  - Subcategories: e.g., CM.AW-P1, CT.DM-P10

Output:
  privacy-framework-subcategories.{csv,json}  — one row per subcategory
"""
import csv
import json
import re


FUNCTION_PREFIX = {
    "ID": "Identify-P",
    "GV": "Govern-P",
    "CT": "Control-P",
    "CM": "Communicate-P",
    "PR": "Protect-P",
}

CATEGORY_NAMES = {
    "ID.IM-P": "Inventory and Mapping",
    "ID.BE-P": "Business Environment",
    "ID.RA-P": "Risk Assessment",
    "ID.DE-P": "Data Processing Ecosystem Risk Management",
    "GV.PO-P": "Governance Policies, Processes, and Procedures",
    "GV.RM-P": "Risk Management Strategy",
    "GV.AT-P": "Awareness and Training",
    "GV.MT-P": "Monitoring and Review",
    "CT.PO-P": "Data Processing Policies, Processes, and Procedures",
    "CT.DM-P": "Data Processing Management",
    "CT.DP-P": "Disassociated Processing",
    "CM.PO-P": "Communication Policies, Processes, and Procedures",
    "CM.AW-P": "Data Processing Awareness",
    "PR.PO-P": "Data Protection Policies, Processes, and Procedures",
    "PR.AC-P": "Identity Management, Authentication, and Access Control",
    "PR.DS-P": "Data Security",
    "PR.MA-P": "Maintenance",
    "PR.PT-P": "Protective Technology",
}


def main():
    md = open("privacy-framework.md", encoding="utf-8").read()
    md = re.sub(r"<br\s*/?>", " ", md)
    md = re.sub(r"\{\d+\}-+", "", md)

    sub_re = re.compile(
        r"\b(?P<id>[A-Z]{2}\.[A-Z]{2}-P\d{1,2}):\s*(?P<text>[^|\n]+?)"
        r"(?=\s+[A-Z]{2}\.[A-Z]{2}-P\d|\s+Continued|\s*\||$)",
    )
    rows = {}
    for m in sub_re.finditer(md):
        sid = m.group("id")
        text = re.sub(r"\s+", " ", m.group("text")).strip()
        if sid not in rows or len(text) > len(rows[sid]["description"]):
            cat_id = sid.rsplit("-P", 1)[0] + "-P"
            func_prefix = sid.split(".")[0]
            rows[sid] = {
                "subcategory_id": sid,
                "function": FUNCTION_PREFIX.get(func_prefix, ""),
                "category_id": cat_id,
                "category_name": CATEGORY_NAMES.get(cat_id, ""),
                "description": text,
            }

    def sort_key(r):
        func_order = ["Identify-P", "Govern-P", "Control-P", "Communicate-P", "Protect-P"]
        m = re.match(r".+P(\d+)$", r["subcategory_id"])
        n = int(m.group(1)) if m else 999
        return (
            func_order.index(r["function"]) if r["function"] in func_order else 99,
            r["category_id"],
            n,
        )

    final = sorted(rows.values(), key=sort_key)
    fields = ["subcategory_id", "function", "category_id", "category_name", "description"]
    with open("privacy-framework-subcategories.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("privacy-framework-subcategories.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Subcategories: {len(final)}")
    funcs = {}
    for r in final:
        funcs.setdefault(r["function"], []).append(r["subcategory_id"])
    for f in ["Identify-P", "Govern-P", "Control-P", "Communicate-P", "Protect-P"]:
        if f in funcs:
            print(f"  {f}: {len(funcs[f])} subcategories")


if __name__ == "__main__":
    main()
