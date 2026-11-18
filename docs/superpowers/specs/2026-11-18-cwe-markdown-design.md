# CWE as Markdown, and CWE 5.0

**Status:** Design, 2026-11-18. Approved by Kurt ("ok lets get datasets updated and that ai markdown stuff done asap"); source switched from CSV to XML by Kurt the same day (see Approaches).
**Issue:** [#160](https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/issues/160)
**Scope:** `weakness/mitre.org/cwe/` (new `5.0/`, `4.20/` and `4.21/` editions, new converter scripts, generated `markdown/` folders for 4.19.1, 4.20, 4.21 and 5.0, metadata and README updates)

## Why

Kurt's asks, verbatim (2026-11-18):

> "can you look in weakness/mitre.org/cwe at cwe? how would we also offer this data as markdown formatted files for easier ingestion? e.g. I'm thinking an index file in markdown, and then one file for each CWE item? formatted nicely/etc? I'm thinking a script that converts the JSON data into markdown?"

> "oh can we also do a markdown for each view?"

> "ok also we need to go get the CWE 5.0 data as well and process that one fully as well"

> "ok lets do the ata here, the csv -> markdown I guess first, and the 5.0, that'll get mnost of what we need right away"

> "is there a better source for the data>? an API? github?"

Answer to the last, chosen by Kurt: "XML, one pass (Recommended)".

> "we also need to get 4.20 and 4.21 I guess?"

MITRE's release archive (https://cwe.mitre.org/data/archive.html) keeps each past release's full XML zip, PDF, schema and difference reports, and no per-view CSV or JSON, so 4.20 and 4.21 are added as XML-only editions: original zip (S3) and sidecar, metadata, `LICENSE.txt` and generated `markdown/`. They have no per-view CSV, per-view JSON or merged files, because MITRE does not publish those for past releases (AI's call, 2026-11-18).

The CWE data here today is CSV and JSON. The CSV packs most fields into ambiguous `::KEY:value::` strings; the per-view JSON is a `yq` conversion of MITRE's XML that loses the order of mixed text and markup. Neither reads well for a person or an AI pipeline. Markdown, one page per entry, gives both a clean unit to read, cite and retrieve.

## Goals

1. Scripts that render one CWE edition as markdown: an index page, one page per weakness, one per category (4.x) or grouping (5.0), and one per view.
2. Render every edition held here: 4.19.1 (existing), 4.20, 4.21 and 5.0 (new).
3. Add CWE 5.0 as a full edition, matching what 4.19.1 holds (MITRE's three per-view CSVs and per-view JSON, merged `cwe-5.0-all.{csv,json}`, `LICENSE.txt`, metadata), plus the full XML original for every edition held (4.19.1, 4.20, 4.21 and 5.0).
4. Output regenerates byte for byte from a pinned input, so the planned reproducibility gate (#158) can re-run it.

## Non-goals

- Changing the existing 4.19.1 CSV, per-view JSON or merged files.
- A corrected JSON export from the XML. The markdown is this pass's readable form; the `yq` per-view JSON is kept for parity and its limitation recorded in metadata.
- A per-item record repo (`SecID-weakness`, AGENTS.md tier 3). These pages are a rendering of the whole catalog, not provenance-enveloped records.

## Anti-goals

- **Silent loss.** No XHTML element, entry, view member or reference is dropped without the run failing or the page saying so.
- **Lost attribution.** MITRE's terms allow copies "on the condition that you reproduce MITRE's copyright designation and this license".
- **Content history in the pages.** MITRE's `Content_History` holds the submission and modification records for each entry. That is editorial history, not weakness content, so the markdown omits it and each page's footer says so. MITRE's XML and the mirrored per-view JSON keep it as MITRE publishes it, under Kurt's rule (2026-11-18): *"we treat mitre like the gov, we republish their data, it's fine."* Author names in References citations are kept (rulings during build, 2026-11-18, recorded on #160).
- **Non-reproducible output.** No timestamps, run dates, absolute local paths or unordered iteration in generated files.

## Approaches considered

| Source | Trade-off | Decision |
|---|---|---|
| **MITRE full XML** (`cwec_v<ver>.xml.zip`) | Authoritative, archived per release, complete: examples, references, mapping notes, every view and category, 5.0's new fields. Structured text needs XHTML-to-markdown conversion. | **Chosen by Kurt**, 2026-11-18 |
| MITRE per-view CSV | Omits examples, references, mapping notes, likelihood of exploit (empty in every 4.19.1 row), categories and most views; flattens paragraphs; packed fields are ambiguous (`PHASE::DESCRIPTION:` means an empty value; values contain literal `::`, e.g. CWE-66 `::$DATA`) | Kurt's first pick, replaced after the source comparison |
| Existing `cwe-<v>-all.json` | Built from the CSV and drops seven of its 23 columns | Rejected |
| MITRE REST API (`cwe-api.mitre.org`) | Clean per-entry JSON, but no version parameter; reports `ContentVersion` 4.21 today, so it can serve neither 4.19.1 nor 5.0's schema-8 fields | Rejected for a versioned dataset; noted in metadata for live lookups |
| GitHub (`CWE-CAPEC` org) | Holds submissions, working-group documents and API docs, not CWE content | No source there |

## Input

Per edition directory: `cwec_v<ver>.xml.zip`, MITRE's versioned download (`https://cwe.mitre.org/data/xml/cwec_v<ver>.xml.zip`). It is a binary original: git-ignored, uploaded to S3 by `sync_originals_to_s3.sh`, and described by a committed sidecar `cwec_v<ver>.xml.zip-file-metadata.json` (`role: source`, `sha256`, `retrieved_from`, `retrieved_at`, `retrieved_method: curl`) per METADATA-SCHEMA's per-file sidecar schema. The scripts read the XML straight from the zip and refuse to run if its SHA-256 differs from the sidecar's or its `Weakness_Catalog/@Version` differs from the edition.

| Edition | sha256 | Weaknesses | Categories / Groupings | Views | External refs |
|---|---|---|---|---|---|
| 4.19.1 (2026-01-21, schema 7.3, namespace `cwe-7`) | `61e08a4e…c68f` | 969 (25 deprecated) | 420 Categories | 58 | 1,012 |
| 4.20 (2026-04-30, schema 7.3, namespace `cwe-7`) | `3976f599…7d50` | 969 (25 deprecated) | 422 Categories | 59 | 1,026 |
| 4.21 (2026-10-28, schema 7.4, namespace `cwe-7`) | `5225e2b4…8862` | 984 (28 deprecated) | 431 Categories | 62 | 1,081 |
| 5.0 (2026-10-28, schema 8.0, namespace `cwe-8`) | `bcda44c9…a3dc` | 984 (28 deprecated) | 431 Groupings | 62 | 1,081 |

Schema 8.0 differences the code handles: `Categories/Category` became `Groupings/Grouping`; new weakness elements `Dimensions` (107 weaknesses; `Dimension/@Type` plus text) and `Technical_Nuance` (53; structured text); new relationship nature `Overlaps`. Element lookups match on local name, so one code path reads both namespaces. The schema major version is the leading integer after `cwe-` in the namespace (a namespace without one fails the run). Two entries with the same CWE ID (in one list or across weaknesses, categories or groupings, and views), or two External_References with the same `Reference_ID`, fail the run rather than one silently replacing the other.

## Output layout

```
weakness/mitre.org/cwe/<version>/markdown/
├── index.md
├── LICENSE.txt                      copy of the edition's LICENSE.txt
├── weaknesses/CWE-<id>.md           every weakness, deprecated ones included
├── categories/CWE-<id>.md           4.19.1 (MITRE's term)
│   or groupings/CWE-<id>.md         5.0 (MITRE's term)
└── views/CWE-<id>.md
```

`categories/` holds the 4.x editions' pages (4.19.1, 4.20, 4.21). Between 1,448 (4.19.1) and 1,478 (4.21, 5.0) pages per edition. Each folder stays under GitHub's 1,000-entry listing limit (largest: 984 weaknesses).

## Entry pages (weakness, category/grouping, view)

YAML front matter, then sections in schema order, each heading named after MITRE's element with underscores as spaces ("Potential Mitigations"). GitHub's anchor for that heading then equals the SecID section subpath: `#potential-mitigations`, as in `secid:weakness/mitre.org/cwe#CWE-79/potential-mitigations`.

Front matter (weakness example):

```yaml
---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-79"
cwe_id: "CWE-79"
entry_type: weakness            # weakness | category | grouping | view
name: "Improper Neutralization of Input During Web Page Generation"
abstraction: Base               # weaknesses only
structure: Simple               # weaknesses only
status: Stable
mapping_usage: Allowed          # from Mapping_Notes/Usage, when present
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/79.html"
---
```

Weakness sections, in order, each left out when empty: Description, Extended Description, Alternate Terms, Related Weaknesses (table: nature, entry linked with its name, view, ordinal), Weakness Ordinalities, Applicable Platforms (table), Background Details, Modes Of Introduction, Exploitation Factors, Likelihood Of Exploit, Common Consequences (table), Detection Methods, Potential Mitigations, Demonstrative Examples, Observed Examples (table, CVE linked to cve.org), Functional Areas, Affected Resources, Dimensions (5.0), Technical Nuance (5.0), Taxonomy Mappings (table), Related Attack Patterns (CAPEC linked to capec.mitre.org), References, Mapping Notes, Notes. A weakness `@Diagram` becomes an image link to MITRE. Deprecated entries render whatever MITRE keeps for them (description, notes and any pointer to the replacement entry).

Category/grouping pages: Summary, Members (from `Relationships/Has_Member`, with the view each membership belongs to), Taxonomy Mappings, References, Mapping Notes, Notes.

Footer on every page:

```markdown
---
Generated from MITRE's CWE <ver> XML (cwec_v<ver>.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: <absolute GitHub URL of this edition's LICENSE.txt>).
```

**Licence decision (AI's call, 2026-11-18, under Kurt's goal order: honesty and correctness over cost).** Each page carries MITRE's copyright designation, the trademark notice and a licence statement with absolute links. Each `markdown/` folder and edition directory carries the full `LICENSE.txt`. Inlining the full licence (about 2.7 KB) on every page was rejected: about 8 MB across 2,900 pages and boilerplate in every retrieval chunk. The repository and each `markdown/` folder are the copies that reproduce the licence in full. Kurt confirmed the licence question is settled (2026-11-18): *"we treat mitre like the gov, we republish their data, it's fine."* The short attribution footer stays because MITRE's terms ask for it and it costs nothing.

## Structured text (XHTML to markdown)

MITRE's structured text fields hold text mixed with XHTML. Measured tag inventory across 5.0: `p`, `div`, `br`, `ul`, `ol`, `li`, `b`, `i`, `table`, `tbody`, `tr`, `th`, `td`, `caption`, `img`, `sup`, `span`. The converter walks elements in document order (`text`, children, `tail`), so order is preserved. Any other tag fails the run with the CWE ID and path. Demonstrative examples: `Intro_Text` and `Body_Text` as prose; each `Example_Code` labelled `*Example (<Nature>, <Language>):*` (Bad, Good, Attack, Result, Informative). An `Example_Code` holding only text, `br`, `div`, `p`, `b`, `i`, `span` or `sup` is a fenced block (an `img` inside it fails the run; none occur) tagged with the lower-cased language; `br` is a newline, each `div` or `p` starts a new line (so several paragraphs are joined by single newlines, with no blank line between them; kept as is by a ruling during build, 2026-11-18), each nested `div` with a `margin-left` style indents four spaces, XML pretty-print whitespace is removed, nothing is escaped, and the fence grows past any backtick run in the code. An `Example_Code` holding a table or list renders as structured markdown under its label, because a fence would destroy the structure (ruling during build, 2026-11-18). Outside code, text renders as written: a backslash before ASCII punctuation is doubled (so it stays a literal backslash), `<` becomes `&lt;`, `&` is escaped only where it would start an entity, `*` and backticks are backslash-escaped, `_` is escaped unless it sits between two alphanumerics, `|` is escaped in table cells, a line-initial `#`, `>`, `-`, `+`, `~~~` or `N.` that would start a heading, quote, list or fence is escaped, as is a line made only of `=` or of two or more `-` (it would underline the line before as a setext heading), and a `br` in prose is a trailing-backslash hard break.

## View pages

Each opens with the view's name, type, status, objective, audience and member counts.

- **Graph views** (39 in 5.0, e.g. 1000, 699, 1194, the Top 25 lists): a nested outline. Roots are the view's `Members/Has_Member`. A category's or grouping's children are its `Has_Member` entries with that `@View_ID`; a weakness's children are the weaknesses with a `ChildOf` to it with that `@View_ID`. Each entry is expanded once, under its `Primary` parent in that view (else its lowest-ID parent); any other parent lists it as a one-line cross-reference. Cycles are guarded. The script asserts every entry reachable in the view is expanded exactly once. Entries that have a parent in the view but that no root reaches are listed at the end of the page under "Not reachable from this view's roots", each with its parent (ruling during build, 2026-11-18). In 4.21 and 5.0, view 1000 has two: CWE-378 and CWE-379, whose only parent there is deprecated CWE-377.
- **Explicit views** (6): a flat list of members.
- **Implicit views** (17): the view's XPath `Filter` shown as code, then the members it selects. The script holds an exact predicate for each of the 15 active filter strings (e.g. `[./Applicable_Platforms/Language/@Name='C']`, `[@Status='Deprecated']`); an unknown filter string gets the filter only, a stated "members not computed", and a warning in the run output.
- Obsolete and deprecated views render their description and status only.

Each line in an outline: `[CWE-79](../weaknesses/CWE-79.md) Name (Base)`.

## Upstream data

The pages reproduce MITRE's data as published, upstream errors included (ruling during build, 2026-11-18). Example: in 4.21 and 5.0, CWE-1475's observed-example row labelled CVE-2025-50328 links to CVE-2026-58052, as MITRE's XML does.

## Index page

Edition, release date, source and SHA-256, licence and attribution; counts by entry type, abstraction and status; then three tables sorted by numeric ID: weaknesses (ID, name, abstraction, status, mapping usage), categories or groupings (ID, name, status), views (ID, name, type, status).

## Scripts

All under `weakness/mitre.org/cwe/scripts/`, Python 3.10+ standard library only, version-independent, tests with `unittest`:

| File | Responsibility |
|---|---|
| `cwe_xml.py` | Load and verify an edition (zip, sidecar SHA-256, version, schema major, unique IDs), index entries by ID, namespace-agnostic element access, view outline construction, implicit-view predicates |
| `cwe_structured_text.py` | XHTML structured text to markdown, and markdown escaping |
| `cwe_to_markdown.py` | Page rendering, `index.md`, writing the folder, `--check`, CLI |
| `merge_cwe_views.py` | Moved from `4.19.1/`, now takes the edition directory and version |

`cwe_to_markdown.py --version <v> [--check]` resolves paths from its own location (no local paths, per #158), rewrites `markdown/` completely (removing files it no longer produces), and in `--check` mode renders in memory and exits 1 listing any file that differs, is missing or is extra. Output is UTF-8 with LF line endings and is sorted numerically.

## Adding CWE 5.0

1. In `weakness/mitre.org/cwe/5.0/`, run `scripts/download-cwe-items.sh` unchanged (it is pinned by the tier gate; editing it is a gate change) to fetch MITRE's current view CSVs and the per-view JSON via `yq`. Confirm every file reports version 5.0. File names keep the script's names (`CWE-Research-Concepts-1000.*`) for continuity across editions; metadata records that view 1000 is named "Complete Weakness Hierarchy" in 5.0.
2. `git mv` `merge_cwe_views.py` to `scripts/`, give it `--edition-dir` and `--version`, prove it regenerates `cwe-4.19.1-all.{csv,json}` byte for byte, then run it for 5.0. Update the `tool` reference in 4.19.1's metadata.
3. `LICENSE.txt` for 5.0 from MITRE's Terms of Use page (the zips hold only the XML), compared with 4.19.1's copy; the differences, if any, are reported.
4. Download both versioned XML zips into their edition directories and write their sidecars.
5. `cwe-5.0-metadata.json` from 4.19.1's, with 5.0's facts: release date 2026-10-28, schema 8.0 changes, counts recomputed from the files, `access_tier: 2` with `tier_evidence` (public web, no login, checked 2026-11-18), a note that the per-view JSON is a mechanical `yq` conversion that does not keep text order (use `markdown/` or the XML for prose), and a note that MITRE's REST API serves only the latest content. In 4.19.1's metadata: `lifecycle.published` to `2026-01-21` (MITRE's catalog date; it says "2025" today), `lifecycle.supersededBy: "5.0"`, the same `yq` note.
6. Upload the zips with `tools-resources/utils/sync_originals_to_s3.sh` (`--dry-run` first).

Later releases follow the procedure in `weakness/mitre.org/cwe/README.md` ("Adding a new CWE release").

## Verification

- `cwe_to_markdown.py --version <v> --check` passes for every edition (4.19.1, 4.20, 4.21, 5.0).
- Page counts equal the catalog counts in the Input table; each view outline expands every reachable entry exactly once.
- Every relative link in `markdown/` resolves to a generated file.
- Structured-text order: CWE-79's "Result" example renders its nested form lines between "Please Login:" and the closing `</div></div>`, as in MITRE's XML.
- Spot-check against MITRE's HTML pages: CWE-79, CWE-89, CWE-1426, CWE-1039 (5.0 `Technical_Nuance`), CWE-1024 (5.0 `Dimensions`), a Pillar, a hardware weakness, a deprecated entry, a grouping, view 1000 and an implicit view.
- Repository checks: `audit_secid_alignment.py`, `build_index.py`, `check_tier_restrictions.py`, and the scripts' `unittest` suite. Tests that need an edition's git-ignored zip skip when it is absent and name it; `CWE_REQUIRE_ZIPS=1` turns those skips into failures (for the #158 gate).
- Report total size of each `markdown/` folder in the PR.

## Left to the builder

- Table versus list per section where the data shape makes one clearly better.
- How Weakness Ordinalities, Alternate Terms, Detection Methods and Potential Mitigations lay out (lists with bold labels are fine).
- Wording of the "members not computed" note and the deprecated-entry banner.

## Follow-ups (separate issues)

- [CloudSecurityAlliance/SecID#298](https://github.com/CloudSecurityAlliance/SecID/issues/298): registry prose names CWE-1425 as the AI/ML view; in MITRE's data it is CWE-1448.
