---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-59"
cwe_id: "CWE-59"
entry_type: weakness
name: "Improper Link Resolution Before File Access ('Link Following')"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/59.html"
---

# CWE-59: Improper Link Resolution Before File Access ('Link Following')

## Description

The product attempts to access a file based on the filename, but it does not properly prevent that filename from identifying a link or shortcut that resolves to an unintended resource.

## Alternate Terms

- **insecure temporary file**: Some people use the phrase "insecure temporary file" when referring to a link following weakness, but other weaknesses can produce insecure temporary files without any symlink involvement at all.
- **Zip Slip**: "Zip slip" is an attack that uses file archives (e.g., ZIP, tar, rar, etc.) that contain filenames with path traversal sequences that cause the files to be written outside of the directory under which the archive is expected to be extracted [REF-1282]. It is most commonly used for relative path traversal (CWE-23) and link following (CWE-59).

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-706](../weaknesses/CWE-706.md) Use of Incorrectly-Resolved Name or Reference (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-706](../weaknesses/CWE-706.md) Use of Incorrectly-Resolved Name or Reference (Class) | [CWE-1003](../views/CWE-1003.md) | Primary |

## Weakness Ordinalities

- **Resultant**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |
| Operating System | Windows | Sometimes |
| Operating System | Unix | Often |
| Technology | Not Technology-Specific | Undetermined |

## Background Details

Soft links are a UNIX term that is synonymous with simple shortcuts on Windows-based platforms.

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Likelihood Of Exploit

Medium

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Integrity<br>Access Control | Read Files or Directories<br>Modify Files or Directories<br>Bypass Protection Mechanism | An attacker may be able to traverse the file system to unintended locations and read or overwrite the contents of unexpected files. If the files are used for a security mechanism then an attacker may be able to bypass the mechanism. |
| Other | Execute Unauthorized Code or Commands | Windows simple shortcuts, sometimes referred to as soft links, can be exploited remotely since a ".LNK" file can be uploaded like a normal file. This can enable remote execution. |

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

## Potential Mitigations

