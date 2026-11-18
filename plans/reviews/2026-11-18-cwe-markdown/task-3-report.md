# Task 3 report: edition loader and view outlines

## Implemented
`weakness/mitre.org/cwe/scripts/cwe_xml.py`: `SourceVerificationError`, frozen `Edition`, `load_edition` (sidecar SHA-256, catalog `@Version`, single zip member), `local/child/children/text`, `entry_kind/name/path`, `OutlineNode`, `view_outline`, `explicit_members`, `implicit_members`, `IMPLICIT_FILTERS` (15 exact-string predicates; the two `[false()]` deprecated views return `None`, i.e. "not computed"). Extra helper not in the brief: `unreachable_in_view(ed, view_id)`.
Tests: `tests/test_cwe_xml.py` (12 tests: the brief's 7 plus entry helpers, determinism, all-active-filters-known).

## TDD evidence
RED: with the module absent, the new test file failed at import (`ModuleNotFoundError` / 1 error). Honest note: I wrote the module before the tests, then moved it aside to show RED. GREEN: after restoring, tests ran; one real failure and one real bug were found and fixed (below). Final: `python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v` -> `Ran 37 tests ... OK`.

## Findings
1. Deviation from the brief: in 5.0, active weaknesses CWE-378 and CWE-379 have `ChildOf` only to CWE-377, which is Deprecated and has no parent in view 1000, so no root reaches them. The expanded set is 954, not 956; with `unreachable_in_view` it totals 956. The test asserts `expanded | unreachable == non-deprecated` (4.19.1: 944, none unreachable). No other Graph view in either edition has unreachable entries. The renderer (later task) must decide how to show these two (suggest listing them under an "Not reachable from the roots" note on view 1000).
2. Bug caught by the test run: `Element` truthiness is False for childless elements; `entry_name` used `or` chaining. Fixed with explicit lookup.
3. Cycle guard: reachable entries whose chosen-parent chain never reaches a root are re-parented under an already-expanded parent (not triggered by current data).

## Counts
4.19.1: 969 weaknesses, 420 categories, 58 views, 1,012 refs (schema 7). 5.0: 984, 431 groupings, 62, 1,081 (schema 8).

| View | Edition | roots | expanded | cross-ref nodes | unreachable |
|---|---|---|---|---|---|
| 1000 | 4.19.1 | 10 | 944 | 151 | none |
| 699 | 4.19.1 | 40 | 439 | 46 | none |
| 1194 | 4.19.1 | 13 | 123 | 16 | none |
| 1000 | 5.0 | 10 | 954 | 160 | 378, 379 |
| 699 | 5.0 | 40 | 445 | 46 | none |
| 1194 | 5.0 | 13 | 125 | 23 | none |

Implicit view member counts (4.19.1 / 5.0): 604: 64/67; 658: 103/103; 659: 97/97; 660: 84/84; 661: 26/26; 677: 523/518; 678: 4/4; 701: 297/305; 702: 835/844; 709: 3/3; 919: 21/21; 1040: 114/114; 1081: 185/200; 1424: 39/39; 2000: 1447/1477 (= all weaknesses + groups + views). 679 and 999 (`[false()]`, Deprecated): not computed (`None`).

## Files
`weakness/mitre.org/cwe/scripts/cwe_xml.py`, `weakness/mitre.org/cwe/scripts/tests/test_cwe_xml.py`.

## Concerns
- Finding 1 above (controller's 956 fact does not hold as a pure expanded-set equality).
- Predicates 658-661, 701, etc. were checked only for existence and, for 658/604, content; others were not independently verified against MITRE's HTML.

## Fix report (review findings 1 and 2)
- Finding 1: `test_version_mismatch_raises` now copies zip and sidecar under `cwec_v9.9.*` names so the SHA passes and the catalog Version check rejects it; both verification tests use `assertRaisesRegex` (`sha256`; `catalog Version '5.0' != '9.9'`).
- Finding 2 (T3-a): new `DanglingReferenceError(ValueError)`; `_view_graph` raises, naming the view and CWE ID, when a view root, a category/grouping `Has_Member` (that view) or a `ChildOf` parent is absent from the catalog. Three synthetic tests mutate a freshly loaded edition in memory (root, group member, ChildOf parent). Real-data tests stay green.
- Command: `python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v` -> `Ran 40 tests ... OK`.
