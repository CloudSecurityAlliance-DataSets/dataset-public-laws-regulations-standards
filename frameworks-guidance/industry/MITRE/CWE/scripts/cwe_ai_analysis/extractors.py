"""
Extraction and search functions for CWE data.

This module provides functions to filter and search CWE entries based on
various criteria, particularly focused on identifying AI-relevant CWEs.

Extraction Strategies:
    1. AI Tag Extraction: Find CWEs that MITRE has already tagged as AI/ML
    2. Keyword Search: Find CWEs containing AI-related terms
    3. Exclusion Filtering: Remove CWEs focused on legacy/irrelevant tech

Why these strategies:
    - MITRE has started tagging some CWEs as AI/ML relevant. These are our
      "ground truth" - if MITRE says it's AI-relevant, we trust that.
    - Keyword search finds candidates that might not be tagged but are relevant.
    - Exclusion filtering helps reduce false positives from generic searches.
"""

import logging
import re
from typing import Optional

from cwe_ai_analysis.models import CWEEntry

logger = logging.getLogger(__name__)


# Keywords that suggest AI relevance
# Why these keywords: They cover the main AI/ML terminology plus attack types.
# Organized by category for maintainability.
AI_INCLUDE_KEYWORDS = {
    # Direct AI/ML terms
    "ai_terms": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "neural network",
        "large language model",
        "llm",
        "generative ai",
        "ai/ml",
        "ml model",
    ],
    # Model-related terms
    "model_terms": [
        "model training",
        "model inference",
        "model extraction",
        "model inversion",
        "training data",
        "inference",
        "embedding",
        "vector database",
    ],
    # Attack-specific terms
    "attack_terms": [
        "prompt injection",
        "adversarial",
        "data poisoning",
        "model poisoning",
        "jailbreak",
    ],
    # AI system terms
    "system_terms": [
        "autonomous",
        "chatbot",
        "agent",
        "nlp",
        "natural language",
    ],
}

# Keywords that suggest the CWE is NOT relevant to AI
# Why these exclusions: These indicate highly specialized legacy tech that
# is unlikely to be relevant to modern AI systems.
AI_EXCLUDE_KEYWORDS = [
    # Legacy web technologies
    "j2ee",
    "asp.net",
    "coldfusion",
    "struts",
    # Legacy protocols/systems
    "cobol",
    "fortran",
    "mainframe",
    # Very specific non-AI domains (unless part of larger context)
    "voip",  # Voice over IP
    "scada",  # Industrial control (though IoT AI might touch this)
]


def extract_ai_tagged(entries: list[CWEEntry]) -> list[CWEEntry]:
    """
    Extract CWEs that MITRE has tagged as AI/ML relevant.

    MITRE tags AI-relevant CWEs by including "AI/ML" in the
    Applicable Platforms field. This is the most reliable indicator
    of AI relevance since it's MITRE's own assessment.

    Why this is important:
        These CWEs are officially recognized by MITRE as AI-relevant.
        They should be prioritized in our analysis and typically receive
        higher View 1 scores.

    Args:
        entries: List of CWEEntry objects to filter.

    Returns:
        List of CWEEntry objects that have the AI/ML tag.
    """
    ai_tagged = [e for e in entries if e.is_ai_tagged]
    logger.info(f"Found {len(ai_tagged)} CWEs with MITRE AI/ML tag")
    return ai_tagged


def search_keywords(
    entries: list[CWEEntry],
    include_keywords: Optional[list[str]] = None,
    exclude_keywords: Optional[list[str]] = None,
    search_fields: Optional[list[str]] = None,
    case_sensitive: bool = False,
) -> list[CWEEntry]:
    """
    Search CWEs for entries containing specified keywords.

    This function searches multiple text fields in each CWE entry
    and returns entries that match at least one include keyword
    and none of the exclude keywords.

    Why keyword search:
        Not all AI-relevant CWEs are tagged by MITRE. Keyword search
        finds candidates that might be relevant based on their content.
        However, this is a heuristic and may have false positives.

    Args:
        entries: List of CWEEntry objects to search.
        include_keywords: Keywords to search for. If None, uses defaults.
        exclude_keywords: Keywords that disqualify a match. If None, uses defaults.
        search_fields: Which fields to search. Default: name, description,
                      extended_description, applicable_platforms.
        case_sensitive: Whether to do case-sensitive matching.

    Returns:
        List of CWEEntry objects matching the criteria.
    """
    # Use default keywords if not provided
    if include_keywords is None:
        # Flatten the categorized keywords into a single list
        include_keywords = []
        for category_keywords in AI_INCLUDE_KEYWORDS.values():
            include_keywords.extend(category_keywords)

    if exclude_keywords is None:
        exclude_keywords = AI_EXCLUDE_KEYWORDS

    if search_fields is None:
        search_fields = [
            "name",
            "description",
            "extended_description",
            "applicable_platforms",
        ]

    # Prepare patterns for matching
    # Why regex: Allows matching whole words and handles word boundaries
    flags = 0 if case_sensitive else re.IGNORECASE

    def matches_any_keyword(text: str, keywords: list[str]) -> bool:
        """Check if text contains any of the keywords."""
        for keyword in keywords:
            # Use word boundary matching for more precise matches
            # Why: Prevents "model" from matching "remodel"
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, text, flags):
                return True
        return False

    matching_entries = []
    for entry in entries:
        # Combine all search fields into one text block
        # Why combine: Simpler matching logic, and we don't care which field matched
        search_text = " ".join(
            getattr(entry, field, "") for field in search_fields
        )

        # Check for exclude keywords first (faster rejection)
        if exclude_keywords and matches_any_keyword(search_text, exclude_keywords):
            # Check if it's ONLY about the excluded tech, not just mentioning it
            # Why this nuance: A CWE might mention J2EE as an example but be
            # generally applicable. We only exclude if it's primarily about that tech.
            if entry.name and matches_any_keyword(entry.name, exclude_keywords):
                continue  # Skip - the name indicates it's specific to excluded tech

        # Check for include keywords
        if matches_any_keyword(search_text, include_keywords):
            matching_entries.append(entry)

    logger.info(
        f"Keyword search found {len(matching_entries)} matches "
        f"(from {len(entries)} entries)"
    )
    return matching_entries


