---
secid: "secid:weakness/mitre.org/cwe@4.21#CWE-93"
cwe_id: "CWE-93"
entry_type: weakness
name: "Improper Neutralization of CRLF Sequences"
abstraction: Base
structure: Simple
status: Draft
mapping_usage: Allowed
cwe_version: "4.21"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/93.html"
---

# CWE-93: Improper Neutralization of CRLF Sequences

## Description

The product uses CRLF (carriage return line feeds) as a special element, e.g. to separate lines or records, but it does not neutralize or incorrectly neutralizes CRLF sequences from inputs. (Roles: Common-Name, Attack-Focused)

![Diagram for CWE-93](https://cwe.mitre.org/data/images/CWE-93-Diagram.png)

## Alternate Terms

- **CRLF Injection**

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-74](../weaknesses/CWE-74.md) Improper Neutralization of Special Elements in Output Used by a Downstream Component (Class) | [CWE-1000](../views/CWE-1000.md) | Primary |
| CanPrecede | [CWE-117](../weaknesses/CWE-117.md) Improper Output Neutralization for Logs (Base) | [CWE-1000](../views/CWE-1000.md) |  |

## Weakness Ordinalities

- **Primary**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Modes Of Introduction

- **Implementation**: REALIZATION: This weakness is caused during implementation of an architectural security tactic.

## Common Consequences

| Scope | Impact |
| --- | --- |
| Integrity | Modify Application Data |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

  **Effectiveness:** High

## Potential Mitigations

- **Phase:** Implementation

  Avoid using CRLF as a special sequence.

- **Phase:** Implementation

  Appropriately filter or quote CRLF sequences in user-controlled input.

## Demonstrative Examples

### Example 1 (DX-224)

The following code segment reads the name of the author of a weblog entry, author, from an HTTP request and sets it in a cookie header of an HTTP response.

*Example (Bad, Java):*

```java
String author = request.getParameter(AUTHOR_PARAM);
...
Cookie cookie = new Cookie("author", author);
cookie.setMaxAge(cookieExpiration);
response.addCookie(cookie);
```

Assuming a string consisting of standard alpha-numeric characters, such as "Jane Smith", is submitted in the request the HTTP response including this cookie might take the following form:

*Example (Result):*

```
HTTP/1.1 200 OK
...
Set-Cookie: author=Jane Smith
...
```

However, because the value of the cookie is composed of unvalidated user input, the response will only maintain this form if the value submitted for AUTHOR_PARAM does not contain any CR and LF characters. If an attacker submits a malicious string, such as

*Example (Attack):*

```
Wiley Hacker\r\nHTTP/1.1 200 OK\r\n
```

then the HTTP response would be split into two responses of the following form:

*Example (Result):*

```
HTTP/1.1 200 OK
...
Set-Cookie: author=Wiley Hacker
HTTP/1.1 200 OK
...
```

The second response is completely controlled by the attacker and can be constructed with any header and body content desired. The ability to construct arbitrary HTTP responses permits a variety of resulting attacks, including:

- cross-user defacement
- web and browser cache poisoning
- cross-site scripting
- page hijacking

### Example 2 (DX-236)

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

The code does not neutralize the value of the file NR, which is attacker controlled because it originates from a pull request that produced pr.zip.

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

### Example 3

If user input data that eventually makes it to a log message isn't checked for CRLF characters, it may be possible for an attacker to forge entries in a log file.

*Example (Bad, Java):*

```java
logger.info("User's street address: " + request.getParameter("streetAddress"));
```

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2002-1771](https://www.cve.org/CVERecord?id=CVE-2002-1771) | CRLF injection enables spam proxy (add mail headers) using email address or name. |
| [CVE-2002-1783](https://www.cve.org/CVERecord?id=CVE-2002-1783) | CRLF injection in API function arguments modify headers for outgoing requests. |
| [CVE-2004-1513](https://www.cve.org/CVERecord?id=CVE-2004-1513) | Spoofed entries in web server log file via carriage returns |
| [CVE-2006-4624](https://www.cve.org/CVERecord?id=CVE-2006-4624) | Chain: inject fake log entries with fake timestamps using CRLF injection |
| [CVE-2005-1951](https://www.cve.org/CVERecord?id=CVE-2005-1951) | Chain: Application accepts CRLF in an object ID, allowing HTTP response splitting. |
| [CVE-2004-1687](https://www.cve.org/CVERecord?id=CVE-2004-1687) | Chain: HTTP response splitting via CRLF in parameter related to URL. |

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name | Mapping Fit |
| --- | --- | --- | --- |
| PLOVER |  | CRLF Injection |  |
| OWASP Top Ten 2007 | A2 | Injection Flaws | CWE More Specific |
| WASC | 24 | HTTP Request Splitting |  |
| Software Fault Patterns | SFP24 | Tainted input to command |  |

## Related Attack Patterns

- [CAPEC-15](https://capec.mitre.org/data/definitions/15.html)
- [CAPEC-81](https://capec.mitre.org/data/definitions/81.html)

## References

- [REF-928] Ulf Harnhammar. "CRLF Injection". Bugtraq. 2002-05-07. <http://marc.info/?l=bugtraq&m=102088154213630&w=2>.
- [REF-1456] Imperva. "CRLF Injection". <https://www.imperva.com/learn/application-security/crlf-injection//> (URL validated: 2025-02-21).
- [REF-1457] R00tendo. "CRLF injection". 2024-02-25. <https://medium.com/@R00tendo/crlf-injection-ae26521c5e4c> (URL validated: 2025-02-21).

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

---
Generated from MITRE's CWE 4.21 XML (cwec_v4.21.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py. Content history is omitted.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.21/LICENSE.txt).
