---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-66"
cwe_id: "CWE-66"
entry_type: weakness
name: "Improper Handling of File Names that Identify Virtual Resources"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/66.html"
---

# CWE-66: Improper Handling of File Names that Identify Virtual Resources

## Description

The product does not handle or incorrectly handles a file name that identifies a "virtual" resource that is not directly specified within the directory that is associated with the file name.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-706](../weaknesses/CWE-706.md) Use of Incorrectly-Resolved Name or Reference (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**
- **Resultant**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Background Details

Virtual file names are represented like normal file names, but they are effectively aliases for other resources that do not behave like typical files. Depending on their functionality, they could be alternate entities that behave differently than typical files. They are not necessarily listed in directories.

## Modes Of Introduction

- **Implementation**
- **Operation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Other | Varies by Context | The product could perform file-based operations on a resource that is not a file. |

## Detection Methods

- **Method:** Automated Static Analysis - Binary or Bytecode

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Cost effective for partial coverage:

  - Bytecode Weakness Analysis - including disassembler + source code weakness analysis

  **Effectiveness:** SOAR Partial

- **Method:** Manual Static Analysis - Binary or Bytecode

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Cost effective for partial coverage:

  - Binary / Bytecode disassembler - then use manual analysis for vulnerabilities & anomalies

  **Effectiveness:** SOAR Partial

- **Method:** Dynamic Analysis with Automated Results Interpretation

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Cost effective for partial coverage:

  - Web Application Scanner
  - Web Services Scanner
  - Database Scanners

  **Effectiveness:** SOAR Partial

- **Method:** Dynamic Analysis with Manual Results Interpretation

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Cost effective for partial coverage:

  - Fuzz Tester
  - Framework-based Fuzzer

  **Effectiveness:** SOAR Partial

- **Method:** Manual Static Analysis - Source Code

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Focused Manual Spotcheck - Focused manual analysis of source
  - Manual Source Code Review (not inspections)

  **Effectiveness:** High

- **Method:** Automated Static Analysis - Source Code

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Cost effective for partial coverage:

  - Source code Weakness Analyzer
  - Context-configured Source Code Weakness Analyzer

  **Effectiveness:** SOAR Partial

- **Method:** Architecture or Design Review

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Formal Methods / Correct-By-Construction

  Cost effective for partial coverage:

  - Inspection (IEEE 1028 standard) (can apply to requirements, design, source code, etc.)

  **Effectiveness:** High

## Demonstrative Examples

### Example 1 (DX-227)

Consider a web server that uses the Apple HFS+ file system. It interprets FILE.cgi as processing instructions.

An adversary could request "FILE.cgi/..namedfork/data" to prevent FILE.cgi from being executed, instead disclosing the source code for FILE.cgi. This might occur because the web server invokes the default handler which may return the contents of the file.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-1999-0278](https://www.cve.org/CVERecord?id=CVE-1999-0278) | In IIS, remote attackers can obtain source code for ASP files by appending "::$DATA" to the URL. |
| [CVE-2004-1084](https://www.cve.org/CVERecord?id=CVE-2004-1084) | Server allows remote attackers to read files and resource fork content via HTTP requests to certain special file names related to multiple data streams in HFS+. |
| [CVE-2002-0106](https://www.cve.org/CVERecord?id=CVE-2002-0106) | Server allows remote attackers to cause a denial of service via a series of requests to .JSP files that contain an MS-DOS device name. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| PLOVER | Virtual Files |

## References

- [REF-1479] Gregory Larsen, E. Kenneth Hong Fong, David A. Wheeler and Rama S. Moorthy. "State-of-the-Art Resources (SOAR) for Software Vulnerability Detection, Test, and Evaluation". 2014-07. <https://www.ida.org/-/media/feature/publications/s/st/stateoftheart-resources-soar-for-software-vulnerability-detection-test-and-evaluation/p-5061.ashx> (URL validated: 2025-09-05).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Description, Relationships, Taxonomy_Mappings, Type |
| Modification | 2009-03-10 | CWE Content Team | MITRE | CWE 1.3, 2009-03-10 | updated Description, Name |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Relationships |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Detection_Factors, Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Affected_Resources, Applicable_Platforms, Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Relationships |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2023-10-26 | CWE Content Team | MITRE | CWE 4.13, 2023-10-26 | updated Observed_Examples |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Detection_Factors, References |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Demonstrative_Examples, Weakness_Ordinalities |
| Modification | 2026-10-28 | CWE Content Team | MITRE | CWE 5.0, 2026-10-28 | updated Background_Details, Common_Consequences, Description |

**Previous Entry Names:**

- Virtual Files — 2008-04-11
- Failure to Handle File Names that Identify Virtual Resources — 2009-03-10

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
