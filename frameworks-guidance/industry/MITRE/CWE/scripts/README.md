# CWE AI Relevance Analysis Tool

A Python library and CLI tool for analyzing CWE (Common Weakness Enumeration) entries to determine their relevance to AI security.

## Overview

This tool classifies every CWE entry using a **two-view model**:

| View | Question | Example |
|------|----------|---------|
| **View 1: Attacks ON AI** | Can this weakness attack/compromise AI systems? | Prompt injection, model poisoning |
| **View 2: Attacks VIA AI** | Can attackers trick AI into causing this weakness? | XSS, command injection |

See [CWE-AI-METHODOLOGY.md](../CWE-AI-METHODOLOGY.md) for the full methodology documentation.

## Installation

### From Source (Recommended for Development)

```bash
# Clone the repository and navigate to the scripts directory
cd frameworks-guidance/industry/MITRE/CWE/scripts

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Dependencies Only

```bash
# Install just the dependencies
pip install -r requirements.txt

# For development (testing, linting, etc.)
pip install -r requirements-dev.txt
```

## Quick Start

### Extract AI-Tagged CWEs

Extract CWEs that MITRE has already tagged as AI/ML relevant:

```bash
cwe-ai extract ../CWE-Research-Concepts-1000.csv --output ai-tagged.csv
```

### Keyword Search

Find CWEs containing AI-related keywords:

```bash
cwe-ai search ../CWE-Research-Concepts-1000.csv --keywords "prompt,injection,model" --output keyword-matches.csv
```

### Full Classification

Run the complete two-view classification on all CWEs:

```bash
cwe-ai classify --input-dir ../ --output results/CWE-AI-Analysis.csv
```

### Generate Report

Create a summary report with statistics:

```bash
cwe-ai report results/CWE-AI-Analysis.csv --format markdown --output results/report.md
```

## CLI Commands

### `cwe-ai extract`

Extract CWEs that have the AI/ML tag in their Applicable Platforms field.

```bash
cwe-ai extract INPUT_FILE [OPTIONS]

Options:
  --output, -o PATH     Output file path [default: ai-tagged.csv]
  --format, -f FORMAT   Output format: csv, json [default: csv]
  --verbose, -v         Enable verbose output
  --help                Show this message and exit
```

### `cwe-ai search`

Search CWEs for specific keywords in their descriptions.

```bash
cwe-ai search INPUT_FILE [OPTIONS]

Options:
  --keywords, -k TEXT   Comma-separated keywords to search
  --exclude, -e TEXT    Comma-separated keywords to exclude
  --output, -o PATH     Output file path
  --help                Show this message and exit
```

### `cwe-ai classify`

Run the full two-view classification on CWE entries.

```bash
cwe-ai classify [OPTIONS]

Options:
  --input-dir, -i PATH  Directory containing CWE CSV files
  --output, -o PATH     Output file path
  --checkpoint PATH     Checkpoint file for resuming interrupted runs
  --batch-size INT      Number of entries to process before checkpointing
  --help                Show this message and exit
```

### `cwe-ai report`

Generate summary statistics and reports.

```bash
cwe-ai report INPUT_FILE [OPTIONS]

Options:
  --format, -f FORMAT   Output format: markdown, json, html
  --output, -o PATH     Output file path
  --help                Show this message and exit
```

## Library Usage

The tool can also be used as a Python library:

```python
from cwe_ai_analysis import load_cwe_data, classify_cwe, CWEClassification

# Load CWE data from CSV
cwes = load_cwe_data("../CWE-Research-Concepts-1000.csv")

# Classify a single CWE
classification = classify_cwe(cwes[0])
print(f"CWE-{classification.cwe_id}: View1={classification.view1_score}, View2={classification.view2_score}")

# Access classification details
print(f"View 1 reasoning: {classification.view1_reasoning}")
print(f"View 2 reasoning: {classification.view2_reasoning}")
```

### Data Models

```python
from cwe_ai_analysis.models import CWEEntry, CWEClassification

