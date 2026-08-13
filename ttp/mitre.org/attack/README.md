# MITRE ATT&CK

A curated knowledge base of adversary tactics and techniques based on real-world observations, organized into three matrices (Enterprise, Mobile, ICS). ATT&CK is the de facto industry vocabulary for describing adversary behavior.

| | |
|---|---|
| **SecID** | `secid:ttp/mitre.org/attack` |
| **Upstream version** | v19.2 — all three matrices (2026-08-05) |
| **License** | MITRE ATT&CK Terms of Use (free use with attribution) |
| **Status** | Active — roughly twice-yearly majors plus patch releases |
| **In this directory** | Metadata only. See [What's here](#whats-in-this-directory). |

## Upstream

ATT&CK is published on GitHub in two parallel repositories. **Both are current** — they were tagged v19.2 within minutes of each other — and the difference is the STIX serialization, not the content.

| Repo | Format | Notes |
|---|---|---|
| [`mitre-attack/attack-stix-data`](https://github.com/mitre-attack/attack-stix-data) | **STIX 2.1** | Canonical. Prefer this for new work. Ships `index.json` cataloguing every released version (41 Enterprise releases as of v19.2). |
| [`mitre/cti`](https://github.com/mitre/cti) | STIX 2.0 | Legacy serialization, still maintained. Also carries the CAPEC STIX distribution under `capec/`. |

Supporting projects: [`attack-navigator`](https://github.com/mitre-attack/attack-navigator) (Apache-2.0, layer visualization) and [`mitreattack-python`](https://github.com/mitre-attack/mitreattack-python) (Python library).

The rendered site is <https://attack.mitre.org/>.

## Getting the data

Pin to a release tag — never track `master`.

```bash
# Enterprise matrix, pinned (~50 MB)
curl -LO https://raw.githubusercontent.com/mitre-attack/attack-stix-data/v19.2/enterprise-attack/enterprise-attack-19.2.json

# Mobile (~4 MB) and ICS (~4 MB)
curl -LO https://raw.githubusercontent.com/mitre-attack/attack-stix-data/v19.2/mobile-attack/mobile-attack-19.2.json
curl -LO https://raw.githubusercontent.com/mitre-attack/attack-stix-data/v19.2/ics-attack/ics-attack-19.2.json

# Discover available versions without cloning
curl -s https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/index.json | jq '.collections[] | {name, versions: [.versions[].version]}'
```

## Identifiers

ATT&CK IDs appear as `external_references[].external_id` where `source_name` starts with `mitre`. Prefixes observed in the v19.2 ICS bundle:

| Prefix | Object |
|---|---|
| `TA####` | Tactic |
| `T####`, `T####.###` | Technique, sub-technique |
| `S####` | Software |
| `G####` | Group |
| `C####` | Campaign |
| `M####` | Mitigation |
| `DS####` | Data source |
| `AN####`, `DET####`, `DC####` | Detection strategies, detections, and analytic components — **newer object types**; code written against pre-v18 ATT&CK will not know about these |
| `A####` | Asset (ICS) |

Unlike [ATLAS](../atlas/), ATT&CK **does** provide deprecation handling: objects carry `revoked` / `x_mitre_deprecated` flags and `revoked-by` relationships, so a reference to a retired ID can be followed forward programmatically. The v19.2 ICS bundle alone contains 11 revoked objects, 37 deprecated ones, and 11 `revoked-by` relationships.

Still pin the version — technique scope changes between majors, and the newer `AN`/`DET`/`DC` object types did not exist before v18.

## What's in this directory

Metadata only, per the repository's [no-bulk-mirror rule](../../../CLAUDE.md#dont-bulk-mirror-data-thats-already-publicly-available-upstream). The upstream bundles are large (~50 MB for Enterprise alone), authoritative, and version-tagged, so a copy here would add nothing but drift. Pull from upstream by tag.

## Relationship to sibling frameworks

- **[ATLAS](../atlas/)** — the AI/ML counterpart; many ATLAS techniques carry an `attack-reference` pointing back to an ATT&CK technique.
- **[FiGHT](../fight/)** — the 5G counterpart; reuses ATT&CK tactic IDs verbatim and mirrors ATT&CK technique numbering as `FGT1###`.
- **[D3FEND](../d3fend/)** — countermeasures mapped to ATT&CK techniques; each D3FEND release pins the ATT&CK version it maps against.
- **[CAPEC](../capec/)** — lower-level attack patterns; CAPEC's STIX form ships in `mitre/cti` alongside ATT&CK.

## Last verified

2026-08-12 — upstream at v19.2 (Enterprise, Mobile, ICS), released 2026-08-05.
