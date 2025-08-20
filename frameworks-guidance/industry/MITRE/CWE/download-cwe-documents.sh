#!/bin/bash

# Download and process CWE documents
# This script downloads important CWE documentation and converts them to clean markdown

set -euo pipefail

# Configuration
BASE_URL="https://cwe.mitre.org"
TARGET_DIR="/Users/kurt/GitHub/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/frameworks-guidance/industry/MITRE/CWE/cwe-documents"
TEMP_DIR="$TARGET_DIR/temp"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

# Check dependencies
check_dependencies() {
    local missing_deps=()
    
    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi
    
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi
    
    if ! command -v pandoc &> /dev/null; then
        warn "pandoc not found - will use alternative conversion methods"
    fi
    
    # Check for marker (PDF to markdown converter)
    if ! command -v marker_single &> /dev/null; then
        warn "marker not found - will use alternative PDF conversion"
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        error "Missing required dependencies: ${missing_deps[*]}"
        echo "Install missing dependencies and run again."
        exit 1
    fi
}

# Create directories
setup_directories() {
    log "Setting up directories..."
    mkdir -p "$TARGET_DIR"
    mkdir -p "$TEMP_DIR"
    mkdir -p "$TARGET_DIR/pdfs"
    mkdir -p "$TARGET_DIR/markdown"
    mkdir -p "$TARGET_DIR/data"
    mkdir -p "$TARGET_DIR/html"
}

# Download a file with error handling
download_file() {
    local url="$1"
    local output_path="$2"
    local description="$3"
    
    log "Downloading $description..."
    if curl -L --fail --silent --show-error --max-time 300 "$url" -o "$output_path"; then
        log "✓ Downloaded: $description"
        return 0
    else
        error "✗ Failed to download: $description"
        return 1
    fi
}

# Download important PDF documents
download_pdf_documents() {
    log "Downloading PDF documents..."
    
    declare -A pdf_docs=(
        ["/documents/mapping_analysis/cwe_mapping_analysis.pdf"]="CWE Mapping Analysis"
        ["/documents/structured_descriptions/Structured_Descriptions.pdf"]="Structured CWE Descriptions" 
        ["/documents/advances_in_information_assuarance_standards.pdf"]="Advances in Information Assurance Standards"
        ["/documents/vulnerability_theory/CWE-Introduction_to_Vulnerability_Theory.pdf"]="Introduction to Vulnerability Theory"
        ["/documents/unforgivable_vulns/unforgivable.pdf"]="Unforgivable Vulnerabilities"
        ["/documents/vuln-trends/vuln-trends.pdf"]="Vulnerability Trends"
        ["/documents/being-explicit/BlackHat_BeingExplicit_WP.pdf"]="Being Explicit White Paper"
        ["/documents/cwe_update.pdf"]="CWE Update"
        ["/documents/case_for_cwes.pdf"]="The Case for CWEs"
        ["/data/published/cwe_latest.pdf"]="CWE Complete Reference (Latest)"
    )
    
    # Special URLs not relative to BASE_URL
    declare -A external_pdfs=(
        ["http://makingsecuritymeasurable.mitre.org/docs/cwe-intro-handout.pdf"]="CWE Introduction Handout"
        ["http://makingsecuritymeasurable.mitre.org/docs/cwss-cwraf-intro-handout.pdf"]="CWSS/CWRAF Introduction Handout"
    )
    
    # Download relative PDFs
    for path in "${!pdf_docs[@]}"; do
        local filename=$(basename "$path")
        local safe_filename="${filename// /_}"
        download_file "$BASE_URL$path" "$TARGET_DIR/pdfs/$safe_filename" "${pdf_docs[$path]}"
    done
    
    # Download external PDFs
    for url in "${!external_pdfs[@]}"; do
        local filename=$(basename "$url")
        local safe_filename="${filename// /_}"
        download_file "$url" "$TARGET_DIR/pdfs/$safe_filename" "${external_pdfs[$url]}"
    done
}

