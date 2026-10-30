# Final review: CCM 4.1.1 (2026-10-23)

- **Reviewer:** a fresh AI reviewer (Opus) with no part in the work, read-only on all checkouts.
- **Ranges:** SecID `723bb8c..2e6f30b` (SecID#207 before fixes) and dataset `74ff4b8..02fd56a` (Tasks 1–5).
- **Brief given:** the plan, the executor's ledger of rulings, the plan's Review Focus, and the areas the author was least sure of.
- **Verdict:** "With fixes".

This record keeps the reviewer's findings, lightly condensed, with local paths and
names of people removed. After them comes the executor's response: the re-grading,
the fixes with their commits, and the rulings.

## What the reviewer verified independently

- **Every extraction reproduces byte for byte** from its source workbook, with all output sent to `/tmp`:
  - 4.1.1, including both CSVs;
  - CAIQ, both the 2026-10-02 generation and the January one at `74ff4b8` (apart from the new `source_workbook` key);
  - 4.1.0, using a patched copy of the parser.
- **All five Review Focus items hold:**
  - no stale `ccm/4.1/` references;
  - DORA: 215 provisions, 727 references, 0 unknown IDs, 7 empty lists, all Full Gap;
  - `No Mapping` matches `Full Gap` exactly;
  - the CAIQ README's 26 rows equal a direct diff of the old and new JSON;
  - the 4.1.1 parser exits 1 on the 4.1.0 workbook.
- **The figures are honest:**
  - its own cell diff reproduces the CHANGES §Method table exactly (6,751 cells; 3,105 booleans retyped as strings);
  - the wording table matches a token diff;
  - the five specifications the detector calls "substantive" are comma-only;
  - the IAM-13 wording appears in 4.0.13 and AICM;
  - S3 objects and hashes match.
- **SecID:** each version node's domain codes and names match the dataset; all gates pass.
- **The guard catches drift:** mutating a README cell, a flag or a DORA figure fails it.
- **No third-party names** appear in the new docs.

## Findings

**Critical**

- **C1. Merging SecID#207 turns SecID-Service's registry deploy red.** `test/resolver-correctness.test.ts` asserts that an unversioned `ccm%23A%26A-01` is `found`, and `registry-kv-upload.yml` runs `npx vitest run` before uploading the registry. Verified: the full suite passes 718/718 with `main`'s registry and fails 1 with the PR's (`expected 'related' to be 'found'`). Fix: pin the query to `ccm@4.0`.

**Important**

- **I1. Bare-ID cross-source search no longer finds CCM.** `namespaceScopedSearch` and `typeScopedSearch` walk only a source's direct children, which for CCM are now version nodes. Verified with a harness, and live:
  - `secid:control/cloudsecurityalliance.org/IAM-01` loses `ccm#IAM-01`;
  - `.../4.1.1` returns a malformed `ccm#4.1.1`. AICM already does this.
- **I2. SecID's `cloudsecurityalliance.md` companion contradicts the corrected JSON:** versions, `IVS`, "4.0.3 current", unversioned examples. The `ccm` notes also name a nonexistent workbook.
- **I3. PR #207's "Before" column and the ADR overstate today's behaviour.** `ccm@4.0.13` and `ccm@v4.1` are `not_found` today.

**Minor**

- **M1.** The "wording" category includes apostrophe, hyphen and case edits, and "punctuation only" includes spacing. The headline "9/7 in wording" is undefined in the 4.1.1 README §3 and in the SecID notes.
- **M2.** "127 reworded cells" is texts: each specification is repeated in four sheets, giving 430 cells. Also, the Change Log names 2 of them, not "the workbook".
- **M3.** The CAIQ README and metadata misquote the questionnaire's Change Log. It has two rows (v4.1 and v4.0.3), both reformatted in October.
- **M4.** A consumer pinned to the January CAIQ isn't told that 233 raw question strings, 150 control-text fields and the embedded `ccm_control` also changed. `ccm-4.1.0-metadata.json` still points at `ccm-caiq/4.1.0/` as its companion.
- **M5.** The root README's "CAIQ 4.1 / v4.1" row has no SecID alias behind it.
- **M6.** DORA `A13.3` lists `SEF-04` twice in CSA's own cell. It is kept verbatim, but no doc mentions it.
- **M7.** `parse_caiq.py --expect-ccm-version 4.1.0` without `--ccm-json` silently embeds 4.1.1 controls.
- **M8.** The id `dcs-11-1-asks-less-than-its-control` reads as a verdict. Its summary is hedged.
- **M9.** The committed plan contains absolute local paths.

**Declined to judge** (the executor's ruling follows each item):

- License fields vs the workbook's own notice: left to the project lead, as the plan says.
- Task 6, which was unfinished at review time: completed after the review.
- `INDEX.md` regeneration: consistent with the files on disk.
- Pattern breadth and case: these predate this work.
- The PR order and the alias exception: decisions already made.
- The 2026-10-06 repack date: it comes from the downloaded ZIP's internal timestamps and a bundled filename (`Introductory Guidance to CCM 20261006.pdf`).

## Executor's response

Findings were re-graded by their effect on a reader. M2, M3 and M4 are factual
errors that a consumer would act on, so they were raised to Important. Every
Critical and Important finding was fixed in one pass, each checked by a test
seen failing first.

| Finding | Fix | Commit | RED → GREEN |
|---|---|---|---|
| C1 | SecID-Service#45 pins the case to `ccm@4.0` | SecID-Service#45 | vitest 717/718 → 718/718, against both SecID `main` and the PR registry |
| I1 | Documented in ADR-015's second amendment, the TODO R1 entry and PR #207. Teaching the search to descend into version nodes is SecID-Service work and outside this scope | SecID `3f8a03b` | doc check fails → passes; 15/15 SecID gates |
| I2 | `.md` companion and the `ccm`/`ccm-caiq` notes updated | SecID `3f8a03b` | same doc check |
| I3 | Baseline corrected in DECISIONS and the PR body, after a live check: `ccm@4.0.13` and `ccm@v4.1` are `not_found`; `ccm@4.1` resolves | SecID `3f8a03b` | same doc check |
| M2→I | "reworded texts", 430 cells, "the Change Log names" | dataset `b66386f` | `check_figures.py` pattern and `FORBIDDEN` fail → pass |
| M3→I | Change Log quoted correctly | dataset `b66386f` | `FORBIDDEN` fails → passes |
| M4→I | 4.1.0 metadata companion note corrected; CAIQ README lists the other differences | dataset `b66386f` | `FORBIDDEN` fails → passes; counts checked against `74ff4b8` |

**Deferred** (Minor, filed as one issue): M1, M5, M6, M7, M8, M9.

**After the fix pass:**
- `ccm/check_figures.py`: 43 invariants, 58 documented figures, 0 problems.
- AICM guard: 60/60 figures, 7/7 invariants.
- SecID audit: 0 missing namespaces.
- SecID: 15/15 CI gates.
- SecID-Service: 718/718 against the fixed PR registry.
