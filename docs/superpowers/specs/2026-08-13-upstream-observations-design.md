# Upstream Publication Observations

**Status:** Design — revised 2026-08-13 after review, pending approval
**Scope:** `METADATA-SCHEMA.md` (new `upstream` object), `CLAUDE.md` (no-bulk-mirror rule), metadata shape validation, seed application to the five `ttp/mitre.org/` sources

## Problem

Nothing in this repository records observable facts about how an upstream publishes its data, when those facts were last checked, or how to check them again. Everything is asserted from memory, one source at a time.

Two consequences surfaced on 2026-08-12 while sweeping `ttp/mitre.org/`:

1. **Stale mirrors accumulated.** `d3fend.csv` held 184 rows against upstream's 272. `fight.yaml` held 624 KB against upstream's 1.14 MB, missing its entire `campaigns:` section. `reference/mitre.org/ctid/` holds ~6.3 MB across 44 files, in eight directories that each declare `desired_end_state: metadata-only / upstream-only` in their own metadata.
2. **Metadata asserted things that were never true or had stopped being true.** ATT&CK was recorded at v16.1 (three majors behind v19.2); its license as "Apache-2.0 for code" (it is the MITRE ATT&CK license — Apache-2.0 belongs to `attack-navigator`, a different repository); CAPEC as "actively maintained" (no release since 2023-01-24); D3FEND under a bespoke `LicenseRef` (the ontology repository ships verbatim MIT).

