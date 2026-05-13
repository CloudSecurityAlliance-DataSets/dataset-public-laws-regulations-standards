# GitHub Advisory Database

GitHub's Advisory Database is a comprehensive collection of security vulnerabilities affecting open source software, curated by GitHub and the security community.

## Overview

The GitHub Advisory Database aggregates security advisories from multiple sources including the National Vulnerability Database (NVD), GitHub Security Advisories, and community contributions. It provides comprehensive vulnerability information with a focus on actionable remediation guidance.

## Key Information

- **Maintainer**: GitHub (Microsoft)
- **Purpose**: Curated vulnerability database for open source software
- **Format**: GitHub Security Advisory (GHSA) format, compatible with OSV Schema
- **Scope**: Open source packages across all major ecosystems
- **Status**: Actively maintained with community contributions

## Documentation and Resources

- **Main Site**: https://github.com/advisories
- **GitHub Advisory Database**: https://github.com/github/advisory-database
- **API Documentation**: https://docs.github.com/en/rest/security-advisories
- **GraphQL API**: https://docs.github.com/en/graphql/reference/objects#securityadvisory
- **Advisory Guidelines**: https://docs.github.com/en/code-security/security-advisories

## Data Sources

- **GitHub API**: https://api.github.com/advisories
- **GraphQL API**: https://api.github.com/graphql (SecurityAdvisory objects)
- **Bulk Repository**: https://github.com/github/advisory-database
- **JSON Downloads**: Available through repository releases
- **Real-time Access**: Through GitHub's REST and GraphQL APIs

## Key Features

### Comprehensive Coverage
- **CVE Integration**: All CVE entries included with enhanced metadata
- **GHSA Entries**: GitHub-specific security advisories
- **Community Reviewed**: Community-contributed vulnerability assessments
- **Malware Advisories**: Information about malicious packages

### Enhanced Metadata
- **Severity Scoring**: CVSS scores and severity levels
- **Affected Versions**: Precise version range specifications
- **Patch Information**: Links to fixes and workarounds
- **Ecosystem Context**: Package manager specific details

## Security Relevance

- **Cloud Security**: Identifies vulnerabilities in cloud-native and infrastructure packages
- **AI Security**: Covers vulnerabilities in ML/AI libraries and dependencies
- **Supply Chain**: Comprehensive dependency vulnerability tracking with remediation guidance
- **DevSecOps**: Powers Dependabot and GitHub's security features

## Ecosystem Coverage

Supported package ecosystems:
- **npm** (JavaScript/Node.js)
- **pip** (Python/PyPI)
- **Composer** (PHP)
- **Maven** (Java)
- **NuGet** (C#/.NET)
- **RubyGems** (Ruby)
- **Go** (Go modules)
- **Cargo** (Rust)
- **Swift** (Swift Package Manager)
- **Actions** (GitHub Actions)

## Integration with Other Systems

### OSV Compatibility
- **OSV Schema**: GitHub advisories are available in OSV format
- **Data Sharing**: Contributes to and consumes from OSV ecosystem
- **Format Alignment**: Compatible JSON schema structure

### GitHub Ecosystem
- **Dependabot**: Powers automated dependency updates
- **Code Scanning**: Integration with security scanning tools
- **Security Advisories**: Repository-specific advisory creation
- **Security Tab**: Vulnerability alerts in repositories

## API Usage

### REST API Examples
```bash
# List all advisories
curl "https://api.github.com/advisories"

# Get specific advisory
curl "https://api.github.com/advisories/GHSA-j8r2-6x86-q33q"

# Search advisories by ecosystem
curl "https://api.github.com/advisories?ecosystem=npm"

# Filter by severity
curl "https://api.github.com/advisories?severity=high"
```

### GraphQL Query Example
```graphql
query {
  securityAdvisories(first: 10) {
    nodes {
      ghsaId
      summary
      severity
      publishedAt
      vulnerabilities(first: 5) {
        nodes {
          package {
            name
            ecosystem
          }
          vulnerableVersionRange
          firstPatchedVersion {
            identifier
          }
        }
      }
    }
  }
}
```

## Processing Notes

GitHub Advisory Database characteristics:
- **Curated Content**: Human-reviewed and enhanced beyond automated feeds
- **Community Contributions**: Accept community-submitted advisories
- **Rich Linking**: Extensive cross-references to patches, documentation, and discussions
- **Historical Data**: Comprehensive historical vulnerability records
- **Machine-Readable**: Structured data optimized for automated tooling

## Advisory Types

### GitHub Security Advisories (GHSA)
- **Repository-specific**: Created by project maintainers
- **Coordinated Disclosure**: Support for responsible disclosure workflows
- **CVE Assignment**: Can receive CVE identifiers through GitHub

### Reviewed Advisories
- **Community Verified**: Community-reviewed and enhanced entries
- **Additional Context**: Extra metadata and remediation guidance
- **Quality Assurance**: Higher confidence through human review

### Malware Advisories
- **Package Identification**: Malicious packages in public registries
- **Threat Intelligence**: Information about package-based attacks
- **Removal Tracking**: Documentation of package removals and mitigations

## Rate Limits and Access

- **Public API**: Rate-limited access for public repositories
- **Authenticated**: Higher rate limits with GitHub authentication
- **Enterprise**: Enhanced access for GitHub Enterprise customers
- **Bulk Access**: Repository cloning for large-scale processing