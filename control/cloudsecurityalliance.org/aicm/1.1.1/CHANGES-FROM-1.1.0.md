# AICM 1.1.0 → 1.1.1: what changed

A complete account of the differences between AICM v1.1.0 and v1.1.1, derived by
diffing the two publisher workbooks and the two extractions in this repository.

Companion to [`README.md`](README.md), which is the summary. This file is the
evidence: it carries the full before/after text of every changed cell, because
the source workbooks are gitignored and this report is therefore the only
in-repository record of what the 1.1.0 text actually said.

| | |
|---|---|
| **Compared** | `AICMv1.1.0-generated_at_2026_06_18.xlsx` → `AICMv1.1.1-generated_at_2026_07_22.xlsx` |
| **Extractions** | [`../1.1.0/aicm-1.1.0.json`](../1.1.0/aicm-1.1.0.json) → [`aicm-1.1.1.json`](aicm-1.1.1.json) |
| **Report date** | 2026-08-11 |

---

## Bottom line

**1.1.1 is a genuine patch release. No control identity changed.** All 247
control IDs, titles, specifications, control types, ownership assignments,
architectural relevance, lifecycle relevance and threat categories are identical
to 1.1.0, as is the entire Auditing Guidelines sheet and the LLM Taxonomy. A
1.1.0 control reference migrates to 1.1.1 by string match — the opposite of the
1.0.3 → 1.1.0 situation, which renumbered 54 identifiers in place. See
[`../VERSIONING.md`](../VERSIONING.md).

Substantively, the release does four things:

| | Change | Weight |
|---|---|---|
| 1 | **Two cross-framework mapping blocks added** — AIUC-1, and NIST restored and widened to the AI RMF | the substance of the release |
| 2 | **Three Model Provider implementation guidelines rewritten** — `GRC-01`, `IAM-13`, `IAM-18` | real, and one warrants a question to CSA |
| 3 | **One AI-CAIQ question de-duplicated** — `SEF-06.1` | small, long-standing defect finally fixed |
| 4 | **Interpretive notes added to a sheet this repo does not extract** | small in size, large in consequence |

**Not announced.** CSA replaced the workbook inside the "AICM v1.1" bundle
without changing the bundle name, the artifact-page version label, or the stated
release date of 06/22/2026. The only outward signals are the filename version
token and the JSON stamp in cell A1. Anyone who downloaded "AICM v1.1" before
roughly 2026-07-22 holds 1.1.0; after, 1.1.1. Both are branded v1.1.

---

## Method

Two independent passes, which agree:

1. **Workbook diff** — every cell of all nine worksheets, whitespace-normalised.
   This is the authoritative pass: it sees sheets the extraction does not read.
2. **Extraction diff** — every field of all 247 controls in the two committed
   JSON files.

The extraction diff found changes in exactly two fields
(`implementation_guidelines`, `caiq_questions`) plus the added mapping keys. The
workbook diff found those same changes and three further sheets. Neither found
anything the other missed within its scope, which is the cross-check.

### Cell accounting

**3,598 differing cells** across the workbook:

| Sheet | Dimensions | Differing | What |
|---|---|---:|---|
| `Scope Applicability (Mappings)` | 270×13 → 270×19 | **3,454** | the two new framework blocks, plus header rows |
| `Change Log` | 19×5 | 52 | three new v1.1.1 rows, pushing older rows down |
| `Introduction` | 81×4 | 44 | new notes, plus row shifts from the insertion |
| `Acknowledgments` | 14×28 | 31 | two new contributor sections |
| `Implementation Guidelines` | 270×10 | 6 | three MP cells, version stamp, copyright |
| `AICM` | 270×30 | 3 | version stamp, title, copyright only |
| `Auditing Guidelines` | 269×9 | 3 | version stamp, title, copyright only |
| `AI-CAIQ` | 342×6 | 3 | one question, version stamp, copyright |
| `LLM Taxonomy` | 86×4 | 2 | version stamp, copyright only |

Which decomposes as:

- **9** — the `{"specification_version":"1.1.x"}` stamp in cell A1, once per sheet
- **3,453** — the mappings sheet excluding its stamp
- **136** — everything else, itemised in full below

Sheet names, sheet order, and every sheet's row count are unchanged. No sheet was
added or removed.

---

## 1. Two mapping frameworks added

The `Scope Applicability (Mappings)` sheet goes from **13 columns to 19** — from
three frameworks to five. Each framework occupies a `Control Mapping` /
`Gap Level` / `Addendum` triple beneath a merged header.

| Framework | 1.1.0 | 1.1.1 | Column (0-indexed) |
|---|---|---|---|
| **AIUC-1 Q2 2026 Version** | — | **added** | 4 |
| BSI AI C4 | ✓ | ✓ | 4 → 7 |
| EU AI Act | ✓ | ✓ | 7 → 10 |
| ISO/IEC 42001:2023 | ✓ | ✓ | 10 → 13 |
| **NIST AI RMF + NIST AI 600-1** | — | **added** | 16 |

