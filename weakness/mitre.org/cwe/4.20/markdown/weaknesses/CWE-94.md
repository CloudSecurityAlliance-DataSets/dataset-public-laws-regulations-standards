---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-94"
cwe_id: "CWE-94"
entry_type: weakness
name: "Improper Control of Generation of Code ('Code Injection')"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed-with-Review
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/94.html"
---

# CWE-94: Improper Control of Generation of Code ('Code Injection')

## Description

The product constructs all or part of a code segment using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the syntax or behavior of the intended code segment.

![Diagram for CWE-94](https://cwe.mitre.org/data/images/CWE-94-Diagram.png)

## Alternate Terms

- **Code Injection**

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') (Class) | [CWE-1003](../views/CWE-1003.md) | Primary |
| ChildOf | [CWE-913](../weaknesses/CWE-913.md) Improper Control of Dynamically-Managed Code Resources (Class) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Primary**
- **Resultant**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Interpreted | Sometimes |
| Technology | AI/ML |  | Undetermined |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Likelihood Of Exploit

Medium

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Access Control | Bypass Protection Mechanism | In some cases, injectable code controls authentication; this may lead to a remote vulnerability. |
| Access Control | Gain Privileges or Assume Identity | Injected code can access resources that the attacker is directly prevented from accessing. |
| Integrity<br>Confidentiality<br>Availability | Execute Unauthorized Code or Commands | When a product allows a user's input to contain code syntax, it might be possible for an attacker to craft the code in such a way that it will alter the intended control flow of the product. As a result, code injection can often result in the execution of arbitrary code. Code injection attacks can also lead to loss of data integrity in nearly all cases, since the control-plane data injected is always incidental to data recall or writing. |
| Non-Repudiation | Hide Activities | Often the actions performed by injected control code are unlogged. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Architecture and Design · **Strategy:** Refactoring

  Refactor your program so that you do not have to dynamically generate code.

- **Phase:** Architecture and Design

  Run your code in a "jail" or similar sandbox environment that enforces strict boundaries between the process and the operating system. This may effectively restrict which code can be executed by your product.

  Examples include the Unix chroot jail and AppArmor. In general, managed code may provide some protection.

  This may not be a feasible solution, and it only limits the impact to the operating system; the rest of your application may still be subject to compromise.

  Be careful to avoid CWE-243 and other weaknesses related to jails.

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

  To reduce the likelihood of code injection, use stringent allowlists that limit which constructs are allowed. If you are dynamically constructing code that invokes a function, then verifying that the input is alphanumeric might be insufficient. An attacker might still be able to reference a dangerous function that you did not intend to allow, such as system(), exec(), or exit().

- **Phase:** Testing

  Use dynamic tools and techniques that interact with the product using large test suites with many diverse inputs, such as fuzz testing (fuzzing), robustness testing, and fault injection. The product's operation may slow down, but it should not become unstable, crash, or generate incorrect results.

- **Phase:** Operation · **Strategy:** Compilation or Build Hardening · **ID:** MIT-32

  Run the code in an environment that performs automatic taint propagation and prevents any command execution that uses tainted variables, such as Perl's "-T" switch. This will force the program to perform validation steps that remove the taint, although you must be careful to correctly validate your inputs so that you do not accidentally mark dangerous inputs as untainted (see CWE-183 and CWE-184).

- **Phase:** Operation · **Strategy:** Environment Hardening · **ID:** MIT-32

  Run the code in an environment that performs automatic taint propagation and prevents any command execution that uses tainted variables, such as Perl's "-T" switch. This will force the program to perform validation steps that remove the taint, although you must be careful to correctly validate your inputs so that you do not accidentally mark dangerous inputs as untainted (see CWE-183 and CWE-184).

- **Phase:** Implementation

  For Python programs, it is frequently encouraged to use the ast.literal_eval() function instead of eval, since it is intentionally designed to avoid executing code. However, an adversary could still cause excessive memory or stack consumption via deeply nested structures [REF-1372], so the python documentation discourages use of ast.literal_eval() on untrusted data [REF-1373].

  **Effectiveness:** Discouraged Common Practice

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

### Example 2 (DX-31)

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

### Example 3 (DX-156)

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

### Example 4 (DX-236)

The following code is a workflow job written using YAML. The code attempts to download pull request artifacts, unzip from the artifact called pr.zip and extract the value of the file NR into a variable "pr_number" that will be used later in another job. It attempts to create a github workflow environment variable, writing to $GITHUB_ENV. The environment variable value is retrieved from an external resource.

*Example (Bad, Other):*

```other
name: Deploy Preview
jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - name: 'Download artifact'
            uses: actions/github-script
            with:
                script: |
                    var artifacts = await github.actions.listWorkflowRunArtifacts({
                        owner: context.repo.owner,
                        repo: context.repo.repo,
                        run_id: ${{ github.event.workflow_run.id }},
                    });
                    var matchPrArtifact = artifacts.data.artifacts.filter((artifact) => {
                        return artifact.name == "pr"
                    })[0];
                    var downloadPr = await github.actions.downloadArtifact({
                        owner: context.repo.owner,
                        repo: context.repo.repo,
                        artifact_id: matchPrArtifact.id,
                        archive_format: 'zip',
                    });
                    var fs = require('fs');
                    fs.writeFileSync('${{github.workspace}}/pr.zip', Buffer.from(downloadPr.data));
            - run: |
                unzip pr.zip
                echo "pr_number=$(cat NR)" >> $GITHUB_ENV
```

The code does not neutralize the value of the file NR, e.g. by validating that NR only contains a number (CWE-1284). The NR file is attacker controlled because it originates from a pull request that produced pr.zip.

The attacker could escape the existing pr_number and create a new variable using a "\n" (CWE-93) followed by any environment variable to be added such as:

*Example (Attack):*

```
\nNODE_OPTIONS="--experimental-modules --experiments-loader=data:text/javascript,console.log('injected code');//"
```

This would result in injecting and running javascript code (CWE-94) on the workflow runner with elevated privileges.

*Example (Good, Other):*

```other
The code could be modified to validate that the NR
file only contains a numeric value, or the code could
retrieve the PR number from a more trusted source.
```

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2023-29374](https://www.cve.org/CVERecord?id=CVE-2023-29374) | Math component in an LLM framework translates user input into a Python expression that is input into the Python exec() method, allowing code execution - one variant of a "prompt injection" attack. |
| [CVE-2024-5565](https://www.cve.org/CVERecord?id=CVE-2024-5565) | Python-based library uses an LLM prompt containing user input to dynamically generate code that is then fed as input into the Python exec() method, allowing code execution - one variant of a "prompt injection" attack. |
| [CVE-2024-4181](https://www.cve.org/CVERecord?id=CVE-2024-4181) | Framework for LLM applications allows eval injection via a crafted response from a hosting provider. |
| [CVE-2022-2054](https://www.cve.org/CVERecord?id=CVE-2022-2054) | Python compiler uses eval() to execute malicious strings as Python code. |
| [CVE-2021-22204](https://www.cve.org/CVERecord?id=CVE-2021-22204) | Chain: regex in EXIF processor code does not correctly determine where a string ends (CWE-625), enabling eval injection (CWE-95), as exploited in the wild per CISA KEV. |
| [CVE-2020-8218](https://www.cve.org/CVERecord?id=CVE-2020-8218) | "Code injection" in VPN product, as exploited in the wild per CISA KEV. |
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
| [CVE-2002-0495](https://www.cve.org/CVERecord?id=CVE-2002-0495) | Perl code directly injected into CGI library file from parameters to another CGI program. |
| [CVE-2005-1876](https://www.cve.org/CVERecord?id=CVE-2005-1876) | Direct PHP code injection into supporting template file. |
| [CVE-2005-1894](https://www.cve.org/CVERecord?id=CVE-2005-1894) | Direct code injection into PHP script that can be accessed by attacker. |
| [CVE-2003-0395](https://www.cve.org/CVERecord?id=CVE-2003-0395) | PHP code from User-Agent HTTP header directly inserted into log file implemented as PHP script. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER | CODE | Code Evaluation and Injection |
| ISA/IEC 62443 | Part 4-2 | Req CR 3.5 |
| ISA/IEC 62443 | Part 3-3 | Req SR 3.5 |
| ISA/IEC 62443 | Part 4-1 | Req SVV-1 |
| ISA/IEC 62443 | Part 4-1 | Req SVV-3 |

## Related Attack Patterns

- [CAPEC-242](https://capec.mitre.org/data/definitions/242.html)
- [CAPEC-35](https://capec.mitre.org/data/definitions/35.html)
- [CAPEC-77](https://capec.mitre.org/data/definitions/77.html)

## References

- [REF-44] Michael Howard, David LeBlanc and John Viega. "24 Deadly Sins of Software Security". "Sin 3: Web-Client Related Vulnerabilities (XSS)." Page 63. McGraw-Hill. 2010.
- [REF-1372] "How ast.literal_eval can cause memory exhaustion". Reddit. 2022-12-14. <https://www.reddit.com/r/learnpython/comments/zmbhcf/how_astliteral_eval_can_cause_memory_exhaustion/> (URL validated: 2023-11-03).
- [REF-1373] "ast - Abstract Syntax Trees". ast.literal_eval(node_or_string). Python. 2023-11-02. <https://docs.python.org/3/library/ast.html#ast.literal_eval> (URL validated: 2023-11-03).

## Mapping Notes

- **Usage:** Allowed-with-Review
- **Rationale:** This entry is frequently misused for vulnerabilities with a technical impact of "code execution," which does not by itself indicate a root cause weakness, since dozens of weaknesses can enable code execution.
- **Comments:** This weakness only applies when the product's functionality intentionally constructs all or part of a code segment. It could be that executing code could be the result of other weaknesses that do not involve the construction of code segments.
- **Reasons:** Frequent Misuse, Frequent Misinterpretation

## Notes

- **Theoretical**: Injection problems encompass a wide variety of issues -- all mitigated in very different ways. For this reason, the most effective way to discuss these weaknesses is to note the distinct features that classify them as injection weaknesses. The most important issue to note is that all injection problems share one thing in common -- i.e., they allow for the injection of control plane data into the user-controlled data plane. This means that the execution of the process may be altered by sending code in through legitimate data channels, using no other mechanism. While buffer overflows, and many other flaws, involve the use of some further issue to gain execution, injection problems need only for the data to be parsed. The most classic instantiations of this category of weakness are SQL injection and format string vulnerabilities.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Contribution (Content) | 2023-06-29 | "Mapping CWE to 62443" Sub-Working Group | CWE-CAPEC ICS/OT SIG | CWE 4.12, 2023-06-29 | Suggested mappings to ISA/IEC 62443. |
| Contribution (Content) | 2024-02-29 | Abhi Balakrishnan |  | CWE 4.17, 2025-04-03 | Contributed usability diagram concepts used by the CWE team. |
| Contribution (Feedback) | 2025-08-22 | Matthew A. Pagan | Spectrum | CWE 4.19, 2025-12-11 | Discovered a syntax issue in the Python3 demox (DX-156) and suggested a fix |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Applicable_Platforms, Relationships, Research_Gaps, Taxonomy_Mappings |
| Modification | 2009-01-12 | CWE Content Team | MITRE | CWE 1.2, 2009-01-12 | updated Common_Consequences, Demonstrative_Examples, Description, Likelihood_of_Exploit, Name, Potential_Mitigations, Relationships |
| Modification | 2009-03-10 | CWE Content Team | MITRE | CWE 1.3, 2009-03-10 | updated Potential_Mitigations |
| Modification | 2009-05-27 | CWE Content Team | MITRE | CWE 1.4, 2009-05-27 | updated Demonstrative_Examples, Name |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 | updated Potential_Mitigations |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Description, Potential_Mitigations |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Name |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Common_Consequences, Demonstrative_Examples, Observed_Examples, References, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2013-02-21 | CWE Content Team | MITRE | CWE 2.4, 2013-02-21 | updated Relationships |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships |
| Modification | 2015-12-07 | CWE Content Team | MITRE | CWE 2.9, 2015-12-07 | updated Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Demonstrative_Examples, Modes_of_Introduction, Relationships |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Related_Attack_Patterns, Type |
| Modification | 2019-09-19 | CWE Content Team | MITRE | CWE 3.4, 2019-09-19 | updated Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Potential_Mitigations, Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Potential_Mitigations |
| Modification | 2020-08-20 | CWE Content Team | MITRE | CWE 4.2, 2020-08-20 | updated Relationships |
| Modification | 2021-03-15 | CWE Content Team | MITRE | CWE 4.4, 2021-03-15 | updated Demonstrative_Examples |
| Modification | 2021-07-20 | CWE Content Team | MITRE | CWE 4.5, 2021-07-20 | updated Relationships |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 | updated Relationships |
| Modification | 2022-04-28 | CWE Content Team | MITRE | CWE 4.7, 2022-04-28 | updated Research_Gaps |
| Modification | 2022-06-28 | CWE Content Team | MITRE | CWE 4.8, 2022-06-28 | updated Observed_Examples, Relationships |
| Modification | 2022-10-13 | CWE Content Team | MITRE | CWE 4.9, 2022-10-13 | updated Observed_Examples |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Demonstrative_Examples, Description, Potential_Mitigations, Relationships |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Demonstrative_Examples, Detection_Factors, Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes, Relationships, Taxonomy_Mappings |
| Modification | 2024-02-29 | CWE Content Team | MITRE | CWE 4.14, 2024-02-29 | updated Demonstrative_Examples, Potential_Mitigations, References |
| Modification | 2024-07-16 | CWE Content Team | MITRE | CWE 4.15, 2024-07-16 | updated Applicable_Platforms, Observed_Examples |
| Modification | 2024-11-19 | CWE Content Team | MITRE | CWE 4.16, 2024-11-19 | updated Mapping_Notes, Relationships |
| Modification | 2025-04-03 | CWE Content Team | MITRE | CWE 4.17, 2025-04-03 | updated Alternate_Terms, Common_Consequences, Description, Diagram, Theoretical_Notes |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Demonstrative_Examples, Relationships, Weakness_Ordinalities |
| Modification | 2026-04-30 | CWE Content Team | MITRE | CWE 4.20, 2026-04-30 | updated Potential_Mitigations, Relationships |

**Previous Entry Names:**

- Code Injection — 2009-01-12
- Failure to Control Generation of Code (aka 'Code Injection') — 2009-05-27
- Failure to Control Generation of Code ('Code Injection') — 2011-03-29

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
