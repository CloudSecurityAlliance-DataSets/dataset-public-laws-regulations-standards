---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-12"
cwe_id: "CWE-12"
entry_type: weakness
name: "ASP.NET Misconfiguration: Missing Custom Error Page"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
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

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://samate.nist.gov/SSATTM_Content/papers/Seven%20Pernicious%20Kingdoms%20-%20Taxonomy%20of%20Sw%20Security%20Errors%20-%20Tsipenyuk%20-%20Chess%20-%20McGraw.pdf>.
- [REF-65] M. Howard, D. LeBlanc and J. Viega. "19 Deadly Sins of Software Security". McGraw-Hill/Osborne. 2005-07-26.
- [REF-66] OWASP, Fortify Software. "ASP.NET Misconfiguration: Missing Custom Error Handling". <https://www.owasp.org/index.php/ASP.NET_Misconfiguration:_Missing_Custom_Error_Handling>.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | 7 Pernicious Kingdoms |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital |  | updated References, Demonstrative_Example, Potential_Mitigations, Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Relationships, Other_Notes, References, Taxonomy_Mappings |
| Modification | 2008-10-14 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2008-11-24 | CWE Content Team | MITRE |  | updated Common_Consequences, Other_Notes, Potential_Mitigations |
| Modification | 2009-03-10 | CWE Content Team | MITRE |  | updated Name, Relationships |
| Modification | 2009-07-27 | CWE Content Team | MITRE |  | updated Background_Details, Common_Consequences, Other_Notes |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2011-06-27 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Demonstrative_Examples, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2013-02-21 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Demonstrative_Examples, Potential_Mitigations, References, Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated References, Relationships |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated References |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Weakness_Ordinalities |

**Previous Entry Names:**

- ASP.NET Misconfiguration: Missing Custom Error Handling — 2009-03-10

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
