# TODO: Registry Gaps — Japan

Focused, scannable list of what's still missing for the Japan cybersecurity/data-protection sourcing work (started 2026-07-16). This is a subset of the full history in [TODO.md](TODO.md) — see that file's "Japan" section for what's already done and why. This file tracks only what's still outstanding.

## Blocked at the source — need a different acquisition path

All five of these live only on `japaneselawtranslation.go.jp`, which returned HTTP 403 to curl, WebFetch, and a real Playwright browser session across every URL tried — a persistent block, not a per-page issue. Nothing else worked (no alternate mirror found for any of the four full laws below). A Japan-based network path or proxy is the most likely unblock.

- [ ] **UCAL** (Act on Prohibition of Unauthorized Computer Access) — `secid:regulation/cas.go.jp/ucal`
- [ ] **Unfair Competition Prevention Act** — `secid:regulation/meti.go.jp/unfair-competition-prevention` (WIPO Lex mirror tried, JS-rendered, only returned site nav chrome — worth a Playwright retry against that mirror specifically)
- [ ] **Payment Services Act** — `secid:regulation/fsa.go.jp/payment-services-act`
- [ ] **Installment Sales Act** — `secid:regulation/meti.go.jp/installment-sales`
- [ ] **Act on the Protection and Use of Critical Economic Security Information** — `secid:regulation/cao.go.jp/economic-security-information` (only a government *outline* exists even at the primary source, not full text)

## Partial — need more of what we already found a path to

- [ ] **MHLW Medical Info Systems Safety Guidelines** — only the Overview volume (1 of 5) is acquired. Management, Planning & Administration, System Operations, and Maintenance Outsourcing volumes are sitting at known URLs, listed in `control/mhlw.go.jp/medical-info-systems-safety/mhlw-medical-page-listing.txt`. Just needs the same curl+pdftotext treatment as the Overview volume.
- [ ] **MIC AI Security Guideline** — only the announcement page (confirming finalization) is acquired. The actual guideline body PDF link wasn't findable in the static HTML (likely JS-constructed or behind a search portal) — needs a Playwright pass on `soumu.go.jp` to find and fetch it.
- [ ] **Active Cyber Defense Act** — only the Japanese chapter/article table of contents was captured (via Playwright rendering e-Gov's JS app). Full article body text still needed — same e-Gov page, just needs deeper extraction than `document.body.innerText` on the landing view (likely needs clicking into each chapter/article in the UI).
- [ ] **Telecommunications Business Act** — full text acquired, but it's an outdated ~2007 revision (per its own header). The Act has been amended since (2022/2023 cookie-consent-style changes per research) — current-revision text still needed. Same japaneselawtranslation.go.jp block applies to the authoritative version; the MIC alternate that worked is the old one.
- [ ] **ISMAP** — ISMAP-LIU (Low-Impact-Use variant) not covered; the JS-rendered "Attached Tables" 1-8 (including the SP800-53 crosswalk, tables 6-7) are still not acquired — served from a ServiceNow portal, would need a Playwright pass similar to what worked for the meti.go.jp/jftc.go.jp blocks this session.

## Needs verification, not acquisition

- [ ] **My Number Act** — 76 articles extracted, but the law has both main-body articles and separately-numbered supplementary provisions (附則) that restart numbering from 1. The parser's dedup logic can pick the wrong one when both share a number. 18 of 76 articles have no recovered title — some may be genuine, some may be dedup collisions. Needs a manual pass against the source PDF (`regulation/digital.go.jp/my-number-act/my-number-act.pdf`).

## Nothing to acquire yet

- [ ] **SCS Evaluation System** (Security Measures Evaluation System for Supply Chain Strengthening) — construction policy published March 2026, but the system isn't operational yet (full launch targeted ~FY2026 end / early FY2027). Revisit once assessment criteria are actually published.
- [ ] **FISC Security Guidelines** — confirmed members-only/paid. Would require an actual FISC membership or purchase; not a research/access problem.
- [ ] **Basic Act on Cybersecurity** — full article text blocked at the only known source (japaneselawtranslation.go.jp), same persistent-block situation as the "Blocked at the source" section above.

## Lower priority

- [ ] Sector-specific narrower items not yet folded in: Medical Care Act cybersecurity enforcement order, Subcontract/Proper Transactions Act
- [ ] MLIT's master index (`https://www.mlit.go.jp/sogoseisaku/jouhouka/sosei_jouhouka9999.html`) also lists Water Supply and Ports sector guidelines that haven't been added to the 6 already registered (aviation, airport, railway, 3x logistics)
