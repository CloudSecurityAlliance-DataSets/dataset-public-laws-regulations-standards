---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-13"
cwe_id: "CWE-13"
entry_type: weakness
name: "ASP.NET Misconfiguration: Password in Configuration File"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/13.html"
---

# CWE-13: ASP.NET Misconfiguration: Password in Configuration File

## Description

Storing a plaintext password in a configuration file allows anyone who can read the file access to the password-protected resource making them an easy target for attackers.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-260](../weaknesses/CWE-260.md) Password in Configuration File (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Prevalence |
| --- | --- | --- |
| Language | ASP.NET | Undetermined |

## Modes Of Introduction

- **Architecture and Design**
- **Implementation**

## Common Consequences

| Scope | Impact |
| --- | --- |
| Access Control | Gain Privileges or Assume Identity |

## Potential Mitigations

- **Phase:** Implementation

  Credentials stored in configuration files should be encrypted, Use standard APIs and industry accepted algorithms to encrypt the credentials stored in configuration files.

## Demonstrative Examples

### Example 1

The following example shows a portion of a configuration file for an ASP.Net application. This configuration file includes username and password information for a connection to a database, but the pair is stored in plaintext.

*Example (Bad, ASP.NET):*

```asp.net
...
<connectionStrings>
    <add name="ud_DEV" connectionString="connectDB=uDB; uid=db2admin; pwd=password; dbalias=uDB;" providerName="System.Data.Odbc" />
</connectionStrings>
...
```

Username and password information should not be included in a configuration file or a properties file in plaintext as this will allow anyone who can read the file access to the resource. If possible, encrypt this information.

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| 7 Pernicious Kingdoms | ASP.NET Misconfiguration: Password in Configuration File |

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://samate.nist.gov/SSATTM_Content/papers/Seven%20Pernicious%20Kingdoms%20-%20Taxonomy%20of%20Sw%20Security%20Errors%20-%20Tsipenyuk%20-%20Chess%20-%20McGraw.pdf>.
- [REF-103] Microsoft Corporation. "How To: Encrypt Configuration Sections in ASP.NET 2.0 Using DPAPI". <https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff647398(v=pandp.10)?redirectedfrom=MSDN> (URL validated: 2023-04-07).
- [REF-104] Microsoft Corporation. "How To: Encrypt Configuration Sections in ASP.NET 2.0 Using RSA". <https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff650304(v=pandp.10)?redirectedfrom=MSDN> (URL validated: 2023-04-07).
- [REF-105] Microsoft Corporation. ".NET Framework Developer's Guide - Securing Connection Strings". <http://msdn.microsoft.com/en-us/library/89211k9b(VS.80).aspx>.

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
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Relationships, References, Taxonomy_Mappings |
| Modification | 2009-07-27 | CWE Content Team | MITRE |  | updated Demonstrative_Examples |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE |  | updated Demonstrative_Examples |
| Modification | 2013-02-21 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Demonstrative_Examples, Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2018-03-27 | CWE Content Team | MITRE |  | updated Demonstrative_Examples |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated References, Relationships |
| Modification | 2021-03-15 | CWE Content Team | MITRE |  | updated Demonstrative_Examples |
| Modification | 2021-10-28 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated References, Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms, Relationships, Weakness_Ordinalities |

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
