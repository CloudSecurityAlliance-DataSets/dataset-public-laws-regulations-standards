#!/usr/bin/env python3
"""Parse the CCM v4.1.1 workbook into JSON, a flat controls CSV, and a DORA reverse-mapping CSV.

Adapted from the 4.1.0 parser (../../4.1.0/scripts/parse_ccm.py). The control
sheets are laid out as in 4.1.0 and are read the same way, so every control
field keeps the name and shape it has in ccm-4.1.0.json. What 4.1.1 adds:

  * The first CCM v4.1 cross-framework mappings. 4.1.0's Scope Applicability
    (Mappings) sheet held only "This dataset is not available yet"; 4.1.1 carries
    NIST SP 800-171 rev2 and MITRE ATT&CK blocks. Frameworks are discovered from
    the sheet's merged group-header row and checked against EXPECTED_FRAMEWORKS,
    as the AICM parser does (../../../aicm/1.1.1/scripts/parse_aicm.py).
  * A new Reverse Mappings sheet mapping DORA provisions onto CCM controls.
  * Guards that refuse rather than misread: the cell A1 version stamp must say
    4.1.1, the mapping frameworks must match EXPECTED_FRAMEWORKS, and the Reverse
    Mappings header and source names must match EXPECTED_REVERSE_*. Each exits 1.

"No Mapping" is a value the publisher writes where no counterpart exists. It is
kept verbatim, not folded into null, and tallied in
source_data_notes.sentinel_values.

Source spreadsheets are gitignored. Pull from
s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/ccm/4.1.1/

Usage:
    ./parse_ccm.py --input ../CCMv4.1.1-generated_at_2026_10_02.xlsx
"""

import argparse
import csv
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(__file__)
DEFAULT_OUTPUT = os.path.join(HERE, "..", "ccm-4.1.1.json")
DEFAULT_CSV = os.path.join(HERE, "..", "ccm-4.1.1-controls.csv")
DEFAULT_REVERSE_CSV = os.path.join(HERE, "..", "ccm-4.1.1-reverse-mappings.csv")

EXPECTED_VERSION = "4.1.1"

# Mapping frameworks in the Scope Applicability sheet, left to right, with the
# JSON key each is emitted under. Keys are explicit rather than slugified:
# slugifying "MITRE ATT&CK" gives "mitre_att_ck".
#   v4.1.0  none ("This dataset is not available yet")
#   v4.1.1  NIST SP 800-171 rev2, MITRE ATT&CK (v17.1 per the Change Log)
FRAMEWORK_KEYS = {
    "NIST SP 800-171 rev2": "nist_sp_800_171_rev2",
    "MITRE ATT&CK": "mitre_attack",
}
EXPECTED_FRAMEWORKS = list(FRAMEWORK_KEYS)

# Reverse Mappings: column headers, and the source sections expected under them.
EXPECTED_REVERSE_HEADER = ["Source Reference(s)", "Source Description", "CCM Controls",
                           "Gap Level", "Addendum", "Analysis"]
EXPECTED_REVERSE_SOURCES = {"Digital Operational Resilience Act": "dora"}
REVERSE_END_MARKER = "End of Standard"

NO_MAPPING_SENTINEL = "No Mapping"
FRAMEWORK_COLUMN_SPAN = 3


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


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def read_sheet(xlsx, sheet_name, skip_rows=2):
    df = pd.read_excel(xlsx, sheet_name=sheet_name, header=None, skiprows=skip_rows)
    df = df.iloc[1:]  # skip column header row
    df.columns = range(df.shape[1])
    return df


def read_specification_version(xlsx):
    """Cell A1 of every sheet carries {"specification_name":...,"specification_version":...}."""
    a1 = pd.read_excel(xlsx, sheet_name="CCM", header=None, nrows=1).iloc[0, 0]
    try:
        return json.loads(a1)["specification_version"]
    except (TypeError, ValueError, KeyError):
        fail(f"could not read the version stamp from cell A1 of the CCM sheet ({a1!r})")


def generated_at(xlsx):
    """'CCMv4.1.1-generated_at_2026_10_02.xlsx' -> '2026-10-02'."""
    m = re.search(r"generated_at_(\d{4})_(\d{2})_(\d{2})", os.path.basename(xlsx))
    return "-".join(m.groups()) if m else None


def parse_ccm_controls(xlsx):
    """Parse the main CCM sheet (23 columns)."""
    df = read_sheet(xlsx, "CCM")
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

        controls.append({
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
        })

    return controls


def parse_implementation_guidelines(xlsx):
    guidelines = {}
    for _, row in read_sheet(xlsx, "Implementation Guidelines").iterrows():
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


def parse_auditing_guidelines(xlsx):
    guidelines = {}
    for _, row in read_sheet(xlsx, "Auditing Guidelines", skip_rows=1).iterrows():
        control_id = clean(row[2])
        if control_id is None:
            continue
        guidelines[control_id] = clean(row[4])
    return guidelines


