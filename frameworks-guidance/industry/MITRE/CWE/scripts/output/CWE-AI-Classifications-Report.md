# CWE AI Relevance Analysis Report

*Generated: 2025-12-30 20:04:49*

## Summary

- **Total CWEs Analyzed**: 944
- **MITRE AI/ML Tagged**: 17
- **AI Relevant (score >= 2)**: 199
- **Highly AI Relevant (score >= 3)**: 57

## Score Distribution

### View 1: Attacks ON AI

| Score | Count | Percentage |
|-------|-------|------------|
| 0 | 761 | 80.6% |
| 1 | 4 | 0.4% |
| 2 | 171 | 18.1% |
| 3 | 4 | 0.4% |
| 4 | 4 | 0.4% |

### View 2: Attacks VIA AI

| Score | Count | Percentage |
|-------|-------|------------|
| 0 | 746 | 79.0% |
| 1 | 119 | 12.6% |
| 2 | 27 | 2.9% |
| 3 | 48 | 5.1% |
| 4 | 4 | 0.4% |

## Category Distribution

| Category | Count |
|----------|-------|
| Not Applicable | 745 |
| Infrastructure | 119 |
| Output Validation | 49 |
| Agent/Autonomous Systems | 25 |
| Supply Chain | 2 |
| Model Security | 1 |
| Prompt Injection | 1 |
| Inference Security | 1 |
| General | 1 |

## Top 10 CWEs: Attacks ON AI (View 1)

| CWE | Name | Score | Reasoning |
|-----|------|-------|-----------|
| CWE-502 | Deserialization of Untrusted Data | 4 | Critical for AI systems. Malicious model files (pickle) can execute code when deserialized. Major ve... |
| CWE-1039 | Inadequate Detection or Handling of Adve | 4 | Directly describes attacks ON ML recognition systems using adversarial inputs designed to cause misc... |
| CWE-1427 | Improper Neutralization of Input Used fo | 4 | Canonical attack ON LLMs - directly targets prompt processing to manipulate model behavior, extract ... |
| CWE-1434 | Insecure Setting of Generative AI/ML Mod | 4 | Directly about insecure configuration of AI model inference parameters. Attackers can exploit miscon... |
| CWE-22 | Improper Limitation of a Pathname to a R | 3 | Path traversal can access model files, training data, configuration. Tagged by MITRE as AI/ML applic... |
| CWE-200 | Exposure of Sensitive Information to an  | 3 | Information exposure can leak model architecture, training data, prompts, or inference details. |
| CWE-862 | Missing Authorization | 3 | Missing authorization in AI systems can allow unauthorized model access, training data access, or in... |
| CWE-1336 | Improper Neutralization of Special Eleme | 3 | Model files contain executable metadata (e.g., Jinja2 chat templates in GGUF). CVE-2024-34359 demons... |

## Top 10 CWEs: Attacks VIA AI (View 2)

| CWE | Name | Score | Reasoning |
|-----|------|-------|-----------|
| CWE-77 | Improper Neutralization of Special Eleme | 4 | Attackers want AI to generate command strings that get executed. The AI-generated command IS the att... |
| CWE-78 | Improper Neutralization of Special Eleme | 4 | Primary target for AI agent attacks. Attackers trick AI into executing shell commands - the AI actio... |
| CWE-918 | Server-Side Request Forgery (SSRF) | 4 | Critical for AI agents. Attackers want AI to make requests to internal URLs - the AI request IS the ... |
| CWE-1426 | Improper Validation of Generative AI Out | 4 | This IS the View 2 problem - AI generates unsafe output that should have been validated. Direct enab... |
| CWE-22 | Improper Limitation of a Pathname to a R | 3 | AI agents with file access can be tricked into reading/writing arbitrary paths. The AI file operatio... |
| CWE-23 | Relative Path Traversal | 3 | AI agents with file access could be tricked into unauthorized file operations. |
| CWE-24 | Path Traversal: '../filedir' | 3 | AI agents with file access could be tricked into unauthorized file operations. |
| CWE-25 | Path Traversal: '/../filedir' | 3 | AI agents with file access could be tricked into unauthorized file operations. |
| CWE-26 | Path Traversal: '/dir/../filename' | 3 | AI agents with file access could be tricked into unauthorized file operations. |
| CWE-27 | Path Traversal: 'dir/../../filename' | 3 | AI agents with file access could be tricked into unauthorized file operations. |

## Methodology

This analysis uses the Two-View Model for CWE AI relevance:

- **View 1 (Attacks ON AI)**: Weaknesses used to attack/compromise AI systems
- **View 2 (Attacks VIA AI)**: Weaknesses attackers want AI to produce/execute

See CWE-AI-METHODOLOGY.md for complete documentation.
