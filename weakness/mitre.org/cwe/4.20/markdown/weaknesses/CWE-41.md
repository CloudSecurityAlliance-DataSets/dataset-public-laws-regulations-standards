---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-41"
cwe_id: "CWE-41"
entry_type: weakness
name: "Improper Resolution of Path Equivalence"
abstraction: Base
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/41.html"
---

# CWE-41: Improper Resolution of Path Equivalence

## Description

The product is vulnerable to file system contents disclosure through path equivalence. Path equivalence involves the use of special characters in file and directory names. The associated manipulations are intended to generate multiple names for the same object.

## Extended Description

Path equivalence is usually employed in order to circumvent access controls expressed using an incomplete set of file name or file path representations. This is different from path traversal, wherein the manipulations are performed to generate a name for a different object.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-706](../weaknesses/CWE-706.md) Use of Incorrectly-Resolved Name or Reference (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-863](../weaknesses/CWE-863.md) Incorrect Authorization (Class) | [CWE-1000](../views/CWE-1000.md) |  |
| ChildOf | [CWE-1390](../weaknesses/CWE-1390.md) Weak Authentication (Class) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Integrity<br>Access Control | Read Files or Directories<br>Modify Files or Directories<br>Bypass Protection Mechanism | An attacker may be able to traverse the file system to unintended locations and read or overwrite the contents of unexpected files. If the files are used for a security mechanism than an attacker may be able to bypass the mechanism. |

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

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

- **Phase:** Implementation · **Strategy:** Output Encoding · **ID:** MIT-30

  Use and specify an output encoding that can be handled by the downstream component that is reading the output. Common encodings include ISO-8859-1, UTF-7, and UTF-8. When an encoding is not specified, a downstream component may choose a different encoding, either by assuming a default encoding or automatically inferring which encoding is being used, which can be erroneous. When the encodings are inconsistent, the downstream component might treat some character or byte sequences as special, even if they are not special in the original encoding. Attackers might then be able to exploit this discrepancy and conduct injection attacks; they even might be able to bypass protection mechanisms that assume the original encoding is also being used by the downstream component.

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-20

  Inputs should be decoded and canonicalized to the application's current internal representation before being validated (CWE-180). Make sure that the application does not decode the same input twice (CWE-174). Such errors could be used to bypass allowlist validation schemes by introducing dangerous inputs after they have been checked.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2000-1114](https://www.cve.org/CVERecord?id=CVE-2000-1114) | Source code disclosure using trailing dot |
