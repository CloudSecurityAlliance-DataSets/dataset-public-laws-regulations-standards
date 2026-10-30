# CCM 4.1.1 scripts

| Script | Where |
|---|---|
| `parse_ccm.py` | **here**. It rebuilds `../ccm-4.1.1.json`, `../ccm-4.1.1-controls.csv` and `../ccm-4.1.1-reverse-mappings.csv` |
| `parse_caiq.py` | **not here**. The standalone questionnaire is still labelled CAIQ 4.1.0, so its extractor lives with it: [`../../../ccm-caiq/4.1.0/scripts/parse_caiq.py`](../../../ccm-caiq/4.1.0/scripts/parse_caiq.py). It embeds control data from `../ccm-4.1.1.json`, so run this directory's parser first. |

## Rebuilding

Source spreadsheets are gitignored. Pull the workbook from
`s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/ccm/4.1.1/`
into the parent directory, then:

```bash
./parse_ccm.py --input ../CCMv4.1.1-generated_at_2026_10_02.xlsx
python3 ../../check_figures.py
```

`parse_ccm.py` needs pandas and openpyxl. Without them installed, use
`uv run --no-project --with pandas --with openpyxl python parse_ccm.py --input …`.

## Guards that exit 1 by design

The parser refuses a workbook rather than misreading it:

| Guard | Trips when |
|---|---|
| `EXPECTED_VERSION` | the JSON stamp in cell A1 of the `CCM` sheet is not `4.1.1`. Run against the 4.1.0 workbook, it exits with "cell A1 stamps specification_version '4.1.0'". |
| `FRAMEWORK_KEYS` | the merged group-header row of `Scope Applicability (Mappings)` names any framework set other than NIST SP 800-171 rev2 and MITRE ATT&CK, in that order |
| `EXPECTED_REVERSE_HEADER` | the `Reverse Mappings` column headers differ |
| `EXPECTED_REVERSE_SOURCES` | `Reverse Mappings` has a source section other than "Digital Operational Resilience Act", or lacks that one |

If a future release trips one, confirm what CSA changed and record it in that
version's `known_source_issues`. Then adapt a copy of this script in the new
version's directory rather than editing this one, so 4.1.1 stays reproducible.

## What it emits

- **Control fields** have the same names and shapes as in `../../4.1.0/ccm-4.1.0.json`,
  plus `scope_applicability_mappings`, keyed `nist_sp_800_171_rev2` and
  `mitre_attack`. Each holds `control_mapping`, `gap_level` and `addendum`.
  `control_mapping` is verbatim: ATT&CK technique IDs stay newline-separated,
  and `No Mapping` stays a string.
- **`reverse_mappings.dora.provisions[]`** holds `source_reference`,
  `source_description`, `ccm_controls` (a list, split on newlines, commas and
  semicolons; `[]` when blank), `gap_level`, `addendum` and `analysis`.
- **`source_data_notes.sentinel_values`** counts `No Mapping` per framework.
  **`gaps_in_source`** lists empty publisher cells; there are none in 4.1.1.
