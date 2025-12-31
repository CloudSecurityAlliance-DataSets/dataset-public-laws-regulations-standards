# AI Attack Surface Model

This document describes a comprehensive model for understanding attack surfaces in AI systems, with particular attention to the different actors involved and their varying levels of control and responsibility.

## Overview

AI systems introduce novel attack surfaces that traditional software security models don't fully capture. This model identifies four key actors in the AI ecosystem and maps their relationships to various attack surfaces.

## Actor Hierarchy

### 1. AI Foundation Provider

**Examples**: Anthropic (Claude), OpenAI (GPT), Google (Gemini), Meta (Llama)

**Role**: Builds and trains the core AI model, provides API access or downloadable models.

**Control Level**: Highest - controls model weights, training data, core safety measures

**Responsibilities**:
- Model safety and alignment
- Training data curation and safety
- Core guardrails and refusals
- API security and rate limiting
- Built-in tool/capability security

**Attack Surfaces They Own**:
- Model vulnerabilities (jailbreaks, prompt injection at model level)
- Training data poisoning
- Model extraction/theft
- Infrastructure supporting the model

### 2. AI Platform/Application Provider

**Examples**: Cursor, Replit, Cody, Windsurf, ChatGPT interface, Claude.ai, enterprise AI platforms

**Role**: Builds applications ON TOP of foundation models, mediates user access to AI capabilities.

**Control Level**: High - controls how users interact with the AI, what tools are exposed, how prompts are constructed

**Responsibilities**:
- Application-level guardrails
- Prompt template security
- Tool/integration restrictions
- Output filtering and validation
- User authentication and authorization
- Responsible disclosure of AI-specific vulnerabilities

**Attack Surfaces They Own**:
- Prompt injection via their UI/templates
- Insecure tool configurations they provide
- Insufficient output validation
- Platform-provided integrations (their MCP servers, their plugins)

**Key Distinction**: Platform providers CAN and SHOULD implement safety measures. They have the capability to filter, restrict, and validate - and therefore bear responsibility for doing so.

### 3. End User

**Examples**: Developers using AI APIs, individuals using AI chat interfaces, enterprises deploying AI solutions

**Role**: Consumes AI capabilities, configures integrations, writes prompts, uses outputs.

**Control Level**: Medium - controls their own usage patterns, integrations, and how they use AI outputs

**Responsibilities**:
- Secure prompt construction
- Validating AI outputs before use
- Secure configuration of user-controlled integrations
- Not deploying AI-generated code without review
- Understanding risks of their integrations

**Attack Surfaces They Own**:
- User-configured MCP servers
- User-directed web browsing
- User's own API integrations
- How they deploy AI-generated artifacts

### 4. Third-Party Data/Service Provider

**Examples**: Airtable, GitHub, Salesforce, web APIs, databases, external services accessed via MCP

**Role**: Provides data or services that AI systems query or integrate with.

**Control Level**: Limited - they control their own service but have no visibility into how AI uses their data

**Responsibilities**:
- Standard API security
- Data integrity within their platform
- NOT responsible for prompt injection in their data (they are AI-unaware)

