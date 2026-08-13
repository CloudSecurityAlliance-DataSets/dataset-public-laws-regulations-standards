# Upstream Publication Observations

**Status:** Design — approved in conversation 2026-08-13, pending written review
**Scope:** `METADATA-SCHEMA.md` (new `upstream` object), `CLAUDE.md` (no-bulk-mirror rule), seed application to 14 sources

## Problem

This repository decides, per document, whether to commit upstream data or point at it. The governing rule (CLAUDE.md, "Don't bulk-mirror data that's already publicly available upstream") is sound but is applied from memory, one source at a time, with no record of *what was observed* about the upstream that justified the decision.

Two consequences showed up on 2026-08-12 while sweeping `ttp/mitre.org/`:

1. **Stale mirrors accumulated.** `d3fend.csv` held 184 rows against upstream's 272. `fight.yaml` held 624 KB against upstream's 1.14 MB, missing its entire `campaigns:` section. `reference/mitre.org/ctid/` holds ~6.3 MB across 44 files, in eight directories that each declare `desired_end_state: metadata-only / upstream-only` in their own metadata.
2. **Metadata asserted things that were never true or had stopped being true.** ATT&CK was recorded at v16.1 (three majors behind), its license as "Apache-2.0 for code" (it is the MITRE ATT&CK license; Apache-2.0 belongs to `attack-navigator`, a different repo), CAPEC as "actively maintained" (no release since 2023-01-24), D3FEND under a bespoke `LicenseRef` (the ontology repo ships verbatim MIT).

Both failures share a root cause: nothing in the repository records observable facts about how an upstream publishes, when they were last checked, or how to verify them again.

## What this is not

**This is not a rating system.** An earlier draft of this design scored sources on numbered maturity ladders. That was rejected, correctly: this repository is a dataset, and a dataset states facts. `pinning: 2` is an opinion; `git tags 1.0.0 through 1.5.0, no GitHub Releases, releases API returns empty` is a fact, and it is strictly more useful because a consumer can draw their own conclusion *and* re-verify it.

Interpretation belongs to consumers. Where this repository itself needs to interpret — the no-bulk-mirror decision is our own policy — that interpretation lives in `CLAUDE.md` and in `desired_end_state`, not in the observation record.

**This is not a SecID `disclosure` record.** SecID's `disclosure` type is vulnerability disclosure: its subtypes are `coordinator` and `psirt`, with `cna` / `bug-bounty` / `security.txt` carried as first-class structured fields (verified against the live `TYPES-AND-SUBTYPES.md`, 2026-08-13). "There is an error in your data" and "there is a vulnerability in your product" are different routes to different teams. We record the former; the latter remains a SecID `disclosure` concern.

SecID's own governing rule points at the right shape, though:

> subtypes name provisional, still-emergent groupings we want to identify but aren't set in stone; a fact important enough to earn explicit first-class support graduates into a structured field — and must not then be duplicated as a subtype (one source of truth).

Contact-and-reporting routes are structured fields there. They are structured fields here too. This repository is the source of truth; SecID consumes.

## Principles

1. **Facts, not judgements.** Record what was observed and where it can be re-checked.
2. **No numbers.** No scores, levels, or ratings. Brief prose values.
3. **No evaluative adjectives in values.** Not "poor contribution guidance" but `no CONTRIBUTING.md, no issue templates`. Not "excellent pinning" but `GitHub Releases tagged vN.N; index.json enumerates all 41 Enterprise releases`. A verdict smuggled in as a word is still a verdict.
4. **Named keys, prose values.** Fixed keys stay greppable and diffable across 500+ directories; prose values avoid forcing false precision. An unknown fact is an absent key, never a fabricated zero.
5. **Dated observations.** Facts decay. Every channel and every feedback route carries `verified`.
6. **Rate what the evidence shows, not what the repository advertises.** FiGHT has an issue tracker enabled and zero issues ever filed. ATT&CK has no `CONTRIBUTING.md` and demonstrably active triage. Affordances and behaviour diverge in both directions.

## Schema

One new optional object per document directory, alongside the existing `links`, `lifecycle`, and `desired_end_state`. Nothing existing changes shape.

```json
"upstream": {
  "verified": "2026-08-13",
  "channels": [ { ... } ],
  "feedback": [ { ... } ]
}
```

### `channels[]`

