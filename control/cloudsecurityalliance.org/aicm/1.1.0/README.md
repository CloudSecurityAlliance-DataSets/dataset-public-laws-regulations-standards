# AICM v1.1.0

`secid:control/cloudsecurityalliance.org/aicm@1.1.0` · 247 controls · 18 domains · published 2026-06-22

**Also known as AICM 1.1.** CSA's download page calls this release "v1.1"; the
spreadsheet calls itself `1.1.0`. Same release, two labels — we use **1.1.0** and
alias 1.1 to it. See [Version naming and aliases](#version-naming-and-aliases) below.

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
> Full analysis: [`../VERSIONING.md`](../VERSIONING.md) · per-control verdicts:
> [`../crosswalks/aicm-1.0.3-to-1.1.0-changelog.md`](../crosswalks/aicm-1.0.3-to-1.1.0-changelog.md)

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

## Version naming and aliases

CSA labels this release two ways, and both are in circulation:

| Where | String |
|---|---|
| Cell A1 of every worksheet | `{"specification_version":"1.1.0"}` |
| Spreadsheet filename | `AICMv1.1.0-generated_at_2026_06_18.xlsx` |
| CSA artifact / download page | "AI Controls Matrix **v1.1**" |
| Bundle ZIP and PDF titles | "AICM **v1.1**" |

**We use `1.1.0` as canonical and alias `1.1` to it.** The artifact's own internal
stamp wins over the download page, because that is the string a consumer parsing
the file will actually encounter — and it keeps the version sort stable against
the sibling releases `1.0.3` and `0.0.2`.

Recorded machine-readably in `aicm-1.1.0-metadata.json`:

```json
"version": "1.1.0",
"version_aliases": ["1.1", "v1.1", "v1.1.0"],
```

So `AICM 1.1`, `AICM v1.1`, and `AICM 1.1.0` all denote **this** directory. Note
this is a labelling alias only — it says nothing about compatibility with 1.0.3,
which is a genuinely different release (see the warning above).

One wrinkle worth knowing: the three guidance PDFs from this bundle live under
`reference/` in directories named `v1.1`, not `1.1.0`. That follows the existing
`reference/` convention (`ccm-implementation-guidelines/v2.0-20240528`) and the
fact that those documents title themselves "v1.1". Different directory string,
same release.

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
