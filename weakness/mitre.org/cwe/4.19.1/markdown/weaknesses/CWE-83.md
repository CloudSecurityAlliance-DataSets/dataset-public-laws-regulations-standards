---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-83"
cwe_id: "CWE-83"
entry_type: weakness
name: "Improper Neutralization of Script in Attributes in a Web Page"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/83.html"
---

# CWE-83: Improper Neutralization of Script in Attributes in a Web Page

## Description

The product does not neutralize or incorrectly neutralizes "javascript:" or other URIs from dangerous attributes within tags, such as onmouseover, onload, onerror, or style.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-79](../weaknesses/CWE-79.md) Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Not Language-Specific | Undetermined |
| Technology |  | Web Based | Often |
| Technology | Web Server |  | Undetermined |

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact |
| --- | --- |
| Confidentiality<br>Integrity<br>Availability | Read Application Data<br>Execute Unauthorized Code or Commands |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Implementation

  Carefully check each input parameter against a rigorous positive specification (allowlist) defining the specific characters and format allowed. All input should be neutralized, not just parameters that the user is supposed to specify, but all data in the request, including tag attributes, hidden fields, cookies, headers, the URL itself, and so forth. A common mistake that leads to continuing XSS vulnerabilities is to validate only fields that are expected to be redisplayed by the site. We often encounter data from the request that is reflected by the application server or the application that the development team did not anticipate. Also, a field that is not currently reflected may be used by a future developer. Therefore, validating ALL parts of the HTTP request is recommended.

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
| [CVE-2001-0520](https://www.cve.org/CVERecord?id=CVE-2001-0520) | Bypass filtering of SCRIPT tags using onload in BODY, href in A, BUTTON, INPUT, and others. |
| [CVE-2002-1493](https://www.cve.org/CVERecord?id=CVE-2002-1493) | guestbook XSS in STYLE or IMG SRC attributes. |
| [CVE-2002-1965](https://www.cve.org/CVERecord?id=CVE-2002-1965) | Javascript in onerror attribute of IMG tag. |
| [CVE-2002-1495](https://www.cve.org/CVERecord?id=CVE-2002-1495) | XSS in web-based email product via onmouseover event. |
| [CVE-2002-1681](https://www.cve.org/CVERecord?id=CVE-2002-1681) | XSS via script in &lt;P> tag. |
| [CVE-2004-1935](https://www.cve.org/CVERecord?id=CVE-2004-1935) | Onload, onmouseover, and other events in an e-mail attachment. |
| [CVE-2005-0945](https://www.cve.org/CVERecord?id=CVE-2005-0945) | Onmouseover and onload events in img, link, and mail tags. |
| [CVE-2003-1136](https://www.cve.org/CVERecord?id=CVE-2003-1136) | Javascript in onmouseover attribute in e-mail address or URL. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | XSS using Script in Attributes |
| Software Fault Patterns | SFP24 | Tainted input to command |

## Related Attack Patterns

- [CAPEC-243](https://capec.mitre.org/data/definitions/243.html)
- [CAPEC-244](https://capec.mitre.org/data/definitions/244.html)
- [CAPEC-588](https://capec.mitre.org/data/definitions/588.html)

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
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Relationships, Observed_Example, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2009-10-29 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2010-04-05 | CWE Content Team | MITRE |  | updated Description, Name, Related_Attack_Patterns |
| Modification | 2010-06-21 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2011-03-29 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-05-03 | CWE Content Team | MITRE |  | updated Potential_Mitigations, Related_Attack_Patterns |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Applicable_Platforms, Causal_Nature |
| Modification | 2019-06-20 | CWE Content Team | MITRE |  | updated Related_Attack_Patterns |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2021-10-28 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Detection_Factors, Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms, Relationships |

**Previous Entry Names:**

- XSS using Script in Attributes — 2008-04-11
- Failure to Sanitize Script in Attributes in a Web Page — 2010-04-05

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
