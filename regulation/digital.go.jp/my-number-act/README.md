# My Number Act

Japan's national ID-number law (Act No. 27 of 2013, effective January 2016) — establishes the Individual Number/Corporate Number system and a dedicated data-protection regime for "Specific Personal Information," layered on top of APPI.

- **SecID:** `secid:regulation/digital.go.jp/my-number-act`
- **Source:** https://www.ppc.go.jp/files/pdf/en3.pdf (English)
- **License:** permitted/redistributable — primary legislation, excluded from copyright under Japan's Copyright Act Art. 13 (same basis as APPI).

**Status:** structured. 76 articles extracted with title + content.

## Known issue

This law has both main-body articles and separately-numbered supplementary provisions (附則) that restart numbering from 1. The parser (adapted from APPI's) can pick the wrong duplicate when both a main-body and supplementary-provision article share a number. Not yet manually verified article-by-article — treat as a solid first pass, not verified-clean.

## Files

| File | Contents |
|---|---|
| `my-number-act-metadata.json` | Directory metadata |
| `my-number-act-articles.json` / `.csv` | 76 articles: `article`, `title`, `content` |
| `my-number-act-raw.txt` | `pdftotext -layout` output |
| `extract_my_number_act.py` | Article parser |

## Regenerating

```bash
python3 extract_my_number_act.py   # reads my-number-act-raw.txt -> my-number-act-articles.{json,csv}
```