# Download HTML documents
download_html_documents() {
    log "Downloading HTML documents..."
    
    declare -A html_docs=(
        ["/documents/schema/"]="CWE Schema Documentation"
        ["/documents/cwe_usage/guidance.html"]="CWE Usage Guidance"
    )
    
    for path in "${!html_docs[@]}"; do
        local filename=$(basename "$path")
        if [[ "$filename" == "" ]]; then
            filename="index.html"
        fi
        local safe_filename="${filename// /_}"
        download_file "$BASE_URL$path" "$TARGET_DIR/html/$safe_filename" "${html_docs[$path]}" || true
    done
}

# Download key data files
download_data_files() {
    log "Downloading data files..."
    
    declare -A data_files=(
        ["/data/xml/cwec_latest.xml.zip"]="Latest CWE XML Data"
        ["/data/xsd/cwe_schema_latest.xsd"]="CWE XML Schema"
    )
    
    for path in "${!data_files[@]}"; do
        local filename=$(basename "$path")
        download_file "$BASE_URL$path" "$TARGET_DIR/data/$filename" "${data_files[$path]}"
    done
    
    # Extract XML if zip was downloaded successfully
    if [[ -f "$TARGET_DIR/data/cwec_latest.xml.zip" ]]; then
        log "Extracting CWE XML data..."
        cd "$TARGET_DIR/data"
        unzip -o cwec_latest.xml.zip
        cd - > /dev/null
    fi
}

# Convert PDF to Markdown using available tools
convert_pdf_to_markdown() {
    local pdf_file="$1"
    local output_file="$2"
    local basename_file=$(basename "$pdf_file" .pdf)
    
    log "Converting $basename_file to markdown..."
    
    # Try marker first (best quality)
    if command -v marker_single &> /dev/null; then
        if marker_single "$pdf_file" --output_format markdown --output_dir "$TEMP_DIR"; then
            local marker_output="$TEMP_DIR/$(basename "$pdf_file" .pdf).md"
            if [[ -f "$marker_output" ]]; then
                mv "$marker_output" "$output_file"
                log "✓ Converted using marker: $basename_file"
                return 0
            fi
        fi
    fi
    
    # Fallback to pandoc if available
    if command -v pandoc &> /dev/null; then
        if pandoc "$pdf_file" -t markdown -o "$output_file" 2>/dev/null; then
            log "✓ Converted using pandoc: $basename_file"
            return 0
        fi
    fi
    
    # Last resort: create placeholder file
    warn "Could not convert $basename_file - creating placeholder"
    cat > "$output_file" << EOF
# $(basename "$pdf_file" .pdf | tr '_' ' ')

**Note**: This document could not be automatically converted to markdown.

**Source**: $pdf_file

**Conversion**: Manual conversion required

Please refer to the original PDF document for content.
EOF
    return 1
}

