"""
Command-line interface for CWE AI Analysis.

This module provides the CLI entry point for the cwe-ai tool.
It uses Typer for a modern CLI experience with automatic help generation.

Why Typer:
    - Automatic help text from type hints and docstrings
    - Clean, Pythonic API
    - Built on Click (battle-tested)
    - Good error messages and validation

Usage:
    cwe-ai extract INPUT_FILE --output OUTPUT_FILE
    cwe-ai search INPUT_FILE --keywords "prompt,injection"
    cwe-ai classify --input-dir ../
    cwe-ai report RESULTS_FILE --format markdown
"""

import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from cwe_ai_analysis.config import Config, get_config
from cwe_ai_analysis.loaders import load_cwe_data, load_all_cwe_views
from cwe_ai_analysis.extractors import (
    extract_ai_tagged,
    search_keywords,
    get_potential_ai_candidates,
)
from cwe_ai_analysis.classifiers import classify_all
from cwe_ai_analysis.exporters import export_to_csv, export_to_json, generate_report
from cwe_ai_analysis.models import ClassificationSummary

# Create the Typer app
# Why Rich: Provides beautiful terminal output with colors and formatting
app = typer.Typer(
    name="cwe-ai",
    help="CWE AI Relevance Analysis Tool - Analyze CWEs for AI security relevance",
    add_completion=False,  # Disable shell completion for simplicity
)
console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity setting."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


@app.command()
def extract(
    input_file: Path = typer.Argument(
        ...,
        help="Input CWE CSV or JSON file",
        exists=True,
        readable=True,
    ),
    output: Path = typer.Option(
        Path("ai-tagged.csv"),
        "--output", "-o",
        help="Output file path",
    ),
    format: str = typer.Option(
        "csv",
        "--format", "-f",
        help="Output format: csv, json",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose output",
    ),
) -> None:
    """
    Extract CWEs that MITRE has tagged as AI/ML relevant.

    This command finds CWEs with "AI/ML" in their Applicable Platforms field.
    These are officially recognized by MITRE as AI-relevant.

    Example:
        cwe-ai extract ../CWE-Research-Concepts-1000.csv -o ai-tagged.csv
    """
    setup_logging(verbose)

    console.print(f"[bold]Loading CWE data from[/bold] {input_file}")
    entries = load_cwe_data(input_file)
    console.print(f"Loaded {len(entries)} CWE entries")

    console.print("[bold]Extracting AI-tagged CWEs...[/bold]")
    ai_tagged = extract_ai_tagged(entries)

    if not ai_tagged:
        console.print("[yellow]No AI-tagged CWEs found[/yellow]")
        return

    # Display results
    table = Table(title=f"AI-Tagged CWEs ({len(ai_tagged)} found)")
    table.add_column("CWE-ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Abstraction", style="dim")

    for entry in ai_tagged[:20]:  # Show first 20
        table.add_row(
            f"CWE-{entry.cwe_id}",
            entry.name[:60] + ("..." if len(entry.name) > 60 else ""),
            entry.abstraction,
        )

    if len(ai_tagged) > 20:
        table.add_row("...", f"({len(ai_tagged) - 20} more)", "")

    console.print(table)

    # Export
    # Why convert to classifications: Maintains consistent output format
    from cwe_ai_analysis.classifiers import classify_cwe
    classifications = [classify_cwe(e) for e in ai_tagged]

    if format.lower() == "json":
        output_path = export_to_json(classifications, output)
    else:
        output_path = export_to_csv(classifications, output)

    console.print(f"[green]Exported to[/green] {output_path}")


