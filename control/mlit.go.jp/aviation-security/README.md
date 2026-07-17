# Safety Guideline for Ensuring Information Security in the Aviation Sector

7th edition, revised April 30, 2026 (152 pages). Covers cybersecurity requirements for airline operational systems (flight ops, reservation systems) as designated critical infrastructure. Includes a full revision history back to the 1st edition.

- **SecID:** `secid:control/mlit.go.jp/aviation-security`
- **Source:** https://www.mlit.go.jp/koku/content/20240425-koku-CyberSecurity.pdf
- **License:** LicenseRef-Japan-Government-Notification-Likely-Excluded (likely_permitted) -- see `aviation-security-metadata.json`

**Status:** Full text acquired (Japanese only).

## Files

| File | Contents |
|---|---|
| `aviation-security-raw.txt` | Full text, Japanese |

## Extraction notes

Full text acquired cleanly. An earlier session pass had characterized MLIT's guidelines as "image/scan-heavy, resisting text extraction" based on WebFetch's built-in PDF handling -- that assessment was wrong. Plain pdftotext -layout extracted ~450,000 characters of clean, readable Japanese text with no OCR needed.
