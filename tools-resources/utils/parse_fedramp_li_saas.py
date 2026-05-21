#!/usr/bin/env python3
"""Parse FedRAMP SSP Appendix A LI-SaaS baseline controls into CSV/JSON.

LI-SaaS uses a different template than the High/Moderate/Low baselines. Each
control appears as a mid-prose bold anchor (not a markdown heading) and the
control name is on a separate preceding line:

    <a id="..."></a>AC-2 Account Management

    <a id="..."></a>**AC-2 Control Requirement(s)**

    a. Define and document the types of accounts ...
    b. [Excluded from FedRAMP Tailored for LI-SaaS]
    ...

    **AC-2 (h) (1) Additional FedRAMP Requirements and Guidance: **[twenty-four (24) hours]
    ...

    **AC-2 Control Summary Information**
    ...

Each control's body runs from the `**X Control Requirement(s)**` anchor to the
next control's anchor (or the `Control Summary Information` block, whichever
comes first).

Output (same schema as parse_fedramp_baseline.py for joinability across the
four baselines):
    ssp-appendix-a-li-saas-fedramp-security-controls-controls.{csv,json}

with columns:
    control_id, control_name, is_enhancement, parent_control_id,
    baseline, baseline_levels, control_text, fedramp_assignments

Usage:
    python3 tools-resources/utils/parse_fedramp_li_saas.py \\
        control/fedramp.gov/ssp-appendix-a-li-saas-fedramp-security-controls
"""
import csv
import json
import re
import sys
from pathlib import Path

# Anchor: optional <a id="..."></a> then bold-wrapped "CTRL Control Requirement(s)"
CONTROL_ANCHOR_RE = re.compile(
    r"(?:<a id=\"[^\"]*\"></a>)?"
    r"\*\*(?P<id>[A-Z]{2,3}-\d+(?:\(\d+\))?)\s+Control Requirement\(s\)\*\*",
)
# Name line preceding the anchor: <a id="..."></a>CTRL Name
NAME_LINE_RE = re.compile(
    r"(?:<a id=\"[^\"]*\"></a>)+(?P<id>[A-Z]{2,3}-\d+(?:\(\d+\))?)\s+(?P<name>[^*\n]+?)\s*$"
)
# Control summary block marks the end of the control body
SUMMARY_RE = re.compile(r"\*\*[A-Z]{2,3}-\d+(?:\(\d+\))?\s+Control Summary Information\*\*")
# FedRAMP "Additional Requirements" inline markers carrying parameter assignment values
ADDITIONAL_RE = re.compile(
    r"\*\*[A-Z]{2,3}-\d+(?:\(\d+\))?[^*]*?Additional FedRAMP Requirements[^*]*?\*\*\s*([^\n]+)",
)
# Markdown punctuation escapes
MD_ESCAPE_RE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])")


def normalize(s: str) -> str:
    s = MD_ESCAPE_RE.sub(r"\1", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def parent_id_of(cid: str) -> str:
    m = re.match(r"^([A-Z]{2,3}-\d+)\(\d+\)$", cid)
    return m.group(1) if m else ""


def find_control_name(md_lines, anchor_line_idx: int, cid: str) -> str:
    """Walk backward from the anchor to find the control's name line.

    Tolerates a space between the control number and the enhancement
    parenthetical (e.g., "IA-2 (1) Multi-factor Authentication"). Searches
    back up to 20 lines or until a `## ` family heading, whichever comes
    first.
    """
    # Allow "IA-2(1)" OR "IA-2 (1)" — split the cid into the AC-2 part and (1)
    m_enh = re.match(r"^([A-Z]{2,3}-\d+)(\(\d+\))$", cid)
    if m_enh:
        flex = re.escape(m_enh.group(1)) + r"\s*" + re.escape(m_enh.group(2))
    else:
        flex = re.escape(cid)
    needle = re.compile(rf"\b{flex}\s+(?!Control Requirement)([A-Z][^\n*]+?)\s*$")
    for i in range(anchor_line_idx - 1, max(-1, anchor_line_idx - 20), -1):
        line = md_lines[i].strip()
        if not line:
            continue
        if line.startswith("## "):
            # Hit family heading — stop searching backward
            break
        cleaned = re.sub(r"^(?:<a id=\"[^\"]*\"></a>)+", "", line)
        m = needle.match(cleaned)
        if m:
            return m.group(1).strip()
    return ""


def main(baseline_dir: Path):
    md_files = [p for p in baseline_dir.glob("*.md") if not p.name.endswith("-metadata.md")]
    if not md_files:
        raise SystemExit(f"No markdown file in {baseline_dir}")
    md = md_files[0].read_text(encoding="utf-8")
    md_lines = md.splitlines()

    # Find every "Control Requirement(s)" anchor along with its file offset
    anchors = []
    pos = 0
    for line_idx, line in enumerate(md_lines):
        for m in CONTROL_ANCHOR_RE.finditer(line):
            anchors.append({
                "control_id": m.group("id"),
                "line_idx": line_idx,
                "offset": pos + m.start(),
                "end": pos + m.end(),
            })
        pos += len(line) + 1  # +1 for the newline

    if not anchors:
        raise SystemExit("No control anchors found")

    rows = []
    for i, a in enumerate(anchors):
        cid = a["control_id"]
        body_start = a["end"]
        body_end = anchors[i + 1]["offset"] if i + 1 < len(anchors) else len(md)
        body = md[body_start:body_end]

        # Trim at Control Summary Information block
        sm = SUMMARY_RE.search(body)
        if sm:
            body = body[:sm.start()]

        # Look backward for the control name
        name = find_control_name(md_lines, a["line_idx"], cid)

        # Extract FedRAMP additional requirements (parameter values)
        fedramp_assignments = []
        for m in ADDITIONAL_RE.finditer(body):
            val = m.group(1).strip()
            val = MD_ESCAPE_RE.sub(r"\1", val)
            # Strip leading [ and trailing ]
            val = re.sub(r"^\[(.*)\]\s*$", r"\1", val)
            fedramp_assignments.append(val)

        is_enhancement = "(" in cid
        rows.append({
            "control_id": cid,
            "control_name": name,
            "is_enhancement": "true" if is_enhancement else "false",
            "parent_control_id": parent_id_of(cid),
            "baseline": "LI-SaaS",
            "baseline_levels": "LI-SaaS",
            "control_text": normalize(body),
            "fedramp_assignments": "\n".join(fedramp_assignments),
        })

    dirname = baseline_dir.name
    csv_path = baseline_dir / f"{dirname}-controls.csv"
    json_path = baseline_dir / f"{dirname}-controls.json"
    fields = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    n_base = sum(1 for r in rows if r["is_enhancement"] == "false")
    n_enh = sum(1 for r in rows if r["is_enhancement"] == "true")
    n_named = sum(1 for r in rows if r["control_name"])
    print(f"Controls: {len(rows)} ({n_base} base + {n_enh} enhancements)")
    print(f"  with name detected: {n_named}/{len(rows)}")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: parse_fedramp_li_saas.py <baseline-dir>")
    main(Path(sys.argv[1]).resolve())
