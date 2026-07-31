# AICM v1.0.3

`secid:control/cloudsecurityalliance.org/aicm@1.0.3` · 243 controls · 18 domains · published 2025-11-10

**Superseded by [AICM v1.1.0](../1.1.0/) (released 2026-06-22).**

> ## ⚠️ Control IDs changed meaning in v1.1.0
>
> **These control IDs are not interchangeable with v1.1.0 control IDs.**
>
> CSA renumbered controls in place in the next release. **55 of the 242 control
> IDs this version shares with v1.1.0 designate a different control there.** The
> identifier string survived; what it points at did not.
>
> | ID | means here (v1.0.3) | means in v1.1.0 |
> |---|---|---|
> | `LOG-15` | Output Monitoring | **Input Monitoring** |
> | `IAM-12` | Safeguard Logs Integrity | **Unique Identities** |
> | `TVM-12` | Threat Analysis and Modelling | **Vulnerability Management Metrics** |
>
> Two consequences:
>
> - **Anything you cite from this directory must say "AICM 1.0.3" explicitly.** A
>   bare `AICM LOG-15` is ambiguous and will be read against whatever version the
>   reader has to hand.
> - **You cannot upgrade a reference to v1.1.0 by string match.** Use
>   [`../crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv`](../crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv).
>
> Full analysis: [`../VERSIONING.md`](../VERSIONING.md)

## Why this version is retained

Superseded, but not obsolete:

- **Assessments authored against v1.0.3 resolve here.** Their control IDs mean
  what this directory says they mean, not what v1.1.0 says.
- **NIST AI 600-1:2024 mappings exist only here.** v1.1.0 withdrew them — its
  Scope Applicability sheet carries only BSI AI C4, the EU AI Act, and ISO/IEC
  42001:2023. This is the last AICM release with the NIST mapping set, populated
  for all 243 controls.

## Contents

| File | What |
|---|---|
| `aicm-1.0.3.json` | Full extraction — 243 controls with guidelines, four-framework mappings, and AI-CAIQ questions |
| `aicm-1.0.3-metadata.json` | Document metadata and licence |
| `scripts/parse_aicm.py` | Original extraction script — **v1.0.3 only, does not run against v1.1.0** |
| `scripts/parse_caiq.py` | Original questionnaire script — **v1.0.2 only** |

The scripts in this directory are pinned to this release's layout: they hardcode
four mapping frameworks and the sheet name `AI-CAIQv1.0.2`. For v1.1.0 use
[`../1.1.0/scripts/`](../1.1.0/scripts/), which discovers both from the workbook.

## Known extraction gap

`parse_llm_taxonomy` in this directory reads only the lifecycle section of the
LLM Taxonomy sheet. The Control Type, Control Ownership, and Threat Category
definition sections are present in the source workbook but absent from
`aicm-1.0.3.json`. Fixed in the [v1.1.0 parser](../1.1.0/scripts/parse_aicm.py);
not backported.
