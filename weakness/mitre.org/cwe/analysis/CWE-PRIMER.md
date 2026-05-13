# CWE (Common Weakness Enumeration) Primer

A comprehensive guide for understanding, using, and contributing to the Common Weakness Enumeration project.

## What is CWE?

**CWE (Common Weakness Enumeration)** is a community-developed, standardized dictionary of software and hardware weakness types maintained by the MITRE Corporation with support from the U.S. Department of Homeland Security (DHS) Cybersecurity and Infrastructure Security Agency (CISA).

### Key Concept: Weaknesses vs. Vulnerabilities

| Term | Definition | Example |
|------|------------|---------|
| **Weakness (CWE)** | A flaw, fault, or error in software/hardware design, code, or architecture that *could* lead to a vulnerability | CWE-89: SQL Injection |
| **Vulnerability (CVE)** | A specific, exploitable instance of a weakness in a particular product | CVE-2024-12345: SQL Injection in ProductX v2.1 |

Think of CWE as describing the **class of problem** (the recipe for a bug), while CVE describes a **specific instance** (a particular bug in a specific product).

## Purpose and Goals

CWE serves multiple purposes:

1. **Common Language** - Provides standardized terminology for discussing security weaknesses across organizations, tools, and researchers

2. **Root Cause Analysis** - Helps identify the underlying weakness that caused a vulnerability, enabling better prevention

3. **Tool Standardization** - Allows security tools (SAST, DAST, SCA) to report findings using consistent identifiers

4. **Education & Training** - Serves as a teaching resource for secure coding practices

5. **Metrics & Measurement** - Enables tracking of weakness trends over time (e.g., "injection flaws decreased 15% this year")

6. **Procurement & Compliance** - Provides benchmarks for evaluating vendor security practices

## CWE Identifier Format

Each weakness is assigned a unique identifier:

```
CWE-[number]
```

Examples:
- **CWE-79**: Improper Neutralization of Input During Web Page Generation (Cross-site Scripting / XSS)
- **CWE-89**: Improper Neutralization of Special Elements used in an SQL Command (SQL Injection)
- **CWE-787**: Out-of-bounds Write
- **CWE-269**: Improper Privilege Management

## CWE Structure and Organization

### Views

CWE organizes weaknesses into different "views" based on use case:

| View ID | Name | Purpose |
|---------|------|---------|
| CWE-1000 | Research Concepts | Complete hierarchical view for researchers |
| CWE-699 | Software Development | Organized by development concepts |
| CWE-1194 | Hardware Design | Hardware-specific weaknesses |
| CWE-1350 | Top 25 Weaknesses | Most dangerous software weaknesses |
| CWE-1387 | Top 25 Hardware | Most important hardware weaknesses |

### Hierarchy Levels

CWE uses a hierarchical structure with different abstraction levels:

```
Pillar (most abstract)
  └── Class
        └── Base
              └── Variant (most specific)
```

- **Pillar**: Highest-level weakness category (e.g., CWE-284: Improper Access Control)
- **Class**: Still abstract but more specific (e.g., CWE-285: Improper Authorization)
- **Base**: A specific weakness independent of language/technology (e.g., CWE-862: Missing Authorization)
- **Variant**: Language or technology-specific (e.g., CWE-434: Unrestricted Upload of File with Dangerous Type)

### Entry Components

Each CWE entry contains:

- **Description**: What the weakness is
- **Extended Description**: Detailed explanation
- **Relationships**: Parent/child and related weaknesses
- **Applicable Platforms**: Languages, technologies, architectures affected
- **Common Consequences**: What can happen if exploited (confidentiality, integrity, availability impacts)
- **Likelihood of Exploit**: How easily it can be exploited
- **Detection Methods**: How to find this weakness
- **Potential Mitigations**: How to prevent or fix it
- **Demonstrative Examples**: Code samples showing the weakness
- **Observed Examples**: Real CVEs that map to this weakness
- **References**: External resources and citations

