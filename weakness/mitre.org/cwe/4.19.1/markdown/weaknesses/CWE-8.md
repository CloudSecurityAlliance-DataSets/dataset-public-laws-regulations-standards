---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-8"
cwe_id: "CWE-8"
entry_type: weakness
name: "J2EE Misconfiguration: Entity Bean Declared Remote"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/8.html"
---

# CWE-8: J2EE Misconfiguration: Entity Bean Declared Remote

## Description

When an application exposes a remote interface for an entity bean, it might also expose methods that get or set the bean's data. These methods could be leveraged to read sensitive information, or to change data in ways that violate the application's expectations, potentially leading to other vulnerabilities.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-668](../weaknesses/CWE-668.md) Exposure of Resource to Wrong Sphere (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Prevalence |
| --- | --- | --- |
| Language | Java | Undetermined |

## Modes Of Introduction

- **Architecture and Design**
- **Implementation**

## Common Consequences

| Scope | Impact |
| --- | --- |
| Confidentiality<br>Integrity | Read Application Data<br>Modify Application Data |

## Potential Mitigations

- **Phase:** Implementation

  Declare Java beans "local" when possible. When a bean must be remotely accessible, make sure that sensitive information is not exposed, and ensure that the application logic performs appropriate validation of any data that might be modified by an attacker.

## Demonstrative Examples

### Example 1

The following example demonstrates the weakness.

*Example (Bad, XML):*

```xml
<ejb-jar>
    <enterprise-beans>
        <entity>
            <ejb-name>EmployeeRecord</ejb-name>
            <home>com.wombat.empl.EmployeeRecordHome</home>
            <remote>com.wombat.empl.EmployeeRecord</remote>
            ...
        </entity>
        ...
    </enterprise-beans>
</ejb-jar>
```

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| 7 Pernicious Kingdoms |  | J2EE Misconfiguration: Unsafe Bean Declaration |
| Software Fault Patterns | SFP23 | Exposed Data |

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://samate.nist.gov/SSATTM_Content/papers/Seven%20Pernicious%20Kingdoms%20-%20Taxonomy%20of%20Sw%20Security%20Errors%20-%20Tsipenyuk%20-%20Chess%20-%20McGraw.pdf>.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Other**: Entity beans that expose a remote interface become part of an application's attack surface. For performance reasons, an application should rarely use remote entity beans, so there is a good chance that a remote entity bean declaration is an error.

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
