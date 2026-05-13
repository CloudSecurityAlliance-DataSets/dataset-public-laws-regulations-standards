# CPE (Common Platform Enumeration)

MITRE's CPE provides a standardized method for describing and identifying classes of applications, operating systems, and hardware devices.

## Overview

CPE is a structured naming scheme for information technology systems, software, and packages. It enables organizations to have a common language for identifying IT assets and their associated vulnerabilities.

## Key Information

- **Maintainer**: MITRE Corporation (in collaboration with NIST)
- **Purpose**: Standardized IT asset identification and naming
- **Format**: cpe:2.3:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other
- **Scope**: Operating systems, applications, hardware devices

## Documentation and Resources

- **Main MITRE Site**: https://cpe.mitre.org/
- **NIST CPE Program**: https://nvd.nist.gov/products/cpe
- **CPE Specification**: https://cpe.mitre.org/specification/
- **User Guide**: https://cpe.mitre.org/files/cpe-specification_2.3.pdf

## Data Sources

- **MITRE CPE Dictionary**: https://cpe.mitre.org/data/
- **NIST NVD CPE Data**: https://nvd.nist.gov/products/cpe
- **Dictionary Downloads**: https://cpe.mitre.org/data/
- **Search Interface**: https://cpe.mitre.org/cgi-bin/cpename.cgi
- **CPE Matching**: https://nvd.nist.gov/products/cpe/search

## Security Relevance

- **Cloud Security**: Essential for asset inventory and vulnerability management in cloud environments
- **AI Security**: Helps identify and categorize AI/ML tools and frameworks
- **Compliance**: Required for many security frameworks and compliance standards

## Processing Notes

CPE data is available in multiple formats:
- XML dictionary format
- JSON format (newer versions)
- CSV exports
- API access through NIST NVD

CPE identifiers are used extensively in vulnerability databases to specify affected products.