| [CVE-2002-1986](https://www.cve.org/CVERecord?id=CVE-2002-1986) | Source code disclosure using trailing dot |
| [CVE-2004-2213](https://www.cve.org/CVERecord?id=CVE-2004-2213) | Source code disclosure using trailing dot or trailing encoding space "%20" |
| [CVE-2005-3293](https://www.cve.org/CVERecord?id=CVE-2005-3293) | Source code disclosure using trailing dot |
| [CVE-2004-0061](https://www.cve.org/CVERecord?id=CVE-2004-0061) | Bypass directory access restrictions using trailing dot in URL |
| [CVE-2000-1133](https://www.cve.org/CVERecord?id=CVE-2000-1133) | Bypass directory access restrictions using trailing dot in URL |
| [CVE-2001-1386](https://www.cve.org/CVERecord?id=CVE-2001-1386) | Bypass check for ".lnk" extension using ".lnk." |
| [CVE-2001-0693](https://www.cve.org/CVERecord?id=CVE-2001-0693) | Source disclosure via trailing encoded space "%20" |
| [CVE-2001-0778](https://www.cve.org/CVERecord?id=CVE-2001-0778) | Source disclosure via trailing encoded space "%20" |
| [CVE-2001-1248](https://www.cve.org/CVERecord?id=CVE-2001-1248) | Source disclosure via trailing encoded space "%20" |
| [CVE-2004-0280](https://www.cve.org/CVERecord?id=CVE-2004-0280) | Source disclosure via trailing encoded space "%20" |
| [CVE-2005-0622](https://www.cve.org/CVERecord?id=CVE-2005-0622) | Source disclosure via trailing encoded space "%20" |
| [CVE-2005-1656](https://www.cve.org/CVERecord?id=CVE-2005-1656) | Source disclosure via trailing encoded space "%20" |
| [CVE-2002-1603](https://www.cve.org/CVERecord?id=CVE-2002-1603) | Source disclosure via trailing encoded space "%20" |
| [CVE-2001-0054](https://www.cve.org/CVERecord?id=CVE-2001-0054) | Multi-Factor Vulnerability (MFV). directory traversal and other issues in FTP server using Web encodings such as "%20"; certain manipulations have unusual side effects. |
| [CVE-2002-1451](https://www.cve.org/CVERecord?id=CVE-2002-1451) | Trailing space ("+" in query string) leads to source code disclosure. |
| [CVE-2000-0293](https://www.cve.org/CVERecord?id=CVE-2000-0293) | Filenames with spaces allow arbitrary file deletion when the product does not properly quote them; some overlap with path traversal. |
| [CVE-2001-1567](https://www.cve.org/CVERecord?id=CVE-2001-1567) | "+" characters in query string converted to spaces before sensitive file/extension (internal space), leading to bypass of access restrictions to the file. |
| [CVE-2002-0253](https://www.cve.org/CVERecord?id=CVE-2002-0253) | Overlaps infoleak |
| [CVE-2001-0446](https://www.cve.org/CVERecord?id=CVE-2001-0446) | Application server allows remote attackers to read source code for .jsp files by appending a / to the requested URL. |
| [CVE-2004-0334](https://www.cve.org/CVERecord?id=CVE-2004-0334) | Bypass Basic Authentication for files using trailing "/" |
| [CVE-2001-0893](https://www.cve.org/CVERecord?id=CVE-2001-0893) | Read sensitive files with trailing "/" |
| [CVE-2001-0892](https://www.cve.org/CVERecord?id=CVE-2001-0892) | Web server allows remote attackers to view sensitive files under the document root (such as .htpasswd) via a GET request with a trailing /. |
| [CVE-2004-1814](https://www.cve.org/CVERecord?id=CVE-2004-1814) | Directory traversal vulnerability in server allows remote attackers to read protected files via .. (dot dot) sequences in an HTTP request. |
| [CVE-2002-1483](https://www.cve.org/CVERecord?id=CVE-2002-1483) | Read files with full pathname using multiple internal slash. |
| [CVE-1999-1456](https://www.cve.org/CVERecord?id=CVE-1999-1456) | Server allows remote attackers to read arbitrary files via a GET request with more than one leading / (slash) character in the filename. |
| [CVE-2004-0578](https://www.cve.org/CVERecord?id=CVE-2004-0578) | Server allows remote attackers to read arbitrary files via leading slash (//) characters in a URL request. |
| [CVE-2002-0275](https://www.cve.org/CVERecord?id=CVE-2002-0275) | Server allows remote attackers to bypass authentication and read restricted files via an extra / (slash) in the requested URL. |
| [CVE-2004-1032](https://www.cve.org/CVERecord?id=CVE-2004-1032) | Product allows local users to delete arbitrary files or create arbitrary empty files via a target filename with a large number of leading slash (/) characters. |
| [CVE-2002-1238](https://www.cve.org/CVERecord?id=CVE-2002-1238) | Server allows remote attackers to bypass access restrictions for files via an HTTP request with a sequence of multiple / (slash) characters such as http://www.example.com///file/. |
| [CVE-2004-1878](https://www.cve.org/CVERecord?id=CVE-2004-1878) | Product allows remote attackers to bypass authentication, obtain sensitive information, or gain access via a direct request to admin/user.pl preceded by // (double leading slash). |
| [CVE-2005-1365](https://www.cve.org/CVERecord?id=CVE-2005-1365) | Server allows remote attackers to execute arbitrary commands via a URL with multiple leading "/" (slash) characters and ".." sequences. |
| [CVE-2000-1050](https://www.cve.org/CVERecord?id=CVE-2000-1050) | Access directory using multiple leading slash. |
| [CVE-2001-1072](https://www.cve.org/CVERecord?id=CVE-2001-1072) | Bypass access restrictions via multiple leading slash, which causes a regular expression to fail. |
| [CVE-2004-0235](https://www.cve.org/CVERecord?id=CVE-2004-0235) | Archive extracts to arbitrary files using multiple leading slash in filenames in the archive. |
| [CVE-2002-1078](https://www.cve.org/CVERecord?id=CVE-2002-1078) | Directory listings in web server using multiple trailing slash |
| [CVE-2004-0847](https://www.cve.org/CVERecord?id=CVE-2004-0847) | web framework for .NET allows remote attackers to bypass authentication for .aspx files in restricted directories via a request containing a (1) "\\" (backslash) or (2) "%5C" (encoded backslash) |
| [CVE-2000-0004](https://www.cve.org/CVERecord?id=CVE-2000-0004) | Server allows remote attackers to read source code for executable files by inserting a . (dot) into the URL. |
| [CVE-2002-0304](https://www.cve.org/CVERecord?id=CVE-2002-0304) | Server allows remote attackers to read password-protected files via a /./ in the HTTP request. |
| [CVE-1999-1083](https://www.cve.org/CVERecord?id=CVE-1999-1083) | Possibly (could be a cleansing error) |
| [CVE-2004-0815](https://www.cve.org/CVERecord?id=CVE-2004-0815) | "/./////etc" cleansed to ".///etc" then "/etc" |
| [CVE-2002-0112](https://www.cve.org/CVERecord?id=CVE-2002-0112) | Server allows remote attackers to view password protected files via /./ in the URL. |
| [CVE-2004-0696](https://www.cve.org/CVERecord?id=CVE-2004-0696) | List directories using desired path and "\*" |
| [CVE-2002-0433](https://www.cve.org/CVERecord?id=CVE-2002-0433) | List files in web server using "\*.ext" |
| [CVE-2001-1152](https://www.cve.org/CVERecord?id=CVE-2001-1152) | Proxy allows remote attackers to bypass denylist restrictions and connect to unauthorized web servers by modifying the requested URL, including (1) a // (double slash), (2) a /SUBDIR/.. where the desired file is in the parentdir, (3) a /./, or (4) URL-encoded characters. |
| [CVE-2000-0191](https://www.cve.org/CVERecord?id=CVE-2000-0191) | application check access for restricted URL before canonicalization |
| [CVE-2005-1366](https://www.cve.org/CVERecord?id=CVE-2005-1366) | CGI source disclosure using "dirname/../cgi-bin" |
| [CVE-1999-0012](https://www.cve.org/CVERecord?id=CVE-1999-0012) | Multiple web servers allow restriction bypass using 8.3 names instead of long names |
| [CVE-2001-0795](https://www.cve.org/CVERecord?id=CVE-2001-0795) | Source code disclosure using 8.3 file name. |
| [CVE-2005-0471](https://www.cve.org/CVERecord?id=CVE-2005-0471) | Multi-Factor Vulnerability. Product generates temporary filenames using long filenames, which become predictable in 8.3 format. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | Path Equivalence |
| CERT C Secure Coding | FIO02-C | Canonicalize path names originating from untrusted sources |

## Related Attack Patterns

- [CAPEC-3](https://capec.mitre.org/data/definitions/3.html)

## References

- [REF-1479] Gregory Larsen, E. Kenneth Hong Fong, David A. Wheeler and Rama S. Moorthy. "State-of-the-Art Resources (SOAR) for Software Vulnerability Detection, Test, and Evaluation". 2014-07. <https://www.ida.org/-/media/feature/publications/s/st/stateoftheart-resources-soar-for-software-vulnerability-detection-test-and-evaluation/p-5061.ashx> (URL validated: 2025-09-05).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Relationship**: Some of these manipulations could be effective in path traversal issues, too.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Potential_Mitigations, Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, Other_Notes, Taxonomy_Mappings, Type |
| Modification | 2008-10-14 | CWE Content Team | MITRE | CWE 1.0.1, 2008-10-14 | updated Description |
| Modification | 2008-11-24 | CWE Content Team | MITRE | CWE 1.1, 2008-11-25 | updated Relationships, Taxonomy_Mappings |
| Modification | 2009-03-10 | CWE Content Team | MITRE | CWE 1.3, 2009-03-10 | updated Relationships |
| Modification | 2009-05-27 | CWE Content Team | MITRE | CWE 1.4, 2009-05-27 | updated Name |
| Modification | 2009-07-27 | CWE Content Team | MITRE | CWE 1.5, 2009-07-27 | updated Potential_Mitigations |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Other_Notes, Potential_Mitigations, Relationship_Notes |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2011-09-13 | CWE Content Team | MITRE | CWE 2.1, 2011-09-13 | updated Relationships, Taxonomy_Mappings |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Common_Consequences, Observed_Examples, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Detection_Factors, Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Affected_Resources, Applicable_Platforms, Relationships, Taxonomy_Mappings |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Related_Attack_Patterns |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Potential_Mitigations, Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Observed_Examples, Potential_Mitigations, Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2023-10-26 | CWE Content Team | MITRE | CWE 4.13, 2023-10-26 | updated Observed_Examples |
| Modification | 2024-02-29 | CWE Content Team | MITRE | CWE 4.14, 2024-02-29 | updated Observed_Examples |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Detection_Factors, Functional_Areas, References |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Observed_Examples, Relationships, Weakness_Ordinalities |

**Previous Entry Names:**

- Path Equivalence — 2008-04-11
- Failure to Resolve Path Equivalence — 2009-05-27

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
