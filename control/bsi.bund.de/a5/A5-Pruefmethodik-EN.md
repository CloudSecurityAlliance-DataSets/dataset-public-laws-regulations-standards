

{0}------------------------------------------------


# A5 Audit Methodology

based on ISAE 3000


{1}------------------------------------------------

## Document History

| Version | Date       | Name | Description                            |
|---------|------------|------|----------------------------------------|
| 0.9     | 30.06.2026 | T 24 | Initial publication<br>community draft |

*Table 1: Document History*

Federal Office for Information Security (BSI) Postfach 20 03 63 53133 Bonn Email: aisecurity@bsi.bund.de Internet: https://www.bsi.bund.de © Federal Office for Information Security (BSI) 2026

{2}------------------------------------------------

| 1 |        | Introduction<br>4                                                       |    |
|---|--------|-------------------------------------------------------------------------|----|
|   | 1.1    | Preliminary Remarks4                                                    |    |
|   | 1.2    | Definitions4                                                            |    |
| 2 |        | Structure and Content of the Criteria9                                  |    |
|   | 2.1    | Positioning within the BSI's Stand-der-Technik-Bibliothek9              |    |
|   | 2.2    | Organisation into Profiles, Profile Modules and Criteria<br>9           |    |
|   | 2.3    | Structure of a Criterion                                                | 10 |
| 3 |        | Demonstrating Conformity through Independent Audits                     | 11 |
|   | 3.1    | Introduction                                                            | 11 |
|   | 3.2    | Audit Standards to be Applied                                           | 11 |
|   | 3.3    | Relationship to Other Audits                                            | 12 |
|   | 3.4    | Special Requirements of the BSI                                         | 12 |
|   | 3.4.1  | Assurance Engagement                                                    | 12 |
|   | 3.4.2  | Description of the Assessment Object<br>                                | 13 |
|   | 3.4.3  | Criteria to be Applied                                                  | 15 |
|   | 3.4.4  | Subject Matter and Objective of the Audit                               | 16 |
|   | 3.4.5  | Requirements for the System Description and the Management Statement    | 17 |
|   | 3.4.6  | Consideration of Subservice Organisations                               | 19 |
|   | 3.4.7  | Obtaining Evidence Regarding the System Description                     | 20 |
|   | 3.4.8  | Assessing the Fulfilment of Criteria                                    | 21 |
|   | 3.4.9  | Obtaining Evidence Regarding the Suitability of Design<br>              | 21 |
|   | 3.4.10 | Handling Deviations                                                     | 22 |
|   | 3.4.11 | Reporting<br>                                                           | 23 |
|   | 3.4.12 | Qualification of the Practitioner                                       | 26 |
|   | 3.4.13 | Information on the Limitation of Liability                              | 26 |
|   | 3.5    | Dealing with Revisions of the A5 Audit Methodology (based on ISAE 3000) | 27 |

{3}------------------------------------------------

## <span id="page-3-0"></span>1 Introduction

## <span id="page-3-1"></span>1.1 Preliminary Remarks

As the Federal Cyber Security Authority, the BSI shapes information security in the context of digitalisation through prevention, detection and response, for the state, the economy and society. Information security is the prerequisite for successful digitalisation, since digitalisation can only succeed if users develop trust in new technologies and are able to use them securely to their benefit.

In recent years, artificial intelligence (AI) has become an integral part of modern IT value chains. AI systems are being integrated, with increasing breadth and depth, into business operations, critical infrastructures and administrative processes. This development is accompanied by a growing need to demonstrate the trustworthiness of these AI systems to users, supervisory authorities and other addressees in a transparent and comparable manner.

AI systems are characterised by properties that differ substantially from those of conventional IT systems: they frequently process large, heterogeneous volumes of data; their behaviour may change through training or adaptation; their outputs are not in every case fully explainable; and they are regularly embedded in complex value chains comprising models, data, platforms and downstream applications. These properties call for a distinct, AI-specific audit approach that purposefully complements the established approaches to information security with AI-specific criteria.

With the A5 audit architecture, the BSI presents such an audit approach. The A5 audit architecture comprises two components:

- **A5 criteria**: a collection of auditable criteria for assessing the trustworthiness of AI systems, AI applications or components thereof;
- **A5 Audit Methodology based on ISAE 3000**: the procedure set out in this document for assessing the A5 criteria by independent practitioners based on ISAE 3000 (Revised).

Under the umbrella of the A5 audit architecture, the BSI may provide further audit methodologies in the future.

The A5 audit architecture is addressed to responsible parties who wish to demonstrate the conformity of an assessment object with the A5 criteria by means of an independent audit, as well as to the addressees of A5 reporting, in particular existing and potential users, their independent practitioners, and supervisory and regulatory authorities.

The structure and content of the A5 criteria are presented in Chapter 2 of this document. The A5 criteria themselves are published on the BSI website as a PDF file and in machine-readable form as a JSON file in OSCAL format.

## <span id="page-3-2"></span>1.2 Definitions

For the purposes of A5, the following definitions relating to AI apply. They are based on definitions from Regulation (EU) 2024/1689 (AI Act), from IDW PS 861, and from the ISO/IEC 22989 standard.

**Provider:** A natural or legal person, public authority, agency or other body that develops an AI system (see below) or a general-purpose AI model (see below), or that has an AI system or model developed, and places it on the market or puts the AI system into service under its own name or trademark, whether for payment or free of charge.

{4}------------------------------------------------

**Deployer:** A natural or legal person, public authority, agency or other body using an AI system (see below) under its own authority, except where the AI system is used in the course of a personal, non-professional activity.

**AI algorithm / AI model:** AI algorithms are algorithms that serve to develop and adapt AI models on the basis of training datasets and that are, as a rule, executed until the AI model delivers results useful for the application. AI models constitute the central AI component (see below) of an AI system (see below), used to make predictions, to take decisions on that basis, or to trigger actions.

**AI application:** An AI application is software into which an AI model is integrated. AI applications comprise both proprietary software and software obtained from third parties, used as custom or standard software for business tasks. AI applications are deployed either independently, in combination with other software programs, or as part of an integrated software solution.

**AI component:** A functionally delimited part of an AI system (see below) that, taken on its own, carries out one or more AI-related processing steps. An AI component may itself be an assessment object.

**AI system:** A machine-based system that is designed to operate with varying levels of autonomy and that may exhibit adaptiveness after deployment, and that, for explicit or implicit objectives, infers, from the input it receives, how to generate outputs such as predictions, content, recommendations or decisions that can influence physical or virtual environments.

**Intended purpose:** The use of the assessment object intended by the provider, including the specific context and conditions of use, as specified by the provider in the technical documentation, in instructions for use or in other accompanying information. For the deployer, the intended purpose is replaced by the specific deployment context (use case) in which the assessment object is used.

The following definitions relate to A5 and the assessment object.

**A5:** Acronym for AI Audit and Assurance Assessment Architecture. The BSI's modular and futureproof, extensible AI audit architecture. A5 defines criteria for assessing the trustworthiness of AI systems. These A5 criteria (see below) form part of the BSI's state-of-the-art library and can be used within different audit methodologies provided under the umbrella of A5. The present document describes the A5 Audit Methodology (based on ISAE 3000) as one such audit methodology.

**A5 criteria:** The AI-specific criteria to be applied in assessing the trustworthiness of an assessment object (see below).

**A5 audit:** An audit of the system description (see below) prepared by the responsible party (see below) and of the controls (see below) described therein, with reference to the applicable A5 criteria, carried out by an independent practitioner in the form of a reasonable assurance engagement.

