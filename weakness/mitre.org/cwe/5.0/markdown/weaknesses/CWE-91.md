---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-91"
cwe_id: "CWE-91"
entry_type: weakness
name: "XML Injection"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed-with-Review
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/91.html"
---

# CWE-91: XML Injection

## Description

The product does not properly neutralize special elements that are used in XML, allowing attackers to modify the syntax, content, or commands of the XML before it is processed by an end system.

## Extended Description

Within XML, special elements could include reserved words or characters such as "&lt;", ">", """, and "&", which could then be used to add new data or modify XML syntax.

## Alternate Terms

- **Blind XPath Injection** (Common-Name, Attack-Focused)

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component (Class) | [CWE-1003](../views/CWE-1003.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Common Consequences

| Scope | Impact |
| --- | --- |
| Confidentiality<br>Integrity<br>Availability | Execute Unauthorized Code or Commands<br>Read Application Data<br>Modify Application Data |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| PLOVER |  | XML injection (aka Blind Xpath injection) |  |
| OWASP Top Ten 2007 | A2 | Injection Flaws | CWE More Specific |
| OWASP Top Ten 2004 | A6 | Injection Flaws | CWE More Specific |
| WASC | 23 | XML Injection |  |
| Software Fault Patterns | SFP24 | Tainted input to command |  |

## Related Attack Patterns

- [CAPEC-250](https://capec.mitre.org/data/definitions/250.html)
- [CAPEC-83](https://capec.mitre.org/data/definitions/83.html)

## References

- [REF-882] Amit Klein. "Blind XPath Injection". 2004-05-19. <https://dl.packetstormsecurity.net/papers/bypass/Blind_XPath_Injection_20040518.pdf> (URL validated: 2023-04-07).
- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 17, "XML Injection", Page 1069. 1st Edition. Addison Wesley. 2006.
- [REF-1534] OMG. "Automated Technical Debt Measure, Version 2". 2024-08. <https://www.omg.org/spec/ATDM2/1.0/PDF> (URL validated: 2026-07-16).

## Mapping Notes

- **Usage:** Allowed-with-Review

- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.

- **Comments:** This weakness might be confused with other weaknesses such as XXE. Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.

- **Reasons:** Acceptable-Use

- **Suggestions:**

  - [CWE-611](../weaknesses/CWE-611.md) Improper Restriction of XML External Entity Reference (Base): XML External Entity (XXE)

## Notes

- **Maintenance**: The description for this entry is generally applicable to XML, but the name includes "blind XPath injection" which is more closely associated with CWE-643. Therefore this entry might need to be deprecated or converted to a general category - although injection into raw XML is not covered by CWE-643 or CWE-652.

- **Theoretical**: In vulnerability theory terms, this is a representation-specific case of a Data/Directive Boundary Error.

- **Research Gap**: Under-reported. This is likely found regularly by third party code auditors, but there are very few publicly reported examples.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-08-15 |  | Veracode | CWE 1.0, 2008-09-09 | Suggested OWASP Top Ten 2004 mapping |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, Other_Notes, Taxonomy_Mappings |
| Modification | 2008-10-14 | CWE Content Team | MITRE | CWE 1.0.1, 2008-10-14 | updated Maintenance_Notes, Other_Notes, Theoretical_Notes |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 | updated Taxonomy_Mappings |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Description, Relationships |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated References, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2014-02-18 | CWE Content Team | MITRE | CWE 2.6, 2014-02-19 | updated Related_Attack_Patterns |
| Modification | 2014-06-23 | CWE Content Team | MITRE | CWE 2.7, 2014-06-23 | updated Relationships |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships, Taxonomy_Mappings |
| Modification | 2015-12-07 | CWE Content Team | MITRE | CWE 2.9, 2015-12-07 | updated Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Applicable_Platforms, Modes_of_Introduction, References, Relationships |
| Modification | 2018-03-27 | CWE Content Team | MITRE | CWE 3.1, 2018-03-27 | updated Relationships |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Related_Attack_Patterns |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Potential_Mitigations, Related_Attack_Patterns, Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Potential_Mitigations |
| Modification | 2020-08-20 | CWE Content Team | MITRE | CWE 4.2, 2020-08-20 | updated Relationships |
| Modification | 2020-12-10 | CWE Content Team | MITRE | CWE 4.3, 2020-12-10 | updated Relationships |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Detection_Factors, References, Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Relationships, Weakness_Ordinalities |
| Modification | 2026-04-30 | CWE Content Team | MITRE | CWE 4.20, 2026-04-30 | updated Mapping_Notes |
| Modification | 2026-10-28 | CWE Content Team | MITRE | CWE 5.0, 2026-10-28 | updated Alternate_Terms, Name, References |

**Previous Entry Names:**

- XML Injection (aka Blind XPath Injection) — 2026-10-28

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