## How CWE Interacts with Other MITRE Projects

CWE is part of a larger ecosystem of security standards:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MITRE Security Ecosystem                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   CWE (Weakness)  ──→  CVE (Vulnerability)  ──→  CVSS (Severity)    │
│        │                      │                                      │
│        │                      │                                      │
│        ▼                      ▼                                      │
│   CAPEC (Attack Pattern)    NVD (Database)                          │
│        │                                                             │
│        ▼                                                             │
│   ATT&CK (Adversary Tactics & Techniques)                           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Relationship Details

| Project | Relationship to CWE |
|---------|---------------------|
| **CVE** | CVEs reference CWEs to identify root cause. One CWE → many CVEs |
| **NVD** | Uses CWE to classify and categorize CVE entries |
| **CAPEC** | Attack patterns that exploit specific CWE weaknesses |
| **ATT&CK** | Higher-level adversary behaviors that leverage CAPEC/CWE |
| **CVSS** | Scores specific CVEs; CWE provides context for scoring |

### Example Chain

```
CWE-89 (SQL Injection weakness)
    │
    ├──→ CVE-2024-XXXXX (SQL Injection in App A)
    │         └──→ CVSS Score: 9.8 Critical
    │
    ├──→ CVE-2024-YYYYY (SQL Injection in App B)
    │
    └──→ CAPEC-66 (SQL Injection attack pattern)
              └──→ ATT&CK T1190 (Exploit Public-Facing Application)
```

## How New CWEs Are Created

### The Content Development Repository (CDR)

