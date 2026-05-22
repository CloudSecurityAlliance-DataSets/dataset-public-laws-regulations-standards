# CSA Cloud Security Glossary

Source: <https://cloudsecurityalliance.org/cloud-security-glossary>

The Cloud Security Alliance's consolidated cloud-security glossary, aggregating
terminology from CSA research publications (Enterprise Architecture Reference
Guide, SDP, Zero Trust, CCM, AI working-group output, etc.) and external
authoritative sources.

## Inclusion authority

The source page footer reads "© 2009-2026 Cloud Security Alliance. All rights
reserved." CSA is both the publisher and the rights-holder. Inclusion in this
public dataset is authorized by CSA leadership as part of the CSA-maintained
`dataset-public-laws-regulations-standards` repository.

The license SPDX is `LicenseRef-CSA-Authorized-Redistribution`. Downstream
redistribution by third parties remains subject to CSA's standard copyright
terms; consult CSA for licensing beyond use within CSA-maintained datasets.

## Files

- `cloud-security-glossary.md` — human-readable A-Z listing
- `cloud-security-glossary-terms.json` — structured term list (1,119 entries)
- `cloud-security-glossary-terms.csv` — same data, CSV form
- `extract_cloud_security_glossary.py` — reproducibility script
- `_source.html` — cached raw HTML from the CSA site (re-downloaded with
  `--refresh`)
- `cloud-security-glossary-metadata.json` — SecID + license metadata

## Refreshing

```bash
python3 extract_cloud_security_glossary.py --refresh
```

This re-downloads the live HTML and regenerates all outputs. After refreshing,
re-run the repo's audit + index scripts from the repo root:

```bash
python3 tools-resources/utils/audit_secid_alignment.py
python3 tools-resources/utils/build_index.py
```
