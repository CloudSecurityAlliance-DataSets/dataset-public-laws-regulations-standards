# Cloud Controls Matrix (CCM)

The Cloud Controls Matrix (CCM) is a cybersecurity control framework for cloud computing developed by the Cloud Security Alliance (CSA). It provides a set of security controls organized across 17 domains that cover key aspects of cloud technology, serving as an industry standard for cloud security and privacy assessments.

- **CCM research page:** https://cloudsecurityalliance.org/research/cloud-controls-matrix
- **Latest version (v4.1):** https://cloudsecurityalliance.org/artifacts/cloud-controls-matrix-v4-1

## Purpose

- Define security controls that should be implemented by actors within the cloud supply chain
- Clarify shared responsibility between Cloud Service Providers (CSPs) and Cloud Service Customers (CSCs)
- Align with and map to major standards and frameworks (ISO/IEC 27001, NIST, PCI-DSS, AICPA TSC, etc.)
- Enable self-assessment and submission to the CSA STAR Registry

## Key Components

The CCM is published alongside the **Consensus Assessments Initiative Questionnaire (CAIQ)**, a set of yes/no questions derived from CCM controls used to evaluate cloud providers. The v4.1 download package includes:

1. Guide to the CCM and CAIQ
2. CCM v4.1 (controls with mappings and auditing guidelines)
3. CAIQ v4.1 (submittable for STAR Registry Level 1 assessments)
4. Code of Practice for Implementing and Maintaining Key Metrics
5. Continuous Auditing Metrics Catalog
6. CCM v4.1 Implementation Guidelines
7. Introductory Guidance (using CCM and the Shared Security Responsibility Model)
8. Change Analysis Document (differences from CAIQ v4.0.3)

Machine-readable formats (JSON, YAML, OSCAL) are also available.

## Control Domains (17)

| Domain | ID | Controls (v4.1) |
|---|---|---|
| Application & Interface Security | AIS | 8 |
| Audit & Assurance | A&A | 6 |
| Business Continuity Management and Operational Resilience | BCR | 11 |
| Change Control and Configuration Management | CCC | 9 |
| Cryptography, Encryption & Key Management | CEK | 21 |
| Data Security and Privacy Lifecycle Management | DSP | 19 |
| Datacenter Security | DCS | 18 |
| Governance, Risk and Compliance | GRC | 8 |
| Human Resources | HRS | 13 |
| Identity & Access Management | IAM | 15 |
| Infrastructure Security | IVS | 9 |
| Interoperability & Portability | IPY | 4 |
| Logging and Monitoring | LOG | 14 |
| Security Incident Management, E-Discovery, & Cloud Forensics | SEF | 10 |
| Supply Chain Management, Transparency, and Accountability | STA | 16 |
| Threat & Vulnerability Management | TVM | 12 |
| Universal Endpoint Management | UEM | 14 |

## Versions in This Repository

### CCM v4.1.0 (January 2026)

Located in `CCM-4.1/`. Contains 207 controls and 283 CAIQ questions.

- `CCMv4.1.0.json` — All controls with implementation guidelines, auditing guidelines, ownership models, architectural/organizational relevance, and embedded CAIQ questions
- `CAIQv4.1.0.json` — All CAIQ questions, each with the full CCM control embedded (denormalized)
- `scripts/parse_ccm.py` — Script used to parse CCM data into JSON
- `scripts/parse_caiq.py` — Script used to parse CAIQ data into JSON

### CCM v4.0.13

Located in `CCM-4.0.13/`. Contains 197 controls split by domain due to size (~187K tokens total).

- Per-domain JSON files for Controls, Implementation Guidelines, and Auditing Guidelines (17 domains x 3 = 51 files)
- `CSV/` subfolder with normalized CSV and JSON per domain
- Consolidated files: `CCM-4.0.13-Controls.json`, `CCM-4.0.13-Implementation-Guidelines.json`, `CCM-4.0.13-Auditing-Guidelines.json`

### CCM v4.0 Implementation Guidelines v2.0

Located in `CCM v4.0 Implementation Guidelines v2.0 20240528/`. PDF-converted markdown of the implementation guidelines document.

## Licensing

No license is required for internal use of the CCM. Organizations can license the CCM for customization or commercial use. See the CSA website for details.
