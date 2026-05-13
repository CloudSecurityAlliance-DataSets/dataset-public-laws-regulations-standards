# CWE Analysis Plugin Design

**Date**: 2026-03-25
**Status**: Draft
**Plugin name**: cwe-analysis
**Target repo**: csa-plugins-official

---

## Purpose

A Claude Code plugin that helps CNAs (CVE Numbering Authorities), security researchers, and vendors assign CWEs to vulnerabilities with high quality. The plugin guides analysts through vulnerability understanding, code examination, CWE identification, chain analysis, and validation — with the analyst controlling how deep they go.

## Users

- **CNAs** assigning CWEs to CVE records
- **Security researchers** reporting vulnerabilities with accurate weakness classification
- **Vendors** triaging and classifying vulnerabilities in their products
- **Anyone** who needs to label a vulnerability with the correct CWE(s)

## Scope

Software weaknesses from the CWE Research Concepts view (CWE-1000). Hardware weaknesses (CWE-1194) are out of scope. The plugin includes AI/ML relevance scoring using the two-view classification model when the vulnerability involves AI systems.

## Key Design Decisions

1. **Analyst controls depth** — can stop after a single CWE assignment or go through full chain analysis with AI relevance scoring
2. **Quality over completeness** — a 5-point failure mode checklist catches the most common CWE assignment errors
3. **Bundled data** — ships with CWE data CSVs updated periodically, no external dependencies
4. **Code analysis capable** — assumes source code may be available and can trace vulnerable code paths
5. **Progressive disclosure** — phase files loaded on demand, not all upfront

## Plugin Structure

```
plugins/cwe-analysis/
├── plugin.json
├── LICENSE                                # Apache 2.0 (plugin code)
├── FEEDBACK.md
├── data/
│   ├── CWE-AI-Classifications.csv         # ~944 entries with two-view AI scores
│   ├── CWE-Research-Concepts-1000.csv     # Full MITRE CWE data
│   ├── MITRE-CWE-LICENSE.txt              # MITRE CWE terms of use
│   └── VERSION.txt                        # CWE data version and export date
├── scripts/
│   └── cwe-tool.py                        # Data query tool (stdlib only)
└── skills/
    └── cwe-analysis/
        ├── SKILL.md                       # Main router with progressive disclosure
        ├── phases/
        │   ├── phase-1-intake.md
        │   ├── phase-2-code-analysis.md
        │   ├── phase-3-cwe-identification.md
        │   ├── phase-4-chain-analysis.md
        │   ├── phase-5-validation.md
        │   └── phase-6-report.md
        └── references/
            ├── confidence-framework.md
            ├── quality-framework.md
            ├── abstraction-guide.md
            ├── chain-patterns.md
            └── ai-relevance-guide.md
```

## Data Bundle

Two CSV files in `data/`:

### CWE-AI-Classifications.csv (~944 rows as of 2026-01)

The classification output from the dataset repo's `cwe-ai classify` tool. Columns:

- CWE_ID, Name, MITRE_AI_Tagged, View1_Score, View2_Score, Max_Score
- Is_AI_Relevant, AI_Category, Attack_Type, Attack_Surface
- View1_Reasoning, View2_Reasoning, AI_Impact
- Description, Source_View

### CWE-Research-Concepts-1000.csv (~944 rows as of 2026-01)

Full MITRE CWE data. All columns from MITRE's export:

- CWE-ID, Name, Weakness Abstraction, Status
- Description, Extended Description
- Related Weaknesses, Weakness Ordinalities, Applicable Platforms
- Background Details, Alternate Terms, Modes Of Introduction
- Exploitation Factors, Likelihood of Exploit
- Common Consequences, Detection Methods, Potential Mitigations
- Observed Examples, Functional Areas, Affected Resources
- Taxonomy Mappings, Related Attack Patterns, Notes

All columns are shipped as-is from MITRE. No trimming — fields like Modes of Introduction and Likelihood of Exploit are useful for analysis.

### VERSION.txt

Records the bundled data version:
```
CWE Version: 4.16
Export Date: 2026-01-21
Row Count: 944
Source: https://cwe.mitre.org/data/csv/1000.csv.zip
```

### MITRE-CWE-LICENSE.txt

