#!/usr/bin/env python3
"""Parse the CAIQ v4.1.0 workbook into JSON with questions and full CCM control data.

CSA has issued two different workbooks under the same CAIQ 4.1.0 label:

  CAIQv4.1.0-star_security_questionnaire-generated_at_2026_01_13.xlsx  (A1 records CCM 4.1.0)
  CAIQv4.1.0-star_security_questionnaire-generated_at_2026_10_02.xlsx  (A1 records CCM 4.1.1)

26 question texts differ between them. ../ccm-caiq-4.1.0.json is extracted
from the 2026-10-02 generation, the one CSA serves now, and enriched from the
CCM 4.1.1 controls it records in cell A1. See ../README.md.

The script refuses a workbook whose cell A1 does not stamp caiq_version 4.1.0
and the CCM version given by --expect-ccm-version (default 4.1.1).

Source spreadsheets are gitignored. Pull from
s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/ccm-caiq/4.1.0/

Usage:
    ./parse_caiq.py --input ../CAIQv4.1.0-star_security_questionnaire-generated_at_2026_10_02.xlsx
"""

import argparse
import json
import os
import re
import sys
import pandas as pd
import numpy as np

HERE = os.path.dirname(__file__)
DEFAULT_CCM_JSON = os.path.join(HERE, "..", "..", "..", "ccm", "4.1.1", "ccm-4.1.1.json")
DEFAULT_OUTPUT = os.path.join(HERE, "..", "ccm-caiq-4.1.0.json")

EXPECTED_CAIQ_VERSION = "4.1.0"
QID_PATTERN = re.compile(r'^[A-Z&]{2,4}-\d+\.\d+$')


def clean(val):
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str):
        return val.strip()
    return val


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def read_stamp(xlsx):
    """Cell A1: {"specification_name":...,"specification_version":...,"caiq_version":...}."""
    a1 = pd.read_excel(xlsx, sheet_name=0, header=None, nrows=1).iloc[0, 0]
    try:
        stamp = json.loads(a1)
        return stamp["caiq_version"], stamp["specification_version"]
    except (TypeError, ValueError, KeyError):
        fail(f"could not read the version stamp from cell A1 ({a1!r})")


def generated_at(xlsx):
    """'…-generated_at_2026_10_02.xlsx' -> '2026-10-02'."""
    m = re.search(r"generated_at_(\d{4})_(\d{2})_(\d{2})", os.path.basename(xlsx))
    return "-".join(m.groups()) if m else None


def load_ccm_controls(ccm_json):
    with open(ccm_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["control_id"]: c for c in data["controls"]}


def parse_caiq(xlsx, sheet_name):
    df = pd.read_excel(xlsx, sheet_name=sheet_name, header=None, skiprows=1)
    df = df.iloc[1:]  # skip header row

    questions = []
    current_control_id = None
    current_control_spec = None
    current_control_title = None
    current_domain_title = None

    for _, row in df.iterrows():
        question_id = clean(row[0])
        if question_id is None:
            continue
        if not QID_PATTERN.match(question_id):
            continue

        cid = clean(row[8])
        if cid:
            current_control_id = cid
        spec = clean(row[9])
        if spec:
            current_control_spec = spec
        title = clean(row[10])
        if title:
            current_control_title = title
        domain = clean(row[11])
        if domain:
            current_domain_title = domain

        questions.append({
            "question_id": question_id,
            "question": clean(row[1]),
            "ccm_control_id": current_control_id,
            "ccm_control_specification": current_control_spec,
            "ccm_control_title": current_control_title,
            "ccm_domain_title": current_domain_title,
        })

    return questions


def enrich_with_ccm(questions, controls_index):
    for q in questions:
        cid = q["ccm_control_id"]
        control = controls_index.get(cid)
        if control:
            q["ccm_control"] = {
                "control_domain": control["control_domain"],
                "control_title": control["control_title"],
                "control_id": control["control_id"],
                "control_specification": control["control_specification"],
                "ccm_lite": control["ccm_lite"],
                "typical_control_applicability_and_ownership": control["typical_control_applicability_and_ownership"],
                "architectural_relevance_cloud_stack_components": control["architectural_relevance_cloud_stack_components"],
                "organizational_relevance": control["organizational_relevance"],
                "implementation_guidelines": control["implementation_guidelines"],
                "auditing_guidelines": control["auditing_guidelines"],
            }
        else:
            q["ccm_control"] = None

    return questions


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", required=True, help="CAIQ v4.1.0 .xlsx")
    ap.add_argument("--ccm-json", default=DEFAULT_CCM_JSON,
                    help="CCM extraction to embed control data from (default: %(default)s)")
    ap.add_argument("--expect-ccm-version", default="4.1.1",
                    help="CCM version the workbook's cell A1 must record (default: %(default)s)")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="Destination JSON (default: %(default)s)")
    args = ap.parse_args()

    caiq_version, ccm_version = read_stamp(args.input)
    if caiq_version != EXPECTED_CAIQ_VERSION or ccm_version != args.expect_ccm_version:
        fail(f"cell A1 stamps caiq_version {caiq_version!r} / CCM {ccm_version!r}; expected "
             f"{EXPECTED_CAIQ_VERSION!r} / {args.expect_ccm_version!r}.")

    if not os.path.exists(args.ccm_json):
        fail(f"{args.ccm_json} not found. Run the CCM parser first.")
    controls_index = load_ccm_controls(args.ccm_json)

    questions = enrich_with_ccm(parse_caiq(args.input, f"CAIQv{caiq_version}"), controls_index)
    unmatched = sorted({q["ccm_control_id"] for q in questions if q["ccm_control"] is None})
    if unmatched:
        print(f"warning: no CCM control found for {unmatched}", file=sys.stderr)

    output = {
        "specification_name": "Consensus Assessments Initiative Questionnaire",
        "caiq_version": caiq_version,
        "ccm_version": ccm_version,
        "generated_at": generated_at(args.input),
        "source_workbook": os.path.basename(args.input),
        "questions": questions,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(questions)} questions to {args.output}")


if __name__ == "__main__":
    main()
