# CWE AI Relevance Classification Methodology

This document describes the methodology for classifying CWE (Common Weakness Enumeration) entries based on their relevance to AI and AI systems.

## Objective

Analyze all CWE entries to determine which weaknesses are relevant to AI security, and in what way. The goal is to produce a dataset that helps security professionals understand:

1. Which CWEs can be used to attack AI systems
2. Which CWEs represent attacks that AI might be tricked into executing

## Attack Surface Context

Before classifying CWEs, it's important to understand the AI ecosystem's attack surfaces. For full details, see [AI-ATTACK-SURFACE-MODEL.md](AI-ATTACK-SURFACE-MODEL.md).

### Four Key Actors

| Actor | Examples | Responsibility Level |
|-------|----------|---------------------|
| **AI Foundation Provider** | Anthropic, OpenAI, Google | Highest - model behavior, training data, core safety |
| **AI Platform/Application Provider** | Cursor, Replit, Claude.ai | High - can add guardrails, filter I/O, restrict tools |
| **End User** | Developers, enterprises | Medium - responsible for their usage and integrations |
| **Third-party Data/Service Provider** | Airtable, GitHub, web APIs | Limited - not AI-aware, can't be held responsible for prompt injection in their data |

### Four Attack Surfaces

| Surface | Description | CWE Coverage |
|---------|-------------|--------------|
| **Supporting Infrastructure** | Servers, APIs, databases hosting AI | Well covered - traditional software security |
| **AI System Core** | Model, prompts, inference pipeline | Poorly covered - only ~4 AI-specific CWEs exist |
| **AI-Controlled/Generated Systems** | Code, configs, actions AI produces | CWEs apply to OUTPUT - AI is the novel vector |
| **AI Knowledge/Supply Chain** | Training data, web search, integrations | Partially covered - trust boundary dependent |

### Why This Context Matters for Scoring

When classifying a CWE:
- **Infrastructure attacks** are traditional security - well understood, well covered
- **AI Core attacks** are novel - this is where AI changes the game
- **AI Output attacks** use traditional CWEs but AI is the attack vector
- **Supply chain attacks** vary by trust boundary - who controls the source?

## The Two-View Model

After analysis, we determined that AI relevance to CWEs falls into two distinct categories that should be scored independently.

### View 1: Attacks ON AI

**Question**: Can this weakness be used to attack, compromise, or manipulate an AI system?

**Scope includes**:
- Model attacks (extraction, inversion, theft)
- Training attacks (data poisoning, backdoors)
- Inference attacks (adversarial inputs, prompt injection)
- Infrastructure attacks (model loading, API security)
- Supply chain attacks (malicious models, compromised dependencies)

**Examples**:
| CWE | Name | View 1 Score | Reasoning |
|-----|------|--------------|-----------|
| 1427 | Prompt Injection | 4 | Canonical attack on LLMs |
| 1039 | Adversarial Input Perturbations | 4 | Attacks ML recognition systems |
| 502 | Deserialization | 4 | Malicious model loading (pickle attacks) |
| 22 | Path Traversal | 3 | Access to model files, training data |

### View 2: Attacks VIA AI

**Question**: Can an attacker trick AI into directly producing or executing this attack?

**Key constraint**: Only score highly if the AI output IS the attack or directly enables it. We deliberately exclude vulnerabilities that would require additional steps (like compiling AI-generated code).

#### Direct vs Indirect Attacks

View 2 encompasses two distinct attack patterns:

**Direct Attacks** (Score higher - 3 or 4):
- Attacker interacts with AI system directly
- AI produces or executes the attack immediately
- No additional steps required for exploitation
- Examples: Command injection via AI agent, XSS in AI-generated HTML, SSRF via AI fetching URLs

**Indirect/Poisoning Attacks** (Score based on impact):
- Attacker manipulates AI's knowledge sources (training data, web search, SEO)
- Victim uses AI for legitimate purpose, gets vulnerable output
- AI becomes unwitting distributor of vulnerabilities
- Examples: Poisoned training data with insecure patterns, SEO manipulation to promote malicious libraries
- Score higher for high-impact outcomes (supply chain, RCE), lower for minor vulnerabilities

**Scope includes**:
- Injection attacks where AI generates the payload (XSS, SQLi, command injection)
- Request forgery where AI makes malicious requests (SSRF)
- File operations where AI reads/writes attacker-controlled paths
- Supply chain attacks where AI recommends malicious dependencies

