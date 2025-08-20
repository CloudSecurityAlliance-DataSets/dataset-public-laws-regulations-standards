# MAEC (Malware Attribute Enumeration and Characterization)

MITRE's MAEC provides a standardized language for encoding and communicating detailed information about malware based upon attributes such as behaviors, artifacts, and attack patterns.

## Overview

MAEC is a community-developed structured language for encoding information about malware specimens and their behaviors. It enables correlation, integration, and automated analysis of malware information.

## Key Information

- **Maintainer**: MITRE Corporation
- **Purpose**: Standardized malware analysis and description
- **Current Version**: MAEC 5.0
- **Format**: JSON-based (MAEC 5.0), XML-based (legacy versions)
- **Status**: Evolved into STIX Malware objects in current implementations

## Key Concepts

### Malware Behaviors
- **Actions**: Specific activities performed by malware
- **Behaviors**: Collections of related actions
- **Capabilities**: High-level categorization of what malware can do

### Malware Attributes
- **Static Analysis**: File properties, strings, imports, etc.
- **Dynamic Analysis**: Runtime behaviors, network communications
- **Metadata**: Analysis context, tools used, timestamps

## Documentation and Resources

- **Main Site**: https://maecproject.github.io/ (archived)
- **MAEC Documentation**: https://maecproject.github.io/documentation/
- **GitHub Repository**: https://github.com/MAECProject/MAEC (archived)
- **Legacy MITRE Site**: https://maec.mitre.org/ (historical)

## Data Sources

- **Historical Downloads**: https://maecproject.github.io/releases/
- **Current Implementation**: Integrated into STIX 2.x Malware objects
- **XML Schemas**: Available for legacy MAEC 5.0 implementations
- **Migration Guide**: MAEC to STIX conversion documentation

## Security Relevance

- **Cloud Security**: Analysis of cloud-targeting malware and behaviors
- **AI Security**: Understanding of AI-specific malware and attack vectors
- **Incident Response**: Structured malware analysis for incident investigation
- **Threat Intelligence**: Malware family classification and behavior mapping

## Evolution to STIX

MAEC has largely been superseded by STIX Malware objects:
- **STIX Malware**: Incorporates MAEC behavior concepts
- **STIX Observed Data**: Captures malware artifacts
- **STIX Relationships**: Links malware to indicators and TTPs

## Processing Notes

For historical MAEC data:
- XML schema validation required for older versions
- JSON format available for MAEC 5.0
- Migration paths available to STIX format
- Legacy tooling may still use MAEC formats

Modern implementations should use STIX Malware objects instead of standalone MAEC.