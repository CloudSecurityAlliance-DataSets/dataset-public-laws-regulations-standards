# CCM v4.1.1

`secid:control/cloudsecurityalliance.org/ccm@4.1.1` · 207 controls · 17 domains · published 2026-10-01

Current Cloud Controls Matrix release. A **patch** over [4.1.0](../4.1.0/): the
control set is unchanged, and the release adds the first CCM v4.1
cross-framework mappings and a DORA reverse mapping, and rewords a large number
of specifications, almost all in punctuation.

> ## ⚠️ CSA ships this release under the label "v4.1", the same as 4.1.0
>
> The artifact page, the bundle name, and the stated release date are all
> unchanged from 4.1.0. Nothing on
> [the download page](https://cloudsecurityalliance.org/artifacts/cloud-controls-matrix-v4-1)
> says 4.1.1: it still reads "CCM v4.1", released 01/27/2026.
>
> | Where | 4.1.0 bundle | 4.1.1 bundle |
> |---|---|---|
> | Artifact page label | "CCM v4.1" | "CCM v4.1" *(unchanged)* |
> | Stated release date | 01/27/2026 | 01/27/2026 *(unchanged)* |
> | Spreadsheet filename | `CCMv4.1.0-generated_at_2026_01_13.xlsx` | `CCMv4.1.1-generated_at_2026_10_02.xlsx` |
> | Cell A1 of every sheet | `{"specification_version":"4.1.0"}` | `{"specification_version":"4.1.1"}` |
>
> The version shows **only** in the filename token and the cell A1 stamp. If
> you downloaded "CCM v4.1" before the bundle was repacked on 2026-10-06, you
> have 4.1.0; after, you have 4.1.1.
>
> **The bare labels `4.1` and `v4.1` resolve to this release.** SecID points
> them at the newest 4.1.x (ADR-015, second amendment, 2026-10-22), so this
> directory claims them in `version_aliases`. Cite `4.1.0` or `4.1.1` when the
> exact text matters.

> ## ✅ Control IDs ARE stable against 4.1.0
>
> All 207 control IDs and titles are the same as in 4.1.0, and so is every
> implementation guideline, auditing guideline, ownership cell, relevance grid
> and CCM-Lite flag, once whitespace is normalised. **A 4.1.0 control ID
> migrates to 4.1.1 by string match.** The content-matching renumbering
> detector agrees: 207 carried, 0 renumbered, 0 added, 0 removed. See
> [`CHANGES-FROM-4.1.0.md`](CHANGES-FROM-4.1.0.md#what-did-not-change).

## Everything that differs from 4.1.0

Full detail, with every reworded specification, is in
[`CHANGES-FROM-4.1.0.md`](CHANGES-FROM-4.1.0.md).

### 1. The first CCM v4.1 mappings

4.1.0's `Scope Applicability (Mappings)` sheet held one cell: "This dataset is
not available yet". 4.1.1 fills it.

| Framework | Status | Populated |
|---|---|---|
| **NIST SP 800-171 rev2** | new | 152 mapped · 55 `No Mapping` · 0 blank |
| **MITRE ATT&CK** | new (v17.1) | 57 mapped · 150 `No Mapping` · 0 blank |

`No Mapping` is a value CSA writes, not an empty cell, and it is kept verbatim.
Filter it out as well as `null` when you want "has a mapping".

**The ATT&CK block is not a compliance mapping.** Its `control_mapping` cell
lists ATT&CK technique IDs (newline-separated), its gap level only says whether
any technique is listed (`No Gap`) or none (`Full Gap`), and it has no addendum.
Don't compare its gap levels with NIST's. CSA's own disclaimer, from the
workbook's `Introduction` sheet, which this extraction does not read:

> DISCLAIMER: Please note that the ‘CCM v4.1 to MITRE ATT&CK v17.1’ mapping,
> featured in this spreadsheet, is structurally different from other CCM
> framework mappings. MITRE ATT&CK is not a compliance or control framework, it
> is a globally accessible knowledge base of adversary tactics and techniques. As
> such, this mapping identifies which ATT&CK technique IDs each CCM control
> addresses (i.e., which threats the control mitigates), rather than aligning
> control specifications to external framework requirements. For this reason,
> the mapping does not include an addendum.

The frameworks CCM v4.0 was mapped to (ISO/IEC 27001/27002/27017/27018, NIST SP
800-53 rev5, NIST CSF, PCI DSS, CIS v8, AICPA TSC and others) are **not** mapped
in 4.1.1. Those mappings exist only for v4.0, in [`../4.0.13/CSV/`](../4.0.13/CSV/),
keyed to v4.0 control IDs.

### 2. A DORA reverse mapping (new sheet)

A new `Reverse Mappings` sheet maps provisions of the EU Digital Operational
Resilience Act onto CCM controls: 215 provisions · 114 Partial Gap · 94 No Gap ·
7 Full Gap. The 7 Full Gap provisions name no CCM control; their addendum says
why. Every other provision names at least one control, and all 727 references
resolve to one of the 207 control IDs. Extracted to `reverse_mappings.dora` in
the JSON and to `ccm-4.1.1-reverse-mappings.csv`.

### 3. Reworded control text

101 of 207 control specifications differ: 92 in punctuation only and 9 in
wording. 26 of 283 CAIQ questions differ: 19 in punctuation only and 7 in
wording. The punctuation edits are mostly an added serial comma ("establish,
document, approve, communicate, apply, evaluate, and maintain"). Most wording
edits are corrections: a contraction (DSP-17, "it's" -> "its"), hyphenation
(IAM-10 "time-limited"), "meta/data" -> "metadata" (LOG-07).

> **⚠️ IAM-13 (Strong Authentication) may now say something different.** 4.1.0,
> like CCM v4.0.13 and AICM, required "multifactor authentication for **at least
> privileged user** and sensitive data access", most naturally read as MFA at
> least for privileged users. 4.1.1 reads "multifactor authentication for **a
> least-privileged user** and sensitive data access", which names a different
> population. The new text matches the wording CAIQ question IAM-13.1 already
> used in 4.1.0. Worth a question to CSA; the extraction keeps CSA's text.

The workbook's Change Log names 2 of the 127 reworded cells: DSP-17 and CCC-03.

The same 26 question changes are in the standalone questionnaire, which CSA
regenerated without changing its CAIQ 4.1.0 label. That questionnaire, with a
table of every changed question, is in
[`../../ccm-caiq/4.1.0/`](../../ccm-caiq/4.1.0/).

### 4. Sheets this extraction does not capture

`parse_ccm.py` reads six of the workbook's nine sheets. The other three changed
too:

- **`Introduction`** describes nine tabs instead of five, adds the ATT&CK
  disclaimer above, and replaces "CCM V4" with "CCM V4.1" throughout. Its CAIQ
  paragraph now says 283 questions; 4.1.0's said 261, the v4.0 count.
- **`Acknowledgments`** adds a CAIQ v4.1 contributor list and drops a "CCM v4.1
  Controls Applicability Matrix" list.
- **`Change Log`** gains the two 4.1.1 rows, and its earlier rows are
  reformatted: dates as `2025-11-01` rather than `2025/11/01`, and component
  names as `mappings`, `components`, `implementation_guidelines` and so on.

## Files

| File | What it is |
|---|---|
| `ccm-4.1.1.json` | 207 controls with guidelines, mappings and embedded CAIQ questions; `reverse_mappings.dora`; `source_data_notes` |
| `ccm-4.1.1-controls.csv` | One row per control, nested fields flattened (`mapping_nist_sp_800_171_rev2_gap_level`, …) |
| `ccm-4.1.1-reverse-mappings.csv` | One row per DORA provision; `ccm_controls` joined with `; ` |
| `ccm-4.1.1-metadata.json` | Document metadata and `known_source_issues` |
| `CHANGES-FROM-4.1.0.md` | Full change report |
| `scripts/parse_ccm.py` | The extractor; see [`scripts/README.md`](scripts/README.md) |
| `CCMv4.1.1-generated_at_2026_10_02.xlsx` | Source workbook (gitignored; in S3) |

JSON keys for the mapping blocks are `nist_sp_800_171_rev2` and `mitre_attack`.

## Rebuilding

```bash
cd scripts
./parse_ccm.py --input ../CCMv4.1.1-generated_at_2026_10_02.xlsx
python3 ../../check_figures.py
```

`../check_figures.py` recomputes every figure quoted here and in
`CHANGES-FROM-4.1.0.md` from the committed data, and exits 1 if any disagree.
