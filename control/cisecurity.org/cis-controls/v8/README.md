# CIS Critical Security Controls v8

Center for Internet Security's Critical Security Controls, version 8. 18 Controls organized into 153 Safeguards across three Implementation Groups (IG1 ⊂ IG2 ⊂ IG3).

- **Source:** https://www.cisecurity.org/controls/v8/
- **Source files** (XLSX, not committed — license-restricted): `CIS_Controls_Version_8.xlsx`, `CIS_Controls_v8_Change_Log.xlsx`

## Files

| File | Contents |
|---|---|
| `cis-controls-v8.json` | Controls with nested safeguards (asset type, security function, IGs, description) |
| `cis-controls-v8.csv` | Flat tabular view — one row per Safeguard |
| `cis-controls-v8.md` | Human-readable rendering |
| `cis-controls-v8-changelog.json` | v8 ↔ v7.1 mapping (abridged) and v7.1 deprecated safeguards |
| `scripts/parse_cis.py` | Converter from XLSX |

## Counts

- **18** Controls, **153** Safeguards
- **IG1** = 56 safeguards (basic cyber hygiene baseline)
- **IG2** = 130 safeguards (cumulative; adds 74 to IG1)
- **IG3** = 153 safeguards (cumulative; adds 23 to IG2 — equals the full set)

## Schema

```json
{
  "framework": {"name": "CIS Controls", "version": "8"},
  "controls": [
    {
      "id": "1",
      "title": "Inventory and Control of Enterprise Assets",
      "description": "...",
      "safeguards": [
        {
          "id": "1.1",
          "title": "...",
          "description": "...",
          "asset_type": "Devices",
          "security_function": "Identify",
          "implementation_groups": ["IG1", "IG2", "IG3"]
        }
      ]
    }
  ]
}
```

## Regenerating

```bash
# Default: read XLSX from ~/Downloads/
python3 scripts/parse_cis.py

# Or override the source directory
CIS_V8_SRC=/path/to/xlsx-folder python3 scripts/parse_cis.py
```

The script writes all outputs into this directory. It expects the two files named exactly as CIS publishes them.

## Licensing

The CIS Controls are © Center for Internet Security and licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). The structured derivatives in this directory are kept for internal CSA research and AI analysis only. Source XLSX files must not be added to git.
