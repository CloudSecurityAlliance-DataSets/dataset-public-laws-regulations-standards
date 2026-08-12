# AICM 1.1.1 scripts

| Script | Where |
|---|---|
| `parse_aicm.py` | **here** — rebuilds `../aicm-1.1.1.json` and `../aicm-1.1.1-controls.csv` |
| `parse_caiq.py` | **not here** — use [`../../1.1.0/scripts/parse_caiq.py`](../../1.1.0/scripts/parse_caiq.py) |

## Why there is no `parse_caiq.py` in this directory

The standalone questionnaire shipped in the 1.1.1 bundle is **still versioned
1.1.0** by the publisher — in its filename, its worksheet name, its document
title, its copyright notice, and its `caiq_version` stamp — even though its own
Change Log sheet adds a row labelled "AI-CAIQ v1.1.1". Only two cells in that
whole workbook changed from the 1.1.0-dated copy: the spec-version stamp in A1
and the `SEF-06.1` question text.

So there is no `secid:control/cloudsecurityalliance.org/aicm-caiq@1.1.1` to
build. The questionnaire extraction lives at
[`../../../aicm-caiq/1.1.0/`](../../../aicm-caiq/1.1.0/) and is built by the
1.1.0 copy of the script, which targets that path.

A copy of `parse_caiq.py` was deliberately **not** placed here: it resolves
`../aicm-1.1.0.json` for the AICM control data it merges in, and writes into
`aicm-caiq/1.1.0/`. Sitting in this directory it would look like it produced a
1.1.1 questionnaire and would fail on a path that does not exist.

### Rebuilding the questionnaire against 1.1.1 control data

If you want the questionnaire enriched from the 1.1.1 controls rather than the
1.1.0 ones, override the AICM input. The only field that differs between the two
is the `SEF-06.1` question text — which is the one cell the publisher fixed.

```bash
cd ../../1.1.0/scripts
./parse_caiq.py \
    --input AI_CAIQv1.1.0-star_security_questionnaire-generated_at_2026_07_22.xlsx \
    --aicm-json ../../1.1.1/aicm-1.1.1.json
```

Doing that would overwrite the committed `aicm-caiq/1.1.0/` extraction with one
built from a differently-dated source workbook, so decide first whether
`aicm-caiq` should gain its own directory for the corrected questionnaire. That
question is open — see the note in
[`../README.md`](../README.md) and `source_bundle.notes` in
[`../aicm-1.1.1-metadata.json`](../aicm-1.1.1-metadata.json).

## Rebuilding the AICM extraction

Source spreadsheets are gitignored. Pull from
`s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/aicm/1.1.1/`.

```bash
./parse_aicm.py --input ../AICMv1.1.1-generated_at_2026_07_22.xlsx
```

`parse_aicm.py` discovers the mapping frameworks from the merged group-header row
of the `Scope Applicability (Mappings)` sheet and **exits 1** if they differ from
`EXPECTED_FRAMEWORKS`. That is intentional, and it is what flagged this release:
run against the 19-column 1.1.1 sheet, the 1.1.0 parser refused rather than
reading AIUC-1's mapping into the BSI AI C4 field. If a future release trips it,
confirm what was added or dropped, update the list, and record it in the new
version's `known_source_issues` before re-running.

After any re-run, verify the documented figures still hold:

```bash
python3 ../../crosswalks/check_figures.py
```
