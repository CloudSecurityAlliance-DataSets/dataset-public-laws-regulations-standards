# CWE AI Relevance Analysis Report

**Analysis Date:** December 2024
**Total CWEs Analyzed:** 944
**Methodology:** Two-View Model for AI Security Classification

## Executive Summary

We analyzed all 944 CWEs in MITRE's Research Concepts view (CWE-1000) to determine their relevance to AI and machine learning security. Our analysis identified:

- **8 CWEs** with the highest AI relevance (Score 4)
- **48 CWEs** with high AI relevance (Score 3)
- **198 CWEs total** with meaningful AI relevance (Score ≥ 2)
- **746 CWEs** that can be safely deprioritized for AI security work

The key finding is that AI security concerns cluster around two distinct patterns:
1. **Attacks ON AI systems** - targeting models, training data, and inference
2. **Attacks VIA AI systems** - using AI as an attack vector to execute traditional vulnerabilities

---

## MITRE's Official AI/ML Tagged CWEs

MITRE has explicitly tagged 17 CWEs as applicable to AI/ML systems in the CWE database. This section examines those official tags and how they align with our broader analysis.

### The 17 MITRE AI/ML Tagged CWEs

| CWE | Name | Our V1 | Our V2 | Our Assessment |
|-----|------|--------|--------|----------------|
| **CWE-1427** | Improper Neutralization of Input Used for LLM Prompting | 4 | 3 | ✅ Core AI weakness - Prompt Injection |
| **CWE-1426** | Improper Validation of Generative AI Output | 2 | 4 | ✅ Core AI weakness - Output Validation |
| **CWE-1434** | Insecure Setting of Generative AI/ML Model Inference Parameters | 4 | 1 | ✅ Core AI weakness - Inference Security |
| **CWE-1039** | Inadequate Detection of Adversarial Input Perturbations | 4 | 0 | ✅ Core AI weakness - Adversarial ML |
| **CWE-502** | Deserialization of Untrusted Data | 4 | 1 | ✅ Critical for model loading (pickle attacks) |
| **CWE-77** | Command Injection | 2 | 4 | ✅ Primary AI agent attack vector |
| **CWE-78** | OS Command Injection | 2 | 4 | ✅ Primary AI agent attack vector |
| **CWE-918** | Server-Side Request Forgery (SSRF) | 2 | 4 | ✅ Primary AI agent attack vector |
| **CWE-22** | Path Traversal | 3 | 3 | ✅ AI file access concerns |
| **CWE-23** | Relative Path Traversal | 2 | 3 | ✅ AI file access variant |
| **CWE-36** | Absolute Path Traversal | 2 | 3 | ✅ AI file access variant |
| **CWE-79** | Cross-site Scripting (XSS) | 1 | 3 | ✅ AI-generated web content |
| **CWE-94** | Code Injection | 2 | 3 | ✅ AI-generated code execution |
| **CWE-95** | Eval Injection | 2 | 3 | ✅ AI-generated code execution |
| **CWE-862** | Missing Authorization | 3 | 2 | ✅ AI action authorization |
| **CWE-116** | Improper Encoding or Escaping of Output | 2 | 0 | 🔍 See analysis below |
| **CWE-1336** | Template Engine Injection | 2 | 0 | 🔍 See analysis below |

### Deep Dive: CWE-116 and CWE-1336

We initially flagged these two CWEs as "generic, less AI-specific" but further research revealed MITRE's insight was deeper than we first recognized.

#### CWE-1336: Template Engine Injection — The "Llama Drama" Vulnerability

**Why MITRE Tagged It:** CWE-1336's observed examples include [CVE-2024-34359](https://github.com/abetlen/llama-cpp-python/security/advisories/GHSA-56xg-wfcc-g829), a critical vulnerability in **llama-cpp-python** (CVSS 9.7):

- **The Attack:** LLM model files (.gguf format) contain chat template metadata processed by Jinja2
- **The Flaw:** llama-cpp-python processed these templates *without sandboxing*
- **The Impact:** A malicious model file could execute arbitrary code when loaded
- **The Scale:** Over 6,000 AI models on HuggingFace were potentially weaponizable

