# TODO

Repository-wide work items. State as of the latest INDEX.md regeneration — see [INDEX.md](INDEX.md) for per-doc current state.

## High-value, still outstanding

### ~~NIST SP 800-53 r5 structured extraction~~ (done — PR #21)

- [x] **`control/nist.gov/800-53/r5/`** — extracted 1,189 entries (322 base + 867 enhancements) across 20 families directly from the NIST-published XLSX. CCM↔800-53 r5 mapping pair in [`CINO-Security-Mapping-CCM-Set-Theory-Mappings`](https://github.com/CloudSecurityAlliance-Internal/CINO-Security-Mapping-CCM-Set-Theory-Mappings) is now unblocked.

### Metadata enrichment

A bulk-author run (PR ~20) created basic `<name>-<version>-metadata.json` for every doc dir that lacked one. The auto-generated entries have:
- secid, name, version, owner, type, license, source URL
- description (best-effort, sometimes placeholder)
- empty `relationToCloudSecurity` / `relationToAISecurity`

These need human enrichment per-doc:
- [ ] **NIST publications** — descriptions are based on title; fill in cloud-security / AI-security relevance
- [ ] **EU regulations** — descriptions are titles only; add scope, effective dates, key controls
- [ ] **US state regulations** — auto-stubs need scope/jurisdiction details
- [ ] **IEEE stubs** — verify the stub language matches each standard
- [ ] **MITRE namespace docs** — not yet bulk-authored (license per source varies); manual per-doc
- [ ] **Best practices / model cards / system cards** — not yet bulk-authored; license varies per company

### ~~MITRE namespace metadata~~ (done)

Authored per-doc metadata for all 13 MITRE doc directories with accurate licenses:
- [x] `weakness/mitre.org/cwe/4.19.1/` — MITRE CWE Terms of Use (attribution required)
- [x] `weakness/mitre.org/maec/` — MITRE Terms (project inactive; ATT&CK supersedes)
- [x] `ttp/mitre.org/attack/` — MITRE ATT&CK Terms of Use (Apache-2.0 for code, attribution for data)
- [x] `ttp/mitre.org/atlas/` — Apache-2.0 (atlas-data GitHub repo)
- [x] `ttp/mitre.org/capec/` — MITRE CAPEC Terms of Use
- [x] `ttp/mitre.org/d3fend/` — MITRE D3FEND Public Release (NSA-sponsored)
- [x] `ttp/mitre.org/fight/` — MITRE FiGHT Terms of Use
- [x] `reference/mitre.org/cpe/` — NIST Public Domain (CPE moved to NIST in 2014)
- [x] `reference/mitre.org/oval/` — CIS OVAL (moved to CIS in 2017)
- [x] `reference/mitre.org/stix-taxii/` — OASIS CTI TC Standard
- [x] `reference/mitre.org/cve-program/` — CC0-1.0 (CVE Records are public domain)
- [x] `reference/mitre.org/cve-program/cna-partners/` — derived dataset (CC0 source)
- [x] `reference/mitre.org/ctid/` — Apache-2.0 (CTID mappings-explorer)

## Standards completion

All 12 from the original list (per [INDEX.md](INDEX.md)):

| Standard | Status |
|---|---|
| NIST SP 800-53 r5 | ✅ Fully structured (XLSX-sourced, 1,189 entries) + metadata |
| NIST CSF v2.0 | ✅ Fully structured + metadata |
| NIST CSF v1.1 | ✅ Fully structured + metadata |
| AICPA TSC 2017 | ✅ Fully structured + metadata |
| CIS Critical Security Controls v8.0 | ✅ Fully structured + metadata |
| ISF SOGP 2022 | ✅ Info-only stub (members-only license) |
| ENX ISA v6.0 | ✅ Fully structured + metadata |
| PCI DSS v4.0 | Legacy markdown + metadata |
| PCI DSS v4.0.1 | ✅ Fully structured + metadata |
| PCI DSS v3.2.1 | ✅ Fully structured + metadata |
| CCM v3.0.1 | ✅ Fully structured + metadata |

## Pipeline infrastructure

- [x] ~~**`pdf_to_md_via_gpu.sh` Mac-side wrapper**~~ — added in `tools-resources/utils/pdf_to_md_via_gpu.sh`; deploys canonical `marker-convert.sh` on every run, polls remote log for `STATUS: DONE`, scp's results back.
- [x] ~~**Fix `~/marker-convert.sh` bugs**~~ — canonical fixed copy lives at `tools-resources/utils/marker-convert.sh`: single-pass markdown by default (was 3-pass), `--force-ocr` opt-in (was always on), doubled-logging removed. Wrapper redeploys it to the GPU box automatically.
- [ ] **CI auto-regenerate INDEX.md** — currently regenerated manually via `python3 tools-resources/utils/build_index.py`. Wire into a GitHub Actions workflow on PR merge.
- [x] ~~**Parser fixes**~~:
  - ~~PCI DSS v3.2.1 Appendix A1/A2 tables (use non-standard column headers; not currently captured)~~ — fixed in PR #22 (254 → 277 requirements; A3.1.3 and A3.2.2.1 still missing due to marker table-split artifact, documented in metadata)
  - ~~AICPA TSC missing criterion (CC1.3 — small parsing gap)~~ — actually 6 missing criteria (CC1.3, CC2.3, CC6.8, CC7.1, CC7.2, C1.2) all due to marker page-break layout artifacts. Restored via `tsc-2017-recovered-criteria.json` patch file the parser merges in. Total now 68 (was 62), Common Criteria complete at 33.

## SecID registry additions

These data-repo entries need corresponding namespace entries in [SecID](https://github.com/CloudSecurityAlliance/SecID):

- [ ] `enx.com` — for ENX ISA v6 (TISAX)
- [ ] `aiuc.com` — for AIUC-1 (need to verify the actual publisher's domain first)

## Plugin

- [ ] **`process-laws-regulations-standards` plugin** in CINO-Plugins — skills for `dataset-ingest`, `dataset-extract`, `dataset-parse`, `dataset-sync`, `dataset-status`. Design discussed previously; will scaffold against the now-stable repo layout.

## Downstream consumers (FYI)

The V1 mapping deliverable [`CINO-Security-Mapping-CCM-Set-Theory-Mappings`](https://github.com/CloudSecurityAlliance-Internal/CINO-Security-Mapping-CCM-Set-Theory-Mappings) consumes from this repo. **All paths changed in the SecID-mirror reorg.** Re-pin needed:

| Framework | New path | Status |
|---|---|---|
| CCM 4.0.13 | `control/cloudsecurityalliance.org/ccm/4.0.13/` | Ready |
| CCM 4.1 | `control/cloudsecurityalliance.org/ccm/4.1/` | Ready |
| CCM 3.0.1 | `control/cloudsecurityalliance.org/ccm/3.0.1/` | Ready (fully structured + metadata) |
| AICM 1.0.3 | `control/cloudsecurityalliance.org/aicm/1.0.3/` | Ready |
| NIST CSF 2.0 | `control/nist.gov/csf/2.0/` | Ready (with full metadata) |
| NIST CSF 1.1 | `control/nist.gov/csf/1.1/` | Ready (with full metadata) |
| PCI DSS v4.0.1 | `control/pcisecuritystandards.org/pci-dss/v4.0.1/` | Ready (with full metadata + 222-row structured CSV/JSON) |
| PCI DSS v3.2.1 | `control/pcisecuritystandards.org/pci-dss/v3.2.1/` | Ready (with full metadata + 254-row structured CSV/JSON) |
| AICPA TSC 2017 | `control/aicpa.org/tsc/2017/` | Ready (62 criteria) |
| CIS Controls v8 | `control/cisecurity.org/cis-controls/v8/` | Ready (153 safeguards) |
| ENX ISA v6 | `control/enx.com/isa/6/` | Ready (80 controls) |
| NIST SP 800-53 r5 | `control/nist.gov/800-53/r5/` | Ready (with full metadata + 1,189-entry structured CSV/JSON) |
