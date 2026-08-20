#!/usr/bin/env python3
"""Build ccm-caiq-3.1.json from the CAIQ v3.1 spreadsheet.

CAIQ v3.1 (2020) is the questionnaire for CCM v3.0.1 (2014). CSA published it as
the successor to CAIQ v3.0.1 -- see the artifact "Transition to CAIQ v3.1".

TWO THINGS THIS PARSER EXISTS TO GET RIGHT
------------------------------------------
1. SPARSE ROWS. Only the FIRST question of each control carries the control-level
   columns (domain, specification, all the mappings). Every subsequent question
   row holds a Question ID and question text and nothing else. A parser that does
   not forward-fill emits questions with no parent, no domain and no mappings --
   records that are complete-looking and empty, which is the worst failure shape
   available.

2. A THREE-ROW MERGED HEADER (rows 2-4) with composite sections. The CSA
   Enterprise Architecture mapping spans three columns (path, Public, Private) and
   ODCA spans two (PA ID, PA level). Reading those as five separate framework
   mappings is exactly the defect that had to be corrected in ccm/3.0.1 -- see
   that directory's README. So this script asserts the expected header text at
   every column it reads and refuses to parse on a mismatch.

Usage:
    python3 build_json.py            # writes ccm-caiq-3.1.json
    python3 build_json.py --check    # verify only, non-zero exit on mismatch
"""
import argparse
import json
import re
import sys

import openpyxl

XLSX = "CAIQ_v3.1_Final.xlsx"
OUT = "ccm-caiq-3.1.json"
SHEET = "CAIQ v3.1"

HEADER_GUARDS = [
    (0, 2, "Control Domain"), (1, 2, "Control ID"), (2, 2, "Question ID"),
    (3, 2, "Control Specification"), (4, 2, "Consensus Assessment Questions"),
    (27, 2, "CCM v3.0.1 Compliance Mapping"),
    (38, 3, "CSA Enterprise Architecture"),
    (38, 4, "Domain > Container > Capability"), (39, 4, "Public"), (40, 4, "Private"),
    (59, 3, "ODCA UM: PA R2.0"), (59, 4, "PA ID"), (60, 4, "PA level"),
]

# Simple (single-column) mapping targets: col -> emitted key, from the sheet's
# own row-3 header text. EA (38-40) and ODCA (59-60) are composites, handled
# separately, and 22-24 (Yes/No/NA response columns) plus 25 (Notes) are a blank
# vendor-response template, not data about the question.
MAPPING_COLS = {
    27: "aicpa_tsc_2009",
    28: "aicpa_trust_service_criteria_soc_2sm_report",
    29: "aicpa_tsc_2014",
    30: "bits_shared_assessments_aup_v5_0",
    31: "bits_shared_assessments_sig_v6_0",
    32: "bsi_germany",
    33: "canada_pipeda",
    34: "cis_aws_foundations_v1_1",
    35: "cobit_4_1",
    36: "cobit_5_0",
    37: "coppa",
    41: "csa_guidance_v3_0",
    42: "enisa_iaf",
    43: "fedramp_security_controls_final_release_jan_2012_low_impact_level",
    44: "fedramp_security_controls_final_release_jan_2012_moderate_impact_level",
    45: "ferpa",
    46: "gapp_aug_2009",
    47: "hipaa_hitech_omnibus_rule",
    48: "hitrust_csf_v8_1",
    49: "iso_iec_27001_2005",
    50: "iso_iec_27001_2013",
    51: "itar",
    52: "jericho_forum",
    53: "mexico_federal_law_on_protection_of_personal_data_held_by_private_parties",
    54: "nerc_cip",
    55: "nist_sp800_53_r3",
    56: "nist_sp800_53_r4_app_j",
    57: "nzism",
    58: "nzism_v2_5",
    61: "pci_dss_v2_0",
    62: "pci_dss_v3_0",
    63: "pci_dss_v3_2",
    64: "shared_assessments_2017_aup",
}
EA_PATH, EA_PUBLIC, EA_PRIVATE = 38, 39, 40
ODCA_ID, ODCA_LEVEL = 59, 60
NO_MAPPING = {"-", "", "n/a", "na"}
QID = re.compile(r"[A-Z&]{2,4}-\d{2}\.\d+")
CID = re.compile(r"[A-Z&]{2,4}-\d{2}")