def search_by_cwe_ids(
    entries: list[CWEEntry],
    cwe_ids: list[int],
) -> list[CWEEntry]:
    """
    Filter CWE entries by specific CWE IDs.

    Why this function:
        Sometimes we want to look at specific CWEs (e.g., from a known list
        like the CWE Top 25). This provides a simple way to filter.

    Args:
        entries: List of CWEEntry objects.
        cwe_ids: List of CWE IDs to include.

    Returns:
        List of CWEEntry objects with matching IDs.
    """
    id_set = set(cwe_ids)
    return [e for e in entries if e.cwe_id in id_set]


def get_potential_ai_candidates(
    entries: list[CWEEntry],
) -> tuple[list[CWEEntry], list[CWEEntry], list[CWEEntry]]:
    """
    Categorize CWEs into different levels of AI relevance likelihood.

    This function combines multiple strategies to identify AI-relevant CWEs
    and categorizes them by confidence level.

    Why three categories:
        - High confidence: MITRE-tagged, definitely relevant
        - Medium confidence: Keyword matches, likely relevant
        - Low confidence: Everything else, needs manual review

    Args:
        entries: All CWE entries to categorize.

    Returns:
        Tuple of (high_confidence, medium_confidence, remaining) lists.

    Example:
        >>> high, medium, remaining = get_potential_ai_candidates(all_cwes)
        >>> print(f"High confidence: {len(high)}")
        >>> print(f"Need review: {len(medium)}")
    """
    # High confidence: MITRE-tagged
    high_confidence = extract_ai_tagged(entries)
    high_ids = {e.cwe_id for e in high_confidence}

    # Remaining entries (not MITRE-tagged)
    non_tagged = [e for e in entries if e.cwe_id not in high_ids]

    # Medium confidence: Keyword matches (excluding already tagged)
    medium_confidence = search_keywords(non_tagged)
    medium_ids = {e.cwe_id for e in medium_confidence}

    # Low confidence: Everything else
    remaining = [e for e in non_tagged if e.cwe_id not in medium_ids]

    logger.info(
        f"Categorized {len(entries)} CWEs: "
        f"{len(high_confidence)} high confidence, "
        f"{len(medium_confidence)} medium confidence, "
        f"{len(remaining)} remaining"
    )

    return high_confidence, medium_confidence, remaining


def get_attack_surface_candidates(entries: list[CWEEntry]) -> list[CWEEntry]:
    """
    Find CWEs that represent potential AI attack surfaces.

    These are weaknesses that, while not AI-specific, become significant
    attack vectors when AI systems use them. For example:
    - Command injection (AI agents executing commands)
    - SSRF (AI fetching external URLs)
    - Deserialization (loading AI models)

    Why this function:
        View 2 (Attacks VIA AI) needs to identify weaknesses that attackers
        would specifically want AI to trigger. This function finds those
        candidates based on the attack type.

    Args:
        entries: List of CWE entries to search.

    Returns:
        List of CWEs that are potential AI attack surfaces.
    """
    # Keywords indicating attack vectors that AI might execute
    attack_surface_keywords = [
        # Injection attacks (AI generates/executes)
        "command injection",
        "os command",
        "code injection",
        "sql injection",
        "script injection",
        "expression injection",
        # Request-based attacks (AI makes requests)
        "server-side request forgery",
        "ssrf",
        "url redirection",
        # File operations (AI reads/writes)
        "path traversal",
        "file inclusion",
        "unrestricted upload",
        # Output-based attacks (AI generates malicious output)
        "cross-site scripting",
        "xss",
        "cross-site request forgery",
        "csrf",
        "html injection",
        # Data handling (AI processes/leaks)
        "information exposure",
        "sensitive data",
        "deserialization",
    ]

    return search_keywords(
        entries,
        include_keywords=attack_surface_keywords,
        exclude_keywords=[],  # Don't exclude anything for attack surface analysis
    )
