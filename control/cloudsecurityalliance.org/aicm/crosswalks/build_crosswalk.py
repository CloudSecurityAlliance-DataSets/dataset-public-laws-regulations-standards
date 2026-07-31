#!/usr/bin/env python3
"""Build a control-ID crosswalk between two AICM versions.

AICM renumbers control IDs between releases (see ../VERSIONING.md). CSA does not
publish a machine-readable old-ID -> new-ID crosswalk, so we reconstruct one by
matching control *content* rather than trusting the identifier.

Matching runs in confidence order. Every row records which pass matched it so a
reviewer can tell a certainty from a guess:

  exact-spec      normalized specification text is identical and unique   (certain)
  same-id+title   identifier and title both unchanged                     (certain)
  domain+title    same domain, identical title, different number          (high)
  same-id         identifier unchanged, title and/or spec reworded        (high)
  domain+fuzzy    same domain, specification similarity >= FUZZY_MIN      (REVIEW)

Matching is constrained to a single domain prefix throughout. AICM renumbering
happens by insertion/deletion within a domain, never across domains, and without
that constraint boilerplate policy language ("Establish, document, approve,
communicate, apply...") cross-matches unrelated domains.

Rows whose match_pass is `domain+fuzzy`, plus every added/removed row, are
flagged review_needed=yes. Those are heuristic. Do not treat this crosswalk as
authoritative for compliance purposes without working-group confirmation.

Usage:
    ./build_crosswalk.py \
        --old ../1.0.3/aicm-1.0.3.json \
        --new /path/to/AICMv1.1.0-generated_at_2026_06_18.xlsx \
        --old-version 1.0.3 --new-version 1.1.0 \
        --output aicm-1.0.3-to-1.1.0-crosswalk.csv

--old and --new each accept either an extracted AICM JSON (as committed in this
repo) or a publisher AICM .xlsx. Source spreadsheets are gitignored here; pull
them from s3://dataset-public-laws-regulations-standards/control/
cloudsecurityalliance.org/aicm/<version>/.
"""

import argparse
import csv
import difflib
import json
import re
import sys
from pathlib import Path

# Minimum specification similarity for a same-domain fuzzy match to be proposed.
# Below this the pair is reported as removed + added rather than as a rename.
FUZZY_MIN = 0.75

# Similarity at or above which a reworded specification is treated as cosmetic
# (whitespace, typo fixes) rather than a substantive requirement change.
SUBSTANTIVE_MAX = 0.95


def norm(text):
    """Collapse whitespace and case so formatting churn doesn't read as a change."""
    return re.sub(r"\s+", " ", text or "").strip().lower()


def domain_of(control_id):
    """DCS-17 -> DCS. Domain codes may contain '&' (A&A, I&S, DSP)."""
    return control_id.rsplit("-", 1)[0]


