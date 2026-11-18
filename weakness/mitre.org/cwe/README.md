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

| Edition | Folder | Pages |
|---|---|---|
| 4.19.1 | [`4.19.1/markdown/`](4.19.1/markdown/index.md) | index, 969 weaknesses, 420 categories, 58 views |
| 5.0 | [`5.0/markdown/`](5.0/markdown/index.md) | index, 984 weaknesses, 431 groupings, 62 views |

- `index.md`: edition, release date, source zip and its SHA-256, licence and attribution, counts, and tables of every weakness, category or grouping, and view.
- `weaknesses/CWE-<id>.md`: one page per weakness, deprecated ones included. YAML front matter (`secid`, `cwe_id`, `name`, `abstraction`, `structure`, `status`, `mapping_usage`, `cwe_version`, `upstream`), then MITRE's sections in schema order. Each heading is MITRE's element name with spaces for underscores, so its GitHub anchor equals the SecID section subpath (`#potential-mitigations`).
- `categories/` (4.x) or `groupings/` (5.0): MITRE's term for the edition. Each page lists its members and the view each membership belongs to.
- `views/`: Graph views as a nested outline (each entry in full once, under its primary parent; other parents point to it), Explicit views as a list, Implicit views as their XPath filter plus the members it selects. Obsolete and deprecated views show their objective and status only.
- `LICENSE.txt`: a copy of the edition's MITRE Terms of Use. Every page ends with MITRE's copyright and trademark notice and a link to the terms.

Regenerate or check a folder (needs `cwec_v<version>.xml.zip` in the edition directory: it is git-ignored, kept in S3 at the same path, and downloadable from `https://cwe.mitre.org/data/xml/`):

```bash
python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 5.0           # rewrite 5.0/markdown/
python3 weakness/mitre.org/cwe/scripts/cwe_to_markdown.py --version 5.0 --check   # exit 1 and list files if it differs
python3 -m unittest discover -s weakness/mitre.org/cwe/scripts/tests -v
```

The script refuses to run if the zip's SHA-256 differs from its committed sidecar (`cwec_v<version>.xml.zip-file-metadata.json`), and it fails rather than dropping anything: on XML elements, attributes or markup it does not know, and on a second copy of an element that MITRE's schema allows only once. Every element the schema lets repeat is rendered in full. Output is byte-for-byte reproducible.

What is left out:

- MITRE's content history (who submitted or modified each entry, and when), because CSA work does not write about specific people. Each page's footer says so.
- Relationships that MITRE's website derives in reverse (a weakness's children, and the categories and views that list it). The view and category/grouping pages hold them.

## Key CWE Views

- **CWE-1000**: Research Concepts View
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