The MITRE CWE Terms of Use covering the bundled data files. Copied from the dataset repo's `frameworks-guidance/industry/MITRE/CWE/LICENSE.txt`.

### Why CSV over JSON

CSVs total ~3.4 MB vs ~15 MB for equivalent JSON. For a plugin where Claude reads and searches data, CSV is more token-efficient. The `cwe-tool.py` script handles CSV parsing properly (quoting, multi-line fields, escaping).

### Update Process

When MITRE publishes new CWE data:
1. Run `download-cwe-items.sh` in the dataset repo
2. Run `cwe-ai classify` to regenerate classifications
3. Copy the two CSVs into the plugin's `data/` directory
4. Update `data/VERSION.txt` with the new version, date, and row count

## Scripts

### cwe-tool.py

A single Python script with subcommands. Uses only stdlib (`csv`, `argparse`, `json`, `os`, `sys`). Resolves the data directory via `os.path.dirname(os.path.abspath(__file__))` navigating to `../data/`.

**Invocation from SKILL.md:** The skill instructs Claude to run the script using the plugin root path:

```
python3 <plugin-root>/scripts/cwe-tool.py <subcommand> [args]
```

Where `<plugin-root>` is resolved from the SKILL.md file's location (`../../`).

**Subcommands:**

```
python3 cwe-tool.py lookup <CWE-ID>
```
Look up a CWE by ID. Returns all fields from both CSVs: description, abstraction level, related weaknesses, mitigations, observed examples, AI relevance scores.

```
python3 cwe-tool.py search "<keywords>"
```
Keyword search across name and description fields. Returns matching CWE IDs with names, abstraction levels, and brief descriptions. Supports multiple keywords (AND logic).

```
python3 cwe-tool.py candidates [OPTIONS]
```
Structured search with filters. Supported flags:
- `--impact "<impact>"` — filter by consequence/impact type (e.g., "code execution", "data leak")
- `--abstraction <level>` — filter by abstraction level (Pillar, Class, Base, Variant)
- `--min-ai-score <n>` — filter by minimum AI relevance score (0-4)
- `--category "<category>"` — filter by AI category (e.g., "Agent/Autonomous Systems", "Supply Chain")
- `--attack-surface "<surface>"` — filter by attack surface (Infrastructure, AI Core, AI Outputs, Supply Chain)

Returns candidates sorted by specificity (Variant > Base > Class > Pillar).

```
python3 cwe-tool.py chain <CWE-ID> <CWE-ID> [<CWE-ID> ...]
```
Given 2+ CWE IDs, show their descriptions, how they relate to each other (using Related Weaknesses field), and whether they form a valid causal chain. Includes AI relevance scores if applicable.

```
python3 cwe-tool.py ai-relevant [--min-score 2]
```
List all CWEs with AI relevance scores at or above the threshold. Useful for Phase 3 when the vulnerability involves AI systems.

**Output format:** Human-readable text by default, `--json` flag for structured output on all subcommands.

## SKILL.md Specification

### YAML Frontmatter

```yaml
---
name: cwe-analysis
description: Assign CWEs to vulnerabilities, analyze weakness chains, validate CWE mappings, and assess AI relevance. Use when the analyst wants to classify a vulnerability with CWE identifiers, review existing CWE assignments, build vulnerability chains, or understand which CWEs apply to a security issue.
---
```

### Scope

Software weaknesses from the CWE Research Concepts view (CWE-1000). Hardware CWEs are out of scope.

### Teaching Mode

On by default — explain reasoning, name CWE abstraction patterns, point out common mapping mistakes. If the analyst says "skip teaching" or "expert mode", suppress teaching annotations and produce only analytical output.

In teaching mode, include links to CWE documentation pages: `https://cwe.mitre.org/data/definitions/<CWE-ID>.html`

### Tool Access

This plugin works primarily with local code and bundled data. No web access is required. The plugin uses:
1. **`cwe-tool.py`** — query bundled CWE data
2. **File reading** — examine source code when available
3. **Grep/search** — trace code paths in the codebase

Web access is optional — if available, it can be used to check CWE pages on mitre.org for the latest information, but the plugin functions fully offline.

### Workflow Routing

