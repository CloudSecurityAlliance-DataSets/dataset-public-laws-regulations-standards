# CWE AI Relevance Analysis Report

**Analysis Date:** January 2026
**Total CWEs Analyzed:** 944
**Methodology:** Two-View Model for AI Security Classification

## File Location

https://github.com/CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards/blob/main/frameworks-guidance/industry/MITRE/CWE/CWE-AI-RELEVANCE-REPORT.md

---

## Executive Summary

This report analyzes all 944 CWEs in MITRE's Research Concepts view (CWE-1000) to determine their relevance to AI and machine learning security. The analysis provides practical guidance for security teams working with AI systems.

**Key Findings:**

- **8 CWEs** with the highest AI relevance (Score 4)
- **49 CWEs** with high AI relevance (Score 3)
- **199 CWEs total** with meaningful AI relevance (Score ≥ 2)
- **745 CWEs** that can be safely deprioritized for AI security work

AI security concerns cluster around two distinct patterns:

1. **Attacks ON AI systems** — targeting models, training data, and inference
2. **Attacks VIA AI systems** — using AI as an attack vector to execute traditional vulnerabilities

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
| **CWE-77** | Command Injection | Primary target for AI agent attacks. Attackers trick AI into executing shell commands—the AI action IS the attack. Full system compromise. |
| **CWE-78** | OS Command Injection | Variant of command injection specific to OS shell commands. Critical for AI agents with system access. |
| **CWE-918** | Server-Side Request Forgery (SSRF) | Critical for AI agents with web access. AI makes requests to internal URLs, enabling cloud metadata theft, internal network scanning. |
| **CWE-1426** | Improper Validation of Generative AI Output | The defensive weakness—failure to validate AI output enables all AI-generated attacks. The direct enabler of View 2 concerns. |

---

## Highly Relevant CWEs (Score 3)

These 49 CWEs have significant AI relevance and should be prioritized in AI security assessments. A CWE is included if it scores 3 in either View 1 (attacks ON AI) or View 2 (attacks VIA AI).

### Complete List of Score 3 CWEs

| CWE | Name | V1 | V2 |
|-----|------|:--:|:--:|
| **CWE-22** | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | 3 | 3 |
| **CWE-23** | Relative Path Traversal | 2 | 3 |
| **CWE-24** | Path Traversal: '../filedir' | 2 | 3 |
| **CWE-25** | Path Traversal: '/../filedir' | 2 | 3 |
| **CWE-26** | Path Traversal: '/dir/../filename' | 2 | 3 |
| **CWE-27** | Path Traversal: 'dir/../../filename' | 2 | 3 |
| **CWE-28** | Path Traversal: '..\\filedir' | 2 | 3 |
| **CWE-29** | Path Traversal: '..\\filename' | 2 | 3 |
| **CWE-30** | Path Traversal: 'dir\\..filename' | 2 | 3 |
| **CWE-31** | Path Traversal: 'dir\\....filename' | 2 | 3 |
| **CWE-32** | Path Traversal: '...' (Triple Dot) | 2 | 3 |
| **CWE-33** | Path Traversal: '....' (Multiple Dot) | 2 | 3 |
| **CWE-34** | Path Traversal: '....//' | 2 | 3 |
| **CWE-35** | Path Traversal: '.../...//' | 2 | 3 |
| **CWE-36** | Absolute Path Traversal | 2 | 3 |
| **CWE-37** | Path Traversal: '/absolute/pathname/here' | 2 | 3 |
| **CWE-38** | Path Traversal: '\\absolute\\pathname\\here' | 2 | 3 |
| **CWE-39** | Path Traversal: 'C:dirname' | 2 | 3 |
| **CWE-40** | Path Traversal: '\\\\UNC\\share\\name' (Windows UNC Share) | 2 | 3 |
| **CWE-74** | Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') | 0 | 3 |
| **CWE-75** | Failure to Sanitize Special Elements into a Different Plane (Special Element Injection) | 0 | 3 |
| **CWE-79** | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | 1 | 3 |
| **CWE-80** | Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS) | 0 | 3 |
| **CWE-85** | Doubled Character XSS Manipulations | 0 | 3 |
| **CWE-87** | Improper Neutralization of Alternate XSS Syntax | 0 | 3 |
| **CWE-88** | Improper Neutralization of Argument Delimiters in a Command ('Argument Injection') | 0 | 3 |
| **CWE-89** | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | 1 | 3 |
| **CWE-90** | Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection') | 0 | 3 |
| **CWE-91** | XML Injection (aka Blind XPath Injection) | 0 | 3 |
| **CWE-93** | Improper Neutralization of CRLF Sequences ('CRLF Injection') | 0 | 3 |
| **CWE-94** | Improper Control of Generation of Code ('Code Injection') | 2 | 3 |
| **CWE-95** | Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') | 2 | 3 |
| **CWE-96** | Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection') | 0 | 3 |
| **CWE-98** | Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') | 2 | 3 |
| **CWE-99** | Improper Control of Resource Identifiers ('Resource Injection') | 0 | 3 |
| **CWE-200** | Exposure of Sensitive Information to an Unauthorized Actor | 3 | 3 |
| **CWE-352** | Cross-Site Request Forgery (CSRF) | 1 | 3 |
| **CWE-434** | Unrestricted Upload of File with Dangerous Type | 2 | 3 |
| **CWE-522** | Insufficiently Protected Credentials | 2 | 3 |
| **CWE-564** | SQL Injection: Hibernate | 0 | 3 |
| **CWE-616** | Incomplete Identification of Uploaded File Variables (PHP) | 2 | 3 |
| **CWE-643** | Improper Neutralization of Data within XPath Expressions ('XPath Injection') | 0 | 3 |
| **CWE-646** | Reliance on File Name or Extension of Externally-Supplied File | 2 | 3 |
| **CWE-652** | Improper Neutralization of Data within XQuery Expressions ('XQuery Injection') | 0 | 3 |
| **CWE-692** | Incomplete Denylist to Cross-Site Scripting | 0 | 3 |
| **CWE-862** | Missing Authorization | 3 | 2 |
| **CWE-917** | Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') | 0 | 3 |
| **CWE-1236** | Improper Neutralization of Formula Elements in a CSV File | 2 | 3 |
| **CWE-1336** | Improper Neutralization of Special Elements Used in a Template Engine | 3 | 0 |

