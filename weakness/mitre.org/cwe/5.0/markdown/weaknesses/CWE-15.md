---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-15"
cwe_id: "CWE-15"
entry_type: weakness
name: "External Control of System or Configuration Setting"
abstraction: Base
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/15.html"
---

# CWE-15: External Control of System or Configuration Setting

## Description

One or more system settings or configuration elements can be externally controlled by a user.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-642](../weaknesses/CWE-642.md) External Control of Critical State Data (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-610](../weaknesses/CWE-610.md) Externally Controlled Reference to a Resource in Another Sphere (Class) | [CWE-1000](../views/CWE-1000.md) |  |
| ChildOf | [CWE-20](../weaknesses/CWE-20.md) Improper Input Validation (Class) | [CWE-700](../views/CWE-700.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Technology | Not Technology-Specific | Undetermined |
| Technology | ICS/OT | Undetermined |

## Modes Of Introduction

- **Implementation**: Setting manipulation vulnerabilities occur when an attacker can control values that govern the behavior of the system, manage specific resources, or in some way affect the functionality of the application.
- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Other | Varies by Context | Allowing external control of system settings can disrupt service or cause an application to behave in unexpected, and potentially malicious ways. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Architecture and Design · **Strategy:** Separation of Privilege · **ID:** MIT-46

  Compartmentalize the system to have "safe" areas where trust boundaries can be unambiguously drawn. Do not allow sensitive data to go outside of the trust boundary and always be careful when interfacing with a compartment outside of the safe area.

  Ensure that appropriate compartmentalization is built into the system design, and the compartmentalization allows for and reinforces privilege separation functionality. Architects and designers should rely on the principle of least privilege to decide the appropriate time to use privileges and the time to drop privileges.

- **Phase:** Implementation; Architecture and Design

  Because setting manipulation covers a diverse set of functions, any attempt at illustrating it will inevitably be incomplete. Rather than searching for a tight-knit relationship between the functions addressed in the setting manipulation category, take a step back and consider the sorts of system values that an attacker should not be allowed to control.

- **Phase:** Implementation; Architecture and Design

  In general, do not allow user-provided or otherwise untrusted data to control sensitive values. The leverage that an attacker gains by controlling these values is not always immediately obvious, but do not underestimate the creativity of the attacker.

## Demonstrative Examples

### Example 1

The following C code accepts a number as one of its command line parameters and sets it as the host ID of the current machine.

*Example (Bad, C):*

```c
...
sethostid(argv[1]);
...
```

Although a process must be privileged to successfully invoke sethostid(), unprivileged users may be able to invoke the program. The code in this example allows user input to directly control the value of a system setting. If an attacker provides a malicious value for host ID, the attacker can misidentify the affected machine on the network or cause other unintended behavior.

### Example 2

The following Java code snippet reads a string from an HttpServletRequest and sets it as the active catalog for a database Connection.

*Example (Bad, Java):*

```java
...
conn.setCatalog(request.getParameter("catalog"));
...
```

In this example, an attacker could cause an error by providing a nonexistent catalog name or connect to an unauthorized portion of the database.

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| 7 Pernicious Kingdoms |  | Setting Manipulation |
| Software Fault Patterns | SFP25 | Tainted input to variable |

## Related Attack Patterns

- [CAPEC-13](https://capec.mitre.org/data/definitions/13.html)
- [CAPEC-146](https://capec.mitre.org/data/definitions/146.html)
- [CAPEC-176](https://capec.mitre.org/data/definitions/176.html)
- [CAPEC-203](https://capec.mitre.org/data/definitions/203.html)
- [CAPEC-270](https://capec.mitre.org/data/definitions/270.html)
- [CAPEC-271](https://capec.mitre.org/data/definitions/271.html)
- [CAPEC-579](https://capec.mitre.org/data/definitions/579.html)
- [CAPEC-69](https://capec.mitre.org/data/definitions/69.html)
- [CAPEC-76](https://capec.mitre.org/data/definitions/76.html)
- [CAPEC-77](https://capec.mitre.org/data/definitions/77.html)

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://cwe.mitre.org/documents/sources/SevenPerniciousKingdoms.pdf>.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
