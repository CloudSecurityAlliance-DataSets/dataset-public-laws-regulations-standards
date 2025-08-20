# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a comprehensive public repository of laws, regulations, standards, frameworks, best practices, and AI transparency documentation related to cloud and AI security. The repository is organized into 7 main categories with structured, searchable access to critical AI governance and security resources.

## Repository Structure

The repository follows a hierarchical organization with 7 main directories:

### `/regulations-mandatory/`
Legally binding laws and regulations organized by country/region:
- EU (AI Act, GDPR, DORA)
- US (federal and state laws including CHIPS Act)
- China, UK, Canada, Australia, Germany
- Each contains acts with full regulatory text converted to multiple formats

### `/standards-voluntary/`
Technical standards and certifications:
- International: ISO/IEC standards (info only due to licensing), IEEE standards (info only)
- US: NIST publications (full content available)
- Industry: PCI-DSS, HITRUST, etc.

### `/frameworks-guidance/`
Security frameworks and guidance documents:
- Government frameworks: FedRAMP, NIST AI RMF, UK NCSC
- Industry frameworks: CSA CCM, MITRE ATLAS, OWASP

### `/best-practices/`
Company and organizational best practices:
- Companies: Microsoft, Google, IBM, OpenAI, Anthropic, Amazon, Cisco, Equifax
- Research papers and academic studies

### `/model-cards/` and `/system-cards/`
AI transparency documentation organized by:
- Companies (OpenAI, Google, Meta, etc.)
- Government agencies
- Research institutions  
- Community/open source projects

### `/tools-resources/`
Templates, utilities, and processed files:
- `utils/`: Conversion scripts and processing tools
- `working/`: Frequently used processed documents
- Templates for model cards and system cards

## Document Processing Workflow

Documents follow a standardized conversion process:

### PDF to Multiple Formats
Primary tool: `marker` for PDF processing
```bash
# Convert PDF to markdown
./tools-resources/utils/pdf_to_md.sh document.pdf
```

### Processing Chain
1. **Original document** (PDF, HTML, XML)
2. **Markdown conversion** (`document.md`) - Clean, readable format
3. **Processed markdown** (`document-processed.md`) - Cleaned with irrelevant sections removed
4. **CSV extraction** (`document.csv`) - Each article/control becomes a row
5. **JSON structuring** (`document.json`) - Machine-readable with metadata

### Key Processing Scripts
- `tools-resources/utils/pdf_to_md.sh` - PDF to markdown conversion using marker
- `tools-resources/utils/convert-HTML-to-Markdown.py` - HTML to markdown
- `tools-resources/utils/convert-CSV-to-JSON-list.py` - CSV to JSON conversion
- `tools-resources/utils/docx_to_md.py` - DOCX to markdown
- Web scraping scripts for AWS, Google, MITRE data

## File Structure Conventions

### Standard Files in Each Document Folder
- `README.json` - Metadata about the document (classification, source, scope)
- `document.md` - Main content in markdown
- `document-processed.md` - Cleaned version with non-relevant sections removed
- `document.csv` - Structured data (articles/controls as rows)
- `document.json` - Machine-readable structured data
- `document_meta.json` - Processing metadata
- `PROCESSING-NOTES.md` - Conversion workflow documentation (when applicable)
- Supporting files: images, diagrams numbered as extracted

### Naming Conventions
- Folders include version: `CCM-4.0.1/`, `PCI-DSS-v4.0/`
- Official naming maintained: `NIST.AI.600-1/`, `NIST.SP.800-53r5/`
- No version subdirectories: use `CCM-4.0.1/` not `CCM/4.0.1/`

## Document Classification System

Reference `PROMPT-CLASSIFICATION.md` for complete classification rules:

### Quick Classification
- **Legally binding** → `/regulations-mandatory/[country]/`
- **Voluntary standards** → `/standards-voluntary/[org]/`
- **Frameworks/guidance** → `/frameworks-guidance/[type]/`
- **Company practices** → `/best-practices/companies/[company]/`
- **Individual model docs** → `/model-cards/[category]/[org]/`
- **AI system docs** → `/system-cards/[category]/[org]/`

### Licensed Standards
For ISO, IEEE, and other licensed standards:
- Only information about the standard is stored, not the full text
- Include purchase URLs and licensing notes in README.json
- Mark with `"license_required": true` in metadata

## Metadata Requirements

### README.json Structure
Every document folder must contain standardized metadata:
```json
{
  "title": "Document title",
  "acronym": "Abbreviation",
  "identifier": "Official ID",
  "version": "Version number",
  "issuer": "Publishing organization",
  "type": "regulation|standard|framework|best-practice|model-card|system-card",
  "geographic_scope": ["regions"],
  "compliance_status": "mandatory|voluntary",
  "source_url": "Official URL",
  "license_required": true/false,
  "relation_to_cloud_security": "Impact description",
  "relation_to_ai_security": "AI security relevance"
}
```

## Working with Processed Data

### Frequently Used Files
The `tools-resources/working/` directory contains commonly accessed processed documents:
- `eu_ai_act-processed.json` - EU AI Act structured data
- `NIST.AI.600-1-processed.json` - NIST AI RMF structured controls
- `AICM-Controls-Info.json` - AI Controls Matrix
- Other frequently referenced processed documents

### Data Format Standards
- **CSV format**: Each control/article/section as a row with standardized columns
- **JSON format**: Structured arrays with consistent field names
- **Markdown format**: Clean, readable text with proper heading structure

## Classification Edge Cases

### Model Cards vs System Cards
- **Model Cards**: Document individual ML models (technical details, performance)
- **System Cards**: Document entire AI systems (safety, deployment, operations)
- Place in respective `/model-cards/` or `/system-cards/` directories

### Multi-Category Documents
- Place in primary category based on main purpose
- Use tags in README.json metadata for secondary categories
- Government frameworks that are mandatory for agencies but voluntary for others go in `/frameworks-guidance/government/`

## Development and Maintenance

### No Build System
This repository contains primarily documentation and data files. There are no traditional build, lint, or test commands. Work focuses on:

1. **Document classification** using PROMPT-CLASSIFICATION.md
2. **Conversion processing** using tools in `tools-resources/utils/`
3. **Metadata creation** following README.json standards
4. **Quality validation** of converted data

### Key Reference Files
- `PROMPT-CLASSIFICATION.md` - Complete classification guide and decision trees
- `TEMPLATE-PROCESSING-NOTES.md` - Template for documenting conversion workflows
- `SOURCES.md` - Source links and references for documents

When adding new documents, always consult the classification guide first and ensure proper metadata is created for discoverability and compliance tracking.