Ask the analyst what they want to do:

**Option 1: Full Workflow** — Walk through all phases. Read each phase file as you reach it. Read `references/confidence-framework.md` before starting Phase 3.

1. **Phase 1 — Intake**: Read `phases/phase-1-intake.md` → understand the vulnerability
   - **Pause**: "Here's my understanding of the vulnerability. Anything to correct?"
2. **Phase 2 — Code Analysis**: Read `phases/phase-2-code-analysis.md` → examine the code path (optional — skip if no code available)
   - **Pause**: "Here's what I found in the code. Does this match your understanding?"
3. **Phase 3 — CWE Identification**: Read `phases/phase-3-cwe-identification.md`, `references/abstraction-guide.md`, and `references/confidence-framework.md` → find candidate CWEs
   - **Pause**: "Here are my top candidates. Do any miss the mark?"
4. **Phase 4 — Chain Analysis**: Read `phases/phase-4-chain-analysis.md` and `references/chain-patterns.md` → build the weakness chain (optional — analyst can stop at single CWE)
   - **Pause**: "Here's the full chain. Does the causal flow make sense?"
5. **Phase 5 — Validation**: Read `phases/phase-5-validation.md` and `references/quality-framework.md` → quality checks
6. **Phase 6 — Report**: Read `phases/phase-6-report.md` → generate final assignment

**Option 2: Specific Phase** — Jump to a phase. Ask which one and proceed.

**Option 3: Continue Previous** — Resume from a prior session. Ask what they have so far.

### Important

- **Tag every CWE assignment with a confidence level** — use the confidence framework in `references/confidence-framework.md`
- **Never assign a CWE without justification** — every CWE choice must reference how the weakness description matches the vulnerability
- **Always check for more specific CWEs** — if you're about to assign a Class, search for Base or Variant children first
- **Never use discouraged CWEs** — CWE-20 (Improper Input Validation), CWE-NVD-noinfo, and similar over-broad entries are not acceptable unless no better option exists, and in that case explain why
- **Pause between phases** — let the analyst review, correct, and add domain knowledge
- **Label all AI inferences** — prefix with "AI assessment:" to distinguish from code-derived or analyst-provided facts
- **Tag chain links independently** — each link in a weakness chain may have a different confidence level
- **Skilled analysts will steer you** — follow their lead on domain-specific knowledge

### Feedback and Bug Reports

Direct analysts to file issues at:
https://github.com/CloudSecurityAlliance/csa-plugins-official/issues

Mention proactively if something goes wrong or at the end of a completed analysis.

## Workflow Phases

### Phase 1 — Intake

**Purpose:** Understand what the analyst knows about the vulnerability.

**Process:**
- What is the affected software/system?
- How is the vulnerability triggered? (input, preconditions, attack scenario)
- What's the impact? (code execution, data leak, DoS, privilege escalation, etc.)
- Is source code available? Where?
- Is there an existing CVE ID or CWE assignment to review/improve?
- Is this an AI/ML system? (determines whether AI relevance scoring applies later)

**Output:** Structured vulnerability summary.

**Pause:** "Here's my understanding of the vulnerability. Anything to correct?"

### Phase 2 — Code Analysis

**Purpose:** Examine the actual code path. Optional — analyst can skip if no code is available.

**Process:**
- Trace the vulnerable code path from input to impact
- Identify where validation/sanitization is missing or insufficient
- Note trust boundaries crossed (user input → internal API → database, etc.)
- Identify the root cause vs. the symptom in the code
- Mark specific lines/functions where each weakness manifests

**Output:** Annotated code path with weakness points marked.

**Pause:** "Here's what I found in the code. Does this match your understanding?"

### Phase 3 — CWE Identification

**Purpose:** Search the bundled data for candidate CWEs.

**Prerequisites:** Read `references/confidence-framework.md` before starting this phase.

**Process:**
- Use `cwe-tool.py search` and `cwe-tool.py candidates` to find matches based on the weakness type, impact, and code patterns from Phases 1-2
- Apply the abstraction guide — find the most specific CWE that fits
- Use `cwe-tool.py lookup` to examine top candidates in detail
- Check Related Weaknesses and Observed Examples for confirmation
- If AI system: check MITRE AI/ML tags and AI relevance scores via `cwe-tool.py ai-relevant`
- **Tag each candidate with a confidence level** from the confidence framework
- Present 3-5 candidates ranked by fit, with confidence tag and reasoning for each
- Watch for over-confidence anti-patterns, especially "First Match" and "Name Match" traps

