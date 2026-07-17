# CRYPTREC Ciphers List

CRYPTREC LS-0001-2022R2, last updated March 30, 2026. Three tiers: e-Government Recommended Ciphers List (public-key: DSA, ECDSA, EdDSA, RSA-PSS, RSASSA-PKCS1-v1_5, RSA-OAEP, DH, ECDH; symmetric: AES, Camellia, KCipher-2; hash: SHA-256/384/512, SHA3 family, SHAKE128/256), Candidate Recommended Ciphers List, and Monitored Ciphers List.

- **SecID:** `secid:control/cryptrec.go.jp/ciphers-list`
- **Source:** https://www.cryptrec.go.jp/list/cryptrec-ls-0001-2022r2.pdf
- **License:** LicenseRef-Japan-Government-Notification-Likely-Excluded (likely_permitted) -- see `ciphers-list-metadata.json`

**Status:** Full text acquired (Japanese document; English surrounding context pages also captured).

## Files

| File | Contents |
|---|---|
| `ciphers-list-raw.txt` | Full text, Japanese (algorithm names in Latin script) |
| `cryptrec-method.txt` | English methodology/specifications page |
| `cryptrec-list-page.txt` | English list-overview page (links to the Japanese PDF) |

## Extraction notes

Full text acquired (Japanese; only a Japanese-language PDF exists for the actual ciphers list, despite cryptrec.go.jp/en/ having English-language surrounding pages). PDF was encrypted (decrypted with qpdf), then pdftotext -layout extracted cleanly. IMPORTANT: cipher/algorithm names themselves are written in Latin script even within the Japanese document and are fully readable/extractable (e.g. "AES", "RSA-PSS", "SHA-256") -- genuinely useful data even without translating the surrounding Japanese prose.
