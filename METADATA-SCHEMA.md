# Metadata Schema

Every document directory in this repository contains a metadata file describing the document. This doc defines the schema.

## File Naming

Use `<name>-<version>` as the filename prefix throughout the directory — the source name plus version, lowercase, hyphenated. This makes every file self-identifying even out of context.

- **Directory metadata** (required, one per document): `<name>-<version>-metadata.json`
- **Per-file sidecar** (optional, when a file deviates from directory defaults): `<filename>-file-metadata.json`

Example layout (illustrative: since 2026-11-13 these PCI DSS files live in the private companion dataset, because PCI DSS is a Tier 4 source, and this repository keeps only the metadata stub; the layout rule is the same in both repositories):

```
control/pcisecuritystandards.org/pci-dss/v4.0.1/
├── pci-dss-v4.0.1-metadata.json          ← directory metadata (REQUIRED)
├── pci-dss-v4.0.1.md                     ← marker markdown extraction
├── pci-dss-v4.0.1.json                   ← marker block tree
├── pci-dss-v4.0.1_meta.json              ← marker's own metadata
├── pci-dss-v4.0.1-requirements.csv       ← structured requirements
├── pci-dss-v4.0.1-requirements.json      ← same as JSON
├── parse_pci_dss.py                      ← reproducibility script (name reflects content)
├── _page_*.jpeg                          ← marker page images (referenced by markdown)
└── pci-dss-v4.0.1.pdf-file-metadata.json ← OPTIONAL sidecar for the gitignored PDF
```

For NIST CSF 2.0:

```
control/nist.gov/csf/2.0/
├── csf-2.0-metadata.json                 ← directory metadata
├── csf-2.0.md                            ← markdown extraction
├── csf-2.0.csv                           ← structured controls
├── csf-2.0.json                          ← structured controls (JSON)
├── csf-2.0-core.xlsx                     ← source spreadsheet (gitignored if large)
└── extract_csf.py                        ← reproducibility script
```

**Rule of thumb:** the `<name>-<version>` prefix matches the last two path components. For `control/pcisecuritystandards.org/pci-dss/v4.0.1/`, that's `pci-dss-v4.0.1`. For `control/nist.gov/csf/2.0/`, that's `csf-2.0`. For documents without versions (e.g., `regulation/europa.eu/ai-act/`), use just the name: `ai-act-metadata.json`.

Scripts, source files retaining publisher's exact filename (XLSX, PDF source), and marker-generated page images keep their natural names — only the extraction outputs follow the `<name>-<version>` prefix convention.

## Directory Metadata Schema

```json
{
  "secid": "secid:control/pcisecuritystandards.org/pci-dss@4.0.1",
  "name": "Payment Card Industry Data Security Standard",
  "acronym": "PCI DSS",
  "alternate_names": ["PCI-DSS"],
  "version": "4.0.1",
  "publication_id": "PCI-DSS-v4_0_1",
  "owner": "PCI Security Standards Council, LLC",
  "type": "Standard",

  "description": "Multi-paragraph description of what the document is.",
  "relationToCloudSecurity": "How this document relates to cloud security.",
  "relationToAISecurity": "How this document relates to AI security.",

  "license": {
    "spdx": "LicenseRef-PCI-SSC-Read-Copy-License",
    "redistribution": "prohibited",
    "derivatives": "modification_prohibited_per_section_III_1_2",
    "publicly_redistributable": false,
    "license_text_url": "https://www.pcisecuritystandards.org/terms_and_conditions/",
    "notes": "Any clarifying notes about the license."
  },

  "links": {
    "wikipedia": "https://en.wikipedia.org/wiki/...",
    "source": "https://www.pcisecuritystandards.org/document_library/",
    "textUsed": "https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf",
    "csaLocation": ""
  },

  "lifecycle": {
    "published": "2024-06",
    "active": true,
    "supersedes": "PCI DSS v4.0 (March 2022)",
    "supersededBy": null,
    "retiredFromActiveUse": null,
    "notes": "Optional context about this version's place in the version history."
  },

  "current_extraction": {
    "s3_timestamp": "2026-05-10T10-03-09Z",
    "tool": "marker_single",
    "tool_version": "marker-pdf 1.10.2",
    "extraction_host": "WSL2 Ubuntu on RTX 3060",
    "flags": [
      "--output_format markdown|json",
      "--highres_image_dpi 288",
      "--paginate_output"
    ],
    "force_ocr": false,
    "notes": "Free-text notes about the extraction (what was tried, what was discarded, why this extraction wins)."
  },

  "extraction_history": [
    {
      "s3_timestamp": "2026-05-09T22-45-48Z",
      "status": "superseded",
      "reason": "Force OCR artifacts and 9 missed requirement IDs",
      "tool": "marker_single",
      "force_ocr": true
    },
    {
      "s3_timestamp": "2026-05-10T10-03-09Z",
      "status": "current",
      "reason": "Clean text-layer extraction; zero OCR artifacts",
      "tool": "marker_single",
      "force_ocr": false
    }
  ],

  "scope": {
    "top_level_requirements": 12,
    "goals": 6
  }
}
```

