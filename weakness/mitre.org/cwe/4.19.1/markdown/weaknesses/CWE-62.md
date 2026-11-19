---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-62"
cwe_id: "CWE-62"
entry_type: weakness
name: "UNIX Hard Link"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/62.html"
---

# CWE-62: UNIX Hard Link

## Description

The product, when opening a file or directory, does not sufficiently account for when the name is associated with a hard link to a target that is outside of the intended control sphere. This could allow an attacker to cause the product to operate on unauthorized files.

## Extended Description

Failure for a system to check for hard links can result in vulnerability to different types of attacks. For example, an attacker can escalate their privileges if a file used by a privileged program is replaced with a hard link to a sensitive file (e.g. /etc/passwd). When the process opens the file, the attacker can assume the privileges of that process.

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
| Operating System | Unix | Undetermined |
| Technology | Not Technology-Specific | Undetermined |

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact |
| --- | --- |
| Confidentiality<br>Integrity | Read Files or Directories<br>Modify Files or Directories |

## Potential Mitigations

- **Phase:** Architecture and Design · **Strategy:** Separation of Privilege · **ID:** MIT-48.1

  Follow the principle of least privilege when assigning access rights to entities in a software system.

  Denying access to a file can prevent an attacker from replacing that file with a link to a sensitive file. Ensure good compartmentalization in the system to provide protected areas that can be trusted.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2001-1494](https://www.cve.org/CVERecord?id=CVE-2001-1494) | Hard link attack, file overwrite; interesting because program checks against soft links |
| [CVE-2002-0793](https://www.cve.org/CVERecord?id=CVE-2002-0793) | Hard link and possibly symbolic link following vulnerabilities in embedded operating system allow local users to overwrite arbitrary files. |
| [CVE-2003-0578](https://www.cve.org/CVERecord?id=CVE-2003-0578) | Server creates hard links and unlinks files as root, which allows local users to gain privileges by deleting and overwriting arbitrary files. |
| [CVE-1999-0783](https://www.cve.org/CVERecord?id=CVE-1999-0783) | Operating system allows local users to conduct a denial of service by creating a hard link from a device special file to a file on an NFS file system. |
| [CVE-2004-1603](https://www.cve.org/CVERecord?id=CVE-2004-1603) | Web hosting manager follows hard links, which allows local users to read or modify arbitrary files. |
| [CVE-2004-1901](https://www.cve.org/CVERecord?id=CVE-2004-1901) | Package listing system allows local users to overwrite arbitrary files via a hard link attack on the lockfiles. |
| [CVE-2005-0342](https://www.cve.org/CVERecord?id=CVE-2005-0342) | The Finder in Mac OS X and earlier allows local users to overwrite arbitrary files and gain privileges by creating a hard link from the .DS_Store file to an arbitrary file. |
| [CVE-2005-1111](https://www.cve.org/CVERecord?id=CVE-2005-1111) | Hard link race condition |
| [CVE-2021-21272](https://www.cve.org/CVERecord?id=CVE-2021-21272) | "Zip Slip" vulnerability in Go-based Open Container Initiative (OCI) registries product allows writing arbitrary files outside intended directory via symbolic links or hard links in a gzipped tarball. |
| [CVE-2003-1366](https://www.cve.org/CVERecord?id=CVE-2003-1366) | setuid root tool allows attackers to read secret data by replacing a temp file with a hard link to a sensitive file |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | UNIX hard link |
| CERT C Secure Coding | FIO05-C | Identify files using multiple file attributes |
| Software Fault Patterns | SFP18 | Link in resource name resolution |

## References

- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 9, "Hard Links", Page 518. 1st Edition. Addison Wesley. 2006.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital |  | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Applicable_Platforms, Relationships, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2008-10-14 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2008-11-24 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2011-09-13 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Observed_Examples, References, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Applicable_Platforms, Causal_Nature, Observed_Examples, Relationships, Taxonomy_Mappings |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2022-04-28 | CWE Content Team | MITRE |  | updated Research_Gaps |
| Modification | 2022-10-13 | CWE Content Team | MITRE |  | updated Observed_Examples |
| Modification | 2023-01-31 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2023-10-26 | CWE Content Team | MITRE |  | updated Observed_Examples |
| Modification | 2024-07-16 | CWE Content Team | MITRE | CWE 4.15, 2024-07-16 | updated Observed_Examples |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Affected_Resources, Functional_Areas |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms |

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
