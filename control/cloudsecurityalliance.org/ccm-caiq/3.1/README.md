# CCM-CAIQ v3.1

Consensus Assessments Initiative Questionnaire v3.1 — **309 questions across all
133 CCM v3.0.1 controls**, published 2020-04-01.

CAIQ v3.1 is the questionnaire for **CCM v3.0.1**. There is no CCM v3.1. CSA
published it as the successor to CAIQ v3.0.1 — see the artifact "Transition to
CAIQ v3.1" — and it is the last questionnaire of the v3 line.

| file | tracked | what |
|---|---|---|
| `ccm-caiq-3.1.json` | yes | 309 questions, each carrying its parent CCM v3.0.1 control |
| `ccm-caiq-3.1-metadata.json` | yes | dataset metadata |
| `build_json.py` | yes | regenerates the extraction; `--check` verifies without writing |
| `CAIQ_v3.1_Final.xlsx` | **no** | the source spreadsheet — see below |

## The source spreadsheet is NOT tracked

`.gitignore` excludes `*.xlsx` repo-wide, and no sibling version directory tracks
its spreadsheet either. So `build_json.py` is a **maintainer tool**: it needs the
xlsx present locally and cannot run from a fresh clone. The committed
`ccm-caiq-3.1.json` is what consumers read.

Where to get the source again: on CSA's website it sits under the **CCAK
study-materials** artifact, not under the CAIQ artifact — `CAIQ_v3.1_Final.xlsx`.
Worth knowing, because CSA serves one file per artifact page and replaces it in
place on update; the original AICM v1.1.0 zip is already unrecoverable that way.

## Two properties of the source that a parser must handle

**Sparse rows.** Only the FIRST question of each control carries the
control-level columns — domain, specification, and all the mappings. Every
subsequent question row holds a Question ID and question text and nothing else.
Without forward-fill, those questions come out with no parent, no domain and no
mappings: complete-looking, empty records.

**A three-row merged header (rows 2-4) with composites.** The CSA Enterprise
Architecture mapping spans three columns (path, Public, Private) and ODCA UM: PA
R2.0 spans two (PA ID, PA level). They are stored as nested objects. Reading
their sub-columns as separate frameworks is the defect corrected in
[`../../ccm/3.0.1/`](../../ccm/3.0.1/README.md).

`build_json.py` asserts the expected header text at every column it reads and
exits non-zero on a mismatch. Verify with `python3 build_json.py --check`.

## Mappings: not a superset of CCM v3.0.1's

35 targets here against 32 in `ccm/3.0.1`, but the sets differ in both
directions. **A consumer wanting every v3-era mapping must union both files.**

| | |
|---|---|
| added here (published after 2014) | CIS-AWS-Foundations v1.1, HITRUST CSF v8.1, NZISM v2.5, PCI DSS v3.2, Shared Assessments 2017 AUP |
| dropped here, present in `ccm/3.0.1` | 95/46/EC EU Data Protection Directive (superseded by GDPR), CCM v1.x lineage |
| same framework, different label | AICPA TSC 2009 / 2014; HIPAA/HITECH, which v3.1 labels "Omnibus Rule" |

## Notes for consumers

- The source writes `-` for "no mapping here"; it is dropped, so an absent key is
  the single encoding of that fact.
- Columns 22-24 (Yes / No / Not Applicable) and 25 (Notes) are a blank
  vendor-response template, not data about the question. Not extracted.
