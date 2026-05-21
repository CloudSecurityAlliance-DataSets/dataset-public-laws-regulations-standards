# Classification Guide

**This repository mirrors [SecID](https://github.com/CloudSecurityAlliance/SecID) 100%.** Every directory path here is a direct projection of a SecID identifier. When SecID and this repo disagree, this repo is wrong and must be reconciled. The audit script in this repo verifies that every metadata `secid` field resolves to a SecID registry namespace.

## TL;DR

Given a new document, decide three things:

1. **SecID type** — one of: `advisory`, `weakness`, `ttp`, `control`, `capability`, `methodology`, `disclosure`, `regulation`, `entity`, `reference`. **`reference/` is the catch-all** — use it whenever a document doesn't cleanly fit another type. Do not invent types and do not force-fit.
2. **Namespace** — the publisher's **DNS domain name** (e.g., `nist.gov`, `pcisecuritystandards.org`, `cloudsecurityalliance.org`). For US states use the canonical state portal DNS (`ca.gov`, `ny.gov`, `mass.gov`, `wa.gov` — not the expanded form). Verify with `host <domain>` when unsure.
3. **Name** — what the publisher calls the source, taken from the SecID registry entry's match_nodes (e.g., `csf`, `pci-dss`, `ccm`, `cwe`, `800-53`).

The directory path is then `{type}/{namespace}/{name}/{version}/`.

## Classification Process

### Step 1 — Determine the SecID Type

| Document is... | SecID type |
|---|---|
| Legally binding (statute, regulation, directive, executive order with regulatory effect) | `regulation` |
| Voluntary control framework / standard | `control` |
| Vulnerability/weakness taxonomy | `weakness` |
| Adversary technique catalog | `ttp` |
| Analysis methodology (mapping, scoring, evaluation process) | `methodology` |
| Vendor security feature / product capability | `capability` |
| Vulnerability disclosure program | `disclosure` |
| Vulnerability advisory / record | `advisory` |
| Organization / product / service identifier | `entity` |
| **Anything else** — research paper, white paper, blog post, model card, system card, mapping document, glossary, vendor guidance, fact sheet | `reference` |

**`reference/` is the catch-all. Use it whenever in doubt.** It's better to land in `reference/` and migrate later than to force-fit into a wrong type or invent a new one.

Type list is **fixed in SecID v1.0** — don't invent new types here. If a document genuinely needs one, raise it in SecID first; only after SecID adds the type does it appear in this repo.

### Step 1.5 — Check for a subtype

Once the type is determined, check the SecID match_node's `data.subtype:` array (if any). Subtypes refine within-type classification without inflating the official type list:

- A glossary is `reference` with `subtype: ["glossary"]`
- CVSS is `methodology` with `subtype: ["scoring"]`
- NIST IR 8477 is `methodology` with `subtype: ["mapping"]`
- TLP is `methodology` with `subtype: ["classification"]`

When in doubt about an emerging sub-category, **try a subtype first** — don't propose a new type. New-type splits require all four criteria (resolution patterns diverge, consumers diverge, semantics drift, volume justifies); subtype tags are reversible registry edits.

The full subtype catalog — named subtypes currently in use, anticipated subtypes (BoK on `control`, course on `reference`), candidate patterns (CNA / bug-bounty on `disclosure`; law / directive / transposition on `regulation`; organization / product / service on `entity`), and the four-criteria split gate — lives in [SecID's TYPES-AND-SUBTYPES.md](https://github.com/CloudSecurityAlliance/SecID/blob/main/docs/reference/TYPES-AND-SUBTYPES.md).

**Fetch the live file from GitHub every time before classifying a document whose sub-category isn't already obvious from a registry match.** Use `WebFetch` against the URL above (or `curl`/`gh` on the raw form). The doc is actively maintained — new subtypes land, candidates get promoted to in-use, and the examples here in PROMPT-CLASSIFICATION.md are a snapshot that drifts. Don't classify from memory or from cached excerpts; read the current file.

### Step 2 — Look Up or Add the SecID Namespace

Consult the SecID registry at `~/GitHub/CloudSecurityAlliance/SecID/registry/{type}/{tld}/{org}.{md,json}`.

- If the org already has a namespace entry → use its canonical namespace and source naming
- If new → propose a SecID registry addition first (PR against SecID), then use what's accepted there. **Do not add a document here pointing at a namespace SecID doesn't know about.**

#### The DNS-canonical rule

A namespace MUST be the **DNS domain of the publishing organization** — the actual hostname they publish from.

- Verify with `host <domain>`. If it's NXDOMAIN, it isn't a namespace.
- For US states: use the **canonical state portal DNS**:
  - California → `ca.gov` (not `california.gov` — NXDOMAIN)
  - Connecticut → `ct.gov` (not `connecticut.gov` — NXDOMAIN)
  - New York → `ny.gov` (not `new-york.gov` — NXDOMAIN)
  - Indiana → `in.gov`, Massachusetts → `mass.gov`, Montana → `mt.gov`
  - Nevada → `nv.gov`, Tennessee → `tn.gov`, Washington → `wa.gov`
- When two domains resolve to the same site, prefer the form the organization uses for itself (`mass.gov`, not `massachusetts.gov`).
- For platforms with sub-sites, use a **path namespace**: `github.com/advisories` for GHSA (not a bespoke domain). See SPEC.md §1.2.

The SecID entry tells you:
- Canonical namespace (`nist.gov` vs `usnist.gov`, `cloudsecurityalliance.org` vs `csa.org`)
- Canonical source name (`csf` not `cybersecurity-framework`, `pci-dss` not `pci`, `ccm` not `cloud-controls-matrix`)
- Known versions and their lifecycle status
- Whether version is required to disambiguate (`version_required: true`)

### Step 3 — Compute the Path

```
{type}/{namespace}/{name}/{version}/
```

Version directory naming follows the publisher's natural convention:

| Publisher convention | Version dir |
|---|---|
| PCI uses "PCI DSS v4.0.1" | `v4.0.1` |
| NIST uses "Revision 5" / "r5" | `r5` |
| CSA artifacts named "CCM 4.0.13" | `4.0.13` |
| Standard has no version | no version subdir |

If the standard later gets a version, retroactively introduce the subdir at that point.

### Step 4 — Add Metadata

Create `[dirname]-metadata.json` per [METADATA-SCHEMA.md](METADATA-SCHEMA.md). Required fields:

- `secid` — the canonical SecID identifier matching the path
- `name`, `acronym`, `version`, `owner`, `type` — basic identification
- `license` — SPDX identifier + redistribution flags
- `links` — source URLs
- `current_extraction` — provenance for the extraction in this directory

## Examples

### Example 1 — NIST CSF 2.0

| Question | Answer |
|---|---|
| Document | NIST Cybersecurity Framework 2.0 (CSWP 29) |
| SecID type | `control` (security framework) |
| Namespace | `nist.gov` |
| Source name (per SecID registry) | `csf` |
| Version | `2.0` (NIST writes "CSF 2.0") |
| Path | `control/nist.gov/csf/2.0/` |
| SecID | `secid:control/nist.gov/csf@2.0` |
| Metadata file | `csf-2.0-metadata.json` |

The publication number (CSWP 29) goes in the metadata as `publication_id`, not in the path.

### Example 2 — PCI DSS v4.0.1

| Question | Answer |
|---|---|
| Document | Payment Card Industry Data Security Standard v4.0.1 |
| SecID type | `control` |
| Namespace | `pcisecuritystandards.org` |
| Source name | `pci-dss` |
| Version | `v4.0.1` (PCI explicitly writes the `v`) |
| Path | `control/pcisecuritystandards.org/pci-dss/v4.0.1/` |
| SecID | `secid:control/pcisecuritystandards.org/pci-dss@4.0.1` (SecID strips the `v`) |

Filesystem and SecID identifier can differ on the `v` prefix — the canonical form for SecID matters for resolution, the filesystem form mirrors what the publisher uses.

### Example 3 — EU AI Act

| Question | Answer |
|---|---|
| SecID type | `regulation` (legally binding) |
| Namespace | `europa.eu` |
| Source name | `ai-act` |
| Version | None (no formal version) |
| Path | `regulation/europa.eu/ai-act/` |

### Example 4 — OpenAI GPT-4 System Card

| Question | Answer |
|---|---|
| SecID type | `reference` (informative AI documentation) |
| Namespace | `openai.com` |
| Source name | `system-cards` (grouped) |
| Item | `gpt-4` |
| Path | `reference/openai.com/system-cards/gpt-4/` |

For organizations with many similar documents, group by document type (`model-cards/`, `system-cards/`). For one-off documents, place directly under the namespace.

### Example 5 — MITRE CWE

| Question | Answer |
|---|---|
| SecID type | `weakness` |
| Namespace | `mitre.org` |
| Source name | `cwe` |
| Version | `4.19.1` (current MITRE release) |
| Path | `weakness/mitre.org/cwe/4.19.1/` |

### Example 6 — A mapping document (edge case)

| Question | Answer |
|---|---|
| Document | CSA CCM → NIST 800-53 control mapping |
| SecID type | `reference` (no first-class mapping type yet) |
| Namespace | `cloudsecurityalliance.org` |
| Source name | `ccm-to-800-53-mapping` |
| Path | `reference/cloudsecurityalliance.org/ccm-to-800-53-mapping/` |

Mappings live in `reference/` for now. As we accumulate them, SecID may introduce a first-class mapping type, at which point we'd migrate.

### Example 7 — Licensed standard (members-only)

| Question | Answer |
|---|---|
| Document | ISF Standard of Good Practice for Information Security 2022 |
| SecID type | `control` |
| Namespace | `securityforum.org` |
| Source name | `sogp` |
| Version | `2022` |
| Path | `control/securityforum.org/sogp/2022/` |
| Content | **Metadata only** — `license.publicly_redistributable: false`, source URL pointing at ISF Member Portal in `links.source`. No actual standard text in this repo. Licensed content stays out of this public repository. |

## Edge Cases

1. **Document spans multiple SecID types** — pick the primary purpose. Document secondary types in metadata if needed.
2. **Multiple versions of same source** — each version is a sibling subdirectory under the source name. The metadata records lifecycle (`current`, `superseded`, `retired`).
3. **Publication number vs semantic name** — use the semantic name from SecID for the source dir (`csf` not `cswp.29`); record the publication number in `publication_id` metadata.
4. **No clear publisher namespace** — for documents from informal groups or individual researchers, use the most stable available domain (university domain, personal site, GitHub org). Note in metadata.
5. **Documents currently in legacy paths** — they're being migrated. See `CLAUDE.md` for migration plan. New additions should go to the new structure even before legacy is fully migrated.

## When to Stop and Ask

- **Cannot determine SecID type** after consulting the SecID registry → ask the human
- **Conflict between publisher's naming and existing SecID entry** → ask, propose SecID update
- **License terms unclear** → don't host; metadata-only stub with link to source
- **Document appears to be already covered by another canonical source** (e.g., OSV — data lives at osv.dev) → do not duplicate; rely on the SecID registry entry

## Verifying SecID Alignment

Run the audit any time you add or rename a document:

```bash
python3 tools-resources/utils/audit_secid_alignment.py
```

It scans every `*-metadata.json` in both this repo and the private repo, derives the expected SecID registry path from each `secid` field, and reports any namespace that isn't registered. A clean audit prints `Missing namespaces: 0` and exits 0.

Non-zero exit means one of:
- **The SecID registry needs a new namespace entry** — open a PR against [SecID](https://github.com/CloudSecurityAlliance/SecID) first, then update this repo to reference it.
- **The dataset metadata `secid` is wrong** — typo, non-canonical DNS (e.g., `california.gov` instead of `ca.gov`), or wrong type. Fix the metadata and rename the directory to match.

## Where the Authoritative Answers Live

- [SecID/SPEC.md](https://github.com/CloudSecurityAlliance/SecID/blob/main/SPEC.md) — full grammar and parsing rules
- [SecID/registry/](https://github.com/CloudSecurityAlliance/SecID/tree/main/registry) — all known namespaces and their canonical naming
- [SecID/docs/reference/TYPES-AND-SUBTYPES.md](https://github.com/CloudSecurityAlliance/SecID/blob/main/docs/reference/TYPES-AND-SUBTYPES.md) — the 10 frozen types, the `subtype:` convention, named subtypes in use today, and the four-criteria gate for splitting into a new type
- [SecID/docs/reference/NAMESPACE-MAPPING.md](https://github.com/CloudSecurityAlliance/SecID/blob/main/docs/reference/NAMESPACE-MAPPING.md) — historical short-name → domain-name migration map (also documents the US-state convention)
- [SecID/docs/reference/DATA-HOSTING-RULES.md](https://github.com/CloudSecurityAlliance/SecID/blob/main/docs/reference/DATA-HOSTING-RULES.md) — when to host content vs reference it externally
- [SecID/docs/explanation/DESIGN-DECISIONS.md](https://github.com/CloudSecurityAlliance/SecID/blob/main/docs/explanation/DESIGN-DECISIONS.md) — why the design is what it is
