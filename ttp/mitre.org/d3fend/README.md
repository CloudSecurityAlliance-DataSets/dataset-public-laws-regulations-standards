# MITRE D3FEND

A knowledge graph of cybersecurity **countermeasures** — the defensive counterpart to ATT&CK. D3FEND is an OWL ontology rather than a flat matrix, modelling defensive techniques and the digital artifacts they operate on, developed with NSA sponsorship.

| | |
|---|---|
| **SecID** | `secid:ttp/mitre.org/d3fend` |
| **Upstream version** | 1.5.0 (2026-07-31) |
| **License** | **MIT** — the ontology repository is MIT-licensed |
| **Status** | Active — quarterly-ish tagged releases, near-daily commits |
| **In this directory** | Metadata only. See [What's here](#whats-in-this-directory). |

Tactics: Model, Harden, Detect, Isolate, Deceive, Evict, Restore.

## Upstream

| Repo | Contents |
|---|---|
| [`d3fend/d3fend-ontology`](https://github.com/d3fend/d3fend-ontology) | **Canonical source.** Ontology sources under `src/ontology/`, build tooling, `CHANGELOG.md` |
| [`d3fend/d3fend`](https://github.com/d3fend/d3fend) | The public static website — <https://d3fend.mitre.org/> is served from GitHub Pages |

Built distributions are published at `d3fend.mitre.org/ontologies/`, **not** as GitHub release assets. Note that `d3fend-ontology` has **no GitHub Releases** — versions are git **tags** (`1.0.0` … `1.5.0`). Resolve a version by tag, not by release API.

## Getting the data

```bash
# Built distributions (current release)
curl -LO https://d3fend.mitre.org/ontologies/d3fend.csv    # flattened technique table
curl -LO https://d3fend.mitre.org/ontologies/d3fend.owl    # OWL/XML
curl -LO https://d3fend.mitre.org/ontologies/d3fend.ttl    # Turtle
curl -LO https://d3fend.mitre.org/ontologies/d3fend.json   # JSON

# Pin to a tagged version from source
git clone --depth 1 --branch 1.5.0 https://github.com/d3fend/d3fend-ontology
```

The `d3fend.csv` columns are: `ID, D3FEND Tactic, D3FEND Technique, D3FEND Technique Level 0, D3FEND Technique Level 1, Definition`.

⚠ The `d3fend.mitre.org/ontologies/` URLs are **unversioned** — they always serve the current release. There is no way to fetch a prior version's built artifact from that path; use a git tag for reproducibility.

## Identifiers

D3FEND technique IDs take the form `D3-XXX`, where the suffix is a mnemonic rather than a number — e.g. `D3-OAM` (Operational Activity Mapping). This differs from every sibling framework here, all of which use zero-padded numeric IDs.

## D3FEND as a crosswalk

Worth knowing beyond the countermeasure catalog: each D3FEND release records the **exact versions of other frameworks it maps against**, which makes it a dated crosswalk between them. From the 1.5.0 changelog:

- ATT&CK **v19.0** and ATLAS **v2026.06** mappings
- ATT&CK for ICS mappings (T0800–T0895)
- SPARTA (space systems) v3.2 artifact mappings
- OCSF event mappings via `seeAlso` links

If you need "which ATT&CK version does this mapping correspond to," D3FEND's changelog answers it explicitly — most crosswalks don't.

## What's in this directory

Metadata only, per the repository's [no-bulk-mirror rule](../../../CLAUDE.md#dont-bulk-mirror-data-thats-already-publicly-available-upstream).

This directory previously held a committed `d3fend.csv` snapshot. It was removed on 2026-08-12 after it was found to contain **184 rows against upstream's 272** — 88 techniques missing. That drift is exactly what the no-mirror rule exists to prevent. Fetch from upstream instead; the file remains in git history and in S3.

## Relationship to sibling frameworks

- **[ATT&CK](../attack/)** — D3FEND countermeasures map to ATT&CK techniques; the defensive-to-offensive pairing is D3FEND's primary use case.
- **[ATLAS](../atlas/)** — mapped as of D3FEND 1.5.0 (ATLAS v2026.06).
- **[CAPEC](../capec/)** — D3FEND countermeasures defend against CAPEC attack patterns.

## Last verified

2026-08-12 — upstream at 1.5.0; `d3fend.csv` served from `d3fend.mitre.org` had 272 rows.
