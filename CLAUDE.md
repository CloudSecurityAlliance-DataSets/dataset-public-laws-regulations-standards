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

Fixed in SecID v1.0; don't invent new ones here:

```
advisory      Vulnerability advisories and records (CVE, GHSA, vendor PSIRTs)
weakness      Vulnerability/weakness taxonomies (CWE, MAEC)
ttp           Adversary tactics/techniques (ATT&CK, ATLAS, CAPEC, D3FEND)
control       Security control frameworks and standards (CCM, CSF, 800-53, PCI DSS)
capability    Vendor security features / product capabilities
methodology   Analysis methodologies (mappings, scoring, evaluation processes)
disclosure    Vulnerability disclosure programs
regulation    Legally-binding rules (laws, statutes, directives)
entity        Organizations / products / services
reference     CATCH-ALL: research papers, white papers, blog posts, model cards,
              system cards, mappings, glossaries, anything else informative
```

### `reference/` is the catch-all

When a document doesn't fit any other type, it goes in `reference/`. **Don't force-fit into a wrong type, and don't invent a new type.** Examples that belong in `reference/`:

- NIST IR / TN / CSWP research papers
- AI model cards, system cards, safety scorecards
- Cross-framework mapping documents (CCM ↔ 800-53, AI RMF crosswalks)
- Glossaries (NIST CSRC glossary)
- Vendor security guidance / white papers
- CISA fact sheets, program documentation

If a pattern of similar-shaped `reference/` entries emerges, it may become a first-class SecID type later — at which point SecID is updated first, then this repo migrates. Don't preempt that here.

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

## No Build System

This repository contains documentation and data files — no build, lint, or test commands. Work involves:
- Document acquisition (download from official sources, S3 archival)
- Extraction (PDF/XLSX/HTML → markdown → CSV/JSON)
- Metadata authoring
- Cross-referencing with SecID

## Extraction Pipeline

### PDF → markdown

Two extraction paths. Both are driven from `tools-resources/utils/`. Output for publicly-redistributable docs lands in this repo; for licensed/restricted PDFs (IEEE, members-only frameworks) point `--output-dir` at a sibling path in [`dataset-private-laws-regulations-standards`](https://github.com/CloudSecurityAlliance-DataSets/dataset-private-laws-regulations-standards) (its [`PROCESSING.md`](https://github.com/CloudSecurityAlliance-DataSets/dataset-private-laws-regulations-standards/blob/main/PROCESSING.md) has the cross-repo invocation).

#### Local Mac (small docs, <~50 pages)

```bash
tools-resources/utils/pdf_to_md.sh /path/to/source.pdf [output_dir]
```

Uses the isolated marker venv at `~/.venvs/marker/`. CPU-bound; fine for small documents.

#### GPU box (larger docs, OCR work, anything where speed matters)

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

### Marker JSON → structured CSV/JSON

Each standard with a regular requirement structure (PCI DSS, CCM, NIST CSF, etc.) has a domain-specific parser script co-located with the data (e.g., `parse_pci_dss.py` in `control/pcisecuritystandards.org/pci-dss/v4.0.1/`). The parser walks marker's `Table` block tree to emit one row per requirement.

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
| `parse_{name}.py` | If custom parser | Reproducibility script |
| `_page_*.jpeg` | If from marker | Page images referenced by markdown |
| `[filename]-file-metadata.json` | Optional | Per-file sidecar (deviation from directory metadata) |

## Git Conventions

- `.gitignore`: `*.pdf`, `*.xlsx`, `*.zip`, `*.gz`, `*.xz`, `.DS_Store`, `.claude`, `.gemini`, `.codex`
- Originals live in S3, not git
- Public repo: feature branches + PRs, never push directly to main

## Quick Classification Decision

When adding a new document:

1. **Find or add the SecID namespace entry** in `~/GitHub/CloudSecurityAlliance/SecID/registry/{type}/{tld}/{org}.json`
2. **Compute the path**: `{type}/{namespace-domain}/{source-name}/{version}/`
3. **Create the directory** and add `[dirname]-metadata.json` per METADATA-SCHEMA.md
4. **Add content files** following the conventions above

If the standard is licensed/restricted (e.g., IEEE, members-only frameworks) and we can't redistribute, the directory contains only the metadata file with `"license.publicly_redistributable": false`. The actual content stays in S3 private and is served via the future private SecID resolver.
