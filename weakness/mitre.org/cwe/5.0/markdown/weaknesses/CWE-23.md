---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-23"
cwe_id: "CWE-23"
entry_type: weakness
name: "Relative Path Traversal"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/23.html"
---

# CWE-23: Relative Path Traversal

## Description

The product uses external input to construct a pathname that should be within a restricted directory, but it does not properly neutralize sequences such as ".." that can resolve to a location that is outside of that directory.

![Diagram for CWE-23](https://cwe.mitre.org/data/images/CWE-23-Diagram.png)

## Alternate Terms

- **Zip Slip**: "Zip slip" is an attack that uses file archives (e.g., ZIP, tar, rar, etc.) that contain filenames with path traversal sequences that cause the files to be written outside of the directory under which the archive is expected to be extracted [REF-1282]. It is most commonly used for relative path traversal (CWE-23) and link following (CWE-59).

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-22](../weaknesses/CWE-22.md) Improper Limitation of a Pathname to a Restricted Directory (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-22](../weaknesses/CWE-22.md) Improper Limitation of a Pathname to a Restricted Directory (Base) | [CWE-1305](../views/CWE-1305.md) | Primary |
| ChildOf | [CWE-22](../weaknesses/CWE-22.md) Improper Limitation of a Pathname to a Restricted Directory (Base) | [CWE-1340](../views/CWE-1340.md) | Primary |

## Weakness Ordinalities

- **Primary**
- **Resultant**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Not Language-Specific | Undetermined |
| Technology |  | Not Technology-Specific | Undetermined |
| Technology |  | Web Based | Often |
| Technology | AI/ML |  | Often |

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Integrity<br>Confidentiality<br>Availability | Execute Unauthorized Code or Commands | The attacker may be able to create or overwrite critical files that are used to execute code, such as programs or libraries. |
| Integrity | Modify Files or Directories | The attacker may be able to overwrite or create critical files, such as programs, libraries, or important data. If the targeted file is used for a security mechanism, then the attacker may be able to bypass that mechanism. For example, appending a new account at the end of a password file may allow an attacker to bypass authentication. |
| Confidentiality | Read Files or Directories | The attacker may be able to read the contents of unexpected files and expose sensitive data by traversing the file system to access files or directories that are outside of the restricted directory. If the targeted file is used for a security mechanism, then the attacker may be able to bypass that mechanism. For example, by reading a password file, the attacker could conduct brute force password guessing attacks in order to break into an account on the system. |
| Availability | DoS: Crash, Exit, or Restart | The attacker may be able to overwrite, delete, or corrupt unexpected critical files such as programs, libraries, or important data. This may prevent the product from working at all and in the case of a protection mechanism such as authentication, it has the potential to lockout every user of the product. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5.1

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

  When validating filenames, use stringent allowlists that limit the character set to be used. If feasible, only allow a single "." character in the filename to avoid weaknesses such as CWE-23, and exclude directory separators such as "/" to avoid CWE-36. Use a list of allowable file extensions, which will help to avoid CWE-434.

  Do not rely exclusively on a filtering mechanism that removes potentially dangerous characters. This is equivalent to a denylist, which may be incomplete (CWE-184). For example, filtering "/" is insufficient protection if the filesystem also supports the use of "\\" as a directory separator. Another possible error could occur when the filtering is applied in a way that still produces dangerous data (CWE-182). For example, if "../" sequences are removed from the ".../...//" string in a sequential fashion, two instances of "../" would be removed from the original string, but the remaining characters would still form the "../" string.

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-20.1

  Inputs should be decoded and canonicalized to the application's current internal representation before being validated (CWE-180). Make sure that the application does not decode the same input twice (CWE-174). Such errors could be used to bypass allowlist validation schemes by introducing dangerous inputs after they have been checked.

  Use a built-in path canonicalization function (such as realpath() in C) that produces the canonical version of the pathname, which effectively removes ".." sequences and symbolic links (CWE-23, CWE-59). This includes:

  - realpath() in C
  - getCanonicalPath() in Java
  - GetFullPath() in ASP.NET
  - realpath() or abs_path() in Perl
  - realpath() in PHP

