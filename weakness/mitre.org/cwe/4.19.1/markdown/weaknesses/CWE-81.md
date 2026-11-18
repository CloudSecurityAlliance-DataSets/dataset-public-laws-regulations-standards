---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-81"
cwe_id: "CWE-81"
entry_type: weakness
name: "Improper Neutralization of Script in an Error Message Web Page"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/81.html"
---

# CWE-81: Improper Neutralization of Script in an Error Message Web Page

## Description

The product receives input from an upstream component, but it does not neutralize or incorrectly neutralizes special characters that could be interpreted as web-scripting elements when they are sent to an error page.

## Extended Description

Error pages may include customized 403 Forbidden or 404 Not Found pages.

When an attacker can trigger an error that contains script syntax within the attacker's input, then cross-site scripting attacks may be possible.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-79](../weaknesses/CWE-79.md) Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |
| CanAlsoBe | [CWE-209](../weaknesses/CWE-209.md) Generation of Error Message Containing Sensitive Information (Base) | [CWE-1000](../views/CWE-1000.md) |  |
| CanAlsoBe | [CWE-390](../weaknesses/CWE-390.md) Detection of Error Condition Without Action (Base) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Resultant**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Not Language-Specific | Undetermined |
| Technology |  | Web Based | Undetermined |
| Technology | Web Server |  | Undetermined |

## Modes Of Introduction

- **Implementation**
- **Operation**

## Common Consequences

| Scope | Impact |
| --- | --- |
| Confidentiality<br>Integrity<br>Availability | Read Application Data<br>Execute Unauthorized Code or Commands |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

## Potential Mitigations

- **Phase:** Implementation

  Do not write user-controlled input to error pages.

- **Phase:** Implementation

  Carefully check each input parameter against a rigorous positive specification (allowlist) defining the specific characters and format allowed. All input should be neutralized, not just parameters that the user is supposed to specify, but all data in the request, including hidden fields, cookies, headers, the URL itself, and so forth. A common mistake that leads to continuing XSS vulnerabilities is to validate only fields that are expected to be redisplayed by the site. We often encounter data from the request that is reflected by the application server or the application that the development team did not anticipate. Also, a field that is not currently reflected may be used by a future developer. Therefore, validating ALL parts of the HTTP request is recommended.

- **Phase:** Implementation · **Strategy:** Output Encoding · **ID:** MIT-30.1

  Use and specify an output encoding that can be handled by the downstream component that is reading the output. Common encodings include ISO-8859-1, UTF-7, and UTF-8. When an encoding is not specified, a downstream component may choose a different encoding, either by assuming a default encoding or automatically inferring which encoding is being used, which can be erroneous. When the encodings are inconsistent, the downstream component might treat some character or byte sequences as special, even if they are not special in the original encoding. Attackers might then be able to exploit this discrepancy and conduct injection attacks; they even might be able to bypass protection mechanisms that assume the original encoding is also being used by the downstream component.

  The problem of inconsistent output encodings often arises in web pages. If an encoding is not specified in an HTTP header, web browsers often guess about which encoding is being used. This can open up the browser to subtle XSS attacks.

- **Phase:** Implementation · **ID:** MIT-43

  With Struts, write all data from form beans with the bean's filter attribute set to true.

- **Phase:** Implementation · **Strategy:** Attack Surface Reduction · **ID:** MIT-31

  To help mitigate XSS attacks against the user's session cookie, set the session cookie to be HttpOnly. In browsers that support the HttpOnly feature (such as more recent versions of Internet Explorer and Firefox), this attribute can prevent the user's session cookie from being accessible to malicious client-side scripts that use document.cookie. This is not a complete solution, since HttpOnly is not supported by all browsers. More importantly, XMLHTTPRequest and other powerful browser technologies provide read access to HTTP headers, including the Set-Cookie header in which the HttpOnly flag is set.

  **Effectiveness:** Defense in Depth

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2002-0840](https://www.cve.org/CVERecord?id=CVE-2002-0840) | XSS in default error page from Host: header. |
| [CVE-2002-1053](https://www.cve.org/CVERecord?id=CVE-2002-1053) | XSS in error message. |
| [CVE-2002-1700](https://www.cve.org/CVERecord?id=CVE-2002-1700) | XSS in error page from targeted parameter. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | XSS in error pages |
| Software Fault Patterns | SFP24 | Tainted input to command |

## Related Attack Patterns

- [CAPEC-198](https://capec.mitre.org/data/definitions/198.html)

## References

- [REF-44] Michael Howard, David LeBlanc and John Viega. "24 Deadly Sins of Software Security". "Sin 11: Failure to Handle Errors Correctly." Page 183. McGraw-Hill. 2010.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
