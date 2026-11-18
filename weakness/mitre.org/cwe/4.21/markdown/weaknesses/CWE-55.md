---
secid: "secid:weakness/mitre.org/cwe@4.21#CWE-55"
cwe_id: "CWE-55"
entry_type: weakness
name: "Path Equivalence: '/./' (Single Dot Directory)"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.21"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/55.html"
---

# CWE-55: Path Equivalence: '/./' (Single Dot Directory)

## Description

The product accepts path input in the form of single dot directory exploit ('/./') without appropriate validation, which can lead to ambiguous path resolution and allow an attacker to traverse the file system to unintended locations or access arbitrary files.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-41](../weaknesses/CWE-41.md) Improper Resolution of Path Equivalence (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**
- **Resultant**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact |
| --- | --- |
| Confidentiality<br>Integrity | Read Files or Directories<br>Modify Files or Directories |

## Potential Mitigations

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-20

  Inputs should be decoded and canonicalized to the application's current internal representation before being validated (CWE-180). Make sure that the application does not decode the same input twice (CWE-174). Such errors could be used to bypass allowlist validation schemes by introducing dangerous inputs after they have been checked.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2024-6091](https://www.cve.org/CVERecord?id=CVE-2024-6091) | Chain: AI agent platform does not restrict pathnames containing internal "/./" sequences (CWE-55), leading to an incomplete denylist (CWE-184) that does not prevent OS command injection (CWE-78) |
| [CVE-2000-0004](https://www.cve.org/CVERecord?id=CVE-2000-0004) | Server allows remote attackers to read source code for executable files by inserting a . (dot) into the URL. |
| [CVE-2002-0304](https://www.cve.org/CVERecord?id=CVE-2002-0304) | Server allows remote attackers to read password-protected files via a /./ in the HTTP request. |
| [CVE-1999-1083](https://www.cve.org/CVERecord?id=CVE-1999-1083) | Possibly (could be a cleansing error) |
| [CVE-2004-0815](https://www.cve.org/CVERecord?id=CVE-2004-0815) | "/./////etc" cleansed to ".///etc" then "/etc" |
| [CVE-2002-0112](https://www.cve.org/CVERecord?id=CVE-2002-0112) | Server allows remote attackers to view password protected files via /./ in the URL. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | /./ (single dot directory) |
| Software Fault Patterns | SFP16 | Path Traversal |

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 4.21 XML (cwec_v4.21.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.21/LICENSE.txt).