**A5 Audit Methodology:** The present document. It describes the audit methodology for carrying out A5 audits based on ISAE 3000 (Revised) and supplementary audit standards.

**Addressees of A5 reporting:** Existing and potential customers and users of the assessment object, their independent practitioners, service providers of those users, as well as supervisory and regulatory authorities to whom the A5 reporting is addressed. The addressees possess sufficient knowledge and understanding of the assessment object, its nature and its intended purpose.

**Applicable A5 criteria:** That subset of the A5 criteria which results from the profile (see below) selected by the responsible party (see below) and which is authoritative for the specific assessment object.

{5}------------------------------------------------

**Assessment object:** Depending on the individual case, the assessment object may be a complete AI system, an AI application, a component thereof, a dataset, a model or another delimited part of an AI system.

**Description of the assessment object:** The description of the assessment object prepared by the responsible party (see below), including its identification, its scope and system boundaries, its operational and deployment context, its life-cycle reference, its function, and its AI-specific and data-related characteristics. The description of the assessment object forms part of the system description (see below). The minimum content for the description of the assessment object is set out in Section 3.4.2.

**Profile:** A set of applicable criteria explicitly predefined by the BSI, which may either consist exclusively of individual A5 criteria, consist exclusively of profile modules, or combine profile modules with further individual A5 criteria.

**Profile module:** A grouping of A5 criteria defined by the BSI that can be used as part of a profile. Profile modules may, for example, address general criteria, technological specificities, provision or operating contexts, regulatory requirements or specific use cases.

**Role:** The position that the responsible party occupies with respect to the assessment object within the AI value chain. The responsible party may take on the role of provider, of deployer, a combined role (provider and deployer at the same time) or another role (e.g. data supplier).

**System description:** This comprises the description of the assessment object as well as the controls (see below) established for the assessment object. The description criteria for the system description are set out in Section 3.4.5.1.

**Responsible party:** The natural or legal person, public authority, agency or other body that is responsible for the assessment object and that wishes to demonstrate conformity with the applicable A5 criteria. The responsible party may be a provider, a deployer or another responsible body. It must be specifically named in the system description.

The following definitions relate to assurance engagements and are derived from the International Standard on Assurance Engagements (ISAE) 3000 (Revised) "Assurance Engagements Other than Audits or Reviews of Historical Financial Information", ISAE 3402 "Assurance Reports on Controls at a Service Organization", the International Ethics Standards Board for Accountants (IESBA) Code of Ethics for Professional Accountants, as well as the IDW Audit Standards (IDW PS) 860, 861 and 951 (new version) of the Institute of Public Auditors in Germany (IDW), which are in line therewith.

**Deviation:** A finding by the practitioner that (a) the system description or the controls (see below) presented therein are not fairly presented, (b) controls are not suitably designed, or (c) controls did not operate effectively as intended. One or more deviations may, individually or in combination, be material and lead to a modification of the conclusion (see below).

**Management statement:** A written statement by management of the responsible party concerning the fair presentation of the controls (see below) in the system description, as well as the suitability of the design and, where applicable, the operating effectiveness of the controls in meeting the applicable A5 criteria. The description criteria for the statement are set out in Section 3.4.5.2.

**Inclusive method:** A method for addressing the services provided by a subservice organisation (see below) in which the complementary controls (see below) at the subservice organisation are subject to the practitioner's procedures. The responsible party's system description includes a presentation of: (a) the nature of the services provided by the subservice organisation; (b) the components of the subservice organisation's internal control system (see below) that are used in providing services to the responsible party, including the subservice organisation's controls that are necessary, together with the responsible party's controls, to meet the applicable A5 criteria

{6}------------------------------------------------

with reasonable assurance; and (c) the responsible party's controls for monitoring the effectiveness of the subservice organisation's controls.

**Internal control system:** The totality of the principles, procedures and measures established by the responsible party for the organisational and technical implementation of management decisions, with the aim of ensuring the trustworthiness of the assessment object and of ensuring compliance with the applicable A5 criteria as well as with the relevant legal and regulatory requirements. The internal control system comprises the components control environment, risk assessment, control activities, information and communication, and monitoring activities. The A5 criteria specify requirements for these components with respect to the assessment object. Controls (see below) form part of the internal control system.

**Complementary user entity controls (CUECs):** Controls (see below) that the responsible party expects to be implemented by customers, users or other parties outside the responsible party when designing its internal control system. These complementary controls are necessary, together with the responsible party's controls, to meet the applicable A5 criteria with reasonable assurance.

**Complementary subservice organisation controls (CSOCs):** Controls (see below) that the responsible party expects to be implemented by the subservice organisation (see below) when designing its internal control system. These complementary subservice organisation controls are necessary, together with the responsible party's controls, to meet the applicable A5 criteria with reasonable assurance.

**Control:** A policy or procedure to reduce the likelihood of events occurring, or to detect events that have occurred, with the aim of maintaining the fulfilment of the applicable A5 criteria. Controls exist within each of the five components of the responsible party's internal control system (control environment, risk assessment, control activities, information and communication, and monitoring activities). A control is either preventive (designed to avoid an unintended event or outcome at first occurrence) or detective (designed to identify an unintended event or outcome after the first occurrence, before the overarching objective is completed, and to initiate measures to correct or avoid it).

**Modification of the conclusion:** The deviation from an unmodified conclusion as a result of one or more material deviations or as a result of the inability to obtain sufficient appropriate evidence. The modification leads to a qualified, adverse or disclaimed conclusion, as well as to a corresponding adjustment of the reporting.

**Attestation engagement:** An assurance engagement in which the management of the responsible party assesses the internal control system with respect to the assessment object against the applicable A5 criteria and presents the resulting subject-matter information in a written statement (including the system description). The practitioner assesses whether the statement is free from material deviations and issues reporting with reasonable assurance. In general usage, assurance engagements are commonly referred to as "audits", whereas public auditors use the term "audit" only for financial statement audit engagements. To aid comprehension, including for general readers, the term "audit" is used in this A5 Audit Methodology in its general sense, even though the engagement in question is not a financial statement audit but an assurance engagement (in the form of an attestation engagement).

**Subservice organisation:** A company or service provider for which the following conditions are cumulatively met: (1) there is an ongoing or recurring service relationship with the responsible party; (2) the services provided are relevant to understanding the assessment object, its system boundaries, its functioning or its integration into the AI value chain; and (3) the fulfilment of applicable A5 criteria requires that complementary controls be established at the company or service provider. The responsible party must establish appropriate monitoring controls regarding the effectiveness of the subservice organisation's controls. These may include, in particular, providers of AI services or foundation models (where integrated through an ongoing contractual

{7}------------------------------------------------

relationship), infrastructure or platform providers, ongoing data suppliers, and integration partners.

**Practitioner:** The person(s) responsible for carrying out the A5 audit.

{8}------------------------------------------------

## <span id="page-8-0"></span>2 Structure and Content of the Criteria

## <span id="page-8-1"></span>2.1 Positioning within the BSI's Stand-der-Technik-Bibliothek

With the *Stand-der-Technik-Bibliothek*, the BSI publishes a comprehensive collection of security regulations for various application areas of information and cyber security in machine-readable form. The A5 criteria are included as a subset within this collection. The *Stand-der-Technik-Bibliothek* is based on the Open Security Controls Assessment Language (OSCAL), a standardised and machine-readable framework developed by NIST that improves the efficiency and consistency of information security documentation and enables automation across the entire compliance life cycle.

