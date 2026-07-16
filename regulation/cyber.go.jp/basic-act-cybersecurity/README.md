# Basic Act on Cybersecurity

Japan's foundational cybersecurity law (Act No. 104 of 2014, effective January 2015). Establishes the Cybersecurity Strategic Headquarters, mandates a national Cybersecurity Strategy, and authorizes the Common Standards for Cybersecurity Measures of Governmental Entities. Administered today by the National Cybersecurity Office (NCO) — the July 2025 successor to NISC.

- **Acronym:** BAC
- **Owner:** National Cybersecurity Office (NCO)
- **SecID:** `secid:regulation/cyber.go.jp/basic-act-cybersecurity`
- **Source:** https://www.cyber.go.jp/eng/
- **License:** permitted / redistributable (Japan Copyright Act Art. 13 excludes laws from copyright) — see `basic-act-cybersecurity-metadata.json`

**Status:** metadata/notes-only stub. **No full text acquired** — see below.

## Why there's no article-level data here

The authoritative English translation, `https://www.japaneselawtranslation.go.jp/en/laws/view/3677/en`, returned **HTTP 403** to every fetch method tried on 2026-07-16: a plain `curl` with realistic browser headers, `WebFetch`, and a real Playwright browser session. This looks like an AWS ELB/WAF-level block (possibly geo/IP-based) rather than a JS-rendering problem, so there was no client-side workaround available in this session.

This entry's `description` and `scope` fields are built from secondary legal-summary sources (ICLG Cybersecurity Laws and Regulations Report, Chambers Global Practice Guides, `cyber.go.jp`'s own English pages) — not the primary text. Treat structural claims (chapter/article counts, exact provisions) as unverified until the primary text can be acquired.

## Follow-up

- Retry acquisition from a Japan-based IP or network path, or via a Japan-based proxy/VPN.
- Check whether a mirror exists (e.g., a law-firm or academic PDF reproduction) with a full unofficial translation.
- See TODO.md's Japan catalog section for tracking.
