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

Machine-readable formats (JSON, YAML, OSCAL) are also available, but CSA's machine-readable bundle is still 4.1.0; 4.1.1's mappings exist only in the spreadsheet and in this repo's extraction.

## Control Domains (17)

CCM v4.1 renamed the infrastructure domain's code from `IVS` (v4.0: Infrastructure & Virtualization Security) to `I&S` (Infrastructure Security). CCM v3.0.1 used a different domain set altogether.

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
| Infrastructure Security | I&S | 9 |
| Interoperability & Portability | IPY | 4 |
| Logging and Monitoring | LOG | 14 |
| Security Incident Management, E-Discovery, & Cloud Forensics | SEF | 10 |
| Supply Chain Management, Transparency, and Accountability | STA | 16 |
| Threat & Vulnerability Management | TVM | 12 |
| Universal Endpoint Management | UEM | 14 |

## Versions in This Repository

| Version | Directory | Controls | Status |
|---|---|---:|---|
| **4.1.1** | [`4.1.1/`](4.1.1/) | 207 | current; claims the bare labels `4.1` / `v4.1` |
| 4.1.0 | [`4.1.0/`](4.1.0/) | 207 | superseded by 4.1.1 (`ccm/4.1/` until 2026-10-23) |
| 4.0.13 | [`4.0.13/`](4.0.13/) | 197 | superseded; CSA's served v4.0 |
| 3.0.1 | [`3.0.1/`](3.0.1/) | 133 | superseded; different domain structure |

The CAIQ questionnaires are extracted separately, under [`../ccm-caiq/`](../ccm-caiq/).

### CCM v4.1.1 (October 2026): current

Located in [`4.1.1/`](4.1.1/). Contains 207 controls and 283 CAIQ questions. A patch release over 4.1.0 that CSA shipped inside the unchanged "v4.1" bundle: same control IDs, the first CCM v4.1 mappings (NIST SP 800-171 rev2, MITRE ATT&CK v17.1), a DORA reverse mapping, and reworded text. See [`4.1.1/README.md`](4.1.1/README.md) and [`4.1.1/CHANGES-FROM-4.1.0.md`](4.1.1/CHANGES-FROM-4.1.0.md).

- `ccm-4.1.1.json`: all controls with guidelines, ownership, relevance grids, mappings and embedded CAIQ questions, plus `reverse_mappings.dora`
- `ccm-4.1.1-controls.csv`, `ccm-4.1.1-reverse-mappings.csv`: flat forms of the same
- `scripts/parse_ccm.py`: the extractor

### CCM v4.1.0 (January 2026)

Located in [`4.1.0/`](4.1.0/). Contains 207 controls and 283 CAIQ questions. No cross-framework mappings: CSA's mappings sheet for 4.1.0 read "This dataset is not available yet".

- `ccm-4.1.0.json`: all controls with implementation guidelines, auditing guidelines, ownership models, architectural/organizational relevance, and embedded CAIQ questions
- `scripts/parse_ccm.py`: reproduces `ccm-4.1.0.json` byte for byte from `CCMv4.1.0-generated_at_2026_01_13.xlsx`

### CCM v4.0.13

Located in [`4.0.13/`](4.0.13/). Contains 197 controls, split by domain because of size.

- Per-domain JSON files for Controls, Implementation Guidelines, and Auditing Guidelines (17 domains x 3 = 51 files)
- Consolidated files: `ccm-4.0.13-Controls.json`, `ccm-4.0.13-Implementation-Guidelines.json`, `ccm-4.0.13-Auditing-Guidelines.json`
- `CSV/`: normalized CSV and JSON, overall and per domain, including the v4.0 cross-framework mapping columns (ISO/IEC 27001/27002/27017/27018, NIST SP 800-53 rev5, NIST CSF, PCI DSS, CIS v8, AICPA TSC and others)

### CCM v3.0.1

Located in [`3.0.1/`](3.0.1/). Contains 133 controls across 16 domains. See [`3.0.1/README.md`](3.0.1/README.md).

### Figure check

[`check_figures.py`](check_figures.py) recomputes every figure the 4.1.1 docs quote, and the CAIQ 4.1.0 table of changed questions, from the committed data. It exits 1 on any drift.

## Licensing

No license is required for internal use of the CCM. Organizations can license the CCM for customization or commercial use. See the CSA website for details.