- **Phase:** Operation · **Strategy:** Firewall · **ID:** MIT-29

  Use an application firewall that can detect attacks against this weakness. It can be beneficial in cases in which the code cannot be fixed (because it is controlled by a third party), as an emergency prevention measure while more comprehensive software assurance measures are applied, or to provide defense in depth [REF-1481].

  **Effectiveness:** Moderate

  **Effectiveness Notes:** An application firewall might not cover all possible input vectors. In addition, attack techniques might be available to bypass the protection mechanism, such as using malformed inputs that can still be processed by the component that receives those inputs. Depending on functionality, an application firewall might inadvertently reject or modify legitimate requests. Finally, some manual effort may be required for customization.

## Demonstrative Examples

### Example 1

The following URLs are vulnerable to this attack:

*Example (Bad, Other):*

```other
http://example.com/get-files.jsp?file=report.pdf
http://example.com/get-page.php?home=aaa.html
http://example.com/some-page.asp?page=index.html
```

A simple way to execute this attack is like this:

*Example (Attack, Other):*

```other
http://example.com/get-files?file=../../../../somedir/somefile
http://example.com/../../../../etc/shadow
http://example.com/get-files?file=../../../../etc/passwd
```

### Example 2 (DX-27)

The following code could be for a social networking application in which each user's profile information is stored in a separate file. All files are stored in a single directory.

*Example (Bad, Perl):*

```perl
my $dataPath = "/users/cwe/profiles";
my $username = param("user");
my $profilePath = $dataPath . "/" . $username;

open(my $fh, "<", $profilePath) || ExitError("profile read error: $profilePath");
print "<ul>\n";
while (<$fh>) {
    print "<li>$_</li>\n";
}
print "</ul>\n";
```

While the programmer intends to access files such as "/users/cwe/profiles/alice" or "/users/cwe/profiles/bob", there is no verification of the incoming user parameter. An attacker could provide a string such as:

*Example (Attack):*

```
../../../etc/passwd
```

The program would generate a profile pathname like this:

*Example (Result):*

```
/users/cwe/profiles/../../../etc/passwd
```

When the file is opened, the operating system resolves the "../" during path canonicalization and actually accesses this file:

*Example (Result):*

```
/etc/passwd
```

As a result, the attacker could read the entire text of the password file.

Notice how this code also contains an error message information leak (CWE-209) if the user parameter does not produce a file that exists: the full pathname is provided. Because of the lack of output encoding of the file that is retrieved, there might also be a cross-site scripting problem (CWE-79) if profile contains any HTML, but other code would need to be examined.

### Example 3 (DX-22)

The following code demonstrates the unrestricted upload of a file with a Java servlet and a path traversal vulnerability. The action attribute of an HTML form is sending the upload file request to the Java servlet.

*Example (Good, HTML):*

```html
<form action="FileUploadServlet" method="post" enctype="multipart/form-data">

Choose a file to upload:
<input type="file" name="filename"/>
<br/>
<input type="submit" name="submit" value="Submit"/>

</form>
```

When submitted the Java servlet's doPost method will receive the request, extract the name of the file from the Http request header, read the file contents from the request and output the file to the local upload directory.

*Example (Bad, Java):*

```java
public class FileUploadServlet extends HttpServlet {
    ...

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        String contentType = request.getContentType();

        // the starting position of the boundary header
        int ind = contentType.indexOf("boundary=");
        String boundary = contentType.substring(ind+9);

        String pLine = new String();
        String uploadLocation = new String(UPLOAD_DIRECTORY_STRING); //Constant value

        // verify that content type is multipart form data
        if (contentType != null && contentType.indexOf("multipart/form-data") != -1) {
            // extract the filename from the Http header
            BufferedReader br = new BufferedReader(new InputStreamReader(request.getInputStream()));
            ...
            pLine = br.readLine();
            String filename = pLine.substring(pLine.lastIndexOf("\\"), pLine.lastIndexOf("\""));
            ...

            // output the file to the local upload directory
            try {
                BufferedWriter bw = new BufferedWriter(new FileWriter(uploadLocation+filename, true));
                for (String line; (line=br.readLine())!=null; ) {
                    if (line.indexOf(boundary) == -1) {
                        bw.write(line);
                        bw.newLine();
                        bw.flush();
                    }
                } //end of for loop
                bw.close();
            } catch (IOException ex) {...}
            // output successful upload response HTML page
        }
        // output unsuccessful upload response HTML page
        else
        {...}
    }
        ...
}
```