def cell(v):
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def split_domain(raw):
    """col0 holds "domain<newline>title"; a stray control may use " - " instead
    (CCM 3.0.1's DCS-07 does). Handle both rather than fusing them."""
    parts = [p.strip() for p in (raw or "").split("\n") if p.strip()]
    if len(parts) == 1 and " - " in parts[0]:
        head, _, tail = parts[0].rpartition(" - ")
        parts = [head.strip(), tail.strip()]
    return (parts[0] if parts else None, parts[1] if len(parts) > 1 else None)


def verify_headers(ws):
    rows = {n: r for n, r in enumerate(ws.iter_rows(min_row=1, max_row=4, values_only=True), start=1)}
    problems = []
    for idx, rownum, expected in HEADER_GUARDS:
        row = rows.get(rownum) or ()
        got = cell(row[idx]) if idx < len(row) else None
        flat = re.sub(r"\s+", " ", got or "")
        if expected.lower() not in flat.lower():
            problems.append(f"col{idx} row{rownum}: expected ~{expected!r}, found {flat[:60]!r}")
    if problems:
        print("HEADER MISMATCH -- refusing to parse:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        sys.exit(2)


def mappings_from(row):
    fm = {}
    for idx, key in MAPPING_COLS.items():
        v = cell(row[idx]) if idx < len(row) else None
        if v and v.lower() not in NO_MAPPING:
            fm[key] = v
    path = cell(row[EA_PATH]) if EA_PATH < len(row) else None
    pub = cell(row[EA_PUBLIC]) if EA_PUBLIC < len(row) else None
    priv = cell(row[EA_PRIVATE]) if EA_PRIVATE < len(row) else None
    if any((path, pub, priv)):
        fm["csa_enterprise_architecture_formerly_trusted_cloud_initiative"] = {
            "path": path, "public": pub, "private": priv}
    oid = cell(row[ODCA_ID]) if ODCA_ID < len(row) else None
    olvl = cell(row[ODCA_LEVEL]) if ODCA_LEVEL < len(row) else None
    if any((oid, olvl)):
        fm["odca_um_pa_r2_0"] = {"pa_id": oid, "pa_level": olvl}
    return fm


def build():
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb[SHEET]
    verify_headers(ws)

    questions = []
    carried = None  # the last control-level context seen; the forward-fill source
    for row in ws.iter_rows(min_row=5, values_only=True):
        cid = cell(row[1]) if len(row) > 1 else None
        qid = cell(row[2]) if len(row) > 2 else None

        if cid and CID.fullmatch(cid):
            domain, title = split_domain(cell(row[0]))
            carried = {
                "control_id": cid,
                "control_domain": domain,
                "control_title": title,
                "control_specification": cell(row[3]) if len(row) > 3 else None,
                "framework_mappings": mappings_from(row),
            }

        if not qid or not QID.fullmatch(qid):
            continue
        if carried is None:
            print(f"question {qid} appears before any control row -- "
                  "forward-fill has nothing to carry", file=sys.stderr)
            sys.exit(3)

        questions.append({
            "question_id": qid,
            "question": cell(row[4]) if len(row) > 4 else None,
            "ccm_control_id": carried["control_id"],
            "ccm_control_specification": carried["control_specification"],
            "ccm_control_title": carried["control_title"],
            "ccm_domain_title": carried["control_domain"],
            "ccm_control": {
                "control_domain": carried["control_domain"],
                "control_title": carried["control_title"],
                "control_id": carried["control_id"],
                "control_specification": carried["control_specification"],
                "framework_mappings": carried["framework_mappings"],
            },
        })
    wb.close()
    return {
        "specification_name": "Consensus Assessments Initiative Questionnaire",
        "caiq_version": "3.1",
        "ccm_version": "3.0.1",
        "generated_at": "2020-04-01",
        "source_file": "CAIQ_v3.1_Final.xlsx",
        "questions": questions,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    doc = build()
    qs = doc["questions"]
    parents = {q["ccm_control_id"] for q in qs}
    targets = set()
    for q in qs:
        targets |= set(q["ccm_control"]["framework_mappings"].keys())
    orphans = [q["question_id"] for q in qs if not q["ccm_control_id"]]
    summary = (f"{len(qs)} questions, {len(parents)} parent controls, "
               f"{len(targets)} mapping targets, {len(orphans)} orphans")
    if orphans:
        print(f"ORPHANED QUESTIONS: {orphans[:5]}", file=sys.stderr)
        sys.exit(4)
    if args.check:
        if json.load(open(OUT, encoding="utf-8")) != doc:
            print(f"{OUT} differs from a fresh build of {XLSX}", file=sys.stderr)
            sys.exit(1)
        print(f"{OUT} matches a fresh build -- {summary}")
        return
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {OUT}: {summary}")


if __name__ == "__main__":
    main()
