"""
Export functions for CWE classification results.

This module handles exporting classification results to various formats:
- CSV for spreadsheet analysis
- JSON for programmatic access
- Markdown for human-readable reports

Why multiple formats:
    - CSV: Easy to open in Excel, good for filtering/sorting
    - JSON: Machine-readable, preserves types, good for APIs
    - Markdown: Human-readable reports with formatting
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from cwe_ai_analysis.models import (
    CWEClassification,
    ClassificationSummary,
    ViewScore,
)

logger = logging.getLogger(__name__)


# CSV column order
# Why explicit order: Ensures consistent column ordering across runs
# and puts the most important columns first.
CSV_COLUMNS = [
    "CWE_ID",
    "Name",
    "MITRE_AI_Tagged",
    "View1_Score",
    "View2_Score",
    "Max_Score",
    "Is_AI_Relevant",
    "AI_Category",
    "Attack_Type",
    "Attack_Surface",
    "View1_Reasoning",
    "View2_Reasoning",
    "AI_Impact",
    "Description",
    "Source_View",
]


def export_to_csv(
    classifications: list[CWEClassification],
    output_path: Path,
    include_not_relevant: bool = True,
    min_score: int = 0,
) -> Path:
    """
    Export classifications to a CSV file.

    Why CSV:
        CSV is the most portable format for tabular data. Users can open it
        in Excel, Google Sheets, or any data analysis tool for filtering,
        sorting, and visualization.

    Args:
        classifications: List of classifications to export.
        output_path: Path for the output CSV file.
        include_not_relevant: If False, exclude CWEs with max_score=0.
        min_score: Minimum max_score to include (0-4).

    Returns:
        Path to the created CSV file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Filter based on options
    filtered = classifications
    if not include_not_relevant:
        filtered = [c for c in filtered if c.max_score > ViewScore.NOT_APPLICABLE]
    if min_score > 0:
        filtered = [c for c in filtered if c.max_score.value >= min_score]

    # Sort by max score descending, then by CWE ID
    # Why this sort: Most relevant CWEs appear first
    filtered.sort(key=lambda c: (-c.max_score.value, c.cwe_id))

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()

        for classification in filtered:
            writer.writerow(classification.to_csv_row())

    logger.info(f"Exported {len(filtered)} classifications to {output_path}")
    return output_path


