# Phase 0 Triage: `control/` extracted-but-unstructured docs

Triage of 112 documents currently in `control/` (state = `extracted`, no per-control CSV/JSON yet). For each doc we decided whether it should be structured in place, reclassified to another SecID type (mostly `reference/`), or dropped as withdrawn/superseded.

Companion CSV: `tools-resources/working/control-extraction-triage.csv`

## Counts by decision

| Decision | Count |
|---|---:|
| `reclassify-reference` | 97 |
| `structure` | 11 |
| `reclassify-methodology` | 3 |
| `drop` | 1 |
| **Total** | **112** |

The dominant outcome is reclassification: only ~10% of the docs currently sitting in `control/` are actual control catalogs. The rest are guidance, templates, white papers, algorithm specs, or methodologies.

## Counts by publisher

| Publisher | structure | reclassify-reference | reclassify-methodology | drop | Total |
|---|---:|---:|---:|---:|---:|
| `fedramp.gov` | 4 | 36 | 1 | 0 | 41 |
| `nist.gov` | 6 | 60 | 2 | 1 | 69 |
| `openai.com` | 0 | 1 | 0 | 0 | 1 |
| `pcisecuritystandards.org` | 1 | 0 | 0 | 0 | 1 |
| **Total** | **11** | **97** | **3** | **1** | **112** |

## The 11 `structure` candidates, grouped by parser family

| `structure_family` | Docs | Notes |
|---|---|---|
| `fedramp-baseline` (4) | `ssp-appendix-a-high-fedramp-security-controls`, `ssp-appendix-a-li-saas-fedramp-security-controls`, `ssp-appendix-a-low-fedramp-security-controls`, `ssp-appendix-a-moderate-fedramp-security-controls` | FedRAMP control baselines (Low/Mod/High/LI-SaaS). Each control has a "Control Summary Information" block. Build one parser used for all four. |
| `nist-nice` (1) | `nist.gov/800-181` | NICE Framework — Task / Knowledge / Skill / Competency / Work-Role taxonomy. |
| `nist-ssdf-ai` (1) | `nist.gov/800-218a` | SSDF AI Community Profile. Shares the Practice/Task schema with the already-structured 800-218; reuse that parser with the AI columns. |
| `fips-categorization` (1) | `nist.gov/fips-199` | Small three-tier C/I/A impact categorization table. One-off but trivial. |
| `pci-dss` (1) | `pcisecuritystandards.org/pci-dss/v4.0` | Previous PCI DSS version. The v4.0.1 parser (`parse_pci_dss.py`) is likely reusable directly. See "Note on PCI DSS v4.0" below. |
| `one-off` (3) | `nist.gov/800-213a` (IoT capability catalog with DI/DC/DP/LA/SU codes), `nist.gov/fips-140/2`, `nist.gov/fips-140/3` (crypto-module requirements per Level 1–4) | Three docs with bespoke shapes. 800-213a is a clean win. FIPS 140-2 has tiered Level requirements that are structurable. FIPS 140-3 normatively references ISO/IEC 19790 and is mostly delta — see note below. |

## Reclassification destinations

### `reclassify-methodology` (3)
Process documents, not control catalogs:
- `nist.gov/800-30` (Guide for Conducting Risk Assessments) → `secid:methodology/nist.gov/800-30`
- `nist.gov/800-39` (Managing Information Security Risk, three-tier RM process) → `secid:methodology/nist.gov/800-39`
- `fedramp.gov/threat-based-risk-profiling-methodology` (FedRAMP threat-based risk-profiling methodology, phase-based scoring process) → `secid:methodology/fedramp.gov/threat-based-risk-profiling-methodology`

### `drop` (1)
- `nist.gov/fips-197` — top of the markdown is the official NIST "Withdrawn NIST Technical Series Publication" notice. Superseded by FIPS 197-upd1 in 2023. No 197-upd1 directory exists in this list, so this is purely a stale withdrawn copy to remove (not a parser-reuse situation).

### `reclassify-reference` (97)
The big bucket. Everything else: FedRAMP playbooks/guides/templates/forms, NIST 800-series guidance prose, FIPS algorithm specifications, NCCoE 1800 practice guides, OpenAI Preparedness Framework. Target SecID is `secid:reference/{namespace}/{name}[/version]` for each (preserved in the CSV `target_secid` column).

## Confidence

- `high`: 105 / 112
- `medium`: 7 / 112
- `low`: 0 / 112

Nothing was rated `low`. The 7 `medium` rows are listed below — all should be sanity-checked by a human before action.

