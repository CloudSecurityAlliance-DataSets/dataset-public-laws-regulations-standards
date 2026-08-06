

{0}------------------------------------------------


# A5 – Cloud Infrastructure Operations Module


{1}------------------------------------------------

### Change history

| Version | Date            | Name | Description     |
|---------|-----------------|------|-----------------|
| 1.0     | 30 June<br>2026 | T 24 | First published |

*Table1: Revision history*

Federal Office for Information Security PO Box 20 03 63 53133 Bonn Email: aisecurity@bsi.bund.de Website: https://www.bsi.bund.de © Federal Office for Information Security 2026

{2}------------------------------------------------

# **Table of Contents**

|   |     | 1 Introduction ………………………………………………………………………………………………                                               |  |
|---|-----|---------------------------------------------------------------------------------------------------|--|
|   | 1.1 | About the A5                                                                                      |  |
|   | 1.2 | Nature and Structure                                                                              |  |
| 2 |     | Governance, Compliance and Scope (GCS)                                                            |  |
|   |     | 2.1 GCS.2 Defining governance, roles and policies                                                 |  |
|   |     | 2.1.1 GCS.2.5 Document evidence of the trustworthiness of the underlying infrastructure and cloud |  |
|   |     | $components$                                                                                      |  |

{3}------------------------------------------------

# <span id="page-3-0"></span>1 Introduction

#### <span id="page-3-1"></span>1.1 About the A5

The trustworthiness of AI systems has become a key prerequisite for their responsible use, from technical, organisational and regulatory perspectives alike. For decision-makers, this concerns the reliability, security and legal compliance of AI applications; for developers, it concerns the foundation for robust, traceable and controllable systems. AI that is inadequately secured can not only lead to erroneous or distorted results, but also pose significant risks to security, fundamental rights and societal acceptance. With the European Union's AI Act, the Cyber Resilience Act and other regulatory frameworks, the requirements for trustworthy AI are no longer merely best practice, but are increasingly becoming a measurable and verifiable prerequisite for the admissibility and marketability of many AI systems.

The 'AI Audit and Assurance Assessment Architecture' (A5) is aimed at all stakeholders along the AI value chain, from providers and deployers to the entities responsible for development, operation and oversight. The aim is to provide structured guidance for the development, deployment and operation of fair, secure and compliant AI systems, thereby making a robust contribution to the trustworthiness of AI throughout its entire lifecycle.

#### <span id="page-3-2"></span>1.2 Nature and Structure

This A5 Cloud Infrastructure Operational Module is a vertically oriented module and supplements the A5 Horizontal Trustworthiness Core Module with those requirements that arise specifically from the operational mode of a cloud-based AI system. It addresses the particular requirements that arise when the underlying infrastructure and essential system and platform components are provided via cloud services.

The module comprises requirements relating to the demonstration of the trustworthiness of the underlying infrastructure and cloud components, and is directly linked to the parent processes established in the core module, in particular risk and security management, as well as the requirements for auditability and evidence management. They identify the responsible party and any dependencies, and contain supplementary guidance differentiated according to the roles of provider and operator; this guidance is intended as purpose-oriented guidance for implementation, without prescribing possible measures in a definitive manner.

{4}------------------------------------------------

# <span id="page-4-0"></span>2 Governance, Compliance and Scope (GCS)

The following lists measures designed to establish a regulated framework for the governance of AI within the organisation by clarifying business objectives and the context of use, defining responsibilities, roles and guidelines, and embedding overarching requirements regarding risk, quality, security and human oversight throughout the entire AI lifecycle.

#### <span id="page-4-1"></span>2.1 GCS.2 Defining governance, roles and policies

#### <span id="page-4-2"></span>2.1.1 GCS.2.5 Document evidence of the trustworthiness of the underlying infrastructure and cloud components

**Criterion:** The responsible party should document the trustworthiness of the underlying infrastructure and cloud components by providing recognised evidence of compliance (C5 certificate), which must have a scope covering at least the infrastructure and components relevant to the AI system, take into account the relevant risk dimensions, and cover a period encompassing the entire assessment period (or, alternatively, a bridge letter to address any gaps), carried out by qualified and independent personnel; a clear description of the test procedures performed, with evidence that no critical security-related issues or anomalies were identified; provision prior to the relevant cut-off date; and change management that assesses the impact of changes to infrastructure and cloud components and documents the timely follow-up of identified issues through appropriate mitigation measures.

**Dependency:** None

#### **Guidance**

**Provider**: The aim is to demonstrate the trustworthiness of the AI system's underlying infrastructure and cloud components by means of recognised evidence of compliance, thereby ensuring that the infrastructure is suitable as a basis for the secure operation of the AI system. To this end, a recognised certificate or test report (C5) may be provided, the scope of which covers the infrastructure, platform and system components relevant to the AI system and takes the relevant risk dimensions into account. The coverage period may encompass the entire assessment period; otherwise, a bridge letter is appropriate to address the gap. The audit may be carried out by qualified and independent personnel; the test procedures performed must be clearly documented and demonstrate that no critical security-related issues or anomalies were identified. In addition, the evidence may be provided in good time before the relevant deadline; the impact of changes to infrastructure or cloud components may be assessed, and any issues identified may be addressed promptly through appropriate mitigation measures.