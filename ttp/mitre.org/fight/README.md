# MITRE FiGHT (5G Hierarchy of Threats)

An ATT&CK-style knowledge base of adversary tactics and techniques against **5G networks** — core, RAN, management plane, and 5G-specific protocols.

| | |
|---|---|
| **SecID** | `secid:ttp/mitre.org/fight` |
| **Upstream version** | ⚠ **Unversioned** — no releases, no tags. Latest commit `097cd5f` (2025-11-14) |
| **License** | MITRE FiGHT Terms of Use — the repo `LICENSE.txt` is not an SPDX-recognized identifier |
| **Status** | ⚠ Quiet — no upstream commits since 2025-11-14 |
| **In this directory** | A snapshot pinned to `097cd5f73811`. See [What's here](#whats-in-this-directory). |

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
# Consolidated dataset, pinned by commit (~1.1 MB) — this is what's committed here
curl -sL -o fight.yaml \
    https://raw.githubusercontent.com/mitre/FiGHT/097cd5f73811/fight.yaml
python3 convert_fight.py          # regenerates fight.json

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

| File | What it is |
|---|---|
| `fight.yaml` | Upstream's file, fetched at commit `097cd5f73811` (1.14 MB) |
| `fight.json` | The same data serialized as JSON — no transformation applied |
| `convert_fight.py` | Reproduces `fight.json` from `fight.yaml` |

**A SHA-pinned snapshot, not a mirror — and this is a deliberate exception to the [no-bulk-mirror rule](../../../CLAUDE.md#dont-bulk-mirror-data-thats-already-publicly-available-upstream).**

That rule directs us to point at upstream rather than copy it. Pointing requires something citable, and FiGHT publishes no releases, no tags, and leaves its own `version` fields empty — a pointer could only ever reference a moving branch. So the data is kept locally, pinned to a commit that can be named.

The history here is worth stating plainly, because it was got wrong once. This directory previously held a `fight.yaml` of 624 KB against upstream's 1.14 MB, missing the entire `campaigns:` section. That stale copy was removed on 2026-08-12 in favour of a pointer, which fixed the staleness and introduced a different problem — there was nothing to pin the pointer to. On 2026-08-14 the data was restored, **fetched fresh at the pinned SHA rather than reverting the old file.**

To refresh: re-run the fetch and conversion in [Getting the data](#getting-the-data) against a newer commit, then update the SHA in `fight-metadata.json` (`scope.pinned_commit`, `current_extraction.notes`) and in this README.

## Relationship to sibling frameworks

- **[ATT&CK](../attack/)** — FiGHT is directly derived from it: same tactic IDs, parallel technique numbering for inherited techniques.
- **[ATLAS](../atlas/)** — the sibling domain-specific ATT&CK extension (AI/ML rather than 5G). ATLAS has by far the stronger publication model of the two; useful contrast if you are evaluating how to consume either.

## Last verified

2026-08-12 — upstream HEAD `097cd5f73811`, committed 2025-11-14.