**Output:** Ranked candidate list with confidence tags and justification.

**Pause:** "Here are my top candidates with confidence levels. Do any miss the mark, or should any confidence levels be adjusted?"

### Phase 4 — Chain Analysis

**Purpose:** Build the weakness chain. Optional — analyst can stop at single CWE.

**Process:**
- Map: root cause → enabling weakness → exploited weakness → impact
- Use `cwe-tool.py chain` to verify relationships between candidate CWEs
- Each link gets its own CWE with the causal relationship explained
- **Tag each chain link with an independent confidence level** — root cause may be Confirmed from code while an enabling weakness is Inferred
- Check chain against common patterns in chain-patterns.md reference
- If AI-relevant: overlay two-view scores and attack surface mapping from ai-relevance-guide.md
- Express relationships using CWE vocabulary (CanPrecede, CanFollow, Requires, PeerOf)

**Output:** Ordered chain with CWEs, confidence tags per link, relationships, and narrative.

**Pause:** "Here's the full chain with confidence levels per link. Does the causal flow make sense?"

### Phase 5 — Validation

**Purpose:** Run the assignment through the quality framework.

**Process:** Check each of the 5 failure modes (from quality-framework.md):

1. **Too abstract?** — Is there a more specific CWE? Search for children of the assigned CWE.
2. **Wrong abstraction level?** — Verify Pillar/Class/Base/Variant is appropriate per abstraction-guide.md.
3. **Missing chain links?** — Any causal gaps between root cause and impact?
4. **Stale mapping?** — Are there newer CWEs (especially post-2023 AI CWEs) that fit better?
5. **Cause vs. consequence confusion?** — Is each CWE in the right role in the chain?

**Output:** Validation report — pass/flag for each check with explanation.

**Flow:** Feeds directly into Phase 6 unless issues found. If flagged, presents issues and asks analyst whether to revise or accept.

### Phase 6 — Report

**Purpose:** Generate the final CWE assignment.

**Output includes:**
- Primary CWE with confidence level (the single best weakness identifier for a CVE record)
- Full chain with per-link confidence levels (if Phase 4 was completed)
- Justification for each CWE choice, citing specific evidence
- Abstraction level confirmation
- AI relevance assessment (if applicable)
- Links to CWE documentation pages for each assigned CWE
- Any **Uncertain** assignments with competing candidates and what would resolve them
- Formatted for direct use in CVE records