**Scope excludes**:
- Memory safety issues in AI-generated code (requires compilation/deployment)
- Complex logic bugs (hard to intentionally induce)
- Generic code quality issues (not directly exploitable)
- Information disclosure (harmful but not "AI output IS the attack" - score V2=2 max)

**Examples**:
| CWE | Name | View 2 Score | Type | Reasoning |
|-----|------|--------------|------|-----------|
| 78 | Command Injection | 4 | Direct | AI agent executes commands - immediate attack |
| 918 | SSRF | 4 | Direct | AI agent fetches attacker URLs - immediate attack |
| 79 | XSS | 3 | Direct | AI generates malicious HTML/JS - executes in browser |
| 89 | SQL Injection | 3 | Direct | AI generates malicious query - immediate attack |
| 829 | Untrusted Functionality | 3 | Indirect | AI recommends malicious library - supply chain impact |
| 200 | Info Exposure | 2 | Direct | AI leaks data - harmful but not attack payload |
| 787 | Out-of-bounds Write | 1 | Indirect | AI might generate vulnerable code, requires compilation |

## Scoring Scale (0-4)

Both views use the same 0-4 scale:

| Score | Label | Definition |
|-------|-------|------------|
| 0 | Not Applicable | This view does not apply to this CWE |
| 1 | Weakly Applicable | Edge cases only, indirect relevance |
| 2 | Moderately Applicable | Relevant but not a primary concern |
| 3 | Highly Applicable | Significant AI relevance |
| 4 | Primary Example | This is exactly what the view describes |

We chose 0-4 instead of 1-5 because 0 clearly indicates "not applicable" whereas a 1 on a 1-5 scale is ambiguous.

## Scoring Considerations

When classifying a CWE, evaluate these factors:

### 1. Which Actors Are Affected?

| If primarily affecting... | Consideration |
|---------------------------|---------------|
| Foundation Provider | Core AI safety issue - likely high View 1 |
| Platform Provider | May need platform-level mitigations |
| End User | User configuration/integration issue |
| Third-party | Usually not their responsibility - user/platform must handle |

### 2. Which Attack Surface?

| Surface | View 1 | View 2 |
|---------|--------|--------|
| Infrastructure | Traditional security scores | Low - not AI-specific |
| AI Core | High if targets model/prompts | N/A |
| AI Outputs | Low unless affects AI infra | High if direct attack |
| Supply Chain | High if poisons AI knowledge | Varies by impact |

### 3. Direct or Indirect Attack?

For View 2:
- **Direct**: AI output IS the attack → Score 3-4
- **Indirect high-impact**: Supply chain, RCE → Score 2-3
- **Indirect low-impact**: Minor vulns, requires compilation → Score 0-1

### 4. Trust Boundaries

- Who controls the attack surface?
- Who bears responsibility to mitigate?
- Is this within AI company control or user-configured?

## Combined Classification Examples

| CWE | Name | V1 | V2 | Attack Type | Notes |
|-----|------|----|----|-------------|-------|
| 1427 | Prompt Injection | 4 | 3 | Direct | Canonical attack ON AI, enables VIA attacks |
| 1426 | GenAI Output Validation | 2 | 4 | Direct | The defense against View 2 attacks |
| 1039 | Adversarial Inputs | 4 | 0 | N/A | Pure View 1 attack on ML models |
| 502 | Deserialization | 4 | 1 | Indirect | Model supply chain attacks |
| 78 | Command Injection | 2 | 4 | Direct | AI agent executes - immediate RCE |
| 918 | SSRF | 2 | 4 | Direct | AI agent makes requests - immediate |
| 79 | XSS | 1 | 3 | Direct | AI generates malicious HTML/JS |
| 89 | SQL Injection | 1 | 3 | Direct | AI generates malicious queries |
| 22 | Path Traversal | 3 | 3 | Direct | Both: model files AND AI file ops |
| 200 | Info Exposure | 3 | 2 | Direct | V2 lowered: leakage, not attack payload |
| 601 | Open Redirect | 1 | 2 | Indirect | Phishing enabler, requires user action |
| 5 | J2EE Misconfiguration | 0 | 0 | N/A | Legacy tech, not AI-related |

## Output Data Format

The analysis produces a CSV with the following columns:

| Column | Description |
|--------|-------------|
| CWE_ID | The CWE identifier |
| Name | CWE name |
| Description | Brief description from CWE |
| MITRE_AI_Tagged | Whether MITRE has tagged this as AI/ML applicable |
| View1_Score | 0-4 score for "Attacks ON AI" |
| View1_Reasoning | Explanation for View 1 score |
| View2_Score | 0-4 score for "Attacks VIA AI" |
| View2_Reasoning | Explanation for View 2 score |
| AI_Category | Category (Prompt Injection, Model Security, etc.) |
| AI_Impact | Potential impact if exploited in AI context |

## Data Sources

We analyze all CWEs from three views:

1. **CWE-1000 (Research Concepts)** - ~944 entries, comprehensive
2. **CWE-699 (Software Development)** - ~399 entries, development-focused
3. **CWE-1194 (Hardware Design)** - ~110 entries, hardware-focused (includes AI hardware)

## Process

1. **Automated extraction**: Identify CWEs already tagged with AI/ML by MITRE
2. **Keyword search**: Find additional candidates via relevant terms
3. **AI classification**: Review all CWEs and assign View 1 and View 2 scores
4. **Merge and validate**: Combine results and validate classifications
5. **Generate report**: Produce final CSV and summary statistics

## How We Arrived at This Methodology

### Initial Approach Considered

We initially considered a single relevance score (1-5) with categories like:
- Direct (AI-specific attacks)
- Applicable (general weaknesses affecting AI)
- Amplified (worse in AI contexts)
- Not Relevant

**Why we rejected this**: It conflated two distinct questions - whether AI is being attacked vs whether AI is being weaponized. A single score couldn't capture that XSS is low for attacking AI but high for AI-generated attacks.

### Direction Field Considered

We considered adding a "Direction" field:
- Inbound (attack targets AI)
- Outbound (AI generates vulnerability)
- Infrastructure
- Training

**Why we evolved this**: This was on the right track but still tried to force a single classification. The two-view model allows independent scoring on each dimension.

### Why Not Score Every CWE for View 2?

We recognized that if AI can write code, theoretically every CWE could be something an attacker might induce. This makes a broad View 2 useless.

**Solution**: Narrow View 2 to only include cases where the AI output IS the attack payload or directly enables it. Buffer overflows in AI-generated C code don't count because they require compilation and deployment - the output isn't immediately exploitable.

### The XSS/CSRF Insight

The key insight came from discussing XSS and CSRF:
- These are NOT attacks on AI (View 1: low)
- These ARE things attackers want AI to produce (View 2: high)
- The AI-generated XSS directly executes in browsers - no additional steps

This clarified that View 2 should focus on "AI output IS the weapon" cases.

### Why 0-4 Instead of 1-5?

A 1-5 scale where 1 means "slightly applicable" creates ambiguity. Starting at 0 makes it clear that 0 = "this view does not apply" while 1+ indicates some level of applicability.

## Exclusions

Certain categories of CWEs are explicitly scored as not AI-relevant (V1=0, V2=0):

### Hardware/Microarchitectural Weaknesses

CWEs related to CPU-level vulnerabilities (Spectre, Meltdown, etc.) are not relevant to AI security in any meaningful way:
- Transient execution vulnerabilities
- Microarchitectural side channels
- Electromagnetic fault injection
- Hardware redundancy issues

**Examples**: CWE-1342, CWE-1420, CWE-1421, CWE-1422, CWE-1423

### Legacy Technology

CWEs specific to legacy or niche technologies that are not used in modern AI systems:
- J2EE-specific misconfigurations
- COBOL, Fortran, ColdFusion
- Mainframe-specific issues
- ASP.NET classic issues

**Examples**: CWE-5, CWE-6, CWE-7 (J2EE misconfigurations)

### Generic Quality Issues

CWEs that describe code quality issues rather than security vulnerabilities:
- Irrelevant/dead code (CWE-1164)
- Generic control flow issues (CWE-691)
- Wrong status codes (CWE-393)

These might appear in AI-generated code but are not security attacks.

## References

### Project Documents
- [AI Attack Surface Model](AI-ATTACK-SURFACE-MODEL.md) - Detailed actor hierarchy and attack surface analysis
- [CWE Primer](CWE-PRIMER.md) - Introduction to CWE and how it relates to AI security

### External Resources
- CWE Official Site: https://cwe.mitre.org/
- CWE Content Development Repository: https://github.com/CWE-CAPEC/CWE-Content-Development-Repository
- MITRE ATLAS (Adversarial Threat Landscape for AI Systems): https://atlas.mitre.org/
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Model Context Protocol: https://modelcontextprotocol.io/

---

*Document created: December 2024*
*Methodology developed through iterative analysis of CWE data and AI security considerations*
