# Act on the Protection of Personal Information

Japan's Act on the Protection of Personal Information (APPI) — Japan's primary data protection statute, originally enacted 2003, most recently amended 2020/2022. Enforced by the Personal Information Protection Commission (PPC).

- **Acronym:** APPI
- **Owner:** Personal Information Protection Commission, Japan (PPC)
- **SecID:** `secid:regulation/ppc.go.jp/appi`
- **Source:** https://www.ppc.go.jp/en/legal/
- **License:** permitted / redistributable — Japan's Copyright Act Article 13 excludes laws and their official government translations from copyright. See `appi-metadata.json`.

**Status:** structured. 81 of 88 articles extracted with title + content (see `scope.known_gaps` in `appi-metadata.json` for the 17 missing article numbers and why).

## Files

| File | Contents |
|---|---|
| `appi-metadata.json` | Directory metadata (schema per METADATA-SCHEMA.md) |
| `appi-articles.json` / `.csv` | 81 articles: `article`, `title` (parenthetical heading, e.g. "Purpose"; `null` where the source has none), `content` |
| `appi.md` | Marker markdown extraction of the source PDF (narrative reference) |
| `appi.pdf` | Source PDF (gitignored) |
| `appi_meta.json` | Marker's own extraction metadata (page structure, TOC) — not the directory metadata |
| `extract_appi.py` | Article parser — see its docstring for the title/content alignment fix and the Article 2 recovery reasoning |

## Known gaps

17 article numbers aren't captured: **7, 18, 23, 27, 28, 30, 36, 42, 44, 53, 58, 59, 63, 68, 71, 76, 87**. Some may be legitimately absent/renumbered in this consolidated text (e.g. plain `58` vs. the present `58-2` through `58-5`); others (e.g. `87`, whose text appears unmarked as sub-paragraphs under Article 86 in the marker output) are the same kind of source-extraction gap that initially hid Article 2 — the PDF's marker/OCR pass silently drops some "Article N" markers. Not yet verified article-by-article against the authoritative `japaneselawtranslation.go.jp` translation database (that site returns HTTP 403 to both WebFetch and plain `curl` — a JS-capable browser fetch, e.g. Playwright, would be needed to re-acquire cleanly). See TODO.md.

## Regenerating

```bash
python3 extract_appi.py   # reads appi.md -> appi-articles.{json,csv}
```