The *Stand-der-Technik-Bibliothek* distinguishes between two types of catalogues: *Quellkataloge* (source catalogues), which serve as foundational documents supporting the editing and further development of regulations, and *Anwenderkataloge* (user catalogues), which can be drawn upon directly within institutions for implementation or auditing. Both types of catalogues are published via the BSI's public GitHub repository and follow a uniform technical and structural approach.

The A5 criteria are aligned with the structural conventions of the *Stand-der-Technik-Bibliothek* and will in future be published in machine-readable form in the OSCAL format. This ensures that the A5 criteria can be integrated into existing OSCAL-based tool chains for compliance processing. In addition, the BSI makes the A5 criteria available as a PDF document on its website and will in future be published in machine-readable form.

The positioning within the *Stand-der-Technik-Bibliothek* concerns the form of provision and technical interoperability. Beyond their use within the A5 Audit Methodology, the A5 criteria can also be used independently of it, for example as a reference for designing internal control systems, for informal selfassessments, or as a basis for other assessment contexts (for example internal audits).

## <span id="page-8-2"></span>2.2 Organisation into Profiles, Profile Modules and Criteria

The A5 criteria comprise a total set of individual criteria for various deployment contexts, technologies and operating models of AI systems, AI applications or components thereof. In order to be able to offer, from this total set, the appropriate selection of criteria for a specific A5 audit, the A5 criteria are structured by means of profiles and profile modules. Both are centrally defined, maintained and released by the BSI.

**Profile:** A profile represents a set of applicable criteria explicitly predefined by the BSI. This may consist of individual A5 criteria, be composed of profile modules, or combine profile modules with individual additional A5 criteria. In the absence of an explicit definition and publication as a profile, individual profile modules and combinations of profile modules are automatically regarded as an implicitly defined profile, which may also be selected and assessed. For the assessor, the profile selected by the responsible party is decisive.

**Profile module:** A profile module is a subset of the A5 criteria predefined by the BSI. Profile modules bundle A5 criteria that address a particular thematic context; these could be, for example, general criteria, technological specificities, provision or operating contexts, regulatory requirements or specific use cases. Profile modules facilitate the targeted selection and filtering of A5 criteria for profiles.

**Criterion:** A criterion is the smallest content unit of the A5 criteria. Each criterion formulates a single, assessable statement about the assessment object or about the controls established for it by the responsible party.

Where necessary, the BSI may adapt existing profiles and profile modules or add further ones, without this affecting this A5 Audit Methodology. The applicable profiles are published as a PDF document and as a JSON file in OSCAL format on the BSI's website.

{9}------------------------------------------------

The application of profiles within an A5 audit, in particular the determination of the set of criteria applicable to a specific assessment object, is governed by Section 3.4.3.

## <span id="page-9-0"></span>2.3 Structure of a Criterion

The A5 criteria contained in a profile are ordered according to the grouping structure specified by the BSI and are divided into six practices:

- Governance, Compliance & Scope (GCS)
- Design, Engineering and Integration (DEI)
- Verification and Validation (VAV)
- Deployment (DEP)
- Operations, Performance and Supervision (OPS)
- Retirement (RET)

Within each practice, topics are defined that delineate a specific subject area of the respective practice. A topic groups together criteria that are related in content, such as "Security Governance: protection goals & threat modelling, red teaming" as the first topic of the GCS practice.

The identifier of each criterion results from this assignment. The identifier reflects the position of the criterion within the structure: the first level designates the practice, the second level the topic within the practice, and the third level the individual criterion within the topic. For example, GCS.1.1 designates the first criterion of the first topic of the GCS practice.

Each criterion consists of the following components:

**Title:** A short designation that names the subject of the criterion (e.g. "Establish a risk management process for discrimination risks").

**Criterion text:** The binding content of the criterion. The criterion text formulates an assessable statement about what the responsible party is to implement with respect to the assessment object. It follows a uniform linguistic structure consisting of:

- **Result:** the state or effect to be achieved;
- **Specification:** the detailing and concretisation of the result by means of characteristics, conditions or standards; and
- **Action word:** the form in which the target object is to be addressed.

**Guidance:** Non-binding explanations that support the interpretation of the criterion. The notes specify possible implementation approaches and documentation approaches, but do not establish any independent obligations beyond the criterion text.

{10}------------------------------------------------

## <span id="page-10-0"></span>3 Demonstrating Conformity through Independent Audits

## <span id="page-10-1"></span>3.1 Introduction

The A5 audit architecture is aimed at two target groups: on the one hand, the A5 criteria can be used by AI providers, AI deployers and other suppliers of AI components or data to design their internal control systems. On the other hand, they serve the addressees of A5 reporting, in particular customers and users, in assessing the suitability of an AI system, an AI component or another object for their use case.

The EU AI Act distinguishes two key roles: the provider, who develops or commissions the development of an AI system and places it on the market under its own name, and the deployer, who uses an AI system under its own authority. An organisation may also assume both roles at the same time, for example where it develops an AI system itself and subsequently also deploys it itself. In that case, the obligations of both roles apply cumulatively. In addition, further bodies may also seek an A5 audit, such as suppliers of upstream AI components or data suppliers, provided that applicable A5 criteria exist for their services.

While AI providers, AI deployers and other bodies can align their principles, procedures and measures with the A5 criteria, customers have a legitimate interest in verifying whether these criteria are met. Individual self-assessments for each interested party are uneconomical for this purpose and offer insufficient assurance. Furthermore, where enquiries are made to different providers, there is no guarantee of a consistent level of detail, which considerably complicates an objective comparison of the information received.

In the view of the BSI, a standardised audit by qualified and independent practitioners, who prepare rulebased reports suitable for disclosure to current and potential users, represents an efficient and appropriate approach.

For the sake of modularity and better readability of this A5 Audit Methodology, two overarching terms are used in the following: the "responsible party" designates the natural or legal person that is responsible for the assessment object and that wishes to demonstrate conformity with the applicable A5 criteria. This includes AI providers, AI deployers, data suppliers and other bodies. The "assessment object" designates the object delimited for the A5 audit. Depending on the individual case, this may be a complete AI system, an AI application, an AI component, a dataset, a model or another delimited part of an AI system.

Therefore, in this A5 Audit Methodology, the BSI sets forth its requirements for demonstrating conformity as well as for A5 reporting to the responsible party and its customers, users, or other intended addressees.

Customers and other users should regard compliance with the A5 criteria as an essential component of their engagement, procurement or use, and should agree on this with the responsible party where applicable. They should not base their decision solely on the existence of current A5 reporting, but should have it presented to them by the responsible party on a regular basis and assess it for their use case.

The BSI is not involved in any part of the audit or reporting. The practitioner carries out the audit independently of any instructions from the BSI. The practitioner renders its services to the responsible party as the client, not to customers, users or other addressees of the reporting.

## <span id="page-10-2"></span>3.2 Audit Standards to be Applied

For determining the demonstrations of conformity, established national and international standards and initiatives were used as a basis.

Specifically, these are:

{11}------------------------------------------------

- 1. the International Standard on Assurance Engagements (ISAE) 3000 (Revised) "Assurance Engagements Other than Audits or Reviews of Historical Financial Information";
- 2. the German IDW PS 860 *"IT-Prüfung außerhalb der Abschlussprüfung"* of the Institute of Public Auditors in Germany (IDW), which is in line therewith; or
- 3. other national equivalents to ISAE 3000 (Revised).

