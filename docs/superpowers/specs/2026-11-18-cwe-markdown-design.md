# CWE as Markdown (CSV pass) and CWE 5.0

**Status:** Design, 2026-11-18, pending Kurt's approval
**Issue:** [#160](https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/issues/160)
**Scope:** `weakness/mitre.org/cwe/` (new `5.0/` edition, a new converter script, generated `markdown/` folders for 4.19.1 and 5.0, metadata and README updates)

## Why

Kurt's asks, verbatim (2026-11-18):

> "can you look in weakness/mitre.org/cwe at cwe? how would we also offer this data as markdown formatted files for easier ingestion? e.g. I'm thinking an index file in markdown, and then one file for each CWE item? formatted nicely/etc? I'm thinking a script that converts the JSON data into markdown?"

> "oh can we also do a markdown for each view?"

> "ok also we need to go get the CWE 5.0 data as well and process that one fully as well"

> "ok lets do the ata here, the csv -> markdown I guess first, and the 5.0, that'll get mnost of what we need right away"

The CWE data here today is CSV and JSON. The CSV packs most fields into `::KEY:value::` strings; the per-view JSON is a `yq` conversion of MITRE's XML. Neither is pleasant for a person or an AI pipeline to read. Markdown, with one page per weakness, gives both a clean unit to read, cite and retrieve.

## Goals

1. A script that renders one CWE edition's data as markdown: an index page, one page per weakness, and one page per view.
2. Render both editions held here: 4.19.1 (existing) and 5.0 (new).
3. Add CWE 5.0 as a full edition, matching what 4.19.1 holds: MITRE's three per-view CSVs and per-view JSON, the merged `cwe-5.0-all.{csv,json}`, `LICENSE.txt` and metadata.
4. Output is reproducible byte for byte from committed inputs, so the planned reproducibility gate (#158) can re-run it.

## Non-goals (this pass)

- **The XML pass.** MITRE's CSV export omits demonstrative examples (code samples; 596 of 944 weaknesses in 4.19.1 have them), references, category/grouping pages, the other ~55 views, deprecated entries, and 5.0's new `Dimensions` (107 weaknesses) and `Technical_Nuance` (53) fields. A later pass that parses MITRE's full XML closes these gaps. This design keeps the page layout ready for it: the renderer takes a parsed record, so a second reader can feed it.
- CWE 4.20 and 4.21 (released between 4.19.1 and 5.0; 4.21 is a schema-7 copy of 5.0 for migrating consumers).
- Changing the existing 4.19.1 data files (CSV, per-view JSON, merged files).
- A per-item record repo (`SecID-weakness`, AGENTS.md tier 3). These pages are a rendering of the whole catalog, not provenance-enveloped records.

## Anti-goals

- **Silent gaps.** A page that looks complete but lacks the examples and references MITRE publishes would mislead a reader. Every weakness page states what this rendering leaves out and links MITRE's page for it.
- **Lost attribution.** MITRE's terms allow copies "on the condition that you reproduce MITRE's copyright designation and this license". A page ingested on its own must still carry that.
- **Non-reproducible output.** No timestamps, run dates, absolute paths or unordered iteration in generated files.

## Approaches considered

| Approach | Trade-off | Decision |
|---|---|---|
| **A. Render from MITRE's per-view CSVs** (plus per-view JSON for category grouping) | Fast to build; plain-text fields; omits examples, references and 5.0's new fields | **Chosen by Kurt** for the first pass ("the csv -> markdown I guess first … that'll get mnost of what we need right away") |
| B. Render from MITRE's full XML | Complete, including code examples and all views; XHTML-to-markdown conversion is extra work | Recommended by the AI as the end state; deferred to a follow-up pass |
| C. Render from the existing `cwe-<v>-all.json` | Kurt's first idea | Rejected: `merge_cwe_views.py` drops seven of the 23 CSV columns (Weakness Ordinalities, Background Details, Alternate Terms, Exploitation Factors, Functional Areas, Affected Resources, Notes) |
| D. MITRE REST API | Per-entry JSON | Rejected: serves only the latest release, so 4.19.1 cannot be reproduced |

## Inputs (per edition directory)

| File | Used for |
|---|---|
| `CWE-*-1000.csv`, `CWE-*-699.csv`, `CWE-*-1194.csv` | All weakness fields (23 columns), view membership |
| `CWE-*-699.json`, `CWE-*-1194.json` | Category (4.x) or Grouping (5.0) membership for the 699 and 1194 view pages: `Has_Member/@CWE_ID` with `@View_ID` equal to the view. Membership is attribute data, so the `yq` mixed-content ordering problem does not affect it. |
| `CWE-*-1000.json`, `-699.json`, `-1194.json` | View name, objective and status for the view pages |
| `cwe-<v>-metadata.json` | Edition version, release date and SecID for page headers |

Files are found by view-ID suffix, so 5.0's files can carry 5.0's view names (view 1000 is "Complete Weakness Hierarchy" in 5.0, "Research Concepts" in 4.19.1).

The CSV rows carry one empty unnamed trailing cell; the reader ignores it.

## Parsing the packed CSV fields

Fifteen columns pack items as `::KEY:value:KEY:value::`. Each column has a small fixed key set (measured on 5.0 view 1000), for example:

| Column | Keys |
|---|---|
| Related Weaknesses | NATURE, CWE ID, VIEW ID, ORDINAL, CHAIN ID |
| Common Consequences | SCOPE, IMPACT, LIKELIHOOD, NOTE |
| Potential Mitigations | PHASE, STRATEGY, DESCRIPTION, EFFECTIVENESS |
| Observed Examples | REFERENCE, DESCRIPTION, LINK |
| Taxonomy Mappings | TAXONOMY NAME, ENTRY ID, ENTRY NAME, MAPPING FIT |

Items split on `::`. Within an item, the parser splits only on the column's known keys, so values that contain colons ("NOTE:REALIZATION: This weakness …") survive intact. Repeated keys (`SCOPE:A:SCOPE:B`) become lists. An unrecognised key, or text before the first key, fails the run with the CWE ID and column named: a silent misparse is worse than a stop. The full key table lives in the script, checked against both editions.

## Output layout

```
weakness/mitre.org/cwe/<version>/markdown/
├── index.md
├── views/
│   ├── CWE-1000.md
│   ├── CWE-699.md
│   └── CWE-1194.md
└── weaknesses/
    ├── CWE-1.md … CWE-1434.md     (944 for 4.19.1, 956 for 5.0)
```

Subfolders keep each directory under GitHub's 1,000-entry listing limit. About 1,900 files across both editions.

## Weakness page

YAML front matter, then sections in MITRE's own order, each heading named after MITRE's field. GitHub's heading anchors then match SecID section subpaths: `## Potential Mitigations` gives `#potential-mitigations`, as in `secid:weakness/mitre.org/cwe#CWE-79/potential-mitigations`.

```markdown
---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-79"
cwe_id: "CWE-79"
name: "Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')"
abstraction: Base
status: Stable
views: ["1000", "699"]
cwe_version: "5.0"
source: "MITRE CWE 5.0 CSV export (views 1000, 699, 1194)"
upstream: "https://cwe.mitre.org/data/definitions/79.html"
---

# CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')

**Abstraction:** Base · **Status:** Stable · **Views:** [1000](../views/CWE-1000.md), [699](../views/CWE-699.md)

## Description
## Extended Description
## Alternate Terms
## Related Weaknesses        (table: nature, CWE (linked, with name), view, ordinal)
## Weakness Ordinalities
## Applicable Platforms      (table: kind, name or class, prevalence)
## Background Details
## Modes Of Introduction     (table: phase, note)
## Exploitation Factors
## Likelihood Of Exploit
## Common Consequences       (table: scope, impact, likelihood, note)
## Detection Methods         (per method: description, effectiveness)
## Potential Mitigations     (per item: phase, strategy, description, effectiveness)
## Observed Examples         (table: CVE linked to cve.org, description)
## Functional Areas
## Affected Resources
## Taxonomy Mappings         (table: taxonomy, entry ID, entry name, fit)
## Related Attack Patterns   (CAPEC IDs linked to capec.mitre.org)
## Notes                     (per note: type, text)

---
Not included in this rendering: demonstrative examples and references. See MITRE's page: <link>.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use (../../LICENSE.txt). Generated from MITRE's CSV export by <script path>.
```

Empty sections are left out. Related weaknesses outside this edition's three views (e.g. a ChildOf in view 1003) keep their CWE ID and link; the link target exists only when that weakness is in view 1000, which holds every active weakness.

## View pages

- **CWE-1000:** a nested outline built from `ChildOf` relationships with `VIEW ID:1000` and `ORDINAL:Primary`, from the 10 Pillars down. Each weakness appears once, under its primary parent, as `[CWE-79](../weaknesses/CWE-79.md) Name (Base)`. Weaknesses with no primary parent in view 1000 are listed in a final section so none goes missing; the script asserts the outline plus that section covers every view-1000 weakness exactly once.
- **CWE-699 and CWE-1194:** one section per category or grouping (40 and 13 in 4.19.1), each listing its member weaknesses sorted by ID. The CSVs have no relationships scoped to these views, so there is no deeper tree in this pass.
- Each view page opens with the view's name, type, status and objective, plus member counts.

## Index page

Edition, release date, source, licence and attribution; counts by abstraction and status; links to the three view pages; then one table of every weakness sorted by numeric ID: ID (linked), name, abstraction, status, views.

## Script

- `weakness/mitre.org/cwe/scripts/cwe_csv_to_markdown.py --version <v>`: Python 3 standard library only, version-independent, so it sits with the existing CWE scripts rather than in one edition folder.
- Resolves paths from its own location (no hard-coded local paths, per #158).
- Rewrites `markdown/` completely each run, removing files it no longer produces.
- `--check` renders to a temporary directory and exits 1 if the result differs from the committed `markdown/`. This is the hook for the #158 gate.
- Deterministic: sorted numerically by CWE ID, LF line endings, UTF-8, no timestamps.

## Adding CWE 5.0

1. Download MITRE's 5.0 view CSVs and view XML (`scripts/download-cwe-items.sh`, which fetches the current release, now 5.0) into `weakness/mitre.org/cwe/5.0/`, and produce the per-view JSON with `yq` as for 4.19.1. Confirm each file's `Version="5.0"` before committing.
2. Make `merge_cwe_views.py` take the edition directory and version as arguments. Move it to `cwe/scripts/`, prove it regenerates 4.19.1's committed `cwe-4.19.1-all.{csv,json}` byte for byte, then run it for 5.0. Update the `tool` reference in 4.19.1's metadata.
3. Copy MITRE's `LICENSE.txt` for 5.0 from the download, not from 4.19.1, and compare the two.
4. Write `cwe-5.0-metadata.json` from 4.19.1's, with 5.0's facts: release date 2026-10-28, schema 8.0, Category renamed Grouping, view 1000 renamed, counts recomputed from the files, `access_tier: 2` with `tier_evidence` (public web, no login, checked 2026-11-18). Record the CSV-pass gaps in `current_extraction.notes`.
5. Update 4.19.1's metadata: `lifecycle.supersededBy: "5.0"`; leave `active` as is, since 4.x mappings stay in use.
6. Store MITRE's full XML zips (`cwec_v4.19.1.xml.zip`, `cwec_v5.0.xml.zip`) under each edition directory (git-ignored) and upload with `tools-resources/utils/sync_originals_to_s3.sh`, `--dry-run` first. These are the inputs for the XML pass.

## Verification

- `cwe_csv_to_markdown.py --check` passes for both editions after generation.
- Page counts equal view-1000 CSV row counts (944, 956); every view-1000 weakness appears exactly once in the 1000 outline.
- No dangling relative links in `markdown/`: a link checker over the generated files.
- Spot-check five pages per edition against MITRE's HTML pages (CWE-79, CWE-89, CWE-1426, a Pillar, a hardware weakness from view 1194).
- Repository checks: `audit_secid_alignment.py`, `build_index.py`, `check_tier_restrictions.py`.
- Size: report total size of each `markdown/` folder in the PR.

## Left to the builder

- Exact table versus list choice per section where the data shape makes one clearly better.
- Markdown escaping rules (pipes in table cells, leading `#`, angle brackets in descriptions).
- Whether the README in `cwe/` gains a short "Markdown" section (it should mention the folders and the gaps).

## Follow-ups (separate issues)

- XML pass: demonstrative examples, references, category/grouping pages, all views, deprecated entries, 5.0's `Dimensions` and `Technical_Nuance`.
- [CloudSecurityAlliance/SecID#298](https://github.com/CloudSecurityAlliance/SecID/issues/298): registry prose names CWE-1425 as the AI/ML view; in MITRE's data it is CWE-1448.
