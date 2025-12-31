"""
Data models for CWE AI Analysis.

This module defines the core data structures used throughout the library.
We use Pydantic models for:
1. Automatic validation - catch malformed data early
2. Serialization - easy conversion to/from JSON, dict
3. Documentation - the model IS the schema documentation

Why Pydantic over dataclasses:
    While dataclasses are built-in, Pydantic provides validation out of the box.
    Given that we're processing external CWE data that might have inconsistencies,
    validation is valuable. Pydantic also provides better JSON serialization.

The Two-View Model:
    We classify each CWE on two independent dimensions:
    - View 1 (Attacks ON AI): Can this weakness attack AI systems?
    - View 2 (Attacks VIA AI): Would attackers want AI to cause this weakness?

    This captures the distinction between AI as target vs AI as weapon.
    See CWE-AI-METHODOLOGY.md for full rationale.
"""

from enum import Enum, IntEnum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ViewScore(IntEnum):
    """
    Scoring scale for View 1 and View 2 relevance (0-4).

    Why 0-4 instead of 1-5:
        A score of 0 clearly means "not applicable" - there's no ambiguity.
        With a 1-5 scale, a score of 1 could mean "slightly applicable" or
        "not really applicable", which is confusing. Starting at 0 makes
        the semantics clearer.

    Score Definitions:
        0 - NOT_APPLICABLE: This view does not apply to this CWE at all
        1 - WEAKLY_APPLICABLE: Edge cases only, very indirect relevance
        2 - MODERATELY_APPLICABLE: Relevant but not a primary concern
        3 - HIGHLY_APPLICABLE: Significant AI relevance
        4 - PRIMARY_EXAMPLE: This is exactly what the view describes
    """

    NOT_APPLICABLE = 0
    WEAKLY_APPLICABLE = 1
    MODERATELY_APPLICABLE = 2
    HIGHLY_APPLICABLE = 3
    PRIMARY_EXAMPLE = 4


class AICategory(str, Enum):
    """
    Categories of AI relevance for classification.

    Why these categories:
        These emerged from analyzing how CWEs relate to AI security.
        They cover the main attack surfaces and concerns in AI systems.

    Categories explained:
        - PROMPT_INJECTION: Attacks that manipulate LLM prompts
        - MODEL_SECURITY: Extraction, inversion, theft of models
        - TRAINING_DATA: Poisoning, leakage of training data
        - OUTPUT_VALIDATION: Unsafe/unvalidated AI outputs
        - INFERENCE_SECURITY: Side channels, resource exhaustion during inference
        - AGENT_AUTONOMY: Risks from AI agents taking autonomous actions
        - SUPPLY_CHAIN: Malicious models, compromised dependencies
        - INFRASTRUCTURE: General infrastructure weaknesses affecting AI systems
        - GENERAL: Broadly applicable but not AI-specific
        - NOT_APPLICABLE: Not relevant to AI
    """

    PROMPT_INJECTION = "Prompt Injection"
    MODEL_SECURITY = "Model Security"
    TRAINING_DATA = "Training Data"
    OUTPUT_VALIDATION = "Output Validation"
    INFERENCE_SECURITY = "Inference Security"
    AGENT_AUTONOMY = "Agent/Autonomous Systems"
    SUPPLY_CHAIN = "Supply Chain"
    INFRASTRUCTURE = "Infrastructure"
    GENERAL = "General"
    NOT_APPLICABLE = "Not Applicable"


class AttackType(str, Enum):
    """
    Type of attack for View 2 classification.

    Why this distinction:
        View 2 (Attacks VIA AI) encompasses two different attack patterns:
        - Direct: Attacker interacts with AI, AI produces attack immediately
        - Indirect: Attacker poisons AI knowledge, victim gets vulnerable output later

        Direct attacks score higher because the AI output IS the attack.
        Indirect attacks are scored based on impact (supply chain = high, minor vuln = low).

    See CWE-AI-METHODOLOGY.md for full explanation.
    """

    DIRECT = "Direct"
    INDIRECT = "Indirect"
    BOTH = "Both"
    NOT_APPLICABLE = "N/A"


