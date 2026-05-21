# Glossary corpus

Aggregate index of every `subtype: ["glossary"]` entry in this repo, with terms merged into a single corpus and a cross-source comparison view.

## Files

- `corpus.csv` / `corpus.json` — one row per (source, term). The full unified dataset.
- `cross-source.csv` / `cross-source.json` — every term that appears in 2+ sources, with each source's definition side-by-side. Useful for answering "what does NIST vs IETF vs OWASP say about X?".
- `stats.md` — generated counts (terms per source, top cross-source overlaps, etc.).

## How it's built

`python3 tools-resources/utils/build_glossary_corpus.py` walks every `reference/*/*/*-metadata.json` carrying `subtype: ["glossary"]`, loads the sibling `*-terms.json`, and aggregates. Re-run the script after adding or refreshing any source's extraction.

## Schema

`corpus.csv` columns:

| Column | Type | Notes |
|---|---|---|
| `source_secid` | string | The glossary's full SecID (e.g., `secid:reference/nist.gov/csrc-glossary`) |
| `source_name` | string | Human-friendly source name from the entry's metadata |
| `license_spdx` | string | SPDX license identifier (or `NOASSERTION` if unknown) |
| `publicly_redistributable` | bool | Whether definitions in this source can be redistributed |
| `term` | string | The term name as published |
| `normalized_term` | string | Lowercased + punctuation-stripped form used for cross-source matching |
| `definition` | string | The definition body |
| `source_anchor` | URL | Direct link back to the term page (or section anchor) |
| `notes` | string | Per-source notes (categories, "see also" links, source citation, etc.) |

`cross-source.csv` is the same schema repeated for every term that appears in multiple sources, with an additional `source_count` column.

## Why a normalized term

The `normalized_term` column collapses surface variation so that:
- `"Two-Factor Authentication"`, `"two-factor authentication"`, `"Two-factor authentication (2FA)"` all match.
- Trailing acronyms in parentheses are dropped (the corpus still preserves the original term in `term`).
- Whitespace and punctuation are normalized.

This is best-effort; it doesn't catch semantic variants (`"2FA"` vs `"two-factor authentication"`). For deeper de-dup the `notes` field often carries acronym/alias info from the source.
