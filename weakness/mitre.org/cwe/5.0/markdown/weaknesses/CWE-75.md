---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-75"
cwe_id: "CWE-75"
entry_type: weakness
name: "Failure to Sanitize Special Elements into a Different Plane"
abstraction: Class
structure: Simple
status: Draft
mapping_usage: Discouraged
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/75.html"
---

# CWE-75: Failure to Sanitize Special Elements into a Different Plane

## Description

The product does not adequately filter user-controlled input for special elements with control implications.

## Alternate Terms

- **Special Element Injection**

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**
- **Resultant**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Common Consequences

| Scope | Impact |
| --- | --- |
| Integrity<br>Confidentiality<br>Availability | Modify Application Data<br>Execute Unauthorized Code or Commands |

## Potential Mitigations

- **Phase:** Requirements

  Programming languages and supporting technologies might be chosen which are not subject to these issues.

- **Phase:** Implementation

  Utilize an appropriate mix of allowlist and denylist parsing to filter special element syntax from all input.

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| PLOVER | Special Element Injection |

## Related Attack Patterns

- [CAPEC-81](https://capec.mitre.org/data/definitions/81.html)
- [CAPEC-93](https://capec.mitre.org/data/definitions/93.html)

## Mapping Notes

- **Usage:** Discouraged
- **Rationale:** This CWE entry might be under consideration for deprecation, as it is not easily distinguishable from CWE-74.
- **Comments:** Examine children and descendants of CWE-74, which are likely to be more appropriate.
- **Reasons:** Potential Deprecation, Frequent Misuse

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