For individual questions concerning the conduct of the audit and reporting, further audit standards may be applied by analogy. These include:

- 1. IDW PS 861 *"Die Prüfung von KI-Systemen"* for AI-specific audit requirements;
- 2. ISAE 3402 "Assurance Reports on Controls at a Service Organization" or national equivalents to ISAE 3402;
- 3. or the German IDW PS 951 (new version) *"Die Prüfung des internen Kontrollsystems bei Dienstleistungsunternehmen"*, which is in line therewith.

## <span id="page-11-0"></span>3.3 Relationship to Other Audits

The A5 criteria are based on established AI standards and publications, which is why responsible parties that already use these standards as a point of reference typically have already considered the necessary principles, procedures and measures in their operations.

These principles, procedures and measures typically also form the basis for additional audits, for which the responsible party may have already engaged independent practitioners. In this context, particular mention should be made of audits according to ISAE 3402, IDW PS 951 (new version) or the US SOC 1 or SOC 2 standards, as well as audits according to the BSI C5, where the assessment object is operated on an audited cloud infrastructure. Where the responsible party seeks certifications (for example ISO/IEC 42001) or conformity assessments under Regulation (EU) 2024/1689 (AI Act), there are likewise considerable overlaps with the A5 criteria. In such cases, it is advisable to align these audits with the A5 audit, both in terms of organisation and timing. This enables practitioners and responsible parties to prepare records simultaneously for reporting to different standards, e.g. both for ISAE 3402, SOC 2 or C5 and for A5 reporting.

Organisational coordination is to be distinguished from the use of third-party audit results within the A5 audit. When assessing the coverage of A5 criteria by results obtained during other audits, particular consideration shall be given to the audit methodology and compared with the reasonable assurance required for the A5 audit. For example, results from ISO certification audits are to be assessed differently from those obtained from an ISAE 3000 assurance engagement. The mere reference to the criteria defined in other standards that bear a similarity to the A5 criteria is not sufficient. The A5 audit requires an independent conclusion by the practitioner, with reasonable assurance, on the basis of the practitioner's own procedures.

## <span id="page-11-1"></span>3.4 Special Requirements of the BSI

The application of the audit standards referred to above is specified in the following.

### <span id="page-11-2"></span>3.4.1 Assurance Engagement

A5 audits must always be carried out in accordance with ISAE 3000 (Revised) or a national equivalent, such as the German audit standard IDW PS 860.

{12}------------------------------------------------

ISAE 3000 (Revised) distinguishes between reasonable assurance engagements and limited assurance engagements. A5 audits must be carried out as reasonable assurance engagements.

Additionally, all A5 audits must be carried out as an attestation engagement. The responsible party makes a management statement on the conformity of its subject matter with the applicable A5 criteria. The practitioner examines this management statement and issues a conclusion with reasonable assurance.

An A5 audit may be carried out as an assessment of the suitability of the design or as an assessment of operating effectiveness. In the view of the BSI, an assessment of operating effectiveness is required in order to issue a conclusion on the effective functioning of the controls over a specified period. An assessment of the suitability of the design, by contrast, is limited to the design and implementation of the controls as at a specified date. Pure assessments of the suitability of the design are therefore only permissible on a one-off basis for an initial engagement, where sufficient evidence is not yet available to issue a conclusion on the operating effectiveness of the controls over a period. Subsequent audits must be designed as assessments of operating effectiveness.

An assessment of the suitability of the design leads to a Type 1 report; an assessment of operating effectiveness leads to a Type 2 report.

#### <span id="page-12-0"></span>3.4.2 Description of the Assessment Object

Pursuant to section 3.4.4, the subject matter of the audit is the system description prepared by the responsible party, including the controls presented therein. The description of the assessment object forms part of this system description (cf. section 3.4.5.1). This section sets out the minimum content that the responsible party must include in the system description in order to describe the assessment object and its intended purpose. This minimum content forms the basis for delineating the system boundaries of the assessment object.

Depending on the individual case, the assessment object may be a complete AI system, an AI application, an AI component, a dataset, a model or another delimited part of an AI system. Precisely because the assessment object does not necessarily have to comprise the AI system in its entirety, a precise description in accordance with the following minimum content is required in order to clearly delineate the system boundaries.

In the view of the BSI, a careful description of the assessment object is required because it

- forms the basis for an assurance engagement assessing the suitability of the design and the operating effectiveness of the responsible party's controls,
- makes transparent which components fall within the scope of the audit and which do not, and
- enables the responsible party to assign the profile applicable to the assessment object and the resulting set of criteria.

The responsible party is obliged to present all of the minimum content set out below in the system description. In each case, this content is to be provided only to the extent that it is materially applicable to the type and structural level of the assessment object. If, for example, the assessment object is a dataset, information on function, model architecture or AI-specific characteristics does not apply. To the extent that individual minimum content is not applicable to the assessment object, the responsible party must set out and substantiate this in the system description.

To the extent that the responsible party assumes the role of the deployer and information required for the description of the assessment object is not available to it, it must obtain this information from the provider.

#### **a) Identification of the assessment object**

- name, version, unique identifier of the assessment object
- information on the responsible party (name, jurisdiction, address)

{13}------------------------------------------------

- role of the responsible party (provider, deployer, other)
- position of the responsible party in the AI value chain (provider, deployer, combined)
- upstream relationships, or components or services obtained from third-party providers (upstream relationships)
- structural level of the assessment object (system, application, component)
- information on the relationship of the current version to previous versions, where material for the identification, traceability and delineation of the assessment object
- relevant version and update dependencies of the assessment object, where material for its function or intended purpose

#### **b) Scope and system boundaries of the assessment object**

- inventory and provenance of the constituent parts (inventory & provenance)
- AI components, including upstream components (e.g. external upstream AI contributions)
- non-AI components included
- excluded components, in order to clarify the boundaries of the audit and its result and to avoid an unintended extension of the scope of the audit
- interfaces and interactions with hardware, software or other AI systems that are not part of the assessment object, where material for its function, delineation or intended purpose
- forms of provision and use of the assessment object (e.g. embedded component, local installation, API, platform-based provision), where material
- intended technical operating environment and material hardware dependencies of the assessment object, where material
- system-wide configurations and integration logics, where material for understanding how the assessment object functions

#### **c) Operational and deployment context of the assessment object**

- intended purpose of the assessment object at the provider, or specific deployment context at the deployer
- deployment mode (e.g. isolated, embedded, on-premise)
- human oversight (degree of autonomy, intervention and fallback mechanisms)
- operational conditions (technical, data-related and use-related limitations)
- basic description of the user or interaction interface, where material for use, monitoring or intervention in operations
- known limits of use, excluded conditions of use and foreseeable misuse, where material for the intended purpose
- material assumptions regarding the operating environment of the assessment object, where required for understanding its intended purpose and its system boundaries

#### **d) Life cycle reference**

- current life cycle phase of the assessment object, where applicable
- relevant life cycle processes
- relevant change mechanisms of the assessment object, including predetermined changes, where these may affect the characteristics, intended purpose or boundaries of the assessment object

{14}------------------------------------------------

• adaptation and further development mechanisms of the assessment object after putting into service, where material

#### **e) Function of the assessment object**

