#!/usr/bin/env python3
"""Parse FedRAMP SSP Appendix A baseline control templates (High/Moderate/Low).

Three of FedRAMP's four baseline SSP templates share a common structure where
each control appears as a markdown heading like:

    ## <a id="_Toc..."></a>AC-1 Policy and Procedures (L)(M)(H)

(Moderate uses two consecutive <a id="..."></a> anchors before the control ID
but is otherwise identical.) The heading carries the control ID, the control
name, and a baseline-membership tag like (L)(M)(H), (M)(H), or (H) indicating
which baselines include that control. The body that follows is the 800-53
control statement (with FedRAMP parameter assignment overrides inline), the
"Control Summary Information" template block, and the "What is the solution
and how is it implemented?" template block.

Output (one row per control): control_id, control_name, is_enhancement,
parent_control_id, baseline, baseline_levels, control_text (statement only,
through but not including the Control Summary Information block), and
fedramp_assignments (the concatenated values of any [FedRAMP Assignment: ...]
overrides found in the statement text).

The LI-SaaS Appendix A document uses a different template and is parsed by a
separate script.

Usage:
    python3 tools-resources/utils/parse_fedramp_baseline.py <baseline-dir>

e.g.:
    python3 tools-resources/utils/parse_fedramp_baseline.py \\
        control/fedramp.gov/ssp-appendix-a-high-fedramp-security-controls

Re-runnable: deletes and re-writes <dirname>-controls.{csv,json}.
"""
import csv
import json
import re
import sys
from pathlib import Path

# Heading patterns:
#   ## <a id="_Toc..."></a>AC-1 Policy and Procedures (L)(M)(H)         (base control)
#   ### <a id="_Toc..."></a>AC-2(1) Automated System Account Management (M)(H)  (enhancement)
# Moderate prefixes with two anchor tags; the (?:<a ...></a>)+ matches one-or-more.
HEADING_RE = re.compile(
    r"^(?P<lvl>##|###)\s+(?:<a id=\"[^\"]*\"></a>)+"
    r"(?P<id>[A-Z]{2,3}-\d+(?:\(\d+\))?)\s+"
    r"(?P<name>.+?)\s*\((?P<levels>[LMH)(]+)\)\s*$",
    re.MULTILINE,
)

SUMMARY_BLOCK_RE = re.compile(
    r"\*\*[A-Z]{2,3}-\d+(?:\(\d+\))?\s+Control Summary Information\*\*"
)
FEDRAMP_ASSIGNMENT_RE = re.compile(r"\[FedRAMP Assignment:\s*([^\]]+)\]")
# Markdown escapes the following ASCII punctuation per CommonMark; unescape
# them all so downstream consumers don't see literal backslashes in body text.
MD_ESCAPE_RE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])")

BASELINE_FROM_DIRNAME = {
    "high": "High",
    "moderate": "Moderate",
    "low": "Low",
}


def parse_baseline_levels(raw):
    """'L)(M)(H' -> 'L,M,H'."""
    parts = raw.replace("(", ")").split(")")
    return ",".join(p.strip() for p in parts if p.strip() in {"L", "M", "H"})


def parent_id_of(cid):
    """For 'AC-2(1)' return 'AC-2'. For 'AC-2' return ''."""
    m = re.match(r"^([A-Z]{2,3}-\d+)\(\d+\)$", cid)
    return m.group(1) if m else ""


def normalize_control_text(s):
    """Unescape markdown-escaped punctuation and collapse runs of blank lines."""
    s = MD_ESCAPE_RE.sub(r"\1", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def parse(baseline_dir):
    dirname = baseline_dir.name
    baseline = None
    for key, val in BASELINE_FROM_DIRNAME.items():
        # Match the literal segment ("-high-", "-moderate-", "-low-") in the dir
        # name to avoid partial matches.
        if f"-{key}-" in dirname:
            baseline = val
            break
    if baseline is None:
        raise SystemExit(f"Cannot determine baseline from dirname: {dirname}")

    md_files = [p for p in baseline_dir.glob("*.md") if not p.name.endswith("-metadata.md")]
    if not md_files:
        raise SystemExit(f"No markdown file in {baseline_dir}")
    md = md_files[0].read_text(encoding="utf-8")

    headings = list(HEADING_RE.finditer(md))
    rows = []
    for i, m in enumerate(headings):
        body_start = m.end()
        body_end = headings[i + 1].start() if i + 1 < len(headings) else len(md)
        body = md[body_start:body_end]

        # Control statement ends where the "Control Summary Information" block
        # begins; the rest is template scaffolding (parameter fill-ins,
        # implementation status checkboxes, "What is the solution...").
        sm = SUMMARY_BLOCK_RE.search(body)
        statement = body[:sm.start()] if sm else body

        cid = m.group("id")
        is_enhancement = "(" in cid
        levels = parse_baseline_levels(m.group("levels"))
        # Normalize before extracting FedRAMP assignment values so backslash-
        # escaped punctuation in the assignment text doesn't bleed through.
        statement_normalized = MD_ESCAPE_RE.sub(r"\1", statement)
        fedramp_assignments = "\n".join(
            a.strip() for a in FEDRAMP_ASSIGNMENT_RE.findall(statement_normalized)
        )

        rows.append({
            "control_id": cid,
            "control_name": m.group("name").strip(),
            "is_enhancement": "true" if is_enhancement else "false",
            "parent_control_id": parent_id_of(cid),
            "baseline": baseline,
            "baseline_levels": levels,
            "control_text": normalize_control_text(statement),
            "fedramp_assignments": fedramp_assignments,
        })

    return baseline, rows


def main(arg):
    baseline_dir = Path(arg).resolve()
    if not baseline_dir.is_dir():
        raise SystemExit(f"Not a directory: {baseline_dir}")

    baseline, rows = parse(baseline_dir)
    if not rows:
        raise SystemExit("No controls parsed — check the heading regex against the markdown.")

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
    print(f"Baseline: {baseline}")
    print(f"Controls: {len(rows)} ({n_base} base + {n_enh} enhancements)")
    print(f"Wrote {csv_path.name}, {json_path.name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__.split("Usage:")[1].strip())
    main(sys.argv[1])