class AttackSurface(str, Enum):
    """
    Which attack surface this CWE primarily targets.

    The Four Attack Surfaces:
        - INFRASTRUCTURE: Traditional servers, APIs, databases hosting AI
        - AI_CORE: The model itself, prompts, inference pipeline
        - AI_OUTPUTS: Code, configs, actions that AI produces
        - SUPPLY_CHAIN: Training data, web search, integrations, dependencies

    Why this matters:
        - Infrastructure attacks are well-covered by existing CWEs
        - AI Core attacks are novel and poorly covered
        - AI Output attacks use traditional CWEs but AI is the vector
        - Supply Chain varies by trust boundary

    See AI-ATTACK-SURFACE-MODEL.md for full details.
    """

    INFRASTRUCTURE = "Infrastructure"
    AI_CORE = "AI Core"
    AI_OUTPUTS = "AI Outputs"
    SUPPLY_CHAIN = "Supply Chain"
    MULTIPLE = "Multiple"
    NOT_APPLICABLE = "N/A"


class CWEEntry(BaseModel):
    """
    Represents a single CWE entry loaded from MITRE data.

    This model captures the essential fields from CWE data files.
    Not all CWE fields are included - only those relevant for AI analysis.

    Why these fields:
        - cwe_id, name, description: Core identification
        - extended_description: More context for classification
        - applicable_platforms: Contains the AI/ML tag we look for
        - abstraction: Helps understand if this is a high-level or specific weakness
        - status: Draft/Incomplete entries might need different handling

    The raw CWE CSV has many more fields (related weaknesses, mitigations, etc.)
    but they're not needed for AI relevance classification.
    """

    cwe_id: int = Field(
        ...,
        ge=1,
        description="CWE identifier (e.g., 79 for XSS)",
        json_schema_extra={"examples": [79, 89, 1427]},
    )
    name: str = Field(
        ...,
        min_length=1,
        description="Short name of the weakness",
        json_schema_extra={"examples": ["Cross-site Scripting (XSS)"]},
    )
    description: str = Field(
        default="",
        description="Brief description of the weakness",
    )
    extended_description: str = Field(
        default="",
        description="Detailed description with more context",
    )
    applicable_platforms: str = Field(
        default="",
        description="Languages, technologies, architectures where this applies",
    )
    abstraction: str = Field(
        default="",
        description="Abstraction level: Pillar, Class, Base, Variant",
    )
    status: str = Field(
        default="",
        description="CWE status: Draft, Incomplete, Stable, etc.",
    )
    related_weaknesses: str = Field(
        default="",
        description="Parent/child and related CWE relationships",
    )
    common_consequences: str = Field(
        default="",
        description="Impact if this weakness is exploited",
    )
    potential_mitigations: str = Field(
        default="",
        description="How to prevent or fix this weakness",
    )

    # Source tracking - which CWE view this came from
    source_view: str = Field(
        default="",
        description="Source view: Research-Concepts-1000, Software-Development-699, Hardware-Design-1194",
    )

    @property
    def is_ai_tagged(self) -> bool:
        """
        Check if MITRE has tagged this CWE as AI/ML relevant.

        Why a property:
            This is derived from applicable_platforms but is frequently needed.
            Making it a property provides a clean API without storing redundant data.

        Returns:
            True if "AI/ML" appears in the applicable platforms field.
        """
        return "AI/ML" in self.applicable_platforms

    @property
    def full_description(self) -> str:
        """
        Get the complete description (description + extended_description).

        Why combine:
            For classification, we want to consider all available text.
            Some CWEs have brief descriptions but detailed extended descriptions.
        """
        parts = [self.description]
        if self.extended_description:
            parts.append(self.extended_description)
        return " ".join(parts)

    def __str__(self) -> str:
        return f"CWE-{self.cwe_id}: {self.name}"