MITRE maintains the [CWE Content Development Repository](https://github.com/CWE-CAPEC/CWE-Content-Development-Repository) on GitHub for transparent, community-driven CWE development.

### Submission Process

**Step 1: Submit via Official Form**
- All new CWE proposals must be submitted through the [CWE Submission Form](https://cwesubmission.mitre.org/)
- Do NOT create GitHub issues directly for new content

**Step 2: MITRE Review**
- CWE Team reviews submission for clarity and appropriateness
- Submission is transferred to the public CDR repository

**Step 3: Community Input**
- Community can view and comment on the GitHub issue
- Discussions help refine the proposal

**Step 4: Publication**
- Approved content is included in the next CWE version release

### The 4 Review Stages

| Stage | Name | Description |
|-------|------|-------------|
| 1 | Initial Submission | CWE Team validates submission is clear and appropriate |
| 2 | Detailed Submission | Submitter provides full technical details |
| 3 | Content Generation | CWE Team prepares final content |
| 4 | Publication | Published in next CWE version |

There are **18 granular phases** within these stages, tracked via GitHub issue labels.

### Community Roles

| Role | Description |
|------|-------------|
| **Content Submitter** | Proposes new CWEs or updates, tracks progress, responds to feedback |
| **Content Participant** | Comments on submissions, participates in discussions |
| **Content Observer** | Watches the process to understand how it works |

### Important Rules

1. **MITRE controls the process** - Community members should not direct submitters or conduct their own reviews
2. **Use the submission form** - GitHub issues for content proposals will be closed
3. **Follow the Code of Conduct** - Be respectful in all interactions
4. **Labels are MITRE-managed** - Don't modify issue labels

## How Existing CWEs Are Updated

Updates to existing CWEs follow the same CDR process:

1. Submit proposed changes via the [CWE Submission Form](https://cwesubmission.mitre.org/)
2. MITRE reviews and creates a GitHub issue
3. Community provides feedback
4. Changes are incorporated into the next release

### Types of Updates

- **Content corrections** - Fixing errors or unclear descriptions
- **New examples** - Adding demonstrative code or observed CVEs
- **Relationship changes** - Updating parent/child relationships
- **Mitigation updates** - Adding new prevention techniques
- **Platform additions** - Extending to new languages/technologies

## CWE Versions and Releases

CWE is versioned and released periodically:

- **Current Version**: Check https://cwe.mitre.org/data/index.html
- **Release Frequency**: Multiple releases per year
- **Version Format**: X.Y (e.g., 4.19)
- **Changelog**: Each release includes detailed change notes

## Practical Usage

### For Developers

1. **Learn the Top 25** - Familiarize yourself with the [CWE Top 25](https://cwe.mitre.org/top25/) most dangerous weaknesses
2. **Secure Coding** - Use CWE mitigations as coding guidelines
3. **Code Review** - Check for CWE patterns during reviews
4. **Training** - Use CWE examples for security training

### For Security Teams

1. **Tool Configuration** - Configure SAST/DAST tools to report CWE IDs
2. **Vulnerability Triage** - Use CWE to understand root causes
3. **Metrics** - Track weakness types over time
4. **Risk Assessment** - Prioritize remediation by CWE severity

### For Procurement/Risk Managers

1. **Vendor Assessment** - Ask vendors about their CWE coverage
2. **Compliance** - Reference CWE in security requirements
3. **Benchmarking** - Compare products by weakness types found

## Data Access

### Official Downloads

- **XML Format**: https://cwe.mitre.org/data/xml/cwec_latest.xml.zip
- **Downloads Page**: https://cwe.mitre.org/data/downloads.html
- **Web Interface**: https://cwe.mitre.org/data/definitions/

### Data Formats Available

| Format | Use Case |
|--------|----------|
| XML | Complete data with full schema |
| JSON | API integration, programmatic access |
| CSV | Spreadsheet analysis, simple parsing |
| PDF | Human-readable reference |
| HTML | Web browsing |

## Key Resources

### Official MITRE Resources

- **Main Site**: https://cwe.mitre.org/
- **CWE List**: https://cwe.mitre.org/data/index.html
- **Top 25**: https://cwe.mitre.org/top25/
- **Submission Form**: https://cwesubmission.mitre.org/
- **Submission Guidelines**: https://cwe.mitre.org/community/submissions/guidelines.html
- **FAQ**: https://cwe.mitre.org/about/faq.html

### GitHub Resources

- **Content Development Repository**: https://github.com/CWE-CAPEC/CWE-Content-Development-Repository
- **CWE-CAPEC Organization**: https://github.com/CWE-CAPEC

### Related Standards

- **CVE**: https://cve.mitre.org/
- **NVD**: https://nvd.nist.gov/
- **CAPEC**: https://capec.mitre.org/
- **ATT&CK**: https://attack.mitre.org/

## Quick Reference: Common CWEs

| CWE ID | Name | Category |
|--------|------|----------|
| CWE-79 | Cross-site Scripting (XSS) | Injection |
| CWE-89 | SQL Injection | Injection |
| CWE-78 | OS Command Injection | Injection |
| CWE-287 | Improper Authentication | Authentication |
| CWE-862 | Missing Authorization | Authorization |
| CWE-306 | Missing Authentication for Critical Function | Authentication |
| CWE-798 | Use of Hard-coded Credentials | Credentials |
| CWE-22 | Path Traversal | Input Validation |
| CWE-352 | Cross-Site Request Forgery (CSRF) | Session |
| CWE-434 | Unrestricted File Upload | Input Validation |
| CWE-787 | Out-of-bounds Write | Memory |
| CWE-125 | Out-of-bounds Read | Memory |
| CWE-416 | Use After Free | Memory |
| CWE-190 | Integer Overflow | Numeric |
| CWE-502 | Deserialization of Untrusted Data | Input Validation |

## Summary

CWE is the foundational taxonomy for software and hardware security weaknesses. It provides:

- **Standardized identification** of weakness types
- **Common language** across tools, teams, and organizations
- **Root cause analysis** linking vulnerabilities to underlying flaws
- **Educational resource** for secure development practices
- **Community-driven development** through the CDR process

Understanding CWE is essential for anyone involved in software security, from developers writing code to security teams analyzing vulnerabilities to executives making procurement decisions.

---

*Last updated: December 2024*
*CWE is maintained by MITRE Corporation with support from DHS CISA*
