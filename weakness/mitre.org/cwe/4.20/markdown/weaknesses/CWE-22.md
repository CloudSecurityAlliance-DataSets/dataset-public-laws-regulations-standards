---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-22"
cwe_id: "CWE-22"
entry_type: weakness
name: "Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')"
abstraction: Base
structure: Simple
status: Stable
mapping_usage: Allowed-with-Review
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/22.html"
---

# CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')

## Description

The product uses external input to construct a pathname that is intended to identify a file or directory that is located underneath a restricted parent directory, but the product does not properly neutralize special elements within the pathname that can cause the pathname to resolve to a location that is outside of the restricted directory.

![Diagram for CWE-22](https://cwe.mitre.org/data/images/CWE-22-Diagram.png)

## Extended Description

Many file operations are intended to take place within a restricted directory. By using special elements such as ".." and "/" separators, attackers can escape outside of the restricted location to access files or directories that are elsewhere on the system. One of the most common special elements is the "../" sequence, which in most modern operating systems is interpreted as the parent directory of the current location. This is referred to as relative path traversal. Path traversal also covers the use of absolute pathnames such as "/usr/local/bin" to access unexpected files. This is referred to as absolute path traversal.

## Alternate Terms

- **Path traversal**: "Path traversal" is preferred over "directory traversal," but both terms are attack-focused.
- **Directory traversal**
- **Path transversal**: an alternate phrasing of "path traversal"

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-706](../weaknesses/CWE-706.md) Use of Incorrectly-Resolved Name or Reference (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-706](../weaknesses/CWE-706.md) Use of Incorrectly-Resolved Name or Reference (Class) | [CWE-1003](../views/CWE-1003.md) | Primary |
| CanPrecede | [CWE-668](../weaknesses/CWE-668.md) Exposure of Resource to Wrong Sphere (Class) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Primary**
- **Resultant**

## Applicable Platforms

| Type | Name | Class | Prevalence |
| --- | --- | --- | --- |
| Language |  | Not Language-Specific | Undetermined |
| Technology | AI/ML |  | Often |

## Modes Of Introduction

- **Implementation**

## Likelihood Of Exploit

High

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Integrity<br>Confidentiality<br>Availability | Execute Unauthorized Code or Commands | The attacker may be able to create or overwrite critical files that are used to execute code, such as programs or libraries. |
| Integrity | Modify Files or Directories | The attacker may be able to overwrite or create critical files, such as programs, libraries, or important data. If the targeted file is used for a security mechanism, then the attacker may be able to bypass that mechanism. For example, appending a new account at the end of a password file may allow an attacker to bypass authentication. |
| Confidentiality | Read Files or Directories | The attacker may be able read the contents of unexpected files and expose sensitive data. If the targeted file is used for a security mechanism, then the attacker may be able to bypass that mechanism. For example, by reading a password file, the attacker could conduct brute force password guessing attacks in order to break into an account on the system. |
| Availability | DoS: Crash, Exit, or Restart | The attacker may be able to overwrite, delete, or corrupt unexpected critical files such as programs, libraries, or important data. This may prevent the product from working at all and in the case of protection mechanisms such as authentication, it has the potential to lock out product users. |

## Detection Methods

- **Method:** Automated Static Analysis

  Automated techniques can find areas where path traversal weaknesses exist. However, tuning or customization may be required to remove or de-prioritize path-traversal problems that are only exploitable by the product's administrator - or other privileged users - and thus potentially valid behavior or, at worst, a bug instead of a vulnerability.

  **Effectiveness:** High

- **Method:** Manual Static Analysis

  Manual white box techniques may be able to provide sufficient code coverage and reduction of false positives if all file access operations can be assessed within limited time constraints.

  **Effectiveness:** High

