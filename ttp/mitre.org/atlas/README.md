# MITRE ATLAS

Adversarial Threat Landscape for Artificial-Intelligence Systems — an ATT&CK-style matrix of adversary tactics and techniques targeting AI and machine-learning systems, built from real-world attack observations plus adversarial-ML research.

| | |
|---|---|
| **SecID** | `secid:ttp/mitre.org/atlas` |
| **Upstream version** | v2026.07 (released 2026-08-07, dated 2026-07-31) |
| **License** | **Apache-2.0** — the most permissive of the MITRE frameworks here |
| **Status** | Active — monthly calendar-versioned releases |
| **In this directory** | Metadata only. See [What's here](#whats-in-this-directory). |

Content as of 2026.07: 1 matrix, 16 tactics, 101 techniques + 77 sub-techniques, 37 mitigations, 68 case studies.

## Upstream

| Repo | Contents |
|---|---|
| [`mitre-atlas/atlas-data`](https://github.com/mitre-atlas/atlas-data) | **Canonical.** YAML distributions under `dist/`, plus a Python API package under `atlas/` |
| [`mitre-atlas/atlas-navigator-data`](https://github.com/mitre-atlas/atlas-navigator-data) | STIX 2.1 bundles, ATT&CK Navigator layers, OpenCTI bundles — **lags `atlas-data` by a release or more** |

The rendered site is <https://atlas.mitre.org/>.

### `dist/` layout

Upstream reorganized its distribution when schema `format-version: 6.0.0` landed:

- `dist/v6/ATLAS-<CalVer>.yaml` — **current line**
- `dist/legacy/ATLAS-<semver>.yaml` — frozen 5.x line
- `dist/manifest.yaml` — machine-readable release → format-version → path index
- `dist/ATLAS.yaml` — still present at top level but **5.x-era sized; not a safe pointer**

Versioning switched from semver to CalVer: `v5.6.0` (2026-05-04) was the last semver release, followed by `v2026.05`, `v2026.06`, `v2026.07`. Releases 2026.02–2026.04 shipped both formats; from 2026.05 onward it is v6 only.

## Getting the data

```bash
# Current release, pinned
curl -LO https://raw.githubusercontent.com/mitre-atlas/atlas-data/v2026.07/dist/v6/ATLAS-2026.07.yaml

# Release index — resolve any release to its file path and format version
curl -s https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/manifest.yaml

# STIX 2.1 (note: trails atlas-data)
curl -LO https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/stix-atlas.json
```

Prefer `manifest.yaml` over any hardcoded path — it is upstream's own index and survives the next `dist/` reshuffle.

## Identifiers

All ATLAS IDs use the `AML.` prefix: `AML.TA####` (tactic), `AML.T####` / `AML.T####.###` (technique, sub-technique), `AML.M####` (mitigation), `AML.CS####` (case study). Dots are preserved in URLs, unlike ATT&CK sub-techniques.

### ⚠ IDs are not permanent, and UUIDs do not help

ATLAS provides **no deprecation mechanism**. Verified against 2026.04 → 2026.07:

- `AML.T0019`, `AML.T0058`, `AML.T0104` were **deleted outright** — folded into `AML.T0115` sub-techniques. No `revoked-by`, no `deprecated` flag, no redirect. The mapping exists only in the upstream CHANGELOG prose.
- The STIX bundle has **zero** objects with `revoked` or `x_mitre_deprecated` set.
- Objects carry a `uuid`, but all are **UUIDv5** — deterministic name-based hashes, not opaque allocated keys. Rename or re-parent an object and its UUID changes by construction. The three retired techniques' UUIDs are absent from 2026.07. (For the 167 IDs present in both releases, UUID drift was zero — UUIDs are stable exactly as long as identity is.)

The nastier failure mode is an ID that survives but changes meaning. **Always cite ATLAS with a release**, e.g. `AML.T0115.000 @ 2026.07`. The unversioned `https://atlas.mitre.org/techniques/{id}` URL is fine for a footnote, not for a mapping table.

Tracked in SecID [#155](https://github.com/CloudSecurityAlliance/SecID/issues/155).

## What's in this directory

Metadata only, per the repository's [no-bulk-mirror rule](../../../CLAUDE.md#dont-bulk-mirror-data-thats-already-publicly-available-upstream). Upstream is Apache-2.0, public, and release-tagged, so pinning to a tag beats mirroring.

## Relationship to sibling frameworks

- **[ATT&CK](../attack/)** — ATLAS is modeled on it; many ATLAS techniques carry an `attack-reference` to the corresponding ATT&CK technique.
- **[D3FEND](../d3fend/)** — maps countermeasures to ATLAS techniques; D3FEND 1.5.0 pins ATLAS v2026.06.
- **CSA AICM** (`control/cloudsecurityalliance.org/aicm/`) — the natural pairing: ATLAS catalogs what adversaries do to AI systems, AICM catalogs the controls.

## Last verified

2026-08-12 — upstream at v2026.07.
