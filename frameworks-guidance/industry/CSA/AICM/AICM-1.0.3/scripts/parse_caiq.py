#!/usr/bin/env python3
"""Parse AI-CAIQv1.0.2 Excel file into JSON with questions and full AICM control data."""

import json
import os
import sys
import pandas as pd
import numpy as np

XLSX_DIR = os.path.join(os.path.dirname(__file__), "..",
    "AICMv1.0.3+AI_CAIQv1.0.2-spreadsheet_bundle-generated_at_2025_11_10")
CAIQ_XLSX = os.path.join(XLSX_DIR,
    "AI_CAIQv1.0.2-star_security_questionnaire-generated_at_2025_11_10.xlsx")
AICM_JSON = os.path.join(os.path.dirname(__file__), "..", "AICMv1.0.3.json")
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "AI-CAIQv1.0.2.json")


def clean(val):
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str):
        return val.strip()
    return val


def load_aicm_controls():
    """Load the AICM JSON (must be generated first) and index by control_id."""
    with open(AICM_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["control_id"]: c for c in data["controls"]}


def parse_caiq():
    """Parse the standalone AI-CAIQ questionnaire file."""
    df = pd.read_excel(CAIQ_XLSX, sheet_name="AI-CAIQv1.0.2", header=None, skiprows=1)
    # Row 0 after skip is headers
    df = df.iloc[1:]

    questions = []
    current_control_id = None
    current_control_spec = None
    current_control_title = None
    current_domain_title = None

    import re
    # Valid question IDs match pattern like A&A-01.1, AIS-02.3, etc.
    qid_pattern = re.compile(r'^[A-Z&]{2,4}-\d+\.\d+$')

    for _, row in df.iterrows():
        question_id = clean(row[0])
        if question_id is None:
            continue
        if not qid_pattern.match(question_id):
            continue

        # Forward-fill AICM reference columns (only first question row per control has values)
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
            "aicm_control_id": current_control_id,
            "aicm_control_specification": current_control_spec,
            "aicm_control_title": current_control_title,
            "aicm_domain_title": current_domain_title,
        })

    return questions


def enrich_with_aicm(questions, controls_index):
    """Add full AICM control data to each question entry."""
    for q in questions:
        cid = q["aicm_control_id"]
        control = controls_index.get(cid)
        if control:
            q["aicm_control"] = {
                "control_domain": control["control_domain"],
                "control_title": control["control_title"],
                "control_id": control["control_id"],
                "control_specification": control["control_specification"],
                "control_type": control["control_type"],
                "typical_control_applicability_and_ownership": control["typical_control_applicability_and_ownership"],
                "architectural_relevance_ai_stack_components": control["architectural_relevance_ai_stack_components"],
                "lifecycle_relevance": control["lifecycle_relevance"],
                "threat_category": control["threat_category"],
                "implementation_guidelines": control["implementation_guidelines"],
                "auditing_guidelines": control["auditing_guidelines"],
                "scope_applicability_mappings": control["scope_applicability_mappings"],
            }
        else:
            q["aicm_control"] = None

    return questions


def parse_llm_taxonomy():
    """Parse LLM Taxonomy from the CAIQ file."""
    df = pd.read_excel(CAIQ_XLSX, sheet_name="LLM Taxonomy", header=None, skiprows=2)
    df = df.iloc[1:]
    taxonomy = []
    current_lifecycle = None
    current_description = None

    for _, row in df.iterrows():
        lifecycle = clean(row[0])
        lifecycle_desc = clean(row[1])
        l2 = clean(row[2])
        l2_desc = clean(row[3])

        if lifecycle:
            current_lifecycle = lifecycle
            current_description = lifecycle_desc

        if l2:
            taxonomy.append({
                "lifecycle": current_lifecycle,
                "lifecycle_description": current_description,
                "lifecycle_l2": l2,
                "lifecycle_l2_description": l2_desc,
            })

    return taxonomy


def main():
    # Parse CAIQ questions
    questions = parse_caiq()

    # Load AICM controls and enrich
    if not os.path.exists(AICM_JSON):
        print(f"Error: {AICM_JSON} not found. Run parse_aicm.py first.")
        sys.exit(1)

    controls_index = load_aicm_controls()
    questions = enrich_with_aicm(questions, controls_index)
    llm_taxonomy = parse_llm_taxonomy()

    output = {
        "specification_name": "AI Consensus Assessments Initiative Questionnaire",
        "caiq_version": "1.0.2",
        "aicm_version": "1.0.3",
        "generated_at": "2025-11-10",
        "questions": questions,
        "llm_taxonomy": llm_taxonomy,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(questions)} questions to {OUTPUT}")


if __name__ == "__main__":
    main()