### Summary by Category

**Path Traversal (19 CWEs):** CWE-22 through CWE-40 — AI agents with file system access can be tricked into reading/writing sensitive paths.

**Injection Attacks (18 CWEs):** CWE-74, 75, 79, 80, 85, 87, 88, 89, 90, 91, 93, 94, 95, 96, 98, 99, 643, 652, 692, 917 — AI generates malicious content that gets interpreted by downstream systems.

**Information/Access Control (4 CWEs):** CWE-200, 522, 862, 1336 — AI may leak sensitive data or bypass authorization.

**File Handling (4 CWEs):** CWE-434, 564, 616, 646 — AI accepting/generating files without validation.

**Other (4 CWEs):** CWE-352 (CSRF), CWE-1236 (CSV Formula Injection) — AI-generated forms/data with embedded attacks.

---

## Moderately Relevant CWEs (Score 2)

These 140+ CWEs have indirect AI relevance, typically as infrastructure concerns:

- **Authentication/Session** (CWE-287, CWE-384, etc.) — AI APIs need proper auth
- **Access Control** (CWE-285, CWE-863, etc.) — AI actions need authorization
- **Information Disclosure** (CWE-209, CWE-532, etc.) — AI may leak data in errors/logs
- **Resource Management** (CWE-400, CWE-770, etc.) — AI inference needs resource limits

---

## CWEs Safe to Deprioritize for AI Security (Score 0-1)

**745 CWEs** (79% of total) have minimal AI relevance. Here's why:

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

## Security Guidance by Role

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

## Key Insights

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

### 4. AI Agents Change the Game

The emergence of AI agents with tool access (file systems, web requests, command execution) dramatically increases View 2 relevance for injection attacks. CWEs like command injection and SSRF that were traditionally server-side concerns become critical when AI can execute them directly.

### 5. Output Validation is the Key Defense

CWE-1426 (Improper Validation of Generative AI Output) is the defensive linchpin. Proper output validation mitigates most View 2 attacks. Organizations should treat all AI output as untrusted input requiring validation before use.

---

## Limitations

This analysis used rule-based classification, which has inherent blind spots:

- **Novel attack patterns** require CVE evidence we may not have seen
- **Defensive CWEs** (mitigations rather than attacks) may be underscored
- **Supply chain complexity** means attack chains span multiple CWEs
- **Rapidly evolving field** — new AI attack surfaces emerge faster than CWE entries

We recommend treating this report as a starting point, not a complete mapping. Security teams should supplement with CVE monitoring, threat intelligence, and hands-on AI security testing.

---

## Appendix A: MITRE's Official AI/ML Tagged CWEs

MITRE has explicitly tagged 17 CWEs as applicable to AI/ML systems. All 17 received non-zero scores in our analysis, confirming their relevance.

