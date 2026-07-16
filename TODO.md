# TODO

Repository-wide work items. State as of 2026-05-15 — see [INDEX.md](INDEX.md) for per-doc current state.

## Active work

### Japan — comprehensive source catalog (added 2026-07-16)

Full landscape scan of Japanese cybersecurity/data-protection law, government guidelines, and certification schemes. Existing coverage before this pass: APPI (regulation, full article extraction done in PR #16 but README stale), FISC Security Guidelines / JIS Q-series / Digital Agency My Number / JCB Data Security Program / JPX-JSCC (control, all thin SecID-only stubs, no DataSets content). Everything else below is net-new.

**In progress this pass** (see SOURCES.md "Japan" section for source URLs):
- [x] ~~**ISMAP** (Information system Security Management and Assessment Program)~~ — done 2026-07-16: Control Criteria (2022-04-01 English reference translation) extracted, 263 control-level rows across governance/management/controls tiers; license unresolved (see below); ISMAP-LIU (Low-Impact Use) variant and the JS-rendered Attached Tables 1-8 (incl. SP800-53 crosswalk) still TODO
- [ ] **APPI** — expand: fix stale README (extraction already exists, 73 articles), quality-check article/title/content split, add article-level SecID subpaths
- [x] ~~**Basic Act on Cybersecurity (BAC)** + **NISC/NCO** governance structure~~ — partial, 2026-07-16: SecID entries added (`regulation/cyber.go.jp/basic-act-cybersecurity`, `entity/cyber.go.jp` for NCO/NISC) and a DataSets metadata-only stub (`regulation/cyber.go.jp/basic-act-cybersecurity/`), but **full article text could not be acquired** — the official translation (japaneselawtranslation.go.jp) returns HTTP 403 to curl, WebFetch, and a real Playwright browser session (looks like a network/WAF-level block, not JS-rendering). Retry from a Japan-based network path, or find a mirror.
- [x] ~~**FISC Security Guidelines**~~ — checked 2026-07-16: confirmed members-only/paid (13th edition, Nov 2025), no free full text available. Added a metadata-only stub (`control/fisc.or.jp/security-guidelines/`) citing an unverified third-party (Open Security Architecture) category mapping, and deepened the SecID stub with 3 low-confidence category match_nodes. Full ingestion would require a FISC membership/purchase.

**Primary legislation (regulation type), not yet ingested:**
- [ ] Act on Prohibition of Unauthorised Computer Access (UCAL)
- [ ] Telecommunications Business Act (TBA) — secrecy of communications provisions
- [ ] Act on the Use of Numbers to Identify a Specific Individual (My Number Act) — distinct from APPI; current SecID stub under digital.go.jp only covers the card, not the Act
- [ ] Active Cyber Defense Act / Cyber Response Capabilities Enhancement Act (enacted May 2025, most provisions effective Oct 1 2026)
- [ ] Act on the Protection and Use of Critical Economic Security Information (security clearance system, effective May 2025)
- [ ] Economic Security Promotion Act (critical infrastructure operator designation)
- [ ] Specified Secret Protection Act
- [ ] Unfair Competition Prevention Act (trade secret protection)
- [ ] Payment Services Act
- [ ] Installment Sales Act (credit card data protection provisions)
- [ ] Act on Prevention of Damage Caused by Unauthorized Acts Against Important Computers (effective Oct 1 2026)

**Government/sector guidelines (control type), not yet ingested:**
- [ ] Common Standards on Cybersecurity Measures of Governmental Entities (NISC/CSHQ — baseline for government agencies, analogous to a FedRAMP moderate baseline)
- [ ] Cybersecurity Management Guidelines / CMG (METI + IPA — CISO-level guidance, "3 principles" + "10 important items")
- [ ] Guidelines on Cybersecurity for the Financial Sector (FSA, effective Oct 2024 — 176 response items across governance/risk/defense/detection/third-party risk)
- [ ] Comprehensive Guidelines for the Supervision of Major Banks (FSA)
- [ ] PPC Guidelines regarding the APPI (PPC GL) — implementing guidance with the concrete security-control detail APPI itself lacks
- [ ] Guidelines on Safety Management of Medical Information Systems (MHLW)
- [ ] Guidelines on Safety Management for Providers of Information Systems/Services Handling Medical Information (METI/MIC)
- [ ] Safety Guidelines for Ensuring Information Security — Air Transport / Airport / Railway / Logistics sectors (MLIT, 4 separate documents)
- [ ] Information Security Measures Guidelines for SMEs (IPA — "5 To-dos" + SECURITY ACTION self-declaration program)
- [ ] Guidelines on Preventing Insider Data Breaches (IPA)
- [ ] AI Business Guidelines (MIC/METI, April 2024) + Draft Guidelines on AI Security (MIC, Dec 2025)
- [ ] Cybersecurity Policy for Critical Infrastructure Protection (NISC — defines 15 critical sectors)
- [ ] Supply chain: "Toward Building Partnerships with Business Partners to Enhance Cybersecurity Across the Entire Supply Chain" (METI/JFTC) + Security Measures Evaluation System for Supply Chain Strengthening (★3–★5 tiered assessment, METI, ops planned H2 2026)

**Certification / assessment schemes (control type), not yet ingested:**
- [ ] JC-STAR (Japan Cyber-Security Technical Assessment Requirements) — IoT product evaluation, IPA
- [ ] JISEC (Japan IT Security Evaluation and Certification Scheme) — Common Criteria/ISO 15408 based, IPA/NITE
- [ ] CRYPTREC — cryptographic algorithm evaluation, publishes the CRYPTREC Ciphers List
- [ ] PrivacyMark (P Mark) — JIPDEC, based on JIS Q 15001, roughly Japan's ISO 27001-equivalent trust mark

**Lower priority / needs a decision:**
- [ ] J-CSIP (Initiative for Cybersecurity Information Sharing Partnership of Japan, IPA) — operational info-sharing, may be reference-only
- [ ] Sector-specific narrower items (Medical Care Act cybersecurity enforcement order, Subcontract/Proper Transactions Act) — likely lower standalone value, may fold into parent guideline entries as notes

### Structured parsing for NIST markdown extractions

109 NIST publications have markdown extractions in their stub directories but no structured CSV/JSON. Of those, only 4 have been parsed into per-control/requirement structured form (800-53 r5, 800-171, 800-172, 800-161 r1, 800-82 r3).

Highest-value next candidates (have requirement/control structure suitable for parsing):
- [x] ~~**NIST SP 800-171 r3**~~ — done in PR #24 (95 active + 33 withdrawn = 128 requirements across 17 families)
- [x] ~~**NIST AI 100-1** (AI RMF Core)~~ — done in PR #24 (72 subcategories across 4 Functions)
- [x] ~~**NIST Privacy Framework**~~ — done in PR #24 (100 subcategories across 5 Functions, 18 categories)
- [x] ~~**NIST SP 800-218** (SSDF)~~ — done in PR #24 (47 tasks across 19 practices in 4 groups)
- [x] ~~**NIST SP 800-37 r2**~~ — done in PR #25 (47 tasks across 7 RMF phases)
- [x] ~~**NIST SP 800-66 r2**~~ — done in PR #25 (22 HIPAA-mapped safeguards)
- [x] ~~**NIST SP 800-207**~~ — done in PR #25 (52 sections; narrative guide so section-level rather than per-control)
- [x] ~~**NIST AI 600-1**~~ — done in PR #25 (212 Suggested Actions across 49 AI RMF subcategories)
- [x] ~~**NIST SP 800-63A / 63B / 63C**~~ — done in PR #26 (acquired + section-level parse for each; 60 / 82 / 50 sections respectively across the 3 sub-publications)
- [x] ~~**NIST SP 800-160 v1** Appendix H~~ — done in PR #26 (108 activities + 474 tasks across 30 ISO/IEC/IEEE 15288 processes)
- [x] ~~**FIPS 200**~~ — done in PR #26 (4 body sections + 17 minimum-security control families)
- [ ] **NIST SP 800-160 v2** — Cyber Resiliency (design principles / techniques / approaches — narrative-heavy; lower-value structured parse)
- [ ] **FIPS 199** — Standards for Security Categorization (mostly narrative; minimal structured value)

The remaining ~100 NIST publications are primarily narrative guides (best practices, glossaries, research papers) where per-section parsing is less valuable than the markdown itself.

### Vendor cloud / AI framework content acquisition

Stubs exist with full metadata. Source content + structured extraction still TODO:

- [ ] AWS: Security Best Practices, Security Hub Standards (AWS Well-Architected done in PR #16)
- [ ] Microsoft: Azure Security Benchmark (MCSB), Secure Score
- [ ] Google: SAIF, Frontier Safety Framework, Cloud Architecture Framework, Cloud Security Best Practices
- [ ] OpenAI: Model Spec, Red Teaming Network, System Cards (Preparedness PDF already acquired)
- [ ] Meta: Purple Llama, CyberSecEval
- [ ] IBM: AI Controls Framework
- [ ] Equifax: Controls Framework

### AI safety benchmark content acquisition

All stubs created (PR ~20). Most are GitHub-hosted, so per the upstream-mirror rule we may keep them reference-only and point at the upstream repo rather than bulk-ingesting:

- [ ] safe.ai: HarmBench, WMDP — decide: ingest or reference-only
- [ ] allenai.org: DecodingTrust, RealToxicityPrompts — decide
- [ ] alignment.org: ARC Evals — decide
- [ ] trustllmbenchmark.github.io: TrustLLM — decide
- [ ] jailbreakbench.github.io: JailbreakBench — decide
- [ ] metr.org: METR Task Standard, METR evaluations — decide
- [ ] mlcommons.org: MLCommons AI Safety, Croissant, MLPerf — decide
- [ ] concordia-ai.com: Frontier AI Risk Management Framework — decide

**`github.com/<subnamespace>` audit-script gap**: registry entries under `registry/control/com/github/*.json` (AdvBench, BBQ, WinoBias, StereoSet, CrowS-Pairs, SafetyBench) aren't handled by `audit_secid_alignment.py` which only walks leaf-namespace files. Need to extend it before adding those.

### Confirmed-redistributable licensable ingestion

License research complete (PR #15). These have explicit open licenses verified — candidates for full ingestion:

- [ ] **UK Open Banking Read/Write API + Security Profile** (`openbanking.org.uk`) — MIT License
- [ ] **PolishAPI specification** (`polishapi.org`) — CC BY 3.0 PL
- [ ] **PQCC Migration Roadmap** (`pqcc.org`) — MITRE public-release
- [ ] **Berlin Group NextGenPSD2 PDFs** (`berlin-group.org`) — CC BY-ND 4.0 (originals only, no marker derivatives)
- [ ] **Berlin Group NextGenPSD2 OpenAPI files** (`berlin-group.org`) — CC BY 4.0 (derivatives OK)
- [ ] **FIX Protocol specifications** (`fixtrading.org`) — CC BY-ND 4.0 (originals only)
- [ ] **Auto-ISAC Best Practice Guides** (`automotiveisac.com`) — confirm with publisher first

### Unresolved license terms (need direct contact or PDF inspection)

- [ ] **ISMAP Control Criteria** (`ismap.go.jp`) — ingested 2026-07-16 (`control/ismap.go.jp/control-criteria/2022-04-01/`), no terms-of-use/copyright statement found on the portal; confirm with the ISMAP Secretariat or by inspecting the site footer before treating as publicly redistributable
- [ ] **STET PSD2 API** (`stet.eu`) — inspect spec PDF footer or contact STET
- [ ] **Kantara Consent Receipt Specification** (`kantarainitiative.org`)
- [ ] **OIX Trust Framework methodology** (`openidentityexchange.org`)
- [ ] **BIS Indigenous Indian Standards** (`bis.gov.in`)
- [ ] **PIX** (`bcb.gov.br`) — Brazilian Central Bank, gov publication terms unclear
- [ ] **PromptPay** (`bot.or.th`)
- [ ] **CoDi + SPEI** (`banxico.org.mx`)
- [ ] **PESONet + InstaPay** (`bsp.gov.ph`)
- [ ] **Aadhaar Authentication API** (`uidai.gov.in`) — likely allows citation, bulk redistribution unclear
- [ ] **DigiLocker Integration Specifications** (`digilocker.gov.in`)
- [ ] **IDRBT publications** (`idrbt.ac.in`)

### Acquisition gaps

- [x] ~~**CIRCIA NPRM** structured parse~~ — done in PR #23 (20 sections via `extract_circia.py`)
- [x] ~~**BSI IT-Grundschutz**~~ — Compendium 2022 PDF + cross-reference XLSX acquired; 1,682 requirements across 104 modules / 10 layers consolidated by `extract_it_grundschutz.py` (PR #23). Compendium PDF OOM'd marker on the GPU box; cross-reference XLSX was used as the structured source instead.
- [ ] **NIST SP 800-222** — forthcoming. Synthesizes the NISTIR 8286 series (cybersecurity ERM/SCRM integration). The number was previously thought unpublished because NIST's CSRC catalog shows 800-221 → 800-223, but 800-222 is reserved for this in-development publication. Metadata marked `desired_end_state: metadata-only / pre-release`. Flip to acquired when NIST releases the IPD/FPD.
- [ ] **South Korea PIPA** (`regulation/pipc.go.kr/pipa/`) — Korean government sites (`pipc.go.kr`, `law.go.kr`) return `net::ERR_CONNECTION_CLOSED` from this network, even via playwright headless browser. Likely a TLS-level geo-block on North-America-region IPs. **Plan: retry with NordVPN connected to a South Korean exit node.** Per-doc blocker note is already in the metadata; once acquired, flip `links.acquisition_status` to `acquired` and record the working retrieval URL.

### Filing reconciliations

- [ ] **D3FEND** — registry has it under `control/mitre.org`; repo has it under `ttp/mitre.org/d3fend/`. Resolve to one type.
- [ ] **OWASP AI Exchange** — registry has both `reference/owasp.org` and `control/org/owasp.json`. Repo has the reference; decide canonical type.
- [ ] **HITRUST namespace** — registry has both `control/net/hitrustalliance.json` (newer) and `control/org/hitrust.json` (older). Reconcile to one.

### Metadata enrichment

Bulk-authored stubs (PR ~20) have basic fields populated but `relationToCloudSecurity` / `relationToAISecurity` are often empty:

- [ ] **NIST publications** — fill in cloud-security / AI-security relevance
- [ ] **EU regulations** — add scope, effective dates, key controls
- [ ] **US state regulations** — auto-stubs need scope/jurisdiction details
- [ ] **IEEE stubs** — verify the stub language matches each standard
- [ ] **Best practices / model cards / system cards** — license varies per company; per-doc review

## Pipeline infrastructure

- [ ] **CI auto-regenerate INDEX.md** — currently regenerated manually via `python3 tools-resources/utils/build_index.py`. Wire into a GitHub Actions workflow on PR merge.
- [ ] **Extend `audit_secid_alignment.py`** to walk sub-namespace directories (`registry/control/com/github/*.json`) for path-namespace lookups.

## Plugin

- [ ] **`process-laws-regulations-standards` plugin** in CINO-Plugins — skills for `dataset-ingest`, `dataset-extract`, `dataset-parse`, `dataset-sync`, `dataset-status`. Design discussed previously; will scaffold against the now-stable repo layout.

## Downstream consumers (FYI — for re-pinning after the SecID-mirror reorg)

The V1 mapping deliverable [`CINO-Security-Mapping-CCM-Set-Theory-Mappings`](https://github.com/CloudSecurityAlliance-Internal/CINO-Security-Mapping-CCM-Set-Theory-Mappings) consumes from this repo.

| Framework | New path | Status |
|---|---|---|
| CCM 4.0.13 | `control/cloudsecurityalliance.org/ccm/4.0.13/` | Ready |
| CCM 4.1 | `control/cloudsecurityalliance.org/ccm/4.1/` | Ready |
| CCM 3.0.1 | `control/cloudsecurityalliance.org/ccm/3.0.1/` | Ready |
| AICM 1.0.3 | `control/cloudsecurityalliance.org/aicm/1.0.3/` | Ready |
| NIST CSF 2.0 | `control/nist.gov/csf/2.0/` | Ready |
| NIST CSF 1.1 | `control/nist.gov/csf/1.1/` | Ready |
| PCI DSS v4.0.1 | `control/pcisecuritystandards.org/pci-dss/v4.0.1/` | Ready (222 rows) |
| PCI DSS v3.2.1 | `control/pcisecuritystandards.org/pci-dss/v3.2.1/` | Ready (277 rows) |
| AICPA TSC 2017 | `control/aicpa.org/tsc/2017/` | Ready (68 criteria) |
| CIS Controls v8 | `control/cisecurity.org/cis-controls/v8/` | Ready (153 safeguards) |
| ENX ISA v6 | `control/enx.com/isa/6/` | Ready (80 controls) |
| NIST SP 800-53 r5 | `control/nist.gov/800-53/r5/` | Ready (1,189 entries) |
| NIST SP 800-171 r3 | `control/nist.gov/800-171/` | Ready (structured) |
| NIST SP 800-172 | `control/nist.gov/800-172/` | Ready (35 enhanced reqs — PR #20) |
| NIST SP 800-161 r1 | `control/nist.gov/800-161/r1/` | Ready (191 controls — PR #20) |
| NIST SP 800-82 r3 | `control/nist.gov/800-82/r3/` | Ready (230 OT controls — PR #21) |
| HITRUST CSF v11.3.0 | `control/hitrustalliance.net/csf/v11.3.0/` | Ready (150 controls — PR #20) |
| AWS Well-Architected Security Pillar | `control/amazon.com/well-architected/` | Ready (63 BPs — PR #16) |

## Recently completed (history)

For reference — major items finished in recent PRs:

- **PR #26** (2026-05-17): NIST round 3 — 800-160 v1 SSE Appendix H (108 activities + 474 tasks); 800-63A/B/C Digital Identity acquired + parsed (60/82/50 sections); FIPS 200 (4 body sections + 17 minimum-security control families).
- **PR #25** (2026-05-16): NIST round 2 — 800-37 r2 RMF (47 tasks across 7 phases); 800-66 r2 HIPAA (22 safeguards); 800-207 Zero Trust (52 sections); AI 600-1 GenAI Profile (212 actions across 49 subcategories).
- **PR #24** (2026-05-16): NIST round 1 — 800-171 r3 (95 active + 33 withdrawn); AI RMF Core (72 subcategories); Privacy Framework (100 subcategories); 800-218 SSDF (47 tasks).
- **PR #23** (2026-05-15): One-offs — CIRCIA NPRM structured parse (20 sections); BSI IT-Grundschutz 2022 (1,682 requirements / 104 modules); NIST 800-222 resolved as non-existent.
- **PR #21** (2026-05-15): NIST 800-82 r3 OT controls; UK PSTI; CA SB-327; COPPA; HAVA; CALEA; UK CMA; EO 14028; CIRCIA acquisition. README scope section.
- **PR #20** (2026-05-15): China GenAI Interim Measures; NIST 800-172; NIST 800-161 r1; HITRUST CSF v11.3.0
- **PR #19** (2026-05-14): 5 Canadian provincial laws — Alberta PIPA/HIA, BC PIPA, Ontario PHIPA, Quebec Loi 25
- **PR #17** (2026-05-14): PIPEDA XML re-extraction (12 → 69 sections); Singapore PDPA full extraction (4 → 86); KEV reference-only
- **PR #16** (2026-05-14): 8 priority docs — CTDPA, DPDP, CO CPA, UCPA, APPI, NYDFS 500, AWS WA Security Pillar, NYDFS Part 500
- **Earlier**: ~50 US state privacy laws (CCPA, VCDPA, ...), EU regulations (GDPR, AI Act, NIS2, DORA, DSA, DMA, CRA, Data Act, ePrivacy), national privacy laws (LGPD, APPI, DPDP, PDPA, PIPA-KR, PIPEDA, Australia Privacy Act, UK GDPR, etc.), MITRE namespace metadata, NIST 800-53 r5 + CSF structured, PCI DSS v4.0.1/v3.2.1, AICPA TSC, CIS Controls, ENX ISA, all CCM/AICM versions, US federal laws (HIPAA, FISMA, GLBA, CFAA), CSA frameworks
