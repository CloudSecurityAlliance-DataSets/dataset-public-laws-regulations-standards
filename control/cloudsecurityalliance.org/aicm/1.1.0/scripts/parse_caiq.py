#!/usr/bin/env python3
"""Parse the standalone AI-CAIQ v1.1.0 questionnaire into JSON, enriched with AICM control data.

Updated from the v1.0.3-era parser (../../1.0.3/scripts/parse_caiq.py). Changes:

  * The questionnaire sheet is named after its own version — 'AI-CAIQv1.0.2'
    became 'AI-CAIQv1.1.0'. It is now discovered by prefix rather than hardcoded,
    so the next release does not break this script.
  * Columns 6 and 7 of the questionnaire sheet are unlabelled and entirely empty
    in v1.1.0. Named columns are addressed via COLUMNS below rather than by bare
    offsets, so a future release that fills or removes those spacers is easier to
    follow.
  * Version is read from the JSON stamp in cell A1 rather than hardcoded.
  * Paths come from the command line.

The AICM side must be parsed first — run parse_aicm.py, then this.

Output lands under aicm-caiq/, not aicm/: the questionnaire is a separate SecID
source (secid:control/cloudsecurityalliance.org/aicm-caiq@1.1.0).

Usage:
    ./parse_caiq.py --input AI_CAIQv1.1.0-star_security_questionnaire-generated_at_2026_06_18.xlsx
"""

import argparse
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(__file__)
DEFAULT_AICM_JSON = os.path.join(HERE, "..", "aicm-1.1.0.json")
DEFAULT_OUTPUT = os.path.join(
    HERE, "..", "..", "..", "aicm-caiq", "1.1.0", "aicm-caiq-1.1.0.json"
)

# Column positions in the questionnaire sheet. Columns 6 and 7 are unlabelled and
# empty in v1.1.0 — left out deliberately rather than forgotten.
COLUMNS = {
    "question_id": 0,
    "question": 1,
    "service_provider_answer": 2,
    "ssrm_control_ownership": 3,
    "service_provider_implementation_description": 4,
    "service_customer_responsibilities": 5,
    "aicm_control_id": 8,
    "aicm_control_specification": 9,
    "aicm_control_title": 10,
    "aicm_domain_title": 11,
}

# Question IDs look like A&A-01.1 / MDS-02.3. Domain codes may contain '&'.
QUESTION_ID = re.compile(r"^[A-Z&]{2,4}-\d+\.\d+$")

# Control fields copied onto each question. Excludes caiq_questions, which would
# be circular, and the per-question answer columns, which belong to the response.
CONTROL_FIELDS = [
    "control_domain",
    "control_title",
    "control_id",
    "control_specification",
    "control_type",
    "typical_control_applicability_and_ownership",
    "architectural_relevance_ai_stack_components",
    "lifecycle_relevance",
    "threat_category",
    "implementation_guidelines",
    "auditing_guidelines",
    "scope_applicability_mappings",
]


def clean(val):
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str):
        return val.strip()
    return val


def find_questionnaire_sheet(xlsx):
    """The questionnaire tab is named for its version: 'AI-CAIQv1.1.0'."""
    candidates = [s for s in pd.ExcelFile(xlsx).sheet_names if s.upper().startswith("AI-CAIQ")]
    if len(candidates) != 1:
        print(
            f"error: expected exactly one AI-CAIQ sheet, found {candidates or 'none'}",
            file=sys.stderr,
        )
        sys.exit(1)
    return candidates[0]


def read_specification_version(xlsx, sheet):
    a1 = pd.read_excel(xlsx, sheet_name=sheet, header=None, nrows=1).iloc[0, 0]
    try:
        return json.loads(a1)["specification_version"]
    except (TypeError, ValueError, KeyError):
        print(f"warning: could not read version stamp from cell A1 ({a1!r})", file=sys.stderr)
        return None


def parse_questions(xlsx, sheet):
    """One row per question. AICM reference columns are populated only on a
    control's first question row, so they are forward-filled."""
    df = pd.read_excel(xlsx, sheet_name=sheet, header=None, skiprows=1).iloc[1:]

    questions = []
    carried = {k: None for k in
               ("aicm_control_id", "aicm_control_specification",
                "aicm_control_title", "aicm_domain_title")}

    for _, row in df.iterrows():
        question_id = clean(row[COLUMNS["question_id"]])
        if not isinstance(question_id, str) or not QUESTION_ID.match(question_id):
            continue  # section separators, 'End of Standard', copyright footer

        for field in carried:
            value = clean(row[COLUMNS[field]])
            if value:
                carried[field] = value

        questions.append({
            "question_id": question_id,
            "question": clean(row[COLUMNS["question"]]),
            **carried,
        })

    return questions


def enrich_with_aicm(questions, aicm_json):
    """Attach the full AICM control record to each question."""
    with open(aicm_json, encoding="utf-8") as fh:
        controls = {c["control_id"]: c for c in json.load(fh)["controls"]}

    unmatched = set()
    for question in questions:
        control = controls.get(question["aicm_control_id"])
        if control is None:
            unmatched.add(question["aicm_control_id"])
            question["aicm_control"] = None
            continue
        question["aicm_control"] = {f: control[f] for f in CONTROL_FIELDS}

    if unmatched:
        print(
            f"warning: {len(unmatched)} control IDs referenced by the questionnaire "
            f"are absent from the AICM extraction: {sorted(unmatched)[:8]}",
            file=sys.stderr,
        )
    return questions


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", required=True, help="Standalone AI-CAIQ v1.1.0 .xlsx")
    ap.add_argument("--aicm-json", default=DEFAULT_AICM_JSON,
                    help="AICM extraction produced by parse_aicm.py (default: %(default)s)")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="Destination JSON (default: %(default)s)")
    args = ap.parse_args()

    if not os.path.exists(args.aicm_json):
        print(f"error: {args.aicm_json} not found. Run parse_aicm.py first.", file=sys.stderr)
        sys.exit(1)

    sheet = find_questionnaire_sheet(args.input)
    questions = enrich_with_aicm(parse_questions(args.input, sheet), args.aicm_json)

    with open(args.aicm_json, encoding="utf-8") as fh:
        aicm_version = json.load(fh)["specification_version"]

    output = {
        "specification_name": "AI Consensus Assessments Initiative Questionnaire",
        "caiq_version": read_specification_version(args.input, sheet),
        "aicm_version": aicm_version,
        "generated_at": "2026-06-18",
        "source_file": os.path.basename(args.input),
        "questions": questions,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2, ensure_ascii=False)

    controls = len({q["aicm_control_id"] for q in questions})
    print(f"Wrote {len(questions)} questions across {controls} controls to {args.output}")


if __name__ == "__main__":
    main()
