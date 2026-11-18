---
secid: "secid:weakness/mitre.org/cwe@4.21#CWE-89"
cwe_id: "CWE-89"
entry_type: weakness
name: "Improper Neutralization of Special Elements used in an SQL Command"
abstraction: Base
structure: Simple
status: Stable
mapping_usage: Allowed
cwe_version: "4.21"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/89.html"
---

# CWE-89: Improper Neutralization of Special Elements used in an SQL Command

## Description

The product constructs all or part of an SQL command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended SQL command when it is sent to a downstream component. Without sufficient removal or quoting of SQL syntax in user-controllable inputs, the generated SQL query can cause those inputs to be interpreted as SQL instead of ordinary user data. (Roles: Attack-Focused, Common-Name, Abbreviation, Attack-Focused)

![Diagram for CWE-89](https://cwe.mitre.org/data/images/CWE-89-Diagram.png)

## Alternate Terms

- **SQL Injection**: a common attack-oriented phrase
- **SQLi**: a common abbreviation for "SQL injection"

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-943](../weaknesses/CWE-943.md) Improper Neutralization of Special Elements in Data Query Logic (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component (Class) | [CWE-1003](../views/CWE-1003.md) | Primary |

## Weakness Ordinalities

- **Primary**
- **Resultant**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Not Language-Specific | Undetermined |
| Language | Go |  | Undetermined |
| Language | SQL |  | Often |
| Language | Python |  | Undetermined |
| Technology | Database Server |  | Undetermined |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.
- **Implementation**: This weakness typically appears in data-rich applications that save user inputs in a database.

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Integrity<br>Availability | Execute Unauthorized Code or Commands | Adversaries could execute system commands, typically by changing the SQL statement to redirect output to a file that can then be executed. |
| Confidentiality | Read Application Data | Since SQL databases generally hold sensitive data, loss of confidentiality is a frequent problem with SQL injection vulnerabilities. |
| Authentication | Gain Privileges or Assume Identity<br>Bypass Protection Mechanism | If poor SQL commands are used to check user names and passwords or perform other kinds of authentication, it may be possible to connect to the product as another user with no previous knowledge of the password. |
| Access Control | Bypass Protection Mechanism | If authorization information is held in a SQL database, it may be possible to change this information through the successful exploitation of a SQL injection vulnerability. |
| Integrity | Modify Application Data | Just as it may be possible to read sensitive information, it is also possible to modify or even delete this information with a SQL injection attack. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-1

  This weakness can often be detected using automated static analysis tools. Many modern tools use data flow analysis or constraint-based techniques to minimize the number of false positives.

  Automated static analysis might not be able to recognize when proper input validation is being performed, leading to false positives - i.e., warnings that do not have any security consequences or do not require any code changes.

  Automated static analysis might not be able to detect the usage of custom API functions or third-party libraries that indirectly invoke SQL commands, leading to false negatives - especially if the API/library code is not available for analysis.

  **Effectiveness Notes:** This is not a perfect solution, since 100% accuracy and coverage are not feasible.

- **Method:** Automated Dynamic Analysis · **ID:** DM-2

  This weakness can be detected using dynamic tools and techniques that interact with the software using large test suites with many diverse inputs, such as fuzz testing (fuzzing), robustness testing, and fault injection. The software's operation may slow down, but it should not become unstable, crash, or generate incorrect results.

  **Effectiveness:** Moderate

- **Method:** Manual Analysis · **ID:** DM-9

  Manual analysis can be useful for finding this weakness, but it might not achieve desired code coverage within limited time constraints. This becomes difficult for weaknesses that must be considered for all inputs, since the attack surface can be too large.

- **Method:** Automated Static Analysis - Binary or Bytecode

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Bytecode Weakness Analysis - including disassembler + source code weakness analysis
  - Binary Weakness Analysis - including disassembler + source code weakness analysis

  **Effectiveness:** High

- **Method:** Dynamic Analysis with Automated Results Interpretation

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Database Scanners

  Cost effective for partial coverage:

  - Web Application Scanner
  - Web Services Scanner

  **Effectiveness:** High

- **Method:** Dynamic Analysis with Manual Results Interpretation

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Cost effective for partial coverage:

  - Fuzz Tester
  - Framework-based Fuzzer

  **Effectiveness:** SOAR Partial

- **Method:** Manual Static Analysis - Source Code

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Manual Source Code Review (not inspections)

  Cost effective for partial coverage:

  - Focused Manual Spotcheck - Focused manual analysis of source

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

  - Formal Methods / Correct-By-Construction

  Cost effective for partial coverage:

  - Inspection (IEEE 1028 standard) (can apply to requirements, design, source code, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Architecture and Design · **Strategy:** Libraries or Frameworks · **ID:** MIT-4

  Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid [REF-1482].

  For example, consider using persistence layers such as Hibernate or Enterprise Java Beans, which can provide significant protection against SQL injection if used properly.

- **Phase:** Architecture and Design · **Strategy:** Parameterization · **ID:** MIT-27

  If available, use structured mechanisms that automatically enforce the separation between data and code. These mechanisms may be able to provide the relevant quoting, encoding, and validation automatically, instead of relying on the developer to provide this capability at every point where output is generated.

  Process SQL queries using prepared statements, parameterized queries, or stored procedures. These features should accept parameters or variables and support strong typing. Do not dynamically construct and execute query strings within these features using "exec" or similar functionality, since this may re-introduce the possibility of SQL injection. [REF-867]

- **Phase:** Architecture and Design; Operation · **Strategy:** Environment Hardening · **ID:** MIT-17

  Run your code using the lowest privileges that are required to accomplish the necessary tasks [REF-76]. If possible, create isolated accounts with limited privileges that are only used for a single task. That way, a successful attack will not immediately give the attacker access to the rest of the software or its environment. For example, database applications rarely need to run as the database administrator, especially in day-to-day operations.

  Specifically, follow the principle of least privilege when creating user accounts to a SQL database. The database users should only have the minimum privileges necessary to use their account. If the requirements of the system indicate that a user can read and modify their own data, then limit their privileges so they cannot read/write others' data. Use the strictest permissions possible on all database objects, such as execute-only for stored procedures.

- **Phase:** Architecture and Design · **ID:** MIT-15

  For any security checks that are performed on the client side, ensure that these checks are duplicated on the server side, in order to avoid CWE-602. Attackers can bypass the client-side checks by modifying values after the checks have been performed, or by changing the client to remove the client-side checks entirely. Then, these modified values would be submitted to the server.

- **Phase:** Implementation · **Strategy:** Output Encoding · **ID:** MIT-28

  While it is risky to use dynamically-generated query strings, code, or commands that mix control and data together, sometimes it may be unavoidable. Properly quote arguments and escape any special characters within those arguments. The most conservative approach is to escape or filter all characters that do not pass an extremely strict allowlist (such as everything that is not alphanumeric or white space). If some special characters are still needed, such as white space, wrap each argument in quotes after the escaping/filtering step. Be careful of argument injection (CWE-88).

  Instead of building a new implementation, such features may be available in the database or programming language. For example, the Oracle DBMS_ASSERT package can check or enforce that parameters have certain properties that make them less vulnerable to SQL injection. For MySQL, the mysql_real_escape_string() API function is available in both C and PHP.

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

  When constructing SQL query strings, use stringent allowlists that limit the character set based on the expected value of the parameter in the request. This will indirectly limit the scope of an attack, but this technique is less important than proper output encoding and escaping.

  Note that proper output encoding, escaping, and quoting is the most effective solution for preventing SQL injection, although input validation may provide some defense-in-depth. This is because it effectively limits what will appear in output. Input validation will not always prevent SQL injection, especially if you are required to support free-form text fields that could contain arbitrary characters. For example, the name "O'Reilly" would likely pass the validation step, since it is a common last name in the English language. However, it cannot be directly inserted into the database because it contains the "'" apostrophe character, which would need to be escaped or otherwise handled. In this case, stripping the apostrophe might reduce the risk of SQL injection, but it would produce incorrect behavior because the wrong name would be recorded.

  When feasible, it may be safest to disallow meta-characters entirely, instead of escaping them. This will provide some defense in depth. After the data is entered into the database, later processes may neglect to escape meta-characters before use, and you may not have control over those processes.

- **Phase:** Architecture and Design · **Strategy:** Enforcement by Conversion · **ID:** MIT-21

  When the set of acceptable objects, such as filenames or URLs, is limited or known, create a mapping from a set of fixed input values (such as numeric IDs) to the actual filenames or URLs, and reject all other inputs.

- **Phase:** Implementation · **ID:** MIT-39

  Ensure that error messages only contain minimal details that are useful to the intended audience and no one else. The messages need to strike the balance between being too cryptic (which can confuse users) or being too detailed (which may reveal more than intended). The messages should not reveal the methods that were used to determine the error. Attackers can use detailed information to refine or optimize their original attack, thereby increasing their chances of success.

  If errors must be captured in some detail, record them in log messages, but consider what could occur if the log messages can be viewed by attackers. Highly sensitive information such as passwords should never be saved to log files.

  Avoid inconsistent messaging that might accidentally tip off an attacker about internal state, such as whether a user account exists or not.

  In the context of SQL Injection, error messages revealing the structure of a SQL query can help attackers tailor successful attack strings.

- **Phase:** Operation · **Strategy:** Firewall · **ID:** MIT-29

  Use an application firewall that can detect attacks against this weakness. It can be beneficial in cases in which the code cannot be fixed (because it is controlled by a third party), as an emergency prevention measure while more comprehensive software assurance measures are applied, or to provide defense in depth [REF-1481.

  **Effectiveness:** Moderate

  **Effectiveness Notes:** An application firewall might not cover all possible input vectors. In addition, attack techniques might be available to bypass the protection mechanism, such as using malformed inputs that can still be processed by the component that receives those inputs. Depending on functionality, an application firewall might inadvertently reject or modify legitimate requests. Finally, some manual effort may be required for customization.

- **Phase:** Operation; Implementation · **Strategy:** Environment Hardening · **ID:** MIT-16

  When using PHP, configure the application so that it does not use register_globals. During implementation, develop the application so that it does not rely on this feature, but be wary of implementing a register_globals emulation that is subject to weaknesses such as CWE-95, CWE-621, and similar issues.

## Demonstrative Examples

### Example 1

In 2008, a large number of web servers were compromised using the same SQL injection attack string. This single string worked against many different programs. The SQL injection was then used to modify the web sites to serve malicious code.

### Example 2 (DX-209)

The following code dynamically constructs and executes a SQL query that searches for items matching a specified name. The query restricts the items displayed to those where owner matches the user name of the currently-authenticated user.

*Example (Bad, C#):*

```c#
...
string userName = ctx.getAuthenticatedUserName();
string query = "SELECT * FROM items WHERE owner = '" + userName + "' AND itemname = '" + ItemName.Text + "'";
sda = new SqlDataAdapter(query, conn);
DataTable dt = new DataTable();
sda.Fill(dt);
...
```

The query that this code intends to execute follows:

*Example (Informative):*

```
SELECT * FROM items WHERE owner = <userName> AND itemname = <itemName>;
```

However, because the query is constructed dynamically by concatenating a constant base query string and a user input string, the query only behaves correctly if itemName does not contain a single-quote character. If an attacker with the user name wiley enters the string:

*Example (Attack):*

```
name' OR 'a'='a
```

for itemName, then the query becomes the following:

*Example (Attack):*

```
SELECT * FROM items WHERE owner = 'wiley' AND itemname = 'name' OR 'a'='a';
```

The addition of the:

*Example (Attack):*

```
OR 'a'='a
```

condition causes the WHERE clause to always evaluate to true, so the query becomes logically equivalent to the much simpler query:

*Example (Attack):*

```
SELECT * FROM items;
```

This simplification of the query allows the attacker to bypass the requirement that the query only return items owned by the authenticated user; the query now returns all entries stored in the items table, regardless of their specified owner.

### Example 3

This example examines the effects of a different malicious value passed to the query constructed and executed in the previous example.

If an attacker with the user name wiley enters the string:

*Example (Attack):*

```
name'; DELETE FROM items; --
```

for itemName, then the query becomes the following two queries:

*Example (Attack, SQL):*

```sql
SELECT * FROM items WHERE owner = 'wiley' AND itemname = 'name';
DELETE FROM items;
--'
```

Many database servers, including Microsoft(R) SQL Server 2000, allow multiple SQL statements separated by semicolons to be executed at once. While this attack string results in an error on Oracle and other database servers that do not allow the batch-execution of statements separated by semicolons, on databases that do allow batch execution, this type of attack allows the attacker to execute arbitrary commands against the database.

Notice the trailing pair of hyphens (--), which specifies to most database servers that the remainder of the statement is to be treated as a comment and not executed. In this case the comment character serves to remove the trailing single-quote left over from the modified query. On a database where comments are not allowed to be used in this way, the general attack could still be made effective using a trick similar to the one shown in the previous example.

If an attacker enters the string

*Example (Attack):*

```
name'; DELETE FROM items; SELECT * FROM items WHERE 'a'='a
```

Then the following three valid statements will be created:

*Example (Attack):*

```
SELECT * FROM items WHERE owner = 'wiley' AND itemname = 'name';
DELETE FROM items;
SELECT * FROM items WHERE 'a'='a';
```

One traditional approach to preventing SQL injection attacks is to handle them as an input validation problem and either accept only characters from an allowlist of safe values or identify and escape a denylist of potentially malicious values. Allowlists can be a very effective means of enforcing strict input validation rules, but parameterized SQL statements require less maintenance and can offer more guarantees with respect to security. As is almost always the case, denylisting is riddled with loopholes that make it ineffective at preventing SQL injection attacks. For example, attackers can:

- Target fields that are not quoted
- Find ways to bypass the need for certain escaped meta-characters
- Use stored procedures to hide the injected meta-characters.

Manually escaping characters in input to SQL queries can help, but it will not make your application secure from SQL injection attacks.

Another solution commonly proposed for dealing with SQL injection attacks is to use stored procedures. Although stored procedures prevent some types of SQL injection attacks, they do not protect against many others. For example, the following PL/SQL procedure is vulnerable to the same SQL injection attack shown in the first example.

*Example (Bad, SQL):*

```sql
procedure get_item ( itm_cv IN OUT ItmCurTyp, usr in varchar2, itm in varchar2)
is open itm_cv for
' SELECT * FROM items WHERE ' || 'owner = '|| usr || ' AND itemname = ' || itm || ';
end get_item;
```

Stored procedures typically help prevent SQL injection attacks by limiting the types of statements that can be passed to their parameters. However, there are many ways around the limitations and many interesting statements that can still be passed to stored procedures. Again, stored procedures can prevent some exploits, but they will not make your application secure against SQL injection attacks.

### Example 4

MS SQL has a built-in function that enables shell command execution. An SQL injection in such a context could be disastrous. For example, a query of the form:

*Example (Bad, SQL):*

```sql
SELECT ITEM,PRICE FROM PRODUCT WHERE ITEM_CATEGORY='$user_input' ORDER BY PRICE
```

Where $user_input is taken from an untrusted source.

If the user provides the string:

*Example (Attack):*

```
'; exec master..xp_cmdshell 'dir' --
```

The query will take the following form:

*Example (Attack):*

```
SELECT ITEM,PRICE FROM PRODUCT WHERE ITEM_CATEGORY=''; exec master..xp_cmdshell 'dir' --' ORDER BY PRICE
```

Now, this query can be broken down into:

1. a first SQL query: SELECT ITEM,PRICE FROM PRODUCT WHERE ITEM_CATEGORY='';
2. a second SQL query, which executes the dir command in the shell: exec master..xp_cmdshell 'dir'
3. an MS SQL comment: --' ORDER BY PRICE

As can be seen, the malicious input changes the semantics of the query into a query, a shell command execution and a comment.

### Example 5

This code intends to print a message summary given the message ID.

*Example (Bad, PHP):*

```php
$id = $_COOKIE["mid"];
mysql_query("SELECT MessageID, Subject FROM messages WHERE MessageID = '$id'");
```

The programmer may have skipped any input validation on $id under the assumption that attackers cannot modify the cookie. However, this is easy to do with custom client code or even in the web browser.

While $id is wrapped in single quotes in the call to mysql_query(), an attacker could simply change the incoming mid cookie to:

*Example (Attack):*

```
1432' or '1' = '1
```

This would produce the resulting query:

*Example (Result):*

```
SELECT MessageID, Subject FROM messages WHERE MessageID = '1432' or '1' = '1'
```

Not only will this retrieve message number 1432, it will retrieve all other messages.

In this case, the programmer could apply a simple modification to the code to eliminate the SQL injection:

*Example (Good, PHP):*

```php
$id = intval($_COOKIE["mid"]);
mysql_query("SELECT MessageID, Subject FROM messages WHERE MessageID = '$id'");
```

However, if this code is intended to support multiple users with different message boxes, the code might also need an access control check (CWE-285) to ensure that the application user has the permission to see that message.

### Example 6

This example attempts to take a last name provided by a user and enter it into a database.

*Example (Bad, Perl):*

```perl
$userKey = getUserID();
$name = getUserInput();

# ensure only letters, hyphens and apostrophe are allowed
$name = allowList($name, "^a-zA-z'-$");
$query = "INSERT INTO last_names VALUES('$userKey', '$name')";
```

While the programmer applies an allowlist to the user input, it has shortcomings. First of all, the user is still allowed to provide hyphens, which are used as comment structures in SQL. If a user specifies "--" then the remainder of the statement will be treated as a comment, which may bypass security logic. Furthermore, the allowlist permits the apostrophe, which is also a data / command separator in SQL. If a user supplies a name with an apostrophe, they may be able to alter the structure of the whole statement and even change control flow of the program, possibly accessing or modifying confidential information. In this situation, both the hyphen and apostrophe are legitimate characters for a last name and permitting them is required. Instead, a programmer may want to use a prepared statement or apply an encoding routine to the input to prevent any data / directive misinterpretations.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2024-6847](https://www.cve.org/CVERecord?id=CVE-2024-6847) | SQL injection in AI chatbot via a conversation message |
| [CVE-2025-26794](https://www.cve.org/CVERecord?id=CVE-2025-26794) | SQL injection in e-mail agent through SQLite integration |
| [CVE-2023-32530](https://www.cve.org/CVERecord?id=CVE-2023-32530) | SQL injection in security product dashboard using crafted certificate fields |
| [CVE-2021-42258](https://www.cve.org/CVERecord?id=CVE-2021-42258) | SQL injection in time and billing software, as exploited in the wild per CISA KEV. |
| [CVE-2021-27101](https://www.cve.org/CVERecord?id=CVE-2021-27101) | SQL injection in file-transfer system via a crafted Host header, as exploited in the wild per CISA KEV. |
| [CVE-2020-12271](https://www.cve.org/CVERecord?id=CVE-2020-12271) | SQL injection in firewall product's admin interface or user portal, as exploited in the wild per CISA KEV. |
| [CVE-2019-3792](https://www.cve.org/CVERecord?id=CVE-2019-3792) | An automation system written in Go contains an API that is vulnerable to SQL injection allowing the attacker to read privileged data. |
| [CVE-2004-0366](https://www.cve.org/CVERecord?id=CVE-2004-0366) | Chain: SQL injection in library intended for database authentication allows SQL injection and authentication bypass. |
| [CVE-2008-2790](https://www.cve.org/CVERecord?id=CVE-2008-2790) | SQL injection through an ID that was supposed to be numeric. |
| [CVE-2008-2223](https://www.cve.org/CVERecord?id=CVE-2008-2223) | SQL injection through an ID that was supposed to be numeric. |
| [CVE-2007-6602](https://www.cve.org/CVERecord?id=CVE-2007-6602) | SQL injection via user name. |
| [CVE-2008-5817](https://www.cve.org/CVERecord?id=CVE-2008-5817) | SQL injection via user name or password fields. |
| [CVE-2003-0377](https://www.cve.org/CVERecord?id=CVE-2003-0377) | SQL injection in security product, using a crafted group name. |
| [CVE-2008-2380](https://www.cve.org/CVERecord?id=CVE-2008-2380) | SQL injection in authentication library. |
| [CVE-2017-11508](https://www.cve.org/CVERecord?id=CVE-2017-11508) | SQL injection in vulnerability management and reporting tool, using a crafted password. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| PLOVER |  | SQL injection |  |
| 7 Pernicious Kingdoms |  | SQL Injection |  |
| CLASP |  | SQL injection |  |
| OWASP Top Ten 2007 | A2 | Injection Flaws | CWE More Specific |
| OWASP Top Ten 2004 | A1 | Unvalidated Input | CWE More Specific |
| OWASP Top Ten 2004 | A6 | Injection Flaws | CWE More Specific |
| WASC | 19 | SQL Injection |  |
| Software Fault Patterns | SFP24 | Tainted input to command |  |
| OMG ASCSM | ASCSM-CWE-89 |  |  |
| SEI CERT Oracle Coding Standard for Java | IDS00-J | Prevent SQL injection | Exact |
| OpenSSF Secure Coding Guide for Python | pyscg-0010 | Prevent SQL Injection |  |
| OWASP Golang Secure Coding Practices Guide |  | Database Security |  |

## Related Attack Patterns

- [CAPEC-108](https://capec.mitre.org/data/definitions/108.html)
- [CAPEC-109](https://capec.mitre.org/data/definitions/109.html)
- [CAPEC-110](https://capec.mitre.org/data/definitions/110.html)
- [CAPEC-470](https://capec.mitre.org/data/definitions/470.html)
- [CAPEC-66](https://capec.mitre.org/data/definitions/66.html)
- [CAPEC-7](https://capec.mitre.org/data/definitions/7.html)

## References

- [REF-1460] rain.forest.puppy. "NT Web Technology Vulnerabilities". Phrack Issue 54, Volume 8. 1998-12-25. <https://phrack.org/issues/54/8> (URL validated: 2025-07-24).
- [REF-44] Michael Howard, David LeBlanc and John Viega. "24 Deadly Sins of Software Security". "Sin 1: SQL Injection." Page 3. McGraw-Hill. 2010.
- [REF-7] Michael Howard and David LeBlanc. "Writing Secure Code". Chapter 12, "Database Input Issues" Page 397. 2nd Edition. Microsoft Press. 2002-12-04. <https://www.microsoftpressstore.com/store/writing-secure-code-9780735617223>.
- [REF-867] OWASP. "SQL Injection Prevention Cheat Sheet". <https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html> (URL validated: 2025-08-04).
- [REF-868] Steven Friedl. "SQL Injection Attacks by Example". 2007-10-10. <http://www.unixwiz.net/techtips/sql-injection.html>.
- [REF-869] Ferruh Mavituna. "SQL Injection Cheat Sheet". 2007-03-15. <https://web.archive.org/web/20080126180244/http://ferruh.mavituna.com/sql-injection-cheatsheet-oku/> (URL validated: 2023-04-07).
- [REF-870] David Litchfield, Chris Anley, John Heasman and Bill Grindlay. "The Database Hacker's Handbook: Defending Database Servers". Wiley. 2005-07-14.
- [REF-871] David Litchfield. "The Oracle Hacker's Handbook: Hacking and Defending Oracle". Wiley. 2007-01-30.
- [REF-872] Microsoft. "SQL Injection". 2008-12. <https://learn.microsoft.com/en-us/previous-versions/sql/sql-server-2008-r2/ms161953(v=sql.105)?redirectedfrom=MSDN> (URL validated: 2023-04-07).
- [REF-873] Microsoft Security Vulnerability Research & Defense. "SQL Injection Attack". <https://msrc.microsoft.com/blog/2008/05/sql-injection-attack/> (URL validated: 2023-04-07).
- [REF-874] Michael Howard. "Giving SQL Injection the Respect it Deserves". 2008-05-15. <https://learn.microsoft.com/en-us/archive/blogs/michael_howard/giving-sql-injection-the-respect-it-deserves> (URL validated: 2023-04-07).
- [REF-875] Frank Kim. "Top 25 Series - Rank 2 - SQL Injection". SANS Software Security Institute. 2010-03-01. <https://www.sans.org/blog/top-25-series-rank-2-sql-injection/> (URL validated: 2023-04-07).
- [REF-76] Sean Barnum and Michael Gegick. "Least Privilege". 2005-09-14. <https://web.archive.org/web/20211209014121/https://www.cisa.gov/uscert/bsi/articles/knowledge/principles/least-privilege> (URL validated: 2023-04-07).
- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 8, "SQL Queries", Page 431. 1st Edition. Addison Wesley. 2006.
- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 17, "SQL Injection", Page 1061. 1st Edition. Addison Wesley. 2006.
- [REF-962] Object Management Group (OMG). "Automated Source Code Security Measure (ASCSM)". ASCSM-CWE-89. 2016-01. <http://www.omg.org/spec/ASCSM/1.0/>.
- [REF-1447] Cybersecurity and Infrastructure Security Agency. "Secure by Design Alert: Eliminating SQL Injection Vulnerabilities in Software". 2024-03-25. <https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-sql-injection-vulnerabilities-software> (URL validated: 2024-07-14).
- [REF-1479] Gregory Larsen, E. Kenneth Hong Fong, David A. Wheeler and Rama S. Moorthy. "State-of-the-Art Resources (SOAR) for Software Vulnerability Detection, Test, and Evaluation". 2014-07. <https://www.ida.org/-/media/feature/publications/s/st/stateoftheart-resources-soar-for-software-vulnerability-detection-test-and-evaluation/p-5061.ashx> (URL validated: 2025-09-05).
- [REF-1481] D3FEND. "D3FEND: Application Layer Firewall". <https://d3fend.mitre.org/dao/artifact/d3f:ApplicationLayerFirewall/> (URL validated: 2025-09-06).
- [REF-1566] OWASP. "Golang Secure Coding Practices guide". Database Security, page 65. 2024. <https://github.com/OWASP/Go-SCP> (URL validated: 2026-10-19).
- [REF-1482] D3FEND. "D3FEND: D3-TL Trusted Library". <https://d3fend.mitre.org/technique/d3f:TrustedLibrary/> (URL validated: 2025-09-06).
- [REF-1534] OMG. "Automated Technical Debt Measure, Version 2". 2024-08. <https://www.omg.org/spec/ATDM2/1.0/PDF> (URL validated: 2026-07-16).
- [REF-1541] OpenSSF. "Secure Coding Guide for Python". 04 Neutralization. <https://best.openssf.org/Secure-Coding-Guide-for-Python/> (URL validated: 2026-10-06). Rationale: Secure-Development-Rules.

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Relationship**: SQL injection can be resultant from special character mismanagement, MAID, or denylist/allowlist problems. It can be primary to authentication errors.

- **Theoretical**:

  This entry has the following dimensions:

  - Behavior-Property: "Improper"
  - Behavior-Type: "Neutralization"
  - Input-Type: "Special Elements"
  - Behavior-Type: "Used"
  - Language-Type: "SQL"
  - Other: "Command"

---
Generated from MITRE's CWE 4.21 XML (cwec_v4.21.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.21/LICENSE.txt).
