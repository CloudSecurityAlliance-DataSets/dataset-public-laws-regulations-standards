---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-64"
cwe_id: "CWE-64"
entry_type: weakness
name: "Windows Shortcut Following (.LNK)"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/64.html"
---

# CWE-64: Windows Shortcut Following (.LNK)

## Description

The product, when opening a file or directory, does not sufficiently handle when the file is a Windows shortcut (.LNK) whose target is outside of the intended control sphere. This could allow an attacker to cause the product to operate on unauthorized files.

## Alternate Terms

- **Windows symbolic link following**
- **symlink**

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-59](../weaknesses/CWE-59.md) Improper Link Resolution Before File Access ('Link Following') (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Resultant**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |
| Operating System | Windows | Undetermined |
| Technology | Not Technology-Specific | Undetermined |

## Modes Of Introduction

- **Operation**

## Likelihood Of Exploit

Low

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Integrity | Read Files or Directories<br>Modify Files or Directories | The shortcut (file with the .lnk extension) can permit an attacker to read/write a file that they originally did not have permissions to access. |

## Potential Mitigations

- **Phase:** Architecture and Design · **Strategy:** Separation of Privilege · **ID:** MIT-48.1

  Follow the principle of least privilege when assigning access rights to entities in a software system.

  Denying access to a file can prevent an attacker from replacing that file with a link to a sensitive file. Ensure good compartmentalization in the system to provide protected areas that can be trusted.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2019-19793](https://www.cve.org/CVERecord?id=CVE-2019-19793) | network access control service executes program with high privileges and allows symlink to invoke another executable or perform DLL injection. |
| [CVE-2000-0342](https://www.cve.org/CVERecord?id=CVE-2000-0342) | Mail client allows remote attackers to bypass the user warning for executable attachments such as .exe, .com, and .bat by using a .lnk file that refers to the attachment, aka "Stealth Attachment." |
| [CVE-2001-1042](https://www.cve.org/CVERecord?id=CVE-2001-1042) | FTP server allows remote attackers to read arbitrary files and directories by uploading a .lnk (link) file that points to the target file. |
| [CVE-2001-1043](https://www.cve.org/CVERecord?id=CVE-2001-1043) | FTP server allows remote attackers to read arbitrary files and directories by uploading a .lnk (link) file that points to the target file. |
| [CVE-2005-0587](https://www.cve.org/CVERecord?id=CVE-2005-0587) | Browser allows remote malicious web sites to overwrite arbitrary files by tricking the user into downloading a .LNK (link) file twice, which overwrites the file that was referenced in the first .LNK file. |
| [CVE-2001-1386](https://www.cve.org/CVERecord?id=CVE-2001-1386) | ".LNK." - .LNK with trailing dot |
| [CVE-2003-1233](https://www.cve.org/CVERecord?id=CVE-2003-1233) | Rootkits can bypass file access restrictions to Windows kernel directories using NtCreateSymbolicLinkObject function to create symbolic link |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | Windows Shortcut Following (.LNK) |
| CERT C Secure Coding | FIO05-C | Identify files using multiple file attributes |
| Software Fault Patterns | SFP18 | Link in resource name resolution |

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Research Gap**: Under-studied. Windows .LNK files are more "portable" than Unix symlinks and have been used in remote exploits. Some Windows API's will access LNK's as if they are regular files, so one would expect that they would be reported more frequently.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Applicable_Platforms, Relationships, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2008-10-14 | CWE Content Team | MITRE | CWE 1.0.1, 2008-10-14 | updated Description |
| Modification | 2008-11-24 | CWE Content Team | MITRE | CWE 1.1, 2008-11-25 | updated Relationships, Taxonomy_Mappings |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2011-09-13 | CWE Content Team | MITRE | CWE 2.1, 2011-09-13 | updated Relationships, Taxonomy_Mappings |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Observed_Examples, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Applicable_Platforms, Causal_Nature, Likelihood_of_Exploit, Relationships, Taxonomy_Mappings |
| Modification | 2019-01-03 | CWE Content Team | MITRE | CWE 3.2, 2019-01-03 | updated Related_Attack_Patterns |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Related_Attack_Patterns |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Relationships |
| Modification | 2022-06-28 | CWE Content Team | MITRE | CWE 4.8, 2022-06-28 | updated Observed_Examples |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Affected_Resources, Functional_Areas |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms, Common_Consequences, Description |

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
