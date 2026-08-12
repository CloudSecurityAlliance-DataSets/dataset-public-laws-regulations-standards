# AICM v1.1.1

`secid:control/cloudsecurityalliance.org/aicm@1.1.1` · 247 controls · 18 domains · published 2026-07-13

Current AICM release. A **patch** over [1.1.0](../1.1.0/): the control set is
untouched, and the changes are two added mapping frameworks plus four corrected
cells.

> ## ⚠️ CSA ships this release under the label "v1.1", the same as 1.1.0
>
> The artifact page, the bundle name, and the stated release date are all
> unchanged from 1.1.0. Nothing on
> [the download page](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix-v1-1)
> says 1.1.1 — it still reads "AI Controls Matrix v1.1", released 06/22/2026.
>
> | Where | 1.1.0 bundle | 1.1.1 bundle |
> |---|---|---|
> | Artifact page label | "AI Controls Matrix v1.1" | "AI Controls Matrix v1.1" *(unchanged)* |
> | Stated release date | 06/22/2026 | 06/22/2026 *(unchanged)* |
> | Spreadsheet filename | `AICMv1.1.0-generated_at_2026_06_18.xlsx` | `AICMv1.1.1-generated_at_2026_07_22.xlsx` |
> | Cell A1 of every sheet | `{"specification_version":"1.1.0"}` | `{"specification_version":"1.1.1"}` |
>
> The version is discoverable **only** from the filename token and the cell A1
> stamp. If you downloaded "AICM v1.1" before roughly 2026-07-22 you have 1.1.0;
> after, you have 1.1.1.
>
> **Consequence: "AICM v1.1" is ambiguous and cannot be resolved to a dataset.**
> Cite `AICM 1.1.0` or `AICM 1.1.1`. The bare aliases `1.1` and `v1.1` are
> claimed by neither directory — 1.1.0 held them until this release shipped and
> has since given them up.

> ## ✅ Control IDs ARE stable against 1.1.0 — no crosswalk needed
>
> This is the opposite of the 1.0.3 → 1.1.0 situation. All 247 control IDs,
> titles, specifications, control types, ownership assignments, relevance grids,
> threat categories, and auditing guidelines are **identical** to the 1.1.0
> extraction, as is the LLM taxonomy.
>
> **A 1.1.0 control ID migrates to 1.1.1 by string match.** No crosswalk is
> provided because none is needed — stated explicitly because "no crosswalk
> exists" and "no crosswalk is needed" look the same from outside.
>
> Migrating from **1.0.3** is a different matter entirely and still requires
> [`../crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv`](../crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv)
> — the 1.0.3 renumbering warning applies to 1.1.1 exactly as it does to 1.1.0.
> See [`../VERSIONING.md`](../VERSIONING.md).

## Everything that differs from 1.1.0

Verified by diffing the two extractions field by field across all 247 controls.
The list is complete — every other field is identical.

### 1. Two mapping frameworks added (13 → 19 columns)

| Framework | Status | Populated |
|---|---|---|
| **AIUC-1 Q2 2026 Version** | **new** | 143 mapped · 103 `No Mapping` · 1 blank (`MDS-13`) |
| **NIST AI RMF + NIST AI 600-1** | **restored** | 137 mapped · 110 `No Mapping` |
| BSI AI C4 | carried over | identical in every cell |
| EU AI Act | carried over | identical in every cell |
| ISO/IEC 42001:2023 | carried over | identical in every cell |

The NIST block **resolves the `nist-ai-600-1-mappings-withdrawn` issue** recorded
against 1.1.0, which shipped no NIST mappings at all while its own change log
claimed otherwise. Those mappings previously existed only in the
[1.0.3 extraction](../1.0.3/), whose control IDs do not carry over; 1.1.1 has
them against current, stable IDs. The block is also wider than 1.0.3's — it
covers the NIST AI RMF as well as AI 600-1.

The three carried-over framework slugs are unchanged, so consumers keying on
them are unaffected by the addition.

### 2. Three Model Provider implementation guidelines corrected

`GRC-01`, `IAM-13`, `IAM-18` — the only cells that differ across the entire
Implementation Guidelines sheet. All three were mis-scoped in 1.1.0: the Model
Provider column held text tagged for *other* actors.

| Control | 1.1.0 MP cell opened with | 1.1.1 replaces it with |
|---|---|---|
| `GRC-01` | `[Application Provider/Orchestrated Service Provider/AI Customer]` | AI governance framework: ownership, accountability, decision authority |
| `IAM-13` | `[MP]`, then continued into `[ALL Actors - AICM - CSP]` guidance | Unique model/variant identifiers and downstream propagation |
| `IAM-18` | `[All Actors]` | Tool/plugin exposure inventory, least-privilege tool access |

### 3. One AI-CAIQ question corrected

`SEF-06.1` shipped in 1.1.0 with two drafts concatenated into a single cell,
joined by an editorial marker:

> Are security-related event triage processes… evaluated? **Alternative
> formulation:** Are processes procedures and technical measures supporting
> business processes to triage s…

1.1.1 keeps only the second wording. The defect **predates 1.1.0** — the same
doubled text is in the 1.0.3 and `aicm-caiq` 1.0.2 extractions — so this is the
first release where the question is clean. Earlier extractions carry it
as-shipped and are not retroactively edited.