**Output options:** Display in terminal, or write to a file (analyst's choice).

## Reference Materials

### confidence-framework.md

Confidence levels for CWE assignments, adapted from the incident-analysis plugin's provenance framework. Every CWE assignment and chain link must be tagged with one of these levels.

| Level | Meaning | When to Use | Example |
|-------|---------|-------------|---------|
| **Confirmed** | Code analysis proves this exact weakness exists | Direct evidence from source code inspection | Traced unsanitized user input through to SQL query construction — this is CWE-89 |
| **Strong** | Multiple evidence types agree on this CWE | Impact matches, description matches, observed examples match | Impact is command execution via user input, CWE-78 description and examples both fit, code shows shell invocation |
| **Supported** | Evidence supports this CWE but not definitively | Description matches well, but code wasn't available or fully traced | Vulnerability description matches CWE-502 deserialization, but couldn't inspect the loading code directly |
| **Inferred** | Logical deduction from other confirmed facts | Deduction, not direct evidence | "The attack achieves RCE through model loading" — likely CWE-502, but could be another deserialization path |
| **Best Fit** | Closest available CWE, but imperfect match | No CWE precisely describes this weakness | Vulnerability involves a novel AI attack pattern; CWE-1039 is closest but doesn't capture the full mechanism |
| **Uncertain** | Multiple CWEs are plausible, can't determine which | Insufficient information to differentiate | Could be CWE-22 (path traversal) or CWE-73 (external control of filename) — need more detail about path construction |

**Usage Rules:**
1. Every CWE assignment in the analysis must have a confidence tag
2. AI-generated assessments are always tagged and prefixed with "AI assessment:"
3. Chain links are tagged independently — root cause may be Confirmed while an enabling weakness is Inferred
4. When uncertain between two adjacent levels, default to the lower one
5. **Uncertain** assignments must list the competing candidates and what information would resolve the ambiguity
6. Confidence can be upgraded during analysis — if Phase 2 (code analysis) confirms what Phase 1 (intake) only suggested, update the tag

**Over-Confidence Anti-Patterns:**

1. **"Impact Implies Weakness" Trap** — "The vulnerability allows code execution, therefore it must be CWE-94 (Code Injection)." Impact describes what happens, not what the weakness is. Code execution can result from command injection, deserialization, buffer overflow, or many other weaknesses.

2. **"Name Match" Trap** — Matching a vulnerability to a CWE because the names sound similar without verifying the technical description matches. "Server-Side Template Injection" sounds like CWE-1336 but verify the actual mechanism.

3. **"First Match" Trap** — Accepting the first CWE that seems reasonable without checking for more specific alternatives. CWE-74 (Injection) matches almost any injection vulnerability — but CWE-89, CWE-78, CWE-79 etc. are almost always more appropriate.

4. **"Vendor Says So" Trap** — Accepting a vendor's CWE assignment without independent verification. Vendors may assign overly broad CWEs to minimize perceived severity, or wrong CWEs due to limited CWE expertise.

### quality-framework.md

The 5 failure modes as an actionable checklist. For each:
- What it looks like (concrete example of the mistake)
- How to detect it (what to check)
- How to fix it (what to do instead)
- Real-world example from actual CVEs where this went wrong

### abstraction-guide.md

MITRE's CWE abstraction hierarchy:
- Pillar → Class → Base → Variant definitions with when each is appropriate
- Decision tree for selecting the right level
- List of discouraged CWEs (CWE-20, CWE-NVD-noinfo, etc.) with what to use instead
- MITRE's mapping guidance for CNAs

### chain-patterns.md

Common multi-CWE vulnerability patterns:
- Web application chains (input validation → injection → execution)
- AI-specific chains (prompt injection → output validation failure → command injection)
- Supply chain chains (deserialization → code execution via malicious artifacts)
- Authentication/authorization chains
- How to express relationships using CWE vocabulary (CanPrecede, CanFollow, Requires, PeerOf)

### ai-relevance-guide.md

Condensed from the dataset repo's methodology docs:
- The two-view model (Attacks ON AI vs Attacks VIA AI)
- Scoring scale (0-4) with examples
- The four attack surfaces (Infrastructure, AI Core, AI Outputs, Supply Chain)
- When to apply AI relevance scoring (decision criteria)
- How to read the AI Classifications data

## plugin.json

```json
{
  "name": "cwe-analysis",
  "description": "CWE assignment and vulnerability chain analysis for CNAs, security researchers, and vendors. Guides analysts through vulnerability understanding, code examination, CWE identification, chain mapping, and quality validation.",
  "version": "0.1.0",
  "author": {
    "name": "Kurt Seifried",
    "email": "kseifried@cloudsecurityalliance.org"
  },
  "skills": [
    "skills/cwe-analysis/SKILL.md"
  ]
}
```

## FEEDBACK.md

Follow the same template as the incident-analysis plugin. Issue prefix: `[cwe-analysis]`. Direct users to:
https://github.com/CloudSecurityAlliance/csa-plugins-official/issues

## Quality Bar

A CWE assignment from this plugin should:
- Use the most specific CWE that accurately describes the weakness (Base or Variant preferred)
- Never use discouraged/deprecated CWEs
- Include justification that references the CWE description and how it matches the vulnerability
- Identify chain relationships when multiple weaknesses are involved
- Flag AI relevance when the vulnerability involves AI/ML systems
- Pass all 5 validation checks in the quality framework

## Open Questions

1. Should the report phase output in a specific format for CVE record submission (e.g., JSON matching CVE 5.0 schema)?
2. Should we include a phase for cross-referencing against CAPEC (attack patterns) or MITRE ATT&CK?
