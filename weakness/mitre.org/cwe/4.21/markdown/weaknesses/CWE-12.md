---
secid: "secid:weakness/mitre.org/cwe@4.21#CWE-12"
cwe_id: "CWE-12"
entry_type: weakness
name: "ASP.NET Misconfiguration: Missing Custom Error Page"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.21"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/12.html"
---

# CWE-12: ASP.NET Misconfiguration: Missing Custom Error Page

## Description

An ASP .NET application must enable custom error pages in order to prevent attackers from mining information from the framework's built-in responses.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-756](../weaknesses/CWE-756.md) Missing Custom Error Page (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Prevalence |
| --- | --- | --- |
| Language | ASP.NET | Undetermined |

## Background Details

The mode attribute of the &lt;customErrors> tag defines whether custom or default error pages are used.

## Modes Of Introduction

- **Implementation**
- **Operation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality | Read Application Data | Default error pages gives detailed information about the error that occurred, and should not be used in production environments. Attackers can leverage the additional information provided by a default error page to mount attacks targeted on the framework, database, or other resources used by the application. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

## Potential Mitigations

- **Phase:** System Configuration

  Handle exceptions appropriately in source code. ASP .NET applications should be configured to use custom error pages instead of the framework default page.

- **Phase:** Architecture and Design

  Do not attempt to process an error or attempt to mask it.

- **Phase:** Implementation

  Verify return values are correct and do not supply sensitive information about the system.

## Demonstrative Examples

### Example 1 (DX-75)

The mode attribute of the &lt;customErrors> tag in the Web.config file defines whether custom or default error pages are used.

In the following insecure ASP.NET application setting, custom error message mode is turned off. An ASP.NET error message with detailed stack trace and platform versions will be returned.

*Example (Bad, ASP.NET):*

```asp.net
<customErrors mode="Off" />
```

A more secure setting is to set the custom error message mode for remote users only. No defaultRedirect error page is specified. The local user on the web server will see a detailed stack trace. For remote users, an ASP.NET error message with the server customError configuration setting and the platform version will be returned.

*Example (Good, ASP.NET):*

```asp.net
<customErrors mode="RemoteOnly" />
```

Another secure option is to set the mode attribute of the &lt;customErrors> tag to use a custom page as follows:

*Example (Good, ASP.NET):*

```asp.net
<customErrors mode="On" defaultRedirect="YourErrorPage.htm" />
```

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| 7 Pernicious Kingdoms | ASP.NET Misconfiguration: Missing Custom Error Handling |

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://cwe.mitre.org/documents/sources/SevenPerniciousKingdoms.pdf>.
- [REF-65] M. Howard, D. LeBlanc and J. Viega. "19 Deadly Sins of Software Security". McGraw-Hill/Osborne. 2005-07-26.
- [REF-66] OWASP, Fortify Software. "ASP.NET Misconfiguration: Missing Custom Error Handling". <https://www.owasp.org/index.php/ASP.NET_Misconfiguration:_Missing_Custom_Error_Handling>.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 4.21 XML (cwec_v4.21.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.21/LICENSE.txt).
