# Control Criteria of ISMAP (2022-04-01 English reference translation)

Japan's ISMAP (Information system Security Management and Assessment Program) — the government cloud security assessment and registration program, jointly operated by NISC, the Digital Agency, MIC, and METI. Direct analogue to FedRAMP (US) or BSI C5 (Germany): government agencies are, in principle, required to procure cloud services from the ISMAP Cloud Service List.

The Control Criteria document defines what cloud service providers must implement to register. It has three tiers:

- **Governance criteria** (Chapter 3) — based on JIS Q 27014:2015 / ISO/IEC 27014:2013
- **Management criteria** (Chapter 4) — based on JIS Q 27001:2014 / ISO/IEC 27001:2013
- **Controls criteria** (Chapter 5) — uses the same 14-domain clause numbering as JIS Q 27002:2014 / ISO/IEC 27002:2013 (domains 5–18), with cloud-specific additions from ISO/IEC 27017:2015 marked `.P`/`.B`/`.PB` on the control ID

- **Source:** https://www.ismap.go.jp/
- **Source file (gitignored, license unclear):** `ismap-control-criteria-2022-04-01.pdf` — English reference translation, downloaded from `https://www.ismap.go.jp/csm/sys_attachment.do?sys_id=bb71912b1b985910f18c65fa234bcb9f`
- **License status:** ⚠️ unresolved — see metadata.json `license` block and TODO.md. Treat as internal working data until confirmed.

## Files

| File | Contents |
|---|---|
| `ismap-control-criteria-2022-04-01-metadata.json` | Directory metadata (schema per METADATA-SCHEMA.md) |
| `ismap-control-criteria-2022-04-01.json` | 263 control-level rows, structured |
| `ismap-control-criteria-2022-04-01.csv` | Same, flat CSV |
| `ismap-control-criteria-2022-04-01-raw.txt` | `pdftotext -layout` output of the (decrypted) source PDF — narrative reference |
| `parse_ismap.py` | ID-anchored parser: narrative text → flat entries keyed by numeric ID depth |
| `extract_ismap.py` | Assembles the final dataset from `parse_ismap.py`'s output (domain/category/objective lookups, cloud-specific flag, ISO cross-reference extraction) |

## Schema

```json
{
  "criteria_type": "controls",
  "domain_id": "9",
  "domain_title": "Access control",
  "category_id": "9.2",
  "category_title": "User access management",
  "control_objective": "To ensure authorized user access and to prevent unauthorized access to systems and services.",
  "control_id": "9.2.3.11.PB",
  "is_cloud_specific": true,
  "iso_reference": "27017",
  "control_text": "Depending on the identified risks, cloud service providers provide sufficiently strong authentication technologies for administrator authentication of cloud service customers that are tailored to the management capabilities of the cloud service."
}
```

## Important scope caveat

Most base-control entries (e.g., `9.2.1`) are **cross-references** to the corresponding ISO/IEC 27002:2013 control — the copyrighted ISO text itself is not reproduced here, only the ID, its category, and the control objective. The cloud-specific sub-controls (`.P`/`.B`/`.PB` suffix, 38 of 263 rows) generally do carry original descriptive text, since those are ISMAP/ISO 27017-Annex-A-specific additions layered on the base ISO structure.

The document also references separate **Attached Tables 1–8** (full tabular control listing, and crosswalks to Japan's Common Standards and to NIST SP 800-53 rev.4) that are **not included** in this extraction — they're served from the JS-rendered (ServiceNow) `ismap.go.jp` portal and weren't retrievable via plain HTTP fetch. A future pass with Playwright/Chrome DevTools MCP could add them; see TODO.md.

## Regenerating

```bash
# From the source PDF (already decrypted with `qpdf --decrypt`):
pdftotext -layout ismap-control-criteria-2022-04-01.pdf ismap-control-criteria-2022-04-01-raw.txt
python3 parse_ismap.py       # narrative text -> ismap-parsed-raw.json (intermediate, not committed)
python3 extract_ismap.py     # -> ismap-control-criteria-2022-04-01.{json,csv}
```
