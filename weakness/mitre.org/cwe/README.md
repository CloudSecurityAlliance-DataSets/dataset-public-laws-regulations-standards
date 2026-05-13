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