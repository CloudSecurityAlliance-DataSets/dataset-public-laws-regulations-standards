# CWE (Common Weakness Enumeration)

MITRE's CWE provides a unified, measurable set of software and hardware weakness types that serve as a common language for describing security weaknesses.

## Overview

CWE is a community-developed list of common software and hardware security weaknesses. It serves as a common language, a measuring stick for tools, and as a baseline for weakness identification, mitigation, and prevention efforts.

## Key Information

- **Maintainer**: MITRE Corporation
- **Purpose**: Standardized software and hardware weakness classification
- **Format**: CWE-ID (e.g., CWE-79, CWE-89)
- **Scope**: Software weaknesses, hardware weaknesses, research concepts

## Documentation and Resources

- **Main Site**: https://cwe.mitre.org/
- **About Documents**: https://cwe.mitre.org/about/documents.html
- **CWE List**: https://cwe.mitre.org/data/index.html
- **Research Resources**: https://cwe.mitre.org/about/resources.html

### Official Documentation
- **Schema Documentation**: Describes CWE data structure elements and development guidance
- **CVE → CWE Mapping & Navigation Guidance**: Mapping criteria and search tips
- **CWE Compatibility Requirements**: Guidelines for information product compatibility with Coverage Claims Representation (CCR)

### Technical Papers
- **"The Evolution of the CWE Development and Research Views"**: Methodologies for constructing CWE views
- **"CWE Mapping Analysis"**: Examines effectiveness of CWE mappings to third-party weakness descriptions  
- **"Structured CWE Descriptions"**: Semi-formal descriptions using vulnerability theory terminology

### Additional Resources
- **Introductory Brochures**: Overview materials for new users
- **Vulnerability Trend Analyses**: Statistical analysis of weakness patterns
- **Presentations and Podcasts**: Educational materials and conference presentations
- **Historical Archive**: Legacy documents and earlier versions

## Data Sources

- **CWE Database**: https://cwe.mitre.org/data/downloads.html
- **XML Format**: https://cwe.mitre.org/data/xml/cwec_latest.xml.zip
- **JSON Format**: Available through various tools and APIs
- **CSV Exports**: Generated from XML data
- **Web Interface**: https://cwe.mitre.org/data/definitions/

## Markdown

Each edition directory holds a `markdown/` folder generated from MITRE's full XML for that edition, for people to read and for AI pipelines to ingest:

| Edition | Folder | Pages | Other files |
|---|---|---|---|
| 4.19.1 | [`4.19.1/markdown/`](4.19.1/markdown/index.md) | index, 969 weaknesses, 420 categories, 58 views | per-view CSV and JSON, merged `cwe-4.19.1-all.*` |
| 4.20 | [`4.20/markdown/`](4.20/markdown/index.md) | index, 969 weaknesses, 422 categories, 59 views | none (XML only) |
| 4.21 | [`4.21/markdown/`](4.21/markdown/index.md) | index, 984 weaknesses, 431 categories, 62 views | none (XML only) |
| 5.0 | [`5.0/markdown/`](5.0/markdown/index.md) | index, 984 weaknesses, 431 groupings, 62 views | per-view CSV and JSON, merged `cwe-5.0-all.*` |

MITRE's [release archive](https://cwe.mitre.org/data/archive.html) has no per-view CSV or JSON for past releases (it keeps each release's full XML zip, PDF, schema and difference reports), so 4.20 and 4.21 (the latter published the same day as 5.0, as the schema-7 release) have the generated markdown but no CSV, per-view JSON or merged files.

