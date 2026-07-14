# C5 — Cloud Computing Compliance Criteria Catalogue (BSI)

Source: https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/kriterienkatalog-c5_node.html

Structured data extracted from BSI's official **editable workbooks**, one CSV/JSON per sheet:

| Edition | Sheets | Notes |
|---|---|---|
| **C5:2020** | `C5_2020_editable-sheet-1-General-Conditions`, `C5_2020_editable-sheet-2-Criteria` | 121 criteria / 17 domains; General Conditions `BC-01…BC-06`. Published under general BSI terms of use. |
| **C5:2026 (v1.0.1)** | `C5_2026_editable-sheet-1-General-Conditions`, `C5_2026_editable-sheet-2-Criteria` | 168 criteria / 17 audited domains → 623 sub-criteria (Basic `B`, Additional/Complementing `AC`, Additional/Sharpening `AS`); General Conditions `GC-01…GC-06`. |

Editable workbooks:
- C5:2020 — https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/CloudComputing/ComplianceControlsCatalogue/2020/C5_2020_editable.html
- C5:2026 — https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/CloudComputing/ComplianceControlsCatalogue/2026/C5_2026_editable.xlsx?__blob=publicationFile&v=1

## License

**C5:2026 is licensed CC BY-ND 4.0** (© Federal Office for Information Security 2026) — https://creativecommons.org/licenses/by-nd/4.0/. Verbatim redistribution with attribution is permitted; NoDerivatives. The CSV/JSON here is a faithful **format-shift** of the editable workbook (criteria text reproduced verbatim, no edits). C5:2020 was published under general BSI terms of use.

## Notes

Excel workbook, saved as CSV (one per sheet), then converted to JSON with `tools-resources/utils/convert-CSV-to-JSON-list.py`.
