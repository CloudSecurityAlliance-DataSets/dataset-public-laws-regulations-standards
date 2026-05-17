#!/usr/bin/env python3
"""Parse NIST AI 600-1 (AI RMF Generative AI Profile) into per-action CSV/JSON.

AI 600-1 v1.0 (July 2024) extends the AI RMF Core with ~200 Suggested
Actions tailored to generative-AI risks. Each action is identified as
`<FN>-<N.M>-<NNN>` where FN is the AI RMF function code (GV/MP/MS/MG),
N.M is the AI RMF subcategory, and NNN is the action sequence number
within that subcategory.

Marker emits the Suggested Actions as a multi-column table; an earlier
processing step (pre-existing `ai-600-1-1.0-processed.csv`) flattened
the tables into a Section / Action ID / Action / GAI Risks / Tasks
schema. This parser cleans up that intermediate CSV into the standard
output naming convention and adds derived columns (function, subcategory
ID, parsed risk list, parsed actor-task list).

Output:
  ai-600-1-1.0-actions.{csv,json}  — one row per Suggested Action
"""
import csv
import json
import re


FUNCTION_FULL = {"GV": "Govern", "MP": "Map", "MS": "Measure", "MG": "Manage"}


def main():
    with open("ai-600-1-1.0-processed.csv", encoding="utf-8") as f:
        rows_in = list(csv.DictReader(f))

    rows = []
    for r in rows_in:
        section = (r.get("Section") or "").strip()
        # Section like "GOVERN 1.1: <description>" — split into ID + description
        m = re.match(r"([A-Z]+\s+\d+\.\d+):\s*(.+)", section)
        subcat_id = m.group(1) if m else ""
        subcat_text = m.group(2).strip() if m else section

        action_id = (r.get("Action ID") or "").strip()
        # GV-1.1-001 → function=GV, function_full=Govern
        fn = action_id.split("-", 1)[0] if "-" in action_id else ""
        function = FUNCTION_FULL.get(fn, "")

        risks_raw = (r.get("GAI Risks") or "").replace("\n", " ").strip()
        risks = [s.strip() for s in re.split(r";\s*", risks_raw) if s.strip()]

        tasks_raw = (r.get("AI Actor Tasks") or "").strip()
        # Format usually: "AI Actor Tasks: <comma- or semicolon-separated list>"
        tasks_clean = re.sub(r"^AI Actor Tasks:\s*", "", tasks_raw)
        tasks = [s.strip() for s in re.split(r"[;,]\s*", tasks_clean) if s.strip()]

        rows.append({
            "action_id": action_id,
            "function": function,
            "subcategory_id": subcat_id,
            "subcategory_text": subcat_text,
            "suggested_action": (r.get("Suggested Action") or "").strip(),
            "gai_risks": risks,
            "ai_actor_tasks": tasks,
        })

    # Sort by action_id (e.g., GV-1.1-001 -> function order, subcategory, sequence)
    func_order = ["GV", "MP", "MS", "MG"]
    def sort_key(r):
        m = re.match(r"^([A-Z]+)-(\d+)\.(\d+)-(\d+)$", r["action_id"])
        if not m:
            return (99, 99, 99, 99)
        fn, n, m2, seq = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
        return (func_order.index(fn) if fn in func_order else 99, n, m2, seq)
    rows.sort(key=sort_key)

    # CSV with pipe-joined lists
    csv_rows = [
        {**r, "gai_risks": "|".join(r["gai_risks"]), "ai_actor_tasks": "|".join(r["ai_actor_tasks"])}
        for r in rows
    ]
    with open("ai-600-1-1.0-actions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["action_id", "function", "subcategory_id", "subcategory_text",
                        "suggested_action", "gai_risks", "ai_actor_tasks"],
            quoting=csv.QUOTE_ALL,
        )
        w.writeheader()
        w.writerows(csv_rows)
    with open("ai-600-1-1.0-actions.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Suggested actions: {len(rows)}")
    funcs = {}
    for r in rows:
        funcs.setdefault(r["function"], []).append(r["action_id"])
    for f in ["Govern", "Map", "Measure", "Manage"]:
        if f in funcs:
            print(f"  {f}: {len(funcs[f])} actions")
    subcats = sorted({r["subcategory_id"] for r in rows if r["subcategory_id"]})
    print(f"AI RMF subcategories covered: {len(subcats)}")


if __name__ == "__main__":
    main()
