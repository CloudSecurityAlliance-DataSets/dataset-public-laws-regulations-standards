#!/usr/bin/env python3
"""Parse NIST SP 800-218 (Secure Software Development Framework — SSDF) into CSV/JSON.

SSDF v1.1 organizes secure-software-development guidance into:
  - 4 Practice Groups: Prepare the Organization (PO), Protect the Software (PS),
    Produce Well-Secured Software (PW), Respond to Vulnerabilities (RV)
  - 19 Practices: PO.1, PO.2, ..., RV.3
  - 47 Tasks: PO.1.1, PO.1.2, ..., RV.3.4

The marker output renders the SSDF as a multi-column table with one row
per task. Each row has the parent practice as a header cell, the task ID
+ description, examples, and external references (BSAFSS, BSIMM, etc).

Output:
  800-218-tasks.{csv,json}  — one row per SSDF task
"""
import csv
import json
import re


PRACTICE_GROUP_NAMES = {
    "PO": "Prepare the Organization",
    "PS": "Protect the Software",
    "PW": "Produce Well-Secured Software",
    "RV": "Respond to Vulnerabilities",
}


def main():
    md = open("800-218.md", encoding="utf-8").read()
    md = re.sub(r"<br\s*/?>", " ", md)
    md = re.sub(r"\{\d+\}-+", "", md)

    # Tasks have IDs like PO.1.1, PS.2.1, PW.4.4, RV.3.3 followed by a colon
    # and description. They appear in tables with surrounding pipe characters.
    task_re = re.compile(
        r"(?P<id>(?:PO|PS|PW|RV)\.\d+\.\d+):\s*(?P<text>[^|]+?)(?=\s*\||\s+(?:PO|PS|PW|RV)\.\d+\.\d+:|$)",
    )
    # Practices have IDs PO.N, PS.N etc. followed by a description, often
    # inline like "Define Security Requirements for Software Development (PO.1):"
    practice_re = re.compile(
        r"\((?P<id>(?:PO|PS|PW|RV)\.\d+)\):\s*(?P<text>[^|]+?)(?=\s*\||$)",
    )
    practices = {}
    for m in practice_re.finditer(md):
        pid = m.group("id")
        text = re.sub(r"\s+", " ", m.group("text")).strip()
        if pid not in practices or len(text) > len(practices[pid]):
            practices[pid] = text

    rows = {}
    for m in task_re.finditer(md):
        tid = m.group("id")
        text = re.sub(r"\s+", " ", m.group("text")).strip()
        if tid not in rows or len(text) > len(rows[tid]["description"]):
            group_prefix = tid.split(".")[0]  # "PO"
            practice_id = ".".join(tid.split(".")[:2])  # "PO.1"
            rows[tid] = {
                "task_id": tid,
                "group_id": group_prefix,
                "group_name": PRACTICE_GROUP_NAMES.get(group_prefix, ""),
                "practice_id": practice_id,
                "practice_text": practices.get(practice_id, ""),
                "description": text,
            }

    def sort_key(r):
        group_order = ["PO", "PS", "PW", "RV"]
        parts = r["task_id"].split(".")
        return (group_order.index(r["group_id"]) if r["group_id"] in group_order else 99,
                int(parts[1]), int(parts[2]))

    final = sorted(rows.values(), key=sort_key)
    fields = ["task_id", "group_id", "group_name", "practice_id", "practice_text", "description"]
    with open("800-218-tasks.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("800-218-tasks.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Tasks: {len(final)}")
    print(f"Practices captured: {len(practices)}")
    for g in ["PO", "PS", "PW", "RV"]:
        cnt = sum(1 for r in final if r["group_id"] == g)
        print(f"  {g} ({cnt} tasks): {PRACTICE_GROUP_NAMES[g]}")


if __name__ == "__main__":
    main()
