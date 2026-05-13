# Dataset: Public Laws, Regulations, and Standards

Public repository of bulk-processed laws, regulations, standards, frameworks, and reference documents related to cloud and AI security. Maintained by the [Cloud Security Alliance](https://cloudsecurityalliance.org).

## What's Here

Machine-readable extractions of public-license security knowledge:

- **Regulations** — EU AI Act, GDPR, NIS2, DORA, BSI AI C4, US federal/state laws
- **Standards & frameworks** — NIST CSF 2.0, NIST SP 800-53, PCI DSS, CSA CCM, CSA AICM, HITRUST CSF
- **Weakness taxonomies** — MITRE CWE, OWASP Top 10
- **Adversary techniques** — MITRE ATT&CK, ATLAS, FIGHT
- **Methodologies** — NIST IR 8477, CVSS, others
- **Reference documents** — AI model cards, system cards, vendor security guidance

Each document is provided as the original markdown extraction plus structured CSV/JSON keyed by the document's atomic units (requirement IDs, control IDs, article numbers, etc.).

## Architecture

This repository is the **bulk-processed layer** of a three-tier data architecture:

```
SecID registry              ← identity, resolution, namespace rules
   ↓
This repository             ← bulk processed content (full docs, MD/CSV/JSON)
   ↓
SecID-{type} repos          ← per-item splits (future)
```

- [SecID registry](https://github.com/CloudSecurityAlliance/SecID) provides the identifier grammar and authoritative classification
- This repo holds the **current** extraction of each document; full extraction history lives in S3
- Future per-item repos (`SecID-control`, `SecID-weakness`, etc.) will split bulk content into per-item JSON files keyed by SecID

## Repository Layout

Mirrors SecID's `type/namespace/name/version/` structure:

```
control/        ← security requirements (CCM, CSF, PCI DSS, 800-53, etc.)
regulation/     ← legally binding (GDPR, AI Act, NIS2, etc.)
weakness/       ← vulnerability taxonomies (CWE, OWASP Top 10)
ttp/            ← adversary techniques (ATT&CK, ATLAS)
methodology/    ← analysis processes (CVSS, IR 8477)
reference/      ← informative documents (model cards, system cards, best practices, research)
tools-resources/ ← extraction utilities and pipeline scripts
```

Within each type, paths follow the SecID identifier:

```
secid:control/nist.gov/800-53@r5#AC-1
   → control/nist.gov/800-53/r5/
```

See [`CLAUDE.md`](CLAUDE.md) for full structural details and [`PROMPT-CLASSIFICATION.md`](PROMPT-CLASSIFICATION.md) for the classification process.

## Metadata Convention

Every document directory contains a `[dirname]-metadata.json` describing the document — SecID identifier, license (SPDX), source URLs, version lifecycle, and extraction provenance. See [`METADATA-SCHEMA.md`](METADATA-SCHEMA.md) for the full schema.

## Licensing

This repository contains only **publicly redistributable** content under each source's license:

- US government works (NIST publications) — public domain
- EU legislation — EUR-Lex reuse policy
- MITRE CWE — MITRE CWE Terms of Use
- CSA CCM/AICM — CSA-published (free for non-commercial use with attribution)
- PCI SSC standards — PCI SSC Read and Copy License
- OWASP — CC BY-SA 4.0

Each document's `[dirname]-metadata.json` carries an SPDX license identifier and redistribution flag.

**Licensed/restricted content** (ISO, IEEE, etc.) is **not** stored here — the directory carries metadata-only stubs with purchase URLs. The full content lives in a separate private archive.

## Sister Repository

- [SecID](https://github.com/CloudSecurityAlliance/SecID) — the identifier grammar, namespace registry, and resolution rules. Defines the classification used by this repo.

## Contributing

Contributions follow standard GitHub flow: fork, branch, PR.

1. Find or add the SecID namespace entry in [SecID](https://github.com/CloudSecurityAlliance/SecID) first
2. Place content at the computed path: `{type}/{namespace}/{name}/{version}/`
3. Add `[dirname]-metadata.json` per [`METADATA-SCHEMA.md`](METADATA-SCHEMA.md)
4. Open a PR

For complex documents requiring extraction (PDFs with structured tables), see `CLAUDE.md` for the marker workflow.

## License

CC0 1.0 Universal for the metadata, extraction scripts, and structural additions. Source content retains its original license; see each document's metadata for specifics.
