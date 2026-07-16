# Sources

Free-form notes on where various documents were found. As metadata files
(`<name>-<version>-metadata.json`) are written for each document, the
information here moves into the per-doc `links` block. This file is the
catch-all for orphaned source URLs.

## AI regulation trackers

- https://www.whitecase.com/insight-our-thinking/ai-watch-global-regulatory-tracker-united-states
- https://tracker.holisticai.com/feed
- https://www.techieray.com/GlobalAIRegulationTracker
- https://www.skadden.com/-/media/files/publications/2023/12/2024-insights/a-list-of-ai-legislation-introduced-around-the-world.pdf

## Canada — Artificial Intelligence and Data Act (AIDA)

- https://ised-isde.canada.ca/site/innovation-better-canada/en/artificial-intelligence-and-data-act-aida-companion-document
- https://ised-isde.canada.ca/site/innovation-better-canada/en/artificial-intelligence-and-data-act
- https://www.canada.ca/en/innovation-science-economic-development/news/2022/06/new-laws-to-strengthen-canadians-privacy-protection-and-trust-in-the-digital-economy.html
- https://ised-isde.canada.ca/site/ai-strategy/en

## Germany BSI

- BSI recommendations by attack target: https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/empfehlungen-nach-angriffszielen_node.html

## Cisco

- AI Security Best Practice Portal: https://aisecurity.cisco.com/

## Microsoft DPR

- https://cloudsecurityalliance.org/blog/2024/10/16/an-overview-of-microsoft-dpr-its-new-ai-requirements-and-iso-42001-s-potential-role
- https://www.schellman.com/blog/privacy/microsoft-dpr-ai-requirements-and-iso-42001

## OECD AI Principles

- https://oecd.ai/en/ai-principles

## OWASP AI Exchange

- https://owaspai.org/

## Japan — landscape survey (2026-07-16)

Sources used to compile the Japan catalog in TODO.md. Per-document links move into `links` blocks as each entry is ingested.

- Legal overview: https://iclg.com/practice-areas/cybersecurity-laws-and-regulations/japan
- Legal overview: https://practiceguides.chambers.com/practice-guides/cybersecurity-2026/japan
- Legal overview (data protection): https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/japan
- DLA Piper Data Protection Laws of the World — Japan: https://www.dlapiperdataprotection.com/index.html?t=law&c=JP

### ISMAP
- Portal: https://www.ismap.go.jp/
- Digital Agency overview: https://www.digital.go.jp/en/policies/security/ismap-liu
- Digital Agency cloud service list updates: https://www.digital.go.jp/en/news/7a38a22f-cc9f-4c39-a0c0-1aa1f0f98d63

### Basic Act on Cybersecurity / NISC / NCO
- NISC (legacy site, being succeeded by NCO as of July 2025): https://www.nisc.go.jp/eng/
- Common Standards on Cybersecurity Measures of Governmental Entities — issued under BAC Art. 26(1) by CSHQ + NCO

### FSA (financial sector)
- Guidelines on Cybersecurity for the Financial Sector (English PDF): https://www.fsa.go.jp/common/law/cybersecurity_guideline_en.pdf
- FSA cybersecurity policy hub: https://www.fsa.go.jp/en/policy/cybersecurity/index.html
- FSA laws & regulations index: https://www.fsa.go.jp/en/laws_regulations/index.html

### IPA (Information-technology Promotion Agency)
- IPA security hub: https://www.ipa.go.jp/en/security/index.html
- SME security guidelines: https://www.ipa.go.jp/en/about/activities/security-action.html
- JISEC (Common Criteria scheme): https://www.ipa.go.jp/en/security/jisec/index.html
- CRYPTREC (crypto evaluation): https://www.ipa.go.jp/en/security/crypto-evaluation/index.html

### JIPDEC / PrivacyMark
- https://en.wikipedia.org/wiki/Japan_Institute_for_Promotion_of_Digital_Economy_and_Community
- PrivacyMark background: https://hstalks.com/article/7969/japans-privacymark-system-as-a-good-illustration-o/

### FISC (financial industry security guidelines)
- Center for Financial Industry Information Systems (existing SecID stub: `fisc.or.jp`) — members-only guideline text; public-availability TBD, check during ingestion

## Japan batch 2 (2026-07-16) — primary legislation

- UCAL: https://www.japaneselawtranslation.go.jp/en/laws/view/3933/en (blocked, 403)
- Telecommunications Business Act: https://www.japaneselawtranslation.go.jp/en/laws/view/3390 (blocked, 403); alternate https://www.soumu.go.jp/main_sosiki/joho_tsusin/eng/Resources/laws/pdf/090204_2.pdf (not tested, possibly outdated)
- My Number Act: https://www.japaneselawtranslation.go.jp/en/laws/view/2755 (blocked, 403); alternate https://www.ppc.go.jp/files/pdf/en3.pdf (downloads fine, text extraction failed)
- Active Cyber Defense Act (Act No. 42 of 2025): Japanese text https://laws.e-gov.go.jp/law/507AC0000000042 — no English translation exists yet
- Act on the Protection and Use of Critical Economic Security Information: outline only https://www.japaneselawtranslation.go.jp/outline/127/905R626.pdf (blocked, 403); Japanese text https://laws.e-gov.go.jp/law/506AC0000000027
- Economic Security Promotion Act: https://www.japaneselawtranslation.go.jp/en/laws/view/4523/en (blocked, 403); overview https://www.cao.go.jp/keizai_anzen_hosho/suishinhou/infra/doc/infra_gaiyou_eng.pdf (not tested)
- Specified Secret Protection Act: https://www.japaneselawtranslation.go.jp/en/laws/view/2543 (blocked, 403); overview (fetched OK) https://www.cas.go.jp/jp/tokuteihimitsu/gaiyou_en.pdf
- Unfair Competition Prevention Act: https://www.japaneselawtranslation.go.jp/en/laws/view/4709 (blocked, 403); WIPO Lex mirror https://www.wipo.int/wipolex/en/legislation/details/19229 (fetched but not text-extractable)
- Payment Services Act: https://www.japaneselawtranslation.go.jp/en/laws/view/3965 (blocked, 403)
- Installment Sales Act: https://www.japaneselawtranslation.go.jp/en/laws/view/4499/en (blocked, 403)