| CWE | Name | V1 | V2 | Notes |
|-----|------|----|----|-------|
| **CWE-1427** | Improper Neutralization of Input Used for LLM Prompting | 4 | 3 | Core AI weakness — Prompt Injection |
| **CWE-1426** | Improper Validation of Generative AI Output | 2 | 4 | Core AI weakness — Output Validation |
| **CWE-1434** | Insecure Setting of Generative AI/ML Model Inference Parameters | 4 | 1 | Core AI weakness — Inference Security |
| **CWE-1039** | Inadequate Detection of Adversarial Input Perturbations | 4 | 0 | Core AI weakness — Adversarial ML |
| **CWE-502** | Deserialization of Untrusted Data | 4 | 1 | Critical for model loading (pickle attacks) |
| **CWE-77** | Command Injection | 2 | 4 | Primary AI agent attack vector |
| **CWE-78** | OS Command Injection | 2 | 4 | Primary AI agent attack vector |
| **CWE-918** | Server-Side Request Forgery (SSRF) | 2 | 4 | Primary AI agent attack vector |
| **CWE-22** | Path Traversal | 3 | 3 | AI file access concerns |
| **CWE-23** | Relative Path Traversal | 2 | 3 | AI file access variant |
| **CWE-36** | Absolute Path Traversal | 2 | 3 | AI file access variant |
| **CWE-79** | Cross-site Scripting (XSS) | 1 | 3 | AI-generated web content |
| **CWE-94** | Code Injection | 2 | 3 | AI-generated code execution |
| **CWE-95** | Eval Injection | 2 | 3 | AI-generated code execution |
| **CWE-862** | Missing Authorization | 3 | 2 | AI action authorization |
| **CWE-116** | Improper Encoding or Escaping of Output | 2 | 0 | Defensive CWE — OWASP LLM02 foundation |
| **CWE-1336** | Template Engine Injection | 3 | 0 | See Appendix B |

### Additional High-Relevance CWEs (Not Tagged by MITRE)

Our analysis identified these additional CWEs with high AI relevance:

| CWE | Name | Relevance |
|-----|------|-----------|
| CWE-89 | SQL Injection | AI-generated queries are a primary attack vector |
| CWE-352 | CSRF | AI-generated forms need CSRF protection |
| CWE-200 | Information Exposure | AI systems leak sensitive data |
| CWE-434 | Unrestricted File Upload | AI file handling concerns |
| CWE-829 | Untrusted Functionality Inclusion | AI supply chain (model dependencies) |

---

## Appendix B: Case Study — CVE-2024-34359 ("Llama Drama")

This case study demonstrates how traditional CWEs apply to AI systems in non-obvious ways.

### The Vulnerability

A critical vulnerability (CVSS 9.7) in [llama-cpp-python](https://github.com/abetlen/llama-cpp-python/security/advisories/GHSA-56xg-wfcc-g829) demonstrated why CWE-1336 (Template Engine Injection) matters for AI:

- **The Attack:** LLM model files (.gguf format) contain chat template metadata processed by Jinja2
- **The Flaw:** llama-cpp-python processed these templates *without sandboxing*
- **The Impact:** A malicious model file could execute arbitrary code when loaded
- **The Scale:** Over 6,000 AI models on HuggingFace were potentially weaponizable

This is a **supply chain attack on AI systems** — you download a model from HuggingFace, and it runs code on your machine.

### Lessons Learned

| Lesson | Implication |
|--------|-------------|
| **CVE evidence reveals AI relevance** | Rule-based classification misses real-world attack patterns |
| **Template engines are AI attack surface** | Model metadata, chat templates, and prompt templates need sandboxing |
| **Supply chain extends beyond pickle** | CWE-502 (deserialization) isn't the only model loading risk |

### Recommendations

1. **Audit template engine usage** in AI pipelines—especially when processing external model files
2. **Sandbox all template processing** that handles model metadata or chat templates
3. **Don't dismiss "generic" CWEs** — their AI relevance may be through non-obvious attack chains
4. **Track CVEs in AI libraries** — they reveal attack patterns faster than theoretical analysis

---

## Appendix C: Classification Statistics

### Score Distribution

**View 1 (Attacks ON AI):**

| Score | Count | Percentage |
|-------|-------|------------|
| 0 | 761 | 80.6% |
| 1 | 4 | 0.4% |
| 2 | 171 | 18.1% |
| 3 | 4 | 0.4% |
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
| Not Applicable | 745 |
| Infrastructure | 119 |
| Output Validation | 49 |
| Agent/Autonomous Systems | 25 |
| Supply Chain | 2 |
| General | 1 |
| Model Security | 1 |
| Prompt Injection | 1 |
| Inference Security | 1 |

---

## References

- [CWE Official Site](https://cwe.mitre.org/)
- [MITRE ATLAS](https://atlas.mitre.org/) — Adversarial Threat Landscape for AI Systems
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP LLM02: Insecure Output Handling](https://genai.owasp.org/llmrisk2023-24/llm02-insecure-output-handling/)
- [CVE-2024-34359: Llama Drama](https://checkmarx.com/blog/llama-drama-critical-vulnerability-cve-2024-34359-threatening-your-software-supply-chain/) — Template injection in llama-cpp-python
- [CWE-AI-METHODOLOGY.md](CWE-AI-METHODOLOGY.md) — Full methodology documentation
- [AI-ATTACK-SURFACE-MODEL.md](AI-ATTACK-SURFACE-MODEL.md) — Detailed attack surface analysis

---

*Report generated as part of the CWE AI Relevance Classification Project*
*Cloud Security Alliance DataSets Repository*
