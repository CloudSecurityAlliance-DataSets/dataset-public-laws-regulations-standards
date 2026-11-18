---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-76"
cwe_id: "CWE-76"
entry_type: weakness
name: "Improper Neutralization of Equivalent Special Elements"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/76.html"
---

# CWE-76: Improper Neutralization of Equivalent Special Elements

## Description

The product correctly neutralizes certain special elements, but it improperly neutralizes equivalent special elements.

## Extended Description

The product may have a fixed list of special characters it believes is complete. However, there may be alternate encodings, or representations that also have the same meaning. For example, the product may filter out a leading slash (/) to prevent absolute path names, but does not account for a tilde (~) followed by a user name, which on some \*nix systems could be expanded to an absolute pathname. Alternately, the product might filter a dangerous "-e" command-line switch when calling an external program, but it might not account for "--exec" or other switches that have the same semantics.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-75](../weaknesses/CWE-75.md) Failure to Sanitize Special Elements into a Different Plane (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact |
| --- | --- |
| Other | Other |

## Potential Mitigations

- **Phase:** Requirements

  Programming languages and supporting technologies might be chosen which are not subject to these issues.

- **Phase:** Implementation

  Utilize an appropriate mix of allowlist and denylist parsing to filter equivalent special element syntax from all input.

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| PLOVER | Equivalent Special Element Injection |

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
