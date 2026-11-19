---
secid: "secid:weakness/mitre.org/cwe@4.19.1"
entry_type: index
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
source: "https://cwe.mitre.org/data/xml/cwec_v4.19.1.xml.zip"
sha256: "61e08a4e9298ba77f2213f6d467ff00557b90d11f37ecf710204237339d9c68f"
---

# CWE 4.19.1

MITRE's Common Weakness Enumeration (CWE) version 4.19.1, released 2026-01-21, as markdown: this index and one page per weakness (`weaknesses/`), category (`categories/`) and view (`views/`).

- **Edition:** CWE 4.19.1, released 2026-01-21
- **Source:** `cwec_v4.19.1.xml` in [cwec_v4.19.1.xml.zip](https://cwe.mitre.org/data/xml/cwec_v4.19.1.xml.zip), SHA-256 `61e08a4e9298ba77f2213f6d467ff00557b90d11f37ecf710204237339d9c68f`
- **Licence:** CWE Terms of Use, <https://cwe.mitre.org/about/termsofuse.html>; full text in [LICENSE.txt](LICENSE.txt)
- **Attribution:** Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
- **Upstream pages:** <https://cwe.mitre.org/data/definitions/> (MITRE's site shows the latest CWE version, which may differ from 4.19.1)

## Counts

### By entry type

| Entry type | Count |
| --- | --- |
| Weaknesses | 969 |
| Categories | 420 |
| Views | 58 |

### Weaknesses by abstraction

| Abstraction | Weaknesses |
| --- | --- |
| Pillar | 10 |
| Class | 114 |
| Base | 539 |
| Variant | 299 |
| Compound | 7 |

### By status

| Status | Weaknesses | Categories | Views |
| --- | --- | --- | --- |
| Stable | 26 | 46 | 8 |
| Draft | 432 | 70 | 18 |
| Incomplete | 486 | 183 | 17 |
| Obsolete | 0 | 86 | 11 |
| Deprecated | 25 | 35 | 4 |

## Weaknesses

| ID | Name | Abstraction | Status | Mapping usage |
| --- | --- | --- | --- | --- |
| [CWE-5](weaknesses/CWE-5.md) | J2EE Misconfiguration: Data Transmission Without Encryption | Variant | Draft | Allowed |
| [CWE-6](weaknesses/CWE-6.md) | J2EE Misconfiguration: Insufficient Session-ID Length | Variant | Incomplete | Allowed |
| [CWE-7](weaknesses/CWE-7.md) | J2EE Misconfiguration: Missing Custom Error Page | Variant | Incomplete | Allowed |
| [CWE-8](weaknesses/CWE-8.md) | J2EE Misconfiguration: Entity Bean Declared Remote | Variant | Incomplete | Allowed |
| [CWE-9](weaknesses/CWE-9.md) | J2EE Misconfiguration: Weak Access Permissions for EJB Methods | Variant | Draft | Allowed |
| [CWE-11](weaknesses/CWE-11.md) | ASP.NET Misconfiguration: Creating Debug Binary | Variant | Draft | Allowed |
| [CWE-12](weaknesses/CWE-12.md) | ASP.NET Misconfiguration: Missing Custom Error Page | Variant | Draft | Allowed |
| [CWE-13](weaknesses/CWE-13.md) | ASP.NET Misconfiguration: Password in Configuration File | Variant | Draft | Allowed |
| [CWE-14](weaknesses/CWE-14.md) | Compiler Removal of Code to Clear Buffers | Variant | Draft | Allowed |
| [CWE-15](weaknesses/CWE-15.md) | External Control of System or Configuration Setting | Base | Incomplete | Allowed |
| [CWE-20](weaknesses/CWE-20.md) | Improper Input Validation | Class | Stable | Discouraged |
| [CWE-22](weaknesses/CWE-22.md) | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | Base | Stable | Allowed-with-Review |
| [CWE-23](weaknesses/CWE-23.md) | Relative Path Traversal | Base | Draft | Allowed |
| [CWE-24](weaknesses/CWE-24.md) | Path Traversal: '../filedir' | Variant | Incomplete | Allowed |
| [CWE-25](weaknesses/CWE-25.md) | Path Traversal: '/../filedir' | Variant | Incomplete | Allowed |
| [CWE-26](weaknesses/CWE-26.md) | Path Traversal: '/dir/../filename' | Variant | Draft | Allowed |
| [CWE-27](weaknesses/CWE-27.md) | Path Traversal: 'dir/../../filename' | Variant | Draft | Allowed |
| [CWE-28](weaknesses/CWE-28.md) | Path Traversal: '..\filedir' | Variant | Incomplete | Allowed |
| [CWE-29](weaknesses/CWE-29.md) | Path Traversal: '\\..\filename' | Variant | Incomplete | Allowed |
| [CWE-30](weaknesses/CWE-30.md) | Path Traversal: '\dir\\..\filename' | Variant | Draft | Allowed |
| [CWE-31](weaknesses/CWE-31.md) | Path Traversal: 'dir\\..\\..\filename' | Variant | Draft | Allowed |
| [CWE-32](weaknesses/CWE-32.md) | Path Traversal: '...' (Triple Dot) | Variant | Incomplete | Allowed |
| [CWE-33](weaknesses/CWE-33.md) | Path Traversal: '....' (Multiple Dot) | Variant | Incomplete | Allowed |
| [CWE-34](weaknesses/CWE-34.md) | Path Traversal: '....//' | Variant | Incomplete | Allowed |
| [CWE-35](weaknesses/CWE-35.md) | Path Traversal: '.../...//' | Variant | Incomplete | Allowed |
| [CWE-36](weaknesses/CWE-36.md) | Absolute Path Traversal | Base | Draft | Allowed |
| [CWE-37](weaknesses/CWE-37.md) | Path Traversal: '/absolute/pathname/here' | Variant | Draft | Allowed |
| [CWE-38](weaknesses/CWE-38.md) | Path Traversal: '\absolute\pathname\here' | Variant | Draft | Allowed |
| [CWE-39](weaknesses/CWE-39.md) | Path Traversal: 'C:dirname' | Variant | Draft | Allowed |
| [CWE-40](weaknesses/CWE-40.md) | Path Traversal: '\\\UNC\share\name\\' (Windows UNC Share) | Variant | Draft | Allowed |
| [CWE-41](weaknesses/CWE-41.md) | Improper Resolution of Path Equivalence | Base | Incomplete | Allowed |
| [CWE-42](weaknesses/CWE-42.md) | Path Equivalence: 'filename.' (Trailing Dot) | Variant | Incomplete | Allowed |
| [CWE-43](weaknesses/CWE-43.md) | Path Equivalence: 'filename....' (Multiple Trailing Dot) | Variant | Incomplete | Allowed |
| [CWE-44](weaknesses/CWE-44.md) | Path Equivalence: 'file.name' (Internal Dot) | Variant | Incomplete | Allowed |
| [CWE-45](weaknesses/CWE-45.md) | Path Equivalence: 'file...name' (Multiple Internal Dot) | Variant | Incomplete | Allowed |
| [CWE-46](weaknesses/CWE-46.md) | Path Equivalence: 'filename ' (Trailing Space) | Variant | Incomplete | Allowed |
| [CWE-47](weaknesses/CWE-47.md) | Path Equivalence: ' filename' (Leading Space) | Variant | Incomplete | Allowed |
| [CWE-48](weaknesses/CWE-48.md) | Path Equivalence: 'file name' (Internal Whitespace) | Variant | Incomplete | Allowed |
| [CWE-49](weaknesses/CWE-49.md) | Path Equivalence: 'filename/' (Trailing Slash) | Variant | Incomplete | Allowed |
| [CWE-50](weaknesses/CWE-50.md) | Path Equivalence: '//multiple/leading/slash' | Variant | Incomplete | Allowed |
| [CWE-51](weaknesses/CWE-51.md) | Path Equivalence: '/multiple//internal/slash' | Variant | Incomplete | Allowed |
| [CWE-52](weaknesses/CWE-52.md) | Path Equivalence: '/multiple/trailing/slash//' | Variant | Incomplete | Allowed |
| [CWE-53](weaknesses/CWE-53.md) | Path Equivalence: '\multiple\\\internal\backslash' | Variant | Incomplete | Allowed |
| [CWE-54](weaknesses/CWE-54.md) | Path Equivalence: 'filedir\\' (Trailing Backslash) | Variant | Incomplete | Allowed |
| [CWE-55](weaknesses/CWE-55.md) | Path Equivalence: '/./' (Single Dot Directory) | Variant | Incomplete | Allowed |
| [CWE-56](weaknesses/CWE-56.md) | Path Equivalence: 'filedir\*' (Wildcard) | Variant | Incomplete | Allowed |
| [CWE-57](weaknesses/CWE-57.md) | Path Equivalence: 'fakedir/../realdir/filename' | Variant | Incomplete | Allowed |
| [CWE-58](weaknesses/CWE-58.md) | Path Equivalence: Windows 8.3 Filename | Variant | Incomplete | Allowed |
| [CWE-59](weaknesses/CWE-59.md) | Improper Link Resolution Before File Access ('Link Following') | Base | Draft | Allowed |
| [CWE-61](weaknesses/CWE-61.md) | UNIX Symbolic Link (Symlink) Following | Compound | Incomplete | Allowed |
| [CWE-62](weaknesses/CWE-62.md) | UNIX Hard Link | Variant | Incomplete | Allowed |
| [CWE-64](weaknesses/CWE-64.md) | Windows Shortcut Following (.LNK) | Variant | Incomplete | Allowed |
| [CWE-65](weaknesses/CWE-65.md) | Windows Hard Link | Variant | Incomplete | Allowed |
| [CWE-66](weaknesses/CWE-66.md) | Improper Handling of File Names that Identify Virtual Resources | Base | Draft | Allowed |
| [CWE-67](weaknesses/CWE-67.md) | Improper Handling of Windows Device Names | Variant | Incomplete | Allowed |
| [CWE-69](weaknesses/CWE-69.md) | Improper Handling of Windows ::DATA Alternate Data Stream | Variant | Incomplete | Allowed |
| [CWE-71](weaknesses/CWE-71.md) | DEPRECATED: Apple '.DS_Store' | Variant | Deprecated | Prohibited |
| [CWE-72](weaknesses/CWE-72.md) | Improper Handling of Apple HFS+ Alternate Data Stream Path | Variant | Incomplete | Allowed |
| [CWE-73](weaknesses/CWE-73.md) | External Control of File Name or Path | Base | Draft | Allowed |
| [CWE-74](weaknesses/CWE-74.md) | Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') | Class | Incomplete | Discouraged |
| [CWE-75](weaknesses/CWE-75.md) | Failure to Sanitize Special Elements into a Different Plane (Special Element Injection) | Class | Draft | Discouraged |
| [CWE-76](weaknesses/CWE-76.md) | Improper Neutralization of Equivalent Special Elements | Base | Draft | Allowed |
| [CWE-77](weaknesses/CWE-77.md) | Improper Neutralization of Special Elements used in a Command ('Command Injection') | Class | Draft | Allowed-with-Review |
| [CWE-78](weaknesses/CWE-78.md) | Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') | Base | Stable | Allowed |
| [CWE-79](weaknesses/CWE-79.md) | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | Base | Stable | Allowed |
| [CWE-80](weaknesses/CWE-80.md) | Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS) | Variant | Incomplete | Allowed |
| [CWE-81](weaknesses/CWE-81.md) | Improper Neutralization of Script in an Error Message Web Page | Variant | Incomplete | Allowed |
| [CWE-82](weaknesses/CWE-82.md) | Improper Neutralization of Script in Attributes of IMG Tags in a Web Page | Variant | Incomplete | Allowed |
| [CWE-83](weaknesses/CWE-83.md) | Improper Neutralization of Script in Attributes in a Web Page | Variant | Draft | Allowed |
| [CWE-84](weaknesses/CWE-84.md) | Improper Neutralization of Encoded URI Schemes in a Web Page | Variant | Draft | Allowed |
| [CWE-85](weaknesses/CWE-85.md) | Doubled Character XSS Manipulations | Variant | Draft | Allowed |
| [CWE-86](weaknesses/CWE-86.md) | Improper Neutralization of Invalid Characters in Identifiers in Web Pages | Variant | Draft | Allowed |
| [CWE-87](weaknesses/CWE-87.md) | Improper Neutralization of Alternate XSS Syntax | Variant | Draft | Allowed |
| [CWE-88](weaknesses/CWE-88.md) | Improper Neutralization of Argument Delimiters in a Command ('Argument Injection') | Base | Draft | Allowed |
| [CWE-89](weaknesses/CWE-89.md) | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | Base | Stable | Allowed |
| [CWE-90](weaknesses/CWE-90.md) | Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection') | Base | Draft | Allowed |
| [CWE-91](weaknesses/CWE-91.md) | XML Injection (aka Blind XPath Injection) | Base | Draft | Allowed |
| [CWE-92](weaknesses/CWE-92.md) | DEPRECATED: Improper Sanitization of Custom Special Characters | Base | Deprecated | Prohibited |
| [CWE-93](weaknesses/CWE-93.md) | Improper Neutralization of CRLF Sequences ('CRLF Injection') | Base | Draft | Allowed |
| [CWE-94](weaknesses/CWE-94.md) | Improper Control of Generation of Code ('Code Injection') | Base | Draft | Allowed-with-Review |
| [CWE-95](weaknesses/CWE-95.md) | Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') | Variant | Incomplete | Allowed |
| [CWE-96](weaknesses/CWE-96.md) | Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection') | Base | Draft | Allowed |
| [CWE-97](weaknesses/CWE-97.md) | Improper Neutralization of Server-Side Includes (SSI) Within a Web Page | Variant | Draft | Allowed |
| [CWE-98](weaknesses/CWE-98.md) | Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') | Variant | Draft | Allowed |
| [CWE-99](weaknesses/CWE-99.md) | Improper Control of Resource Identifiers ('Resource Injection') | Class | Draft | Allowed-with-Review |
| [CWE-102](weaknesses/CWE-102.md) | Struts: Duplicate Validation Forms | Variant | Incomplete | Allowed |
| [CWE-103](weaknesses/CWE-103.md) | Struts: Incomplete validate() Method Definition | Variant | Draft | Allowed |
| [CWE-104](weaknesses/CWE-104.md) | Struts: Form Bean Does Not Extend Validation Class | Variant | Draft | Allowed |
| [CWE-105](weaknesses/CWE-105.md) | Struts: Form Field Without Validator | Variant | Draft | Allowed |
| [CWE-106](weaknesses/CWE-106.md) | Struts: Plug-in Framework not in Use | Variant | Draft | Allowed |
| [CWE-107](weaknesses/CWE-107.md) | Struts: Unused Validation Form | Variant | Draft | Allowed |
| [CWE-108](weaknesses/CWE-108.md) | Struts: Unvalidated Action Form | Variant | Incomplete | Allowed |
| [CWE-109](weaknesses/CWE-109.md) | Struts: Validator Turned Off | Variant | Draft | Allowed |
| [CWE-110](weaknesses/CWE-110.md) | Struts: Validator Without Form Field | Variant | Draft | Allowed |
| [CWE-111](weaknesses/CWE-111.md) | Direct Use of Unsafe JNI | Variant | Draft | Allowed |
| [CWE-112](weaknesses/CWE-112.md) | Missing XML Validation | Base | Draft | Allowed |
| [CWE-113](weaknesses/CWE-113.md) | Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Request/Response Splitting') | Variant | Incomplete | Allowed |
| [CWE-114](weaknesses/CWE-114.md) | Process Control | Class | Incomplete | Discouraged |
| [CWE-115](weaknesses/CWE-115.md) | Misinterpretation of Input | Base | Incomplete | Allowed |
| [CWE-116](weaknesses/CWE-116.md) | Improper Encoding or Escaping of Output | Class | Draft | Allowed-with-Review |
| [CWE-117](weaknesses/CWE-117.md) | Improper Output Neutralization for Logs | Base | Draft | Allowed |
| [CWE-118](weaknesses/CWE-118.md) | Incorrect Access of Indexable Resource ('Range Error') | Class | Incomplete | Discouraged |
| [CWE-119](weaknesses/CWE-119.md) | Improper Restriction of Operations within the Bounds of a Memory Buffer | Class | Stable | Discouraged |
| [CWE-120](weaknesses/CWE-120.md) | Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') | Base | Incomplete | Allowed-with-Review |
| [CWE-121](weaknesses/CWE-121.md) | Stack-based Buffer Overflow | Variant | Draft | Allowed |
| [CWE-122](weaknesses/CWE-122.md) | Heap-based Buffer Overflow | Variant | Draft | Allowed |
| [CWE-123](weaknesses/CWE-123.md) | Write-what-where Condition | Base | Draft | Allowed |
| [CWE-124](weaknesses/CWE-124.md) | Buffer Underwrite ('Buffer Underflow') | Base | Incomplete | Allowed |
| [CWE-125](weaknesses/CWE-125.md) | Out-of-bounds Read | Base | Draft | Allowed |
| [CWE-126](weaknesses/CWE-126.md) | Buffer Over-read | Variant | Draft | Allowed |
| [CWE-127](weaknesses/CWE-127.md) | Buffer Under-read | Variant | Draft | Allowed |
| [CWE-128](weaknesses/CWE-128.md) | Wrap-around Error | Base | Incomplete | Allowed |
| [CWE-129](weaknesses/CWE-129.md) | Improper Validation of Array Index | Variant | Draft | Allowed |
| [CWE-130](weaknesses/CWE-130.md) | Improper Handling of Length Parameter Inconsistency | Base | Incomplete | Allowed |
| [CWE-131](weaknesses/CWE-131.md) | Incorrect Calculation of Buffer Size | Base | Draft | Allowed |
| [CWE-132](weaknesses/CWE-132.md) | DEPRECATED: Miscalculated Null Termination | Base | Deprecated | Prohibited |
| [CWE-134](weaknesses/CWE-134.md) | Use of Externally-Controlled Format String | Base | Draft | Allowed |
| [CWE-135](weaknesses/CWE-135.md) | Incorrect Calculation of Multi-Byte String Length | Base | Draft | Allowed |
| [CWE-138](weaknesses/CWE-138.md) | Improper Neutralization of Special Elements | Class | Draft | Discouraged |
| [CWE-140](weaknesses/CWE-140.md) | Improper Neutralization of Delimiters | Base | Draft | Allowed |
| [CWE-141](weaknesses/CWE-141.md) | Improper Neutralization of Parameter/Argument Delimiters | Variant | Draft | Allowed |
| [CWE-142](weaknesses/CWE-142.md) | Improper Neutralization of Value Delimiters | Variant | Draft | Allowed |
| [CWE-143](weaknesses/CWE-143.md) | Improper Neutralization of Record Delimiters | Variant | Draft | Allowed |
| [CWE-144](weaknesses/CWE-144.md) | Improper Neutralization of Line Delimiters | Variant | Draft | Allowed |
| [CWE-145](weaknesses/CWE-145.md) | Improper Neutralization of Section Delimiters | Variant | Incomplete | Allowed |
| [CWE-146](weaknesses/CWE-146.md) | Improper Neutralization of Expression/Command Delimiters | Variant | Incomplete | Allowed |
| [CWE-147](weaknesses/CWE-147.md) | Improper Neutralization of Input Terminators | Variant | Draft | Allowed |
| [CWE-148](weaknesses/CWE-148.md) | Improper Neutralization of Input Leaders | Variant | Draft | Allowed |
| [CWE-149](weaknesses/CWE-149.md) | Improper Neutralization of Quoting Syntax | Variant | Draft | Allowed |
| [CWE-150](weaknesses/CWE-150.md) | Improper Neutralization of Escape, Meta, or Control Sequences | Variant | Incomplete | Allowed |
| [CWE-151](weaknesses/CWE-151.md) | Improper Neutralization of Comment Delimiters | Variant | Draft | Allowed |
| [CWE-152](weaknesses/CWE-152.md) | Improper Neutralization of Macro Symbols | Variant | Draft | Allowed |
| [CWE-153](weaknesses/CWE-153.md) | Improper Neutralization of Substitution Characters | Variant | Draft | Allowed |
| [CWE-154](weaknesses/CWE-154.md) | Improper Neutralization of Variable Name Delimiters | Variant | Incomplete | Allowed |
| [CWE-155](weaknesses/CWE-155.md) | Improper Neutralization of Wildcards or Matching Symbols | Variant | Draft | Allowed |
| [CWE-156](weaknesses/CWE-156.md) | Improper Neutralization of Whitespace | Variant | Draft | Allowed |
| [CWE-157](weaknesses/CWE-157.md) | Failure to Sanitize Paired Delimiters | Variant | Draft | Allowed |
| [CWE-158](weaknesses/CWE-158.md) | Improper Neutralization of Null Byte or NUL Character | Variant | Incomplete | Allowed |
| [CWE-159](weaknesses/CWE-159.md) | Improper Handling of Invalid Use of Special Elements | Class | Draft | Allowed-with-Review |
| [CWE-160](weaknesses/CWE-160.md) | Improper Neutralization of Leading Special Elements | Variant | Incomplete | Allowed |
| [CWE-161](weaknesses/CWE-161.md) | Improper Neutralization of Multiple Leading Special Elements | Variant | Incomplete | Allowed |
| [CWE-162](weaknesses/CWE-162.md) | Improper Neutralization of Trailing Special Elements | Variant | Incomplete | Allowed |
| [CWE-163](weaknesses/CWE-163.md) | Improper Neutralization of Multiple Trailing Special Elements | Variant | Incomplete | Allowed |
| [CWE-164](weaknesses/CWE-164.md) | Improper Neutralization of Internal Special Elements | Variant | Incomplete | Allowed |
| [CWE-165](weaknesses/CWE-165.md) | Improper Neutralization of Multiple Internal Special Elements | Variant | Incomplete | Allowed |
| [CWE-166](weaknesses/CWE-166.md) | Improper Handling of Missing Special Element | Base | Draft | Allowed |
| [CWE-167](weaknesses/CWE-167.md) | Improper Handling of Additional Special Element | Base | Draft | Allowed |
| [CWE-168](weaknesses/CWE-168.md) | Improper Handling of Inconsistent Special Elements | Base | Draft | Allowed |
| [CWE-170](weaknesses/CWE-170.md) | Improper Null Termination | Base | Incomplete | Allowed |
| [CWE-172](weaknesses/CWE-172.md) | Encoding Error | Class | Draft | Allowed-with-Review |
| [CWE-173](weaknesses/CWE-173.md) | Improper Handling of Alternate Encoding | Variant | Draft | Allowed |
| [CWE-174](weaknesses/CWE-174.md) | Double Decoding of the Same Data | Variant | Draft | Allowed |
| [CWE-175](weaknesses/CWE-175.md) | Improper Handling of Mixed Encoding | Variant | Draft | Allowed |
| [CWE-176](weaknesses/CWE-176.md) | Improper Handling of Unicode Encoding | Variant | Draft | Allowed |
| [CWE-177](weaknesses/CWE-177.md) | Improper Handling of URL Encoding (Hex Encoding) | Variant | Draft | Allowed |
| [CWE-178](weaknesses/CWE-178.md) | Improper Handling of Case Sensitivity | Base | Incomplete | Allowed |
| [CWE-179](weaknesses/CWE-179.md) | Incorrect Behavior Order: Early Validation | Base | Incomplete | Allowed |
| [CWE-180](weaknesses/CWE-180.md) | Incorrect Behavior Order: Validate Before Canonicalize | Variant | Draft | Allowed |
| [CWE-181](weaknesses/CWE-181.md) | Incorrect Behavior Order: Validate Before Filter | Variant | Draft | Allowed |
| [CWE-182](weaknesses/CWE-182.md) | Collapse of Data into Unsafe Value | Base | Draft | Allowed |
| [CWE-183](weaknesses/CWE-183.md) | Permissive List of Allowed Inputs | Base | Draft | Allowed |
| [CWE-184](weaknesses/CWE-184.md) | Incomplete List of Disallowed Inputs | Base | Draft | Allowed |
| [CWE-185](weaknesses/CWE-185.md) | Incorrect Regular Expression | Class | Draft | Allowed-with-Review |
| [CWE-186](weaknesses/CWE-186.md) | Overly Restrictive Regular Expression | Base | Draft | Allowed |
| [CWE-187](weaknesses/CWE-187.md) | Partial String Comparison | Variant | Incomplete | Allowed |
| [CWE-188](weaknesses/CWE-188.md) | Reliance on Data/Memory Layout | Base | Draft | Allowed |
| [CWE-190](weaknesses/CWE-190.md) | Integer Overflow or Wraparound | Base | Stable | Allowed |
| [CWE-191](weaknesses/CWE-191.md) | Integer Underflow (Wrap or Wraparound) | Base | Draft | Allowed |
| [CWE-192](weaknesses/CWE-192.md) | Integer Coercion Error | Variant | Incomplete | Allowed |
| [CWE-193](weaknesses/CWE-193.md) | Off-by-one Error | Base | Draft | Allowed |
| [CWE-194](weaknesses/CWE-194.md) | Unexpected Sign Extension | Variant | Incomplete | Allowed |
| [CWE-195](weaknesses/CWE-195.md) | Signed to Unsigned Conversion Error | Variant | Draft | Allowed |
| [CWE-196](weaknesses/CWE-196.md) | Unsigned to Signed Conversion Error | Variant | Draft | Allowed |
| [CWE-197](weaknesses/CWE-197.md) | Numeric Truncation Error | Base | Incomplete | Allowed |
| [CWE-198](weaknesses/CWE-198.md) | Use of Incorrect Byte Ordering | Variant | Draft | Allowed |
| [CWE-200](weaknesses/CWE-200.md) | Exposure of Sensitive Information to an Unauthorized Actor | Class | Draft | Discouraged |
| [CWE-201](weaknesses/CWE-201.md) | Insertion of Sensitive Information Into Sent Data | Base | Draft | Allowed |
| [CWE-202](weaknesses/CWE-202.md) | Exposure of Sensitive Information Through Data Queries | Base | Draft | Allowed |
| [CWE-203](weaknesses/CWE-203.md) | Observable Discrepancy | Base | Incomplete | Allowed |
| [CWE-204](weaknesses/CWE-204.md) | Observable Response Discrepancy | Base | Incomplete | Allowed |
| [CWE-205](weaknesses/CWE-205.md) | Observable Behavioral Discrepancy | Base | Incomplete | Allowed |
| [CWE-206](weaknesses/CWE-206.md) | Observable Internal Behavioral Discrepancy | Variant | Incomplete | Allowed |
| [CWE-207](weaknesses/CWE-207.md) | Observable Behavioral Discrepancy With Equivalent Products | Variant | Draft | Allowed |
| [CWE-208](weaknesses/CWE-208.md) | Observable Timing Discrepancy | Base | Incomplete | Allowed |
| [CWE-209](weaknesses/CWE-209.md) | Generation of Error Message Containing Sensitive Information | Base | Draft | Allowed |
| [CWE-210](weaknesses/CWE-210.md) | Self-generated Error Message Containing Sensitive Information | Base | Draft | Allowed |
| [CWE-211](weaknesses/CWE-211.md) | Externally-Generated Error Message Containing Sensitive Information | Base | Incomplete | Allowed |
| [CWE-212](weaknesses/CWE-212.md) | Improper Removal of Sensitive Information Before Storage or Transfer | Base | Incomplete | Allowed |
| [CWE-213](weaknesses/CWE-213.md) | Exposure of Sensitive Information Due to Incompatible Policies | Base | Draft | Allowed |
| [CWE-214](weaknesses/CWE-214.md) | Invocation of Process Using Visible Sensitive Information | Base | Incomplete | Allowed |
| [CWE-215](weaknesses/CWE-215.md) | Insertion of Sensitive Information Into Debugging Code | Base | Draft | Allowed |
| [CWE-216](weaknesses/CWE-216.md) | DEPRECATED: Containment Errors (Container Errors) | Class | Deprecated | Prohibited |
| [CWE-217](weaknesses/CWE-217.md) | DEPRECATED: Failure to Protect Stored Data from Modification | Base | Deprecated | Prohibited |
| [CWE-218](weaknesses/CWE-218.md) | DEPRECATED: Failure to provide confidentiality for stored data | Base | Deprecated | Prohibited |
| [CWE-219](weaknesses/CWE-219.md) | Storage of File with Sensitive Data Under Web Root | Variant | Draft | Allowed |
| [CWE-220](weaknesses/CWE-220.md) | Storage of File With Sensitive Data Under FTP Root | Variant | Draft | Allowed |
| [CWE-221](weaknesses/CWE-221.md) | Information Loss or Omission | Class | Incomplete | Allowed-with-Review |
| [CWE-222](weaknesses/CWE-222.md) | Truncation of Security-relevant Information | Base | Draft | Allowed |
| [CWE-223](weaknesses/CWE-223.md) | Omission of Security-relevant Information | Base | Draft | Allowed |
| [CWE-224](weaknesses/CWE-224.md) | Obscured Security-relevant Information by Alternate Name | Base | Incomplete | Allowed |
| [CWE-225](weaknesses/CWE-225.md) | DEPRECATED: General Information Management Problems | Base | Deprecated | Prohibited |
| [CWE-226](weaknesses/CWE-226.md) | Sensitive Information in Resource Not Removed Before Reuse | Base | Draft | Allowed |
| [CWE-228](weaknesses/CWE-228.md) | Improper Handling of Syntactically Invalid Structure | Class | Incomplete | Allowed-with-Review |
| [CWE-229](weaknesses/CWE-229.md) | Improper Handling of Values | Base | Incomplete | Allowed |
| [CWE-230](weaknesses/CWE-230.md) | Improper Handling of Missing Values | Variant | Draft | Allowed |
| [CWE-231](weaknesses/CWE-231.md) | Improper Handling of Extra Values | Variant | Draft | Allowed |
| [CWE-232](weaknesses/CWE-232.md) | Improper Handling of Undefined Values | Variant | Draft | Allowed |
| [CWE-233](weaknesses/CWE-233.md) | Improper Handling of Parameters | Base | Incomplete | Allowed |
| [CWE-234](weaknesses/CWE-234.md) | Failure to Handle Missing Parameter | Variant | Incomplete | Discouraged |
| [CWE-235](weaknesses/CWE-235.md) | Improper Handling of Extra Parameters | Variant | Draft | Allowed |
| [CWE-236](weaknesses/CWE-236.md) | Improper Handling of Undefined Parameters | Variant | Draft | Allowed |
| [CWE-237](weaknesses/CWE-237.md) | Improper Handling of Structural Elements | Base | Incomplete | Allowed |
| [CWE-238](weaknesses/CWE-238.md) | Improper Handling of Incomplete Structural Elements | Variant | Draft | Allowed |
| [CWE-239](weaknesses/CWE-239.md) | Failure to Handle Incomplete Element | Variant | Draft | Allowed |
| [CWE-240](weaknesses/CWE-240.md) | Improper Handling of Inconsistent Structural Elements | Base | Draft | Allowed |
| [CWE-241](weaknesses/CWE-241.md) | Improper Handling of Unexpected Data Type | Base | Draft | Allowed |
| [CWE-242](weaknesses/CWE-242.md) | Use of Inherently Dangerous Function | Base | Draft | Allowed |
| [CWE-243](weaknesses/CWE-243.md) | Creation of chroot Jail Without Changing Working Directory | Variant | Draft | Allowed |
| [CWE-244](weaknesses/CWE-244.md) | Improper Clearing of Heap Memory Before Release ('Heap Inspection') | Variant | Draft | Allowed |
| [CWE-245](weaknesses/CWE-245.md) | J2EE Bad Practices: Direct Management of Connections | Variant | Draft | Allowed |
| [CWE-246](weaknesses/CWE-246.md) | J2EE Bad Practices: Direct Use of Sockets | Variant | Draft | Allowed |
| [CWE-247](weaknesses/CWE-247.md) | DEPRECATED: Reliance on DNS Lookups in a Security Decision | Base | Deprecated | Prohibited |
| [CWE-248](weaknesses/CWE-248.md) | Uncaught Exception | Base | Draft | Allowed |
| [CWE-249](weaknesses/CWE-249.md) | DEPRECATED: Often Misused: Path Manipulation | Variant | Deprecated | Prohibited |
| [CWE-250](weaknesses/CWE-250.md) | Execution with Unnecessary Privileges | Base | Draft | Allowed |
| [CWE-252](weaknesses/CWE-252.md) | Unchecked Return Value | Base | Draft | Allowed |
| [CWE-253](weaknesses/CWE-253.md) | Incorrect Check of Function Return Value | Base | Incomplete | Allowed |
| [CWE-256](weaknesses/CWE-256.md) | Plaintext Storage of a Password | Base | Incomplete | Allowed |
| [CWE-257](weaknesses/CWE-257.md) | Storing Passwords in a Recoverable Format | Base | Incomplete | Allowed |
| [CWE-258](weaknesses/CWE-258.md) | Empty Password in Configuration File | Variant | Incomplete | Allowed |
| [CWE-259](weaknesses/CWE-259.md) | Use of Hard-coded Password | Variant | Draft | Allowed |
| [CWE-260](weaknesses/CWE-260.md) | Password in Configuration File | Base | Incomplete | Allowed |
| [CWE-261](weaknesses/CWE-261.md) | Weak Encoding for Password | Base | Incomplete | Allowed |
| [CWE-262](weaknesses/CWE-262.md) | Not Using Password Aging | Base | Draft | Allowed |
| [CWE-263](weaknesses/CWE-263.md) | Password Aging with Long Expiration | Base | Draft | Discouraged |
| [CWE-266](weaknesses/CWE-266.md) | Incorrect Privilege Assignment | Base | Draft | Allowed |
| [CWE-267](weaknesses/CWE-267.md) | Privilege Defined With Unsafe Actions | Base | Incomplete | Allowed |
| [CWE-268](weaknesses/CWE-268.md) | Privilege Chaining | Base | Draft | Allowed |
| [CWE-269](weaknesses/CWE-269.md) | Improper Privilege Management | Class | Draft | Discouraged |
| [CWE-270](weaknesses/CWE-270.md) | Privilege Context Switching Error | Base | Draft | Allowed |
| [CWE-271](weaknesses/CWE-271.md) | Privilege Dropping / Lowering Errors | Class | Incomplete | Allowed-with-Review |
| [CWE-272](weaknesses/CWE-272.md) | Least Privilege Violation | Base | Incomplete | Allowed |
| [CWE-273](weaknesses/CWE-273.md) | Improper Check for Dropped Privileges | Base | Incomplete | Allowed |
| [CWE-274](weaknesses/CWE-274.md) | Improper Handling of Insufficient Privileges | Base | Draft | Discouraged |
| [CWE-276](weaknesses/CWE-276.md) | Incorrect Default Permissions | Base | Draft | Allowed |
| [CWE-277](weaknesses/CWE-277.md) | Insecure Inherited Permissions | Variant | Draft | Allowed |
| [CWE-278](weaknesses/CWE-278.md) | Insecure Preserved Inherited Permissions | Variant | Incomplete | Allowed |
| [CWE-279](weaknesses/CWE-279.md) | Incorrect Execution-Assigned Permissions | Variant | Draft | Allowed |
| [CWE-280](weaknesses/CWE-280.md) | Improper Handling of Insufficient Permissions or Privileges | Base | Draft | Allowed |
| [CWE-281](weaknesses/CWE-281.md) | Improper Preservation of Permissions | Base | Draft | Allowed |
| [CWE-282](weaknesses/CWE-282.md) | Improper Ownership Management | Class | Draft | Allowed-with-Review |
| [CWE-283](weaknesses/CWE-283.md) | Unverified Ownership | Base | Draft | Allowed |
| [CWE-284](weaknesses/CWE-284.md) | Improper Access Control | Pillar | Incomplete | Discouraged |
| [CWE-285](weaknesses/CWE-285.md) | Improper Authorization | Class | Draft | Discouraged |
| [CWE-286](weaknesses/CWE-286.md) | Incorrect User Management | Class | Incomplete | Allowed-with-Review |
| [CWE-287](weaknesses/CWE-287.md) | Improper Authentication | Class | Draft | Discouraged |
| [CWE-288](weaknesses/CWE-288.md) | Authentication Bypass Using an Alternate Path or Channel | Base | Incomplete | Allowed |
| [CWE-289](weaknesses/CWE-289.md) | Authentication Bypass by Alternate Name | Base | Incomplete | Allowed |
| [CWE-290](weaknesses/CWE-290.md) | Authentication Bypass by Spoofing | Base | Incomplete | Allowed |
| [CWE-291](weaknesses/CWE-291.md) | Reliance on IP Address for Authentication | Variant | Incomplete | Allowed |
| [CWE-292](weaknesses/CWE-292.md) | DEPRECATED: Trusting Self-reported DNS Name | Variant | Deprecated | Prohibited |
| [CWE-293](weaknesses/CWE-293.md) | Using Referer Field for Authentication | Variant | Draft | Allowed |
| [CWE-294](weaknesses/CWE-294.md) | Authentication Bypass by Capture-replay | Base | Incomplete | Allowed |
| [CWE-295](weaknesses/CWE-295.md) | Improper Certificate Validation | Base | Draft | Allowed |
| [CWE-296](weaknesses/CWE-296.md) | Improper Following of a Certificate's Chain of Trust | Base | Draft | Allowed |
| [CWE-297](weaknesses/CWE-297.md) | Improper Validation of Certificate with Host Mismatch | Variant | Incomplete | Allowed |
| [CWE-298](weaknesses/CWE-298.md) | Improper Validation of Certificate Expiration | Variant | Draft | Allowed |
| [CWE-299](weaknesses/CWE-299.md) | Improper Check for Certificate Revocation | Base | Draft | Allowed |
| [CWE-300](weaknesses/CWE-300.md) | Channel Accessible by Non-Endpoint | Class | Draft | Discouraged |
| [CWE-301](weaknesses/CWE-301.md) | Reflection Attack in an Authentication Protocol | Base | Draft | Allowed |
| [CWE-302](weaknesses/CWE-302.md) | Authentication Bypass by Assumed-Immutable Data | Base | Incomplete | Allowed |
| [CWE-303](weaknesses/CWE-303.md) | Incorrect Implementation of Authentication Algorithm | Base | Draft | Allowed |
| [CWE-304](weaknesses/CWE-304.md) | Missing Critical Step in Authentication | Base | Draft | Allowed |
| [CWE-305](weaknesses/CWE-305.md) | Authentication Bypass by Primary Weakness | Base | Draft | Allowed |
| [CWE-306](weaknesses/CWE-306.md) | Missing Authentication for Critical Function | Base | Draft | Allowed |
| [CWE-307](weaknesses/CWE-307.md) | Improper Restriction of Excessive Authentication Attempts | Base | Draft | Allowed |
| [CWE-308](weaknesses/CWE-308.md) | Use of Single-factor Authentication | Base | Draft | Allowed |
| [CWE-309](weaknesses/CWE-309.md) | Use of Password System for Primary Authentication | Base | Draft | Allowed |
| [CWE-311](weaknesses/CWE-311.md) | Missing Encryption of Sensitive Data | Class | Draft | Discouraged |
| [CWE-312](weaknesses/CWE-312.md) | Cleartext Storage of Sensitive Information | Base | Draft | Allowed |
| [CWE-313](weaknesses/CWE-313.md) | Cleartext Storage in a File or on Disk | Variant | Draft | Allowed |
| [CWE-314](weaknesses/CWE-314.md) | Cleartext Storage in the Registry | Variant | Draft | Allowed |
| [CWE-315](weaknesses/CWE-315.md) | Cleartext Storage of Sensitive Information in a Cookie | Variant | Draft | Allowed |
| [CWE-316](weaknesses/CWE-316.md) | Cleartext Storage of Sensitive Information in Memory | Variant | Draft | Allowed |
| [CWE-317](weaknesses/CWE-317.md) | Cleartext Storage of Sensitive Information in GUI | Variant | Draft | Allowed |
| [CWE-318](weaknesses/CWE-318.md) | Cleartext Storage of Sensitive Information in Executable | Variant | Draft | Allowed |
| [CWE-319](weaknesses/CWE-319.md) | Cleartext Transmission of Sensitive Information | Base | Draft | Allowed |
| [CWE-321](weaknesses/CWE-321.md) | Use of Hard-coded Cryptographic Key | Variant | Draft | Allowed |
| [CWE-322](weaknesses/CWE-322.md) | Key Exchange without Entity Authentication | Base | Draft | Allowed |
| [CWE-323](weaknesses/CWE-323.md) | Reusing a Nonce, Key Pair in Encryption | Base | Incomplete | Allowed |
| [CWE-324](weaknesses/CWE-324.md) | Use of a Key Past its Expiration Date | Base | Draft | Allowed |
| [CWE-325](weaknesses/CWE-325.md) | Missing Cryptographic Step | Base | Draft | Allowed |
| [CWE-326](weaknesses/CWE-326.md) | Inadequate Encryption Strength | Class | Draft | Allowed-with-Review |
| [CWE-327](weaknesses/CWE-327.md) | Use of a Broken or Risky Cryptographic Algorithm | Class | Draft | Allowed-with-Review |
| [CWE-328](weaknesses/CWE-328.md) | Use of Weak Hash | Base | Draft | Allowed |
| [CWE-329](weaknesses/CWE-329.md) | Generation of Predictable IV with CBC Mode | Variant | Draft | Allowed |
| [CWE-330](weaknesses/CWE-330.md) | Use of Insufficiently Random Values | Class | Stable | Discouraged |
| [CWE-331](weaknesses/CWE-331.md) | Insufficient Entropy | Base | Draft | Allowed |
| [CWE-332](weaknesses/CWE-332.md) | Insufficient Entropy in PRNG | Variant | Draft | Allowed |
| [CWE-333](weaknesses/CWE-333.md) | Improper Handling of Insufficient Entropy in TRNG | Variant | Draft | Allowed |
| [CWE-334](weaknesses/CWE-334.md) | Small Space of Random Values | Base | Draft | Allowed |
| [CWE-335](weaknesses/CWE-335.md) | Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG) | Base | Draft | Allowed |
| [CWE-336](weaknesses/CWE-336.md) | Same Seed in Pseudo-Random Number Generator (PRNG) | Variant | Draft | Allowed |
| [CWE-337](weaknesses/CWE-337.md) | Predictable Seed in Pseudo-Random Number Generator (PRNG) | Variant | Draft | Allowed |
| [CWE-338](weaknesses/CWE-338.md) | Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG) | Base | Draft | Allowed |
| [CWE-339](weaknesses/CWE-339.md) | Small Seed Space in PRNG | Variant | Draft | Allowed |
| [CWE-340](weaknesses/CWE-340.md) | Generation of Predictable Numbers or Identifiers | Class | Incomplete | Allowed-with-Review |
| [CWE-341](weaknesses/CWE-341.md) | Predictable from Observable State | Base | Draft | Allowed |
| [CWE-342](weaknesses/CWE-342.md) | Predictable Exact Value from Previous Values | Base | Draft | Allowed |
| [CWE-343](weaknesses/CWE-343.md) | Predictable Value Range from Previous Values | Base | Draft | Allowed |
| [CWE-344](weaknesses/CWE-344.md) | Use of Invariant Value in Dynamically Changing Context | Base | Draft | Allowed |
| [CWE-345](weaknesses/CWE-345.md) | Insufficient Verification of Data Authenticity | Class | Draft | Discouraged |
| [CWE-346](weaknesses/CWE-346.md) | Origin Validation Error | Class | Draft | Allowed-with-Review |
| [CWE-347](weaknesses/CWE-347.md) | Improper Verification of Cryptographic Signature | Base | Draft | Allowed |
| [CWE-348](weaknesses/CWE-348.md) | Use of Less Trusted Source | Base | Draft | Allowed |
| [CWE-349](weaknesses/CWE-349.md) | Acceptance of Extraneous Untrusted Data With Trusted Data | Base | Draft | Allowed |
| [CWE-350](weaknesses/CWE-350.md) | Reliance on Reverse DNS Resolution for a Security-Critical Action | Variant | Draft | Allowed |
| [CWE-351](weaknesses/CWE-351.md) | Insufficient Type Distinction | Base | Draft | Allowed |
| [CWE-352](weaknesses/CWE-352.md) | Cross-Site Request Forgery (CSRF) | Compound | Stable | Allowed |
| [CWE-353](weaknesses/CWE-353.md) | Missing Support for Integrity Check | Base | Draft | Allowed |
| [CWE-354](weaknesses/CWE-354.md) | Improper Validation of Integrity Check Value | Base | Draft | Allowed |
| [CWE-356](weaknesses/CWE-356.md) | Product UI does not Warn User of Unsafe Actions | Base | Incomplete | Allowed |
| [CWE-357](weaknesses/CWE-357.md) | Insufficient UI Warning of Dangerous Operations | Base | Draft | Allowed |
| [CWE-358](weaknesses/CWE-358.md) | Improperly Implemented Security Check for Standard | Base | Draft | Allowed |
| [CWE-359](weaknesses/CWE-359.md) | Exposure of Private Personal Information to an Unauthorized Actor | Base | Incomplete | Allowed |
| [CWE-360](weaknesses/CWE-360.md) | Trust of System Event Data | Base | Incomplete | Allowed |
| [CWE-362](weaknesses/CWE-362.md) | Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') | Class | Draft | Allowed-with-Review |
| [CWE-363](weaknesses/CWE-363.md) | Race Condition Enabling Link Following | Base | Draft | Allowed |
| [CWE-364](weaknesses/CWE-364.md) | Signal Handler Race Condition | Base | Incomplete | Allowed |
| [CWE-365](weaknesses/CWE-365.md) | DEPRECATED: Race Condition in Switch | Base | Deprecated | Prohibited |
| [CWE-366](weaknesses/CWE-366.md) | Race Condition within a Thread | Base | Draft | Allowed |
| [CWE-367](weaknesses/CWE-367.md) | Time-of-check Time-of-use (TOCTOU) Race Condition | Base | Incomplete | Allowed |
| [CWE-368](weaknesses/CWE-368.md) | Context Switching Race Condition | Base | Draft | Allowed |
| [CWE-369](weaknesses/CWE-369.md) | Divide By Zero | Base | Draft | Allowed |
| [CWE-370](weaknesses/CWE-370.md) | Missing Check for Certificate Revocation after Initial Check | Variant | Draft | Allowed |
| [CWE-372](weaknesses/CWE-372.md) | Incomplete Internal State Distinction | Base | Draft | Discouraged |
| [CWE-373](weaknesses/CWE-373.md) | DEPRECATED: State Synchronization Error | Base | Deprecated | Prohibited |
| [CWE-374](weaknesses/CWE-374.md) | Passing Mutable Objects to an Untrusted Method | Base | Draft | Allowed |
| [CWE-375](weaknesses/CWE-375.md) | Returning a Mutable Object to an Untrusted Caller | Base | Draft | Allowed |
| [CWE-377](weaknesses/CWE-377.md) | Insecure Temporary File | Class | Incomplete | Allowed-with-Review |
| [CWE-378](weaknesses/CWE-378.md) | Creation of Temporary File With Insecure Permissions | Base | Draft | Allowed |
| [CWE-379](weaknesses/CWE-379.md) | Creation of Temporary File in Directory with Insecure Permissions | Base | Incomplete | Allowed |
| [CWE-382](weaknesses/CWE-382.md) | J2EE Bad Practices: Use of System.exit() | Variant | Draft | Allowed |
| [CWE-383](weaknesses/CWE-383.md) | J2EE Bad Practices: Direct Use of Threads | Variant | Draft | Allowed |
| [CWE-384](weaknesses/CWE-384.md) | Session Fixation | Compound | Incomplete | Allowed |
| [CWE-385](weaknesses/CWE-385.md) | Covert Timing Channel | Base | Incomplete | Allowed |
| [CWE-386](weaknesses/CWE-386.md) | Symbolic Name not Mapping to Correct Object | Base | Draft | Allowed |
| [CWE-390](weaknesses/CWE-390.md) | Detection of Error Condition Without Action | Base | Draft | Allowed |
| [CWE-391](weaknesses/CWE-391.md) | Unchecked Error Condition | Base | Incomplete | Prohibited |
| [CWE-392](weaknesses/CWE-392.md) | Missing Report of Error Condition | Base | Draft | Allowed |
| [CWE-393](weaknesses/CWE-393.md) | Return of Wrong Status Code | Base | Draft | Allowed |
| [CWE-394](weaknesses/CWE-394.md) | Unexpected Status Code or Return Value | Base | Draft | Allowed |
| [CWE-395](weaknesses/CWE-395.md) | Use of NullPointerException Catch to Detect NULL Pointer Dereference | Base | Draft | Allowed |
| [CWE-396](weaknesses/CWE-396.md) | Declaration of Catch for Generic Exception | Base | Draft | Allowed |
| [CWE-397](weaknesses/CWE-397.md) | Declaration of Throws for Generic Exception | Base | Draft | Allowed |
| [CWE-400](weaknesses/CWE-400.md) | Uncontrolled Resource Consumption | Class | Draft | Discouraged |
| [CWE-401](weaknesses/CWE-401.md) | Missing Release of Memory after Effective Lifetime | Variant | Draft | Allowed |
| [CWE-402](weaknesses/CWE-402.md) | Transmission of Private Resources into a New Sphere ('Resource Leak') | Class | Draft | Allowed-with-Review |
| [CWE-403](weaknesses/CWE-403.md) | Exposure of File Descriptor to Unintended Control Sphere ('File Descriptor Leak') | Base | Draft | Allowed |
| [CWE-404](weaknesses/CWE-404.md) | Improper Resource Shutdown or Release | Class | Draft | Allowed-with-Review |
| [CWE-405](weaknesses/CWE-405.md) | Asymmetric Resource Consumption (Amplification) | Class | Incomplete | Allowed-with-Review |
| [CWE-406](weaknesses/CWE-406.md) | Insufficient Control of Network Message Volume (Network Amplification) | Class | Incomplete | Allowed-with-Review |
| [CWE-407](weaknesses/CWE-407.md) | Inefficient Algorithmic Complexity | Class | Incomplete | Allowed-with-Review |
| [CWE-408](weaknesses/CWE-408.md) | Incorrect Behavior Order: Early Amplification | Base | Draft | Allowed |
| [CWE-409](weaknesses/CWE-409.md) | Improper Handling of Highly Compressed Data (Data Amplification) | Base | Incomplete | Allowed |
| [CWE-410](weaknesses/CWE-410.md) | Insufficient Resource Pool | Class | Incomplete | Allowed |
| [CWE-412](weaknesses/CWE-412.md) | Unrestricted Externally Accessible Lock | Base | Incomplete | Allowed |
| [CWE-413](weaknesses/CWE-413.md) | Improper Resource Locking | Base | Draft | Allowed |
| [CWE-414](weaknesses/CWE-414.md) | Missing Lock Check | Base | Draft | Allowed |
| [CWE-415](weaknesses/CWE-415.md) | Double Free | Variant | Draft | Allowed |
| [CWE-416](weaknesses/CWE-416.md) | Use After Free | Variant | Stable | Allowed |
| [CWE-419](weaknesses/CWE-419.md) | Unprotected Primary Channel | Base | Draft | Allowed |
| [CWE-420](weaknesses/CWE-420.md) | Unprotected Alternate Channel | Base | Draft | Allowed |
| [CWE-421](weaknesses/CWE-421.md) | Race Condition During Access to Alternate Channel | Base | Draft | Allowed |
| [CWE-422](weaknesses/CWE-422.md) | Unprotected Windows Messaging Channel ('Shatter') | Variant | Draft | Allowed |
| [CWE-423](weaknesses/CWE-423.md) | DEPRECATED: Proxied Trusted Channel | Base | Deprecated | Prohibited |
| [CWE-424](weaknesses/CWE-424.md) | Improper Protection of Alternate Path | Class | Draft | Allowed-with-Review |
| [CWE-425](weaknesses/CWE-425.md) | Direct Request ('Forced Browsing') | Base | Incomplete | Allowed |
| [CWE-426](weaknesses/CWE-426.md) | Untrusted Search Path | Base | Stable | Allowed-with-Review |
| [CWE-427](weaknesses/CWE-427.md) | Uncontrolled Search Path Element | Base | Draft | Allowed-with-Review |
| [CWE-428](weaknesses/CWE-428.md) | Unquoted Search Path or Element | Base | Draft | Allowed |
| [CWE-430](weaknesses/CWE-430.md) | Deployment of Wrong Handler | Base | Incomplete | Allowed |
| [CWE-431](weaknesses/CWE-431.md) | Missing Handler | Base | Draft | Allowed |
| [CWE-432](weaknesses/CWE-432.md) | Dangerous Signal Handler not Disabled During Sensitive Operations | Base | Draft | Allowed |
| [CWE-433](weaknesses/CWE-433.md) | Unparsed Raw Web Content Delivery | Variant | Incomplete | Allowed |
| [CWE-434](weaknesses/CWE-434.md) | Unrestricted Upload of File with Dangerous Type | Base | Draft | Allowed |
| [CWE-435](weaknesses/CWE-435.md) | Improper Interaction Between Multiple Correctly-Behaving Entities | Pillar | Draft | Discouraged |
| [CWE-436](weaknesses/CWE-436.md) | Interpretation Conflict | Class | Incomplete | Allowed-with-Review |
| [CWE-437](weaknesses/CWE-437.md) | Incomplete Model of Endpoint Features | Base | Incomplete | Allowed |
| [CWE-439](weaknesses/CWE-439.md) | Behavioral Change in New Version or Environment | Base | Draft | Allowed |
| [CWE-440](weaknesses/CWE-440.md) | Expected Behavior Violation | Base | Draft | Allowed |
| [CWE-441](weaknesses/CWE-441.md) | Unintended Proxy or Intermediary ('Confused Deputy') | Class | Draft | Allowed-with-Review |
| [CWE-443](weaknesses/CWE-443.md) | DEPRECATED: HTTP response splitting | Base | Deprecated | Prohibited |
| [CWE-444](weaknesses/CWE-444.md) | Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling') | Base | Incomplete | Allowed |
| [CWE-446](weaknesses/CWE-446.md) | UI Discrepancy for Security Feature | Class | Incomplete | Allowed-with-Review |
| [CWE-447](weaknesses/CWE-447.md) | Unimplemented or Unsupported Feature in UI | Base | Draft | Allowed |
| [CWE-448](weaknesses/CWE-448.md) | Obsolete Feature in UI | Base | Draft | Allowed |
| [CWE-449](weaknesses/CWE-449.md) | The UI Performs the Wrong Action | Base | Incomplete | Allowed |
| [CWE-450](weaknesses/CWE-450.md) | Multiple Interpretations of UI Input | Base | Draft | Allowed |
| [CWE-451](weaknesses/CWE-451.md) | User Interface (UI) Misrepresentation of Critical Information | Class | Draft | Allowed-with-Review |
| [CWE-453](weaknesses/CWE-453.md) | Insecure Default Variable Initialization | Variant | Draft | Allowed |
| [CWE-454](weaknesses/CWE-454.md) | External Initialization of Trusted Variables or Data Stores | Base | Draft | Allowed |
| [CWE-455](weaknesses/CWE-455.md) | Non-exit on Failed Initialization | Base | Draft | Allowed |
| [CWE-456](weaknesses/CWE-456.md) | Missing Initialization of a Variable | Variant | Draft | Allowed |
| [CWE-457](weaknesses/CWE-457.md) | Use of Uninitialized Variable | Variant | Draft | Allowed |
| [CWE-458](weaknesses/CWE-458.md) | DEPRECATED: Incorrect Initialization | Base | Deprecated | Prohibited |
| [CWE-459](weaknesses/CWE-459.md) | Incomplete Cleanup | Base | Draft | Allowed |
| [CWE-460](weaknesses/CWE-460.md) | Improper Cleanup on Thrown Exception | Base | Draft | Allowed |
| [CWE-462](weaknesses/CWE-462.md) | Duplicate Key in Associative List (Alist) | Variant | Incomplete | Allowed |
| [CWE-463](weaknesses/CWE-463.md) | Deletion of Data Structure Sentinel | Base | Incomplete | Allowed |
| [CWE-464](weaknesses/CWE-464.md) | Addition of Data Structure Sentinel | Base | Incomplete | Allowed |
| [CWE-466](weaknesses/CWE-466.md) | Return of Pointer Value Outside of Expected Range | Base | Draft | Allowed |
| [CWE-467](weaknesses/CWE-467.md) | Use of sizeof() on a Pointer Type | Variant | Draft | Allowed |
| [CWE-468](weaknesses/CWE-468.md) | Incorrect Pointer Scaling | Base | Incomplete | Allowed |
| [CWE-469](weaknesses/CWE-469.md) | Use of Pointer Subtraction to Determine Size | Base | Draft | Allowed |
| [CWE-470](weaknesses/CWE-470.md) | Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection') | Base | Draft | Allowed |
| [CWE-471](weaknesses/CWE-471.md) | Modification of Assumed-Immutable Data (MAID) | Base | Draft | Allowed |
| [CWE-472](weaknesses/CWE-472.md) | External Control of Assumed-Immutable Web Parameter | Base | Draft | Allowed |
| [CWE-473](weaknesses/CWE-473.md) | PHP External Variable Modification | Variant | Draft | Allowed |
| [CWE-474](weaknesses/CWE-474.md) | Use of Function with Inconsistent Implementations | Base | Draft | Allowed |
| [CWE-475](weaknesses/CWE-475.md) | Undefined Behavior for Input to API | Base | Incomplete | Allowed |
| [CWE-476](weaknesses/CWE-476.md) | NULL Pointer Dereference | Base | Stable | Allowed |
| [CWE-477](weaknesses/CWE-477.md) | Use of Obsolete Function | Base | Draft | Allowed |
| [CWE-478](weaknesses/CWE-478.md) | Missing Default Case in Multiple Condition Expression | Base | Draft | Allowed |
| [CWE-479](weaknesses/CWE-479.md) | Signal Handler Use of a Non-reentrant Function | Variant | Draft | Allowed |
| [CWE-480](weaknesses/CWE-480.md) | Use of Incorrect Operator | Base | Draft | Allowed |
| [CWE-481](weaknesses/CWE-481.md) | Assigning instead of Comparing | Variant | Draft | Allowed |
| [CWE-482](weaknesses/CWE-482.md) | Comparing instead of Assigning | Variant | Draft | Allowed |
| [CWE-483](weaknesses/CWE-483.md) | Incorrect Block Delimitation | Base | Draft | Allowed |
| [CWE-484](weaknesses/CWE-484.md) | Omitted Break Statement in Switch | Base | Draft | Allowed |
| [CWE-486](weaknesses/CWE-486.md) | Comparison of Classes by Name | Variant | Draft | Allowed |
| [CWE-487](weaknesses/CWE-487.md) | Reliance on Package-level Scope | Base | Incomplete | Allowed |
| [CWE-488](weaknesses/CWE-488.md) | Exposure of Data Element to Wrong Session | Base | Draft | Allowed |
| [CWE-489](weaknesses/CWE-489.md) | Active Debug Code | Base | Draft | Allowed |
| [CWE-491](weaknesses/CWE-491.md) | Public cloneable() Method Without Final ('Object Hijack') | Variant | Draft | Allowed |
| [CWE-492](weaknesses/CWE-492.md) | Use of Inner Class Containing Sensitive Data | Variant | Draft | Allowed |
| [CWE-493](weaknesses/CWE-493.md) | Critical Public Variable Without Final Modifier | Variant | Draft | Allowed |
| [CWE-494](weaknesses/CWE-494.md) | Download of Code Without Integrity Check | Base | Draft | Allowed |
| [CWE-495](weaknesses/CWE-495.md) | Private Data Structure Returned From A Public Method | Variant | Draft | Allowed |
| [CWE-496](weaknesses/CWE-496.md) | Public Data Assigned to Private Array-Typed Field | Variant | Incomplete | Allowed |
| [CWE-497](weaknesses/CWE-497.md) | Exposure of Sensitive System Information to an Unauthorized Control Sphere | Base | Incomplete | Allowed |
| [CWE-498](weaknesses/CWE-498.md) | Cloneable Class Containing Sensitive Information | Variant | Draft | Allowed |
| [CWE-499](weaknesses/CWE-499.md) | Serializable Class Containing Sensitive Data | Variant | Draft | Allowed |
| [CWE-500](weaknesses/CWE-500.md) | Public Static Field Not Marked Final | Variant | Draft | Allowed |
| [CWE-501](weaknesses/CWE-501.md) | Trust Boundary Violation | Base | Draft | Allowed |
| [CWE-502](weaknesses/CWE-502.md) | Deserialization of Untrusted Data | Base | Draft | Allowed |
| [CWE-506](weaknesses/CWE-506.md) | Embedded Malicious Code | Class | Incomplete | Allowed-with-Review |
| [CWE-507](weaknesses/CWE-507.md) | Trojan Horse | Base | Incomplete | Allowed |
| [CWE-508](weaknesses/CWE-508.md) | Non-Replicating Malicious Code | Base | Incomplete | Allowed |
| [CWE-509](weaknesses/CWE-509.md) | Replicating Malicious Code (Virus or Worm) | Base | Incomplete | Allowed |
| [CWE-510](weaknesses/CWE-510.md) | Trapdoor | Base | Incomplete | Allowed |
| [CWE-511](weaknesses/CWE-511.md) | Logic/Time Bomb | Base | Incomplete | Allowed |
| [CWE-512](weaknesses/CWE-512.md) | Spyware | Base | Incomplete | Allowed |
| [CWE-514](weaknesses/CWE-514.md) | Covert Channel | Class | Incomplete | Allowed-with-Review |
| [CWE-515](weaknesses/CWE-515.md) | Covert Storage Channel | Base | Incomplete | Allowed |
| [CWE-516](weaknesses/CWE-516.md) | DEPRECATED: Covert Timing Channel | Base | Deprecated | Prohibited |
| [CWE-520](weaknesses/CWE-520.md) | .NET Misconfiguration: Use of Impersonation | Variant | Incomplete | Allowed |
| [CWE-521](weaknesses/CWE-521.md) | Weak Password Requirements | Base | Draft | Allowed |
| [CWE-522](weaknesses/CWE-522.md) | Insufficiently Protected Credentials | Class | Incomplete | Allowed-with-Review |
| [CWE-523](weaknesses/CWE-523.md) | Unprotected Transport of Credentials | Base | Incomplete | Allowed |
| [CWE-524](weaknesses/CWE-524.md) | Use of Cache Containing Sensitive Information | Base | Incomplete | Allowed |
| [CWE-525](weaknesses/CWE-525.md) | Use of Web Browser Cache Containing Sensitive Information | Variant | Incomplete | Allowed |
| [CWE-526](weaknesses/CWE-526.md) | Cleartext Storage of Sensitive Information in an Environment Variable | Variant | Incomplete | Allowed |
| [CWE-527](weaknesses/CWE-527.md) | Exposure of Version-Control Repository to an Unauthorized Control Sphere | Variant | Incomplete | Allowed |
| [CWE-528](weaknesses/CWE-528.md) | Exposure of Core Dump File to an Unauthorized Control Sphere | Variant | Draft | Allowed |
| [CWE-529](weaknesses/CWE-529.md) | Exposure of Access Control List Files to an Unauthorized Control Sphere | Variant | Incomplete | Allowed |
| [CWE-530](weaknesses/CWE-530.md) | Exposure of Backup File to an Unauthorized Control Sphere | Variant | Incomplete | Allowed |
| [CWE-531](weaknesses/CWE-531.md) | Inclusion of Sensitive Information in Test Code | Variant | Incomplete | Allowed |
| [CWE-532](weaknesses/CWE-532.md) | Insertion of Sensitive Information into Log File | Base | Incomplete | Allowed |
| [CWE-533](weaknesses/CWE-533.md) | DEPRECATED: Information Exposure Through Server Log Files | Variant | Deprecated | Prohibited |
| [CWE-534](weaknesses/CWE-534.md) | DEPRECATED: Information Exposure Through Debug Log Files | Variant | Deprecated | Prohibited |
| [CWE-535](weaknesses/CWE-535.md) | Exposure of Information Through Shell Error Message | Variant | Incomplete | Allowed |
| [CWE-536](weaknesses/CWE-536.md) | Servlet Runtime Error Message Containing Sensitive Information | Variant | Incomplete | Allowed |
| [CWE-537](weaknesses/CWE-537.md) | Java Runtime Error Message Containing Sensitive Information | Variant | Incomplete | Allowed |
| [CWE-538](weaknesses/CWE-538.md) | Insertion of Sensitive Information into Externally-Accessible File or Directory | Base | Draft | Allowed |
| [CWE-539](weaknesses/CWE-539.md) | Use of Persistent Cookies Containing Sensitive Information | Variant | Incomplete | Allowed |
| [CWE-540](weaknesses/CWE-540.md) | Inclusion of Sensitive Information in Source Code | Base | Incomplete | Allowed |
| [CWE-541](weaknesses/CWE-541.md) | Inclusion of Sensitive Information in an Include File | Variant | Incomplete | Allowed |
| [CWE-542](weaknesses/CWE-542.md) | DEPRECATED: Information Exposure Through Cleanup Log Files | Variant | Deprecated | Prohibited |
| [CWE-543](weaknesses/CWE-543.md) | Use of Singleton Pattern Without Synchronization in a Multithreaded Context | Variant | Incomplete | Allowed |
| [CWE-544](weaknesses/CWE-544.md) | Missing Standardized Error Handling Mechanism | Base | Draft | Allowed |
| [CWE-545](weaknesses/CWE-545.md) | DEPRECATED: Use of Dynamic Class Loading | Variant | Deprecated | Prohibited |
| [CWE-546](weaknesses/CWE-546.md) | Suspicious Comment | Variant | Draft | Allowed |
| [CWE-547](weaknesses/CWE-547.md) | Use of Hard-coded, Security-relevant Constants | Base | Draft | Allowed |
| [CWE-548](weaknesses/CWE-548.md) | Exposure of Information Through Directory Listing | Variant | Draft | Allowed |
| [CWE-549](weaknesses/CWE-549.md) | Missing Password Field Masking | Base | Draft | Allowed |
| [CWE-550](weaknesses/CWE-550.md) | Server-generated Error Message Containing Sensitive Information | Variant | Incomplete | Allowed |
| [CWE-551](weaknesses/CWE-551.md) | Incorrect Behavior Order: Authorization Before Parsing and Canonicalization | Base | Incomplete | Allowed |
| [CWE-552](weaknesses/CWE-552.md) | Files or Directories Accessible to External Parties | Base | Draft | Allowed |
| [CWE-553](weaknesses/CWE-553.md) | Command Shell in Externally Accessible Directory | Variant | Incomplete | Allowed |
| [CWE-554](weaknesses/CWE-554.md) | ASP.NET Misconfiguration: Not Using Input Validation Framework | Variant | Draft | Allowed |
| [CWE-555](weaknesses/CWE-555.md) | J2EE Misconfiguration: Plaintext Password in Configuration File | Variant | Draft | Allowed |
| [CWE-556](weaknesses/CWE-556.md) | ASP.NET Misconfiguration: Use of Identity Impersonation | Variant | Incomplete | Allowed |
| [CWE-558](weaknesses/CWE-558.md) | Use of getlogin() in Multithreaded Application | Variant | Draft | Allowed |
| [CWE-560](weaknesses/CWE-560.md) | Use of umask() with chmod-style Argument | Variant | Draft | Allowed |
| [CWE-561](weaknesses/CWE-561.md) | Dead Code | Base | Draft | Allowed |
| [CWE-562](weaknesses/CWE-562.md) | Return of Stack Variable Address | Base | Draft | Allowed |
| [CWE-563](weaknesses/CWE-563.md) | Assignment to Variable without Use | Base | Draft | Allowed |
| [CWE-564](weaknesses/CWE-564.md) | SQL Injection: Hibernate | Variant | Incomplete | Allowed |
| [CWE-565](weaknesses/CWE-565.md) | Reliance on Cookies without Validation and Integrity Checking | Base | Incomplete | Allowed |
| [CWE-566](weaknesses/CWE-566.md) | Authorization Bypass Through User-Controlled SQL Primary Key | Variant | Incomplete | Allowed |
| [CWE-567](weaknesses/CWE-567.md) | Unsynchronized Access to Shared Data in a Multithreaded Context | Base | Draft | Allowed |
| [CWE-568](weaknesses/CWE-568.md) | finalize() Method Without super.finalize() | Variant | Draft | Allowed |
| [CWE-570](weaknesses/CWE-570.md) | Expression is Always False | Base | Draft | Allowed |
| [CWE-571](weaknesses/CWE-571.md) | Expression is Always True | Base | Draft | Allowed |
| [CWE-572](weaknesses/CWE-572.md) | Call to Thread run() instead of start() | Variant | Draft | Allowed |
| [CWE-573](weaknesses/CWE-573.md) | Improper Following of Specification by Caller | Class | Draft | Allowed-with-Review |
| [CWE-574](weaknesses/CWE-574.md) | EJB Bad Practices: Use of Synchronization Primitives | Variant | Draft | Allowed |
| [CWE-575](weaknesses/CWE-575.md) | EJB Bad Practices: Use of AWT Swing | Variant | Draft | Allowed |
| [CWE-576](weaknesses/CWE-576.md) | EJB Bad Practices: Use of Java I/O | Variant | Draft | Allowed |
| [CWE-577](weaknesses/CWE-577.md) | EJB Bad Practices: Use of Sockets | Variant | Draft | Allowed |
| [CWE-578](weaknesses/CWE-578.md) | EJB Bad Practices: Use of Class Loader | Variant | Draft | Allowed |
| [CWE-579](weaknesses/CWE-579.md) | J2EE Bad Practices: Non-serializable Object Stored in Session | Variant | Draft | Allowed |
| [CWE-580](weaknesses/CWE-580.md) | clone() Method Without super.clone() | Variant | Draft | Allowed |
| [CWE-581](weaknesses/CWE-581.md) | Object Model Violation: Just One of Equals and Hashcode Defined | Variant | Draft | Allowed |
| [CWE-582](weaknesses/CWE-582.md) | Array Declared Public, Final, and Static | Variant | Draft | Allowed |
| [CWE-583](weaknesses/CWE-583.md) | finalize() Method Declared Public | Variant | Incomplete | Allowed |
| [CWE-584](weaknesses/CWE-584.md) | Return Inside Finally Block | Base | Draft | Allowed |
| [CWE-585](weaknesses/CWE-585.md) | Empty Synchronized Block | Variant | Draft | Allowed |
| [CWE-586](weaknesses/CWE-586.md) | Explicit Call to Finalize() | Base | Draft | Allowed |
| [CWE-587](weaknesses/CWE-587.md) | Assignment of a Fixed Address to a Pointer | Variant | Draft | Allowed |
| [CWE-588](weaknesses/CWE-588.md) | Attempt to Access Child of a Non-structure Pointer | Variant | Incomplete | Allowed |
| [CWE-589](weaknesses/CWE-589.md) | Call to Non-ubiquitous API | Variant | Incomplete | Allowed |
| [CWE-590](weaknesses/CWE-590.md) | Free of Memory not on the Heap | Variant | Incomplete | Allowed |
| [CWE-591](weaknesses/CWE-591.md) | Sensitive Data Storage in Improperly Locked Memory | Variant | Draft | Allowed |
| [CWE-592](weaknesses/CWE-592.md) | DEPRECATED: Authentication Bypass Issues | Class | Deprecated | Prohibited |
| [CWE-593](weaknesses/CWE-593.md) | Authentication Bypass: OpenSSL CTX Object Modified after SSL Objects are Created | Variant | Draft | Allowed |
| [CWE-594](weaknesses/CWE-594.md) | J2EE Framework: Saving Unserializable Objects to Disk | Variant | Incomplete | Allowed |
| [CWE-595](weaknesses/CWE-595.md) | Comparison of Object References Instead of Object Contents | Variant | Incomplete | Allowed |
| [CWE-596](weaknesses/CWE-596.md) | DEPRECATED: Incorrect Semantic Object Comparison | Base | Deprecated | Prohibited |
| [CWE-597](weaknesses/CWE-597.md) | Use of Wrong Operator in String Comparison | Variant | Draft | Allowed |
| [CWE-598](weaknesses/CWE-598.md) | Use of GET Request Method With Sensitive Query Strings | Variant | Draft | Allowed |
| [CWE-599](weaknesses/CWE-599.md) | Missing Validation of OpenSSL Certificate | Variant | Incomplete | Allowed |
| [CWE-600](weaknesses/CWE-600.md) | Uncaught Exception in Servlet | Variant | Draft | Allowed |
| [CWE-601](weaknesses/CWE-601.md) | URL Redirection to Untrusted Site ('Open Redirect') | Base | Draft | Allowed |
| [CWE-602](weaknesses/CWE-602.md) | Client-Side Enforcement of Server-Side Security | Class | Draft | Allowed-with-Review |
| [CWE-603](weaknesses/CWE-603.md) | Use of Client-Side Authentication | Base | Draft | Allowed |
| [CWE-605](weaknesses/CWE-605.md) | Multiple Binds to the Same Port | Variant | Draft | Allowed |
| [CWE-606](weaknesses/CWE-606.md) | Unchecked Input for Loop Condition | Base | Draft | Allowed |
| [CWE-607](weaknesses/CWE-607.md) | Public Static Final Field References Mutable Object | Variant | Draft | Allowed |
| [CWE-608](weaknesses/CWE-608.md) | Struts: Non-private Field in ActionForm Class | Variant | Draft | Allowed |
| [CWE-609](weaknesses/CWE-609.md) | Double-Checked Locking | Base | Draft | Allowed |
| [CWE-610](weaknesses/CWE-610.md) | Externally Controlled Reference to a Resource in Another Sphere | Class | Draft | Discouraged |
| [CWE-611](weaknesses/CWE-611.md) | Improper Restriction of XML External Entity Reference | Base | Draft | Allowed |
| [CWE-612](weaknesses/CWE-612.md) | Improper Authorization of Index Containing Sensitive Information | Base | Draft | Allowed |
| [CWE-613](weaknesses/CWE-613.md) | Insufficient Session Expiration | Base | Incomplete | Allowed |
| [CWE-614](weaknesses/CWE-614.md) | Sensitive Cookie in HTTPS Session Without 'Secure' Attribute | Variant | Draft | Allowed |
| [CWE-615](weaknesses/CWE-615.md) | Inclusion of Sensitive Information in Source Code Comments | Variant | Incomplete | Allowed |
| [CWE-616](weaknesses/CWE-616.md) | Incomplete Identification of Uploaded File Variables (PHP) | Variant | Incomplete | Allowed |
| [CWE-617](weaknesses/CWE-617.md) | Reachable Assertion | Base | Draft | Allowed |
| [CWE-618](weaknesses/CWE-618.md) | Exposed Unsafe ActiveX Method | Variant | Incomplete | Allowed |
| [CWE-619](weaknesses/CWE-619.md) | Dangling Database Cursor ('Cursor Injection') | Base | Incomplete | Allowed |
| [CWE-620](weaknesses/CWE-620.md) | Unverified Password Change | Base | Draft | Allowed |
| [CWE-621](weaknesses/CWE-621.md) | Variable Extraction Error | Variant | Incomplete | Allowed |
| [CWE-622](weaknesses/CWE-622.md) | Improper Validation of Function Hook Arguments | Variant | Draft | Allowed |
| [CWE-623](weaknesses/CWE-623.md) | Unsafe ActiveX Control Marked Safe For Scripting | Variant | Draft | Allowed |
| [CWE-624](weaknesses/CWE-624.md) | Executable Regular Expression Error | Base | Incomplete | Allowed |
| [CWE-625](weaknesses/CWE-625.md) | Permissive Regular Expression | Base | Draft | Allowed |
| [CWE-626](weaknesses/CWE-626.md) | Null Byte Interaction Error (Poison Null Byte) | Variant | Draft | Allowed |
| [CWE-627](weaknesses/CWE-627.md) | Dynamic Variable Evaluation | Variant | Incomplete | Allowed |
| [CWE-628](weaknesses/CWE-628.md) | Function Call with Incorrectly Specified Arguments | Base | Draft | Allowed |
| [CWE-636](weaknesses/CWE-636.md) | Not Failing Securely ('Failing Open') | Class | Draft | Allowed-with-Review |
| [CWE-637](weaknesses/CWE-637.md) | Unnecessary Complexity in Protection Mechanism (Not Using 'Economy of Mechanism') | Class | Draft | Allowed-with-Review |
| [CWE-638](weaknesses/CWE-638.md) | Not Using Complete Mediation | Class | Draft | Allowed-with-Review |
| [CWE-639](weaknesses/CWE-639.md) | Authorization Bypass Through User-Controlled Key | Base | Incomplete | Allowed |
| [CWE-640](weaknesses/CWE-640.md) | Weak Password Recovery Mechanism for Forgotten Password | Base | Incomplete | Allowed-with-Review |
| [CWE-641](weaknesses/CWE-641.md) | Improper Restriction of Names for Files and Other Resources | Base | Incomplete | Allowed |
| [CWE-642](weaknesses/CWE-642.md) | External Control of Critical State Data | Class | Draft | Allowed-with-Review |
| [CWE-643](weaknesses/CWE-643.md) | Improper Neutralization of Data within XPath Expressions ('XPath Injection') | Base | Incomplete | Allowed |
| [CWE-644](weaknesses/CWE-644.md) | Improper Neutralization of HTTP Headers for Scripting Syntax | Variant | Incomplete | Allowed |
| [CWE-645](weaknesses/CWE-645.md) | Overly Restrictive Account Lockout Mechanism | Base | Incomplete | Allowed |
| [CWE-646](weaknesses/CWE-646.md) | Reliance on File Name or Extension of Externally-Supplied File | Variant | Incomplete | Allowed |
| [CWE-647](weaknesses/CWE-647.md) | Use of Non-Canonical URL Paths for Authorization Decisions | Variant | Incomplete | Allowed |
| [CWE-648](weaknesses/CWE-648.md) | Incorrect Use of Privileged APIs | Base | Incomplete | Allowed |
| [CWE-649](weaknesses/CWE-649.md) | Reliance on Obfuscation or Encryption of Security-Relevant Inputs without Integrity Checking | Base | Incomplete | Allowed |
| [CWE-650](weaknesses/CWE-650.md) | Trusting HTTP Permission Methods on the Server Side | Variant | Incomplete | Allowed |
| [CWE-651](weaknesses/CWE-651.md) | Exposure of WSDL File Containing Sensitive Information | Variant | Incomplete | Allowed |
| [CWE-652](weaknesses/CWE-652.md) | Improper Neutralization of Data within XQuery Expressions ('XQuery Injection') | Base | Incomplete | Allowed |
| [CWE-653](weaknesses/CWE-653.md) | Improper Isolation or Compartmentalization | Class | Draft | Allowed |
| [CWE-654](weaknesses/CWE-654.md) | Reliance on a Single Factor in a Security Decision | Base | Draft | Allowed |
| [CWE-655](weaknesses/CWE-655.md) | Insufficient Psychological Acceptability | Class | Draft | Allowed-with-Review |
| [CWE-656](weaknesses/CWE-656.md) | Reliance on Security Through Obscurity | Class | Draft | Allowed-with-Review |
| [CWE-657](weaknesses/CWE-657.md) | Violation of Secure Design Principles | Class | Draft | Discouraged |
| [CWE-662](weaknesses/CWE-662.md) | Improper Synchronization | Class | Draft | Discouraged |
| [CWE-663](weaknesses/CWE-663.md) | Use of a Non-reentrant Function in a Concurrent Context | Base | Draft | Allowed |
| [CWE-664](weaknesses/CWE-664.md) | Improper Control of a Resource Through its Lifetime | Pillar | Draft | Discouraged |
| [CWE-665](weaknesses/CWE-665.md) | Improper Initialization | Class | Draft | Discouraged |
| [CWE-666](weaknesses/CWE-666.md) | Operation on Resource in Wrong Phase of Lifetime | Class | Draft | Discouraged |
| [CWE-667](weaknesses/CWE-667.md) | Improper Locking | Class | Draft | Allowed-with-Review |
| [CWE-668](weaknesses/CWE-668.md) | Exposure of Resource to Wrong Sphere | Class | Draft | Discouraged |
| [CWE-669](weaknesses/CWE-669.md) | Incorrect Resource Transfer Between Spheres | Class | Draft | Allowed-with-Review |
| [CWE-670](weaknesses/CWE-670.md) | Always-Incorrect Control Flow Implementation | Class | Draft | Allowed-with-Review |
| [CWE-671](weaknesses/CWE-671.md) | Lack of Administrator Control over Security | Class | Draft | Allowed-with-Review |
| [CWE-672](weaknesses/CWE-672.md) | Operation on a Resource after Expiration or Release | Class | Draft | Allowed-with-Review |
| [CWE-673](weaknesses/CWE-673.md) | External Influence of Sphere Definition | Class | Draft | Allowed-with-Review |
| [CWE-674](weaknesses/CWE-674.md) | Uncontrolled Recursion | Class | Draft | Allowed-with-Review |
| [CWE-675](weaknesses/CWE-675.md) | Multiple Operations on Resource in Single-Operation Context | Class | Draft | Allowed-with-Review |
| [CWE-676](weaknesses/CWE-676.md) | Use of Potentially Dangerous Function | Base | Draft | Allowed |
| [CWE-680](weaknesses/CWE-680.md) | Integer Overflow to Buffer Overflow | Compound | Draft | Discouraged |
| [CWE-681](weaknesses/CWE-681.md) | Incorrect Conversion between Numeric Types | Base | Draft | Allowed |
| [CWE-682](weaknesses/CWE-682.md) | Incorrect Calculation | Pillar | Draft | Discouraged |
| [CWE-683](weaknesses/CWE-683.md) | Function Call With Incorrect Order of Arguments | Variant | Draft | Allowed |
| [CWE-684](weaknesses/CWE-684.md) | Incorrect Provision of Specified Functionality | Class | Draft | Allowed-with-Review |
| [CWE-685](weaknesses/CWE-685.md) | Function Call With Incorrect Number of Arguments | Variant | Draft | Allowed |
| [CWE-686](weaknesses/CWE-686.md) | Function Call With Incorrect Argument Type | Variant | Draft | Allowed |
| [CWE-687](weaknesses/CWE-687.md) | Function Call With Incorrectly Specified Argument Value | Variant | Draft | Allowed |
| [CWE-688](weaknesses/CWE-688.md) | Function Call With Incorrect Variable or Reference as Argument | Variant | Draft | Allowed |
| [CWE-689](weaknesses/CWE-689.md) | Permission Race Condition During Resource Copy | Compound | Draft | Allowed |
| [CWE-690](weaknesses/CWE-690.md) | Unchecked Return Value to NULL Pointer Dereference | Compound | Draft | Discouraged |
| [CWE-691](weaknesses/CWE-691.md) | Insufficient Control Flow Management | Pillar | Draft | Discouraged |
| [CWE-692](weaknesses/CWE-692.md) | Incomplete Denylist to Cross-Site Scripting | Compound | Draft | Discouraged |
| [CWE-693](weaknesses/CWE-693.md) | Protection Mechanism Failure | Pillar | Draft | Discouraged |
| [CWE-694](weaknesses/CWE-694.md) | Use of Multiple Resources with Duplicate Identifier | Base | Incomplete | Allowed |
| [CWE-695](weaknesses/CWE-695.md) | Use of Low-Level Functionality | Base | Incomplete | Allowed |
| [CWE-696](weaknesses/CWE-696.md) | Incorrect Behavior Order | Class | Incomplete | Allowed-with-Review |
| [CWE-697](weaknesses/CWE-697.md) | Incorrect Comparison | Pillar | Incomplete | Discouraged |
| [CWE-698](weaknesses/CWE-698.md) | Execution After Redirect (EAR) | Base | Incomplete | Allowed |
| [CWE-703](weaknesses/CWE-703.md) | Improper Check or Handling of Exceptional Conditions | Pillar | Incomplete | Discouraged |
| [CWE-704](weaknesses/CWE-704.md) | Incorrect Type Conversion or Cast | Class | Incomplete | Allowed-with-Review |
| [CWE-705](weaknesses/CWE-705.md) | Incorrect Control Flow Scoping | Class | Incomplete | Allowed-with-Review |
| [CWE-706](weaknesses/CWE-706.md) | Use of Incorrectly-Resolved Name or Reference | Class | Incomplete | Allowed-with-Review |
| [CWE-707](weaknesses/CWE-707.md) | Improper Neutralization | Pillar | Incomplete | Discouraged |
| [CWE-708](weaknesses/CWE-708.md) | Incorrect Ownership Assignment | Base | Incomplete | Allowed |
| [CWE-710](weaknesses/CWE-710.md) | Improper Adherence to Coding Standards | Pillar | Incomplete | Discouraged |
| [CWE-732](weaknesses/CWE-732.md) | Incorrect Permission Assignment for Critical Resource | Class | Draft | Allowed-with-Review |
| [CWE-733](weaknesses/CWE-733.md) | Compiler Optimization Removal or Modification of Security-critical Code | Base | Incomplete | Allowed |
| [CWE-749](weaknesses/CWE-749.md) | Exposed Dangerous Method or Function | Base | Incomplete | Allowed |
| [CWE-754](weaknesses/CWE-754.md) | Improper Check for Unusual or Exceptional Conditions | Class | Incomplete | Allowed-with-Review |
| [CWE-755](weaknesses/CWE-755.md) | Improper Handling of Exceptional Conditions | Class | Incomplete | Discouraged |
| [CWE-756](weaknesses/CWE-756.md) | Missing Custom Error Page | Base | Incomplete | Allowed |
| [CWE-757](weaknesses/CWE-757.md) | Selection of Less-Secure Algorithm During Negotiation ('Algorithm Downgrade') | Base | Incomplete | Allowed |
| [CWE-758](weaknesses/CWE-758.md) | Reliance on Undefined, Unspecified, or Implementation-Defined Behavior | Class | Incomplete | Allowed-with-Review |
| [CWE-759](weaknesses/CWE-759.md) | Use of a One-Way Hash without a Salt | Variant | Incomplete | Allowed |
| [CWE-760](weaknesses/CWE-760.md) | Use of a One-Way Hash with a Predictable Salt | Variant | Incomplete | Allowed |
| [CWE-761](weaknesses/CWE-761.md) | Free of Pointer not at Start of Buffer | Variant | Incomplete | Allowed |
| [CWE-762](weaknesses/CWE-762.md) | Mismatched Memory Management Routines | Variant | Incomplete | Allowed |
| [CWE-763](weaknesses/CWE-763.md) | Release of Invalid Pointer or Reference | Base | Incomplete | Allowed |
| [CWE-764](weaknesses/CWE-764.md) | Multiple Locks of a Critical Resource | Base | Incomplete | Allowed |
| [CWE-765](weaknesses/CWE-765.md) | Multiple Unlocks of a Critical Resource | Base | Incomplete | Allowed |
| [CWE-766](weaknesses/CWE-766.md) | Critical Data Element Declared Public | Base | Incomplete | Allowed |
| [CWE-767](weaknesses/CWE-767.md) | Access to Critical Private Variable via Public Method | Base | Incomplete | Allowed |
| [CWE-768](weaknesses/CWE-768.md) | Incorrect Short Circuit Evaluation | Variant | Incomplete | Allowed |
| [CWE-769](weaknesses/CWE-769.md) | DEPRECATED: Uncontrolled File Descriptor Consumption | Base | Deprecated | Prohibited |
| [CWE-770](weaknesses/CWE-770.md) | Allocation of Resources Without Limits or Throttling | Base | Incomplete | Allowed |
| [CWE-771](weaknesses/CWE-771.md) | Missing Reference to Active Allocated Resource | Base | Incomplete | Allowed |
| [CWE-772](weaknesses/CWE-772.md) | Missing Release of Resource after Effective Lifetime | Base | Draft | Allowed |
| [CWE-773](weaknesses/CWE-773.md) | Missing Reference to Active File Descriptor or Handle | Variant | Incomplete | Allowed |
| [CWE-774](weaknesses/CWE-774.md) | Allocation of File Descriptors or Handles Without Limits or Throttling | Variant | Incomplete | Allowed |
| [CWE-775](weaknesses/CWE-775.md) | Missing Release of File Descriptor or Handle after Effective Lifetime | Variant | Incomplete | Allowed |
| [CWE-776](weaknesses/CWE-776.md) | Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion') | Base | Draft | Allowed |
| [CWE-777](weaknesses/CWE-777.md) | Regular Expression without Anchors | Variant | Incomplete | Allowed |
| [CWE-778](weaknesses/CWE-778.md) | Insufficient Logging | Base | Draft | Allowed |
| [CWE-779](weaknesses/CWE-779.md) | Logging of Excessive Data | Base | Draft | Allowed |
| [CWE-780](weaknesses/CWE-780.md) | Use of RSA Algorithm without OAEP | Variant | Incomplete | Allowed |
| [CWE-781](weaknesses/CWE-781.md) | Improper Address Validation in IOCTL with METHOD_NEITHER I/O Control Code | Variant | Draft | Allowed |
| [CWE-782](weaknesses/CWE-782.md) | Exposed IOCTL with Insufficient Access Control | Variant | Draft | Allowed |
| [CWE-783](weaknesses/CWE-783.md) | Operator Precedence Logic Error | Base | Draft | Allowed |
| [CWE-784](weaknesses/CWE-784.md) | Reliance on Cookies without Validation and Integrity Checking in a Security Decision | Variant | Draft | Allowed |
| [CWE-785](weaknesses/CWE-785.md) | Use of Path Manipulation Function without Maximum-sized Buffer | Variant | Incomplete | Allowed |
| [CWE-786](weaknesses/CWE-786.md) | Access of Memory Location Before Start of Buffer | Base | Incomplete | Discouraged |
| [CWE-787](weaknesses/CWE-787.md) | Out-of-bounds Write | Base | Draft | Allowed |
| [CWE-788](weaknesses/CWE-788.md) | Access of Memory Location After End of Buffer | Base | Incomplete | Discouraged |
| [CWE-789](weaknesses/CWE-789.md) | Memory Allocation with Excessive Size Value | Variant | Draft | Allowed |
| [CWE-790](weaknesses/CWE-790.md) | Improper Filtering of Special Elements | Class | Incomplete | Allowed-with-Review |
| [CWE-791](weaknesses/CWE-791.md) | Incomplete Filtering of Special Elements | Base | Incomplete | Allowed |
| [CWE-792](weaknesses/CWE-792.md) | Incomplete Filtering of One or More Instances of Special Elements | Variant | Incomplete | Allowed |
| [CWE-793](weaknesses/CWE-793.md) | Only Filtering One Instance of a Special Element | Variant | Incomplete | Allowed |
| [CWE-794](weaknesses/CWE-794.md) | Incomplete Filtering of Multiple Instances of Special Elements | Variant | Incomplete | Allowed |
| [CWE-795](weaknesses/CWE-795.md) | Only Filtering Special Elements at a Specified Location | Base | Incomplete | Allowed |
| [CWE-796](weaknesses/CWE-796.md) | Only Filtering Special Elements Relative to a Marker | Variant | Incomplete | Allowed |
| [CWE-797](weaknesses/CWE-797.md) | Only Filtering Special Elements at an Absolute Position | Variant | Incomplete | Allowed |
| [CWE-798](weaknesses/CWE-798.md) | Use of Hard-coded Credentials | Base | Draft | Allowed-with-Review |
| [CWE-799](weaknesses/CWE-799.md) | Improper Control of Interaction Frequency | Class | Incomplete | Allowed-with-Review |
| [CWE-804](weaknesses/CWE-804.md) | Guessable CAPTCHA | Base | Incomplete | Allowed |
| [CWE-805](weaknesses/CWE-805.md) | Buffer Access with Incorrect Length Value | Base | Incomplete | Allowed |
| [CWE-806](weaknesses/CWE-806.md) | Buffer Access Using Size of Source Buffer | Variant | Incomplete | Allowed |
| [CWE-807](weaknesses/CWE-807.md) | Reliance on Untrusted Inputs in a Security Decision | Base | Incomplete | Allowed |
| [CWE-820](weaknesses/CWE-820.md) | Missing Synchronization | Base | Incomplete | Allowed |
| [CWE-821](weaknesses/CWE-821.md) | Incorrect Synchronization | Base | Incomplete | Allowed |
| [CWE-822](weaknesses/CWE-822.md) | Untrusted Pointer Dereference | Base | Incomplete | Allowed |
| [CWE-823](weaknesses/CWE-823.md) | Use of Out-of-range Pointer Offset | Base | Incomplete | Allowed |
| [CWE-824](weaknesses/CWE-824.md) | Access of Uninitialized Pointer | Base | Incomplete | Allowed |
| [CWE-825](weaknesses/CWE-825.md) | Expired Pointer Dereference | Base | Incomplete | Allowed |
| [CWE-826](weaknesses/CWE-826.md) | Premature Release of Resource During Expected Lifetime | Base | Incomplete | Allowed |
| [CWE-827](weaknesses/CWE-827.md) | Improper Control of Document Type Definition | Variant | Incomplete | Allowed |
| [CWE-828](weaknesses/CWE-828.md) | Signal Handler with Functionality that is not Asynchronous-Safe | Variant | Incomplete | Allowed |
| [CWE-829](weaknesses/CWE-829.md) | Inclusion of Functionality from Untrusted Control Sphere | Base | Incomplete | Allowed |
| [CWE-830](weaknesses/CWE-830.md) | Inclusion of Web Functionality from an Untrusted Source | Variant | Incomplete | Allowed |
| [CWE-831](weaknesses/CWE-831.md) | Signal Handler Function Associated with Multiple Signals | Variant | Incomplete | Allowed |
| [CWE-832](weaknesses/CWE-832.md) | Unlock of a Resource that is not Locked | Base | Incomplete | Allowed |
| [CWE-833](weaknesses/CWE-833.md) | Deadlock | Base | Incomplete | Allowed |
| [CWE-834](weaknesses/CWE-834.md) | Excessive Iteration | Class | Incomplete | Discouraged |
| [CWE-835](weaknesses/CWE-835.md) | Loop with Unreachable Exit Condition ('Infinite Loop') | Base | Incomplete | Allowed |
| [CWE-836](weaknesses/CWE-836.md) | Use of Password Hash Instead of Password for Authentication | Base | Incomplete | Allowed |
| [CWE-837](weaknesses/CWE-837.md) | Improper Enforcement of a Single, Unique Action | Base | Incomplete | Allowed |
| [CWE-838](weaknesses/CWE-838.md) | Inappropriate Encoding for Output Context | Base | Incomplete | Allowed |
| [CWE-839](weaknesses/CWE-839.md) | Numeric Range Comparison Without Minimum Check | Base | Incomplete | Allowed |
| [CWE-841](weaknesses/CWE-841.md) | Improper Enforcement of Behavioral Workflow | Class | Incomplete | Allowed |
| [CWE-842](weaknesses/CWE-842.md) | Placement of User into Incorrect Group | Base | Incomplete | Allowed |
| [CWE-843](weaknesses/CWE-843.md) | Access of Resource Using Incompatible Type ('Type Confusion') | Base | Incomplete | Allowed |
| [CWE-862](weaknesses/CWE-862.md) | Missing Authorization | Class | Incomplete | Allowed-with-Review |
| [CWE-863](weaknesses/CWE-863.md) | Incorrect Authorization | Class | Incomplete | Allowed-with-Review |
| [CWE-908](weaknesses/CWE-908.md) | Use of Uninitialized Resource | Base | Incomplete | Allowed |
| [CWE-909](weaknesses/CWE-909.md) | Missing Initialization of Resource | Class | Incomplete | Allowed-with-Review |
| [CWE-910](weaknesses/CWE-910.md) | Use of Expired File Descriptor | Base | Incomplete | Allowed |
| [CWE-911](weaknesses/CWE-911.md) | Improper Update of Reference Count | Base | Incomplete | Allowed |
| [CWE-912](weaknesses/CWE-912.md) | Hidden Functionality | Class | Incomplete | Allowed-with-Review |
| [CWE-913](weaknesses/CWE-913.md) | Improper Control of Dynamically-Managed Code Resources | Class | Incomplete | Allowed-with-Review |
| [CWE-914](weaknesses/CWE-914.md) | Improper Control of Dynamically-Identified Variables | Base | Incomplete | Allowed |
| [CWE-915](weaknesses/CWE-915.md) | Improperly Controlled Modification of Dynamically-Determined Object Attributes | Base | Incomplete | Allowed |
| [CWE-916](weaknesses/CWE-916.md) | Use of Password Hash With Insufficient Computational Effort | Base | Incomplete | Allowed |
| [CWE-917](weaknesses/CWE-917.md) | Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') | Base | Incomplete | Allowed |
| [CWE-918](weaknesses/CWE-918.md) | Server-Side Request Forgery (SSRF) | Base | Incomplete | Allowed |
| [CWE-920](weaknesses/CWE-920.md) | Improper Restriction of Power Consumption | Base | Incomplete | Allowed |
| [CWE-921](weaknesses/CWE-921.md) | Storage of Sensitive Data in a Mechanism without Access Control | Base | Incomplete | Allowed |
| [CWE-922](weaknesses/CWE-922.md) | Insecure Storage of Sensitive Information | Class | Incomplete | Allowed-with-Review |
| [CWE-923](weaknesses/CWE-923.md) | Improper Restriction of Communication Channel to Intended Endpoints | Class | Incomplete | Allowed-with-Review |
| [CWE-924](weaknesses/CWE-924.md) | Improper Enforcement of Message Integrity During Transmission in a Communication Channel | Base | Incomplete | Allowed |
| [CWE-925](weaknesses/CWE-925.md) | Improper Verification of Intent by Broadcast Receiver | Variant | Incomplete | Allowed |
| [CWE-926](weaknesses/CWE-926.md) | Improper Export of Android Application Components | Variant | Incomplete | Allowed |
| [CWE-927](weaknesses/CWE-927.md) | Use of Implicit Intent for Sensitive Communication | Variant | Incomplete | Allowed |
| [CWE-939](weaknesses/CWE-939.md) | Improper Authorization in Handler for Custom URL Scheme | Base | Incomplete | Allowed |
| [CWE-940](weaknesses/CWE-940.md) | Improper Verification of Source of a Communication Channel | Base | Incomplete | Allowed |
| [CWE-941](weaknesses/CWE-941.md) | Incorrectly Specified Destination in a Communication Channel | Base | Incomplete | Allowed |
| [CWE-942](weaknesses/CWE-942.md) | Permissive Cross-domain Security Policy with Untrusted Domains | Variant | Incomplete | Allowed |
| [CWE-943](weaknesses/CWE-943.md) | Improper Neutralization of Special Elements in Data Query Logic | Class | Incomplete | Allowed-with-Review |
| [CWE-1004](weaknesses/CWE-1004.md) | Sensitive Cookie Without 'HttpOnly' Flag | Variant | Incomplete | Allowed |
| [CWE-1007](weaknesses/CWE-1007.md) | Insufficient Visual Distinction of Homoglyphs Presented to User | Base | Incomplete | Allowed |
| [CWE-1021](weaknesses/CWE-1021.md) | Improper Restriction of Rendered UI Layers or Frames | Base | Incomplete | Allowed |
| [CWE-1022](weaknesses/CWE-1022.md) | Use of Web Link to Untrusted Target with window.opener Access | Variant | Incomplete | Allowed |
| [CWE-1023](weaknesses/CWE-1023.md) | Incomplete Comparison with Missing Factors | Class | Incomplete | Allowed-with-Review |
| [CWE-1024](weaknesses/CWE-1024.md) | Comparison of Incompatible Types | Base | Incomplete | Allowed |
| [CWE-1025](weaknesses/CWE-1025.md) | Comparison Using Wrong Factors | Base | Incomplete | Allowed |
| [CWE-1037](weaknesses/CWE-1037.md) | Processor Optimization Removal or Modification of Security-critical Code | Base | Incomplete | Allowed |
| [CWE-1038](weaknesses/CWE-1038.md) | Insecure Automated Optimizations | Class | Draft | Allowed-with-Review |
| [CWE-1039](weaknesses/CWE-1039.md) | Inadequate Detection or Handling of Adversarial Input Perturbations in Automated Recognition Mechanism | Class | Incomplete | Allowed-with-Review |
| [CWE-1041](weaknesses/CWE-1041.md) | Use of Redundant Code | Base | Incomplete | Prohibited |
| [CWE-1042](weaknesses/CWE-1042.md) | Static Member Data Element outside of a Singleton Class Element | Variant | Incomplete | Prohibited |
| [CWE-1043](weaknesses/CWE-1043.md) | Data Element Aggregating an Excessively Large Number of Non-Primitive Elements | Base | Incomplete | Prohibited |
| [CWE-1044](weaknesses/CWE-1044.md) | Architecture with Number of Horizontal Layers Outside of Expected Range | Base | Incomplete | Prohibited |
| [CWE-1045](weaknesses/CWE-1045.md) | Parent Class with a Virtual Destructor and a Child Class without a Virtual Destructor | Base | Incomplete | Allowed |
| [CWE-1046](weaknesses/CWE-1046.md) | Creation of Immutable Text Using String Concatenation | Base | Incomplete | Allowed |
| [CWE-1047](weaknesses/CWE-1047.md) | Modules with Circular Dependencies | Base | Incomplete | Prohibited |
| [CWE-1048](weaknesses/CWE-1048.md) | Invokable Control Element with Large Number of Outward Calls | Base | Incomplete | Prohibited |
| [CWE-1049](weaknesses/CWE-1049.md) | Excessive Data Query Operations in a Large Data Table | Base | Incomplete | Allowed |
| [CWE-1050](weaknesses/CWE-1050.md) | Excessive Platform Resource Consumption within a Loop | Base | Incomplete | Allowed |
| [CWE-1051](weaknesses/CWE-1051.md) | Initialization with Hard-Coded Network Resource Configuration Data | Base | Incomplete | Prohibited |
| [CWE-1052](weaknesses/CWE-1052.md) | Excessive Use of Hard-Coded Literals in Initialization | Base | Incomplete | Allowed |
| [CWE-1053](weaknesses/CWE-1053.md) | Missing Documentation for Design | Base | Incomplete | Prohibited |
| [CWE-1054](weaknesses/CWE-1054.md) | Invocation of a Control Element at an Unnecessarily Deep Horizontal Layer | Base | Incomplete | Prohibited |
| [CWE-1055](weaknesses/CWE-1055.md) | Multiple Inheritance from Concrete Classes | Base | Incomplete | Prohibited |
| [CWE-1056](weaknesses/CWE-1056.md) | Invokable Control Element with Variadic Parameters | Base | Incomplete | Prohibited |
| [CWE-1057](weaknesses/CWE-1057.md) | Data Access Operations Outside of Expected Data Manager Component | Base | Incomplete | Prohibited |
| [CWE-1058](weaknesses/CWE-1058.md) | Invokable Control Element in Multi-Thread Context with non-Final Static Storable or Member Element | Base | Incomplete | Allowed |
| [CWE-1059](weaknesses/CWE-1059.md) | Insufficient Technical Documentation | Class | Incomplete | Prohibited |
| [CWE-1060](weaknesses/CWE-1060.md) | Excessive Number of Inefficient Server-Side Data Accesses | Base | Incomplete | Prohibited |
| [CWE-1061](weaknesses/CWE-1061.md) | Insufficient Encapsulation | Class | Incomplete | Allowed-with-Review |
| [CWE-1062](weaknesses/CWE-1062.md) | Parent Class with References to Child Class | Base | Incomplete | Prohibited |
| [CWE-1063](weaknesses/CWE-1063.md) | Creation of Class Instance within a Static Code Block | Base | Incomplete | Prohibited |
| [CWE-1064](weaknesses/CWE-1064.md) | Invokable Control Element with Signature Containing an Excessive Number of Parameters | Base | Incomplete | Prohibited |
| [CWE-1065](weaknesses/CWE-1065.md) | Runtime Resource Management Control Element in a Component Built to Run on Application Servers | Base | Incomplete | Prohibited |
| [CWE-1066](weaknesses/CWE-1066.md) | Missing Serialization Control Element | Base | Incomplete | Prohibited |
| [CWE-1067](weaknesses/CWE-1067.md) | Excessive Execution of Sequential Searches of Data Resource | Base | Incomplete | Allowed |
| [CWE-1068](weaknesses/CWE-1068.md) | Inconsistency Between Implementation and Documented Design | Base | Incomplete | Prohibited |
| [CWE-1069](weaknesses/CWE-1069.md) | Empty Exception Block | Variant | Incomplete | Prohibited |
| [CWE-1070](weaknesses/CWE-1070.md) | Serializable Data Element Containing non-Serializable Item Elements | Base | Incomplete | Prohibited |
| [CWE-1071](weaknesses/CWE-1071.md) | Empty Code Block | Base | Incomplete | Allowed |
| [CWE-1072](weaknesses/CWE-1072.md) | Data Resource Access without Use of Connection Pooling | Base | Incomplete | Prohibited |
| [CWE-1073](weaknesses/CWE-1073.md) | Non-SQL Invokable Control Element with Excessive Number of Data Resource Accesses | Base | Incomplete | Prohibited |
| [CWE-1074](weaknesses/CWE-1074.md) | Class with Excessively Deep Inheritance | Base | Incomplete | Prohibited |
| [CWE-1075](weaknesses/CWE-1075.md) | Unconditional Control Flow Transfer outside of Switch Block | Base | Incomplete | Allowed |
| [CWE-1076](weaknesses/CWE-1076.md) | Insufficient Adherence to Expected Conventions | Class | Incomplete | Prohibited |
| [CWE-1077](weaknesses/CWE-1077.md) | Floating Point Comparison with Incorrect Operator | Variant | Incomplete | Allowed |
| [CWE-1078](weaknesses/CWE-1078.md) | Inappropriate Source Code Style or Formatting | Class | Incomplete | Prohibited |
| [CWE-1079](weaknesses/CWE-1079.md) | Parent Class without Virtual Destructor Method | Base | Incomplete | Allowed |
| [CWE-1080](weaknesses/CWE-1080.md) | Source Code File with Excessive Number of Lines of Code | Base | Incomplete | Prohibited |
| [CWE-1082](weaknesses/CWE-1082.md) | Class Instance Self Destruction Control Element | Base | Incomplete | Prohibited |
| [CWE-1083](weaknesses/CWE-1083.md) | Data Access from Outside Expected Data Manager Component | Base | Incomplete | Prohibited |
| [CWE-1084](weaknesses/CWE-1084.md) | Invokable Control Element with Excessive File or Data Access Operations | Base | Incomplete | Prohibited |
| [CWE-1085](weaknesses/CWE-1085.md) | Invokable Control Element with Excessive Volume of Commented-out Code | Base | Incomplete | Prohibited |
| [CWE-1086](weaknesses/CWE-1086.md) | Class with Excessive Number of Child Classes | Base | Incomplete | Prohibited |
| [CWE-1087](weaknesses/CWE-1087.md) | Class with Virtual Method without a Virtual Destructor | Base | Incomplete | Allowed |
| [CWE-1088](weaknesses/CWE-1088.md) | Synchronous Access of Remote Resource without Timeout | Base | Incomplete | Allowed |
| [CWE-1089](weaknesses/CWE-1089.md) | Large Data Table with Excessive Number of Indices | Base | Incomplete | Allowed |
| [CWE-1090](weaknesses/CWE-1090.md) | Method Containing Access of a Member Element from Another Class | Base | Incomplete | Prohibited |
| [CWE-1091](weaknesses/CWE-1091.md) | Use of Object without Invoking Destructor Method | Base | Incomplete | Allowed |
| [CWE-1092](weaknesses/CWE-1092.md) | Use of Same Invokable Control Element in Multiple Architectural Layers | Base | Incomplete | Prohibited |
| [CWE-1093](weaknesses/CWE-1093.md) | Excessively Complex Data Representation | Class | Incomplete | Allowed-with-Review |
| [CWE-1094](weaknesses/CWE-1094.md) | Excessive Index Range Scan for a Data Resource | Base | Incomplete | Prohibited |
| [CWE-1095](weaknesses/CWE-1095.md) | Loop Condition Value Update within the Loop | Base | Incomplete | Prohibited |
| [CWE-1096](weaknesses/CWE-1096.md) | Singleton Class Instance Creation without Proper Locking or Synchronization | Variant | Incomplete | Allowed |
| [CWE-1097](weaknesses/CWE-1097.md) | Persistent Storable Data Element without Associated Comparison Control Element | Base | Incomplete | Prohibited |
| [CWE-1098](weaknesses/CWE-1098.md) | Data Element containing Pointer Item without Proper Copy Control Element | Base | Incomplete | Allowed |
| [CWE-1099](weaknesses/CWE-1099.md) | Inconsistent Naming Conventions for Identifiers | Base | Incomplete | Prohibited |
| [CWE-1100](weaknesses/CWE-1100.md) | Insufficient Isolation of System-Dependent Functions | Base | Incomplete | Allowed |
| [CWE-1101](weaknesses/CWE-1101.md) | Reliance on Runtime Component in Generated Code | Base | Incomplete | Prohibited |
| [CWE-1102](weaknesses/CWE-1102.md) | Reliance on Machine-Dependent Data Representation | Base | Incomplete | Allowed |
| [CWE-1103](weaknesses/CWE-1103.md) | Use of Platform-Dependent Third Party Components | Base | Incomplete | Prohibited |
| [CWE-1104](weaknesses/CWE-1104.md) | Use of Unmaintained Third Party Components | Base | Incomplete | Allowed |
| [CWE-1105](weaknesses/CWE-1105.md) | Insufficient Encapsulation of Machine-Dependent Functionality | Base | Incomplete | Prohibited |
| [CWE-1106](weaknesses/CWE-1106.md) | Insufficient Use of Symbolic Constants | Base | Incomplete | Prohibited |
| [CWE-1107](weaknesses/CWE-1107.md) | Insufficient Isolation of Symbolic Constant Definitions | Base | Incomplete | Prohibited |
| [CWE-1108](weaknesses/CWE-1108.md) | Excessive Reliance on Global Variables | Base | Incomplete | Allowed |
| [CWE-1109](weaknesses/CWE-1109.md) | Use of Same Variable for Multiple Purposes | Base | Incomplete | Prohibited |
| [CWE-1110](weaknesses/CWE-1110.md) | Incomplete Design Documentation | Base | Incomplete | Prohibited |
| [CWE-1111](weaknesses/CWE-1111.md) | Incomplete I/O Documentation | Base | Incomplete | Prohibited |
| [CWE-1112](weaknesses/CWE-1112.md) | Incomplete Documentation of Program Execution | Base | Incomplete | Prohibited |
| [CWE-1113](weaknesses/CWE-1113.md) | Inappropriate Comment Style | Base | Incomplete | Prohibited |
| [CWE-1114](weaknesses/CWE-1114.md) | Inappropriate Whitespace Style | Base | Incomplete | Prohibited |
| [CWE-1115](weaknesses/CWE-1115.md) | Source Code Element without Standard Prologue | Base | Incomplete | Prohibited |
| [CWE-1116](weaknesses/CWE-1116.md) | Inaccurate Source Code Comments | Base | Incomplete | Allowed |
| [CWE-1117](weaknesses/CWE-1117.md) | Callable with Insufficient Behavioral Summary | Base | Incomplete | Prohibited |
| [CWE-1118](weaknesses/CWE-1118.md) | Insufficient Documentation of Error Handling Techniques | Base | Incomplete | Prohibited |
| [CWE-1119](weaknesses/CWE-1119.md) | Excessive Use of Unconditional Branching | Base | Incomplete | Prohibited |
| [CWE-1120](weaknesses/CWE-1120.md) | Excessive Code Complexity | Class | Incomplete | Allowed-with-Review |
| [CWE-1121](weaknesses/CWE-1121.md) | Excessive McCabe Cyclomatic Complexity | Base | Incomplete | Prohibited |
| [CWE-1122](weaknesses/CWE-1122.md) | Excessive Halstead Complexity | Base | Incomplete | Prohibited |
| [CWE-1123](weaknesses/CWE-1123.md) | Excessive Use of Self-Modifying Code | Base | Incomplete | Allowed |
| [CWE-1124](weaknesses/CWE-1124.md) | Excessively Deep Nesting | Base | Incomplete | Prohibited |
| [CWE-1125](weaknesses/CWE-1125.md) | Excessive Attack Surface | Base | Incomplete | Prohibited |
| [CWE-1126](weaknesses/CWE-1126.md) | Declaration of Variable with Unnecessarily Wide Scope | Base | Incomplete | Allowed |
| [CWE-1127](weaknesses/CWE-1127.md) | Compilation with Insufficient Warnings or Errors | Base | Incomplete | Allowed |
| [CWE-1164](weaknesses/CWE-1164.md) | Irrelevant Code | Class | Incomplete | Allowed-with-Review |
| [CWE-1173](weaknesses/CWE-1173.md) | Improper Use of Validation Framework | Base | Draft | Allowed |
| [CWE-1174](weaknesses/CWE-1174.md) | ASP.NET Misconfiguration: Improper Model Validation | Variant | Draft | Allowed |
| [CWE-1176](weaknesses/CWE-1176.md) | Inefficient CPU Computation | Class | Incomplete | Allowed-with-Review |
| [CWE-1177](weaknesses/CWE-1177.md) | Use of Prohibited Code | Class | Incomplete | Allowed-with-Review |
| [CWE-1187](weaknesses/CWE-1187.md) | DEPRECATED: Use of Uninitialized Resource | Base | Deprecated | Prohibited |
| [CWE-1188](weaknesses/CWE-1188.md) | Initialization of a Resource with an Insecure Default | Base | Incomplete | Allowed |
| [CWE-1189](weaknesses/CWE-1189.md) | Improper Isolation of Shared Resources on System-on-a-Chip (SoC) | Base | Stable | Allowed |
| [CWE-1190](weaknesses/CWE-1190.md) | DMA Device Enabled Too Early in Boot Phase | Base | Draft | Allowed |
| [CWE-1191](weaknesses/CWE-1191.md) | On-Chip Debug and Test Interface With Improper Access Control | Base | Stable | Allowed |
| [CWE-1192](weaknesses/CWE-1192.md) | Improper Identifier for IP Block used in System-On-Chip (SOC) | Base | Draft | Allowed |
| [CWE-1193](weaknesses/CWE-1193.md) | Power-On of Untrusted Execution Core Before Enabling Fabric Access Control | Base | Draft | Allowed |
| [CWE-1204](weaknesses/CWE-1204.md) | Generation of Weak Initialization Vector (IV) | Base | Incomplete | Allowed |
| [CWE-1209](weaknesses/CWE-1209.md) | Failure to Disable Reserved Bits | Base | Incomplete | Allowed |
| [CWE-1220](weaknesses/CWE-1220.md) | Insufficient Granularity of Access Control | Base | Incomplete | Allowed |
| [CWE-1221](weaknesses/CWE-1221.md) | Incorrect Register Defaults or Module Parameters | Base | Incomplete | Allowed |
| [CWE-1222](weaknesses/CWE-1222.md) | Insufficient Granularity of Address Regions Protected by Register Locks | Variant | Incomplete | Allowed |
| [CWE-1223](weaknesses/CWE-1223.md) | Race Condition for Write-Once Attributes | Base | Incomplete | Allowed |
| [CWE-1224](weaknesses/CWE-1224.md) | Improper Restriction of Write-Once Bit Fields | Base | Incomplete | Allowed |
| [CWE-1229](weaknesses/CWE-1229.md) | Creation of Emergent Resource | Class | Incomplete | Allowed-with-Review |
| [CWE-1230](weaknesses/CWE-1230.md) | Exposure of Sensitive Information Through Metadata | Base | Incomplete | Allowed |
| [CWE-1231](weaknesses/CWE-1231.md) | Improper Prevention of Lock Bit Modification | Base | Stable | Allowed |
| [CWE-1232](weaknesses/CWE-1232.md) | Improper Lock Behavior After Power State Transition | Base | Incomplete | Allowed |
| [CWE-1233](weaknesses/CWE-1233.md) | Security-Sensitive Hardware Controls with Missing Lock Bit Protection | Base | Stable | Allowed |
| [CWE-1234](weaknesses/CWE-1234.md) | Hardware Internal or Debug Modes Allow Override of Locks | Base | Incomplete | Allowed |
| [CWE-1235](weaknesses/CWE-1235.md) | Incorrect Use of Autoboxing and Unboxing for Performance Critical Operations | Base | Incomplete | Allowed |
| [CWE-1236](weaknesses/CWE-1236.md) | Improper Neutralization of Formula Elements in a CSV File | Base | Incomplete | Allowed |
| [CWE-1239](weaknesses/CWE-1239.md) | Improper Zeroization of Hardware Register | Variant | Draft | Allowed |
| [CWE-1240](weaknesses/CWE-1240.md) | Use of a Cryptographic Primitive with a Risky Implementation | Base | Draft | Allowed |
| [CWE-1241](weaknesses/CWE-1241.md) | Use of Predictable Algorithm in Random Number Generator | Base | Draft | Allowed |
| [CWE-1242](weaknesses/CWE-1242.md) | Inclusion of Undocumented Features or Chicken Bits | Base | Incomplete | Allowed |
| [CWE-1243](weaknesses/CWE-1243.md) | Sensitive Non-Volatile Information Not Protected During Debug | Base | Incomplete | Allowed |
| [CWE-1244](weaknesses/CWE-1244.md) | Internal Asset Exposed to Unsafe Debug Access Level or State | Base | Stable | Allowed |
| [CWE-1245](weaknesses/CWE-1245.md) | Improper Finite State Machines (FSMs) in Hardware Logic | Base | Incomplete | Allowed |
| [CWE-1246](weaknesses/CWE-1246.md) | Improper Write Handling in Limited-write Non-Volatile Memories | Base | Incomplete | Allowed |
| [CWE-1247](weaknesses/CWE-1247.md) | Improper Protection Against Voltage and Clock Glitches | Base | Stable | Allowed |
| [CWE-1248](weaknesses/CWE-1248.md) | Semiconductor Defects in Hardware Logic with Security-Sensitive Implications | Base | Incomplete | Allowed |
| [CWE-1249](weaknesses/CWE-1249.md) | Application-Level Admin Tool with Inconsistent View of Underlying Operating System | Base | Incomplete | Allowed |
| [CWE-1250](weaknesses/CWE-1250.md) | Improper Preservation of Consistency Between Independent Representations of Shared State | Base | Incomplete | Allowed |
| [CWE-1251](weaknesses/CWE-1251.md) | Mirrored Regions with Different Values | Base | Incomplete | Allowed |
| [CWE-1252](weaknesses/CWE-1252.md) | CPU Hardware Not Configured to Support Exclusivity of Write and Execute Operations | Base | Incomplete | Allowed |
| [CWE-1253](weaknesses/CWE-1253.md) | Incorrect Selection of Fuse Values | Base | Draft | Allowed |
| [CWE-1254](weaknesses/CWE-1254.md) | Incorrect Comparison Logic Granularity | Base | Draft | Allowed |
| [CWE-1255](weaknesses/CWE-1255.md) | Comparison Logic is Vulnerable to Power Side-Channel Attacks | Variant | Draft | Allowed |
| [CWE-1256](weaknesses/CWE-1256.md) | Improper Restriction of Software Interfaces to Hardware Features | Base | Stable | Allowed |
| [CWE-1257](weaknesses/CWE-1257.md) | Improper Access Control Applied to Mirrored or Aliased Memory Regions | Base | Incomplete | Allowed |
| [CWE-1258](weaknesses/CWE-1258.md) | Exposure of Sensitive System Information Due to Uncleared Debug Information | Base | Draft | Allowed |
| [CWE-1259](weaknesses/CWE-1259.md) | Improper Restriction of Security Token Assignment | Base | Incomplete | Allowed |
| [CWE-1260](weaknesses/CWE-1260.md) | Improper Handling of Overlap Between Protected Memory Ranges | Base | Stable | Allowed |
| [CWE-1261](weaknesses/CWE-1261.md) | Improper Handling of Single Event Upsets | Base | Draft | Allowed |
| [CWE-1262](weaknesses/CWE-1262.md) | Improper Access Control for Register Interface | Base | Stable | Allowed |
| [CWE-1263](weaknesses/CWE-1263.md) | Improper Physical Access Control | Class | Incomplete | Allowed-with-Review |
| [CWE-1264](weaknesses/CWE-1264.md) | Hardware Logic with Insecure De-Synchronization between Control and Data Channels | Base | Incomplete | Allowed |
| [CWE-1265](weaknesses/CWE-1265.md) | Unintended Reentrant Invocation of Non-reentrant Code Via Nested Calls | Base | Draft | Allowed |
| [CWE-1266](weaknesses/CWE-1266.md) | Improper Scrubbing of Sensitive Data from Decommissioned Device | Base | Incomplete | Allowed |
| [CWE-1267](weaknesses/CWE-1267.md) | Policy Uses Obsolete Encoding | Base | Draft | Allowed |
| [CWE-1268](weaknesses/CWE-1268.md) | Policy Privileges are not Assigned Consistently Between Control and Data Agents | Base | Draft | Allowed |
| [CWE-1269](weaknesses/CWE-1269.md) | Product Released in Non-Release Configuration | Base | Incomplete | Allowed |
| [CWE-1270](weaknesses/CWE-1270.md) | Generation of Incorrect Security Tokens | Base | Incomplete | Allowed |
| [CWE-1271](weaknesses/CWE-1271.md) | Uninitialized Value on Reset for Registers Holding Security Settings | Base | Incomplete | Allowed |
| [CWE-1272](weaknesses/CWE-1272.md) | Sensitive Information Uncleared Before Debug/Power State Transition | Base | Stable | Allowed |
| [CWE-1273](weaknesses/CWE-1273.md) | Device Unlock Credential Sharing | Base | Incomplete | Allowed |
| [CWE-1274](weaknesses/CWE-1274.md) | Improper Access Control for Volatile Memory Containing Boot Code | Base | Stable | Allowed |
| [CWE-1275](weaknesses/CWE-1275.md) | Sensitive Cookie with Improper SameSite Attribute | Variant | Incomplete | Allowed |
| [CWE-1276](weaknesses/CWE-1276.md) | Hardware Child Block Incorrectly Connected to Parent System | Base | Incomplete | Allowed |
| [CWE-1277](weaknesses/CWE-1277.md) | Firmware Not Updateable | Base | Draft | Allowed |
| [CWE-1278](weaknesses/CWE-1278.md) | Missing Protection Against Hardware Reverse Engineering Using Integrated Circuit (IC) Imaging Techniques | Base | Incomplete | Allowed |
| [CWE-1279](weaknesses/CWE-1279.md) | Cryptographic Operations are run Before Supporting Units are Ready | Base | Incomplete | Allowed |
| [CWE-1280](weaknesses/CWE-1280.md) | Access Control Check Implemented After Asset is Accessed | Base | Incomplete | Allowed |
| [CWE-1281](weaknesses/CWE-1281.md) | Sequence of Processor Instructions Leads to Unexpected Behavior | Base | Incomplete | Allowed |
| [CWE-1282](weaknesses/CWE-1282.md) | Assumed-Immutable Data is Stored in Writable Memory | Base | Incomplete | Allowed |
| [CWE-1283](weaknesses/CWE-1283.md) | Mutable Attestation or Measurement Reporting Data | Base | Incomplete | Allowed |
| [CWE-1284](weaknesses/CWE-1284.md) | Improper Validation of Specified Quantity in Input | Base | Incomplete | Allowed |
| [CWE-1285](weaknesses/CWE-1285.md) | Improper Validation of Specified Index, Position, or Offset in Input | Base | Incomplete | Allowed |
| [CWE-1286](weaknesses/CWE-1286.md) | Improper Validation of Syntactic Correctness of Input | Base | Incomplete | Allowed |
| [CWE-1287](weaknesses/CWE-1287.md) | Improper Validation of Specified Type of Input | Base | Incomplete | Allowed |
| [CWE-1288](weaknesses/CWE-1288.md) | Improper Validation of Consistency within Input | Base | Incomplete | Allowed |
| [CWE-1289](weaknesses/CWE-1289.md) | Improper Validation of Unsafe Equivalence in Input | Base | Incomplete | Allowed |
| [CWE-1290](weaknesses/CWE-1290.md) | Incorrect Decoding of Security Identifiers | Base | Incomplete | Allowed |
| [CWE-1291](weaknesses/CWE-1291.md) | Public Key Re-Use for Signing both Debug and Production Code | Base | Draft | Allowed |
| [CWE-1292](weaknesses/CWE-1292.md) | Incorrect Conversion of Security Identifiers | Base | Draft | Allowed |
| [CWE-1293](weaknesses/CWE-1293.md) | Missing Source Correlation of Multiple Independent Data | Base | Draft | Allowed |
| [CWE-1294](weaknesses/CWE-1294.md) | Insecure Security Identifier Mechanism | Class | Incomplete | Allowed-with-Review |
| [CWE-1295](weaknesses/CWE-1295.md) | Debug Messages Revealing Unnecessary Information | Base | Incomplete | Allowed |
| [CWE-1296](weaknesses/CWE-1296.md) | Incorrect Chaining or Granularity of Debug Components | Base | Incomplete | Allowed |
| [CWE-1297](weaknesses/CWE-1297.md) | Unprotected Confidential Information on Device is Accessible by OSAT Vendors | Base | Incomplete | Allowed |
| [CWE-1298](weaknesses/CWE-1298.md) | Hardware Logic Contains Race Conditions | Base | Draft | Allowed |
| [CWE-1299](weaknesses/CWE-1299.md) | Missing Protection Mechanism for Alternate Hardware Interface | Base | Draft | Allowed |
| [CWE-1300](weaknesses/CWE-1300.md) | Improper Protection of Physical Side Channels | Base | Stable | Allowed |
| [CWE-1301](weaknesses/CWE-1301.md) | Insufficient or Incomplete Data Removal within Hardware Component | Base | Incomplete | Allowed |
| [CWE-1302](weaknesses/CWE-1302.md) | Missing Source Identifier in Entity Transactions on a System-On-Chip (SOC) | Base | Incomplete | Allowed |
| [CWE-1303](weaknesses/CWE-1303.md) | Non-Transparent Sharing of Microarchitectural Resources | Base | Draft | Allowed |
| [CWE-1304](weaknesses/CWE-1304.md) | Improperly Preserved Integrity of Hardware Configuration State During a Power Save/Restore Operation | Base | Draft | Allowed |
| [CWE-1310](weaknesses/CWE-1310.md) | Missing Ability to Patch ROM Code | Base | Draft | Allowed |
| [CWE-1311](weaknesses/CWE-1311.md) | Improper Translation of Security Attributes by Fabric Bridge | Base | Draft | Allowed |
| [CWE-1312](weaknesses/CWE-1312.md) | Missing Protection for Mirrored Regions in On-Chip Fabric Firewall | Base | Draft | Allowed |
| [CWE-1313](weaknesses/CWE-1313.md) | Hardware Allows Activation of Test or Debug Logic at Runtime | Base | Draft | Allowed |
| [CWE-1314](weaknesses/CWE-1314.md) | Missing Write Protection for Parametric Data Values | Base | Draft | Allowed |
| [CWE-1315](weaknesses/CWE-1315.md) | Improper Setting of Bus Controlling Capability in Fabric End-point | Base | Incomplete | Allowed |
| [CWE-1316](weaknesses/CWE-1316.md) | Fabric-Address Map Allows Programming of Unwarranted Overlaps of Protected and Unprotected Ranges | Base | Draft | Allowed |
| [CWE-1317](weaknesses/CWE-1317.md) | Improper Access Control in Fabric Bridge | Base | Draft | Allowed |
| [CWE-1318](weaknesses/CWE-1318.md) | Missing Support for Security Features in On-chip Fabrics or Buses | Base | Incomplete | Allowed |
| [CWE-1319](weaknesses/CWE-1319.md) | Improper Protection against Electromagnetic Fault Injection (EM-FI) | Base | Incomplete | Allowed |
| [CWE-1320](weaknesses/CWE-1320.md) | Improper Protection for Outbound Error Messages and Alert Signals | Base | Draft | Allowed |
| [CWE-1321](weaknesses/CWE-1321.md) | Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution') | Variant | Incomplete | Allowed |
| [CWE-1322](weaknesses/CWE-1322.md) | Use of Blocking Code in Single-threaded, Non-blocking Context | Base | Incomplete | Allowed |
| [CWE-1323](weaknesses/CWE-1323.md) | Improper Management of Sensitive Trace Data | Base | Draft | Allowed |
| [CWE-1324](weaknesses/CWE-1324.md) | DEPRECATED: Sensitive Information Accessible by Physical Probing of JTAG Interface | Base | Deprecated | Prohibited |
| [CWE-1325](weaknesses/CWE-1325.md) | Improperly Controlled Sequential Memory Allocation | Base | Incomplete | Allowed |
| [CWE-1326](weaknesses/CWE-1326.md) | Missing Immutable Root of Trust in Hardware | Base | Draft | Allowed |
| [CWE-1327](weaknesses/CWE-1327.md) | Binding to an Unrestricted IP Address | Base | Incomplete | Allowed |
| [CWE-1328](weaknesses/CWE-1328.md) | Security Version Number Mutable to Older Versions | Base | Draft | Allowed |
| [CWE-1329](weaknesses/CWE-1329.md) | Reliance on Component That is Not Updateable | Base | Incomplete | Allowed |
| [CWE-1330](weaknesses/CWE-1330.md) | Remanent Data Readable after Memory Erase | Variant | Draft | Allowed |
| [CWE-1331](weaknesses/CWE-1331.md) | Improper Isolation of Shared Resources in Network On Chip (NoC) | Base | Stable | Allowed |
| [CWE-1332](weaknesses/CWE-1332.md) | Improper Handling of Faults that Lead to Instruction Skips | Base | Stable | Allowed |
| [CWE-1333](weaknesses/CWE-1333.md) | Inefficient Regular Expression Complexity | Base | Draft | Allowed |
| [CWE-1334](weaknesses/CWE-1334.md) | Unauthorized Error Injection Can Degrade Hardware Redundancy | Base | Draft | Allowed |
| [CWE-1335](weaknesses/CWE-1335.md) | Incorrect Bitwise Shift of Integer | Base | Draft | Allowed |
| [CWE-1336](weaknesses/CWE-1336.md) | Improper Neutralization of Special Elements Used in a Template Engine | Base | Incomplete | Allowed |
| [CWE-1338](weaknesses/CWE-1338.md) | Improper Protections Against Hardware Overheating | Base | Draft | Allowed |
| [CWE-1339](weaknesses/CWE-1339.md) | Insufficient Precision or Accuracy of a Real Number | Base | Draft | Allowed |
| [CWE-1341](weaknesses/CWE-1341.md) | Multiple Releases of Same Resource or Handle | Base | Incomplete | Allowed |
| [CWE-1342](weaknesses/CWE-1342.md) | Information Exposure through Microarchitectural State after Transient Execution | Base | Incomplete | Allowed |
| [CWE-1351](weaknesses/CWE-1351.md) | Improper Handling of Hardware Behavior in Exceptionally Cold Environments | Base | Incomplete | Allowed |
| [CWE-1357](weaknesses/CWE-1357.md) | Reliance on Insufficiently Trustworthy Component | Class | Incomplete | Allowed-with-Review |
| [CWE-1384](weaknesses/CWE-1384.md) | Improper Handling of Physical or Environmental Conditions | Class | Incomplete | Allowed-with-Review |
| [CWE-1385](weaknesses/CWE-1385.md) | Missing Origin Validation in WebSockets | Variant | Incomplete | Allowed |
| [CWE-1386](weaknesses/CWE-1386.md) | Insecure Operation on Windows Junction / Mount Point | Base | Incomplete | Allowed |
| [CWE-1389](weaknesses/CWE-1389.md) | Incorrect Parsing of Numbers with Different Radices | Base | Incomplete | Allowed |
| [CWE-1390](weaknesses/CWE-1390.md) | Weak Authentication | Class | Incomplete | Allowed-with-Review |
| [CWE-1391](weaknesses/CWE-1391.md) | Use of Weak Credentials | Class | Incomplete | Allowed-with-Review |
| [CWE-1392](weaknesses/CWE-1392.md) | Use of Default Credentials | Base | Incomplete | Allowed |
| [CWE-1393](weaknesses/CWE-1393.md) | Use of Default Password | Base | Incomplete | Allowed |
| [CWE-1394](weaknesses/CWE-1394.md) | Use of Default Cryptographic Key | Base | Incomplete | Allowed |
| [CWE-1395](weaknesses/CWE-1395.md) | Dependency on Vulnerable Third-Party Component | Class | Incomplete | Allowed-with-Review |
| [CWE-1419](weaknesses/CWE-1419.md) | Incorrect Initialization of Resource | Class | Incomplete | Allowed-with-Review |
| [CWE-1420](weaknesses/CWE-1420.md) | Exposure of Sensitive Information during Transient Execution | Base | Incomplete | Allowed-with-Review |
| [CWE-1421](weaknesses/CWE-1421.md) | Exposure of Sensitive Information in Shared Microarchitectural Structures during Transient Execution | Base | Incomplete | Allowed |
| [CWE-1422](weaknesses/CWE-1422.md) | Exposure of Sensitive Information caused by Incorrect Data Forwarding during Transient Execution | Base | Incomplete | Allowed |
| [CWE-1423](weaknesses/CWE-1423.md) | Exposure of Sensitive Information caused by Shared Microarchitectural Predictor State that Influences Transient Execution | Base | Incomplete | Allowed |
| [CWE-1426](weaknesses/CWE-1426.md) | Improper Validation of Generative AI Output | Base | Incomplete | Discouraged |
| [CWE-1427](weaknesses/CWE-1427.md) | Improper Neutralization of Input Used for LLM Prompting | Base | Incomplete | Allowed |
| [CWE-1428](weaknesses/CWE-1428.md) | Reliance on HTTP instead of HTTPS | Base | Incomplete | Allowed |
| [CWE-1429](weaknesses/CWE-1429.md) | Missing Security-Relevant Feedback for Unexecuted Operations in Hardware Interface | Base | Incomplete | Allowed |
| [CWE-1431](weaknesses/CWE-1431.md) | Driving Intermediate Cryptographic State/Results to Hardware Module Outputs | Base | Incomplete | Allowed |
| [CWE-1434](weaknesses/CWE-1434.md) | Insecure Setting of Generative AI/ML Model Inference Parameters | Base | Draft | Allowed |