Writing this spec surfaced a third, in `CLAUDE.md` itself — see [A correction this design surfaced](#a-correction-this-design-surfaced).

### Why this is worth recording, beyond our own decisions

The immediate motivation is this repository's no-bulk-mirror rule, but the observations are not only for us:

- **This repository is independently useful.** "How does MITRE publish ATLAS, how do you pin a version, and how do you report an error in it" is valuable to any consumer, whether or not they care about our mirroring policy.
- **This repository is a source for SecID.** SecID v1 lists identifiers and how to find them; v2 will hold a registry of the data itself, built independently but drawing on this repository as a parallel source. Publication facts recorded here feed that directly.
- **Coverage runs both ways.** Everything in this public repository should be covered in SecID; SecID will hold things that belong here and are not here yet. Facts recorded in a consistent shape make that reconciliation mechanical rather than manual.

## What this is not

**This is not a rating system.** An earlier draft scored sources on numbered maturity ladders. That was rejected, correctly: this repository is a dataset, and a dataset states facts. `pinning: 2` is an opinion. `git tags 1.0.0 through 1.5.0, no GitHub Releases, releases API returns empty` is a fact — more useful, because a consumer can draw their own conclusion *and* re-verify it.

Interpretation belongs to consumers. Where this repository must interpret — the no-bulk-mirror decision is our own policy — that interpretation lives in `CLAUDE.md` and in `desired_end_state`, never in the observation record.

**Feedback routes are expected to feed SecID's `disclosure` type**, which is being broadened beyond vulnerability disclosure to cover feedback and bug reporting generally. This design does not encode any assumption about that type's eventual shape: it records what was observed, and the mapping happens when SecID is ready. Note that "there is an error in your data" and "there is a vulnerability in your product" may still be different routes to different teams at the same publisher, and both are worth recording when both exist.

## Principles

1. **Facts, not judgements.** Record what was observed and where it can be re-checked.
2. **No numbers.** No scores, levels, or ratings.
3. **No evaluative adjectives in values.** Not "poor contribution guidance" but `no CONTRIBUTING.md, no issue templates`. Not "excellent pinning" but `GitHub Releases tagged vN.N; index.json enumerates all 41 Enterprise releases`. A verdict smuggled in as a word is still a verdict.
4. **One fact per value.** A value is a string holding a single fact, or an **array of strings** where several facts belong under one key. Long run-on values are the failure mode: they diff badly, and they hide the fact that several separate observations have been jammed together.
5. **Named keys.** Fixed keys stay greppable across 500+ directories. An unknown fact is an absent key, never a fabricated value.
6. **Dated observations.** Facts decay. Every channel and feedback route carries `verified`.
7. **Record what the evidence shows, not what the repository advertises.** FiGHT has an issue tracker enabled and zero issues ever filed. ATT&CK has no `CONTRIBUTING.md` and demonstrably active triage. Affordances and behaviour diverge in both directions.

## Where the object attaches

**`upstream` attaches to the source-level metadata file, whose `secid` is the *unversioned* identifier.**

Publication facts belong to the source, not to one of its versions. How MITRE publishes CCM is a fact about CCM, not about CCM 4.1. Recording it on each version directory would duplicate it across 3–4 files and guarantee the drift this design exists to prevent.

This mirrors SecID, which already distinguishes `secid:control/cloudsecurityalliance.org/ccm` from `secid:control/cloudsecurityalliance.org/ccm@4.1` — and mirroring SecID is required by `CLAUDE.md` regardless.

No new convention is needed. Source-level metadata files already exist and follow the standard `[dirname]-metadata.json` rule:

- `reference/mitre.org/ctid/ctid-metadata.json` → `secid:reference/mitre.org/ctid`
- `reference/nist.gov/ai-rmf-crosswalks/ai-rmf-crosswalks-metadata.json` → `secid:reference/nist.gov/ai-rmf-crosswalks`

`build_index.py` already indexes them as rows.

**Single-directory sources are already at source level.** All five `ttp/mitre.org/` frameworks have one directory each, so the seed set needs no restructuring.

**Multi-version sources mostly lack the file.** 12 of 522 sources have more than one version directory; only 2 have a source-level record. CCM, AICM, PCI DSS, CSF and others would each need one before they can carry `upstream`. That backfill is **sequenced as separate follow-on work** — it is independently valuable (it gives each source a SecID-resolvable unversioned record, supporting full SecID coverage) and this design should not be gated on it.

### Relationship to `links`

`links` is untouched. The division:

| | Records | Lives on |
|---|---|---|
| `upstream.channels[]` | How the publisher publishes, ongoing | source-level metadata |
| `links` | What we used for *this* version — the specific PDF, that release's page | version-level metadata |

These are different facts, not two homes for one fact.

## Schema

```json
"upstream": {
  "verified": "2026-08-13",
  "channels": [ { ... } ],
  "feedback": [ { ... } ]
}
```

### `channels[]`

A source may publish the same content several ways, and the ways differ. ATT&CK ships STIX 2.1 and STIX 2.0 from two repositories plus a per-technique website. ATLAS's primary channel (bespoke YAML) is not its standard-format channel (STIX), and the standard-format one lags. One entry per channel.

| Key | Records |
|---|---|
| `id` | Short slug, unique within the source (`stix-2.1`, `yaml-dist`, `website`) |
| `url` | Where the channel lives |
| `relationship` | How this channel relates to the source's others, stated factually — `"the repository the publisher updates first"`, `"same content as stix-2.1, serialized as STIX 2.0"`, `"generated from atlas-data"`. **Not** a boolean verdict about which is authoritative |
| `format` | The serialization, and whether it is an external standard or the publisher's own |
| `version_control` | Whether the data sits in a VCS, and whether it is the repository's primary artifact or incidental to something else |
| `pinning` | How a specific version is named and fetched: releases, tags, version-stamped URLs, a version field inside the payload, or nothing |
| `addressing` | Granularity — one blob, one file per item, internal IDs requiring a parse, resolvable per-item URLs |
| `identifiers` | The ID scheme, and what happens to an ID when the underlying thing is renamed, merged, or retired |
| `currency` | Latest version and date; observed cadence; whether this channel lags another |
| `license` | What the channel's own LICENSE file says, **as read** — not what a license detector reports |
| `notes` | Anything observed that does not fit above |
| `verified` | Date this channel was checked |

All keys optional except `id`. Omit what has not been checked rather than guessing. Any value may be a string or an array of strings.

**Sources with no machine-readable channel still get one.** A PDF-only regulation records `format`, `url`, and `pinning: "none"`. That is a fact worth having, and under a broadened SecID `disclosure` the feedback route matters regardless of format.

### `feedback[]`

How to tell the publisher about a problem in the data. One entry per route.

| Key | Records |
|---|---|
| `route` | URL or address |
| `kind` | `public issue tracker`, `email`, `mailing list`, `web form`, `contribution portal` |
| `intake` | What structure exists — `CONTRIBUTING.md`, issue templates, DCO, PR policy |
| `observed` | What actually happens — open/closed counts, response evidence, traceability from report to release |
| `verified` | Date this was checked |

## Worked examples

All values verified 2026-08-12/13.

### ATT&CK

```json
"upstream": {
  "verified": "2026-08-13",
  "channels": [
    {
      "id": "stix-2.1",
      "url": "https://github.com/mitre-attack/attack-stix-data",
      "relationship": "STIX 2.1 serialization; tagged v19.2 within minutes of the STIX 2.0 repository",
      "format": "STIX 2.1; open standard (OASIS), multiple independent implementations",
      "version_control": "git; the data is the repository's primary artifact",
      "pinning": [
        "GitHub Releases tagged vN.N; v19.2 current, released 2026-08-05",
        "index.json enumerates every released version (41 for Enterprise)"
      ],
      "addressing": [
        "one bundle per matrix: ~50 MB Enterprise, ~4 MB Mobile, ~4 MB ICS",
        "no per-object files; objects carry STIX ids and external_id"
      ],
      "identifiers": [
        "external_id where source_name starts with 'mitre'",
        "TA#### tactic; T####[.###] technique and sub-technique; S#### software; G#### group; C#### campaign; M#### mitigation; DS#### data source; A#### asset (ICS)",
        "AN####, DET####, DC#### are detection strategies, detections and analytic components, added in v18",
        "revoked and x_mitre_deprecated flags plus revoked-by relationships allow retired ids to be followed forward",
        "v19.2 ICS bundle carries 11 revoked, 37 deprecated, 11 revoked-by"
      ],
      "currency": "v19.2 for all three matrices, 2026-08-05; roughly twice-yearly majors plus patch releases",
      "license": [
        "LICENSE.txt is the MITRE ATT&CK license, not Apache-2.0",
        "GitHub's license detector reports NOASSERTION",
        "requires reproducing MITRE's copyright designation verbatim"
      ],
      "verified": "2026-08-13"
    },
    {
      "id": "stix-2.0",
      "url": "https://github.com/mitre/cti",
      "relationship": "same content as stix-2.1, serialized as STIX 2.0; tagged ATT&CK-v19.2 on 2026-08-05",
      "format": "STIX 2.0; open standard, legacy serialization",
      "notes": "also carries the CAPEC STIX distribution under capec/2.0/ and capec/2.1/",
      "verified": "2026-08-13"
    },
    {
      "id": "website",
      "url": "https://attack.mitre.org/",
      "relationship": "rendered site",
      "format": "HTML",
      "addressing": "one page per object, machine-fetchable (e.g. /techniques/T1195)",
      "pinning": "none; serves current version only",
      "verified": "2026-08-13"
    }
  ],
  "feedback": [
    {
      "route": "https://github.com/mitre-attack/attack-stix-data/issues",
      "kind": "public issue tracker",
      "intake": "no CONTRIBUTING.md and no issue templates in either ATT&CK repository",
      "observed": [
        "18 open on attack-stix-data; 136 forks",
        "mitre/cti triages actively: #240, a missing Stealth tactic in the v19 Enterprise TAXII feed, closed with discussion 2026-05-10",
        "493 forks on mitre/cti"
      ],
      "verified": "2026-08-13"
    }
  ]
}
```

### ATLAS

The case that motivated the design: strong on every observable except identifiers.

```json
"channels": [
  {
    "id": "yaml-dist",
    "url": "https://github.com/mitre-atlas/atlas-data",
    "relationship": "the repository the publisher updates first; atlas-navigator-data is generated from it",
    "format": "YAML, publisher's own schema; JSON Schema published under dist/schemas/",
    "pinning": [
      "GitHub Releases, CalVer monthly; v2026.07 current",
      "dist/manifest.yaml indexes release to format-version to path",
      "switched from semver after v5.6.0 (2026-05-04)"
    ],
    "addressing": [
      "one file per release; 717 KB at 2026.07",
      "techniques, tactics, mitigations and case-studies are keyed by ID in mappings, so an item is addressable only after parsing"
    ],
    "identifiers": [
      "AML.TA####, AML.T####[.###], AML.M####, AML.CS####",
      "no deprecation mechanism: AML.T0019, AML.T0058 and AML.T0104 were deleted outright between 2026.04 and 2026.07, folded into AML.T0115 sub-techniques, with no revoked-by, no deprecated flag and no redirect",
      "the retirement mapping appears only in CHANGELOG prose",
      "object uuid values are UUIDv5, derived from names, so they change on rename; all three retired techniques' UUIDs are absent from 2026.07",
      "the 167 IDs present in both 2026.04 and 2026.07 showed no UUID drift"
    ],
    "currency": "v2026.07 released 2026-08-07, dated 2026-07-31; monthly",
    "license": "Apache-2.0",
    "verified": "2026-08-13"
  },
  {
    "id": "stix",
    "url": "https://github.com/mitre-atlas/atlas-navigator-data",
    "relationship": "generated from atlas-data; lags it",
    "format": "STIX 2.1; also ATT&CK Navigator layers and OpenCTI bundles",
    "currency": "dist/stix-atlas.json carried 170 attack-patterns on 2026-08-12, matching the 2026.04 snapshot",
    "identifiers": [
      "same UUIDv5 values as the YAML; AML.T0000 is attack-pattern--c02f812d-59cc-5366-b1aa-7eb05154b772",
      "zero objects carry revoked or x_mitre_deprecated"
    ],
    "verified": "2026-08-13"
  },
  {
    "id": "website",
    "url": "https://atlas.mitre.org/",
    "relationship": "rendered site",
    "format": "HTML",
    "addressing": "one page per object, but client-side routed — URLs resolve in a browser and return HTTP 404 to direct server requests (also recorded in the SecID registry)",
    "verified": "2026-08-13"
  }
],
"feedback": [
  {
    "route": "https://github.com/mitre-atlas/atlas-data/issues",
    "kind": "public issue tracker",
    "intake": [
      "CONTRIBUTING.md states issues and pull requests are welcome",
      "includes Developer's Certificate of Origin 1.1",
      "separate contribution portal at https://atlas.mitre.org/contribute",
      "no issue templates"
    ],
    "observed": [
      "14 open, 43 forks",
      "issues are substantive content proposals: new mitigations, new case studies, wording corrections",
      "the four most recent (#19, #21, #22, #23) each have zero comments"
    ],
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
    "relationship": "the only data channel; published as part of the website build",
    "format": "YAML, publisher's own schema",
    "version_control": "git, but the repository is a built Nuxt static website (_nuxt/, index.html, CNAME) with the data included in the deploy artifact rather than published as a first-class dataset",
    "pinning": [
      "no GitHub Releases and no tags",
      "the data's own version fields are largely empty strings",
      "commit SHA is the only stable reference; HEAD is 097cd5f73811, committed 2025-11-14"
    ],
    "addressing": [
      "one fight.yaml, 1.14 MB; per-object sources also under raw-fight-data/ and fight-data/",
      "top-level keys: tactics, techniques, mitigations, 'data sources' (with a space), groups, software, campaigns, case-studies"
    ],
    "identifiers": [
      "tactics reuse ATT&CK tactic IDs verbatim: TA0001, TA0042, TA0043",
      "FGT1### techniques align to ATT&CK T1### (113 of 183); FGT5### are 5G-original (70 of 183)",
      "also FGM#### mitigation, FGDS####[.###] data source, FGG5### group, FGS5### software",
      "campaigns mix reused ATT&CK IDs (C0024) with FiGHT-original (FGC5001)"
    ],
    "currency": "no commits since 2025-11-14",
    "license": "LICENSE.txt present; GitHub's detector reports NOASSERTION",
    "verified": "2026-08-13"
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
    "relationship": "the publisher's own distribution",
    "format": "XML, publisher's own schema; XSD published",
    "version_control": "none; direct download only",
    "pinning": [
      "no tags or releases",
      "Version and Date attributes on the XML root element are the only version identifier",
      "capec_latest.xml is an unversioned URL"
    ],
    "addressing": [
      "one catalog, ~3.8 MB",
      "attack patterns, categories and views share one CAPEC-<n> ID space, so a bare ID does not indicate object kind"
    ],
    "currency": "Version=\"3.9\" Date=\"2023-01-24\"; HTTP Last-Modified agrees; no release since",
    "license": "MITRE CAPEC Terms of Use",
    "verified": "2026-08-13"
  },
  {
    "id": "stix",
    "url": "https://github.com/mitre/cti/tree/master/capec",
    "relationship": "STIX rendering distributed in the ATT&CK CTI repository",
    "format": "STIX 2.0 and 2.1; open standard",
    "notes": "usage documented in USAGE-CAPEC.md",
    "verified": "2026-08-13"
  },
  {
    "id": "website",
    "url": "https://capec.mitre.org/data/definitions/",
    "relationship": "rendered site",
    "format": "HTML",
    "addressing": "one page per pattern, machine-fetchable",
    "verified": "2026-08-13"
  }
],
"feedback": [
  {
    "route": "capec@mitre.org",
    "kind": "email",
    "intake": "no published contribution process",
    "observed": [
      "no public repository and no public issue tracker for CAPEC itself; a report leaves no visible record",
      "capec-research-list@mitre.org is also published on the site"
    ],
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
    "relationship": "the repository the publisher updates; the built distributions are generated from it",
    "format": "OWL/Turtle sources; open standard (W3C)",
    "version_control": "git with source under src/ontology/, plus Makefile, CI, Dockerfile, CONTRIBUTING.md and CHANGELOG.md",
    "pinning": [
      "git tags 1.0.0 through 1.5.0",
      "no GitHub Releases; the releases API returns an empty list",
      "resolve by tag"
    ],
    "currency": "1.5.0 dated 2026-07-31; roughly quarterly tags, near-daily commits",
    "license": "LICENSE.md is verbatim MIT, Copyright (c) 2022 The MITRE Corporation",
    "notes": "each release's CHANGELOG records the versions of other frameworks it maps against; 1.5.0 pins ATT&CK v19.0, ATLAS v2026.06 and SPARTA v3.2",
    "verified": "2026-08-13"
  },
  {
    "id": "built-distributions",
    "url": "https://d3fend.mitre.org/ontologies/",
    "relationship": "built from d3fend-ontology; served from GitHub Pages",
    "format": "d3fend.csv, d3fend.owl, d3fend.ttl, d3fend.json",
    "pinning": [
      "none; unversioned URLs always serve the current release",
      "no path exists to fetch a prior version's built artifact"
    ],
    "addressing": [
      "one file per format",
      "CSV columns: ID, D3FEND Tactic, D3FEND Technique, D3FEND Technique Level 0, D3FEND Technique Level 1, Definition"
    ],
    "identifiers": "D3-XXX, where the suffix is a mnemonic rather than a number (D3-OAM = Operational Activity Mapping)",
    "verified": "2026-08-13"
  }
],
"feedback": [
  {
    "route": "https://github.com/d3fend/d3fend-ontology/issues",
    "kind": "public issue tracker",
    "intake": [
      "CONTRIBUTING.md present",
      "issue template new-d3fend-technique-proposal.md"
    ],
    "observed": [
      "187 open across 643 issue numbers",
      "issues closed same-day (#640, #641 on 2026-08-12)",
      "CHANGELOG entries cite issue numbers, so a report can be traced to the release that shipped its fix"
    ],
    "verified": "2026-08-13"
  }
]
```

## Relationship to the no-bulk-mirror rule

`CLAUDE.md`'s rule is a policy and stays a policy. What changes is that it cites recorded observations instead of relying on recall, and its existing exception stops being a special case.

Restated against observations, the rule reads:

- A channel that is version-pinnable and license-permitting should be pointed at, not copied.
- A channel with **no pinning mechanism** cannot be safely pointed at. If it is needed offline, snapshot it with the commit SHA or retrieval date recorded.
- A source with **no machine-readable channel** is extracted, and the derived form is committed. This is the current exception, now derived from a recorded fact rather than asserted.

Consequence for FiGHT: it has no pinning mechanism at all, which places it in the second case, not the first. **The 2026-08-12 removal of `fight.yaml` and `fight.json` (PR #115) may therefore have been the wrong call** — a dated snapshot pinned to `097cd5f73811` is arguably correct. Flagged as an open item rather than silently reversed.

### A correction this design surfaced

`CLAUDE.md` currently names **NIST SP 800-53 r5** as the worked example for the exception — "structured extraction produces the *first* machine-readable form." That does not survive checking: NIST publishes 800-53 rev5 as **OSCAL** in [`usnistgov/oscal-content`](https://github.com/usnistgov/oscal-content), at `nist.gov/SP800-53/rev5/` in JSON, XML and YAML, with tagged releases (v1.5.0, 2026-05-13). OSCAL is an external standard with independent implementations, so 800-53 r5 does have a pinnable, standard-format machine-readable channel, and the local `800-53-r5-controls.json` (derived from the NIST XLSX) is not the first machine-readable form of that content.

That does not automatically make the local extraction wrong — it derives from a different source artifact and has a different shape — but its stated justification is wrong.

**PCI DSS v4.0.1 is the example that holds**, verified rather than assumed: published only as a PDF behind a document library, no repository, no tags, no structured distribution, and `parse_pci_dss.py` produces the first structured form.

## Validation

Two checks, both cheap, both separable from the harder problem of re-verifying facts:

1. **Metadata shape validation.** The repository has one validator, `audit_secid_alignment.py`, which checks that `secid` resolves. Nothing checks key names. A misspelled `pining` would silently do nothing across hundreds of files. Add key-name validation for the `upstream` object — either extending the existing script or as a new `validate_metadata.py`.
2. **`desired_end_state` contradiction check.** A directory declaring `metadata-only` while containing non-metadata data files is a mechanically detectable contradiction. This is the CTID case — eight directories that each state the rule correctly and hold 6.3 MB anyway — and it would also have caught `d3fend.csv` and `fight.yaml`. Worth adding to `build_index.py` **independently of this design**; it needs no observation records to work.

## Non-goals

- No scoring, ranking, or maturity level, now or later.
- No automated re-verification of recorded facts in this pass. A `recheck_upstream.py` that re-fetches and diffs is a named follow-on, not a deliverable here. `verified` dates are honest about age but do not by themselves solve staleness.
- No change to `links`, `lifecycle`, `desired_end_state` or any existing field.
- No SecID registry changes. SecID consumes this when it chooses to.

## Deliverables

1. `METADATA-SCHEMA.md` — new `### Upstream Observations` section defining `channels[]` and `feedback[]`, the seven principles, and the attachment rule.
2. `CLAUDE.md` — no-bulk-mirror rule revised to reference observations; exception's worked example changed from NIST 800-53 r5 to PCI DSS v4.0.1.
3. The five `ttp/mitre.org/` metadata files populated with the observations above.
4. Metadata shape validation for the `upstream` object.

## Sequenced follow-on work

1. **Source-level metadata backfill** — ~10 multi-version sources (CCM, AICM, PCI DSS, CSF and others) have no source-level `[dirname]-metadata.json` and cannot carry `upstream` until they do. Independently valuable for SecID coverage.
2. **CTID and CWE observations** — not yet gathered.
3. **`recheck_upstream.py`** — re-fetch and diff recorded facts.

## Open items

1. **PR #115 and FiGHT.** Under this model FiGHT is the "snapshot with a recorded SHA" case, not the pointer-only case. Decide whether to restore `fight.yaml` pinned to `097cd5f73811`, or leave #115 as it stands.
2. **CTID.** ~6.3 MB across 44 files in eight directories that declare themselves `metadata-only`, mapping ATT&CK 8.2–14.1 against a current 19.2, with every version still available upstream. Explained by this design, not resolved by it.
3. **NIST OSCAL.** Record the OSCAL channel on `control/nist.gov/800-53/r5`, then decide separately whether the local derivation still earns its place. The same question applies to CSF, SP800-171, SP800-172 and SP800-218, all of which are in `oscal-content` and all of which this repository also holds.
4. **Integrity and provenance.** Signed releases and published checksums would be a legitimate key. None was observed on any source examined, so it is not defined yet — add it when a source earns it rather than carrying an empty column.
