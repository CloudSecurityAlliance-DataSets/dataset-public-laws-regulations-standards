---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-61"
cwe_id: "CWE-61"
entry_type: weakness
name: "UNIX Symbolic Link (Symlink) Following"
abstraction: Compound
structure: Composite
status: Incomplete
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/61.html"
---

# CWE-61: UNIX Symbolic Link (Symlink) Following

## Description

The product, when opening a file or directory, does not sufficiently account for when the file is a symbolic link that resolves to a target outside of the intended control sphere. This could allow an attacker to cause the product to operate on unauthorized files.

## Alternate Terms

- **Symlink following**
- **symlink vulnerability**

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-59](../weaknesses/CWE-59.md) Improper Link Resolution Before File Access (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |
| Requires | [CWE-362](../weaknesses/CWE-362.md) Concurrent Execution using Shared Resource with Improper Synchronization (Class) | [CWE-1000](../views/CWE-1000.md) |  |
| Requires | [CWE-340](../weaknesses/CWE-340.md) Generation of Predictable Numbers or Identifiers (Class) | [CWE-1000](../views/CWE-1000.md) |  |
| Requires | [CWE-386](../weaknesses/CWE-386.md) Symbolic Name not Mapping to Correct Object (Base) | [CWE-1000](../views/CWE-1000.md) |  |
| Requires | [CWE-732](../weaknesses/CWE-732.md) Incorrect Permission Assignment for Critical Resource (Class) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Resultant**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Modes Of Introduction

- **Implementation**: These are typically reported for temporary files or privileged programs.

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Integrity | Read Files or Directories<br>Modify Files or Directories | A product that allows a symbolic link (symlink) as part of a path - whether in internal code or through user input - can allow an attacker to spoof the symbolic link and traverse the file system to unintended locations or access arbitrary files. An attacker could read, write, or /corrupt a file that they originally did not have permissions to access directly. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

## Potential Mitigations

- **Phase:** Implementation

  Symbolic link attacks often occur when a program creates a tmp directory that stores files/links. Access to the directory should be restricted to the program as to prevent attackers from manipulating the files.

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
| [CVE-2004-0689](https://www.cve.org/CVERecord?id=CVE-2004-0689) | Possible interesting example |
| [CVE-2005-1879](https://www.cve.org/CVERecord?id=CVE-2005-1879) | Second-order symlink vulnerabilities |
| [CVE-2005-1880](https://www.cve.org/CVERecord?id=CVE-2005-1880) | Second-order symlink vulnerabilities |
| [CVE-2005-1916](https://www.cve.org/CVERecord?id=CVE-2005-1916) | Symlink in Python program |
| [CVE-2000-0972](https://www.cve.org/CVERecord?id=CVE-2000-0972) | Setuid product allows file reading by replacing a file being edited with a symlink to the targeted file, leaking the result in error messages when parsing fails. |
| [CVE-2005-0824](https://www.cve.org/CVERecord?id=CVE-2005-0824) | Signal causes a dump that follows symlinks. |
| [CVE-2015-3629](https://www.cve.org/CVERecord?id=CVE-2015-3629) | A Libcontainer used in Docker Engine allows local users to escape containerization and write to an arbitrary file on the host system via a symlink attack in an image when respawning a container. |
| [CVE-2020-26277](https://www.cve.org/CVERecord?id=CVE-2020-26277) | In a MySQL database deployment tool, users may craft a maliciously packaged tarball that contains symlinks to files external to the target and once unpacked, will execute. |
| [CVE-2021-21272](https://www.cve.org/CVERecord?id=CVE-2021-21272) | "Zip Slip" vulnerability in Go-based Open Container Initiative (OCI) registries product allows writing arbitrary files outside intended directory via symbolic links or hard links in a gzipped tarball. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| PLOVER | UNIX symbolic link following |

## Related Attack Patterns

- [CAPEC-27](https://capec.mitre.org/data/definitions/27.html)

## References

- [REF-493] Steve Christey. "Second-Order Symlink Vulnerabilities". Bugtraq. 2005-06-07. <https://seclists.org/bugtraq/2005/Jun/44> (URL validated: 2023-04-07).
- [REF-494] Shaun Colley. "Crafting Symlinks for Fun and Profit". Infosec Writers Text Library. 2004-04-12. <https://web.archive.org/web/20040502153535/http://www.infosecwriters.com/texts.php?op=display&id=159> (URL validated: 2025-07-29).
- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 9, "Symbolic Link Attacks", Page 518. 1st Edition. Addison Wesley. 2006.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This is a well-known Composite of multiple weaknesses that must all occur simultaneously, although it is attack-oriented in nature.
- **Comments:** While attack-oriented composites are supported in CWE, they have not been a focus of research. There is a chance that future research or CWE scope clarifications will change or deprecate them. Perform root-cause analysis to determine which weaknesses allow symlink following to occur, and map to those weaknesses. For example, predictable file names might be intended functionality, but creation in a directory with insecure permissions might not.
- **Reasons:** Other

## Notes

- **Research Gap**:

  Symlink vulnerabilities are regularly found in C and shell programs, but all programming languages can have this problem. Even shell programs are probably under-reported.

  "Second-order symlink vulnerabilities" may exist in programs that invoke other programs that follow symlinks. They are rarely reported but are likely to be fairly common when process invocation is used [REF-493].

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, Observed_Example, Other_Notes, Research_Gaps, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2008-10-14 | CWE Content Team | MITRE | CWE 1.0.1, 2008-10-14 | updated Description |
| Modification | 2009-07-27 | CWE Content Team | MITRE | CWE 1.5, 2009-07-27 | updated Observed_Examples |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Observed_Examples, References |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2014-06-23 | CWE Content Team | MITRE | CWE 2.7, 2014-06-23 | updated Modes_of_Introduction, Other_Notes |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Applicable_Platforms, Causal_Nature, Likelihood_of_Exploit, References, Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Relationships |
| Modification | 2022-04-28 | CWE Content Team | MITRE | CWE 4.7, 2022-04-28 | updated Research_Gaps |
| Modification | 2022-10-13 | CWE Content Team | MITRE | CWE 4.9, 2022-10-13 | updated Observed_Examples |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated References, Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Affected_Resources, Functional_Areas, References |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Detection_Factors, Relationships |
| Modification | 2026-10-28 | CWE Content Team | MITRE | CWE 5.0, 2026-10-28 | updated Common_Consequences, Description |

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
