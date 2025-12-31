"""
Tests for data models.

These tests verify that our Pydantic models correctly validate data
and provide the expected behavior for properties and methods.
"""

import pytest
from pydantic import ValidationError

from cwe_ai_analysis.models import (
    AICategory,
    CWEEntry,
    CWEClassification,
    ClassificationSummary,
    ViewScore,
)


class TestViewScore:
    """Tests for the ViewScore enum."""

    def test_score_values(self):
        """Verify score values are 0-4."""
        assert ViewScore.NOT_APPLICABLE == 0
        assert ViewScore.WEAKLY_APPLICABLE == 1
        assert ViewScore.MODERATELY_APPLICABLE == 2
        assert ViewScore.HIGHLY_APPLICABLE == 3
        assert ViewScore.PRIMARY_EXAMPLE == 4

    def test_score_comparison(self):
        """Scores should be comparable."""
        assert ViewScore.PRIMARY_EXAMPLE > ViewScore.NOT_APPLICABLE
        assert ViewScore.HIGHLY_APPLICABLE >= ViewScore.MODERATELY_APPLICABLE


class TestCWEEntry:
    """Tests for CWEEntry model."""

    def test_valid_entry(self, sample_cwe_entry: CWEEntry):
        """Valid entries should be created without errors."""
        assert sample_cwe_entry.cwe_id == 79
        assert "Cross-site Scripting" in sample_cwe_entry.name

    def test_cwe_id_must_be_positive(self):
        """CWE ID must be >= 1."""
        with pytest.raises(ValidationError):
            CWEEntry(cwe_id=0, name="Invalid")

        with pytest.raises(ValidationError):
            CWEEntry(cwe_id=-1, name="Invalid")

    def test_name_required(self):
        """Name is required and cannot be empty."""
        with pytest.raises(ValidationError):
            CWEEntry(cwe_id=1, name="")

    def test_is_ai_tagged_property(self, ai_tagged_cwe_entry: CWEEntry, sample_cwe_entry: CWEEntry):
        """is_ai_tagged should correctly detect AI/ML tag."""
        assert ai_tagged_cwe_entry.is_ai_tagged is True
        assert sample_cwe_entry.is_ai_tagged is False

    def test_full_description_combines_fields(self):
        """full_description should combine description and extended_description."""
        entry = CWEEntry(
            cwe_id=1,
            name="Test",
            description="Short desc.",
            extended_description="Extended information.",
        )
        assert "Short desc." in entry.full_description
        assert "Extended information." in entry.full_description

    def test_str_representation(self, sample_cwe_entry: CWEEntry):
        """String representation should include ID and name."""
        str_repr = str(sample_cwe_entry)
        assert "CWE-79" in str_repr


class TestCWEClassification:
    """Tests for CWEClassification model."""

    def test_valid_classification(self, sample_classification: CWEClassification):
        """Valid classifications should be created."""
        assert sample_classification.cwe_id == 79
        assert sample_classification.view2_score == ViewScore.HIGHLY_APPLICABLE

    def test_max_score_property(self):
        """max_score should return the higher of the two view scores."""
        classification = CWEClassification(
            cwe_id=1,
            name="Test",
            view1_score=ViewScore.WEAKLY_APPLICABLE,
            view2_score=ViewScore.PRIMARY_EXAMPLE,
        )
        assert classification.max_score == ViewScore.PRIMARY_EXAMPLE

        classification2 = CWEClassification(
            cwe_id=2,
            name="Test2",
            view1_score=ViewScore.HIGHLY_APPLICABLE,
            view2_score=ViewScore.NOT_APPLICABLE,
        )
        assert classification2.max_score == ViewScore.HIGHLY_APPLICABLE

    def test_is_ai_relevant_property(self):
        """is_ai_relevant should be True when max_score >= 2."""
        relevant = CWEClassification(
            cwe_id=1,
            name="Relevant",
            view1_score=ViewScore.MODERATELY_APPLICABLE,
            view2_score=ViewScore.NOT_APPLICABLE,
        )
        assert relevant.is_ai_relevant is True

        not_relevant = CWEClassification(
            cwe_id=2,
            name="Not Relevant",
            view1_score=ViewScore.WEAKLY_APPLICABLE,
            view2_score=ViewScore.NOT_APPLICABLE,
        )
        assert not_relevant.is_ai_relevant is False

    def test_is_highly_ai_relevant_property(self):
        """is_highly_ai_relevant should be True when max_score >= 3."""
        highly_relevant = CWEClassification(
            cwe_id=1,
            name="Highly Relevant",
            view1_score=ViewScore.HIGHLY_APPLICABLE,
        )
        assert highly_relevant.is_highly_ai_relevant is True

        moderately_relevant = CWEClassification(
            cwe_id=2,
            name="Moderately Relevant",
            view1_score=ViewScore.MODERATELY_APPLICABLE,
        )
        assert moderately_relevant.is_highly_ai_relevant is False

    def test_to_csv_row(self, sample_classification: CWEClassification):
        """to_csv_row should return a flat dictionary."""
        row = sample_classification.to_csv_row()

        assert isinstance(row, dict)
        assert row["CWE_ID"] == 79
        assert row["View1_Score"] == 1
        assert row["View2_Score"] == 3
        assert row["MITRE_AI_Tagged"] == "No"
        assert row["Is_AI_Relevant"] == "Yes"

    def test_str_representation(self, sample_classification: CWEClassification):
        """String representation should include key info."""
        str_repr = str(sample_classification)
        assert "CWE-79" in str_repr
        assert "View1=" in str_repr
        assert "View2=" in str_repr


class TestClassificationSummary:
    """Tests for ClassificationSummary model."""

    def test_from_classifications(self, sample_classifications: list[CWEClassification]):
        """Summary should correctly aggregate classifications."""
        summary = ClassificationSummary.from_classifications(sample_classifications)

        assert summary.total_cwes == 3
        assert summary.mitre_ai_tagged_count == 1
        assert summary.ai_relevant_count == 2  # Scores >= 2
        assert summary.highly_ai_relevant_count == 2  # Scores >= 3

    def test_score_distribution(self, sample_classifications: list[CWEClassification]):
        """Score distributions should be correctly counted."""
        summary = ClassificationSummary.from_classifications(sample_classifications)

        # View 1: One 4, one 1, one 0
        assert summary.view1_score_counts[4] == 1
        assert summary.view1_score_counts[1] == 1
        assert summary.view1_score_counts[0] == 1

    def test_category_counts(self, sample_classifications: list[CWEClassification]):
        """Category counts should be correct."""
        summary = ClassificationSummary.from_classifications(sample_classifications)

        assert summary.category_counts[AICategory.PROMPT_INJECTION.value] == 1
        assert summary.category_counts[AICategory.OUTPUT_VALIDATION.value] == 1
        assert summary.category_counts[AICategory.NOT_APPLICABLE.value] == 1

    def test_empty_list(self):
        """Summary should handle empty list."""
        summary = ClassificationSummary.from_classifications([])
        assert summary.total_cwes == 0
        assert summary.ai_relevant_count == 0
