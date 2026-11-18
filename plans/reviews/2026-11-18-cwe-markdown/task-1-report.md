# Task 1 report: CWE 5.0 edition data, merge script, metadata

## Implemented
- `git mv` merge_cwe_views.py to `weakness/mitre.org/cwe/scripts/`; argparse `--edition-dir` / `--version`; output columns and format unchanged.
- Ran unchanged `scripts/download-cwe-items.sh` in `5.0/`; ran merge for 5.0.
- `5.0/LICENSE.txt`, `5.0/cwe-5.0-metadata.json`; edited 4.19.1 metadata.

## Verification
- Merge proof, SHA-256 before and after (identical):
  - cwe-4.19.1-all.csv  b59a41dd3e0943b4005971c5f67ec38bcd83e62756f887f9ddc9f3d0d935e29a
  - cwe-4.19.1-all.json c557dfaec8e94ff2aae70922af882c5a7c43883bc185d1d3b3e0681709280269
- CSV data rows: 1000 = 956, 699 = 405, 1194 = 112. All three JSON `.Weakness_Catalog."+@Version"` = "5.0". Directory holds only the expected files plus the zip and its sidecar.
- 5.0 merge summary: 958 distinct entries; 507 multi-view; view 1000: 956, 699: 405, 1194: 112; Base 520, Variant 293, Class 128, Pillar 10, Compound 7.
- XML counts (cwec_v5.0.xml): 984 Weakness, 28 Deprecated weaknesses, 431 Grouping, 62 View, 1081 External_Reference; View 1000 name "Complete Weakness Hierarchy"; Weakness_Catalog Date 2026-10-28, schema cwe-8.
- LICENSE: MITRE terms page fetched live (page last updated July 20, 2023). After normalising curly quotes, (TM) and whitespace, the body text equals 4.19.1's LICENSE.txt exactly; 5.0/LICENSE.txt is a copy, `diff` empty. No difference to report.
- `audit_secid_alignment.py`: 1380 metadata files, 0 missing namespaces. `check_tier_restrictions.py`: PASS (all checks).

## Files changed
- R  4.19.1/merge_cwe_views.py -> scripts/merge_cwe_views.py (modified)
- M  4.19.1/cwe-4.19.1-metadata.json
- A  5.0/CWE-{Research-Concepts-1000,Software-Development-699,Hardware-Design-1194}.{csv,json}, 5.0/cwe-5.0-all.{csv,json}, 5.0/LICENSE.txt, 5.0/cwe-5.0-metadata.json

## Self-review / concerns
- Writing 4.19.1 metadata with `ensure_ascii=False` (per brief) turned existing `—` escapes into literal em dashes (3 places): harmless, but extra diff lines.
- 4.19.1 `lifecycle.notes`/`supersedes` left as is. 5.0 `tier_evidence.method` is `fetch`.
- 5.0 metadata/4.19.1 notes reference `markdown/` and `scripts/cwe_to_markdown.py`, which later tasks create.
- Used a scratchpad dir for the extracted XML; nothing left in the repo.

## Fix report (review findings)
- Finding 1: the three "Research Concepts before 5.0 / in 4.x" claims in `5.0/cwe-5.0-metadata.json` now say "Research Concepts in 4.19.1; renamed by 4.21/5.0" (description, scope.views_included, current_extraction.notes). No rename release is claimed more precisely.
- Finding 2: `4.19.1/cwe-4.19.1-metadata.json` lifecycle: `active: false`; note now past tense ("4.x was the active major version from 2018 until 5.0 (2026-10-28); 4.20 and 4.21, which are not held here, were released between 4.19.1 and 5.0").
- Checks: json.load on both metadata files printed ok/ok; `audit_secid_alignment.py` 0 missing namespaces; `python3 -I tools-resources/utils/check_tier_restrictions.py` PASS.
