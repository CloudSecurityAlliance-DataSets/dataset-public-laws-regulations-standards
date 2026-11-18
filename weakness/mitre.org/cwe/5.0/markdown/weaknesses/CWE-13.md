---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-13"
cwe_id: "CWE-13"
entry_type: weakness
name: "ASP.NET Misconfiguration: Password in Configuration File"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
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

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

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

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://cwe.mitre.org/documents/sources/SevenPerniciousKingdoms.pdf>.
- [REF-103] Microsoft Corporation. "How To: Encrypt Configuration Sections in ASP.NET 2.0 Using DPAPI". <https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff647398(v=pandp.10)?redirectedfrom=MSDN> (URL validated: 2023-04-07).
- [REF-104] Microsoft Corporation. "How To: Encrypt Configuration Sections in ASP.NET 2.0 Using RSA". <https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff650304(v=pandp.10)?redirectedfrom=MSDN> (URL validated: 2023-04-07).
- [REF-105] Microsoft Corporation. ".NET Framework Developer's Guide - Securing Connection Strings". <http://msdn.microsoft.com/en-us/library/89211k9b(VS.80).aspx>.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
