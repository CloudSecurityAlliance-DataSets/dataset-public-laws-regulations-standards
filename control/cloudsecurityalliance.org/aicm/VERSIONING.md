# AICM versioning — control IDs are not stable across releases

**A bare AICM control ID is not an identifier. It is an identifier *plus* an
implied version, and the implication is usually wrong.**

Between AICM v1.0.3 and v1.1.0, CSA renumbered controls in place. Fifty-five
control IDs survived the release unchanged as strings while coming to mean a
different control. Nothing in the identifier, the file, or the change log
signals this. Any consumer that stored `LOG-15` and re-resolved it against
"current AICM" silently changed which requirement it was pointing at.

This document records what happened, why it defeats the obvious ways of
detecting it, and what this repo and [SecID](https://github.com/CloudSecurityAlliance/SecID)
must do about it — on the assumption that **it will happen again in v1.2**.

---

## 1. What changed between v1.0.3 and v1.1.0

| | v1.0.3 | v1.1.0 |
|---|---|---|
| Controls | 243 | 247 |
| Domains | 18 | 18 |
| Released | 2025-11-10 | 2026-06-22 |

> **A note on "1.1" vs "1.1.0".** CSA's download page brands this release
> "v1.1"; the spreadsheet stamps itself `1.1.0`. These are the same release.
> **This repo uses `1.1.0` as canonical and aliases `1.1` to it**, because the
> artifact's own internal version string is what a consumer parsing the file
> sees, and because it keeps the version sort stable against `1.0.3` and
> `0.0.2`. Both forms are recorded in `version_aliases` in the metadata; see
> [`1.1.0/README.md`](1.1.0/README.md#version-naming-and-aliases).
>
> This is a *labelling* alias. It says nothing about compatibility — which is
> the entire subject of the rest of this page.

Reconstructed by content-matching the two releases
([`crosswalks/`](crosswalks/)):

| Outcome | Count |
|---|---|
| Carried over | 240 |
| ...of which **renumbered** | **53** |
| ...of which specification substantively rewritten | 34 |
| Added | 7 |
| Removed | 3 |

### The number that matters

| Measure | Count |
|---|---|
| Control IDs present in both releases | 242 |
| ...that still mean the same control | 187 |
| ...**that now mean a *different* control** | **55** |
| IDs that disappeared entirely | 1 (`IAM-19`) |
| IDs that are new strings | 5 (`DCS-16`, `DCS-17`, `DCS-18`, `LOG-16`, `SEF-10`) |

**23% of shared identifiers were silently repointed.** Meanwhile only one ID
vanished and five appeared.

### Why the obvious check fails

The cheap integrity check on a version bump is a set-difference of control IDs.
Run against this release it reports:

```
added:   DCS-16, DCS-17, DCS-18, LOG-16, SEF-10
removed: IAM-19
```

Six rows. Looks like a routine incremental release. It is not — it misses all
55 repointed IDs, because set-difference compares *identifiers* and every one of
those identifiers is present on both sides.

Detecting this requires comparing **content**, not identifiers.

### How the renumbering works

New controls were inserted *mid-domain*, shifting every subsequent number by
one. `DCS` is the clearest case — a new `DCS-01` at the top pushed the entire
domain down:

| ID | v1.0.3 meant | v1.1.0 means |
|---|---|---|
| `DCS-01` | Off-Site Equipment Disposal Policy and Procedures | **Physical and Environmental Security Policy and Procedures** *(new)* |
| `DCS-02` | Off-Site Transfer Authorization Policy and Procedures | Off-Site Equipment Disposal Policy and Procedures |
| `DCS-15` | Equipment Location | Secure Utilities |
| `DCS-16` | *(did not exist)* | Equipment Location |

The same insertion-shift pattern hit `AIS`, `IAM`, `LOG`, `SEF`, `STA`, and
`TVM`. `IAM` also had a deletion, shifting the tail *up* instead of down.

Three worked examples of how badly a stale reference reads:

| ID | v1.0.3 | v1.1.0 | Consequence |
|---|---|---|---|
| `LOG-15` | Output Monitoring | **Input Monitoring** | Adjacent, plausible, wrong. Output monitoring moved to `LOG-16`. |
| `IAM-12` | Safeguard Logs Integrity | **Unique Identities** | Unrelated requirement. |
| `TVM-12` | Threat Analysis and Modelling | **Vulnerability Management Metrics** | Threat modelling moved to `TVM-04` — eight positions away. |

### Identical ID, identical title, rewritten requirement

The hardest category to catch. These controls kept both their number and their
name, but the specification text was substantially rewritten:

| ID | Title (unchanged) | Spec similarity |
|---|---|---|
| `I&S-03` | Network Security | 0.24 |
| `A&A-05` | Audit Management Process | 0.27 |
| `IPY-04` | Data Portability Contractual Obligations | 0.28 |
| `I&S-05` | Production and Non-Production Environments | 0.37 |
| `I&S-08` | Network Architecture Documentation | 0.58 |
| `TVM-03` | Vulnerability Identification | 0.63 |

A diff keyed on ID *or* on title sees nothing. Only the requirement text moved.

### The change log understates it

The v1.1.0 `Change Log` sheet describes the release as five new controls
(`DCS-01`, `DCS-17`, `DCS-18`, `LOG-08`, `SEF-09`) and one deletion (`IAM-12`).
That accounting is correct as far as it goes, and our reconstruction agrees on
those five. **It never mentions that 53 controls were renumbered or that 34
specifications were rewritten.**

Treat the CSA change log as a summary of intent, not as a delta. Diff the
content.

### Separately: NIST AI 600-1 mappings were withdrawn

The `Scope Applicability (Mappings)` sheet dropped from 16 columns to 13. The
`NIST AI 600-1:2024` mapping block — populated for all 243 controls in v1.0.3 —
is absent from v1.1.0, while the same workbook's change log claims mapping rows
were added "across all four external frameworks." Only three frameworks are
present (BSI AI C4, EU AI Act, ISO/IEC 42001:2023).

**Accepted as shipped.** The v1.1.0 extraction carries the three frameworks that
are actually there. Anyone who needs NIST AI 600-1 mappings has to fall back to
the 1.0.3 extraction — and its control IDs do not carry over, which is the whole
subject of this page.

The v1.1.0 parser discovers the mapping frameworks from the sheet's group header
row and refuses to run if they differ from what it expects, so the next
add-or-drop is a loud failure rather than a silently short record.

Three smaller source quirks are handled explicitly and catalogued under
`known_source_issues` in
[`1.1.0/aicm-1.1.0-metadata.json`](1.1.0/aicm-1.1.0-metadata.json):

| Quirk | Handling |
|---|---|
| `GRC-01`–`GRC-08` say `Cloud Service Provider (CSP)` where 239 others say `Owned by the Cloud Service Provider (CSP)` | **Normalized** to the full form. All 8 substitutions itemized in `source_data_notes.normalizations_applied`. |
| 5 ownership cells empty (`DSP-21`, `DSP-23`, `DSP-24`) | **Absent at source, not a conversion error.** Emitted as `null` and itemized in `source_data_notes.gaps_in_source`. |
| `DSP-08` has no BSI AI C4 mapping | **Absent at source, not a conversion error.** Same gap in v1.0.3. Recorded in `gaps_in_source`. |

Both `source_data_notes` blocks are recomputed from the parsed data on every run,
so the record cannot drift from what was actually extracted.

---

## 2. Why this makes SecID load-bearing

SecID's job is to say *which thing* an identifier names. AICM is the case that
proves the version qualifier is not decoration.

**`secid:control/cloudsecurityalliance.org/aicm/LOG-15` is not answerable.**
It resolves to "Output Monitoring" under v1.0.3 and "Input Monitoring" under
v1.1.0, and the plain string carries nothing to choose between them. Only
`...aicm@1.0.3/LOG-15` and `...aicm@1.1.0/LOG-15` are questions with answers.

Three consequences:

**The resolver must not silently answer unversioned control-level queries.**
The AICM node in the SecID registry currently carries
`"version_required": false` with `"unversioned_behavior": "current_with_history"`.
For the *framework* that is fine — "AICM" reasonably means the current AICM.
For a *control inside it*, "current" is exactly the failure mode: the answer
changes under the caller without the query changing. A caller that asked in
May 2026 and again in July 2026 gets two different controls and no signal.

**Stored references are the real exposure.** Anything that persisted a bare
AICM control ID — crosswalks, STAR submissions, mapping tables, this repo's own
derived data — is now ambiguous. It was written against a version; that version
was not recorded; the identifier still resolves; the answer is different. This
is the failure SecID exists to make impossible, and it is invisible unless the
registry is explicit about it.

**A version list is not enough.** Knowing that 1.0.3 and 1.1.0 both exist does
not tell a consumer that `LOG-15` moved between them. The registry needs the
*discontinuity* recorded, not just the versions.

---

## 3. Standing policy — assume it recurs

CSA has renumbered AICM once without flagging it. Plan for v1.2 doing the same.

### On acquiring any new AICM release

1. **Never overwrite a version directory.** New release, new directory. This is
   already the repo convention and this is the reason for it.
2. **Name the directory from the artifact's own version stamp**, not the
   download page, and record every other label CSA uses in `version_aliases`.
   CSA has published this release as both "v1.1" and "1.1.0"; expect the same
   split next time.
3. **Generate the per-control changelog** with
   [`crosswalks/build_changelog.py`](crosswalks/build_changelog.py) and commit it.
   CSA's Change Log worksheet states intent, not the delta — for 1.1.0 it omitted
   every renumbering and every rewritten specification.
4. **Diff by content, never by ID.** Run
   [`crosswalks/build_crosswalk.py`](crosswalks/build_crosswalk.py) against the
   previous release before doing anything else.
5. **Commit the crosswalk** as `crosswalks/aicm-<old>-to-<new>-crosswalk.csv`.
   It is the only artifact that lets a downstream consumer migrate stored
   references, and CSA does not publish one.
6. **Read the change log, then distrust it.** It records intent. It has already
   proven silent on renumbering and wrong about mapping coverage.
7. **Re-verify the parsers.** Column layouts and sheet names move between
   releases. See [`1.0.3/scripts/`](1.0.3/scripts/) and the notes in
   [`1.1.0/aicm-1.1.0-metadata.json`](1.1.0/aicm-1.1.0-metadata.json).
8. **Report the renumbering count in the PR.** "N of M shared IDs now point
   somewhere else" is the review-critical number.

### On writing AICM references anywhere

- **Always qualify with a version.** `AICM 1.1.0 LOG-15`, never `AICM LOG-15`.
  In SecID form, `secid:control/cloudsecurityalliance.org/aicm@1.1.0/LOG-15`.
- **A control ID plus a title is still not enough** — six controls in this
  release kept both and changed meaning. Pin the version.
- **Never migrate a reference by string match.** `LOG-15` → `LOG-15` is wrong
  53 times over in this release. Migrate through the crosswalk.

### On the crosswalk's limits

The crosswalk is **reconstructed, not authoritative**. CSA publishes no
old-ID → new-ID mapping, so it is inferred from specification-text similarity.
The 11 rows flagged `review_needed=yes` are genuine judgment calls, mostly where
a control was simultaneously renumbered *and* rewritten — `IAM-02`, `SEF-07`,
`SEF-09`, and `IAM-14`/`IAM-15` are the contested ones. Those need
working-group confirmation before anyone relies on them for compliance
purposes.

That limitation is itself the argument: **once a renumbering ships without a
crosswalk, the mapping cannot be fully recovered afterward.** The only reliable
fix is to record the version at the time the reference is written.

---

## 4. Files

| Path | What |
|---|---|
| [`0.0.2/`](0.0.2/) | Pre-release draft (`aicm@0.0.2`) |
| [`1.0.3/`](1.0.3/) | AICM v1.0.3 — 243 controls. Last release carrying NIST AI 600-1 mappings. [README](1.0.3/README.md) |
| [`1.1.0/`](1.1.0/) | AICM v1.1.0 — 247 controls, current. Parsers in [`1.1.0/scripts/`](1.1.0/scripts/). [README](1.1.0/README.md) |
| [`crosswalks/build_crosswalk.py`](crosswalks/build_crosswalk.py) | Content-based crosswalk generator |
| [`crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv`](crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv) | Machine-readable old-ID → new-ID mapping, one row per control |
| [`crosswalks/aicm-1.0.3-to-1.1.0-changelog.md`](crosswalks/aicm-1.0.3-to-1.1.0-changelog.md) | **Per-control changelog** — every control in either release with a verdict, including "unchanged" |
| [`crosswalks/aicm-1.0.3-to-1.1.0-changelog.json`](crosswalks/aicm-1.0.3-to-1.1.0-changelog.json) | Same, machine-readable |
| [`crosswalks/build_changelog.py`](crosswalks/build_changelog.py) | Generates both from the extractions + crosswalk |

The AI-CAIQ companion versions in lockstep and inherits every problem on this
page — question IDs are derived from control IDs, so `LOG-15.1` moved too. See
[`../aicm-caiq/`](../aicm-caiq/).
