"""
Data loading functions for CWE files.

This module handles loading CWE data from various file formats (CSV, JSON).
It's responsible for parsing the raw data and converting it into CWEEntry objects.

Why a separate loaders module:
    - Single responsibility: Loading is distinct from processing/classification
    - Testability: Easy to test loading in isolation
    - Flexibility: Can add new data sources (API, database) without changing other code

Data Sources:
    The CWE data comes in multiple views, each as a separate file:
    - CWE-Research-Concepts-1000.csv: Most comprehensive (~944 entries)
    - CWE-Software-Development-699.csv: Development-focused (~399 entries)
    - CWE-Hardware-Design-1194.csv: Hardware weaknesses (~110 entries)

    When loading all views, we deduplicate by CWE ID since some CWEs appear
    in multiple views.
"""

import csv
import json
import logging
from pathlib import Path
from typing import Optional

from cwe_ai_analysis.config import Config, get_config
from cwe_ai_analysis.models import CWEEntry

logger = logging.getLogger(__name__)


# Column name mappings from CSV headers to our model fields
# Why this mapping: CWE CSV uses different naming conventions than our model.
# This centralizes the mapping so changes only need to happen here.
CSV_COLUMN_MAPPING = {
    "CWE-ID": "cwe_id",
    "Name": "name",
    "Description": "description",
    "Extended Description": "extended_description",
    "Applicable Platforms": "applicable_platforms",
    "Weakness Abstraction": "abstraction",
    "Status": "status",
    "Related Weaknesses": "related_weaknesses",
    "Common Consequences": "common_consequences",
    "Potential Mitigations": "potential_mitigations",
}


def load_cwe_from_csv(
    file_path: Path,
    source_view: Optional[str] = None,
) -> list[CWEEntry]:
    """
    Load CWE entries from a CSV file.

    Why standard csv module:
        The MITRE CWE CSV files have data rows with an extra trailing column
        (24 columns vs 23 header columns). The standard csv module handles this
        gracefully by reading each row's actual columns, while pandas expects
        consistent column counts and misaligns the data.

    Args:
        file_path: Path to the CSV file.
        source_view: Optional name to identify which view this data came from.
                    If not provided, derived from filename.

    Returns:
        List of CWEEntry objects.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the file can't be parsed as valid CWE data.
    """
    logger.info(f"Loading CWE data from {file_path}")

    if not file_path.exists():
        raise FileNotFoundError(f"CWE data file not found: {file_path}")

    # Derive source_view from filename if not provided
    # Why: Helps track where each CWE came from when merging multiple views
    if source_view is None:
        source_view = file_path.stem  # e.g., "CWE-Research-Concepts-1000"

    entries = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for idx, row in enumerate(reader):
                try:
                    # Convert CWE-ID to integer
                    # Why explicit conversion: The ID should always be numeric,
                    # and we want to catch any non-numeric IDs early.
                    cwe_id_str = row.get("CWE-ID", "")
                    if not cwe_id_str or not cwe_id_str.isdigit():
                        logger.warning(f"Skipping row {idx}: invalid CWE-ID '{cwe_id_str}'")
                        continue

                    # Map CSV column names to our model fields
                    entry = CWEEntry(
                        cwe_id=int(cwe_id_str),
                        name=row.get("Name", ""),
                        description=row.get("Description", ""),
                        extended_description=row.get("Extended Description", ""),
                        applicable_platforms=row.get("Applicable Platforms", ""),
                        abstraction=row.get("Weakness Abstraction", ""),
                        status=row.get("Status", ""),
                        related_weaknesses=row.get("Related Weaknesses", ""),
                        common_consequences=row.get("Common Consequences", ""),
                        potential_mitigations=row.get("Potential Mitigations", ""),
                        source_view=source_view,
                    )
                    entries.append(entry)

                except Exception as e:
                    # Log but continue - don't let one bad row stop the whole load
                    # Why: CWE data might have inconsistencies, but we want to process
                    # as much as possible rather than failing completely.
                    logger.warning(f"Error parsing row {idx}: {e}")
                    continue

    except Exception as e:
        raise ValueError(f"Failed to parse CSV file {file_path}: {e}") from e

    logger.info(f"Loaded {len(entries)} CWE entries from {file_path}")
    return entries


