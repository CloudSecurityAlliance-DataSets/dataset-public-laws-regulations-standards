# AIVSS (Agentic AI Vulnerability Scoring System)

AIVSS is an OWASP project that extends CVSS v4.0 vulnerability scoring methodology specifically for agentic AI systems. Agentic AI systems demonstrate autonomous goal pursuit, independent decision-making, and interaction with external tools - creating unique attack surfaces that require specialized vulnerability assessment beyond traditional security controls. 

**AIVSS is a superset of CVSS v4.0** - it includes all standard CVSS metrics and calculations, then adds 10 additional agentic-specific risk amplification factors. This ensures compatibility with existing vulnerability management workflows while addressing the unique risks of autonomous AI agents.

## How AIVSS Extends CVSS v4.0

AIVSS works by:
1. **Starting with full CVSS v4.0 assessment** - All traditional metrics (Attack Vector, Attack Complexity, Privileges Required, User Interaction, Impact metrics, etc.)
2. **Adding agentic risk evaluation** - 10 additional factors specific to autonomous AI agent behavior
3. **Combining both scores equally** - Takes 50/50 average to balance traditional and agentic risks
4. **Applying threat context** - Adjusts final score based on current exploitability

## Scoring Formula

**AIVSS_Score = ((CVSS_Base_Score + AARS) / 2) × ThM**

Where:
- **CVSS_Base_Score**: Full CVSS v4.0 base score (0-10) using all standard metrics
- **AARS**: Agentic AI Risk Score - sum of 10 agentic risk amplification factors (0-10)
- **ThM**: Threat Multiplier (default: 0.97, max: 1.0 for active exploitation)

## 10 Agentic Risk Amplification Factors (AARS)

Each factor scored 0.0, 0.5, or 1.0:

1. **Autonomy** - Agent's capacity for independent action
2. **Tool Use** - Access to external tools and systems
3. **Memory** - Persistent context and learning capabilities
4. **Dynamic Identity** - Ability to assume different roles/permissions
5. **Multi-Agent** - Interactions with other AI agents
6. **Non-Determinism** - Unpredictable behavior patterns
7. **Self-Modification** - Ability to modify own code/behavior
8. **Goal-Planning** - Long-term objective pursuit
9. **Context Awareness** - Understanding of operational environment
10. **Opacity** - Difficulty in understanding decision-making process

## Scoring Scale

- **0.0-3.9**: Low Risk
- **4.0-6.9**: Medium Risk  
- **7.0-8.9**: High Risk
- **9.0-10.0**: Critical Risk

## AIVSS Vector Format

`(CVSS: [score] / AARS: [score])`

Example: `(CVSS: 9.4 / AARS: 8.5)` = Final AIVSS Score: 8.7

## Compatibility with CVSS v4.0

- **Fully compatible** with existing CVSS v4.0 workflows and tools
- **Uses all standard CVSS metrics** - no traditional scoring is lost
- **Can leverage full CVSS v4.0 context** - Threat, Environmental, and Supplemental metrics
- **Extends rather than replaces** - Organizations can adopt AIVSS while maintaining CVSS processes

## Official Resources

- Project Website: https://aivss.owasp.org/
- Documentation: https://vineethsai.github.io/aivss/AIVSS%20Scoring%20System%20For%20OWASP%20Agentic%20AI%20Core%20Security%20Risks%20v0.5.pdf