Note the three surviving blocks all **shifted right** by three columns to make
room for AIUC-1 at the front. This is why a parser addressing fixed column
offsets would have silently mis-attributed every mapping in the sheet — see
[Reproducing](#reproducing-this-diff).

### 1.1.0 documented these two blocks without shipping them

The repo previously recorded 1.1.0's missing NIST mappings as
`nist-ai-600-1-mappings-withdrawn`. That framing was too generous to the
"withdrawn" reading, and the `Introduction` sheet settles it. **1.1.0's own
Introduction already described a five-framework sheet**, naming both blocks that
were absent from it:

> *(1.1.0, `Introduction` r50)* This tab includes the mappings between AICM V1.1
> and numerous standards (**NIST AI 600-1 and NIST AI RMF**, BSI AIC4 Catalogue,
> ISO 42001(complemented by ISO 27001 and 27002\*), **AIUC-1**) and regulations
> (EU AI Act) control sets relevant to AI systems operating in cloud environments.

Its `Change Log` independently claimed mapping rows were added "across all four
external frameworks", and its `Acknowledgments` sheet — see
[section 4](#acknowledgments) — had no contributor section for either. So three
sheets of the 1.1.0 workbook disagreed with each other about what the release
contained.

Read together, the likelier explanation is that **1.1.0 was documented against
content it failed to ship** — a packaging or build slip — rather than a decision
to remove two frameworks. 1.1.1 is then best understood not as adding two
mappings but as *finally shipping the release 1.1.0 was described as being*. That
also explains why 1.1.1 needed no other corrections: the rest of 1.1.0 was fine.

The practical upshot for consumers is unchanged — use 1.1.1 for NIST or AIUC-1
mappings — but the label matters for how much trust the change log earns. See
[section 4](#change-log).

### The carried-over blocks

**The three carried-over blocks are unchanged in every cell for every control.**
Verified explicitly: 0 of 247 differ on BSI mapping, gap level or addendum; 0 on
EU AI Act; 0 on ISO/IEC 42001. Their JSON slugs are also unchanged, so a consumer
keying on `bsi_ai_c4`, `eu_ai_act` or `iso_iec_42001_2023` is unaffected by the
addition.

### Coverage of the new blocks

| Block | Mapped | `No Mapping` | Blank | Addendum populated |
|---|---:|---:|---:|---:|
| AIUC-1 | 143 | 103 | 1 (`MDS-13`) | 247 / 247 |
| NIST AI RMF + AI 600-1 | 137 | 110 | 0 | 231 / 247 |

### Gap levels, all five frameworks

| Framework | No Gap | Partial Gap | Full Gap |
|---|---:|---:|---:|
| BSI AI C4 | 210 | 34 | **3** |
| ISO/IEC 42001:2023 | 145 | 97 | **5** |
| EU AI Act | 50 | 112 | 85 |
| **AIUC-1** | 70 | 73 | **104** |
| **NIST AI RMF + AI 600-1** | 18 | 119 | **110** |

The two new blocks are far gappier than the two oldest. **Do not read that as the
target frameworks being weak** — CSA's own explanation, added to the
`Introduction` sheet in this same release, is that the gap is one of *scope*. Both
notes are quoted in [section 4](#4-changes-to-sheets-this-repo-does-not-extract).
In short: the AICM carries cloud infrastructure controls (CCM v4.1 lineage) that
are simply outside what NIST AI 600-1 / AI RMF and AIUC-1 set out to cover.

The per-domain pattern supports that reading. Domains that are essentially
cloud-infrastructure concerns go almost entirely `Full Gap` against AIUC-1 —
Datacenter Security 18/18, Human Resources 15/15, Infrastructure & Virtualization
9/9, Interoperability 4/4 — while AI-native domains like Model Security (1/13) and
Threat & Vulnerability Management (0/13) map well.

| Domain | n | AIUC-1 No/Part/Full | NIST No/Part/Full |
|---|---:|---:|---:|
| Audit & Assurance | 6 | 1 / 3 / 2 | 0 / 6 / 0 |
| Application & Interface Security | 15 | 8 / 6 / 1 | 0 / 12 / 3 |
| Business Continuity | 11 | 0 / 3 / 8 | 0 / 9 / 2 |
| Change Control | 9 | 3 / 3 / 3 | 0 / 8 / 1 |
| Cryptography, Encryption & Key Mgmt | 21 | 3 / 16 / 2 | 0 / 4 / 17 |
| Datacenter Security | 18 | 0 / 0 / **18** | 0 / 3 / 15 |
| Data Security & Privacy | 24 | 12 / 7 / 5 | 1 / 19 / 4 |
| Governance, Risk & Compliance | 15 | 7 / 2 / 6 | 5 / 8 / 2 |
| Human Resources | 15 | 0 / 0 / **15** | 1 / 7 / 7 |
| Identity & Access Management | 18 | 7 / 8 / 3 | 0 / 0 / **18** |
| Interoperability & Portability | 4 | 0 / 0 / **4** | 0 / 0 / **4** |
| Infrastructure & Virtualization | 9 | 0 / 0 / **9** | 1 / 1 / 7 |
| Logging and Monitoring | 16 | 6 / 5 / 5 | 0 / 0 / **16** |
| Model Security | 13 | 7 / 5 / 1 | 3 / 9 / 1 |
| Security Incident Mgmt | 10 | 6 / 1 / 3 | 2 / 8 / 0 |
| Supply Chain Mgmt | 16 | 0 / 4 / 12 | 3 / 12 / 1 |
| Threat & Vulnerability Mgmt | 13 | 7 / 6 / 0 | 1 / 8 / 4 |
| Universal Endpoint Mgmt | 14 | 3 / 4 / 7 | 1 / 5 / 8 |

### `No Mapping` is a value, not an absence

Three of the five blocks write the literal string `No Mapping` where no
counterpart control exists: AIUC-1 (103), NIST (110), and the EU AI Act (83 —
**this predates 1.1.1**, it was already so in 1.1.0 and passed unremarked).

The extraction **preserves the string verbatim** rather than folding it to `null`.
An explicit publisher finding of "we looked, there is no counterpart" is a
different fact from an unstated mapping, and collapsing them would destroy the
distinction the `gaps_in_source` machinery exists to protect.

> ⚠️ **Consumers filtering for "has a mapping" must exclude the string
> `No Mapping` as well as `null`.** 296 cells across three frameworks are
> affected. Counts are recomputed per framework into
> `source_data_notes.sentinel_values` on every parse run.

`MDS-13` (Secure Model Format) is the sole exception: its AIUC-1 mapping cell is
genuinely **blank**, while `Gap Level` says `Full Gap` and the addendum reads
"Address model-artifact protection or format integrity". It looks like an
omission where `No Mapping` was intended. The extraction does not infer that — it
emits `null` and records the cell in `source_data_notes.gaps_in_source`.

---

## 2. Three Model Provider implementation guidelines rewritten

`GRC-01`, `IAM-13`, `IAM-18` — the **only** three cells that differ across the
entire 270×10 Implementation Guidelines sheet. All three are in the
`Implementation Guidelines for Model Provider (MP)` column; no other actor column
changed for any control.

All three were defective in 1.1.0 in the same way: the Model Provider cell held
text explicitly tagged for **other** actors.

| Control | Title | 1.1.0 opened with | 1.1.0 → 1.1.1 size |
|---|---|---|---|
| `GRC-01` | Governance Program Policy and Procedures | `[Application Provider/Orchestrated Service Provider/AI Customer]` | 812 → 3,546 ch |
| `IAM-13` | Strong Authentication | `[MP]` … then `[ALL Actors - AICM - CSP]` … then `[All Actors]` | 4,620 → 2,629 ch |
| `IAM-18` | Agent Access Restriction | `[All Actors]` | 527 → 1,900 ch |

The 1.1.1 replacements drop the bracket-tag convention entirely and are written
as Model-Provider-specific guidance throughout.

### GRC-01 — Governance Program Policy and Procedures

> **Specification:** Establish, document, approve, communicate, apply, evaluate
> and maintain policies and procedures for an information governance program,
> which is sponsored by the leadership of the organization and related to AI
> systems as well. Review and update the policies and procedures at least
> annually, or upon significant changes.

The 1.1.0 text was written for the *consumer* side — "tailoring it to the
consumer's organizational goals", "outline the consumer's responsibilities …
with the AI service provider" — which is the wrong perspective for the party that
*builds* the model.

<details>
<summary><strong>1.1.0</strong> (812 chars)</summary>

```
[Application Provider/Orchestrated Service Provider/AI Customer]
1. Establish an internal AI governance policy aligned with the provider's guidelines, tailoring it to the consumer's organizational goals and regulatory requirements.

2. Integrate AI risk management into existing governance structures, specifying roles for data governance, risk management, and compliance teams focusing on AI.

3. Evaluate and approve AI use cases, ensuring they comply with established organizational ethics, data protection standards, and risk appetite.

4. Conduct reviews of AI systems and processes, including checks for data integrity, model bias, and performance.

5. Maintain documented procedures that outline the consumer's responsibilities, escalation paths, and communication protocols with the AI service provider.
```
</details>

<details>
<summary><strong>1.1.1</strong> (3,546 chars) — nine items, MP-specific</summary>

```
1. Establish a documented AI governance framework that defines clear ownership, accountability structures, and decision-making authority across all AI model activities. Ensure alignment with organizational objectives, ethical standards, and applicable regulatory requirements.

2. AI Model Lifecycle Policies and Procedures: Define and periodically review (at least annually) policies and procedures covering the full AI model lifecycle: design, development, training, fine-tuning, alignment, deployment, monitoring, and decommissioning. Include provisions for data quality, bias detection, transparency, regulatory compliance, and documented stage gates with approval checkpoints at each lifecycle phase.

3. Training Data Governance: Establish dedicated policies governing training data sourcing, provenance documentation, consent and licensing compliance, and data poisoning risk management. As the originating actor in the AI supply chain, the MP holds unique responsibility for the data on which model behaviour is founded.

4. AI-Specific Risk Assessment and Continuous Monitoring: Incorporate risk assessments specifically designed for AI systems, with defined criteria for evaluating AI-related threats including data privacy breaches, algorithmic bias, model drift, adversarial attacks, and post-deployment model drift and behavioural degradation. Implement controls and continuous monitoring mechanisms to detect and respond to these risks at the model level.

5. AI Safety, Alignment, and Responsible Release Governance: Prior to deployment establish a formal governance process for model releases, including mandatory pre-release safety evaluations, red-teaming requirements, capability thresholds that trigger additional review, and criteria for staged versus open release. Define leadership-sponsored commitments to AI safety and alignment practices, including escalation paths when a model exhibits unexpected or harmful outputs at scale.

6. Supply Chain Transparency Obligations: Define governance requirements for what the MP communicates to downstream actors (OSPs, APs, and AICs), including model cards, known limitations, intended use boundaries, prohibited use cases, and licensing terms. The MP is the originating point of the AI supply chain and carries a governance responsibility to equip downstream actors to govern their own use responsibly.

7. Model Versioning, Deprecation, and Migration Governance: Establish policies governing model versioning, backward compatibility commitments, deprecation timelines, and migration support obligations. Downstream actors depend on model stability; the MP governance program must account for the impact of model changes across the full supply chain.

8. Executive Sponsorship and Cross-Functional Resourcing: Ensure executive sponsorship and cross-functional support to provide adequate resources, expertise, and oversight for the AI governance program. Assign senior leadership accountability for AI governance outcomes, consistent with the GRC-01 control requirement for leadership-sponsored governance. Designate responsible owners for each component of the governance program.

9. Internal Stakeholder Communication and Training: Communicate governance policies, updates, and responsibilities to internal stakeholders, including model developers, data scientists, alignment researchers, and compliance teams, through regular training and awareness sessions. Ensure that all personnel involved in model development understand their obligations under the governance framework.
```
</details>

This is a clear improvement: pre-release safety evaluation, red-teaming, capability
thresholds, staged-versus-open release, training-data provenance and model
deprecation are all MP-specific obligations that had no coverage at all in 1.1.0.

### IAM-18 — Agent Access Restriction

> **Specification:** Restrict agents' access to the tools and plugins necessary
> for the activity or use case at hand, ensuring adherence to the principles of
> need-to-know and least privilege.

<details>
<summary><strong>1.1.0</strong> (527 chars)</summary>

```
[All Actors]
1. Inventory Agent tools and categorize them based:
   i. Risk of accessible resource and the operations it can perform on those resources
   ii. Sensitivity and Criticality of resources
   iii. Establish stakeholder and tool owners

2. Implement access control mechanism that authorize the agent-based system and/or authorize the user interacting with the agent-based system.

3. Implement policies and workflows to ensure users and not given access to information or privileged outside of the role requirements.
```
</details>

<details>
<summary><strong>1.1.1</strong> (1,900 chars) — five items, MP-specific</summary>

```
1. Tool and Plugin Exposure Inventory: Maintain a documented inventory of all tools, APIs, and plugins the model exposes for agent use through function-calling or tool-use capabilities. Categorise each by risk level, resource sensitivity, operational scope, and designated owner. Review and update the inventory at least annually and upon any significant change to the model's tool-use capabilities.

2. Least-Privilege Tool Access as Default: Ensure the model's default configuration enforces least-privilege tool access. No tool or plugin should be accessible to an agent unless explicitly permitted for the specific activity or use case. Tools must not be accessible by default simply because they are available. Access should be affirmatively granted per use case.

3. Technical Controls Against Privilege Escalation: Implement technical controls that prevent the model from being instructed, whether through direct prompting, prompt injection, or agentic chaining, to invoke tools or access resources beyond the scope sanctioned at instantiation. The model must not facilitate privilege escalation across single or multi-step agent interactions.

4. Downstream Tool Integration Requirements: Establish and communicate documented requirements for downstream actors (OSPs, APs) integrating tools and plugins with MP-based agents. Specify which tool categories are permitted, what access scopes are sanctioned, and what must not be exposed to agent-based systems regardless of downstream actor configuration choices.

5. Agent Authorisation Boundary Documentation: Document the authorisation boundaries within which agents built on the model are designed to operate. Make these boundaries available to downstream actors as part of model documentation, enabling OSPs and APs to design their agent architectures with accurate knowledge of what the model will and will not do at the tool-access level.
```
</details>

Also a clear improvement — prompt injection and agentic chaining as
privilege-escalation vectors are named explicitly, which the generic 1.1.0 text
did not do.

### IAM-13 — Strong Authentication ⚠️ worth a question to CSA

> **Specification:** Define, implement and evaluate processes, procedures and
> technical measures for authenticating access to systems, application and data
> assets, including multifactor authentication for at least privileged user and
> sensitive data access. Adopt digital certificates or alternatives which achieve
> an equivalent level of security for system identities.

This is the one rewrite that is not straightforwardly an improvement. Two things
to separate.

**Nothing was lost.** The 1.1.0 MP cell was 4,620 characters, of which the great
majority was a block tagged `[ALL Actors - AICM - CSP]` covering centralised
authentication, MFA scope, TOTP and hardware tokens, passwordless/FIDO2,
credential protection, continuous user authentication, SSO, and the full digital
certificate lifecycle including CRL/OCSP. That block **survives verbatim in the
same control's `cloud_service_provider` column**, where it was already duplicated
in 1.1.0 (8,626 chars, unchanged in 1.1.1). Its removal from the MP column is
de-duplication of text that was never MP-specific, not a loss of guidance. The
genuinely MP-specific part of 1.1.0 — SSO plus MFA for raw training data, model
repositories, debugging tools and ML/AIOps platforms — is **preserved and
expanded** as item 3 of the new text.

**But the new text is mostly about a different control.** Three of its four items
concern the *uniqueness and propagation of identifiers*, not authentication:

| Item | Subject |
|---|---|
| 1 | Unique Identification of AI Models and Variants |
| 2 | Model Identifier Propagation to Downstream Consumers |
| 3 | Unique Identification of Human Users … SSO + MFA ← *the only authentication item* |
| 4 | Unique Identification of Non-Human Identities in Automated Pipelines |

Items 1 and 2 restate, at greater length, what **`IAM-12` "Unique Identities"**
already says in its own MP column:

```
[MP]
1. Ensure that model versions & variants are given unique identifiers to
ensure they are identifiable when used in Agent-Based systems.

2. Provided mechanisms and procedures to provide downstream
consumers with model identifier information to be integrated with their
unique ID mechanisms.
```

**`IAM-12`'s MP guidance is byte-identical between 1.1.0 and 1.1.1** — it was not
touched. So 1.1.1 leaves the AICM with two controls whose MP guidance covers
model-and-variant identifier assignment and downstream propagation, one of which
(`IAM-13`) is titled and specified for *Strong Authentication*.

The plausible readings are that the new text was drafted against `IAM-12` and
filed under `IAM-13`, or that it was intended as a combined identity-and-
authentication block. Either way `IAM-12` should probably have been updated or
folded in at the same time. Worth raising with the working group; **recorded here
as an observation, not asserted as a defect**, since the control's own
authentication requirement *is* addressed by item 3 and the specification text is
broad enough to admit system identities.

Note also the historical trap: `IAM-12` meant **Safeguard Logs Integrity** in
1.0.3 and means **Unique Identities** in 1.1.x. Any conversation with CSA about
these two controls needs the version stated explicitly.

<details>
<summary><strong>IAM-13: 1.1.0</strong> (4,620 chars)</summary>

```
[MP]
1. Integrate SSO and ensure MFA is required to access sensitive information such as
   i. Raw Training data
   ii. Accessing Models or debugging tools that may expose sensitive information
   iii: ML/AIOps platforms (such as CI/CD, and Model Repositories).

[ALL Actors - AICM - CSP]
1. Authentication Management:
i. A centralized authentication system that can manage identities, authentication credentials, and access control permissions across all AI service components should be implemented
ii. Users that require privileged access (e.g.,administrators and IT staff) should be identified to establish stricter authentication measures
iii. Specific authentication factors and technical measures should be defined and implemented for each access level, including MF A for privileged identities and sensitive data access

2. MFA Usage Scope:
i. Sensitive Data Access: Strong authentication should be enforced at all user accounts, requiring a combination of something the user: Knows (such as a password); Has (such as a mobile device or token); Is (such as biometrics); MFA for all users should be enabled, including non-privileged users who access sensitive data.
ii. Administrative Access: MFA should be enforced for all administrative access (e.g., access to management consoles, AI lifecycle components, and other critical AI infrastructure elements). If MFA cannot be implemented in a particular situation, the risk should be formally registered
iii. Third-Party Access: MFA should be enforced for third-party access, such as through APIs or AI services, to protect against unauthorized access by external entities.

3. Second Factor Authentication: Second factor authentication should be leveraged in addition to passwords to add an extra layer of security by requiring a second factor of:
i. Time-Based One-Time Passwords (TOTPs) to allow users to generate temporary codes via email or a smartphone app synchronized with an authentication server.
ii. Hardware tokens or USB keys that generate unique codes for authentication.

4. Passwordless Authentication: Passwordless authentication solutions should be implemented that replace traditional passwords with secure alternatives such as phishing-resistant MFA and FIDO2-compliant security keys or biometrics.

5. Authentication Credentials Protection: All authentication credentials should be transmitted through secure channels (e.g., TLS/HTTPS) and never stored in plaintext but rendered unreadable in storage on all system components using strong cryptography.

6. Authentication Credentials Change Approval: Requests to change or modify authentication credentials (i.e., performing password resets, provisioning new tokens, generating new keys) should be approved only after verification of the user's identity.

7. Continuous User Authentication (CUA): CUA should be leveraged as a method of maintaining user authentication throughout their session, requiring periodic reauthentication to ensure that the user is still authorized and has not been compromised.

8. Single Sign-On (SSO): SSO should be implemented for accessing multiple services and applications with a single login credential to simplify the authentication process for users.

9. Digital Certificates: Digital certificates should be utilized for authentication and authorization purposes, especially for system identities.

10. CRL and OCSP Checks: Certificate Revocation Lists (CRLs) and Online Certificate Status Protocol (OCSP) checks should be implemented to verify the validity and revocation status of digital certificates.

11. Certificate Lifecycle: The lifecycle of digital certificates should be securely managed including issuance, renewal, and revocation.

12. Certificate Storage: Digital certificates should be stored securely, using encryption and access control mechanisms.

13. Authentication Usage Monitoring:
i. All authentication mechanisms and enabled features should be properly installed, configured, and authentication logs monitored for the desired and expected results.
ii. MFA, credentials, and digital certificate usage patterns should be continuously monitored and reviewed to proactively identify potential vulnerabilities or compromises.

[All Actors]
1. Implement risk-based authentication controls that evaluate host and user risk (examples: IP reputation and requesting device posture).

2. Enforce the use of phish-resistant MFA (Hardware Key, Certificate Based) for high-risk systems where possible.

3. Provide self-service MFA enrollment for AI service users, supporting FIDO2 security keys, TOTP apps, biometrics, and more.
```
</details>

<details>
<summary><strong>IAM-13: 1.1.1</strong> (2,629 chars)</summary>

```
1. Unique Identification of AI Models and Variants: Assign unique, persistent identifiers to every model version and variant produced, including base models, fine-tuned derivatives, quantized versions, and alignment-modified variants. Identifiers must be structured to remain traceable across the full AI model lifecycle, from development through deployment, update, and decommissioning.

2. Model Identifier Propagation to Downstream Consumers: Establish documented mechanisms and procedures to communicate model identifier information to downstream consumers (OSPs, APs, and AICs ) enabling them to integrate MP-assigned identifiers into their own identity and traceability systems. Provide identifier metadata in a structured, machine-readable format alongside model artefacts, model cards, and API references, so that downstream actors can maintain an auditable record of which specific model version or variant is operating within their system at any point in time. Identifiers should be structured and communicated in a manner that ensures they are preserved when models are integrated into agent-based or multi-model pipeline architectures, where multiple model versions or variants may operate in concert and identity attribution could otherwise be lost.

3. Unique Identification of Human Users Accessing MP Infrastructure: Ensure that all personnel accessing sensitive MP infrastructure are assigned unique individual identifiers, no shared accounts, service credentials used by humans, or generic team logins. Enforce Single Sign-On (SSO) with mandatory Multi-Factor Authentication (MFA) for access to:
  a. Raw and pre-processed training datasets
  b. Model repositories and model registry platforms
  c. Debugging, interpretability, and inspection tools that may expose model internals or sensitive training data
  d. ML/AIOps platforms including CI/CD pipeline configuration and management interfaces, experiment tracking systems, and hyperparameter management tools

4. Unique Identification of Non-Human Identities in Automated Pipelines: Assign distinct, individually attributable identities to all non-human actors operating within MP infrastructure,  including training jobs, automated evaluation pipelines, CI/CD service accounts, inference services, and orchestration agents. Non-human identities must be segregated from human user accounts, scoped to the minimum permissions required for their specific function, subject to the same uniqueness requirements as human identities, and logged in a manner that enables attribution of any action to a specific automated process rather than a generic service role.
```
</details>

---

## 3. One AI-CAIQ question de-duplicated

`SEF-06.1`, under `SEF-06` Event Triage Processes. The only changed cell in the
342-row AI-CAIQ sheet. The 1.1.0 text shipped **two drafts concatenated into one
cell**, joined by an editorial marker that was never meant to reach publication:

**1.1.0:**
> Are security-related event triage processes, procedures and technical measures
> supporting business processes, defined, implemented and evaluated?
> **Alternative formulation:** Are processes procedures and technical measures
> supporting business processes to triage security-related events, defined,
> implemented and evaluated?

**1.1.1:**
> Are processes, procedures and technical measures supporting business processes
> to triage security-related events, defined, implemented and evaluated?

CSA kept the second wording and describes it in the change log as "the
alternative version … kept as more correct". Note it also gains a comma after
"processes".

**The defect predates 1.1.0.** The same doubled text is present in the
[1.0.3](../1.0.3/) and [`aicm-caiq` 1.0.2](../../aicm-caiq/1.0.2/) extractions.
1.1.1 is the first release in which this question is clean. Those earlier
extractions carry it as-shipped and are **not** retroactively edited — they record
what the publisher published.

The same fix appears in the standalone questionnaire workbook, which is otherwise
untouched: a full cell-by-cell diff of
`AI_CAIQv1.1.0-star_security_questionnaire-*` between the two bundles finds only
the A1 spec-version stamp, this question, and the Change Log rows.

---

## 4. Changes to sheets this repo does not extract

`parse_aicm.py` reads six of the nine worksheets: `AICM`,
`Implementation Guidelines`, `Auditing Guidelines`,
`Scope Applicability (Mappings)`, `AI-CAIQ`, `LLM Taxonomy`. It does not read
`Introduction`, `Acknowledgments`, or `Change Log`.

All three changed, and the `Introduction` changes matter.

### The two scoping notes — read these before using the new mappings

New in 1.1.1, and the reason the gap-level table in
[section 1](#gap-levels-all-five-frameworks) looks the way it does:

> **\*\*** Please note: Regarding the 'AICM to NIST AI RMF & AI 600-1' Mapping:
> The AICM is a set of security controls for AI systems that operate on the
> cloud, thus including infrastructure security controls as well (CCM v4.1
> controls). NIST AI 600-1 and AI RMF are focused only on AI and genAI. The gaps
> identified that fall outside the scope of these 2 NIST frameworks, are expected
> to be covered by other NIST frameworks like NIST SP 800-53, etc.

> **\*\*\*** Please note: AIUC-1 does not cover non-AI risks that are already
> addressed by broader frameworks and regulations such as SOC 2, ISO 27001, or
> GDPR. Organizations are expected to manage compliance with these frameworks
> separately.

Without these, 104 and 110 `Full Gap` findings invite the conclusion that AIUC-1
and the NIST frameworks are deficient. CSA's stated position is that the gaps are
out of those frameworks' declared scope and are expected to be covered elsewhere.

### A new caveat on the ownership columns

This one qualifies data that **is** extracted, from a sheet that is not:

> **IMPORTANT NOTE:** Both the control ownership attributions and applicability
> to the service model/layer (Cloud/GenAIOps - Model - Orchestrated Service -
> AI-Service) are meant to represent a high-level simplification. The AICM user
> should revise those attributions depending on the contractually agreed SSRM for
> the specific LLM/GenAI services environment.

It applies to `typical_control_applicability_and_ownership` for all 247 controls
in `aicm-1.1.1.json`. 1.1.0 carried the equivalent caveat for *architectural
relevance* only; 1.1.1 adds this parallel one for ownership and applicability.

### Smaller `Introduction` edits

- The mapping-tab paragraph reorders its framework list to put AIUC-1 first
  (it was last in 1.1.0, where it named frameworks the sheet did not contain —
  see [above](#110-documented-these-two-blocks-without-shipping-them)). The
  same reordering is applied to the `Control Mapping` column description.
- "The column describes the suggested compensating control…" → "**The addendum
  column** describes…"
- The ISO 27001/27002 alignment note is demoted from a `•` bullet to footnote `*`.
- The two ISO scenarios gain `A)` / `B)` labels and the word "compliant":
  "If your Organization: ISO 42001 **compliant** only".
- "contributed to the AICM V1.0's and v1.1 update" → "…and **its** v1.1 update".

### `Acknowledgments`

Two contributor sections added, matching the two new mappings:
`AIUC-1 (Q2 2026) Mapping` and `NIST AI RMF & AI 600-1 Mapping (2024)`. One
column group is relabelled `Authors` → `Contributors`. Section list goes from
seven to nine.

### `Change Log`

Three v1.1.1 rows added, all dated 2026/07/13, pushing the existing rows down
(which accounts for most of the 52 differing cells in a 19-row sheet):

| Version | Date | Component | Description |
|---|---|---|---|
| AICM v1.1.1 | 2026/07/13 | Mappings | Added the AIUC-1 Mapping and the NIST AI RMF & AI 600-1. |
| AICM v1.1.1 | 2026/07/13 | Implementation Guidelines | Updated the Implementation Guidelines of the Model Provider, for the GRC-01, IAM-13, IAM-18 controls. |
| AICM v1.1.1 | 2026/07/13 | AI-CAIQ | Updated the SEF-06 control's question which contained two versions of the control's self-assessment question. The alternative version is kept as more correct. |

With respect to the data sheets this log is **accurate and complete** — a contrast
with the 1.1.0 log, which claimed mapping rows were added "across all four
external frameworks" while shipping three, and said nothing at all about
renumbering 54 control IDs.

Two caveats on trusting it, though. It does not mention the `Introduction` notes
at all, so "complete" holds only for the sheets it covers. And its
`Implementation Guidelines` row names the three changed controls without saying
that all three were rewritten because they had held the wrong actor's guidance —
"Updated the Implementation Guidelines of the Model Provider" reads as
enhancement rather than correction. The standing advice in
[`../VERSIONING.md`](../VERSIONING.md) §3 — read the change log, then distrust
it — still applies.

### Open question

These notes are guidance the data cannot be read correctly without, and they
currently exist only in the gitignored workbook and quoted in this report and the
README. Capturing the `Introduction` sheet into the extraction — as a
`source_notes` block alongside `definitions` — would put them in the JSON where a
consumer would find them. That is an addition to the extraction contract and
would apply to 1.1.0 and 1.0.3 as well, so it is deliberately **not** done here.
Recorded as `known_source_issues/introduction-sheet-notes-not-extracted` in
[`aicm-1.1.1-metadata.json`](aicm-1.1.1-metadata.json).

---

## What did not change

Asserted as invariants in
[`../crosswalks/check_figures.py`](../crosswalks/check_figures.py), so these are
verified on every run rather than merely claimed here:

| | |
|---|---|
| Control IDs | **0** added, **0** removed. All 247 identical. |
| Control identity | **0** of 247 differ on domain, title, specification, control type, ownership, architectural relevance, lifecycle relevance, or threat category. |
| Auditing Guidelines | **0** differing cells across the whole sheet. |
| LLM Taxonomy | Identical — 53 lifecycle entries, 4 definition sections, 24 terms. |
| Carried-over mappings | **0** of 247 differ on BSI AI C4, EU AI Act, or ISO/IEC 42001 mapping, gap level, or addendum. |
| Other actor columns | Only the MP column changed, and only for 3 controls. |
| Sheet structure | Same nine sheets, same order, same row counts. |
| Extraction schema | Unchanged, except `scope_applicability_mappings` gains two keys and `source_data_notes` gains `sentinel_values`. Existing slugs are stable. |

**Consequence: no crosswalk is provided, because none is needed.** This is stated
explicitly because "no crosswalk exists" and "no crosswalk is needed" look
identical from outside. Migrating from **1.0.3** is a different matter entirely
and still requires
[`../crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv`](../crosswalks/aicm-1.0.3-to-1.1.0-crosswalk.csv).

---

## Version labelling

| Where | 1.1.0 | 1.1.1 |
|---|---|---|
| Artifact page label | "AI Controls Matrix v1.1" | "AI Controls Matrix v1.1" *(unchanged)* |
| Stated release date | 06/22/2026 | 06/22/2026 *(unchanged)* |
| Bundle / PDF titles | "AICM v1.1" | "AICM v1.1" *(unchanged)* |
| Spreadsheet filename | `AICMv1.1.0-generated_at_2026_06_18.xlsx` | `AICMv1.1.1-generated_at_2026_07_22.xlsx` |
| Cell A1, every sheet | `{"specification_version":"1.1.0"}` | `{"specification_version":"1.1.1"}` |
| `docProps/core.xml` created | — | 2026-07-22T17:15:10Z |
| Change Log rows | dated 2026/06/23 | dated 2026/07/13 |

Because two datasets ship under the label "v1.1", the bare aliases `1.1` and
`v1.1` are claimed by **neither** version directory — 1.1.0 held them until this
release and gave them up. `version_aliases_withdrawn` in
[`../1.1.0/aicm-1.1.0-metadata.json`](../1.1.0/aicm-1.1.0-metadata.json) records
why. **Cite `AICM 1.1.0` or `AICM 1.1.1`; a bare "AICM v1.1" citation is not
resolvable to a dataset.**

The standalone questionnaire is a further wrinkle: its Change Log gained a row
labelled `AI-CAIQ v1.1.1`, but its filename, sheet name, document title,
copyright notice and `caiq_version` stamp all still say 1.1.0. See
[`scripts/README.md`](scripts/README.md).

---

## Reproducing this diff

Both workbooks are gitignored. Pull from S3:

```bash
aws --profile csa s3 cp \
  s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/aicm/1.1.0/AICMv1.1.0-generated_at_2026_06_18.xlsx .
aws --profile csa s3 cp \
  s3://dataset-public-laws-regulations-standards/control/cloudsecurityalliance.org/aicm/1.1.1/AICMv1.1.1-generated_at_2026_07_22.xlsx .
```

The extraction-level diff needs no source workbook — both JSON files are
committed:

```bash
python3 - <<'PY'
import json
a={c['control_id']:c for c in json.load(open('../1.1.0/aicm-1.1.0.json'))['controls']}
b={c['control_id']:c for c in json.load(open('aicm-1.1.1.json'))['controls']}
for cid in a:
    for field in a[cid]:
        if field == 'scope_applicability_mappings':
            continue
        if json.dumps(a[cid][field], sort_keys=True) != json.dumps(b[cid][field], sort_keys=True):
            print(cid, field)
PY
```

Expected output: exactly four lines — `GRC-01`, `IAM-13`, `IAM-18`
implementation_guidelines and `SEF-06` caiq_questions.

### A note on the parser guard

`parse_aicm.py` discovers the mapping frameworks from the merged group-header row
and **exits 1** if they differ from `EXPECTED_FRAMEWORKS`. Run against this
release, the 1.1.0 parser refused and named both new frameworks.

That mattered more than it might appear. AIUC-1 was inserted at the **front** of
the mapping blocks, shifting BSI, EU and ISO three columns right. A parser
trusting fixed offsets would not have failed — it would have read AIUC-1's mapping
into the BSI AI C4 field, BSI's into the EU field, and EU's into the ISO field,
emitting 247 complete, well-formed, entirely wrong rows. Nothing downstream would
have flagged it.

---

## References

| | |
|---|---|
| [`README.md`](README.md) | Summary of this report, plus contents and reproduction |
| [`aicm-1.1.1-metadata.json`](aicm-1.1.1-metadata.json) | `known_source_issues` — ten entries, machine-readable |
| [`../VERSIONING.md`](../VERSIONING.md) §1b | This release in the context of AICM's versioning history and standing policy |
| [`../crosswalks/check_figures.py`](../crosswalks/check_figures.py) | Recomputes every figure quoted here and fails on drift |
| [`../1.1.0/README.md`](../1.1.0/README.md) | The superseded release |
| CSA artifact page | https://cloudsecurityalliance.org/artifacts/ai-controls-matrix-v1-1 |