def load_cwe_from_json(
    file_path: Path,
    source_view: Optional[str] = None,
) -> list[CWEEntry]:
    """
    Load CWE entries from a JSON file.

    The JSON format from MITRE has a nested structure. This function handles
    extracting the weakness entries from that structure.

    Why support JSON:
        JSON preserves data types and structure better than CSV.
        It's also the format used by some MITRE APIs and tools.

    Args:
        file_path: Path to the JSON file.
        source_view: Optional name to identify which view this data came from.

    Returns:
        List of CWEEntry objects.
    """
    logger.info(f"Loading CWE data from JSON: {file_path}")

    if not file_path.exists():
        raise FileNotFoundError(f"CWE data file not found: {file_path}")

    if source_view is None:
        source_view = file_path.stem

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON file {file_path}: {e}") from e

    # Navigate the nested MITRE JSON structure
    # Why this path: MITRE's JSON format nests weaknesses under
    # Weakness_Catalog -> Weaknesses -> Weakness
    weaknesses = []
    try:
        catalog = data.get("Weakness_Catalog", data)
        weaknesses_container = catalog.get("Weaknesses", {})
        weaknesses = weaknesses_container.get("Weakness", [])

        # Handle single weakness (not in a list)
        if isinstance(weaknesses, dict):
            weaknesses = [weaknesses]
    except (KeyError, TypeError) as e:
        logger.warning(f"Unexpected JSON structure in {file_path}: {e}")
        # Try to handle as a simple list of weaknesses
        if isinstance(data, list):
            weaknesses = data

    entries = []
    for w in weaknesses:
        try:
            # MITRE JSON uses +@ID format for attributes
            # Why this format: It's how the XML-to-JSON conversion preserves XML attributes
            cwe_id = w.get("+@ID") or w.get("ID") or w.get("cwe_id")
            if not cwe_id:
                continue

            # Extract applicable platforms from nested structure
            platforms = ""
            platforms_data = w.get("Applicable_Platforms", {})
            if isinstance(platforms_data, dict):
                # Collect all platform types (Language, Technology, etc.)
                platform_parts = []
                for key in ["Language", "Technology", "Operating_System", "Architecture"]:
                    platform_info = platforms_data.get(key, [])
                    if isinstance(platform_info, dict):
                        platform_info = [platform_info]
                    for p in platform_info:
                        if isinstance(p, dict):
                            name = p.get("+@Name") or p.get("+@Class") or ""
                            if name:
                                platform_parts.append(name)
                platforms = "::".join(platform_parts)

            entry = CWEEntry(
                cwe_id=int(cwe_id),
                name=w.get("+@Name") or w.get("Name") or "",
                description=w.get("Description") or "",
                extended_description=w.get("Extended_Description") or "",
                applicable_platforms=platforms,
                abstraction=w.get("+@Abstraction") or w.get("Abstraction") or "",
                status=w.get("+@Status") or w.get("Status") or "",
                related_weaknesses=str(w.get("Related_Weaknesses", "")),
                common_consequences=str(w.get("Common_Consequences", "")),
                potential_mitigations=str(w.get("Potential_Mitigations", "")),
                source_view=source_view,
            )
            entries.append(entry)

        except Exception as e:
            logger.warning(f"Error parsing JSON weakness entry: {e}")
            continue

    logger.info(f"Loaded {len(entries)} CWE entries from {file_path}")
    return entries


def load_cwe_data(
    file_path: Path | str,
    source_view: Optional[str] = None,
) -> list[CWEEntry]:
    """
    Load CWE data from a file, auto-detecting the format.

    This is the main entry point for loading CWE data. It determines
    the file format from the extension and delegates to the appropriate loader.

    Why auto-detection:
        Makes the API simpler - users don't need to know which loader to use.
        Just pass a file path and it works.

    Args:
        file_path: Path to the CWE data file (CSV or JSON).
        source_view: Optional identifier for the data source.

    Returns:
        List of CWEEntry objects.

    Raises:
        ValueError: If the file format is not supported.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return load_cwe_from_csv(path, source_view)
    elif suffix == ".json":
        return load_cwe_from_json(path, source_view)
    else:
        raise ValueError(f"Unsupported file format: {suffix}. Use .csv or .json")


def load_all_cwe_views(
    config: Optional[Config] = None,
    deduplicate: bool = True,
) -> list[CWEEntry]:
    """
    Load CWE entries from all three standard views.

    This loads:
    - CWE-1000 (Research Concepts): ~944 entries
    - CWE-699 (Software Development): ~399 entries
    - CWE-1194 (Hardware Design): ~110 entries

    Why load all views:
        Different views organize CWEs differently. The Research Concepts view
        is most comprehensive, but Hardware Design view includes hardware-specific
        weaknesses that might be relevant to AI hardware (GPUs, TPUs, etc.).

    Args:
        config: Configuration object. If not provided, uses default config.
        deduplicate: If True, remove duplicate CWE IDs (keeping first occurrence).

    Returns:
        Combined list of CWEEntry objects from all views.
    """
    if config is None:
        config = get_config()

    all_entries: list[CWEEntry] = []

    # Define the files to load with their source identifiers
    # Why this order: Research Concepts is most comprehensive, so load it first.
    # When deduplicating, the first occurrence is kept.
    files_to_load = [
        (config.research_concepts_file, "Research-Concepts-1000"),
        (config.software_development_file, "Software-Development-699"),
        (config.hardware_design_file, "Hardware-Design-1194"),
    ]

    for filename, source_view in files_to_load:
        file_path = config.get_data_file_path(filename)
        if file_path.exists():
            try:
                entries = load_cwe_data(file_path, source_view)
                all_entries.extend(entries)
                logger.info(f"Loaded {len(entries)} entries from {source_view}")
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}")
        else:
            logger.warning(f"File not found, skipping: {file_path}")

    if deduplicate:
        # Remove duplicates, keeping first occurrence
        # Why: A CWE might appear in multiple views. We keep the first (from
        # Research Concepts) since it's typically most complete.
        seen_ids: set[int] = set()
        unique_entries: list[CWEEntry] = []
        duplicates = 0

        for entry in all_entries:
            if entry.cwe_id not in seen_ids:
                seen_ids.add(entry.cwe_id)
                unique_entries.append(entry)
            else:
                duplicates += 1

        if duplicates > 0:
            logger.info(f"Removed {duplicates} duplicate CWE entries")

        all_entries = unique_entries

    logger.info(f"Total CWE entries loaded: {len(all_entries)}")
    return all_entries
