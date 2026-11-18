---
secid: "secid:weakness/mitre.org/cwe@4.20#CWE-36"
cwe_id: "CWE-36"
entry_type: weakness
name: "Absolute Path Traversal"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.20"
cwe_release_date: "2026-04-30"
upstream: "https://cwe.mitre.org/data/definitions/36.html"
---

# CWE-36: Absolute Path Traversal

## Description

The product uses external input to construct a pathname that should be within a restricted directory, but it does not properly neutralize absolute path sequences such as "/abs/path" that can resolve to a location that is outside of that directory.

## Extended Description

This allows attackers to traverse the file system to access files or directories that are outside of the restricted directory.

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-22](../weaknesses/CWE-22.md) Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |
| ChildOf | [CWE-22](../weaknesses/CWE-22.md) Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (Base) | [CWE-1305](../views/CWE-1305.md) | Primary |
| ChildOf | [CWE-22](../weaknesses/CWE-22.md) Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (Base) | [CWE-1340](../views/CWE-1340.md) | Primary |

## Weakness Ordinalities

- **Primary**

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
| Confidentiality | Read Files or Directories | The attacker may be able read the contents of unexpected files and expose sensitive data. If the targeted file is used for a security mechanism, then the attacker may be able to bypass that mechanism. For example, by reading a password file, the attacker could conduct brute force password guessing attacks in order to break into an account on the system. |
| Availability | DoS: Crash, Exit, or Restart | The attacker may be able to overwrite, delete, or corrupt unexpected critical files such as programs, libraries, or important data. This may prevent the product from working at all and in the case of a protection mechanisms such as authentication, it has the potential to lockout every user of the product. |

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

  **Effectiveness:** High

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-20

  Inputs should be decoded and canonicalized to the application's current internal representation before being validated (CWE-180). Make sure that the application does not decode the same input twice (CWE-174). Such errors could be used to bypass allowlist validation schemes by introducing dangerous inputs after they have been checked.

- **Phase:** Operation · **Strategy:** Firewall · **ID:** MIT-29

  Use an application firewall that can detect attacks against this weakness. It can be beneficial in cases in which the code cannot be fixed (because it is controlled by a third party), as an emergency prevention measure while more comprehensive software assurance measures are applied, or to provide defense in depth [REF-1481].

  **Effectiveness:** Moderate

  **Effectiveness Notes:** An application firewall might not cover all possible input vectors. In addition, attack techniques might be available to bypass the protection mechanism, such as using malformed inputs that can still be processed by the component that receives those inputs. Depending on functionality, an application firewall might inadvertently reject or modify legitimate requests. Finally, some manual effort may be required for customization.

## Demonstrative Examples

### Example 1 (DX-18)

In the example below, the path to a dictionary file is read from a system property and used to initialize a File object.

*Example (Bad, Java):*

```java
String filename = System.getProperty("com.domain.application.dictionaryFile");
File dictionaryFile = new File(filename);
```

However, the path is not validated or modified to prevent it from containing relative or absolute path sequences before creating the File object. This allows anyone who can control the system property to determine what file is used. Ideally, the path should be resolved relative to some kind of application or user home directory.

### Example 2 (DX-159)

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

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2024-0520](https://www.cve.org/CVERecord?id=CVE-2024-0520) | Product for managing datasets for AI model training and evaluation allows both relative (CWE-23) and absolute (CWE-36) path traversal to overwrite files via the Content-Disposition header |
| [CVE-2022-31503](https://www.cve.org/CVERecord?id=CVE-2022-31503) | Python package constructs filenames using an unsafe os.path.join call on untrusted input, allowing absolute path traversal because os.path.join resets the pathname to an absolute path that is specified as part of the input. |
| [CVE-2002-1345](https://www.cve.org/CVERecord?id=CVE-2002-1345) | Multiple FTP clients write arbitrary files via absolute paths in server responses |
| [CVE-2001-1269](https://www.cve.org/CVERecord?id=CVE-2001-1269) | ZIP file extractor allows full path |
| [CVE-2002-1818](https://www.cve.org/CVERecord?id=CVE-2002-1818) | Path traversal using absolute pathname |
| [CVE-2002-1913](https://www.cve.org/CVERecord?id=CVE-2002-1913) | Path traversal using absolute pathname |
| [CVE-2005-2147](https://www.cve.org/CVERecord?id=CVE-2005-2147) | Path traversal using absolute pathname |
| [CVE-2000-0614](https://www.cve.org/CVERecord?id=CVE-2000-0614) | Arbitrary files may be overwritten via compressed attachments that specify absolute path names for the decompressed output. |
| [CVE-1999-1263](https://www.cve.org/CVERecord?id=CVE-1999-1263) | Mail client allows remote attackers to overwrite arbitrary files via an e-mail message containing a uuencoded attachment that specifies the full pathname for the file to be modified. |
| [CVE-2003-0753](https://www.cve.org/CVERecord?id=CVE-2003-0753) | Remote attackers can read arbitrary files via a full pathname to the target file in config parameter. |
| [CVE-2002-1525](https://www.cve.org/CVERecord?id=CVE-2002-1525) | Remote attackers can read arbitrary files via an absolute pathname. |
| [CVE-2001-0038](https://www.cve.org/CVERecord?id=CVE-2001-0038) | Remote attackers can read arbitrary files by specifying the drive letter in the requested URL. |
| [CVE-2001-0255](https://www.cve.org/CVERecord?id=CVE-2001-0255) | FTP server allows remote attackers to list arbitrary directories by using the "ls" command and including the drive letter name (e.g. C:) in the requested pathname. |
| [CVE-2001-0933](https://www.cve.org/CVERecord?id=CVE-2001-0933) | FTP server allows remote attackers to list the contents of arbitrary drives via a ls command that includes the drive letter as an argument. |
| [CVE-2002-0466](https://www.cve.org/CVERecord?id=CVE-2002-0466) | Server allows remote attackers to browse arbitrary directories via a full pathname in the arguments to certain dynamic pages. |
| [CVE-2002-1483](https://www.cve.org/CVERecord?id=CVE-2002-1483) | Remote attackers can read arbitrary files via an HTTP request whose argument is a filename of the form "C:" (Drive letter), "//absolute/path", or ".." . |
| [CVE-2004-2488](https://www.cve.org/CVERecord?id=CVE-2004-2488) | FTP server read/access arbitrary files using "C:\\" filenames |
| [CVE-2001-0687](https://www.cve.org/CVERecord?id=CVE-2001-0687) | FTP server allows a remote attacker to retrieve privileged web server system information by specifying arbitrary paths in the UNC format (\\\computername\sharename). |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | Absolute Path Traversal |
| Software Fault Patterns | SFP16 | Path Traversal |

## Related Attack Patterns

- [CAPEC-597](https://capec.mitre.org/data/definitions/597.html)

## References

- [REF-62] Mark Dowd, John McDonald and Justin Schuh. "The Art of Software Security Assessment". Chapter 9, "Filenames and Paths", Page 503. 1st Edition. Addison Wesley. 2006.
- [REF-1448] Cybersecurity and Infrastructure Security Agency. "Secure by Design Alert: Eliminating Directory Traversal Vulnerabilities in Software". 2024-05-02. <https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-directory-traversal-vulnerabilities-software> (URL validated: 2024-07-14).
- [REF-1481] D3FEND. "D3FEND: Application Layer Firewall". <https://d3fend.mitre.org/dao/artifact/d3f:ApplicationLayerFirewall/> (URL validated: 2025-09-06).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 4.20 XML (cwec_v4.20.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.20/LICENSE.txt).
