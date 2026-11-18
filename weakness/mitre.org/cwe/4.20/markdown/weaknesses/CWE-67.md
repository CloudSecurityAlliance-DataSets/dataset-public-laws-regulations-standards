---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-67"
cwe_id: "CWE-67"
entry_type: weakness
name: "Improper Handling of Windows Device Names"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/67.html"
---

# CWE-67: Improper Handling of Windows Device Names

## Description

The product constructs pathnames from user input, but it does not handle or incorrectly handles a pathname containing a Windows device name such as AUX or CON. This typically leads to denial of service or an information exposure when the application attempts to process the pathname as a regular file.

## Extended Description

Not properly handling virtual filenames (e.g. AUX, CON, PRN, COM1, LPT1) can result in different types of vulnerabilities. In some cases an attacker can request a device via injection of a virtual filename in a URL, which may cause an error that leads to a denial of service or an error page that reveals sensitive information. A product that allows device names to bypass filtering runs the risk of an attacker injecting malicious code in a file with the name of a device.

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

| Scope | Impact |
| --- | --- |
| Availability<br>Confidentiality<br>Other | DoS: Crash, Exit, or Restart<br>Read Application Data<br>Other |

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

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
