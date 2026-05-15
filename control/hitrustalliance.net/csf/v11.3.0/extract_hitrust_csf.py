#!/usr/bin/env python3
"""Parse HITRUST CSF v11.3.0 into per-control CSV/JSON.

HITRUST CSF organizes controls into:
  - 14 Control Categories (0.0 through 13.0)
  - ~49 Control Objectives (e.g., 01.01, 01.02, ...)
  - ~156 Control References (e.g., 01.a, 01.b, ...)

Each Control Reference contains Implementation Requirements at multiple
Levels (1, 2, 3) plus regulatory-specific levels (HICP, FedRAMP,
EHNAC, NYDFS, etc.) and an Authoritative Source Mapping.

In the marker-extracted markdown, these appear as:
  ## **Control Category: 01.0 - Access Control**
  ## **Objective Name: 01.01 Business Requirement for Access Control**
  #### **Control Reference: 01.a Access Control Policy**
  ...body, level requirements, mappings...
  #### **Control Reference: 01.b ...**

Each Control Reference's body extends until the next Control Reference
or Objective Name marker.

Output:
  csf-v11.3.0-controls.{csv,json}  — one row per Control Reference
"""
import csv
import json
import re


CATEGORY_RE = re.compile(
    r"\*\*Control Category:\s+(\d+\.\d+)\s*-\s*([^*]+?)\*\*",
)
OBJECTIVE_RE = re.compile(
    r"\*\*Objective Name:\s+(\d+\.\d+)\s+([^*]+?)\*\*",
)
CONTROL_RE = re.compile(
    r"\*\*Control Reference:\s+(\d+\.[a-z])\s+([^*]+?)\*\*",
)


def main():
    md = open("csf-v11.3.0.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    # Normalize marker's table-cell <br> separators to spaces so headings like
    # "Control<br>Reference:<br>02.b<br>Screening" match the same regex as
    # bolded forms.
    md = re.sub(r"<br\s*/?>", " ", md)

    # Walk all category / objective / control markers in document order so
    # each control inherits its current Category and Objective context.
    EVENT_RE = re.compile(
        r"\*\*Control Category:\s+(?P<cat_id>\d+\.\d+)\s*-\s*(?P<cat_name>[^*]+?)\*\*"
        r"|\*\*Objective Name:\s+(?P<obj_id>\d+\.\d+)\s+(?P<obj_name>[^*]+?)\*\*"
        r"|Control Reference:\s+(?P<ctrl_id>\d+\.[a-z])\s+(?P<ctrl_name>[^*|\n]{0,120}?)(?=\s{2,}|\s*\||\s*\*\*|$)",
    )

    events = list(EVENT_RE.finditer(md))
    cur_cat = ("", "")
    cur_obj = ("", "")
    rows_raw = []
    for i, m in enumerate(events):
        if m.group("cat_id"):
            cur_cat = (m.group("cat_id"), m.group("cat_name").strip())
        elif m.group("obj_id"):
            cur_obj = (m.group("obj_id"), m.group("obj_name").strip())
        elif m.group("ctrl_id"):
            cid = m.group("ctrl_id")
            cname = m.group("ctrl_name").strip()
            body_start = m.end()
            # Body ends at next Control Reference / Objective / Category
            body_end = events[i + 1].start() if i + 1 < len(events) else len(md)
            body = re.sub(r"\s+", " ", md[body_start:body_end]).strip()
            # Strip leading markdown/table artifacts left over from heading close
            body = re.sub(r"^[\*\|\s\-]+", "", body).strip()
            rows_raw.append({
                "control_id": cid,
                "title": cname,
                "category_id": cur_cat[0],
                "category_name": cur_cat[1],
                "objective_id": cur_obj[0],
                "objective_name": cur_obj[1],
                "content": body,
            })

    # Dedupe by control_id, keep longest content (TOC entries have very short
    # body before the next control reference is mentioned)
    by_id = {}
    for r in rows_raw:
        existing = by_id.get(r["control_id"])
        if not existing or len(r["content"]) > len(existing["content"]):
            by_id[r["control_id"]] = r

    def sort_key(r):
        family, letter = r["control_id"].split(".")
        return (int(family), letter)

    final = sorted(by_id.values(), key=sort_key)
    fields = ["control_id", "title", "category_id", "category_name",
              "objective_id", "objective_name", "content"]
    with open("csf-v11.3.0-controls.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("csf-v11.3.0-controls.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Controls: {len(final)}")
    cats = sorted({(r["category_id"], r["category_name"]) for r in final},
                  key=lambda kv: (float(kv[0]) if kv[0] else 999))
    for cat_id, cat_name in cats:
        cnt = sum(1 for r in final if r["category_id"] == cat_id)
        print(f"  Cat {cat_id} ({cnt} controls): {cat_name}")


if __name__ == "__main__":
    main()
