---
secid: "secid:weakness/mitre.org/cwe@4.21#CWE-84"
cwe_id: "CWE-84"
entry_type: weakness
name: "Improper Neutralization of Encoded URI Schemes in a Web Page"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.21"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/84.html"
---

# CWE-84: Improper Neutralization of Encoded URI Schemes in a Web Page

## Description

The web application improperly neutralizes user-controlled input for executable script disguised with URI encodings.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-79](../weaknesses/CWE-79.md) Improper Neutralization of Input During Web Page Generation (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

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
| Integrity | Unexpected State |

## Potential Mitigations

- **Phase:** Implementation · **Strategy:** Input Validation

  Resolve all URIs to absolute or canonical representations before processing.

- **Phase:** Implementation · **Strategy:** Input Validation

  Carefully check each input parameter against a rigorous positive specification (allowlist) defining the specific characters and format allowed. All input should be neutralized, not just parameters that the user is supposed to specify, but all data in the request, including tag attributes, hidden fields, cookies, headers, the URL itself, and so forth. A common mistake that leads to continuing XSS vulnerabilities is to validate only fields that are expected to be redisplayed by the site. We often encounter data from the request that is reflected by the application server or the application that the development team did not anticipate. Also, a field that is not currently reflected may be used by a future developer. Therefore, validating ALL parts of the HTTP request is recommended.

- **Phase:** Implementation · **Strategy:** Output Encoding · **ID:** MIT-30.1

  Use and specify an output encoding that can be handled by the downstream component that is reading the output. Common encodings include ISO-8859-1, UTF-7, and UTF-8. When an encoding is not specified, a downstream component may choose a different encoding, either by assuming a default encoding or automatically inferring which encoding is being used, which can be erroneous. When the encodings are inconsistent, the downstream component might treat some character or byte sequences as special, even if they are not special in the original encoding. Attackers might then be able to exploit this discrepancy and conduct injection attacks; they even might be able to bypass protection mechanisms that assume the original encoding is also being used by the downstream component.

  The problem of inconsistent output encodings often arises in web pages. If an encoding is not specified in an HTTP header, web browsers often guess about which encoding is being used. This can open up the browser to subtle XSS attacks.

- **Phase:** Implementation · **ID:** MIT-43

  With Struts, write all data from form beans with the bean's filter attribute set to true.

- **Phase:** Implementation · **Strategy:** Attack Surface Reduction · **ID:** MIT-31

  To help mitigate XSS attacks against the user's session cookie, set the session cookie to be HttpOnly. In browsers that support the HttpOnly feature (such as more recent versions of Internet Explorer and Firefox), this attribute can prevent the user's session cookie from being accessible to malicious client-side scripts that use document.cookie. This is not a complete solution, since HttpOnly is not supported by all browsers. More importantly, XmlHttpRequest and other powerful browser technologies provide read access to HTTP headers, including the Set-Cookie header in which the HttpOnly flag is set.

  **Effectiveness:** Defense in Depth

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2005-0563](https://www.cve.org/CVERecord?id=CVE-2005-0563) | Cross-site scripting (XSS) vulnerability in Microsoft Outlook Web Access (OWA) component in Exchange Server 5.5 allows remote attackers to inject arbitrary web script or HTML via an email message with an encoded javascript: URL ("jav&#X41sc&amp;#0010;ript:") in an IMG tag. |
| [CVE-2005-2276](https://www.cve.org/CVERecord?id=CVE-2005-2276) | Cross-site scripting (XSS) vulnerability in Novell Groupwise WebAccess 6.5 before July 11, 2005 allows remote attackers to inject arbitrary web script or HTML via an e-mail message with an encoded javascript URI (e.g. "j&#X41vascript" in an IMG tag). |
| [CVE-2005-0692](https://www.cve.org/CVERecord?id=CVE-2005-0692) | Encoded script within BBcode IMG tag. |
| [CVE-2002-0117](https://www.cve.org/CVERecord?id=CVE-2002-0117) | Encoded "javascript" in IMG tag. |
| [CVE-2002-0118](https://www.cve.org/CVERecord?id=CVE-2002-0118) | Encoded "javascript" in IMG tag. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | XSS using Script Via Encoded URI Schemes |
| Software Fault Patterns | SFP24 | Tainted input to command |

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2010-04-05 | CWE Content Team | MITRE | CWE 1.8.1, 2010-04-05 | updated Related_Attack_Patterns |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Description, Name, Potential_Mitigations |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Potential_Mitigations |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2011-06-27 | CWE Content Team | MITRE | CWE 2.0, 2011-06-27 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2013-02-21 | CWE Content Team | MITRE | CWE 2.4, 2013-02-21 | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-05-03 | CWE Content Team | MITRE | CWE 2.11, 2017-05-05 | updated Potential_Mitigations, Related_Attack_Patterns |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Applicable_Platforms, Causal_Nature |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Related_Attack_Patterns |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Potential_Mitigations |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms |

**Previous Entry Names:**

- XSS using Script Via Encoded URI Schemes — 2008-04-11
- Failure to Resolve Encoded URI Schemes in a Web Page — 2010-06-21

---
Generated from MITRE's CWE 4.21 XML (cwec_v4.21.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.21/LICENSE.txt).
