# AI Classification Prompt and Repository Structure Guide

## Classification Prompt for AI

You are helping to organize documents into a repository of public laws, regulations, standards, and best practices related to cloud and AI security. When classifying a document, follow these steps:

### Quick Classification Guide
- **Laws, acts, regulations** → `/regulations-mandatory/`
- **ISO, IEEE, NIST standards** → `/standards-voluntary/` (ISO/IEEE: info only due to licensing)
- **Frameworks (MITRE, CSA, OWASP)** → `/frameworks-guidance/`
- **Company docs (Microsoft, Google)** → `/best-practices/`
- **Scripts and tools** → `/tools-resources/`

### Detailed Classification Process

1. **Identify the document type** by asking:
   - Is this legally binding/mandatory? → `regulations-mandatory`
   - Is this a voluntary standard or certification? → `standards-voluntary`
   - Is this guidance or a framework? → `frameworks-guidance`
   - Is this a company/organization's practices? → `best-practices`
   - Is this a tool or utility? → `tools-resources`

2. **Determine the geographic scope**:
   - If region-specific, identify the country/region
   - If international, identify the issuing body
   - If company-specific, note the company

3. **Check the issuing authority**:
   - Government body → Consider if it's regulation or guidance
   - Standards organization (ISO, IEEE, NIST) → Usually `standards-voluntary`
   - Industry consortium (CSA, OWASP, MITRE) → Usually `frameworks-guidance`
   - Company → `best-practices`
   
   Note: For licensed standards (ISO, IEEE, etc.), we only store information about the standard, not the standard itself.

4. **When uncertain**, ask the human:
   - "This appears to be [X] issued by [Y]. Should this go in [proposed location]?"
   - "I'm unsure if this is mandatory or voluntary. Can you clarify the compliance requirements?"
   - "This document seems to fit multiple categories. Primary purpose appears to be [X]. Is this correct?"
   - "I found [N] documents from [Organization]. Should I create a subdirectory for them?"
   - "This is a new organization not currently in the structure. Should it get its own subdirectory?"
   - "What version number should I use in the folder name for [Document]?"
   - "This appears to be a licensed standard. Should I only include information about it?"

## Repository Structure

```
/regulations-mandatory
  /EU
    - AI-Act/
    - GDPR/
    - DORA/
  /US
    /federal
      - CHIPS-Act/
      - whitehouse/ (Executive orders, memos, strategies)
      - [Other federal laws]
    /state
      - California-Privacy/
      - [Other state laws]
  /China
    - Cybersecurity-Law/
    - [Other Chinese regulations]
  /UK
    - Online-Safety-Bill/
    - [Other UK laws]
  /Canada
    - [Canadian laws]
  /Australia
    - [Australian laws]
  /Germany
    - [German-specific laws beyond EU]

/standards-voluntary
  /international
    /ISO
      - ISO-IEC-42001/ (info only - licensed)
      - ISO-IEC-27001-2022/ (info only - licensed)
      - [Other ISO standards]
    /IEEE
      - IEEE-7001-2021/ (info only - licensed)
      - [Other IEEE standards]
  /US
    /NIST
      - NIST.AI.100-1/
      - NIST.AI.600-1/
      - NIST.SP.800-53r5/
      - NIST.SP.800-137/
      - NIST.FIPS.140-3/
      - [Other NIST publications]
  /industry
    /PCI-DSS
      - PCI-DSS-v4.0/
      - PCI-DSS-v3.2.1/
      - [Other PCI standards]
    /HITRUST
      - HITRUST-CSF-v11.2/
      - [Other HITRUST frameworks]
    - [Other industry-specific standards]

/frameworks-guidance
  /government
    - US-FedRAMP/
    - US-govCAR/
    - UK-NCSC/
    - [Other government frameworks]
  /industry
    /CSA
      - CCM-4.0.1/
      - CCM-4.0.2/
      - AI-Controls-Matrix-1.0/
      - [Other CSA frameworks]
    /MITRE
      - ATLAS/
      - ATT&CK/
      - [Other MITRE frameworks]
    /OWASP
      - Top-10/
      - ASVS/
      - [Other OWASP projects]
    - [Other organizations]
  /international
    /OECD
      - AI-Principles/
      - [Other OECD guidance]

/best-practices
  /companies
    /Microsoft
      - AI-Security-Guidelines/
      - [Other Microsoft docs]
    /Google
      - GCP-Security/
      - Responsible-AI/
      - [Other Google practices]
    /IBM
      - Generative-AI-Controls/
      - [Other IBM frameworks]
    /OpenAI
      - Safety-Guidelines/
      - [Other OpenAI docs]
    /Anthropic
      - Constitutional-AI/
      - [Other Anthropic docs]
    /Amazon
      - AWS-AI-Service-Cards/
      - [Other Amazon docs]
    - CISCO/
    - EQUIFAX/
  /research
    - Academic-Papers/
    - Industry-Reports/
    - [Research organizations]

/tools-resources
  - utils/ (conversion scripts, etc.)
  - templates/
  - checklists/
  - working/ (frequently used processed docs, e.g., eu_ai_act-processed.json)
```