**Attack Surfaces**:
- Their data could contain prompt injection payloads (but this is the User or Platform's responsibility to handle)
- Their APIs could be abused by AI (rate limiting, access control)

**Key Distinction**: Third-party providers generally cannot be held responsible for AI-specific attacks like prompt injection in their data. They are "AI-unaware" - their data wasn't designed to be consumed by AI systems.

---

## Trust Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Foundation Provider                        │
│                  (Anthropic, OpenAI, etc.)                      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Foundation Trust                         │ │
│  │  - Model weights and behavior                               │ │
│  │  - Training data                                            │ │
│  │  - Core safety measures                                     │ │
│  │  - Built-in capabilities (web search, code execution)       │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 AI Platform/Application Provider                 │
│                   (Cursor, Replit, Claude.ai)                   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Platform Trust                           │ │
│  │  - Prompt templates and system prompts                      │ │
│  │  - Tool configurations                                      │ │
│  │  - Output filtering                                         │ │
│  │  - Platform-provided integrations                           │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          End User                                │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                      User Trust                             │ │
│  │  - User prompts                                             │ │
│  │  - User-configured MCP servers                              │ │
│  │  - User integrations                                        │ │
│  │  - Deployment of AI outputs                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                Third-Party Data/Service Providers                │
│                  (Airtable, GitHub, Web APIs)                   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  External/Untrusted                         │ │
│  │  - Data content (may contain prompt injection)              │ │
│  │  - API responses                                            │ │
│  │  - Web content                                              │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Four Attack Surfaces

### Surface 1: Supporting Infrastructure

Traditional software infrastructure that hosts and supports AI systems.

| Actor | Examples | CWE Coverage |
|-------|----------|--------------|
| Foundation Provider | Anthropic's servers, API gateways, databases | Well covered |
| Platform Provider | Cursor's servers, authentication systems | Well covered |
| End User | User's self-hosted LLM server, local inference | Well covered |

**Assessment**: This is traditional software security. Existing CWEs cover this well. Not AI-specific.

### Surface 2: The AI System Core

The AI model itself and direct attacks on AI behavior.

| Attack Type | Description | CWE Coverage |
|-------------|-------------|--------------|
| Prompt Injection | Manipulating AI via crafted inputs | Poorly covered (CWE-1427) |
| Adversarial Inputs | Inputs designed to cause misclassification | Poorly covered (CWE-1039) |
| Jailbreaks | Bypassing safety measures | Not covered |
| Model Extraction | Stealing model weights/behavior | Not covered |
| Training Data Poisoning | Corrupting training data | Not covered |

**Assessment**: This is where AI changes the game. Very few CWEs exist for these attacks.

**Recursive Risk**: AI Foundation Providers increasingly use their own AI to build and debug their AI. Anthropic has documented feeding error screenshots to Claude to fix issues. This creates recursive risk:
- Attack training data → affects AI behavior → AI helps debug production code → introduces vulnerability → affects all users

### Surface 3: AI-Controlled/Generated Systems

Systems that AI creates, configures, or manages.

| Context | Description | Example |
|---------|-------------|---------|
| AI Company Operations | AI helping build/run AI infrastructure | AI debugging production, auto-scaling |
| Platform Operations | AI managing platform systems | AI-generated configs, automated responses |
| End User Systems | Code/configs AI generates for users | AI-written application code, Terraform configs |

**Attack Types**:

1. **Direct AI Attacks** - Attacker interacts with AI, AI produces attack immediately
   - AI executes command injection → immediate system compromise
   - AI generates XSS → immediate browser execution
   - AI makes SSRF request → immediate internal network access
   - *The AI output IS the attack*

2. **Indirect/Poisoning Attacks** - Attacker manipulates AI knowledge, victim gets vulnerable output later
   - Training data contains insecure code patterns
   - Web search SEO'd to return vulnerable tutorials
   - Malicious library gets recommended
   - *AI becomes unwitting distributor of vulnerabilities*

**Assessment**: CWEs apply to the OUTPUT (the generated code/config), but AI is the novel attack vector. Impact varies:
- High impact: Supply chain attacks (malicious imports), RCE patterns
- Lower impact: Minor vulnerabilities requiring specific conditions

### Surface 4: AI Knowledge & Supply Chain

Sources of information and capabilities that AI relies on.

| Scope | Controller | Trust Level | Examples |
|-------|------------|-------------|----------|
| Foundation-managed | AI Provider | Highest | Training data, built-in web search, built-in code execution |
| Platform-managed | Platform Provider | High | Platform-provided plugins, platform MCP servers |
| User-configured | End User | Medium | User's MCP servers, user-directed browsing |
| External/Third-party | Third-party | Low | Airtable data, web pages, API responses |

**Key Distinctions**:
- Built-in Claude web search = Anthropic's responsibility to handle safely
- Platform-provided GitHub integration = Platform's responsibility
- User's MCP web search server = User accepts the risk
- Airtable returning data with prompt injection = User/Platform must handle, not Airtable's fault

---

## Responsibility Matrix

| Attack Surface | Foundation Provider | Platform Provider | End User | Third-Party |
|----------------|--------------------|--------------------|----------|-------------|
| Infrastructure | Own infra | Own infra | Own infra | Own infra |
| AI Core | Full responsibility | Report vulnerabilities | Report issues | N/A |
| AI Outputs (Direct) | Core safety | Output filtering | Validate before use | N/A |
| AI Outputs (Indirect) | Training data safety | Integration safety | Review AI output | Not responsible |
| Knowledge Sources | Built-in sources | Platform integrations | User integrations | Data integrity only |

---

## Implications for CWE Classification

When evaluating a CWE for AI relevance, consider:

1. **Which actors are affected?**
   - Does this affect Foundation Providers differently than End Users?
   - Does the Platform Provider have responsibility to mitigate?

2. **Which attack surface?**
   - Infrastructure (traditional security)
   - AI Core (novel, poorly covered)
   - AI Outputs (CWEs apply to output, AI is vector)
   - Knowledge/Supply Chain (trust boundary dependent)

3. **Direct vs Indirect attack?**
   - Direct: AI output IS the attack (score higher)
   - Indirect: AI teaches/distributes vulnerability (consider impact)

4. **Who bears responsibility?**
   - If Third-party data causes the issue, responsibility falls on User/Platform
   - Platform Providers have capability and therefore responsibility to filter

---

## References

- MITRE CWE: https://cwe.mitre.org/
- MITRE ATLAS: https://atlas.mitre.org/
- OWASP Top 10 for LLM: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Anthropic Claude Documentation: https://docs.anthropic.com/
- Model Context Protocol: https://modelcontextprotocol.io/

---

*Document created: December 2024*
*Part of the CWE AI Relevance Classification Project*
