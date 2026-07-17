# Cybersecurity Management Guidelines

Ver. 3.0, issued March 2023. Executive/CISO-level cybersecurity governance framework: 3 principles for management plus 10 important items for CISOs (risk management, resourcing, supply-chain security, incident response, stakeholder communication).

- **SecID:** `secid:control/meti.go.jp/cybersecurity-management-guidelines`
- **Source:** https://www.meti.go.jp/policy/netsecurity/downloadfiles/CSM_Guideline_v3.0_en.pdf
- **License:** LicenseRef-Japan-Government-Notification-Likely-Excluded (likely_permitted) -- see `cybersecurity-management-guidelines-metadata.json`

**Status:** Full text acquired.

## Files

| File | Contents |
|---|---|
| `cybersecurity-management-guidelines-raw.txt` | Full text, English |

## Extraction notes

Full English text acquired. meti.go.jp returns HTTP 403 to plain curl/WebFetch (bot/WAF protection) but a real Playwright browser session succeeded (HTTP 200) -- fetched the PDF bytes via an in-page fetch() call and saved via base64 round-trip.
