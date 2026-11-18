---
secid: "secid:weakness/mitre.org/cwe@4.21#CWE-73"
cwe_id: "CWE-73"
entry_type: weakness
name: "External Control of File Name or Path"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.21"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/73.html"
---

# CWE-73: External Control of File Name or Path

## Description

The product allows user input to control or influence paths or file names that are used in filesystem operations.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-642](../weaknesses/CWE-642.md) External Control of Critical State Data (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-610](../weaknesses/CWE-610.md) Externally Controlled Reference to a Resource in Another Sphere (Class) | [CWE-1000](../views/CWE-1000.md) |  |
| ChildOf | [CWE-20](../weaknesses/CWE-20.md) Improper Input Validation (Class) | [CWE-700](../views/CWE-700.md) | Primary |
| CanPrecede | [CWE-22](../weaknesses/CWE-22.md) Improper Limitation of a Pathname to a Restricted Directory (Base) | [CWE-1000](../views/CWE-1000.md) |  |
| CanPrecede | [CWE-41](../weaknesses/CWE-41.md) Improper Resolution of Path Equivalence (Base) | [CWE-1000](../views/CWE-1000.md) |  |
| CanPrecede | [CWE-98](../weaknesses/CWE-98.md) Improper Control of Filename for Include/Require Statement in PHP Program (Variant) | [CWE-1000](../views/CWE-1000.md) |  |
| CanPrecede | [CWE-434](../weaknesses/CWE-434.md) Unrestricted Upload of File with Dangerous Type (Base) | [CWE-1000](../views/CWE-1000.md) |  |
| CanPrecede | [CWE-59](../weaknesses/CWE-59.md) Improper Link Resolution Before File Access (Base) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |
| Operating System | Unix | Often |
| Operating System | Windows | Often |
| Operating System | macOS | Often |

## Modes Of Introduction

- **Architecture and Design**

- **Implementation**:

  Path manipulation errors occur when the following two conditions are met:

  1. An attacker can specify a path used in an operation on the filesystem.
  2. By specifying the resource, the attacker gains a capability that would not otherwise be permitted.

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Integrity<br>Confidentiality | Read Files or Directories | The application can operate on unexpected files, such as system files or configuration files. Confidentiality is violated when the targeted filename is not directly readable by the attacker. |
| Integrity<br>Confidentiality<br>Availability | Modify Files or Directories<br>Execute Unauthorized Code or Commands | The application can operate on unexpected files. This may violate integrity if the filename is written to, or if the filename is for a program or other form of executable code. |
| Availability | DoS: Crash, Exit, or Restart<br>DoS: Resource Consumption (Other) | The application can operate on unexpected files. Availability can be violated if the attacker specifies an unexpected file that the application modifies. Availability can also be affected if the attacker specifies a filename for a large file, or points to a special device or a file that does not have the format that the application expects. |

## Detection Methods

- **Method:** Automated Static Analysis

  The external control or influence of filenames can often be detected using automated static analysis that models data flow within the product.

  Automated static analysis might not be able to recognize when proper input validation is being performed, leading to false positives - i.e., warnings that do not have any security consequences or require any code changes.

## Potential Mitigations

- **Phase:** Architecture and Design

  When the set of filenames is limited or known, create a mapping from a set of fixed input values (such as numeric IDs) to the actual filenames, and reject all other inputs. For example, ID 1 could map to "inbox.txt" and ID 2 could map to "profile.txt". Features such as the ESAPI AccessReferenceMap provide this capability.

- **Phase:** Architecture and Design; Operation

  Run your code in a "jail" or similar sandbox environment that enforces strict boundaries between the process and the operating system. This may effectively restrict all access to files within a particular directory.

  Examples include the Unix chroot jail and AppArmor. In general, managed code may provide some protection.

  This may not be a feasible solution, and it only limits the impact to the operating system; the rest of your application may still be subject to compromise.

  Be careful to avoid CWE-243 and other weaknesses related to jails.

- **Phase:** Architecture and Design

  For any security checks that are performed on the client side, ensure that these checks are duplicated on the server side, in order to avoid CWE-602. Attackers can bypass the client-side checks by modifying values after the checks have been performed, or by changing the client to remove the client-side checks entirely. Then, these modified values would be submitted to the server.

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5.1

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

  When validating filenames, use stringent allowlists that limit the character set to be used. If feasible, only allow a single "." character in the filename to avoid weaknesses such as CWE-23, and exclude directory separators such as "/" to avoid CWE-36. Use a list of allowable file extensions, which will help to avoid CWE-434.

  Do not rely exclusively on a filtering mechanism that removes potentially dangerous characters. This is equivalent to a denylist, which may be incomplete (CWE-184). For example, filtering "/" is insufficient protection if the filesystem also supports the use of "\\" as a directory separator. Another possible error could occur when the filtering is applied in a way that still produces dangerous data (CWE-182). For example, if "../" sequences are removed from the ".../...//" string in a sequential fashion, two instances of "../" would be removed from the original string, but the remaining characters would still form the "../" string.

  **Effectiveness:** High

