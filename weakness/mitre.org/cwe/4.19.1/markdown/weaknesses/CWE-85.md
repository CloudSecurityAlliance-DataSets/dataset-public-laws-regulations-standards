---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-85"
cwe_id: "CWE-85"
entry_type: weakness
name: "Doubled Character XSS Manipulations"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/85.html"
---

# CWE-85: Doubled Character XSS Manipulations

## Description

The web application does not filter user-controlled input for executable script disguised using doubling of the involved characters.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-79](../weaknesses/CWE-79.md) Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |
| PeerOf | [CWE-675](../weaknesses/CWE-675.md) Multiple Operations on Resource in Single-Operation Context (Class) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Not Language-Specific | Undetermined |
| Technology |  | Web Based | Undetermined |
| Technology | Web Server |  | Undetermined |

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact |
| --- | --- |
| Confidentiality<br>Integrity<br>Availability | Read Application Data<br>Execute Unauthorized Code or Commands |

## Potential Mitigations

- **Phase:** Implementation

  Resolve all filtered input to absolute or canonical representations before processing.

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
| [CVE-2002-2086](https://www.cve.org/CVERecord?id=CVE-2002-2086) | XSS using "&lt;script". |
| [CVE-2000-0116](https://www.cve.org/CVERecord?id=CVE-2000-0116) | Encoded "javascript" in IMG tag. |
| [CVE-2001-1157](https://www.cve.org/CVERecord?id=CVE-2001-1157) | Extra "&lt;" in front of SCRIPT tag. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | DOUBLE - Doubled character XSS manipulations, e.g. "&lt;script" |
| Software Fault Patterns | SFP24 | Tainted input to command |

## Related Attack Patterns

- [CAPEC-245](https://capec.mitre.org/data/definitions/245.html)

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
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2010-04-05 | CWE Content Team | MITRE |  | updated Related_Attack_Patterns |
| Modification | 2010-06-21 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2010-12-13 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2011-03-29 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Related_Attack_Patterns, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-05-03 | CWE Content Team | MITRE |  | updated Potential_Mitigations, Related_Attack_Patterns |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Applicable_Platforms, Causal_Nature |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms |

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
