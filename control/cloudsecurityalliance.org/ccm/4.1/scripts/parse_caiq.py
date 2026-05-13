#!/usr/bin/env python3
"""Parse CAIQv4.1.0 Excel file into JSON with questions and full CCM control data."""

import json
import os
import re
import sys
import pandas as pd
import numpy as np

XLSX_DIR = os.path.join(os.path.dirname(__file__), "..", "..",
    "CCM+CAIQv4.1 Bundle")
CAIQ_XLSX = os.path.join(XLSX_DIR,
    "CAIQv4.1.0-star_security_questionnaire-generated_at_2026_01_13.xlsx")
CCM_JSON = os.path.join(os.path.dirname(__file__), "..", "CCMv4.1.0.json")
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "CAIQv4.1.0.json")

QID_PATTERN = re.compile(r'^[A-Z&]{2,4}-\d+\.\d+$')


def clean(val):
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str):
        return val.strip()
    return val


def load_ccm_controls():
    with open(CCM_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["control_id"]: c for c in data["controls"]}


def parse_caiq():
    df = pd.read_excel(CAIQ_XLSX, sheet_name="CAIQv4.1.0", header=None, skiprows=1)
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
    questions = parse_caiq()

    if not os.path.exists(CCM_JSON):
        print(f"Error: {CCM_JSON} not found. Run parse_ccm.py first.")
        sys.exit(1)

    controls_index = load_ccm_controls()
    questions = enrich_with_ccm(questions, controls_index)

    output = {
        "specification_name": "Consensus Assessments Initiative Questionnaire",
        "caiq_version": "4.1.0",
        "ccm_version": "4.1.0",
        "generated_at": "2026-01-13",
        "questions": questions,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(questions)} questions to {OUTPUT}")


if __name__ == "__main__":
    main()