A source may publish the same content several ways, and the ways differ. ATT&CK ships STIX 2.1 and STIX 2.0 from two repositories plus a per-technique website. ATLAS's authoritative channel (bespoke YAML) is not its standard-format channel (STIX), and the standard-format one lags. One entry per channel.

| Key | Records |
|---|---|
| `id` | Short slug, unique within the source (`stix-2.1`, `yaml-dist`, `website`) |
| `url` | Where the channel lives |
| `authoritative` | Boolean. Is this the channel the publisher treats as canonical, or a derived rendering? |
| `format` | The serialization, and whether it is an external standard or the publisher's own |
| `version_control` | Whether the data sits in a VCS, and whether it is the repository's primary artifact or incidental to something else |
| `pinning` | How a specific version is named and fetched: releases, tags, version-stamped URLs, a version field inside the payload, or nothing |
| `addressing` | Granularity. One blob, one file per item, internal IDs requiring a parse, resolvable per-item URLs |
| `identifiers` | The ID scheme, and what happens to an ID when the underlying thing is renamed, merged, or retired |
| `currency` | Latest version and date; observed cadence; whether this channel lags another |
| `license` | What the channel's own LICENSE file says, as read — not what a license detector reports |
| `notes` | Anything else observed that does not fit above |

All values optional. Omit what has not been checked rather than guessing.

### `feedback[]`

How to tell the publisher about a problem in the data. One entry per route.

| Key | Records |
|---|---|
| `route` | URL or address |
| `kind` | `public issue tracker`, `email`, `mailing list`, `web form`, `contribution portal` |
| `intake` | What structure exists: `CONTRIBUTING.md`, issue templates, DCO, PR policy |
| `observed` | What actually happens — open/closed counts, response evidence, traceability from report to release |
| `verified` | Date this was checked |

## Worked examples

All values below were verified on 2026-08-12/13.

### ATT&CK

```json
"upstream": {
  "verified": "2026-08-13",
  "channels": [
    {
      "id": "stix-2.1",
      "url": "https://github.com/mitre-attack/attack-stix-data",
      "authoritative": true,
      "format": "STIX 2.1; open standard (OASIS), multiple independent implementations",
      "version_control": "git; the data is the repository's primary artifact",
      "pinning": "GitHub Releases tagged vN.N; v19.2 current, released 2026-08-05. index.json enumerates every released version (41 for Enterprise)",
      "addressing": "one bundle per matrix (~50 MB Enterprise, ~4 MB Mobile, ~4 MB ICS); no per-object files; objects carry STIX ids and external_id",
      "identifiers": "external_id where source_name starts with 'mitre': TA####, T####[.###], S####, G####, C####, M####, DS####, A#### (ICS), AN####/DET####/DC#### (added v18). revoked and x_mitre_deprecated flags plus revoked-by relationships allow retired ids to be followed forward; the v19.2 ICS bundle carries 11 revoked, 37 deprecated, 11 revoked-by",
      "currency": "v19.2 for all three matrices, 2026-08-05; roughly twice-yearly majors plus patch releases",
      "license": "LICENSE.txt is the MITRE ATT&CK license, not Apache-2.0; GitHub's detector reports NOASSERTION. Requires reproducing the copyright designation verbatim"
    },
    {
      "id": "stix-2.0",
      "url": "https://github.com/mitre/cti",
      "authoritative": false,
      "format": "STIX 2.0; open standard, legacy serialization of the same content",
      "pinning": "GitHub Releases tagged ATT&CK-vN.N; ATT&CK-v19.2 released 2026-08-05, within minutes of the 2.1 repo",
      "notes": "also carries the CAPEC STIX distribution under capec/2.0/ and capec/2.1/"
    },
    {
      "id": "website",
      "url": "https://attack.mitre.org/",
      "authoritative": false,
      "format": "HTML",
      "addressing": "one page per object, machine-fetchable (e.g. /techniques/T1195)",
      "pinning": "none; serves current version only"
    }
  ],
  "feedback": [
    {
      "route": "https://github.com/mitre-attack/attack-stix-data/issues",
      "kind": "public issue tracker",
      "intake": "no CONTRIBUTING.md and no issue templates in either ATT&CK repository",
      "observed": "18 open. mitre/cti triages actively: #240, a missing Stealth tactic in the v19 Enterprise TAXII feed, was closed with discussion 2026-05-10. 493 forks on mitre/cti, 136 on attack-stix-data",
      "verified": "2026-08-13"
    }
  ]
}
```