# CWEEntry represents raw CWE data
entry = CWEEntry(
    cwe_id=1427,
    name="Improper Neutralization of Input Used for LLM Prompting",
    description="...",
    extended_description="...",
    applicable_platforms=["AI/ML"],
)

# CWEClassification represents the analysis result
classification = CWEClassification(
    cwe_id=1427,
    name="Improper Neutralization of Input Used for LLM Prompting",
    description="...",
    mitre_ai_tagged=True,
    view1_score=4,
    view1_reasoning="Canonical attack on LLMs - directly targets prompt processing",
    view2_score=3,
    view2_reasoning="Prompt injection often used to induce other attacks (command execution, data exfiltration)",
    ai_category="Prompt Injection",
    ai_impact="Full control over model output, potential code execution, data exfiltration",
)
```

## Configuration

Configuration can be set via environment variables or a `.env` file:

```bash
# .env file
CWE_AI_DATA_DIR=../           # Directory containing CWE CSV files
CWE_AI_OUTPUT_DIR=./output    # Default output directory
CWE_AI_LOG_LEVEL=INFO         # Logging level: DEBUG, INFO, WARNING, ERROR
```

Or via environment variables:

```bash
export CWE_AI_DATA_DIR=../
export CWE_AI_LOG_LEVEL=DEBUG
cwe-ai classify
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cwe_ai_analysis --cov-report=html

# Run specific test file
pytest tests/test_loaders.py -v
```

### Code Quality

```bash
# Format code
black cwe_ai_analysis tests
isort cwe_ai_analysis tests

# Type checking
mypy cwe_ai_analysis

# Linting
ruff check cwe_ai_analysis tests
```

### Project Structure

```
scripts/
├── README.md                 # This file
├── pyproject.toml            # Package configuration
├── requirements.txt          # Runtime dependencies
├── requirements-dev.txt      # Development dependencies
│
├── cwe_ai_analysis/          # Main library package
│   ├── __init__.py           # Package exports
│   ├── cli.py                # CLI entry point
│   ├── config.py             # Configuration management
│   ├── models.py             # Pydantic data models
│   ├── loaders.py            # CWE data loading
│   ├── extractors.py         # AI tag extraction, keyword search
│   ├── classifiers.py        # Two-view classification logic
│   ├── exporters.py          # Output formatting (CSV, JSON, Markdown)
│   └── utils.py              # Shared utilities
│
└── tests/                    # Unit tests
    ├── __init__.py
    ├── conftest.py           # Pytest fixtures
    ├── test_models.py
    ├── test_loaders.py
    ├── test_extractors.py
    └── test_classifiers.py
```

## Methodology

The classification uses a two-view model:

### View 1: Attacks ON AI (0-4 scale)

Measures whether a weakness can be used to attack AI systems:
- **4**: AI-specific (prompt injection, adversarial inputs)
- **3**: AI-critical (deserialization for model loading)
- **2**: AI-applicable (authentication issues in AI APIs)
- **1**: Weakly applicable (edge cases only)
- **0**: Not applicable

### View 2: Attacks VIA AI (0-4 scale)

Measures whether attackers would want AI to produce this weakness:
- **4**: Primary target (XSS, command injection - AI output IS the attack)
- **3**: Highly valuable (SQL injection, SSRF)
- **2**: Moderately useful (information disclosure)
- **1**: Indirect only (requires additional steps)
- **0**: Not applicable

See [CWE-AI-METHODOLOGY.md](../CWE-AI-METHODOLOGY.md) for complete documentation.

## Data Sources

The tool processes these CWE views:
- **CWE-1000** (Research Concepts): ~944 entries
- **CWE-699** (Software Development): ~399 entries
- **CWE-1194** (Hardware Design): ~110 entries

## License

MIT License - see repository root for details.

## Contributing

Contributions welcome! Please:
1. Follow the existing code style (enforced by black/ruff)
2. Add tests for new functionality
3. Update documentation as needed
4. Include contextual comments explaining WHY, not just WHAT
