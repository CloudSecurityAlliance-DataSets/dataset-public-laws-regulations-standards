# OSV (Open Source Vulnerability Database)

OSV is a vulnerability database and triage infrastructure for open source projects aimed at helping both open source maintainers and consumers of open source.

## Overview

OSV provides a distributed vulnerability database that aggregates vulnerability data from multiple sources and provides a unified API for querying vulnerabilities across different ecosystems. It focuses specifically on open source software vulnerabilities.

## Key Information

- **Maintainer**: Google (with open source community contributions)
- **Purpose**: Unified vulnerability database for open source software
- **Format**: OSV Schema (JSON-based standard)
- **Scope**: Open source packages across multiple ecosystems (npm, PyPI, Go, Rust, etc.)
- **Status**: Active development and widely adopted

## Documentation and Resources

- **Main Site**: https://osv.dev/
- **OSV Schema Specification**: https://ossf.github.io/osv-schema/
- **API Documentation**: https://osv.dev/docs/
- **GitHub Repository**: https://github.com/google/osv
- **Schema Repository**: https://github.com/ossf/osv-schema

## Data Sources

- **OSV API**: https://api.osv.dev/
- **Bulk Downloads**: https://osv-vulnerabilities.storage.googleapis.com/
- **Per-ecosystem Data**: Available for npm, PyPI, Go, Rust, Debian, Alpine, Android, etc.
- **Real-time Updates**: Continuous synchronization with upstream sources
- **Query Interface**: https://osv.dev/list

## Key Features

### Multi-Ecosystem Support
- **JavaScript/Node.js**: npm packages
- **Python**: PyPI packages  
- **Go**: Go modules
- **Rust**: Crates.io packages
- **Linux Distributions**: Debian, Alpine, Ubuntu
- **Android**: Android Open Source Project
- **Other**: Maven, NuGet, RubyGems, and more

### OSV Schema
- **Standardized Format**: Common schema for vulnerability data
- **Rich Metadata**: Affected versions, severity, references
- **Ecosystem-Specific**: Tailored fields for different package managers
- **Machine-Readable**: JSON format optimized for automation

## Security Relevance

- **Cloud Security**: Critical for identifying vulnerabilities in cloud-native applications and dependencies
- **AI Security**: Covers vulnerabilities in AI/ML libraries and frameworks (TensorFlow, PyTorch, etc.)
- **Supply Chain**: Comprehensive dependency vulnerability tracking
- **DevSecOps**: Integration with CI/CD pipelines for automated vulnerability scanning

## Integration with Other Systems

- **GitHub Advisory Database**: Compatible format and data sharing
- **CVE**: Links to CVE identifiers where available
- **GHSA**: GitHub Security Advisory integration
- **Dependabot**: Powers GitHub's dependency scanning
- **Google Cloud**: Integrated into Google Cloud security tools

## API Usage

### Basic Query Examples
```bash
# Query by package
curl "https://api.osv.dev/v1/query" -d '{"package":{"name":"requests","ecosystem":"PyPI"}}'

# Query by commit
curl "https://api.osv.dev/v1/query" -d '{"commit":"6879efc2c1596d11a6a6ad296f80063b558d5e0f"}'

# Get vulnerability by ID
curl "https://api.osv.dev/v1/vulns/GHSA-j8r2-6x86-q33q"
```

### Rate Limits
- No authentication required for basic usage
- Reasonable rate limits for automated tools
- Bulk download options for large-scale processing

## Processing Notes

OSV data characteristics:
- **Real-time Updates**: Continuously updated as new vulnerabilities are disclosed
- **Structured Data**: Consistent JSON schema across all ecosystems  
- **Version Ranges**: Precise affected version specifications
- **Rich Context**: Links to patches, advisories, and documentation
- **Automated Ingestion**: Can be automated for security tooling integration

## Ecosystem Coverage

Major ecosystems supported:
- **npm** (JavaScript/Node.js packages)
- **PyPI** (Python packages)
- **Go** (Go modules)
- **Packagist** (PHP/Composer packages)
- **Maven** (Java packages)
- **NuGet** (C#/.NET packages)
- **RubyGems** (Ruby packages)
- **crates.io** (Rust packages)
- **Debian** (Debian packages)
- **Alpine** (Alpine Linux packages)
- **Android** (AOSP components)