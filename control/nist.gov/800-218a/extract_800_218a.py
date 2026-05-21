#!/usr/bin/env python3
"""Parse NIST SP 800-218A (SSDF Community Profile for AI Model Development) into CSV/JSON.

800-218A augments the SSDF v1.1 (NIST SP 800-218) for generative AI and dual-use
foundation models. It is published as a single large table (Table 1) where each
row is an SSDF task with AI-specific additions:

  - Practice: name + ID + brief explanation
  - Task: ID + description (PO.1.1, PS.2.1, PW.4.4, RV.3.3 style)
  - Priority: High / Medium / Low (for AI relevance)
  - Recommendations [R], Considerations [C], Notes [N] specific to AI
  - Informative References: AI RMF / OWASP-LLM / Adversarial-ML pointers

The marker-rendered markdown breaks each logical row across multiple pipe-table
rows (PDF column layout). We aggregate cells by detecting task-ID anchors in
column 1 OR column 2, then collecting nearby content rows.

Known limitation: marker's markdown-pipe-table output for this document has
cell-level layout artifacts that occasionally bleed content between adjacent
tasks (priority value or references attributed to neighbor row). Affected
fields are `ai_priority`, `ai_additions`, `informative_references`. Task
identity (`task_id`, `group_id`, `practice_id`) and `task_text` are reliable.
For a cleaner extraction, re-run marker with `--formats markdown,json` and
walk the Table block tree directly (as the PCI DSS v4.0.1 parser does).

Output (alongside 800-218-tasks.{csv,json} from the parent SSDF):
  800-218a-tasks.{csv,json}  — one row per SSDF task with AI Profile fields
"""
import csv
import json
import re
from pathlib import Path

PRACTICE_GROUP_NAMES = {
    "PO": "Prepare the Organization",
    "PS": "Protect the Software",
    "PW": "Produce Well-Secured Software",
    "RV": "Respond to Vulnerabilities",
}

TASK_ID_RE = re.compile(r"\b((?:PO|PS|PW|RV)\.\d+\.\d+)\b")
PRACTICE_ID_RE = re.compile(r"\(((?:PO|PS|PW|RV)\.\d+)\)")
RCN_ITEM_RE = re.compile(r"\b([RCN]\d+):\s*", re.MULTILINE)


def normalize_cell(s: str) -> str:
    """Collapse marker's column-wrapped whitespace into flowing text."""
    if not s:
        return ""
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s


def parse_pipe_table_rows(md_lines, start_idx, stop_pattern=r"^#+\s+\S"):
    """Yield lists of cells from a pipe-table block starting at start_idx.

    Skips non-pipe lines (captions, image refs, blanks) without stopping —
    the marker-rendered table can contain a mid-table caption ("Table 1...")
    and page-break image refs. Only stops at a markdown header line (matches
    stop_pattern) which signals the next section.
    """
    stop_re = re.compile(stop_pattern)
    i = start_idx
    while i < len(md_lines):
        line = md_lines[i].rstrip("\n")
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stop_re.match(stripped):
            break
        if not stripped.startswith("|"):
            i += 1
            continue
        # Detect alignment row (|---|---|...) and skip
        if re.match(r"^\|[\s\|:-]+\|$", stripped):
            i += 1
            continue
        # Split on pipe; drop leading/trailing empty splits
        cells = [c for c in re.split(r"\|", stripped)]
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        yield cells
        i += 1


