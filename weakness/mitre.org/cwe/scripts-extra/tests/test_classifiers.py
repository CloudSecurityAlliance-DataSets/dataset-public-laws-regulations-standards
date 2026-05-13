"""
Tests for classification logic.

These tests verify that the two-view classification model correctly
classifies CWE entries based on their AI relevance.
"""

from pathlib import Path

import pytest

from cwe_ai_analysis.classifiers import (
    classify_cwe,
    classify_all,
    KNOWN_CLASSIFICATIONS,
)
from cwe_ai_analysis.models import (
    AICategory,
    CWEEntry,
    CWEClassification,
    ViewScore,
)


class TestClassifyCWE:
    """Tests for single CWE classification."""

    def test_known_classification_prompt_injection(self):
        """Prompt injection (CWE-1427) should get high View 1 score."""
        entry = CWEEntry(
            cwe_id=1427,
            name="Improper Neutralization of Input Used for LLM Prompting",
            description="The product does not properly neutralize input.",
            applicable_platforms="TECHNOLOGY NAME:AI/ML::",
        )

        result = classify_cwe(entry)

        assert result.cwe_id == 1427
        assert result.view1_score == ViewScore.PRIMARY_EXAMPLE
        assert result.ai_category == AICategory.PROMPT_INJECTION

    def test_known_classification_xss(self):
        """XSS (CWE-79) should get high View 2 score."""
        entry = CWEEntry(
            cwe_id=79,
            name="Cross-site Scripting (XSS)",
            description="The product does not neutralize user input.",
        )

        result = classify_cwe(entry)

        assert result.cwe_id == 79
        assert result.view2_score >= ViewScore.HIGHLY_APPLICABLE
        # View 1 should be low for XSS
        assert result.view1_score <= ViewScore.WEAKLY_APPLICABLE

    def test_known_classification_command_injection(self):
        """Command injection (CWE-78) should get high View 2 score."""
        entry = CWEEntry(
            cwe_id=78,
            name="OS Command Injection",
            description="Constructs OS command using external input.",
        )

        result = classify_cwe(entry)

        assert result.view2_score == ViewScore.PRIMARY_EXAMPLE

    def test_known_classification_deserialization(self):
        """Deserialization (CWE-502) should get high View 1 score."""
        entry = CWEEntry(
            cwe_id=502,
            name="Deserialization of Untrusted Data",
            description="The product deserializes untrusted data.",
        )

        result = classify_cwe(entry)

        assert result.view1_score == ViewScore.PRIMARY_EXAMPLE
        assert result.ai_category == AICategory.SUPPLY_CHAIN

    def test_legacy_tech_classification(self, legacy_cwe_entry: CWEEntry):
        """Legacy tech CWEs should get low scores."""
        result = classify_cwe(legacy_cwe_entry)

        assert result.view1_score == ViewScore.NOT_APPLICABLE
        assert result.view2_score == ViewScore.NOT_APPLICABLE
        assert result.ai_category == AICategory.NOT_APPLICABLE

    def test_unknown_cwe_gets_default(self):
        """Unknown CWEs should get conservative default scores."""
        entry = CWEEntry(
            cwe_id=99999,  # Nonexistent CWE
            name="Unknown Weakness",
            description="Some generic weakness.",
        )

        result = classify_cwe(entry)

        # Should get some classification, even if low
        assert isinstance(result, CWEClassification)
        assert result.cwe_id == 99999

    def test_classification_preserves_entry_data(self, sample_cwe_entry: CWEEntry):
        """Classification should preserve original entry data."""
        result = classify_cwe(sample_cwe_entry)

        assert result.cwe_id == sample_cwe_entry.cwe_id
        assert result.name == sample_cwe_entry.name
        assert result.source_view == sample_cwe_entry.source_view

    def test_mitre_ai_tagged_flag(self, ai_tagged_cwe_entry: CWEEntry):
        """Classification should reflect MITRE AI/ML tagging."""
        result = classify_cwe(ai_tagged_cwe_entry)

        assert result.mitre_ai_tagged is True