This is a **supply chain attack on AI systems**—you download a model from HuggingFace, and it runs code on your machine. The template engine becomes the attack vector for model poisoning.

**Our Revised Assessment:** CWE-1336 deserves higher View 1 scoring for AI supply chain attacks. The template engine processes model metadata, making it a direct attack ON AI infrastructure.

#### CWE-116: Improper Encoding or Escaping of Output — The Foundation of LLM Output Security

**Why MITRE Tagged It:** CWE-116 is the parent weakness underlying [OWASP LLM02: Insecure Output Handling](https://genai.owasp.org/llmrisk2023-24/llm02-insecure-output-handling/):

- **The Problem:** LLM output is used in downstream systems (web pages, databases, shells)
- **The Defense:** Output encoding strips special characters before the output reaches interpreters
- **Without It:** AI-generated XSS, SQL injection, and command injection all become possible

CWE-116 represents the *defensive mechanism* that prevents View 2 attacks. While we scored it V2=0 (AI doesn't "produce" encoding failures), it's actually the mitigation layer between AI output and injection vulnerabilities.

**What We Learned:**
1. MITRE's tagging captures both offensive (attacks using AI) and defensive (protections for AI output) perspectives
2. Template engines are an underappreciated attack surface in AI model loading
3. The CVE evidence (CVE-2024-34359) demonstrates real-world AI relevance we missed in rule-based classification

**Recommendation:** Security teams should audit template engine usage in AI pipelines, especially when processing model metadata, chat templates, or prompt templates from external sources.

### Analysis of MITRE's Tagging

**What MITRE Got Right:**

1. **Core AI-Specific CWEs (4 entries):** CWE-1427 (Prompt Injection), CWE-1426 (Output Validation), CWE-1434 (Inference Parameters), and CWE-1039 (Adversarial Inputs) are purpose-built for AI security. These represent novel attack surfaces that didn't exist before AI systems.

2. **Supply Chain Recognition:** Including CWE-502 (Deserialization) shows awareness of the pickle attack vector for malicious model loading—a critical AI supply chain concern.

3. **AI Agent Attack Vectors:** The inclusion of CWE-77, CWE-78 (Command Injection) and CWE-918 (SSRF) demonstrates understanding that AI agents with tool access create new exploitation paths for traditional vulnerabilities.

4. **File Operation Risks:** Path traversal CWEs (22, 23, 36) recognize that AI systems with file access can be manipulated to access unauthorized paths.

**Gaps in MITRE's Tagging:**

1. **Incomplete Injection Coverage:** While MITRE tagged XSS (CWE-79) and SQL Injection is conspicuously absent, yet AI-generated SQL queries are a significant attack vector.

2. **Missing CSRF:** CWE-352 (Cross-Site Request Forgery) is not tagged, but AI-generated forms without CSRF protection are a real concern.

3. **Limited Path Traversal:** Only 3 of 20+ path traversal variants are tagged. While the parent CWE-22 covers the concept, the inconsistent tagging of variants is confusing.

4. **No Information Disclosure:** CWE-200 and related information exposure CWEs aren't tagged, despite AI systems being prone to leaking training data and system information.

**Our Extended Analysis Found:**

- **198 CWEs** with meaningful AI relevance (vs. MITRE's 17)
- **56 CWEs** with high AI relevance (Score ≥ 3)
- Most additions are injection variants (View 2) and infrastructure concerns (View 1)

### Why the Gap?

MITRE's tagging appears focused on:
1. **Novel AI-specific weaknesses** (prompt injection, adversarial inputs)
2. **The most critical traditional weaknesses** when applied to AI

Our analysis extends this by systematically evaluating ALL CWEs through the AI security lens, capturing:
- The full family of injection attacks relevant to AI-generated output
- Infrastructure weaknesses affecting AI system deployment
- Indirect/supply chain concerns

### Recommendations for MITRE

Based on our analysis, we suggest MITRE consider tagging these additional high-relevance CWEs:

| CWE | Name | Rationale |
|-----|------|-----------|
| CWE-89 | SQL Injection | AI-generated queries are a primary attack vector |
| CWE-352 | CSRF | AI-generated forms need CSRF protection |
| CWE-200 | Information Exposure | AI systems leak sensitive data |
| CWE-434 | Unrestricted File Upload | AI file handling concerns |
| CWE-829 | Untrusted Functionality Inclusion | AI supply chain (model dependencies) |

---

## The Two-View Classification Model

### Why Two Views?

Traditional single-score relevance ratings fail to capture the dual nature of AI security. A weakness like XSS (CWE-79) scores low for attacking AI systems but high for attacks executed through AI—a single score would obscure this critical distinction.

### View 1: Attacks ON AI

*"Can this weakness be used to attack, compromise, or manipulate an AI system?"*

This view covers:
- Model attacks (extraction, inversion, theft)
- Training data attacks (poisoning, backdoors)
- Inference attacks (adversarial inputs, prompt injection)
- AI infrastructure attacks (model loading, API security)
- Supply chain attacks (malicious models, compromised dependencies)

### View 2: Attacks VIA AI

*"Would attackers specifically want AI to produce or execute this weakness?"*

This view covers cases where the AI output IS the attack:
- AI agent executes shell commands → Command Injection
- AI generates malicious HTML/JS → XSS
- AI makes requests to internal URLs → SSRF
- AI writes to sensitive file paths → Path Traversal

**Key constraint:** We only score highly when the AI output is the attack payload. Buffer overflows in AI-generated C code don't count because they require compilation—the output isn't immediately exploitable.

### Scoring Scale (0-4)

| Score | Label | Definition |
|-------|-------|------------|
| 0 | Not Applicable | This view does not apply to this CWE |
| 1 | Weakly Applicable | Edge cases only, indirect relevance |
| 2 | Moderately Applicable | Relevant but not a primary concern |
| 3 | Highly Applicable | Significant AI relevance |
| 4 | Primary Example | This is exactly what the view describes |

---

## Critical AI-Relevant CWEs (Score 4)

These 8 CWEs represent the most important weaknesses for AI security:

### Attacks ON AI (View 1 = 4)

| CWE | Name | Why Critical |
|-----|------|--------------|
| **CWE-1427** | Improper Neutralization of Input Used for LLM Prompting (Prompt Injection) | The canonical attack on LLMs. Directly targets prompt processing to manipulate model behavior, extract information, or bypass safety controls. |
| **CWE-1039** | Inadequate Detection of Adversarial Input Perturbations | Attacks ML recognition systems using adversarial inputs designed to cause misclassification. Critical for computer vision and audio systems. |
| **CWE-502** | Deserialization of Untrusted Data | Malicious model files (especially Python pickle) can execute arbitrary code when loaded. Major vector for model supply chain attacks. |
| **CWE-1434** | Insecure Setting of Generative AI/ML Model Inference Parameters | Misconfigured temperature, top_k, and other inference parameters can be exploited to bypass safety measures or cause unexpected behavior. |

### Attacks VIA AI (View 2 = 4)

| CWE | Name | Why Critical |
|-----|------|--------------|
| **CWE-77/78** | Command Injection / OS Command Injection | Primary target for AI agent attacks. Attackers trick AI into executing shell commands—the AI action IS the attack. Full system compromise. |
| **CWE-918** | Server-Side Request Forgery (SSRF) | Critical for AI agents with web access. AI makes requests to internal URLs, enabling cloud metadata theft, internal network scanning. |
| **CWE-1426** | Improper Validation of Generative AI Output | The defensive weakness—failure to validate AI output enables all AI-generated attacks. The direct enabler of View 2 concerns. |

---

## Highly Relevant CWEs (Score 3)

These 48 CWEs have significant AI relevance and should be prioritized in AI security assessments:

### Path Traversal Family (20 CWEs)
CWE-22 and its variants (CWE-23 through CWE-40) score V1=2-3, V2=3. AI agents with file system access can be tricked into reading/writing sensitive paths. Both infrastructure concern (V1) and direct attack vector (V2).

### Injection Attacks (15 CWEs)
| CWE | Attack Type | AI Relevance |
|-----|-------------|--------------|
| CWE-79 | XSS | AI generates malicious HTML/JS that executes in browsers |
| CWE-89 | SQL Injection | AI generates malicious queries that execute against databases |
| CWE-90 | LDAP Injection | AI generates malicious LDAP queries |
| CWE-94/95 | Code/Eval Injection | AI generates code that gets dynamically executed |
| CWE-643 | XPath Injection | AI generates malicious XPath expressions |
| CWE-917 | Expression Language Injection | AI generates malicious EL statements |

### Other High-Priority CWEs
| CWE | Name | Relevance |
|-----|------|-----------|
| CWE-200 | Information Exposure | AI may leak sensitive training data or system information |
| CWE-862 | Missing Authorization | AI systems must enforce authorization on AI-initiated actions |
| CWE-434 | Unrestricted File Upload | AI accepting/generating file uploads without validation |
| CWE-352 | CSRF | AI-generated forms/requests without CSRF protection |
| CWE-1236 | CSV Formula Injection | AI generating CSV files with executable formulas |

---

## Moderately Relevant CWEs (Score 2)

These 140+ CWEs have indirect AI relevance, typically as infrastructure concerns:

- **Authentication/Session** (CWE-287, CWE-384, etc.) - AI APIs need proper auth
- **Access Control** (CWE-285, CWE-863, etc.) - AI actions need authorization
- **Information Disclosure** (CWE-209, CWE-532, etc.) - AI may leak data in errors/logs
- **Resource Management** (CWE-400, CWE-770, etc.) - AI inference needs resource limits

---

## CWEs Safe to Deprioritize for AI Security (Score 0-1)

**746 CWEs** (79% of total) have minimal AI relevance. Here's why:

### Memory Safety Issues (43 CWEs)
Buffer overflows, use-after-free, etc. require compiled code. AI-generated memory bugs need compilation and deployment before exploitation—the AI output is not immediately dangerous.

**Examples:** CWE-119 (Buffer Overflow), CWE-416 (Use After Free), CWE-787 (Out-of-bounds Write)

### Hardware/Microarchitecture (33 CWEs)
CPU-level vulnerabilities (Spectre, Meltdown variants) are not AI-specific and don't represent novel AI attack surfaces.

**Examples:** CWE-1342 (Transient Execution), CWE-1420-1423 (Spectre variants)

### Legacy Technology (35 CWEs)
J2EE, Struts, ASP.NET Classic, and other legacy frameworks are not used in modern AI systems.

**Examples:** CWE-5 through CWE-9 (J2EE), CWE-102-110 (Struts), CWE-11-13 (ASP.NET)

### Path Equivalence Variants (17 CWEs)
Low-level filesystem tricks (trailing dots, slashes, spaces) are OS-specific implementation details. The parent CWE-22 covers AI-relevant path concerns.

**Examples:** CWE-42 (Trailing Dot), CWE-46 (Trailing Space), CWE-58 (Windows 8.3 Filenames)

### Abstract Input Neutralization (37 CWEs)
Generic sanitization concepts without specific attack context. More specific injection CWEs cover AI-relevant cases.

**Examples:** CWE-138 (Special Elements), CWE-140-165 (Various Delimiter Neutralization)

### Code Quality Issues (14 CWEs)
Style, complexity, and maintainability issues that don't represent security vulnerabilities.

**Examples:** CWE-1120 (Excessive Complexity), CWE-1078 (Inappropriate Formatting)

### Cryptography (16 CWEs)
General cryptographic weaknesses apply to all software equally and aren't AI-specific.

**Examples:** CWE-326 (Weak Encryption), CWE-328 (Weak Hash)

---

## Attack Surface Model

We developed a four-surface model to understand where AI security concerns arise:

### The Four Attack Surfaces

| Surface | Description | CWE Coverage |
|---------|-------------|--------------|
| **Supporting Infrastructure** | Servers, APIs, databases hosting AI | Well covered by existing CWEs |
| **AI System Core** | Model, prompts, inference pipeline | Poorly covered (only ~4 AI-specific CWEs) |
| **AI-Controlled/Generated Systems** | Code, configs, actions AI produces | CWEs apply to OUTPUT—AI is the novel vector |
| **AI Knowledge/Supply Chain** | Training data, web search, integrations | Partially covered, trust boundary dependent |

### The Four Actors

| Actor | Examples | Responsibility |
|-------|----------|----------------|
| **AI Foundation Provider** | Anthropic, OpenAI, Google | Highest—model behavior, training data, core safety |
| **AI Platform Provider** | Cursor, Replit, Claude.ai | High—can add guardrails, filter I/O, restrict tools |
| **End User** | Developers, enterprises | Medium—responsible for their usage and integrations |
| **Third-party Data Provider** | Airtable, GitHub, web APIs | Limited—not AI-aware, can't prevent prompt injection in their data |

### Key Insight: Trust Boundaries

Third-party data providers cannot be held responsible for prompt injection in their data—they are "AI-unaware." The responsibility falls on AI Platform Providers and End Users to sanitize and validate data from external sources.

---

## What We Learned

### 1. The Dual Nature of AI Security

AI security isn't a single dimension. The same CWE can be irrelevant for attacking AI (View 1) but critical for attacks through AI (View 2). XSS is the clearest example—it rarely threatens AI infrastructure but is a primary concern when AI generates web content.

### 2. Direct vs. Indirect Attacks Matter

For View 2, we distinguish:
- **Direct attacks**: AI output IS the attack (command injection, SSRF)
- **Indirect attacks**: AI distributes vulnerabilities (poisoned training data)

Direct attacks score higher because exploitation is immediate.

### 3. Most CWEs Don't Apply to AI

79% of CWEs can be safely deprioritized for AI security work. They fall into:
- Memory safety (requires compilation)
- Legacy technology (not used in AI)
- Hardware vulnerabilities (not AI-specific)
- Abstract concepts (covered by specific CWEs)

### 4. MITRE's AI Tagging is Incomplete but Accurate

MITRE has tagged 17 CWEs as AI/ML relevant. All 17 received non-zero scores in our analysis, confirming their relevance. However, our analysis identified 198 CWEs with meaningful AI relevance—suggesting MITRE's tagging captures only the most obvious cases.

### 5. AI Agents Change the Game

The emergence of AI agents with tool access (file systems, web requests, command execution) dramatically increases View 2 relevance for injection attacks. CWEs like command injection and SSRF that were traditionally server-side concerns become critical when AI can execute them directly.

### 6. Output Validation is the Key Defense

CWE-1426 (Improper Validation of Generative AI Output) is the defensive linchpin. Proper output validation mitigates most View 2 attacks. Organizations should treat all AI output as untrusted input requiring validation before use.

---

## Recommendations

### For AI Foundation Providers
1. Prioritize CWE-1427 (Prompt Injection) defenses
2. Implement robust model loading security (CWE-502)
3. Document safe inference parameter ranges (CWE-1434)
4. Test for adversarial input vulnerabilities (CWE-1039)

### For AI Platform Providers
1. Implement output validation for all AI-generated content (CWE-1426)
2. Restrict AI agent capabilities to minimum necessary
3. Sandbox AI-executed commands and file operations
4. Filter AI outputs for injection patterns before execution

### For End Users
1. Never execute AI-generated code/commands without review
2. Validate AI-generated file paths before use
3. Sanitize AI output before including in web pages or queries
4. Treat all AI integrations as untrusted data sources

---

## Appendix: Classification Statistics

### Score Distribution

**View 1 (Attacks ON AI):**
| Score | Count | Percentage |
|-------|-------|------------|
| 0 | 762 | 80.7% |
| 1 | 4 | 0.4% |
| 2 | 171 | 18.1% |
| 3 | 3 | 0.3% |
| 4 | 4 | 0.4% |

**View 2 (Attacks VIA AI):**
| Score | Count | Percentage |
|-------|-------|------------|
| 0 | 746 | 79.0% |
| 1 | 119 | 12.6% |
| 2 | 27 | 2.9% |
| 3 | 48 | 5.1% |
| 4 | 4 | 0.4% |

### Category Distribution

| Category | Count |
|----------|-------|
| Not Applicable | 746 |
| Infrastructure | 119 |
| Output Validation | 47 |
| Agent/Autonomous Systems | 25 |
| General | 3 |
| Supply Chain | 1 |
| Model Security | 1 |
| Prompt Injection | 1 |
| Inference Security | 1 |

---

## Addendum: Lessons from MITRE's Tagging

After completing our initial analysis, we revisited CWE-116 and CWE-1336—two MITRE-tagged CWEs we had flagged as "generic, less AI-specific." Deeper research revealed we were wrong, and MITRE's insight was more sophisticated than we initially recognized.

### The Key Discovery: CVE-2024-34359 ("Llama Drama")

A critical vulnerability (CVSS 9.7) in [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/security/advisories/GHSA-56xg-wfcc-g829) demonstrated why CWE-1336 (Template Engine Injection) matters for AI:

- LLM model files (.gguf) contain chat templates in their metadata
- These templates are processed by Jinja2 when loading the model
- Without sandboxing, malicious templates execute arbitrary code
- **6,000+ models on HuggingFace** were potentially weaponizable

This is a **supply chain attack on AI infrastructure**—download a model, get owned.

### What This Teaches Us

| Lesson | Implication |
|--------|-------------|
| **CVE evidence reveals AI relevance** | Rule-based classification misses real-world attack patterns |
| **Template engines are AI attack surface** | Model metadata, chat templates, and prompt templates need sandboxing |
| **MITRE tags defensive CWEs too** | CWE-116 (output encoding) is the *mitigation* for View 2 attacks |
| **Supply chain extends beyond pickle** | CWE-502 (deserialization) isn't the only model loading risk |

### Recommendations Based on This Analysis

1. **Audit template engine usage** in AI pipelines—especially when processing external model files
2. **Sandbox all template processing** that handles model metadata or chat templates
3. **Don't dismiss "generic" CWEs**—their AI relevance may be through non-obvious attack chains
4. **Track CVEs in AI libraries**—they reveal attack patterns faster than theoretical analysis

### Limitations of This Report

This analysis used rule-based classification, which has inherent blind spots:

- **Novel attack patterns** require CVE evidence we may not have seen
- **Defensive CWEs** (mitigations rather than attacks) may be underscored
- **Supply chain complexity** means attack chains span multiple CWEs
- **Rapidly evolving field**—new AI attack surfaces emerge faster than CWE entries

We recommend treating this report as a starting point, not a complete mapping. Security teams should supplement with CVE monitoring, threat intelligence, and hands-on AI security testing.

---

## References

- [CWE Official Site](https://cwe.mitre.org/)
- [MITRE ATLAS](https://atlas.mitre.org/) - Adversarial Threat Landscape for AI Systems
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP LLM02: Insecure Output Handling](https://genai.owasp.org/llmrisk2023-24/llm02-insecure-output-handling/)
- [CVE-2024-34359: Llama Drama](https://checkmarx.com/blog/llama-drama-critical-vulnerability-cve-2024-34359-threatening-your-software-supply-chain/) - Template injection in llama-cpp-python
- [CWE-AI-METHODOLOGY.md](CWE-AI-METHODOLOGY.md) - Full methodology documentation
- [AI-ATTACK-SURFACE-MODEL.md](AI-ATTACK-SURFACE-MODEL.md) - Detailed attack surface analysis

---

*Report generated as part of the CWE AI Relevance Classification Project*
*Cloud Security Alliance DataSets Repository*