- type of task(s) (e.g. classification, regression, generation, ranking)
- specification of inputs and outputs (types, rules, constraints)
- description of the processing
- model architecture at a high level
- general logic and material functioning of the assessment object
- key design decisions and material assumptions, where material for the function, limits of use or assessment of the assessment object
- intended target metrics, optimisation logics or quality objectives, where material
- expected type and quality of the outputs, as well as known functional limits of the assessment object
- basic error characteristics and foreseeable malfunctions, where known and material

#### **f) AI-specific characteristics**

- AI technology used (e.g. machine learning, deep learning, symbolic AI)
- learning paradigm (e.g. supervised, unsupervised, reinforcement)
- adaptation behaviour (e.g. static, continuous)
- use of pre-trained models, foundation models, third-party models or other upstream AI contributions, as well as their integration, adaptation or modification, where material
- material characteristics of the model behaviour, where material for the description of the assessment object

#### **g) Data-related characteristics**

- sources, collection and labelling of the training data
- data lineage and provenance
- information on validation and test data and their governance, where material
- material features, scope and composition of the datasets used for training, validation and testing
- selection, preparation, cleansing and, where applicable, augmentation steps, where material
- relationship and delineation between training, validation and test data, where material
- known data gaps, underrepresentation or other material limitations of the data basis, where material

The description of the assessment object must be provided in a level of detail that enables an appropriate delineation of the system boundaries of the assessment object and the audit of the controls established for it with reasonable assurance.

### <span id="page-14-0"></span>3.4.3 Criteria to be Applied

The set of criteria to be assessed is determined by the profile selected for the assessment object. The structure and functioning of profiles are set out in section 2.2. The responsible party selects the profile appropriate for its assessment object; the selection must appropriately reflect the assessment object and its 

{15}------------------------------------------------

intended purpose. As a matter of principle, all A5 criteria contained in a profile are deemed applicable and are binding.

The responsible party may designate individual A5 criteria within the selected profile as not applicable, subject to justification. Justifications must be limited to the type and design of the assessment object, to the role of the responsible party in relation to the assessment object, or to the controls established for the assessment object. In particular, A5 criteria may not be excluded from the scope of the audit because the responsible party's controls were not suitably designed or did not operate effectively to meet those A5 criteria, or because the responsible party is unwilling or unable to demonstrate conformity. Where a criterion requires a risk-based approach and the responsible party's risk assessment concludes that there are no risks to be mitigated, this assessment shall likewise be included when setting out the applicability of the criterion.

The selected profile, the resulting set of criteria and, where applicable, the justifications for excluding individual A5 criteria are to be set out by the responsible party in the system description.

## <span id="page-15-0"></span>3.4.4 Subject Matter and Objective of the Audit

The subject matter of the audit is the system description prepared by the responsible party and the controls described therein. The controls form part of the internal control system established for the assessment object and relate to the A5 criteria. The audit is based on a written statement by the responsible party's management (management statement) regarding the suitability of the design of the controls to meet the applicable A5 criteria as of the specified date (Type 1 report) and, where so engaged, the operating effectiveness of the controls throughout the specified period (Type 2 report).

The objective of the audit is to enable the practitioner to reach a conclusion, with reasonable assurance, as to whether

- the system description fairly presents the assessment object and the controls established for it as of the specified date (Type 1 report) or throughout the specified period (Type 2 report), in accordance with the description criteria set out in section 3.4.5.1 of this A5 Audit Methodology;
- the controls presented in the system description are suitably designed and implemented as of the specified date (Type 1 report) to meet the applicable A5 criteria;
- where so engaged (Type 2 report), the controls presented in the system description operated effectively throughout the specified period to meet the applicable A5 criteria.

Type 1 reports are only permissible for an initial engagement. Subsequent audits must be designed as Type 2 reports. In the case of a Type 2 report, the specified period should cover at least three months. For shorter periods, the practitioner cannot obtain sufficient evidence regarding the operating effectiveness of the controls. The period should not exceed twelve months. In exceptional cases, the period may extend beyond twelve months, for example in order to enable better alignment with other audits. As a matter of principle, consistency in the audit period is recommended.

The practitioner's conclusion on the design and operation of the responsible party's controls may relate to complementary subservice organisation controls (CSOCs) and/or complementary user entity controls (CUECs) at users and other parties which the responsible party took into account when designing its own controls in order to meet the A5 criteria. Owing to shared responsibilities between the responsible party, subservice organisations (e.g. providers of upstream AI components, data suppliers, infrastructure or platform providers) and users, it is likely that complementary controls, together with the responsible party's controls, are required in order to meet certain A5 criteria. The practitioner's procedures do not extend to the actual controls at users and other parties, but are limited in this respect to the appropriate presentation, in the system description, of the responsible party's assumptions regarding these

{16}------------------------------------------------

complementary controls. With respect to the complementary subservice organisation controls (CSOCs), section 3.4.6 applies.

In the view of the BSI, responsible parties that already have a system description may reuse it in audits in accordance with this A5 Audit Methodology. However, an existing system description that meets the requirements of another standard may need to be adapted to the description criteria of this A5 Audit Methodology.

### <span id="page-16-0"></span>3.4.5 Requirements for the System Description and the Management Statement

#### 3.4.5.1 System Description

The system description of the assessment object is to be prepared in accordance with the following description criteria.

1.) The system description must fairly present the assessment object as it was designed and implemented as of the specified date (Type 1 report) or throughout the specified period (Type 2 report). For this purpose, it must contain at least the following information, so that the intended addressees obtain sufficient transparency regarding the trustworthiness of the assessment object and the fulfilment of the applicable A5 criteria:

- 1. a description of the assessment object in accordance with the minimum content of section 3.4.2, including the designation, type and scope of the assessment object, its intended purpose, the role of the responsible party, its system boundaries, as well as the constituent parts, functions, interfaces, dependencies and other relevant characteristics that are material for its intended purpose; the presentation must be provided in the level of detail required for the audit;
- 2. the selected profile, the applicable A5 criteria resulting therefrom, and the justification where individual criteria have been classified as not applicable;
- 3. the controls established for the assessment object, including the control environment, risk assessment, control activities, information and communication processes, and monitoring activities, to the extent that these are relevant to the fulfilment of the applicable A5 criteria;
- 4. the handling of significant events (cf. below) and circumstances that constitute exceptions to normal operation, in particular security incidents, failures of material constituent parts of the assessment object, and other events such as significant malfunctions, unexpected behaviour or impairments of the reliability of the assessment object, to the extent that these are material to the fulfilment of the applicable A5 criteria or to the secure operation of the assessment object;
- 5. the required CUECs at users and other parties which were taken into account while designing the controls, to the extent that the fulfilment of individual applicable A5 criteria also depends on such controls;
- 6. the functions and services of subservice organisations and other external parties, as well as outsourced functions in relation to the applicable A5 criteria, including
  - the nature of the services obtained, including the identity of the external party involved, the location of processing and storage of relevant data where material, the complexity and uniqueness of the services obtained, the resulting dependency of the responsible party, and the availability of relevant audit or reporting evidence, where available;
  - the types of CSOCs whose performance is required at the subservice organisation or other external party so that, together with the responsible party's controls, the applicable A5 criteria can be met;

{17}------------------------------------------------

• the responsible party's controls for the selection, integration, management, monitoring and assessment of subservice organisations and other external parties, as well as for monitoring the effectiveness of the controls required therein.

In the case of an assessment of operating effectiveness (Type 2 report), the system description must be supplemented by the following content:

