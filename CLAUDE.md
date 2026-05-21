# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A public repository of bulk-processed laws, regulations, standards, frameworks, and reference documents related to cloud and AI security. Maintained by the Cloud Security Alliance (CSA).

This repo is the **bulk-processed layer** of a three-tier data architecture:

1. **SecID registry** ([`~/GitHub/CloudSecurityAlliance/SecID`](https://github.com/CloudSecurityAlliance/SecID)) — identity, resolution rules, namespace metadata. The authoritative classifier.
2. **This repo** (`dataset-public-laws-regulations-standards`) — bulk processed content (full standards/regulations/frameworks in md/csv/json form).
3. **Per-item SecID-{type} repos** (future, e.g. `SecID-control`, `SecID-weakness`) — per-control / per-weakness / per-article splits with provenance envelopes.

Originals (PDFs, XLSX, etc.) and full extraction history live in S3:
- `s3://dataset-public-laws-regulations-standards/` — public-license content
- `s3://dataset-private-laws-regulations-standards/` — restricted/licensed content

This git repo holds only the **current extraction** of each document; S3 has all extractions ever produced.

S3 layout mirrors the repo's SecID structure exactly: an original PDF at `control/nist.gov/800-53/r5/800-53-r5.pdf` in git lands at `s3://dataset-public-laws-regulations-standards/control/nist.gov/800-53/r5/800-53-r5.pdf` in S3. To populate or refresh the public bucket from local originals (idempotent — only uploads new/changed files):

```bash
tools-resources/utils/sync_originals_to_s3.sh             # do it
tools-resources/utils/sync_originals_to_s3.sh --dry-run   # preview first
```

The script uses the `csa` AWS profile and only touches binary originals (`*.pdf`, `*.xlsx`, `*.docx`, `*.zip`, `*.tar.gz`) under SecID type roots. It does NOT upload markdown extractions or derived CSV/JSON — those live in git. It also skips `tools-resources/PROCESSED-US/` (working-copy DOCX files not at SecID-canonical paths; map and move those by hand when needed).

Companion private repo: [`dataset-private-laws-regulations-standards`](https://github.com/CloudSecurityAlliance-DataSets/dataset-private-laws-regulations-standards) mirrors this same SecID layout for licensed/restricted sources (ISO, IEEE, members-only frameworks). Access is gated; content from those sources must not appear here.

## Directory Layout Mirrors SecID

The repository organizes content by **SecID type → namespace → name → version**:

```
control/
├── cloudsecurityalliance.org/
│   ├── ccm/4.0.13/
│   ├── ccm/4.1/
│   ├── aicm/1.0.3/
│   └── ccm-caiq/4.0.3/
├── pcisecuritystandards.org/
│   └── pci-dss/v4.0.1/
└── nist.gov/
    ├── csf/2.0/
    ├── 800-53/r5/
    └── ai-rmf/1.0/
regulation/
├── europa.eu/
│   ├── ai-act/
│   └── gdpr/
└── bsi.bund.de/
    └── ai-c4/
weakness/
└── mitre.org/
    └── cwe/4.19.1/
ttp/
└── mitre.org/
    ├── attack/
    └── atlas/
reference/
├── openai.com/
│   ├── model-cards/gpt-4/
│   └── system-cards/gpt-4/
└── microsoft.com/
    └── security-guidance/
methodology/
└── nist.gov/
    └── ir-8477/
tools-resources/
└── (pipeline scripts, unchanged)
```

The path is composable from the SecID identifier:

| SecID | Filesystem path |
|---|---|
| `secid:control/nist.gov/800-53@r5` | `control/nist.gov/800-53/r5/` |
| `secid:control/pcisecuritystandards.org/pci-dss@4.0.1` | `control/pcisecuritystandards.org/pci-dss/v4.0.1/` |
| `secid:weakness/mitre.org/cwe@4.19.1` | `weakness/mitre.org/cwe/4.19.1/` |
| `secid:regulation/europa.eu/gdpr` | `regulation/europa.eu/gdpr/` |

**Version directory naming** follows each publisher's natural convention (PCI uses `v4.0.1`, NIST uses `r5`, CSA uses `4.0.13`). Aliases are recorded in metadata.

## SecID Is Authoritative — Mirror It 100%

**This repository mirrors [SecID](https://github.com/CloudSecurityAlliance/SecID) exactly.** Every directory path here is derivable from a SecID identifier and vice versa. Don't invent classifications, naming, or path conventions — if SecID and this repo disagree, this repo is wrong and must be reconciled.

### The 10 SecID types

Fixed in SecID v1.0: `advisory`, `weakness`, `ttp`, `control`, `capability`, `methodology`, `disclosure`, `regulation`, `entity`, `reference`. Don't invent new ones. Full descriptions and a decision table live in [PROMPT-CLASSIFICATION.md](PROMPT-CLASSIFICATION.md).

The canonical source of truth for the 10 types **and** their sub-classifications (subtypes) is [TYPES-AND-SUBTYPES.md](https://github.com/CloudSecurityAlliance/SecID/blob/main/docs/reference/TYPES-AND-SUBTYPES.md) in the SecID repo. **Fetch the live version from GitHub before any classification work** — that doc evolves (new subtypes get added, candidates get promoted, language gets refined), and whatever's summarized in this CLAUDE.md is a snapshot that may already be stale. Don't rely on memory, prior sessions, or the excerpts below; fetch and read the current file.

### SecID subtypes (the in-type extension mechanism)

The 10 types are frozen at v1.0. Within them, **subtypes** name sub-classifications via a `subtype:` array on the source-level match_node's `data:` block — registry-data, not a schema change. Examples in use today: a glossary is `reference` with `subtype: ["glossary"]`; CVSS is `methodology` with `subtype: ["scoring"]`; NIST IR 8477 is `methodology` with `subtype: ["mapping"]`.

**Default rule:** when a new sub-category emerges, try a subtype first. Splitting into a new type is the exception — gated on **all four** criteria being met: resolution patterns diverge, consumers diverge, semantics drift, volume justifies it. Most candidates fail at least one and stay as subtypes.

**Before classifying any new document — especially when a possible sub-category is in play — fetch the current version of the canonical guide from GitHub:**

[https://github.com/CloudSecurityAlliance/SecID/blob/main/docs/reference/TYPES-AND-SUBTYPES.md](https://github.com/CloudSecurityAlliance/SecID/blob/main/docs/reference/TYPES-AND-SUBTYPES.md)

Use `WebFetch` (or `curl`/`gh` against the raw URL) to read the **live** file every time — not a cached recollection, not the excerpts in this CLAUDE.md. The doc changes as new subtypes are tagged, candidates get promoted, or implicit overloads become explicit. As of the last time this CLAUDE.md was updated it enumerated named subtypes in use (`reference` → glossary; `methodology` → 11 categories), anticipated subtypes (BoK on `control`, course on `reference`), and candidate patterns (CNA / bug-bounty / PSIRT on `disclosure`; law / directive / transposition on `regulation`; organization / product / service on `entity`) — but treat that list as **possibly out of date** and verify against the live file. When this repo's labeling and the live SecID doc disagree, the live SecID doc is right.

### `reference/` is the catch-all

When a document doesn't fit any other type, it goes in `reference/`. **Don't force-fit into a wrong type, and don't invent a new type.** Examples that belong in `reference/`:

- NIST IR / TN / CSWP research papers
- AI model cards, system cards, safety scorecards
- Cross-framework mapping documents (CCM ↔ 800-53, AI RMF crosswalks)
- Glossaries (NIST CSRC glossary)
- Vendor security guidance / white papers
- CISA fact sheets, program documentation

If a pattern of similar-shaped `reference/` entries emerges, it may become a first-class SecID type later — at which point SecID is updated first, then this repo migrates. Don't preempt that here.

### Don't bulk-mirror data that's already publicly available upstream

If a publisher hosts their authoritative data in a public, version-tagged location (e.g., GitHub repo with releases) and consumers can pull it directly, **do not import the data into this repo**. Keep only the metadata stub describing the source and pointing at upstream. Examples that should stay reference-only:

- **MITRE ATT&CK** — STIX bundles at `github.com/mitre-attack/attack-stix-data` (~50MB per matrix, version-tagged)
- **MITRE ATLAS** — `dist/ATLAS.yaml` at `github.com/mitre-atlas/atlas-data` (Apache-2.0, release-tagged)
- **MITRE CTID mappings** — JSON files at `github.com/center-for-threat-informed-defense/mappings-explorer`
- **CVE Project records** — `github.com/CVEProject/cvelistV5` (huge, hourly-updated)
- Other GitHub-hosted SecID-registered datasets

Reasons:
- Upstream is authoritative; mirrors drift.
- Bulk JSON/YAML inflates this repo for no marginal value over a `git clone` of upstream.
- Version-pinning via upstream tag is more reliable than committing one snapshot here.

Exception: if structured-extraction from a PDF/XLSX produces the *first* machine-readable form of a doc (e.g., NIST SP 800-53 r5 from the NIST-published XLSX, PCI DSS from marker output of the PDF), commit the derived structured form. The derived data didn't exist publicly before.

### Licensed/restricted content is not committed here

Sources whose terms prohibit redistribution — ISO/IEC standards, IEEE standards, members-only frameworks — must not be added to this repo in any form: **no full content, no metadata stub, no README**. Identity records for such sources live in the SecID registry (`~/GitHub/CloudSecurityAlliance/SecID/registry/{type}/{tld}/{org}.json`). Full extracted content lives in the companion private repo `dataset-private-laws-regulations-standards`, accessible only to authorized CSA users via the future private SecID resolver.

### Namespaces are **DNS domain names of the publishing organization**

The SecID spec ([SPEC.md §1.2](https://github.com/CloudSecurityAlliance/SecID/blob/main/SPEC.md)) requires the namespace to be the publishing org's domain name. In practice this means:

- Use the **actual DNS domain** the org publishes from. Verify with `host <domain>` if unsure.
- US states use the **canonical state portal DNS**: `ca.gov` (not `california.gov`), `ny.gov`, `ct.gov`, `mass.gov`, `wa.gov`, etc. — never the expanded form.
- Platforms with sub-sites use a path namespace: `github.com/advisories` for GHSA, not a bespoke domain.
- When multiple domains resolve to the same org (e.g., `mass.gov` and `massachusetts.gov`), use the canonical/short form the org uses for itself.

### Workflow when adding a new document

1. **Determine the SecID type.** When in doubt → `reference/`.
2. **Find the namespace entry** in `~/GitHub/CloudSecurityAlliance/SecID/registry/{type}/{tld}/{org}.json`.
   - If it doesn't exist: open a PR against SecID first to add it. Don't add documents here pointing at a non-registered namespace.
3. **Use the canonical source name** from the SecID match_nodes (e.g., `csf` not `cybersecurity-framework`, `pci-dss` not `pci`).
4. **Compute the path** as `{type}/{namespace}/{name}/{version}/` (version optional).
5. **The `secid` field in metadata must match the directory path exactly.** This is verified by the audit script.

See [PROMPT-CLASSIFICATION.md](PROMPT-CLASSIFICATION.md) for the full step-by-step decision flow with examples.

## Metadata Files

Every document directory has a `[dirname]-metadata.json` describing it. See [METADATA-SCHEMA.md](METADATA-SCHEMA.md) for the schema.

Naming convention:
- `[dirname]-metadata.json` — required, one per document directory, describes the document
- `[filename]-file-metadata.json` — optional sidecar for an individual file when it deviates from directory defaults (different license, retrieval source, etc.)

The `secid` field is the canonical SecID for the document and must match the directory path.

## Repository health checks

This repository contains documentation and data — no traditional build/lint/test. But two scripts enforce the repo's structural invariants and should be run after any structural change:

| Command | When |
|---|---|
| `python3 tools-resources/utils/audit_secid_alignment.py` | After adding or moving any document directory. Verifies every metadata `secid` field resolves to a registered SecID namespace. Exits 1 if anything is missing. |
| `python3 tools-resources/utils/build_index.py` | After adding/removing documents or changing extraction state. Regenerates `INDEX.md` at repo root. |

The audit script requires `~/GitHub/CloudSecurityAlliance/SecID/registry/` to exist locally (it cross-references the SecID registry checkout). If that path is missing, clone https://github.com/CloudSecurityAlliance/SecID alongside this repo before running the audit.

`INDEX.md` is generated by `build_index.py` — do not hand-edit; regenerate.

Day-to-day work involves:
- Document acquisition (download from official sources, S3 archival)
- Extraction (PDF/XLSX/HTML → markdown → CSV/JSON)
- Metadata authoring
- Cross-referencing with SecID

## Extraction Pipeline

### PDF → markdown

**Always use the GPU box** (`markersinglehost`). Local CPU extraction via `marker_single` is unusably slow and is not the right tool for this repo's documents. Driven from `tools-resources/utils/pdf_to_md_via_gpu.sh`. Output for publicly-redistributable docs lands in this repo; for licensed/restricted PDFs (IEEE, members-only frameworks) point `--output-dir` at a sibling path in [`dataset-private-laws-regulations-standards`](https://github.com/CloudSecurityAlliance-DataSets/dataset-private-laws-regulations-standards) (its [`PROCESSING.md`](https://github.com/CloudSecurityAlliance-DataSets/dataset-private-laws-regulations-standards/blob/main/PROCESSING.md) has the cross-repo invocation).

```bash
tools-resources/utils/pdf_to_md_via_gpu.sh \
    --output-dir control/example.org/spec/version \
    /path/to/source.pdf
```

What it does:
1. scp's the canonical `marker-convert.sh` to the GPU box (keeps versions in sync — no drift)
2. scp's the PDF to `~/marker-work/` on the GPU box
3. Launches a detached tmux session running marker
4. Polls the remote log every 30s until `STATUS: DONE` or `STATUS: FAILED`
5. scp's the output directory back to `--output-dir`
6. Cleans up remote files (unless `--keep-remote`)

Flags: `--output-dir`, `--formats markdown,json,html` (default `markdown` single-pass), `--force-ocr` (opt-in), `--remote-host` (default `markersinglehost`), `--remote-dir` (default `~/marker-work`), `--poll-interval` (default 30s), `--timeout` (default 7200s), `--keep-remote`, `--help`.

**GPU box details:**
- SSH alias: `markersinglehost` → `192.168.1.232` (WSL2 Ubuntu on a Windows machine)
- GPU: NVIDIA RTX 3060
- Remote marker venv: `~/marker-env/`
- Remote worker: `~/marker-convert.sh` (overwritten on each wrapper run from the canonical copy in this repo)

#### When to use `--force-ocr`

Default is **OFF**. Clean text-layer PDFs come out faster and cleaner without it — PCI DSS v4.0.1 measurement showed 17× speedup and strictly better output without OCR forcing. Only flip on `--force-ocr` for scans or PDFs that show garbled text in marker output.

#### After extraction: name files to match SecID

Marker outputs `<input-basename>.md`. The SecID convention requires `<name>-<version>.md` matching the directory path. Rename marker's output before committing — e.g., if your input was `PCI-DSS-v4_0_1.pdf` landing in `control/pcisecuritystandards.org/pci-dss/v4.0.1/`, rename `PCI-DSS-v4_0_1.md` → `pci-dss-v4.0.1.md` (and the companion `_meta.json`). The `_page_*.jpeg` images keep their marker-assigned names.

#### Common pitfalls

- **Encrypted PDFs.** Marker can't read password-protected PDFs. Decrypt first: `qpdf --password='PASSWORD' --decrypt encrypted.pdf decrypted.pdf`.
- **Filename mismatch.** Always rename marker outputs to match the SecID-derived filename prefix before committing.
- **Forgetting metadata.** A directory without `<name>-<version>-metadata.json` won't be SecID-resolvable and won't show up correctly in INDEX.md. Author metadata before commit; verify with `python3 tools-resources/utils/audit_secid_alignment.py`.

### Marker output → structured CSV/JSON

Each standard with a regular requirement structure has a domain-specific extraction script co-located with the data. Two naming conventions are in use; pick whichever matches the document's nearest sibling:

- `extract_<name>.py` in the version directory — current convention (NIST 800-171, AI RMF, Privacy Framework, 800-218, 800-37 r2, 800-66 r2, 800-207, AI 600-1, 800-63A/B/C, 800-160 v1, FIPS 200, and most other NIST extractions; also `regulation/` jurisdiction extractors).
- `parse_<name>.py` co-located or under `scripts/` — older convention (PCI DSS, CCM, AICM, CIS Controls, AICPA TSC).

The script walks marker's `Table` block tree (or the source's native structure for XLSX/HTML inputs) to emit one row per requirement/control/article.

### Excel → CSV

`tools-resources/utils/excel_to_csv.py` handles `.xlsx` extraction with merged-cell handling.

### Other utilities

```bash
# HTML to markdown
python3 tools-resources/utils/convert-HTML-to-Markdown.py

# CSV to JSON (list of dicts)
python3 tools-resources/utils/convert-CSV-to-JSON-list.py --input file.csv

# DOCX to markdown
python3 tools-resources/utils/docx_to_md.py

# Remove BOM from CSV
./tools-resources/utils/remove-BOM-from-CSV.sh
```

## Standard Files in Each Document Folder

| File | Required? | Purpose |
|---|---|---|
| `[dirname]-metadata.json` | Yes | Document-level metadata (SecID, license, lifecycle, extraction provenance) |
| `[dirname].md` | Usually | Full markdown extraction |
| `[dirname].json` | If from marker | Marker's structured block tree |
| `[dirname]_meta.json` | If from marker | Marker's per-page OCR/TOC provenance |
| `[dirname]-requirements.csv` / `.json` | If parsed | Structured per-control/per-requirement data |
| `extract_{name}.py` or `parse_{name}.py` | If custom extractor | Reproducibility script (see naming note under Extraction Pipeline) |
| `_page_*.jpeg` | If from marker | Page images referenced by markdown |
| `[filename]-file-metadata.json` | Optional | Per-file sidecar (deviation from directory metadata) |

## Git Conventions

- `.gitignore`: `*.pdf`, `*.xlsx`, `*.zip`, `*.gz`, `*.xz`, `.DS_Store`, `.claude`, `.gemini`, `.codex`
- Originals live in S3, not git
- Public repo: feature branches + PRs, never push directly to main

For the step-by-step flow when adding a new document, see [Workflow when adding a new document](#workflow-when-adding-a-new-document) above. For licensed/restricted material that doesn't belong here, see [Licensed/restricted content is not committed here](#licensedrestricted-content-is-not-committed-here).
