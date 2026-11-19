---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-99"
cwe_id: "CWE-99"
entry_type: weakness
name: "Improper Control of Resource Identifiers ('Resource Injection')"
abstraction: Class
structure: Simple
status: Draft
mapping_usage: Allowed-with-Review
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/99.html"
---

# CWE-99: Improper Control of Resource Identifiers ('Resource Injection')

## Description

The product receives input from an upstream component, but it does not restrict or incorrectly restricts the input before it is used as an identifier for a resource that may be outside the intended sphere of control.

## Extended Description

A resource injection issue occurs when the following two conditions are met:

1. An attacker can specify the identifier used to access a system resource. For example, an attacker might be able to specify part of the name of a file to be opened or a port number to be used.
2. By specifying the resource, the attacker gains a capability that would not otherwise be permitted. For example, the program may give the attacker the ability to overwrite the specified file, run with a configuration controlled by the attacker, or transmit sensitive information to a third-party server.

This may enable an attacker to access or modify otherwise protected system resources.

## Alternate Terms

- **Insecure Direct Object Reference**: OWASP uses this term, although it is effectively the same as resource injection.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| PeerOf | [CWE-706](../weaknesses/CWE-706.md) Use of Incorrectly-Resolved Name or Reference (Class) | [CWE-1000](../views/CWE-1000.md) |  |
| CanAlsoBe | [CWE-73](../weaknesses/CWE-73.md) External Control of File Name or Path (Base) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Modes Of Introduction

- **Architecture and Design**
- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Integrity | Read Application Data<br>Modify Application Data<br>Read Files or Directories<br>Modify Files or Directories | An attacker could gain access to or modify sensitive data or system resources. This could allow access to protected files or directories including configuration files and files containing sensitive information. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, it can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

## Demonstrative Examples

### Example 1

The following Java code uses input from an HTTP request to create a file name. The programmer has not considered the possibility that an attacker could provide a file name such as "../../tomcat/conf/server.xml", which causes the application to delete one of its own configuration files.

*Example (Bad, Java):*

```java
String rName = request.getParameter("reportName");
File rFile = new File("/usr/local/apfr/reports/" + rName);
...
rFile.delete();
```

### Example 2

The following code uses input from the command line to determine which file to open and echo back to the user. If the program runs with privileges and malicious users can create soft links to the file, they can use the program to read the first part of any file on the system.

*Example (Bad, C++):*

```c++
ifstream ifs(argv[0]);
string s;
ifs >> s;
cout << s;
```

The kind of resource the data affects indicates the kind of content that may be dangerous. For example, data containing special characters like period, slash, and backslash, are risky when used in methods that interact with the file system. (Resource injection, when it is related to file system resources, sometimes goes by the name "path manipulation.") Similarly, data that contains URLs and URIs is risky for functions that create remote connections.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2013-4787](https://www.cve.org/CVERecord?id=CVE-2013-4787) | chain: mobile OS verifies cryptographic signature of file in an archive, but then installs a different file with the same name that is also listed in the archive. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| 7 Pernicious Kingdoms |  | Resource Injection |
| Software Fault Patterns | SFP24 | Tainted input to command |
| OMG ASCSM | ASCSM-CWE-99 |  |

## Related Attack Patterns

- [CAPEC-10](https://capec.mitre.org/data/definitions/10.html)
- [CAPEC-240](https://capec.mitre.org/data/definitions/240.html)
- [CAPEC-75](https://capec.mitre.org/data/definitions/75.html)

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://samate.nist.gov/SSATTM_Content/papers/Seven%20Pernicious%20Kingdoms%20-%20Taxonomy%20of%20Sw%20Security%20Errors%20-%20Tsipenyuk%20-%20Chess%20-%20McGraw.pdf>.
- [REF-962] Object Management Group (OMG). "Automated Source Code Security Measure (ASCSM)". ASCSM-CWE-99. 2016-01. <http://www.omg.org/spec/ASCSM/1.0/>.

## Mapping Notes

- **Usage:** Allowed-with-Review
- **Rationale:** This CWE entry is a Class and might have Base-level children that would be more appropriate
- **Comments:** Examine children of this entry to see if there is a better fit
- **Reasons:** Abstraction

## Notes

- **Relationship**: Resource injection that involves resources stored on the filesystem goes by the name path manipulation (CWE-73).

- **Maintenance**: The relationship between CWE-99 and CWE-610 needs further investigation and clarification. They might be duplicates. CWE-99 "Resource Injection," as originally defined in Seven Pernicious Kingdoms taxonomy, emphasizes the "identifier used to access a system resource" such as a file name or port number, yet it explicitly states that the "resource injection" term does not apply to "path manipulation," which effectively identifies the path at which a resource can be found and could be considered to be one aspect of a resource identifier. Also, CWE-610 effectively covers any type of resource, whether that resource is at the system layer, the application layer, or the code layer.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | 7 Pernicious Kingdoms |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital |  | updated Time_of_Introduction |
| Modification | 2008-08-01 |  | KDM Analytics |  | added/updated white box definitions |
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Relationships, Other_Notes, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2009-05-27 | CWE Content Team | MITRE |  | updated Description, Name |
| Modification | 2009-07-17 | KDM Analytics |  |  | Improved the White_Box_Definition |
| Modification | 2009-07-27 | CWE Content Team | MITRE |  | updated White_Box_Definitions |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences, Other_Notes |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Common_Consequences, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2013-02-21 | CWE Content Team | MITRE |  | updated Alternate_Terms, Maintenance_Notes, Other_Notes, Relationships |
| Modification | 2013-07-17 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2014-06-23 | CWE Content Team | MITRE |  | updated Alternate_Terms, Description, Relationship_Notes, Relationships |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2015-12-07 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2017-01-19 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2017-05-03 | CWE Content Team | MITRE |  | updated Related_Attack_Patterns, Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Applicable_Platforms, Causal_Nature, Modes_of_Introduction, Relationships, White_Box_Definitions |
| Modification | 2019-01-03 | CWE Content Team | MITRE |  | updated References, Relationships, Taxonomy_Mappings |
| Modification | 2019-06-20 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated Other_Notes, Potential_Mitigations, References, Relationships, Type |
| Modification | 2020-08-20 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2020-12-10 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2021-10-28 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Detection_Factors, Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2023-10-26 | CWE Content Team | MITRE |  | updated Observed_Examples |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Relationships |

**Previous Entry Names:**

- Resource Injection — 2008-04-11
- Insufficient Control of Resource Identifiers (aka 'Resource Injection') — 2009-05-27

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
