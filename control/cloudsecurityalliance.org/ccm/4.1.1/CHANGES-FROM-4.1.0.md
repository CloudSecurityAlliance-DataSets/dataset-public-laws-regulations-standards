# CCM 4.1.0 → 4.1.1: what changed

A full account of the differences between the two CCM v4.1 workbooks CSA has
served under the same "CCM v4.1" label:
`CCMv4.1.0-generated_at_2026_01_13.xlsx` and
`CCMv4.1.1-generated_at_2026_10_02.xlsx`.

Every count below that describes the extracted data is recomputed from the
committed JSON by [`../check_figures.py`](../check_figures.py), which exits 1 if
any figure here disagrees with the data. The workbook-level cell counts under
[Method](#method) are the exception: the source workbooks are gitignored, so
those are not machine-checked.

## Bottom line

A patch release. All 207 control IDs and titles carry over unchanged, and
nothing was renumbered: a 4.1.0 control ID names the same control in 4.1.1.

| | Change | Weight |
|---|---|---|
| 1 | **First CCM v4.1 cross-framework mappings**: NIST SP 800-171 rev2 and MITRE ATT&CK v17.1 | the substance of the release |
| 2 | **A DORA reverse mapping**, in a new sheet | new, and useful to financial entities |
| 3 | **Reworded control text**, almost all punctuation | wide but shallow; one edit (IAM-13) may change meaning |
| 4 | **Edits to sheets this repo does not extract** | small; one disclaimer matters |

**Not announced.** CSA replaced the workbook inside the "CCM v4.1" bundle
without changing the bundle name, the artifact-page version label, or the
stated release date of 01/27/2026. The only outward signals are the filename
version token and the JSON stamp in cell A1. The bundle was repacked on
2026-10-06; anyone who downloaded "CCM v4.1" before then holds 4.1.0.

**The Change Log understates the edits.** It records the new mappings and two
text fixes, DSP-17 and CCC-03. Compared field by field, the Change Log names 2 of
the 127 reworded texts: 101 of 207 control specifications differ: 92 in
punctuation only and 9 in wording, and 26 of 283 CAIQ questions differ: 19 in
punctuation only and 7 in wording. Each specification also appears in the
Implementation Guidelines, Auditing Guidelines and CAIQ sheets, so the 127
texts account for 430 of the differing cells counted under [Method](#method).

---

## Method

Two passes, which agree.

1. **Extraction diff.** Every field of every control in `ccm-4.1.0.json` and
   `ccm-4.1.1.json`, compared after whitespace normalisation. CSA regenerated
   the workbook and moved line breaks inside hundreds of cells without changing
   their words, so un-normalised text differs in many more places than the
   wording does. This is the pass `../check_figures.py` repeats on every run.
2. **Workbook diff.** Every cell of every worksheet, whitespace-normalised and
   compared by position. This pass sees sheets the extraction does not read.

**Two definitions** are used throughout:

- *Normalised*: whitespace runs collapsed to one space, ends stripped.
- *Punctuation only*: the two texts are equal once whitespace, commas,
  semicolons and full stops are removed and case is ignored. Anything else,
  including a changed apostrophe or a new hyphen, counts as a wording change.

### Cell accounting

Not machine-checked (the workbooks are gitignored); counted on 2026-10-23 with
`openpyxl` in full-load mode. Read-only mode trusts each sheet's stored
dimension tag, which stops at column D here, and silently undercounts.

| Sheet | Differing cells | What they are |
|---|---:|---|
| `Introduction` | 67 | rewritten for v4.1 (see §4); most are rows shifted by inserted lines |
| `CCM` | 3,210 | 3,105 relevance-grid cells re-typed (below), 101 specifications, 2 version stamps, 1 column header, 1 copyright line |
| `Implementation Guidelines` | 105 | 101 specifications (repeated from `CCM`), 2 stamps, 1 header, 1 copyright line |
| `Auditing Guidelines` | 104 | 101 specifications, 2 stamps, 1 copyright line |
| `Scope Applicability (Mappings)` | 1,896 | all new content; 4.1.0 held one cell |
| `Reverse Mappings` | 1,111 | new sheet |
| `CAIQ` | 129 | 101 specifications, 26 questions, 1 stamp, 1 copyright line |
| `Acknowledgments` | 45 | contributor lists (see §4) |
| `Change Log` | 84 | two new rows, and every older row reformatted (see §4) |
| **Total** | **6,751** | |

**The 3,105 re-typed cells change no data.** The architectural- and
organizational-relevance grids (15 columns × 207 controls) were stored as
spreadsheet booleans in 4.1.0 and as the strings `"true"` / `"false"` in 4.1.1.
The parser maps both to the same JSON booleans, which is why the extracted grids
are identical.

The column header that changed reads "Typical Control Applicability and
Ownership" in 4.1.0 and "Typical Control Applicability and Ownership
(IaaS/PaaS/SaaS)" in 4.1.1.

---

## 1. The first CCM v4.1 mappings

4.1.0's `Scope Applicability (Mappings)` sheet held one cell: "This dataset is
not available yet". 4.1.1 fills it with two framework blocks, each a Control
Mapping, Gap Level and Addendum column per control.

### Coverage

| Framework | Mapped | `No Mapping` | Blank |
|---|---:|---:|---:|
| NIST SP 800-171 rev2 | 152 | 55 | 0 |
| MITRE ATT&CK v17.1 | 57 | 150 | 0 |

### Gap levels

| Framework | Partial Gap | No Gap | Full Gap |
|---|---:|---:|---:|
| NIST SP 800-171 rev2 | 98 | 54 | 55 |
| MITRE ATT&CK v17.1 | 0 | 57 | 150 |

### `No Mapping` is a value, not an absence

Both blocks write the literal `No Mapping` where there is no counterpart, and
pair it with `Full Gap`. The extraction keeps the string: CSA stating "we looked
and there is nothing" is a different fact from an empty cell. No mapping cell in
either block is empty. To select controls that have a mapping, exclude
`"No Mapping"` as well as `null`.

### The ATT&CK block is a threat-coverage list

Its Control Mapping cell holds newline-separated technique IDs (for example
AIS-02 lists eleven, from `T1496.004` to `T1648`), its gap level is `No Gap`
exactly when a technique is listed, and its Addendum is always empty. So
`Full Gap` there means "this control addresses no ATT&CK technique", not "this
control falls short of a requirement", and ATT&CK gap counts should not be read
alongside NIST's. CSA says the same in the `Introduction` sheet, which the
extraction does not read:

> DISCLAIMER: Please note that the ‘CCM v4.1 to MITRE ATT&CK v17.1’ mapping,
> featured in this spreadsheet, is structurally different from other CCM
> framework mappings. MITRE ATT&CK is not a compliance or control framework, it
> is a globally accessible knowledge base of adversary tactics and techniques. As
> such, this mapping identifies which ATT&CK technique IDs each CCM control
> addresses (i.e., which threats the control mitigates), rather than aligning
> control specifications to external framework requirements. For this reason,
> the mapping does not include an addendum.

### What is still not mapped

None of the frameworks CCM v4.0 was mapped to is mapped for 4.1: ISO/IEC
27001/27002/27017/27018, NIST SP 800-53 rev5, NIST CSF, PCI DSS, CIS v8, AICPA
TSC, ENX ISA, ISF SOGP and CCM v3.0.1. Those mappings exist only for v4.0, in
[`../4.0.13/CSV/`](../4.0.13/CSV/), keyed to v4.0 control IDs.

---

## 2. A DORA reverse mapping

A new `Reverse Mappings` sheet runs the other way from the mappings above: it
takes each provision of the EU Digital Operational Resilience Act (Regulation
(EU) 2022/2554) and names the CCM controls that cover it. Columns: Source
Reference(s), Source Description, CCM Controls, Gap Level, Addendum, Analysis.

215 provisions · 114 Partial Gap · 94 No Gap · 7 Full Gap. References run from
Article 4(1) (`A4.1`) to Article 45(3) (`A45.3`). Together the provisions cite
CCM controls 727 times, and every reference resolves to one of the 207 control
IDs.

The 7 Full Gap provisions name no CCM control. Their addendum says why:

| Provision | Addendum |
|---|---|
| `A10.4` | The full DORA provision is missing from CCM v4.1 and has to be used to close the gap. |
| `A16.1` | DORA provision out of scope of cybersecurity. |
| `A27.2a)` | The full DORA provision is missing from CCM v4.1 and has to be used to close the gap. |
| `A27.2b)` | The full DORA provision is missing from CCM v4.1 and has to be used to close the gap. |
| `A27.2c)` | The full DORA provision is missing from CCM v4.1 and has to be used to close the gap. |
| `A27.3` | The full DORA provision is missing from CCM v4.1 and has to be used to close the gap. |
| `A45.3` | The full DORA provision is missing from CCM v4.1 and has to be used to close the gap. |

In the JSON they carry `ccm_controls: []`. The CCM Controls cell is empty in
CSA's workbook; that is a statement by CSA, not a conversion loss.

---

## 3. Reworded control text

### Specifications

101 of 207 control specifications differ: 92 in punctuation only and 9 in
wording. Nearly all of the punctuation edits add a serial comma, for example
"Establish, document, approve, communicate, apply, evaluate**,** and maintain".

The 9 wording changes, word by word:

| Control | Title | Change |
|---|---|---|
| `CCC-06` | Change Management Baseline | "document" → "document,"; "organization" → "organizational" |
| `DCS-06` | Assets Classification | "physical," → "physical"; "assets’" → "assets'" (curly to straight apostrophe) |
| `DSP-17` | Sensitive Data Protection | "procedures" → "procedures,"; "it's" → "its" |
| `IAM-10` | Management of Privileged Access Roles | "time limited" → "time-limited" |
| `IAM-12` | Unique Identities | serial commas; "identities’" → "identities'" |
| `IAM-13` | Strong Authentication | serial commas; "application" → "applications,"; **"at least privileged" → "a least-privileged"** |
| `LOG-07` | Logging Scope | "document" → "document,"; "meta/data" → "metadata" |
| `STA-11` | Primary Service and Contractual Agreement | "mutually-agreed" → "mutually agreed"; "third party" → "third-party"; "Resilience" → "resilience"; a serial comma |
| `TVM-06` | External Library Vulnerabilities | serial commas; "third party" → "third-party" |

### IAM-13 ⚠️ worth a question to CSA

In 4.1.0, as in CCM v4.0.13 and AICM, IAM-13 reads:

> …including multifactor authentication for **at least privileged user** and
> sensitive data access.

4.1.1 reads:

> …including multifactor authentication for **a least-privileged user** and
> sensitive data access.

The first is most naturally read as "MFA, at least for privileged users"; the
second names a least-privileged user, a different population. The new text
matches CAIQ question IAM-13.1, which already said "a least-privileged user" in
4.1.0, so CSA may have aligned the control to the question rather than the
other way round. The Change Log does not mention IAM-13. The extraction keeps
CSA's text. Recorded as `known_source_issues/iam-13-mfa-wording-changed`.

### The two edits the Change Log names

- **DSP-17**: "it's lifecycle" → "its lifecycle", as logged (plus a serial
  comma, not logged).
- **CCC-03**: the redundant comma after "assets" is removed, as logged, and a
  serial comma is added after "controlled". The matching CAIQ question CCC-03.1
  still has the comma after "assets": "…applying changes to assets, owned,
  controlled, or used by the organization?"

### CAIQ questions

26 of 283 CAIQ questions differ: 19 in punctuation only and 7 in wording. The
same 26 changes are in the standalone questionnaire, which CSA regenerated
without changing its 4.1.0 label. Every changed question, with both texts, is
tabled in [`../../ccm-caiq/4.1.0/README.md`](../../ccm-caiq/4.1.0/README.md).
One of them matters: in **DCS-11.1** the dropped words "and surveillance
systems" leave the question asking about one of the two locations its control
names.

---

## 4. Changes to sheets this repo does not extract

`parse_ccm.py` reads `CCM`, `Implementation Guidelines`, `Auditing Guidelines`,
`Scope Applicability (Mappings)`, `Reverse Mappings` and `CAIQ`.

### `Introduction`

- Describes the spreadsheet as having nine tabs (4.1.0: five), and adds bullets
  for "CCM Reverse Mapping (DORA)" and "Change Log".
- Replaces "CCM V4" with "CCM V4.1" in each tab description, and fixes the
  Auditing Guidelines paragraph, which in 4.1.0 began "This tab includes the CCM
  V4 Implementation Guidelines".
- The mappings paragraph now cites "NIST 800-171 rev 2., ISO 27001/17/18 etc."
  instead of "ISO 27001/2/17 … CIS V8".
- Adds the ATT&CK disclaimer quoted in §1.
- The CAIQ paragraph now says 283 questions. In 4.1.0 it said 261, the v4.0
  count.

### `Acknowledgments`

The header reads "CCM v4.1 | CAIQ v4.1" where it read "CCM v4.1 | CCM v4.1
Controls Applicability Matrix". A CAIQ v4.1 contributor list replaces the
Controls Applicability Matrix list, and one name is added to another list.
(Names are not reproduced here.)

### `Change Log`

Two rows added, both "CCM v4.1.1 | 2026-10-01": one for the mappings, one for
the DSP-17 and CCC-03 fixes. Every older row is reformatted: dates as
`2025-11-01` rather than `2025/11/01`, and the component column uses
`mappings`, `components`, `implementation_guidelines`, `auditing_guidelines`
and `assessment_questionnaire` where 4.1.0 used `Mapping`, `Control`,
`Guidelines`, `CAIQ` and `Relation`.

---

## What did not change

Field by field, after whitespace normalisation, these are identical for every
control: `control_title`, `implementation_guidelines`, `auditing_guidelines`,
`typical_control_applicability_and_ownership`,
`architectural_relevance_cloud_stack_components`, `organizational_relevance`
and `ccm_lite`. All 207 control IDs carry over, with none added or removed.
`../check_figures.py` asserts each of these as an invariant.

### Checked with the renumbering detector, not only by ID

"No IDs moved" is the claim that was false for AICM 1.0.3 → 1.1.0, in a way a
set-difference of IDs could not see. So this release was also run through
[`../../aicm/crosswalks/build_crosswalk.py`](../../aicm/crosswalks/build_crosswalk.py),
which matches controls by content and ignores the identifier. It reads the
committed CCM JSON unchanged:

```
python3 control/cloudsecurityalliance.org/aicm/crosswalks/build_crosswalk.py \
  --old control/cloudsecurityalliance.org/ccm/4.1.0/ccm-4.1.0.json \
  --new control/cloudsecurityalliance.org/ccm/4.1.1/ccm-4.1.1.json \
  --old-version 4.1.0 --new-version 4.1.1 --output /tmp/ccm-crosswalk.csv
```

| | Count |
|---|---:|
| Carried | 207 |
| Renumbered (ID moved) | 0 |
| Added / removed | 0 / 0 |
| Matched on identical specification text (`exact-spec`) | 106 |
| Matched on unchanged ID and title (`same-id+title`) | 101 |
| Rows needing human review | 0 |

(The script's summary line says "AICM"; its label is hard-coded.)

**Why the detector says "6 substantive" and this report says "9 in wording".**
The detector also grades each carried specification by character similarity,
and calls six `spec-substantive`: CEK-15, CEK-16, CEK-18, CEK-19, IAM-13 and
SEF-07, with similarity between 0.836 and 0.879. Five of those six gained only
serial commas; on long specifications with many commas, a character-level
ratio drops below the detector's threshold for punctuation alone. Only IAM-13
is a wording change on both measures. This report uses the word-level
definition under [Method](#method).

---

## Version labelling

- **In this repo:** 4.1.0 is in [`../4.1.0/`](../4.1.0/), which was `ccm/4.1/`
  until 2026-10-23, and 4.1.1 is here. This directory's `version_aliases`
  claims `4.1` and `v4.1`.
- **In SecID:** CCM gained version nodes in ADR-015's second amendment
  (2026-10-22). `ccm@4.1` and `ccm@v4.1` resolve to 4.1.1, `ccm@4.1.0` to 4.1.0,
  and `ccm@4.0.13` to `ccm@4.0`.
- **csa-mcp:** CSA's own server labels its CCM 4.1 data "4.1" and, as of
  2026-10-22, holds 4.1.0 with "cross-framework mappings PENDING upstream".
  Until it loads 4.1.1, `ccm 4.1` names different releases in csa-mcp and in
  SecID.

## Reproducing

```bash
cd control/cloudsecurityalliance.org/ccm
(cd 4.1.0/scripts && python3 parse_ccm.py)   # reproduces ../ccm-4.1.0.json byte for byte
(cd 4.1.1/scripts && python3 parse_ccm.py --input ../CCMv4.1.1-generated_at_2026_10_02.xlsx)
python3 check_figures.py
```

Both workbooks are in
`s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/ccm/<version>/`.
`parse_ccm.py` needs pandas and openpyxl; for example,
`uv run --no-project --with pandas --with openpyxl python parse_ccm.py …`.

## References

- CSA artifact page: https://cloudsecurityalliance.org/artifacts/cloud-controls-matrix-v4-1
- Bundle download (no account required): https://cloudsecurityalliance.org/download/artifacts/cloud-controls-matrix-v4-1
- Machine-readable bundle, still 4.1.0: https://cloudsecurityalliance.org/artifacts/ccm-machine-readable-bundle-json-yaml-oscal
- [`ccm-4.1.1-metadata.json`](ccm-4.1.1-metadata.json), `known_source_issues`
- [`../../ccm-caiq/4.1.0/README.md`](../../ccm-caiq/4.1.0/README.md), the 26 changed questions
