# MITRE FiGHT (5G Hierarchy of Threats)

An ATT&CK-style knowledge base of adversary tactics and techniques against **5G networks** — core, RAN, management plane, and 5G-specific protocols.

| | |
|---|---|
| **SecID** | `secid:ttp/mitre.org/fight` |
| **Upstream version** | ⚠ **Unversioned** — no releases, no tags. Latest commit `097cd5f` (2025-11-14) |
| **License** | MITRE FiGHT Terms of Use — the repo `LICENSE.txt` is not an SPDX-recognized identifier |
| **Status** | ⚠ Quiet — no upstream commits since 2025-11-14 |
| **In this directory** | Metadata only. See [What's here](#whats-in-this-directory). |

Content at commit `097cd5f`: 15 tactics, 183 techniques, 92 mitigations, 169 data sources, 10 groups, 16 software entries, 2 campaigns.

## ⚠ Upstream is a website build, not a data repository

This is the weakest upstream story of the MITRE frameworks in this tree, and it shapes how you should consume it.

[`mitre/FiGHT`](https://github.com/mitre/FiGHT) is described as "publicly accessible version of the FiGHT website" — it is a **built Nuxt static site** committed to git (`_nuxt/`, `index.html`, `404.html`, `CNAME`). The data files happen to be included in that deploy artifact rather than published as a first-class dataset.

Practical consequences:

- **No GitHub Releases and no tags.** There is no version identifier to cite.
- **Pin by commit SHA** — it is the only stable reference available.
- The data's own `version` fields are largely empty strings.
- Upstream has been quiet since 2025-11-14; verify currency before relying on it.

The rendered site is <https://fight.mitre.org/>.

## Getting the data

```bash
# Consolidated dataset, pinned by commit (~1.1 MB)
curl -LO https://raw.githubusercontent.com/mitre/FiGHT/097cd5f73811/fight.yaml

# Current HEAD (unpinned — prefer the SHA above)
curl -LO https://raw.githubusercontent.com/mitre/FiGHT/main/fight.yaml
```

Per-object source files also live under `raw-fight-data/` and `fight-data/` in the same repo.

Top-level keys in `fight.yaml`: `tactics`, `techniques`, `mitigations`, `data sources`, `groups`, `software`, `campaigns`, `case-studies`. Note the space in `data sources` — it is not a valid identifier in most languages and needs quoting.

## Identifiers

FiGHT's ID scheme encodes **what it inherited from ATT&CK versus what it originated**, which is genuinely useful for triage:

| Pattern | Meaning |
|---|---|
| `TA####` | Tactic — **ATT&CK tactic IDs reused verbatim** (`TA0001`, `TA0042`, `TA0043`), not FiGHT-specific |
| `FGT1###` | Technique inherited from / aligned to an ATT&CK `T1###` technique (113 of 183) |
| `FGT5###` | Technique **original to FiGHT** — 5G-specific (70 of 183) |
| `FGM####` | Mitigation |
| `FGDS####`, `FGDS####.###` | Data source, sub-source |
| `FGG5###` | Group |
| `FGS5###` | Software |
| `C####` / `FGC5###` | Campaign — ATT&CK campaign IDs reused (`C0024` = SolarWinds) alongside FiGHT-original ones |

The `5` in `FGT5###` / `FGG5###` / `FGS5###` marks 5G-original content; the `1` in `FGT1###` marks ATT&CK lineage. So `FGT1195` corresponds to ATT&CK `T1195` (Supply Chain Compromise), while `FGT5xxx` has no ATT&CK counterpart.

## What's in this directory

Metadata only, per the repository's [no-bulk-mirror rule](../../../CLAUDE.md#dont-bulk-mirror-data-thats-already-publicly-available-upstream), and consistent with this document's own metadata (`desired_end_state: metadata-only / upstream-only`).

This directory previously held committed `fight.yaml` (624 KB) and `fight.json` (782 KB) snapshots. Both were removed on 2026-08-12: the committed YAML was **624 KB against upstream's 1.14 MB** and was missing the entire `campaigns:` section (SolarWinds Compromise, Operation Soft Cell). The files remain in git history and in S3.

## Relationship to sibling frameworks

- **[ATT&CK](../attack/)** — FiGHT is directly derived from it: same tactic IDs, parallel technique numbering for inherited techniques.
- **[ATLAS](../atlas/)** — the sibling domain-specific ATT&CK extension (AI/ML rather than 5G). ATLAS has by far the stronger publication model of the two; useful contrast if you are evaluating how to consume either.

## Last verified

2026-08-12 — upstream HEAD `097cd5f73811`, committed 2025-11-14.