def similarity(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return [
        (c["control_id"], c["control_title"], c["control_specification"])
        for c in data["controls"]
    ]


def load_xlsx(path):
    """Read the 'AICM' sheet directly, mirroring parse_aicm.py's row geometry.

    Sheet layout: row 0 carries a JSON version stamp, row 1 spans group headers,
    row 2 is the real column header, data starts at row 3. Rows with a domain
    name but no Control ID are section separators and are skipped.
    """
    import pandas as pd

    df = pd.read_excel(path, sheet_name="AICM", header=None, skiprows=2).iloc[1:]
    controls = []
    for _, row in df.iterrows():
        control_id = row[2]
        if not isinstance(control_id, str) or not control_id.strip():
            continue
        controls.append(
            (control_id.strip(), str(row[1]).strip(), str(row[3]).strip())
        )
    return controls


def load(path):
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xlsm"):
        return load_xlsx(path)
    return load_json(path)


def match_controls(old, new):
    """Return {new_id: (old_id, match_pass)} using the passes described above."""
    old_by_id = {i: (t, s) for i, t, s in old}
    consumed = set()
    matches = {}

    by_spec = {}
    for i, _t, s in old:
        by_spec.setdefault(norm(s), []).append(i)

    for i, _t, s in new:  # pass 1 — exact, unique specification text
        candidates = by_spec.get(norm(s))
        if candidates and len(candidates) == 1 and candidates[0] not in consumed:
            matches[i] = (candidates[0], "exact-spec")
            consumed.add(candidates[0])

    for i, t, _s in new:  # pass 2 — identifier and title both unchanged
        if i in matches or i in consumed:
            continue
        if i in old_by_id and norm(old_by_id[i][0]) == norm(t):
            matches[i] = (i, "same-id+title")
            consumed.add(i)

    for i, t, _s in new:  # pass 3 — renumbered within domain, title intact
        if i in matches:
            continue
        candidates = [
            oi for oi, ot, _os in old
            if oi not in consumed and domain_of(oi) == domain_of(i) and norm(ot) == norm(t)
        ]
        if len(candidates) == 1:
            matches[i] = (candidates[0], "domain+title")
            consumed.add(candidates[0])

    for i, t, s in new:  # pass 4 — identifier held, text reworded
        if i in matches or i in consumed or i not in old_by_id:
            continue
        old_title, old_spec = old_by_id[i]
        if similarity(s, old_spec) >= FUZZY_MIN or similarity(t, old_title) >= 0.85:
            matches[i] = (i, "same-id")
            consumed.add(i)

    for i, _t, s in new:  # pass 5 — same domain, best surviving spec match
        if i in matches:
            continue
        best_id, best_score = None, 0.0
        for oi, _ot, os_ in old:
            if oi in consumed or domain_of(oi) != domain_of(i):
                continue
            score = similarity(s, os_)
            if score > best_score:
                best_id, best_score = oi, score
        if best_id and best_score >= FUZZY_MIN:
            matches[i] = (best_id, f"domain+fuzzy({best_score:.2f})")
            consumed.add(best_id)

    return matches, consumed


def classify_change(old_title, old_spec, new_title, new_spec, old_id, new_id):
    """Summarize what moved: the number, the title, the requirement text, or nothing."""
    parts = []
    if old_id != new_id:
        parts.append("id")
    if norm(old_title) != norm(new_title):
        parts.append("title")
    spec_sim = similarity(old_spec, new_spec)
    if norm(old_spec) != norm(new_spec):
        parts.append("spec-substantive" if spec_sim < SUBSTANTIVE_MAX else "spec-cosmetic")
    return ("+".join(parts) or "unchanged"), spec_sim


def build_rows(old, new, old_version, new_version):
    old_by_id = {i: (t, s) for i, t, s in old}
    matches, consumed = match_controls(old, new)
    rows = []

    for new_id, new_title, new_spec in new:
        if new_id not in matches:
            rows.append({
                "status": "added",
                "old_id": "", "new_id": new_id,
                "old_title": "", "new_title": new_title,
                "change": "added", "spec_similarity": "",
                "match_pass": "", "review_needed": "yes",
            })
            continue
        old_id, match_pass = matches[new_id]
        old_title, old_spec = old_by_id[old_id]
        change, spec_sim = classify_change(
            old_title, old_spec, new_title, new_spec, old_id, new_id
        )
        rows.append({
            "status": "carried",
            "old_id": old_id, "new_id": new_id,
            "old_title": old_title, "new_title": new_title,
            "change": change, "spec_similarity": f"{spec_sim:.3f}",
            "match_pass": match_pass,
            "review_needed": "yes" if match_pass.startswith("domain+fuzzy") else "no",
        })

    for old_id, old_title, _old_spec in old:
        if old_id in consumed:
            continue
        rows.append({
            "status": "removed",
            "old_id": old_id, "new_id": "",
            "old_title": old_title, "new_title": "",
            "change": "removed", "spec_similarity": "",
            "match_pass": "", "review_needed": "yes",
        })

    rows.sort(key=lambda r: (r["new_id"] == "", r["new_id"] or r["old_id"]))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--old", required=True, help="Older AICM version (.json or .xlsx)")
    ap.add_argument("--new", required=True, help="Newer AICM version (.json or .xlsx)")
    ap.add_argument("--old-version", required=True)
    ap.add_argument("--new-version", required=True)
    ap.add_argument("--output", required=True, help="Destination CSV")
    args = ap.parse_args()

    old = load(args.old)
    new = load(args.new)
    rows = build_rows(old, new, args.old_version, args.new_version)

    with open(args.output, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "status", "old_id", "new_id", "old_title", "new_title",
            "change", "spec_similarity", "match_pass", "review_needed",
        ])
        writer.writeheader()
        writer.writerows(rows)

    counts = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    renumbered = sum(
        1 for r in rows if r["status"] == "carried" and r["old_id"] != r["new_id"]
    )
    substantive = sum(1 for r in rows if "spec-substantive" in r["change"])
    review = sum(1 for r in rows if r["review_needed"] == "yes")

    print(f"AICM {args.old_version} ({len(old)}) -> {args.new_version} ({len(new)})")
    print(f"  carried    {counts.get('carried', 0)}  (renumbered {renumbered})")
    print(f"  added      {counts.get('added', 0)}")
    print(f"  removed    {counts.get('removed', 0)}")
    print(f"  specification substantively changed: {substantive}")
    print(f"  rows needing human review:           {review}")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
