# AI-CAIQ v1.1.0

`secid:control/cloudsecurityalliance.org/aicm-caiq@1.1.0` · 320 questions · 247 controls · published 2026-06-22

The vendor self-assessment questionnaire companion to
[AICM v1.1.0](../../aicm/1.1.0/). Used for CSA STAR for AI Level 1 submissions.

**Also known as AI-CAIQ 1.1.** The workbook stamps itself `1.1.0`; the bundle it
ships in is branded "v1.1". We use **1.1.0** as canonical and alias 1.1 to it,
matching the parent AICM. Recorded as `version_aliases` in the metadata:

```json
"version": "1.1.0",
"version_aliases": ["1.1", "v1.1", "v1.1.0"],
```

A labelling alias only — it implies nothing about compatibility with 1.0.2, which
numbers its questions differently (see the warning above).

> ## ⚠️ Question IDs changed meaning in this release
>
> **AI-CAIQ v1.1.0 question IDs are not interchangeable with v1.0.2 question IDs.**
>
> Question IDs derive from AICM control IDs (`LOG-15.1` belongs to control
> `LOG-15`), and AICM v1.1.0 renumbered controls in place. **The question IDs
> moved with them.** `LOG-15.1` asks about Output Monitoring under v1.0.2 and
> Input Monitoring under v1.1.0.
>
> A completed v1.0.2 questionnaire cannot be re-scored against v1.1.0 by
> matching question IDs. Migrate the parent controls through
> [`../../aicm/crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv`](../../aicm/crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv).
>
> Full analysis: [`../../aicm/VERSIONING.md`](../../aicm/VERSIONING.md)

The questionnaire jumped **1.0.2 → 1.1.0** to version in lockstep with AICM.
There is no AI-CAIQ 1.0.3.

## Contents

| File | What |
|---|---|
| `aicm-caiq-1.1.0.json` | 320 questions, each enriched with its full parent AICM control record |
| `aicm-caiq-1.1.0-questions.csv` | Flat view — one row per question with its parent control's identifying fields |
| `aicm-caiq-1.1.0-metadata.json` | Document metadata and licence |

Built by [`../../aicm/1.1.0/scripts/parse_caiq.py`](../../aicm/1.1.0/scripts/parse_caiq.py),
which requires the AICM extraction to exist first.

The CSV carries the question plus its control ID, title, domain and
specification. The full nested control record — ownership, relevance grids,
mappings, guidelines — stays in the JSON, where it can be represented properly.

Respondent instructions for completing this questionnaire are extracted at
[`reference/cloudsecurityalliance.org/ai-caiq-instructions/v1.1/`](../../../../reference/cloudsecurityalliance.org/ai-caiq-instructions/v1.1/),
and the submission procedure at
[`reference/cloudsecurityalliance.org/star-for-ai-level-1-submission-guide/v1.1/`](../../../../reference/cloudsecurityalliance.org/star-for-ai-level-1-submission-guide/v1.1/).

## Verification

The standalone questionnaire workbook was checked against the `AI-CAIQ` tab
embedded in the AICM workbook: **identical 320 question IDs, identical question
text, identical parent-control assignment, zero discrepancies.** Every one of
the 247 AICM controls carries at least one question, and question numbering is
contiguous within every control.

## Answer columns ship blank

The questionnaire's response fields — Service Provider AI-CAIQ Answer, SSRM
Control Ownership, Service Provider Implementation Description, Service Customer
Responsibilities — are empty in the published workbook. That is by design: they
are the vendor response template. They are not extracted as content.