- **Phase:** Implementation

  Use a built-in path canonicalization function (such as realpath() in C) that produces the canonical version of the pathname, which effectively removes ".." sequences and symbolic links (CWE-23, CWE-59).

- **Phase:** Installation; Operation

  Use OS-level permissions and run as a low-privileged user to limit the scope of any successful attack.

- **Phase:** Operation; Implementation

  If you are using PHP, configure your application so that it does not use register_globals. During implementation, develop your application so that it does not rely on this feature, but be wary of implementing a register_globals emulation that is subject to weaknesses such as CWE-95, CWE-621, and similar issues.

- **Phase:** Testing

  Use tools and techniques that require manual (human) analysis, such as penetration testing, threat modeling, and interactive tools that allow the tester to record and modify an active session. These may be more effective than strictly automated techniques. This is especially the case with weaknesses that are related to design and business rules.

## Demonstrative Examples

### Example 1 (DX-65)

The following code uses input from an HTTP request to create a file name. The programmer has not considered the possibility that an attacker could provide a file name such as "../../tomcat/conf/server.xml", which causes the application to delete one of its own configuration files (CWE-22).

*Example (Bad, Java):*

```java
String rName = request.getParameter("reportName");
File rFile = new File("/usr/local/apfr/reports/" + rName);
...
rFile.delete();
```

### Example 2 (DX-66)

The following code uses input from a configuration file to determine which file to open and echo back to the user. If the program runs with privileges and malicious users can change the configuration file, they can use the program to read any file on the system that ends with the extension .txt.

*Example (Bad, Java):*

```java
fis = new FileInputStream(cfg.getProperty("sub")+".txt");
amt = fis.read(arr);
out.println(arr);
```

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2022-45918](https://www.cve.org/CVERecord?id=CVE-2022-45918) | Chain: a learning management tool debugger uses external input to locate previous session logs (CWE-73) and does not properly validate the given path (CWE-20), allowing for filesystem path traversal using "../" sequences (CWE-24) |
| [CVE-2008-5748](https://www.cve.org/CVERecord?id=CVE-2008-5748) | Chain: external control of values for user's desired language and theme enables path traversal. |
| [CVE-2008-5764](https://www.cve.org/CVERecord?id=CVE-2008-5764) | Chain: external control of user's target language enables remote file inclusion. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| 7 Pernicious Kingdoms |  | Path Manipulation |
| Software Fault Patterns | SFP16 | Path Traversal |

## Related Attack Patterns

- [CAPEC-13](https://capec.mitre.org/data/definitions/13.html)
- [CAPEC-267](https://capec.mitre.org/data/definitions/267.html)
- [CAPEC-64](https://capec.mitre.org/data/definitions/64.html)
- [CAPEC-72](https://capec.mitre.org/data/definitions/72.html)
- [CAPEC-76](https://capec.mitre.org/data/definitions/76.html)
- [CAPEC-78](https://capec.mitre.org/data/definitions/78.html)
- [CAPEC-79](https://capec.mitre.org/data/definitions/79.html)
- [CAPEC-80](https://capec.mitre.org/data/definitions/80.html)

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://cwe.mitre.org/documents/sources/SevenPerniciousKingdoms.pdf>.
- [REF-45] OWASP. "OWASP Enterprise Security API (ESAPI) Project". <https://owasp.org/www-project-enterprise-security-api/> (URL validated: 2025-07-24).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Maintenance**: CWE-114 is a Class, but it is listed a child of CWE-73 in view 1000. This suggests some abstraction problems that should be resolved in future versions.

- **Relationship**:

  The external control of filenames can be the primary link in chains with other file-related weaknesses, as seen in the CanPrecede relationships. This is because software systems use files for many different purposes: to execute programs, load code libraries, to store application data, to store configuration settings, record temporary data, act as signals or semaphores to other processes, etc.

  However, those weaknesses do not always require external control. For example, link-following weaknesses (CWE-59) often involve pathnames that are not controllable by the attacker at all.

  The external control can be resultant from other issues. For example, in PHP applications, the register_globals setting can allow an attacker to modify variables that the programmer thought were immutable, enabling file inclusion (CWE-98) and path traversal (CWE-22). Operating with excessive privileges (CWE-250) might allow an attacker to specify an input filename that is not directly readable by the attacker, but is accessible to the privileged program. A buffer overflow (CWE-119) might give an attacker control over nearby memory locations that are related to pathnames, but were not directly modifiable by the attacker.

---
Generated from MITRE's CWE 4.21 XML (cwec_v4.21.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.21/LICENSE.txt).
