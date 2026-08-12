#!/usr/bin/env python3
"""Parse the AICM v1.1.1 workbook into a single JSON with controls and all associated data.

Updated from the v1.1.0 parser (../../1.1.0/scripts/parse_aicm.py). The control set
is untouched between the two releases — same 247 IDs, same specifications, no
renumbering — so the only parser-visible change is in the mappings sheet:

  * Two mapping frameworks were added, taking the Scope Applicability sheet from
    13 columns to 19. AIUC-1 is new; NIST is back after being absent from 1.1.0,
    now covering the AI RMF as well as AI 600-1. EXPECTED_FRAMEWORKS grows from
    three entries to five. The discovery-and-verify approach the 1.1.0 parser
    introduced did its job here: it hard-errored on the new layout rather than
    silently emitting three frameworks' worth of a five-framework sheet.
  * Both new blocks state "No Mapping" as a literal cell value where no
    counterpart control exists. That is an affirmative publisher statement, not
    an empty cell, so it is preserved verbatim rather than folded into null —
    see NO_MAPPING_SENTINEL and source_data_notes.sentinel_values. Exactly one
    cell (MDS-13 / AIUC-1) is genuinely blank and is reported as a source gap.

    This convention is not new in 1.1.1 and the 1.1.0 parser was already
    subject to it: the EU AI Act block used "No Mapping" for 83 controls in
    1.1.0 and does so identically here. What 1.1.1 changes is only its reach —
    three of five blocks now use it. Counting it explicitly is the new part.

Everything else is inherited unchanged: ownership normalization, full LLM
Taxonomy parsing, version read from the cell A1 stamp, paths from the command
line.

Source spreadsheets are gitignored. Pull from
s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/aicm/1.1.1/

Usage:
    ./parse_aicm.py --input AICMv1.1.1-generated_at_2026_07_22.xlsx
    ./parse_aicm.py --input <xlsx> --output ../aicm-1.1.1.json
"""

import argparse
import csv
import json
import os
import re
import sys

import numpy as np
import pandas as pd

DEFAULT_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "aicm-1.1.1.json")
DEFAULT_CSV = os.path.join(os.path.dirname(__file__), "..", "aicm-1.1.1-controls.csv")

# Mapping frameworks expected in the Scope Applicability sheet, left to right.
# Discovery below compares against this; a mismatch is a hard error, not a silent
# short record. History of this list, which is why the check exists:
#   v1.0.3  BSI AI C4, EU AI Act, ISO/IEC 42001:2023, NIST AI 600-1:2024   (16 cols)
#   v1.1.0  NIST dropped, leaving three frameworks                        (13 cols)
#   v1.1.1  AIUC-1 added; NIST restored and widened to the AI RMF         (19 cols)
EXPECTED_FRAMEWORKS = [
    "AIUC-1 Q2 2026 Version",
    "BSI AI C4",
    "EU AI Act",
    "ISO/IEC 42001:2023",
    "NIST AI RMF + NIST AI 600-1",
]

# Written where a framework has no counterpart control. A stated finding by the
# publisher ("we looked; there is nothing to map to") is not the same as an empty
# cell ("unstated"), so it is preserved verbatim rather than folded into null.
# Used by the EU AI Act block since 1.1.0 and by both blocks added in 1.1.1 —
# three of the five frameworks here. Counted in
# source_data_notes.sentinel_values so a consumer can see how much of a block is
# an explicit no-mapping declaration versus an actual mapping.
NO_MAPPING_SENTINEL = "No Mapping"

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