class CWEClassification(BaseModel):
    """
    The result of classifying a CWE for AI relevance.

    This is the primary output model - it contains the original CWE info
    plus our two-view classification scores and reasoning.

    Two-View Model Recap:
        - View 1 (Attacks ON AI): Measures whether this weakness can be used
          to attack, compromise, or manipulate AI systems. High scores mean
          this is a significant threat TO AI systems.

        - View 2 (Attacks VIA AI): Measures whether attackers would want AI
          to produce or execute this weakness. High scores mean this is
          something attackers specifically want AI to do because the AI output
          IS the attack (like generating XSS).

    Why separate scores and reasoning:
        Scores enable filtering and sorting (e.g., "show me all View 1 >= 3")
        Reasoning explains WHY that score, which is essential for:
        - Validating classifications
        - Understanding edge cases
        - Updating classifications as AI evolves
    """

    # Core CWE identification
    cwe_id: int = Field(..., ge=1, description="CWE identifier")
    name: str = Field(..., description="CWE name")
    description: str = Field(default="", description="CWE description")

    # MITRE's own AI tagging
    mitre_ai_tagged: bool = Field(
        default=False,
        description="Whether MITRE has tagged this as AI/ML applicable",
    )

    # View 1: Attacks ON AI
    view1_score: ViewScore = Field(
        default=ViewScore.NOT_APPLICABLE,
        description="Score for 'Attacks ON AI' (0-4)",
    )
    view1_reasoning: str = Field(
        default="",
        description="Explanation for View 1 score",
    )

    # View 2: Attacks VIA AI
    view2_score: ViewScore = Field(
        default=ViewScore.NOT_APPLICABLE,
        description="Score for 'Attacks VIA AI' (0-4)",
    )
    view2_reasoning: str = Field(
        default="",
        description="Explanation for View 2 score",
    )

    # Category and impact
    ai_category: AICategory = Field(
        default=AICategory.NOT_APPLICABLE,
        description="Primary AI relevance category",
    )
    ai_impact: str = Field(
        default="",
        description="Potential impact if exploited in AI context",
    )

    # Attack characterization (from updated methodology)
    attack_type: AttackType = Field(
        default=AttackType.NOT_APPLICABLE,
        description="Direct (AI output IS attack) vs Indirect (AI distributes vuln)",
    )
    attack_surface: AttackSurface = Field(
        default=AttackSurface.NOT_APPLICABLE,
        description="Which attack surface: Infrastructure, AI Core, AI Outputs, Supply Chain",
    )

    # Source tracking
    source_view: str = Field(
        default="",
        description="Which CWE view this came from",
    )

    @property
    def max_score(self) -> ViewScore:
        """
        Get the maximum score across both views.

        Why this property:
            Useful for filtering "any AI relevance" without specifying which view.
            A CWE with View1=0, View2=4 should still be considered AI-relevant.
        """
        return ViewScore(max(self.view1_score, self.view2_score))

    @property
    def is_ai_relevant(self) -> bool:
        """
        Check if this CWE has any significant AI relevance.

        Threshold: Score >= 2 on either view is considered relevant.

        Why >= 2:
            Score 1 is "weakly applicable / edge cases only"
            Score 2+ indicates meaningful AI relevance worth noting
        """
        return self.max_score >= ViewScore.MODERATELY_APPLICABLE

    @property
    def is_highly_ai_relevant(self) -> bool:
        """
        Check if this CWE is highly relevant to AI security.

        Threshold: Score >= 3 on either view.

        Why >= 3:
            These are the CWEs that should be prioritized for AI security work.
            Score 3-4 indicates significant or primary AI relevance.
        """
        return self.max_score >= ViewScore.HIGHLY_APPLICABLE

    def to_csv_row(self) -> dict:
        """
        Convert to a flat dictionary suitable for CSV export.

        Why this method:
            CSV export needs flat key-value pairs. This method handles
            the conversion from nested/enum types to strings.
        """
        return {
            "CWE_ID": self.cwe_id,
            "Name": self.name,
            "Description": self.description[:500] if self.description else "",  # Truncate for CSV
            "MITRE_AI_Tagged": "Yes" if self.mitre_ai_tagged else "No",
            "View1_Score": self.view1_score.value,
            "View1_Reasoning": self.view1_reasoning,
            "View2_Score": self.view2_score.value,
            "View2_Reasoning": self.view2_reasoning,
            "AI_Category": self.ai_category.value,
            "AI_Impact": self.ai_impact,
            "Attack_Type": self.attack_type.value,
            "Attack_Surface": self.attack_surface.value,
            "Source_View": self.source_view,
            "Max_Score": self.max_score.value,
            "Is_AI_Relevant": "Yes" if self.is_ai_relevant else "No",
        }

    def __str__(self) -> str:
        return (
            f"CWE-{self.cwe_id}: {self.name} "
            f"[View1={self.view1_score.value}, View2={self.view2_score.value}]"
        )


