---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-97"
cwe_id: "CWE-97"
entry_type: weakness
name: "Improper Neutralization of Server-Side Includes (SSI) Within a Web Page"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/97.html"
---

# CWE-97: Improper Neutralization of Server-Side Includes (SSI) Within a Web Page

## Description

The product generates a web page, but does not neutralize or incorrectly neutralizes user-controllable input that could be interpreted as a server-side include (SSI) directive.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-96](../weaknesses/CWE-96.md) Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection') (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Not Language-Specific | Undetermined |
| Technology |  | Web Based | Undetermined |
| Technology | Web Server |  | Undetermined |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Common Consequences

| Scope | Impact |
| --- | --- |
| Confidentiality<br>Integrity<br>Availability | Execute Unauthorized Code or Commands |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | Server-Side Includes (SSI) Injection |
| WASC | 36 | SSI Injection |

## Related Attack Patterns

- [CAPEC-101](https://capec.mitre.org/data/definitions/101.html)
- [CAPEC-35](https://capec.mitre.org/data/definitions/35.html)

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Relationship**: This can be resultant from XSS/HTML injection because the same special characters can be involved. However, this is server-side code execution, not client-side.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital |  | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Relationships, Other_Notes, Taxonomy_Mappings |
| Modification | 2009-10-29 | CWE Content Team | MITRE |  | updated Other_Notes, Relationship_Notes |
| Modification | 2010-02-16 | CWE Content Team | MITRE |  | updated Taxonomy_Mappings |
| Modification | 2010-06-21 | CWE Content Team | MITRE |  | updated Description, Name, Type |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2017-05-03 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Applicable_Platforms, Modes_of_Introduction, Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated Potential_Mitigations, Relationships |
| Modification | 2021-10-28 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms, Relationships, Weakness_Ordinalities |

**Previous Entry Names:**

- Server-Side Includes (SSI) Injection — 2008-04-11
- Failure to Sanitize Server-Side Includes (SSI) Within a Web Page — 2010-06-21

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
