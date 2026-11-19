---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-67"
cwe_id: "CWE-67"
entry_type: weakness
name: "Improper Handling of Windows Device Names"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/67.html"
---

# CWE-67: Improper Handling of Windows Device Names

## Description

The product constructs pathnames from user input, but it does not handle or incorrectly handles a pathname containing a Windows device name such as AUX or CON. This typically leads to denial of service or an information exposure when the application attempts to process the pathname as a regular file.

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

Historically, there was a bug in the Windows operating system that caused a blue screen of death. Even after that issue was fixed DOS device names continue to be a factor.

## Modes Of Introduction

- **Implementation**
- **Operation**

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Availability<br>Confidentiality<br>Other | DoS: Crash, Exit, or Restart<br>Read Application Data<br>Other | Not properly handling virtual filenames (e.g. AUX, CON, PRN, COM1, LPT1) can result in different types of vulnerabilities. In some cases an attacker can request a device via injection of a virtual filename in a URL, which may cause an error that leads to a denial of service or an error page that reveals sensitive information. A product that allows device names to bypass filtering runs the risk of an attacker injecting malicious code in a file with the name of a device. |

## Potential Mitigations

- **Phase:** Implementation

  Be familiar with the device names in the operating system where your system is deployed. Check input for these device names.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2002-0106](https://www.cve.org/CVERecord?id=CVE-2002-0106) | Server allows remote attackers to cause a denial of service via a series of requests to .JSP files that contain an MS-DOS device name. |
| [CVE-2002-0200](https://www.cve.org/CVERecord?id=CVE-2002-0200) | Server allows remote attackers to cause a denial of service via an HTTP request for an MS-DOS device name. |
| [CVE-2002-1052](https://www.cve.org/CVERecord?id=CVE-2002-1052) | Product allows remote attackers to use MS-DOS device names in HTTP requests to cause a denial of service or obtain the physical path of the server. |
| [CVE-2001-0493](https://www.cve.org/CVERecord?id=CVE-2001-0493) | Server allows remote attackers to cause a denial of service via a URL that contains an MS-DOS device name. |
| [CVE-2001-0558](https://www.cve.org/CVERecord?id=CVE-2001-0558) | Server allows a remote attacker to create a denial of service via a URL request which includes a MS-DOS device name. |
| [CVE-2000-0168](https://www.cve.org/CVERecord?id=CVE-2000-0168) | Microsoft Windows 9x operating systems allow an attacker to cause a denial of service via a pathname that includes file device names, aka the "DOS Device in Path Name" vulnerability. |
| [CVE-2001-0492](https://www.cve.org/CVERecord?id=CVE-2001-0492) | Server allows remote attackers to determine the physical path of the server via a URL containing MS-DOS device names. |
| [CVE-2004-0552](https://www.cve.org/CVERecord?id=CVE-2004-0552) | Product does not properly handle files whose names contain reserved MS-DOS device names, which can allow malicious code to bypass detection when it is installed, copied, or executed. |
| [CVE-2005-2195](https://www.cve.org/CVERecord?id=CVE-2005-2195) | Server allows remote attackers to cause a denial of service (application crash) via a URL with a filename containing a .cgi extension and an MS-DOS device name. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| PLOVER |  | Windows MS-DOS device names |  |
| CERT C Secure Coding | FIO32-C | Do not perform operations on devices that are only appropriate for files | CWE More Specific |
| The CERT Oracle Secure Coding Standard for Java (2011) | FIO00-J | Do not operate on files in shared directories |  |
| Software Fault Patterns | SFP16 | Path Traversal |  |

## References

- [REF-7] Michael Howard and David LeBlanc. "Writing Secure Code". 2nd Edition. Microsoft Press. 2002-12-04. <https://www.microsoftpressstore.com/store/writing-secure-code-9780735617223>.
- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 11, "Device Files", Page 666. 1st Edition. Addison Wesley. 2006.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Applicable_Platforms, Relationships, Other_Notes, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2008-10-14 | CWE Content Team | MITRE | CWE 1.0.1, 2008-10-14 | updated Description |
| Modification | 2008-11-24 | CWE Content Team | MITRE | CWE 1.1, 2008-11-25 | updated Relationships, Taxonomy_Mappings |
| Modification | 2009-03-10 | CWE Content Team | MITRE | CWE 1.3, 2009-03-10 | updated Description, Name |
| Modification | 2009-10-29 | CWE Content Team | MITRE | CWE 1.6, 2009-10-29 | updated Background_Details, Other_Notes |
| Modification | 2010-09-27 | CWE Content Team | MITRE | CWE 1.10, 2010-09-27 | updated Description |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Description |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences, Relationships, Taxonomy_Mappings |
| Modification | 2011-09-13 | CWE Content Team | MITRE | CWE 2.1, 2011-09-13 | updated Relationships, Taxonomy_Mappings |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Observed_Examples, References, Relationships, Taxonomy_Mappings |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Affected_Resources, Applicable_Platforms, Causal_Nature, Likelihood_of_Exploit, References, Relationships, Taxonomy_Mappings |
| Modification | 2018-03-27 | CWE Content Team | MITRE | CWE 3.1, 2018-03-27 | updated References |
| Modification | 2019-01-03 | CWE Content Team | MITRE | CWE 3.2, 2019-01-03 | updated Relationships, Taxonomy_Mappings |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Functional_Areas |
| Modification | 2026-10-28 | CWE Content Team | MITRE | CWE 5.0, 2026-10-28 | updated Common_Consequences, Description |

**Previous Entry Names:**

- Windows MS-DOS Device Names — 2008-04-11
- Failure to Handle Windows Device Names — 2009-03-10

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
