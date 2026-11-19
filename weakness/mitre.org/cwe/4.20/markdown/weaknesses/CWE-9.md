---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-9"
cwe_id: "CWE-9"
entry_type: weakness
name: "J2EE Misconfiguration: Weak Access Permissions for EJB Methods"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/9.html"
---

# CWE-9: J2EE Misconfiguration: Weak Access Permissions for EJB Methods

## Description

If elevated access rights are assigned to EJB methods, then an attacker can take advantage of the permissions to exploit the product.

## Extended Description

If the EJB deployment descriptor contains one or more method permissions that grant access to the special ANYONE role, it indicates that access control for the application has not been fully thought through or that the application is structured in such a way that reasonable access control restrictions are impossible.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-266](../weaknesses/CWE-266.md) Incorrect Privilege Assignment (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

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
| Other | Other |

## Potential Mitigations

- **Phase:** Architecture and Design; System Configuration

  Follow the principle of least privilege when assigning access rights to EJB methods. Permission to invoke EJB methods should not be granted to the ANYONE role.

## Demonstrative Examples

### Example 1

The following deployment descriptor grants ANYONE permission to invoke the Employee EJB's method named getSalary().

*Example (Bad, XML):*

```xml
<ejb-jar>
    ...
    <assembly-descriptor>
        <method-permission>
            <role-name>ANYONE</role-name>
            <method>
            <ejb-name>Employee</ejb-name>
            <method-name>getSalary</method-name>
        </method-permission>
    </assembly-descriptor>
    ...
</ejb-jar>
```

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| 7 Pernicious Kingdoms | J2EE Misconfiguration: Weak Access Permissions |

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://samate.nist.gov/SSATTM_Content/papers/Seven%20Pernicious%20Kingdoms%20-%20Taxonomy%20of%20Sw%20Security%20Errors%20-%20Tsipenyuk%20-%20Chess%20-%20McGraw.pdf>.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | 7 Pernicious Kingdoms |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, Other_Notes, Taxonomy_Mappings |
| Modification | 2009-03-10 | CWE Content Team | MITRE | CWE 1.3, 2009-03-10 | updated Relationships |
| Modification | 2009-07-27 | CWE Content Team | MITRE | CWE 1.5, 2009-07-27 | updated Demonstrative_Examples |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2014-06-23 | CWE Content Team | MITRE | CWE 2.7, 2014-06-23 | updated Description, Other_Notes |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated References, Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms, Weakness_Ordinalities |

**Previous Entry Names:**

- J2EE Misconfiguration: Weak Access Permissions — 2008-04-11

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
