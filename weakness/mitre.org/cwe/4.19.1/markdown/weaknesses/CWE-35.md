---
secid: "secid:weakness/mitre.org/cwe@4.19.1#CWE-35"
cwe_id: "CWE-35"
entry_type: weakness
name: "Path Traversal: '.../...//'"
abstraction: Variant
structure: Simple
status: Incomplete
mapping_usage: Allowed
cwe_version: "4.19.1"
cwe_release_date: "2026-01-21"
upstream: "https://cwe.mitre.org/data/definitions/35.html"
---

# CWE-35: Path Traversal: '.../...//'

## Description

The product uses external input to construct a pathname that should be within a restricted directory, but it does not properly neutralize '.../...//' (doubled triple dot slash) sequences that can resolve to a location that is outside of that directory.

![Diagram for CWE-35](https://cwe.mitre.org/data/images/CWE-35-Diagram.png)

## Related Weaknesses

| Nature | Entry | View | Ordinal |
| --- | --- | --- | --- |
| ChildOf | [CWE-23](../weaknesses/CWE-23.md) Relative Path Traversal (Base) | [CWE-1000](../views/CWE-1000.md) | Primary |

## Weakness Ordinalities

- **Resultant**

## Applicable Platforms

| Type | Class | Prevalence |
| --- | --- | --- |
| Language | Not Language-Specific | Undetermined |

## Modes Of Introduction

- **Implementation**

## Common Consequences

| Scope | Impact | Note |
| --- | --- | --- |
| Confidentiality<br>Integrity | Read Files or Directories<br>Modify Files or Directories<br>Bypass Protection Mechanism | Not properly neutralizing '.../...//' (doubled triple dot slash) allows attackers to traverse the file system to access files or directories that are outside of the restricted directory. |

## Detection Methods

- **Method:** Automated Static Analysis · **ID:** DM-14

  Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)

## Potential Mitigations

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-5.1

  Assume all input is malicious. Use an "accept known good" input validation strategy, i.e., use a list of acceptable inputs that strictly conform to specifications. Reject any input that does not strictly conform to specifications, or transform it into something that does.

  When performing input validation, consider all potentially relevant properties, including length, type of input, the full range of acceptable values, missing or extra inputs, syntax, consistency across related fields, and conformance to business rules. As an example of business rule logic, "boat" may be syntactically valid because it only contains alphanumeric characters, but it is not valid if the input is only expected to contain colors such as "red" or "blue."

  Do not rely exclusively on looking for malicious or malformed inputs. This is likely to miss at least one undesirable input, especially if the code's environment changes. This can give attackers enough room to bypass the intended validation. However, denylists can be useful for detecting potential attacks or determining which inputs are so malformed that they should be rejected outright.

  When validating filenames, use stringent allowlists that limit the character set to be used. If feasible, only allow a single "." character in the filename to avoid weaknesses such as CWE-23, and exclude directory separators such as "/" to avoid CWE-36. Use a list of allowable file extensions, which will help to avoid CWE-434.

  Do not rely exclusively on a filtering mechanism that removes potentially dangerous characters. This is equivalent to a denylist, which may be incomplete (CWE-184). For example, filtering "/" is insufficient protection if the filesystem also supports the use of "\\" as a directory separator. Another possible error could occur when the filtering is applied in a way that still produces dangerous data (CWE-182). For example, the ".../...//" manipulation is useful for bypassing some path traversal protection schemes. If "../" sequences are removed from the ".../...//" string in a sequential fashion (as some regular expression engines and other algorithms operate) the string can collapse into the unsafe "../" value (CWE-182). Removing the first "../" yields "....//" and the second removal yields "../".

  **Effectiveness:** High

- **Phase:** Implementation · **Strategy:** Input Validation · **ID:** MIT-20

  Inputs should be decoded and canonicalized to the application's current internal representation before being validated (CWE-180). Make sure that the application does not decode the same input twice (CWE-174). Such errors could be used to bypass allowlist validation schemes by introducing dangerous inputs after they have been checked.

## Demonstrative Examples

### Example 1

Suppose the product serves files from a specific "public" directory -- /home/product/public/ -- and has an algorithm that attempts to protect against common path traversal attacks. The algorithm works by sequentially scanning through a requested filename and removes each occurrence of "../" that it encounters, then appending the filename to the public directory.

If an attacker provides this filename:

*Example (Attack):*

```
    ../secret.dat
```

then the code would correctly remove the "../" resulting in the name:

*Example (Result):*

