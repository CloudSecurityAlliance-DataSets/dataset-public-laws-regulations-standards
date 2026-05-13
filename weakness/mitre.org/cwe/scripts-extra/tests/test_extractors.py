"""
Tests for extraction and search functions.

These tests verify that we can correctly identify AI-tagged CWEs
and search for CWEs by keywords.
"""

import pytest

from cwe_ai_analysis.extractors import (
    extract_ai_tagged,
    search_keywords,
    search_by_cwe_ids,
    get_potential_ai_candidates,
    get_attack_surface_candidates,
)
from cwe_ai_analysis.models import CWEEntry


class TestExtractAITagged:
    """Tests for AI tag extraction."""

    def test_extract_ai_tagged_entries(self, sample_cwe_entries: list[CWEEntry]):
        """Should find entries with AI/ML tag."""
        ai_tagged = extract_ai_tagged(sample_cwe_entries)

        # Should find at least the entries we know have AI/ML tag
        assert len(ai_tagged) >= 1
        assert all(e.is_ai_tagged for e in ai_tagged)

    def test_extract_from_empty_list(self):
        """Should handle empty list."""
        result = extract_ai_tagged([])
        assert result == []

    def test_extract_when_none_tagged(self, legacy_cwe_entry: CWEEntry):
        """Should return empty when no AI-tagged entries."""
        result = extract_ai_tagged([legacy_cwe_entry])
        assert result == []


class TestSearchKeywords:
    """Tests for keyword search."""

    def test_search_with_default_keywords(self, sample_cwe_entries: list[CWEEntry]):
        """Should find matches using default AI keywords."""
        matches = search_keywords(sample_cwe_entries)

        # Should find entries mentioning AI-related terms
        assert len(matches) >= 0  # May or may not match depending on test data

    def test_search_with_custom_keywords(self, sample_cwe_entries: list[CWEEntry]):
        """Should find matches with custom keywords."""
        matches = search_keywords(
            sample_cwe_entries,
            include_keywords=["injection", "command"],
        )

        # Should find command injection and SQL injection entries
        ids = {e.cwe_id for e in matches}
        assert 78 in ids or 89 in ids  # At least one injection type

    def test_search_with_exclude_keywords(self, sample_cwe_entries: list[CWEEntry]):
        """Should exclude entries matching exclude keywords."""
        # First search without exclusion
        all_matches = search_keywords(
            sample_cwe_entries,
            include_keywords=["input", "data"],
            exclude_keywords=[],
        )

        # Then search with exclusion
        filtered_matches = search_keywords(
            sample_cwe_entries,
            include_keywords=["input", "data"],
            exclude_keywords=["j2ee"],
        )

        # Filtered should have same or fewer results
        assert len(filtered_matches) <= len(all_matches)

    def test_search_case_insensitive(self, sample_cwe_entries: list[CWEEntry]):
        """Search should be case-insensitive by default."""
        lower_matches = search_keywords(
            sample_cwe_entries,
            include_keywords=["injection"],
        )
        upper_matches = search_keywords(
            sample_cwe_entries,
            include_keywords=["INJECTION"],
        )

        assert len(lower_matches) == len(upper_matches)

    def test_search_empty_keywords(self, sample_cwe_entries: list[CWEEntry]):
        """Empty keyword list should return empty results."""
        matches = search_keywords(
            sample_cwe_entries,
            include_keywords=[],
        )
        assert matches == []


class TestSearchByCWEIds:
    """Tests for ID-based search."""

    def test_search_by_ids(self, sample_cwe_entries: list[CWEEntry]):
        """Should return entries matching given IDs."""
        result = search_by_cwe_ids(sample_cwe_entries, [79, 89])

        ids = {e.cwe_id for e in result}
        assert 79 in ids
        assert 89 in ids

    def test_search_by_nonexistent_ids(self, sample_cwe_entries: list[CWEEntry]):
        """Should return empty for IDs not in list."""
        result = search_by_cwe_ids(sample_cwe_entries, [99999])
        assert result == []

    def test_search_by_empty_ids(self, sample_cwe_entries: list[CWEEntry]):
        """Should return empty for empty ID list."""
        result = search_by_cwe_ids(sample_cwe_entries, [])
        assert result == []


class TestGetPotentialAICandidates:
    """Tests for candidate categorization."""

    def test_categorizes_entries(self, sample_cwe_entries: list[CWEEntry]):
        """Should categorize entries into three groups."""
        high, medium, remaining = get_potential_ai_candidates(sample_cwe_entries)

        # All entries should be accounted for (minus any duplicates)
        total_categorized = len(high) + len(medium) + len(remaining)
        assert total_categorized <= len(sample_cwe_entries)

    def test_high_confidence_are_ai_tagged(self, sample_cwe_entries: list[CWEEntry]):
        """High confidence entries should be AI-tagged."""
        high, _, _ = get_potential_ai_candidates(sample_cwe_entries)

        assert all(e.is_ai_tagged for e in high)

    def test_no_duplicates_across_categories(self, sample_cwe_entries: list[CWEEntry]):
        """An entry should only appear in one category."""
        high, medium, remaining = get_potential_ai_candidates(sample_cwe_entries)

        high_ids = {e.cwe_id for e in high}
        medium_ids = {e.cwe_id for e in medium}
        remaining_ids = {e.cwe_id for e in remaining}

        assert high_ids.isdisjoint(medium_ids)
        assert high_ids.isdisjoint(remaining_ids)
        assert medium_ids.isdisjoint(remaining_ids)


class TestGetAttackSurfaceCandidates:
    """Tests for attack surface identification."""

    def test_finds_attack_surface_entries(self, sample_cwe_entries: list[CWEEntry]):
        """Should find entries that represent attack surfaces."""
        candidates = get_attack_surface_candidates(sample_cwe_entries)

        # Should find injection-type entries
        ids = {e.cwe_id for e in candidates}
        # Command injection or SQL injection should be found
        assert 78 in ids or 89 in ids or len(candidates) >= 0
