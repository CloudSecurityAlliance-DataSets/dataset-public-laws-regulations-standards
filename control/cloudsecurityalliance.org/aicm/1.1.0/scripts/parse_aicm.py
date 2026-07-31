#!/usr/bin/env python3
"""Parse the AICM v1.1.0 workbook into a single JSON with controls and all associated data.

Updated from the v1.0.3 parser (../../1.0.3/scripts/parse_aicm.py). Changes:

  * NIST AI 600-1:2024 mappings are gone. The Scope Applicability sheet dropped
    from 16 columns to 13 and now carries only BSI AI C4, the EU AI Act, and
    ISO/IEC 42001:2023. Rather than hardcode three frameworks and break again on
    the next release, the mapping columns are discovered from the sheet's group
    header row and checked against EXPECTED_FRAMEWORKS. A layout change is
    reported instead of silently producing a short record.
  * The ownership column formerly labelled "Gen AI Ops/Processing Infrastructure"
    is now "Cloud/AI Processing Infrastructure (PI)". The JSON key follows the
    source: cloud_ai_processing_infrastructure (was
    gen_ai_ops_processing_infrastructure in the 1.0.3 output).
  * The LLM Taxonomy sheet is read in full. The 1.0.3 parser emitted only the
    lifecycle section and silently dropped the Control Type, Control Ownership,
    Threat Category, and (new in 1.1.0) Other Definitions sections.
  * Version is read from the JSON stamp in cell A1 rather than hardcoded.
  * Paths come from the command line instead of a hardcoded bundle directory.

Source spreadsheets are gitignored. Pull from
s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/aicm/1.1.0/

Usage:
    ./parse_aicm.py --input AICMv1.1.0-generated_at_2026_06_18.xlsx
    ./parse_aicm.py --input <xlsx> --output ../aicm-1.1.0.json
"""

import argparse
import json
import os
import re
import sys

import numpy as np
import pandas as pd

DEFAULT_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "aicm-1.1.0.json")

# Mapping frameworks expected in the Scope Applicability sheet. Discovery below
# compares against this; a mismatch is a hard error, not a silent short record.
# NIST AI 600-1:2024 was present in v1.0.3 and dropped in v1.1.0.
EXPECTED_FRAMEWORKS = ["BSI AI C4", "EU AI Act", "ISO/IEC 42001:2023"]

# Each framework occupies three consecutive columns under its merged header.
FRAMEWORK_COLUMN_SPAN = 3

# GRC-01 through GRC-08 name the CSP owner without the "Owned by the" prefix that
# the other 239 controls use. Same meaning, inconsistent phrasing in the source.
# Normalized so the ownership vocabulary is a closed set; every substitution is
# recorded in source_data_notes.normalizations_applied.
OWNERSHIP_NORMALIZATIONS = {
    "Cloud Service Provider (CSP)": "Owned by the Cloud Service Provider (CSP)",
}

# Sheets whose first three rows are: version stamp, group headers, column headers.
GROUPED_HEADER_SKIP = 2
# Sheets whose first two rows are: version stamp, column headers.
FLAT_HEADER_SKIP = 1


def clean(val):
    """NaN -> None, strings stripped. Everything else passes through."""
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str):
        return val.strip()
    return val


def parse_bool_or_text(val):
    """The relevance grids hold TRUE/FALSE, but occasionally free text. Keep both."""
    if isinstance(val, bool):
        return val
    if isinstance(val, float) and np.isnan(val):
        return False
    if isinstance(val, str):
        lowered = val.strip().lower()
        if lowered == "true":
            return True
        if lowered in ("false", ""):
            return False
        return val.strip()
    return val


def normalize_ownership(value, control_id, field, log):
    """Apply OWNERSHIP_NORMALIZATIONS, recording every substitution made."""
    replacement = OWNERSHIP_NORMALIZATIONS.get(value)
    if replacement is None:
        return value
    log.append({"control_id": control_id, "field": field, "from": value, "to": replacement})
    return replacement


def slugify(name):
    """'ISO/IEC 42001:2023' -> 'iso_iec_42001_2023'"""
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", name.lower())).strip("_")


def read_sheet(xlsx, sheet_name, skiprows=GROUPED_HEADER_SKIP):
    """Return data rows only, with the column-header row consumed."""
    df = pd.read_excel(xlsx, sheet_name=sheet_name, header=None, skiprows=skiprows)
    return df.iloc[1:]


def read_specification_version(xlsx):
    """Cell A1 of every sheet carries {"specification_name":...,"specification_version":...}."""
    a1 = pd.read_excel(xlsx, sheet_name="AICM", header=None, nrows=1).iloc[0, 0]
    try:
        return json.loads(a1)["specification_version"]
    except (TypeError, ValueError, KeyError):
        print(f"warning: could not read version stamp from cell A1 ({a1!r})", file=sys.stderr)
        return None