class TestRuleBasedClassification:
    """Tests for rule-based classification patterns."""

    def test_injection_pattern_detection(self):
        """Entries with 'injection' should get high View 2."""
        entry = CWEEntry(
            cwe_id=9999,
            name="Code Injection",
            description="The product executes injected code.",
        )

        result = classify_cwe(entry)

        assert result.view2_score >= ViewScore.HIGHLY_APPLICABLE

    def test_path_traversal_pattern(self):
        """Path traversal entries should score on both views."""
        entry = CWEEntry(
            cwe_id=9998,
            name="Path Traversal",
            description="Directory traversal allows file access.",
        )

        result = classify_cwe(entry)

        assert result.view1_score >= ViewScore.MODERATELY_APPLICABLE
        assert result.view2_score >= ViewScore.HIGHLY_APPLICABLE

    def test_ssrf_pattern(self):
        """SSRF entries should get high View 2."""
        entry = CWEEntry(
            cwe_id=9997,
            name="Server-Side Request Forgery",
            description="SSRF allows making requests.",
        )

        result = classify_cwe(entry)

        assert result.view2_score == ViewScore.PRIMARY_EXAMPLE

    def test_auth_pattern(self):
        """Authentication entries should get moderate scores."""
        entry = CWEEntry(
            cwe_id=9996,
            name="Improper Authentication",
            description="Authentication weakness.",
        )

        result = classify_cwe(entry)

        assert result.view1_score >= ViewScore.MODERATELY_APPLICABLE


class TestClassifyAll:
    """Tests for batch classification."""

    def test_classify_all_entries(self, sample_cwe_entries: list[CWEEntry]):
        """Should classify all entries."""
        results = classify_all(sample_cwe_entries)

        assert len(results) == len(sample_cwe_entries)
        assert all(isinstance(r, CWEClassification) for r in results)

    def test_classify_all_unique_ids(self, sample_cwe_entries: list[CWEEntry]):
        """Each entry should be classified once."""
        results = classify_all(sample_cwe_entries)

        ids = [r.cwe_id for r in results]
        assert len(ids) == len(set(ids))  # No duplicates

    def test_classify_all_with_checkpoint(
        self,
        sample_cwe_entries: list[CWEEntry],
        temp_output_dir: Path,
    ):
        """Should save and use checkpoint."""
        checkpoint_file = temp_output_dir / "checkpoint.json"

        # First run
        results1 = classify_all(
            sample_cwe_entries,
            checkpoint_file=checkpoint_file,
            checkpoint_interval=2,
        )

        # Checkpoint should exist
        assert checkpoint_file.exists()

        # Second run should load from checkpoint
        results2 = classify_all(
            sample_cwe_entries,
            checkpoint_file=checkpoint_file,
        )

        assert len(results1) == len(results2)

    def test_classify_empty_list(self):
        """Should handle empty list."""
        results = classify_all([])
        assert results == []


class TestKnownClassifications:
    """Tests for the known classifications dictionary."""

    def test_known_classifications_exist(self):
        """Should have pre-defined classifications for key CWEs."""
        # Check that important CWEs are pre-classified
        assert 1427 in KNOWN_CLASSIFICATIONS  # Prompt injection
        assert 79 in KNOWN_CLASSIFICATIONS     # XSS
        assert 78 in KNOWN_CLASSIFICATIONS     # Command injection
        assert 502 in KNOWN_CLASSIFICATIONS    # Deserialization

    def test_known_classifications_have_required_fields(self):
        """Each known classification should have all required fields."""
        required_fields = [
            "view1_score",
            "view1_reasoning",
            "view2_score",
            "view2_reasoning",
            "ai_category",
            "ai_impact",
        ]

        for cwe_id, classification in KNOWN_CLASSIFICATIONS.items():
            for field in required_fields:
                assert field in classification, f"CWE-{cwe_id} missing {field}"

    def test_known_classification_scores_are_valid(self):
        """Scores should be valid ViewScore values."""
        for cwe_id, classification in KNOWN_CLASSIFICATIONS.items():
            assert classification["view1_score"] in ViewScore
            assert classification["view2_score"] in ViewScore

    def test_known_classification_categories_are_valid(self):
        """Categories should be valid AICategory values."""
        for cwe_id, classification in KNOWN_CLASSIFICATIONS.items():
            assert classification["ai_category"] in AICategory
