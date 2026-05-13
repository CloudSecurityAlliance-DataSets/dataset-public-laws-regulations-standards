"""
Pytest fixtures for CWE AI Analysis tests.

This module provides shared test fixtures that can be used across all test files.
Fixtures create consistent test data and avoid code duplication.

Why fixtures:
    - Consistent test data across tests
    - Isolation between tests
    - Reusable setup code
    - Clear test dependencies
"""

import csv
import json
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from cwe_ai_analysis.models import (
    AICategory,
    CWEEntry,
    CWEClassification,
    ViewScore,
)


@pytest.fixture
def sample_cwe_entry() -> CWEEntry:
    """
    A basic CWE entry for testing.

    Why this fixture:
        Provides a simple, valid CWE entry that can be used in many tests.
        Based on a real CWE but simplified for testing.
    """
    return CWEEntry(
        cwe_id=79,
        name="Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')",
        description="The product does not neutralize or incorrectly neutralizes user-controllable input.",
        extended_description="Cross-site scripting (XSS) vulnerabilities occur when...",
        applicable_platforms="LANGUAGE CLASS:Not Language-Specific::TECHNOLOGY CLASS:Web Based::",
        abstraction="Base",
        status="Stable",
        source_view="Research-Concepts-1000",
    )


@pytest.fixture
def ai_tagged_cwe_entry() -> CWEEntry:
    """
    A CWE entry that has the AI/ML tag.

    Why this fixture:
        Tests that check AI tag detection need entries with the tag.
    """
    return CWEEntry(
        cwe_id=1427,
        name="Improper Neutralization of Input Used for LLM Prompting",
        description="The product does not properly neutralize input used in LLM prompts.",
        applicable_platforms="TECHNOLOGY NAME:AI/ML:TECHNOLOGY PREVALENCE:Undetermined::",
        abstraction="Base",
        status="Incomplete",
        source_view="Research-Concepts-1000",
    )


@pytest.fixture
def legacy_cwe_entry() -> CWEEntry:
    """
    A CWE entry for legacy technology (should not be AI-relevant).

    Why this fixture:
        Tests that legacy tech is correctly identified as not AI-relevant.
    """
    return CWEEntry(
        cwe_id=5,
        name="J2EE Misconfiguration: Data Transmission Without Encryption",
        description="Information sent over a network can be compromised while in transit.",
        applicable_platforms="LANGUAGE NAME:Java::",
        abstraction="Variant",
        status="Draft",
        source_view="Research-Concepts-1000",
    )


@pytest.fixture
def sample_cwe_entries(
    sample_cwe_entry: CWEEntry,
    ai_tagged_cwe_entry: CWEEntry,
    legacy_cwe_entry: CWEEntry,
) -> list[CWEEntry]:
    """
    A collection of diverse CWE entries for testing.

    Why this fixture:
        Many tests need multiple entries with different characteristics.
    """
    return [
        sample_cwe_entry,
        ai_tagged_cwe_entry,
        legacy_cwe_entry,
        CWEEntry(
            cwe_id=78,
            name="Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')",
            description="The product constructs an OS command using externally-influenced input.",
            applicable_platforms="TECHNOLOGY NAME:AI/ML::",
            abstraction="Base",
            status="Stable",
            source_view="Research-Concepts-1000",
        ),
        CWEEntry(
            cwe_id=89,
            name="Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')",
            description="The product constructs an SQL command using externally-influenced input.",
            applicable_platforms="LANGUAGE CLASS:Not Language-Specific::",
            abstraction="Base",
            status="Stable",
            source_view="Research-Concepts-1000",
        ),
    ]


