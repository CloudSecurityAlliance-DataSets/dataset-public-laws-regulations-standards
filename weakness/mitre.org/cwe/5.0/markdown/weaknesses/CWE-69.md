---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-69"
cwe_id: "CWE-69"
entry_type: weakness
name: "Improper Handling of Windows ::DATA Alternate Data Stream"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/69.html"
---

# CWE-69: Improper Handling of Windows ::DATA Alternate Data Stream

## Description

The product does not properly prevent access to, or detect usage of, alternate data streams (ADS).

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-66](../weaknesses/CWE-66.md) Improper Handling of File Names that Identify Virtual Resources (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Resultant**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |
| Operating System | Windows | Undetermined |

## Background Details

Alternate data streams (ADS) were first implemented in the Windows NT operating system to provide compatibility between NTFS and the Macintosh Hierarchical File System (HFS). In HFS, data and resource forks are used to store information about a file. The data fork provides information about the contents of the file while the resource fork stores metadata such as file type.

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Access Control<br>Non-Repudiation<br>Other | Bypass Protection Mechanism<br>Hide Activities<br>Other | An attacker can use an ADS to hide information about a file (e.g. size, the name of the process) from a system or file browser tools such as Windows Explorer and 'dir' at the command line utility. Alternately, the attacker might be able to bypass intended access restrictions for the associated data fork. |

## Detection Methods

- **Method:** Automated Analysis

  Software tools are capable of finding ADSs on your system.

## Potential Mitigations

- **Phase:** Implementation

  Ensure that the source code correctly parses the filename to read or write to the correct stream.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-1999-0278](https://www.cve.org/CVERecord?id=CVE-1999-0278) | In IIS, remote attackers can obtain source code for ASP files by appending "::$DATA" to the URL. |
| [CVE-2000-0927](https://www.cve.org/CVERecord?id=CVE-2000-0927) | Product does not properly record file sizes if they are stored in alternative data streams, which allows users to bypass quota restrictions. |

## Functional Areas

- File Processing

## Affected Resources

- System Process
- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| PLOVER | Windows ::DATA alternate data stream |

## Related Attack Patterns

- [CAPEC-168](https://capec.mitre.org/data/definitions/168.html)

## References

- [REF-562] Don Parker. "Windows NTFS Alternate Data Streams". 2005-02-16. <https://seclists.org/basics/2005/Feb/312> (URL validated: 2023-04-07).
- [REF-7] Michael Howard and David LeBlanc. "Writing Secure Code". 2nd Edition. Microsoft Press. 2002-12-04. <https://www.microsoftpressstore.com/store/writing-secure-code-9780735617223>.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Theoretical**: This and similar problems exist because the same resource can have multiple identifiers that dictate which behavior can be performed on the resource.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Applicable_Platforms, Background_Details, Description, Relationships, Other_Notes, References, Taxonomy_Mappings |
| Modification | 2008-10-14 | CWE Content Team | MITRE | CWE 1.0.1, 2008-10-14 | updated Description |
| Modification | 2009-10-29 | CWE Content Team | MITRE | CWE 1.6, 2009-10-29 | updated Other_Notes, Theoretical_Notes |
| Modification | 2010-04-05 | CWE Content Team | MITRE | CWE 1.8.1, 2010-04-05 | updated Related_Attack_Patterns |
| Modification | 2010-12-13 | CWE Content Team | MITRE | CWE 1.11, 2010-12-13 | updated Name |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Observed_Examples, References, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Applicable_Platforms, References, Relationships |
| Modification | 2018-03-27 | CWE Content Team | MITRE | CWE 3.1, 2018-03-27 | updated References |
| Modification | 2019-01-03 | CWE Content Team | MITRE | CWE 3.2, 2019-01-03 | updated Related_Attack_Patterns |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated References, Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Affected_Resources, Functional_Areas |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Detection_Factors, Potential_Mitigations, Weakness_Ordinalities |
| Modification | 2026-10-28 | CWE Content Team | MITRE | CWE 5.0, 2026-10-28 | updated Common_Consequences, Description |

**Previous Entry Names:**

- Windows ::DATA Alternate Data Stream — 2008-04-11
- Failure to Handle Windows ::DATA Alternate Data Stream — 2010-12-13

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