def parse_caiq_questions(xlsx):
    """Parse the CAIQ sheet embedded in the CCM workbook, grouped by control_id."""
    questions = {}
    current_control_id = None

    for _, row in read_sheet(xlsx, "CAIQ", skip_rows=1).iterrows():
        question_id = clean(row[4])
        control_id = clean(row[2])
        if control_id:
            current_control_id = control_id
        if question_id is None:
            continue
        questions.setdefault(current_control_id, []).append({
            "question_id": question_id,
            "question": clean(row[5]),
            "caiq_lite": clean(row[6]),
        })

    return questions


def discover_mapping_frameworks(xlsx):
    """Read framework names and start columns from the merged group-header row (row 2)."""
    header = pd.read_excel(xlsx, sheet_name="Scope Applicability (Mappings)", header=None,
                           skiprows=1, nrows=1).iloc[0]
    frameworks = [(value.strip(), column) for column, value in enumerate(header)
                  if isinstance(value, str) and value.strip()]
    found = [name for name, _ in frameworks]
    if found != EXPECTED_FRAMEWORKS:
        fail("mapping frameworks in the workbook do not match expectations.\n"
             f"  expected: {EXPECTED_FRAMEWORKS}\n"
             f"  found:    {found}\n"
             "The publisher changed the mappings layout. Confirm what was added or dropped,\n"
             "update FRAMEWORK_KEYS, and record it in the metadata's known_source_issues.")
    return frameworks


def parse_scope_applicability_mappings(xlsx):
    frameworks = discover_mapping_frameworks(xlsx)
    mappings = {}
    for _, row in read_sheet(xlsx, "Scope Applicability (Mappings)").iterrows():
        control_id = clean(row[2])
        if control_id is None:
            continue
        mappings[control_id] = {
            FRAMEWORK_KEYS[name]: {
                "control_mapping": clean(row[start]),
                "gap_level": clean(row[start + 1]),
                "addendum": clean(row[start + 2]),
            }
            for name, start in frameworks
        }
    return mappings


def split_ccm_controls(cell):
    """'GRC-01\\nGRC-02' -> ['GRC-01', 'GRC-02']; blank -> []."""
    if not cell:
        return []
    return [part.strip() for part in re.split(r"[\n,;]+", cell) if part.strip()]


def parse_reverse_mappings(xlsx):
    """Parse the Reverse Mappings sheet: provisions of another framework -> CCM controls.

    Row 1 is the version stamp, row 2 the column header. Below that, a row with
    only its first cell set names a source framework; rows with a reference and a
    description are that source's provisions; "End of Standard" ends the data.
    """
    df = pd.read_excel(xlsx, sheet_name="Reverse Mappings", header=None, skiprows=1)
    header = [clean(v) for v in df.iloc[0].tolist()]
    if header[:len(EXPECTED_REVERSE_HEADER)] != EXPECTED_REVERSE_HEADER:
        fail("Reverse Mappings header does not match expectations.\n"
             f"  expected: {EXPECTED_REVERSE_HEADER}\n"
             f"  found:    {header}")

    sources = {}
    current = None
    for _, row in df.iloc[1:].iterrows():
        cells = [clean(row[i]) if i < len(row) else None for i in range(len(EXPECTED_REVERSE_HEADER))]
        reference, description = cells[0], cells[1]
        if reference == REVERSE_END_MARKER:
            break
        if reference and not any(cells[1:]):
            if reference not in EXPECTED_REVERSE_SOURCES:
                fail(f"unexpected source section in Reverse Mappings: {reference!r}. "
                     "Add it to EXPECTED_REVERSE_SOURCES once confirmed.")
            current = sources.setdefault(EXPECTED_REVERSE_SOURCES[reference],
                                         {"source_name": reference, "provisions": []})
            continue
        if not (reference and description):
            continue
        if current is None:
            fail(f"provision {reference!r} appears before any source section")
        current["provisions"].append({
            "source_reference": reference,
            "source_description": description,
            "ccm_controls": split_ccm_controls(cells[2]),
            "gap_level": cells[3],
            "addendum": cells[4],
            "analysis": cells[5],
        })

    missing = set(EXPECTED_REVERSE_SOURCES.values()) - set(sources)
    if missing:
        fail(f"Reverse Mappings has no section for {sorted(missing)}")
    return sources


def flatten(prefix, value, out):
    """Nested dicts become prefix_sub columns."""
    if isinstance(value, dict):
        for sub, inner in value.items():
            flatten(f"{prefix}_{sub}", inner, out)
    else:
        out[prefix] = value


def write_controls_csv(controls, path):
    """One row per control; nested fields flattened with prefixes."""
    groups = [
        ("ownership", "typical_control_applicability_and_ownership"),
        ("arch", "architectural_relevance_cloud_stack_components"),
        ("org", "organizational_relevance"),
        ("mapping", "scope_applicability_mappings"),
        ("impl", "implementation_guidelines"),
        ("audit", "auditing_guidelines"),
    ]
    rows = []
    for control in controls:
        row = {field: control[field] for field in
               ("control_domain", "control_id", "control_title", "control_specification", "ccm_lite")}
        for prefix, key in groups:
            flatten(prefix, control.get(key), row)
        questions = control.get("caiq_questions", [])
        row["caiq_question_count"] = len(questions)
        row["caiq_question_ids"] = "; ".join(q["question_id"] for q in questions)
        rows.append(row)

    fieldnames = list(rows[0])
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return fieldnames