- **Method:** Automated Static Analysis - Binary or Bytecode

  According to SOAR [REF-1479], the following detection techniques may be useful:

  Highly cost effective:

  - Bytecode Weakness Analysis - including disassembler + source code weakness analysis

  Cost effective for partial coverage:

  - Binary Weakness Analysis - including disassembler + source code weakness analysis

  **Effectiveness:** High

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

  **Effectiveness:** High

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

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5.1

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

  When validating filenames, use stringent allowlists that limit the character set to be used. If feasible, only allow a single "." character in the filename to avoid weaknesses such as CWE-23, and exclude directory separators such as "/" to avoid CWE-36. Use a list of allowable file extensions, which will help to avoid CWE-434.

  Do not rely exclusively on a filtering mechanism that removes potentially dangerous characters. This is equivalent to a denylist, which may be incomplete (CWE-184). For example, filtering "/" is insufficient protection if the filesystem also supports the use of "\\" as a directory separator. Another possible error could occur when the filtering is applied in a way that still produces dangerous data (CWE-182). For example, if "../" sequences are removed from the ".../...//" string in a sequential fashion, two instances of "../" would be removed from the original string, but the remaining characters would still form the "../" string.

- **Phase:** Architecture and Design · **ID:** MIT-15

  For any security checks that are performed on the client side, ensure that these checks are duplicated on the server side, in order to avoid CWE-602. Attackers can bypass the client-side checks by modifying values after the checks have been performed, or by changing the client to remove the client-side checks entirely. Then, these modified values would be submitted to the server.

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-20.1

  Inputs should be decoded and canonicalized to the application's current internal representation before being validated (CWE-180). Make sure that the application does not decode the same input twice (CWE-174). Such errors could be used to bypass allowlist validation schemes by introducing dangerous inputs after they have been checked.

  Use a built-in path canonicalization function (such as realpath() in C) that produces the canonical version of the pathname, which effectively removes ".." sequences and symbolic links (CWE-23, CWE-59). This includes:

  - realpath() in C
  - getCanonicalPath() in Java
  - GetFullPath() in ASP.NET
  - realpath() or abs_path() in Perl
  - realpath() in PHP

- **Phase:** Architecture and Design · **Strategy:** Libraries or Frameworks · **ID:** MIT-4

  Use a vetted library or framework that does not allow this weakness to occur or provides constructs that make this weakness easier to avoid [REF-1482].

- **Phase:** Operation · **Strategy:** Firewall · **ID:** MIT-29

  Use an application firewall that can detect attacks against this weakness. It can be beneficial in cases in which the code cannot be fixed (because it is controlled by a third party), as an emergency prevention measure while more comprehensive software assurance measures are applied, or to provide defense in depth [REF-1481].

  **Effectiveness:** Moderate

  **Effectiveness Notes:** An application firewall might not cover all possible input vectors. In addition, attack techniques might be available to bypass the protection mechanism, such as using malformed inputs that can still be processed by the component that receives those inputs. Depending on functionality, an application firewall might inadvertently reject or modify legitimate requests. Finally, some manual effort may be required for customization.

- **Phase:** Architecture and Design; Operation · **Strategy:** Environment Hardening · **ID:** MIT-17

  Run your code using the lowest privileges that are required to accomplish the necessary tasks [REF-76]. If possible, create isolated accounts with limited privileges that are only used for a single task. That way, a successful attack will not immediately give the attacker access to the rest of the software or its environment. For example, database applications rarely need to run as the database administrator, especially in day-to-day operations.

- **Phase:** Architecture and Design · **Strategy:** Enforcement by Conversion · **ID:** MIT-21.1

  When the set of acceptable objects, such as filenames or URLs, is limited or known, create a mapping from a set of fixed input values (such as numeric IDs) to the actual filenames or URLs, and reject all other inputs.

  For example, ID 1 could map to "inbox.txt" and ID 2 could map to "profile.txt". Features such as the ESAPI AccessReferenceMap [REF-185] provide this capability.

- **Phase:** Architecture and Design; Operation · **Strategy:** Sandbox or Jail · **ID:** MIT-22

  Run the code in a "jail" or similar sandbox environment that enforces strict boundaries between the process and the operating system. This may effectively restrict which files can be accessed in a particular directory or which commands can be executed by the software.

  OS-level examples include the Unix chroot jail, AppArmor, and SELinux. In general, managed code may provide some protection. For example, java.io.FilePermission in the Java SecurityManager allows the software to specify restrictions on file operations.

  This may not be a feasible solution, and it only limits the impact to the operating system; the rest of the application may still be subject to compromise.

  Be careful to avoid CWE-243 and other weaknesses related to jails.

  **Effectiveness:** Limited

  **Effectiveness Notes:** The effectiveness of this mitigation depends on the prevention capabilities of the specific sandbox or jail being used and might only help to reduce the scope of an attack, such as restricting the attacker to certain system calls or limiting the portion of the file system that can be accessed.

