#!/usr/bin/env python3
"""Parse AICMv1.0.3 Excel file into a single JSON with controls and all associated data."""

import json
import sys
import os
import pandas as pd
import numpy as np

XLSX_DIR = os.path.join(os.path.dirname(__file__), "..",
    "AICMv1.0.3+AI_CAIQv1.0.2-spreadsheet_bundle-generated_at_2025_11_10")
AICM_XLSX = os.path.join(XLSX_DIR, "AICMv1.0.3-generated_at_2025_11_10.xlsx")
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "AICMv1.0.3.json")


def clean(val):
    """Convert NaN to None and strip strings."""
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str):
        return val.strip()
    if isinstance(val, bool):
        return val
    return val


def parse_bool_or_text(val):
    """Parse True/False booleans or text values from cells."""
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
    """Read a sheet, skipping metadata/header rows, and drop domain-header rows (no Control ID)."""
    df = pd.read_excel(AICM_XLSX, sheet_name=sheet_name, header=None, skiprows=skip_rows)
    # Row 0 after skip is the column header row
    headers = df.iloc[0].tolist()
    df = df.iloc[1:]  # actual data
    df.columns = range(len(headers))
    return df, headers


def parse_aicm_controls():
    """Parse the main AICM sheet."""
    df, _ = read_sheet("AICM")

    controls = []
    current_domain = None

    for _, row in df.iterrows():
        control_id = clean(row[2])
        domain_raw = clean(row[0])

        # Domain header row (no control ID)
        if control_id is None:
            if domain_raw:
                current_domain = domain_raw
            continue

        # Update domain from non-null values
        if domain_raw:
            current_domain = domain_raw

        control = {
            "control_domain": current_domain,
            "control_title": clean(row[1]),
            "control_id": control_id,
            "control_specification": clean(row[3]),
            "control_type": clean(row[4]),
            "typical_control_applicability_and_ownership": {
                "gen_ai_ops_processing_infrastructure": clean(row[5]),
                "model": clean(row[6]),
                "orchestrated_services": clean(row[7]),
                "application": clean(row[8]),
            },
            "architectural_relevance_ai_stack_components": {
                "physical": parse_bool_or_text(row[9]),
                "network": parse_bool_or_text(row[10]),
                "compute": parse_bool_or_text(row[11]),
                "storage": parse_bool_or_text(row[12]),
                "app": parse_bool_or_text(row[13]),
                "data": parse_bool_or_text(row[14]),
            },
            "lifecycle_relevance": {
                "preparation": clean(row[15]),
                "development": clean(row[16]),
                "evaluation_validation": clean(row[17]),
                "deployment": clean(row[18]),
                "delivery": clean(row[19]),
                "service_retirement": clean(row[20]),
            },
            "threat_category": {
                "model_manipulation": parse_bool_or_text(row[21]),
                "data_poisoning": parse_bool_or_text(row[22]),
                "sensitive_data_disclosure": parse_bool_or_text(row[23]),
                "model_theft": parse_bool_or_text(row[24]),
                "model_service_failure_malfunctioning": parse_bool_or_text(row[25]),
                "insecure_supply_chain": parse_bool_or_text(row[26]),
                "insecure_apps_plugins": parse_bool_or_text(row[27]),
                "denial_of_service": parse_bool_or_text(row[28]),
                "loss_of_governance_compliance": parse_bool_or_text(row[29]),
            },
        }
        controls.append(control)

    return controls


def parse_implementation_guidelines():
    """Parse Implementation Guidelines sheet, keyed by control_id."""
    df, _ = read_sheet("Implementation Guidelines")
    guidelines = {}

    for _, row in df.iterrows():
        control_id = clean(row[2])
        if control_id is None:
            continue
        guidelines[control_id] = {
            "shared": clean(row[4]),
            "model_provider": clean(row[5]),
            "orchestrated_service_provider": clean(row[6]),
            "application_provider": clean(row[7]),
            "ai_customer": clean(row[8]),
            "cloud_service_provider": clean(row[9]),
        }

    return guidelines


def parse_auditing_guidelines():
    """Parse Auditing Guidelines sheet, keyed by control_id."""
    df = pd.read_excel(AICM_XLSX, sheet_name="Auditing Guidelines", header=None, skiprows=1)
    # Header row is at index 0 after skip
    df = df.iloc[1:]  # skip the header row
    guidelines = {}

    for _, row in df.iterrows():
        control_id = clean(row[2])
        if control_id is None:
            continue
        guidelines[control_id] = {
            "application_provider": clean(row[4]),
            "orchestrated_service_provider": clean(row[5]),
            "model_provider": clean(row[6]),
            "ai_customer": clean(row[7]),
            "cloud_service_provider": clean(row[8]),
        }

    return guidelines


def parse_scope_applicability_mappings():
    """Parse Scope Applicability (Mappings) sheet, keyed by control_id."""
    df, _ = read_sheet("Scope Applicability (Mappings)")
    mappings = {}

    for _, row in df.iterrows():
        control_id = clean(row[2])
        if control_id is None:
            continue
        mappings[control_id] = {
            "bsi_ai_c4": {
                "control_mapping": clean(row[4]),
                "gap_level": clean(row[5]),
                "addendum": clean(row[6]),
            },
            "eu_ai_act": {
                "control_mapping": clean(row[7]),
                "gap_level": clean(row[8]),
                "addendum": clean(row[9]),
            },
            "iso_iec_42001_2023": {
                "control_mapping": clean(row[10]),
                "gap_level": clean(row[11]),
                "addendum": clean(row[12]),
            },
            "nist_ai_600_1_2024": {
                "control_mapping": clean(row[13]),
                "gap_level": clean(row[14]),
                "addendum": clean(row[15]),
            },
        }

    return mappings


def parse_caiq_questions():
    """Parse AI-CAIQ sheet from the AICM file, returning questions grouped by control_id."""
    df = pd.read_excel(AICM_XLSX, sheet_name="AI-CAIQ", header=None, skiprows=1)
    df = df.iloc[1:]  # skip header row
    questions = {}
    current_domain = None

    for _, row in df.iterrows():
        question_id = clean(row[4])
        domain_raw = clean(row[0])
        control_id = clean(row[2])

        # Domain header row
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
        })

    return questions


def parse_llm_taxonomy():
    """Parse LLM Taxonomy sheet."""
    df = pd.read_excel(AICM_XLSX, sheet_name="LLM Taxonomy", header=None, skiprows=2)
    df = df.iloc[1:]  # skip header row
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
    controls = parse_aicm_controls()
    impl_guidelines = parse_implementation_guidelines()
    audit_guidelines = parse_auditing_guidelines()
    mappings = parse_scope_applicability_mappings()
    caiq_questions = parse_caiq_questions()
    llm_taxonomy = parse_llm_taxonomy()

    # Merge everything into controls
    for control in controls:
        cid = control["control_id"]
        control["implementation_guidelines"] = impl_guidelines.get(cid)
        control["auditing_guidelines"] = audit_guidelines.get(cid)
        control["scope_applicability_mappings"] = mappings.get(cid)
        control["caiq_questions"] = caiq_questions.get(cid, [])

    output = {
        "specification_name": "AI Controls Matrix",
        "specification_version": "1.0.3",
        "generated_at": "2025-11-10",
        "controls": controls,
        "llm_taxonomy": llm_taxonomy,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(controls)} controls to {OUTPUT}")


if __name__ == "__main__":
    main()
