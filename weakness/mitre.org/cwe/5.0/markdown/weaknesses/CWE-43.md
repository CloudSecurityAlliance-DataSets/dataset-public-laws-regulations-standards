---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-43"
cwe_id: "CWE-43"
entry_type: weakness
name: "Path Equivalence: 'filename....' (Multiple Trailing Dot)"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/43.html"
---

# CWE-43: Path Equivalence: 'filename....' (Multiple Trailing Dot)

## Description

The product accepts path input in the form of multiple trailing dot ('filedir....') without appropriate validation, which can lead to ambiguous path resolution and allow an attacker to traverse the file system to unintended locations or access arbitrary files.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-42](../weaknesses/CWE-42.md) Path Equivalence: 'filename.' (Trailing Dot) (Variant) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-163](../weaknesses/CWE-163.md) Improper Neutralization of Multiple Trailing Special Elements (Variant) | [CWE-1000](../views/CWE-1000.md) |  |

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
| [CVE-2004-0281](https://www.cve.org/CVERecord?id=CVE-2004-0281) | Multiple trailing dot allows directory listing |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | Multiple Trailing Dot - 'filedir....' |
| Software Fault Patterns | SFP16 | Path Traversal |

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