### Field-by-Field

#### Required

| Field | Type | Description |
|---|---|---|
| `secid` | string | Canonical SecID identifier for the document. Format: `secid:{type}/{namespace}/{name}@{version}`. Must match the directory path. |
| `name` | string | Full official name of the document. |
| `acronym` | string | Common abbreviation (e.g., "PCI DSS", "CCM", "CSF"). |
| `version` | string | Version designator (e.g., `4.0.1`, `r5`, `2022`). |
| `owner` | string | Publishing organization. |
| `type` | string | Free-text classification (e.g., "Standard", "Regulation", "Framework"). The SecID type lives in the `secid` field. |
| `description` | string | What the document is. Multi-paragraph allowed. |
| `license` | object | Machine-readable license info (see below). |
| `links` | object | URLs for the document (see below). |

#### Recommended

| Field | Type | Description |
|---|---|---|
| `alternate_names` | array | Other names/aliases practitioners use. |
| `version_aliases` | array | Other version strings that denote this same release. See [Version aliases](#version-aliases). |
| `publication_id` | string | Publisher's exact publication identifier (e.g., `NIST.CSWP.29`, `PCI-DSS-v4_0_1`). |
| `access_tier` | integer | The source's tier under the 4-tier hosting rule: `1`, `2`, `3` or `4`. See [Access tier and evidence](#access-tier-and-evidence). |
| `tier_evidence` | object | How the tier was established: `url`, `checked`, `method`, `note`. Required whenever `access_tier` is set. |
| `relationToCloudSecurity` | string | How this affects cloud security. |
| `relationToAISecurity` | string | How this affects AI security. |
| `lifecycle` | object | Version lifecycle (published, supersedes, retired). |
| `current_extraction` | object | Provenance of the data in this directory. |
| `extraction_history` | array | Prior extractions preserved in S3 archive. |

#### Optional

| Field | Type | Description |
|---|---|---|
| `scope` | object | Source-specific stats (number of controls, requirements, articles, etc.). |
| `notes` | string | Free-text additional info. |

### Version aliases

Publishers routinely refer to one release by more than one version string —
a download page says "v1.1" while the file inside says "1.1.0", or a spec is
cited both as `4.0.1` and `v4_0_1`. The directory name picks one; `version_aliases`
records the others so a lookup on any of them lands on the right release.

**Rule: the directory and the `version` field use the version the artifact states
about itself** — the string inside the file, not the one on the download page.
Marketing pages round and abbreviate; the artifact's internal stamp is what a
consumer parsing the file will actually see. Everything else goes in
`version_aliases`.

```json
"version": "1.1.0",
"version_aliases": ["1.1", "v1.1", "v1.1.0"],
```

Worked example — CSA AICM v1.1:

| Where | String |
|---|---|
| Cell A1 of every worksheet | `{"specification_version":"1.1.0"}` |
| Spreadsheet filename | `AICMv1.1.0-generated_at_2026_06_18.xlsx` |
| CSA artifact / download page | "AI Controls Matrix **v1.1**" |
| Bundle ZIP and PDF titles | "AICM **v1.1**" |

The artifact stamps itself `1.1.0`, so the directory is `aicm/1.1.0/`, `version`
is `"1.1.0"`, and `"1.1"` is an alias. This also matches the sibling releases
(`1.0.3`, `0.0.2`), keeping the version sort stable across the source.

Aliases are for the *same* release under a different label. They are **not** a
compatibility claim: two genuinely different releases never alias to each other,
however similar their numbers look.

Note that the `v` prefix is a directory-naming convention that varies by
publisher and by SecID type root, not part of the version itself — PCI uses
`v4.0.1`, NIST uses `r5`, CSA control frameworks use bare `1.1.0` while CSA
guidance documents under `reference/` use `v1.1`. List both forms as aliases
when the distinction could trip up a lookup.

### License Object

```json
"license": {
  "spdx": "LicenseRef-PCI-SSC-Read-Copy-License",
  "redistribution": "prohibited",
  "derivatives": "modification_prohibited_per_section_III_1_2",
  "publicly_redistributable": false,
  "license_text_url": "https://www.pcisecuritystandards.org/terms_and_conditions/",
  "notes": "Optional clarifying notes."
}
```

| Field | Required? | Description |
|---|---|---|
| `spdx` | Yes | SPDX identifier when available (e.g., `CC-BY-4.0`, `CC-BY-SA-4.0`, `Apache-2.0`, `CC0-1.0`). Use `LicenseRef-{custom}` for non-SPDX licenses. |
| `redistribution` | Yes | Free-text: `permitted`, `permitted_with_attribution`, `permitted_for_study_purposes`, `prohibited`, etc. |
| `derivatives` | Yes | Free-text: `permitted`, `permitted_with_attribution`, `share_alike_required`, `adaptations_noncommercial_only_never_shared` (e.g., CC BY-NC-ND 4.0: Adapted Material may be produced for non-commercial purposes only and never shared; format-only conversions are not Adapted Material under its Section 2(a)(4)), `prohibited`. |
| `publicly_redistributable` | Yes | Boolean. Drives whether content goes in this public repo or the private archive. Set it from the source's access tier under the 4-tier hosting rule (AGENTS.md), not only from the licence text: a Tier 3 (free login) or Tier 4 (paid / members-only) source is `false` here unless Kurt grants an exception (see [Public hosting exceptions](#public-hosting-exceptions)); a Tier 1 or Tier 2 source is `true` even when the publisher's terms do not grant redistribution. When `access_tier` is recorded, CI checks that the two agree (see [Access tier and evidence](#access-tier-and-evidence)). A directory that holds content may not say `false`. |
| `license_text_url` | Recommended | URL to the full license text. |
| `notes` | Optional | Free-text caveats. |

The other licence fields (`spdx`, `redistribution`, `derivatives`, `notes`) record what the **publisher's terms** say, and they stay accurate even when the tier rule overrides them. A government document whose terms are unclear, or a vendor glossary whose copyright notice grants nothing, keeps `redistribution: "unclear"` or `"not_permitted_without_authorization"`, while `publicly_redistributable` is `true` because the 4-tier rule allows hosting it. Say so in `notes` (for example: "the public copy here rests on the 4-tier hosting rule, not on a licence from the publisher"); never write "internal use only" or "private working copy" in the metadata of a public entry.

### Access tier and evidence

```json
"access_tier": 1,
"tier_evidence": {
  "url": "https://www.ipa.go.jp/security/guide/hjuojm00000055l0-att/000045873.pdf",
  "checked": "2026-11-14",
  "method": "fetch",
  "note": "Direct PDF download from ipa.go.jp, no login (HTTP 206, application/pdf)."
}
```

`access_tier` records which tier of the 4-tier hosting rule (AGENTS.md) the source is in; place it right after `license`. Kurt Seifried, 2026-11-09: *"so in general anything we get from a public gov website, goes into the public dataset repo regardless of license. in general if it's on the web, and there's no login, we treat it as if we can mirror it. if there is a free login, ask me, and if it' a paid login, or paid access like iso.org, we do NOT mirror it publicly ever unless there is a specific exception granted, and it would have to be explicit and well documented and have solid reasons for it."*

| `access_tier` | Meaning | `publicly_redistributable` | Content in this repository |
|---|---|---|---|
| `1` | Public government or intergovernmental website | `true` | Allowed, regardless of licence |
| `2` | Open web, no login | `true` | Allowed, regardless of licence |
| `3` | Free login or registration wall | `false` | Not allowed: Kurt approves each source first |
| `4` | Paid, members-only, or (as the program treats PCI SSC) a click-through licence | `false` | Not allowed unless Kurt grants an explicit exception |

A Tier 3 or Tier 4 source with a granted exception is the only case where the tier and `publicly_redistributable` disagree: the exception is an entry in the gate's `ALLOWLIST` (see [Public hosting exceptions](#public-hosting-exceptions)), never a metadata field.

`tier_evidence` says how the tier was established:

| Field | Description |
|---|---|
| `url` | The http(s) URL that was checked: the document itself where possible (`textUsed`), else the page that serves it. |
| `checked` | The date of the check, `YYYY-MM-DD`. |
| `method` | `fetch` (a scripted GET showed the content with no login), `browser` (loaded in a real browser, for JavaScript-rendered or bot-filtered sites), `host-suffix` (Tier 1 only, and only for a document that was acquired and whose metadata and README note no access restriction: the URL's host is a government domain in the gate's `GOV_HOST_SUFFIXES`; not fetched), or `recorded` (Tier 3 or 4 only: the program's own classification, not re-observed). |
| `note` | What was observed, in a sentence: "direct PDF download, no login", "registration form before download", "store sells it at US$90". |

Leave both fields out when the tier has not been established. Do not guess: a missing tier is honest, a wrong one is not. The tier belongs to the document, not to its publisher's domain: a government body can still put a document behind a members-only portal. `tools-resources/utils/backfill_access_tier.py` records Tier 1 by `host-suffix` only for entries that are already `publicly_redistributable: true`, whose every recorded source URL is on a government host, whose document was acquired (content other than README, metadata and sidecars), and whose metadata and README mention no access restriction (members-only, purchase, subscription, registration, awaiting a licensed copy, ...). Re-running it removes tags that no longer qualify. Anything else is set by hand after a check.

**Enforced in CI** by `tools-resources/utils/check_tier_restrictions.py` (check 4, blocking), for every edition metadata file:

- every file is governed by the metadata of the nearest directory at or above it that has metadata; one directory may hold only one edition metadata file, and a record that is not restrictive may not sit below a restrictive one;
- `license.publicly_redistributable` must be present and a boolean (`"false"` as a string fails);
- a restrictive record (`publicly_redistributable` not true, or Tier 3/4) governs only a stub: the metadata within the stub caps, one `README.md` beside it within the README cap, and no content. Content is everything else, including `-file-metadata.json` sidecars and READMEs in subdirectories;
- `access_tier` must be the integer 1-4 with a complete `tier_evidence` (`checked` a real date, not in the future); `tier_evidence` without `access_tier` fails;
- Tier 1 or 2 requires `publicly_redistributable: true`; Tier 3 or 4 requires `false`, unless a `tier3-4-exception` `ALLOWLIST` entry names that exact directory and the record's SecID, in which case only the entry's listed files, directly in that directory, may be there;
- `host-suffix` may only claim Tier 1, on a host in `GOV_HOST_SUFFIXES`, for an acquired document whose metadata and README mention no access restriction; `recorded` may only claim Tier 3 or 4. A record can keep a source private, never make it public.

### Links Object

```json
"links": {
  "wikipedia": "https://en.wikipedia.org/wiki/...",
  "source": "https://publisher.tld/document-page",
  "textUsed": "https://publisher.tld/path/to.pdf",
  "csaLocation": ""
}
```

| Field | Description |
|---|---|
| `wikipedia` | Wikipedia article URL if one exists. |
| `source` | Publisher's main page for the document. |
| `textUsed` | Direct URL to the file we extracted from. |
| `csaLocation` | If CSA has a relevant page (free-text, sometimes empty). |

Add other keys as needed (`api`, `docs`, `bulk_data`, etc.) following the same `{type}: {url}` pattern.

### Lifecycle Object

```json
"lifecycle": {
  "published": "2024-06",
  "active": true,
  "supersedes": "PCI DSS v4.0 (March 2022)",
  "supersededBy": null,
  "retiredFromActiveUse": null,
  "notes": ""
}
```

| Field | Description |
|---|---|
| `published` | ISO date or `YYYY-MM` of publication. |
| `active` | Boolean — is this version currently in force? |
| `supersedes` | Human-readable reference to the previous version (or null). |
| `supersededBy` | Human-readable reference to the successor version (or null). |
| `retiredFromActiveUse` | ISO date when this version was retired (or null if still active). |
| `notes` | Free-text context. |

### Current Extraction Object

```json
"current_extraction": {
  "s3_timestamp": "2026-05-10T10-03-09Z",
  "tool": "marker_single",
  "tool_version": "marker-pdf 1.10.2",
  "extraction_host": "WSL2 Ubuntu on RTX 3060",
  "flags": ["--output_format markdown|json", "--paginate_output"],
  "force_ocr": false,
  "notes": ""
}
```

| Field | Description |
|---|---|
| `s3_timestamp` | UTC timestamp of the extraction folder in S3, format `YYYY-MM-DDTHH-MM-SSZ`. |
| `tool` | Extraction tool name (`marker_single`, `pdfplumber`, `excel_to_csv`, etc.). |
| `tool_version` | Version of the tool used. |
| `extraction_host` | Free-text description of the host (informational, for debugging). |
| `flags` | List of CLI flags used. |
| `force_ocr` | Boolean (for marker extractions). |
| `notes` | Free-text — why this extraction was chosen, what failed before. |

### Desired End State Object

```json
"desired_end_state": {
  "state": "structured",
  "reason": "control-catalog",
  "notes": null
}
```

Records the **intended** terminal state for the document, paired with `current_extraction` (which records what's actually been done). The gap between `desired_end_state.state` and the doc's current filesystem state (computed by `build_index.py`) is the actual work backlog — and where they match, the doc is "done" relative to its intent.

| Field | Description |
|---|---|
| `state` | One of: `structured`, `extracted`, `metadata-only`, `dropped`. |
| `reason` | Controlled-vocab tag explaining *why* this is the intended state. |
| `notes` | Optional free-text nuance (e.g., "borderline; review when CIS license clarifies"). |

#### Controlled `reason` vocabulary (paired with `state`)

| `state` | `reason` | meaning |
|---|---|---|
| `structured` | `control-catalog` | per-control rows (NIST 800-53, FedRAMP baselines, CCM) |
| `structured` | `taxonomy` | hierarchical taxonomy (CWE, ATT&CK, AI 100-2 attacks) |
| `structured` | `requirement-list` | numbered requirements (PCI DSS, regulations with statute provisions) |
| `structured` | `glossary` | per-term rows |
| `extracted` | `prose-guidance` | guidance doc; markdown is canonical (NIST SP guidance, CSWPs) |
| `extracted` | `algorithm-spec` | crypto / protocol specification (FIPS 197 AES, FIPS 202 SHA-3) |
| `extracted` | `policy-doc` | policy/framework with no per-item structure (NSM-AI Framework) |
| `extracted` | `template` | fillable template (FedRAMP SSP appendices F/G/Q) |
| `extracted` | `playbook` | process playbook (FedRAMP CSP Authorization Playbook) |
| `metadata-only` | `licensed` | restricted-license or Tier 3/4 access; can't host publicly (ISO, IEEE, PCI DSS, HITRUST, members-only) |
| `metadata-only` | `upstream-only` | publisher hosts version-tagged authoritative data (MITRE ATT&CK STIX, CVE Project) |
| `metadata-only` | `pending-acquisition` | source not yet acquired |
| `metadata-only` | `pending-extraction` | source acquired, marker run pending |
| `metadata-only` | `pending-structuring` | extracted, parser not yet written |
| `metadata-only` | `pre-release` | publication is forthcoming / in draft at the publisher; nothing to acquire yet |
| `metadata-only` | `historical` | program/document is from a bygone era (e.g., 2018–2019); publisher no longer maintains or publishes the source; stub kept as a historical reference, not a gap |
| `dropped` | `withdrawn` | publisher withdrew; no successor in repo |
| `dropped` | `superseded` | newer version already structured here |

For the meaningful-gap analysis, see `tools-resources/utils/backfill_desired_end_state.py` (heuristic backfill) and the `build_index.py` summary which compares current vs desired.

### Public hosting exceptions

There is no metadata field for this. Under the 4-tier hosting rule (see [AGENTS.md](AGENTS.md#licensedrestricted-content-is-not-committed-here-4-tier-hosting-rule-2026-11-09)), content from a Tier 3 (free login) or Tier 4 (paid / members-only) source is never hosted in this public repository unless Kurt grants a specific, explicit, well-documented exception with solid reasons. A metadata file cannot grant itself one.

When Kurt grants an exception, it is recorded as an entry in the `ALLOWLIST` constant in `tools-resources/utils/check_tier_restrictions.py`:

```python
{
    "kind": "tier3-4-exception",
    "path": "control/<namespace>/<name>/<version>",      # one exact edition directory
    "secid": "secid:control/<namespace>/<name>@<version>",  # must equal that directory's metadata secid
    "files": ["<name>-<version>.md"],                    # explicit file names in that directory only
    "approved_by": "Kurt Seifried",
    "date": "YYYY-MM-DD",
    "reason": "The solid reasons, in enough detail to be checked.",
    "reference": "https://github.com/<CSA org>/<repo>/issues/<n>",  # his recorded decision
}
```

The gate validates every entry: all fields present, a real date that is neither in the future nor before the rule (2026-11-09), a reason of substance, a reference to a GitHub issue, PR or decision document in a CSA organization, and, for this kind, `approved_by` equal to Kurt. An entry covers only the files it lists, directly in its directory. Subdirectories, sibling editions and the publisher directory inherit nothing.

A second kind, `tier1-2-source`, records a source that is itself Tier 1 or 2 (public, no login) although its publisher's standards are gated. It is a classification, not an exception, and it carries an `evidence` URL for the public upstream. Today the only entry is the OVAL Repository text under `reference/cisecurity.org/oval/` (upstream: the public GitHub repository CISecurity/OVALRepo).

Adding or widening an entry changes a CI gate. Under the program's rules that needs a different-vendor review and a decision record, so an agent cannot approve its own exception. The gate checks entries for syntax only: a typed `approved_by` proves nothing. The reviewer must open the linked `reference` and confirm Kurt approved that exact entry.

**Every file under a Tier 3/4 publisher domain is also fingerprinted.** The script's `FINGERPRINTS` maps each allowed path to its reviewed SHA-256. That covers stubs as well as allowlisted files. A new stub, or an edit to an existing one, fails CI until a reviewed gate change adds or updates its line; `--print-fingerprints` prints the lines to add. This stops restricted text from being placed in a capped stub, chunked across new edition directories, or swapped into an existing README.

Without an entry (and in addition to its fingerprint), a file in a Tier 3/4 publisher directory must be a stub: the edition's own `<dir>-metadata.json` (or `<parent>-<dir>-metadata.json`), which must be valid JSON within 16 KiB, with no string longer than 3,000 characters and a `secid` that names the directory, plus at most one `README.md` of up to 6 KiB beside it. Per-file sidecars and marker `_meta.json` files count as content there.

### Extraction History (Array)

Each element is a prior extraction kept in S3. Same shape as `current_extraction` plus a `status` and `reason`:

```json
{
  "s3_timestamp": "2026-05-09T22-45-48Z",
  "status": "superseded",
  "reason": "Force OCR artifacts and 9 missed requirement IDs",
  "tool": "marker_single",
  "force_ocr": true
}
```

Status values: `current`, `superseded`, `failed`, `legacy`.

## Per-File Sidecar Schema

Sidecars are **optional** — only present when a file deviates from the directory's default license/source/method.

Naming: `[filename]-file-metadata.json` (filename including extension). For example, `PCI-DSS-v4.0.1.pdf-file-metadata.json` for the PDF.

```json
{
  "filename": "PCI-DSS-v4.0.1.pdf",
  "role": "source",
  "sha256": "...",
  "retrieved_from": "https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf",
  "retrieved_at": "2026-05-09T13:40:00Z",
  "retrieved_method": "manual_browser_after_pci_ssc_license_accept",
  "license_override": null,
  "notes": ""
}
```

| Field | Description |
|---|---|
| `filename` | Filename this sidecar describes. |
| `role` | What this file is in the directory: `source`, `extraction`, `derived`, `image`, etc. |
| `sha256` | Hex digest of the file content. |
| `retrieved_from` | Source URL if the file was downloaded. |
| `retrieved_at` | ISO timestamp of retrieval. |
| `retrieved_method` | How: `curl`, `manual_browser`, `manual_browser_after_pci_ssc_license_accept`, `marker_extraction`, etc. |
| `license_override` | If this specific file has a different license than the directory default (rare). |
| `notes` | Free-text. |

## Validation

Future tooling will validate metadata files. For now, manual review during PR.

A metadata file is **valid** when:
1. It parses as JSON
2. Required fields are present
3. `secid` matches the directory path
4. `license.spdx` is set (use `LicenseRef-{...}` for non-SPDX)
5. `license.publicly_redistributable` is set (boolean), and is not `false` in a directory that holds content
6. If `access_tier` is set, it agrees with `publicly_redistributable` and carries valid `tier_evidence` (see [Access tier and evidence](#access-tier-and-evidence))

Tier restrictions and rules 5-6 are checked in CI: `python3 -I tools-resources/utils/check_tier_restrictions.py` (see [Public hosting exceptions](#public-hosting-exceptions) and [Access tier and evidence](#access-tier-and-evidence)).

## Examples in the Repo

- `control/pcisecuritystandards.org/pci-dss/v4.0.1/pci-dss-v4.0.1-metadata.json` (metadata-only stub for a Tier 4 source; the full extraction is in the private dataset)
- `control/nist.gov/csf/2.0/csf-2.0-metadata.json`
