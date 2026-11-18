---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-50"
cwe_id: "CWE-50"
entry_type: weakness
name: "Path Equivalence: '//multiple/leading/slash'"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/50.html"
---

# CWE-50: Path Equivalence: '//multiple/leading/slash'

## Description

The product accepts path input in the form of multiple leading slash ('//multiple/leading/slash') without appropriate validation, which can lead to ambiguous path resolution and allow an attacker to traverse the file system to unintended locations or access arbitrary files.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-41](../weaknesses/CWE-41.md) Improper Resolution of Path Equivalence (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-161](../weaknesses/CWE-161.md) Improper Neutralization of Multiple Leading Special Elements (Variant) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

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

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2002-1483](https://www.cve.org/CVERecord?id=CVE-2002-1483) | Read files with full pathname using multiple internal slash. |
| [CVE-1999-1456](https://www.cve.org/CVERecord?id=CVE-1999-1456) | Server allows remote attackers to read arbitrary files via a GET request with more than one leading / (slash) character in the filename. |
| [CVE-2004-0578](https://www.cve.org/CVERecord?id=CVE-2004-0578) | Server allows remote attackers to read arbitrary files via leading slash (//) characters in a URL request. |
| [CVE-2002-0275](https://www.cve.org/CVERecord?id=CVE-2002-0275) | Server allows remote attackers to bypass authentication and read restricted files via an extra / (slash) in the requested URL. |
| [CVE-2004-1032](https://www.cve.org/CVERecord?id=CVE-2004-1032) | Product allows local users to delete arbitrary files or create arbitrary empty files via a target filename with a large number of leading slash (/) characters. |
| [CVE-2002-1238](https://www.cve.org/CVERecord?id=CVE-2002-1238) | Server allows remote attackers to bypass access restrictions for files via an HTTP request with a sequence of multiple / (slash) characters such as http://www.example.com///file/. |
| [CVE-2004-1878](https://www.cve.org/CVERecord?id=CVE-2004-1878) | Product allows remote attackers to bypass authentication, obtain sensitive information, or gain access via a direct request to admin/user.pl preceded by // (double leading slash). |
| [CVE-2005-1365](https://www.cve.org/CVERecord?id=CVE-2005-1365) | Server allows remote attackers to execute arbitrary commands via a URL with multiple leading "/" (slash) characters and ".." sequences. |
| [CVE-2000-1050](https://www.cve.org/CVERecord?id=CVE-2000-1050) | Access directory using multiple leading slash. |
| [CVE-2001-1072](https://www.cve.org/CVERecord?id=CVE-2001-1072) | Bypass access restrictions via multiple leading slash, which causes a regular expression to fail. |
| [CVE-2004-0235](https://www.cve.org/CVERecord?id=CVE-2004-0235) | Archive extracts to arbitrary files using multiple leading slash in filenames in the archive. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | //multiple/leading/slash ('multiple leading slash') |
| Software Fault Patterns | SFP16 | Path Traversal |

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