## Contents

| File | What |
|---|---|
| `aicm-1.1.1.json` | Full extraction — 247 controls with guidelines, five-framework mappings, and AI-CAIQ questions, plus the LLM taxonomy and definition sections |
| `aicm-1.1.1-controls.csv` | Flat view — one row per control, 247 × 58 columns (52 in 1.1.0; +6 for the two new framework triples) |
| `aicm-1.1.1-metadata.json` | Document metadata, licence, and known source issues |
| `scripts/parse_aicm.py` | Rebuilds the JSON and CSV from the publisher's workbook |

Two files that 1.1.0 has and this directory deliberately does not:

- **No `CHANGELOG.md` / per-control changelog JSON.** Those exist to carry the
  1.0.3 → 1.1.0 renumbering, which has no counterpart here. The four changed
  cells are enumerated above in full.
- **No `scripts/parse_caiq.py`.** The standalone questionnaire in this bundle is
  still labelled 1.1.0 (see below), so there is no `aicm-caiq@1.1.1` to build.
  Use [`../1.1.0/scripts/parse_caiq.py`](../1.1.0/scripts/parse_caiq.py), which
  targets `aicm-caiq/1.1.0/`. Note it enriches its output from
  `../aicm-1.1.0.json`, so pointing it at this directory requires
  `--aicm-json ../../1.1.1/aicm-1.1.1.json` — the only field that differs is the
  `SEF-06.1` question text.

### Companion guidance

The bundle ships the same three PDFs as the 1.1.0 release, with unchanged
filenames, already extracted to markdown under `reference/`:

| Document | Path |
|---|---|
| Introductory Guidance to AICM v1.1 | [`reference/cloudsecurityalliance.org/aicm-introductory-guidance/v1.1/`](../../../../reference/cloudsecurityalliance.org/aicm-introductory-guidance/v1.1/) |
| Filling in the AI-CAIQ: Instructions and Recommendations | [`reference/cloudsecurityalliance.org/ai-caiq-instructions/v1.1/`](../../../../reference/cloudsecurityalliance.org/ai-caiq-instructions/v1.1/) |
| STAR for AI Level 1 Submission Guide | [`reference/cloudsecurityalliance.org/star-for-ai-level-1-submission-guide/v1.1/`](../../../../reference/cloudsecurityalliance.org/star-for-ai-level-1-submission-guide/v1.1/) |

The standalone questionnaire in this bundle is **still labelled 1.1.0** in its
filename, sheet name, title, copyright notice, and `caiq_version` stamp — even
though its own Change Log adds an "AI-CAIQ v1.1.1" row. Only two cells changed
in that workbook: the spec-version stamp and the `SEF-06.1` question. It lives
under [`../../aicm-caiq/`](../../aicm-caiq/).

## Reproducing

Source spreadsheets are gitignored. Pull from
`s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/aicm/1.1.1/`.

```bash
cd scripts
./parse_aicm.py --input ../AICMv1.1.1-generated_at_2026_07_22.xlsx
```

`parse_aicm.py` is adapted from the 1.1.0 copy. `EXPECTED_FRAMEWORKS` grew from
three entries to five; everything else is inherited. The parser discovers the
mapping frameworks from the sheet's merged group-header row and **hard-errors**
if they do not match that list, which is exactly what it did when first run
against this workbook. A parser trusting fixed column offsets would have read
AIUC-1's mapping into the BSI field and emitted a plausible, entirely wrong
extraction.

## Source data notes

Recorded in `source_data_notes` inside `aicm-1.1.1.json`, recomputed on every
parse run.

**`No Mapping` is a value, not an absence.** Three of the five framework blocks
state the literal string where no counterpart control exists — AIUC-1 (103
controls), EU AI Act (83, unchanged from 1.1.0), NIST (110). It is preserved
verbatim rather than folded into `null`, because an explicit publisher finding of
"we looked and there is no counterpart" is a different fact from an unstated
mapping. **If you filter for "has a mapping", exclude the string `No Mapping` as
well as `null`.** Counts are tallied per framework in
`source_data_notes.sentinel_values`.

**`MDS-13` has a blank AIUC-1 mapping cell** — the only one. Conspicuous because
the neighbouring cells *are* populated (`Full Gap`, plus an addendum reading
"Address model-artifact protection or format integrity"), and because the same
column says `No Mapping` for the other 103 unmapped controls. It looks like an
omission where `No Mapping` was meant, but the extraction does not infer that: it
emits `null` and records the cell as a source gap.

Carried over unchanged from 1.1.0, and still true here:

- **One normalization applied.** `GRC-01`–`GRC-08` state the CSP owner without
  the `Owned by the` prefix every other control uses. Normalized to the full
  form so the ownership vocabulary is a closed set of 10 values. All 8
  substitutions are itemized by control ID.
- **Five ownership cells are empty at source** — `DSP-21`, `DSP-23`, `DSP-24`.
  Not a conversion error; CSA's workbook states no owner. Emitted as `null`.
- **`DSP-08` has no BSI AI C4 mapping at source.** Not a conversion error, and
  long-standing — the same gap exists in v1.0.3.

Everything else is complete: all 247 controls have implementation guidelines,
auditing guidelines, populated cells in all five mapping blocks (bar the two
noted above), and at least one AI-CAIQ question.