- **Phase:** Architecture and Design · **Strategy:** Separation of Privilege · **ID:** MIT-48.1

  Follow the principle of least privilege when assigning access rights to entities in a software system.

  Denying access to a file can prevent an attacker from replacing that file with a link to a sensitive file. Ensure good compartmentalization in the system to provide protected areas that can be trusted.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-1999-1386](https://www.cve.org/CVERecord?id=CVE-1999-1386) | Some versions of Perl follow symbolic links when running with the -e option, which allows local users to overwrite arbitrary files via a symlink attack. |
| [CVE-2000-1178](https://www.cve.org/CVERecord?id=CVE-2000-1178) | Text editor follows symbolic links when creating a rescue copy during an abnormal exit, which allows local users to overwrite the files of other users. |
| [CVE-2004-0217](https://www.cve.org/CVERecord?id=CVE-2004-0217) | Antivirus update allows local users to create or append to arbitrary files via a symlink attack on a logfile. |
| [CVE-2003-0517](https://www.cve.org/CVERecord?id=CVE-2003-0517) | Symlink attack allows local users to overwrite files. |
| [CVE-2004-0689](https://www.cve.org/CVERecord?id=CVE-2004-0689) | Window manager does not properly handle when certain symbolic links point to "stale" locations, which could allow local users to create or truncate arbitrary files. |
| [CVE-2005-1879](https://www.cve.org/CVERecord?id=CVE-2005-1879) | Second-order symlink vulnerabilities |
| [CVE-2005-1880](https://www.cve.org/CVERecord?id=CVE-2005-1880) | Second-order symlink vulnerabilities |
| [CVE-2005-1916](https://www.cve.org/CVERecord?id=CVE-2005-1916) | Symlink in Python program |
| [CVE-2000-0972](https://www.cve.org/CVERecord?id=CVE-2000-0972) | Setuid product allows file reading by replacing a file being edited with a symlink to the targeted file, leaking the result in error messages when parsing fails. |
| [CVE-2005-0824](https://www.cve.org/CVERecord?id=CVE-2005-0824) | Signal causes a dump that follows symlinks. |
| [CVE-2001-1494](https://www.cve.org/CVERecord?id=CVE-2001-1494) | Hard link attack, file overwrite; interesting because program checks against soft links |
| [CVE-2002-0793](https://www.cve.org/CVERecord?id=CVE-2002-0793) | Hard link and possibly symbolic link following vulnerabilities in embedded operating system allow local users to overwrite arbitrary files. |
| [CVE-2003-0578](https://www.cve.org/CVERecord?id=CVE-2003-0578) | Server creates hard links and unlinks files as root, which allows local users to gain privileges by deleting and overwriting arbitrary files. |
| [CVE-1999-0783](https://www.cve.org/CVERecord?id=CVE-1999-0783) | Operating system allows local users to conduct a denial of service by creating a hard link from a device special file to a file on an NFS file system. |
| [CVE-2004-1603](https://www.cve.org/CVERecord?id=CVE-2004-1603) | Web hosting manager follows hard links, which allows local users to read or modify arbitrary files. |
| [CVE-2004-1901](https://www.cve.org/CVERecord?id=CVE-2004-1901) | Package listing system allows local users to overwrite arbitrary files via a hard link attack on the lockfiles. |
| [CVE-2005-1111](https://www.cve.org/CVERecord?id=CVE-2005-1111) | Hard link race condition |
| [CVE-2000-0342](https://www.cve.org/CVERecord?id=CVE-2000-0342) | Mail client allows remote attackers to bypass the user warning for executable attachments such as .exe, .com, and .bat by using a .lnk file that refers to the attachment, aka "Stealth Attachment." |
| [CVE-2001-1042](https://www.cve.org/CVERecord?id=CVE-2001-1042) | FTP server allows remote attackers to read arbitrary files and directories by uploading a .lnk (link) file that points to the target file. |
| [CVE-2001-1043](https://www.cve.org/CVERecord?id=CVE-2001-1043) | FTP server allows remote attackers to read arbitrary files and directories by uploading a .lnk (link) file that points to the target file. |
| [CVE-2005-0587](https://www.cve.org/CVERecord?id=CVE-2005-0587) | Browser allows remote malicious web sites to overwrite arbitrary files by tricking the user into downloading a .LNK (link) file twice, which overwrites the file that was referenced in the first .LNK file. |
| [CVE-2001-1386](https://www.cve.org/CVERecord?id=CVE-2001-1386) | ".LNK." - .LNK with trailing dot |
| [CVE-2003-1233](https://www.cve.org/CVERecord?id=CVE-2003-1233) | Rootkits can bypass file access restrictions to Windows kernel directories using NtCreateSymbolicLinkObject function to create symbolic link |
| [CVE-2002-0725](https://www.cve.org/CVERecord?id=CVE-2002-0725) | File system allows local attackers to hide file usage activities via a hard link to the target file, which causes the link to be recorded in the audit trail instead of the target file. |
| [CVE-2003-0844](https://www.cve.org/CVERecord?id=CVE-2003-0844) | Web server plugin allows local users to overwrite arbitrary files via a symlink attack on predictable temporary filenames. |
| [CVE-2015-3629](https://www.cve.org/CVERecord?id=CVE-2015-3629) | A Libcontainer used in Docker Engine allows local users to escape containerization and write to an arbitrary file on the host system via a symlink attack in an image when respawning a container. |
| [CVE-2021-21272](https://www.cve.org/CVERecord?id=CVE-2021-21272) | "Zip Slip" vulnerability in Go-based Open Container Initiative (OCI) registries product allows writing arbitrary files outside intended directory via symbolic links or hard links in a gzipped tarball. |
| [CVE-2020-27833](https://www.cve.org/CVERecord?id=CVE-2020-27833) | "Zip Slip" vulnerability in container management product allows writing arbitrary files outside intended directory via a container image (.tar format) with filenames that are symbolic links that point to other files within the same tar file; however, the files being pointed to can also be symbolic links to destinations outside the intended directory, bypassing the initial check. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| PLOVER |  | Link Following |  |
| CERT C Secure Coding | FIO02-C | Canonicalize path names originating from untrusted sources |  |
| CERT C Secure Coding | POS01-C | Check for the existence of links when dealing with files |  |
| SEI CERT Perl Coding Standard | FIO01-PL | Do not operate on files that can be modified by untrusted users | CWE More Specific |
| Software Fault Patterns | SFP18 | Link in resource name resolution |  |

## Related Attack Patterns

- [CAPEC-132](https://capec.mitre.org/data/definitions/132.html)
- [CAPEC-17](https://capec.mitre.org/data/definitions/17.html)
- [CAPEC-35](https://capec.mitre.org/data/definitions/35.html)
- [CAPEC-76](https://capec.mitre.org/data/definitions/76.html)

## References

- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 9, "Symbolic Link Attacks", Page 518. 1st Edition. Addison Wesley. 2006.
- [REF-1282] Snyk. "Zip Slip Vulnerability". 2018-06-05. <https://security.snyk.io/research/zip-slip-vulnerability>.
- [REF-1479] Gregory Larsen, E. Kenneth Hong Fong, David A. Wheeler and Rama S. Moorthy. "State-of-the-Art Resources (SOAR) for Software Vulnerability Detection, Test, and Evaluation". 2014-07. <https://www.ida.org/-/media/feature/publications/s/st/stateoftheart-resources-soar-for-software-vulnerability-detection-test-and-evaluation/p-5061.ashx> (URL validated: 2025-09-05).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Theoretical**:

  Link following vulnerabilities are Multi-factor Vulnerabilities (MFV). They are the combination of multiple elements: file or directory permissions, filename predictability, race conditions, and in some cases, a design limitation in which there is no mechanism for performing atomic file creation operations.

  Some potential factors are race conditions, permissions, and predictability.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital |  | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Alternate_Terms, Applicable_Platforms, Relationships, Other_Notes, Relationship_Notes, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2008-11-24 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2009-01-12 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2009-05-27 | CWE Content Team | MITRE |  | updated Description, Name |
| Modification | 2009-10-29 | CWE Content Team | MITRE |  | updated Background_Details, Other_Notes |
| Modification | 2010-02-16 | CWE Content Team | MITRE |  | updated Potential_Mitigations, Relationships |
| Modification | 2010-04-05 | CWE Content Team | MITRE |  | updated Related_Attack_Patterns |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2011-09-13 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Common_Consequences, Observed_Examples, References, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2014-06-23 | CWE Content Team | MITRE |  | updated Common_Consequences, Other_Notes |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Detection_Factors, Relationships, Taxonomy_Mappings |
| Modification | 2015-12-07 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Affected_Resources, Applicable_Platforms, Causal_Nature, Common_Consequences, Functional_Areas, Likelihood_of_Exploit, Modes_of_Introduction, Relationships, Taxonomy_Mappings |
| Modification | 2019-01-03 | CWE Content Team | MITRE |  | updated Taxonomy_Mappings |
| Modification | 2019-06-20 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2021-03-15 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2021-10-28 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2022-04-28 | CWE Content Team | MITRE |  | updated Research_Gaps |
| Modification | 2022-06-28 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2022-10-13 | CWE Content Team | MITRE |  | updated Alternate_Terms, Background_Details, Observed_Examples, References, Relationship_Notes, Theoretical_Notes |
| Modification | 2023-01-31 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Detection_Factors, References |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms, Relationships |

**Previous Entry Names:**

- Link Following — 2008-04-11
- Failure to Resolve Links Before File Access (aka 'Link Following') — 2009-05-27

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
