# Processing a license-restricted glossary into this repo

How to extract a license-restricted security glossary (vendor cyberpedia, paywalled analyst glossary, members-only association vocabulary, etc.) into structured term/definition form and land the output here.

This is a sibling workflow to [`PROCESSING.md`](PROCESSING.md), which covers PDF-based standards/controls extraction. Both workflows share the SecID-mirrored layout, the per-doc metadata convention, and the audit/index validation steps. They differ in **what gets extracted**, the **output schema**, the **path shape**, and the **fetch tooling**:

| | Standards/controls ([`PROCESSING.md`](PROCESSING.md)) | Glossaries (this file) |
|---|---|---|
| SecID type | `control/` (mostly) | `reference/` with `subtype: ["glossary"]` |
| Path shape | `{type}/{ns}/{name}/{version}/` | `{type}/{ns}/{name}/` — no version segment (glossaries are rolling) |
| Output schema | `{framework, controls[]}` JSON | `{term, definition, source_anchor, notes}` rows (CSV + JSON) |
| Fetch tooling | marker GPU pipeline | `requests`+`BeautifulSoup` / Playwright / marker GPU / `python-docx` (per-source) |
| Reproducibility | shared `extract_iso_clauses.py` / `extract_controls_via_ai.py` in `tools-resources/utils/` | per-source `extract_{name}.py` committed alongside the data |
| Marker `_page_*.jpeg` | kept (table-cell visual context) | skipped (regenerable, glossaries are plain text) |

## The mirror-stub architecture

Glossary content follows a **metadata-mirror pattern** that differs from how this repo treats ISO standards:

- **Public repo** keeps its existing `*-metadata.json` stub for each license-restricted glossary unchanged. The stub advertises the SecID, the upstream URL, and the restrictive license — telling a public consumer "this exists, here's where to acquire it" without redistributing content.
- **Private repo (here)** holds a *copy* of that metadata file at the same SecID-derived path, with `license`, `current_extraction`, and `desired_end_state` fields updated to reflect the actual extraction performed here.

A consumer with public-only access sees the public stub. A consumer with private access pulls the populated metadata + extracted terms from here. Same SecID identifier, same filesystem path, different stratification by access tier.

This is **different** from how this repo treats ISO standards. ISO metadata files exist only here — there is no public-repo counterpart for ISO 27001 etc. Glossaries are special because the public repo already enumerates them as metadata-only stubs (Phase 4b classification sweep tagged them with `subtype: ["glossary"]` + `license.publicly_redistributable: false`), so the metadata file legitimately exists in both places.

## The work queue

As of 2026-05-21, ~121 license-restricted glossary entries live in the public repo as metadata-only stubs awaiting extraction here. Re-run this sanity check from the public repo root to confirm the current count:

```bash
cd ../dataset-public-laws-regulations-standards

# Total glossary entries (~151)
find reference -name '*-metadata.json' -exec jq -r 'select(.subtype // [] | index("glossary")) | .secid' {} \; | wc -l

# Restricted + still-stub — the work queue (~121)
find reference -name '*-metadata.json' -exec jq -r '
  select(.subtype // [] | index("glossary"))
  | select(.license.publicly_redistributable != true)
  | select(.current_extraction.tool == "n/a (stub)")
  | .secid
' {} \; | wc -l

# SPDX tier breakdown
find reference -name '*-metadata.json' -exec jq -r '
  select(.subtype // [] | index("glossary"))
  | select(.license.publicly_redistributable != true)
  | select(.current_extraction.tool == "n/a (stub)")
  | .license.spdx
' {} \; | sort | uniq -c | sort -rn
```

Current tier composition of the ~121 work queue:

| SPDX | ~Count | Examples |
|---|--:|---|
| `LicenseRef-Vendor-Copyright` | ~98 | Palo Alto, Fortinet, Cisco, MSRC, IBM, Intel, ESET, Trellix, Trend Micro, Sophos, Check Point, Symantec/Broadcom, ISACA, HITRUST, SANS, IAPP |
| `LicenseRef-Proprietary` | ~2 | Gartner IT Glossary, OECD.AI Glossary |
| `NOASSERTION` | ~21 | License unverified during Phase 4b — must triage first; some may turn out permissive and belong in the public repo |

If the counts diverge significantly from the above, the public repo has moved since this doc was written — re-read the queue output to understand the current state before extracting.

## Workflow

### Step 1: Pick a candidate and resolve its license