- **Phase:** Architecture and Design; Operation · **Strategy:** Attack Surface Reduction · **ID:** MIT-34

  Store library, include, and utility files outside of the web document root, if possible. Otherwise, store them in a separate directory and use the web server's access control capabilities to prevent attackers from directly requesting them. One common practice is to define a fixed constant in each calling program, then check for the existence of the constant in the library/include file; if the constant does not exist, then the file was directly requested, and it can exit immediately.

  This significantly reduces the chance of an attacker being able to bypass any protection mechanisms that are in the base program but not in the include files. It will also reduce the attack surface.

- **Phase:** Implementation · **ID:** MIT-39

  Ensure that error messages only contain minimal details that are useful to the intended audience and no one else. The messages need to strike the balance between being too cryptic (which can confuse users) or being too detailed (which may reveal more than intended). The messages should not reveal the methods that were used to determine the error. Attackers can use detailed information to refine or optimize their original attack, thereby increasing their chances of success.

  If errors must be captured in some detail, record them in log messages, but consider what could occur if the log messages can be viewed by attackers. Highly sensitive information such as passwords should never be saved to log files.

  Avoid inconsistent messaging that might accidentally tip off an attacker about internal state, such as whether a user account exists or not.

  In the context of path traversal, error messages which disclose path information can help attackers craft the appropriate attack strings to move through the file system hierarchy.

- **Phase:** Operation; Implementation · **Strategy:** Environment Hardening · **ID:** MIT-16

  When using PHP, configure the application so that it does not use register_globals. During implementation, develop the application so that it does not rely on this feature, but be wary of implementing a register_globals emulation that is subject to weaknesses such as CWE-95, CWE-621, and similar issues.

## Demonstrative Examples

### Example 1 (DX-27)

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

### Example 2 (DX-18)

In the example below, the path to a dictionary file is read from a system property and used to initialize a File object.

*Example (Bad, Java):*

```java
String filename = System.getProperty("com.domain.application.dictionaryFile");
File dictionaryFile = new File(filename);
```

However, the path is not validated or modified to prevent it from containing relative or absolute path sequences before creating the File object. This allows anyone who can control the system property to determine what file is used. Ideally, the path should be resolved relative to some kind of application or user home directory.

### Example 3 (DX-2)

The following code takes untrusted input and uses a regular expression to filter "../" from the input. It then appends this result to the /home/user/ directory and attempts to read the file in the final resulting path.

*Example (Bad, Perl):*

```perl
my $Username = GetUntrustedInput();
$Username =~ s/\.\.\///;
my $filename = "/home/user/" . $Username;
ReadAndSendFile($filename);
```

Since the regular expression does not have the /g global match modifier, it only removes the first instance of "../" it comes across. So an input value such as:

*Example (Attack):*

```
../../../etc/passwd
```

will have the first "../" stripped, resulting in:

*Example (Result):*

```
../../etc/passwd
```

This value is then concatenated with the /home/user/ directory:

*Example (Result):*

```
/home/user/../../etc/passwd
```

which causes the /etc/passwd file to be retrieved once the operating system has resolved the ../ sequences in the pathname. This leads to relative path traversal (CWE-23).

### Example 4

The following code attempts to validate a given input path by checking it against an allowlist and once validated delete the given file. In this specific case, the path is considered valid if it starts with the string "/safe_dir/".

*Example (Bad, Java):*

```java
String path = getInputPath();
if (path.startsWith("/safe_dir/"))
{
    File f = new File(path);
    f.delete()
}
```

An attacker could provide an input such as this:

*Example (Attack):*

```
/safe_dir/../important.dat
```

The software assumes that the path is valid because it starts with the "/safe_path/" sequence, but the "../" sequence will cause the program to delete the important.dat file in the parent directory

### Example 5 (DX-22)

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

### Example 6 (DX-159)

This script intends to read a user-supplied file from the current directory. The user inputs the relative path to the file and the script uses Python's os.path.join() function to combine the path to the current working directory with the provided path to the specified file. This results in an absolute path to the desired file. If the file does not exist when the script attempts to read it, an error is printed to the user.

*Example (Bad, Python):*