def export_to_json(
    classifications: list[CWEClassification],
    output_path: Path,
    include_metadata: bool = True,
    pretty_print: bool = True,
) -> Path:
    """
    Export classifications to a JSON file.

    Why JSON:
        JSON preserves data types (enums become strings, but integers stay integers).
        It's ideal for programmatic access and can include metadata about
        the classification run.

    Args:
        classifications: List of classifications to export.
        output_path: Path for the output JSON file.
        include_metadata: If True, include metadata about the export.
        pretty_print: If True, format with indentation for readability.

    Returns:
        Path to the created JSON file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data: dict = {}

    if include_metadata:
        data["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "total_classifications": len(classifications),
            "version": "1.0.0",
            "methodology": "two-view-model",
        }

    # Convert classifications to dictionaries
    # Why model_dump: Pydantic's method handles enum conversion properly
    data["classifications"] = [
        c.model_dump(mode="json") for c in classifications
    ]

    # Add summary statistics
    if include_metadata:
        summary = ClassificationSummary.from_classifications(classifications)
        data["summary"] = summary.model_dump()

    indent = 2 if pretty_print else None
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, default=str)

    logger.info(f"Exported {len(classifications)} classifications to {output_path}")
    return output_path


def generate_report(
    classifications: list[CWEClassification],
    output_path: Optional[Path] = None,
    format: str = "markdown",
) -> str:
    """
    Generate a human-readable summary report.

    Why reports:
        While CSV/JSON are good for data, humans need summaries.
        The report provides key statistics and highlights important findings.

    Args:
        classifications: List of classifications to summarize.
        output_path: If provided, write report to this file.
        format: Output format: "markdown", "text", or "html".

    Returns:
        The report content as a string.
    """
    summary = ClassificationSummary.from_classifications(classifications)

    if format == "markdown":
        report = _generate_markdown_report(classifications, summary)
    elif format == "html":
        report = _generate_html_report(classifications, summary)
    else:
        report = _generate_text_report(classifications, summary)

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"Report written to {output_path}")

    return report


def _generate_markdown_report(
    classifications: list[CWEClassification],
    summary: ClassificationSummary,
) -> str:
    """Generate a Markdown-formatted report."""
    lines = [
        "# CWE AI Relevance Analysis Report",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "## Summary",
        "",
        f"- **Total CWEs Analyzed**: {summary.total_cwes}",
        f"- **MITRE AI/ML Tagged**: {summary.mitre_ai_tagged_count}",
        f"- **AI Relevant (score >= 2)**: {summary.ai_relevant_count}",
        f"- **Highly AI Relevant (score >= 3)**: {summary.highly_ai_relevant_count}",
        "",
        "## Score Distribution",
        "",
        "### View 1: Attacks ON AI",
        "",
        "| Score | Count | Percentage |",
        "|-------|-------|------------|",
    ]

    for score in range(5):
        count = summary.view1_score_counts.get(score, 0)
        pct = (count / summary.total_cwes * 100) if summary.total_cwes > 0 else 0
        lines.append(f"| {score} | {count} | {pct:.1f}% |")

    lines.extend([
        "",
        "### View 2: Attacks VIA AI",
        "",
        "| Score | Count | Percentage |",
        "|-------|-------|------------|",
    ])

    for score in range(5):
        count = summary.view2_score_counts.get(score, 0)
        pct = (count / summary.total_cwes * 100) if summary.total_cwes > 0 else 0
        lines.append(f"| {score} | {count} | {pct:.1f}% |")

    lines.extend([
        "",
        "## Category Distribution",
        "",
        "| Category | Count |",
        "|----------|-------|",
    ])

    for category, count in sorted(
        summary.category_counts.items(),
        key=lambda x: -x[1]
    ):
        lines.append(f"| {category} | {count} |")

    # Top View 1 CWEs
    top_view1 = sorted(
        [c for c in classifications if c.view1_score >= ViewScore.HIGHLY_APPLICABLE],
        key=lambda c: (-c.view1_score.value, c.cwe_id)
    )[:10]

    if top_view1:
        lines.extend([
            "",
            "## Top 10 CWEs: Attacks ON AI (View 1)",
            "",
            "| CWE | Name | Score | Reasoning |",
            "|-----|------|-------|-----------|",
        ])
        for c in top_view1:
            reasoning = c.view1_reasoning[:100] + "..." if len(c.view1_reasoning) > 100 else c.view1_reasoning
            lines.append(f"| CWE-{c.cwe_id} | {c.name[:40]} | {c.view1_score.value} | {reasoning} |")

    # Top View 2 CWEs
    top_view2 = sorted(
        [c for c in classifications if c.view2_score >= ViewScore.HIGHLY_APPLICABLE],
        key=lambda c: (-c.view2_score.value, c.cwe_id)
    )[:10]

    if top_view2:
        lines.extend([
            "",
            "## Top 10 CWEs: Attacks VIA AI (View 2)",
            "",
            "| CWE | Name | Score | Reasoning |",
            "|-----|------|-------|-----------|",
        ])
        for c in top_view2:
            reasoning = c.view2_reasoning[:100] + "..." if len(c.view2_reasoning) > 100 else c.view2_reasoning
            lines.append(f"| CWE-{c.cwe_id} | {c.name[:40]} | {c.view2_score.value} | {reasoning} |")

    lines.extend([
        "",
        "## Methodology",
        "",
        "This analysis uses the Two-View Model for CWE AI relevance:",
        "",
        "- **View 1 (Attacks ON AI)**: Weaknesses used to attack/compromise AI systems",
        "- **View 2 (Attacks VIA AI)**: Weaknesses attackers want AI to produce/execute",
        "",
        "See CWE-AI-METHODOLOGY.md for complete documentation.",
        "",
    ])

    return "\n".join(lines)


def _generate_text_report(
    classifications: list[CWEClassification],
    summary: ClassificationSummary,
) -> str:
    """Generate a plain text report."""
    lines = [
        "CWE AI Relevance Analysis Report",
        "=" * 40,
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "SUMMARY",
        "-" * 20,
        f"Total CWEs Analyzed: {summary.total_cwes}",
        f"MITRE AI/ML Tagged: {summary.mitre_ai_tagged_count}",
        f"AI Relevant (score >= 2): {summary.ai_relevant_count}",
        f"Highly AI Relevant (score >= 3): {summary.highly_ai_relevant_count}",
        "",
        "VIEW 1 SCORE DISTRIBUTION (Attacks ON AI)",
        "-" * 20,
    ]

    for score in range(5):
        count = summary.view1_score_counts.get(score, 0)
        lines.append(f"  Score {score}: {count}")

    lines.extend([
        "",
        "VIEW 2 SCORE DISTRIBUTION (Attacks VIA AI)",
        "-" * 20,
    ])

    for score in range(5):
        count = summary.view2_score_counts.get(score, 0)
        lines.append(f"  Score {score}: {count}")

    lines.append("")
    return "\n".join(lines)


def _generate_html_report(
    classifications: list[CWEClassification],
    summary: ClassificationSummary,
) -> str:
    """Generate an HTML report."""
    # Convert markdown to basic HTML
    md_report = _generate_markdown_report(classifications, summary)

    html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<title>CWE AI Relevance Analysis Report</title>",
        "<style>",
        "body { font-family: -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; }",
        "table { border-collapse: collapse; width: 100%; margin: 10px 0; }",
        "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
        "th { background-color: #f5f5f5; }",
        "h1, h2, h3 { color: #333; }",
        "code { background: #f5f5f5; padding: 2px 5px; }",
        "</style>",
        "</head>",
        "<body>",
    ]

    # Simple markdown to HTML conversion
    for line in md_report.split("\n"):
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("- "):
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.startswith("| ") and "---" not in line:
            cells = line.split("|")[1:-1]
            if "Score" in line or "CWE" in line or "Category" in line:
                row = "".join(f"<th>{c.strip()}</th>" for c in cells)
                html_lines.append(f"<tr>{row}</tr>")
            else:
                row = "".join(f"<td>{c.strip()}</td>" for c in cells)
                html_lines.append(f"<tr>{row}</tr>")
        elif line.startswith("*") and line.endswith("*"):
            html_lines.append(f"<em>{line[1:-1]}</em>")
        elif line:
            html_lines.append(f"<p>{line}</p>")

    html_lines.extend([
        "</body>",
        "</html>",
    ])

    return "\n".join(html_lines)