The merged `cwe-<v>-all.{csv,json}` (4.19.1 and 5.0, built from MITRE's three per-view CSVs by `scripts/merge_cwe_views.py`) keep 16 of the 23 columns in MITRE's per-view CSVs and leave out Weakness Ordinalities, Background Details, Alternate Terms, Exploitation Factors, Functional Areas, Affected Resources and Notes, which remain in the per-view CSVs; tracked in [#165](https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/issues/165).

- `index.md`: edition, release date, source zip and its SHA-256, licence and attribution, counts, and tables of every weakness, category or grouping, and view.
- `weaknesses/CWE-<id>.md`: one page per weakness, deprecated ones included. YAML front matter (`secid`, `cwe_id`, `entry_type`, `name`, `abstraction`, `structure`, `status`, `mapping_usage` when MITRE gives one, `cwe_version`, `cwe_release_date`, `upstream`), then MITRE's sections in schema order, the last being `Content History`. Each heading is MITRE's element name with spaces for underscores, so its GitHub anchor equals the SecID section subpath (`#potential-mitigations`, `#content-history`).
- `categories/` (4.x) or `groupings/` (5.0): MITRE's term for the edition. Each page lists its members and the view each membership belongs to. Front matter as for weaknesses, without `abstraction` and `structure`.
- `views/`: Graph views as a nested outline (each entry in full once, under its primary parent; other parents point to it), Explicit views as a list, Implicit views as their XPath filter plus the members it selects. Obsolete and deprecated views show their objective, status and content history only. Front matter as for categories, plus `view_type` (Graph, Explicit or Implicit).
- `Content History`, the last section of every weakness, category or grouping, and view page, directly above the footer: MITRE's submission, contribution and modification records as one table (event, date, name, organization, release, importance, comment; submissions first, then contributions, then modifications, each in MITRE's order), then the entry's previous names, each with the date MITRE stopped using it (and, where MITRE gives one, the CWE version). Names and organizations appear as MITRE publishes them.
- `index.md` front matter: `secid`, `entry_type: index`, `cwe_version`, `cwe_release_date`, `source` (the zip's URL) and `sha256`.
- `LICENSE.txt`: a copy of the edition's MITRE Terms of Use. Every page ends with MITRE's copyright and trademark notice and a link to the terms.

Regenerate or check a folder (needs `cwec_v<version>.xml.zip` in the edition directory: it is git-ignored, kept in S3 at the same path, and downloadable from `https://cwe.mitre.org/data/xml/`):

```bash
python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 5.0           # rewrite 5.0/markdown/
python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 5.0 --check   # exit 1 and list files if it differs
python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v
```

Tests that need an edition's zip skip when it is absent and say which zip to fetch; set `CWE_REQUIRE_ZIPS=1` to make them fail instead.

The script refuses to run if the zip's SHA-256 differs from its committed sidecar (`cwec_v<version>.xml.zip-file-metadata.json`), and it fails rather than dropping anything: on XML elements, attributes or markup it does not know, and on a second copy of an element that MITRE's schema allows only once. Every element the schema lets repeat is rendered in full. One exception to the first rule: in content history, submissions and the submitter and contributor names are rendered in full in every edition, because schema 8.0 lets them repeat; schema 7.x allows one of each, but a repeat in a 4.x edition is rendered rather than rejected (none occurs today). Output is byte-for-byte reproducible.

The data is reproduced as MITRE published it, upstream errors included. For example, in 4.21 and 5.0, CWE-1475's observed-example row labelled CVE-2025-50328 links to CVE-2026-58052, as it does in MITRE's XML and on MITRE's own page for CWE-1475 (the link target is CVE-2026-58052; the visible text is CVE-2025-50328).

People's names are kept as MITRE publishes them, in the content history and in the citations under References (Kurt, 2026-11-19: *"lets default to mirroring data faithfully, so that means leaving names in."*; see "Mirror faithfully" in the repository's AGENTS.md). The first build (2026-11-18) left content history out of the markdown as editorial history; that decision was superseded on 2026-11-19 ([#166](https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/issues/166)). MITRE's XML and the mirrored per-view JSON keep it too (Kurt, 2026-11-18: *"we treat mitre like the gov, we republish their data, it's fine."*).

What is left out:

- Relationships that MITRE's website derives in reverse (a weakness's children, and the categories and views that list it). The view and category/grouping pages hold them.
- For obsolete and deprecated views, everything except the objective, status and content history: their audience, members, filter, references, mapping notes and notes. Each such page names what it leaves out and links to MITRE's page. This is a known gap against the "Mirror faithfully" default, tracked in [#165](https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/issues/165).

## Adding a new CWE release

1. Download MITRE's `cwec_v<v>.xml.zip` (`https://cwe.mitre.org/data/xml/cwec_v<v>.xml.zip`) into a new edition directory `weakness/mitre.org/cwe/<v>/`.
2. Write its sidecar `cwec_v<v>.xml.zip-file-metadata.json` with the zip's `sha256`, `retrieved_from` and `retrieved_at` (copy the shape of another edition's sidecar).
3. Copy `LICENSE.txt` from the previous edition after confirming MITRE's [Terms of Use](https://cwe.mitre.org/about/termsofuse.html) have not changed; if they have, take the new text.
4. Write `cwe-<v>-metadata.json` from the previous edition's, with this edition's facts measured from its XML and `access_tier` with `tier_evidence`.
5. Set the previous edition's `lifecycle.supersededBy` to `<v>`.
6. Run `python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version <v>`, then the same with `--check`.
7. Add the edition's catalog counts to `EXPECTED` in `scripts/tests/cwe_test_editions.py`, then run the tests (`python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v`).
8. Upload the zip to S3: `tools-resources/utils/sync_originals_to_s3.sh --dry-run`, then without `--dry-run`.
9. Add the edition to the table under Markdown above.
10. Regenerate `INDEX.md`: `python3 tools-resources/utils/build_index.py`.

## Key CWE Views

- **CWE-1000**: Research Concepts in 4.19.1 and 4.20; Complete Weakness Hierarchy in 4.21 and 5.0
- **CWE-699**: Software Development View  
- **CWE-1194**: Hardware Design View
- **CWE-1350**: Weaknesses in the 2023 CWE Top 25

## Security Relevance

- **Cloud Security**: Identifies common weaknesses in cloud applications and infrastructure
- **AI Security**: Catalogs weaknesses specific to AI/ML systems and algorithms
- **Secure Development**: Foundation for secure coding practices and training
- **Vulnerability Assessment**: Links vulnerabilities (CVEs) to underlying weaknesses

## Relationship to Other MITRE Frameworks

- **CVE**: CVEs often reference the underlying CWE weakness types
- **CAPEC**: Attack patterns in CAPEC exploit weaknesses catalogued in CWE
- **OWASP Top 10**: Many OWASP categories map to specific CWE entries

## Processing Notes

CWE data includes:
- Weakness descriptions and examples
- Common consequences and likelihood
- Detection methods and mitigation strategies
- Relationships between different weakness types
- Mapping to other standards and frameworks