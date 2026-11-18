# Task 5 report: CWE 4.20 and 4.21 (XML-only)

Status: DONE. Commits: d86a49cc (metadata, sidecars, LICENSE, README, 4.19.1/5.0 edits), 56d75b8b (generated markdown).

## Measured facts
| | 4.20 | 4.21 | 5.0 (reference) |
|---|---|---|---|
| zip sha256 | 3976f599e5e5200219a3108bb896d06e2a88fbb293369e1883cb423a5e9d7d50 | 5225e2b4976696b5b90b62cdad0ddab4e8898103d61350971e366a377e718862 | (existing) |
| retrieved_at (UTC) | 2026-11-18T20:56:37Z | 2026-11-18T20:56:40Z | |
| catalog Version/Date | 4.20 / 2026-04-30 | 4.21 / 2026-10-28 | 5.0 / 2026-10-28 |
| schema | 7.3 (cwe-7) | 7.4 (cwe-7) | 8.0 (cwe-8) |
| weaknesses (deprecated) | 969 (25) | 984 (28) | 984 (28) |
| categories/groupings (deprecated) | 422 (35) | 431 (35) | 431 groupings (35) |
| views (deprecated) | 59 (4) | 62 (4) | 62 (4) |
| external references | 1026 | 1081 | 1081 |
| view 1000 name | Research Concepts | Complete Weakness Hierarchy | same as 4.21 |

Each zip holds one file, cwec_v<v>.xml. Duplicate check: no duplicate Weakness/Category/View @ID (per type or combined) and no duplicate External_Reference_ID, in either new edition (also none in 4.19.1 and 5.0).
4.21 vs 5.0: all counts identical; differs in schema (7.4 vs 8.0) and Category vs Grouping element. 1049 markdown files differ between the two folders (diff -rq).
MITRE terms page re-fetched: every license sentence in 5.0/LICENSE.txt (except the page-title line) is present; LICENSE.txt copied unchanged.

## Generation and check
Generated 4.20 (1452 files) and 4.21 (1479 files), rc 0, no errors raised. --check: 4.19.1 1449 match, 4.20 1452 match, 4.21 1479 match, 5.0 1479 match; all rc 0.
Files / du -sh markdown: 4.19.1 1449 / 12M; 4.20 1452 / 12M (969 weaknesses, 422 categories, 59 views); 4.21 1479 / 12M (984, 431, 62); 5.0 1479 / 12M.

## Verification
unittest: 69 tests OK. audit_secid_alignment: missing namespaces 0. check_tier_restrictions (after git add -N): PASS (re-run after commit: PASS).

## Files changed
New: 4.20/ and 4.21/ each cwe-<v>-metadata.json, cwec_v<v>.xml.zip-file-metadata.json, LICENSE.txt, markdown/** (zips present locally, git-ignored). Edited: 4.19.1 metadata (supersededBy 4.20, note says 4.20/4.21 are held), 5.0 metadata (supersedes names 4.21, 4.20, 4.19.1), cwe/README.md (four-edition table, says which have CSV/JSON).

## Concerns
- 4.20/4.21 metadata scope holds only the measured full_xml counts, schema and view-1000 name; no distinct-entry/view-membership counts (no CSVs).
- tier_evidence url is the archive page per the brief; method "fetch" but I fetched only the Terms page and the zips, not archive.html itself.
- Did not run build_index.py or S3 sync (controller).