## Classification Examples

### Example 1: EU AI Act
- **Type**: Legally binding regulation
- **Geographic**: EU
- **Classification**: `/regulations-mandatory/EU/AI-Act/`

### Example 2: NIST AI Risk Management Framework
- **Type**: Voluntary framework
- **Geographic**: US (but used globally)
- **Issuer**: US Government agency (NIST)
- **Classification**: `/standards-voluntary/US/NIST/NIST.AI.600-1/`

### Example 3: Microsoft AI Security Guidelines v2.0
- **Type**: Company best practices
- **Issuer**: Microsoft
- **Version**: 2.0
- **Classification**: `/best-practices/companies/Microsoft/AI-Security-Guidelines-v2.0/`

### Example 4: CSA Cloud Controls Matrix v4.0.1
- **Type**: Industry framework
- **Issuer**: Cloud Security Alliance (industry consortium)
- **Version**: 4.0.1
- **Classification**: `/frameworks-guidance/industry/CSA/CCM-4.0.1/`

### Example 5: MITRE ATLAS
- **Type**: Industry framework
- **Issuer**: MITRE
- **Classification**: `/frameworks-guidance/industry/MITRE/ATLAS/`

### Example 6: White House AI Executive Order
- **Type**: Government guidance/policy
- **Geographic**: US Federal
- **Mandatory for**: Federal agencies
- **Classification**: `/regulations-mandatory/US/federal/whitehouse/`

### Example 7: FedRAMP
- **Type**: Government framework
- **Mandatory for**: US federal cloud procurement
- **Voluntary for**: Others
- **Classification**: `/frameworks-guidance/government/US-FedRAMP/`

### Example 8: ISO/IEC 42001 (Licensed Standard)
- **Type**: International standard
- **Issuer**: ISO
- **License**: Required (not freely available)
- **Classification**: `/standards-voluntary/international/ISO/ISO-IEC-42001/`
- **Contents**: Information about the standard only, not the standard itself

### Example Directory: NIST Subdirectory
```
/standards-voluntary/US/NIST/
  - NIST.AI.100-1/
  - NIST.AI.100-1-crosswalks/
  - NIST.AI.100-2e2023/
  - NIST.AI.600-1/
  - NIST.CSWP.02042020-1/
  - NIST.CSWP.31/
  - NIST.FIPS.140-2/
  - NIST.FIPS.140-3/
  - NIST.FIPS.199/
  - NIST.FIPS.200/
  - NIST.IR.8360/
  - NIST.IR.8408/
  - NIST.SP.1800-13/
  - NIST.SP.1800-26/
  - NIST.SP.800-137/
  - NIST.SP.800-161r1/
  - NIST.SP.800-218A/
  - NIST.SP.800-53r5/
  - README.md
```

Note: Organization subdirectories may also contain:
- Glossaries (e.g., `NIST/CSRC-Glossary/`)
- Crosswalks between standards
- General documentation about the organization's standards

### Example: Multiple Versions
When an organization releases multiple versions:
```
/frameworks-guidance/industry/CSA/
  - CCM-4.0.1/
  - CCM-4.0.2/
  - CCM-4.0.10/  (Note: version sorting)
  - AI-Controls-Matrix-1.0/
```

## Edge Cases and Clarifications

1. **NIST Publications**: 
   - While NIST is a government agency, their publications are voluntary standards
   - Place in `/standards-voluntary/US/NIST/`

2. **FedRAMP**:
   - Mandatory for US federal agencies, but framework for others
   - Place in `/frameworks-guidance/government/`

3. **International Standards adopted as Law**:
   - If a country makes an ISO standard mandatory, create entries in both:
     - Original in `/standards-voluntary/international/ISO/`
     - Reference/adoption notice in `/regulations-mandatory/[country]/`

4. **Multi-national efforts**:
   - MITRE works internationally → `/frameworks-guidance/industry/MITRE/`
   - OECD principles → `/frameworks-guidance/international/OECD/`

5. **Company Standards that become Industry Standards**:
   - Start in `/best-practices/companies/[Company]/`
   - If formally adopted by standards body, also add to appropriate standards location

6. **When to create organization subdirectories**:
   - Create a subdirectory when an organization has 3+ documents
   - Organizations with only 1-2 documents can be placed directly in the parent directory
   - Large publishers (ISO, NIST, MITRE, OWASP, CSA) should always have subdirectories

7. **Documents spanning multiple categories**:
   - Place in primary category based on main purpose
   - Use tags in metadata to indicate secondary categories
   - Consider creating symbolic links or references if needed

