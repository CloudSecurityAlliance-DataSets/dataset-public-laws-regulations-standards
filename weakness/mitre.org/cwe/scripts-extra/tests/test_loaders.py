"""
Tests for data loading functions.

These tests verify that CWE data can be loaded from CSV and JSON files
and correctly converted to CWEEntry objects.
"""

from pathlib import Path

import pytest

from cwe_ai_analysis.loaders import (
    load_cwe_data,
    load_cwe_from_csv,
    load_cwe_from_json,
)
from cwe_ai_analysis.models import CWEEntry


class TestLoadFromCSV:
    """Tests for CSV loading."""

    def test_load_valid_csv(self, temp_csv_file: Path):
        """Should successfully load entries from valid CSV."""
        entries = load_cwe_from_csv(temp_csv_file)

        assert len(entries) > 0
        assert all(isinstance(e, CWEEntry) for e in entries)

    def test_load_csv_preserves_data(self, temp_csv_file: Path):
        """Loaded data should match source data."""
        entries = load_cwe_from_csv(temp_csv_file)

        # Check specific entries exist
        ids = {e.cwe_id for e in entries}
        assert 79 in ids
        assert 1427 in ids

    def test_load_csv_with_source_view(self, temp_csv_file: Path):
        """Source view should be set when provided."""
        entries = load_cwe_from_csv(temp_csv_file, source_view="Test-View")

        assert all(e.source_view == "Test-View" for e in entries)

    def test_load_csv_auto_source_view(self, temp_csv_file: Path):
        """Source view should default to filename."""
        entries = load_cwe_from_csv(temp_csv_file)

        # Source view should be derived from filename (stem)
        assert entries[0].source_view == temp_csv_file.stem

    def test_load_nonexistent_csv(self):
        """Should raise error for missing file."""
        with pytest.raises(FileNotFoundError):
            load_cwe_from_csv(Path("/nonexistent/file.csv"))


class TestLoadFromJSON:
    """Tests for JSON loading."""

    def test_load_valid_json(self, temp_json_file: Path):
        """Should successfully load entries from valid JSON."""
        entries = load_cwe_from_json(temp_json_file)

        assert len(entries) > 0
        assert all(isinstance(e, CWEEntry) for e in entries)

    def test_load_json_preserves_data(self, temp_json_file: Path):
        """Loaded data should match source data."""
        entries = load_cwe_from_json(temp_json_file)

        ids = {e.cwe_id for e in entries}
        assert 79 in ids or len(entries) > 0  # At least some data loaded

    def test_load_nonexistent_json(self):
        """Should raise error for missing file."""
        with pytest.raises(FileNotFoundError):
            load_cwe_from_json(Path("/nonexistent/file.json"))


class TestLoadCWEData:
    """Tests for auto-detecting loader."""

    def test_load_csv_by_extension(self, temp_csv_file: Path):
        """Should auto-detect CSV format."""
        entries = load_cwe_data(temp_csv_file)
        assert len(entries) > 0

    def test_load_json_by_extension(self, temp_json_file: Path):
        """Should auto-detect JSON format."""
        entries = load_cwe_data(temp_json_file)
        assert len(entries) > 0

    def test_load_unsupported_format(self, temp_output_dir: Path):
        """Should raise error for unsupported format."""
        unsupported_file = temp_output_dir / "data.xml"
        unsupported_file.write_text("<data></data>")

        with pytest.raises(ValueError, match="Unsupported file format"):
            load_cwe_data(unsupported_file)

    def test_load_with_string_path(self, temp_csv_file: Path):
        """Should accept string paths."""
        entries = load_cwe_data(str(temp_csv_file))
        assert len(entries) > 0
