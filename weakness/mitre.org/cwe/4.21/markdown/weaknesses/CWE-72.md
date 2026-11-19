---
secid: "secid:weakness/mitre.org/cwe@4.21#CWE-72"
cwe_id: "CWE-72"
entry_type: weakness
name: "Improper Handling of Apple HFS+ Alternate Data Stream Path"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.21"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/72.html"
---

# CWE-72: Improper Handling of Apple HFS+ Alternate Data Stream Path

## Description

The product does not properly handle special paths that may identify the data or resource fork of a file on the HFS+ file system.

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
| Operating System | macOS | Undetermined |

## Background Details

The Apple HFS+ file system permits files to have multiple data input streams, accessible through special paths. The Mac OS X operating system provides a way to access the different data input streams through special paths and as an extended attribute:

\- Resource fork: file/..namedfork/rsrc, file/rsrc (deprecated), xattr:com.apple.ResourceFork

\- Data fork: file/..namedfork/data (only versions prior to Mac OS X v10.5)

Additionally, on filesystems that lack native support for multiple streams, the resource fork and file metadata may be stored in a file with ".\_" prepended to the name.

Forks can also be accessed through non-portable APIs.

Forks inherit the file system access controls of the file they belong to.

Programs need to control access to these paths, if the processing of a file system object is dependent on the structure of its path.

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Integrity | Read Files or Directories<br>Modify Files or Directories<br>Bypass Protection Mechanism | If the product chooses actions to take based on the file name, then if an attacker provides the data or resource fork, the product may take unexpected actions. Further, if the product intends to restrict access to a file, then an attacker might still be able to bypass intended access restrictions by requesting the data or resource fork for that file. |

## Demonstrative Examples

### Example 1 (DX-227)

Consider a web server that uses the Apple HFS+ file system. It interprets FILE.cgi as processing instructions.

An adversary could request "FILE.cgi/..namedfork/data" to prevent FILE.cgi from being executed, instead disclosing the source code for FILE.cgi. This might occur because the web server invokes the default handler which may return the contents of the file.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2004-1084](https://www.cve.org/CVERecord?id=CVE-2004-1084) | Server allows remote attackers to read files and resource fork content via HTTP requests to certain special file names related to multiple data streams in HFS+. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## References

- [REF-578] NetSec. "NetSec Security Advisory: Multiple Vulnerabilities Resulting From Use Of Apple OSX HFS+". BugTraq. 2005-02-16. <https://seclists.org/bugtraq/2005/Feb/309> (URL validated: 2023-04-07).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Theoretical**: This and similar problems exist because the same resource can have multiple identifiers that dictate which behavior can be performed on the resource.

- **Research Gap**: Under-studied

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, Other_Notes, Taxonomy_Mappings |
| Modification | 2008-11-05 | David Remahl | Apple | CWE 1.1, 2008-11-25 | clarified description, provided background details, and added demonstrative example |
| Modification | 2008-11-24 | CWE Content Team | MITRE | CWE 1.1, 2008-11-25 | updated Applicable_Platforms, Background_Details, Demonstrative_Examples, Description, Name, References |
| Modification | 2009-05-27 | CWE Content Team | MITRE | CWE 1.4, 2009-05-27 | updated Name |
| Modification | 2009-10-29 | CWE Content Team | MITRE | CWE 1.6, 2009-10-29 | updated Other_Notes, Theoretical_Notes |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Observed_Examples, Relationships |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Applicable_Platforms, References, Relationships, Taxonomy_Mappings |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated References, Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Affected_Resources, Functional_Areas |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Demonstrative_Examples, Weakness_Ordinalities |

**Previous Entry Names:**

- Apple HFS+ Alternate Data Stream — 2008-11-24
- Failure to Handle Apple HFS+ Alternate Data Stream Path — 2009-05-27

---
Generated from MITRE's CWE 4.21 XML (cwec_v4.21.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.21/LICENSE.txt).
