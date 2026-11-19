---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-96"
cwe_id: "CWE-96"
entry_type: weakness
name: "Improper Neutralization of Directives in Statically Saved Code"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/96.html"
---

# CWE-96: Improper Neutralization of Directives in Statically Saved Code

## Description

The product receives input from an upstream component, but it does not neutralize or incorrectly neutralizes code syntax before inserting the input into an executable resource, such as a library, configuration file, or template.

## Alternate Terms

- **Static Code Injection** (Common-Name, Attack-Focused)

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-94](../weaknesses/CWE-94.md) Improper Control of Generation of Code (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language | PHP |  | Undetermined |
| Language | Perl |  | Undetermined |
| Language |  | Interpreted | Undetermined |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.
- **Implementation**: This issue is frequently found in PHP applications that allow users to set configuration variables that are stored within executable PHP files. Technically, this could also be performed in some compiled code (e.g., by byte-patching an executable), although it is highly unlikely.

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality | Read Files or Directories<br>Read Application Data | The injected code could access restricted data / files. |
| Access Control | Bypass Protection Mechanism | In some cases, injectable code controls authentication; this may lead to a remote vulnerability. |
| Access Control | Gain Privileges or Assume Identity | Injected code can access resources that the attacker is directly prevented from accessing. |
| Integrity<br>Confidentiality<br>Availability<br>Other | Execute Unauthorized Code or Commands | Code injection attacks can lead to loss of data integrity in nearly all cases as the control-plane data injected is always incidental to data recall or writing. Additionally, code injection can often result in the execution of arbitrary code. |
| Non-Repudiation | Hide Activities | Often the actions performed by injected control code are unlogged. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

## Potential Mitigations

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

- **Phase:** Implementation · **Strategy:** Output Encoding

  Perform proper output validation and escaping to neutralize all code syntax from data written to code files.

## Demonstrative Examples

### Example 1 (DX-32)

This example attempts to write user messages to a message file and allow users to view them.

*Example (Bad, PHP):*

```php
$MessageFile = "messages.out";
if ($_GET["action"] == "NewMessage") {
    $name = $_GET["name"];
    $message = $_GET["message"];
    $handle = fopen($MessageFile, "a+");
    fwrite($handle, "<b>$name</b> says '$message'<hr>\n");
    fclose($handle);
    echo "Message Saved!<p>\n";
}
else if ($_GET["action"] == "ViewMessages") {
    include($MessageFile);
}
```

While the programmer intends for the MessageFile to only include data, an attacker can provide a message such as:

*Example (Attack):*

```
name=h4x0r
message=%3C?php%20system(%22/bin/ls%20-l%22);?%3E
```

which will decode to the following:

*Example (Attack):*

```
<?php system("/bin/ls -l");?>
```

The programmer thought they were just including the contents of a regular data file, but PHP parsed it and executed the code. Now, this code is executed any time people view messages.

Notice that XSS (CWE-79) is also possible in this situation.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2002-0495](https://www.cve.org/CVERecord?id=CVE-2002-0495) | Perl code directly injected into CGI library file from parameters to another CGI program. |
| [CVE-2005-1876](https://www.cve.org/CVERecord?id=CVE-2005-1876) | Direct PHP code injection into supporting template file. |
| [CVE-2005-1894](https://www.cve.org/CVERecord?id=CVE-2005-1894) | Direct code injection into PHP script that can be accessed by attacker. |
| [CVE-2003-0395](https://www.cve.org/CVERecord?id=CVE-2003-0395) | PHP code from User-Agent HTTP header directly inserted into log file implemented as PHP script. |
| [CVE-2007-6652](https://www.cve.org/CVERecord?id=CVE-2007-6652) | Chain: execution after redirect allows non-administrator to perform static code injection. |

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | Direct Static Code Injection |
| Software Fault Patterns | SFP24 | Tainted Input to Command |

## Related Attack Patterns

- [CAPEC-35](https://capec.mitre.org/data/definitions/35.html)
- [CAPEC-73](https://capec.mitre.org/data/definitions/73.html)
- [CAPEC-77](https://capec.mitre.org/data/definitions/77.html)
- [CAPEC-81](https://capec.mitre.org/data/definitions/81.html)
- [CAPEC-85](https://capec.mitre.org/data/definitions/85.html)

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Relationship**: "HTML injection" (see CWE-79: XSS) could be thought of as an example of this, but the code is injected and executed on the client side, not the server side. Server-Side Includes (SSI) are an example of direct static code injection.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Potential_Mitigations, Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Applicable_Platforms, Relationships, Other_Notes, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2009-05-27 | CWE Content Team | MITRE | CWE 1.4, 2009-05-27 | updated Description, Name |
| Modification | 2010-04-05 | CWE Content Team | MITRE | CWE 1.8.1, 2010-04-05 | updated Description, Name |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Potential_Mitigations |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Common_Consequences, Demonstrative_Examples, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2013-02-21 | CWE Content Team | MITRE | CWE 2.4, 2013-02-21 | updated Observed_Examples |
| Modification | 2014-06-23 | CWE Content Team | MITRE | CWE 2.7, 2014-06-23 | updated Enabling_Factors_for_Exploitation, Other_Notes, Relationship_Notes |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-05-03 | CWE Content Team | MITRE | CWE 2.11, 2017-05-05 | updated Related_Attack_Patterns |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Affected_Resources, Applicable_Platforms, Causal_Nature, Demonstrative_Examples, Enabling_Factors_for_Exploitation, Modes_of_Introduction, Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Potential_Mitigations, Relationships, Taxonomy_Mappings |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Potential_Mitigations |
| Modification | 2021-03-15 | CWE Content Team | MITRE | CWE 4.4, 2021-03-15 | updated Demonstrative_Examples |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 | updated Relationships |
| Modification | 2022-10-13 | CWE Content Team | MITRE | CWE 4.9, 2022-10-13 | updated Relationships, Taxonomy_Mappings |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Modes_of_Introduction, Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Detection_Factors, Relationships |
| Modification | 2026-10-28 | CWE Content Team | MITRE | CWE 5.0, 2026-10-28 | updated Alternate_Terms, Name |

**Previous Entry Names:**

- Direct Static Code Injection — 2008-04-11
- Insufficient Control of Directives in Statically Saved Code (Static Code Injection) — 2009-05-27
- Improper Sanitization of Directives in Statically Saved Code ('Static Code Injection') — 2010-04-05
- Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection') — 2026-10-28

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
