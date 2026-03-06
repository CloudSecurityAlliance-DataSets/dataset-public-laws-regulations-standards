# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A public repository of laws, regulations, standards, frameworks, best practices, and AI transparency documentation related to cloud and AI security. Maintained by the Cloud Security Alliance (CSA). Organized into 7 main content categories plus supporting directories.

## No Build System

This repository contains documentation and data files — no build, lint, or test commands. Work involves document classification, format conversion, metadata creation, and data quality validation.

## Key Reference Files

- `PROMPT-CLASSIFICATION.md` — **The authoritative classification guide.** Consult this before adding any document. Contains decision trees, edge cases, naming conventions, README.json schema, and model card vs system card rules.
- `TEMPLATE-PROCESSING-NOTES.md` — Template for documenting conversion workflows.
- `SOURCES.md` — Source links and references for documents.
- `prompts/PROMPT-ANALYSIS-2025-06-09.md` — Detailed prompt for analyzing/extracting structured data from governance documents (Level 1 and Level 2 analysis).

## Repository Structure

### Content Directories

| Directory | Contents | Key Detail |
|-----------|----------|------------|
| `/regulations-mandatory/` | Legally binding laws by country (EU, US, China, UK, etc.) | Full regulatory text in multiple formats |
| `/standards-voluntary/` | ISO/IEC (info only — licensed), IEEE (info only), NIST (full content), PCI-DSS, HITRUST | Licensed standards: metadata + purchase links only |
| `/frameworks-guidance/` | Government (FedRAMP, NIST AI RMF) and industry (CSA CCM, MITRE ATLAS, OWASP) | Subdirs: `government/`, `industry/` |
| `/best-practices/` | Company guidelines (Microsoft, Google, IBM, OpenAI, Anthropic, Amazon, Cisco, Equifax) and research | Subdirs: `companies/`, `research/` |
| `/model-cards/` | Individual ML model documentation | By company, government, research, community |
| `/system-cards/` | Entire AI system documentation | Safety, deployment, operations focus |
| `/tools-resources/` | Scripts, templates, working files, scraped data | See details below |

### Supporting Directories

- `/organizations/` — Organization-specific data (currently CSA/CAIQ)
- `/prompts/` — Analysis prompts for document processing

### tools-resources/ Layout

- `utils/` — Conversion scripts (Python + shell)
- `working/` — Frequently used processed JSON files (EU AI Act, NIST AI 600-1, AICM Controls, IBM Controls)
- `PROCESSED-US/` — Source .docx files for FedRAMP documents
- `mitre.org/` — MITRE data scraping scripts (ATLAS, ATT&CK, CWE, FIGHT) and category definitions
- `first.org/` — FIRST.org data
- `owasp.org/` — OWASP data

## Document Processing

### Conversion Pipeline

1. **Original** (PDF, HTML, XML, DOCX) → 2. **Markdown** (`document.md`) → 3. **Processed markdown** (`document-processed.md`, cleaned) → 4. **CSV** (`document.csv`, one row per article/control) → 5. **JSON** (`document.json`, machine-readable)

### Conversion Commands

```bash
# PDF to markdown (uses marker)
./tools-resources/utils/pdf_to_md.sh document.pdf

# Alternative PDF conversion (external CSA utils repo)
~/GitHub/CSA-utils/utils/convert-pdf-to-markdown.sh --input filename.pdf

# HTML to markdown
python3 tools-resources/utils/convert-HTML-to-Markdown.py

# CSV to JSON
python3 tools-resources/utils/convert-CSV-to-JSON-list.py --input file.csv

# DOCX to markdown
python3 tools-resources/utils/docx_to_md.py

# Excel to CSV
python3 tools-resources/utils/excel_to_csv.py

# Remove BOM from CSV
./tools-resources/utils/remove-BOM-from-CSV.sh
```

### Standard Files in Each Document Folder

- `README.json` — Required metadata (see `PROMPT-CLASSIFICATION.md` for full schema)
- `document.md` — Main content in markdown
- `document-processed.md` — Cleaned version
- `document.csv` — Structured rows
- `document.json` — Machine-readable
- `document_meta.json` — Processing metadata from marker
- `PROCESSING-NOTES.md` — Conversion workflow docs (when applicable)

## Git and File Conventions

### .gitignore Rules

Binary and large files are excluded from git: `*.pdf`, `*.xlsx`, `*.zip`, `*.gz`, `*.xz`, `.DS_Store`. Also excluded: `.claude`, `.gemini`, `.codex` directories.

### Naming Conventions

- Folders include version: `CCM-4.0.13/`, `PCI-DSS-v4.0/`
- Official naming maintained: `NIST.AI.600-1/`, `NIST.SP.800-53r5/`
- No version subdirectories: use `CCM-4.0.1/` not `CCM/4.0.1/`

### Licensed Standards (ISO, IEEE)

Only store information *about* the standard, not the full text. Mark with `"license_required": true` in README.json and include purchase URLs.

## Quick Classification

When adding documents, consult `PROMPT-CLASSIFICATION.md` for the full guide. Summary:

- **Legally binding** → `/regulations-mandatory/[country]/`
- **Voluntary standards** → `/standards-voluntary/[org]/`
- **Frameworks/guidance** → `/frameworks-guidance/[government|industry]/`
- **Company practices** → `/best-practices/companies/[company]/`
- **Individual model docs** → `/model-cards/[category]/[org]/`
- **AI system docs** → `/system-cards/[category]/[org]/`
- **Model cards** = single ML model technical docs; **System cards** = entire AI system safety/deployment docs
