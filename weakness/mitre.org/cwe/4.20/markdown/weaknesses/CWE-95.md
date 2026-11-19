---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-95"
cwe_id: "CWE-95"
entry_type: weakness
name: "Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/95.html"
---

# CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')

## Description

The product receives input from an upstream component, but it does not neutralize or incorrectly neutralizes code syntax before using the input in a dynamic evaluation call (e.g. "eval").

![Diagram for CWE-95](https://cwe.mitre.org/data/images/CWE-95-Diagram.png)

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-94](../weaknesses/CWE-94.md) Improper Control of Generation of Code ('Code Injection') (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language | Java |  | Undetermined |
| Language | JavaScript |  | Undetermined |
| Language | Python |  | Undetermined |
| Language | Perl |  | Undetermined |
| Language | PHP |  | Undetermined |
| Language | Ruby |  | Undetermined |
| Language |  | Interpreted | Undetermined |
| Technology | AI/ML |  | Often |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.
- **Implementation**: This weakness is prevalent in handler/dispatch procedures that might want to invoke a large number of functions, or set a large number of variables.

## Likelihood Of Exploit

Medium

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality | Read Files or Directories<br>Read Application Data | The injected code could access restricted data / files. |
| Access Control | Bypass Protection Mechanism | In some cases, injectable code controls authentication; this may lead to a remote vulnerability. |
| Access Control | Gain Privileges or Assume Identity | Injected code can access resources that the attacker is directly prevented from accessing. |
| Integrity<br>Confidentiality<br>Availability<br>Other | Execute Unauthorized Code or Commands | Code injection attacks can lead to loss of data integrity in nearly all cases as the control-plane data injected is always incidental to data recall or writing. Additionally, code injection can often result in the execution of arbitrary code or at least modify what code can be executed. |
| Non-Repudiation | Hide Activities | Often the actions performed by injected control code are unlogged. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Architecture and Design; Implementation · **Strategy:** Refactoring

  If possible, refactor your code so that it does not need to use eval() at all.

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

- **Phase:** Implementation

  Inputs should be decoded and canonicalized to the application's current internal representation before being validated (CWE-180, CWE-181). Make sure that your application does not inadvertently decode the same input twice (CWE-174). Such errors could be used to bypass allowlist schemes by introducing dangerous inputs after they have been checked. Use libraries such as the OWASP ESAPI Canonicalization control.

  Consider performing repeated canonicalization until your input does not change any more. This will avoid double-decoding and similar scenarios, but it might inadvertently modify inputs that are allowed to contain properly-encoded dangerous content.

- **Phase:** Implementation

  For Python programs, it is frequently encouraged to use the ast.literal_eval() function instead of eval, since it is intentionally designed to avoid executing code. However, an adversary could still cause excessive memory or stack consumption via deeply nested structures [REF-1372], so the python documentation discourages use of ast.literal_eval() on untrusted data [REF-1373].

  **Effectiveness:** Discouraged Common Practice

## Demonstrative Examples

### Example 1 (DX-31)

edit-config.pl: This CGI script is used to modify settings in a configuration file.

*Example (Bad, Perl):*

```perl
use CGI qw(:standard);

sub config_file_add_key {
    my ($fname, $key, $arg) = @_;
    # code to add a field/key to a file goes here
}

sub config_file_set_key {
    my ($fname, $key, $arg) = @_;
    # code to set key to a particular file goes here
}

sub config_file_delete_key {
    my ($fname, $key, $arg) = @_;
    # code to delete key from a particular file goes here
}

sub handleConfigAction {
    my ($fname, $action) = @_;
    my $key = param('key');
    my $val = param('val');
    # this is super-efficient code, especially if you have to invoke
    # any one of dozens of different functions!

    my $code = "config_file_$action_key(\$fname, \$key, \$val);";
    eval($code);
}

$configfile = "/home/cwe/config.txt";
print header;
if (defined(param('action'))) {
    handleConfigAction($configfile, param('action'));
}
else {
    print "No action specified!\n";
}
```

The script intends to take the 'action' parameter and invoke one of a variety of functions based on the value of that parameter - config_file_add_key(), config_file_set_key(), or config_file_delete_key(). It could set up a conditional to invoke each function separately, but eval() is a powerful way of doing the same thing in fewer lines of code, especially when a large number of functions or variables are involved. Unfortunately, in this case, the attacker can provide other values in the action parameter, such as:

*Example (Attack):*

```
add_key(",","); system("/bin/ls");
```

This would produce the following string in handleConfigAction():

*Example (Result):*

```
config_file_add_key(",","); system("/bin/ls");
```

Any arbitrary Perl code could be added after the attacker has "closed off" the construction of the original function call, in order to prevent parsing errors from causing the malicious eval() to fail before the attacker's payload is activated. This particular manipulation would fail after the system() call, because the "\_key(\\$fname, \\$key, \\$val)" portion of the string would cause an error, but this is irrelevant to the attack because the payload has already been activated.

### Example 2 (DX-156)

This simple python3 script asks a user to supply a comma-separated list of numbers as input and adds them together.

*Example (Bad, Python):*

```python
def main():
    sum = 0
    try:
        numbers = eval(input("Enter a comma-separated list of numbers: "))
    except SyntaxError:
        print("Error: invalid input")
        return
    for num in numbers:
        sum = sum + num
    print(f"Sum of {numbers} = {sum}")
main()
```

The eval() function can take the user-supplied list and convert it into a Python list object, therefore allowing the programmer to use list comprehension methods to work with the data. However, if code is supplied to the eval() function, it will execute that code. For example, a malicious user could supply the following string:

*Example (Attack):*

```
__import__('subprocess').getoutput('rm -r *')
```

This would delete all the files in the current directory. For this reason, it is not recommended to use eval() with untrusted input.

A way to accomplish this without the use of eval() is to apply an integer conversion on the input within a try/except block. If the user-supplied input is not numeric, this will raise a ValueError. By avoiding eval(), there is no opportunity for the input string to be executed as code.

*Example (Good, Python):*

```python
def main():
    sum = 0
    numbers = input("Enter a comma-separated list of numbers: ").split(",")
    try:
        for num in numbers:
            sum = sum + int(num)
        print(f"Sum of {numbers} = {sum}")
    except ValueError:
        print("Error: invalid input")
main()
```

An alternative, commonly-cited mitigation for this kind of weakness is to use the ast.literal_eval() function, since it is intentionally designed to avoid executing code. However, an adversary could still cause excessive memory or stack consumption via deeply nested structures [REF-1372], so the python documentation discourages use of ast.literal_eval() on untrusted data [REF-1373].

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2024-4181](https://www.cve.org/CVERecord?id=CVE-2024-4181) | Framework for LLM applications allows eval injection via a crafted response from a hosting provider. |
| [CVE-2022-2054](https://www.cve.org/CVERecord?id=CVE-2022-2054) | Python compiler uses eval() to execute malicious strings as Python code. |
| [CVE-2021-22204](https://www.cve.org/CVERecord?id=CVE-2021-22204) | Chain: regex in EXIF processor code does not correctly determine where a string ends (CWE-625), enabling eval injection (CWE-95), as exploited in the wild per CISA KEV. |
| [CVE-2021-22205](https://www.cve.org/CVERecord?id=CVE-2021-22205) | Chain: backslash followed by a newline can bypass a validation step (CWE-20), leading to eval injection (CWE-95), as exploited in the wild per CISA KEV. |
| [CVE-2008-5071](https://www.cve.org/CVERecord?id=CVE-2008-5071) | Eval injection in PHP program. |
| [CVE-2002-1750](https://www.cve.org/CVERecord?id=CVE-2002-1750) | Eval injection in Perl program. |
| [CVE-2008-5305](https://www.cve.org/CVERecord?id=CVE-2008-5305) | Eval injection in Perl program using an ID that should only contain hyphens and numbers. |
| [CVE-2002-1752](https://www.cve.org/CVERecord?id=CVE-2002-1752) | Direct code injection into Perl eval function. |
| [CVE-2002-1753](https://www.cve.org/CVERecord?id=CVE-2002-1753) | Eval injection in Perl program. |
| [CVE-2005-1527](https://www.cve.org/CVERecord?id=CVE-2005-1527) | Direct code injection into Perl eval function. |
| [CVE-2005-2837](https://www.cve.org/CVERecord?id=CVE-2005-2837) | Direct code injection into Perl eval function. |
| [CVE-2005-1921](https://www.cve.org/CVERecord?id=CVE-2005-1921) | MFV. code injection into PHP eval statement using nested constructs that should not be nested. |
| [CVE-2005-2498](https://www.cve.org/CVERecord?id=CVE-2005-2498) | MFV. code injection into PHP eval statement using nested constructs that should not be nested. |
| [CVE-2005-3302](https://www.cve.org/CVERecord?id=CVE-2005-3302) | Code injection into Python eval statement from a field in a formatted file. |
| [CVE-2007-1253](https://www.cve.org/CVERecord?id=CVE-2007-1253) | Eval injection in Python program. |
| [CVE-2001-1471](https://www.cve.org/CVERecord?id=CVE-2001-1471) | chain: Resultant eval injection. An invalid value prevents initialization of variables, which can be modified by attacker and later injected into PHP eval statement. |
| [CVE-2007-2713](https://www.cve.org/CVERecord?id=CVE-2007-2713) | Chain: Execution after redirect triggers eval injection. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| PLOVER |  | Direct Dynamic Code Evaluation ('Eval Injection') |  |
| OWASP Top Ten 2007 | A3 | Malicious File Execution | CWE More Specific |
| OWASP Top Ten 2004 | A6 | Injection Flaws | CWE More Specific |
| Software Fault Patterns | SFP24 | Tainted input to command |  |
| SEI CERT Perl Coding Standard | IDS35-PL | Do not invoke the eval form with a string argument | Exact |

## Related Attack Patterns

- [CAPEC-35](https://capec.mitre.org/data/definitions/35.html)

## References

- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 18, "Inline Evaluation", Page 1095. 1st Edition. Addison Wesley. 2006.
- [REF-1372] "How ast.literal_eval can cause memory exhaustion". Reddit. 2022-12-14. <https://www.reddit.com/r/learnpython/comments/zmbhcf/how_astliteral_eval_can_cause_memory_exhaustion/> (URL validated: 2023-11-03).
- [REF-1373] "ast - Abstract Syntax Trees". ast.literal_eval(node_or_string). Python. 2023-11-02. <https://docs.python.org/3/library/ast.html#ast.literal_eval> (URL validated: 2023-11-03).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Other**: Factors: special character errors can play a role in increasing the variety of code that can be injected, although some vulnerabilities do not require special characters at all, e.g. when a single function without arguments can be referenced and a terminator character is not necessary.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-08-15 |  | Veracode | CWE 1.0, 2008-09-09 | Suggested OWASP Top Ten 2004 mapping |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Applicable_Platforms, Description, Modes_of_Introduction, Relationships, Other_Notes, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2009-01-12 | CWE Content Team | MITRE | CWE 1.2, 2009-01-12 | updated Description, Observed_Examples, Other_Notes, Research_Gaps |
| Modification | 2009-05-27 | CWE Content Team | MITRE | CWE 1.4, 2009-05-27 | updated Alternate_Terms, Applicable_Platforms, Demonstrative_Examples, Description, Name, References |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 | updated Potential_Mitigations |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Description, Name |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Common_Consequences, Demonstrative_Examples, References, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2013-02-21 | CWE Content Team | MITRE | CWE 2.4, 2013-02-21 | updated Observed_Examples |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Causal_Nature, Modes_of_Introduction, References, Relationships, Taxonomy_Mappings |
| Modification | 2019-01-03 | CWE Content Team | MITRE | CWE 3.2, 2019-01-03 | updated Taxonomy_Mappings |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Type |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Potential_Mitigations, Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Potential_Mitigations |
| Modification | 2021-03-15 | CWE Content Team | MITRE | CWE 4.4, 2021-03-15 | updated Relationships |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 | updated Relationships |
| Modification | 2022-04-28 | CWE Content Team | MITRE | CWE 4.7, 2022-04-28 | updated Research_Gaps |
| Modification | 2022-06-28 | CWE Content Team | MITRE | CWE 4.8, 2022-06-28 | updated Observed_Examples |
| Modification | 2022-10-13 | CWE Content Team | MITRE | CWE 4.9, 2022-10-13 | updated Observed_Examples |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Demonstrative_Examples, Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Demonstrative_Examples, Detection_Factors, Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2024-02-29 | CWE Content Team | MITRE | CWE 4.14, 2024-02-29 | updated Demonstrative_Examples, Potential_Mitigations, References |
| Modification | 2024-07-16 | CWE Content Team | MITRE | CWE 4.15, 2024-07-16 | updated Applicable_Platforms, Observed_Examples |
| Modification | 2025-04-03 | CWE Content Team | MITRE | CWE 4.17, 2025-04-03 | updated Common_Consequences, Description, Diagram |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Demonstrative_Examples, Relationships |
| Modification | 2026-04-30 | CWE Content Team | MITRE | CWE 4.20, 2026-04-30 | updated Applicable_Platforms, Potential_Mitigations, Relationships |

**Previous Entry Names:**

- Direct Dynamic Code Evaluation ('Eval Injection') — 2008-04-11
- Insufficient Control of Directives in Dynamically Evaluated Code (aka 'Eval Injection') — 2009-05-27
- Improper Sanitization of Directives in Dynamically Evaluated Code ('Eval Injection') — 2010-06-21

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
