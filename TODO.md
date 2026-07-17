# TODO

Repository-wide work items. State as of 2026-05-15 — see [INDEX.md](INDEX.md) for per-doc current state.

## Active work

### Japan — comprehensive source catalog (added 2026-07-16)

Full landscape scan of Japanese cybersecurity/data-protection law, government guidelines, and certification schemes. Existing coverage before this pass: APPI (regulation, full article extraction done in PR #16 but README stale), FISC Security Guidelines / JIS Q-series / Digital Agency My Number / JCB Data Security Program / JPX-JSCC (control, all thin SecID-only stubs, no DataSets content). Everything else below is net-new.

**Batch 1** (see SOURCES.md "Japan" section for source URLs):
- [x] ~~**ISMAP** (Information system Security Management and Assessment Program)~~ — done 2026-07-16: Control Criteria (2022-04-01 English reference translation) extracted, 263 control-level rows across governance/management/controls tiers; license unresolved (see below); ISMAP-LIU (Low-Impact Use) variant and the JS-rendered Attached Tables 1-8 (incl. SP800-53 crosswalk) still TODO
- [x] ~~**APPI**~~ — done 2026-07-16: fixed stale README, fixed a title/content misalignment bug in the extraction (73 -> 81 of 88 articles recovered), added article-level SecID subpaths (`#art-N`)
- [x] ~~**Basic Act on Cybersecurity (BAC)** + **NISC/NCO** governance structure~~ — partial, 2026-07-16: SecID entries added (`regulation/cyber.go.jp/basic-act-cybersecurity`, `entity/cyber.go.jp` for NCO/NISC) and a DataSets metadata-only stub (`regulation/cyber.go.jp/basic-act-cybersecurity/`), but **full article text could not be acquired** — the official translation (japaneselawtranslation.go.jp) returns HTTP 403 to curl, WebFetch, and a real Playwright browser session (looks like a network/WAF-level block, not JS-rendering). Retry from a Japan-based network path, or find a mirror.
- [x] ~~**FISC Security Guidelines**~~ — checked 2026-07-16: confirmed members-only/paid (13th edition, Nov 2025), no free full text available. Added a metadata-only stub (`control/fisc.or.jp/security-guidelines/`) citing an unverified third-party (Open Security Architecture) category mapping, and deepened the SecID stub with 3 low-confidence category match_nodes. Full ingestion would require a FISC membership/purchase.

**Batch 2 (2026-07-16)** — SecID coverage complete for all 30 items (PR CloudSecurityAlliance/SecID#116). **Follow-up acquisition pass (same day)** closed most of the DataSets gap the first pass left open: the "blocked to automated fetch" findings were mostly bot/WAF protection, not genuine unavailability — a real Playwright browser session bypassed `meti.go.jp` and `jftc.go.jp` (fetch their PDF bytes via an in-page `fetch()` call, save via base64 round-trip), and the "image-heavy" MLIT PDFs turned out to extract perfectly cleanly with plain `pdftotext -layout` (the original assessment was an artifact of WebFetch's weaker built-in extraction, not the documents themselves). **24 of 30 items now have real acquired text in DataSets** (mix of full-text and partial/excerpt — see each directory's README). Only `japaneselawtranslation.go.jp` remained genuinely blocked even to a real browser (confirmed persistent, likely network/WAF-level, not a JS-rendering issue) — that domain is the sole remaining blocker, affecting 5 items below.

**Primary legislation (regulation type):**
- [x] UCAL — `secid:regulation/cas.go.jp/ucal`. **Still blocked** — only source is japaneselawtranslation.go.jp (persistent 403, confirmed via real Playwright browser). No DataSets content.
- [x] ~~Telecommunications Business Act~~ — `regulation/soumu.go.jp/telecommunications-business-act/`. **Full text acquired** (MIC's alternate English PDF). Caveat: this translation is an outdated ~2007 revision, not current law.
- [x] ~~My Number Act~~ — `regulation/digital.go.jp/my-number-act/`. **Full text acquired**, 76 articles structured into JSON/CSV (PPC-hosted PDF; a plain local `pdftotext` succeeded where the earlier WebFetch-based attempt failed). Known issue: main-body vs. supplementary-provisions (附則) article-numbering collisions in a few entries — not yet manually verified.
- [x] ~~Active Cyber Defense Act~~ — `regulation/cyber.go.jp/active-cyber-defense-act/`. **Structure acquired** (Japanese chapter/article TOC, rendered via Playwright from e-Gov's JS app — plain fetch only got the empty app shell). No official English translation exists yet; full article body text still TODO.
- [ ] Act on the Protection and Use of Critical Economic Security Information — `secid:regulation/cao.go.jp/economic-security-information`. **Still blocked** (only a government outline exists, on japaneselawtranslation.go.jp). No DataSets content.
- [x] ~~Economic Security Promotion Act~~ — `regulation/cao.go.jp/economic-security-promotion/`. **Overview acquired** (Cabinet Office English PDF) — not full statutory text, which remains blocked.
- [x] ~~Specified Secret Protection Act~~ — `regulation/cas.go.jp/specified-secret-protection/`. **Overview acquired** (Cabinet Secretariat 5-page English PDF) — not full statutory text, which remains blocked.
- [ ] Unfair Competition Prevention Act — `secid:regulation/meti.go.jp/unfair-competition-prevention`. **Still blocked** (japaneselawtranslation.go.jp; WIPO Lex mirror is JS-rendered, only captured site nav, not the actual text). No DataSets content.
- [ ] Payment Services Act — `secid:regulation/fsa.go.jp/payment-services-act`. **Still blocked**, no alternate source found. No DataSets content.
- [ ] Installment Sales Act — `secid:regulation/meti.go.jp/installment-sales`. **Still blocked**, no alternate source found. No DataSets content.

**Government/sector guidelines (control type) — all acquired:**
- [x] ~~Common Standards for Government Entities~~ — `control/cyber.go.jp/common-standards/`. **Full text acquired** (GPKI-encrypted PDF, decrypted with `qpdf --decrypt` then `pdftotext -layout`).
- [x] ~~Cybersecurity Management Guidelines / CMG~~ — `control/meti.go.jp/cybersecurity-management-guidelines/`. **Full text acquired** via the Playwright/meti.go.jp bypass.
- [x] ~~Guidelines on Cybersecurity for the Financial Sector~~ — `control/fsa.go.jp/cybersecurity-guidelines-financial-sector/`. **Full text acquired** (this PDF wasn't actually encrypted — plain local `pdftotext` succeeded where WebFetch had failed).
- [x] ~~Comprehensive Guidelines for the Supervision of Major Banks~~ — `control/fsa.go.jp/supervision-major-banks/`. **Excerpt acquired** — the cybersecurity-relevant section (III-3-7 IT System Risk) only, not the full 513-page bank-supervision manual (full PDF kept locally, gitignored).
- [x] ~~PPC Guidelines regarding the APPI~~ — `control/ppc.go.jp/appi-guidelines/`. **Full text acquired** (Japanese; no official English translation exists for this edition).
- [x] ~~MHLW Medical Info Systems Safety Guidelines~~ — `control/mhlw.go.jp/medical-info-systems-safety/`. **1 of 5 volumes acquired** (Overview only; Management/Planning/System Operations/Maintenance Outsourcing volume URLs recorded for a future pass).
- [x] ~~METI/MIC Medical Info Provider Safety Guideline~~ — `control/mhlw.go.jp/medical-info-provider-safety/`. **Full text acquired** via the Playwright/meti.go.jp bypass.
- [x] ~~6 MLIT sector guidelines~~ (aviation, airport, railway, truck-freight/warehousing/maritime logistics) — all under `control/mlit.go.jp/*/`. **Full text acquired for all 6** — turned out NOT to be image-heavy as originally assessed; plain `pdftotext -layout` extracted ~450K clean characters each.
- [x] ~~SME Security Guidelines (IPA)~~ — `control/ipa.go.jp/sme-security-guidelines/`. **Full text acquired** (English v3.1, behind current Japanese v4.0).
- [x] ~~Insider Breach Guidelines (IPA)~~ — `control/ipa.go.jp/insider-breach-guidelines/`. **Full text acquired** (English v3.0, behind current Japanese v5).
- [x] ~~AI Business Guidelines~~ — `control/meti.go.jp/ai-business-guidelines/`. **Full text acquired** via the Playwright/meti.go.jp bypass.
- [x] ~~AI Security Guideline (MIC)~~ — `control/soumu.go.jp/ai-security-guideline/`. **Announcement page only** acquired (confirms finalization); the guideline body PDF's direct link wasn't found in static HTML — still TODO.
- [x] ~~Cybersecurity Policy for CIP~~ — `control/cyber.go.jp/cip-policy/`. **Full text acquired** (same GPKI-decrypt approach as Common Standards).
- [x] ~~Supply chain partnership doc~~ — `control/meti.go.jp/supply-chain-partnership/`. **Full text acquired** (Japanese; jftc.go.jp reachable via the same Playwright bypass technique). SCS Evaluation System (`secid:control/meti.go.jp/scs-evaluation-system`) still has no document to acquire — not yet operational, construction policy published March 2026.

**Certification / assessment schemes (control type) — all acquired:**
- [x] ~~JC-STAR~~ — `control/ipa.go.jp/jc-star/`. **Full text acquired** (STAR-1 requirements, English).
- [x] ~~JISEC~~ — `control/ipa.go.jp/jisec/`. **Full page content acquired** (no separate scheme PDF found beyond the web pages).
- [x] ~~CRYPTREC~~ — `control/cryptrec.go.jp/ciphers-list/`. **Full text acquired** (Japanese; cipher/algorithm names are in Latin script and fully readable even within the Japanese document).
- [x] ~~PrivacyMark~~ — `control/jipdec.or.jp/privacymark/`. **Full page content acquired** (English).

**Lower priority:**
- [x] ~~J-CSIP~~ — `control/ipa.go.jp/j-csip/`. **Full (thin) English documentation captured** — genuinely just the one overview page; annual reports/SIG lists are Japanese-only, not pursued.
- [ ] Sector-specific narrower items (Medical Care Act cybersecurity enforcement order, Subcontract/Proper Transactions Act) — still not folded in; likely lower standalone value.

**Remaining gaps:** 5 items fully blocked (UCAL, Unfair Competition Prevention Act, Payment Services Act, Installment Sales Act, Economic Security Information Act outline) — all solely hosted on `japaneselawtranslation.go.jp`, which returned HTTP 403 to curl, WebFetch, and a real Playwright browser session across every path tried this session. This looks like a persistent network/WAF-level block (not fixable by user-agent or JS-rendering workarounds) rather than a per-page issue. Worth trying from a different network path (e.g. a Japan-based proxy) if this remains a priority. Also TODO: MHLW's other 4 guideline volumes, the MIC AI Security Guideline's actual body text, and the Active Cyber Defense Act's full article text (only the Japanese TOC/structure was captured so far).

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
