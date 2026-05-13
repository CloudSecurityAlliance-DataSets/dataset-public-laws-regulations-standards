# AIUC-1 Data Extraction Tool

This tool extracts structured data from the AIUC-1 (AI Use Cases) standard website files and converts them into a CSV spreadsheet format for analysis and compliance planning.

## Overview

The AIUC-1 standard contains 51 AI governance requirements across 6 categories:
- **A. Data & Privacy** (7 requirements)
- **B. Security** (9 requirements) 
- **C. Safety** (12 requirements)
- **D. Reliability** (4 requirements)
- **E. Accountability** (17 requirements)
- **F. Society** (2 requirements)

This extraction tool parses the HTML files and extracts key metadata and implementation guidance for each requirement.

## Prerequisites

- Python 3.6+
- Required Python packages:
  ```bash
  pip install beautifulsoup4
  ```

## Usage

1. Ensure you have the AIUC-1 website files in the current directory structure:
   ```
   ./
   ├── aiuc-1.com/
   │   ├── security/
   │   ├── data-and-privacy/
   │   ├── safety/
   │   ├── reliability/
   │   ├── accountability/
   │   └── society/
   └── extract_to_csv.py
   ```

   This structure matches what you get when using wget to mirror the site:
   ```bash
   wget -m https://aiuc-1.com/
   ```

2. Run the extraction script:
   ```bash
   python3 extract_to_csv.py
   ```

3. The script will process all 51 requirement files and generate `aiuc-1-standard-data.csv`

## Output Format

The generated CSV contains the following columns:

| Column | Description |
|--------|-------------|
| **title** | Full page title including requirement ID |
| **section** | Main category (Security, Data & Privacy, etc.) |
| **heading** | Requirement name |
| **description** | Brief requirement summary |
| **keywords** | Relevant tags (semicolon-separated) |
| **application** | Whether requirement is Mandatory or Optional |
| **frequency** | Review frequency (Every 3/6/12 months) |
| **type** | Control type (Preventative, Detective, Corrective) |
| **crosswalks** | Framework mappings (NIST AI RMF, OWASP Top 10, EU AI Act, etc.) |
| **control_activities** | Complete implementation guidance including "Should include" and "May include" sections |
| **url_path** | Full URL to the original requirement page |

## Example Output

```csv
title,section,heading,description,keywords,application,frequency,type,crosswalks,control_activities,url_path
"B001. Test adversarial robustness | AIUC-1","Security","Test adversarial robustness","Implement adversarial testing program to validate system resilience","Adversarial Testing; Red Teaming","Mandatory","Every 3 months","Preventative","MITRE ATLAS; ISO 42001; NIST AI RMF","Should include Establishing a taxonomy for adversarial risks...","https://aiuc-1.com/security/test-adversarial-robustness"
```

## Key Features

- **Complete Control Activities**: Extracts full implementation guidance between "Should include" and "Organizations can submit alternative evidence"
- **Preserved Formatting**: Maintains line breaks and structure in control activities for better readability
- **Structured Metadata**: Parses all requirement metadata including keywords, frequency, and framework crosswalks
- **Full URLs**: Provides complete links back to original requirement pages
- **Clean Data**: Handles HTML parsing and produces clean, structured CSV output

## File Processing

The script processes files from these directories:
- `./aiuc-1.com/security/` - 9 security requirements
- `./aiuc-1.com/data-and-privacy/` - 7 data & privacy requirements  
- `./aiuc-1.com/safety/` - 12 safety requirements
- `./aiuc-1.com/reliability/` - 4 reliability requirements
- `./aiuc-1.com/accountability/` - 17 accountability requirements
- `./aiuc-1.com/society/` - 2 societal impact requirements

## Error Handling

- Files that cannot be processed will show error messages but won't stop the overall extraction
- The script provides progress updates as it processes each file
- Final count shows total number of successfully processed records

## Use Cases

This extracted data can be used for:
- **Compliance Mapping**: Cross-reference requirements with existing frameworks
- **Gap Analysis**: Identify missing controls in your AI systems
- **Implementation Planning**: Use detailed control activities for implementation guidance
- **Risk Assessment**: Analyze requirements by type, frequency, and criticality
- **Audit Preparation**: Create evidence collection plans based on control activities

## Generated Files

After running the script, you will have:
- `aiuc-1-standard-data.csv` - The main output file with all extracted data
- `extract_to_csv.py` - The extraction script
- `README.md` - This documentation file

## Support

The original AIUC-1 standard is available at: https://aiuc-1.com/

For issues with this extraction tool, check that:
1. All required HTML files are present in the correct directory structure
2. BeautifulSoup4 is properly installed (`pip install beautifulsoup4`)
3. Python 3.6+ is being used
4. The `aiuc-1.com/` directory contains the mirrored website files

## Version

This extraction tool is designed to work with the AIUC-1 standard as of 2024. If the website structure changes, the script may need updates to maintain compatibility.