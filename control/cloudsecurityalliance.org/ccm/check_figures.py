#!/usr/bin/env python3
"""Assert that figures quoted about CCM 4.1.1 match the committed data.

CSA shipped CCM 4.1.1 inside the unchanged "v4.1" bundle, and its Change Log
names two text fixes where the workbook carries 127 reworded cells. Every count
the 4.1.1 docs quote was measured once, by hand, against the downloaded
workbooks; this script recomputes them from the committed extractions so they
cannot drift. It is the CCM counterpart of ../aicm/crosswalks/check_figures.py
and follows its shape:

  INVARIANTS  claims about the data itself — what the 4.1.1 write-up rests on.
  CHECKS      every place the prose states a figure. Each pattern must match at
              least once, so rewording a sentence fails loudly instead of
              silently ending the check.

Text comparisons between 4.1.0 and 4.1.1 are made on *normalised* text
(whitespace runs collapsed, ends stripped), because CSA regenerated the workbook
and changed line breaks in hundreds of cells without changing their words. A
change is *punctuation only* if the two texts are equal once whitespace, commas,
semicolons and full stops are deleted and case is folded.

    python3 check_figures.py          # from anywhere; paths resolve relative to this file

Exit 0 if every figure agrees, 1 otherwise.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

CCM = Path(__file__).resolve().parent
CSA = CCM.parent
REPO = CSA.parent.parent

OLD, NEW = "4.1.0", "4.1.1"
NEW_JSON = CCM / NEW / f"ccm-{NEW}.json"
OLD_JSON = CCM / OLD / f"ccm-{OLD}.json"

# The standalone questionnaire. CSA regenerated it on 2026-10-02 without changing
# its 4.1.0 label, and ccm-caiq/4.1.0/ was re-extracted in place; its README lists
# every question whose text changed. The 2026-01-13 text is checked against the
# questions embedded in ccm-4.1.0.json, which match the replaced extraction.
CAIQ_DIR = CSA / "ccm-caiq" / "4.1.0"
CAIQ_JSON = CAIQ_DIR / "ccm-caiq-4.1.0.json"
CAIQ_README = CAIQ_DIR / "README.md"
TABLE_ROW = re.compile(r"^\| `([A-Z&]+-\d+\.\d+)` \| (.*?) \| (.*?) \| (yes|no) \|$")

NIST, ATTACK = "nist_sp_800_171_rev2", "mitre_attack"
NO_MAPPING = "No Mapping"

# The fields whose equality across 4.1.0 -> 4.1.1 the docs claim.
UNCHANGED_FIELDS = ["control_title", "implementation_guidelines", "auditing_guidelines",
                    "typical_control_applicability_and_ownership",
                    "architectural_relevance_cloud_stack_components",
                    "organizational_relevance", "ccm_lite"]


def norm(text):
    return re.sub(r"\s+", " ", text).strip() if isinstance(text, str) else text


def punct_only(a, b):
    strip = lambda s: re.sub(r"[\s,;.]", "", s).lower()
    return strip(a) == strip(b)


def deep_norm(value):
    if isinstance(value, dict):
        return {k: deep_norm(v) for k, v in value.items()}
    if isinstance(value, list):
        return [deep_norm(v) for v in value]
    return norm(value)


def load():
    def controls(path):
        doc = json.loads(path.read_text())
        return {c["control_id"]: c for c in doc["controls"]}, doc
    old, _ = controls(OLD_JSON)
    new, new_doc = controls(NEW_JSON)
    return old, new, new_doc


def compute(old, new, new_doc):
    """The authoritative figures. Everything the prose says must trace to one of these."""
    shared = sorted(set(old) & set(new))

    def mapping_tally(key):
        cells = [(c.get("scope_applicability_mappings") or {}).get(key) or {} for c in new.values()]
        values = [m.get("control_mapping") for m in cells]
        return {
            "mapped": sum(1 for v in values if v and v != NO_MAPPING),
            "no_mapping": sum(1 for v in values if v == NO_MAPPING),
            "blank": sum(1 for v in values if not v),
            "gap": dict(sorted(Counter(m.get("gap_level") for m in cells).items())),
        }

    spec_changed = [cid for cid in shared
                    if norm(old[cid]["control_specification"]) != norm(new[cid]["control_specification"])]
    spec_wording = [cid for cid in spec_changed
                    if not punct_only(norm(old[cid]["control_specification"]),
                                      norm(new[cid]["control_specification"]))]

    def questions(controls):
        return {q["question_id"]: norm(q["question"])
                for c in controls.values() for q in c["caiq_questions"]}
    old_q, new_q = questions(old), questions(new)
    caiq_changed = [qid for qid in sorted(set(old_q) & set(new_q)) if old_q[qid] != new_q[qid]]
    caiq_wording = [qid for qid in caiq_changed if not punct_only(old_q[qid], new_q[qid])]

    provisions = new_doc["reverse_mappings"]["dora"]["provisions"]
    refs = [cid for p in provisions for cid in p["ccm_controls"]]

    nist, attack = mapping_tally(NIST), mapping_tally(ATTACK)
    figures = {
        "specification_version": new_doc["specification_version"],
        "generated_at": new_doc["generated_at"],
        "controls": len(new),
        "domains": len({c["control_domain"] for c in new.values()}),
        "ids_added": len(set(new) - set(old)),
        "ids_removed": len(set(old) - set(new)),
        "caiq_embedded": len(new_q),
        "frameworks": new_doc["mapping_frameworks"],
        "nist_mapped": nist["mapped"], "nist_no_mapping": nist["no_mapping"],
        "nist_blank": nist["blank"], "nist_gap": nist["gap"],
        "attack_mapped": attack["mapped"], "attack_no_mapping": attack["no_mapping"],
        "attack_blank": attack["blank"], "attack_gap": attack["gap"],
        "dora_provisions": len(provisions),
        "dora_gap": dict(sorted(Counter(p["gap_level"] for p in provisions).items())),
        "dora_empty_ccm_controls": sum(1 for p in provisions if not p["ccm_controls"]),
        "dora_refs": len(refs),
        "dora_unknown_refs": sorted(set(refs) - set(new)),
        "spec_changed": len(spec_changed),
        "spec_punct_only": len(spec_changed) - len(spec_wording),
        "spec_wording": spec_wording,
        "caiq_changed": len(caiq_changed),
        "caiq_punct_only": len(caiq_changed) - len(caiq_wording),
        "caiq_wording": caiq_wording,
    }
    for field in UNCHANGED_FIELDS:
        figures[f"changed_{field}"] = sum(
            1 for cid in shared if deep_norm(old[cid].get(field)) != deep_norm(new[cid].get(field)))
    figures.update(compute_caiq(old_q, caiq_changed))
    return figures


def compute_caiq(old_q, caiq_changed):
    """The standalone questionnaire, and the README table of its changed questions."""
    caiq = json.loads(CAIQ_JSON.read_text())
    standalone = {q["question_id"]: norm(q["question"]) for q in caiq["questions"]}
    rows = []
    if CAIQ_README.exists():
        for line in CAIQ_README.read_text().splitlines():
            m = TABLE_ROW.match(line.strip())
            if m:
                qid, before, after, flag = m.groups()
                rows.append((qid, before.replace("\\|", "|"), after.replace("\\|", "|"), flag == "yes"))
    return {
        "caiq_version": caiq.get("caiq_version"),
        "caiq_ccm_version": caiq.get("ccm_version"),
        "caiq_generated_at": caiq.get("generated_at"),
        "caiq_questions": len(standalone),
        "readme_rows": len(rows),
        "readme_ids_match_changed": sorted(r[0] for r in rows) == sorted(caiq_changed),
        "readme_old_text_mismatch": [r[0] for r in rows if old_q.get(r[0]) != r[1]],
        "readme_new_text_mismatch": [r[0] for r in rows if standalone.get(r[0]) != r[2]],
        "readme_punct_flag_wrong": [r[0] for r in rows if punct_only(r[1], r[2]) != r[3]],
    }


# (figure, expected value, why it must hold) — asserted against the data itself,
# not against prose. Measured 2026-10-22 against CCMv4.1.1-generated_at_2026_10_02.xlsx.
INVARIANTS = [
    ("specification_version", NEW, "cell A1 of the source workbook stamps 4.1.1"),
    ("generated_at", "2026-10-02", "the source workbook's filename token"),
    ("controls", 207, "4.1.1 has 207 controls"),
    ("domains", 17, "4.1.1 has 17 domains"),
    ("ids_added", 0, "4.1.1 adds no control IDs"),
    ("ids_removed", 0, "4.1.1 removes no control IDs"),
    ("caiq_embedded", 283, "the CAIQ sheet carries 283 questions"),
    ("frameworks", ["NIST SP 800-171 rev2", "MITRE ATT&CK"], "the two mapping blocks 4.1.1 ships"),
    ("nist_mapped", 152, "NIST SP 800-171 rev2: controls with a mapping"),
    ("nist_no_mapping", 55, "NIST SP 800-171 rev2: the literal 'No Mapping'"),
    ("nist_blank", 0, "NIST SP 800-171 rev2: no empty mapping cell"),
    ("nist_gap", {"Full Gap": 55, "No Gap": 54, "Partial Gap": 98}, "NIST gap levels"),
    ("attack_mapped", 57, "MITRE ATT&CK: controls mapped to technique IDs"),
    ("attack_no_mapping", 150, "MITRE ATT&CK: the literal 'No Mapping'"),
    ("attack_blank", 0, "MITRE ATT&CK: no empty mapping cell"),
    ("attack_gap", {"Full Gap": 150, "No Gap": 57}, "ATT&CK gap levels"),
    ("dora_provisions", 215, "DORA provisions in the reverse mapping"),
    ("dora_gap", {"Full Gap": 7, "No Gap": 94, "Partial Gap": 114}, "DORA gap levels"),
    ("dora_empty_ccm_controls", 7, "the Full Gap provisions list no CCM control"),
    ("dora_refs", 727, "DORA -> CCM control references"),
    ("dora_unknown_refs", [], "every DORA reference names one of the 207 controls"),
    ("spec_changed", 101, "control specifications whose normalised text differs from 4.1.0"),
    ("spec_punct_only", 92, "of those, punctuation-only edits"),
    ("spec_wording", ["CCC-06", "DCS-06", "DSP-17", "IAM-10", "IAM-12", "IAM-13",
                      "LOG-07", "STA-11", "TVM-06"], "the specifications whose wording changed"),
    ("caiq_changed", 26, "CAIQ questions whose normalised text differs from 4.1.0"),
    ("caiq_punct_only", 19, "of those, punctuation-only edits"),
    ("caiq_wording", ["DCS-02.2", "DCS-06.2", "DCS-11.1", "I&S-05.1", "IAM-13.1",
                      "LOG-07.1", "UEM-02.1"], "the questions whose wording changed"),
] + [(f"changed_{field}", 0, f"{field} is unchanged from 4.1.0 once whitespace is normalised")
     for field in UNCHANGED_FIELDS] + [
    ("caiq_version", "4.1.0", "the regenerated questionnaire still calls itself CAIQ 4.1.0"),
    ("caiq_ccm_version", NEW, "its cell A1 records the CCM release it was generated from"),
    ("caiq_generated_at", "2026-10-02", "the 2026-10-02 generation is the one extracted"),
    ("caiq_questions", 283, "the standalone questionnaire carries 283 questions"),
    ("readme_rows", 26, "ccm-caiq/4.1.0/README.md lists every changed question, one row each"),
    ("readme_ids_match_changed", True, "the README rows are exactly the changed questions"),
    ("readme_old_text_mismatch", [], "each 2026-01-13 cell is the 4.1.0 text"),
    ("readme_new_text_mismatch", [], "each 2026-10-02 cell is the committed text"),
    ("readme_punct_flag_wrong", [], "each 'Punctuation only' flag is right"),
]

# (figure, regex with one capturing group, files it must appear in). Paths are
# relative to this directory unless absolute.
CHECKS = []


def flatten(text):
    """Normalise prose so a figure split across a line wrap still matches."""
    return re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>\s?", "", text))


def check_prose(figures, checks):
    failures = []
    for figure, pattern, files in checks:
        expected = str(figures[figure])
        for rel in files:
            path = Path(rel) if Path(rel).is_absolute() else CCM / rel
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
                    failures.append(f"{rel}: {figure} says {value}, data says {expected}")
    return failures


def check_invariants(figures, invariants):
    return [
        f"INVARIANT BROKEN: {figure} is {figures[figure]!r}, must be {expected!r} — {why}"
        for figure, expected, why in invariants
        if figures[figure] != expected
    ]


def main():
    missing = [p for p in (OLD_JSON, NEW_JSON, CAIQ_JSON) if not p.exists()]
    if missing:
        for p in missing:
            print(f"missing extraction: {p.relative_to(REPO)}", file=sys.stderr)
        return 1

    figures = compute(*load())
    failures = check_invariants(figures, INVARIANTS) + check_prose(figures, CHECKS)

    print(f"CCM {OLD} -> {NEW} figures from the committed data:")
    for key, value in figures.items():
        print(f"  {key:46} {value}")
    print()

    if failures:
        print(f"{len(failures)} problem(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    documented = sum(len(files) for _, _, files in CHECKS)
    print(f"All {len(INVARIANTS)} invariants hold, and all {documented} documented figures agree with the data.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