This code does not perform a check on the type of the file being uploaded (CWE-434). This could allow an attacker to upload any executable file or other file with malicious code.

Additionally, the creation of the BufferedWriter object is subject to relative path traversal (CWE-23). Since the code does not check the filename that is provided in the header, an attacker can use "../" sequences to write to files outside of the intended directory. Depending on the executing environment, the attacker may be able to specify arbitrary files to write to, leading to a wide variety of consequences, from code execution, XSS (CWE-79), or system crash.

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2024-37032](https://www.cve.org/CVERecord?id=CVE-2024-37032) | Large language model (LLM) management tool does not validate the format of a digest value (CWE-1287) from a private, untrusted model registry, enabling relative path traversal (CWE-23), a.k.a. Probllama |
| [CVE-2024-0520](https://www.cve.org/CVERecord?id=CVE-2024-0520) | Product for managing datasets for AI model training and evaluation allows both relative (CWE-23) and absolute (CWE-36) path traversal to overwrite files via the Content-Disposition header |
| [CVE-2022-45918](https://www.cve.org/CVERecord?id=CVE-2022-45918) | Chain: a learning management tool debugger uses external input to locate previous session logs (CWE-73) and does not properly validate the given path (CWE-20), allowing for filesystem path traversal using "../" sequences (CWE-24) |
| [CVE-2019-20916](https://www.cve.org/CVERecord?id=CVE-2019-20916) | Python package manager does not correctly restrict the filename specified in a Content-Disposition header, allowing arbitrary file read using path traversal sequences such as "../" |
| [CVE-2022-24877](https://www.cve.org/CVERecord?id=CVE-2022-24877) | directory traversal in Go-based Kubernetes operator app allows accessing data from the controller's pod file system via ../ sequences in a yaml file |
| [CVE-2020-4053](https://www.cve.org/CVERecord?id=CVE-2020-4053) | a Kubernetes package manager written in Go allows malicious plugins to inject path traversal sequences into a plugin archive ("Zip slip") to copy a file outside the intended directory |
| [CVE-2021-21972](https://www.cve.org/CVERecord?id=CVE-2021-21972) | Chain: Cloud computing virtualization platform does not require authentication for upload of a tar format file (CWE-306), then uses .. path traversal sequences (CWE-23) in the file to access unexpected files, as exploited in the wild per CISA KEV. |
| [CVE-2019-10743](https://www.cve.org/CVERecord?id=CVE-2019-10743) | Go-based archive library allows extraction of files to locations outside of the target folder with "../" path traversal sequences in filenames in a zip file, aka "Zip Slip" |
| [CVE-2002-0298](https://www.cve.org/CVERecord?id=CVE-2002-0298) | Server allows remote attackers to cause a denial of service via certain HTTP GET requests containing a %2e%2e (encoded dot-dot), several "/../" sequences, or several "../" in a URI. |
| [CVE-2002-0661](https://www.cve.org/CVERecord?id=CVE-2002-0661) | "\\" not in denylist for web server, allowing path traversal attacks when the server is run in Windows and other OSes. |
| [CVE-2002-0946](https://www.cve.org/CVERecord?id=CVE-2002-0946) | Arbitrary files may be read files via ..\ (dot dot) sequences in an HTTP request. |
| [CVE-2002-1042](https://www.cve.org/CVERecord?id=CVE-2002-1042) | Directory traversal vulnerability in search engine for web server allows remote attackers to read arbitrary files via "..\\" sequences in queries. |
| [CVE-2002-1209](https://www.cve.org/CVERecord?id=CVE-2002-1209) | Directory traversal vulnerability in FTP server allows remote attackers to read arbitrary files via "..\\" sequences in a GET request. |
| [CVE-2002-1178](https://www.cve.org/CVERecord?id=CVE-2002-1178) | Directory traversal vulnerability in servlet allows remote attackers to execute arbitrary commands via "..\\" sequences in an HTTP request. |
| [CVE-2002-1987](https://www.cve.org/CVERecord?id=CVE-2002-1987) | Protection mechanism checks for "/.." but doesn't account for Windows-specific "\\.." allowing read of arbitrary files. |
| [CVE-2005-2142](https://www.cve.org/CVERecord?id=CVE-2005-2142) | Directory traversal vulnerability in FTP server allows remote authenticated attackers to list arbitrary directories via a "\\.." sequence in an LS command. |
| [CVE-2002-0160](https://www.cve.org/CVERecord?id=CVE-2002-0160) | The administration function in Access Control Server allows remote attackers to read HTML, Java class, and image files outside the web root via a "..\\.." sequence in the URL to port 2002. |
| [CVE-2001-0467](https://www.cve.org/CVERecord?id=CVE-2001-0467) | "\\..." in web server |
| [CVE-2001-0963](https://www.cve.org/CVERecord?id=CVE-2001-0963) | "..." in cd command in FTP server |
| [CVE-2001-1193](https://www.cve.org/CVERecord?id=CVE-2001-1193) | "..." in cd command in FTP server |
| [CVE-2001-1131](https://www.cve.org/CVERecord?id=CVE-2001-1131) | "..." in cd command in FTP server |
| [CVE-2001-0480](https://www.cve.org/CVERecord?id=CVE-2001-0480) | read of arbitrary files and directories using GET or CD with "..." in Windows-based FTP server. |
| [CVE-2002-0288](https://www.cve.org/CVERecord?id=CVE-2002-0288) | read files using "." and Unicode-encoded "/" or "\\" characters in the URL. |
| [CVE-2003-0313](https://www.cve.org/CVERecord?id=CVE-2003-0313) | Directory listing of web server using "..." |
| [CVE-2005-1658](https://www.cve.org/CVERecord?id=CVE-2005-1658) | Triple dot |
| [CVE-2000-0240](https://www.cve.org/CVERecord?id=CVE-2000-0240) | read files via "/........../" in URL |
| [CVE-2000-0773](https://www.cve.org/CVERecord?id=CVE-2000-0773) | read files via "...." in web server |
| [CVE-1999-1082](https://www.cve.org/CVERecord?id=CVE-1999-1082) | read files via "......" in web server (doubled triple dot?) |
| [CVE-2004-2121](https://www.cve.org/CVERecord?id=CVE-2004-2121) | read files via "......" in web server (doubled triple dot?) |
| [CVE-2001-0491](https://www.cve.org/CVERecord?id=CVE-2001-0491) | multiple attacks using "..", "...", and "...." in different commands |
| [CVE-2001-0615](https://www.cve.org/CVERecord?id=CVE-2001-0615) | "..." or "...." in chat server |
| [CVE-2005-2169](https://www.cve.org/CVERecord?id=CVE-2005-2169) | Chain: ".../...//" bypasses protection mechanism using regexp's that remove "../" resulting in collapse into an unsafe value "../" (CWE-182) and resultant path traversal. |
| [CVE-2005-0202](https://www.cve.org/CVERecord?id=CVE-2005-0202) | ".../....///" bypasses regexp's that remove "./" and "../" |
| [CVE-2004-1670](https://www.cve.org/CVERecord?id=CVE-2004-1670) | Mail server allows remote attackers to create arbitrary directories via a ".." or rename arbitrary files via a "....//" in user supplied parameters. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | Relative Path Traversal |
| Software Fault Patterns | SFP16 | Path Traversal |

## Related Attack Patterns

- [CAPEC-139](https://capec.mitre.org/data/definitions/139.html)
- [CAPEC-76](https://capec.mitre.org/data/definitions/76.html)

## References

- [REF-192] OWASP. "OWASP Attack listing". <http://www.owasp.org/index.php/Relative_Path_Traversal>.
- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 9, "Filenames and Paths", Page 503. 1st Edition. Addison Wesley. 2006.
- [REF-1282] Snyk. "Zip Slip Vulnerability". 2018-06-05. <https://security.snyk.io/research/zip-slip-vulnerability>.
- [REF-1448] Cybersecurity and Infrastructure Security Agency. "Secure by Design Alert: Eliminating Directory Traversal Vulnerabilities in Software". 2024-05-02. <https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-directory-traversal-vulnerabilities-software> (URL validated: 2024-07-14).
- [REF-1481] D3FEND. "D3FEND: Application Layer Firewall". <https://d3fend.mitre.org/dao/artifact/d3f:ApplicationLayerFirewall/> (URL validated: 2025-09-06).
- [REF-1534] OMG. "Automated Technical Debt Measure, Version 2". 2024-08. <https://www.omg.org/spec/ATDM2/1.0/PDF> (URL validated: 2026-07-16).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Contribution (Feedback) | 2022-07-11 | Nick Johnston |  | CWE 4.9, 2022-10-13 | Identified weakness in Perl demonstrative example |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated References, Demonstrative_Example, Potential_Mitigations, Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Relationships, References, Taxonomy_Mappings |
| Modification | 2008-10-14 | CWE Content Team | MITRE | CWE 1.0.1, 2008-10-14 | updated Description |
| Modification | 2009-07-27 | CWE Content Team | MITRE | CWE 1.5, 2009-07-27 | updated Potential_Mitigations |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 | updated Demonstrative_Examples |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Description, Potential_Mitigations |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Potential_Mitigations |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Common_Consequences, Demonstrative_Examples, Observed_Examples, References, Relationships |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-01-19 | CWE Content Team | MITRE | CWE 2.10, 2017-01-19 | updated Related_Attack_Patterns |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Applicable_Platforms |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Related_Attack_Patterns |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Potential_Mitigations, Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Observed_Examples, Potential_Mitigations |
| Modification | 2020-08-20 | CWE Content Team | MITRE | CWE 4.2, 2020-08-20 | updated Relationships |
| Modification | 2020-12-10 | CWE Content Team | MITRE | CWE 4.3, 2020-12-10 | updated Relationships |
| Modification | 2021-03-15 | CWE Content Team | MITRE | CWE 4.4, 2021-03-15 | updated Demonstrative_Examples |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 | updated Relationships |
| Modification | 2022-06-28 | CWE Content Team | MITRE | CWE 4.8, 2022-06-28 | updated Observed_Examples |
| Modification | 2022-10-13 | CWE Content Team | MITRE | CWE 4.9, 2022-10-13 | updated Alternate_Terms, Observed_Examples, References |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Common_Consequences, Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Detection_Factors, Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes |
| Modification | 2023-10-26 | CWE Content Team | MITRE | CWE 4.13, 2023-10-26 | updated Observed_Examples |
| Modification | 2024-07-16 | CWE Content Team | MITRE | CWE 4.15, 2024-07-16 | updated Observed_Examples, References |
| Modification | 2025-04-03 | CWE Content Team | MITRE | CWE 4.17, 2025-04-03 | updated Demonstrative_Examples |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Affected_Resources, Applicable_Platforms, Common_Consequences, Description, Diagram, Functional_Areas, Observed_Examples, Potential_Mitigations, References |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Applicable_Platforms, Relationships, Weakness_Ordinalities |
| Modification | 2026-04-30 | CWE Content Team | MITRE | CWE 4.20, 2026-04-30 | updated Applicable_Platforms |
| Modification | 2026-10-28 | CWE Content Team | MITRE | CWE 5.0, 2026-10-28 | updated Common_Consequences, References |

---
Generated from MITRE's CWE 5.0 XML (cwec_v5.0.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/5.0/LICENSE.txt).
