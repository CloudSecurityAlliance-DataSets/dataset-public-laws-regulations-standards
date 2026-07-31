# AICM v1.1.0

`secid:control/cloudsecurityalliance.org/aicm@1.1.0` · 247 controls · 18 domains · published 2026-06-22

> ## ⚠️ Control IDs changed meaning in this release
>
> **AICM v1.1.0 control IDs are not interchangeable with v1.0.3 control IDs.**
>
> CSA renumbered controls in place. **55 of the 242 control IDs shared with
> v1.0.3 now designate a different control.** The identifier string survived;
> what it points at did not.
>
> | ID | means in v1.0.3 | means in v1.1.0 |
> |---|---|---|
> | `LOG-15` | Output Monitoring | **Input Monitoring** |
> | `IAM-12` | Safeguard Logs Integrity | **Unique Identities** |
> | `TVM-12` | Threat Analysis and Modelling | **Vulnerability Management Metrics** |
>
> If you are carrying references forward from v1.0.3 — mappings, assessments,
> crosswalks, STAR submissions — **you cannot migrate them by string match.**
> Use [`../crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv`](../crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv).
>
> Full analysis: [`../VERSIONING.md`](../VERSIONING.md)

## Contents

| File | What |
|---|---|
| `aicm-1.1.0.json` | Full extraction — 247 controls with guidelines, mappings, and AI-CAIQ questions, plus the LLM taxonomy and definition sections |
| `aicm-1.1.0-controls.csv` | Flat view — one row per control, 247 × 52 columns |
| `aicm-1.1.0-metadata.json` | Document metadata, licence, and known source issues |
| `scripts/parse_aicm.py` | Rebuilds the JSON and CSV from the publisher's workbook |
| `scripts/parse_caiq.py` | Builds the companion questionnaire extraction under [`../../aicm-caiq/1.1.0/`](../../aicm-caiq/1.1.0/) |

The JSON is the complete record; the CSV flattens the nested ownership,
relevance, mapping and guideline groups into prefixed columns for spreadsheet
and dataframe use. Mapping columns are generated from the frameworks actually
present, so a future add-or-drop reshapes the CSV rather than silently losing a
column.

### Companion guidance

The AICM v1.1 bundle also ships three PDFs, extracted to markdown under
`reference/`:

| Document | Path |
|---|---|
| Introductory Guidance to AICM v1.1 | [`reference/cloudsecurityalliance.org/aicm-introductory-guidance/v1.1/`](../../../../reference/cloudsecurityalliance.org/aicm-introductory-guidance/v1.1/) |
| Filling in the AI-CAIQ: Instructions and Recommendations | [`reference/cloudsecurityalliance.org/ai-caiq-instructions/v1.1/`](../../../../reference/cloudsecurityalliance.org/ai-caiq-instructions/v1.1/) |
| STAR for AI Level 1 Submission Guide | [`reference/cloudsecurityalliance.org/star-for-ai-level-1-submission-guide/v1.1/`](../../../../reference/cloudsecurityalliance.org/star-for-ai-level-1-submission-guide/v1.1/) |

Source spreadsheets are gitignored. Pull from
`s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/aicm/1.1.0/`.

```bash
cd scripts
./parse_aicm.py --input AICMv1.1.0-generated_at_2026_06_18.xlsx
./parse_caiq.py --input AI_CAIQv1.1.0-star_security_questionnaire-generated_at_2026_06_18.xlsx
```

## What else differs from v1.0.3

**NIST AI 600-1:2024 mappings were withdrawn.** The Scope Applicability sheet
dropped from 16 columns to 13. Only BSI AI C4, the EU AI Act, and ISO/IEC
42001:2023 remain. Accepted as shipped — if you need NIST AI 600-1 mappings,
they exist only in the [v1.0.3 extraction](../1.0.3/), whose control IDs do not
carry over.

**Schema change in the extraction.** The ownership key
`gen_ai_ops_processing_infrastructure` is now
`cloud_ai_processing_infrastructure`, following the source column rename to
"Cloud/AI Processing Infrastructure (PI)". The JSON also gains a top-level
`definitions` object (Control Type, Control Ownership, Threat Category, Other
Definitions) that the 1.0.3 extraction omitted, and a `source_data_notes` block.

## Source data notes

Recorded in `source_data_notes` inside `aicm-1.1.0.json`, recomputed on every
parse run:

- **One normalization applied.** `GRC-01`–`GRC-08` state the CSP owner without
  the `Owned by the` prefix every other control uses. Normalized to the full
  form so the ownership vocabulary is a closed set of 10 values. All 8
  substitutions are itemized by control ID.
- **Five ownership cells are empty at source** — `DSP-21`, `DSP-23`, `DSP-24`.
  Not a conversion error; CSA's workbook states no owner for these cells. Emitted
  as `null`.
- **`DSP-08` has no BSI AI C4 mapping at source.** Not a conversion error; the
  cell is empty in CSA's workbook. Long-standing — the same gap exists in v1.0.3.

Everything else is complete: all 247 controls have implementation guidelines,
auditing guidelines, EU AI Act and ISO/IEC 42001 mappings, and at least one
AI-CAIQ question.