class ClassificationSummary(BaseModel):
    """
    Summary statistics for a set of CWE classifications.

    Why this model:
        After classifying all CWEs, we want aggregate statistics.
        This model structures that data for reporting.
    """

    total_cwes: int = Field(..., description="Total number of CWEs processed")
    mitre_ai_tagged_count: int = Field(
        ..., description="CWEs with MITRE AI/ML tag"
    )

    # View 1 distribution
    view1_score_counts: dict[int, int] = Field(
        default_factory=dict,
        description="Count of CWEs at each View 1 score level",
    )

    # View 2 distribution
    view2_score_counts: dict[int, int] = Field(
        default_factory=dict,
        description="Count of CWEs at each View 2 score level",
    )

    # Category distribution
    category_counts: dict[str, int] = Field(
        default_factory=dict,
        description="Count of CWEs in each AI category",
    )

    # Relevance counts
    ai_relevant_count: int = Field(
        ..., description="CWEs with max score >= 2"
    )
    highly_ai_relevant_count: int = Field(
        ..., description="CWEs with max score >= 3"
    )

    # Source view breakdown
    source_view_counts: dict[str, int] = Field(
        default_factory=dict,
        description="Count of CWEs from each source view",
    )

    @classmethod
    def from_classifications(
        cls, classifications: list[CWEClassification]
    ) -> "ClassificationSummary":
        """
        Create a summary from a list of classifications.

        Why a classmethod:
            This is the natural way to construct a summary - from the data.
            It encapsulates all the aggregation logic in one place.
        """
        view1_counts: dict[int, int] = {i: 0 for i in range(5)}
        view2_counts: dict[int, int] = {i: 0 for i in range(5)}
        category_counts: dict[str, int] = {}
        source_counts: dict[str, int] = {}

        mitre_tagged = 0
        ai_relevant = 0
        highly_relevant = 0

        for c in classifications:
            # Score distributions
            view1_counts[c.view1_score.value] += 1
            view2_counts[c.view2_score.value] += 1

            # Category counts
            cat = c.ai_category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1

            # Source view counts
            if c.source_view:
                source_counts[c.source_view] = source_counts.get(c.source_view, 0) + 1

            # Flags
            if c.mitre_ai_tagged:
                mitre_tagged += 1
            if c.is_ai_relevant:
                ai_relevant += 1
            if c.is_highly_ai_relevant:
                highly_relevant += 1

        return cls(
            total_cwes=len(classifications),
            mitre_ai_tagged_count=mitre_tagged,
            view1_score_counts=view1_counts,
            view2_score_counts=view2_counts,
            category_counts=category_counts,
            ai_relevant_count=ai_relevant,
            highly_ai_relevant_count=highly_relevant,
            source_view_counts=source_counts,
        )