For a `LicenseRef-Vendor-Copyright` or `LicenseRef-Proprietary` entry, no further license analysis is needed — it goes here.

For a `NOASSERTION` entry, **verify the actual terms before extracting anywhere**:

- Try a browser-realistic user agent: `curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 ..." $URL`
- Try an Internet Archive snapshot: `https://web.archive.org/web/*/{url}`
- Download the PDF directly if the landing page is bot-blocked
- Check the publisher's `/terms`, `/legal`, or footer

Outcomes:

- **Verified open license** (CC-BY-*, Apache-2.0, OGL, government public domain) → open a PR against the **public** repo updating `license.spdx` + `license.publicly_redistributable: true`, and extract there using the public repo's processing patterns. Don't bring it here.
- **Verified restrictive** → extract here.
- **Genuinely unverifiable after due diligence** → leave the public stub as-is, don't extract until license clarifies.

### Step 2: Don't bulk-mirror upstream-hosted authoritative data

Same rule as the public repo: if the publisher hosts their canonical data in a public, version-tagged location (a GitHub repo with releases, an open API feed), keep only a metadata stub pointing upstream. Don't import the bulk content into this repo just because *we* can — the publisher is the authoritative version-pinned source.

Restricted glossaries virtually never fit this pattern (they're behind login walls or vendor cyberpedias by definition), but it's worth checking before extracting a new source.

### Step 3: Verify the SecID namespace is registered

Every glossary's metadata `secid` field resolves to a registry file at `~/GitHub/CloudSecurityAlliance/SecID/registry/{type}/{tld}/{org}.json`. For the current 121 candidates, namespaces are already registered — no SecID PR needed. If you encounter a brand-new namespace, open a SecID PR adding it before landing content here.

### Step 4: Create the private-repo directory

Match the public repo's path exactly. Example for Palo Alto's Cyberpedia (`secid:reference/paloaltonetworks.com/cyberpedia`):

```
reference/paloaltonetworks.com/cyberpedia/
├── cyberpedia-metadata.json     ← copy from public repo, then update license + extraction state
├── extract_cyberpedia.py        ← per-source reproducibility script
├── cyberpedia.md                ← human-readable: ## Term + definition body
├── cyberpedia-terms.csv         ← canonical schema (see Step 6)
├── cyberpedia-terms.json        ← list of {term, definition, source_anchor, notes}
└── _marker/ (if PDF source)     ← keep .md + _meta.json only; skip _page_*.jpeg
```

The directory name matches the source name from the SecID registry (`cyberpedia` in this example). **No version segment** — glossaries are continuously-updated rolling documents, not versioned standards.

### Step 5: Build the per-source extractor

Write `extract_{name}.py` using the closest-shape template from the public repo. Read the template, understand its parsing approach, then adapt to your source's specific HTML/format:

| Source shape | Template in the public repo |
|---|---|
| HTML `<dl>/<dt>/<dd>` | `reference/amazon.com/aws-glossary/extract_aws_glossary.py` |
| HTML `<h3>` + paragraphs | `reference/mitre.org/cwe-glossary/extract_cwe_glossary.py` |
| RFC plain-text glossary | `reference/ietf.org/rfc4949-internet-security-glossary/extract_rfc4949_internet_security_glossary.py` |
| MediaWiki | `reference/wikimedia.org/security-team-definitions/extract_security_team_definitions.py` |
| DOCX download | `reference/texas.gov/cybersecurity-terminology/extract_cybersecurity_terminology.py` |
| PDF via marker GPU | `reference/incibe.es/glosario-terminos-ciberseguridad/extract_glosario_terminos_ciberseguridad.py` |
| JS-rendered accordion | `reference/gov.uk/ncsc-glossary/extract_ncsc_glossary.py` |
| Cloudflare-gated + archive.org fallback | `reference/fedramp.gov/fedramp-glossary/extract_fedramp_glossary.py` |
| Per-letter paginated CMS | `reference/gov.br/glossario-seguranca-informacao/extract_glossario_seguranca_informacao.py` |
| NIST CSRC JSON-feed | `reference/nist.gov/csrc-glossary/extract_csrc_glossary.py` |
| Per-term sub-page links | `reference/agid.gov.it/cert-agid-glossario/extract_cert_agid_glossario.py` |

The script must be **idempotent**: re-running it should produce the same outputs (or new ones if the source has updated, with the script's logic unchanged). Commit it alongside the data.

For PDF sources, invoke the GPU marker pipeline (same wrapper as PROCESSING.md):

```bash
PRIV=~/GitHub/CloudSecurityAlliance-DataSets/dataset-private-laws-regulations-standards
~/GitHub/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/tools-resources/utils/pdf_to_md_via_gpu.sh \
    --output-dir "$PRIV/reference/{ns}/{dir}/_marker/" \
    /path/to/source.pdf
```

Then write a parser that walks `_marker/{name}.md`. Commit `_marker/{name}.md` and `_marker/{name}_meta.json`; **skip the `_page_*.jpeg` images** — they're regenerable and bulky. (This is a departure from PROCESSING.md's controls workflow, which keeps the page JPEGs. Glossaries don't need them because the parser output is plain text, not table cells with visual context.)

For HTML sources behind anti-bot defenses, see the FedRAMP template — it caches an Internet Archive snapshot as `.source-cache.html` and falls back to it when the live page is blocked.

For JS-rendered SPAs and Cloudflare/anti-bot-gated sources, use `tools-resources/utils/playwright_fetch.py` to capture a hydrated DOM as `.source-cache.html`, then write the parser against the cache. Two modes:

- `--auto` — networkidle + dwell, then auto-capture. Use for JS-rendered pages without anti-bot.
- `--pause` — polls for a sentinel file (default `/tmp/playwright-go`) before capturing. Use for pages with anti-bot/CAPTCHA/login: the user clears the challenge in the visible browser, then `touch /tmp/playwright-go` from any terminal to signal "ready, capture now."

Example:
```bash
python3 tools-resources/utils/playwright_fetch.py \
  https://example.com/glossary \
  reference/example.com/glossary/.source-cache.html \
  --auto --dwell 8
```

For SingleFile browser-extension captures (BeyondTrust pattern): save the live page using the SingleFile extension and place the resulting `.html` file as `.source-cache.html` in the source's directory. No Playwright needed; the parser reads the cached file directly. Document the re-capture instructions in the extractor's header.

### Hub-with-per-term-pages: harvest-then-fetch pattern

Many JS-rendered "glossary" indexes (Bitsight, Forescout, Fortinet, Cribl, …) are actually **hub pages**: the hydrated index lists term titles + deep-links, but each term's definition lives on a separate per-term page (e.g., `/glossary/<slug>`). Single-page extraction doesn't apply — you need a two-stage flow:

1. **Capture the index** with `playwright_fetch.py` to a `.source-cache.html` (the hydration step is what gives you the URL list).
2. **Harvest the term URLs** by parsing the cached index for the appropriate anchor selector (e.g., `.definition-block a[href]`).
3. **Polite per-term fetch** via plain `requests` (per-term pages are usually server-rendered and don't need JS). Use a 1.5-2s delay between requests, real browser UA, set a reasonable timeout. ~119 pages at 1.5s = ~3 min — entirely tractable.
4. **Parse each per-term page** for the canonical "h1 + first article paragraph" or similar.

Reference implementation: `reference/bitsight.com/cybersecurity-glossary/extract_cybersecurity_glossary.py`. Same shape applies to other vendor cyberpedias that look like SPAs but are really hub indexes.

The two-stage flow is reproducible because the index `.source-cache.html` is committed alongside the extractor — re-running the extractor just re-walks the per-term pages without needing the browser again. Re-capture the index only when the publisher reorganizes their glossary.

### Step 6: Canonical terms schema

Every glossary uses the same four-column schema for both CSV and JSON:

| Column | Type | Notes |
|---|---|---|
| `term` | string | The term as published. Preserve case and punctuation. |
| `definition` | string | The definition body, HTML stripped, plain text. Preserve sentence structure; don't summarize. |
| `source_anchor` | URL | Deep-link to the term's section anchor when one exists (e.g., `https://vendor.com/glossary#term-anchor`); fall back to the parent page URL if no per-term anchor. |
| `notes` | string | Per-source metadata in `key: value \| key: value` format. Use for "see also" references, aliases, source citations the publisher gives, category tags. Empty string when nothing relevant. |

The JSON is a flat list of objects with the same four keys. Don't add extra columns — schema consistency is what makes cross-source corpus building tractable.

### Step 7: Mirror the metadata file

Copy `*-metadata.json` from the public repo to this repo at the same path. Then update three fields:

1. **`license`** — record the actual restrictive license you verified in Step 1.
   - Default for vendor cyberpedias: `LicenseRef-Vendor-Copyright`
   - For specific known licenses, use a more specific identifier (e.g., `LicenseRef-Gartner-Terms`, `LicenseRef-IAPP-Member`)
   - `license.publicly_redistributable` stays `false`
2. **`current_extraction`** — replace the stub fields (`"tool": "n/a (stub)"`) with actual extraction provenance: tool name, version, host, flags, date.
3. **`desired_end_state`** — flip from `"metadata-only"` to `"structured"` once `*-terms.csv` and `*-terms.json` exist. The `reason` field stays `"glossary"`.

**The public repo's metadata stub stays unchanged.** It still says metadata-only and points at the upstream URL. Consumers without private access see the public stub; consumers with private access pull from here.

### Step 8: Audit, INDEX, commit

```bash
# From this private repo's root
python3 ../dataset-public-laws-regulations-standards/tools-resources/utils/audit_secid_alignment.py
python3 tools-resources/utils/build_index.py
```

The audit script lives in the public repo (cross-repo invocation) — there's no local copy here, that's intentional. It scans every `*-metadata.json` in both repos and reports any namespace that isn't registered in SecID. Clean run = `Missing namespaces: 0`. `build_index.py` regenerates this repo's `INDEX.md` and should show your new entries under `structured`.

Commit directly to `main` (private repo; no PR workflow per the workspace convention):

```bash
git add reference/paloaltonetworks.com/cyberpedia/ INDEX.md
git commit -m "Add Palo Alto Networks Cyberpedia glossary extraction"
git push
```

Source documents (PDFs, DOCX, raw HTML caches that aren't `.source-cache.html` for archive fallback) are `.gitignore`-excluded — double-check `git status --short` shows no `.pdf`/`.docx` before committing.

### Step 9: Cross-source corpus (optional, future)

The public repo has a `tools-resources/utils/build_glossary_corpus.py` script that produces a cross-source term/definition corpus across all extracted public glossaries. The script doesn't read private-repo data.

If a private-repo equivalent is later built, any export of that corpus would mix vendor-licensed terms with public terms — fine for **internal** CSA analytics, not for redistribution. Gate exports carefully.

## Recommended chunking

Don't commit all 121 in one batch — even with direct-to-main, smaller commits keep review and bisect tractable:

- **Per vendor cyberpedia** — Palo Alto, then Fortinet, then Cisco, then MSRC, … (each its own commit)
- **Per category** — one commit for analyst firms (Gartner, etc.), one for industry orgs (ISACA, HITRUST, SANS, IAPP), one for AI safety (OECD.AI, etc.)
- **NOASSERTION batch separately** — license-verification work is its own concern; group those entries into a single triage commit after verification.

Suggested starting order:

1. **Palo Alto Networks Cyberpedia** — canonical HTML `<dl>` pattern, large term set, good first lap
2. **Fortinet Cyberglossary**
3. **Cisco Security Glossary**
4. … iterate through the rest of the vendor cyberpedias before moving to analyst firms / industry orgs

## Common pitfalls

- **Copying the public stub's license SPDX verbatim.** The public stub reflects the public stance ("we couldn't redistribute, here's the upstream URL"). The private metadata records what license you actually verified — they may differ in specificity (e.g., public stub says `LicenseRef-Vendor-Copyright`; private metadata may pin a more specific `LicenseRef-PaloAlto-Cyberpedia-Terms` you found in the publisher's footer).
- **Forgetting `extract_{name}.py`.** Without it the extraction isn't reproducible and re-running becomes a one-shot exercise. Commit the script.
- **Including `_page_*.jpeg` from marker.** Skip them in glossary extractions. Marker emits them; `git add` selectively.
- **Editing the public repo for a license-restricted source.** If you find yourself opening files under `dataset-public-laws-regulations-standards/reference/` to add restricted content, stop — that's the wrong repo.
- **Inventing a new SecID type.** Restricted glossaries still go in `reference/` with `subtype: ["glossary"]`. The 10 types are frozen at v1.0.
- **Bypassing license verification on `NOASSERTION` entries.** Some of those ~21 will turn out to be permissive and belong in the public repo. Don't extract them privately just because they're tagged as restricted-stub today.

## Receipt for a good extraction

1. `audit_secid_alignment.py` exits 0
2. `build_index.py` shows the new entries under `structured` in this repo's INDEX.md
3. Re-running `extract_{name}.py` reproduces the same outputs (idempotent)
4. Term count matches what the source page advertises, or the commit message documents what got dropped and why