def parse_controls(xlsx, normalization_log):
    """Parse the main AICM sheet. Rows carrying a domain but no Control ID are separators."""
    controls = []
    current_domain = None
    ownership_columns = {
        "cloud_ai_processing_infrastructure": 5,
        "model": 6,
        "orchestrated_services": 7,
        "application": 8,
    }

    for _, row in read_sheet(xlsx, "AICM").iterrows():
        control_id = clean(row[2])
        domain = clean(row[0])

        if domain:
            current_domain = domain
        if control_id is None:
            continue

        ownership = {
            field: normalize_ownership(clean(row[column]), control_id, field, normalization_log)
            for field, column in ownership_columns.items()
        }

        controls.append({
            "control_domain": current_domain,
            "control_title": clean(row[1]),
            "control_id": control_id,
            "control_specification": clean(row[3]),
            "control_type": clean(row[4]),
            "typical_control_applicability_and_ownership": ownership,
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
        })

    return controls


def parse_implementation_guidelines(xlsx):
    guidelines = {}
    for _, row in read_sheet(xlsx, "Implementation Guidelines").iterrows():
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


def parse_auditing_guidelines(xlsx):
    guidelines = {}
    for _, row in read_sheet(xlsx, "Auditing Guidelines", FLAT_HEADER_SKIP).iterrows():
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


def discover_mapping_frameworks(xlsx):
    """Read framework names and their start columns from the sheet's group header row.

    Row 1 holds merged cells naming each framework above its Control Mapping /
    Gap Level / Addendum triple. Returns [(name, first_column), ...] left to right.
    """
    header = pd.read_excel(
        xlsx, sheet_name="Scope Applicability (Mappings)", header=None,
        skiprows=1, nrows=1,
    ).iloc[0]

    frameworks = [
        (value.strip(), column)
        for column, value in enumerate(header)
        if isinstance(value, str) and value.strip()
    ]

    found = [name for name, _ in frameworks]
    if found != EXPECTED_FRAMEWORKS:
        print(
            "error: mapping frameworks in the workbook do not match expectations.\n"
            f"  expected: {EXPECTED_FRAMEWORKS}\n"
            f"  found:    {found}\n"
            "The publisher changed the mappings layout. Confirm whether a framework was\n"
            "added or withdrawn, update EXPECTED_FRAMEWORKS, and note it in the metadata's\n"
            "open_questions before re-running. Refusing to emit a partial mapping set.",
            file=sys.stderr,
        )
        sys.exit(1)

    return frameworks


def parse_scope_applicability_mappings(xlsx):
    frameworks = discover_mapping_frameworks(xlsx)
    mappings = {}

    for _, row in read_sheet(xlsx, "Scope Applicability (Mappings)").iterrows():
        control_id = clean(row[2])
        if control_id is None:
            continue
        mappings[control_id] = {
            slugify(name): {
                "control_mapping": clean(row[start]),
                "gap_level": clean(row[start + 1]),
                "addendum": clean(row[start + 2]),
            }
            for name, start in frameworks
        }

    return mappings


def parse_caiq_questions(xlsx):
    """Parse the AI-CAIQ tab embedded in the AICM workbook, grouped by control_id."""
    questions = {}
    current_control_id = None

    for _, row in read_sheet(xlsx, "AI-CAIQ", FLAT_HEADER_SKIP).iterrows():
        control_id = clean(row[2])
        if control_id:
            current_control_id = control_id

        question_id = clean(row[4])
        if question_id is None or current_control_id is None:
            continue

        questions.setdefault(current_control_id, []).append({
            "question_id": question_id,
            "question": clean(row[5]),
        })

    return questions


def parse_llm_taxonomy(xlsx):
    """Parse every section of the LLM Taxonomy sheet.

    The sheet stacks four differently-shaped sections under one tab:

      Lifecycle          two-level — a lifecycle phase in col 0 spanning
                         several L2 entries in col 2
      Control Type       flat term/definition pairs in cols 0-1
      Control Ownership  flat term/definition pairs
      Threat Category    flat term/definition pairs
      Other Definitions  flat term/definition pairs (new in v1.1.0)

    A section starts at a row with a value in col 0 and nothing in cols 1-3.
    The 1.0.3 parser only emitted the lifecycle rows.
    """
    df = pd.read_excel(xlsx, sheet_name="LLM Taxonomy", header=None, skiprows=GROUPED_HEADER_SKIP)
    df = df.iloc[1:]

    lifecycle = []
    definitions = {}
    section = "Lifecycle"
    current_phase = None
    current_phase_description = None

    for _, row in df.iterrows():
        col0, col1, col2, col3 = (clean(row[i]) for i in range(4))

        if col0 and not col1 and not col2 and not col3:
            if col0.lower().startswith(("end of", "©", "copyright")):
                break
            section = col0
            current_phase = None
            continue

        if section == "Lifecycle":
            if col0:
                current_phase, current_phase_description = col0, col1
            if col2:
                lifecycle.append({
                    "lifecycle": current_phase,
                    "lifecycle_description": current_phase_description,
                    "lifecycle_l2": col2,
                    "lifecycle_l2_description": col3,
                })
        elif col0:
            definitions.setdefault(slugify(section), []).append({
                "term": col0,
                "definition": col1,
            })

    return lifecycle, definitions


