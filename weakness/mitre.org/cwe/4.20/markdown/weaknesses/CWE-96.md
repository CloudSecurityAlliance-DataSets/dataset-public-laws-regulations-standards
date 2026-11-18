---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-96"
cwe_id: "CWE-96"
entry_type: weakness
name: "Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection')"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/96.html"
---

# CWE-96: Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection')

## Description

The product receives input from an upstream component, but it does not neutralize or incorrectly neutralizes code syntax before inserting the input into an executable resource, such as a library, configuration file, or template.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-94](../weaknesses/CWE-94.md) Improper Control of Generation of Code ('Code Injection') (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

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
| [CVE-2007-6652](https://www.cve.org/CVERecord?id=CVE-2007-6652) | chain: execution after redirect allows non-administrator to perform static code injection. |

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

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