@pytest.fixture
def sample_classification() -> CWEClassification:
    """
    A sample classification result for testing.

    Why this fixture:
        Tests for export, reporting, etc. need classification objects.
    """
    return CWEClassification(
        cwe_id=79,
        name="Cross-site Scripting (XSS)",
        description="The product does not neutralize user input.",
        mitre_ai_tagged=False,
        view1_score=ViewScore.WEAKLY_APPLICABLE,
        view1_reasoning="XSS could affect AI web interfaces, not AI-specific.",
        view2_score=ViewScore.HIGHLY_APPLICABLE,
        view2_reasoning="Attackers want AI to generate XSS payloads.",
        ai_category=AICategory.OUTPUT_VALIDATION,
        ai_impact="Session hijacking via AI-generated content.",
        source_view="Research-Concepts-1000",
    )


@pytest.fixture
def sample_classifications() -> list[CWEClassification]:
    """
    A collection of classifications for testing aggregation/export.

    Why this fixture:
        Export and report tests need multiple classifications.
    """
    return [
        CWEClassification(
            cwe_id=1427,
            name="Prompt Injection",
            mitre_ai_tagged=True,
            view1_score=ViewScore.PRIMARY_EXAMPLE,
            view1_reasoning="Canonical attack on LLMs.",
            view2_score=ViewScore.HIGHLY_APPLICABLE,
            view2_reasoning="Enables other attacks.",
            ai_category=AICategory.PROMPT_INJECTION,
        ),
        CWEClassification(
            cwe_id=79,
            name="XSS",
            mitre_ai_tagged=False,
            view1_score=ViewScore.WEAKLY_APPLICABLE,
            view1_reasoning="Not AI-specific.",
            view2_score=ViewScore.HIGHLY_APPLICABLE,
            view2_reasoning="AI generates XSS.",
            ai_category=AICategory.OUTPUT_VALIDATION,
        ),
        CWEClassification(
            cwe_id=5,
            name="J2EE Misconfiguration",
            mitre_ai_tagged=False,
            view1_score=ViewScore.NOT_APPLICABLE,
            view1_reasoning="Legacy tech.",
            view2_score=ViewScore.NOT_APPLICABLE,
            view2_reasoning="Legacy tech.",
            ai_category=AICategory.NOT_APPLICABLE,
        ),
    ]


@pytest.fixture
def temp_csv_file(sample_cwe_entries: list[CWEEntry]) -> Generator[Path, None, None]:
    """
    Create a temporary CSV file with CWE data for testing.

    Why this fixture:
        Loader tests need actual files to read. Using temp files ensures
        tests don't affect real data and cleanup happens automatically.
    """
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "CWE-ID", "Name", "Description", "Extended Description",
                "Applicable Platforms", "Weakness Abstraction", "Status",
            ],
        )
        writer.writeheader()

        for entry in sample_cwe_entries:
            writer.writerow({
                "CWE-ID": str(entry.cwe_id),
                "Name": entry.name,
                "Description": entry.description,
                "Extended Description": entry.extended_description,
                "Applicable Platforms": entry.applicable_platforms,
                "Weakness Abstraction": entry.abstraction,
                "Status": entry.status,
            })

        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    temp_path.unlink(missing_ok=True)


@pytest.fixture
def temp_json_file(sample_cwe_entries: list[CWEEntry]) -> Generator[Path, None, None]:
    """
    Create a temporary JSON file with CWE data for testing.

    Why this fixture:
        Tests JSON loading separately from CSV loading.
    """
    data = {
        "Weakness_Catalog": {
            "Weaknesses": {
                "Weakness": [
                    {
                        "+@ID": str(entry.cwe_id),
                        "+@Name": entry.name,
                        "Description": entry.description,
                        "Extended_Description": entry.extended_description,
                        "+@Abstraction": entry.abstraction,
                        "+@Status": entry.status,
                        "Applicable_Platforms": {
                            "Technology": [{"+@Name": "AI/ML"}] if entry.is_ai_tagged else [],
                        },
                    }
                    for entry in sample_cwe_entries
                ]
            }
        }
    }

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
    ) as f:
        json.dump(data, f)
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    temp_path.unlink(missing_ok=True)


@pytest.fixture
def temp_output_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory for test outputs.

    Why this fixture:
        Export tests need a directory to write to. Using temp ensures
        no test artifacts remain after tests complete.
    """
    import tempfile
    import shutil

    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)