### ATLAS

The case that motivated the whole design: strong on every observable except identifiers.

```json
"channels": [
  {
    "id": "yaml-dist",
    "url": "https://github.com/mitre-atlas/atlas-data",
    "authoritative": true,
    "format": "YAML, publisher's own schema; JSON Schema published under dist/schemas/",
    "pinning": "GitHub Releases, CalVer monthly; v2026.07 current. dist/manifest.yaml indexes release to format-version to path. Switched from semver after v5.6.0 (2026-05-04)",
    "addressing": "one file per release (717 KB at 2026.07); techniques/tactics/mitigations/case-studies keyed by ID in mappings, so an item is addressable only after parsing",
    "identifiers": "AML.TA####, AML.T####[.###], AML.M####, AML.CS####. No deprecation mechanism: AML.T0019, AML.T0058 and AML.T0104 were deleted outright between 2026.04 and 2026.07, folded into AML.T0115 sub-techniques, with no revoked-by, no deprecated flag and no redirect; the mapping appears only in CHANGELOG prose. Object uuid values are UUIDv5, derived from names, so they change on rename — all three retired techniques' UUIDs are absent from 2026.07, while the 167 IDs present in both releases showed no UUID drift",
    "currency": "v2026.07 released 2026-08-07, dated 2026-07-31; monthly",
    "license": "Apache-2.0"
  },
  {
    "id": "stix",
    "url": "https://github.com/mitre-atlas/atlas-navigator-data",
    "authoritative": false,
    "format": "STIX 2.1; also ATT&CK Navigator layers and OpenCTI bundles",
    "currency": "lags atlas-data; dist/stix-atlas.json carried 170 attack-patterns on 2026-08-12, matching the 2026.04 snapshot",
    "identifiers": "same UUIDv5 values as the YAML (AML.T0000 is attack-pattern--c02f812d-...); zero objects carry revoked or x_mitre_deprecated"
  },
  {
    "id": "website",
    "url": "https://atlas.mitre.org/",
    "authoritative": false,
    "format": "HTML",
    "addressing": "one page per object, but client-side routed — URLs resolve in a browser and return HTTP 404 to direct server requests (recorded in the SecID registry)"
  }
],
"feedback": [
  {
    "route": "https://github.com/mitre-atlas/atlas-data/issues",
    "kind": "public issue tracker",
    "intake": "CONTRIBUTING.md present, states issues and pull requests welcome, includes Developer's Certificate of Origin 1.1; separate contribution portal at https://atlas.mitre.org/contribute; no issue templates",
    "observed": "14 open, 43 forks. Issues are substantive content proposals (new mitigations, new case studies, wording corrections). The four most recent (#19, #21, #22, #23) each have zero comments",
    "verified": "2026-08-13"
  }
]
```

### FiGHT

```json
"channels": [
  {
    "id": "yaml",
    "url": "https://github.com/mitre/FiGHT",
    "authoritative": true,
    "format": "YAML, publisher's own schema",
    "version_control": "git, but the repository is a built Nuxt static website (_nuxt/, index.html, CNAME) with the data included in the deploy artifact rather than published as a first-class dataset",
    "pinning": "none. No GitHub Releases, no tags. The data's own version fields are largely empty strings. Commit SHA is the only stable reference; HEAD is 097cd5f73811, committed 2025-11-14",
    "addressing": "one fight.yaml (1.14 MB) plus per-object sources under raw-fight-data/ and fight-data/. Top-level keys: tactics, techniques, mitigations, 'data sources' (with a space), groups, software, campaigns, case-studies",
    "identifiers": "tactics reuse ATT&CK tactic IDs verbatim (TA0001, TA0042, TA0043). Techniques split by lineage: FGT1### align to ATT&CK T1### (113 of 183), FGT5### are 5G-original (70 of 183). Also FGM####, FGDS####[.###], FGG5###, FGS5###; campaigns mix reused ATT&CK IDs (C0024) with FiGHT-original (FGC5001)",
    "currency": "no commits since 2025-11-14",
    "license": "LICENSE.txt present; GitHub reports NOASSERTION"
  }
],
"feedback": [
  {
    "route": "https://github.com/mitre/FiGHT/issues",
    "kind": "public issue tracker",
    "intake": "no CONTRIBUTING.md, no issue templates",
    "observed": "enabled; zero issues ever, across all states. 7 forks",
    "verified": "2026-08-13"
  }
]
```

