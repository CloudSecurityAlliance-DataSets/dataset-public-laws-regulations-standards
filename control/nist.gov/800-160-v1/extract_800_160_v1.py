#!/usr/bin/env python3
"""Parse NIST SP 800-160 v1 (Systems Security Engineering) Appendix H into CSV/JSON.

Appendix H provides security-engineering activities and tasks aligned
with the ISO/IEC/IEEE 15288 system life cycle processes. Each process
contributes a set of Activities (2-letter prefix + number) with
sub-tasks:

  #### **BA-1** PREPARE FOR BUSINESS OR MISSION ANALYSIS
  - **BA-1.1** Identify the security aspects ...
  - **BA-1.2** Identify and plan ...

15288 process prefixes used in 800-160 v1:
  AA Acquisition       AR Architecture Definition       MO Maintenance
  AG Agreement         BA Business/Mission Analysis     OP Operation
  AR (also Risk Mgmt)  CO Configuration Management     PA Project Assess
  AQ Acquisition       DE Design Definition            PL Project Planning
  ... and many more for the full 15288 process set

Output:
  800-160-v1-tasks.{csv,json}     — one row per task (AA-N.M)
  800-160-v1-activities.{csv,json} — one row per activity (AA-N)
"""
import csv
import json
import re


ACTIVITY_RE = re.compile(
    r"^#{2,4}\s+\*\*(?P<id>[A-Z]{2}-\d+)\*\*\s+(?P<title>[A-Z][^\n*]+?)$",
    re.MULTILINE,
)
TASK_RE = re.compile(
    r"\*\*(?P<id>[A-Z]{2}-\d+\.\d+)\*\*\s+(?P<text>[^*\n]+?)(?=\n|$)",
)


def main():
    md = open("800-160-v1.md", encoding="utf-8").read()
    md = re.sub(r"\{\d+\}-+", "", md)

    # Activities — keyed by ID, keep longest title
    activities = {}
    for m in ACTIVITY_RE.finditer(md):
        aid = m.group("id")
        title = re.sub(r"\s+", " ", m.group("title")).strip()
        existing = activities.get(aid)
        if not existing or len(title) > len(existing["title"]):
            activities[aid] = {
                "activity_id": aid,
                "process_prefix": aid.split("-")[0],
                "title": title,
            }

    # Tasks — keyed by ID, keep longest text
    tasks = {}
    for m in TASK_RE.finditer(md):
        tid = m.group("id")
        text = re.sub(r"\s+", " ", m.group("text")).strip()
        existing = tasks.get(tid)
        if not existing or len(text) > len(existing["description"]):
            parent_activity = tid.rsplit(".", 1)[0]  # "BA-1.2" -> "BA-1"
            tasks[tid] = {
                "task_id": tid,
                "activity_id": parent_activity,
                "process_prefix": tid.split("-")[0],
                "description": text,
            }

    # Sort activities by process prefix then number
    def act_key(r):
        pref, num = r["activity_id"].split("-")
        return (pref, int(num))
    act_final = sorted(activities.values(), key=act_key)

    # Sort tasks similarly
    def task_key(r):
        pref = r["task_id"].split("-")[0]
        nums = r["task_id"].split("-")[1].split(".")
        return (pref, int(nums[0]), int(nums[1]))
    task_final = sorted(tasks.values(), key=task_key)

    # Activities output
    with open("800-160-v1-activities.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=["activity_id", "process_prefix", "title"], quoting=csv.QUOTE_ALL
        )
        w.writeheader()
        w.writerows(act_final)
    with open("800-160-v1-activities.json", "w", encoding="utf-8") as f:
        json.dump(act_final, f, indent=2, ensure_ascii=False)

    # Tasks output (with activity title joined in)
    activity_title = {a["activity_id"]: a["title"] for a in act_final}
    task_rows_out = [
        {**t, "activity_title": activity_title.get(t["activity_id"], "")}
        for t in task_final
    ]
    with open("800-160-v1-tasks.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["task_id", "activity_id", "activity_title", "process_prefix", "description"],
            quoting=csv.QUOTE_ALL,
        )
        w.writeheader()
        w.writerows(task_rows_out)
    with open("800-160-v1-tasks.json", "w", encoding="utf-8") as f:
        json.dump(task_rows_out, f, indent=2, ensure_ascii=False)

    print(f"Activities: {len(act_final)}")
    print(f"Tasks: {len(task_final)}")
    prefixes = sorted({a["process_prefix"] for a in act_final})
    for p in prefixes:
        ac = sum(1 for a in act_final if a["process_prefix"] == p)
        tc = sum(1 for t in task_final if t["process_prefix"] == p)
        print(f"  {p}: {ac} activities, {tc} tasks")


if __name__ == "__main__":
    main()
