#!/usr/bin/env python3
"""Parse NIST SP 800-37 r2 (Risk Management Framework) into per-task CSV/JSON.

RMF r2 organizes risk-management activities into 7 steps × per-step tasks:
  - Prepare (P): P-1 .. P-18 (organization-level) plus system-level Prepare tasks
  - Categorize (C): C-1, C-2, C-3
  - Select (S): S-1 .. S-6
  - Implement (I): I-1, I-2
  - Assess (A): A-1 .. A-6
  - Authorize (R): R-1 .. R-5 (sometimes labeled differently)
  - Monitor (M): M-1 .. M-7

Marker emits each task body header as `**TASK <ID>** <Task statement>`.
Tasks also appear in summary tables earlier in the document; we dedupe
by ID and keep the longest body.

Output:
  800-37-r2-tasks.{csv,json}  — one row per RMF Task
"""
import csv
import json
import re


PHASE_NAMES = {
    "P": "Prepare",
    "C": "Categorize",
    "S": "Select",
    "I": "Implement",
    "A": "Assess",
    "R": "Authorize",
    "M": "Monitor",
}


TASK_RE = re.compile(
    r"\*\*[Tt][Aa][Ss][Kk]\s+(?P<phase>[A-Z])-(?P<num>\d+)\*\*\s+(?P<text>[^*\n]+?)(?=\n|\*\*[Tt][Aa][Ss][Kk])",
)


def main():
    md = open("800-37-r2.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)
    md = re.sub(r"<br\s*/?>", " ", md)

    matches = list(TASK_RE.finditer(md))
    by_id = {}
    for i, m in enumerate(matches):
        phase = m.group("phase")
        if phase not in PHASE_NAMES:
            continue
        num = int(m.group("num"))
        tid = f"{phase}-{num}"
        statement = re.sub(r"\s+", " ", m.group("text")).strip()
        # Capture additional context until the next TASK or major heading
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = re.sub(r"\s+", " ", md[body_start:body_end][:5000]).strip()

        existing = by_id.get(tid)
        if not existing or len(body) > len(existing["content"]):
            by_id[tid] = {
                "task_id": tid,
                "phase_id": phase,
                "phase_name": PHASE_NAMES[phase],
                "task_statement": statement,
                "content": body,
            }

    def sort_key(r):
        phase_order = list(PHASE_NAMES.keys())
        return (phase_order.index(r["phase_id"]) if r["phase_id"] in phase_order else 99,
                int(r["task_id"].split("-")[1]))

    final = sorted(by_id.values(), key=sort_key)
    fields = ["task_id", "phase_id", "phase_name", "task_statement", "content"]
    with open("800-37-r2-tasks.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final)
    with open("800-37-r2-tasks.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Tasks: {len(final)}")
    for p in PHASE_NAMES:
        cnt = sum(1 for r in final if r["phase_id"] == p)
        if cnt:
            print(f"  {p} ({PHASE_NAMES[p]}): {cnt} tasks")


if __name__ == "__main__":
    main()
