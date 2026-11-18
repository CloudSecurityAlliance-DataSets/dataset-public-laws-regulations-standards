# Task 4 report: page rendering, CLI, generated markdown

**Status:** DONE_WITH_CONCERNS (all concerns are observations for the reviewer; nothing is failing).
**Commits** (branch `feat/160-cwe-markdown`, not pushed):
- `2c3a33d3` feat: render CWE editions as markdown (cwe_to_markdown.py) (#160): code, tests, README, metadata and sidecar wording
- `6cbf8471` chore: generate CWE markdown for 4.19.1 and 5.0 (#160): the two `markdown/` folders only (2,928 files)

## What I implemented

`weakness/mitre.org/cwe/scripts/cwe_to_markdown.py` (stdlib only), with the brief's interface: `render_weakness`, `render_group`, `render_view`, `render_index`, `render_edition` (includes `LICENSE.txt` copied byte for byte), `write_markdown` (writes changed files only, deletes files not produced, removes empty dirs), `diff_markdown`, `main(--version V [--check])`. Extra public names: `UnexpectedMarkupError`, `footer`, `entry_line`, `cwe_link`.

- **Weakness pages:** spec front matter, then the spec's 24 sections in its fixed order (not XML order: 5.0 puts `Technical_Nuance` right after `Description`), empty ones left out. The diagram is an image linked to MITRE at the end of Description. Tables: Related Weaknesses (nature, linked entry with name and abstraction, linked view, ordinal, plus Chain and 5.0 per-relationship Dimensions columns when present), Applicable Platforms, Common Consequences, Observed Examples (with Link and 5.0 Rationale), Taxonomy Mappings. Columns that are empty in every row are dropped. Lists with bold labels: Alternate Terms (with 5.0 Roles), Weakness Ordinalities, Modes Of Introduction (phases incl. 5.0 `Custom_Phase` as `Training (AI)`), Detection Methods, Potential Mitigations (key line `**Phase:** ... · **Strategy:** ... · **ID:** MIT-n`, body indented below), Mapping Notes (usage, rationale, comments, reasons, suggestions linked), Notes (type plus 5.0 `Version`/`ReleaseDate`). Demonstrative Examples use `### Example n (DX-id)` with Intro/Body/Example_Code in XML order and 4.19.1's per-example References. References are formatted like MITRE's (authors, title, section, edition, publication, publisher, date from XSD gYear/gMonth/gDay, URL with validated date, alternate URL, access restrictions, media type, rationale).
- **Category/grouping pages:** Summary, Members (table: member line, view link plus name), Taxonomy Mappings, References, Mapping Notes, Notes.
- **View pages:** a type, status and member-count line, then Objective and Audience. Graph views get a nested outline: each entry expanded once, and cross-references end `*(listed in full under CWE-p)*` or `*(listed in full at the top level)*`. Then `## Not reachable from this view's roots` when `unreachable_in_view` is non-empty (ruling 2). Explicit views get a flat list. Implicit views get `## Filter` (fenced `xpath`) plus `## Members`; an active view with an unknown filter gets "Members not computed" plus a stderr warning. Deprecated and obsolete views are checked first (ruling 3) and render status, banner, objective and a note naming exactly which parts (audience, members, filter, references, mapping notes, notes) are not rendered, with MITRE's URL.
- **Index:** front matter (secid, entry_type, version, date, source zip URL, sha256), edition, source and SHA-256, licence (link to `LICENSE.txt`), attribution, what is omitted. Counts by entry type, by abstraction and by status. Three tables in numeric order.
- **Ruling 4:** IDs that are not in the edition render as `CWE-n (not in CWE <v>)`, never as a link. This applies to relationships, members, suggestions and outlines. A missing REF renders as plain text that says so.
- **No silent loss:** a declarative `_check` on every element the renderer walks fails on any unknown child element or attribute, naming the CWE ID and path, and `_leaf` fails if a text-only field gains markup. `Content_History` is in the allowed set but is never read.
- **README:** new "Markdown" section covering folders, editions, page layout, how to regenerate and check, and what is left out.
- **Metadata (ruling 5):** `current_extraction.tool` in both edition records now names `scripts/cwe_to_markdown.py (markdown/ from MITRE's full XML)`. The "#161" sentence now reads "The markdown/ folder (an index and one page per weakness, category|grouping and view) is generated from that XML by scripts/cwe_to_markdown.py." Both sidecars say "Input to scripts/cwe_to_markdown.py, which refuses to run if this sha256 does not match." I first confirmed that a `json.dumps(indent=2, ensure_ascii=False)+"\n"` round-trip reproduces all four files byte for byte, so the diff is exactly 6 changed lines.
- Not run: `build_index.py` (ruling 6).

## TDD evidence

- RED 1: test module written first. `python3 -m unittest discover ...` gave `ModuleNotFoundError: No module named 'cwe_to_markdown'` (1 error, 41 run).
- RED 2: a signature-only stub (functions returning empty values). 20 of the 23 tests then written fail or error (6 FAIL, 14 ERROR). The 3 that pass on the stub are vacuous on empty output (`test_deterministic`, `test_content_history_has_no_effect`, `test_no_empty_sections_anywhere`) and become meaningful with real pages: the footer test requires more than 1,400 pages.
- GREEN: the implementation passed 23/23 on its first run. I distrusted that and read the real output; the defects it showed are listed below. Each fix got a regression assertion: `test_cwe79_tables_and_links` (mitigation label run-in; inline alternate-term form) and `test_line_hygiene` (no trailing spaces, no empty list items, no escaped `<br>` in cells).
- Self-review added `test_unknown_filter_on_active_view_says_not_computed`. Its first run failed on a test bug (the section body starts with the blank line after the heading), which I fixed in the test.
- Final: `python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v` → `Ran 65 tests ... OK` (40 existing + 25 new), about 8 s.

New tests: front_matter_cwe79, section_order, no_empty_sections_anywhere, line_hygiene, new_5_0_sections, footer_on_every_page, all_relative_links_resolve (more than 10,000 links per edition, fenced and inline code stripped), counts (folders and index rows vs catalog, numeric order), license_copied, index_header, content_history_has_no_effect (ruling 1: 26 weaknesses incl. 79/89/1426/1039/1024/377 plus 5 groupings and 5 views, rendered with and without `Content_History`, identical; no `Content History` heading in any page), deterministic, check_mode, main_rejects_unknown_version, cwe79_result_example_order (spec §Verification), cwe79_tables_and_links, group_page, deprecated_weakness_banner, view_1000_lists_every_active_weakness (ruling 2, both editions; 378/379 with parent 377 in 5.0; no section in 4.19.1), graph_view_outline_shape, explicit_and_implicit_views, deprecated_and_obsolete_views_description_only (629/679/999/630; no warning printed), unknown_filter_on_active_view_says_not_computed, dangling_targets_render_as_plain_text (ruling 4), unknown_element_fails.

### Defects found by reading real output (all fixed before commit)
1. A one-paragraph mitigation or detection description ran into its key line (`**ID:** MIT-15 For any security checks...`).
2. A mitigation with no phase, strategy or ID (5.0 CWE-256) rendered as an empty `- ` item.
3. The deprecated-view banner pointed to "Mapping Notes and Notes below", which are not rendered for views; the omitted-parts sentence was ungrammatical.
4. The deprecated-category banner said "description" (categories have a Summary). It now reads "The sections below may name a replacement."
5. The index linked the folder name `weaknesses/` to `CWE-5.md`; folders are now named in code spans.
6. The CLI said "wrote 1479 files" when only 3 changed. It now prints `N files, M written or removed`.
7. Lists mixing one-line and multi-block items had no blank lines between items (valid, but untidy as raw text).

## Files changed
- Created: `weakness/mitre.org/cwe/scripts/cwe_to_markdown.py` (1,080 lines), `weakness/mitre.org/cwe/scripts/tests/test_cwe_to_markdown.py` (435 lines)
- Modified: `weakness/mitre.org/cwe/README.md` (+30), `weakness/mitre.org/cwe/4.19.1/cwe-4.19.1-metadata.json`, `weakness/mitre.org/cwe/5.0/cwe-5.0-metadata.json`, `weakness/mitre.org/cwe/4.19.1/cwec_v4.19.1.xml.zip-file-metadata.json`, `weakness/mitre.org/cwe/5.0/cwec_v5.0.xml.zip-file-metadata.json`
- Generated: `weakness/mitre.org/cwe/4.19.1/markdown/**`, `weakness/mitre.org/cwe/5.0/markdown/**`
- Not touched: `cwe_xml.py`, `cwe_structured_text.py`, the three pinned scripts.

## Counts and sizes

| Edition | Files | weaknesses/ | categories/ or groupings/ | views/ | other | Bytes | `du -sh` |
|---|---|---|---|---|---|---|---|
| 4.19.1 | 1,449 | 969 | 420 (categories) | 58 | index.md, LICENSE.txt | 9,236,896 (9.2 MB) | 12M |
| 5.0 | 1,479 | 984 | 431 (groupings) | 62 | index.md, LICENSE.txt | 9,514,402 (9.5 MB) | 12M |

Generation takes about 1.6 s per edition.

## `--check` results
- After generation: `--version 4.19.1 --check` gives "1449 files match", exit 0; `--version 5.0 --check` gives "1479 files match", exit 0. Both were re-run on the committed tree, from `/tmp` as working directory and under `python3 -I`, all exit 0.
- Failure path, exercised on the real folder: appending to index.md, adding `views/stray.md` and deleting `groupings/CWE-1210.md` gave the three relative paths listed and exit 1. Re-running the generator restored the folder, removed the stray file and `--check` gave exit 0.
- An unknown version (`--version 9.9`) gives exit 2 with the loader's "cannot read sidecar" message.
- Other repository checks: `check_tier_restrictions.py` PASS (after `git add -N`; `--self-test` passes); `audit_secid_alignment.py`: 0 missing namespaces.

Corpus-wide checks on all 2,928 generated files, run from scratch scripts:
- 8,967 tables, 0 rows whose cell count differs from the header.
- No raw HTML outside code except `<br>` in cells, `<sup>` and autolinks.
- Link targets: 45,325 relative (all resolve, per the test), 6,227 www.cve.org, 2,424 capec.mitre.org, 180 MITRE diagram images, 2 zip links. No accidental links from MITRE prose.
- No CR, no trailing spaces, no absolute local paths. Tabs appear only inside code fences (4 pages).

## Spot-checks against https://cwe.mitre.org/data/definitions/<id>.html (fetched 2026-11-18; MITRE shows version 5.0)

Method: MITRE's HTML converted to text (content region only, content history and tooltips cut). Checked in both directions: (a) every prose sentence of 8 or more words and every code line on my page must appear verbatim on MITRE's page after normalisation; (b) MITRE sentences missing from my page; (c) CVE, CAPEC, REF and CWE ID sets.

| Page | CVE / CAPEC / REF sets | My prose on MITRE | My code lines on MITRE | Differences (content) |
|---|---|---|---|---|
| CWE-79 | 20/6/24, identical | 198 sentences, all present except the page name and related-entry names (MITRE shows those as table cells) | 83 of 83 | none. MITRE-only text is derived reverse relationships (children, MemberOf categories/views), usage help text and formatting ("Note:" vs "Effectiveness Notes:") |
| CWE-89 | 15/6/22, identical | 167; the 3 unmatched are the page name and 2 related-entry name lines | 35 of 35 | none (same kinds of MITRE-only text) |
| CWE-1426 | 1/0/5, identical | 37; the 3 unmatched are my labels (2 suggestion lines, 1 note label) | n/a | none; MITRE shows Note Version/ReleaseDate the same way |
| CWE-1039 (Technical Nuance) | 1/0/8, identical | 46; 1 unmatched: the page name | n/a | none |
| CWE-1024 (Dimensions) | 0/0/0 | 10 of 10 | n/a | none |
| CWE-284 (Pillar) | 10/17/4, identical | 49 of 49 | 20 of 20 | none; MITRE also lists its children (derived) |
| CWE-1191 (hardware) | 1/2/10, identical | 52; 1 unmatched: the page name | 52 of 52 | none |
| CWE-391, CWE-377 (deprecated, 5.0) | identical | 17 and 7; unmatched only my banner | n/a | none |
| CWE-1210 (grouping) | n/a | 6; 1 unmatched: a member-name line | n/a | members: mine 6, MITRE 6 (same IDs) |
| View 658 (implicit, C) | n/a | n/a | n/a | members: mine 103, MITRE 103, same IDs |
| View 1000 | n/a | n/a | n/a | MITRE's page lists 954 entries, the same as the outline. Mine adds CWE-378 and CWE-379 (plus parent CWE-377) in "Not reachable from this view's roots"; MITRE's own page omits them, which confirms the Task 3 finding |
| CWE-1475 | 3/0/0 | 14; 1 unmatched: a related-entry name line | n/a | MITRE data defect, see Concerns |

## Self-review against spec and rulings
- Spec §Output layout, §Entry pages (front matter, order, footer text verbatim with a blank line before `---`), §View pages, §Index page, §Scripts: met. Two additions: `view_type` in view front matter, and front matter (with `source` and `sha256`) on index.md.
- §Verification: `--check` passes for both editions; page counts equal the catalog; every relative link resolves; the CWE-79 Result order is tested; all spot-check pages checked; tier gate, audit and unittest pass; sizes reported above.
- Rulings 1 to 6: all met as described above.
- Global constraints: stdlib only; UTF-8, LF, trailing newline; no timestamps or local paths; numeric order; no `Content_History` names (proved by ruling 1's test); pinned scripts and the T2/T3 modules unchanged; explicit `git add` paths; two commits; not pushed.

## Concerns
1. **Spec example vs data (no action needed):** the spec's front-matter example names CWE-79 "Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')". In 5.0 MITRE renamed it to "Improper Neutralization of Input During Web Page Generation" (XML and live site agree). The test asserts the XML value; the spec example may want a refresh.
2. **MITRE data defect:** 5.0 CWE-1475, observed example `CVE-2025-50328` has `<Link>` pointing to `https://www.cve.org/CVERecord?id=CVE-2026-58052`. MITRE's live page has the same mismatch. I render MITRE's Link faithfully. Alternatives: build CVE links from the ID (spec: "CVE linked to cve.org"), or report it upstream to MITRE. Reviewer or controller call.
3. **Reverse relationships not on weakness pages:** MITRE's site shows a weakness's children and the categories and views it belongs to (e.g. the Top 25 lists). These are derived from other entries and the spec does not ask for them; grouping and view pages carry them. The README states this. A "Member Of" section would help retrieval and could be a follow-up.
4. **Small additions beyond the spec, for the reviewer to accept or trim:** MITRE's internal IDs (`MIT-n`, `DM-n`, `DX-n`) are shown; obsolete entries get a banner like deprecated ones; the index has front matter.
5. Carried from Task 2 (unchanged here): `$` is not escaped in prose (fine on GitHub; pandoc math could misread it).

## Excerpt 1: 5.0 `weaknesses/CWE-79.md`, lines 1 to 150 (558 lines in total)

`````markdown
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
`````

## Excerpt 2: 5.0 `views/CWE-1000.md`, lines 1 to 60

`````markdown
---
secid: "secid:weakness/mitre.org/cwe@5.0#CWE-1000"
cwe_id: "CWE-1000"
entry_type: view
name: "Complete Weakness Hierarchy"
view_type: Graph
status: Draft
mapping_usage: Prohibited
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
upstream: "https://cwe.mitre.org/data/definitions/1000.html"
---

# CWE-1000: Complete Weakness Hierarchy

**View type:** Graph · **Status:** Draft · **Members:** 956 weaknesses

## Objective

This view has a hierarchical organization of all weaknesses within CWE. It is intended to facilitate research into weaknesses, including their inter-dependencies, and can be leveraged to systematically identify theoretical gaps within CWE. It is mainly organized according to abstractions of behaviors and other dimensions instead of how the weaknesses can be detected or mitigated, where they appear in code, or when they are introduced in the development life cycle. By design, this view is expected to include every weakness within CWE.

## Audience

- **Academic Researchers**: Academic researchers can use the high-level classes that lack a significant number of children to identify potential areas for future research.
- **Vulnerability Analysts**: Those who perform vulnerability discovery/analysis use this view to identify related weaknesses that might be leveraged by following relationships between higher-level classes and bases.
- **Assessment Tool Vendors**: Assessment vendors often use this view to help identify additional weaknesses that a tool may be able to detect as the relationships are more aligned with a tool's technical capabilities.
- **Product Vendors**: Product vendors can use this view to assist with mapping vulnerabilities to their root-cause weaknesses.

## Members

- [CWE-284](../weaknesses/CWE-284.md) Improper Access Control (Pillar)
  - [CWE-269](../weaknesses/CWE-269.md) Improper Privilege Management (Class)
    - [CWE-250](../weaknesses/CWE-250.md) Execution with Unnecessary Privileges (Base)
    - [CWE-266](../weaknesses/CWE-266.md) Incorrect Privilege Assignment (Base)
      - [CWE-9](../weaknesses/CWE-9.md) J2EE Misconfiguration: Weak Access Permissions for EJB Methods (Variant)
      - [CWE-520](../weaknesses/CWE-520.md) .NET Misconfiguration: Use of Impersonation (Variant)
      - [CWE-556](../weaknesses/CWE-556.md) ASP.NET Misconfiguration: Use of Identity Impersonation (Variant)
      - [CWE-1022](../weaknesses/CWE-1022.md) Use of Web Link to Untrusted Target with window.opener Access (Variant)
      - [CWE-1268](../weaknesses/CWE-1268.md) Policy Privileges are not Assigned Consistently Between Control and Data Agents (Base)
    - [CWE-267](../weaknesses/CWE-267.md) Privilege Defined With Unsafe Actions (Base)
      - [CWE-623](../weaknesses/CWE-623.md) Unsafe ActiveX Control Marked Safe For Scripting (Variant)
    - [CWE-268](../weaknesses/CWE-268.md) Privilege Chaining (Base)
    - [CWE-270](../weaknesses/CWE-270.md) Privilege Context Switching Error (Base)
    - [CWE-271](../weaknesses/CWE-271.md) Privilege Dropping / Lowering Errors (Class)
      - [CWE-272](../weaknesses/CWE-272.md) Least Privilege Violation (Base)
      - [CWE-273](../weaknesses/CWE-273.md) Improper Check for Dropped Privileges (Base) *(listed in full under CWE-754)*
    - [CWE-274](../weaknesses/CWE-274.md) Improper Handling of Insufficient Privileges (Base) *(listed in full under CWE-755)*
    - [CWE-648](../weaknesses/CWE-648.md) Incorrect Use of Privileged APIs (Base)
  - [CWE-282](../weaknesses/CWE-282.md) Improper Ownership Management (Class)
    - [CWE-283](../weaknesses/CWE-283.md) Unverified Ownership (Base)
    - [CWE-708](../weaknesses/CWE-708.md) Incorrect Ownership Assignment (Base)
  - [CWE-285](../weaknesses/CWE-285.md) Improper Authorization (Class)
    - [CWE-356](../weaknesses/CWE-356.md) Missing User Interaction for Potentially Unsafe Action (Base)
    - [CWE-552](../weaknesses/CWE-552.md) Files or Directories Accessible to External Parties (Base) *(listed in full under CWE-668)*
    - [CWE-732](../weaknesses/CWE-732.md) Incorrect Permission Assignment for Critical Resource (Class)
      - [CWE-276](../weaknesses/CWE-276.md) Incorrect Default Permissions (Base)
      - [CWE-277](../weaknesses/CWE-277.md) Insecure Inherited Permissions (Variant)
      - [CWE-278](../weaknesses/CWE-278.md) Insecure Preserved Inherited Permissions (Variant)
      - [CWE-279](../weaknesses/CWE-279.md) Incorrect Execution-Assigned Permissions (Variant)
      - [CWE-281](../weaknesses/CWE-281.md) Improper Preservation of Permissions (Base)
`````

## Excerpt 3: 5.0 `index.md`, lines 1 to 40

`````markdown
---
secid: "secid:weakness/mitre.org/cwe@5.0"
entry_type: index
cwe_version: "5.0"
cwe_release_date: "2026-10-28"
source: "https://cwe.mitre.org/data/xml/cwec_v5.0.xml.zip"
sha256: "bcda44c9abf61ff977f50c3c6649eea5a97a7b0626b0396c2c3ec4bfb973a3dc"
---

# CWE 5.0

MITRE's Common Weakness Enumeration (CWE) version 5.0, released 2026-10-28, as markdown: this index and one page per weakness (`weaknesses/`), grouping (`groupings/`) and view (`views/`).

- **Edition:** CWE 5.0, released 2026-10-28
- **Source:** `cwec_v5.0.xml` in [cwec_v5.0.xml.zip](https://cwe.mitre.org/data/xml/cwec_v5.0.xml.zip), SHA-256 `bcda44c9abf61ff977f50c3c6649eea5a97a7b0626b0396c2c3ec4bfb973a3dc`
- **Licence:** CWE Terms of Use, <https://cwe.mitre.org/about/termsofuse.html>; full text in [LICENSE.txt](LICENSE.txt)
- **Attribution:** Copyright © The MITRE Corporation. CWE™ is a trademark of The MITRE Corporation.
- **Omitted:** MITRE's content history (who submitted or modified each entry, and when)
- **Upstream pages:** <https://cwe.mitre.org/data/definitions/> (MITRE's site shows the latest CWE version, which may differ from 5.0)

## Counts

### By entry type

| Entry type | Count |
| --- | --- |
| Weaknesses | 984 |
| Groupings | 431 |
| Views | 62 |

### Weaknesses by abstraction

| Abstraction | Weaknesses |
| --- | --- |
| Pillar | 10 |
| Class | 131 |
| Base | 536 |
| Variant | 300 |
| Compound | 7 |

`````

---

# Fix report: review of 2c3a33d3 / 6cbf8471 (fix round 1)

**Commits:** `fd3d9e47` fix: render repeated CWE values in full; fail on repeated single values; plural headings (#160) (code, tests, README). `2e83d13b` chore: regenerate CWE markdown after review fixes (#160) (14 markdown files only).

## Finding 1: repeated child elements silently dropped (fixed)
- **Schema check first.** I fetched MITRE's `cwe_schema_v7.3.xsd` and `cwe_schema_v8.0.xsd` (the `xsi:schemaLocation` of 4.19.1 and 5.0) and listed every element with `maxOccurs` > 1 by parent. Of those, only two were read single-valued: `Observed_Example/Rationale` and `External_Reference/Media_Type`, both new in 8.0. Every other repeatable element (Phase, Custom_Phase, Role, Scope, Impact, Author, External_Reference/Rationale, Dimension, Note, Background_Detail, Example_Code/Body_Text, and so on) was already rendered in full. This matches the reviewer's scan.
- **Render all values.** Observed Examples' Rationale cell joins every value with `; ` (CWE-125 now shows "Influential/Newsworthy; Chain"). References print `Media type: X` for one value and `Media types: X; Y` for several (REF-1556 now shows "Common-Proprietary-Text; Video").
- **Single-value accessor.** New `_one(parent, name, ctx)` raises `UnexpectedMarkupError("<ctx>: <Name> appears N times in <Parent>; expected at most one")`. All 40-odd single-valued reads now go through it: front matter, index usage, every weakness, group and view top-level section, Mapping_Notes parts, Alternate_Term Term/Description, Ordinality, Introduction Note, Method, Strategy, Description, Effectiveness, Effectiveness_Notes, Reference/Link, Taxonomy_Mapping fields, Related_Weakness Dimensions, Stakeholder fields, view Filter/Objective/Audience, `_stated_parents`, and every External_Reference single field. The `child` import was removed from the module. `render_view` also validates `Members` with `_one`, because `cwe_xml`'s outline helpers read it with `child()`.
- **README** line 70 now says the script fails "on XML elements, attributes or markup it does not know, and on a second copy of an element that MITRE's schema allows only once. Every element the schema lets repeat is rendered in full." That is now true.

## Finding 2: "Categorys" (fixed)
New `_plural_noun()` (weakness → weaknesses, category → categories, Grouping → Groupings); `_plural()` uses it. The index counts row, the status-table header and the section heading use it. `test_counts` now expects `Categories` (4.19.1) and `Groupings` (5.0) explicitly.

## Covering tests (4 new, 1 changed; 69 total)
- `test_repeated_values_all_rendered`: the 5.0 CWE-125 CVE-2014-0160 row contains "Influential/Newsworthy; Chain"; the 5.0 CWE-1461 REF-1556 line contains "Media types: Common-Proprietary-Text; Video".
- `test_repeated_single_valued_element_fails`: a duplicated top-level `Description`, a second Mapping_Notes `Usage`, two `Strategy` in a Mitigation, a duplicated view-1000 `Members`, and a second `Title` in REF-709 (via `dataclasses.replace` on the edition) each raise `UnexpectedMarkupError` naming the CWE or REF and the element.
- `test_no_unchecked_single_reads`: the module source has no bare `child(` or `cx.child(` call.
- `test_index_plurals`: the headings, the counts row and the status header say Categories or Groupings; no file contains "Categorys".
- `test_counts`: expects "Categories" or "Groupings" (changed).
- RED: before the fix, 5 failed (4 FAIL, 1 ERROR: `test_counts` KeyError on the missing heading). GREEN after the fix.

## Commands and output
```
python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v
  -> Ran 69 tests in 7.6s  OK
python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 4.19.1
  -> weakness/mitre.org/cwe/4.19.1/markdown: 1449 files, 1 written or removed
python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 5.0
  -> weakness/mitre.org/cwe/5.0/markdown: 1479 files, 13 written or removed
python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 4.19.1 --check
  -> 1449 files match (exit 0)
python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 5.0 --check
  -> 1479 files match (exit 0)
python3 -I tools-resources/utils/check_tier_restrictions.py
  -> PASS (exit 0)
```

## Generated files changed
- 4.19.1: **1** (`index.md`: "Categorys" changed to "Categories" in the counts row, the status header and the `## Categories` heading).
- 5.0: **13**. Twelve pages gain the second observed-example rationale: weaknesses CWE-125, 126, 130 and 240 (CVE-2014-0160), and 295, 300, 393, 483, 561, 705, 1114 and 1164 (CVE-2014-1266). CWE-1461 lists both REF-1556 media types. 5.0's index is unchanged ("Groupings" was already correct).
- Files touched: `cwe_to_markdown.py`, `test_cwe_to_markdown.py`, `README.md`, and the two `markdown/` folders only.

## Observation (outside my scope; not changed)
`cwe_xml.load_edition` indexes weaknesses, groups, views and references in dicts keyed by ID, and its outline helpers read `Members`, `Relationships` and `Related_Weaknesses` with `child()`. A duplicate ID, or a duplicate of those containers, would be dropped there without error. Today's data has none: in both editions the counts of External_Reference and Weakness IDs equal their distinct counts. A duplicated container on a weakness, group or view now fails in this renderer (via `_one`) before any page is written. A duplicate ID would still pass, so a guard in `cwe_xml` may be worth a later task.
