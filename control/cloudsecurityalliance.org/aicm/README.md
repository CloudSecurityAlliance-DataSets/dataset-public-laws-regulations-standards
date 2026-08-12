# CSA AI Controls Matrix (AICM)

`secid:control/cloudsecurityalliance.org/aicm`

CSA's AI security controls catalog — the AI-specific companion to the Cloud
Controls Matrix. Current release is **1.1.1**.

> ## ⚠️ "AICM v1.1" is ambiguous — it names two different datasets
>
> CSA published **1.1.1** on 2026-07-13 through the same artifact page, the same
> bundle name, and the same "AI Controls Matrix v1.1" label as 1.1.0, without
> updating the stated release date. Both releases are branded "v1.1" upstream.
>
> | Where | 1.1.0 bundle | 1.1.1 bundle |
> |---|---|---|
> | CSA artifact / download page | "AI Controls Matrix **v1.1**" | "AI Controls Matrix **v1.1**" *(unchanged)* |
> | Stated release date | 06/22/2026 | 06/22/2026 *(unchanged)* |
> | Bundle ZIP and PDF titles | "AICM **v1.1**" | "AICM **v1.1**" *(unchanged)* |
> | Spreadsheet filename | `AICMv1.1.0-generated_at_2026_06_18.xlsx` | `AICMv1.1.1-generated_at_2026_07_22.xlsx` |
> | Cell A1 of every worksheet | `{"specification_version":"1.1.0"}` | `{"specification_version":"1.1.1"}` |
>
> The version is discoverable only from the filename token and the cell A1 stamp.
> Downloaded before roughly 2026-07-22 → 1.1.0. After → 1.1.1.
>
> **This repo uses the workbook's own internal stamp as canonical**, so the two
> live in [`1.1.0/`](1.1.0/) and [`1.1.1/`](1.1.1/). The bare aliases `1.1` and
> `v1.1` are claimed by **neither** — `1.1.0/` held them until 1.1.1 shipped and
> has since given them up, because they no longer resolve to one dataset.
>
> **Cite `AICM 1.1.0` or `AICM 1.1.1`. A bare "AICM v1.1" citation cannot be
> resolved to an extraction.**
>
> All of the above is **labelling**. For compatibility, 1.1.0 → 1.1.1 is safe
> (identical control IDs) and 1.0.3 → 1.1.x is not — see the next box.

> ## ⚠️ Control IDs are not stable between 1.0.3 and 1.1.x
>
> CSA renumbered controls in place in 1.1.0, and 1.1.1 inherits that numbering
> unchanged. **54 of the 242 control IDs shared between 1.0.3 and 1.1.x now
> designate a different control.**
>
> | ID | means in 1.0.3 | means in 1.1.x |
> |---|---|---|
> | `LOG-15` | Output Monitoring | **Input Monitoring** |
> | `IAM-12` | Safeguard Logs Integrity | **Unique Identities** |
> | `TVM-12` | Threat Analysis and Modelling | **Vulnerability Management Metrics** |
>
> Only one ID disappeared outright, so a set-difference of control IDs does *not*
> detect this. Never migrate a 1.0.3 reference forward by string match — use
> the crosswalk.
>
> **1.1.0 → 1.1.1 is the exception: IDs are stable there** and migrate by string
> match. 1.1.1 is a patch release that touches no control identity.
>
> **Always cite AICM control IDs with a version.** `AICM 1.1.1 LOG-15`, never
> `AICM LOG-15`.
>
> Full analysis and standing policy: [`VERSIONING.md`](VERSIONING.md)

## Versions

| Version | Controls | Released | State | Notes |
|---|---:|---|---|---|
| [`1.1.1/`](1.1.1/) | 247 | 2026-07-13 | **current** | Patch over 1.1.0 — same control IDs. Adds AIUC-1 + NIST AI RMF/600-1 mappings; corrects 3 MP guidelines and 1 CAIQ question. Shipped unannounced under the "v1.1" label. |
| [`1.1.0/`](1.1.0/) | 247 | 2026-06-22 | superseded | Renumbered IDs vs 1.0.3. NIST mappings withdrawn (restored in 1.1.1). |
| [`1.0.3/`](1.0.3/) | 243 | 2025-11-10 | superseded | Last release before the renumbering. |
| [`0.0.2/`](0.0.2/) | — | — | pre-release draft | Early working draft. |

Neither 1.1.x directory claims the bare `1.1` / `v1.1` alias — see the box above.

## Also here

| Path | What |
|---|---|
| [`VERSIONING.md`](VERSIONING.md) | What changed between releases, why ID-based diffs miss it, why the SecID version qualifier is load-bearing, and standing policy for future releases |
| [`1.1.0/aicm-1.1.0-changelog.json`](1.1.0/aicm-1.1.0-changelog.json) | **Per-control changelog, machine-readable** — `previous_id`, `changes[]`, `spec_similarity`, `id_reuse` per control |
| [`1.1.0/CHANGELOG.md`](1.1.0/CHANGELOG.md) | The same for reading, plus the JSON's schema |
| [`1.1.1/CHANGES-FROM-1.1.0.md`](1.1.1/CHANGES-FROM-1.1.0.md) | **1.1.0 → 1.1.1 change report** — complete before/after text of every changed cell, mapping coverage by domain, and why no crosswalk is needed |
| [`crosswalks/`](crosswalks/) | Content-based 1.0.3 → 1.1.0 control-ID crosswalk and the generators for it and the changelog |

## Companions

| | |
|---|---|
| [`../aicm-caiq/`](../aicm-caiq/) | AI-CAIQ — the vendor self-assessment questionnaire derived from AICM. Versions in lockstep and inherits the ID-renumbering problem: **63 question IDs now ask a different question**. See [`../aicm-caiq/1.1.0/CHANGELOG.md`](../aicm-caiq/1.1.0/CHANGELOG.md). |
| [`../ccm/`](../ccm/) | Cloud Controls Matrix — the general cloud-security controls AICM layers on top of. Use both together for AI workloads in cloud. |

Guidance documents shipped in the AICM v1.1 bundle are extracted under
`reference/cloudsecurityalliance.org/`:
[introductory guidance](../../../reference/cloudsecurityalliance.org/aicm-introductory-guidance/v1.1/),
[AI-CAIQ instructions](../../../reference/cloudsecurityalliance.org/ai-caiq-instructions/v1.1/),
[STAR for AI L1 submission guide](../../../reference/cloudsecurityalliance.org/star-for-ai-level-1-submission-guide/v1.1/).