def main():
    here = Path(__file__).parent
    md_path = here / "800-218a.md"
    csv_path = here / "800-218a-tasks.csv"
    json_path = here / "800-218a-tasks.json"

    md = md_path.read_text(encoding="utf-8")
    md_lines = md.splitlines()

    # Locate the header row of Table 1 (contains "Practice | Task | Priority").
    header_idx = None
    for i, line in enumerate(md_lines):
        if "Practice" in line and "Task" in line and "Priority" in line and line.startswith("|"):
            header_idx = i
            break
    if header_idx is None:
        raise SystemExit("Could not locate Table 1 header row")

    raw_rows = list(parse_pipe_table_rows(md_lines, header_idx + 1))
    if not raw_rows:
        raise SystemExit("Table 1 has no data rows")

    # Pre-process: pad each row to 5 columns, normalize cells. Drop rows that
    # are duplicate header rows (the marker output repeats "Practice | Task | ..."
    # on every page break).
    rows = []
    for cells in raw_rows:
        cells = cells + [""] * (5 - len(cells))
        cells = [normalize_cell(c) for c in cells[:5]]
        if cells[0] == "Practice" and cells[1] == "Task" and cells[2] == "Priority":
            continue
        rows.append(cells)

    # Identify task anchors. A row is an "anchor" if col 1 OR col 2 starts with
    # a task ID. Marker sometimes places PO.1.3's content row BEFORE its anchor
    # row (PDF layout); a content row immediately preceding an empty-content
    # anchor should attribute to that next task, not the previous one.
    task_re = re.compile(r"^((?:PO|PS|PW|RV)\.\d+\.\d+):\s*(.*)$", re.DOTALL)

    def anchor_match(row):
        """Return (task_id, task_text, practice_cell) or None."""
        col1, col2 = row[0], row[1]
        m2 = task_re.match(col2)
        if m2:
            return m2.group(1), m2.group(2), col1
        m1 = task_re.match(col1)
        if m1:
            return m1.group(1), m1.group(2), ""
        return None

    def has_substantive_content(row):
        """True if a row carries priority / R/C/N / refs (not just task or practice)."""
        return any(row[i] for i in (2, 3, 4))

    # Pass: assign each row to an "owning" task based on anchor position.
    # Rule: each anchor owns its own row, plus following content rows, UNLESS a
    # content row immediately precedes an empty-content anchor (then the content
    # row attributes to that next anchor).
    n = len(rows)
    owners = [None] * n  # task_id per row

    # First pass: mark anchor rows and detect empty-content anchors
    anchor_info = {}  # idx -> (task_id, task_text, practice_cell, is_empty_anchor)
    for i, row in enumerate(rows):
        a = anchor_match(row)
        if a:
            tid, ttext, pcell = a
            is_empty = not has_substantive_content(row)
            anchor_info[i] = (tid, ttext, pcell, is_empty)

    anchor_indices = sorted(anchor_info)

    # Second pass: assign rows to owners using look-ahead for empty anchors
    for k, idx in enumerate(anchor_indices):
        tid, _, _, _ = anchor_info[idx]
        owners[idx] = tid

    for k, idx in enumerate(anchor_indices):
        tid, _, _, _ = anchor_info[idx]
        next_idx = anchor_indices[k + 1] if k + 1 < len(anchor_indices) else n
        # Rows strictly between this anchor and the next belong to this task,
        # unless the next anchor is empty AND the row directly before next_idx
        # has substantive content (it belongs to next anchor instead).
        for i in range(idx + 1, next_idx):
            owners[i] = tid
        # Look-ahead reattribution: only the IMMEDIATELY preceding content row
        # belongs to the next task (PDF layout puts one orphan content row
        # before an empty-content anchor). Grabbing more would over-claim.
        if k + 1 < len(anchor_indices):
            next_tid, _, _, next_empty = anchor_info[next_idx]
            if next_empty:
                j = next_idx - 1
                if j > idx and j not in anchor_info and has_substantive_content(rows[j]):
                    owners[j] = next_tid

    # Build tasks dict
    tasks = {}
    practice_text_by_id = {}
    current_group = None

    for i, row in enumerate(rows):
        col_practice, col_task, col_priority, col_rcn, col_refs = row

        # Detect a group header row like "Prepare the Organization (PO)"
        if col_practice and col_task == "" and col_priority == "":
            mg = re.search(r"\((PO|PS|PW|RV)\)\s*$", col_practice)
            if mg:
                current_group = mg.group(1)
                continue

        # Pick up practice text whenever a cell names a practice (has (PO.N) id)
        for candidate in (col_practice, col_task):
            if candidate:
                pm = PRACTICE_ID_RE.search(candidate)
                if pm:
                    pid = pm.group(1)
                    # Don't store if the candidate IS the task ID (PO.N.M)
                    if not re.match(r"^(?:PO|PS|PW|RV)\.\d+\.\d+:", candidate):
                        if pid not in practice_text_by_id or len(candidate) > len(practice_text_by_id[pid]):
                            practice_text_by_id[pid] = candidate

        owner_tid = owners[i]
        if owner_tid is None:
            continue

        # If this row is the anchor for its owner, create the task entry
        if i in anchor_info:
            tid, ttext, _, _ = anchor_info[i]
            if tid == owner_tid and tid not in tasks:
                group_id = tid.split(".")[0]
                practice_id = ".".join(tid.split(".")[:2])
                tasks[tid] = {
                    "task_id": tid,
                    "group_id": group_id,
                    "group_name": PRACTICE_GROUP_NAMES.get(group_id, ""),
                    "practice_id": practice_id,
                    "practice_text": "",
                    "task_text": ttext,
                    "ai_priority": "",
                    "ai_additions": "",
                    "informative_references": "",
                }
                current_group = group_id

        # Make sure the owner has an entry (it may be a forward-attributed row
        # whose anchor we haven't seen yet — defer task_text fill).
        if owner_tid not in tasks:
            group_id = owner_tid.split(".")[0]
            practice_id = ".".join(owner_tid.split(".")[:2])
            tasks[owner_tid] = {
                "task_id": owner_tid,
                "group_id": group_id,
                "group_name": PRACTICE_GROUP_NAMES.get(group_id, ""),
                "practice_id": practice_id,
                "practice_text": "",
                "task_text": "",
                "ai_priority": "",
                "ai_additions": "",
                "informative_references": "",
            }
            current_group = group_id

        t = tasks[owner_tid]

        # Accumulate substantive cells. Skip col_task/col_practice if they are
        # the anchor row (already absorbed) — for non-anchor rows, col_task
        # text is treated as continuation of task_text.
        if i in anchor_info:
            # Anchor row: priority/R/C/N/refs (but task text already captured)
            if col_priority and not t["ai_priority"]:
                t["ai_priority"] = col_priority
            if col_rcn:
                t["ai_additions"] = (t["ai_additions"] + " " + col_rcn).strip() if t["ai_additions"] else col_rcn
            if col_refs:
                t["informative_references"] = (t["informative_references"] + " " + col_refs).strip() if t["informative_references"] else col_refs
        else:
            # Continuation / forward-attributed row
            if col_task and not task_re.match(col_task):
                t["task_text"] = (t["task_text"] + " " + col_task).strip()
            if col_priority and not t["ai_priority"]:
                t["ai_priority"] = col_priority
            if col_rcn:
                t["ai_additions"] = (t["ai_additions"] + " " + col_rcn).strip() if t["ai_additions"] else col_rcn
            if col_refs:
                t["informative_references"] = (t["informative_references"] + " " + col_refs).strip() if t["informative_references"] else col_refs

    # Backfill practice_text from the practice ID
    for t in tasks.values():
        t["practice_text"] = practice_text_by_id.get(t["practice_id"], "")

    # Split ai_additions into structured R/C/N items
    for t in tasks.values():
        items = []
        text = t["ai_additions"]
        if text and text != "No additions to SSDF 1.1":
            # Split on R\d+:, C\d+:, N\d+: anchors while keeping the markers
            parts = RCN_ITEM_RE.split(text)
            # parts = [prefix, "R1", body1, "C1", body2, ...]
            for j in range(1, len(parts), 2):
                marker = parts[j]
                body = parts[j + 1].strip() if j + 1 < len(parts) else ""
                # Trim a trailing fragment that belongs to the next item
                items.append({
                    "id": f"{t['task_id']}.{marker}",
                    "kind": {"R": "recommendation", "C": "consideration", "N": "note"}[marker[0]],
                    "marker": marker,
                    "text": body,
                })
        t["ai_additions_parsed"] = items

    def sort_key(r):
        group_order = ["PO", "PS", "PW", "RV"]
        parts = r["task_id"].split(".")
        return (
            group_order.index(r["group_id"]) if r["group_id"] in group_order else 99,
            int(parts[1]),
            int(parts[2]),
        )

    final = sorted(tasks.values(), key=sort_key)

    # CSV fields — flatten ai_additions_parsed back to a string for the CSV
    csv_fields = [
        "task_id", "group_id", "group_name",
        "practice_id", "practice_text", "task_text",
        "ai_priority", "ai_additions", "informative_references",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=csv_fields, quoting=csv.QUOTE_ALL,
                           extrasaction="ignore")
        w.writeheader()
        for row in final:
            w.writerow(row)

    # JSON keeps the parsed R/C/N item structure
    json_path.write_text(json.dumps(final, indent=2, ensure_ascii=False))

    print(f"Tasks: {len(final)}")
    print(f"Practices captured: {len(practice_text_by_id)}")
    for g in ["PO", "PS", "PW", "RV"]:
        cnt = sum(1 for r in final if r["group_id"] == g)
        n_high = sum(1 for r in final if r["group_id"] == g and r["ai_priority"] == "High")
        print(f"  {g} ({cnt} tasks, {n_high} High priority): {PRACTICE_GROUP_NAMES[g]}")


if __name__ == "__main__":
    main()
