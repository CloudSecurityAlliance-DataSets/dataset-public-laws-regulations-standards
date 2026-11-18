---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-14"
cwe_id: "CWE-14"
entry_type: weakness
name: "Compiler Removal of Code to Clear Buffers"
abstraction: Variant
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/14.html"
---

# CWE-14: Compiler Removal of Code to Clear Buffers

## Description

Sensitive memory is cleared according to the source code, but compiler optimizations leave the memory untouched when it is not read from again, aka "dead store removal."

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-733](../weaknesses/CWE-733.md) Compiler Optimization Removal or Modification of Security-critical Code (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Class | Prevalence | Note |
| --- | --- | --- | --- | --- |
| Language | C |  | Undetermined |  |
| Language | C++ |  | Undetermined |  |
| Language |  | Compiled | Undetermined |  |
| Architecture |  | Not Architecture-Specific | Undetermined | While the nature of the error may vary depending on the architecture being targeted by the compiler, this weakness is not specific to any particular architecture. |

## Modes Of Introduction

- **Implementation; Build and Compilation**:

  This compiler optimization error occurs when:

  - Secret data are stored in memory.
  - The secret data are scrubbed from memory by overwriting its contents.
  - The source code is compiled using an optimizing compiler, which identifies and removes the function that overwrites the contents as a dead store because the memory is not used subsequently.

- **Build and Compilation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Access Control | Read Memory<br>Bypass Protection Mechanism | This weakness will allow data that has not been cleared from memory to be read. If this data contains sensitive password information, then an attacker can read the password and use the information to bypass protection mechanisms. |

## Detection Methods

- **Method:** Black Box

  This specific weakness is impossible to detect using black box methods. While an analyst could examine memory to see that it has not been scrubbed, an analysis of the executable would not be successful. This is because the compiler has already removed the relevant code. Only the source code shows whether the programmer intended to clear the memory or not, so this weakness is indistinguishable from others.

  **Effectiveness:** Limited

- **Method:** White Box

  This weakness is only detectable using white box methods (see black box detection factor). Careful analysis is required to determine if the code is likely to be removed by the compiler.

## Potential Mitigations

- **Phase:** Implementation

  Store the sensitive data in a "volatile" memory location if available.

- **Phase:** Build and Compilation

  If possible, configure the compiler so that it does not remove dead stores.

- **Phase:** Architecture and Design

  Where possible, encrypt sensitive data that are used by a software system.

## Demonstrative Examples

### Example 1 (DX-200)

The following code reads a password from the user, uses the password to connect to a back-end mainframe, and then attempts to scrub the password from memory using memset().

*Example (Bad, C):*

```c
void GetData(char *MFAddr) {
    char pwd[64];
    if (GetPasswordFromUser(pwd, sizeof(pwd))) {
        if (ConnectToMainframe(MFAddr, pwd)) {
            // Interaction with mainframe
        }
    }
    memset(pwd, 0, sizeof(pwd));
}
```

The code in the example will behave correctly if it is executed verbatim, but if the code is compiled using an optimizing compiler, then the call to memset() might be removed as a dead store, because the buffer pwd is not used after its value is overwritten. Because the buffer pwd contains a sensitive value, the application may be vulnerable to attack if the data are left memory resident. If attackers are able to access the correct region of memory, they may use the recovered password to gain control of the system.

It is common practice to overwrite sensitive data manipulated in memory, such as passwords or cryptographic keys, in order to prevent attackers from learning system secrets. However, with the advent of optimizing compilers, programs do not always behave as their source code alone would suggest. In the example, the compiler interprets the call to memset() as dead code because the memory being written to is not subsequently used, despite the fact that there is clearly a security motivation for the operation to occur. The problem here is that many compilers, and in fact many programming languages, do not take this and other security concerns into consideration in their efforts to improve efficiency.

Attackers typically exploit this type of vulnerability by using a core dump or runtime mechanism to access the memory used by a particular application and recover the secret information. Once an attacker has access to the secret information, it is relatively straightforward to further exploit the system and possibly compromise other resources with which the application interacts.

## Affected Resources

- Memory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| 7 Pernicious Kingdoms |  | Insecure Compiler Optimization |  |
| PLOVER |  | Sensitive memory uncleared by compiler optimization |  |
| OWASP Top Ten 2004 | A8 | Insecure Storage | CWE More Specific |
| CERT C Secure Coding | MSC06-C | Be aware of compiler optimization when dealing with sensitive data |  |
| Software Fault Patterns | SFP23 | Exposed Data |  |

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://cwe.mitre.org/documents/sources/SevenPerniciousKingdoms.pdf>.
- [REF-7] Michael Howard and David LeBlanc. "Writing Secure Code". Chapter 9, "A Compiler Optimization Caveat" Page 322. 2nd Edition. Microsoft Press. 2002-12-04. <https://www.microsoftpressstore.com/store/writing-secure-code-9780735617223>.
- [REF-124] Michael Howard. "When scrubbing secrets in memory doesn't work". BugTraq. 2002-11-05. <https://seclists.org/bugtraq/2002/Nov/48> (URL validated: 2025-07-24).
- [REF-125] Michael Howard. "Some Bad News and Some Good News". Microsoft. 2002-10-21. <https://learn.microsoft.com/en-us/previous-versions/ms972826(v=msdn.10)> (URL validated: 2023-04-07).
- [REF-126] Joseph Wagner. "GNU GCC: Optimizer Removes Code Necessary for Security". Bugtraq. 2002-11-16. <https://seclists.org/bugtraq/2002/Nov/266> (URL validated: 2023-04-07).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
