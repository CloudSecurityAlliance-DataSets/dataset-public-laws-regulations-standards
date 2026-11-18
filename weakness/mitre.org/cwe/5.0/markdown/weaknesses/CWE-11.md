---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-11"
cwe_id: "CWE-11"
entry_type: weakness
name: "ASP.NET Misconfiguration: Creating Debug Binary"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/11.html"
---

# CWE-11: ASP.NET Misconfiguration: Creating Debug Binary

## Description

The product has an ASP .NET component that contains a debug binary.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-489](../weaknesses/CWE-489.md) Active Debug Code (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Prevalence |
| --- | --- | --- |
| Language | ASP.NET | Undetermined |

## Background Details

ASP .NET applications can be configured to produce debug binaries. The debug attribute of the &lt;compilation> tag defines whether compiled binaries should include debugging information. The use of debug binaries causes an application to provide as much information about itself as possible to the user. Such binaries are only meant to be used in a development or testing environment.

## Modes Of Introduction

- **Implementation**
- **Build and Compilation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality | Read Application Data | Debug binaries give detailed debugging messages, which is useful in a development or testing environment, but can pose a security risk if the debug binary is deployed to production. Attackers can leverage the additional information they gain from debugging output to mount attacks targeted on the framework, database, or other resources used by the application. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** System Configuration

  Avoid releasing debug binaries into the production environment. Change the debug mode to false when the application is deployed into production.

## Demonstrative Examples

### Example 1

The file web.config contains the debug mode setting. Setting debug to "true" will let the browser display debugging information.

*Example (Bad, XML):*

```xml
<?xml version="1.0" encoding="utf-8" ?>
<configuration>
    <system.web>
        <compilation
        defaultLanguage="c#"
        debug="true"
        />
        ...
    </system.web>
</configuration>
```

Change the debug mode to false when the application is deployed into production.

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| 7 Pernicious Kingdoms | ASP.NET Misconfiguration: Creating Debug Binary |

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://cwe.mitre.org/documents/sources/SevenPerniciousKingdoms.pdf>.
- [REF-1513] CodeQL. "Creating an ASP.NET debug binary may reveal sensitive information". <https://codeql.github.com/codeql-query-help/csharp/cs-web-debug-binary/> (URL validated: 2025-12-07).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