- 1. material changes to the controls established for the assessment object in relation to the applicable A5 criteria that were carried out during the audit period;
- 2. the occurrence and handling of significant events during the audit period that constituted exceptions to normal operation, fell within the responsible party's area of responsibility and resulted in
  - contractual agreements on the availability of, or on material performance characteristics of, the assessment object not being met, or
  - unauthorised third parties gaining access to data processed or stored in connection with the assessment object, or
  - the integrity of processed or stored data, or of other system constituent parts material to the assessment object, being impaired and the protective measures established for this purpose not being effective,
- 3. as well as the measures initiated by the responsible party to prevent such events in the future.

An event is typically significant where several affected parties or users were concerned by it and where the affected persons themselves or the public were informed of it by the responsible party. The information on the events and the protective measures established must be made transparent to the greatest extent possible, without disclosing vulnerabilities or potential attack surfaces. Furthermore, the system description must not endanger the confidentiality of information worthy of protection and shall therefore not contain an unnecessarily granular presentation of individual events.

2.) The system description must not omit or misrepresent any information that is relevant to the fulfilment of the applicable A5 criteria. This does not mean that all aspects of the assessment object that might be regarded as important by individual intended addressees must be presented. Rather, it is to be taken into account that the system description serves the common information needs of a broad range of intended addressees and therefore is not required to fully cover every particular information need of individual addressees.

### 3.4.5.2 Management Statement

The management of the responsible party must provide a written statement (management statement) in which it confirms that

- the system description fairly presents the assessment object and the controls established for it as of the specified date (Type 1 report) or throughout the specified period (Type 2 report), in accordance with the description criteria set out in section 3.4.5.1 of this A5 Audit Methodology;
- the controls presented in the system description are suitably designed and implemented as of the specified date (Type 1 report) to meet the applicable A5 criteria;
- where so engaged (Type 2 report), the controls presented in the system description operated effectively throughout the specified period to meet the applicable A5 criteria.

In addition to the description criteria, the following assessment requirements are to be applied as a basis for the statement:

• the risks that may prevent the fulfilment of the applicable A5 criteria have been identified;

{18}------------------------------------------------

- the controls presented in the system description have been implemented as presented and, if they operate effectively, are suitable to address these risks in such a way that the applicable A5 criteria can be met;
- where a Type 2 report has been engaged, the controls presented in the system description operated effectively throughout the specified period; this presupposes that the controls were applied consistently in accordance with their design and that manual controls were performed by persons with the appropriate competence and authority.

Where, in the case of a Type 2 report, the management statement covers a period of more than twelve months, the reason for this must be stated in the statement.

The management of the responsible party must have a reasonable basis for its written statement. In the case of a Type 2 report, this basis may draw on the responsible party's monitoring activities regarding the effectiveness of the controls over time. This involves identifying and reporting deviations to appropriate individuals within the responsible party's organisation, as well as taking necessary corrective actions. The responsible party may accomplish the monitoring of controls through ongoing activities, separate assessments, or a combination of both. Internal auditors or personnel performing similar functions may contribute to such activities. It may also include using information communicated by external parties, such as feedback from users or customers or comments from supervisory or regulatory authorities, which may indicate problems or highlight areas in need of improvement in relation to the assessment object or the controls established for it. The fact that the practitioner assesses the operating effectiveness of the controls is not a substitute for the responsible party's own processes to provide a reasonable basis for its statement.

### <span id="page-18-0"></span>3.4.6 Consideration of Subservice Organisations

Where applicable, the responsible party outsources parts of its development, provisioning, integration, operation or support processes relevant to the assessment object to other companies or service providers or obtains corresponding services from them. The responsible party must present this in its system description, and the practitioner must take it into account accordingly in the audit.

A company or service provider is to be regarded as a subservice organisation within the meaning of this A5 Audit Methodology where the following conditions are met cumulatively:

- there is an ongoing or recurring service relationship between the responsible party and the company or service provider;
- the services provided by the company or service provider are relevant for understanding the assessment object, its system boundaries, its mode of operation or its integration into the AI value chain; and
- the fulfilment of applicable A5 criteria requires complementary controls to be established at the company or service provider.

These may include, in particular, providers of upstream AI models or components, data suppliers, infrastructure or platform providers, annotation or labelling service providers, integration partners, and other external service providers.

A service provider for which no complementary controls are required for the fulfilment of applicable A5 criteria is not a subservice organisation within the meaning of this A5 Audit Methodology.

The inclusive method is to be applied for the consideration of subservice organisations. Under the inclusive method, the complementary controls of the subservice organisation that are relevant to the assessment object and the applicable A5 criteria are likewise the subject of the responsible party's system description and its assessment. The practitioner therefore also assesses the complementary controls of the subservice organisation with regard to their suitability of design and, where applicable, their operating effectiveness.

{19}------------------------------------------------

To the extent that third-party audit reports are already available for a subservice organisation or for externally procured AI components, the practitioner may evaluate and take these into account in accordance with general professional principles. The responsibility for the practitioner's own conclusion remains with the practitioner.

The responsible party must establish appropriate monitoring activities for subservice organisations in order to assess the continuing suitability and effectiveness of the services they provide and of the complementary controls required for this purpose. The responsible party ultimately remains responsible for ensuring that the assessment object and the controls established for it meet the applicable A5 criteria.

Where subservice organisations exist, the responsible party must disclose, in particular, the following information in the system description:

- 1. the nature of the services provided by the subservice organisation, including
  - the name of the company with which a contractual or service relationship exists for the services provided;
  - the nature of the service relationship and the role of the subservice organisation in the AI value chain, in particular whether it is a provider of upstream AI models or components, a data supplier, an infrastructure or platform provider, an annotation or labelling service provider, an integration or implementation partner, or another service provider;
  - the assessment of the complexity and uniqueness of the services provided, as well as the resulting dependency of the responsible party on the subservice organisation;
  - the availability of relevant audit or reporting evidence, where available;
- 2. the types of complementary controls whose establishment and performance is required at the subservice organisation in order to meet the applicable A5 criteria with reasonable assurance together with the responsible party's controls;
- 3. the responsible party's controls that serve to select, integrate, manage, monitor and assess subservice organisations, as well as to monitor the effectiveness of the complementary controls required at the subservice organisation.

## <span id="page-19-0"></span>3.4.7 Obtaining Evidence Regarding the System Description

The practitioner must obtain and read the responsible party's system description and assess whether the parts of the system description within the scope of the audit are fairly presented.

In particular, it must be assessed whether the system description contains the description criteria set out in section 3.4.5.1 and whether the description of the assessment object, its system boundaries and the controls established for it has been carried out in a comprehensible and appropriate manner to the extent necessary for the audit.

The practitioner must determine, through other suitable audit procedures in combination with inquiries, whether the assessment object and the controls included in the audit have actually been implemented or were applied throughout the specified period. These procedures include, in particular, observation and the inspection of records and other documentation regarding the manner in which the object operates and the controls are applied.

A system description is to be regarded as fairly presented only if it has been prepared in accordance with the requirements of this A5 Audit Methodology. Particular attention is to be paid to the description criteria of the system description, the minimum content of the description of the assessment object pursuant to section 3.4.2, and, where relevant, the consideration of subservice organisations and of complementary controls at users and other parties.

{20}------------------------------------------------

## <span id="page-20-0"></span>3.4.8 Assessing the Fulfilment of Criteria

The practitioner must assess the fulfilment of each applicable A5 criterion. The assessment is carried out on the basis of the risks identified by the responsible party that may prevent the fulfilment of the respective criterion, as well as the combination of controls assigned to the criterion by which these risks are addressed, and the interaction of those controls.

