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

# The 1.1.0 -> 1.1.1 patch release. Checked differently from the pair above: there
# is no crosswalk because no control IDs moved, so the figures are computed by
# diffing the two extractions directly, and the "nothing moved" claim the 1.1.1
# docs rest on is itself asserted as an invariant.
PATCH_OLD, PATCH_NEW = "1.1.0", "1.1.1"


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


def load_patch():
    def controls(version):
        data = json.loads((AICM / version / f"aicm-{version}.json").read_text())
        return {c["control_id"]: c for c in data["controls"]}, data
    old, old_doc = controls(PATCH_OLD)
    new, new_doc = controls(PATCH_NEW)
    return old, old_doc, new, new_doc


def compute_patch(old, old_doc, new, new_doc):
    """Figures for the 1.1.0 -> 1.1.1 patch, straight from the two extractions."""
    shared = set(old) & set(new)

    def mapping(control, slug):
        return ((control.get("scope_applicability_mappings") or {})
                .get(slug, {}) or {}).get("control_mapping")

    def tally(slug, predicate):
        return sum(1 for c in new.values() if predicate(mapping(c, slug)))

    mapped = lambda v: bool(v) and v != "No Mapping"
    no_mapping = lambda v: v == "No Mapping"
    blank = lambda v: not v

    # Fields whose equality across the two releases is what "patch release" means.
    identity = ["control_domain", "control_title", "control_specification",
                "control_type", "typical_control_applicability_and_ownership",
                "architectural_relevance_ai_stack_components", "lifecycle_relevance",
                "threat_category", "auditing_guidelines"]

    def differing(field):
        return sum(1 for cid in shared
                   if json.dumps(old[cid][field], sort_keys=True)
                   != json.dumps(new[cid][field], sort_keys=True))

    return {
        "patch_controls": len(new),
        "patch_domains": len({c["control_domain"] for c in new.values()}),
        "patch_ids_added": len(set(new) - set(old)),
        "patch_ids_removed": len(set(old) - set(new)),
        "patch_identity_changed": sum(differing(f) for f in identity),
        "patch_impl_changed": differing("implementation_guidelines"),
        "patch_caiq_changed": differing("caiq_questions"),
        "patch_frameworks_old": len(old_doc["mapping_frameworks"]),
        "patch_frameworks_new": len(new_doc["mapping_frameworks"]),
        "aiuc_mapped": tally("aiuc_1_q2_2026_version", mapped),
        "aiuc_no_mapping": tally("aiuc_1_q2_2026_version", no_mapping),
        "aiuc_blank": tally("aiuc_1_q2_2026_version", blank),
        "nist_mapped": tally("nist_ai_rmf_nist_ai_600_1", mapped),
        "nist_no_mapping": tally("nist_ai_rmf_nist_ai_600_1", no_mapping),
        "eu_no_mapping": tally("eu_ai_act", no_mapping),
    }


# (figure, expected value, why it must hold) — asserted against the data itself,
# not against prose. These are the claims the whole 1.1.1 write-up rests on: if
# any breaks, the docs are wrong no matter what numbers they quote.
PATCH_INVARIANTS = [
    ("patch_ids_added", 0, "1.1.1 must add no control IDs"),
    ("patch_ids_removed", 0, "1.1.1 must remove no control IDs"),
    ("patch_identity_changed", 0,
     "no control's domain, title, specification, type, ownership, relevance grids, "
     "threat categories or auditing guidelines may differ from 1.1.0 — this is what "
     "licenses migrating a reference by string match, and the absence of a crosswalk"),
    ("patch_impl_changed", 3, "exactly GRC-01, IAM-13, IAM-18 differ in implementation guidelines"),
    ("patch_caiq_changed", 1, "exactly SEF-06 differs in its AI-CAIQ questions"),
    ("patch_frameworks_old", 3, "1.1.0 carried three mapping frameworks"),
    ("patch_frameworks_new", 5, "1.1.1 carries five mapping frameworks"),
]

# (figure, regex with one capturing group, files it must appear in)
PATCH_CHECKS = [
    ("patch_controls",  r"· (\d+) controls · \d+ domains",          [f"{PATCH_NEW}/README.md"]),
    ("patch_domains",   r"· \d+ controls · (\d+) domains",          [f"{PATCH_NEW}/README.md"]),
    ("aiuc_mapped",     r"(\d+) mapped · \d+ `No Mapping` · \d+ blank", [f"{PATCH_NEW}/README.md"]),
    ("aiuc_no_mapping", r"\d+ mapped · (\d+) `No Mapping` · \d+ blank", [f"{PATCH_NEW}/README.md"]),
    ("aiuc_blank",      r"`No Mapping` · (\d+) blank",              [f"{PATCH_NEW}/README.md"]),
    ("nist_mapped",     r"(\d+) mapped · \d+ `No Mapping` \|",      [f"{PATCH_NEW}/README.md"]),
    ("nist_no_mapping", r"\d+ mapped · (\d+) `No Mapping` \|",      [f"{PATCH_NEW}/README.md"]),
    ("aiuc_no_mapping", r"AIUC-1 \((\d+) controls?\)",
     [f"{PATCH_NEW}/README.md", f"{PATCH_NEW}/aicm-{PATCH_NEW}-metadata.json"]),
    ("nist_no_mapping", r"NIST \((\d+)\)",                          [f"{PATCH_NEW}/README.md"]),
    ("nist_no_mapping", r"AI 600-1 \((\d+) controls\)",
     [f"{PATCH_NEW}/aicm-{PATCH_NEW}-metadata.json"]),
    ("eu_no_mapping",   r"EU AI Act \((\d+), unchanged",            [f"{PATCH_NEW}/README.md"]),
    ("eu_no_mapping",   r"EU AI Act \((\d+) controls, unchanged",
     [f"{PATCH_NEW}/aicm-{PATCH_NEW}-metadata.json"]),
    ("aiuc_no_mapping", r"the other (\d+) unmapped controls",       [f"{PATCH_NEW}/README.md"]),
    ("aiuc_no_mapping", r"the other (\d+) controls with no AIUC-1",
     [f"{PATCH_NEW}/aicm-{PATCH_NEW}-metadata.json"]),
]


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


def check_prose(figures, checks):
    """Verify every place the prose states a figure. Returns a list of failures."""
    failures = []
    for figure, pattern, files in checks:
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
    return failures


def check_invariants(figures, invariants):
    """Verify structural claims against the data rather than against prose."""
    return [
        f"INVARIANT BROKEN: {figure} is {figures[figure]}, must be {expected} — {why}"
        for figure, expected, why in invariants
        if figures[figure] != expected
    ]


def report(title, figures):
    print(title)
    for key, value in figures.items():
        print(f"  {key:24} {value}")
    print()


def main():
    figures = compute(*load())
    patch = compute_patch(*load_patch())

    failures = (check_prose(figures, CHECKS)
                + check_invariants(patch, PATCH_INVARIANTS)
                + check_prose(patch, PATCH_CHECKS))

    report(f"AICM {OLD_VERSION} -> {NEW_VERSION} figures from the committed data:", figures)
    report(f"AICM {PATCH_OLD} -> {PATCH_NEW} figures from the committed data:", patch)

    if failures:
        print(f"{len(failures)} problem(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    documented = sum(len(f) for _, _, f in CHECKS) + sum(len(f) for _, _, f in PATCH_CHECKS)
    print(f"All {documented} documented figures agree with the data, "
          f"and all {len(PATCH_INVARIANTS)} patch invariants hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
