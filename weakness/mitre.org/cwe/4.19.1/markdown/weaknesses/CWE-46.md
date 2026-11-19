---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-46"
cwe_id: "CWE-46"
entry_type: weakness
name: "Path Equivalence: 'filename ' (Trailing Space)"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/46.html"
---

# CWE-46: Path Equivalence: 'filename ' (Trailing Space)

## Description

The product accepts path input in the form of trailing space ('filedir ') without appropriate validation, which can lead to ambiguous path resolution and allow an attacker to traverse the file system to unintended locations or access arbitrary files.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-41](../weaknesses/CWE-41.md) Improper Resolution of Path Equivalence (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-162](../weaknesses/CWE-162.md) Improper Neutralization of Trailing Special Elements (Variant) | [CWE-1000](../views/CWE-1000.md) |  |
| CanPrecede | [CWE-289](../weaknesses/CWE-289.md) Authentication Bypass by Alternate Name (Base) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Resultant**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |
| Technology | Not Technology-Specific | Undetermined |
| Technology | Web Based | Undetermined |

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact |
| --- | --- |
| Confidentiality<br>Integrity | Read Files or Directories<br>Modify Files or Directories |

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2001-0693](https://www.cve.org/CVERecord?id=CVE-2001-0693) | Source disclosure via trailing encoded space "%20" |
| [CVE-2001-0778](https://www.cve.org/CVERecord?id=CVE-2001-0778) | Source disclosure via trailing encoded space "%20" |
| [CVE-2001-1248](https://www.cve.org/CVERecord?id=CVE-2001-1248) | Source disclosure via trailing encoded space "%20" |
| [CVE-2004-0280](https://www.cve.org/CVERecord?id=CVE-2004-0280) | Source disclosure via trailing encoded space "%20" |
| [CVE-2004-2213](https://www.cve.org/CVERecord?id=CVE-2004-2213) | Source disclosure via trailing encoded space "%20" |
| [CVE-2005-0622](https://www.cve.org/CVERecord?id=CVE-2005-0622) | Source disclosure via trailing encoded space "%20" |
| [CVE-2005-1656](https://www.cve.org/CVERecord?id=CVE-2005-1656) | Source disclosure via trailing encoded space "%20" |
| [CVE-2002-1603](https://www.cve.org/CVERecord?id=CVE-2002-1603) | Source disclosure via trailing encoded space "%20" |
| [CVE-2001-0054](https://www.cve.org/CVERecord?id=CVE-2001-0054) | Multi-Factor Vulnerability (MFV). directory traversal and other issues in FTP server using Web encodings such as "%20"; certain manipulations have unusual side effects. |
| [CVE-2002-1451](https://www.cve.org/CVERecord?id=CVE-2002-1451) | Trailing space ("+" in query string) leads to source code disclosure. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | Trailing Space - 'filedir ' |
| Software Fault Patterns | SFP16 | Path Traversal |

## Related Attack Patterns

- [CAPEC-649](https://capec.mitre.org/data/definitions/649.html)

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital |  | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Applicable_Platforms |
| Modification | 2019-06-20 | CWE Content Team | MITRE |  | updated Related_Attack_Patterns |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2023-10-26 | CWE Content Team | MITRE |  | updated Observed_Examples |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Affected_Resources, Functional_Areas |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms, Weakness_Ordinalities |

**Previous Entry Names:**

- Path Issue - Trailing Space - 'filedir ' — 2008-04-11

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
