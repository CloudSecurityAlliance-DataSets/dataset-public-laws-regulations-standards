# CWE Document Download and Processing

This directory contains scripts to download and process CWE (Common Weakness Enumeration) documentation.

## Quick Start

To download and process all CWE documents:

```bash
cd /Users/kurt/GitHub/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/frameworks-guidance/industry/MITRE/CWE
./download-cwe-documents.sh
```

## What Gets Downloaded

### PDF Documents
- **CWE Mapping Analysis** - Analysis of CWE mappings to third-party descriptions
- **Structured CWE Descriptions** - Semi-formal descriptions using vulnerability theory
- **Introduction to Vulnerability Theory** - Theoretical foundation for CWE
- **Vulnerability Trends** - Statistical analysis of weakness patterns
- **Being Explicit White Paper** - BlackHat presentation materials
- **CWE Complete Reference** - Latest full CWE documentation
- **Introduction Handouts** - Overview materials for new users

### Data Files
- **Latest CWE XML** - Complete CWE database in XML format
- **CWE XML Schema** - Schema definition for CWE XML data

### HTML Documents
- **Schema Documentation** - CWE data structure documentation
- **Usage Guidance** - Guidelines for using CWE effectively

## Output Structure

After running the script, documents will be organized as:

```
cwe-documents/
├── README.md                 # Index of all downloaded documents
├── pdfs/                     # Original PDF files
├── markdown/                 # Converted markdown files
├── html/                     # Original HTML files  
├── data/                     # XML data and schema files
└── temp/                     # Temporary processing files (cleaned up)
```

## Dependencies

### Required
- `curl` - For downloading files
- `python3` - For HTML to Markdown conversion

### Optional (improves conversion quality)
- `pandoc` - Better HTML/PDF to Markdown conversion
- `marker` - High-quality PDF to Markdown conversion (https://github.com/VikParuchuri/marker)

### Installing Dependencies

**macOS:**
```bash
# Install pandoc
brew install pandoc

# Install marker (optional, for best PDF conversion)
pip install marker-pdf
```

**Ubuntu/Debian:**
```bash
# Install pandoc
sudo apt-get install pandoc

# Install marker (optional)
pip install marker-pdf
```

## Manual Usage

### Download Script Only
```bash
./download-cwe-documents.sh
```

### Convert Single HTML File
```bash
python3 html_to_markdown.py input.html output.md --title "Document Title"
```

### Convert with Base URL (for fixing relative links)
```bash
python3 html_to_markdown.py input.html output.md --base-url "https://cwe.mitre.org/"
```

## Script Features

- **Robust downloading** with error handling and retries
- **Multiple conversion methods** - tries best available tools first
- **Automatic cleanup** of temporary files
- **Comprehensive logging** with colored output
- **Index generation** - creates README with links to all documents
- **Dependency checking** - verifies required tools are available

## Troubleshooting

### Download Failures
- Check internet connection
- Some documents may be temporarily unavailable
- Script will continue with other documents if one fails

### Conversion Issues
- Install `pandoc` for better conversion quality
- Install `marker` for best PDF conversion results
- Some complex formatting may not convert perfectly
- Original files are preserved for reference

### Permission Errors
- Ensure the script is executable: `chmod +x download-cwe-documents.sh`
- Check write permissions to target directory
- Run with appropriate user permissions

## Customization

To modify what documents are downloaded, edit the arrays in `download-cwe-documents.sh`:

- `pdf_docs` - PDF documents to download
- `external_pdfs` - External PDF URLs
- `html_docs` - HTML documents to download  
- `data_files` - Data files to download

## Output Quality

The conversion process prioritizes:
1. **marker** - Highest quality PDF conversion with OCR and formatting preservation
2. **pandoc** - Good quality HTML/PDF conversion
3. **Python fallback** - Basic conversion that preserves content structure

All original files are preserved, so you can always reference the source documents for complete accuracy.