The responsible party must prepare its own system description for the assessment object in accordance with the requirements of this A5 Audit Methodology. To the extent that the responsible party draws on existing documentation, controls or evidence from other audit or certification contexts, it must ensure that the applicable A5 criteria are nevertheless fully covered. A reference to other audit results or certifications does not replace the responsible party's own presentation in the system description.

The practitioner must inform the responsible party of any gaps identified where the controls presented in the system description do not fully cover individual applicable A5 criteria or individual aspects of such criteria.

To the extent that the responsible party can provide evidence, for aspects not covered, of additional controls that have actually been implemented but have not yet been presented in the system description, it must include these controls in the system description or adjust the existing control descriptions accordingly.

Where the practitioner determines that a material deviation exists, it must modify its conclusion in the report with regard to the affected A5 criteria. A material deviation may exist in particular where:

- the system description does not fairly present the internal control system in material respects (weakness in the system description);
- controls are not suitably designed to address the identified risks and to meet the applicable A5 criteria;
- controls are suitably designed but have not been implemented as presented in the system description; or
- controls did not operate effectively during the specified period (only in the case of Type 2 reporting).

The conclusion is modified by means of a qualification or, where the deviation identified is so pervasive that a qualification is not sufficient, by means of an adverse conclusion.

### <span id="page-20-1"></span>3.4.9 Obtaining Evidence Regarding the Suitability of Design

The practitioner must assess whether the responsible party's controls are suitably designed to meet the applicable A5 criteria. A control is suitably designed to the extent that, individually or in combination with other controls, it provides reasonable assurance, when complied with satisfactorily, that the identified risks which prevent the fulfilment of the assigned A5 criteria are effectively addressed. In assessing the suitability of design, the practitioner must take into account, in particular:

- 1. whether the control (where applicable, in combination with other controls) covers the identified risks and the aspects of the assigned A5 criteria at all levels;
- 2. to the extent that a criterion requires a risk-based approach: whether the responsible party's risk assessment has been carried out appropriately, in particular with regard to the completeness and accuracy of the identified threats and vulnerabilities in comparison with the practitioner's own risk assessment;

{21}------------------------------------------------

- 3. the frequency or timing of the execution of the control;
- 4. the authority and competence of the individual responsible for performing the control, in particular their hierarchical position, role within the organisation and any conflicting duties;
- 5. the tasks performed within the control, as well as their precision and sensitivity, in particular the results of reviews and related follow-up measures;
- 6. whether the information used in performing the control is reliable;
- 7. whether the control is appropriately adapted to changing circumstances, for example in the case of organisational changes or new risks, threats and vulnerabilities;
- 8. whether the control has been implemented as presented in the system description as at the specified date (Type 1 reporting) or throughout the specified period (Type 2 reporting).

#### <span id="page-21-0"></span>3.4.10 Handling Deviations

The handling of identified deviations relating to the system description, the design of the controls or their operating effectiveness is governed by the audit standards. Where the practitioner identifies a deviation, it must perform, in particular, the following audit procedures in order to assess whether the deviation is material and leads to a modification of the conclusion:

- inquiry of the responsible party's management regarding the root cause of the identified deviation;
- evaluation of how the responsible party has dealt with the identified deviation;
- examination of whether comparable deviations were identified by the responsible party's monitoring activities and which corrective actions were initiated as a result;
- examination of whether compensating controls are suitably designed and, in the case of Type 2 reporting, operated effectively, so as to address the risks arising from the deviation in such a way that the applicable A5 criteria can be met with reasonable assurance.

Where the practitioner concludes that

- 1. the responsible party's system description does not fairly present, in all material respects, the assessment object and the controls established for it,
- 2. the controls assigned to the applicable A5 criteria are not suitably designed, in all material respects, to address the identified risks and to meet the applicable A5 criteria,
- 3. in the case of Type 2 reporting, the assessed controls did not operate effectively in all material respects, or
- 4. the practitioner is unable to obtain sufficient appropriate evidence (special case of a limitation),

then a material deviation exists and the conclusion must be modified. In this case, the report must contain a separate section with a clear presentation of all reasons for the modification.

The audit procedures performed and their results, including all identified deviations, must be presented in the report, irrespective of whether the conclusion is modified. This information is intended to enable the intended addressees to assess the effects of the identified deviations on their risk assessment.

For this purpose, the following additional information from the responsible party must, in particular, be attached to the report:

• where the deviation was detected by the responsible party itself, when and in the course of which measures this occurred;

{22}------------------------------------------------

- where the deviation was already presented in a previous report, a reference to that report as well as an explanation of why the deviation has not yet been remedied by effective corrective and preventive actions;
- planned or already initiated corrective and preventive actions to eliminate the causes of the deviation and to prevent comparable deviations in the future, including the point in time at which these actions are expected to be completed or effectively implemented.

This additional information is not the subject of the audit. The practitioner does not express a conclusion on it. It must be presented in a separately marked section of the report, for example under the heading "Other Information Provided by the Responsible Party".

#### <span id="page-22-0"></span>3.4.11 Reporting

The reporting is governed, mutatis mutandis, by the requirements of ISAE 3402.53. The details result from the provisions set out below.

The reporting must comprise the following components:

- 1. Independent Practitioner's Reasonable Assurance Report
  - 1. Scope

In this section, the practitioner must refer to the system description and to the statement of the responsible party's management.

Where the system description contains a reference to the necessity of complementary controls at users or other parties, it must be stated that the practitioner has assessed neither the suitability of the design nor, in the case of Type 2 reporting, the operating effectiveness of these complementary controls, and that the applicable A5 criteria can only be met if these complementary controls, together with the responsible party's controls, are suitably designed and, where relevant, operate effectively.

Where services are provided by subservice organisations, the nature of the activities performed by the subservice organisations must be presented in accordance with the system description. Furthermore, it must be stated that the responsible party's system description also covers the complementary controls of the subservice organisation and that the practitioner's audit procedures have also extended to these complementary controls.

2. Responsibility of the Responsible Party

It must be stated that the responsible party is responsible for:

- the preparation of the system description and the management statement, including the completeness, accuracy and method of presentation;
- the provision, operation or other use, for which it is responsible, of the assessment object presented in the system description;
- the selection of the profile applied and the resulting determination of the applicable A5 criteria;
- the identification of the risks that may prevent the fulfilment of the applicable A5 criteria; and
- the design, implementation, maintenance, monitoring and documentation of the controls that are suitably designed and, in the case of Type 2 reporting, operate effectively to address the identified risks and to meet the applicable A5 criteria.
- 3. Independence and Quality Management of the Practitioner or the Audit Firm

{23}------------------------------------------------

It must be stated that the audit firm

- complies with the independence requirements and other professional ethical requirements of the International Code of Ethics for Professional Accountants (including International Independence Standards) of the International Ethics Standards Board for Accountants (IESBA Code), which is founded on the fundamental principles of integrity, objectivity, professional competence and due care, confidentiality and professional behaviour;
- applies the International Standard on Quality Management (ISQM) 1 or other professional requirements or legal or regulatory provisions that are at least as demanding as ISQM 1; and
- has complied with the supplementary requirements for the qualification of the engagement team pursuant to section 3.4.12 of this A5 Audit Methodology.

Where the practitioner is not a public auditor or an audit firm, the professional requirements or legal or regulatory provisions applied that are at least as demanding as the IESBA Code and ISQM 1 must be named.

4. Responsibility of the Practitioner

