# AI Classification Prompt and Repository Structure Guide

## Classification Prompt for AI

You are helping to organize documents into a repository of public laws, regulations, standards, and best practices related to cloud and AI security. When classifying a document, follow these steps:

### Quick Classification Guide
- **Laws, acts, regulations** → `/regulations-mandatory/`
- **ISO, IEEE, NIST standards** → `/standards-voluntary/` (ISO/IEEE: info only due to licensing)
- **Frameworks (MITRE, CSA, OWASP)** → `/frameworks-guidance/`
- **Company docs (Microsoft, Google)** → `/best-practices/`
- **Model cards** → `/model-cards/`
- **System cards** → `/system-cards/`
- **Scripts and tools** → `/tools-resources/`

### Detailed Classification Process

1. **Identify the document type** by asking:
   - Is this legally binding/mandatory? → `regulations-mandatory`
   - Is this a voluntary standard or certification? → `standards-voluntary`
   - Is this guidance or a framework? → `frameworks-guidance`
   - Is this a company/organization's practices? → `best-practices`
   - Is this a model card or system card? → See [Model Cards and System Cards Classification](#model-cards-and-system-cards-classification) below
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

## Model Cards and System Cards Classification

### Understanding Model Cards vs System Cards

**Model Cards** are structured documentation that accompanies individual machine learning models, providing essential information about how a specific model was designed, trained, and evaluated. They function like "nutrition labels" for AI models.

**System Cards** are comprehensive documents that outline the capabilities, limitations, safety measures, and ethical considerations associated with entire AI systems, which may include multiple models plus infrastructure components.

### Key Differences:

| Aspect | Model Cards | System Cards |
|--------|-------------|---------------|
| **Scope** | Single, specific trained ML model | Complete AI system (multiple models + infrastructure) |
| **Focus** | Technical model details | System-wide safety, deployment, operations |
| **Content** | Performance metrics, training data, evaluation procedures, demographic analysis | Safety testing, risk assessments, access controls, monitoring, mitigation strategies |
| **Length** | Brief (often one-pagers) | More comprehensive documents |
| **Audience** | Data scientists, ML practitioners, developers | Stakeholders, regulators, safety researchers, auditors |
| **Creation Difficulty** | Can be easily filled by data scientists | Requires extensive system knowledge |
| **Examples** | HuggingFace model documentation, Google face detection model card | OpenAI GPT-4 system card, Meta Llama system card |

### Classification Rules for Model/System Cards:

**All model cards go to `/model-cards/` and all system cards go to `/system-cards/`** with the following organizational structure:

1. **Company Model/System Cards** → `/model-cards/companies/[Company]/` or `/system-cards/companies/[Company]/`
   - Examples: `/model-cards/companies/Google/Face-Detection/`, `/system-cards/companies/OpenAI/GPT-4/`
   - Most common category for commercial AI documentation

2. **Government Model/System Cards** → `/model-cards/government/[Country]/` or `/system-cards/government/[Country]/`
   - Examples: `/system-cards/government/US/Defense-AI-System/`, `/model-cards/government/UK/NHS-Diagnostic-Model/`
   - When government entities document their AI systems

3. **Academic Research Model/System Cards** → `/model-cards/research/[Institution]/` or `/system-cards/research/[Institution]/`
   - Examples: `/model-cards/research/Stanford/BERT-Variant/`, `/system-cards/research/MIT/Autonomous-System/`
   - University and research institution documentation

4. **Open Source Community Cards** → `/model-cards/community/[Project]/` or `/system-cards/community/[Project]/`
   - Examples: `/model-cards/community/HuggingFace/BERT-Base/`, `/system-cards/community/Stable-Diffusion/`
   - Community-driven and open source model documentation

5. **Industry Consortium Cards** → `/model-cards/consortiums/[Consortium]/` or `/system-cards/consortiums/[Consortium]/`
   - Examples: `/model-cards/consortiums/MLCommons/ResNet/`, `/system-cards/consortiums/Partnership-AI/Ethics-Framework/`
   - Industry group or consortium-developed documentation

6. **Templates and Frameworks** → `/tools-resources/templates/model-cards/` or `/tools-resources/templates/system-cards/`
   - Examples: `/tools-resources/templates/model-cards/HuggingFace-Template/`, `/tools-resources/templates/system-cards/NIST-Framework/`
   - Templates, standards, and frameworks for creating cards

### Folder Naming Conventions for Model/System Cards:

- **Individual Cards**: `[Model/System-Name]/` (e.g., `GPT-4/`, `Face-Detection/`, `BERT-Base/`)
- **Versioned Cards**: `[Model/System-Name]-v[Version]/` (e.g., `GPT-4-v1.0/`, `Llama-2-v2.1/`)
- **Dated Cards**: `[Model/System-Name]-[YYYY-MM]/` (e.g., `Claude-3-2024-03/`, `Gemini-2024-12/`)

**Organization Hierarchy:**
```
/model-cards/
  /companies/
    /OpenAI/
      - GPT-4/
      - DALL-E-2/
      - Whisper/
    /Google/
      - BERT-Base/
      - Face-Detection/
      - Gemini/
    /Meta/
      - Llama-2/
      - SAM/
  /government/
    /US/
      - Defense-Vision-Model/
    /UK/
      - NHS-Diagnostic-Model/
  /research/
    /Stanford/
      - BERT-Variant/
    /MIT/
      - Custom-NLP-Model/
  /community/
    /HuggingFace/
      - BERT-Base-Multilingual/
    /Stable-Diffusion/
      - SD-v1.5/

/system-cards/
  /companies/
    /OpenAI/
      - GPT-4-System/
      - DALL-E-2-System/
    /Meta/
      - Llama-2-System/
  /government/
    /US/
      - Military-AI-System/
  /research/
    /MIT/
      - Autonomous-Driving-System/
```

### Content Structure within Model/System Card Folders:

**Model Card Folders should contain:**
- `model-card.md` - The actual model card content
- `model-card_meta.json` - Metadata about the model card
- `README.json` - Information about the model card document itself
- Supporting files: performance charts, evaluation data, etc.

**System Card Folders should contain:**
- `system-card.md` - The actual system card content
- `system-card_meta.json` - Metadata about the system card
- `README.json` - Information about the system card document itself
- Supporting files: safety evaluation reports, red team findings, etc.

### Example Classifications:

**OpenAI GPT-4 System Card**
- **Type**: System card (covers entire GPT-4 system)
- **Issuer**: OpenAI (company)
- **Classification**: `/system-cards/companies/OpenAI/GPT-4/`

**Google Face Detection Model Card**
- **Type**: Model card (specific to face detection model)
- **Issuer**: Google (company)
- **Classification**: `/model-cards/companies/Google/Face-Detection/`

**Meta Llama 2 System Card**
- **Type**: System card (covers Llama 2 system)
- **Issuer**: Meta (company)
- **Classification**: `/system-cards/companies/Meta/Llama-2/`

**Stanford BERT Variant Model Card**
- **Type**: Model card (academic research model)
- **Issuer**: Stanford University
- **Classification**: `/model-cards/research/Stanford/BERT-Variant/`

**US Defense AI System Card**
- **Type**: System card (government AI system)
- **Issuer**: US Department of Defense
- **Classification**: `/system-cards/government/US/Defense-AI-System/`

**HuggingFace Model Card Template**
- **Type**: Model card template/framework
- **Issuer**: HuggingFace (community)
- **Classification**: `/tools-resources/templates/model-cards/HuggingFace-Template/`

### Questions to Ask When Classifying Model/System Cards:

1. "Is this documenting a single model or an entire AI system?"
2. "Who created this card - a company, government agency, or research institution?"
3. "Is this a template/framework for creating cards, or an actual card for a specific model/system?"
4. "Does this card focus on technical model details or broader system safety and deployment considerations?"
5. "Is this part of a larger collection of cards from the same organization?"
6. "Should this be grouped with other cards in a collection folder or stand alone?"

### Important Notes:

- **System cards are more comprehensive** than model cards and typically cover safety evaluations, red teaming results, and deployment considerations
- **Model cards focus on individual models** with technical details about training, performance, and evaluation
- **Both types serve transparency and accountability functions** but at different levels of analysis
- **Companies often publish both** - model cards for individual models and system cards for major AI system releases
- **Regulatory importance**: System cards are increasingly important for AI governance and compliance

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

/model-cards
  /companies
    /OpenAI
      - GPT-4/
      - DALL-E-2/
      - Whisper/
    /Google
      - BERT-Base/
      - Face-Detection/
      - Gemini/
    /Meta
      - Llama-2/
      - SAM/
    /Microsoft
      - Turing-NLG/
    /Anthropic
      - Claude-3/
    - [Other companies]
  /government
    /US
      - Defense-Vision-Model/
      - Healthcare-Diagnostic/
    /UK
      - NHS-AI-Models/
    - [Other countries]
  /research
    /Stanford
      - BERT-Variants/
    /MIT
      - Custom-Models/
    - [Other institutions]
  /community
    /HuggingFace
      - Community-Models/
    /Stable-Diffusion
      - Model-Variants/
    - [Other communities]
  /consortiums
    /MLCommons
      - Benchmark-Models/
    - [Other consortiums]

/system-cards
  /companies
    /OpenAI
      - GPT-4-System/
      - DALL-E-2-System/
    /Meta
      - Llama-2-System/
    /Google
      - Bard-System/
    /Anthropic
      - Claude-System/
    - [Other companies]
  /government
    /US
      - Military-AI-Systems/
      - Federal-AI-Systems/
    - [Other countries]
  /research
    /MIT
      - Autonomous-Systems/
    - [Other institutions]
  /community
    - Open-Source-Systems/

/tools-resources
  - utils/ (conversion scripts, etc.)
  - templates/
    - model-cards/
      - HuggingFace-Template/
      - Google-Template/
    - system-cards/
      - NIST-Framework/
      - Industry-Standard/
    - TEMPLATE-PROCESSING-NOTES.md (for documenting conversion workflows)
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

### Example 9: OpenAI GPT-4 System Card
- **Type**: System card (comprehensive AI system documentation)
- **Issuer**: OpenAI (company)
- **Purpose**: Transparency about GPT-4 system capabilities, limitations, and safety measures
- **Classification**: `/best-practices/companies/OpenAI/GPT-4-system-card/`

### Example 10: Google Face Detection Model Card
- **Type**: Model card (individual ML model documentation)
- **Issuer**: Google (company)
- **Purpose**: Technical documentation of face detection model performance and limitations
- **Classification**: `/best-practices/companies/Google/Face-Detection-model-card/`

### Example 11: HuggingFace Model Card Template
- **Type**: Model card template/framework
- **Issuer**: HuggingFace (community platform)
- **Purpose**: Standardized template for creating model cards
- **Classification**: `/tools-resources/templates/model-cards/HuggingFace-Template/`

### Example 12: OpenAI GPT-4 System Card (Updated)
- **Type**: System card (comprehensive AI system documentation)
- **Issuer**: OpenAI (company)
- **Purpose**: Transparency about GPT-4 system capabilities, limitations, and safety measures
- **Classification**: `/system-cards/companies/OpenAI/GPT-4/`

### Example 13: Google Face Detection Model Card (Updated)
- **Type**: Model card (individual ML model documentation)
- **Issuer**: Google (company)
- **Purpose**: Technical documentation of face detection model performance and limitations
- **Classification**: `/model-cards/companies/Google/Face-Detection/`

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

11. **Model Cards vs System Cards**:
   - **Model cards** document individual ML models → `/model-cards/[category]/[organization]/`
   - **System cards** document entire AI systems → `/system-cards/[category]/[organization]/`
   - **Templates and frameworks** for creating cards → `/tools-resources/templates/model-cards/` or `/tools-resources/templates/system-cards/`
   - **Government AI documentation** → `/model-cards/government/[country]/` or `/system-cards/government/[country]/`
   - **Academic research documentation** → `/model-cards/research/[institution]/` or `/system-cards/research/[institution]/`
   - When in doubt, ask: "Does this document a single model or an entire AI system?"

12. **Multiple cards from the same organization**:
   - Organizations automatically get their own subdirectories under the appropriate category
   - Examples: `/model-cards/companies/OpenAI/GPT-4/`, `/model-cards/companies/OpenAI/DALL-E-2/`
   - No need to create additional collection folders

13. **Model/System card versions**:
   - Include version information when available: `/model-cards/companies/OpenAI/GPT-4-v1.0/`
   - For updated cards, create new folders rather than overwriting: `/model-cards/companies/OpenAI/GPT-4-v2.0/`
   - Document version history in metadata files

14. **Cross-organization models**:
   - If multiple organizations collaborate on a model/system, place in the primary developer's folder
   - Document collaborations in the metadata
   - Example: If Google and DeepMind collaborate, place under Google with DeepMind noted in metadata

## Questions to Ask When Uncertain

1. "Is [document] legally enforceable in [region]?"
2. "Is compliance with [document] mandatory for any specific industry or region?"
3. "Who is the primary issuing authority for [document]?"
4. "Is [document] a standard (defines requirements) or a framework (provides guidance)?"
5. "Has [document] been superseded by a newer version?"
6. "Should [Organization] have its own subdirectory, or should its documents be placed directly in the parent directory?"
7. "Is this a licensed standard that we can only provide information about?"
8. "What version number should be included in the folder name?"
9. "Is this documenting a single model or an entire AI system?" (for model vs system cards)
10. "Is this an actual model/system card or a template for creating cards?"
11. "Should multiple cards from this organization be grouped together or kept separate?"
12. "Does this card focus on technical model details or broader system safety considerations?"

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

## File Documentation Requirements

### Standard Metadata: README.json
Every document folder should contain a `README.json` with classification and discovery metadata:

```json
{
  "title": "Full Document Title",
  "acronym": "Document acronym/abbreviation if applicable",
  "identifier": "Official document ID",
  "version": "Document version",
  "date": "Publication/effective date",
  "issuer": "Issuing organization",
  "type": "regulation|standard|framework|guidance|best-practice|model-card|system-card",
  "geographic_scope": ["countries or regions"],
  "industry_scope": ["applicable industries"],
  "compliance_status": "mandatory|voluntary|varies",
  "source_url": "Official source URL",
  "wikipedia_url": "Wikipedia page URL if available",
  "license_required": true/false,
  "purchase_url": "URL to purchase if licensed",
  "last_updated": "When we last updated this",
  "tags": ["ai", "security", "privacy", "etc"],
  "relation_to_cloud_security": "How this impacts cloud security",
  "relation_to_ai_security": "How this impacts AI security",
  "description": "Brief summary of document purpose and key provisions"
}
```

### Processing Documentation: PROCESSING-NOTES.md
For documents that undergo conversion/processing (PDF→Markdown→CSV→JSON), also include a `PROCESSING-NOTES.md` file using the template at `/TEMPLATE-PROCESSING-NOTES.md`. This tracks:

- **Conversion steps taken** (tools used, process followed)
- **File format notes** (document structure, organization)
- **Data removal notes** (what sections were excluded and why)
- **Generated files list** (all artifacts created during processing)
- **Quality and validation notes** (accuracy, completeness)

### When to Use Each:
- **README.json**: **Required for ALL folders** - provides standardized metadata for discovery and classification
- **PROCESSING-NOTES.md**: **Use for processed documents only** - documents complex conversion workflows

This separation keeps classification metadata standardized while allowing detailed workflow documentation where needed.

For licensed standards, always include:
- `"license_required": true`
- `"purchase_url": "https://..."`
- Clear note that only information about the standard is provided

For model cards, also include:
```json
{
  "card_type": "model_card",
  "model_name": "Specific model name",
  "model_version": "Model version if available",
  "training_data": "Brief description of training data",
  "performance_metrics": ["accuracy", "f1_score", "etc"],
  "intended_tasks": ["classification", "generation", "etc"],
  "limitations": "Key model limitations",
  "ethical_considerations": "Bias, fairness considerations"
}
```

For system cards, also include:
```json
{
  "card_type": "system_card",
  "system_name": "Full AI system name",
  "system_version": "System version if available",
  "models_included": ["list of models in the system"],
  "safety_evaluations": ["red_teaming", "adversarial_testing", "etc"],
  "deployment_context": "How/where the system is deployed",
  "risk_mitigations": "Key safety measures implemented",
  "monitoring_measures": "Ongoing monitoring and controls"
}
```

If any classification decision is unclear, always ask for human guidance rather than guessing.

