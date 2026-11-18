## Task State Summary — 2026-11-18

**Objective:** Offer MITRE CWE as markdown (index, one page per CWE item, one per view) for easier ingestion, and add CWE 5.0, 4.21 and 4.20 to the dataset.

Kurt's asks, verbatim, in order:

> "can you look in weakness/mitre.org/cwe at cwe? how would we also offer this data as markdown formatted files for easier ingestion? e.g. I'm thinking an index file in markdown, and then one file for each CWE item? formatted nicely/etc? I'm thinking a script that converts the JSON data into markdown?"
>
> "oh can we also do a markdown for each view?"
>
> "ok also we need to go get the CWE 5.0 data as well and process that one fully as well"
>
> "ok lets do the ata here, the csv -> markdown I guess first, and the 5.0, that'll get mnost of what we need right away"
>
> "is there a better source for the data>? an API? github?" (answered; Kurt chose "XML, one pass (Recommended)")
>
> "we also need to get 4.20 and 4.21 I guess?"
>
> "we treat mitre like the gov, we republish their data, it's fine."
>
> "merge 5.0 in now real quick"

**Current status:** All planned work is done and reviewed. #162 (5.0 data) merged as `17971737`. #161 (markdown for 4.19.1, 4.20, 4.21 and 5.0; scripts; 4.20/4.21 editions; docs; INDEX) is ready, with every check passing.

**What changed:**
- `weakness/mitre.org/cwe/scripts/`: `cwe_xml.py`, `cwe_structured_text.py`, `cwe_to_markdown.py` (+78 unittest tests); `merge_cwe_views.py` moved here (in #162).
- `weakness/mitre.org/cwe/{4.19.1,4.20,4.21,5.0}/markdown/`: about 5,860 generated pages.
- `weakness/mitre.org/cwe/{4.20,4.21}/`: new XML-only editions (metadata, sidecar, LICENSE). `5.0/`: full edition (in #162).
- XML originals for all four editions in S3, pinned by committed SHA-256 sidecars.
- `tools-resources/utils/build_index.py`: only canonical edition metadata counts; a `markdown/index.md` marks a directory as structured. `INDEX.md` and the root README inventory regenerated.
- `AGENTS.md`: Kurt's MITRE rule; `markdown/` in the standard-files table; CWE health checks.
- Design, plan, review brief and review evidence: `docs/superpowers/specs/2026-11-18-cwe-markdown-design.md`, `docs/superpowers/plans/2026-11-18-cwe-markdown.md`, `plans/2026-11-18-cwe-markdown-review-brief.md`, `plans/reviews/2026-11-18-cwe-markdown/`.

**Key findings:**
- MITRE's REST API is unversioned (reports 4.21); MITRE's GitHub org holds no CWE content; the CSV export is lossy (no examples, references, mapping notes; likelihood of exploit empty) and its packed fields are ambiguous. The versioned full XML is the right source.
- The `yq` per-view JSON loses the order of mixed text and markup; the markdown is the readable form.
- View 1000 was renamed "Complete Weakness Hierarchy" in 4.21 (4.20 still says "Research Concepts").
- In 5.0, CWE-378 and CWE-379 are active but their only parent in view 1000 is deprecated CWE-377, so no root reaches them.
- MITRE data error: 5.0/4.21 CWE-1475 lists CVE-2025-50328 with a link to CVE-2026-58052.
- SecID registry prose named CWE-1425 as the AI/ML view; it is CWE-1448 (CloudSecurityAlliance/SecID#298).
- `build_index.py` counts git-ignored originals, so INDEX.md must be regenerated in a full checkout, not a fresh worktree.

**Decisions made:**
- Kurt, 2026-11-18: markdown lives in this repo; source is MITRE's full XML ("XML, one pass"); add 4.20 and 4.21; MITRE data is republished like government data (AGENTS.md); merge 5.0 data first (#162).
- AI's calls (recorded in the spec and on #160): short MITRE attribution footer on every page plus `LICENSE.txt` per folder; content history omitted from markdown but kept in the mirrored per-view JSON (FR-1); upstream errors reproduced as published; 4.20/4.21 as XML-only editions; `access_tier` 2 for MITRE (Tier 1 is defined as a government host).

**Assumptions used:** MITRE's versioned zip URLs stay stable (the sidecars and S3 copies cover it if not); GitHub's markdown renderer is the target for escaping.

**Risks / uncertainties:** Future MITRE releases may bring new XHTML tags, implicit-view filters or schema changes; the scripts fail loudly on most of these (an unknown filter string warns instead). CI does not regenerate or check the markdown (#158).

**Open questions:** None blocking.

**Human input needed:**
- Optional: whether to strip MITRE's content history (contributor names) from the mirrored per-view JSON (currently kept under the MITRE rule; recorded on #160).
- Optional: whether to report the CWE-1475 link error to MITRE.

**Recommended next action:** Merge #161 once CI is green; then the follow-ups #163 (hardening), #164 (navigation: reverse relationships, outline anchors), #165 (4.19.1 tier, merge tooling), and wire CWE into the reproducibility gate (#158).

**Files / artifacts changed:** #160 (issue), #161, #162, #163, #164, #165, comment on #158, CloudSecurityAlliance/SecID#298.

**Not on GitHub:** the session transcript and the per-task subagent ledger (git-ignored scratch); the task and fix reports were copied into `plans/reviews/2026-11-18-cwe-markdown/` with local paths scrubbed. The XML zips are in S3, not git.

**Confidence level:** High for the generated output (byte-reproducible, all relative links resolve, every task independently reviewed, implicit views matched against an XPath engine). Medium for rendering on markdown engines other than GitHub's.