# Convert HTML to Markdown
convert_html_to_markdown() {
    local html_file="$1"
    local output_file="$2"
    local basename_file=$(basename "$html_file" .html)
    
    log "Converting $basename_file to markdown..."
    
    # Try pandoc first
    if command -v pandoc &> /dev/null; then
        if pandoc "$html_file" -f html -t markdown -o "$output_file" 2>/dev/null; then
            log "✓ Converted using pandoc: $basename_file"
            return 0
        fi
    fi
    
    # Fallback: Python-based conversion
    python3 -c "
import sys
import re
from pathlib import Path

def html_to_markdown(html_content):
    # Basic HTML to Markdown conversion
    # Remove HTML tags but preserve content
    content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up whitespace
    lines = [line.strip() for line in content.split('\n')]
    content = '\n'.join(line for line in lines if line)
    
    return content

try:
    with open('$html_file', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    markdown_content = html_to_markdown(html_content)
    
    with open('$output_file', 'w', encoding='utf-8') as f:
        f.write(f'# {Path(\"$html_file\").stem.replace(\"_\", \" \").title()}\n\n')
        f.write(markdown_content)
    
    print('✓ Converted using Python: $basename_file')
except Exception as e:
    print(f'✗ Failed to convert: $basename_file - {e}', file=sys.stderr)
    sys.exit(1)
" && log "✓ Converted using Python: $basename_file"
}

# Process all downloaded documents
process_documents() {
    log "Processing documents to markdown..."
    
    # Process PDFs
    if [[ -d "$TARGET_DIR/pdfs" ]] && [[ "$(ls -A "$TARGET_DIR/pdfs")" ]]; then
        for pdf_file in "$TARGET_DIR/pdfs"/*.pdf; do
            if [[ -f "$pdf_file" ]]; then
                local basename_file=$(basename "$pdf_file" .pdf)
                local markdown_file="$TARGET_DIR/markdown/$basename_file.md"
                convert_pdf_to_markdown "$pdf_file" "$markdown_file"
            fi
        done
    fi
    
    # Process HTML files
    if [[ -d "$TARGET_DIR/html" ]] && [[ "$(ls -A "$TARGET_DIR/html" 2>/dev/null)" ]]; then
        for html_file in "$TARGET_DIR/html"/*.html; do
            if [[ -f "$html_file" ]]; then
                local basename_file=$(basename "$html_file" .html)
                local markdown_file="$TARGET_DIR/markdown/$basename_file.md"
                convert_html_to_markdown "$html_file" "$markdown_file"
            fi
        done
    fi
}

# Clean up temporary files
cleanup() {
    log "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
}

# Create index file
create_index() {
    log "Creating index of downloaded documents..."
    
    cat > "$TARGET_DIR/README.md" << EOF
# CWE Documents Collection

This directory contains important CWE (Common Weakness Enumeration) documentation converted to markdown format.

Generated on: $(date)

## Contents

### PDF Documents (converted to Markdown)
EOF

    if [[ -d "$TARGET_DIR/markdown" ]] && [[ "$(ls -A "$TARGET_DIR/markdown" 2>/dev/null)" ]]; then
        for md_file in "$TARGET_DIR/markdown"/*.md; do
            if [[ -f "$md_file" ]]; then
                local basename_file=$(basename "$md_file" .md)
                local title="${basename_file//_/ }"
                echo "- [$title](./markdown/$(basename "$md_file"))" >> "$TARGET_DIR/README.md"
            fi
        done
    fi

    cat >> "$TARGET_DIR/README.md" << EOF

### Data Files
EOF

    if [[ -d "$TARGET_DIR/data" ]] && [[ "$(ls -A "$TARGET_DIR/data" 2>/dev/null)" ]]; then
        for data_file in "$TARGET_DIR/data"/*; do
            if [[ -f "$data_file" ]]; then
                local basename_file=$(basename "$data_file")
                echo "- [$basename_file](./data/$basename_file)" >> "$TARGET_DIR/README.md"
            fi
        done
    fi

    cat >> "$TARGET_DIR/README.md" << EOF

### Original Files
- **PDFs**: [./pdfs/](./pdfs/) - Original PDF documents
- **HTML**: [./html/](./html/) - Original HTML documents

## Usage

The markdown files in the \`./markdown/\` directory contain the converted content from the original documents. These are optimized for reading and searching within the repository.

For the most accurate information, refer to the original documents at https://cwe.mitre.org/about/documents.html

## Processing Notes

- PDF conversion performed using available tools (marker, pandoc, or fallback methods)
- HTML conversion performed using pandoc or Python fallback
- Some complex formatting may not be perfectly preserved
- Images and diagrams may not be included in markdown versions

EOF
}

# Main execution
main() {
    log "Starting CWE document download and processing..."
    
    check_dependencies
    setup_directories
    
    download_pdf_documents
    download_html_documents
    download_data_files
    
    process_documents
    create_index
    cleanup
    
    log "✓ CWE document processing completed successfully!"
    log "Documents available in: $TARGET_DIR"
}

# Handle script interruption
trap 'error "Script interrupted"; cleanup; exit 1' INT TERM

# Run main function
main "$@"