```python
import os
import sys
def main():
    filename = sys.argv[1]
    path = os.path.join(os.getcwd(), filename)
    try:
        with open(path, 'r') as f:
            file_data = f.read()
    except FileNotFoundError as e:
        print("Error - file not found")
main()
```

However, if the user supplies an absolute path, the os.path.join() function will discard the path to the current working directory and use only the absolute path provided. For example, if the current working directory is /home/user/documents, but the user inputs /etc/passwd, os.path.join() will use only /etc/passwd, as it is considered an absolute path. In the above scenario, this would cause the script to access and read the /etc/passwd file.

*Example (Good, Python):*

```python
import os
import sys
def main():
    filename = sys.argv[1]
    path = os.path.normpath(f"{os.getcwd()}{os.sep}{filename}")
    if path.startswith("/home/cwe/documents/"):
        try:
            with open(path, 'r') as f:
                file_data = f.read()
        except FileNotFoundError as e:
            print("Error - file not found")
main()
```

The constructed path string uses os.sep to add the appropriate separation character for the given operating system (e.g. '\\' or '/') and the call to os.path.normpath() removes any additional slashes that may have been entered - this may occur particularly when using a Windows path. The path is checked against an expected directory (/home/cwe/documents); otherwise, an attacker could provide relative path sequences like ".." to cause normpath() to generate paths that are outside the intended directory (CWE-23). By putting the pieces of the path string together in this fashion, the script avoids a call to os.path.join() and any potential issues that might arise if an absolute path is entered. With this version of the script, if the current working directory is /home/cwe/documents, and the user inputs /etc/passwd, the resulting path will be /home/cwe/documents/etc/passwd. The user is therefore contained within the current working directory as intended.

### Example 7

This PHP code takes user input in a file argument, obtains its contents, and presents the contents back to the caller.

*Example (Bad, PHP):*

```php
$filename = $_GET['file']; // User-controlled input
echo file_get_contents($filename); // Read and display the file contents
```

An attacker could manipulate the file path using relative (../) or absolute paths, potentially accessing sensitive system files. For example, if an attacker provides ../../../../etc/passwd as input, the script will fetch and display the contents of the system's password file. Ideally, the file path should be validated and restricted to a specific directory to prevent unauthorized file access.

*Example (Good, PHP):*

