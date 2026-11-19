---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-75"
cwe_id: "CWE-75"
entry_type: weakness
name: "Failure to Sanitize Special Elements into a Different Plane (Special Element Injection)"
abstraction: Class
structure: Simple
status: Draft
mapping_usage: Discouraged
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/75.html"
---

# CWE-75: Failure to Sanitize Special Elements into a Different Plane (Special Element Injection)

## Description

The product does not adequately filter user-controlled input for special elements with control implications.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |

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
- **Rationale:** This CWE entry might be under consideraton for deprecation, as it is not easily distinguishable from CWE-74.
- **Comments:** N/A
- **Reasons:** Potential Deprecation

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital |  | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2010-12-13 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2017-05-03 | CWE Content Team | MITRE |  | updated Potential_Mitigations, Related_Attack_Patterns |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Applicable_Platforms, Modes_of_Introduction, Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2021-10-28 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Weakness_Ordinalities |

**Previous Entry Names:**

- Special Element Injection — 2008-04-11

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
