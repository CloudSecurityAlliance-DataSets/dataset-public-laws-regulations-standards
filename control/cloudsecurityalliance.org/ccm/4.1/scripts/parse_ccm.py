#!/usr/bin/env python3
"""Parse CCMv4.1.0 Excel file into a single JSON with controls and all associated data."""

import json
import sys
import os
import pandas as pd
import numpy as np

XLSX_DIR = os.path.join(os.path.dirname(__file__), "..", "..",
    "CCM+CAIQv4.1 Bundle")
CCM_XLSX = os.path.join(XLSX_DIR, "CCMv4.1.0-generated_at_2026_01_13.xlsx")
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "CCMv4.1.0.json")


def clean(val):
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str):
        return val.strip()
    if isinstance(val, bool):
        return val
    return val


def parse_bool_or_text(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, float) and np.isnan(val):
        return False
    if isinstance(val, str):
        v = val.strip().lower()
        if v == "true":
            return True
        if v == "false" or v == "":
            return False
        return val.strip()
    return val


def read_sheet(sheet_name, skip_rows=2):
    df = pd.read_excel(CCM_XLSX, sheet_name=sheet_name, header=None, skiprows=skip_rows)
    df = df.iloc[1:]  # skip column header row
    df.columns = range(df.shape[1])
    return df


def parse_ccm_controls():
    """Parse the main CCM sheet (23 columns)."""
    df = read_sheet("CCM")
    controls = []
    current_domain = None

    for _, row in df.iterrows():
        control_id = clean(row[2])
        domain_raw = clean(row[0])

        if control_id is None:
            if domain_raw:
                current_domain = domain_raw
            continue

        if domain_raw:
            current_domain = domain_raw

        control = {
            "control_domain": current_domain,
            "control_title": clean(row[1]),
            "control_id": control_id,
            "control_specification": clean(row[3]),
            "ccm_lite": clean(row[4]),
            "typical_control_applicability_and_ownership": {
                "iaas": clean(row[5]),
                "paas": clean(row[6]),
                "saas": clean(row[7]),
            },
            "architectural_relevance_cloud_stack_components": {
                "physical": parse_bool_or_text(row[8]),
                "network": parse_bool_or_text(row[9]),
                "compute": parse_bool_or_text(row[10]),
                "storage": parse_bool_or_text(row[11]),
                "app": parse_bool_or_text(row[12]),
                "data": parse_bool_or_text(row[13]),
            },
            "organizational_relevance": {
                "cybersecurity": parse_bool_or_text(row[14]),
                "internal_audit": parse_bool_or_text(row[15]),
                "architecture_team": parse_bool_or_text(row[16]),
                "sw_development": parse_bool_or_text(row[17]),
                "operations": parse_bool_or_text(row[18]),
                "legal_privacy": parse_bool_or_text(row[19]),
                "grc_team": parse_bool_or_text(row[20]),
                "supply_chain_management": parse_bool_or_text(row[21]),
                "hr": parse_bool_or_text(row[22]),
            },
        }
        controls.append(control)

    return controls


def parse_implementation_guidelines():
    """Parse Implementation Guidelines sheet (9 columns including ownership)."""
    df = read_sheet("Implementation Guidelines")
    guidelines = {}

    for _, row in df.iterrows():
        control_id = clean(row[2])
        if control_id is None:
            continue
        guidelines[control_id] = {
            "typical_control_applicability_and_ownership": {
                "iaas": clean(row[4]),
                "paas": clean(row[5]),
                "saas": clean(row[6]),
            },
            "csp": clean(row[7]),
            "csc": clean(row[8]),
        }

    return guidelines


def parse_auditing_guidelines():
    """Parse Auditing Guidelines sheet (5 columns, single guidelines column)."""
    df = pd.read_excel(CCM_XLSX, sheet_name="Auditing Guidelines", header=None, skiprows=1)
    df = df.iloc[1:]
    guidelines = {}

    for _, row in df.iterrows():
        control_id = clean(row[2])
        if control_id is None:
            continue
        guidelines[control_id] = clean(row[4])

    return guidelines


def parse_caiq_questions():
    """Parse CAIQ sheet from the CCM file, returning questions grouped by control_id."""
    df = pd.read_excel(CCM_XLSX, sheet_name="CAIQ", header=None, skiprows=1)
    df = df.iloc[1:]  # skip header row
    questions = {}
    current_domain = None
    current_control_id = None

    for _, row in df.iterrows():
        question_id = clean(row[4])
        domain_raw = clean(row[0])
        control_id = clean(row[2])

        if question_id is None and control_id is None:
            if domain_raw:
                current_domain = domain_raw
            continue

        if domain_raw:
            current_domain = domain_raw
        if control_id:
            current_control_id = control_id
        if question_id is None:
            continue

        if current_control_id not in questions:
            questions[current_control_id] = []
        questions[current_control_id].append({
            "question_id": question_id,
            "question": clean(row[5]),
            "caiq_lite": clean(row[6]),
        })

    return questions


def main():
    controls = parse_ccm_controls()
    impl_guidelines = parse_implementation_guidelines()
    audit_guidelines = parse_auditing_guidelines()
    caiq_questions = parse_caiq_questions()

    for control in controls:
        cid = control["control_id"]
        control["implementation_guidelines"] = impl_guidelines.get(cid)
        control["auditing_guidelines"] = audit_guidelines.get(cid)
        control["caiq_questions"] = caiq_questions.get(cid, [])

    output = {
        "specification_name": "Cloud Controls Matrix",
        "specification_version": "4.1.0",
        "generated_at": "2026-01-13",
        "controls": controls,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(controls)} controls to {OUTPUT}")


if __name__ == "__main__":
    main()