### CAPEC

```json
"channels": [
  {
    "id": "xml",
    "url": "https://capec.mitre.org/data/xml/capec_latest.xml",
    "authoritative": true,
    "format": "XML, publisher's own schema; XSD published",
    "version_control": "none; direct download only",
    "pinning": "no tags or releases. Version and Date attributes on the XML root element are the only version identifier; capec_latest.xml is an unversioned URL",
    "addressing": "one catalog (~3.8 MB). Attack patterns, categories and views share one CAPEC-<n> ID space, so a bare ID does not indicate object kind",
    "currency": "Version=\"3.9\" Date=\"2023-01-24\"; HTTP Last-Modified agrees. No release since",
    "license": "MITRE CAPEC Terms of Use"
  },
  {
    "id": "stix",
    "url": "https://github.com/mitre/cti/tree/master/capec",
    "authoritative": false,
    "format": "STIX 2.0 and 2.1; open standard",
    "notes": "distributed in the ATT&CK CTI repository; usage documented in USAGE-CAPEC.md"
  },
  {
    "id": "website",
    "url": "https://capec.mitre.org/data/definitions/",
    "authoritative": false,
    "format": "HTML",
    "addressing": "one page per pattern, machine-fetchable"
  }
],
"feedback": [
  {
    "route": "capec@mitre.org",
    "kind": "email",
    "intake": "no published contribution process",
    "observed": "no public repository and no public issue tracker for CAPEC itself; a report leaves no visible record. capec-research-list@mitre.org is also published on the site",
    "verified": "2026-08-13"
  }
]
```

### D3FEND

```json
"channels": [
  {
    "id": "ontology-source",
    "url": "https://github.com/d3fend/d3fend-ontology",
    "authoritative": true,
    "format": "OWL/Turtle sources; open standard (W3C)",
    "version_control": "git with source under src/ontology/, Makefile, CI, Dockerfile, CONTRIBUTING.md, CHANGELOG.md",
    "pinning": "git tags 1.0.0 through 1.5.0. No GitHub Releases — the releases API returns an empty list. Resolve by tag",
    "currency": "1.5.0 dated 2026-07-31; roughly quarterly tags, near-daily commits",
    "license": "LICENSE.md is verbatim MIT, Copyright (c) 2022 The MITRE Corporation",
    "notes": "each release's CHANGELOG records the versions of other frameworks it maps against — 1.5.0 pins ATT&CK v19.0, ATLAS v2026.06, SPARTA v3.2"
  },
  {
    "id": "built-distributions",
    "url": "https://d3fend.mitre.org/ontologies/",
    "authoritative": false,
    "format": "d3fend.csv, d3fend.owl, d3fend.ttl, d3fend.json",
    "pinning": "none; unversioned URLs always serve the current release. No path exists to fetch a prior version's built artifact",
    "addressing": "one file per format. CSV columns: ID, D3FEND Tactic, D3FEND Technique, D3FEND Technique Level 0, D3FEND Technique Level 1, Definition",
    "identifiers": "D3-XXX, where the suffix is a mnemonic rather than a number (D3-OAM = Operational Activity Mapping)",
    "notes": "served from GitHub Pages"
  }
],
"feedback": [
  {
    "route": "https://github.com/d3fend/d3fend-ontology/issues",
    "kind": "public issue tracker",
    "intake": "CONTRIBUTING.md present; issue template new-d3fend-technique-proposal.md",
    "observed": "187 open across 643 issue numbers; issues closed same-day (#640, #641 on 2026-08-12). CHANGELOG entries cite issue numbers, so a report can be traced to the release that shipped its fix",
    "verified": "2026-08-13"
  }
]
```

## Relationship to the no-bulk-mirror rule

`CLAUDE.md`'s rule is a policy and stays a policy. What changes is that it can cite recorded observations instead of relying on recall, and that its existing exception stops being a special case.

Current exception: *"if structured-extraction from a PDF/XLSX produces the first machine-readable form of a doc, commit the derived structured form."* Restated against observations, that is simply what a source with no machine-readable channel gets. PCI DSS v4.0.1 is published only as a PDF behind a document library, with no repository, no tags and no structured distribution, so the marker extraction and `parse_pci_dss.py` output are the first machine-readable forms — same answer as today, now derivable from a recorded fact rather than asserted.

