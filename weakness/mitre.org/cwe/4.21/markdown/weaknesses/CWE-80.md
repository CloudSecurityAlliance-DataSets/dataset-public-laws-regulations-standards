---
secid: "secid:weakness/mitre.org/cwe@4.21#CWE-80"
cwe_id: "CWE-80"
entry_type: weakness
name: "Improper Neutralization of Script-Related HTML Tags in a Web Page"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.21"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/80.html"
---

# CWE-80: Improper Neutralization of Script-Related HTML Tags in a Web Page

## Description

The product receives input from an upstream component, but it does not neutralize or incorrectly neutralizes special characters such as "&lt;", ">", and "&" that could be interpreted as web-scripting elements when they are sent to a downstream component that processes web pages. (Roles: Acronym, Attack-Focused)

![Diagram for CWE-80](https://cwe.mitre.org/data/images/CWE-80-Diagram.png)

## Alternate Terms

- **Basic XSS**

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
| Technology |  | Web Based | Often |
| Technology | Web Server |  | Undetermined |

## Modes Of Introduction

- **Implementation**

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Integrity<br>Availability | Read Application Data<br>Execute Unauthorized Code or Commands | An attacker could insert special characters that are processed client-side in the context of the user's session. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Implementation

  Carefully check each input parameter against a rigorous positive specification (allowlist) defining the specific characters and format allowed. All input should be neutralized, not just parameters that the user is supposed to specify, but all data in the request, including hidden fields, cookies, headers, the URL itself, and so forth. A common mistake that leads to continuing XSS vulnerabilities is to validate only fields that are expected to be redisplayed by the site. We often encounter data from the request that is reflected by the application server or the application that the development team did not anticipate. Also, a field that is not currently reflected may be used by a future developer. Therefore, validating ALL parts of the HTTP request is recommended.

- **Phase:** Implementation · **Strategy:** Output Encoding · **ID:** MIT-30.1

  Use and specify an output encoding that can be handled by the downstream component that is reading the output. Common encodings include ISO-8859-1, UTF-7, and UTF-8. When an encoding is not specified, a downstream component may choose a different encoding, either by assuming a default encoding or automatically inferring which encoding is being used, which can be erroneous. When the encodings are inconsistent, the downstream component might treat some character or byte sequences as special, even if they are not special in the original encoding. Attackers might then be able to exploit this discrepancy and conduct injection attacks; they even might be able to bypass protection mechanisms that assume the original encoding is also being used by the downstream component.

  The problem of inconsistent output encodings often arises in web pages. If an encoding is not specified in an HTTP header, web browsers often guess about which encoding is being used. This can open up the browser to subtle XSS attacks.

- **Phase:** Implementation · **ID:** MIT-43

  With Struts, write all data from form beans with the bean's filter attribute set to true.

- **Phase:** Implementation · **Strategy:** Attack Surface Reduction · **ID:** MIT-31

  To help mitigate XSS attacks against the user's session cookie, set the session cookie to be HttpOnly. In browsers that support the HttpOnly feature (such as more recent versions of Internet Explorer and Firefox), this attribute can prevent the user's session cookie from being accessible to malicious client-side scripts that use document.cookie. This is not a complete solution, since HttpOnly is not supported by all browsers. More importantly, XmlHttpRequest and other powerful browser technologies provide read access to HTTP headers, including the Set-Cookie header in which the HttpOnly flag is set.

  **Effectiveness:** Defense in Depth

## Demonstrative Examples

### Example 1

In the following example, a guestbook comment isn't properly encoded, filtered, or otherwise neutralized for script-related tags before being displayed in a client browser.

*Example (Bad, JSP):*

```jsp
<% for (Iterator i = guestbook.iterator(); i.hasNext(); ) {
    Entry e = (Entry) i.next(); %>
    <p>Entry #<%= e.getId() %></p>
    <p><%= e.getText() %></p>
    <%
    } %>
```

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2002-0938](https://www.cve.org/CVERecord?id=CVE-2002-0938) | XSS in parameter in a link. |
| [CVE-2002-1495](https://www.cve.org/CVERecord?id=CVE-2002-1495) | XSS in web-based email product via attachment filenames. |
| [CVE-2003-1136](https://www.cve.org/CVERecord?id=CVE-2003-1136) | HTML injection in posted message. |
| [CVE-2004-2171](https://www.cve.org/CVERecord?id=CVE-2004-2171) | XSS not quoted in error page. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | Basic XSS |
| Software Fault Patterns | SFP24 | Tainted input to command |

## Related Attack Patterns

- [CAPEC-18](https://capec.mitre.org/data/definitions/18.html)
- [CAPEC-193](https://capec.mitre.org/data/definitions/193.html)
- [CAPEC-32](https://capec.mitre.org/data/definitions/32.html)
- [CAPEC-86](https://capec.mitre.org/data/definitions/86.html)

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Other**: Although this can be classified as an injection problem, the more pertinent issue is the improper conversion of such special characters to respective context-appropriate entities before displaying them to the user.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Sean Eidemiller | Cigital | CWE 1.0, 2008-09-09 | added/updated demonstrative examples |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-08-01 |  | KDM Analytics | CWE 1.0, 2008-09-09 | added/updated white box definitions |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2008-10-14 | CWE Content Team | MITRE | CWE 1.0.1, 2008-10-14 | updated Description |
| Modification | 2009-05-27 | CWE Content Team | MITRE | CWE 1.4, 2009-05-27 | updated Demonstrative_Examples, Description, Name |
| Modification | 2009-07-17 | KDM Analytics |  | CWE 1.5, 2009-07-27 | Improved the White_Box_Definition |
| Modification | 2009-07-27 | CWE Content Team | MITRE | CWE 1.5, 2009-07-27 | updated White_Box_Definitions |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Demonstrative_Examples, Description, Name, Potential_Mitigations |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Description, Potential_Mitigations |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Related_Attack_Patterns, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-05-03 | CWE Content Team | MITRE | CWE 2.11, 2017-05-05 | updated Potential_Mitigations, Related_Attack_Patterns |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Applicable_Platforms, Causal_Nature, Likelihood_of_Exploit, Relationships, White_Box_Definitions |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Potential_Mitigations |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Detection_Factors, Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Common_Consequences, Description, Diagram, Other_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms, Relationships |

**Previous Entry Names:**

- Basic XSS — 2008-04-11
- Failure to Sanitize Script-Related HTML Tags in a Web Page (Basic XSS) — 2009-05-27
- Improper Sanitization of Script-Related HTML Tags in a Web Page (Basic XSS) — 2010-06-21

---
Generated from MITRE's CWE 4.21 XML (cwec_v4.21.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.21/LICENSE.txt).