## Categories

| ID | Name | Status |
| --- | --- | --- |
| [CWE-1](categories/CWE-1.md) | DEPRECATED: Location | Deprecated |
| [CWE-2](categories/CWE-2.md) | 7PK - Environment | Draft |
| [CWE-3](categories/CWE-3.md) | DEPRECATED: Technology-specific Environment Issues | Deprecated |
| [CWE-4](categories/CWE-4.md) | DEPRECATED: J2EE Environment Issues | Deprecated |
| [CWE-10](categories/CWE-10.md) | DEPRECATED: ASP.NET Environment Issues | Deprecated |
| [CWE-16](categories/CWE-16.md) | Configuration | Obsolete |
| [CWE-17](categories/CWE-17.md) | DEPRECATED: Code | Deprecated |
| [CWE-18](categories/CWE-18.md) | DEPRECATED: Source Code | Deprecated |
| [CWE-19](categories/CWE-19.md) | Data Processing Errors | Draft |
| [CWE-21](categories/CWE-21.md) | DEPRECATED: Pathname Traversal and Equivalence Errors | Deprecated |
| [CWE-60](categories/CWE-60.md) | DEPRECATED: UNIX Path Link Problems | Deprecated |
| [CWE-63](categories/CWE-63.md) | DEPRECATED: Windows Path Link Problems | Deprecated |
| [CWE-68](categories/CWE-68.md) | DEPRECATED: Windows Virtual File Problems | Deprecated |
| [CWE-70](categories/CWE-70.md) | DEPRECATED: Mac Virtual File Problems | Deprecated |
| [CWE-100](categories/CWE-100.md) | DEPRECATED: Technology-Specific Input Validation Problems | Deprecated |
| [CWE-101](categories/CWE-101.md) | DEPRECATED: Struts Validation Problems | Deprecated |
| [CWE-133](categories/CWE-133.md) | String Errors | Draft |
| [CWE-136](categories/CWE-136.md) | Type Errors | Draft |
| [CWE-137](categories/CWE-137.md) | Data Neutralization Issues | Draft |
| [CWE-139](categories/CWE-139.md) | DEPRECATED: General Special Element Problems | Deprecated |
| [CWE-169](categories/CWE-169.md) | DEPRECATED: Technology-Specific Special Elements | Deprecated |
| [CWE-171](categories/CWE-171.md) | DEPRECATED: Cleansing, Canonicalization, and Comparison Errors | Deprecated |
| [CWE-189](categories/CWE-189.md) | Numeric Errors | Draft |
| [CWE-199](categories/CWE-199.md) | Information Management Errors | Draft |
| [CWE-227](categories/CWE-227.md) | 7PK - API Abuse | Draft |
| [CWE-251](categories/CWE-251.md) | Often Misused: String Management | Incomplete |
| [CWE-254](categories/CWE-254.md) | 7PK - Security Features | Incomplete |
| [CWE-255](categories/CWE-255.md) | Credentials Management Errors | Draft |
| [CWE-264](categories/CWE-264.md) | Permissions, Privileges, and Access Controls | Obsolete |
| [CWE-265](categories/CWE-265.md) | Privilege Issues | Incomplete |
| [CWE-275](categories/CWE-275.md) | Permission Issues | Draft |
| [CWE-310](categories/CWE-310.md) | Cryptographic Issues | Draft |
| [CWE-320](categories/CWE-320.md) | Key Management Errors | Obsolete |
| [CWE-355](categories/CWE-355.md) | User Interface Security Issues | Draft |
| [CWE-361](categories/CWE-361.md) | 7PK - Time and State | Incomplete |
| [CWE-371](categories/CWE-371.md) | State Issues | Draft |
| [CWE-376](categories/CWE-376.md) | DEPRECATED: Temporary File Issues | Deprecated |
| [CWE-380](categories/CWE-380.md) | DEPRECATED: Technology-Specific Time and State Issues | Deprecated |
| [CWE-381](categories/CWE-381.md) | DEPRECATED: J2EE Time and State Issues | Deprecated |
| [CWE-387](categories/CWE-387.md) | Signal Errors | Incomplete |
| [CWE-388](categories/CWE-388.md) | 7PK - Errors | Draft |
| [CWE-389](categories/CWE-389.md) | Error Conditions, Return Values, Status Codes | Incomplete |
| [CWE-398](categories/CWE-398.md) | 7PK - Code Quality | Draft |
| [CWE-399](categories/CWE-399.md) | Resource Management Errors | Draft |
| [CWE-411](categories/CWE-411.md) | Resource Locking Problems | Draft |
| [CWE-417](categories/CWE-417.md) | Communication Channel Errors | Draft |
| [CWE-418](categories/CWE-418.md) | DEPRECATED: Channel Errors | Deprecated |
| [CWE-429](categories/CWE-429.md) | Handler Errors | Draft |
| [CWE-438](categories/CWE-438.md) | Behavioral Problems | Draft |
| [CWE-442](categories/CWE-442.md) | DEPRECATED: Web Problems | Deprecated |
| [CWE-445](categories/CWE-445.md) | DEPRECATED: User Interface Errors | Deprecated |
| [CWE-452](categories/CWE-452.md) | Initialization and Cleanup Errors | Draft |
| [CWE-461](categories/CWE-461.md) | DEPRECATED: Data Structure Issues | Deprecated |
| [CWE-465](categories/CWE-465.md) | Pointer Issues | Draft |
| [CWE-485](categories/CWE-485.md) | 7PK - Encapsulation | Draft |
| [CWE-490](categories/CWE-490.md) | DEPRECATED: Mobile Code Issues | Deprecated |
| [CWE-503](categories/CWE-503.md) | DEPRECATED: Byte/Object Code | Deprecated |
| [CWE-504](categories/CWE-504.md) | DEPRECATED: Motivation/Intent | Deprecated |
| [CWE-505](categories/CWE-505.md) | DEPRECATED: Intentionally Introduced Weakness | Deprecated |
| [CWE-513](categories/CWE-513.md) | DEPRECATED: Intentionally Introduced Nonmalicious Weakness | Deprecated |
| [CWE-517](categories/CWE-517.md) | DEPRECATED: Other Intentional, Nonmalicious Weakness | Deprecated |
| [CWE-518](categories/CWE-518.md) | DEPRECATED: Inadvertently Introduced Weakness | Deprecated |
| [CWE-519](categories/CWE-519.md) | DEPRECATED: .NET Environment Issues | Deprecated |
| [CWE-557](categories/CWE-557.md) | Concurrency Issues | Draft |
| [CWE-559](categories/CWE-559.md) | DEPRECATED: Often Misused: Arguments and Parameters | Deprecated |
| [CWE-569](categories/CWE-569.md) | Expression Issues | Draft |
| [CWE-632](categories/CWE-632.md) | DEPRECATED: Weaknesses that Affect Files or Directories | Deprecated |
| [CWE-633](categories/CWE-633.md) | DEPRECATED: Weaknesses that Affect Memory | Deprecated |
| [CWE-634](categories/CWE-634.md) | DEPRECATED: Weaknesses that Affect System Processes | Deprecated |
| [CWE-712](categories/CWE-712.md) | OWASP Top Ten 2007 Category A1 - Cross Site Scripting (XSS) | Obsolete |
| [CWE-713](categories/CWE-713.md) | OWASP Top Ten 2007 Category A2 - Injection Flaws | Obsolete |
| [CWE-714](categories/CWE-714.md) | OWASP Top Ten 2007 Category A3 - Malicious File Execution | Obsolete |
| [CWE-715](categories/CWE-715.md) | OWASP Top Ten 2007 Category A4 - Insecure Direct Object Reference | Obsolete |
| [CWE-716](categories/CWE-716.md) | OWASP Top Ten 2007 Category A5 - Cross Site Request Forgery (CSRF) | Obsolete |
| [CWE-717](categories/CWE-717.md) | OWASP Top Ten 2007 Category A6 - Information Leakage and Improper Error Handling | Obsolete |
| [CWE-718](categories/CWE-718.md) | OWASP Top Ten 2007 Category A7 - Broken Authentication and Session Management | Obsolete |
| [CWE-719](categories/CWE-719.md) | OWASP Top Ten 2007 Category A8 - Insecure Cryptographic Storage | Obsolete |
| [CWE-720](categories/CWE-720.md) | OWASP Top Ten 2007 Category A9 - Insecure Communications | Obsolete |
| [CWE-721](categories/CWE-721.md) | OWASP Top Ten 2007 Category A10 - Failure to Restrict URL Access | Obsolete |
| [CWE-722](categories/CWE-722.md) | OWASP Top Ten 2004 Category A1 - Unvalidated Input | Obsolete |
| [CWE-723](categories/CWE-723.md) | OWASP Top Ten 2004 Category A2 - Broken Access Control | Obsolete |
| [CWE-724](categories/CWE-724.md) | OWASP Top Ten 2004 Category A3 - Broken Authentication and Session Management | Obsolete |
| [CWE-725](categories/CWE-725.md) | OWASP Top Ten 2004 Category A4 - Cross-Site Scripting (XSS) Flaws | Obsolete |
| [CWE-726](categories/CWE-726.md) | OWASP Top Ten 2004 Category A5 - Buffer Overflows | Obsolete |
| [CWE-727](categories/CWE-727.md) | OWASP Top Ten 2004 Category A6 - Injection Flaws | Obsolete |
| [CWE-728](categories/CWE-728.md) | OWASP Top Ten 2004 Category A7 - Improper Error Handling | Obsolete |
| [CWE-729](categories/CWE-729.md) | OWASP Top Ten 2004 Category A8 - Insecure Storage | Obsolete |
| [CWE-730](categories/CWE-730.md) | OWASP Top Ten 2004 Category A9 - Denial of Service | Obsolete |
| [CWE-731](categories/CWE-731.md) | OWASP Top Ten 2004 Category A10 - Insecure Configuration Management | Obsolete |
| [CWE-735](categories/CWE-735.md) | CERT C Secure Coding Standard (2008) Chapter 2 - Preprocessor (PRE) | Obsolete |
| [CWE-736](categories/CWE-736.md) | CERT C Secure Coding Standard (2008) Chapter 3 - Declarations and Initialization (DCL) | Obsolete |
| [CWE-737](categories/CWE-737.md) | CERT C Secure Coding Standard (2008) Chapter 4 - Expressions (EXP) | Obsolete |
| [CWE-738](categories/CWE-738.md) | CERT C Secure Coding Standard (2008) Chapter 5 - Integers (INT) | Obsolete |
| [CWE-739](categories/CWE-739.md) | CERT C Secure Coding Standard (2008) Chapter 6 - Floating Point (FLP) | Obsolete |
| [CWE-740](categories/CWE-740.md) | CERT C Secure Coding Standard (2008) Chapter 7 - Arrays (ARR) | Obsolete |
| [CWE-741](categories/CWE-741.md) | CERT C Secure Coding Standard (2008) Chapter 8 - Characters and Strings (STR) | Obsolete |
| [CWE-742](categories/CWE-742.md) | CERT C Secure Coding Standard (2008) Chapter 9 - Memory Management (MEM) | Obsolete |
| [CWE-743](categories/CWE-743.md) | CERT C Secure Coding Standard (2008) Chapter 10 - Input Output (FIO) | Obsolete |
| [CWE-744](categories/CWE-744.md) | CERT C Secure Coding Standard (2008) Chapter 11 - Environment (ENV) | Obsolete |
| [CWE-745](categories/CWE-745.md) | CERT C Secure Coding Standard (2008) Chapter 12 - Signals (SIG) | Obsolete |
| [CWE-746](categories/CWE-746.md) | CERT C Secure Coding Standard (2008) Chapter 13 - Error Handling (ERR) | Obsolete |
| [CWE-747](categories/CWE-747.md) | CERT C Secure Coding Standard (2008) Chapter 14 - Miscellaneous (MSC) | Obsolete |
| [CWE-748](categories/CWE-748.md) | CERT C Secure Coding Standard (2008) Appendix - POSIX (POS) | Obsolete |
| [CWE-751](categories/CWE-751.md) | 2009 Top 25 - Insecure Interaction Between Components | Obsolete |
| [CWE-752](categories/CWE-752.md) | 2009 Top 25 - Risky Resource Management | Obsolete |
| [CWE-753](categories/CWE-753.md) | 2009 Top 25 - Porous Defenses | Obsolete |
| [CWE-801](categories/CWE-801.md) | 2010 Top 25 - Insecure Interaction Between Components | Obsolete |
| [CWE-802](categories/CWE-802.md) | 2010 Top 25 - Risky Resource Management | Obsolete |
| [CWE-803](categories/CWE-803.md) | 2010 Top 25 - Porous Defenses | Obsolete |
| [CWE-808](categories/CWE-808.md) | 2010 Top 25 - Weaknesses On the Cusp | Obsolete |
| [CWE-810](categories/CWE-810.md) | OWASP Top Ten 2010 Category A1 - Injection | Obsolete |
| [CWE-811](categories/CWE-811.md) | OWASP Top Ten 2010 Category A2 - Cross-Site Scripting (XSS) | Obsolete |
| [CWE-812](categories/CWE-812.md) | OWASP Top Ten 2010 Category A3 - Broken Authentication and Session Management | Obsolete |
| [CWE-813](categories/CWE-813.md) | OWASP Top Ten 2010 Category A4 - Insecure Direct Object References | Obsolete |
| [CWE-814](categories/CWE-814.md) | OWASP Top Ten 2010 Category A5 - Cross-Site Request Forgery(CSRF) | Obsolete |
| [CWE-815](categories/CWE-815.md) | OWASP Top Ten 2010 Category A6 - Security Misconfiguration | Obsolete |
| [CWE-816](categories/CWE-816.md) | OWASP Top Ten 2010 Category A7 - Insecure Cryptographic Storage | Obsolete |
| [CWE-817](categories/CWE-817.md) | OWASP Top Ten 2010 Category A8 - Failure to Restrict URL Access | Obsolete |
| [CWE-818](categories/CWE-818.md) | OWASP Top Ten 2010 Category A9 - Insufficient Transport Layer Protection | Obsolete |
| [CWE-819](categories/CWE-819.md) | OWASP Top Ten 2010 Category A10 - Unvalidated Redirects and Forwards | Obsolete |
| [CWE-840](categories/CWE-840.md) | Business Logic Errors | Incomplete |
| [CWE-845](categories/CWE-845.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 2 - Input Validation and Data Sanitization (IDS) | Obsolete |
| [CWE-846](categories/CWE-846.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 3 - Declarations and Initialization (DCL) | Obsolete |
| [CWE-847](categories/CWE-847.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 4 - Expressions (EXP) | Obsolete |
| [CWE-848](categories/CWE-848.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 5 - Numeric Types and Operations (NUM) | Obsolete |
| [CWE-849](categories/CWE-849.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 6 - Object Orientation (OBJ) | Obsolete |
| [CWE-850](categories/CWE-850.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 7 - Methods (MET) | Obsolete |
| [CWE-851](categories/CWE-851.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 8 - Exceptional Behavior (ERR) | Obsolete |
| [CWE-852](categories/CWE-852.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 9 - Visibility and Atomicity (VNA) | Obsolete |
| [CWE-853](categories/CWE-853.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 10 - Locking (LCK) | Obsolete |
| [CWE-854](categories/CWE-854.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 11 - Thread APIs (THI) | Obsolete |
| [CWE-855](categories/CWE-855.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 12 - Thread Pools (TPS) | Obsolete |
| [CWE-856](categories/CWE-856.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 13 - Thread-Safety Miscellaneous (TSM) | Obsolete |
| [CWE-857](categories/CWE-857.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 14 - Input Output (FIO) | Obsolete |
| [CWE-858](categories/CWE-858.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 15 - Serialization (SER) | Obsolete |
| [CWE-859](categories/CWE-859.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 16 - Platform Security (SEC) | Obsolete |
| [CWE-860](categories/CWE-860.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 17 - Runtime Environment (ENV) | Obsolete |
| [CWE-861](categories/CWE-861.md) | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 18 - Miscellaneous (MSC) | Obsolete |
| [CWE-864](categories/CWE-864.md) | 2011 Top 25 - Insecure Interaction Between Components | Obsolete |
| [CWE-865](categories/CWE-865.md) | 2011 Top 25 - Risky Resource Management | Obsolete |
| [CWE-866](categories/CWE-866.md) | 2011 Top 25 - Porous Defenses | Obsolete |
| [CWE-867](categories/CWE-867.md) | 2011 Top 25 - Weaknesses On the Cusp | Obsolete |
| [CWE-869](categories/CWE-869.md) | CERT C++ Secure Coding Section 01 - Preprocessor (PRE) | Incomplete |
| [CWE-870](categories/CWE-870.md) | CERT C++ Secure Coding Section 02 - Declarations and Initialization (DCL) | Incomplete |
| [CWE-871](categories/CWE-871.md) | CERT C++ Secure Coding Section 03 - Expressions (EXP) | Incomplete |
| [CWE-872](categories/CWE-872.md) | CERT C++ Secure Coding Section 04 - Integers (INT) | Incomplete |
| [CWE-873](categories/CWE-873.md) | CERT C++ Secure Coding Section 05 - Floating Point Arithmetic (FLP) | Incomplete |
| [CWE-874](categories/CWE-874.md) | CERT C++ Secure Coding Section 06 - Arrays and the STL (ARR) | Incomplete |
| [CWE-875](categories/CWE-875.md) | CERT C++ Secure Coding Section 07 - Characters and Strings (STR) | Incomplete |
| [CWE-876](categories/CWE-876.md) | CERT C++ Secure Coding Section 08 - Memory Management (MEM) | Incomplete |
| [CWE-877](categories/CWE-877.md) | CERT C++ Secure Coding Section 09 - Input Output (FIO) | Incomplete |
| [CWE-878](categories/CWE-878.md) | CERT C++ Secure Coding Section 10 - Environment (ENV) | Incomplete |
| [CWE-879](categories/CWE-879.md) | CERT C++ Secure Coding Section 11 - Signals (SIG) | Incomplete |
| [CWE-880](categories/CWE-880.md) | CERT C++ Secure Coding Section 12 - Exceptions and Error Handling (ERR) | Incomplete |
| [CWE-881](categories/CWE-881.md) | CERT C++ Secure Coding Section 13 - Object Oriented Programming (OOP) | Incomplete |
| [CWE-882](categories/CWE-882.md) | CERT C++ Secure Coding Section 14 - Concurrency (CON) | Incomplete |
| [CWE-883](categories/CWE-883.md) | CERT C++ Secure Coding Section 49 - Miscellaneous (MSC) | Incomplete |
| [CWE-885](categories/CWE-885.md) | SFP Primary Cluster: Risky Values | Incomplete |
| [CWE-886](categories/CWE-886.md) | SFP Primary Cluster: Unused entities | Incomplete |
| [CWE-887](categories/CWE-887.md) | SFP Primary Cluster: API | Incomplete |
| [CWE-889](categories/CWE-889.md) | SFP Primary Cluster: Exception Management | Incomplete |
| [CWE-890](categories/CWE-890.md) | SFP Primary Cluster: Memory Access | Incomplete |
| [CWE-891](categories/CWE-891.md) | SFP Primary Cluster: Memory Management | Incomplete |
| [CWE-892](categories/CWE-892.md) | SFP Primary Cluster: Resource Management | Incomplete |
| [CWE-893](categories/CWE-893.md) | SFP Primary Cluster: Path Resolution | Incomplete |
| [CWE-894](categories/CWE-894.md) | SFP Primary Cluster: Synchronization | Incomplete |
| [CWE-895](categories/CWE-895.md) | SFP Primary Cluster: Information Leak | Incomplete |
| [CWE-896](categories/CWE-896.md) | SFP Primary Cluster: Tainted Input | Incomplete |
| [CWE-897](categories/CWE-897.md) | SFP Primary Cluster: Entry Points | Incomplete |
| [CWE-898](categories/CWE-898.md) | SFP Primary Cluster: Authentication | Incomplete |
| [CWE-899](categories/CWE-899.md) | SFP Primary Cluster: Access Control | Incomplete |
| [CWE-901](categories/CWE-901.md) | SFP Primary Cluster: Privilege | Incomplete |
| [CWE-902](categories/CWE-902.md) | SFP Primary Cluster: Channel | Incomplete |
| [CWE-903](categories/CWE-903.md) | SFP Primary Cluster: Cryptography | Incomplete |
| [CWE-904](categories/CWE-904.md) | SFP Primary Cluster: Malware | Incomplete |
| [CWE-905](categories/CWE-905.md) | SFP Primary Cluster: Predictability | Incomplete |
| [CWE-906](categories/CWE-906.md) | SFP Primary Cluster: UI | Incomplete |
| [CWE-907](categories/CWE-907.md) | SFP Primary Cluster: Other | Incomplete |
| [CWE-929](categories/CWE-929.md) | OWASP Top Ten 2013 Category A1 - Injection | Obsolete |
| [CWE-930](categories/CWE-930.md) | OWASP Top Ten 2013 Category A2 - Broken Authentication and Session Management | Obsolete |
| [CWE-931](categories/CWE-931.md) | OWASP Top Ten 2013 Category A3 - Cross-Site Scripting (XSS) | Obsolete |
| [CWE-932](categories/CWE-932.md) | OWASP Top Ten 2013 Category A4 - Insecure Direct Object References | Obsolete |
| [CWE-933](categories/CWE-933.md) | OWASP Top Ten 2013 Category A5 - Security Misconfiguration | Obsolete |
| [CWE-934](categories/CWE-934.md) | OWASP Top Ten 2013 Category A6 - Sensitive Data Exposure | Obsolete |
| [CWE-935](categories/CWE-935.md) | OWASP Top Ten 2013 Category A7 - Missing Function Level Access Control | Obsolete |
| [CWE-936](categories/CWE-936.md) | OWASP Top Ten 2013 Category A8 - Cross-Site Request Forgery (CSRF) | Obsolete |
| [CWE-937](categories/CWE-937.md) | OWASP Top Ten 2013 Category A9 - Using Components with Known Vulnerabilities | Obsolete |
| [CWE-938](categories/CWE-938.md) | OWASP Top Ten 2013 Category A10 - Unvalidated Redirects and Forwards | Obsolete |
| [CWE-944](categories/CWE-944.md) | SFP Secondary Cluster: Access Management | Incomplete |
| [CWE-945](categories/CWE-945.md) | SFP Secondary Cluster: Insecure Resource Access | Incomplete |
| [CWE-946](categories/CWE-946.md) | SFP Secondary Cluster: Insecure Resource Permissions | Incomplete |
| [CWE-947](categories/CWE-947.md) | SFP Secondary Cluster: Authentication Bypass | Incomplete |
| [CWE-948](categories/CWE-948.md) | SFP Secondary Cluster: Digital Certificate | Incomplete |
| [CWE-949](categories/CWE-949.md) | SFP Secondary Cluster: Faulty Endpoint Authentication | Incomplete |
| [CWE-950](categories/CWE-950.md) | SFP Secondary Cluster: Hardcoded Sensitive Data | Incomplete |
| [CWE-951](categories/CWE-951.md) | SFP Secondary Cluster: Insecure Authentication Policy | Incomplete |
| [CWE-952](categories/CWE-952.md) | SFP Secondary Cluster: Missing Authentication | Incomplete |
| [CWE-953](categories/CWE-953.md) | SFP Secondary Cluster: Missing Endpoint Authentication | Incomplete |
| [CWE-954](categories/CWE-954.md) | SFP Secondary Cluster: Multiple Binds to the Same Port | Incomplete |
| [CWE-955](categories/CWE-955.md) | SFP Secondary Cluster: Unrestricted Authentication | Incomplete |
| [CWE-956](categories/CWE-956.md) | SFP Secondary Cluster: Channel Attack | Incomplete |
| [CWE-957](categories/CWE-957.md) | SFP Secondary Cluster: Protocol Error | Incomplete |
| [CWE-958](categories/CWE-958.md) | SFP Secondary Cluster: Broken Cryptography | Incomplete |
| [CWE-959](categories/CWE-959.md) | SFP Secondary Cluster: Weak Cryptography | Incomplete |
| [CWE-960](categories/CWE-960.md) | SFP Secondary Cluster: Ambiguous Exception Type | Incomplete |
| [CWE-961](categories/CWE-961.md) | SFP Secondary Cluster: Incorrect Exception Behavior | Incomplete |
| [CWE-962](categories/CWE-962.md) | SFP Secondary Cluster: Unchecked Status Condition | Incomplete |
| [CWE-963](categories/CWE-963.md) | SFP Secondary Cluster: Exposed Data | Incomplete |
| [CWE-964](categories/CWE-964.md) | SFP Secondary Cluster: Exposure Temporary File | Incomplete |
| [CWE-965](categories/CWE-965.md) | SFP Secondary Cluster: Insecure Session Management | Incomplete |
| [CWE-966](categories/CWE-966.md) | SFP Secondary Cluster: Other Exposures | Incomplete |
| [CWE-967](categories/CWE-967.md) | SFP Secondary Cluster: State Disclosure | Incomplete |
| [CWE-968](categories/CWE-968.md) | SFP Secondary Cluster: Covert Channel | Incomplete |
| [CWE-969](categories/CWE-969.md) | SFP Secondary Cluster: Faulty Memory Release | Incomplete |
| [CWE-970](categories/CWE-970.md) | SFP Secondary Cluster: Faulty Buffer Access | Incomplete |
| [CWE-971](categories/CWE-971.md) | SFP Secondary Cluster: Faulty Pointer Use | Incomplete |
| [CWE-972](categories/CWE-972.md) | SFP Secondary Cluster: Faulty String Expansion | Incomplete |
| [CWE-973](categories/CWE-973.md) | SFP Secondary Cluster: Improper NULL Termination | Incomplete |
| [CWE-974](categories/CWE-974.md) | SFP Secondary Cluster: Incorrect Buffer Length Computation | Incomplete |
| [CWE-975](categories/CWE-975.md) | SFP Secondary Cluster: Architecture | Incomplete |
| [CWE-976](categories/CWE-976.md) | SFP Secondary Cluster: Compiler | Incomplete |
| [CWE-977](categories/CWE-977.md) | SFP Secondary Cluster: Design | Incomplete |
| [CWE-978](categories/CWE-978.md) | SFP Secondary Cluster: Implementation | Incomplete |
| [CWE-979](categories/CWE-979.md) | SFP Secondary Cluster: Failed Chroot Jail | Incomplete |
| [CWE-980](categories/CWE-980.md) | SFP Secondary Cluster: Link in Resource Name Resolution | Incomplete |
| [CWE-981](categories/CWE-981.md) | SFP Secondary Cluster: Path Traversal | Incomplete |
| [CWE-982](categories/CWE-982.md) | SFP Secondary Cluster: Failure to Release Resource | Incomplete |
| [CWE-983](categories/CWE-983.md) | SFP Secondary Cluster: Faulty Resource Use | Incomplete |
| [CWE-984](categories/CWE-984.md) | SFP Secondary Cluster: Life Cycle | Incomplete |
| [CWE-985](categories/CWE-985.md) | SFP Secondary Cluster: Unrestricted Consumption | Incomplete |
| [CWE-986](categories/CWE-986.md) | SFP Secondary Cluster: Missing Lock | Incomplete |
| [CWE-987](categories/CWE-987.md) | SFP Secondary Cluster: Multiple Locks/Unlocks | Incomplete |
| [CWE-988](categories/CWE-988.md) | SFP Secondary Cluster: Race Condition Window | Incomplete |
| [CWE-989](categories/CWE-989.md) | SFP Secondary Cluster: Unrestricted Lock | Incomplete |
| [CWE-990](categories/CWE-990.md) | SFP Secondary Cluster: Tainted Input to Command | Incomplete |
| [CWE-991](categories/CWE-991.md) | SFP Secondary Cluster: Tainted Input to Environment | Incomplete |
| [CWE-992](categories/CWE-992.md) | SFP Secondary Cluster: Faulty Input Transformation | Incomplete |
| [CWE-993](categories/CWE-993.md) | SFP Secondary Cluster: Incorrect Input Handling | Incomplete |
| [CWE-994](categories/CWE-994.md) | SFP Secondary Cluster: Tainted Input to Variable | Incomplete |
| [CWE-995](categories/CWE-995.md) | SFP Secondary Cluster: Feature | Incomplete |
| [CWE-996](categories/CWE-996.md) | SFP Secondary Cluster: Security | Incomplete |
| [CWE-997](categories/CWE-997.md) | SFP Secondary Cluster: Information Loss | Incomplete |
| [CWE-998](categories/CWE-998.md) | SFP Secondary Cluster: Glitch in Computation | Incomplete |
| [CWE-1001](categories/CWE-1001.md) | SFP Secondary Cluster: Use of an Improper API | Incomplete |
| [CWE-1002](categories/CWE-1002.md) | SFP Secondary Cluster: Unexpected Entry Points | Incomplete |
| [CWE-1005](categories/CWE-1005.md) | 7PK - Input Validation and Representation | Draft |
| [CWE-1006](categories/CWE-1006.md) | Bad Coding Practices | Draft |
| [CWE-1009](categories/CWE-1009.md) | Audit | Draft |
| [CWE-1010](categories/CWE-1010.md) | Authenticate Actors | Draft |
| [CWE-1011](categories/CWE-1011.md) | Authorize Actors | Draft |
| [CWE-1012](categories/CWE-1012.md) | Cross Cutting | Draft |
| [CWE-1013](categories/CWE-1013.md) | Encrypt Data | Draft |
| [CWE-1014](categories/CWE-1014.md) | Identify Actors | Draft |
| [CWE-1015](categories/CWE-1015.md) | Limit Access | Draft |
| [CWE-1016](categories/CWE-1016.md) | Limit Exposure | Draft |
| [CWE-1017](categories/CWE-1017.md) | Lock Computer | Draft |
| [CWE-1018](categories/CWE-1018.md) | Manage User Sessions | Draft |
| [CWE-1019](categories/CWE-1019.md) | Validate Inputs | Draft |
| [CWE-1020](categories/CWE-1020.md) | Verify Message Integrity | Draft |
| [CWE-1027](categories/CWE-1027.md) | OWASP Top Ten 2017 Category A1 - Injection | Incomplete |
| [CWE-1028](categories/CWE-1028.md) | OWASP Top Ten 2017 Category A2 - Broken Authentication | Incomplete |
| [CWE-1029](categories/CWE-1029.md) | OWASP Top Ten 2017 Category A3 - Sensitive Data Exposure | Incomplete |
| [CWE-1030](categories/CWE-1030.md) | OWASP Top Ten 2017 Category A4 - XML External Entities (XXE) | Incomplete |
| [CWE-1031](categories/CWE-1031.md) | OWASP Top Ten 2017 Category A5 - Broken Access Control | Incomplete |
| [CWE-1032](categories/CWE-1032.md) | OWASP Top Ten 2017 Category A6 - Security Misconfiguration | Incomplete |
| [CWE-1033](categories/CWE-1033.md) | OWASP Top Ten 2017 Category A7 - Cross-Site Scripting (XSS) | Incomplete |
| [CWE-1034](categories/CWE-1034.md) | OWASP Top Ten 2017 Category A8 - Insecure Deserialization | Incomplete |
| [CWE-1035](categories/CWE-1035.md) | OWASP Top Ten 2017 Category A9 - Using Components with Known Vulnerabilities | Incomplete |
| [CWE-1036](categories/CWE-1036.md) | OWASP Top Ten 2017 Category A10 - Insufficient Logging & Monitoring | Incomplete |
| [CWE-1129](categories/CWE-1129.md) | CISQ Quality Measures (2016) - Reliability | Draft |
| [CWE-1130](categories/CWE-1130.md) | CISQ Quality Measures (2016) - Maintainability | Draft |
| [CWE-1131](categories/CWE-1131.md) | CISQ Quality Measures (2016) - Security | Draft |
| [CWE-1132](categories/CWE-1132.md) | CISQ Quality Measures (2016) - Performance Efficiency | Draft |
| [CWE-1134](categories/CWE-1134.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 00. Input Validation and Data Sanitization (IDS) | Stable |
| [CWE-1135](categories/CWE-1135.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 01. Declarations and Initialization (DCL) | Stable |
| [CWE-1136](categories/CWE-1136.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 02. Expressions (EXP) | Stable |
| [CWE-1137](categories/CWE-1137.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 03. Numeric Types and Operations (NUM) | Stable |
| [CWE-1138](categories/CWE-1138.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 04. Characters and Strings (STR) | Stable |
| [CWE-1139](categories/CWE-1139.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 05. Object Orientation (OBJ) | Stable |
| [CWE-1140](categories/CWE-1140.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 06. Methods (MET) | Stable |
| [CWE-1141](categories/CWE-1141.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 07. Exceptional Behavior (ERR) | Stable |
| [CWE-1142](categories/CWE-1142.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 08. Visibility and Atomicity (VNA) | Stable |
| [CWE-1143](categories/CWE-1143.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 09. Locking (LCK) | Stable |
| [CWE-1144](categories/CWE-1144.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 10. Thread APIs (THI) | Stable |
| [CWE-1145](categories/CWE-1145.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 11. Thread Pools (TPS) | Stable |
| [CWE-1146](categories/CWE-1146.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 12. Thread-Safety Miscellaneous (TSM) | Stable |
| [CWE-1147](categories/CWE-1147.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 13. Input Output (FIO) | Stable |
| [CWE-1148](categories/CWE-1148.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 14. Serialization (SER) | Stable |
| [CWE-1149](categories/CWE-1149.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 15. Platform Security (SEC) | Stable |
| [CWE-1150](categories/CWE-1150.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 16. Runtime Environment (ENV) | Stable |
| [CWE-1151](categories/CWE-1151.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 17. Java Native Interface (JNI) | Stable |
| [CWE-1152](categories/CWE-1152.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 49. Miscellaneous (MSC) | Stable |
| [CWE-1153](categories/CWE-1153.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 50. Android (DRD) | Stable |
| [CWE-1155](categories/CWE-1155.md) | SEI CERT C Coding Standard - Guidelines 01. Preprocessor (PRE) | Stable |
| [CWE-1156](categories/CWE-1156.md) | SEI CERT C Coding Standard - Guidelines 02. Declarations and Initialization (DCL) | Stable |
| [CWE-1157](categories/CWE-1157.md) | SEI CERT C Coding Standard - Guidelines 03. Expressions (EXP) | Stable |
| [CWE-1158](categories/CWE-1158.md) | SEI CERT C Coding Standard - Guidelines 04. Integers (INT) | Stable |
| [CWE-1159](categories/CWE-1159.md) | SEI CERT C Coding Standard - Guidelines 05. Floating Point (FLP) | Stable |
| [CWE-1160](categories/CWE-1160.md) | SEI CERT C Coding Standard - Guidelines 06. Arrays (ARR) | Stable |
| [CWE-1161](categories/CWE-1161.md) | SEI CERT C Coding Standard - Guidelines 07. Characters and Strings (STR) | Stable |
| [CWE-1162](categories/CWE-1162.md) | SEI CERT C Coding Standard - Guidelines 08. Memory Management (MEM) | Stable |
| [CWE-1163](categories/CWE-1163.md) | SEI CERT C Coding Standard - Guidelines 09. Input Output (FIO) | Stable |
| [CWE-1165](categories/CWE-1165.md) | SEI CERT C Coding Standard - Guidelines 10. Environment (ENV) | Stable |
| [CWE-1166](categories/CWE-1166.md) | SEI CERT C Coding Standard - Guidelines 11. Signals (SIG) | Stable |
| [CWE-1167](categories/CWE-1167.md) | SEI CERT C Coding Standard - Guidelines 12. Error Handling (ERR) | Stable |
| [CWE-1168](categories/CWE-1168.md) | SEI CERT C Coding Standard - Guidelines 13. Application Programming Interfaces (API) | Stable |
| [CWE-1169](categories/CWE-1169.md) | SEI CERT C Coding Standard - Guidelines 14. Concurrency (CON) | Stable |
| [CWE-1170](categories/CWE-1170.md) | SEI CERT C Coding Standard - Guidelines 48. Miscellaneous (MSC) | Stable |
| [CWE-1171](categories/CWE-1171.md) | SEI CERT C Coding Standard - Guidelines 50. POSIX (POS) | Stable |
| [CWE-1172](categories/CWE-1172.md) | SEI CERT C Coding Standard - Guidelines 51. Microsoft Windows (WIN) | Stable |
| [CWE-1175](categories/CWE-1175.md) | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 18. Concurrency (CON) | Stable |
| [CWE-1179](categories/CWE-1179.md) | SEI CERT Perl Coding Standard - Guidelines 01. Input Validation and Data Sanitization (IDS) | Stable |
| [CWE-1180](categories/CWE-1180.md) | SEI CERT Perl Coding Standard - Guidelines 02. Declarations and Initialization (DCL) | Stable |
| [CWE-1181](categories/CWE-1181.md) | SEI CERT Perl Coding Standard - Guidelines 03. Expressions (EXP) | Stable |
| [CWE-1182](categories/CWE-1182.md) | SEI CERT Perl Coding Standard - Guidelines 04. Integers (INT) | Stable |
| [CWE-1183](categories/CWE-1183.md) | SEI CERT Perl Coding Standard - Guidelines 05. Strings (STR) | Stable |
| [CWE-1184](categories/CWE-1184.md) | SEI CERT Perl Coding Standard - Guidelines 06. Object-Oriented Programming (OOP) | Stable |
| [CWE-1185](categories/CWE-1185.md) | SEI CERT Perl Coding Standard - Guidelines 07. File Input and Output (FIO) | Stable |
| [CWE-1186](categories/CWE-1186.md) | SEI CERT Perl Coding Standard - Guidelines 50. Miscellaneous (MSC) | Stable |
| [CWE-1195](categories/CWE-1195.md) | Manufacturing and Life Cycle Management Concerns | Draft |
| [CWE-1196](categories/CWE-1196.md) | Security Flow Issues | Draft |
| [CWE-1197](categories/CWE-1197.md) | Integration Issues | Draft |
| [CWE-1198](categories/CWE-1198.md) | Privilege Separation and Access Control Issues | Draft |
| [CWE-1199](categories/CWE-1199.md) | General Circuit and Logic Design Concerns | Draft |
| [CWE-1201](categories/CWE-1201.md) | Core and Compute Issues | Draft |
| [CWE-1202](categories/CWE-1202.md) | Memory and Storage Issues | Draft |
| [CWE-1203](categories/CWE-1203.md) | Peripherals, On-chip Fabric, and Interface/IO Problems | Draft |
| [CWE-1205](categories/CWE-1205.md) | Security Primitives and Cryptography Issues | Draft |
| [CWE-1206](categories/CWE-1206.md) | Power, Clock, Thermal, and Reset Concerns | Draft |
| [CWE-1207](categories/CWE-1207.md) | Debug and Test Problems | Draft |
| [CWE-1208](categories/CWE-1208.md) | Cross-Cutting Problems | Draft |
| [CWE-1210](categories/CWE-1210.md) | Audit / Logging Errors | Draft |
| [CWE-1211](categories/CWE-1211.md) | Authentication Errors | Draft |
| [CWE-1212](categories/CWE-1212.md) | Authorization Errors | Draft |
| [CWE-1213](categories/CWE-1213.md) | Random Number Issues | Draft |
| [CWE-1214](categories/CWE-1214.md) | Data Integrity Issues | Draft |
| [CWE-1215](categories/CWE-1215.md) | Data Validation Issues | Draft |
| [CWE-1216](categories/CWE-1216.md) | Lockout Mechanism Errors | Draft |
| [CWE-1217](categories/CWE-1217.md) | User Session Errors | Draft |
| [CWE-1218](categories/CWE-1218.md) | Memory Buffer Errors | Draft |
| [CWE-1219](categories/CWE-1219.md) | File Handling Issues | Draft |
| [CWE-1225](categories/CWE-1225.md) | Documentation Issues | Draft |
| [CWE-1226](categories/CWE-1226.md) | Complexity Issues | Draft |
| [CWE-1227](categories/CWE-1227.md) | Encapsulation Issues | Draft |
| [CWE-1228](categories/CWE-1228.md) | API / Function Errors | Draft |
| [CWE-1237](categories/CWE-1237.md) | SFP Primary Cluster: Faulty Resource Release | Incomplete |
| [CWE-1238](categories/CWE-1238.md) | SFP Primary Cluster: Failure to Release Memory | Incomplete |
| [CWE-1306](categories/CWE-1306.md) | CISQ Quality Measures - Reliability | Incomplete |
| [CWE-1307](categories/CWE-1307.md) | CISQ Quality Measures - Maintainability | Incomplete |
| [CWE-1308](categories/CWE-1308.md) | CISQ Quality Measures - Security | Incomplete |
| [CWE-1309](categories/CWE-1309.md) | CISQ Quality Measures - Efficiency | Incomplete |
| [CWE-1345](categories/CWE-1345.md) | OWASP Top Ten 2021 Category A01:2021 - Broken Access Control | Incomplete |
| [CWE-1346](categories/CWE-1346.md) | OWASP Top Ten 2021 Category A02:2021 - Cryptographic Failures | Incomplete |
| [CWE-1347](categories/CWE-1347.md) | OWASP Top Ten 2021 Category A03:2021 - Injection | Incomplete |
| [CWE-1348](categories/CWE-1348.md) | OWASP Top Ten 2021 Category A04:2021 - Insecure Design | Incomplete |
| [CWE-1349](categories/CWE-1349.md) | OWASP Top Ten 2021 Category A05:2021 - Security Misconfiguration | Incomplete |
| [CWE-1352](categories/CWE-1352.md) | OWASP Top Ten 2021 Category A06:2021 - Vulnerable and Outdated Components | Incomplete |
| [CWE-1353](categories/CWE-1353.md) | OWASP Top Ten 2021 Category A07:2021 - Identification and Authentication Failures | Incomplete |
| [CWE-1354](categories/CWE-1354.md) | OWASP Top Ten 2021 Category A08:2021 - Software and Data Integrity Failures | Incomplete |
| [CWE-1355](categories/CWE-1355.md) | OWASP Top Ten 2021 Category A09:2021 - Security Logging and Monitoring Failures | Incomplete |
| [CWE-1356](categories/CWE-1356.md) | OWASP Top Ten 2021 Category A10:2021 - Server-Side Request Forgery (SSRF) | Incomplete |
| [CWE-1359](categories/CWE-1359.md) | ICS Communications | Incomplete |
| [CWE-1360](categories/CWE-1360.md) | ICS Dependencies (& Architecture) | Incomplete |
| [CWE-1361](categories/CWE-1361.md) | ICS Supply Chain | Incomplete |
| [CWE-1362](categories/CWE-1362.md) | ICS Engineering (Constructions/Deployment) | Incomplete |
| [CWE-1363](categories/CWE-1363.md) | ICS Operations (& Maintenance) | Incomplete |
| [CWE-1364](categories/CWE-1364.md) | ICS Communications: Zone Boundary Failures | Incomplete |
| [CWE-1365](categories/CWE-1365.md) | ICS Communications: Unreliability | Incomplete |
| [CWE-1366](categories/CWE-1366.md) | ICS Communications: Frail Security in Protocols | Incomplete |
| [CWE-1367](categories/CWE-1367.md) | ICS Dependencies (& Architecture): External Physical Systems | Incomplete |
| [CWE-1368](categories/CWE-1368.md) | ICS Dependencies (& Architecture): External Digital Systems | Incomplete |
| [CWE-1369](categories/CWE-1369.md) | ICS Supply Chain: IT/OT Convergence/Expansion | Incomplete |
| [CWE-1370](categories/CWE-1370.md) | ICS Supply Chain: Common Mode Frailties | Incomplete |
| [CWE-1371](categories/CWE-1371.md) | ICS Supply Chain: Poorly Documented or Undocumented Features | Incomplete |
| [CWE-1372](categories/CWE-1372.md) | ICS Supply Chain: OT Counterfeit and Malicious Corruption | Incomplete |
| [CWE-1373](categories/CWE-1373.md) | ICS Engineering (Construction/Deployment): Trust Model Problems | Incomplete |
| [CWE-1374](categories/CWE-1374.md) | ICS Engineering (Construction/Deployment): Maker Breaker Blindness | Incomplete |
| [CWE-1375](categories/CWE-1375.md) | ICS Engineering (Construction/Deployment): Gaps in Details/Data | Incomplete |
| [CWE-1376](categories/CWE-1376.md) | ICS Engineering (Construction/Deployment): Security Gaps in Commissioning | Incomplete |
| [CWE-1377](categories/CWE-1377.md) | ICS Engineering (Construction/Deployment): Inherent Predictability in Design | Incomplete |
| [CWE-1378](categories/CWE-1378.md) | ICS Operations (& Maintenance): Gaps in obligations and training | Incomplete |
| [CWE-1379](categories/CWE-1379.md) | ICS Operations (& Maintenance): Human factors in ICS environments | Incomplete |
| [CWE-1380](categories/CWE-1380.md) | ICS Operations (& Maintenance): Post-analysis changes | Incomplete |
| [CWE-1381](categories/CWE-1381.md) | ICS Operations (& Maintenance): Exploitable Standard Operational Procedures | Incomplete |
| [CWE-1382](categories/CWE-1382.md) | ICS Operations (& Maintenance): Emerging Energy Technologies | Incomplete |
| [CWE-1383](categories/CWE-1383.md) | ICS Operations (& Maintenance): Compliance/Conformance with Regulatory Requirements | Incomplete |
| [CWE-1388](categories/CWE-1388.md) | Physical Access Issues and Concerns | Draft |
| [CWE-1396](categories/CWE-1396.md) | Comprehensive Categorization: Access Control | Incomplete |
| [CWE-1397](categories/CWE-1397.md) | Comprehensive Categorization: Comparison | Incomplete |
| [CWE-1398](categories/CWE-1398.md) | Comprehensive Categorization: Component Interaction | Incomplete |
| [CWE-1399](categories/CWE-1399.md) | Comprehensive Categorization: Memory Safety | Incomplete |
| [CWE-1401](categories/CWE-1401.md) | Comprehensive Categorization: Concurrency | Incomplete |
| [CWE-1402](categories/CWE-1402.md) | Comprehensive Categorization: Encryption | Incomplete |
| [CWE-1403](categories/CWE-1403.md) | Comprehensive Categorization: Exposed Resource | Incomplete |
| [CWE-1404](categories/CWE-1404.md) | Comprehensive Categorization: File Handling | Incomplete |
| [CWE-1405](categories/CWE-1405.md) | Comprehensive Categorization: Improper Check or Handling of Exceptional Conditions | Incomplete |
| [CWE-1406](categories/CWE-1406.md) | Comprehensive Categorization: Improper Input Validation | Incomplete |
| [CWE-1407](categories/CWE-1407.md) | Comprehensive Categorization: Improper Neutralization | Incomplete |
| [CWE-1408](categories/CWE-1408.md) | Comprehensive Categorization: Incorrect Calculation | Incomplete |
| [CWE-1409](categories/CWE-1409.md) | Comprehensive Categorization: Injection | Incomplete |
| [CWE-1410](categories/CWE-1410.md) | Comprehensive Categorization: Insufficient Control Flow Management | Incomplete |
| [CWE-1411](categories/CWE-1411.md) | Comprehensive Categorization: Insufficient Verification of Data Authenticity | Incomplete |
| [CWE-1412](categories/CWE-1412.md) | Comprehensive Categorization: Poor Coding Practices | Incomplete |
| [CWE-1413](categories/CWE-1413.md) | Comprehensive Categorization: Protection Mechanism Failure | Incomplete |
| [CWE-1414](categories/CWE-1414.md) | Comprehensive Categorization: Randomness | Incomplete |
| [CWE-1415](categories/CWE-1415.md) | Comprehensive Categorization: Resource Control | Incomplete |
| [CWE-1416](categories/CWE-1416.md) | Comprehensive Categorization: Resource Lifecycle Management | Incomplete |
| [CWE-1417](categories/CWE-1417.md) | Comprehensive Categorization: Sensitive Information Exposure | Incomplete |
| [CWE-1418](categories/CWE-1418.md) | Comprehensive Categorization: Violation of Secure Design Principles | Incomplete |
| [CWE-1433](categories/CWE-1433.md) | 2025 MIHW Supplement: Expert Insights | Obsolete |
| [CWE-1436](categories/CWE-1436.md) | OWASP Top Ten 2025 Category A01:2025 - Broken Access Control | Incomplete |
| [CWE-1437](categories/CWE-1437.md) | OWASP Top Ten 2025 Category A02:2025 - Security Misconfiguration | Incomplete |
| [CWE-1438](categories/CWE-1438.md) | OWASP Top Ten 2025 Category A03:2025 - Software Supply Chain Failures | Incomplete |
| [CWE-1439](categories/CWE-1439.md) | OWASP Top Ten 2025 Category A04:2025 - Cryptographic Failures | Incomplete |
| [CWE-1440](categories/CWE-1440.md) | OWASP Top Ten 2025 Category A05:2025 - Injection | Incomplete |
| [CWE-1441](categories/CWE-1441.md) | OWASP Top Ten 2025 Category A06:2025 - Insecure Design | Incomplete |
| [CWE-1442](categories/CWE-1442.md) | OWASP Top Ten 2025 Category A07:2025 - Authentication Failures | Incomplete |
| [CWE-1443](categories/CWE-1443.md) | OWASP Top Ten 2025 Category A08:2025 - Software or Data Integrity Failures | Incomplete |
| [CWE-1444](categories/CWE-1444.md) | OWASP Top Ten 2025 Category A09:2025 - Logging & Alerting Failures | Incomplete |
| [CWE-1445](categories/CWE-1445.md) | OWASP Top Ten 2025 Category A10:2025 - Mishandling of Exceptional Conditions | Incomplete |

## Views

| ID | Name | Type | Status |
| --- | --- | --- | --- |
| [CWE-604](views/CWE-604.md) | Deprecated Entries | Implicit | Draft |
| [CWE-629](views/CWE-629.md) | Weaknesses in OWASP Top Ten (2007) | Graph | Obsolete |
| [CWE-630](views/CWE-630.md) | DEPRECATED: Weaknesses Examined by SAMATE | Explicit | Deprecated |
| [CWE-631](views/CWE-631.md) | DEPRECATED: Resource-specific Weaknesses | Graph | Deprecated |
| [CWE-635](views/CWE-635.md) | Weaknesses Originally Used by NVD from 2008 to 2016 | Explicit | Obsolete |
| [CWE-658](views/CWE-658.md) | Weaknesses in Software Written in C | Implicit | Draft |
| [CWE-659](views/CWE-659.md) | Weaknesses in Software Written in C++ | Implicit | Draft |
| [CWE-660](views/CWE-660.md) | Weaknesses in Software Written in Java | Implicit | Draft |
| [CWE-661](views/CWE-661.md) | Weaknesses in Software Written in PHP | Implicit | Draft |
| [CWE-677](views/CWE-677.md) | Weakness Base Elements | Implicit | Draft |
| [CWE-678](views/CWE-678.md) | Composites | Implicit | Draft |
| [CWE-679](views/CWE-679.md) | DEPRECATED: Chain Elements | Implicit | Deprecated |
| [CWE-699](views/CWE-699.md) | Software Development | Graph | Draft |
| [CWE-700](views/CWE-700.md) | Seven Pernicious Kingdoms | Graph | Incomplete |
| [CWE-701](views/CWE-701.md) | Weaknesses Introduced During Design | Implicit | Incomplete |
| [CWE-702](views/CWE-702.md) | Weaknesses Introduced During Implementation | Implicit | Incomplete |
| [CWE-709](views/CWE-709.md) | Named Chains | Implicit | Incomplete |
| [CWE-711](views/CWE-711.md) | Weaknesses in OWASP Top Ten (2004) | Graph | Obsolete |
| [CWE-734](views/CWE-734.md) | Weaknesses Addressed by the CERT C Secure Coding Standard (2008) | Graph | Obsolete |
| [CWE-750](views/CWE-750.md) | Weaknesses in the 2009 CWE/SANS Top 25 Most Dangerous Programming Errors | Graph | Obsolete |
| [CWE-800](views/CWE-800.md) | Weaknesses in the 2010 CWE/SANS Top 25 Most Dangerous Programming Errors | Graph | Obsolete |
| [CWE-809](views/CWE-809.md) | Weaknesses in OWASP Top Ten (2010) | Graph | Obsolete |
| [CWE-844](views/CWE-844.md) | Weaknesses Addressed by The CERT Oracle Secure Coding Standard for Java (2011) | Graph | Obsolete |
| [CWE-868](views/CWE-868.md) | Weaknesses Addressed by the SEI CERT C++ Coding Standard (2016 Version) | Graph | Obsolete |
| [CWE-884](views/CWE-884.md) | CWE Cross-section | Explicit | Incomplete |
| [CWE-888](views/CWE-888.md) | Software Fault Pattern (SFP) Clusters | Graph | Incomplete |
| [CWE-900](views/CWE-900.md) | Weaknesses in the 2011 CWE/SANS Top 25 Most Dangerous Software Errors | Graph | Obsolete |
| [CWE-919](views/CWE-919.md) | Weaknesses in Mobile Applications | Implicit | Incomplete |
| [CWE-928](views/CWE-928.md) | Weaknesses in OWASP Top Ten (2013) | Graph | Obsolete |
| [CWE-999](views/CWE-999.md) | DEPRECATED: Weaknesses without Software Fault Patterns | Implicit | Deprecated |
| [CWE-1000](views/CWE-1000.md) | Research Concepts | Graph | Draft |
| [CWE-1003](views/CWE-1003.md) | Weaknesses for Simplified Mapping of Published Vulnerabilities | Graph | Incomplete |
| [CWE-1008](views/CWE-1008.md) | Architectural Concepts | Graph | Incomplete |
| [CWE-1026](views/CWE-1026.md) | Weaknesses in OWASP Top Ten (2017) | Graph | Incomplete |
| [CWE-1040](views/CWE-1040.md) | Quality Weaknesses with Indirect Security Impacts | Implicit | Incomplete |
| [CWE-1081](views/CWE-1081.md) | Entries with Maintenance Notes | Implicit | Draft |
| [CWE-1128](views/CWE-1128.md) | CISQ Quality Measures (2016) | Graph | Incomplete |
| [CWE-1133](views/CWE-1133.md) | Weaknesses Addressed by the SEI CERT Oracle Coding Standard for Java | Graph | Stable |
| [CWE-1154](views/CWE-1154.md) | Weaknesses Addressed by the SEI CERT C Coding Standard | Graph | Stable |
| [CWE-1178](views/CWE-1178.md) | Weaknesses Addressed by the SEI CERT Perl Coding Standard | Graph | Stable |
| [CWE-1194](views/CWE-1194.md) | Hardware Design | Graph | Draft |
| [CWE-1200](views/CWE-1200.md) | Weaknesses in the 2019 CWE Top 25 Most Dangerous Software Errors | Graph | Stable |
| [CWE-1305](views/CWE-1305.md) | CISQ Quality Measures (2020) | Graph | Incomplete |
| [CWE-1337](views/CWE-1337.md) | Weaknesses in the 2021 CWE Top 25 Most Dangerous Software Weaknesses | Graph | Stable |
| [CWE-1340](views/CWE-1340.md) | CISQ Data Protection Measures | Graph | Incomplete |
| [CWE-1343](views/CWE-1343.md) | Weaknesses in the 2021 CWE Most Important Hardware Weaknesses List | Explicit | Stable |
| [CWE-1344](views/CWE-1344.md) | Weaknesses in OWASP Top Ten (2021) | Graph | Incomplete |
| [CWE-1350](views/CWE-1350.md) | Weaknesses in the 2020 CWE Top 25 Most Dangerous Software Weaknesses | Graph | Stable |
| [CWE-1358](views/CWE-1358.md) | Weaknesses in SEI ETF Categories of Security Vulnerabilities in ICS | Graph | Incomplete |
| [CWE-1387](views/CWE-1387.md) | Weaknesses in the 2022 CWE Top 25 Most Dangerous Software Weaknesses | Graph | Draft |
| [CWE-1400](views/CWE-1400.md) | Comprehensive Categorization for Software Assurance Trends | Graph | Draft |
| [CWE-1424](views/CWE-1424.md) | Weaknesses Addressed by ISA/IEC 62443 Requirements | Implicit | Draft |
| [CWE-1425](views/CWE-1425.md) | Weaknesses in the 2023 CWE Top 25 Most Dangerous Software Weaknesses | Graph | Draft |
| [CWE-1430](views/CWE-1430.md) | Weaknesses in the 2024 CWE Top 25 Most Dangerous Software Weaknesses | Graph | Draft |
| [CWE-1432](views/CWE-1432.md) | Weaknesses in the 2025 CWE Most Important Hardware Weaknesses List | Graph | Stable |
| [CWE-1435](views/CWE-1435.md) | Weaknesses in the 2025 CWE Top 25 Most Dangerous Software Weaknesses | Graph | Draft |
| [CWE-1450](views/CWE-1450.md) | Weaknesses in OWASP Top Ten RC1 (2025) | Graph | Incomplete |
| [CWE-2000](views/CWE-2000.md) | Comprehensive CWE Dictionary | Implicit | Draft |

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