**A caution about that exception, discovered while writing this spec.** CLAUDE.md currently names NIST SP 800-53 r5 as the exception's worked example. That example does not survive checking: NIST publishes 800-53 rev5 as **OSCAL** in [`usnistgov/oscal-content`](https://github.com/usnistgov/oscal-content) — `nist.gov/SP800-53/rev5/` in JSON, XML and YAML, with tagged releases (v1.5.0, 2026-05-13). OSCAL is an external standard with independent implementations. So 800-53 r5 has a pinnable, standard-format, machine-readable upstream channel, and the local `800-53-r5-controls.json` (derived from the NIST XLSX via `extract_800_53.py`) is *not* the first machine-readable form of that content.

That does not automatically make the local extraction wrong — it is derived from a different source artifact and has a different shape — but the stated justification for it is wrong, and CLAUDE.md's exception needs a different worked example. Recording the OSCAL channel as an observation on `control/nist.gov/800-53/r5` is the fix; whether the local derivation should survive alongside it is a separate decision, listed as an open item.

This is the model working as intended: the observation record is what turns "we have always said this" into a checkable claim.

The rule's revision should read the observations and say, in prose:

- A channel that is version-pinnable and license-permitting should be pointed at, not copied.
- A channel with no pinning mechanism cannot be safely pointed at; if it is needed offline, snapshot it with the commit SHA or retrieval date recorded.
- A source with no machine-readable channel is extracted, and the derived form is committed.

Note the consequence for FiGHT: it has no pinning mechanism at all, which puts it in the second case, not the first. **The 2026-08-12 removal of `fight.yaml` and `fight.json` (PR #115) may therefore have been the wrong call** — a dated snapshot pinned to `097cd5f73811` is arguably the correct handling. Flagged as an open item below rather than silently reversed.

## Scope

Seed set of 14 sources, chosen because they are the ones already examined in depth:

- `ttp/mitre.org/` — attack, atlas, capec, d3fend, fight (observations complete, above)
- `reference/mitre.org/ctid/` — AWS, azure, cve, gcp, m365, nist_800_53, veris (observations **not yet gathered**)
- `weakness/mitre.org/cwe/` (observations **not yet gathered**)

Everything else gets the `upstream` object as it is touched. A document with no machine-readable upstream simply omits the object.

## Non-goals

- No scoring, ranking, or maturity level, now or later.
- No automated verification of the observations in this pass. A checker that re-fetches and diffs recorded facts is a plausible follow-on but is not in scope.
- No change to `desired_end_state`, `links`, `lifecycle`, or any existing field.
- No SecID registry changes. SecID consumes this when it chooses to; this design does not depend on that.

## Deliverables

1. `METADATA-SCHEMA.md` — new `### Upstream Observations` section defining `channels[]` and `feedback[]`, the six principles, and the no-evaluative-adjectives rule.
2. `CLAUDE.md` — no-bulk-mirror rule revised to reference observations and restate its exception in those terms.
3. The five `ttp/mitre.org/` metadata files populated with the observations above.
4. CTID (8) and CWE observations gathered and populated.

## Open items

1. **PR #115 and FiGHT.** Under this model FiGHT is the "snapshot with a recorded SHA" case, not the pointer-only case. Decide whether to restore `fight.yaml` pinned to `097cd5f73811` with the SHA recorded, or leave #115 as merged.
2. **CTID.** ~6.3 MB across 44 files in eight directories that declare themselves `metadata-only`, mapping ATT&CK 8.2–14.1 against a current 19.2, with every version still available upstream. Decision deferred from 2026-08-12 and unaffected by this design, which explains the situation but does not resolve it.
3. **NIST 800-53 r5 and OSCAL.** The local `800-53-r5-controls.json` is derived from the NIST XLSX, but NIST also publishes rev5 as tagged OSCAL. Record the OSCAL channel as an observation, then decide separately whether the local derivation still earns its place or should be replaced by a pointer. The same question likely applies to the other NIST documents in `usnistgov/oscal-content` — CSF, SP800-171, SP800-172, SP800-218 — all of which this repository also holds.
4. **Integrity/provenance.** Signed releases and published checksums would be a legitimate observation key. None was observed on any source examined so far, so the key is not defined yet; add it when a source earns it rather than carrying an empty column.