8. **Distinguishing companies from organizations**:
   - Commercial entities (Microsoft, Google, Amazon) → `/best-practices/companies/`
   - Standards bodies (ISO, IEEE) → `/standards-voluntary/`
   - Non-profit consortiums (CSA, OWASP) → `/frameworks-guidance/`
   - Research organizations (MITRE) → `/frameworks-guidance/`

9. **Cloud provider documentation**:
   - Security best practices from cloud providers → `/best-practices/companies/[Provider]/`
   - Compliance frameworks (e.g., AWS Well-Architected) → Still goes in `/best-practices/companies/`
   - Unless adopted as industry standard → Then also reference in appropriate standards location

10. **Copyright and licensing**:
   - Even freely available documents may have copyright restrictions
   - Always check and document the license terms
   - When in doubt, provide information about the document rather than the full text
   - Government documents (NIST, EU regulations) are typically public domain or freely redistributable

## Questions to Ask When Uncertain

1. "Is [document] legally enforceable in [region]?"
2. "Is compliance with [document] mandatory for any specific industry or region?"
3. "Who is the primary issuing authority for [document]?"
4. "Is [document] a standard (defines requirements) or a framework (provides guidance)?"
5. "Has [document] been superseded by a newer version?"
6. "Should [Organization] have its own subdirectory, or should its documents be placed directly in the parent directory?"
7. "Is this a licensed standard that we can only provide information about?"
8. "What version number should be included in the folder name?"

## File Naming Conventions

**Folder naming:**
- Include version in folder name: `CCM-4.0.1/`, `NIST.SP.800-53r5/`
- Never create version subdirectories: ❌ `CCM/4.0.1/` → ✅ `CCM-4.0.1/`
- Use official naming when available: `NIST.AI.600-1/`
- Use hyphens to separate name and version: `PCI-DSS-v4.0/`

**Within each folder:**
- Main document: `[IDENTIFIER].md` (e.g., `NIST.AI.600-1.md`) - the actual content or information about it
- Processed versions: `[IDENTIFIER]-processed.csv`, `[IDENTIFIER]-processed.json`
- Metadata: `[IDENTIFIER]_meta.json` or `README.json` - describes the document
- Images/diagrams: Numbered as extracted (e.g., `0_image_0.png`)

For licensed standards:
- `README.json` - metadata and how to obtain
- `[IDENTIFIER]-info.md` - public information about the standard
- NO actual standard content files

Note: For NIST documents, maintain their official naming convention (e.g., `NIST.AI.600-1`, `NIST.SP.800-53r5`, `NIST.FIPS.140-3`)

## Document Versioning

- **Include version in folder name** for standards: `CCM-4.0.1/`, `PCI-DSS-v4.0/`, `NIST.SP.800-53r5/`
- **Never use** subdirectories for versions: ❌ `CCM/4.0.1/` → ✅ `CCM-4.0.1/`
- For regulations without clear versions, use generic names: `GDPR/`, `AI-Act/`
- Document version history in the README.json metadata
- Maintain official naming conventions (e.g., NIST uses `NIST.SP.800-53r5`)

## Licensed Standards Notice

**Important**: Some standards (particularly ISO, IEEE, and certain industry standards) are not freely available due to licensing restrictions. For these documents:

- The repository contains **information about** the standard, not the standard itself
- Files typically include:
  - `README.json` with metadata about the standard
  - Summary of what the standard covers
  - Key topics and scope (without reproducing the standard)
  - How to obtain the official standard
  - Related resources and references
  - Public information about the standard's requirements
- What we DON'T include:
  - The actual standard text
  - Detailed requirements from the standard
  - Any copyrighted content from the standard
- Example: `/standards-voluntary/international/ISO/ISO-IEC-42001/` contains:
  - Description of the AI management system standard
  - High-level overview of its purpose
  - Link to purchase from ISO
  - But NOT the actual standard text or specific requirements

## Metadata Requirements

Each document folder should contain a `README.json` with:
```json
{
  "title": "Full Document Title",
  "identifier": "Official document ID",
  "version": "Document version",
  "date": "Publication/effective date",
  "issuer": "Issuing organization",
  "type": "regulation|standard|framework|guidance|best-practice",
  "geographic_scope": ["countries or regions"],
  "industry_scope": ["applicable industries"],
  "compliance_status": "mandatory|voluntary|varies",
  "source_url": "Official source URL",
  "license_required": true/false,
  "purchase_url": "URL to purchase if licensed",
  "last_updated": "When we last updated this",
  "tags": ["ai", "security", "privacy", "etc"]
}
```

For licensed standards, always include:
- `"license_required": true`
- `"purchase_url": "https://..."`
- Clear note that only information about the standard is provided

If any classification decision is unclear, always ask for human guidance rather than guessing.