```
    /home/product/public/secret.dat
```

This request would fail, because secret.dat is not in /home/product/public/secret.dat.

The attacker could attempt to bypass this protection mechanism using this string:

*Example (Attack):*

```
    .../...//secret.dat
```

The algorithm would remove the first occurrence of "../" to produce:

*Example (Result):*

```
    ....//secret.dat
```

The algorithm would then find and remove the second (and final) "../" sequence, producing:

*Example (Result):*

```
    ../secret.dat
```

At this point, the algorithm stops because it removed all "../" that appeared in the original string, but the algorithm has collapsed the original input into an unsafe value (CWE-182) that is still subject to path traversal.

The end result is:

*Example (Result):*

```
    /home/product/public/../secret.dat
```

Which the OS resolves to /home/product/secret.dat, a file that is outside the public directory.

*Example (Good, Other):*

```other
The algorithm could be changed to use a built-in path canonicalization function that effectively removes "../" sequences, removes symbolic links, etc., such as realpath() in C. An alternate approach might be to run a loop that continues to remove "../" sequences from successive outputs until all suspect sequences are removed. However, relying solely on such a filter may be risky, since there may be sequences or characters that the filter is not covering for all environments.
```

## Observed Examples

| Reference | Description |
| --- | --- |
| [CVE-2005-2169](https://www.cve.org/CVERecord?id=CVE-2005-2169) | chain: ".../...//" bypasses protection mechanism using regexp's that remove "../" resulting in collapse into an unsafe value "../" (CWE-182) and resultant path traversal. |
| [CVE-2005-0202](https://www.cve.org/CVERecord?id=CVE-2005-0202) | ".../....///" bypasses regexp's that remove "./" and "../" |

## Functional Areas

- File Processing

## Affected Resources

- File or Directory

## Taxonomy Mappings

| Taxonomy | Entry ID | Entry Name |
| --- | --- | --- |
| PLOVER |  | '.../...//' |
| Software Fault Patterns | SFP16 | Path Traversal |

## Mapping Notes

- **Usage:** Allowed
- **Rationale:** This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.
- **Comments:** Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.
- **Reasons:** Acceptable-Use

## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Modification | 2008-07-01 | Eric Dalci | Cigital |  | updated Potential_Mitigations, Time_of_Introduction |
| Modification | 2008-09-08 | CWE Content Team | MITRE |  | updated Description, Relationships, Taxonomy_Mappings |
| Modification | 2008-10-14 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2008-11-24 | CWE Content Team | MITRE |  | updated Observed_Examples |
| Modification | 2009-07-27 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2010-06-21 | CWE Content Team | MITRE |  | updated Description, Potential_Mitigations |
| Modification | 2010-12-13 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2011-03-29 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2011-06-01 | CWE Content Team | MITRE |  | updated Common_Consequences |
| Modification | 2012-05-11 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2014-07-30 | CWE Content Team | MITRE |  | updated Relationships, Taxonomy_Mappings |
| Modification | 2017-11-08 | CWE Content Team | MITRE |  | updated Applicable_Platforms |
| Modification | 2020-02-24 | CWE Content Team | MITRE |  | updated Potential_Mitigations, Relationships |
| Modification | 2020-06-25 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2021-03-15 | CWE Content Team | MITRE |  | updated Potential_Mitigations |
| Modification | 2021-10-28 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-01-31 | CWE Content Team | MITRE |  | updated Description |
| Modification | 2023-04-27 | CWE Content Team | MITRE |  | updated Relationships |
| Modification | 2023-06-29 | CWE Content Team | MITRE |  | updated Mapping_Notes |
| Modification | 2025-09-09 | CWE Content Team | MITRE | CWE 4.18, 2025-09-09 | updated Affected_Resources, Functional_Areas |
| Modification | 2025-12-11 | CWE Content Team | MITRE | CWE 4.19, 2025-12-11 | updated Common_Consequences, Demonstrative_Examples, Description, Detection_Factors, Diagram, Potential_Mitigations, Weakness_Ordinalities |

**Previous Entry Names:**

- Path Issue - Doubled Triple Dot Slash - '.../...//' — 2008-04-11

---
Generated from MITRE's CWE 4.19.1 XML (cwec_v4.19.1.xml) by weakness/mitre.org/cwe/scripts/cwe_to_markdown.py.
Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
Used under the CWE Terms of Use: https://cwe.mitre.org/about/termsofuse.html (full text: https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/4.19.1/LICENSE.txt).
