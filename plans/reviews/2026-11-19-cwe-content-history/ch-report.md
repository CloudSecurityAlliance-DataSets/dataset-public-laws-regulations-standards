# Report: CWE content history in the markdown (#166)

**Status:** DONE_WITH_CONCERNS (everything in the brief is done and passes. The concerns are judgment calls and one gap in the brief, listed at the end.)

Branch `feat/166-cwe-content-history`, not pushed.

| Commit | What |
|---|---|
| `22066893` | feat: code + tests + docs (5 files) |
| `27147cd7` | chore: regenerated markdown, 4 editions (5,855 files, +120,545 / -5,921 lines). INDEX.md is unchanged. |

## What changed

### `weakness/mitre.org/cwe/scripts/cwe_to_markdown.py`
- `:14-19`: the docstring now says Content_History is rendered in full as the last section of every entry page (with a pointer to AGENTS.md "Mirror faithfully" and #166). It no longer says the history is "never read".
- `:245-252` `footer()`: removed "Content history is omitted.". The footer line now ends at the script path.
- `:1029`: removed the index's `- **Omitted:** MITRE's content history ...` line, which would otherwise be false.
- `:437-447`: added `HISTORY_EVENTS`, listing the kinds in the order MITRE's own pages use (Submission, Contribution, Modification) with their `<Kind>_<Field>` children, and `HISTORY_REPEATED_NAMES`.
- `:449` `_history_row()`: renders one event row. `_check` covers the children, plus the `Type` attribute on Contribution only. `_one` covers every single-valued field. `_leaves` renders all `Submission_Name` and `Contribution_Name` values, which schema 8 allows to repeat.
- `:468` `_content_history()`: `_check` on Content_History (Submission, Modification, Contribution, Previous_Entry_Name). It builds one table (via `_table`, so a column empty on the whole page is dropped), then `**Previous Entry Names:**` as a list of `- name — date[, CWE version]`. `Previous_Entry_Name` is checked for attributes (`Date`, `Version`), and any child element (XHTML included) raises.
- `:800` weakness, `:833` category/grouping, `:928` and `:996` view: `("Content History", ...)` is the last section. Inactive views get it too, after Objective. The note at `:938` now reads "Only the objective, status and content history of an obsolete or deprecated view are rendered here."

### `weakness/mitre.org/cwe/scripts/tests/test_cwe_to_markdown.py`
- Removed `test_content_history_has_no_effect`.
- `:38`: `SECTION_ORDER` now ends with "Content History". `footer()` no longer has the omitted sentence. New helpers `history_section`, `history_rows`, `history_events` (`:111-128`) and `_entries` (`:513`).
- `:417-422`: the inactive-view test now expects `["Objective", "Content History"]` and the new note wording.
- New `ContentHistoryTests` (`:521`):
  - `test_cwe79_history_is_last_section`, every edition: it is the last `## ` heading and sits directly above the footer. Every Submission_Name and Submission_Organization from the XML is present. The Modification rows' Date column equals the XML's Modification_Date list, in order.
  - `test_every_entry_page_ends_with_history`: every weakness, group and view in every edition. It includes spot checks of 4.19.1 categories/CWE-1210, 5.0 groupings/CWE-1210 and views/CWE-1000.
  - `test_every_history_value_in_its_row`: for every event on every page of every edition, the row count matches, the Event label matches (including `Contribution (<Type>)`), the Date matches, and every leaf value appears in its own row.
  - `test_previous_entry_names`: exact list items for every entry. It checks that exactly 4 versioned names exist per edition, and the CWE-113 item `- HTTP Response Splitting — 2008-04-11, CWE Draft 9`.
  - `test_two_submissions_both_shown`: finds 5.0's only two-Submission entry from the XML and asserts it is CWE-1461. Both rows match name, organization and date. Every other edition has exactly one Submission per entry.
  - `test_repeated_names_all_shown`: every 5.0 Submission or Contribution with more than one name shows all of them, joined by `<br>`.
  - `test_multiline_comment_collapses_into_one_cell` (CWE-1461), `test_history_cells_escaped` (`|`, `*`, `<`, newline), and `test_no_page_says_history_omitted`.
  - `test_unknown_or_repeated_history_markup_fails`: these must fail: an unknown child of Content_History or of Modification, an unknown attribute on Submission or Previous_Entry_Name, XHTML inside Previous_Entry_Name, an attribute on a leaf, repeated Modification_Date, Submission_Organization or Modification_Name, a repeated Content_History, and an unknown child in a grouping, an active view and an obsolete view.

### Docs
- `AGENTS.md:157-161`: new section "Mirror faithfully (2026-11-19)", with Kurt's sentence verbatim, the rule, and the CWE content history as the example (#166). It is placed after the 4-tier section and before Namespaces. No other rule changed.
- `weakness/mitre.org/cwe/README.md`:
  - `:61`: sections are in schema order, "the last being `Content History`", with anchor `#content-history`.
  - `:63`: obsolete and deprecated views show "objective, status and content history only".
  - `:64`: new bullet describing the section.
  - `:80`: CWE-1475 note: "...as it does in MITRE's XML and on MITRE's own page for CWE-1475 (the link target is CVE-2026-58052; the visible text is CVE-2025-50328)". I checked this live today: cwe.mitre.org/data/definitions/1475.html has `<a href="...CVE-2026-58052">CVE-2025-50328</a>`.
  - `:82`: names kept, Kurt's 2026-11-19 quote, and the 2026-11-18 omission named as superseded.
  - `:84`: "What is left out" now has only the reverse-relationships item.
- `docs/superpowers/specs/2026-11-18-cwe-markdown-design.md`:
  - `:3-4`: Status gains "Updated 2026-11-19", and Issue gains #166.
  - `:46`: the anti-goal is now "Stripping or rewriting upstream content, people's names included". It quotes Kurt's sentence and his choice "Include, at page end (Recommended)", and states that this superseded the first build's 2026-11-18 ruling, which it describes.
  - `:108` and `:110`: Content History added as the last weakness and category/grouping section.
  - `:112-116`: the section spec.
  - `:122`: the footer block no longer has the omitted sentence.
  - `:140-141`: view pages updated.

## Judgment calls (please review)
1. **A gap in the brief: names repeat in 5.0.** The brief's measured structure has no repeated names, but 5.0 has them. CWE-1342 has one Submission with 2 `Submission_Name`. CWE-483 has a Contribution with 2 `Contribution_Name`, and CWE-1298 has two Contributions with 3 each. MITRE's schema 8.0 XSD (`cwe_schema_v8.0.xsd`, fetched from cwe.mitre.org) declares `Submission_Name` and `Contribution_Name` with `maxOccurs="unbounded"`, and `Submission` too. Every other field is maxOccurs 1, and schema 7.3 has all names single. The brief would have run these names through `_one`, which would fail the 5.0 run. Instead I followed the module's existing rule (a repeatable element is rendered in full, a once-only element fails), so all names are rendered, joined by `<br>`. Tests cover both behaviours.
2. **Cell escaping uses `_esc`, not `st.escape_table_cell` directly.** Content_History values are plain `xs:string`. Every other plain-text table cell in the module uses `_esc(_leaf(...))`. That collapses whitespace, escapes inline markdown and escapes `|`, so for single-line text the result is what `escape_table_cell` would produce, plus markdown escaping. Applying both would double-escape `|`. All 14 multi-line comments (Contribution_Comment in 4.21 and 5.0) are hard-wrapped XML indentation, so collapsing them to spaces matches the existing table rules and MITRE's site.
3. **Row order across kinds is Submission, Contribution, Modification.** This is MITRE's website order (checked on the live CWE-79 and CWE-1461 pages), not XML order (Submission, Modification, Contribution). Within each kind, rows keep document order. The brief's Event list uses the same order.
4. **The column header is "Release", not "Version".** The cell is `CWE <version>, <release date>`, matching MITRE's site ("(CWE 5.0, 2026-10-28)") and the module's Notes stamp.
5. **The footer and index text changed.** Both said content history was omitted and would have become false. The brief's list was "docstring and comments", so these two were not named in it.
6. **Obsolete and deprecated views render content history too.** The brief says "every ... view page", so their note now says so.

## TDD evidence
- **RED** (new tests in place, old code): `Ran 87 tests ... FAILED (failures=19, errors=13)`.
  - The 13 errors are all `KeyError: 'Content History'` (the section is absent).
  - The failures:
    - 8 heading assertions (`'Notes' != 'Content History'`).
    - 4 footer failures.
    - 4 `**Omitted:**` matches.
    - The deprecated-view headings test.
    - `UnexpectedMarkupError not raised`: Content_History was never checked.
- **GREEN**, first run: 1 failure, a bug in my test. CWE-79's Submission has no organization, so adding one did not create a repeat. I changed the test to add two. Then `Ran 87 tests ... OK`.
- I then refactored the closure-in-loop into a module-level `_history_row`, and re-ran: still OK.
- **Final run** on the committed tree with `CWE_REQUIRE_ZIPS=1`: `Ran 87 tests in 15.976s OK`.

## Command outputs (on the committed tree)
```
--version 4.19.1: 1449 files, 1448 written or removed   (exit 0)
--version 4.20:   1452 files, 1451 written or removed   (exit 0)
--version 4.21:   1479 files, 1478 written or removed   (exit 0)
--version 5.0:    1479 files, 1478 written or removed   (exit 0)
--check 4.19.1: 1449 files match (exit 0)
--check 4.20:   1452 files match (exit 0)
--check 4.21:   1479 files match (exit 0)
--check 5.0:    1479 files match (exit 0)
unittest (CWE_REQUIRE_ZIPS=1): Ran 87 tests, OK
build_index.py: Wrote INDEX.md (162,627 chars), exit 0; git status empty -> INDEX.md and README.md unchanged
check_tier_restrictions.py (-I): PASS ... exit 0
audit_secid_alignment.py: Scanned: 1382 metadata files; Missing namespaces: 0; exit 0
```

## Files changed and sizes

Every `.md` file changed in every edition; LICENSE.txt is unchanged.

| Edition | Files changed | Bytes before | Bytes after | `du -sh` before | `du -sh` after |
|---|---|---|---|---|---|
| 4.19.1 | 1448 of 1449 | 9,236,899 | 11,282,610 (+22%) | 12M | 13M |
| 4.20 | 1451 of 1452 | 9,272,162 | 11,620,602 (+25%) | 12M | 14M |
| 4.21 | 1478 of 1479 | 9,531,138 | 11,892,998 (+25%) | 12M | 14M |
| 5.0 | 1478 of 1479 | 9,514,494 | 12,036,332 (+27%) | 12M | 14M |

## Rendered: 5.0 CWE-79, first 25 lines of the section
```
## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2006-07-19 | PLOVER |  | CWE Draft 3, 2006-07-19 |  |
| Contribution (Content) | 2025-03-10 | Abhi Balakrishnan |  | CWE 4.17, 2025-04-03 | Provided diagram to improve CWE usability. |
| Modification | 2008-07-01 | Eric Dalci | Cigital | CWE 1.0, 2008-09-09 | updated Time_of_Introduction |
| Modification | 2008-08-15 |  | Veracode | CWE 1.0, 2008-09-09 | Suggested OWASP Top Ten 2004 mapping |
| Modification | 2008-09-08 | CWE Content Team | MITRE | CWE 1.0, 2008-09-09 | updated Alternate_Terms, Applicable_Platforms, Background_Details, Common_Consequences, Description, Relationships, Other_Notes, References, Taxonomy_Mappings, Weakness_Ordinalities |
| Modification | 2009-01-12 | CWE Content Team | MITRE | CWE 1.2, 2009-01-12 | updated Alternate_Terms, Applicable_Platforms, Background_Details, Common_Consequences, Demonstrative_Examples, Description, Detection_Factors, Enabling_Factors_for_Exploitation, Name, Observed_Examples, Other_Notes, Potential_Mitigations, References, Relationships |
| Modification | 2009-03-10 | CWE Content Team | MITRE | CWE 1.3, 2009-03-10 | updated Potential_Mitigations |
| Modification | 2009-05-27 | CWE Content Team | MITRE | CWE 1.4, 2009-05-27 | updated Name |
| Modification | 2009-07-27 | CWE Content Team | MITRE | CWE 1.5, 2009-07-27 | updated Description |
| Modification | 2009-10-29 | CWE Content Team | MITRE | CWE 1.6, 2009-10-29 | updated Observed_Examples, Relationships |
| Modification | 2009-12-28 | CWE Content Team | MITRE | CWE 1.7, 2009-12-28 | updated Demonstrative_Examples, Description, Detection_Factors, Enabling_Factors_for_Exploitation, Observed_Examples |
| Modification | 2010-02-16 | CWE Content Team | MITRE | CWE 1.8, 2010-02-16 | updated Applicable_Platforms, Detection_Factors, Potential_Mitigations, References, Relationships, Taxonomy_Mappings |
| Modification | 2010-04-05 | CWE Content Team | MITRE | CWE 1.8.1, 2010-04-05 | updated Description, Potential_Mitigations, Related_Attack_Patterns |
| Modification | 2010-06-21 | CWE Content Team | MITRE | CWE 1.9, 2010-06-21 | updated Common_Consequences, Description, Name, Potential_Mitigations, References, Relationships |
| Modification | 2010-09-27 | CWE Content Team | MITRE | CWE 1.10, 2010-09-27 | updated Potential_Mitigations |
| Modification | 2011-03-29 | CWE Content Team | MITRE | CWE 1.12, 2011-03-30 | updated Demonstrative_Examples, References |
| Modification | 2011-06-01 | CWE Content Team | MITRE | CWE 1.13, 2011-06-01 | updated Common_Consequences |
| Modification | 2011-06-27 | CWE Content Team | MITRE | CWE 2.0, 2011-06-27 | updated Relationships |
| Modification | 2011-09-13 | CWE Content Team | MITRE | CWE 2.1, 2011-09-13 | updated Detection_Factors, Potential_Mitigations |
```
The page ends with `**Previous Entry Names:**` (5 items, e.g. `- Cross-site Scripting (XSS) — 2008-04-11`), then the footer.

## Rendered: 5.0 CWE-1461, the two-Submission entry (whole section)
```
## Content History

| Event | Date | Name | Organization | Release | Comment |
| --- | --- | --- | --- | --- | --- |
| Submission | 2025-05-20 | Raghul Saravanan | George Mason University | CWE 5.0, 2026-10-28 |  |
| Submission | 2025-05-20 | Sudipta Paria | University of Florida | CWE 5.0, 2026-10-28 |  |
| Contribution (Content) | 2026-03-30 | CWE Ad Hoc RTL WG |  | CWE 5.0, 2026-10-28 | Participated in a series of meetings betwee March 2026 and September 26, in which members contributed significant feedback related to this entry as it evolved before publication in CWE 5.0. |
| Contribution (Content) | 2026-03-30 | MITRE |  | CWE 5.0, 2026-10-28 | Guided evolution of the name and description for this entry, followed by suggestions for mitigations, demonstrative examples, and detection methods. Note: some content development was AI-assisted, with expert review and editing by MITRE and members of the CWE Ad Hoc RTL WG. |
```
"betwee" and "September 26" are as in MITRE's XML.

Rendered repeated names, for example: `| Submission | 2021-09-22 | Anders Nordstrom<br>Alric Althoff | Cycuity (originally submitted as Tortuga Logic) | CWE 4.6, 2021-10-28 |  |` (CWE-1342).

## Stale-claim grep
Command: `grep -n -i "omit\|content history\|content_history\|names"` over AGENTS.md, the CWE README, the spec, `scripts/*.py`, `scripts/*.sh` and `scripts/tests/*.py`.

No stale claim remains. The remaining "omit" hits are:
- The spec's CSV row ("MITRE per-view CSV | Omits examples ..."), which is about the CSV.
- The `omitted` variable in `render_view`, which lists the sections not rendered for an inactive view.

"names" hits are unrelated (namespaces, zip member names, the new rule). The scripts-extra and analysis folders and all CWE metadata JSON have no content-history statements.

Outside the three docs, these dated 2026-11-18 records still describe the omission. I did not change them, because they are history:
- `plans/2026-11-18-cwe-markdown-review-brief.md`: `:45`, `:61`, and `:83`. `:61` is claim 9, "Markdown never contains content-history names", tied to the removed `test_content_history_has_no_effect`.
- `plans/reviews/2026-11-18-cwe-markdown/*`
- `docs/superpowers/plans/2026-11-18-cwe-markdown.md`
- `resumption-summaries/2026-11-18-cwe-markdown.md`

## Concerns
1. **The review brief's claim 9 is now obsolete.** If that review brief is treated as a living document rather than a dated record, it needs a note pointing to #166.
2. **The wording of the AGENTS.md rule.** It says mirrored data "and every form derived from it here (markdown, CSV, JSON)" keeps upstream content as published, and "do not strip". This follows the brief. But the existing `cwe-<v>-all.{csv,json}` (built from MITRE's CSV) drops 7 of its 23 columns, per the spec. That is a column subset that predates the rule, not name-stripping, but a reviewer may read it as a conflict. Kurt may want an explicit carve-out, or a follow-up issue.
3. **The meaning of a previous name's date is not on the page.** The page shows `name — date` without saying what the date means. Per MITRE's XSD, it is "the date on which this name was no longer used". The README and spec say so. A short label hint would make pages more self-contained for AI ingestion. I kept the brief's format.
4. **Size.** Each `markdown/` folder grows by about 2.0 to 2.5 MB (22-27%). The largest per-page growth is on old, much-modified entries.
5. **Tests use `ctm._esc`.** They call the private helper to compute expected escaped values, which couples them to that helper.
6. **Kurt's private global instructions.** They say never to write about specific people in a work repo. The pages now carry upstream people's names under Kurt's explicit 2026-11-19 rule. AGENTS.md frames it as upstream content kept as published, not CSA writing about people.
7. **What I fetched.** MITRE's XSDs (v8.0, v7.3) and three cwe.mitre.org pages (79, 1461, 1475) went to the scratchpad only, used for verification. Nothing fetched was committed.

---

## Fix round (review of 22066893..36f0f5b0, verdict "With fixes")

**Commit:** `58864d34` fix: narrow the "mirror faithfully" reading; fail on XHTML in content history (#166). Five files changed. The generated markdown is unchanged, so nothing was regenerated.

### I1: "Mirror faithfully" was worded too broadly
- `AGENTS.md:161`: I replaced the paragraph after Kurt's quote with the reviewer's text, word for word ("The AI's reading, recorded 2026-11-19: ..."). The heading and the quote line are unchanged.
- Spec `:46`: the anti-goal used to read "Stripping or rewriting upstream content, people's names included". It is now "Stripping people's names, or altering or dropping a value a page carries", followed by what the pages leave out and say so:
  - relationships that MITRE's website derives in reverse;
  - for obsolete and deprecated views, everything but the objective, status and content history (pointer to #165).
- README: `:82` was already specific to names, so I left it. The "What is left out" list is aligned under M5 below.

### M1: XHTML inside content history was skipped
- `cwe_to_markdown.py:452`: new `_no_xhtml()`. It raises `UnexpectedMarkupError("<CWE-n>/Content_History[/<Kind>[k]]: unexpected element <xhtml:...>")`.
- It is called in `_history_row` (`:462`) and `_content_history` (`:486`). The `Previous_Entry_Name` values and the leaf fields already rejected any child element.
- New test `test_xhtml_inside_history_containers_fails` (`test_cwe_to_markdown.py:720`). It injects `xhtml:p` into Content_History, Submission[1], Modification[3] and Contribution[1] (CWE-79), into a grouping (CWE-1210) and into an obsolete view (CWE-629). Each case must raise with the entry ID and path.
- RED, before the fix: `FAILED (failures=6)`, all six "UnexpectedMarkupError not raised". GREEN, after the fix: passes.

### M2: wording about repeats (behaviour unchanged)
I changed four places:
- README `:78`: one exception is now named. In content history, submissions and submitter and contributor names are rendered in full in every edition. Schema 8.0 lets them repeat. Schema 7.x allows one of each, but a repeat in 4.x is rendered rather than rejected (none occurs today).
- Spec `:116`: the same, plus "(an XHTML element included)", and "a repeat of any field other than the names fails".
- Module docstring `:17-21`: adds a parenthetical naming the same exception.
- `HISTORY_EVENTS` comment `:439-442`: aligned with the same wording.

### M5: README "What is left out"
`:84-87` is now a list:
- Reverse relationships.
- For obsolete and deprecated views: their audience, members, filter, references, mapping notes and notes. Each such page names what it leaves out and links to MITRE's page. A known gap, tracked in #165.

I listed "filter" because the code's omitted list includes it.

### Checks (committed tree)
```
unittest (CWE_REQUIRE_ZIPS=1): Ran 88 tests in 15.904s, OK
--check 4.19.1: 1449 files match (exit 0)
--check 4.20:   1452 files match (exit 0)
--check 4.21:   1479 files match (exit 0)
--check 5.0:    1479 files match (exit 0)
check_tier_restrictions.py (-I): PASS, exit 0
build_index.py: exit 0, INDEX.md unchanged
```

### Concerns from this round
1. **#165 does not yet track these gaps.** Its body today covers only the 4.19.1 access_tier and merge_cwe_views checks. AGENTS.md ("Known gaps ... are tracked in #165"), the README and the spec now point there for:
   - the inactive-view omissions;
   - the merged `cwe-<v>-all.*` files dropping 7 of 23 CSV columns (and `scripts-extra/output/CWE-Basic-Data.csv`).

   Someone needs to add those gaps to #165, or the pointers overstate it. I did not post to GitHub.
2. **The merged `cwe-<v>-all.*` files do not say what they leave out.** The new reading says a derived form "says what it leaves out". The design spec (Approaches table) records that these files drop 7 of the CSV's 23 columns. I did not check whether their metadata or the README says this; that belongs on #165.
3. **Stray text is not checked.** Stray non-whitespace text directly inside a Content_History container (not in an element) would still be ignored, as everywhere else in the module. None occurs, and this round did not ask for it.

### Fix round 2: the merged files now say what they leave out (follow-up to concern 2)

**Commit:** `d41078ac` docs: say which CSV columns the merged CWE files leave out (#166). Three files changed.

**Verification before writing.** `merge_cwe_views.py` reads 16 source columns:
- CWE-ID, Name, Weakness Abstraction, Status, Description, Extended Description
- Related Weaknesses, Applicable Platforms, Modes Of Introduction, Common Consequences
- Detection Methods, Potential Mitigations, Observed Examples, Taxonomy Mappings
- Related Attack Patterns, Likelihood of Exploit

Every per-view CSV header (views 1000, 699 and 1194, in both 4.19.1 and 5.0) has 23 columns. The script reads 16 of them and never reads these 7: Weakness Ordinalities, Background Details, Alternate Terms, Exploitation Factors, Functional Areas, Affected Resources, Notes. Every column the script reads is present in every header.

The committed `cwe-<v>-all.csv` headers and the JSON keys are the script's 18 output fields: the 16 columns, plus `cwe_identifier` and `views`.

**Changes:**
- `weakness/mitre.org/cwe/4.19.1/cwe-4.19.1-metadata.json` and `weakness/mitre.org/cwe/5.0/cwe-5.0-metadata.json`: in `current_extraction.notes`, after the distinct-entries sentence, added: "The merged files keep 16 of the 23 columns in MITRE's per-view CSVs and leave out Weakness Ordinalities, Background Details, Alternate Terms, Exploitation Factors, Functional Areas, Affected Resources and Notes, which remain in the per-view CSVs; tracked in #165 (<issue URL>)."
  - I edited the JSON through `json.loads` and `json.dumps(indent=2, ensure_ascii=False)` plus a trailing newline. I first confirmed both files round-trip byte for byte, so the diff is exactly one line per file.
- `weakness/mitre.org/cwe/README.md:60`: a new paragraph under the editions table with the same statement. It names `scripts/merge_cwe_views.py` and links #165.

**Checks:**
```
both metadata files: valid JSON, canonical 2-space / ensure_ascii=False / trailing newline: True
check_tier_restrictions.py (-I): PASS, exit 0
audit_secid_alignment.py: Scanned: 1382 metadata files; Missing namespaces: 0; exit 0
build_index.py: exit 0, INDEX.md unchanged
```
I did not re-run the test suite or `--check`: no code or markdown changed since `58864d34`, where both passed.

**Side note:** the merged files hold 944 entries (4.19.1) and 958 (5.0), fewer than the 969 and 984 weaknesses in those editions. The 5.0 notes already explain why; the 4.19.1 notes give the count without the reason. I did not change that.
