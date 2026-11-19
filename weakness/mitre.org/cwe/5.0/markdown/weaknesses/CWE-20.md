---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-20"
cwe_id: "CWE-20"
entry_type: weakness
name: "Improper Input Validation"
abstraction: Class
structure: Simple
status: Stable
mapping_usage: Discouraged
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/20.html"
---

# CWE-20: Improper Input Validation

## Description

The product receives input or data, but it does not validate or incorrectly validates that the input has the properties that are required to process the data safely and correctly.

![Diagram for CWE-20](https://cwe.mitre.org/data/images/CWE-20-Diagram.png)

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-707](../weaknesses/CWE-707.md) Improper Neutralization (Pillar) | [CWE-1000](../views/CWE-1000.md) | Primary |
| PeerOf | [CWE-345](../weaknesses/CWE-345.md) Insufficient Verification of Data Authenticity (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| CanPrecede | [CWE-22](../weaknesses/CWE-22.md) Improper Limitation of a Pathname to a Restricted Directory (Base) | [CWE-1000](../views/CWE-1000.md) |  |
| CanPrecede | [CWE-41](../weaknesses/CWE-41.md) Improper Resolution of Path Equivalence (Base) | [CWE-1000](../views/CWE-1000.md) |  |
| CanPrecede | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component (Class) | [CWE-1000](../views/CWE-1000.md) |  |
| CanPrecede | [CWE-119](../weaknesses/CWE-119.md) Improper Restriction of Operations within the Bounds of a Memory Buffer (Class) | [CWE-1000](../views/CWE-1000.md) |  |
| CanPrecede | [CWE-770](../weaknesses/CWE-770.md) Allocation of Resources Without Limits or Throttling (Base) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Not Language-Specific | Often |
| Language | Go |  | Undetermined |
| Technology | AI/ML |  | Often |

## Modes Of Introduction

- **Architecture and Design**

- **Implementation**:

  REALIZATION: This weakness is caused during implementation of an architectural security tactic.

  If a programmer believes that an attacker cannot modify certain inputs, then the programmer might not perform any input validation at all. For example, in web applications, many programmers believe that cookies and hidden form fields can not be modified from a web browser (CWE-472), although they can be altered using a proxy or a custom program. In a client-server architecture, the programmer might assume that client-side security checks cannot be bypassed, even when a custom client could be written that skips those checks (CWE-602).

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Availability | DoS: Crash, Exit, or Restart<br>DoS: Resource Consumption (CPU)<br>DoS: Resource Consumption (Memory) | An attacker could provide unexpected values and cause a program crash or arbitrary control of resource allocation, leading to excessive consumption of resources such as memory and CPU. |
| Confidentiality | Read Memory<br>Read Files or Directories | An attacker could read confidential data if they are able to control resource references. |
| Integrity<br>Confidentiality<br>Availability | Modify Memory<br>Execute Unauthorized Code or Commands | An attacker could use malicious input to modify data or possibly alter control flow in unexpected ways, including arbitrary command execution. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-3

  Some instances of improper input validation can be detected using automated static analysis.

  A static analysis tool might allow the user to specify which application-specific methods or functions perform input validation; the tool might also have built-in knowledge of validation frameworks such as Struts. The tool may then suppress or de-prioritize any associated warnings. This allows the analyst to focus on areas of the software in which input validation does not appear to be present.

  Except in the cases described in the previous paragraph, automated static analysis might not be able to recognize when proper input validation is being performed, leading to false positives - i.e., warnings that do not have any security consequences or require any code changes.

- **Method:** Manual Static Analysis · **ID:** DM-4

  When custom input validation is required, such as when enforcing business rules, manual analysis is necessary to ensure that the validation is properly implemented.

- **Method:** Fuzzing · **ID:** DM-5

  Fuzzing techniques can be useful for detecting input validation errors. When unexpected inputs are provided to the software, the software should not crash or otherwise become unstable, and it should generate application-controlled error messages. If exceptions or interpreter-generated error messages occur, this indicates that the input was not detected and handled within the application logic itself.

- **Method:** Automated Static Analysis - Binary or Bytecode

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Cost effective for partial coverage:

  - Bytecode Weakness Analysis - including disassembler + source code weakness analysis
  - Binary Weakness Analysis - including disassembler + source code weakness analysis

  **Effectiveness:** SOAR Partial

- **Method:** Manual Static Analysis - Binary or Bytecode

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Cost effective for partial coverage:

  - Binary / Bytecode disassembler - then use manual analysis for vulnerabilities & anomalies

  **Effectiveness:** SOAR Partial

- **Method:** Dynamic Analysis with Automated Results Interpretation

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Web Application Scanner
  - Web Services Scanner
  - Database Scanners

  **Effectiveness:** High

- **Method:** Dynamic Analysis with Manual Results Interpretation

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Fuzz Tester
  - Framework-based Fuzzer

  Cost effective for partial coverage:

  - Host Application Interface Scanner
  - Monitored Virtual Environment - run potentially malicious code in sandbox / wrapper / virtual machine, see if it does anything suspicious

  **Effectiveness:** High

- **Method:** Manual Static Analysis - Source Code

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Focused Manual Spotcheck - Focused manual analysis of source
  - Manual Source Code Review (not inspections)

  **Effectiveness:** High

- **Method:** Automated Static Analysis - Source Code

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Source code Weakness Analyzer
  - Context-configured Source Code Weakness Analyzer

  **Effectiveness:** High

- **Method:** Architecture or Design Review

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Inspection (IEEE 1028 standard) (can apply to requirements, design, source code, etc.)
  - Formal Methods / Correct-By-Construction

  Cost effective for partial coverage:

  - Attack Modeling

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Architecture and Design · **Strategy:** Attack Surface Reduction

  Consider using language-theoretic security (LangSec) techniques that characterize inputs using a formal language and build "recognizers" for that language. This effectively requires parsing to be a distinct layer that effectively enforces a boundary between raw input and internal data representations, instead of allowing parser code to be scattered throughout the program, where it could be subject to errors or inconsistencies that create weaknesses. [REF-1109] [REF-1110] [REF-1111]

- **Phase:** Architecture and Design · **Strategy:** Libraries or Frameworks · **ID:** MIT-7

  Use an input validation framework such as Struts or the OWASP ESAPI Validation API. Note that using a framework does not automatically address all input validation problems; be mindful of weaknesses that could arise from misusing the framework itself (CWE-1173).

- **Phase:** Architecture and Design; Implementation · **Strategy:** Attack Surface Reduction · **ID:** MIT-6

  Understand all the potential areas where untrusted inputs can enter the product, including but not limited to: parameters or arguments, cookies, anything read from the network, environment variables, reverse DNS lookups, query results, request headers, URL components, e-mail, files, filenames, databases, and any external systems that provide data to the application. Remember that such inputs may be obtained indirectly through API calls.

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

  **Effectiveness:** High

- **Phase:** Architecture and Design

  For any security checks that are performed on the client side, ensure that these checks are duplicated on the server side, in order to avoid CWE-602. Attackers can bypass the client-side checks by modifying values after the checks have been performed, or by changing the client to remove the client-side checks entirely. Then, these modified values would be submitted to the server.

  Even though client-side checks provide minimal benefits with respect to server-side security, they are still useful. First, they can support intrusion detection. If the server receives input that should have been rejected by the client, then it may be an indication of an attack. Second, client-side error-checking can provide helpful feedback to the user about the expectations for valid input. Third, there may be a reduction in server-side processing time for accidental input errors, although this is typically a small savings.

- **Phase:** Implementation

  When your application combines data from multiple sources, perform the validation after the sources have been combined. The individual data elements may pass the validation step but violate the intended restrictions after they have been combined.

- **Phase:** Implementation · **ID:** MIT-35

  Be especially careful to validate all input when invoking code that crosses language boundaries, such as from an interpreted language to native code. This could create an unexpected interaction between the language boundaries. Ensure that you are not violating any of the expectations of the language with which you are interfacing. For example, even though Java may not be susceptible to buffer overflows, providing a large argument in a call to native code might trigger an overflow.

- **Phase:** Implementation

  Directly convert your input type into the expected data type, such as using a conversion function that translates a string into a number. After converting to the expected data type, ensure that the input's values fall within the expected range of allowable values and that multi-field consistencies are maintained.

- **Phase:** Implementation

  Inputs should be decoded and canonicalized to the application's current internal representation before being validated (CWE-180, CWE-181). Make sure that your application does not inadvertently decode the same input twice (CWE-174). Such errors could be used to bypass allowlist schemes by introducing dangerous inputs after they have been checked. Use libraries such as the OWASP ESAPI Canonicalization control.

  Consider performing repeated canonicalization until your input does not change any more. This will avoid double-decoding and similar scenarios, but it might inadvertently modify inputs that are allowed to contain properly-encoded dangerous content.

- **Phase:** Implementation

  When exchanging data between components, ensure that both components are using the same character encoding. Ensure that the proper encoding is applied at each interface. Explicitly set the encoding you are using whenever the protocol allows you to do so.

## Demonstrative Examples

### Example 1 (DX-135)

This example demonstrates a shopping interaction in which the user is free to specify the quantity of items to be purchased and a total is calculated.

*Example (Bad, Java):*

```java
...
public static final double price = 20.00;
int quantity = currentUser.getAttribute("quantity");
double total = price * quantity;
chargeUser(total);
...
```

The user has no control over the price variable, however the code does not prevent a negative value from being specified for quantity. If an attacker were to provide a negative value, then the user would have their account credited instead of debited.

### Example 2 (DX-136)

This example asks the user for a height and width of an m X n game board with a maximum dimension of 100 squares.

*Example (Bad, C):*

```c
...
#define MAX_DIM 100
...
/* board dimensions */

int m,n, error;
board_square_t *board;
printf("Please specify the board height: \n");
error = scanf("%d", &m);
if ( EOF == error ){
    die("No integer passed: Die evil hacker!\n");
}
printf("Please specify the board width: \n");
error = scanf("%d", &n);
if ( EOF == error ){
    die("No integer passed: Die evil hacker!\n");
}
if ( m > MAX_DIM || n > MAX_DIM ) {
    die("Value too large: Die evil hacker!\n");
}
board = (board_square_t*) malloc( m * n * sizeof(board_square_t));
...
```

While this code checks to make sure the user cannot specify large, positive integers and consume too much memory, it does not check for negative values supplied by the user. As a result, an attacker can perform a resource consumption (CWE-400) attack against this program by specifying two, large negative values that will not overflow, resulting in a very large memory allocation (CWE-789) and possibly a system crash. Alternatively, an attacker can provide very large negative values which will cause an integer overflow (CWE-190) and unexpected behavior will follow depending on how the values are treated in the remainder of the program.

### Example 3

The following example shows a PHP application in which the programmer attempts to display a user's birthday and homepage.

*Example (Bad, PHP):*

```php
$birthday = $_GET['birthday'];
$homepage = $_GET['homepage'];
echo "Birthday: $birthday<br>Homepage: <a href=$homepage>click here</a>"
```

The programmer intended for $birthday to be in a date format and $homepage to be a valid URL. However, since the values are derived from an HTTP request, if an attacker can trick a victim into clicking a crafted URL with &lt;script> tags providing the values for birthday and / or homepage, then the script will run on the client's browser when the web server echoes the content. Notice that even if the programmer were to defend the $birthday variable by restricting input to integers and dashes, it would still be possible for an attacker to provide a string of the form:

*Example (Attack):*

```
2009-01-09--
```

If this data were used in a SQL statement, it would treat the remainder of the statement as a comment. The comment could disable other security-related logic in the statement. In this case, encoding combined with input validation would be a more useful protection mechanism.

Furthermore, an XSS (CWE-79) attack or SQL injection (CWE-89) are just a few of the potential consequences when input validation is not used. Depending on the context of the code, CRLF Injection (CWE-93), Argument Injection (CWE-88), or Command Injection (CWE-77) may also be possible.

### Example 4 (DX-34)

The following example takes a user-supplied value to allocate an array of objects and then operates on the array.

*Example (Bad, Java):*

```java
private void buildList ( int untrustedListSize ){
    if ( 0 > untrustedListSize ){
        die("Negative value supplied for list size, die evil hacker!");
    }
    Widget[] list = new Widget [ untrustedListSize ];
    list[0] = new Widget();
}
```

This example attempts to build a list from a user-specified value, and even checks to ensure a non-negative value is supplied. If, however, a 0 value is provided, the code will build an array of size 0 and then try to store a new Widget in the first location, causing an exception to be thrown.

### Example 5 (DX-110)

This Android application has registered to handle a URL when sent an intent:

*Example (Bad, Java):*

```java
...
IntentFilter filter = new IntentFilter("com.example.URLHandler.openURL");
MyReceiver receiver = new MyReceiver();
registerReceiver(receiver, filter);
...

public class UrlHandlerReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if("com.example.URLHandler.openURL".equals(intent.getAction())) {
            String URL = intent.getStringExtra("URLToOpen");
            int length = URL.length();
        ...
        }
    }
}
```

The application assumes the URL will always be included in the intent. When the URL is not present, the call to getStringExtra() will return null, thus causing a null pointer exception when length() is called.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2024-37032](https://www.cve.org/CVERecord?id=CVE-2024-37032) | Large language model (LLM) management tool does not validate the format of a digest value (CWE-1287) from a private, untrusted model registry, enabling relative path traversal (CWE-23), a.k.a. Probllama |
| [CVE-2022-45918](https://www.cve.org/CVERecord?id=CVE-2022-45918) | Chain: a learning management tool debugger uses external input to locate previous session logs (CWE-73) and does not properly validate the given path (CWE-20), allowing for filesystem path traversal using "../" sequences (CWE-24) |
| [CVE-2021-30860](https://www.cve.org/CVERecord?id=CVE-2021-30860) | Chain: improper input validation (CWE-20) leads to integer overflow (CWE-190) in mobile OS, as exploited in the wild per CISA KEV. |
| [CVE-2021-30663](https://www.cve.org/CVERecord?id=CVE-2021-30663) | Chain: improper input validation (CWE-20) leads to integer overflow (CWE-190) in mobile OS, as exploited in the wild per CISA KEV. |
| [CVE-2021-22205](https://www.cve.org/CVERecord?id=CVE-2021-22205) | Chain: backslash followed by a newline can bypass a validation step (CWE-20), leading to eval injection (CWE-95), as exploited in the wild per CISA KEV. |
| [CVE-2021-21220](https://www.cve.org/CVERecord?id=CVE-2021-21220) | Chain: insufficient input validation (CWE-20) in browser allows heap corruption (CWE-787), as exploited in the wild per CISA KEV. |
| [CVE-2020-9054](https://www.cve.org/CVERecord?id=CVE-2020-9054) | Chain: improper input validation (CWE-20) in username parameter, leading to OS command injection (CWE-78), as exploited in the wild per CISA KEV. |
| [CVE-2020-3452](https://www.cve.org/CVERecord?id=CVE-2020-3452) | Chain: security product has improper input validation (CWE-20) leading to directory traversal (CWE-22), as exploited in the wild per CISA KEV. |
| [CVE-2020-3161](https://www.cve.org/CVERecord?id=CVE-2020-3161) | Improper input validation of HTTP requests in IP phone, as exploited in the wild per CISA KEV. |
| [CVE-2020-3580](https://www.cve.org/CVERecord?id=CVE-2020-3580) | Chain: improper input validation (CWE-20) in firewall product leads to XSS (CWE-79), as exploited in the wild per CISA KEV. |
| [CVE-2021-37147](https://www.cve.org/CVERecord?id=CVE-2021-37147) | Chain: caching proxy server has improper input validation (CWE-20) of headers, allowing HTTP response smuggling (CWE-444) using an "LF line ending" |
| [CVE-2008-5305](https://www.cve.org/CVERecord?id=CVE-2008-5305) | Eval injection in Perl program using an ID that should only contain hyphens and numbers. |
| [CVE-2008-2223](https://www.cve.org/CVERecord?id=CVE-2008-2223) | SQL injection through an ID that was supposed to be numeric. |
| [CVE-2008-3477](https://www.cve.org/CVERecord?id=CVE-2008-3477) | lack of input validation in spreadsheet program leads to buffer overflows, integer overflows, array index errors, and memory corruption. |
| [CVE-2008-3843](https://www.cve.org/CVERecord?id=CVE-2008-3843) | insufficient validation enables XSS |
| [CVE-2008-3174](https://www.cve.org/CVERecord?id=CVE-2008-3174) | driver in security product allows code execution due to insufficient validation |
| [CVE-2007-3409](https://www.cve.org/CVERecord?id=CVE-2007-3409) | infinite loop from DNS packet with a label that points to itself |
| [CVE-2006-6870](https://www.cve.org/CVERecord?id=CVE-2006-6870) | infinite loop from DNS packet with a label that points to itself |
| [CVE-2008-1303](https://www.cve.org/CVERecord?id=CVE-2008-1303) | missing parameter leads to crash |
| [CVE-2007-5893](https://www.cve.org/CVERecord?id=CVE-2007-5893) | HTTP request with missing protocol version number leads to crash |
| [CVE-2006-6658](https://www.cve.org/CVERecord?id=CVE-2006-6658) | request with missing parameters leads to information exposure |
| [CVE-2008-4114](https://www.cve.org/CVERecord?id=CVE-2008-4114) | system crash with offset value that is inconsistent with packet size |
| [CVE-2006-3790](https://www.cve.org/CVERecord?id=CVE-2006-3790) | size field that is inconsistent with packet size leads to buffer over-read |
| [CVE-2008-2309](https://www.cve.org/CVERecord?id=CVE-2008-2309) | product uses a denylist to identify potentially dangerous content, allowing attacker to bypass a warning |
| [CVE-2008-3494](https://www.cve.org/CVERecord?id=CVE-2008-3494) | security bypass via an extra header |
| [CVE-2008-3571](https://www.cve.org/CVERecord?id=CVE-2008-3571) | empty packet triggers reboot |
| [CVE-2006-5525](https://www.cve.org/CVERecord?id=CVE-2006-5525) | incomplete denylist allows SQL injection |
| [CVE-2008-1284](https://www.cve.org/CVERecord?id=CVE-2008-1284) | NUL byte in theme name causes directory traversal impact to be worse |
| [CVE-2008-0600](https://www.cve.org/CVERecord?id=CVE-2008-0600) | kernel does not validate an incoming pointer before dereferencing it |
| [CVE-2008-1738](https://www.cve.org/CVERecord?id=CVE-2008-1738) | anti-virus product has insufficient input validation of hooked SSDT functions, allowing code execution |
| [CVE-2008-1737](https://www.cve.org/CVERecord?id=CVE-2008-1737) | anti-virus product allows DoS via zero-length field |
| [CVE-2008-3464](https://www.cve.org/CVERecord?id=CVE-2008-3464) | driver does not validate input from userland to the kernel |
| [CVE-2008-2252](https://www.cve.org/CVERecord?id=CVE-2008-2252) | kernel does not validate parameters sent in from userland, allowing code execution |
| [CVE-2008-2374](https://www.cve.org/CVERecord?id=CVE-2008-2374) | lack of validation of string length fields allows memory consumption or buffer over-read |
| [CVE-2008-1440](https://www.cve.org/CVERecord?id=CVE-2008-1440) | lack of validation of length field leads to infinite loop |
| [CVE-2008-1625](https://www.cve.org/CVERecord?id=CVE-2008-1625) | lack of validation of input to an IOCTL allows code execution |
| [CVE-2008-3177](https://www.cve.org/CVERecord?id=CVE-2008-3177) | zero-length attachment causes crash |
| [CVE-2008-5563](https://www.cve.org/CVERecord?id=CVE-2008-5563) | crash via a malformed frame structure |
| [CVE-2008-5285](https://www.cve.org/CVERecord?id=CVE-2008-5285) | infinite loop from a long SMTP request |
| [CVE-2008-3812](https://www.cve.org/CVERecord?id=CVE-2008-3812) | router crashes with a malformed packet |
| [CVE-2008-3680](https://www.cve.org/CVERecord?id=CVE-2008-3680) | packet with invalid version number leads to NULL pointer dereference |
| [CVE-2008-3660](https://www.cve.org/CVERecord?id=CVE-2008-3660) | crash via multiple "." characters in file extension |

## Dimensions

- **Behavior-Type:** Validation
- **Behavior-Property:** Improper
- **Input-Type:** Input

## Technical Nuance

Input validation is a frequently-used technique for checking potentially dangerous inputs in order to ensure that the inputs are safe for processing within the code, or when communicating with other components.

Input can consist of:

- raw data - strings, numbers, parameters, file contents, etc.
- metadata - information about the raw data, such as headers or size

Data can be simple or structured. Structured data can be composed of many nested layers, composed of combinations of metadata and raw data, with other simple or structured data.

Many properties of raw data or metadata may need to be validated upon entry into the code, such as:

- specified quantities such as size, length, frequency, price, rate, number of operations, time, etc.
- implied or derived quantities, such as the actual size of a file instead of a specified size
- indexes, offsets, or positions into more complex data structures
- symbolic keys or other elements into hash tables, associative arrays, etc.
- well-formedness, i.e. syntactic correctness - compliance with expected syntax
- lexical token correctness - compliance with rules for what is treated as a token
- specified or derived type - the actual type of the input (or what the input appears to be)
- consistency - between individual data elements, between raw data and metadata, between references, etc.
- conformance to domain-specific rules, e.g. business logic
- equivalence - ensuring that equivalent inputs are treated the same
- authenticity, ownership, or other attestations about the input, e.g. a cryptographic signature to prove the source of the data

Implied or derived properties of data must often be calculated or inferred by the code itself. Errors in deriving properties may be considered a contributing factor to improper input validation.

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| 7 Pernicious Kingdoms |  | Input validation and representation |  |
| OWASP Top Ten 2004 | A1 | Unvalidated Input | CWE More Specific |
| CERT C Secure Coding | ERR07-C | Prefer functions that support error checking over equivalent functions that don't |  |
| CERT C Secure Coding | FIO30-C | Exclude user input from format strings | CWE More Abstract |
| CERT C Secure Coding | MEM10-C | Define and use a pointer validation function |  |
| WASC | 20 | Improper Input Handling |  |
| Software Fault Patterns | SFP25 | Tainted input to variable |  |
| OWASP Golang Secure Coding Practices Guide |  | Input Validation |  |

## Related Attack Patterns

- [CAPEC-10](https://capec.mitre.org/data/definitions/10.html)
- [CAPEC-101](https://capec.mitre.org/data/definitions/101.html)
- [CAPEC-104](https://capec.mitre.org/data/definitions/104.html)
- [CAPEC-108](https://capec.mitre.org/data/definitions/108.html)
- [CAPEC-109](https://capec.mitre.org/data/definitions/109.html)
- [CAPEC-110](https://capec.mitre.org/data/definitions/110.html)
- [CAPEC-120](https://capec.mitre.org/data/definitions/120.html)
- [CAPEC-13](https://capec.mitre.org/data/definitions/13.html)
- [CAPEC-135](https://capec.mitre.org/data/definitions/135.html)
- [CAPEC-136](https://capec.mitre.org/data/definitions/136.html)
- [CAPEC-14](https://capec.mitre.org/data/definitions/14.html)
- [CAPEC-153](https://capec.mitre.org/data/definitions/153.html)
- [CAPEC-182](https://capec.mitre.org/data/definitions/182.html)
- [CAPEC-209](https://capec.mitre.org/data/definitions/209.html)
- [CAPEC-22](https://capec.mitre.org/data/definitions/22.html)
- [CAPEC-23](https://capec.mitre.org/data/definitions/23.html)
- [CAPEC-230](https://capec.mitre.org/data/definitions/230.html)
- [CAPEC-231](https://capec.mitre.org/data/definitions/231.html)
- [CAPEC-24](https://capec.mitre.org/data/definitions/24.html)
- [CAPEC-250](https://capec.mitre.org/data/definitions/250.html)
- [CAPEC-261](https://capec.mitre.org/data/definitions/261.html)
- [CAPEC-267](https://capec.mitre.org/data/definitions/267.html)
- [CAPEC-28](https://capec.mitre.org/data/definitions/28.html)
- [CAPEC-3](https://capec.mitre.org/data/definitions/3.html)
- [CAPEC-31](https://capec.mitre.org/data/definitions/31.html)
- [CAPEC-42](https://capec.mitre.org/data/definitions/42.html)
- [CAPEC-43](https://capec.mitre.org/data/definitions/43.html)
- [CAPEC-45](https://capec.mitre.org/data/definitions/45.html)
- [CAPEC-46](https://capec.mitre.org/data/definitions/46.html)
- [CAPEC-47](https://capec.mitre.org/data/definitions/47.html)
- [CAPEC-473](https://capec.mitre.org/data/definitions/473.html)
- [CAPEC-52](https://capec.mitre.org/data/definitions/52.html)
- [CAPEC-53](https://capec.mitre.org/data/definitions/53.html)
- [CAPEC-588](https://capec.mitre.org/data/definitions/588.html)
- [CAPEC-63](https://capec.mitre.org/data/definitions/63.html)
- [CAPEC-64](https://capec.mitre.org/data/definitions/64.html)
- [CAPEC-664](https://capec.mitre.org/data/definitions/664.html)
- [CAPEC-67](https://capec.mitre.org/data/definitions/67.html)
- [CAPEC-7](https://capec.mitre.org/data/definitions/7.html)
- [CAPEC-71](https://capec.mitre.org/data/definitions/71.html)
- [CAPEC-72](https://capec.mitre.org/data/definitions/72.html)
- [CAPEC-73](https://capec.mitre.org/data/definitions/73.html)
- [CAPEC-78](https://capec.mitre.org/data/definitions/78.html)
- [CAPEC-79](https://capec.mitre.org/data/definitions/79.html)
- [CAPEC-8](https://capec.mitre.org/data/definitions/8.html)
- [CAPEC-80](https://capec.mitre.org/data/definitions/80.html)
- [CAPEC-81](https://capec.mitre.org/data/definitions/81.html)
- [CAPEC-83](https://capec.mitre.org/data/definitions/83.html)
- [CAPEC-85](https://capec.mitre.org/data/definitions/85.html)
- [CAPEC-88](https://capec.mitre.org/data/definitions/88.html)
- [CAPEC-9](https://capec.mitre.org/data/definitions/9.html)

## References

- [REF-6] Katrina Tsipenyuk, Brian Chess and Gary McGraw. "Seven Pernicious Kingdoms: A Taxonomy of Software Security Errors". NIST Workshop on Software Security Assurance Tools Techniques and Metrics. NIST. 2005-11-07. <https://cwe.mitre.org/documents/sources/SevenPerniciousKingdoms.pdf>.
- [REF-166] Jim Manico. "Input Validation with ESAPI - Very Important". 2008-08-15. <https://manicode.blogspot.com/2008/08/input-validation-with-esapi.html> (URL validated: 2023-04-07).
- [REF-45] OWASP. "OWASP Enterprise Security API (ESAPI) Project". <https://owasp.org/www-project-enterprise-security-api/> (URL validated: 2025-07-24).
- [REF-168] Joel Scambray, Mike Shema and Caleb Sima. "Hacking Exposed Web Applications, Second Edition". Input Validation Attacks. McGraw-Hill. 2006-06-05.
- [REF-48] Jeremiah Grossman. "Input validation or output filtering, which is better?". 2007-01-30. <https://blog.jeremiahgrossman.com/2007/01/input-validation-or-output-filtering.html> (URL validated: 2023-04-07).
- [REF-170] Kevin Beaver. "The importance of input validation". 2006-09-06. <http://searchsoftwarequality.techtarget.com/tip/0,289483,sid92_gci1214373,00.html>.
- [REF-7] Michael Howard and David LeBlanc. "Writing Secure Code". Chapter 10, "All Input Is Evil!" Page 341. 2nd Edition. Microsoft Press. 2002-12-04. <https://www.microsoftpressstore.com/store/writing-secure-code-9780735617223>.
- [REF-1109] "LANGSEC: Language-theoretic Security". <http://langsec.org/>.
- [REF-1110] "LangSec: Recognition, Validation, and Compositional Correctness for Real World Security". <http://langsec.org/bof-handout.pdf>.
- [REF-1111] Sergey Bratus, Lars Hermerschmidt, Sven M. Hallberg, Michael E. Locasto, Falcon D. Momot, Meredith L. Patterson and Anna Shubina. "Curing the Vulnerable Parser: Design Patterns for Secure Input Handling". USENIX ;login:. 2017. <https://www.usenix.org/system/files/login/articles/login_spring17_08_bratus.pdf>.
- [REF-1287] MITRE. "Supplemental Details - 2022 CWE Top 25". Details of Problematic Mappings. 2022-06-28. <https://cwe.mitre.org/top25/archive/2022/2022_cwe_top25_supplemental.html#problematicMappingDetails> (URL validated: 2024-11-17).
- [REF-1479] Gregory Larsen, E. Kenneth Hong Fong, David A. Wheeler and Rama S. Moorthy. "State-of-the-Art Resources (SOAR) for Software Vulnerability Detection, Test, and Evaluation". 2014-07. <https://www.ida.org/-/media/feature/publications/s/st/stateoftheart-resources-soar-for-software-vulnerability-detection-test-and-evaluation/p-5061.ashx> (URL validated: 2025-09-05).
- [REF-1566] OWASP. "Golang Secure Coding Practices guide". Input Validation, page 6. 2024. <https://github.com/OWASP/Go-SCP> (URL validated: 2026-10-19).

## Mapping Notes

- **Usage:** Discouraged

- **Rationale:** CWE-20 is commonly misused in low-information vulnerability reports when lower-level CWEs could be used instead, or when more details about the vulnerability are available [REF-1287]. It is not useful for trend analysis. It is also a level-1 Class (i.e., a child of a Pillar). Finally, CWE-20 is often misused when the root cause issue is related to how input is incorrectly transformed, instead of "validated" to be correct as-is.

- **Comments:**

  Within CWE, the "input validation" term focuses on the act of checking whether an input is already safe, which is different from other techniques that ensure safe processing of input. Carefully perform root-cause analysis to be sure that the issue is not due to techniques that attempt to transform potentially-dangerous input into something safe, such as filtering (CWE-790) - which attempts to remove dangerous inputs - or encoding/escaping (CWE-116), which attempts to ensure that the input is not misinterpreted when it is included in output to another component.

  If the issue is truly due to improper input validation, consider using lower-level children.

- **Reasons:** Frequent Misuse, Frequent Misinterpretation, Abstraction

- **Suggestions:**

  - [CWE-1173](../weaknesses/CWE-1173.md) Improper Use of Validation Framework (Base): Not Using an Input Validation Framework
  - [CWE-116](../weaknesses/CWE-116.md) Improper Encoding or Escaping of Output (Class)
  - [CWE-790](../weaknesses/CWE-790.md) Improper Filtering of Special Elements (Class)
  - [CWE-1284](../weaknesses/CWE-1284.md) Improper Validation of Specified Quantity in Input (Base): Specified Quantity
  - [CWE-1285](../weaknesses/CWE-1285.md) Improper Validation of Specified Index, Position, or Offset in Input (Base): Specified Index, Position, or Offset
  - [CWE-1286](../weaknesses/CWE-1286.md) Improper Validation of Syntactic Correctness of Input (Base): Syntactic Correctness
  - [CWE-1287](../weaknesses/CWE-1287.md) Improper Validation of Specified Type of Input (Base): Specified Type
  - [CWE-1288](../weaknesses/CWE-1288.md) Improper Validation of Consistency within Input (Base): Consistency within Input
  - [CWE-1289](../weaknesses/CWE-1289.md) Improper Validation of Unsafe Equivalence in Input (Base): Unsafe Equivalence

## Notes

- **Relationship**:

  CWE-116 and CWE-20 have a close association because, depending on the nature of the structured message, proper input validation can indirectly prevent special characters from changing the meaning of a structured message. For example, by validating that a numeric ID field should only contain the 0-9 characters, the programmer effectively prevents injection attacks.

  Multiple techniques exist to transform potentially dangerous input into something safe, which is different than "validation," which is a technique to check if an input is already safe. CWE users need to be cautious during root cause analysis to ensure that an issue is truly an input-validation problem.

- **Maintenance**: As of 2020, this entry is used more often than preferred, and it is a source of frequent confusion. It is being actively modified for CWE 4.1 and subsequent versions.

- **Maintenance**: Concepts such as validation, data transformation, and neutralization are being refined, so relationships between CWE-20 and other entries such as CWE-707 may change in future versions, along with an update to the Vulnerability Theory document.

- **Maintenance**: Input validation - whether missing or incorrect - is such an essential and widespread part of secure development that it is implicit in many different weaknesses. Traditionally, problems such as buffer overflows and XSS have been classified as input validation problems by many security professionals. However, input validation is not necessarily the only protection mechanism available for avoiding such problems, and in some cases it is not even sufficient. The CWE team has begun capturing these subtleties in chains within the Research Concepts view (CWE-1000), but more work is needed.

- **Terminology**:

  The "input validation" term is extremely common, but it is used in many different ways. In some cases its usage can obscure the real underlying weakness or otherwise hide chaining and composite relationships.

  Some people use "input validation" as a general term that covers many different neutralization techniques for ensuring that input is appropriate, such as filtering, i.e., attempting to remove dangerous inputs (related to CWE-790); encoding/escaping, i.e., attempting to ensure that the input is not misinterpreted when it is included in output to another component (related to CWE-116); or canonicalization, which often indirectly removes otherwise-dangerous inputs. Others use the term in a narrower context to simply mean "checking if an input conforms to expectations without changing it." CWE uses this narrow interpretation.

  Note that "input validation" has very different meanings to different people, or within different classification schemes. Caution must be used when referencing this CWE entry or mapping to it. For example, some weaknesses might involve inadvertently giving control to an attacker over an input when they should not be able to provide an input at all, but sometimes this is referred to as input validation.

  Finally, it is important to emphasize that the distinctions between input validation and output escaping are often blurred. Developers must be careful to understand the difference, including how input validation is not always sufficient to prevent vulnerabilities, especially when less stringent data types must be supported, such as free-form text. Consider a SQL injection scenario in which a person's last name is inserted into a query. The name "O'Reilly" would likely pass the validation step since it is a common last name in the English language. However, this valid name cannot be directly inserted into the database because it contains the "'" apostrophe character, which would need to be escaped or otherwise transformed. In this case, removing the apostrophe might reduce the risk of SQL injection, but it would produce incorrect behavior because the wrong name would be recorded.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | 7 Pernicious Kingdoms |  | CWE Draft 3, 2006-07-19 |  |
| Contribution (Content) | 2024-02-29 | Abhi Balakrishnan |  | CWE 4.17, 2025-04-03 | Contributed usability diagram concepts used by the CWE team. |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Potential_Mitigations, Time_of_Introduction |
| Modification | 2008-08-15 |  | Veracode | CWE 1.0, 2008-09-09 | Suggested OWASP Top Ten 2004 mapping |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, Other_Notes, Taxonomy_Mappings |
| Modification | 2008-11-24 | CWE Content Team | MITRE | CWE 1.1, 2008-11-25 | updated Relationships, Taxonomy_Mappings |
| Modification | 2009-01-12 | CWE Content Team | MITRE | CWE 1.2, 2009-01-12 | updated Applicable_Platforms, Common_Consequences, Demonstrative_Examples, Description, Likelihood_of_Exploit, Name, Observed_Examples, Other_Notes, Potential_Mitigations, References, Relationship_Notes, Relationships |
| Modification | 2009-03-10 | CWE Content Team | MITRE | CWE 1.3, 2009-03-10 | updated Description, Potential_Mitigations |
| Modification | 2009-05-27 | CWE Content Team | MITRE | CWE 1.4, 2009-05-27 | updated Related_Attack_Patterns |
| Modification | 2009-07-27 | CWE Content Team | MITRE | CWE 1.5, 2009-07-27 | updated Relationships |
| Modification | 2009-10-29 | CWE Content Team | MITRE | CWE 1.6, 2009-10-29 | updated Common_Consequences, Demonstrative_Examples, Maintenance_Notes, Modes_of_Introduction, Observed_Examples, Relationships, Research_Gaps, Terminology_Notes |
| Modification | 2009-12-28 | CWE Content Team | MITRE | CWE 1.7, 2009-12-28 | updated Applicable_Platforms, Demonstrative_Examples, Detection_Factors |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 | updated Detection_Factors, Potential_Mitigations, References, Taxonomy_Mappings |
| Modification | 2010-04-05 | CWE Content Team | MITRE | CWE 1.8.1, 2010-04-05 | updated Related_Attack_Patterns |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Potential_Mitigations, Research_Gaps, Terminology_Notes |
| Modification | 2010-09-27 | CWE Content Team | MITRE | CWE 1.10, 2010-09-27 | updated Potential_Mitigations, Relationships |
| Modification | 2010-12-13 | CWE Content Team | MITRE | CWE 1.11, 2010-12-13 | updated Demonstrative_Examples, Description |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Observed_Examples |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Applicable_Platforms, Common_Consequences, Relationship_Notes |
| Modification | 2011-09-13 | CWE Content Team | MITRE | CWE 2.1, 2011-09-13 | updated Relationships, Taxonomy_Mappings |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Demonstrative_Examples, References, Related_Attack_Patterns, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2013-02-21 | CWE Content Team | MITRE | CWE 2.4, 2013-02-21 | updated Relationships |
| Modification | 2013-07-17 | CWE Content Team | MITRE | CWE 2.5, 2013-07-17 | updated Relationships |
| Modification | 2014-02-18 | CWE Content Team | MITRE | CWE 2.6, 2014-02-19 | updated Demonstrative_Examples, Related_Attack_Patterns |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Detection_Factors, Relationships, Taxonomy_Mappings |
| Modification | 2015-12-07 | CWE Content Team | MITRE | CWE 2.9, 2015-12-07 | updated Relationships |
| Modification | 2017-01-19 | CWE Content Team | MITRE | CWE 2.10, 2017-01-19 | updated Related_Attack_Patterns, Relationships |
| Modification | 2017-05-03 | CWE Content Team | MITRE | CWE 2.11, 2017-05-05 | updated Related_Attack_Patterns, Relationships |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Modes_of_Introduction, References, Relationships, Taxonomy_Mappings |
| Modification | 2018-03-27 | CWE Content Team | MITRE | CWE 3.1, 2018-03-27 | updated References |
| Modification | 2019-01-03 | CWE Content Team | MITRE | CWE 3.2, 2019-01-03 | updated Related_Attack_Patterns, Relationships |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Related_Attack_Patterns, Relationships |
| Modification | 2019-09-19 | CWE Content Team | MITRE | CWE 3.4, 2019-09-19 | updated Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Potential_Mitigations, References, Related_Attack_Patterns, Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Applicable_Platforms, Demonstrative_Examples, Description, Maintenance_Notes, Observed_Examples, Potential_Mitigations, References, Relationship_Notes, Relationships, Research_Gaps, Terminology_Notes |
| Modification | 2020-08-20 | CWE Content Team | MITRE | CWE 4.2, 2020-08-20 | updated Potential_Mitigations, Related_Attack_Patterns, Relationships |
| Modification | 2021-03-15 | CWE Content Team | MITRE | CWE 4.4, 2021-03-15 | updated Description, Potential_Mitigations |
| Modification | 2021-07-20 | CWE Content Team | MITRE | CWE 4.5, 2021-07-20 | updated Related_Attack_Patterns, Relationships |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 | updated Relationships |
| Modification | 2022-04-28 | CWE Content Team | MITRE | CWE 4.7, 2022-04-28 | updated Relationships |
| Modification | 2022-06-28 | CWE Content Team | MITRE | CWE 4.8, 2022-06-28 | updated Observed_Examples, Relationships |
| Modification | 2022-10-13 | CWE Content Team | MITRE | CWE 4.9, 2022-10-13 | updated References, Relationships |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated References, Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes, Relationships |
| Modification | 2023-10-26 | CWE Content Team | MITRE | CWE 4.13, 2023-10-26 | updated Observed_Examples |
| Modification | 2024-07-16 | CWE Content Team | MITRE | CWE 4.15, 2024-07-16 | updated Observed_Examples |
| Modification | 2024-11-19 | CWE Content Team | MITRE | CWE 4.16, 2024-11-19 | updated Relationships |
| Modification | 2025-04-03 | CWE Content Team | MITRE | CWE 4.17, 2025-04-03 | updated Common_Consequences, Description, Diagram, Mapping_Notes, Potential_Mitigations, Relationship_Notes, Terminology_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Detection_Factors, References |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Relationships, Weakness_Ordinalities |
| Modification | 2026-04-30 | CWE Content Team | MITRE | CWE 4.20, 2026-04-30 | updated Applicable_Platforms, Mapping_Notes |
| Modification | 2026-10-28 | CWE Content Team | MITRE | CWE 5.0, 2026-10-28 | updated Applicable_Platforms, Description, Dimensions, Mapping_Notes, Observed_Examples, References, Relationships, Taxonomy_Mappings, Technical_Nuance |

**Previous Entry Names:**

- Insufficient Input Validation — 2009-01-12

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
