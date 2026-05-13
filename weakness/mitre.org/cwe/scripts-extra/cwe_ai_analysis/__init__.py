"""
CWE AI Relevance Analysis Library

This library provides tools for analyzing CWE (Common Weakness Enumeration) entries
to determine their relevance to AI security using a two-view classification model.

Two-View Model:
    - View 1 (Attacks ON AI): Can this weakness attack/compromise AI systems?
    - View 2 (Attacks VIA AI): Can attackers trick AI into causing this weakness?

Why Two Views:
    We initially considered a single relevance score, but realized this conflated
    two distinct questions. A weakness like XSS scores low for attacking AI (View 1)
    but high for AI-generated attacks (View 2). The two-view model captures this
    nuance and provides more actionable insights.

Example Usage:
    >>> from cwe_ai_analysis import load_cwe_data, classify_cwe
    >>> cwes = load_cwe_data("CWE-Research-Concepts-1000.csv")
    >>> result = classify_cwe(cwes[0])
    >>> print(f"View 1: {result.view1_score}, View 2: {result.view2_score}")

See CWE-AI-METHODOLOGY.md for complete methodology documentation.
"""

from cwe_ai_analysis.models import (
    CWEEntry,
    CWEClassification,
    AICategory,
    ViewScore,
)
from cwe_ai_analysis.loaders import (
    load_cwe_data,
    load_cwe_from_csv,
    load_cwe_from_json,
)
from cwe_ai_analysis.extractors import (
    extract_ai_tagged,
    search_keywords,
)
from cwe_ai_analysis.classifiers import (
    classify_cwe,
    classify_all,
)
from cwe_ai_analysis.exporters import (
    export_to_csv,
    export_to_json,
    generate_report,
)
from cwe_ai_analysis.config import Config, get_config

__version__ = "1.0.0"
__author__ = "Cloud Security Alliance"

# Public API - these are the main entry points for library users
__all__ = [
    # Version info
    "__version__",
    # Data models
    "CWEEntry",
    "CWEClassification",
    "AICategory",
    "ViewScore",
    # Data loading
    "load_cwe_data",
    "load_cwe_from_csv",
    "load_cwe_from_json",
    # Extraction and search
    "extract_ai_tagged",
    "search_keywords",
    # Classification
    "classify_cwe",
    "classify_all",
    # Export
    "export_to_csv",
    "export_to_json",
    "generate_report",
    # Configuration
    "Config",
    "get_config",
]