```php
$allowed_files = [
    'readme' => 'public_files/readme.txt',
    'terms'  => 'public_files/terms.txt',
];
$key = $_GET['file'] ?? '';
if (!isset($allowed_files[$key])) {
    http_response_code(404);
    exit('File not found.');
}
$filepath = __DIR__ . '/' . $allowed_files[$key];
if (!is_file($filepath) || !is_readable($filepath)) {
    http_response_code(404);
    exit('File not found.');
}
echo htmlspecialchars(file_get_contents($filepath), ENT_QUOTES, 'UTF-8');
```

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2024-37032](https://www.cve.org/CVERecord?id=CVE-2024-37032) | Large language model (LLM) management tool does not validate the format of a digest value (CWE-1287) from a private, untrusted model registry, enabling relative path traversal (CWE-23), a.k.a. Probllama |
| [CVE-2024-4315](https://www.cve.org/CVERecord?id=CVE-2024-4315) | Chain: API for text generation using Large Language Models (LLMs) does not include the "\\" Windows folder separator in its denylist (CWE-184) when attempting to prevent Local File Inclusion via path traversal (CWE-22), allowing deletion of arbitrary files on Windows systems. |
| [CVE-2024-0520](https://www.cve.org/CVERecord?id=CVE-2024-0520) | Product for managing datasets for AI model training and evaluation allows both relative (CWE-23) and absolute (CWE-36) path traversal to overwrite files via the Content-Disposition header |
| [CVE-2022-45918](https://www.cve.org/CVERecord?id=CVE-2022-45918) | Chain: a learning management tool debugger uses external input to locate previous session logs (CWE-73) and does not properly validate the given path (CWE-20), allowing for filesystem path traversal using "../" sequences (CWE-24) |
| [CVE-2019-20916](https://www.cve.org/CVERecord?id=CVE-2019-20916) | Python package manager does not correctly restrict the filename specified in a Content-Disposition header, allowing arbitrary file read using path traversal sequences such as "../" |
| [CVE-2022-31503](https://www.cve.org/CVERecord?id=CVE-2022-31503) | Python package constructs filenames using an unsafe os.path.join call on untrusted input, allowing absolute path traversal because os.path.join resets the pathname to an absolute path that is specified as part of the input. |
| [CVE-2022-24877](https://www.cve.org/CVERecord?id=CVE-2022-24877) | directory traversal in Go-based Kubernetes operator app allows accessing data from the controller's pod file system via ../ sequences in a yaml file |
| [CVE-2021-21972](https://www.cve.org/CVERecord?id=CVE-2021-21972) | Chain: Cloud computing virtualization platform does not require authentication for upload of a tar format file (CWE-306), then uses .. path traversal sequences (CWE-23) in the file to access unexpected files, as exploited in the wild per CISA KEV. |
| [CVE-2020-4053](https://www.cve.org/CVERecord?id=CVE-2020-4053) | a Kubernetes package manager written in Go allows malicious plugins to inject path traversal sequences into a plugin archive ("Zip slip") to copy a file outside the intended directory |
| [CVE-2020-3452](https://www.cve.org/CVERecord?id=CVE-2020-3452) | Chain: security product has improper input validation (CWE-20) leading to directory traversal (CWE-22), as exploited in the wild per CISA KEV. |
| [CVE-2019-10743](https://www.cve.org/CVERecord?id=CVE-2019-10743) | Go-based archive library allows extraction of files to locations outside of the target folder with "../" path traversal sequences in filenames in a zip file, aka "Zip Slip" |
| [CVE-2010-0467](https://www.cve.org/CVERecord?id=CVE-2010-0467) | Newsletter module allows reading arbitrary files using "../" sequences. |
| [CVE-2006-7079](https://www.cve.org/CVERecord?id=CVE-2006-7079) | Chain: PHP app uses extract for register_globals compatibility layer (CWE-621), enabling path traversal (CWE-22) |
| [CVE-2009-4194](https://www.cve.org/CVERecord?id=CVE-2009-4194) | FTP server allows deletion of arbitrary files using ".." in the DELE command. |
| [CVE-2009-4053](https://www.cve.org/CVERecord?id=CVE-2009-4053) | FTP server allows creation of arbitrary directories using ".." in the MKD command. |
| [CVE-2009-0244](https://www.cve.org/CVERecord?id=CVE-2009-0244) | FTP service for a Bluetooth device allows listing of directories, and creation or reading of files using ".." sequences. |
| [CVE-2009-4013](https://www.cve.org/CVERecord?id=CVE-2009-4013) | Software package maintenance program allows overwriting arbitrary files using "../" sequences. |
| [CVE-2009-4449](https://www.cve.org/CVERecord?id=CVE-2009-4449) | Bulletin board allows attackers to determine the existence of files using the avatar. |
| [CVE-2009-4581](https://www.cve.org/CVERecord?id=CVE-2009-4581) | PHP program allows arbitrary code execution using ".." in filenames that are fed to the include() function. |
| [CVE-2010-0012](https://www.cve.org/CVERecord?id=CVE-2010-0012) | Overwrite of files using a .. in a Torrent file. |
| [CVE-2010-0013](https://www.cve.org/CVERecord?id=CVE-2010-0013) | Chat program allows overwriting files using a custom smiley request. |
| [CVE-2008-5748](https://www.cve.org/CVERecord?id=CVE-2008-5748) | Chain: external control of values for user's desired language and theme enables path traversal. |
| [CVE-2009-1936](https://www.cve.org/CVERecord?id=CVE-2009-1936) | Chain: library file sends a redirect if it is directly requested but continues to execute, allowing remote file inclusion and path traversal. |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| PLOVER |  | Path Traversal |  |
| OWASP Top Ten 2007 | A4 | Insecure Direct Object Reference | CWE More Specific |
| OWASP Top Ten 2004 | A2 | Broken Access Control | CWE More Specific |
| CERT C Secure Coding | FIO02-C | Canonicalize path names originating from untrusted sources |  |
| SEI CERT Perl Coding Standard | IDS00-PL | Canonicalize path names before validating them | Exact |
| WASC | 33 | Path Traversal |  |
| Software Fault Patterns | SFP16 | Path Traversal |  |
| OMG ASCSM | ASCSM-CWE-22 |  |  |

## Related Attack Patterns

- [CAPEC-126](https://capec.mitre.org/data/definitions/126.html)
- [CAPEC-64](https://capec.mitre.org/data/definitions/64.html)
- [CAPEC-76](https://capec.mitre.org/data/definitions/76.html)
- [CAPEC-78](https://capec.mitre.org/data/definitions/78.html)
- [CAPEC-79](https://capec.mitre.org/data/definitions/79.html)

## References

- [REF-7] Michael Howard and David LeBlanc. "Writing Secure Code". Chapter 11, "Directory Traversal and Using Parent Paths (..)" Page 370. 2nd Edition. Microsoft Press. 2002-12-04. <https://www.microsoftpressstore.com/store/writing-secure-code-9780735617223>.
- [REF-45] OWASP. "OWASP Enterprise Security API (ESAPI) Project". <https://owasp.org/www-project-enterprise-security-api/> (URL validated: 2025-07-24).
- [REF-185] OWASP. "Testing for Path Traversal (OWASP-AZ-001)". <http://www.owasp.org/index.php/Testing_for_Path_Traversal_(OWASP-AZ-001)>.
- [REF-186] Johannes Ullrich. "Top 25 Series - Rank 7 - Path Traversal". SANS Software Security Institute. 2010-03-09. <https://www.sans.org/blog/top-25-series-rank-7-path-traversal/> (URL validated: 2023-04-07).
- [REF-76] Sean Barnum and Michael Gegick. "Least Privilege". 2005-09-14. <https://web.archive.org/web/20211209014121/https://www.cisa.gov/uscert/bsi/articles/knowledge/principles/least-privilege> (URL validated: 2023-04-07).
- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 9, "Filenames and Paths", Page 503. 1st Edition. Addison Wesley. 2006.
- [REF-962] Object Management Group (OMG). "Automated Source Code Security Measure (ASCSM)". ASCSM-CWE-22. 2016-01. <http://www.omg.org/spec/ASCSM/1.0/>.
- [REF-1448] Cybersecurity and Infrastructure Security Agency. "Secure by Design Alert: Eliminating Directory Traversal Vulnerabilities in Software". 2024-05-02. <https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-directory-traversal-vulnerabilities-software> (URL validated: 2024-07-14).
- [REF-1479] Gregory Larsen, E. Kenneth Hong Fong, David A. Wheeler and Rama S. Moorthy. "State-of-the-Art Resources (SOAR) for Software Vulnerability Detection, Test, and Evaluation". 2014-07. <https://www.ida.org/-/media/feature/publications/s/st/stateoftheart-resources-soar-for-software-vulnerability-detection-test-and-evaluation/p-5061.ashx> (URL validated: 2025-09-05).
- [REF-1481] D3FEND. "D3FEND: Application Layer Firewall". <https://d3fend.mitre.org/dao/artifact/d3f:ApplicationLayerFirewall/> (URL validated: 2025-09-06).
- [REF-1482] D3FEND. "D3FEND: D3-TL Trusted Library". <https://d3fend.mitre.org/technique/d3f:TrustedLibrary/> (URL validated: 2025-09-06).

## Mapping Notes

- **Usage:** Allowed-with-Review

- **Rationale:** This CWE entry might have children that would be more appropriate.

- **Comments:** Examine children of this entry to see if there is a better fit. Consider children such as CWE-23 (or its descendants) for relative path traversal, or CWE-36 for absolute path traversal.

- **Reasons:** Abstraction

- **Suggestions:**

  - [CWE-23](../weaknesses/CWE-23.md) Relative Path Traversal (Base): relative path traversal - also consider descendants
  - [CWE-36](../weaknesses/CWE-36.md) Absolute Path Traversal (Base): absolute path traversal

## Notes

- **Other**: In many programming languages, the injection of a null byte (the 0 or NUL) may allow an attacker to truncate a generated filename to apply to a wider range of files. For example, the product may add ".txt" to any pathname, thus limiting the attacker to text files, but a null injection may effectively remove this restriction.

- **Relationship**: Pathname equivalence can be regarded as a type of canonicalization error.

- **Relationship**: Some pathname equivalence issues are not directly related to directory traversal, rather are used to bypass security-relevant checks for whether a file/directory can be accessed by the attacker (e.g. a trailing "/" on a filename could bypass access rules that don't expect a trailing /, causing a server to provide the file when it normally would not).

- **Terminology**:

  Like other weaknesses, terminology is often based on the types of manipulations used, instead of the underlying weaknesses. Some people use "directory traversal" only to refer to the injection of ".." and equivalent sequences whose specific meaning is to traverse directories.

  Other variants like "absolute pathname" and "drive letter" have the \*effect\* of directory traversal, but some people may not call it such, since it doesn't involve ".." or equivalent.

- **Research Gap**: Many variants of path traversal attacks are probably under-studied with respect to root cause. CWE-790 and CWE-182 begin to cover part of this gap.

- **Research Gap**:

  Incomplete diagnosis or reporting of vulnerabilities can make it difficult to know which variant is affected. For example, a researcher might say that "..\\" is vulnerable, but not test "../" which may also be vulnerable.

  Any combination of directory separators ("/", "\\", etc.) and numbers of "." (e.g. "....") can produce unique variants; for example, the "//../" variant is not listed (CVE-2004-0325). See this entry's children and lower-level descendants.

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Contribution (Feedback) | 2022-07-11 | Nick Johnston |  |  | Identified weakness in Perl demonstrative example |
| Contribution (Content) | 2024-02-29 | Abhi Balakrishnan |  | CWE 4.15, 2024-07-16 | Provided diagram to improve CWE usability |
| Contribution (Feedback) | 2024-11-01 | Drew Buttner | MITRE |  | Identified weakness in "good code" for Python demonstrative example |
| Contribution (Content) | 2025-02-08 | Affan Ahmed |  | CWE 4.20, 2026-04-30 | Provided a demonstrative example in PHP |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Potential_Mitigations, Time_of_Introduction |
| Modification | 2008-08-15 |  | Veracode | CWE 1.0, 2008-09-09 | Suggested OWASP Top Ten 2004 mapping |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Alternate_Terms, Relationships, Other_Notes, Relationship_Notes, Relevant_Properties, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2008-10-14 | CWE Content Team | MITRE | CWE 1.0.1, 2008-10-14 | updated Description |
| Modification | 2008-11-24 | CWE Content Team | MITRE | CWE 1.1, 2008-11-25 | updated Relationships, Taxonomy_Mappings |
| Modification | 2009-07-27 | CWE Content Team | MITRE | CWE 1.5, 2009-07-27 | updated Potential_Mitigations |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 | updated Alternate_Terms, Applicable_Platforms, Common_Consequences, Demonstrative_Examples, Description, Detection_Factors, Likelihood_of_Exploit, Name, Observed_Examples, Other_Notes, Potential_Mitigations, References, Related_Attack_Patterns, Relationship_Notes, Relationships, Research_Gaps, Taxonomy_Mappings, Terminology_Notes, Time_of_Introduction, Weakness_Ordinalities |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Common_Consequences, Demonstrative_Examples, Description, Detection_Factors, Potential_Mitigations, References, Relationships |
| Modification | 2010-09-27 | CWE Content Team | MITRE | CWE 1.10, 2010-09-27 | updated Potential_Mitigations |
| Modification | 2010-12-13 | CWE Content Team | MITRE | CWE 1.11, 2010-12-13 | updated Potential_Mitigations |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Potential_Mitigations |
| Modification | 2011-06-27 | CWE Content Team | MITRE | CWE 2.0, 2011-06-27 | updated Relationships |
| Modification | 2011-09-13 | CWE Content Team | MITRE | CWE 2.1, 2011-09-13 | updated Potential_Mitigations, References, Relationships, Taxonomy_Mappings |
| Modification | 2012-05-11 | CWE Content Team | MITRE | CWE 2.2, 2012-05-15 | updated Demonstrative_Examples, References, Relationships |
| Modification | 2012-10-30 | CWE Content Team | MITRE | CWE 2.3, 2012-10-30 | updated Potential_Mitigations |
| Modification | 2013-02-21 | CWE Content Team | MITRE | CWE 2.4, 2013-02-21 | updated Observed_Examples |
| Modification | 2013-07-17 | CWE Content Team | MITRE | CWE 2.5, 2013-07-17 | updated Related_Attack_Patterns, Relationships |
| Modification | 2014-06-23 | CWE Content Team | MITRE | CWE 2.7, 2014-06-23 | updated Other_Notes, Research_Gaps |
| Modification | 2014-07-30 | CWE Content Team | MITRE | CWE 2.8, 2014-07-31 | updated Detection_Factors, Relationships, Taxonomy_Mappings |
| Modification | 2015-12-07 | CWE Content Team | MITRE | CWE 2.9, 2015-12-07 | updated Relationships |
| Modification | 2017-01-19 | CWE Content Team | MITRE | CWE 2.10, 2017-01-19 | updated Related_Attack_Patterns |
| Modification | 2017-05-03 | CWE Content Team | MITRE | CWE 2.11, 2017-05-05 | updated Demonstrative_Examples |
| Modification | 2017-11-08 | CWE Content Team | MITRE | CWE 3.0, 2017-11-08 | updated Affected_Resources, Causal_Nature, Likelihood_of_Exploit, References, Relationships, Relevant_Properties, Taxonomy_Mappings |
| Modification | 2018-03-27 | CWE Content Team | MITRE | CWE 3.1, 2018-03-27 | updated References, Relationships |
| Modification | 2019-01-03 | CWE Content Team | MITRE | CWE 3.2, 2019-01-03 | updated References, Related_Attack_Patterns, Relationships, Taxonomy_Mappings |
| Modification | 2019-06-20 | CWE Content Team | MITRE | CWE 3.3, 2019-06-20 | updated Related_Attack_Patterns, Relationships, Type |
| Modification | 2019-09-19 | CWE Content Team | MITRE | CWE 3.4, 2019-09-19 | updated Relationships |
| Modification | 2020-02-24 | CWE Content Team | MITRE | CWE 4.0, 2020-02-24 | updated Potential_Mitigations, Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE | CWE 4.1, 2020-06-25 | updated Demonstrative_Examples, Potential_Mitigations |
| Modification | 2020-08-20 | CWE Content Team | MITRE | CWE 4.2, 2020-08-20 | updated Relationships |
| Modification | 2020-12-10 | CWE Content Team | MITRE | CWE 4.3, 2020-12-10 | updated Potential_Mitigations, Relationships |
| Modification | 2021-03-15 | CWE Content Team | MITRE | CWE 4.4, 2021-03-15 | updated Demonstrative_Examples, Relationships |
| Modification | 2021-07-20 | CWE Content Team | MITRE | CWE 4.5, 2021-07-20 | updated Relationships |
| Modification | 2021-10-28 | CWE Content Team | MITRE | CWE 4.6, 2021-10-28 | updated Observed_Examples, Relationships |
| Modification | 2022-06-28 | CWE Content Team | MITRE | CWE 4.8, 2022-06-28 | updated Observed_Examples, Relationships |
| Modification | 2022-10-13 | CWE Content Team | MITRE | CWE 4.9, 2022-10-13 | updated Observed_Examples, References |
| Modification | 2023-01-31 | CWE Content Team | MITRE | CWE 4.10, 2023-01-31 | updated Common_Consequences, Description, Detection_Factors |
| Modification | 2023-04-27 | CWE Content Team | MITRE | CWE 4.11, 2023-04-27 | updated Demonstrative_Examples, References, Relationships, Time_of_Introduction |
| Modification | 2023-06-29 | CWE Content Team | MITRE | CWE 4.12, 2023-06-29 | updated Mapping_Notes, Relationships |
| Modification | 2023-10-26 | CWE Content Team | MITRE | CWE 4.13, 2023-10-26 | updated Observed_Examples |
| Modification | 2024-07-16 | CWE Content Team | MITRE | CWE 4.15, 2024-07-16 | updated Common_Consequences, Description, Diagram, Observed_Examples, Other_Notes, References |
| Modification | 2024-11-19 | CWE Content Team | MITRE | CWE 4.16, 2024-11-19 | updated Demonstrative_Examples, Relationships |
| Modification | 2025-04-03 | CWE Content Team | MITRE | CWE 4.17, 2025-04-03 | updated Relationships |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Applicable_Platforms, Detection_Factors, Observed_Examples, Potential_Mitigations, References |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Mapping_Notes, Relationships |
| Modification | 2026-04-30 | CWE Content Team | MITRE | CWE 4.20, 2026-04-30 | updated Alternate_Terms, Applicable_Platforms, Demonstrative_Examples, Relationships |

**Previous Entry Names:**

- Path Traversal — 2010-02-16

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
