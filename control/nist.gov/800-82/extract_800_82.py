#!/usr/bin/env python3
"""Parse NIST SP 800-82r3 Appendix F (OT Overlay) into structured CSV/JSON.

Appendix F defines an OT-specific overlay of the NIST SP 800-53 control
catalog. Its primary structured content is:

  - Section F.3 Table 22: Control Baselines — one row per 800-53 control with
    LOW / MOD / HIGH baseline allocations indicating which controls (and
    which enhancements) the OT overlay selects at each impact level.

  - Section F.7+ per-control discussion: each control with OT-specific
    tailoring has an "OT Discussion:" paragraph. Some have additional
    "Control Enhancement: (N) OT Discussion: ..." paragraphs and "Rationale
    for adding ..." paragraphs.

Output: 800-82-r3-overlay.{csv,json} — one row per control with columns:
  control_id            e.g., "AC-1"
  control_name          e.g., "Policy and Procedures"
  low_baseline          text from Table 22's LOW column (or "")
  moderate_baseline     Table 22 MOD column
  high_baseline         Table 22 HIGH column
  ot_discussion         prose from the per-control discussion section (or "")
  enhancement_discussion the "Control Enhancement: (N) OT Discussion:" content
"""
import csv
import json
import re
from pathlib import Path

MD_ESCAPE_RE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])")
# Control ID at start of a markdown table row: | AC-1 | ...
CONTROL_ROW_RE = re.compile(
    r"^\|\s*(?P<id>[A-Z]{2,3}-\d+(?:\s*\(\d+\))?)\s*\|"
)
# Per-control discussion heading: #### **AC-1 ACCESS CONTROL POLICY AND PROCEDURES**
DISCUSSION_HEADING_RE = re.compile(
    r"^#+\s+(?:[➊-➓])?\s*\*\*(?P<id>[A-Z]{2,3}-\d+)\s+(?P<name>[A-Z][A-Z\s\-/'’,]+?)\*\*\s*$",
    re.MULTILINE,
)
OT_DISCUSSION_RE = re.compile(
    r"^(?:- )?(?:➑\s*)?OT Discussion:\s*(.+?)(?=\n\s*\n|\n- |\n\|)",
    re.DOTALL | re.MULTILINE,
)
ENH_DISCUSSION_RE = re.compile(
    r"^(?:- )?(?:➒\s*)?Control Enhancement:\s*\(\d+\)\s*OT Discussion:\s*(.+?)(?=\n\s*\n|\n- |\n\|)",
    re.DOTALL | re.MULTILINE,
)