### Medium-confidence rows requiring human review

| Path | Decision | Why medium |
|---|---|---|
| `control/nist.gov/800-61/r2/` | `reclassify-reference` | Incident Handling Guide has a regular preparation/detection/containment/recovery phase structure. Could be argued as `reclassify-methodology`. Leaned `reference` because the document is a well-known prose guide, not a numbered methodology spec. |
| `control/nist.gov/800-63/3/` | `reclassify-reference` | This is the 800-63 overview/umbrella document. Its three companions (800-63A, B, C) are already structured per CLAUDE.md. The overview itself is prose. |
| `control/nist.gov/fips-140/2/` | `structure` | FIPS 140-2 spec has Level 1–4 requirements per module aspect. The shape is structurable (one row per (module aspect, level)) but the parsing surface is small relative to the prose around it. If a parser is too costly, this could be reclassified to `reference`. |
| `control/nist.gov/fips-140/3/` | `structure` | FIPS 140-3 normatively defers to ISO/IEC 19790:2012(E) and ISO/IEC 24759:2017(E) (ISO can't be redistributed) — the FIPS 140-3 document body is mostly references and a thin US delta. Structurable rows are limited to the delta. If on inspection the delta is too sparse, reclassify to `reference`. |
| `control/nist.gov/fips-201/` | `reclassify-reference` | PIV credential standard. Has detailed spec sections but is a specification not a control catalog (closer to a technology spec). |
| `control/openai.com/preparedness/` | `reclassify-reference` | Risk-category framework with four tracked categories (cyber/CBRN/persuasion/autonomy) and scorecard levels. Not a per-control catalog; closer to a policy/playbook. Could conceivably be `methodology` or its own type later. |
| `control/pcisecuritystandards.org/pci-dss/v4.0/` | `structure` | The newer v4.0.1 is already structured; v4.0 is the older baseline. The `parse_pci_dss.py` parser in the v4.0.1 directory is reusable. Marked `structure` to preserve v4.0 as a historical row-set, but a defensible alternative is `drop` since v4.0.1 supersedes it in production use. See note below. |

## Note on PCI DSS v4.0

The task brief flagged this as a candidate for `drop` (since v4.0.1 is structured) but also acknowledged it might be Phase 1 parser-reuse. I chose `structure` (family `pci-dss`) because: (a) the v4.0.1 `parse_pci_dss.py` should require zero or trivial changes against v4.0's nearly-identical schema, (b) consumers comparing two versions benefit from having both row-sets, and (c) "drop" implies removing files, which is more destructive than structuring. If you'd rather drop it, the CSV is one row-edit away.

## Methodology

For each of the 112 paths the bot:

1. Read `*-metadata.json` to extract `secid`, `name`, `description`, lifecycle status.
2. If present, read the `README.md` (typically a 5–10 line orientation summary the previous bulk processor wrote).
3. Scanned the first ~30 markdown headings (`grep -E '^#'`) of the main `*.md` file looking for:
   - "WITHDRAWN" notice (signals `drop`)
   - `<Insert ...>` placeholders (signals `reclassify-reference`, template)
   - Per-control identifier patterns (`AC-1`, `PR.1.1`, `Practice PO.1`, `(DI)`, etc.) signaling structurable shape
   - Section-level numeric headings only (`1.0 Purpose`, `2.0 Scope` …) signaling prose `reclassify-reference`
   - Phase / step / process language in the title signaling `reclassify-methodology`
4. For ambiguous cases (FedRAMP SSP Appendix A, FIPS 140-2/3, FIPS 199, 800-181, 800-213a, 800-218a, 800-61), read deeper into the body to confirm whether the control structure is real (e.g. counted `**AC-N Control Summary Information**` blocks in SSP Appendix A High → many, confirming the per-control row shape).

Decisions were grouped by publisher rather than per-doc to limit reads — 41 FedRAMP docs were classified as a single batch once the FedRAMP corpus shape (templates / playbooks / guidance, with 4 Appendix-A baseline exceptions) was visible; 12 FIPS docs were classified as one batch (algorithm specs → reference; FIPS 199 / 140-x → structure); 57 NIST SP docs were classified by README + heading scan.

## What was NOT done (per task brief)

- No files were moved, edited, or deleted under `control/`.
- No extractor scripts were written.
- No git commits made.
- No new SecID identifiers were invented for ambiguous cases — all `target_secid` values are direct `control` → `reference` / `methodology` rewrites using the existing namespace and name segments.