def find_source_gaps(controls):
    """Locate cells the publisher left empty.

    These are absences in CSA's workbook, not extraction failures. Recording them
    explicitly — rather than letting a null read as a parser bug — means a
    consumer can tell "the publisher did not state this" from "we lost it".
    Computed from the parsed data on every run, so the record cannot go stale.
    """
    gaps = []

    ownership = [
        {"control_id": c["control_id"], "field": field}
        for c in controls
        for field, value in c["typical_control_applicability_and_ownership"].items()
        if value is None
    ]
    if ownership:
        gaps.append({
            "field": "typical_control_applicability_and_ownership",
            "affected_cells": ownership,
            "control_ids": sorted({g["control_id"] for g in ownership}),
            "note": (
                "These ownership cells are empty in the publisher's workbook. "
                "The values are absent at source, not lost in conversion; they are "
                "emitted as null to preserve that distinction."
            ),
        })

    for framework in EXPECTED_FRAMEWORKS:
        key = slugify(framework)
        missing = sorted(
            c["control_id"] for c in controls
            if c.get("scope_applicability_mappings")
            and not c["scope_applicability_mappings"][key]["control_mapping"]
        )
        if missing:
            gaps.append({
                "field": f"scope_applicability_mappings.{key}.control_mapping",
                "control_ids": missing,
                "note": (
                    f"No {framework} mapping is stated for these controls in the "
                    "publisher's workbook. The mapping is absent at source, not "
                    "lost in conversion."
                ),
            })

    return gaps


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", required=True, help="AICM v1.1.0 .xlsx")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="Destination JSON (default: %(default)s)")
    args = ap.parse_args()

    xlsx = args.input
    normalizations = []
    controls = parse_controls(xlsx, normalizations)
    implementation = parse_implementation_guidelines(xlsx)
    auditing = parse_auditing_guidelines(xlsx)
    mappings = parse_scope_applicability_mappings(xlsx)
    caiq = parse_caiq_questions(xlsx)
    lifecycle, definitions = parse_llm_taxonomy(xlsx)

    for control in controls:
        cid = control["control_id"]
        control["implementation_guidelines"] = implementation.get(cid)
        control["auditing_guidelines"] = auditing.get(cid)
        control["scope_applicability_mappings"] = mappings.get(cid)
        control["caiq_questions"] = caiq.get(cid, [])

    missing = {
        "implementation_guidelines": [c["control_id"] for c in controls if not c["implementation_guidelines"]],
        "auditing_guidelines": [c["control_id"] for c in controls if not c["auditing_guidelines"]],
        "scope_applicability_mappings": [c["control_id"] for c in controls if not c["scope_applicability_mappings"]],
        "caiq_questions": [c["control_id"] for c in controls if not c["caiq_questions"]],
    }
    for field, ids in missing.items():
        if ids:
            print(f"warning: {len(ids)} controls missing {field}: {ids[:8]}", file=sys.stderr)

    grouped_normalizations = []
    for original, replacement in OWNERSHIP_NORMALIZATIONS.items():
        applied = [n for n in normalizations if n["from"] == original]
        if applied:
            grouped_normalizations.append({
                "field": "typical_control_applicability_and_ownership",
                "from": original,
                "to": replacement,
                "control_ids": sorted({n["control_id"] for n in applied}),
                "cells_changed": len(applied),
                "reason": (
                    "The publisher's workbook states this owner without the "
                    "'Owned by the' prefix used by every other control. Normalized "
                    "so the ownership vocabulary is a closed set. Meaning is unchanged."
                ),
            })

    output = {
        "specification_name": "AI Controls Matrix",
        "specification_version": read_specification_version(xlsx),
        "published": "2026-06-22",
        "generated_at": "2026-06-18",
        "source_file": os.path.basename(xlsx),
        "mapping_frameworks": EXPECTED_FRAMEWORKS,
        "source_data_notes": {
            "normalizations_applied": grouped_normalizations,
            "gaps_in_source": find_source_gaps(controls),
        },
        "controls": controls,
        "llm_taxonomy": lifecycle,
        "definitions": definitions,
    }

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2, ensure_ascii=False)

    questions = sum(len(c["caiq_questions"]) for c in controls)
    domains = len({c["control_domain"] for c in controls})
    print(f"Wrote {len(controls)} controls across {domains} domains to {args.output}")
    print(f"  AI-CAIQ questions:   {questions}")
    print(f"  lifecycle entries:   {len(lifecycle)}")
    print(f"  definition sections: {', '.join(f'{k} ({len(v)})' for k, v in definitions.items())}")
    for entry in grouped_normalizations:
        print(f"  normalized {entry['cells_changed']} cells: {entry['from']!r} -> {entry['to']!r} "
              f"({', '.join(entry['control_ids'])})")
    for gap in output["source_data_notes"]["gaps_in_source"]:
        print(f"  source gap in {gap['field']}: {', '.join(gap['control_ids'])}")


if __name__ == "__main__":
    main()
