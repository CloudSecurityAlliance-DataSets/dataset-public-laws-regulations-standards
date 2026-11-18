---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-7"
cwe_id: "CWE-7"
entry_type: weakness
name: "J2EE Misconfiguration: Missing Custom Error Page"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/7.html"
---

# CWE-7: J2EE Misconfiguration: Missing Custom Error Page

## Description

The product has a J2EE component that does not have a custom error page.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-756](../weaknesses/CWE-756.md) Missing Custom Error Page (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language | Java |  | Undetermined |
| Technology |  | Web Based | Undetermined |
| Technology | Web Server |  | Undetermined |

## Modes Of Introduction

- **Implementation; System Configuration; Operation**: Without a custom error page, J2EE may serve a default error page that includes potentially sensitive information.

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality | Read Application Data | When an attacker explores a web site looking for vulnerabilities, the amount of information that the site provides is crucial to the eventual success or failure of any attempted attacks. A stack trace might show the attacker a malformed SQL query string, the type of database being used, and the version of the application container. This information enables the attacker to target known vulnerabilities in these components. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

## Potential Mitigations

- **Phase:** Implementation

  Handle exceptions appropriately in source code. Catch java.lang.Throwable exceptions to prevent attackers from mining information from the application container's built-in error response.

- **Phase:** Implementation; System Configuration

  Always define appropriate error pages, including for 4xx errors (e.g. 404) and 5xx (e.g. 500) errors. The application configuration should specify a default error page in order to guarantee that the application will never leak error messages to an attacker. Handling standard HTTP error codes is useful and user-friendly in addition to being a good security practice, and a good configuration will also define a last-chance error handler that catches any exception that could possibly be thrown by the application.

- **Phase:** Implementation

  Do not attempt to process an error or attempt to mask it.

- **Phase:** Implementation

  Verify return values are correct and do not supply sensitive information about the system.

## Demonstrative Examples

### Example 1 (DX-76)

In the snippet below, an unchecked runtime exception thrown from within the try block may cause the container to display its default error page (which may contain a full stack trace, among other things).

*Example (Bad, Java):*

```java
Public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    try {
        ...
    } catch (ApplicationSpecificException ase) {
        logger.error("Caught: " + ase.toString());
    }
}
```

## Taxonomy Mappings

| Taxonomy | Entry Name |
| --- | --- |
| 7 Pernicious Kingdoms | J2EE Misconfiguration: Missing Error Handling |

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://cwe.mitre.org/documents/sources/SevenPerniciousKingdoms.pdf>.
- [REF-65] M. Howard, D. LeBlanc and J. Viega. "19 Deadly Sins of Software Security". McGraw-Hill/Osborne. 2005-07-26.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
