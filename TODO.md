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

## Licensable-candidate ingestion

License research completed 2026-05-14 for candidates identified during the `dataset-private-laws-regulations-standards` audit rounds. Results below are split into **confirmed-redistributable** (ready to ingest), **free-access-but-restricted** (stay as SecID-only), and **unresolved** (need direct contact or PDF inspection).

### Confirmed redistributable — ingestion candidates

These have explicit open licenses verified at the publisher's site. Each is a candidate for full ingestion (PDFs and/or derivatives, subject to per-license modification rules).

- [ ] **UK Open Banking Read/Write API + Security Profile** (`openbanking.org.uk`) — **MIT License**, © Open Banking Limited 2023. Most permissive. Full ingestion (originals + extracted markdown + structured derivatives) all allowed. Companion SecID entry at `registry/control/uk/org/openbanking.json`.
- [ ] **PolishAPI specification** (`polishapi.org`) — **Creative Commons Attribution 3.0 Poland**. Full ingestion allowed; attribution required. SecID at `registry/control/org/polishapi.json`.
- [ ] **PQCC Migration Roadmap** (`pqcc.org`) — MITRE public-release language: "Approved for Public Release; Distribution Unlimited" (Case 24-1154). Effectively unrestricted redistribution. SecID at `registry/control/org/pqcc.json`.
- [ ] **Berlin Group NextGenPSD2 PDFs** (`berlin-group.org`) — **CC BY-ND 4.0 International** for the specification PDFs. Redistribution of unmodified originals permitted with attribution. **Cannot run through marker for markdown extraction** (that's a derivative — prohibited under ND). SecID at `registry/control/org/berlin-group.json`.
- [ ] **Berlin Group NextGenPSD2 OpenAPI files** (`berlin-group.org`) — Same publisher but separate license: **CC BY 4.0 International** (no ND restriction). Derivatives, transformations, and reformatting all allowed. Worth ingesting these separately from the PDFs.
- [ ] **FIX Protocol specifications** (`fixtrading.org`) — **CC BY-ND 4.0 International**, © FIX Protocol Ltd. Redistribution of unmodified originals permitted with attribution. **Cannot run through marker for markdown extraction** under ND. SecID at `registry/control/org/fixtrading.json`.
- [ ] **Auto-ISAC Best Practice Guides (6 guides)** (`automotiveisac.com`) — Publicly downloadable from `/best-practice-guides`; framed as "voluntarily adopted, not required". **No explicit redistribution license** stated, so direct confirmation with Auto-ISAC recommended before bulk-mirroring. Likely permissive given the public-availability stance. SecID at `registry/control/com/automotiveisac.json`.

### Free-access-but-restricted — stay as SecID-only

These are free to download for personal use but publishers explicitly retain copyright and require permission for redistribution. Identity records remain in SecID; content stays out of this repo.

- **ETSI deliverables** (`etsi.org`) — Including EN 303 645 (consumer IoT cyber), ISG QSC quantum-safe series (TS 103 744 etc.), and the broader TC CYBER catalogue. Free download, ETSI copyright retained. SecID at `registry/control/org/etsi.json`. Same posture as AICPA TSC.
- **ITU-T Recommendations** (`itu.int`) — Free download at `itu.int/rec/T-REC/`. ITU retains copyright; reproduction requests go to `jur@itu.int` per `https://www.itu.int/en/Pages/copyright.aspx`. SecID at `registry/control/int/itu.json`.

### Unresolved — need direct contact or PDF inspection

License terms could not be determined from publisher websites during automated checking. Each needs a manual check (download a sample PDF and read the footer / contact the publisher).

- [ ] **STET PSD2 API** (`stet.eu`) — Resources page lists downloadable PDFs/YAML/JSON but no license stated; "Legals" page returned 404. Inspect a downloaded spec PDF for license footer or contact STET.
- [ ] **Kantara Consent Receipt Specification** (`kantarainitiative.org`) — Policy and permanent-documents URLs returned 404. The spec PDF itself likely carries a license statement; download and inspect, or contact `hello@kantarainitiative.org`.
- [ ] **OIX Trust Framework methodology** (`openidentityexchange.org`) — Policies page returned 403 (auth-gated). Need a direct PDF inspection or member-list query.
- [ ] **BIS Indigenous Indian Standards** (`bis.gov.in`) — Their portal at `standardsbis.bsbedge.com` advertises "Indigenous Indian Standards can be downloaded free of cost" but doesn't publish explicit redistribution terms. ISO/IEC adoptions remain subject to ISO terms regardless. Contact BIS or inspect a downloaded indigenous-IS PDF.

### Important nuance: derivatives vs. originals under CC BY-ND

Three of the confirmed-redistributable sources are CC BY-ND (NoDerivatives): Berlin Group NextGenPSD2 PDFs and FIX Protocol. The ND clause means we can host the original PDFs but **cannot extract them to markdown** (the standard pipeline produces derivatives). For these, the path is:

- Commit the PDF as the canonical artefact (with attribution metadata)
- Skip the marker → markdown → controls.json pipeline
- Note `"derivatives_extracted": false` in the metadata

UK OBIE (MIT), PolishAPI (CC BY 3.0), PQCC (public release), and Berlin Group OpenAPI files (CC BY 4.0) all permit derivatives, so the full extraction pipeline can run.

## Source PDF acquisition (2026-05-13 sweep)

84 source PDFs auto-downloaded from canonical publishers and placed in their stub directories (gitignored). Marker extraction is the next step — feed each through `pdf_to_md_via_gpu.sh` to produce markdown/JSON.

**Acquired (84):**
- NIST: 800-12, 39, 40, 46, 52, 53a, 57 (pt1/2/3), 66, 77, 82, 83, 84, 86, 92, 94, 100, 111, 115, 122, 124, 125, 126, 128, 131a, 145, 146, 150, 153, 160-v1, 160-v2, 167, 171, 172, 177, 181, 184, 188, 190, 201, 204, 207, 209, 210, 213, 213a, 216, 218, 219, 221, 223, 224, 227 (53 SP), FIPS 180/186/197/198/201/202/203/204/205 (9), AI 100-4, Privacy Framework, IR 7621/8062/8228/8259/8276/8286/8374/8425/8454 (9), CSWP 30/32/33 (3) = 76
- CPE (NIST IR 7695 spec)
- HIPAA, GLBA, FISMA, CFAA (US federal laws via govinfo.gov PLAW + USCODE)
- Colorado AI Act (CO leg)
- OpenAI Preparedness Framework

**Still need acquisition (skipped — vendor landing pages, no direct PDF link in metadata):**

Vendor cloud frameworks (HTML-only published — would need manual download or marker on HTML):
- [ ] AWS: Well-Architected, Security Best Practices, Security Hub Standards
- [ ] Microsoft: Azure Security Benchmark (MCSB), Secure Score
- [ ] Google: SAIF, Frontier Safety, Cloud Architecture Framework, Cloud Security Best Practices
- [ ] OpenAI: Model Spec, Red Teaming Network, System Cards (Preparedness already acquired)
- [ ] Meta: Purple Llama, CyberSecEval
- [ ] IBM: AI Controls Framework
- [ ] Equifax: Controls Framework

AI safety benchmarks (mostly GitHub READMEs):
- [ ] HarmBench, WMDP, JailbreakBench, TrustLLM, DecodingTrust, RealToxicityPrompts, ARC Evals, METR Task Standard / Evaluations, MLCommons (AI Safety / Croissant / MLPerf), Concordia Frontier AI RMF

National AI frameworks:
- [ ] Singapore: AI Verify, Model AI Governance Framework
- [ ] China: TC260 AI Safety Governance Framework

Industry frameworks (members/paid):
- [ ] COBIT (ISACA — login required)
- [ ] ITIL (AXELOS — paid)
- [ ] SWIFT CSP (SWIFT customer login)
- [ ] PCI: PCI PIN, PA-DSS (retired), Secure Software Standard (PCI SSC click-through)

National privacy laws (varied: many use HTML legislation portals):
- [ ] Brazil LGPD (planalto.gov.br — HTML)
- [ ] Japan APPI (ppc.go.jp — HTML)
- [ ] India DPDP (meity.gov.in — HTML)
- [ ] Singapore PDPA (pdpc.gov.sg — HTML)
- [ ] Korea PIPA (pipc.go.kr — HTML)
- [ ] Canada PIPEDA (laws-lois.justice.gc.ca — needs direct URL)
- [ ] Australia Privacy Act 1988 (oaic.gov.au — HTML, federalregister text)
- [ ] UK GDPR, DPA 2018, NIS Regs (legislation.gov.uk — HTML)
- [ ] California CalOPPA (leginfo — HTML)
- [ ] NY: NYDFS 500, SHIELD Act, NYBCL (varied sources)

EU regulations (WAF-blocked from automated curl — EUR-Lex anti-bot):
- [ ] NIS2, DSA, DMA, Data Act, CRA, ePrivacy — all returned EUR-Lex CloudFront WAF challenge. May work from a browser; use a session cookie or manual download.

CISA programs (JSON feeds rather than PDFs):
- [ ] KEV (JSON feed at cisa.gov/known-exploited-vulnerabilities.json)
- [ ] CPGs, SCuBA (HTML / mixed)

Reference docs (HTML-only or registered):
- [ ] CIS OVAL (HTML site)
- [ ] OASIS STIX/TAXII (HTML specs)
- [ ] MITRE ATT&CK, ATLAS, CAPEC, MAEC (HTML / STIX JSON, not PDF)

NIST stragglers:
- [ ] 800-222 (Web App Pen Testing — IPD; URL pattern may have moved)

BSI:
- [ ] IT-Grundschutz (BSI portal, requires navigation)

Next steps:
- Feed the 84 acquired PDFs through `pdf_to_md_via_gpu.sh` for marker extraction
- For HTML-only docs, can use `convert-HTML-to-Markdown.py` after fetching pages with a real browser (Playwright)
- For EUR-Lex WAF-blocked items, manual download via browser is fastest

## Content gaps (publicly-redistributable docs in SecID registry but not in repo)

Gap analysis 2026-05: SecID registry lists these publicly-available standards/regulations that aren't here yet. Excludes ISO/IEEE/ISF-SOGP/HITRUST (licensed; private repo or stubs only).

### ⭐ Highest-impact (laws and regulations)

**US federal laws** (`regulation/govinfo.gov` — namespace exists, zero docs):
- [ ] **HIPAA** — Health Insurance Portability and Accountability Act
- [ ] **FISMA** — Federal Information Security Management Act
- [ ] **GLBA** — Gramm-Leach-Bliley Act
- [ ] **CFAA** — Computer Fraud and Abuse Act

**EU** (`regulation/europa.eu` — namespace covered, doc missing):
- [ ] **NIS2** — Network and Information Security Directive 2

**New York** (`regulation/ny.gov` — only LL144 in repo):
- [ ] **NYDFS Cybersecurity Regulation (23 NYCRR 500)** — heavily referenced in financial services
- [ ] **SHIELD Act** — Stop Hacks and Improve Electronic Data Security Act
- [ ] **NYBCL** — New York Biometric Collection Law

**State laws** (registered namespaces, docs missing):
- [ ] **CalOPPA** — California Online Privacy Protection Act
- [ ] **Colorado AI Act** — first US state AI law of consequence (`colorado.gov` has CPA but not the AI Act)
- [ ] **Massachusetts AI bills** (`mass.gov`)
- [ ] **Maryland facial recognition statutes** (`maryland.gov`)
- [ ] **Nevada SB 220/260 privacy amendments** (`nv.gov`)
- [ ] **Washington My Health My Data Act** (`wa.gov`)
- [ ] **Florida biometric privacy provisions** (`florida.gov`)

### ~~Vendor cloud / AI control frameworks~~ (stubs done — content TODO)

All stubs created with full metadata + READMEs. Source content acquisition + structured extraction is the next step per doc.

**AWS** (`control/amazon.com`):
- [x] AWS Well-Architected Framework, Security Best Practices, Security Hub Standards (3 stubs)

**Microsoft** (`control/microsoft.com`):
- [x] Microsoft Cloud Security Benchmark (MCSB), Secure Score (2 stubs)

**Google** (`control/google.com`):
- [x] SAIF, Frontier Safety Framework, Cloud Architecture Framework, Cloud Security Best Practices (4 stubs)

**OpenAI / Meta / IBM / Equifax**:
- [x] OpenAI Model Spec, Preparedness, Red Teaming Network, System Cards (4 stubs)
- [x] Meta Purple Llama, CyberSecEval (2 stubs)
- [x] IBM Generative AI Controls Framework (1 stub)
- [x] Equifax Controls Framework (1 stub)

### ~~National government AI frameworks~~ (stubs done — content TODO)

- [x] Singapore: AI Verify, Model AI Governance Framework (`control/imda.gov.sg`) — 2 stubs
- [x] China: AI Safety Governance Framework (`control/tc260.org.cn`) — 1 stub
- [x] EU control-type: ALTAI, Ethics Guidelines for Trustworthy AI (`control/europa.eu`) — 2 stubs

### ~~AI safety benchmarks~~ (most stubs done — content TODO)

Stubs created for non-path-namespace registry entries:
- [x] safe.ai: HarmBench, WMDP (2 stubs)
- [x] allenai.org: DecodingTrust, RealToxicityPrompts (2 stubs)
- [x] alignment.org: ARC Evals (1 stub)
- [x] trustllmbenchmark.github.io: TrustLLM (1 stub)
- [x] jailbreakbench.github.io: JailbreakBench (1 stub)
- [x] metr.org: METR Task Standard, METR frontier model evaluations (2 stubs)
- [x] mlcommons.org: MLCommons AI Safety, Croissant, MLPerf (3 stubs)
- [x] concordia-ai.com: Frontier AI Risk Management Framework (1 stub)

**Deferred** — `github.com/<subnamespace>` registry entries use path-namespaces that the current `audit_secid_alignment.py` doesn't handle (it derives leaf-only namespace files, not nested sub-paths). Need to extend the audit script before adding these:
- [ ] github.com/llm-attacks: AdvBench
- [ ] github.com/nyu-mll: BBQ, WinoBias, StereoSet, CrowS-Pairs
- [ ] github.com/thu-coai: SafetyBench
- [ ] **Tooling:** extend `audit_secid_alignment.py` to walk into sub-namespace directories (registry/control/com/github/*.json) for path-namespace lookups

### Filing reconciliations

- [x] ~~**AIDA**~~ — consolidated under `parl.ca` (Parliament of Canada is legal publisher); `canada.ca/aida` deprecated with redirect_to.
- [ ] **D3FEND** — registry has under `control/mitre.org`; repo has under `ttp/mitre.org/d3fend/`. Resolve to one type.
- [ ] **OWASP AI Exchange** — registry has under both `reference/owasp.org` and `control/org/owasp.json` (as "AI Exchange Controls"). Repo has the reference. Decide on canonical type and possibly add the controls view.
- [ ] **HITRUST** — registry has both `control/net/hitrustalliance.json` (added recently) and `control/org/hitrust.json` (older). Reconcile to one.

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