It must be stated that the practitioner's responsibility is to express, on the basis of the audit procedures performed, a conclusion as to whether the responsible party's system description fairly presents, in all material respects, the assessment object and the controls established for it, whether the controls are suitably designed, in all material respects, to meet the applicable A5 criteria and, in the case of Type 2 reporting, operated effectively in all material respects.

5. Inherent Limitations

Reference must be made to the inherent limitations of controls. In the case of Type 2 reporting, reference must additionally be made to the risk that the assessment of the operating effectiveness of controls for past periods is not readily transferable to future periods.

6. Conclusion

The practitioner's conclusion must be aligned with the audit objectives set out in section 3.4.4.

7. Intended Addressees and Restricted Use

It must be stated for which specific addressees the reporting is intended. Intended addressees within the meaning of this A5 Audit Methodology are users of the assessment object (existing and potential customers), their independent practitioners, service providers of those users, as well as supervisory and regulatory authorities, to the extent that they possess sufficient knowledge and understanding with regard to:

- the designation, nature and scope of the assessment object;
- the nature of the assessment object and its intended use case;
- the interaction of the assessment object with users, subservice organisations and other parties involved;
- internal controls and their limits;
- complementary controls at users and other parties and their interaction with the responsible party's controls to meet the applicable A5 criteria;
- responsibilities of users or other parties involved and their influence on the appropriate use of the assessment object;
- the A5 criteria; and

{24}------------------------------------------------

- the risks that may prevent the fulfilment of the applicable A5 criteria, as well as the manner in which controls address these risks.
- 8. General Engagement Terms

Reference must be made to the engagement terms, for practitioners in Germany typically on the basis of the General Engagement Terms for German Public Auditors and Public Audit Firms (Allgemeine Auftragsbedingungen für Wirtschaftsprüfer und Wirtschaftsprüfungsgesellschaften). This section must also contain information on applicable liability provisions, as these may be of significance for the specific addressees of the reporting. In the case of audits outside statutory reserved duties, the practitioner's liability is generally governed by civil law provisions and may be further specified by contractual agreements. Such agreements may be made individually or through the incorporation of pre-formulated contractual terms. Any existing liability agreement must be referred to in the reporting.

#### 2. Management Statement

Written statement of the responsible party's management in accordance with the requirements of section 3.4.5.2 of this A5 Audit Methodology.

3. Presentation of the System Description

Presentation of the assessment object and the controls established for it in accordance with the description criteria of section 3.4.5.1 of this A5 Audit Methodology.

4. The Responsible Party's Controls, the Practitioner's Audit Procedures and Results

Presentation of the responsible party's controls in relation to the applicable A5 criteria, of the audit procedures performed by the practitioner, and of the results. The audit procedures must be presented in both types of report, that is, in both Type 1 reporting and Type 2 reporting.

In describing the audit procedures, the practitioner must present, in particular:

- the nature of the audit procedures performed (e.g. inquiry, observation, inspection or reperformance) in sufficient detail to enable the intended addressees to assess the effects on their risk assessment. This includes stating the function and role of the responsible party's personnel to whom inquiries were directed, as well as abstract descriptions of the documents or electronic files on which the practitioner relied in order to obtain evidence;
- the extent of the audit procedures, including a statement as to whether the elements assessed represent the entirety or a selection (sample) from the population. Even though it is not necessary to state the exact number of elements in the population and the sample size for each individual audit procedure, the practitioner must at least present the general approach to determining the extent of the audit, for example by disclosing sample sizes for ranges of elements in the population or the frequency of a control.

The presentation of the results may be limited to the statement "No deviations identified", provided that no deviations were identified. Where deviations were identified, the practitioner must present the extent of the audit procedures that led to the identification of these deviations, including the sample size where sampling was used, as well as the number and nature of the deviations identified. Deviations must also be presented where the practitioner has concluded, on the basis of the audit procedures performed, that the affected applicable A5 criteria were nevertheless met.

5. Optional: Other Information Provided by the Responsible Party

The responsible party may use this component to present further information, in particular comments on identified deviations or mappings of controls to other standards. This information is not the subject of the audit; the practitioner does not express a conclusion on it.

{25}------------------------------------------------

## <span id="page-25-0"></span>3.4.12 Qualification of the Practitioner

Under ISAE 3000 (Revised), the practitioner must determine, before accepting an engagement, that the professional obligations are complied with, for practitioners in Germany in particular those under section 43 of the German Public Accountant Act (WPO), including the obligation of independence.

On the basis of its understanding of the subject matter, the practitioner must assess whether the members of the engagement team entrusted with the engagement possess the professional competence required to carry out the audit, a sufficient understanding of the relevant professional and technical environment, and the necessary skills. The practitioner must further assess whether the experience required to carry out the engagement in relation to the relevant professional, methodological and regulatory requirements is present within the engagement team or can be ensured in an appropriate manner.

The BSI takes the view that audits in accordance with the A5 criteria and this A5 Audit Methodology place heightened requirements on the professional qualification and practical experience of the practitioner and the engagement team. The qualifications and experience set out below serve as indicators that these requirements are met. Those members of the engagement team who, under the International Standard on Quality Management (ISQM) 1 or the corresponding German quality management standard of the IDW, are responsible for the ongoing monitoring of the conduct of the engagement and for the final review of the engagement results must possess these qualifications and experience.

These include, in particular:

• at least three years of relevant professional experience with IT audits in a public audit firm,

or one of the following qualifications or certifications:

- Information Systems Audit and Control Association (ISACA) Certified Information Systems Auditor (CISA),
- Information Systems Audit and Control Association (ISACA) Certified Information Security Manager (CISM),
- Information Systems Audit and Control Association (ISACA) Certified in Risk and Information Systems Control (CRISC),
- ISO/IEC 27001 Lead Auditor, or an ISO 27001 auditor certified by the BSI for audits on the basis of BSI IT-Grundschutz,
- ISO 42001 Lead Implementer: Artificial Intelligence Management System (AIMS),
- ISACA Advanced in AI Audit (AAIA),
- CSA AI Control Matrix STAR AI Controls Auditor.

The practitioner must be able to demonstrate appropriately, at the request of the client, that the engagement team possesses the necessary qualifications.

Confirmation of the fulfilment of the qualification requirements is provided in the section "Independence and Quality Management of the Practitioner or the Audit Firm" of the assurance report (component 1 of the reporting).

### <span id="page-25-1"></span>3.4.13 Information on the Limitation of Liability

In the view of the BSI, information on liability provisions constitutes significant information for the recipients of the report.

In the case of audits outside statutory reserved duties, the practitioner's liability is based on civil law provisions, which may be specified by contractual agreements. Liability agreements are possible both through individual provisions and through standardised contractual terms.

{26}------------------------------------------------

The relevant explanations may be provided, for example, in the section "Reference to the Engagement Terms" (where applicable, with a reference to further annexes).

Accordingly, any liability agreements made must be documented in the reporting. The presentation is typically provided in the report section "Reference to the Engagement Terms" or by reference to attached documents.

## <span id="page-26-0"></span>3.5 Dealing with Revisions of the A5 Audit Methodology (based on ISAE 3000)

The BSI intends to update this A5 Audit Methodology regularly in order to take account of both general technological progress and the continuous further development of the underlying standards.

The BSI grants responsible parties and practitioners an appropriate lead time to carry out the adjustments to the assessment object, to the controls established for it, and to the conduct of the audit that are required as a result of updates to the A5 Audit Methodology.