@app.command()
def search(
    input_file: Path = typer.Argument(
        ...,
        help="Input CWE CSV or JSON file",
        exists=True,
        readable=True,
    ),
    keywords: str = typer.Option(
        None,
        "--keywords", "-k",
        help="Comma-separated keywords to search for",
    ),
    exclude: str = typer.Option(
        None,
        "--exclude", "-e",
        help="Comma-separated keywords to exclude",
    ),
    output: Path = typer.Option(
        Path("keyword-matches.csv"),
        "--output", "-o",
        help="Output file path",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose output",
    ),
) -> None:
    """
    Search CWEs for specific keywords.

    Searches CWE names, descriptions, and applicable platforms for matches.
    Use this to find potentially AI-relevant CWEs not tagged by MITRE.

    Example:
        cwe-ai search ../CWE-Research-Concepts-1000.csv -k "prompt,injection,model"
    """
    setup_logging(verbose)

    console.print(f"[bold]Loading CWE data from[/bold] {input_file}")
    entries = load_cwe_data(input_file)

    # Parse keywords
    include_kw = keywords.split(",") if keywords else None
    exclude_kw = exclude.split(",") if exclude else None

    if include_kw:
        console.print(f"Searching for: {', '.join(include_kw)}")

    matches = search_keywords(entries, include_kw, exclude_kw)
    console.print(f"[bold]Found {len(matches)} matches[/bold]")

    if not matches:
        console.print("[yellow]No matching CWEs found[/yellow]")
        return

    # Display results
    table = Table(title=f"Keyword Matches ({len(matches)} found)")
    table.add_column("CWE-ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("AI Tagged", style="green")

    for entry in matches[:20]:
        table.add_row(
            f"CWE-{entry.cwe_id}",
            entry.name[:50] + ("..." if len(entry.name) > 50 else ""),
            "Yes" if entry.is_ai_tagged else "No",
        )

    if len(matches) > 20:
        table.add_row("...", f"({len(matches) - 20} more)", "")

    console.print(table)

    # Export
    from cwe_ai_analysis.classifiers import classify_cwe
    classifications = [classify_cwe(e) for e in matches]
    output_path = export_to_csv(classifications, output)
    console.print(f"[green]Exported to[/green] {output_path}")


@app.command()
def classify(
    input_dir: Path = typer.Option(
        Path(".."),
        "--input-dir", "-i",
        help="Directory containing CWE CSV files",
    ),
    output: Path = typer.Option(
        Path("output/CWE-AI-Analysis.csv"),
        "--output", "-o",
        help="Output file path",
    ),
    checkpoint: Optional[Path] = typer.Option(
        None,
        "--checkpoint", "-c",
        help="Checkpoint file for resuming interrupted runs",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Also export as JSON",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose output",
    ),
) -> None:
    """
    Run full two-view classification on all CWEs.

    Processes all CWE views (Research Concepts, Software Development,
    Hardware Design) and classifies each for AI relevance.

    Example:
        cwe-ai classify --input-dir ../ --output results/CWE-AI-Analysis.csv
    """
    setup_logging(verbose)

    # Update config with provided paths
    config = Config(data_dir=input_dir)

    console.print("[bold]Loading all CWE views...[/bold]")
    entries = load_all_cwe_views(config)
    console.print(f"Loaded {len(entries)} unique CWE entries")

    console.print("[bold]Classifying CWEs...[/bold]")
    classifications = classify_all(
        entries,
        checkpoint_file=checkpoint,
        checkpoint_interval=50,
    )

    # Generate summary
    summary = ClassificationSummary.from_classifications(classifications)

    # Display summary
    console.print("\n[bold]Classification Summary[/bold]")
    table = Table()
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Total CWEs", str(summary.total_cwes))
    table.add_row("MITRE AI/ML Tagged", str(summary.mitre_ai_tagged_count))
    table.add_row("AI Relevant (score >= 2)", str(summary.ai_relevant_count))
    table.add_row("Highly Relevant (score >= 3)", str(summary.highly_ai_relevant_count))

    console.print(table)

    # Export
    csv_path = export_to_csv(classifications, output)
    console.print(f"[green]CSV exported to[/green] {csv_path}")

    if json_output:
        json_path = output.with_suffix(".json")
        export_to_json(classifications, json_path)
        console.print(f"[green]JSON exported to[/green] {json_path}")


@app.command()
def report(
    input_file: Path = typer.Argument(
        ...,
        help="Input classification results (CSV or JSON)",
        exists=True,
        readable=True,
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path (prints to console if not specified)",
    ),
    format: str = typer.Option(
        "markdown",
        "--format", "-f",
        help="Output format: markdown, text, html",
    ),
) -> None:
    """
    Generate a summary report from classification results.

    Creates a human-readable report with statistics and highlights.

    Example:
        cwe-ai report results/CWE-AI-Analysis.csv --format markdown -o report.md
    """
    import csv as csv_module
    import json

    # Load classifications from file
    # Why support both formats: Users might have either from previous runs
    suffix = input_file.suffix.lower()

    classifications = []
    if suffix == ".json":
        with open(input_file, "r") as f:
            data = json.load(f)
            from cwe_ai_analysis.models import CWEClassification
            for item in data.get("classifications", data):
                classifications.append(CWEClassification(**item))
    else:
        # Assume CSV
        with open(input_file, "r") as f:
            reader = csv_module.DictReader(f)
            from cwe_ai_analysis.models import CWEClassification, ViewScore, AICategory
            for row in reader:
                classifications.append(CWEClassification(
                    cwe_id=int(row["CWE_ID"]),
                    name=row["Name"],
                    description=row.get("Description", ""),
                    mitre_ai_tagged=row.get("MITRE_AI_Tagged") == "Yes",
                    view1_score=ViewScore(int(row["View1_Score"])),
                    view1_reasoning=row.get("View1_Reasoning", ""),
                    view2_score=ViewScore(int(row["View2_Score"])),
                    view2_reasoning=row.get("View2_Reasoning", ""),
                    ai_category=AICategory(row.get("AI_Category", "Not Applicable")),
                    ai_impact=row.get("AI_Impact", ""),
                    source_view=row.get("Source_View", ""),
                ))

    console.print(f"Loaded {len(classifications)} classifications")

    report_content = generate_report(
        classifications,
        output_path=output,
        format=format,
    )

    if not output:
        console.print(report_content)
    else:
        console.print(f"[green]Report written to[/green] {output}")


@app.command()
def info() -> None:
    """
    Display information about the tool and methodology.
    """
    console.print("[bold]CWE AI Relevance Analysis Tool[/bold]")
    console.print()
    console.print("This tool classifies CWE entries for AI security relevance")
    console.print("using a two-view classification model:")
    console.print()
    console.print("[cyan]View 1: Attacks ON AI[/cyan]")
    console.print("  Can this weakness be used to attack/compromise AI systems?")
    console.print("  Examples: Prompt injection, model poisoning, adversarial inputs")
    console.print()
    console.print("[cyan]View 2: Attacks VIA AI[/cyan]")
    console.print("  Would attackers want AI to produce/execute this weakness?")
    console.print("  Examples: XSS, command injection, SSRF (via AI agents)")
    console.print()
    console.print("[bold]Scoring Scale (0-4):[/bold]")
    console.print("  0 - Not Applicable")
    console.print("  1 - Weakly Applicable")
    console.print("  2 - Moderately Applicable")
    console.print("  3 - Highly Applicable")
    console.print("  4 - Primary Example")
    console.print()
    console.print("See CWE-AI-METHODOLOGY.md for complete documentation.")


@app.command()
def version() -> None:
    """
    Display version information.
    """
    from cwe_ai_analysis import __version__
    console.print(f"cwe-ai version {__version__}")


# Entry point
# Why this pattern: Allows both `python -m cwe_ai_analysis.cli` and
# the installed `cwe-ai` command to work.
if __name__ == "__main__":
    app()
