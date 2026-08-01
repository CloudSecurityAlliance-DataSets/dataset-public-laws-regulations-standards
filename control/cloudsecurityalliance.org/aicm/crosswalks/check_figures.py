#!/usr/bin/env python3
"""Assert that figures quoted in AICM prose match the committed data.

The AICM docs state counts — how many controls were renumbered, how many
identifiers now designate a different control — across seven files. Those figures
were derived from the crosswalk when written, and there is nothing stopping them
drifting when the crosswalk is regenerated. That has already happened once: a
matcher fix moved the repointed count from 55 to 54 and six files kept saying 55.

This recomputes each figure from the committed extractions and crosswalk, then
checks every place the prose states it.

Each check requires its pattern to match **at least once**. That is deliberate:
if someone rewords a sentence so the pattern stops matching, the check fails with
"pattern not found" rather than silently ceasing to verify anything. A failing
check means either the number is wrong or the checker needs teaching about the
new wording — both worth a human look.

    python3 check_figures.py          # from anywhere; paths are resolved relative to this file

Exit 0 if every figure agrees, 1 otherwise.
"""

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AICM = HERE.parent
REPO = AICM.parent.parent.parent

OLD_VERSION, NEW_VERSION = "1.0.3", "1.1.0"


def load():
    old = {c["control_id"]: c for c in
           json.loads((AICM / OLD_VERSION / f"aicm-{OLD_VERSION}.json").read_text())["controls"]}
    new = {c["control_id"]: c for c in
           json.loads((AICM / NEW_VERSION / f"aicm-{NEW_VERSION}.json").read_text())["controls"]}
    with open(HERE / f"aicm-{OLD_VERSION}-to-{NEW_VERSION}-crosswalk.csv", encoding="utf-8") as fh:
        crosswalk = list(csv.DictReader(fh))
    return old, new, crosswalk


def compute(old, new, crosswalk):
    """The authoritative figures. Everything the prose says must trace to one of these."""
    came_from = {r["new_id"]: r["old_id"] for r in crosswalk if r["new_id"]}
    shared = set(old) & set(new)
    repointed = sum(1 for cid in shared if came_from.get(cid) != cid)
    return {
        "carried": sum(1 for r in crosswalk if r["status"] == "carried"),
        "added": sum(1 for r in crosswalk if r["status"] == "added"),
        "removed": sum(1 for r in crosswalk if r["status"] == "removed"),
        "renumbered": sum(1 for r in crosswalk
                          if r["status"] == "carried" and r["old_id"] != r["new_id"]),
        "substantive": sum(1 for r in crosswalk if "spec-substantive" in r["change"]),
        "review_needed": sum(1 for r in crosswalk if r["review_needed"] == "yes"),
        "shared": len(shared),
        "repointed": repointed,
        "stable": len(shared) - repointed,
        "repointed_pct": round(repointed / len(shared) * 100),
    }


# (figure, regex with one capturing group, files it must appear in)
CHECKS = [
    ("carried",        r"\|\s*Carried over\s*\|\s*(\d+)\s*\|",                      ["VERSIONING.md"]),
    ("renumbered",     r"of which \*\*renumbered\*\*\s*\|\s*\*\*(\d+)\*\*",         ["VERSIONING.md"]),
    ("substantive",    r"specification substantively rewritten\s*\|\s*(\d+)\s*\|",  ["VERSIONING.md"]),
    ("added",          r"\|\s*Added\s*\|\s*(\d+)\s*\|",                             ["VERSIONING.md"]),
    ("removed",        r"\|\s*Removed\s*\|\s*(\d+)\s*\|",                           ["VERSIONING.md"]),
    ("shared",         r"Control IDs present in both releases\s*\|\s*(\d+)\s*\|",   ["VERSIONING.md"]),
    ("stable",         r"that still mean the same control\s*\|\s*(\d+)\s*\|",       ["VERSIONING.md"]),
    ("repointed",      r"now mean a \*different\* control\*\*\s*\|\s*\*\*(\d+)\*\*", ["VERSIONING.md"]),
    ("repointed_pct",  r"\*\*(\d+)% of shared identifiers were silently repointed",  ["VERSIONING.md"]),
    ("review_needed",  r"The (\d+) rows flagged `review_needed=yes`",                ["VERSIONING.md"]),
    ("repointed",      r"(\d+) of the 242 (?:control|shared) IDs",
     ["README.md", f"{NEW_VERSION}/README.md", f"{OLD_VERSION}/README.md",
      f"{NEW_VERSION}/aicm-{NEW_VERSION}-metadata.json",
      f"{OLD_VERSION}/aicm-{OLD_VERSION}-metadata.json"]),
    ("repointed",      r"\*\*(\d+) control IDs designate a different control in 1\.1\.0",
     [str(REPO / "README.md")]),
    ("shared",         r"\d+ of the (\d+) (?:control|shared) IDs",
     ["README.md", f"{NEW_VERSION}/README.md", f"{OLD_VERSION}/README.md",
      f"{NEW_VERSION}/aicm-{NEW_VERSION}-metadata.json",
      f"{OLD_VERSION}/aicm-{OLD_VERSION}-metadata.json"]),
]


def flatten(text):
    """Normalize prose so a figure split across a line wrap still matches.

    Hard-wrapped markdown puts arbitrary newlines mid-sentence, and inside a
    blockquote each continuation line also carries a `> ` marker. Strip the
    markers, then collapse whitespace, so patterns can be written as they read.
    """
    return re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>\s?", "", text))


def main():
    figures = compute(*load())
    failures = []

    for figure, pattern, files in CHECKS:
        expected = str(figures[figure])
        for rel in files:
            path = Path(rel) if Path(rel).is_absolute() else AICM / rel
            if not path.exists():
                failures.append(f"{rel}: file not found")
                continue
            found = re.findall(pattern, flatten(path.read_text()))
            if not found:
                failures.append(
                    f"{rel}: no match for {figure} — pattern {pattern!r} found nothing. "
                    "Prose reworded? Update the pattern or restore the figure.")
                continue
            for value in found:
                if value != expected:
                    failures.append(
                        f"{rel}: {figure} says {value}, data says {expected}")

    print(f"AICM {OLD_VERSION} -> {NEW_VERSION} figures from the committed data:")
    for key, value in figures.items():
        print(f"  {key:16} {value}")
    print()

    if failures:
        print(f"{len(failures)} mismatch(es):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"All {sum(len(f) for _, _, f in CHECKS)} documented figures agree with the data.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