def write_reverse_csv(reverse, path):
    fieldnames = ["source", "source_reference", "source_description", "ccm_controls",
                  "gap_level", "addendum", "analysis"]
    count = 0
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for key, source in reverse.items():
            for p in source["provisions"]:
                writer.writerow({**p, "source": key, "ccm_controls": "; ".join(p["ccm_controls"])})
                count += 1
    return count


def find_source_gaps(controls):
    """Cells the publisher left empty — absent at source, not lost in conversion."""
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
            "note": "These ownership cells are empty in the publisher's workbook.",
        })
    for name, key in FRAMEWORK_KEYS.items():
        missing = sorted(c["control_id"] for c in controls
                         if not ((c.get("scope_applicability_mappings") or {}).get(key) or {}).get("control_mapping"))
        if missing:
            gaps.append({
                "field": f"scope_applicability_mappings.{key}.control_mapping",
                "control_ids": missing,
                "note": (f"The {name} mapping cell is empty for these controls in the publisher's "
                         f"workbook — a blank, not the {NO_MAPPING_SENTINEL!r} value."),
            })
    return gaps


def count_sentinel_values(controls):
    """Tally the literal "No Mapping" declarations per framework."""
    tallies = []
    for name, key in FRAMEWORK_KEYS.items():
        ids = sorted(c["control_id"] for c in controls
                     if ((c.get("scope_applicability_mappings") or {}).get(key) or {}).get("control_mapping")
                     == NO_MAPPING_SENTINEL)
        if ids:
            tallies.append({
                "field": f"scope_applicability_mappings.{key}.control_mapping",
                "value": NO_MAPPING_SENTINEL,
                "count": len(ids),
                "control_ids": ids,
                "note": (f"{name} states {NO_MAPPING_SENTINEL!r} for these controls. Preserved "
                         "verbatim: an explicit no-counterpart finding is not an unstated mapping."),
            })
    return tallies


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", required=True, help="CCM v4.1.1 .xlsx")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="Destination JSON (default: %(default)s)")
    ap.add_argument("--csv", default=DEFAULT_CSV, help="Destination controls CSV (default: %(default)s)")
    ap.add_argument("--reverse-csv", default=DEFAULT_REVERSE_CSV,
                    help="Destination reverse-mapping CSV (default: %(default)s)")
    args = ap.parse_args()
    xlsx = args.input

    version = read_specification_version(xlsx)
    if version != EXPECTED_VERSION:
        fail(f"cell A1 stamps specification_version {version!r}; this parser reads {EXPECTED_VERSION!r} only. "
             "Use the parser in that version's directory, or adapt a copy.")

    controls = parse_ccm_controls(xlsx)
    implementation = parse_implementation_guidelines(xlsx)
    auditing = parse_auditing_guidelines(xlsx)
    mappings = parse_scope_applicability_mappings(xlsx)
    caiq = parse_caiq_questions(xlsx)
    reverse = parse_reverse_mappings(xlsx)

    for control in controls:
        cid = control["control_id"]
        control["implementation_guidelines"] = implementation.get(cid)
        control["auditing_guidelines"] = auditing.get(cid)
        control["scope_applicability_mappings"] = mappings.get(cid)
        control["caiq_questions"] = caiq.get(cid, [])

    for field in ("implementation_guidelines", "auditing_guidelines",
                  "scope_applicability_mappings", "caiq_questions"):
        ids = [c["control_id"] for c in controls if not c[field]]
        if ids:
            print(f"warning: {len(ids)} controls missing {field}: {ids[:8]}", file=sys.stderr)

    output = {
        "specification_name": "Cloud Controls Matrix",
        "specification_version": version,
        "generated_at": generated_at(xlsx),
        "source_workbook": os.path.basename(xlsx),
        "mapping_frameworks": EXPECTED_FRAMEWORKS,
        "source_data_notes": {
            "gaps_in_source": find_source_gaps(controls),
            "sentinel_values": count_sentinel_values(controls),
        },
        "controls": controls,
        "reverse_mappings": reverse,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    columns = write_controls_csv(controls, args.csv)
    provisions = write_reverse_csv(reverse, args.reverse_csv)

    print(f"Wrote {len(controls)} controls to {args.output}")
    print(f"Wrote {len(controls)} rows x {len(columns)} columns to {args.csv}")
    print(f"Wrote {provisions} provisions to {args.reverse_csv}")
    for tally in output["source_data_notes"]["sentinel_values"]:
        print(f"  {tally['value']!r} stated for {tally['count']} controls in {tally['field']}")
    for gap in output["source_data_notes"]["gaps_in_source"]:
        print(f"  source gap in {gap['field']}: {', '.join(gap['control_ids'])}")


if __name__ == "__main__":
    main()
