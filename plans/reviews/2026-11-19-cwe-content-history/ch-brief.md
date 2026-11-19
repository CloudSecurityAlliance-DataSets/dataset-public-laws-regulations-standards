# Brief: include MITRE content history in the CWE markdown (issue #166)

Repo root: <repo>
Branch: feat/166-cwe-content-history (already checked out, from main at ec6385ed)

## Why
Kurt, 2026-11-19, verbatim: "lets default to mirroring data faithfully, so that means leaving names in." He then chose "Include, at page end (Recommended)": a "Content History" section as the LAST section of every weakness, category/grouping and view page, directly above the footer.

## Code: weakness/mitre.org/cwe/scripts/cwe_to_markdown.py
1. Render `Content_History` for weaknesses, categories/groupings and views as the final `## Content History` section (after every other section, before the footer). The heading text must be exactly `Content History` (GitHub anchor `#content-history`, matching SecID's section-subpath convention used by the other headings).
2. Measured structure (both schemas, 4.19.1 and 5.0):
   - `Submission` (1 per entry, but 5.0 has ONE entry with TWO Submissions — render every one): Submission_Name, Submission_Organization, Submission_Date, Submission_Version, Submission_ReleaseDate, Submission_Comment.
   - `Modification` (~17,800 in 5.0): Modification_Name, Modification_Organization, Modification_Date, Modification_Version, Modification_ReleaseDate, Modification_Importance, Modification_Comment.
   - `Contribution` with attribute `Type`: Contribution_Name, Contribution_Organization, Contribution_Date, Contribution_Version, Contribution_ReleaseDate, Contribution_Comment.
   - `Previous_Entry_Name` (text) with attributes `Date` and optionally `Version`.
   Render faithfully and in MITRE's document order within each kind. Suggested layout (your call if a clearly better one exists): one markdown table for submissions/contributions/modifications with columns Event (Submission / Contribution (<Type>) / Modification), Date, Name, Organization, Version (with release date), Importance, Comment; then a "Previous entry names" list (`name` — date, version). Every value appears; escape cells with the existing `escape_table_cell`; multi-line comments collapse per existing table rules. Empty columns may be dropped only if empty for the whole table on that page.
3. Keep the module's fail-loud rules: unknown children/attributes inside Content_History fail via the existing `_check` mechanism; repeated single-valued children (e.g. two Modification_Date in one Modification) fail via `_one`; repeated elements that are legitimately multiple (Submission, Modification, Contribution, Previous_Entry_Name) render all.
4. Update the module docstring and any comment that says content history is omitted.

## Tests: weakness/mitre.org/cwe/scripts/tests/test_cwe_to_markdown.py
- Remove `test_content_history_has_no_effect` and any assertion that no page has a `Content History` heading.
- Add: for CWE-79 (every edition present), the page has `## Content History` as its LAST `## ` heading, and the section contains the Submission name and organization and every Modification date from the XML (compare against the element).
- Add: the 5.0 entry with two Submissions shows both (find it from the XML in the test; do not hard-code the ID unless you also assert it).
- Add: a category/grouping page and a view page have the section when their XML has Content_History.
- Keep the edition-derivation and skip/CWE_REQUIRE_ZIPS behaviour.

## Regenerate and check
- `python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version V` for 4.19.1, 4.20, 4.21, 5.0, then `--check` for each (exit 0).
- `python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests` (all pass).
- Report per edition: files changed, `du -sh` of markdown/ before and after.
- `python3 tools-resources/utils/build_index.py` in THIS checkout (it has the git-ignored originals); the INDEX.md diff must touch only CWE rows if anything; if file counts are unchanged expect no diff. If unrelated rows change, revert INDEX.md/README.md and report.
- `python3 -I tools-resources/utils/check_tier_restrictions.py` and `python3 tools-resources/utils/audit_secid_alignment.py` pass.

## Docs (make every statement true after the change)
- AGENTS.md: add, near the 4-tier rule / no-bulk-mirror section, a short "Mirror faithfully" rule with Kurt's words verbatim and date: mirrored and derived data keep upstream content as published, including people's names in upstream records (e.g. MITRE CWE content history); do not strip or rewrite upstream content unless Kurt records an exception. Do not change any other rule.
- weakness/mitre.org/cwe/README.md: remove/replace every statement that the markdown omits content history; list `Content History` as the last section; update the CWE-1475 note to say MITRE's own page also links the row labelled CVE-2025-50328 to CVE-2026-58052 (the link target; the visible text is CVE-2025-50328).
- docs/superpowers/specs/2026-11-18-cwe-markdown-design.md: replace the content-history-omitted anti-goal/ruling text with Kurt's 2026-11-19 decision (quote both his sentence and his choice "Include, at page end (Recommended)"), add `Content History` as the final section in §Entry pages, and keep the earlier history honest (say it superseded the earlier omission).
- grep afterwards for "omit", "Content History", "content history", "names" across those three files and the scripts; report any remaining stale claim.

## Constraints
- Python 3.10+ standard library only. Do not edit `download-cwe-items.sh`, `download-cwe-documents.sh`, `html_to_markdown.py` (tier-gate pinned). Do not modify cwe_xml.py or cwe_structured_text.py unless a bug blocks you (then stop and report).
- Commit with conventional messages referencing #166, ending `Co-Authored-By: Claude <noreply@anthropic.com>`, explicit `git add` paths only, no push. Separate commits: (a) code + tests + docs; (b) regenerated markdown (+ INDEX if changed).
- Do not dispatch subagents.

## Report
Write the full report to <scratch> what changed (file:line), TDD evidence (RED/GREEN), command outputs listed above, the rendered Content History section of 5.0 CWE-79 (first 25 lines of it) and of the two-Submission entry, sizes before/after, stale-claim grep result, concerns. Reply with ONLY (under 15 lines): Status, commits, one-line verification summary, concerns, report path.