def write_controls_csv(controls, frameworks, path):
    """Flatten to one row per control.

    The JSON nests ownership, relevance grids, mappings and guidelines; a CSV
    cannot, so nested keys are prefixed and flattened. Mapping columns are built
    from the frameworks actually present rather than a fixed list, so a future
    add-or-drop reshapes the CSV instead of silently dropping a column.
    """
    scalar = ["control_domain", "control_id", "control_title",
              "control_specification", "control_type"]
    groups = [
        ("ownership", "typical_control_applicability_and_ownership"),
        ("arch", "architectural_relevance_ai_stack_components"),
        ("lifecycle", "lifecycle_relevance"),
        ("threat", "threat_category"),
    ]
    guidelines = [("impl", "implementation_guidelines"), ("audit", "auditing_guidelines")]

    fieldnames = list(scalar)
    for prefix, key in groups:
        fieldnames += [f"{prefix}_{sub}" for sub in controls[0][key]]
    for framework in frameworks:
        slug = slugify(framework)
        fieldnames += [f"{slug}_control_mapping", f"{slug}_gap_level", f"{slug}_addendum"]
    for prefix, key in guidelines:
        fieldnames += [f"{prefix}_{sub}" for sub in controls[0][key]]
    fieldnames += ["caiq_question_count", "caiq_question_ids"]

    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for control in controls:
            row = {field: control[field] for field in scalar}
            for prefix, key in groups:
                row.update({f"{prefix}_{sub}": value for sub, value in control[key].items()})
            for framework in frameworks:
                slug = slugify(framework)
                mapping = (control.get("scope_applicability_mappings") or {}).get(slug) or {}
                row.update({
                    f"{slug}_control_mapping": mapping.get("control_mapping"),
                    f"{slug}_gap_level": mapping.get("gap_level"),
                    f"{slug}_addendum": mapping.get("addendum"),
                })
            for prefix, key in guidelines:
                for sub, value in (control.get(key) or {}).items():
                    row[f"{prefix}_{sub}"] = value
            questions = control.get("caiq_questions", [])
            row["caiq_question_count"] = len(questions)
            row["caiq_question_ids"] = "; ".join(q["question_id"] for q in questions)
            writer.writerow(row)

    return fieldnames


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
                    f"The {framework} mapping cell is empty for these controls in "
                    "the publisher's workbook. The mapping is absent at source, not "
                    f"lost in conversion. Note this is a blank cell, not the "
                    f"{NO_MAPPING_SENTINEL!r} value the same sheet uses elsewhere to "
                    "state affirmatively that no counterpart control exists."
                ),
            })

    return gaps


def count_sentinel_values(controls):
    """Tally the literal "No Mapping" declarations per framework.

    "No Mapping" is a positive assertion of absence, so the value is kept as-is
    rather than normalized to null — otherwise a consumer cannot tell "CSA
    determined there is no counterpart" from "CSA said nothing". Three of the
    five frameworks use it here (EU AI Act, as in 1.1.0, plus both blocks added
    in 1.1.1). The counts are recomputed on every run so they cannot drift from
    the data.
    """
    tallies = []
    for framework in EXPECTED_FRAMEWORKS:
        key = slugify(framework)
        ids = sorted(
            c["control_id"] for c in controls
            if (c.get("scope_applicability_mappings") or {}).get(key, {}).get("control_mapping")
            == NO_MAPPING_SENTINEL
        )
        if ids:
            tallies.append({
                "field": f"scope_applicability_mappings.{key}.control_mapping",
                "value": NO_MAPPING_SENTINEL,
                "count": len(ids),
                "control_ids": ids,
                "note": (
                    f"{framework} states {NO_MAPPING_SENTINEL!r} for these controls. "
                    "Preserved verbatim rather than converted to null: an explicit "
                    "no-counterpart finding is not the same as an unstated mapping."
                ),
            })
    return tallies


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", required=True, help="AICM v1.1.1 .xlsx")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="Destination JSON (default: %(default)s)")
    ap.add_argument("--csv", default=DEFAULT_CSV, help="Destination flat CSV (default: %(default)s)")
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
        # The Change Log sheet dates every v1.1.1 entry 2026/07/13; the workbook
        # itself was generated 2026-07-22 (filename, and docProps/core.xml
        # dcterms:created 2026-07-22T17:15:10Z).
        "published": "2026-07-13",
        "generated_at": "2026-07-22",
        "source_file": os.path.basename(xlsx),
        "mapping_frameworks": EXPECTED_FRAMEWORKS,
        "source_data_notes": {
            "normalizations_applied": grouped_normalizations,
            "gaps_in_source": find_source_gaps(controls),
            "sentinel_values": count_sentinel_values(controls),
        },
        "controls": controls,
        "llm_taxonomy": lifecycle,
        "definitions": definitions,
    }

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2, ensure_ascii=False)

    columns = write_controls_csv(controls, EXPECTED_FRAMEWORKS, args.csv)

    questions = sum(len(c["caiq_questions"]) for c in controls)
    domains = len({c["control_domain"] for c in controls})
    print(f"Wrote {len(controls)} controls across {domains} domains to {args.output}")
    print(f"Wrote {len(controls)} rows x {len(columns)} columns to {args.csv}")
    print(f"  AI-CAIQ questions:   {questions}")
    print(f"  lifecycle entries:   {len(lifecycle)}")
    print(f"  definition sections: {', '.join(f'{k} ({len(v)})' for k, v in definitions.items())}")
    for entry in grouped_normalizations:
        print(f"  normalized {entry['cells_changed']} cells: {entry['from']!r} -> {entry['to']!r} "
              f"({', '.join(entry['control_ids'])})")
    for gap in output["source_data_notes"]["gaps_in_source"]:
        print(f"  source gap in {gap['field']}: {', '.join(gap['control_ids'])}")
    for tally in output["source_data_notes"]["sentinel_values"]:
        print(f"  {tally['value']!r} stated for {tally['count']} controls in {tally['field']}")


if __name__ == "__main__":
    main()