## Japan batch 2 (2026-07-16) — government/sector guidelines

- Common Standards for Government Entities (FY2025): https://www.cyber.go.jp/pdf/policy/general/kijyunr7-en.pdf (freely accessible, GPKI-signed)
- Cybersecurity Policy for CIP (2024): https://www.cyber.go.jp/eng/pdf/cip_policy_2024_eng.pdf (freely accessible, GPKI-signed)
- Cybersecurity Management Guidelines v3.0: https://www.meti.go.jp/policy/netsecurity/downloadfiles/CSM_Guideline_v3.0_en.pdf (blocked, 403)
- FSA Cybersecurity Guidelines for Financial Sector: https://www.fsa.go.jp/common/law/cybersecurity_guideline_en.pdf (fetched OK, PDF text extraction failed)
- FSA Comprehensive Guidelines for Supervision of Major Banks: https://www.fsa.go.jp/common/law/guide/en_city.pdf (fetched OK, PDF text extraction failed)
- PPC APPI Guidelines (General Rules): https://www.ppc.go.jp/files/pdf/241202_guidelines01.pdf (Japanese only, no English translation exists)
- MHLW Medical Info Systems Safety Guidelines (v7.0, June 2026): https://www.mhlw.go.jp/stf/shingi/0000516275_00006.html (Japanese, freely accessible; MHLW English site section blocked 403)
- METI/MIC Medical Info Provider Safety Guideline (v2.0): https://www.meti.go.jp/policy/mono_info_service/healthcare/01gl_20250328.pdf (blocked, 403); MIC notice https://www.soumu.go.jp/menu_news/s-news/01ryutsu06_02000427.html
- MLIT master index (all sector guidelines): https://www.mlit.go.jp/sogoseisaku/jouhouka/sosei_jouhouka9999.html
  - Aviation: https://www.mlit.go.jp/koku/koku_CyberSecurity.html / https://www.mlit.go.jp/koku/content/20240425-koku-CyberSecurity.pdf
  - Airport: https://www.mlit.go.jp/koku/content/20240425-kuko-CyberSecurity.pdf
  - Railway: https://www.mlit.go.jp/tetudo/tetudo_fr1_000092.html / https://www.mlit.go.jp/tetudo/content/001998629.pdf
  - Logistics (truck/motor freight): https://www.mlit.go.jp/jidosha/jidosha_tk4_000121.html / https://www.mlit.go.jp/jidosha/content/002010708.pdf
  - Logistics (warehousing): https://www.mlit.go.jp/jidosha/content/002010718.pdf
  - Logistics (maritime): https://www.mlit.go.jp/maritime/content/001744764.pdf
  - (Also listed but not yet added to SecID: Water Supply, Ports)
- IPA SME Security Guidelines (English v3.1): https://www.ipa.go.jp/en/about/activities/gg62ps000000103j-att/Information_Security_Measures_Guidelines_for_Small_and_Medium-sized_Enterprises_Version_3-1.pdf
- IPA Insider Breach Prevention Guidelines: https://www.ipa.go.jp/security/guide/insider.html
- AI Business Guidelines (Ver 1.1): https://www.meti.go.jp/shingikai/mono_info_service/ai_shakai_jisso/pdf/20240419_14.pdf (blocked, 403)
- MIC AI Security Guideline (finalized): https://www.soumu.go.jp/menu_news/s-news/01cyber01_02000001_00282.html (Japanese only)
- METI/JFTC Supply Chain Partnership doc: https://www.jftc.go.jp/dk/guideline/unyoukijun/cyber_security/cyber_security_02.pdf (Japanese only)
- SCS Evaluation System: https://www.meti.go.jp/policy/netsecurity/scs.html (blocked, 403); English interim report https://www.meti.go.jp/english/press/2025/0414_003.html

## Japan batch 2 (2026-07-16) — certification schemes

- JC-STAR: https://www.ipa.go.jp/en/security/jc-star/index.html
- JISEC: https://www.ipa.go.jp/en/security/jisec/index.html
- CRYPTREC: https://www.cryptrec.go.jp/en/list.html (use `www.` subdomain — bare domain has a TLS cert mismatch)
- PrivacyMark: https://english.jipdec.or.jp/activities/pmark.html / https://privacymark.org/about/outline_and_purpose.html
- J-CSIP: https://www.ipa.go.jp/en/about/activities/jcsip-jcrat.html (thin English documentation, bundled with J-CRAT)