def normalize(s):
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>", " ", s)
    s = MD_ESCAPE_RE.sub(r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_para(s):
    """Normalize but keep paragraph breaks."""
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>", " ", s)
    s = MD_ESCAPE_RE.sub(r"\1", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def find_table_22(md):
    """Locate Table 22 (Control Baselines). It starts with a header row
    'CNTL NO.' or 'CNTL\nNO.' and ends at the first '## ' heading after it."""
    # Find the Table 22 caption
    m = re.search(r"\*\*Table 22\.?\*\*\s+Control baselines", md, re.IGNORECASE)
    if not m:
        # Try without bold markers
        m = re.search(r"Table 22\.?\s+Control baselines", md, re.IGNORECASE)
    if not m:
        return ""
    start = m.end()
    # End at next major section heading
    end_m = re.search(r"\n##\s+", md[start:])
    end = start + (end_m.start() if end_m else 4000)
    return md[start:end]


def parse_table_22(block):
    """Yield (control_id, control_name, low, mod, high) tuples."""
    # Walk pipe-table rows
    rows = []
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        # Skip alignment rows
        if re.match(r"^\|[\s\|:-]+\|$", line.strip()):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)

    # The Table 22 row format: | CNTL_ID | CTRL_NAME | LOW | MOD | HIGH |
    # But marker may render headers and data inconsistently. The CONTROL_NAME
    # column may span multiple physical rows (continuation). Treat each row
    # with a CNTL_ID-shaped first cell as a new control.
    cnt_re = re.compile(r"^[A-Z]{2,3}-\d+(?:\s*\(\d+\))?$")
    results = []
    current = None
    for cells in rows:
        if not cells:
            continue
        first = cells[0].strip()
        if cnt_re.match(first):
            # New control row
            if current:
                results.append(current)
            # Pad to 5 cells if short
            cells = cells + [""] * (5 - len(cells))
            current = (first,
                       normalize(cells[1]) if len(cells) > 1 else "",
                       normalize(cells[2]) if len(cells) > 2 else "",
                       normalize(cells[3]) if len(cells) > 3 else "",
                       normalize(cells[4]) if len(cells) > 4 else "")
        elif current and any(c.strip() for c in cells):
            # Continuation row — append to current's fields
            cells = cells + [""] * (5 - len(cells))
            cid, name, low, mod, high = current
            current = (
                cid,
                (name + " " + normalize(cells[1])).strip() if cells[1].strip() else name,
                (low + " " + normalize(cells[2])).strip() if cells[2].strip() else low,
                (mod + " " + normalize(cells[3])).strip() if cells[3].strip() else mod,
                (high + " " + normalize(cells[4])).strip() if cells[4].strip() else high,
            )
    if current:
        results.append(current)
    return results


def find_per_control_discussions(md):
    """Walk F.7+ sections and pull each control's OT Discussion text.

    Returns {control_id: {"ot_discussion": str, "enhancement_discussion": str}}.
    """
    # Anchor on F.7 as a real markdown heading (not the TOC entry). Use
    # the second occurrence of "F.7." in the markdown — first is the TOC.
    matches = list(re.finditer(r"F\.7\.", md))
    start = matches[1].start() if len(matches) >= 2 else 0
    body = md[start:]

    out = {}
    # Find every per-control heading and capture the body until the next heading
    headings = list(DISCUSSION_HEADING_RE.finditer(body))
    for i, h in enumerate(headings):
        cid = h.group("id")
        sec_start = h.end()
        sec_end = headings[i + 1].start() if i + 1 < len(headings) else len(body)
        section = body[sec_start:sec_end]

        ot_m = OT_DISCUSSION_RE.search(section)
        ot_disc = normalize_para(ot_m.group(1)) if ot_m else ""
        enh_m = ENH_DISCUSSION_RE.search(section)
        enh_disc = normalize_para(enh_m.group(1)) if enh_m else ""

        if cid in out:
            # Multi-occurrence — concatenate
            if ot_disc and ot_disc not in out[cid]["ot_discussion"]:
                out[cid]["ot_discussion"] = (out[cid]["ot_discussion"] + "\n\n" + ot_disc).strip()
            if enh_disc and enh_disc not in out[cid]["enhancement_discussion"]:
                out[cid]["enhancement_discussion"] = (out[cid]["enhancement_discussion"] + "\n\n" + enh_disc).strip()
        else:
            out[cid] = {"ot_discussion": ot_disc, "enhancement_discussion": enh_disc}
    return out


def main():
    here = Path(__file__).parent
    md = (here / "800-82.md").read_text(encoding="utf-8")

    t22_block = find_table_22(md)
    baselines = parse_table_22(t22_block)
    discussions = find_per_control_discussions(md)

    # Merge: one row per control_id. Skip rows whose id ends with an
    # enhancement parenthesis (the enhancement-only rows fold into their
    # parent's baseline strings; we keep a separate "enhancement" view in
    # parent_id-based aggregation but for the primary table emit base controls).
    base_rows = {}
    for cid, name, low, mod, high in baselines:
        # Distinguish base from enhancement rows
        m_enh = re.match(r"^([A-Z]{2,3}-\d+)\s*\((\d+)\)$", cid)
        if m_enh:
            base_id = m_enh.group(1)
            # Append enhancement to parent's baseline strings (just record the
            # enhancement label in whichever baseline columns are non-empty).
            if base_id in base_rows:
                r = base_rows[base_id]
                # Annotate which baselines this enhancement applies to
                if low:
                    r["low_baseline_enhancements"] = (r.get("low_baseline_enhancements", "") + f" ({cid})").strip()
                if mod:
                    r["moderate_baseline_enhancements"] = (r.get("moderate_baseline_enhancements", "") + f" ({cid})").strip()
                if high:
                    r["high_baseline_enhancements"] = (r.get("high_baseline_enhancements", "") + f" ({cid})").strip()
            continue
        # Base control
        d = discussions.get(cid, {})
        base_rows[cid] = {
            "control_id": cid,
            "control_name": name,
            "low_baseline": low,
            "moderate_baseline": mod,
            "high_baseline": high,
            "ot_discussion": d.get("ot_discussion", ""),
            "enhancement_discussion": d.get("enhancement_discussion", ""),
        }

    # Add any controls that have OT discussion but didn't appear in Table 22
    for cid, d in discussions.items():
        if cid not in base_rows:
            base_rows[cid] = {
                "control_id": cid,
                "control_name": "",
                "low_baseline": "",
                "moderate_baseline": "",
                "high_baseline": "",
                "ot_discussion": d["ot_discussion"],
                "enhancement_discussion": d["enhancement_discussion"],
            }

    # Sort by control family + number
    def sort_key(r):
        m = re.match(r"^([A-Z]+)-(\d+)$", r["control_id"])
        return (m.group(1), int(m.group(2))) if m else (r["control_id"], 0)

    rows = sorted(base_rows.values(), key=sort_key)
    fields = ["control_id", "control_name", "low_baseline", "moderate_baseline",
              "high_baseline", "ot_discussion", "enhancement_discussion"]

    csv_path = here / "800-82-r3-overlay.csv"
    json_path = here / "800-82-r3-overlay.json"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL,
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    n_with_low = sum(1 for r in rows if r["low_baseline"])
    n_with_mod = sum(1 for r in rows if r["moderate_baseline"])
    n_with_high = sum(1 for r in rows if r["high_baseline"])
    n_with_disc = sum(1 for r in rows if r["ot_discussion"])
    print(f"Base controls: {len(rows)}")
    print(f"  in LOW baseline:  {n_with_low}")
    print(f"  in MOD baseline:  {n_with_mod}")
    print(f"  in HIGH baseline: {n_with_high}")
    print(f"  with OT Discussion text: {n_with_disc}")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    main()
