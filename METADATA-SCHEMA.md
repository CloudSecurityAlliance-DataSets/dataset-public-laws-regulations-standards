# Metadata Schema

Every document directory in this repository contains a metadata file describing the document. This doc defines the schema.

## File Naming

Use `<name>-<version>` as the filename prefix throughout the directory — the source name plus version, lowercase, hyphenated. This makes every file self-identifying even out of context.

- **Directory metadata** (required, one per document): `<name>-<version>-metadata.json`
- **Per-file sidecar** (optional, when a file deviates from directory defaults): `<filename>-file-metadata.json`

Example layout:

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
    "redistribution": "permitted_for_study_purposes",
    "derivatives": "modification_prohibited_per_section_III_1_2",
    "publicly_redistributable": true,
    "license_text_url": "https://www.pcisecuritystandards.org/document_library_terms/",
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
| `publication_id` | string | Publisher's exact publication identifier (e.g., `NIST.CSWP.29`, `PCI-DSS-v4_0_1`). |
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

### License Object

```json
"license": {
  "spdx": "LicenseRef-PCI-SSC-Read-Copy-License",
  "redistribution": "permitted_for_study_purposes",
  "derivatives": "modification_prohibited_per_section_III_1_2",
  "publicly_redistributable": true,
  "license_text_url": "https://www.pcisecuritystandards.org/document_library_terms/",
  "notes": "Optional clarifying notes."
}
```

| Field | Required? | Description |
|---|---|---|
| `spdx` | Yes | SPDX identifier when available (e.g., `CC-BY-4.0`, `CC-BY-SA-4.0`, `Apache-2.0`, `CC0-1.0`). Use `LicenseRef-{custom}` for non-SPDX licenses. |
| `redistribution` | Yes | Free-text: `permitted`, `permitted_with_attribution`, `permitted_for_study_purposes`, `prohibited`, etc. |
| `derivatives` | Yes | Free-text: `permitted`, `permitted_with_attribution`, `share_alike_required`, `prohibited`. |
| `publicly_redistributable` | Yes | Boolean. Drives whether content goes in this public repo or the private archive. |
| `license_text_url` | Recommended | URL to the full license text. |
| `notes` | Optional | Free-text caveats. |

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
| `metadata-only` | `licensed` | restricted-license; can't redistribute (ISO, IEEE, members-only) |
| `metadata-only` | `upstream-only` | publisher hosts version-tagged authoritative data (MITRE ATT&CK STIX, CVE Project) |
| `metadata-only` | `pending-acquisition` | source not yet acquired |
| `metadata-only` | `pending-extraction` | source acquired, marker run pending |
| `metadata-only` | `pending-structuring` | extracted, parser not yet written |
| `metadata-only` | `pre-release` | publication is forthcoming / in draft at the publisher; nothing to acquire yet |
| `dropped` | `withdrawn` | publisher withdrew; no successor in repo |
| `dropped` | `superseded` | newer version already structured here |

For the meaningful-gap analysis, see `tools-resources/utils/backfill_desired_end_state.py` (heuristic backfill) and the `build_index.py` summary which compares current vs desired.

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
5. `license.publicly_redistributable` is set (boolean)

## Examples in the Repo

- `control/pcisecuritystandards.org/pci-dss/v4.0.1/pci-dss-v4.0.1-metadata.json`
- `control/pcisecuritystandards.org/pci-dss/v4.0/pci-dss-v4.0-metadata.json` (legacy markdown only)
- `control/nist.gov/csf/2.0/csf-2.0-metadata.json`
