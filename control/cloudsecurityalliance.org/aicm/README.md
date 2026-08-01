# CSA AI Controls Matrix (AICM)

`secid:control/cloudsecurityalliance.org/aicm`

CSA's AI security controls catalog — the AI-specific companion to the Cloud
Controls Matrix. Current release is **1.1.0**.

> ## "AICM 1.1" and "AICM 1.1.0" are the same release
>
> CSA labels the current release two ways and both are in circulation:
>
> | Where | String |
> |---|---|
> | Cell A1 of every worksheet | `{"specification_version":"1.1.0"}` |
> | Spreadsheet filename | `AICMv1.1.0-generated_at_2026_06_18.xlsx` |
> | CSA artifact / download page | "AI Controls Matrix **v1.1**" |
> | Bundle ZIP and PDF titles | "AICM **v1.1**" |
>
> **This repo uses `1.1.0` as canonical and aliases `1.1` to it.** The artifact's
> own internal version stamp wins over the download page — it is what a consumer
> parsing the file actually encounters, and it keeps the version sort stable
> against the sibling releases `1.0.3` and `0.0.2`.
>
> So `AICM 1.1`, `AICM v1.1`, and `AICM 1.1.0` all mean [`1.1.0/`](1.1.0/).
> Recorded machine-readably as `version_aliases` in the metadata.
>
> This is a **labelling** alias. It says nothing about compatibility — see the
> next box, which is the opposite situation.

> ## ⚠️ Control IDs are not stable between 1.0.3 and 1.1.0
>
> CSA renumbered controls in place in 1.1.0. **55 of the 242 control IDs shared
> between the two releases now designate a different control.**
>
> | ID | means in 1.0.3 | means in 1.1.0 |
> |---|---|---|
> | `LOG-15` | Output Monitoring | **Input Monitoring** |
> | `IAM-12` | Safeguard Logs Integrity | **Unique Identities** |
> | `TVM-12` | Threat Analysis and Modelling | **Vulnerability Management Metrics** |
>
> Only one ID disappeared outright, so a set-difference of control IDs does *not*
> detect this. Never migrate a reference between versions by string match — use
> the crosswalk.
>
> **Always cite AICM control IDs with a version.** `AICM 1.1.0 LOG-15`, never
> `AICM LOG-15`.
>
> Full analysis and standing policy: [`VERSIONING.md`](VERSIONING.md)

## Versions

| Version | Controls | Released | State | Notes |
|---|---:|---|---|---|
| [`1.1.0/`](1.1.0/) | 247 | 2026-06-22 | **current** | Aliases: 1.1, v1.1. Renumbered IDs. NIST AI 600-1 mappings withdrawn. |
| [`1.0.3/`](1.0.3/) | 243 | 2025-11-10 | superseded | Last release carrying NIST AI 600-1 mappings. |
| [`0.0.2/`](0.0.2/) | — | — | pre-release draft | Early working draft. |

## Also here

| Path | What |
|---|---|
| [`VERSIONING.md`](VERSIONING.md) | What changed between releases, why ID-based diffs miss it, why the SecID version qualifier is load-bearing, and standing policy for future releases |
| [`crosswalks/`](crosswalks/) | Content-based 1.0.3 → 1.1.0 control-ID crosswalk plus the generator that builds it |

## Companions

| | |
|---|---|
| [`../aicm-caiq/`](../aicm-caiq/) | AI-CAIQ — the vendor self-assessment questionnaire derived from AICM. Versions in lockstep and inherits the ID-renumbering problem, since question IDs derive from control IDs. |
| [`../ccm/`](../ccm/) | Cloud Controls Matrix — the general cloud-security controls AICM layers on top of. Use both together for AI workloads in cloud. |

Guidance documents shipped in the AICM v1.1 bundle are extracted under
`reference/cloudsecurityalliance.org/`:
[introductory guidance](../../../reference/cloudsecurityalliance.org/aicm-introductory-guidance/v1.1/),
[AI-CAIQ instructions](../../../reference/cloudsecurityalliance.org/ai-caiq-instructions/v1.1/),
[STAR for AI L1 submission guide](../../../reference/cloudsecurityalliance.org/star-for-ai-level-1-submission-guide/v1.1/).
