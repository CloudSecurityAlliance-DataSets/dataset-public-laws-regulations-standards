---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-5"
cwe_id: "CWE-5"
entry_type: weakness
name: "J2EE Misconfiguration: Data Transmission Without Encryption"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/5.html"
---

# CWE-5: J2EE Misconfiguration: Data Transmission Without Encryption

## Description

The product uses J2EE with a configuration that transmits data without encryption.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-319](../weaknesses/CWE-319.md) Cleartext Transmission of Sensitive Information (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Prevalence |
| --- | --- | --- |
| Language | Java | Undetermined |

## Modes Of Introduction

- **Implementation**
- **Operation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality | Read Application Data | An attacker may be able to read the data sent in plaintext. |
| Integrity | Modify Application Data | Information sent over a network can be compromised while in transit. An attacker may be able to modify the contents of data sent in plaintext. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

## Potential Mitigations

- **Phase:** System Configuration

  The product configuration should ensure that SSL or an encryption mechanism of equivalent strength and vetted reputation is used for all access-controlled pages.

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| 7 Pernicious Kingdoms | J2EE Misconfiguration: Insecure Transport |

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://cwe.mitre.org/documents/sources/SevenPerniciousKingdoms.pdf>.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Other**:

  If an application uses SSL to guarantee confidential communication with client browsers, the application configuration should make it impossible to view any access controlled page without SSL. There are three common ways for SSL to be bypassed:

  - A user manually enters URL and types "HTTP" rather than "HTTPS".
  - Attackers intentionally send a user to an insecure URL.
  - A programmer erroneously creates a relative link to a page in the application, which does not switch from HTTP to HTTPS. (This is particularly easy to do when the link moves between public and secured areas on a web site.)

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | 7 Pernicious Kingdoms |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, Other_Notes, Taxonomy_Mappings |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Other_Notes |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Common_Consequences, Description |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated References, Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Potential_Mitigations |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Relationships, Weakness_Ordinalities |
| Modification | 2026-10-28 | CWE Content Team | MITRE | CWE 5.0, 2026-10-28 | updated Common_Consequences, Description, Detection_Factors, References |

**Previous Entry Names:**

- J2EE Misconfiguration: Insecure Transport — 2008-04-11

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
