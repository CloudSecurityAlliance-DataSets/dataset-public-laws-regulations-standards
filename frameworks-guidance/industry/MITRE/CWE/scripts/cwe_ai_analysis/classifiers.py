"""
Classification logic for CWE AI relevance analysis.

This module implements the two-view classification model for determining
how each CWE relates to AI security.

The Two-View Model:
    View 1 (Attacks ON AI): Can this weakness be used to attack AI systems?
    View 2 (Attacks VIA AI): Would attackers want AI to produce this weakness?

Why Two Views:
    We initially tried a single relevance score, but this conflated different
    types of AI relevance. For example, XSS scores low for attacking AI (View 1)
    but high for AI-generated attacks (View 2). The two-view model captures
    this nuance.

Classification Approach:
    This module provides rule-based classification using patterns and keywords.
    For full classification of all ~1000+ CWEs, AI-assisted review is recommended.
    The rules here handle the clear-cut cases and provide defaults for others.

See CWE-AI-METHODOLOGY.md for complete methodology documentation.
"""

import json
import logging
import re
from pathlib import Path
from typing import Callable, Optional

from tqdm import tqdm

from cwe_ai_analysis.models import (
    AICategory,
    AttackSurface,
    AttackType,
    CWEClassification,
    CWEEntry,
    ViewScore,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Known Classifications
# =============================================================================
# These are CWEs with well-understood AI relevance that we can classify
# automatically with high confidence. The classifications are based on
# our methodology document and expert analysis.

# Why maintain this list:
# 1. Provides consistent classification for important CWEs
# 2. Serves as training examples for understanding the model
# 3. Speeds up processing by avoiding re-analysis of known cases

KNOWN_CLASSIFICATIONS: dict[int, dict] = {
    # AI-Specific CWEs (View 1 = 4)
    # These are CWEs explicitly designed for or about AI/ML systems
    1427: {
        "view1_score": ViewScore.PRIMARY_EXAMPLE,
        "view1_reasoning": (
            "Canonical attack ON LLMs - directly targets prompt processing to "
            "manipulate model behavior, extract information, or bypass safety controls."
        ),
        "view2_score": ViewScore.HIGHLY_APPLICABLE,
        "view2_reasoning": (
            "Prompt injection is often the mechanism used to trick AI into executing "
            "View 2 attacks (command injection, data exfiltration, etc.)."
        ),
        "ai_category": AICategory.PROMPT_INJECTION,
        "ai_impact": (
            "Full control over model output, safety bypass, potential code execution, "
            "data exfiltration, and reputation damage."
        ),
    },
    1426: {
        "view1_score": ViewScore.MODERATELY_APPLICABLE,
        "view1_reasoning": (
            "This is a defensive weakness - failure to validate AI output. "
            "Not an attack ON AI, but a failure in AI system design."
        ),
        "view2_score": ViewScore.PRIMARY_EXAMPLE,
        "view2_reasoning": (
            "This IS the View 2 problem - AI generates unsafe output that should "
            "have been validated. Direct enabler of all AI-generated attacks."
        ),
        "ai_category": AICategory.OUTPUT_VALIDATION,
        "ai_impact": (
            "AI-generated XSS, command injection, malicious code, harmful content, "
            "and other unsafe outputs reach end users or systems."
        ),
    },
    1039: {
        "view1_score": ViewScore.PRIMARY_EXAMPLE,
        "view1_reasoning": (
            "Directly describes attacks ON ML recognition systems using adversarial "
            "inputs designed to cause misclassification."
        ),
        "view2_score": ViewScore.NOT_APPLICABLE,
        "view2_reasoning": "This is an attack ON AI, not something AI would produce.",
        "ai_category": AICategory.MODEL_SECURITY,
        "ai_impact": (
            "Misclassification leading to safety failures (e.g., self-driving cars), "
            "authentication bypass, or content filter evasion."
        ),
    },
    1434: {
        "view1_score": ViewScore.PRIMARY_EXAMPLE,
        "view1_reasoning": (
            "Directly about insecure configuration of AI model inference parameters. "
            "Attackers can exploit misconfigured temperature, top_k, etc."
        ),
        "view2_score": ViewScore.WEAKLY_APPLICABLE,
        "view2_reasoning": (
            "Insecure parameters might make AI more likely to produce unsafe outputs, "
            "but this is indirect."
        ),
        "ai_category": AICategory.INFERENCE_SECURITY,
        "ai_impact": (
            "Model behavior manipulation, increased likelihood of unsafe outputs, "
            "resource exhaustion, or quality degradation."
        ),
    },

    # High View 2 - Attack Outputs (things attackers want AI to do)
    79: {
        "view1_score": ViewScore.WEAKLY_APPLICABLE,
        "view1_reasoning": (
            "XSS could affect web interfaces of AI systems, but this is not "
            "specific to AI - it's a general web vulnerability."
        ),
        "view2_score": ViewScore.HIGHLY_APPLICABLE,
        "view2_reasoning": (
            "Classic target for AI-generated attacks. Attackers want AI to generate "
            "HTML/JS containing XSS payloads that execute in user browsers."
        ),
        "ai_category": AICategory.OUTPUT_VALIDATION,
        "ai_impact": (
            "Session hijacking, credential theft, malware distribution via "
            "AI-generated web content."
        ),
    },
    89: {
        "view1_score": ViewScore.WEAKLY_APPLICABLE,
        "view1_reasoning": (
            "SQL injection could affect AI systems using databases, but this is "
            "not AI-specific."
        ),
        "view2_score": ViewScore.HIGHLY_APPLICABLE,
        "view2_reasoning": (
            "Attackers want AI to generate SQL queries containing injection payloads. "
            "AI output IS the attack when generating database queries."
        ),
        "ai_category": AICategory.OUTPUT_VALIDATION,
        "ai_impact": (
            "Database breach, data exfiltration, data manipulation via "
            "AI-generated queries."
        ),
    },
    78: {
        "view1_score": ViewScore.MODERATELY_APPLICABLE,
        "view1_reasoning": (
            "Command injection could target AI infrastructure, but primary AI "
            "relevance is as an attack AI might execute."
        ),
        "view2_score": ViewScore.PRIMARY_EXAMPLE,
        "view2_reasoning": (
            "Primary target for AI agent attacks. Attackers trick AI into executing "
            "shell commands - the AI action IS the attack."
        ),
        "ai_category": AICategory.AGENT_AUTONOMY,
        "ai_impact": (
            "Full system compromise, lateral movement, data destruction via "
            "AI-executed commands."
        ),
    },
    77: {
        "view1_score": ViewScore.MODERATELY_APPLICABLE,
        "view1_reasoning": "Similar to OS command injection but more general.",
        "view2_score": ViewScore.PRIMARY_EXAMPLE,
        "view2_reasoning": (
            "Attackers want AI to generate command strings that get executed. "
            "The AI-generated command IS the attack payload."
        ),
        "ai_category": AICategory.AGENT_AUTONOMY,
        "ai_impact": "System compromise via AI-generated command execution.",
    },
    918: {
        "view1_score": ViewScore.MODERATELY_APPLICABLE,
        "view1_reasoning": (
            "SSRF could be used to attack AI infrastructure or internal services "
            "that AI systems depend on."
        ),
        "view2_score": ViewScore.PRIMARY_EXAMPLE,
        "view2_reasoning": (
            "Critical for AI agents. Attackers want AI to make requests to internal "
            "URLs - the AI request IS the attack."
        ),
        "ai_category": AICategory.AGENT_AUTONOMY,
        "ai_impact": (
            "Internal network scanning, cloud metadata theft, internal service "
            "exploitation via AI-initiated requests."
        ),
    },
    352: {
        "view1_score": ViewScore.WEAKLY_APPLICABLE,
        "view1_reasoning": "CSRF could affect AI system web interfaces, not AI-specific.",
        "view2_score": ViewScore.HIGHLY_APPLICABLE,
        "view2_reasoning": (
            "Attackers want AI to generate HTML forms or links that perform "
            "unwanted actions when users interact with them."
        ),
        "ai_category": AICategory.OUTPUT_VALIDATION,
        "ai_impact": (
            "Unauthorized actions on behalf of users via AI-generated malicious "
            "forms or links."
        ),
    },

    # High View 1 - Attacks ON AI Infrastructure
    502: {
        "view1_score": ViewScore.PRIMARY_EXAMPLE,
        "view1_reasoning": (
            "Critical for AI systems. Malicious model files (pickle) can execute "
            "code when deserialized. Major vector for model supply chain attacks."
        ),
        "view2_score": ViewScore.WEAKLY_APPLICABLE,
        "view2_reasoning": (
            "AI could potentially generate serialized data, but this is uncommon "
            "and indirect."
        ),
        "ai_category": AICategory.SUPPLY_CHAIN,
        "ai_impact": (
            "Remote code execution when loading malicious models from untrusted "
            "sources (HuggingFace, model registries)."
        ),
    },
    22: {
        "view1_score": ViewScore.HIGHLY_APPLICABLE,
        "view1_reasoning": (
            "Path traversal can access model files, training data, configuration. "
            "Tagged by MITRE as AI/ML applicable."
        ),
        "view2_score": ViewScore.HIGHLY_APPLICABLE,
        "view2_reasoning": (
            "AI agents with file access can be tricked into reading/writing "
            "arbitrary paths. The AI file operation IS the attack."
        ),
        "ai_category": AICategory.INFRASTRUCTURE,
        "ai_impact": (
            "Model theft, training data exposure, configuration manipulation, "
            "or system file access via AI."
        ),
    },

    # General but AI-Applicable
    200: {
        "view1_score": ViewScore.HIGHLY_APPLICABLE,
        "view1_reasoning": (
            "Information exposure can leak model architecture, training data, "
            "prompts, or inference details."
        ),
        "view2_score": ViewScore.HIGHLY_APPLICABLE,
        "view2_reasoning": (
            "Attackers want AI to leak sensitive information in its outputs - "
            "PII, credentials, internal data."
        ),
        "ai_category": AICategory.GENERAL,
        "ai_impact": (
            "Exposure of model IP, training data, user data, or system "
            "information via AI outputs or errors."
        ),
    },
    287: {
        "view1_score": ViewScore.MODERATELY_APPLICABLE,
        "view1_reasoning": (
            "Authentication weaknesses affect AI API access, model access controls."
        ),
        "view2_score": ViewScore.MODERATELY_APPLICABLE,
        "view2_reasoning": (
            "AI could potentially be tricked into bypassing authentication "
            "or exposing credentials."
        ),
        "ai_category": AICategory.INFRASTRUCTURE,
        "ai_impact": "Unauthorized access to AI systems or resources.",
    },
    862: {
        "view1_score": ViewScore.HIGHLY_APPLICABLE,
        "view1_reasoning": (
            "Missing authorization in AI systems can allow unauthorized model "
            "access, training data access, or inference. MITRE AI/ML tagged."
        ),
        "view2_score": ViewScore.MODERATELY_APPLICABLE,
        "view2_reasoning": (
            "AI agents might perform actions without proper authorization checks."
        ),
        "ai_category": AICategory.INFRASTRUCTURE,
        "ai_impact": (
            "Unauthorized access to models, data, or AI system functionality."
        ),
    },
    601: {
        "view1_score": ViewScore.WEAKLY_APPLICABLE,
        "view1_reasoning": (
            "Open redirect could affect AI web interfaces, but this is a general "
            "web vulnerability not specific to AI systems."
        ),
        "view2_score": ViewScore.MODERATELY_APPLICABLE,
        "view2_reasoning": (
            "AI could generate URLs containing redirect payloads, but this is "
            "primarily a phishing enabler requiring user interaction - not a "
            "direct attack where the AI output IS the attack payload."
        ),
        "ai_category": AICategory.OUTPUT_VALIDATION,
        "ai_impact": (
            "Phishing attacks via AI-generated redirect URLs, but requires "
            "victim interaction to exploit."
        ),
    },
    # Lowered from Score 3 - not direct attack outputs
    393: {
        "view1_score": ViewScore.NOT_APPLICABLE,
        "view1_reasoning": "Status code errors are logic issues, not AI-specific.",
        "view2_score": ViewScore.WEAKLY_APPLICABLE,
        "view2_reasoning": (
            "AI could generate incorrect status codes, but this is a logic error "
            "not an attack payload."
        ),
        "ai_category": AICategory.NOT_APPLICABLE,
        "ai_impact": "",
    },
    691: {
        "view1_score": ViewScore.NOT_APPLICABLE,
        "view1_reasoning": "Too generic to be AI-relevant.",
        "view2_score": ViewScore.WEAKLY_APPLICABLE,
        "view2_reasoning": (
            "AI-generated code could have control flow issues, but this is too "
            "generic to be a primary concern."
        ),
        "ai_category": AICategory.NOT_APPLICABLE,
        "ai_impact": "",
    },
    1164: {
        "view1_score": ViewScore.NOT_APPLICABLE,
        "view1_reasoning": "Dead/irrelevant code is not an attack vector.",
        "view2_score": ViewScore.NOT_APPLICABLE,
        "view2_reasoning": (
            "AI generating dead code is a quality issue, not a security attack."
        ),
        "ai_category": AICategory.NOT_APPLICABLE,
        "ai_impact": "",
    },
    532: {
        "view1_score": ViewScore.MODERATELY_APPLICABLE,
        "view1_reasoning": "AI system logs could expose sensitive model or user data.",
        "view2_score": ViewScore.MODERATELY_APPLICABLE,
        "view2_reasoning": (
            "AI could log sensitive information, but this is data exposure "
            "not an attack payload."
        ),
        "ai_category": AICategory.OUTPUT_VALIDATION,
        "ai_impact": "Sensitive data exposure via AI logging.",
    },
    619: {
        "view1_score": ViewScore.NOT_APPLICABLE,
        "view1_reasoning": "Niche database cursor issue, not AI-specific.",
        "view2_score": ViewScore.WEAKLY_APPLICABLE,
        "view2_reasoning": (
            "AI generating database code could leave cursors open, but this is "
            "a niche issue not a primary attack vector."
        ),
        "ai_category": AICategory.NOT_APPLICABLE,
        "ai_impact": "",
    },
}


# =============================================================================
# Attack Type and Surface Derivation
# =============================================================================
# These helper functions derive attack_type and attack_surface from other
# classification fields. This keeps the logic centralized and avoids
# duplicating these values in every KNOWN_CLASSIFICATIONS entry.


def _determine_attack_type(
    view1_score: ViewScore,
    view2_score: ViewScore,
    ai_category: AICategory,
) -> AttackType:
    """
    Derive attack type from scores and category.

    Logic:
        - Direct: View 2 high + category suggests immediate attack output
        - Indirect: Supply chain or training data poisoning
        - Both: High scores on both views with relevant category
        - N/A: Not relevant to View 2 attacks

    Why derive instead of hardcode:
        This ensures consistency and reduces maintenance burden.
        The attack type is fundamentally determined by HOW the CWE
        relates to AI, which is captured in scores and category.
    """
    # If not AI-relevant at all, N/A
    if view1_score == ViewScore.NOT_APPLICABLE and view2_score == ViewScore.NOT_APPLICABLE:
        return AttackType.NOT_APPLICABLE

    # Supply chain is inherently indirect
    if ai_category == AICategory.SUPPLY_CHAIN:
        # But if View 2 is also high, could be both (e.g., deserialization)
        if view2_score >= ViewScore.HIGHLY_APPLICABLE:
            return AttackType.BOTH
        return AttackType.INDIRECT

    # Training data poisoning is indirect
    if ai_category == AICategory.TRAINING_DATA:
        return AttackType.INDIRECT

    # High View 2 with output-related categories = Direct
    direct_categories = {
        AICategory.OUTPUT_VALIDATION,
        AICategory.AGENT_AUTONOMY,
    }
    if view2_score >= ViewScore.HIGHLY_APPLICABLE and ai_category in direct_categories:
        # If View 1 also high, it's both
        if view1_score >= ViewScore.HIGHLY_APPLICABLE:
            return AttackType.BOTH
        return AttackType.DIRECT

    # High View 1 only = N/A for attack type (it's an attack ON AI, not VIA)
    if view1_score >= ViewScore.MODERATELY_APPLICABLE and view2_score <= ViewScore.WEAKLY_APPLICABLE:
        return AttackType.NOT_APPLICABLE

    # Moderate View 2 could be indirect
    if view2_score >= ViewScore.MODERATELY_APPLICABLE:
        if view1_score >= ViewScore.MODERATELY_APPLICABLE:
            return AttackType.BOTH
        return AttackType.DIRECT

    return AttackType.NOT_APPLICABLE


def _determine_attack_surface(
    view1_score: ViewScore,
    view2_score: ViewScore,
    ai_category: AICategory,
) -> AttackSurface:
    """
    Derive attack surface from scores and category.

    Logic:
        - AI Core: Prompt injection, model security, inference attacks
        - AI Outputs: Output validation, agent actions (View 2 focus)
        - Supply Chain: Supply chain category
        - Infrastructure: Infrastructure category
        - Multiple: High relevance to multiple surfaces

    Why derive instead of hardcode:
        Attack surface is largely determined by the AI category,
        with some nuance based on which view scores higher.
    """
    # If not AI-relevant at all, N/A
    if view1_score == ViewScore.NOT_APPLICABLE and view2_score == ViewScore.NOT_APPLICABLE:
        return AttackSurface.NOT_APPLICABLE

    # Direct mappings from category
    category_to_surface = {
        AICategory.PROMPT_INJECTION: AttackSurface.AI_CORE,
        AICategory.MODEL_SECURITY: AttackSurface.AI_CORE,
        AICategory.INFERENCE_SECURITY: AttackSurface.AI_CORE,
        AICategory.TRAINING_DATA: AttackSurface.SUPPLY_CHAIN,
        AICategory.SUPPLY_CHAIN: AttackSurface.SUPPLY_CHAIN,
        AICategory.INFRASTRUCTURE: AttackSurface.INFRASTRUCTURE,
    }

    if ai_category in category_to_surface:
        base_surface = category_to_surface[ai_category]
        # If both views are high, might be multiple surfaces
        if view1_score >= ViewScore.HIGHLY_APPLICABLE and view2_score >= ViewScore.HIGHLY_APPLICABLE:
            return AttackSurface.MULTIPLE
        return base_surface

    # Output validation and agent autonomy → AI Outputs (View 2 focus)
    if ai_category in {AICategory.OUTPUT_VALIDATION, AICategory.AGENT_AUTONOMY}:
        if view1_score >= ViewScore.HIGHLY_APPLICABLE and view2_score >= ViewScore.HIGHLY_APPLICABLE:
            return AttackSurface.MULTIPLE
        return AttackSurface.AI_OUTPUTS

    # General category - determine by which view is higher
    if ai_category == AICategory.GENERAL:
        if view1_score > view2_score:
            return AttackSurface.INFRASTRUCTURE
        elif view2_score > view1_score:
            return AttackSurface.AI_OUTPUTS
        elif view1_score >= ViewScore.MODERATELY_APPLICABLE:
            return AttackSurface.MULTIPLE
        return AttackSurface.NOT_APPLICABLE

    return AttackSurface.NOT_APPLICABLE


# =============================================================================
# Classification Rules
# =============================================================================
# These rules provide heuristic-based classification for CWEs not in the
# known list. They're based on patterns in CWE names and descriptions.

def _classify_by_rules(entry: CWEEntry) -> CWEClassification:
    """
    Apply rule-based classification to a CWE entry.

    Why rules-based:
        For many CWEs, simple patterns in the name/description indicate
        AI relevance. This handles clear-cut cases automatically.

    This function should be conservative - when in doubt, classify as
    needing manual review rather than making strong claims.
    """
    text = f"{entry.name} {entry.description}".lower()

    # Default scores (will be overridden by rules that match)
    view1_score = ViewScore.NOT_APPLICABLE
    view1_reasoning = "No specific AI relevance identified."
    view2_score = ViewScore.NOT_APPLICABLE
    view2_reasoning = "No specific AI relevance identified."
    ai_category = AICategory.NOT_APPLICABLE
    ai_impact = ""

    # Check if MITRE tagged this as AI/ML
    if entry.is_ai_tagged:
        view1_score = ViewScore.MODERATELY_APPLICABLE
        view1_reasoning = (
            "MITRE has tagged this CWE as applicable to AI/ML systems. "
            "Specific AI impact should be reviewed."
        )
        ai_category = AICategory.GENERAL

    # Rule: Injection-type weaknesses (high View 2)
    injection_patterns = [
        r"injection",
        r"command.*execution",
        r"code.*execution",
        r"eval\b",
        r"script.*execution",
    ]
    if any(re.search(p, text) for p in injection_patterns):
        view2_score = max(view2_score, ViewScore.HIGHLY_APPLICABLE)
        view2_reasoning = (
            "Injection weakness - attackers may want AI to generate payloads "
            "that execute in target systems."
        )
        ai_category = AICategory.OUTPUT_VALIDATION
        ai_impact = "Potential code/command execution via AI-generated output."

    # Rule: File/path operations (both views)
    file_patterns = [
        r"path.*traversal",
        r"file.*inclusion",
        r"directory.*traversal",
        r"file.*upload",
        r"file.*read",
        r"file.*write",
    ]
    if any(re.search(p, text) for p in file_patterns):
        view1_score = max(view1_score, ViewScore.MODERATELY_APPLICABLE)
        view1_reasoning = (
            "File operation weakness could affect AI model files, training data, "
            "or configuration."
        )
        view2_score = max(view2_score, ViewScore.HIGHLY_APPLICABLE)
        view2_reasoning = (
            "AI agents with file access could be tricked into unauthorized "
            "file operations."
        )
        ai_category = AICategory.AGENT_AUTONOMY
        ai_impact = "Unauthorized file access via AI."

    # Rule: Request forgery (high View 2 for agents)
    request_patterns = [
        r"server.side.*request.*forgery",
        r"ssrf",
        r"url.*redirect",
        r"open.*redirect",
    ]
    if any(re.search(p, text) for p in request_patterns):
        view2_score = ViewScore.PRIMARY_EXAMPLE
        view2_reasoning = (
            "Request forgery is critical for AI agents - attackers want AI "
            "to make malicious requests."
        )
        view1_score = max(view1_score, ViewScore.MODERATELY_APPLICABLE)
        view1_reasoning = "Could be used to attack AI infrastructure."
        ai_category = AICategory.AGENT_AUTONOMY
        ai_impact = "Internal network access or service exploitation via AI requests."

    # Rule: Serialization/deserialization (high View 1)
    serial_patterns = [
        r"deserializ",
        r"pickle",
        r"marshal",
        r"untrusted.*data.*interpret",
    ]
    if any(re.search(p, text) for p in serial_patterns):
        view1_score = ViewScore.PRIMARY_EXAMPLE
        view1_reasoning = (
            "Deserialization is critical for AI model loading. Malicious model "
            "files can execute code."
        )
        ai_category = AICategory.SUPPLY_CHAIN
        ai_impact = "Code execution via malicious model files."

    # Rule: Authentication/Authorization (moderate both views)
    auth_patterns = [
        r"authenticat",
        r"authori[sz]",
        r"access.*control",
        r"privilege",
        r"permission",
    ]
    if any(re.search(p, text) for p in auth_patterns):
        view1_score = max(view1_score, ViewScore.MODERATELY_APPLICABLE)
        view1_reasoning = (
            "Authentication/authorization affects AI API access and model protection."
        )
        view2_score = max(view2_score, ViewScore.WEAKLY_APPLICABLE)
        view2_reasoning = (
            "AI might be tricked into bypassing or exposing authentication."
        )
        ai_category = AICategory.INFRASTRUCTURE
        ai_impact = "Unauthorized access to AI systems."

    # Rule: Information disclosure (both views)
    # Note: V2 is MODERATE not HIGH because info leakage is not "AI output IS the attack"
    # - the AI leaking data is harmful but distinct from AI generating attack payloads
    disclosure_patterns = [
        r"information.*expos",
        r"information.*disclos",
        r"information.*leak",
        r"sensitive.*data",
        r"data.*expos",
    ]
    if any(re.search(p, text) for p in disclosure_patterns):
        view1_score = max(view1_score, ViewScore.MODERATELY_APPLICABLE)
        view1_reasoning = "Could expose model details, training data, or prompts."
        view2_score = max(view2_score, ViewScore.MODERATELY_APPLICABLE)
        view2_reasoning = (
            "AI could leak sensitive information, but this is data exposure "
            "not AI generating attack payloads."
        )
        ai_category = AICategory.OUTPUT_VALIDATION
        ai_impact = "Data leakage via AI outputs."

    # Rule: XSS/HTML injection (high View 2)
    xss_patterns = [
        r"cross.site.*script",
        r"\bxss\b",
        r"html.*injection",
        r"script.*injection",
    ]
    if any(re.search(p, text) for p in xss_patterns):
        view2_score = ViewScore.HIGHLY_APPLICABLE
        view2_reasoning = (
            "XSS is a primary target for AI-generated attacks. AI output "
            "containing XSS executes in user browsers."
        )
        ai_category = AICategory.OUTPUT_VALIDATION
        ai_impact = "Client-side attacks via AI-generated web content."

    # Rule: Hardware/microarchitectural weaknesses (not AI-relevant)
    # These are CPU-level vulnerabilities (Spectre, Meltdown, etc.) that don't
    # apply to AI systems in any meaningful way
    hardware_patterns = [
        r"microarchitectur",
        r"transient.*execution",
        r"speculative.*execution",
        r"electromagnetic.*fault",
        r"fault.*injection",
        r"hardware.*redundancy",
        r"processor.*optimization",
        r"trace.*data",
        r"debug.*logic.*runtime",
    ]
    if any(re.search(p, text) for p in hardware_patterns):
        view1_score = ViewScore.NOT_APPLICABLE
        view2_score = ViewScore.NOT_APPLICABLE
        view1_reasoning = "Hardware/microarchitectural weakness, not AI-relevant."
        view2_reasoning = "Hardware/microarchitectural weakness, not AI-relevant."
        ai_category = AICategory.NOT_APPLICABLE
        ai_impact = ""

    # Rule: Legacy/specialized tech (reduce scores)
    legacy_patterns = [
        r"\bj2ee\b",
        r"\basp\.net\b",
        r"\bcobol\b",
        r"\bfortran\b",
        r"\bmainframe\b",
        r"\bcoldfusion\b",
    ]
    if any(re.search(p, text) for p in legacy_patterns):
        # If the name contains legacy tech, this is probably not AI-relevant
        if any(re.search(p, entry.name.lower()) for p in legacy_patterns):
            view1_score = ViewScore.NOT_APPLICABLE
            view2_score = ViewScore.NOT_APPLICABLE
            view1_reasoning = "Specific to legacy technology, not AI-relevant."
            view2_reasoning = "Specific to legacy technology, not AI-relevant."
            ai_category = AICategory.NOT_APPLICABLE
            ai_impact = ""

    return CWEClassification(
        cwe_id=entry.cwe_id,
        name=entry.name,
        description=entry.description,
        mitre_ai_tagged=entry.is_ai_tagged,
        view1_score=view1_score,
        view1_reasoning=view1_reasoning,
        view2_score=view2_score,
        view2_reasoning=view2_reasoning,
        ai_category=ai_category,
        ai_impact=ai_impact,
        source_view=entry.source_view,
    )


# =============================================================================
# Main Classification Functions
# =============================================================================

def classify_cwe(entry: CWEEntry) -> CWEClassification:
    """
    Classify a single CWE entry for AI relevance.

    This function first checks for known classifications, then falls back
    to rule-based classification. After getting the base classification,
    it derives attack_type and attack_surface from the other fields.

    Args:
        entry: The CWE entry to classify.

    Returns:
        CWEClassification with View 1 and View 2 scores and reasoning.
    """
    # Check if we have a known classification
    if entry.cwe_id in KNOWN_CLASSIFICATIONS:
        known = KNOWN_CLASSIFICATIONS[entry.cwe_id]
        classification = CWEClassification(
            cwe_id=entry.cwe_id,
            name=entry.name,
            description=entry.description,
            mitre_ai_tagged=entry.is_ai_tagged,
            view1_score=known["view1_score"],
            view1_reasoning=known["view1_reasoning"],
            view2_score=known["view2_score"],
            view2_reasoning=known["view2_reasoning"],
            ai_category=known["ai_category"],
            ai_impact=known["ai_impact"],
            source_view=entry.source_view,
        )
    else:
        # Fall back to rule-based classification
        classification = _classify_by_rules(entry)

    # Derive attack_type and attack_surface from the classification
    # This is done here rather than in each classification path to ensure
    # consistency and keep the logic centralized
    classification.attack_type = _determine_attack_type(
        classification.view1_score,
        classification.view2_score,
        classification.ai_category,
    )
    classification.attack_surface = _determine_attack_surface(
        classification.view1_score,
        classification.view2_score,
        classification.ai_category,
    )

    return classification


def classify_all(
    entries: list[CWEEntry],
    checkpoint_file: Optional[Path] = None,
    checkpoint_interval: int = 50,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> list[CWEClassification]:
    """
    Classify all CWE entries with optional checkpointing.

    Why checkpointing:
        When processing 1000+ CWEs, especially with AI-assisted classification,
        we don't want to lose progress if something fails. Checkpointing saves
        intermediate results that can be resumed.

    Args:
        entries: List of CWE entries to classify.
        checkpoint_file: Path to save checkpoints. If None, no checkpointing.
        checkpoint_interval: Save checkpoint every N entries.
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        List of CWEClassification objects.
    """
    results: list[CWEClassification] = []
    processed_ids: set[int] = set()

    # Load existing checkpoint if present
    if checkpoint_file and checkpoint_file.exists():
        logger.info(f"Loading checkpoint from {checkpoint_file}")
        try:
            with open(checkpoint_file, "r") as f:
                checkpoint_data = json.load(f)
                for item in checkpoint_data:
                    classification = CWEClassification(**item)
                    results.append(classification)
                    processed_ids.add(classification.cwe_id)
            logger.info(f"Resumed with {len(results)} already classified")
        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}")

    # Process remaining entries
    total = len(entries)
    for i, entry in enumerate(tqdm(entries, desc="Classifying CWEs")):
        if entry.cwe_id in processed_ids:
            continue  # Already processed

        classification = classify_cwe(entry)
        results.append(classification)
        processed_ids.add(entry.cwe_id)

        # Progress callback
        if progress_callback:
            progress_callback(len(results), total)

        # Save checkpoint
        if checkpoint_file and len(results) % checkpoint_interval == 0:
            _save_checkpoint(results, checkpoint_file)

    # Final checkpoint save
    if checkpoint_file:
        _save_checkpoint(results, checkpoint_file)

    logger.info(f"Classified {len(results)} CWE entries")
    return results


def _save_checkpoint(
    classifications: list[CWEClassification],
    checkpoint_file: Path,
) -> None:
    """Save classifications to a checkpoint file."""
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
    with open(checkpoint_file, "w") as f:
        data = [c.model_dump() for c in classifications]
        json.dump(data, f, indent=2, default=str)
    logger.debug(f"Checkpoint saved: {len(classifications)} entries")
