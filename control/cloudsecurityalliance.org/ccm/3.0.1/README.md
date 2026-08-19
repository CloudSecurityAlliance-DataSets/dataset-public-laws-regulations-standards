# CCM v3.0.1

Cloud Controls Matrix v3.0.1 — 133 controls, published 2014-07-11. The last CCM
release before the v4 line.

| file | what |
|---|---|
| `ccm-3.0.1.xlsx` | the source spreadsheet, `CSA_CCM_v3.0.1-09-16-2014.xlsx` as published |
| `build_json.py` | regenerates `ccm-3.0.1.json` from the xlsx; `--check` verifies without writing |
| `ccm-3.0.1.json` | structured extraction, 133 controls |
| `build_csv.py` | flattens the JSON into `ccm-3.0.1.csv` |
| `ccm-3.0.1.csv` | one row per control, nested objects namespaced |
| `ccm-3.0.1.md` | prose rendering |
| `ccm-3.0.1-metadata.json` | dataset metadata |

## Correction, 2026-08-19: four misattributed mapping columns

The previous `ccm-3.0.1.json` carried four keys under `framework_mappings` that
are not framework mappings. All four were column drift across the spreadsheet's
**three-row merged header** (rows 2-4), and there was no generator script, so the
error could not be re-derived or diffed against source.

| old key | true column | what it actually is |
|---|---|---|
| `tenant_consumer` | col14 | Supplier Relationship sub-column; value is the marker `X`. Already correct at `supplier_relationship.tenant_consumer` |
| `csa_enterprise_architecture_formerly_trusted_cloud_initiative_2` | col27 | CSA EA composite's **Public** sub-column; value `shared` |
| `csa_enterprise_architecture_formerly_trusted_cloud_initiative_3` | col28 | CSA EA composite's **Private** sub-column; value `x` |
| `odca_um_pa_r2_0_2` | col47 | ODCA composite's **PA level** sub-column; value `SGP/BSGP` |

The sheet's Scope Applicability section holds **32** real mapping targets, two of
which span several columns and are now nested rather than split:

```json
"csa_enterprise_architecture_formerly_trusted_cloud_initiative": {
  "path": "Application Services > Development Process > Software Quality Assurance",
  "public": "shared",
  "private": "x"
},
"odca_um_pa_r2_0": { "pa_id": "PA17\nPA31", "pa_level": "SGP\nBSGP" }
```

`build_json.py` now **asserts the expected header text at every column it reads**
before parsing a row, and exits non-zero on a mismatch. A positional parser
against a merged header that does not check its headers is how this defect
happened; verify with `python3 build_json.py --check`.

## Two source facts that look like bugs and are not

- **`IVS-13` (Network Architecture) has no mappings at all.** Zero mapping columns
  are filled for it in the spreadsheet. An empty `framework_mappings` is faithful.
- **`DCS-07` separates its domain and title with ` - `**, not a newline, unlike the
  other 132 controls. `build_json.py` handles both, so DCS-07 gets
  `"Datacenter Security"` / `"Secure Area Authorization"` rather than one fused
  string and no title.

## Notes for consumers

- The source writes `-` to mean "no mapping here". That is dropped rather than
  stored, so an absent key is the single encoding of "no mapping".
- `ccm_v1_x` is a mapping target pointing at CCM v1.x, for which no source files
  are published anywhere. It is preserved as published but cannot be resolved.
- `service_delivery_model` (SaaS/PaaS/IaaS) is genuine published data in v3.
