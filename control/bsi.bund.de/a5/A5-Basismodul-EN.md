

{0}------------------------------------------------


# A5 – Horizontal Trustworthiness Core Module


{1}------------------------------------------------

# Change history

| Version | Date            | Name | Description     |
|---------|-----------------|------|-----------------|
| 0.9     | 30 June<br>2026 | T 24 | First published |

*Table1: Revision history*

Federal Office for Information Security PO Box 20 03 63 53133 Bonn Email: aisecurity@bsi.bund.de Website: https://www.bsi.bund.de © Federal Office for Information Security 2026

{2}------------------------------------------------

# Table of Contents

| 1     |       | Introduction<br>6                                                                 |    |
|-------|-------|-----------------------------------------------------------------------------------|----|
|       | 1.1   | About the A56                                                                     |    |
| 1.2   |       | Nature and Structure6                                                             |    |
|       | 1.3   | Dimensions of Trustworthiness6                                                    |    |
| 2     |       | Governance, Compliance and Scope (GCS)8                                           |    |
|       | 2.1   | GCS.1 Stakeholder & Impact Scoping8                                               |    |
|       | 2.1.1 | GCS.1.1 Establish a risk management process<br>8                                  |    |
|       | 2.1.2 | GCS.1.2 Risk management process for traceability risks9                           |    |
|       | 2.1.3 | GCS.1.3 Risk management process for explainability risks<br>                      | 10 |
| 2.1.4 |       | GCS.1.4 Risk management process for human agency and oversight risks              | 11 |
|       | 2.1.5 | GCS.1.5 Risk management process for performance risks                             | 12 |
|       | 2.1.6 | GCS.1.6 Risk management process for robustness risks<br>                          | 13 |
|       | 2.1.7 | GCS.1.7 Risk management process for bias risks                                    | 14 |
|       | 2.2   | GCS.2 Defining Governance, Roles & Policies                                       | 15 |
|       | 2.2.1 | GCS.2.1 Document risk management guidelines                                       | 15 |
|       | 2.2.2 | GCS.2.2 Document development guidelines                                           | 16 |
|       | 2.2.3 | GCS.2.3 Document the AI policy                                                    | 17 |
|       | 2.2.4 | GCS.2.4 Document AI provisions in General Terms and Conditions/EULAs              | 18 |
|       | 2.3   | GCS.3 Define metrics and measurement framework                                    | 19 |
|       | 2.3.1 | GCS.3.1 Establish a quality management process                                    | 19 |
|       | 2.3.2 | GCS.3.2 Quality management process for transparency                               | 20 |
|       | 2.3.3 | GCS.3.3 Quality management process for robustness                                 | 21 |
|       | 2.3.4 | GCS.3.4 Quality management process for performance                                | 22 |
|       | 2.3.5 | GCS.3.5 Quality management process for bias<br>                                   | 23 |
|       | 2.3.6 | GCS.3.6 Quality management process for explainability<br>                         | 24 |
|       | 2.4   | GCS.4 Privacy Governance & Data Protection                                        | 25 |
|       | 2.4.1 | GCS.4.1 Establish a process for exercising data subjects' and users' rights<br>   | 25 |
|       | 2.5   | GCS.5 Security Governance: Protection Objectives & Threat Modelling, Red Teaming  | 26 |
|       | 2.5.1 | GCS.5.1 Establish measures and security controls for access to AI data            | 26 |
|       | 2.5.2 | GCS.5.2 Establish tiered security controls<br>                                    | 27 |
|       | 2.5.3 | GCS.5.3 Establish architecture and design decisions based on 'Security-by-Design' | 28 |
|       | 2.5.4 | GCS.5.4 Risk management process for AI-specific vulnerability management          | 29 |
|       | 2.6   | GCS.6 Human Oversight (HO), Human in the Loop (HITL) & Competence<br>             | 30 |
|       | 2.6.1 | GCS.6.1 Establish a process to protect human integrity<br>                        | 30 |
|       | 2.6.2 | GCS.6.2 Establish mechanisms for challenging and correcting decisions<br>         | 31 |
|       | 2.6.3 | GCS.6.3 Quality management process for human agency and oversight                 | 32 |

{3}------------------------------------------------

|   | 2.6.4 | GCS.6.4 Establish a competence and training process                           | 33 |
|---|-------|-------------------------------------------------------------------------------|----|
|   | 2.6.5 | GCS.6.5 Establish a transparency and user protection process                  | 34 |
| 3 |       | Design, Engineering and Integration (DEI)                                     | 35 |
|   | 3.1   | DEI.1 Data Acquisition (Acquire)                                              | 35 |
|   | 3.1.1 | DEI.1.1 Establish a data management process                                   | 35 |
|   | 3.1.2 | DEI.1.2 Data management process for training data                             | 36 |
|   | 3.1.3 | DEI.1.3 Data management process for validation data<br>                       | 37 |
|   | 3.1.4 | DEI.1.4 Data management process for test data                                 | 38 |
|   | 3.2   | DEI.2 Data validation & quality checks                                        | 39 |
|   | 3.2.1 | DEI.2.1 Establish a data quality process<br>                                  | 39 |
|   | 3.2.2 | DEI.2.2 Data quality process to ensure completeness and coverage              | 40 |
|   | 3.3   | DEI.3 Data Documentation & Lineage<br>                                        | 41 |
|   | 3.3.1 | DEI.3.1 Establish a Data Provenance Process                                   | 41 |
|   | 3.4   | DEI.4 Define baseline/heuristics & model approach                             | 42 |
|   | 3.4.1 | DEI.4.1 Establish a development process                                       | 42 |
|   | 3.5   | DEI.5 Integration of external models                                          | 43 |
|   | 3.5.1 | DEI.5.1 Document AI system architecture<br>                                   | 43 |
|   | 3.5.2 | DEI.5.2 Document the use of pre-trained models                                | 44 |
|   | 3.5.3 | DEI.5.3 Document upstream AI products                                         | 45 |
| 4 |       | Verification and Validation (VAV)                                             | 46 |
|   | 4.1   | VAV.1 Security/Robustness Testing<br>                                         | 46 |
|   | 4.1.1 | VAV.1.1 Quality management process for AI-specific cybersecurity              | 46 |
| 5 |       | Deployment (DEP)                                                              | 47 |
|   | 5.1   | DEP.1 Deployment Plan & Release<br>                                           | 47 |
|   | 5.1.1 | DEP.1.1 Establish change management and release procedures                    | 47 |
| 6 |       | Operations, Performance and Supervision (OPS)                                 | 48 |
|   | 6.1   | OPS.1 Monitoring in Production                                                | 48 |
|   | 6.1.1 | OPS.1.1. Data management process for operational and input data               | 48 |
|   | 6.1.2 | OPS.1.2 Establish a monitoring process                                        | 49 |
|   | 6.1.3 | OPS.1.3 Monitoring process for robustness<br>                                 | 50 |
|   | 6.1.4 | OPS.1.4 Monitoring process for data in operation                              | 51 |
|   | 6.1.5 | OPS.1.5 Monitoring process for performance-                                   | 52 |
|   | 6.1.6 | OPS.1.6 Monitoring process for AI-specific cybersecurity                      | 53 |
|   | 6.1.7 | OPS.1.7 Monitoring process for security-related incidents in the supply chain | 54 |
|   | 6.1.8 | OPS.1.8 Establish a logging process                                           | 55 |
|   | 6.2   | OPS.2 Incident Response & Rollback                                            | 56 |
|   | 6.2.1 | OPS.2.1 Establish a security incident reporting process<br>                   | 56 |
|   | 6.2.2 | OPS.2.2 Establish emergency shutdown and fallback mechanisms                  | 57 |
|   |       |                                                                               |    |

{4}------------------------------------------------

| 6.2.3 | OPS.2.3 Establish an incident management process<br>                                | 58 |
|-------|-------------------------------------------------------------------------------------|----|
| 6.2.4 | OPS.2.4 Incident management process for security-related events in the supply chain | 59 |
| 6.3   | OPS.3 Iteration: Retraining & Updates                                               | 60 |
| 6.3.1 | OPS.3.1 Establish a quality metric adjustment process<br>                           | 60 |
| 6.4   | OPS.4 Maintenance & Support                                                         | 61 |
| 6.4.1 | OPS.4.1 Establish a complaints and feedback process                                 | 61 |
| 7     | Retirement (RET)                                                                    | 62 |
| 7.1   | RET.1 Decommissioning / Retirement<br>                                              | 62 |
| 7.1.1 | RET.1.1 Establish an end-of-life process                                            | 62 |

{5}------------------------------------------------

# <span id="page-5-0"></span>1 Introduction

# <span id="page-5-1"></span>1.1 About the A5

The trustworthiness of AI systems has become a key prerequisite for their responsible use, from technical, organisational and regulatory perspectives alike. For decision-makers, this concerns the reliability, security and legal compliance of AI applications; for developers, it concerns the foundation for robust, traceable and controllable systems. AI that is inadequately secured can not only lead to erroneous or distorted results, but also pose significant risks to security, fundamental rights and societal acceptance. With the European Union's AI Act, the Cyber Resilience Act and other regulatory frameworks, the requirements for trustworthy AI are no longer merely best practice but are increasingly becoming a measurable and verifiable prerequisite for the admissibility and marketability of many AI systems.

The 'AI Audit and Assurance Assessment Architecture' (A5) is aimed at all stakeholders along the AI value chain, from providers and deployers to the entities responsible for development, operation and oversight. The aim is to provide structured guidance for the development, deployment and operation of fair, secure and compliant AI systems, thereby making a robust contribution to the trustworthiness of AI throughout its entire lifecycle.

# <span id="page-5-2"></span>1.2 Nature and Structure

This A5 Horizontal Trustworthiness Core Module forms the foundation of the A5 framework and is designed to apply horizontally across all dimensions of trustworthiness and technologies. In contrast to specialised, vertically oriented modules that explore individual areas of application or specific trustworthiness dimensions in depth, the Horizontal Trustworthiness Core Module creates a comprehensive and uniform framework that brings together the fundamental organisational and technical measures required for trustworthy AI. It is based on the BSI's state-of-the-art guidelines on artificial intelligence and draws on relevant, recognised standards and frameworks in their current versions (as of June 2026), ensuring that the criteria remain both regulatory-compliant and practically viable.

A key feature of the core module is the consistent integration of overarching processes, which serve as a common foundation for a wide range of downstream requirements. For example, the risk management process and the quality management process are overarching parent processes whose fundamental procedural steps – such as the identification, analysis, assessment, mitigation and review of risks – apply equally to the requirements that depend on them. The individual criteria draw on these parent processes and specify them for particular dimensions of trustworthiness, without having to fully reformulate the underlying procedural logic in each case. This creates a consistent and reusable framework that avoids redundancies and enhances the traceability of the relationships between the requirements.

The A5 criteria are organised according to a grouping structure and covers the areas of governance, compliance and scope; design, development and integration; verification and validation; deployment, operation and monitoring; and retirement. Each criterion specifies the responsible party and any dependencies on other criteria and contains supplementary notes that are differentiated according to the roles of provider and deployer. These notes are intended as guidance for implementation and describe possible measures without prescribing them definitively.

# <span id="page-5-3"></span>1.3 Dimensions of Trustworthiness

The core module addresses the dimensions relevant to trustworthy AI horizontally and integrates them into the overarching processes and measures. The following descriptions explain which aspects each dimension encompasses and form the conceptual background on which the criteria are based.

{6}------------------------------------------------

Across the board, aspects of **AI governance** are addressed, which create a regulated organisational framework for the development, deployment and operation of AI and bring together those requirements that are not directly assigned to a single dimension of trustworthiness.

**Data Quality and Data Governance** refer to ensuring data quality, data governance processes and further guidelines for handling data in the context of AI. This includes, in particular, respect for privacy, the quality and integrity of data, and regulated data access throughout the entire data lifecycle.

**Transparency and Explainability** refers to the transparency of machine-based decision-making, transparency towards users, and the traceability of methods and decisions from the system's design through to its operation. This encompasses traceability, the explainability of model decisions and model behaviour, as well as communication with end users and other stakeholders.

**Human agency and oversight** refer to human action and to oversight concepts such as 'human-in-theloop', 'human-on-the-loop' or 'human-in-command'. The focus is on preserving human decision-making and ensuring human oversight of the AI system.

**Robustness** refers to the resilience and reliability of AI systems in the face of errors, disruptions and unexpected inputs. This includes technical robustness – for example, against adversarial attacks, data drift and edge cases – the stability of accuracy in the face of disturbances, the reliability and reproducibility of results, fallback plans, and general safety in the sense of security, as well as fault tolerance and resilience. Closely related to this is the protection of the AI system against unauthorised access, manipulation and attacks, including cybersecurity aspects such as model poisoning, model evasion, model stealing and membership inference; ensuring confidentiality, integrity and availability; system and authorisation management; and secure development and operational processes.

**Performance** refers to the AI system's capability in relation to defined target metrics. These include accuracy, precision, recall, F1 score or other domain-specific metrics, efficiency in terms of latency, throughput and resource consumption, and the fulfilment of functional performance requirements within the defined operational context.

**Record-keeping and logging** refer to the (automatic) recording of events and their retention, thereby creating a robust basis for traceability, fault analysis, security monitoring and regulatory compliance.

**Monitoring** refers to the supervision of the AI system after it has been placed on the market or during operation. This includes the detection of model drift, data drift and concept drift; performance monitoring against defined key performance indicators and thresholds; and the detection of incidents and response to anomalies.

**Bias** refers to the avoidance of unjustified bias and discrimination, as well as to inclusion and diversity as objectives.

**Accountability** refers to responsibility and accountability for AI systems and their outcomes. This includes auditability, the minimisation and reporting of negative impacts, the documentation of trade-offs and compromises, as well as legal protection and remedies.

{7}------------------------------------------------

# <span id="page-7-0"></span>2 Governance, Compliance and Scope (GCS)

The following lists measures designed to establish a regulated framework for the governance of AI within the organisation by clarifying business objectives and the context of use, defining responsibilities, roles and guidelines, and embedding overarching requirements regarding risk, quality, security and human oversight throughout the entire AI lifecycle.

# <span id="page-7-1"></span>2.1 GCS.1 Stakeholder & Impact Scoping

## <span id="page-7-2"></span>2.1.1 GCS.1.1 Establish a risk management process

**Criterion:** The responsible party should establish a risk management process comprising the identification, analysis and assessment of risks according to severity, probability of occurrence, priority and uncertainty; mitigation through organisational measures; the management of residual risks; verification of the effectiveness of mitigation measures; the assessment of AI risks**;** and the documentation and disclosure of residual risks to relevant stakeholders in a manner appropriate to the audience**.**

**Dependency:** None

# **Guidance**

**Provider**: The aim is to ensure robust risk management throughout the entire lifecycle. Risk owners may carry out reviews at least annually and as and when necessary. In addition, it is advisable to document further assessment requirements and integrate them into the risk assessment; changes such as new features, model adjustments or retraining may be included.

**Deployer:** The aim is to ensure that risks are continuously addressed in the operational context. To this end, risk owners may carry out regular and ad hoc reviews; changes in the usage context, such as an extension of the intended purpose or changes to user groups, may be taken into account. In addition, provider information on system boundaries, performance and retraining can be utilised, and additional regulatory or contractual assessment requirements can be documented and integrated. Traceable evidence of the assessments, including decisions and measures, is recommended.

{8}------------------------------------------------

# <span id="page-8-0"></span>2.1.2 GCS.1.2 Risk management process for traceability risks

**Criterion:** The responsible party should establish a risk management process for risks arising from a lack of traceability in the AI system**.**

**Dependency:** [GCS.1.1](#page-7-2)

# **Guidance**

**Provider:** The aim is to ensure that risks arising from a lack of traceability are thoroughly understood and prioritised so that effectiveness, product quality and accountability can be safeguarded. To this end, risks and their causes can be identified and risk responsibilities assigned; relevant sources of risk may include, for example, a lack of user trust, unclear accountability, the concealment of biases or security vulnerabilities, non-compliance with regulatory requirements, and interoperability issues. The intended use may be taken into account during the assessment. In addition, results and assumptions can be documented in a transparent manner.

**Deployer:** The aim is to ensure that the documentation provided by the supplier is checked for completeness and applicability, and that an independent risk analysis regarding the traceability of operational processes can be carried out. This may include identifying gaps in the supplier's documentation and assessing risks arising from insufficient logging of the deployer's own activities. Relevant sources of risk may include, for example, difficulties in providing evidence during audits, the inability to reconstruct system decisions for data subjects, inefficient fault rectification, or a lack of traceability regarding configuration changes. In addition, the results can be incorporated into the establishment of the organisation's own, context-specific documentation and logging requirements for operations.

{9}------------------------------------------------

# <span id="page-9-0"></span>2.1.3 GCS.1.3 Risk management process for explainability risks

**Criterion:** The responsible party should establish a risk management process for risks arising from a lack of explainability in the AI system**.**

**Dependency:** [GC S .1.1](#page-7-2)

# **Guidance**

**Provider:** The aim is to ensure that risks arising from a lack of explainability are specifically understood, assessed and made manageable, so that development, quality assurance and subsequent use can take place on a robust risk basis. To this end, relevant risks and their causes can be identified and risk responsibilities assigned; the specific intended use can be taken into account. Sources of risk may include, for example, a lack of trust on the part of users, a lack of understanding of the outputs, or erroneous decisions due to insufficient understanding. In addition, results and assumptions can be documented in a transparent manner.

**Deployer:** The aim is to ensure that risks arising from a lack of explainability in the specific operational context can be assessed and managed in order to avoid incorrect decisions and a loss of trust. This may involve adopting and context-specific supplementation of the provider's risk analysis; deployment-specific risks can be identified, e.g. insufficient understanding of the outputs among one's own user groups, erroneous decisions due to misinterpreted results, or a lack of trust among affected individuals. In addition, the results can be documented in a transparent manner and incorporated into the organisation's risk management framework.

{10}------------------------------------------------

# <span id="page-10-0"></span>2.1.4 GCS.1.4 Risk management process for human agency and oversight risks

**Criterion:** The responsible party should establish a risk management process for risks relating to human agency and oversight**.**

**Dependency:** [GCS.1.1](#page-7-2)

# **Guidance**

**Provider:** The aim is to ensure that risks arising from a restriction of human agency and insufficient human oversight are systematically identified, assessed and documented, so that product quality, safety and responsible use can be safeguarded in a structured manner. To this end, risks and causes can be identified and risk responsibilities assigned; Risk sources can be aligned with the intended use, including, for example, automation bias and excessive reliance, a lack of traceability of decisions, unclear accountability and authorship for outputs, the simulation of human traits, increased susceptibility to errors without human detection, and incorrect or improper use by inadequately qualified staff. In addition, the results can be documented in a traceable manner and updated.

**Deployer:** The aim is to ensure that risks arising from the restriction of human agency and the lack of human oversight within the organisation's own operational context can be realistically assessed, managed and controlled in a targeted manner, and that responsibilities are clearly defined. To this end, the provider's risk analysis can be adopted as a starting point and evaluated and supplemented for the specific operational context; operation-specific risks can be identified, including, for example, automation bias and excessive reliance amongst the respective user groups, unclear accountability within one's own organisation, the simulation of human traits or unclear authorship, a lack of traceability for affected individuals, a failure to detect operational errors, and improper use by the relevant staff, including a lack of appropriate qualifications. In addition, findings can be documented, responsibilities assigned, and measures derived to strengthen human agency and human oversight.

{11}------------------------------------------------

# <span id="page-11-0"></span>2.1.5 GCS.1.5 Risk management process for performance risks

**Criterion:** The responsible party should establish a risk management process for risks arising from inadequate performance of the AI system**.**

**Dependency:** [GCS.1.1](#page-7-2)

# **Guidance**

**Provider:** The aim is to ensure that risks of inadequate performance regarding the intended use are systematically understood and made addressable. To this end, sources of risk can be considered, e.g. faulty model training, incorrect model selection and unsuitable optimisation and validation strategies; poor selection of metrics and tests can also be included. Limitations in training can be addressed, e.g. insufficient data quality or quantity, insufficient validation or test data, and overfitting. Furthermore, limitations imposed by hardware during training and inference, as well as risks arising from changes to the system's composition – particularly through retraining or online learning – can be assessed. In addition, results can be documented in a transparent manner.

**Deployer:** The aim is to ensure that risks of inadequate performance in the specific operational context can be realistically assessed and targeted protective measures derived. This may involve adopting and contextually supplementing the provider's analysis; deployment-specific risks can be identified, e.g. deviating data distributions in production, hardware limitations of the organisation's own infrastructure, changed usage patterns or risks arising from online learning in the operational environment. Deviations from the provider's assumptions can be documented. In addition, results can be incorporated into the organisation's risk and quality management systems.

{12}------------------------------------------------

# <span id="page-12-0"></span>2.1.6 GCS.1.6 Risk management process for robustness risks

**Criterion:** The responsible party should establish a risk management process for risks arising from insufficient robustness of the AI system**.**

**Dependency:** [GCS.1.1](#page-7-2)

# **Guidance**

**Provider:** The aim is to ensure that risks arising from malfunctions or failures are understood and prioritised at an early stage so that targeted protective and quality measures can be derived. To this end, risk sources can be taken into account, e.g. insufficient robustness, the criticality of the intended use and scope of application, functional reasons for (partial) failures, misuse outside the intended use, and input/output interfaces. The potential consequences for fundamental rights, as well as for property and assets, can be outlined. In addition, results can be documented in a transparent manner and updated.

**Deployer:** The aim is to ensure that risks arising from malfunctions or failures in the specific operational environment can be assessed, supplemented and effectively incorporated into operations and precautionary measures. This may include reviewing the supplier analysis for contextual fit; deploymentspecific risks can be identified, e.g. criticality within the specific area of application, potential harm to fundamental rights, property and assets, the likelihood of incorrect or misuse by the relevant personnel, and risks arising from connected system components. In addition, deviations from the supplier's assumptions can be documented and the results incorporated into risk and emergency management.

{13}------------------------------------------------

### <span id="page-13-0"></span>2.1.7 GCS.1.7 Risk management process for bias risks

**Criterion:** The responsible party should establish a risk management process for bias risks in connection with the intended purpose of the AI system**.**

**Dependency:** [GCS.1.1](#page-7-2)

### **Guidance**

**Provider:** The aim is to ensure that bias risks are systematically identified, assessed and prioritised, so that effective mitigation measures can be planned at an early stage and downstream stakeholders can be provided with well-founded information. To this end, significant sources of risk can be taken into account in light of the intended use, e.g. historical biases, sampling and model biases, attribution errors or implicit bias; this also includes user interactions, confirmation bias, misinterpretations of results, insufficient consideration of relevant user groups and discrimination against protected groups. Risks can be systematically categorised, prioritised and assigned to specific parties responsible for managing them. In addition, results can be documented in a transparent manner and made available to downstream stakeholders. Further information on bias in the context of the catalogue can be found in publications by the BSI, such as 'Bias in Artificial Intelligence'.

**Deployer:** The aim is to ensure that bias risks can be reliably addressed in the specific operational context and documented as part of a fundamental rights impact assessment (FRIA). This may involve supplementing the risk analysis documented by the provider with context-specific information; operationspecific protected groups and additional bias risks can be identified. Context-specific sources can be taken into account, e.g. changes in user groups, cultural or regional characteristics, and application-specific impacts on affected individuals. Unauthorised extensions of the intended use can be avoided and, where necessary, coordination with the provider can be arranged. In addition, the results can be documented in a traceable manner, incorporated into the organisation's risk management framework and – where applicable – made available as part of the FRIA. Further information on bias in the context of the catalogue can be found in BSI publications, such as 'Bias in Artificial Intelligence'.

{14}------------------------------------------------

# <span id="page-14-0"></span>2.2 GCS.2 Defining Governance, Roles & Policies

### <span id="page-14-1"></span>2.2.1 GCS.2.1 Document risk management guidelines

**Criterion:** The responsible party should document the policy and instructions for risk management procedures, comprising the scope and business context, roles and responsibilities (including risk ownership), risk categories and scenarios, the assessment methodology (including a risk matrix), detection measures and their success rates, criteria for the acceptance of residual risks, and guidelines on communication and the regular review of the policy**.**

#### **Dependency:** None

### **Guidance**

**Provider:** The aim is to establish a consistent normative basis for risk decisions and to empower downstream stakeholders. To this end, the scope can be defined, including a risk-based classification in relation to business and operational context, as well as criteria for assigning a qualified risk owner; the policy may specify risk scenarios, including threats and causes, as a methodological framework. Assessment methods for probability of occurrence and impact, including a risk matrix, as well as guidelines on detection measures with success rates, are appropriate. In addition, criteria for the authorisation and acceptance of residual risks, conclusions regarding mitigation mechanisms and their impact on risk levels, and guidelines on communication can be addressed; a review of the policy at least once a year is recommended.

**Deployer:** The aim is for an organisation-specific policy to provide a binding framework for operational risk management in the operational context. To this end, the risk information provided by the supplier can be used as a basis and supplemented with operation-specific scopes, scenarios and threats; criteria for appointing a qualified risk owner can be established. Assessment methods and the risk matrix can be adapted to the operational context, and guidelines for detection measures and acceptance criteria for residual risks can be defined. In addition, communication channels, reporting obligations to management and a regular review of the policy in the event of changed operational conditions can be provided for.

{15}------------------------------------------------

# <span id="page-15-0"></span>2.2.2 GCS.2.2 Document development guidelines

**Criterion:** The responsible party should document the policy and instructions for the AI system's development process, comprising at least requirements for training material (data sets, guidelines required for training), system robustness, design, development, deployment, verification (e.g. application tests, code reviews), validation, relevant subsystems, and testing and approval procedures by management**.**

**Dependency:** None

# **Guidance**

**Provider:** The aim is to ensure that the specifications for the development of the system are recorded transparently so that they are, on the one hand, traceable retrospectively and, on the other hand, can be used consistently in future as a basis for further developments. To this end, the scope of documentation may include requirements for training materials, e.g. data sets and guidelines, aspects of system robustness, and phases such as design, development and delivery. This also includes instructions on testing activities such as verification (e.g. application tests and code reviews) and validation, as well as the consideration of relevant subsystems. In addition, review and approval procedures may be defined by management, for example as a sign-off prior to major development milestones or prior to delivery. Clear responsibilities, version control and change tracking support the purpose of the documentation.

{16}------------------------------------------------

### <span id="page-16-0"></span>2.2.3 GCS.2.3 Document the AI policy

C**riterion:** The responsible party should establish a process for an AI policy for internal use in accordance with regulatory requirements, comprising a documented strategy for the development and deployment of AI, including AI objectives and guidelines for achieving them; a structural and procedural organisation for the development and operation of AI systems; a concept for roles and permissions; guidelines on the permissible use of AI technologies within the organisation for all staff, and a review cycle for regularly assessing the policy's currency, appropriateness and effectiveness**.**

#### **Dependency:** None

#### **Guidance**

**Provider:** The aim is to establish a binding internal framework for the development, deployment and use of AI and to ensure that it remains effective. To this end, clear objectives, including the scope, organisational structure and processes, as well as roles and responsibilities, can be documented. A roles and permissions framework can define responsibilities for development and deployment; Guidelines on the permissible use of AI technologies can be drawn up for all staff. Review criteria can cover suitability, appropriateness and effectiveness; triggers include, for example, new technologies, regulatory changes or incidents. In addition, changes can be documented with version control, communicated and integrated into related management systems, e.g. for quality and information security.

**Deployer:** The aim is to ensure that the use of AI within their own context is managed in a controlled and compliant manner. To this end, an AI policy can be adapted to the operational context and aligned with internal requirements, e.g. information security. A roles and permissions framework can define responsibilities for operation, monitoring and use; Guidelines on permissible use can be drawn up for all staff and integrated into operational procedures such as training, incident handling and change management. Periodic reviews can take into account practical experience, new risks and changes to requirements. In addition, deviations can be documented and mitigation measures defined; communication to the relevant roles is recommended.

{17}------------------------------------------------

# <span id="page-17-0"></span>2.2.4 GCS.2.4 Document AI provisions in General Terms and Conditions/EULAs

**Criterion:** The responsible party should document AI-specific provisions regarding user rights, obligations and liability in the general terms and conditions and end-user licence agreements**.**

#### **Dependency:** None

# **Guidance**

**Provider:** The purpose of this requirement is to ensure legal certainty and to clearly address expectations between the provider and users regarding AI functions. To this end, it is advisable to ensure consistent coverage of user inputs (e.g. prompts), rights and ownership of outputs, liability, compliance requirements and limitations on the use of outputs. The protection of sensitive data must be emphasised; this also includes transparency regarding data processing and storage. In addition, linguistic clarity is desirable; internal quality assurance and checks against regulatory requirements are recommended.

{18}------------------------------------------------

# <span id="page-18-0"></span>2.3 GCS.3 Define metrics and measurement framework

## <span id="page-18-1"></span>2.3.1 GCS.3.1 Establish a quality management process

**Criterion:** The responsible party should establish a quality management process comprising the assessment of requirements within the relevant quality dimension, the definition of requirements, the definition of metrics including thresholds, and tests to assess compliance with requirements; the establishment of a test plan under conditions representative of the scope of application; the execution of the tests; the documentation of results, including deviations and KPIs; the implementation of appropriate corrective measures; and the verification of the effectiveness of the measures taken**.**

#### **Dependencies:** None

## **Guidance**

**Provider:** The aim is to establish a systematic quality management process across all relevant quality dimensions in order to provide verifiable evidence of the AI system's quality and to be able to address any changes reliably. This may include assessing the need within the respective quality dimension; requirements can be defined on a risk-based basis and supported by suitable metrics and tests. A test plan under conditions representative of the scope of application can be established and carried out; results, including deviations and KPIs, can be documented. In addition, the effectiveness of measures taken can be reviewed and adjusted where necessary; the documentation can ensure traceability for downstream stakeholders.

**Deployer:** The aim is to systematically monitor and maintain the quality of the AI system within its operational context. To this end, the requirements, metrics and tests documented by the provider can be applied to the specific operational context and supplemented where necessary; an operational test plan can be established under representative operational conditions and carried out regularly. Results, including deviations and KPIs, can be documented and evaluated. In addition, the effectiveness of operational measures can be reviewed, adjustments made in the event of changes in context, and relevant findings reported back to the provider.

{19}------------------------------------------------

# <span id="page-19-0"></span>2.3.2 GCS.3.2 Quality management process for transparency

**Criterion:** The responsible party should establish a quality management process for transparency**.**

**Dependency:** [GCS.3.1](#page-18-1)

# **Guidance**

**Provider:** The aim is to define the required level of transparency in a well-founded manner and to document it in a traceable way, so that users and affected individuals are adequately informed about the use, capabilities and limitations of the AI system. To this end, it can be specified which information is to be disclosed – e.g. the fact that it is an AI system, its intended use, the system's capabilities and limitations, and how outputs are handled. Legal transparency and labelling obligations can be categorised and the results of the risk analysis incorporated; target groups and the appropriate level of information for each can be determined. In addition, the form, timing and channel of the transparency information, as well as the involvement of subject-matter experts and the documentation of the specifications, can be described.

**Deployer:** The aim is to ensure that the transparency information provided by the supplier is effectively communicated to users and affected individuals within the operational context. To this end, labelling and information requirements can be implemented in specific use cases and incorporated into user guidance, training and communication channels; application-specific transparency requirements can be added. In addition, it is advisable to map this to the organisation's own regulatory obligations; the provision of the information can be documented in a traceable manner.

{20}------------------------------------------------

### <span id="page-20-0"></span>2.3.3 GCS.3.3 Quality management process for robustness

**Criterion:** The responsible party should establish a quality management process for robustness**.**

**Dependency:** [GCS.3.1](#page-18-1)

### **Guidance**

**Provider:** The aim is to ensure that the robustness of the AI system can be demonstrated in a well-founded and application-specific manner, so that performance limits, uncertainties and malfunctions can be identified and addressed at an early stage. This may involve selecting different metrics and test categories tailored to the area of application and intended use; statistical analyses of robustness, including the identification of edge cases, as well as experiments under extreme conditions, may be carried out. Methods for determining uncertainty, including calibration metrics, may be employed depending on the model type or supported by probabilistic architectures; mechanisms for detecting erroneous inputs may be provided. Methods can be defined per model and, in the case of aggregated output, additionally at system level. In addition, threshold values can be set according to deployment scenario and documented with justification based on purpose, model type and system configuration.

**Deployer:** The aim is to continuously monitor and maintain the robustness of the AI system within its operational context. To this end, the robustness metrics and thresholds defined by the provider can be applied and monitored in operation; edge cases and extreme conditions in specific operational scenarios can be identified and incorporated into operational tests. Mechanisms for detecting faulty inputs can be activated and monitored; deviations from defined tolerance intervals can be documented and escalated. In addition, findings regarding reductions in robustness, new edge cases or changed operational conditions can be regularly evaluated and reported back to the provider; operational thresholds can be adjusted in consultation with the provider.

{21}------------------------------------------------

# <span id="page-21-0"></span>2.3.4 GCS.3.4 Quality management process for performance

**Criterion:** The responsible party should establish a quality management process for performance**.**

**Dependency:** [GCS.3.1](#page-18-1)

# **Guidance**

**Provider:** The aim is to establish a robust, context-specific test plan for performance, so that system quality can be verifiably demonstrated and reliably addressed in the event of changes. This may include the specification of test objects; defined test methods can cover the intended metrics, supplemented where necessary by advanced procedures, and their characteristics documented. Test data and parameters can be described, and a production-like test environment and test frequencies can be defined; this also includes plans for the operational phase. Resource requirements and responsibilities can be specified. The plan can be tailored to the application context, and the coverage of relevant scenarios can be justified.

**Deployer:** The aim is to ensure that the test plan is effectively implemented during operation so that performance is maintained under realistic conditions. This may include the planning and execution of regular tests, with a particular focus following system adjustments or changes to operational data. Production-like test environments may be utilised; defined metrics and methods may be applied operationally and results documented. Sufficient resources and a responsible person can be designated. In addition, test data sources and parameters can be described and kept up to date; coverage of relevant operational scenarios can be continuously reviewed and the test plan updated in the event of changes to the context.

{22}------------------------------------------------

### <span id="page-22-0"></span>2.3.5 GCS.3.5 Quality management process for bias

**Criterion:** The responsible party should establish a quality management process to prevent unjustified bias**.**

**Dependency:** [GCS.3.1](#page-18-1)

### **Guidance**

**Provider:** The aim is to define risk-based metrics for bias that are tailored to the intended purpose and to justify them in a transparent manner. To this end, the selection process may draw on the risk assessment and determine the appropriate definition of bias; combinations are often appropriate. Tolerance intervals can be calibrated and justified on a risk-oriented basis. In addition, the selection, intervals and reasons can be documented; consistency is desirable, and assumptions and conflicting objectives can be explained transparently. Further information on bias in the context of the catalogue can be found in BSI publications, such as 'Bias in Artificial Intelligence'.

**Deployer:** The aim is to ensure that the bias metrics specified by the provider are applied in the operational context and assessed for appropriateness. To this end, the defined metrics and tolerance intervals can be monitored operationally and results checked against the documented thresholds; contextspecific bias risks can also be identified and assessed. In addition, deviations can be documented and, in the event of systematic anomalies, countermeasures can be initiated or the matter escalated to the provider; feedback on the appropriateness of the selected bias definitions in the specific operational context can be provided. Further information on bias in the context of the catalogue can be found in BSI publications, such as 'Bias in Artificial Intelligence'.

{23}------------------------------------------------

# <span id="page-23-0"></span>2.3.6 GCS.3.6 Quality management process for explainability

**Criterion:** The responsible party should establish a quality management process for explainability**.**

**Dependency:** [GCS.3.1](#page-18-1)

# **Guidance**

**Provider:** The aim is to assess and document the system's need for explainability so that various stakeholders can understand the model's decisions and behaviour on the basis of the explanations provided. To this end, the assessment may take into account the system's purpose and the stakeholders affected; consider potential harm, user needs for human decisions and the handling of outliers; classify legal and regulatory obligations; make the trade-off between explainability and performance transparent and recognise justified user interests. In addition, criteria, target levels, choice of methods (e.g. postdecision explanations (global/local)), limitations, and the reporting and communication approach may be documented.

**Deployer:** The aim is to ensure that the level of explainability required in the operational context is appropriately determined and made available to those affected in a usable form. To this end, the provider's assessment can be adopted and refined for the specific use case; users' information needs and the prerequisites for human decision-making can be addressed. Procedures for handling outliers, as well as reporting and disclosure obligations towards interested parties and supervisory authorities, can be incorporated. In addition, the decision and degree of explainability, the user information provided, as well as the underlying assumptions and limitations of the explanation methods can be documented.

{24}------------------------------------------------

# <span id="page-24-0"></span>2.4 GCS.4 Privacy Governance & Data Protection

# <span id="page-24-1"></span>2.4.1 GCS.4.1 Establish a process for exercising data subjects' and users' rights

**Criterion:** The responsible party should establish a process for ensuring the rights of data subjects and users regarding personal data in the operation of the AI system (including rights relating to data management, erasure and use, and information obligations), in compliance with legal requirements**.**

#### **Dependency:** None

# **Guidance**

**Provider:** The purpose of this requirement is to ensure that the provider enables the exercise of data subjects' and users' rights in a technically feasible and user-centred manner, so that transparency, traceability and legally compliant processes are guaranteed from the outset. This may include providing clear, comprehensible explanations regarding data processing, rights and responsibilities within the user interface; logging of processing activities and the exercise of rights may be provided for. Functions and interfaces for access, rectification, erasure, data portability, objection and withdrawal may be implemented; mechanisms for automatic erasure following retention periods and upon request may be integrated. In addition, system support may be provided for obtaining and managing explicit consents, as well as for providing timely information about changes.

**Deployer:** The purpose of this requirement is to ensure that the deployer makes operational use of the mechanisms provided by the provider and acts in a legally compliant manner towards data subjects. To this end, clear responsibilities and processes may be defined for the receipt, identity verification and timely processing of data subject requests; the interfaces provided by the provider for access, erasure, rectification and objection must be used and monitored in day-to-day operations. In addition, regular checks may be carried out to verify that data has actually been deleted and that retention periods are being adhered to. Furthermore, it is advisable to document and log the requests processed, including response times, in order to demonstrate the effectiveness of the processes.

{25}------------------------------------------------

# <span id="page-25-0"></span>2.5 GCS.5 Security Governance: Protection Objectives & Threat Modelling, Red Teaming

### <span id="page-25-1"></span>2.5.1 GCS.5.1 Establish measures and security controls for access to AI data

**Criterion:** The responsible party should establish measures and security controls for access to relevant datasets throughout the entire AI lifecycle**.**

#### **Dependency:** None

#### **Guidance**

**Provider**: The aim is for the provider to secure access to AI data throughout the entire lifecycle in a riskbased manner, so that sensitive, personal and proprietary information is protected and downstream stakeholders can rely on clearly defined controls. This may include the definition of individual, purposespecific access rights; the principles of least privilege and need-to-know must be applied, and tasks must be segregated. This also encompasses regular recertification and the revocation of rights in the event of changes in role or employment; unauthorised access must be prevented through technical and organisational measures. A technical access management system may be operated and described in the data documentation. In addition, data transfers between parties or to the cloud must be secured using encryption and communication security measures and must be documented; in the case of personal data, for example, data subject access must be taken into account.

{26}------------------------------------------------

# <span id="page-26-0"></span>2.5.2 GCS.5.2 Establish tiered security controls

**Criterion:** The responsible party should establish mechanisms for implementing tiered security measures for the AI system based on the risk, sensitivity and criticality of the system and data**.**

#### **Dependency:** None

# **Guidance**

**Provider:** The aim is to ensure that security measures can be applied effectively in a multi-layered and tiered manner, commensurate with the level of exposure. To this end, mechanisms can be designed so that controls are applied in tiers based on the risk, sensitivity or criticality of the system and data; these include, in particular, network and access controls such as secure gateways, VPNs and controlled routing for AI/ML systems. Criteria catalogues and assignment rules, e.g. data classification and system criticality, can support the establishment of these levels; policy- and template-based configurations are appropriate, and automation via access management using a role- or attribute-based rights concept can assist. In addition, the characteristics of each level, the layers of protection and the trigger conditions can be documented in a traceable manner and versioned.

**Deployer:** The aim is to ensure that the appropriate security level and protection layer are active at all times during operation. To this end, predefined levels and network controls such as gateways, VPNs and routing can be adopted and selected on the basis of the organisation's own risk, sensitivity and criticality assessments; configurations for each level can be applied consistently and changes documented in a traceable manner. Monitoring compliance with the selected level is recommended; deviations can be analysed and corrected. In addition, the assignment of systems and data to the levels can be reviewed regularly and adjusted as necessary.

{27}------------------------------------------------

# <span id="page-27-0"></span>2.5.3 GCS.5.3 Establish architecture and design decisions based on 'Security-by-Design'

**Criterion:** The responsible party should establish security-conscious architecture and design decisions for the AI system in accordance with Security-by-Design, including data and AI components**.**

**Dependency:** None

# **Guidance**

**Provider:** The purpose of this requirement is to strengthen confidentiality, integrity and availability through robust architectural decisions and to ensure that identified threats can be addressed. To this end, the selection of model family and architecture may take into account security features such as robustness, attack surface and interpretability; security-related conflicting objectives can be documented in a transparent manner. In addition, AI-specific security controls (e.g. input validation, output sanitisation, protection boundaries, access restrictions) are advisable; security and trust boundaries between AI and conventional components can be defined. Furthermore, metrics and thresholds can be analysed for vulnerabilities and justified against the threat analysis.

{28}------------------------------------------------

# <span id="page-28-0"></span>2.5.4 GCS.5.4 Risk management process for AI-specific vulnerability management

**Criterion:** The responsible party should establish a risk management process for AI-specific vulnerability management, including corresponding security objectives, a scope covering AI-specific assets worthy of protection (models, data, pipelines, interfaces), as well as associated security requirements and response times according to severity level**.**

**Dependency:** [GCS.1.1](#page-7-2)

# **Guidance**

**Provider:** The aim is to ensure that vulnerabilities in AI-enabled applications – including both traditional software vulnerabilities and AI-specific vulnerabilities in models, training and input data, prompts, libraries and the ML supply chain – are systematically identified, prioritised, remedied and verified throughout the entire lifecycle, so that risks are mitigated in a timely and traceable manner. This may involve a governance framework with clear roles, escalation paths and cross-functional coordination; consistent documentation standards can enhance traceability and auditability. Risk-based prioritisation (e.g. according to CVSS, exploitability) and response times based on severity are appropriate; alignment with relevant standards can support consistency. Automation in CI/CD can accelerate scans, tracking and, where appropriate, remediation. In addition, quality assurance measures such as retests and root-cause analyses can be carried out; findings from monitoring and attack-based assessments can serve as input, and remediation can be implemented via change management.

**Deployer:** The aim is to ensure that disclosed vulnerabilities are systematically identified, prioritised, rectified and verified within the operational context, so that risks are reduced in a timely and traceable manner. This may involve a process that receives security advisories from the vendor, assesses the impact on the organisation's own usage, and coordinates measures such as updates, configuration changes or temporary usage restrictions. Clear roles, escalation paths and response times based on severity are advisable; risk-based prioritisation, e.g. according to exploitability and affected business processes, can support this management. In addition, it is advisable to report one's own observations to the provider – for example, suspicious output or anomalies in integrations – and to establish vulnerability management processes for one's own adjacent components; the implementation of corrective measures can be managed via change management.

{29}------------------------------------------------

# <span id="page-29-0"></span>2.6 GCS.6 Human Oversight (HO), Human in the Loop (HITL) & Competence

### <span id="page-29-1"></span>2.6.1 GCS.6.1 Establish a process to protect human integrity

**Criterion:** The responsible party should establish a process for the protection of human integrity to safeguard human autonomy and prevent emotional dependence and covert or exploitative manipulation of users' beliefs, emotions or behaviour by the AI product, and to minimise harmful influence, taking into account the structure and design of the AI product**.**

#### **Dependency:** None

# **Guidance**

**Provider:** The aim is to ensure that the AI product does not exert any covert or exploitative influence and that users' human autonomy is protected. To this end, measures may include the analysis of system characteristics and interaction patterns, e.g. manipulative design patterns, persuasive or subliminal techniques, cognitive biases and emotionally charged language. Functions for content generation, personalisation and recommendation can be assessed for their potential to exert influence, and reactions to users experiencing emotional distress can be taken into account. In addition, protective measures are recommended, including checks for emotionally exploitative patterns; residual risks can be assessed and documented. Furthermore, monitoring can identify emerging patterns and dependency dynamics; corrective actions can be justified and tracked.

**Deployer:** The aim is to ensure that, within the operational context, risks of manipulation are reduced and identified patterns can be effectively addressed. To this end, protective mechanisms can be activated, configured and regularly tested during operation; conspicuous outputs, emotionally exploitative language or anomalous interactions can be monitored and escalated. Corrective measures (e.g. adjustment of prompts, filters, personalisation limits) can be implemented promptly and documented in a traceable manner; particular attention can be paid to interactions with users in stressful situations. In addition, feedback and reporting channels are appropriate. Furthermore, findings from monitoring and user feedback can be incorporated into operational decisions and feedback to the provider.

{30}------------------------------------------------

# <span id="page-30-0"></span>2.6.2 GCS.6.2 Establish mechanisms for challenging and correcting decisions

**Criterion:** The responsible party should establish mechanisms for users or affected individuals to reject, challenge, correct or suspend decisions and outputs of the AI system**.**

**Dependency:** None

# **Guidance**

**Provider:** The aim is to ensure that effective intervention and challenge mechanisms are provided on a technically sound basis, so that incorrect decisions can be limited, damage avoided and human oversight reliably enabled. This may include a risk-based design and implementation tailored to the purpose and target audience; an objection workflow with a submission option, e.g. via a form, and a processing status can be provided. Technical forwarding to a qualified and authorised natural person for the review of decisions and outputs can be implemented. An emergency stop function can put the system into a safe state. In addition, an interactive graphical user interface can support the triggering and tracking of the aforementioned actions.

**Deployer:** The aim is to provide data subjects and users with effective rights of intervention in the specific operational context and to enable prompt intervention where necessary. To this end, mechanisms can be configured and made accessible in a manner appropriate to the operational risk; an objection form can be provided, and incoming objections can be processed. Human reviews by qualified, authorised personnel can be ensured at an organisational level. The emergency stop function can be activated, and responsibilities and procedures can be defined and practised regularly. In addition, interactive user interfaces can be made available and their use monitored to ensure effectiveness and accessibility.

{31}------------------------------------------------

# <span id="page-31-0"></span>2.6.3 GCS.6.3 Quality management process for human agency and oversight

**Criterion:** The responsible party should establish a quality management process for Human Agency & Oversight**.**

**Dependency:** [GCS.3.1](#page-18-1)

# **Guidance**

**Provider:** The aim is to define and make transparent an appropriate level of human agency and human oversight. To this end, experts can carry out the assessment on the basis of the risk assessment and identified standards and legal requirements; the task, context of use and risks, including legal risks, can be analysed. Requirements for effective human oversight and for safeguarding human agency can be derived, e.g. qualifications, timeframes and the information available. Technical provisions for human control and the ability to intervene can be embedded in the system architecture, e.g. options to interrupt processes, confirmation steps and information displays to support decision-making. In addition, results—including the justified degree of autonomy, control points and escalation procedures—can be documented; assumptions and limitations should be recorded as appropriate.

**Deployer:** The aim is to ensure that human oversight and human agency are effectively implemented and maintained in the operational context. To this end, the control mechanisms provided by the supplier can be activated, configured and integrated into operational processes; control points can be adapted to the specific context of use and the risk situation. Qualified staff can be appointed and trained to carry out monitoring tasks; sufficient time allocations, access to information and decision-making authority are recommended. In addition, the effectiveness and appropriateness of human oversight can be regularly reviewed, e.g. through spot checks, analysis of intervention frequencies and feedback from the monitoring personnel; any need for adjustments can be documented and reported back to the provider.

{32}------------------------------------------------

# <span id="page-32-0"></span>2.6.4 GCS.6.4 Establish a competence and training process

**Criterion:** The responsible party should establish a competence and training process for all individuals involved in the AI lifecycle and AI stakeholders along the supply chain, including required qualifications, role-based training programmes, practical exercises to strengthen cybersecurity competencies and risk awareness, as well as security awareness training**.**

**Dependency:** None

# **Guidance**

**Provider:** The aim is for development, quality assurance and integration to be carried out by technically competent individuals. To this end, role and competence profiles can be defined, qualification matrices maintained and competence gaps identified through assessments; building on this, training plans, induction and continuous professional development can be implemented, e.g. on AI security, risk management and robustness. Practical exercises to strengthen cybersecurity competencies and risk awareness, as well as security awareness training, can be incorporated. Evidence such as certificates, certificates of attendance and proof of practical experience can be documented in a version-controlled manner. In addition, individuals with supervisory responsibilities in the development process, as well as relevant stakeholders along the supply chain, can also be taken into account.

**Deployer:** The aim is to ensure that the deployment, operation and oversight of the AI system are carried out competently and in a responsible manner. To this end, roles and responsibilities can be defined and linked to qualification requirements; training can cover system boundaries, risks, biases, security requirements, monitoring, incident management and change management. Practical exercises to strengthen cyber security skills and security awareness training can be scheduled. For supervisory roles, decisionmaking frameworks, escalation procedures and options for intervention can be addressed. In addition, records of training and qualifications can be maintained, and regular refresher courses and recertification can be planned.

{33}------------------------------------------------

### <span id="page-33-0"></span>2.6.5 GCS.6.5 Establish a transparency and user protection process

C**riterion:** The responsible party should establish a transparency and user protection process to inform affected individuals and users about the application, limitations and outputs of the AI system, and to facilitate their interpretation and decision-making support through the labelling of AI interactions, user information, guidelines tailored to user groups, system settings that promote transparency, user guides and system prompts, as well as verifying the suitability of explanations and the communication of uncertainty**.**

#### **Dependency:** None

### **Guidance**

**Provider:** The aim is to ensure that information and instructions tailored to the target audience are embedded in such a way that users and affected individuals can use the AI system appropriately, interpret outputs correctly, and ensure that human oversight remains effective. This may include the structured provision of contact details, the purpose and scope of application, as well as expected performance and functionality; known risks and implications of use may be outlined. Expected input data and guidance on interpreting outputs may be described; the degree of autonomy and decision-making processes, as well as necessary measures for human oversight and user requirements (e.g. training), may be specified. The continuous maintenance and updating of the underlying model documentation (e.g. SBOM for AI – Minimum Elements), including periodic checks for completeness, accuracy and consistency with the current model status, forms the basis for these transparency measures; changes to data, models and controls can be tracked by version, and findings can be incorporated into updates and lessons learnt. In addition, maintenance measures, including software updates, can be versioned, maintained and delivered with the product; notes can be presented in a contextually understandable manner.

**Deployer:** The aim is to ensure transparency and the correct interpretation of system outputs during operation, and to effectively address automation bias. To this end, visible and accessible information can be made available to users and affected individuals; notifications stating that results and potential decisions are based on the AI system can be integrated. Information on outputs and decisions can be presented in such a way as to enable correct interpretation; warnings regarding automation bias and possible consequences can be included. Instructions provided by the supplier can be disseminated internally and training requirements can be implemented. In addition, maintenance and update notices can be actively communicated and taken into account in operational processes.

{34}------------------------------------------------

# <span id="page-34-0"></span>3 Design, Engineering and Integration (DEI)

The following section lists measures intended to establish a regulated framework for data acquisition, data preparation and model development by addressing the quality-assured, traceable and reproducible collection, documentation and processing of data, as well as the selection, training and secure integration of in-house and external models.

# <span id="page-34-1"></span>3.1 DEI.1 Data Acquisition (Acquire)

# <span id="page-34-2"></span>3.1.1 DEI.1.1 Establish a data management process

**Criterion:** The responsible party should establish a data management process comprising the definition of data requirements, data planning, procurement or collection, documentation of relevant data attributes, origin and versions, data preparation, controlled provision, storage and retention, logging of relevant data states to ensure reproducibility, as well as archiving, deletion and data decommissioning**.**

**Dependency:** None

# **Guidance**

**Provider:** The aim is to ensure that data is handled consistently, for specific purposes and securely throughout the entire AI lifecycle. To this end, a framework may specify standards for data structures and interfaces; purposes of use and retention periods may be defined, and security measures and access management described. In the case of reinforcement learning, state-action relations – including transition probabilities to other environmental states, agent policies and data dynamically generated by the environment – may also be covered. In addition, the origin, quality and distribution of these data types should be appropriately addressed.

**Deployer:** The aim is to ensure that operational and input data are handled consistently, for specific purposes and securely within the operational context. To this end, data requirements for operational activities can be defined and data sources regularly checked for suitability and quality; processing, provision and storage can follow documented standards. Retention periods and deletion policies can be established and implemented; access management and integrity checks are recommended. In addition, relevant data states can be logged for reproducibility, and anomalies or quality deviations can be reported back to the provider.

{35}------------------------------------------------

# <span id="page-35-0"></span>3.1.2 DEI.1.2 Data management process for training data

**Criterion:** The responsible party should establish a data management process for training data**.**

**Dependency:** [DEI.1.1](#page-34-2)

# **Guidance**

**Provider:** The aim is to ensure that training data is selected, prepared and documented in such a way that it adequately reflects the desired model behaviour and remains traceable and reproducible throughout its lifecycle. To this end, the suitability, quality, representativeness and coverage of the training data in relation to the scope of application can be assessed, and the quality of annotations/labels can be ensured. Data categories and retention periods can be defined, a logging system for training data states can be designed, and access to training and test data following deployment can be regulated both organisationally and technically. Reproducibility can be ensured through versioning of models, hyperparameters, random initialisations and pipeline configurations. In addition, procedures for secure deletion must be devised; the appropriateness of the measures can be justified and documented on a risk-based basis. Further guidance on this can be found in the BSI's QUAIDAL product series.

{36}------------------------------------------------

# <span id="page-36-0"></span>3.1.3 DEI.1.3 Data management process for validation data

**Criterion:** The responsible party should establish a data management process for validation data**.**

**Dependency:** [DEI.1.1](#page-34-2)

# **Guidance**

**Provider:** The aim is for the provider to make validation data available in such a way that it is representative, independent of the training data and reproducible, so that model selection and hyperparameter tuning can be carried out reliably. To this end, the distinction between validation data and training and test data can be clearly defined and ensured through data splitting strategies (e.g. hold-out, kfold cross-validation); overlap with training data (data leakage) can be specifically avoided. Representativeness with regard to the application domain can be checked and documented; transformation steps can be applied consistently with the training data but logged separately. The handling of missing values and class imbalance can be justified, and its impact on validation quality assessed. Further guidance on this can be found in the BSI's QUAIDAL product series.

{37}------------------------------------------------

# <span id="page-37-0"></span>3.1.4 DEI.1.4 Data management process for test data

**Criterion:** The responsible party should establish a data management process for test data**.**

**Dependency:** [DEI.1.1](#page-34-2)

# **Guidance**

**Provider:** The aim is to ensure that test data is provided and documented in such a way as to enable an independent, robust and traceable assessment of the model's compliance with requirements. To this end, the independence of the test data from training and validation data can be ensured in order to avoid data leakage and over-optimistic results; its representativeness with regard to the intended scope of application can be verified and documented. The documentation may establish links to data planning and data quality principles, and set out ownership, responsibilities, licences and rights of use. Key data attributes may be described, e.g. origin, potential biases, consistency, reliability, validity, data types, schema, format and noise content; The source and reliability of each data source can be assessed, and the collection process and method explained, e.g. manual collection, sensors, surveys or data streams. In addition, the original purpose of collection must be noted in the case of personal data.

{38}------------------------------------------------

# <span id="page-38-0"></span>3.2 DEI.2 Data validation & quality checks

## <span id="page-38-1"></span>3.2.1 DEI.2.1 Establish a data quality process

**Criterion:** The responsible party should establish a data quality process for data requirements and data quality management across the entire data lifecycle, comprising the risk-based definition of quality criteria, metrics and acceptance thresholds, checking the data against the defined criteria, assessing deviations and gaps, implementing corrective and mitigation measures, providing traceable documentation of requirements, methods, results, decisions and residual risks, as well as continuous monitoring and reevaluation**.**

#### **Dependencies:** None

## **Guidance**

**Provider:** The aim is to ensure the traceability, reproducibility and suitability of the training, validation and test data throughout the lifecycle. To this end, quality dimensions such as accuracy, consistency, completeness and timeliness can be recorded; required features, data volumes, statistical parameters and representativeness can be defined. Inclusion and exclusion criteria, the handling of uncertainty, annotation guidelines with quality assurance, and guidelines on synthetic data may be included; a reference to regulatory requirements is advisable. In addition, regular reviews and traceable documentation of methods, results, decisions and residual risks may be carried out.

**Deployer:** The aim is to ensure that the input data used in operations is fit for the intended purpose and is used in accordance with the provider's specifications. To this end, the requirements and guidance provided regarding data attributes, permissible inputs, and timeliness and completeness can be applied to the data used in operations. Appropriate monitoring and validation intervals are recommended in order to detect deviations in data quality at an early stage during ongoing operations. Processes for recording, prioritising and rectifying such findings can be established.

{39}------------------------------------------------

# <span id="page-39-0"></span>3.2.2 DEI.2.2 Data quality process to ensure completeness and coverage

**Criterion:** The responsible party should establish a data quality process to ensure the completeness and coverage of the relevant data sets**.**

**Dependency:** [DEI.2.1](#page-38-1)

# **Guidance**

**Provider:** The aim is to ensure that the completeness and coverage of the relevant datasets are designed in such a way that models are developed on the basis of sufficiently representative data and that quality risks are identified at an early stage. This may include defining expected attributes and entity instances for the use case; checks for data completeness can be implemented, including analysis of missing values according to loss patterns (MCAR, MAR, MNAR). The coverage of relevant features can be systematically checked; basic statistical analyses can identify gaps at the dataset, column and data point levels. In addition, domainspecific completeness criteria can be taken into account, e.g. the completeness of labels in image recognition. Further guidance on this can be found in the BSI's QUAIDAL product series.

**Deployer:** The aim is to ensure that only input data of sufficient quality is used during operation, thereby avoiding unreliable results and associated risks. To this end, input data can be checked for completeness against the attribute requirements documented by the provider; processes for detecting incomplete data can be put in place. If issues are identified, processing can be prevented or escalated to defined points. Recurring completeness issues can be documented; feedback to the provider or upstream data suppliers can be provided in a structured manner to address the root causes and improve data quality in the long term. Further guidance on this can be found in the BSI's QUAIDAL product series.

{40}------------------------------------------------

# <span id="page-40-0"></span>3.3 DEI.3 Data Documentation & Lineage

## <span id="page-40-1"></span>3.3.1 DEI.3.1 Establish a Data Provenance Process

**Criterion:** The responsible party should establish a data provenance process for the documentation and traceability of data sources throughout the entire data lifecycle, comprising the definition of requirements for data sources and their procurement, assessing the suitability, trustworthiness and integrity of the sources, recording and maintaining information on origin, processing and versioning, regularly reviewing procurement and usage, and providing traceable documentation of assessments, evidence and changes**.**

#### **Dependencies:** None

## **Guidance**

**Provider:** The aim is to ensure that data sources and their history for training, validation and test data are made fully traceable and that their provision can be organised in a legally compliant manner. Standards and metadata models can map provenance, context and transformations; documentation of, for example, imputation, normalisation and encoding is advisable. Automated lineage, immutable logs and versioning can be supplemented by signatures, checksums or hashes; catalogues can support audits. Access control, consent and licence management, as well as segregation of duties, can reduce the risk of misuse. Integration with data governance and ETL tools is recommended; regular audits, monitoring and secure logs can support compliance. In addition, the deletion of provenance data in accordance with its lifecycle is desirable. Further guidance on this can be found in the BSI's QUAIDAL product range.

**Deployer:** The aim is to ensure that data sources and their history for operational and input data are documented in a way that is comprehensible within the operational context and can be traced. To this end, the origin, context and processing steps of incoming data can be recorded and tagged with metadata; version control and a change history are advisable. Automated logging and checksums can safeguard the integrity of input data; data sources can be regularly checked for suitability, reliability and timeliness. Access control and segregation of duties can reduce the risk of manipulation. In addition, relevant provenance information can be fed back to the provider, e.g. in the event of anomalies or changes to sources; it is recommended that proofs of origin be retained and deleted in accordance with their lifecycle. Further guidance on this can be found in the BSI's QUAIDAL product range.

{41}------------------------------------------------

# <span id="page-41-0"></span>3.4 DEI.4 Define baseline/heuristics & model approach

# <span id="page-41-1"></span>3.4.1 DEI.4.1 Establish a development process

**Criterion:** The responsible party should establish a development process to fulfil the defined quality characteristics and objectives, comprising requirements analysis and conceptual design, as well as the justified selection of methodology, algorithms and models; design decisions regarding architecture and functionality; development and training; validation and verification; release and delivery; and traceable documentation across all phases**.**

#### **Dependency:** None

# **Guidance**

**Provider:** The aim is for the development of the AI system to follow a structured and traceable approach across all phases, ensuring quality, safety and regulatory compliance from conception through to delivery. To this end, the process may be based on established process models, e.g. MLOps reference architectures, and integrated into the overarching quality and change management framework. Clear handover criteria between phases are advisable, as is a consistent link between requirements, design decisions, training runs, validation results and approvals. In addition, the reproducibility of training runs, versioning of data, code and model artefacts, and a level of phase documentation commensurate with the risk are desirable; the early incorporation of security and compliance requirements supports deliverability.

{42}------------------------------------------------

# <span id="page-42-0"></span>3.5 DEI.5 Integration of external models

### <span id="page-42-1"></span>3.5.1 DEI.5.1 Document AI system architecture

**Criterion:** The responsible party should document the architecture of the AI system, comprising the AI components and their roles in the context of the system's purpose, the hardware and software integration including associated requirements, the interfaces for users and to connected systems, the information flows between the system components, and the rationale for the architectural choices**.**

#### **Dependency:** None

### **Guidance**

**Provider:** The aim is to ensure that the system architecture is documented in a way that is sufficiently transparent to support integrability, maintainability and secure further development throughout the system's lifecycle. The documentation may be sufficiently detailed to make the relationships between the building blocks and their interaction with regard to the system's purpose understandable; presentation tools such as architecture diagrams, component models and data flow models can enhance comprehensibility. The hardware and software integration, including associated requirements, as well as the interfaces for users and to connected systems, can be described, and the information flows between the system components can be illustrated. When justifying the choice of architecture, conflicts of interest relating to security and quality (e.g. between performance, robustness and maintainability) can be presented in a comprehensible manner. For independent adaptations such as online learning, it is advisable to describe the framework conditions, limitations and control points in order to prevent uncontrolled changes. In addition, the architecture documentation can be versioned and updated in the event of significant changes, ensuring that it remains consistent with the actual system status.

{43}------------------------------------------------

# <span id="page-43-0"></span>3.5.2 DEI.5.2 Document the use of pre-trained models

**Criterion:** The responsible party should document a justification for the use of pre-trained models, comprising a rationale for their suitability for the intended task (e.g. domain coverage, cost-benefit), an assessment of service level agreements (in particular availability, scalability and performance under typical load profiles), as well as a phase-out and continuity strategy, including fallback options, migration paths and data and artefact portability**.**

#### **Dependencies:** None

## **Guidance**

**Provider:** The aim is to ensure the traceability of the model selection and operational viability in the event of dependency on third-party providers. To this end, the documentation may justify why a pre-trained model is suitable for the task, e.g. domain coverage, cost-benefit. An assessment of service level agreements is advisable, particularly regarding availability, scalability and performance under typical load profiles. In addition, an exit and continuity strategy is appropriate; this may include a description of fallback options, migration paths and data or artefact portability, e.g. model descriptions, intermediate results and tokenisers.

{44}------------------------------------------------

# <span id="page-44-0"></span>3.5.3 DEI.5.3 Document upstream AI products

**Criterion:** The responsible party should document the upstream AI products used directly, specifying whether and which upstream AI products are integrated (including information at the system level (e.g. versioning and input/output modalities), model level (e.g. training modalities and licensing model), dataset (e.g. name and origin), infrastructure (e.g. AI-specific hardware and firmware), as well as information relating to security (e.g. compliance and vulnerabilities) and KPIs (e.g. security and performance metrics)), and a description of the integration and existing data flows**.**

#### **Dependency:** None

# **Guidance**

**Provider:** The aim is to make dependencies on upstream AI products transparent and to ensure that their influence on the object of conformity remains traceable. To this end, it can be documented whether and which upstream AI products are integrated; identifying characteristics, source, licence and terms of use, as well as available conformity documentation, are helpful. In addition, a description can be provided of how the integration takes place, what data flows exist and what changes have been made to the upstream product, e.g. fine-tuning or quantisation.

{45}------------------------------------------------

# <span id="page-45-0"></span>4 Verification and Validation (VAV)

The following section lists measures designed to establish a regulated framework for the robust testing of the AI system by embedding the systematic assessment of security and robustness against AI-specific attack vectors, as well as the traceable verification of compliance with requirements prior to deployment.

# <span id="page-45-1"></span>4.1 VAV.1 Security/Robustness Testing

# <span id="page-45-2"></span>4.1.1 VAV.1.1 Quality management process for AI-specific cybersecurity

**Criterion:** The responsible party should establish a quality management process for AI-specific cybersecurity, including the assessment of the attack surface, the derivation of attack scenarios and test cases, the simulation of attacks, and the implementation and testing of the effectiveness of countermeasures**.**

**Dependency:** [GCS.3.1](#page-18-1)

# **Guidance**

**Provider:** The aim is to ensure that risk-based and verifiable requirements underpin the security of the AI system and that AI-specific attack vectors are systematically identified and addressed. To this end, requirements can be derived from the risk assessment and incorporated into the system description; this includes adverse scenarios, minimum protection levels, and degrees of resilience against specific threats and attacks. The attack surface of the AI system can be assessed (e.g. input/output interfaces, model access, training/inference pipeline); from which attack scenarios and test cases can be derived, e.g. evasion, data poisoning, model extraction or prompt injection. The effectiveness of the derived countermeasures can be verified through simulated attacks (e.g. adversarial testing, red teaming). In addition, cybersecurity metrics with target values and tolerance intervals are appropriate; the requirements, scenarios, results and measures can be documented in a consistent and traceable manner and made available to downstream stakeholders, thereby enabling efficient audits and verification.

**Deployer:** The aim is to ensure that the security requirements defined by the provider are effectively implemented and monitored within the operational context, and that AI-specific attack vectors are actively tested within the organisation's own operational environment. To this end, the documented minimum protection levels and resistance levels can be applied to the specific operational environment and, where necessary, supplemented with context-specific threat scenarios. Cybersecurity metrics can be monitored operationally and checked against the defined target values and tolerance intervals; deviations can be documented and escalated. Regular security audits can be carried out during operations, drawing on threat intelligence and observations from live operations to derive and simulate attack scenarios (e.g. adversarial testing, red teaming). In addition, findings can be incorporated into operational risk management and fed back to the provider.

{46}------------------------------------------------

# <span id="page-46-0"></span>5 Deployment (DEP)

The following section lists measures designed to establish a regulated framework for the controlled transition of the AI system into live operation by ensuring that only authorised and tested changes take effect via regulated change, testing and release procedures.

# <span id="page-46-1"></span>5.1 DEP.1 Deployment Plan & Release

### <span id="page-46-2"></span>5.1.1 DEP.1.1 Establish change management and release procedures

**Criterion:** The responsible party should establish change management, testing and release procedures to ensure that only authorised and approved changes to the AI application are used in production**.**

**Dependency:** None

# **Guidance**

**Provider:** The aim is to establish robust change, testing and release processes to ensure that only authorised, tested changes are safely deployed into production, whilst guaranteeing traceability and operational security. This may include defining and documenting procedures for change, testing and release; changes can be classified, authorised and handled in accordance with the dual-control principle and separation of duties. Prior to rollout, testing and validation can be carried out and acceptance documented. Release and deployment processes may include versioning, rollback and migration steps. Procedures for the installation and monitoring of model changes, as well as operational performance and drift monitoring, including alerting, can be established; evidence can be stored in an audit-proof manner. In addition, emergency and standard changes – including CAB and exceptions – can be regulated, access controlled and changes communicated to stakeholders.

**Deployer:** The aim is to ensure that changes to the AI system are introduced in a controlled manner within the organisation's own operational context, so that only authorised and verified changes take effect in production and operational reliability can be guaranteed at all times. This may involve establishing a documented and approved change management process that classifies and assesses changes and authorises them in accordance with the dual-control principle and the separation of duties. Before vendor updates, configuration adjustments or model changes are deployed into production, tests can be carried out in a representative environment and acceptance procedures formally documented. Release and deployment procedures may include versioning, rollback and migration steps, as well as defined maintenance windows. The installation and monitoring of model changes can be logged in a traceable manner; operational performance and drift monitoring with alerts can support the early detection of deviations. Evidence relating to tests, approvals and rollouts can be stored in an audit-proof manner; emergency and standard changes, including escalation and exception processes, can be regulated. In addition, access to production systems can be controlled, relevant changes communicated internally and, in the event of significant deviations, reported back to the supplier.

{47}------------------------------------------------

# <span id="page-47-0"></span>6 Operations, Performance and Supervision (OPS)

The following section lists measures designed to establish a regulated framework for the secure and monitored operation of the AI system by embedding the ongoing monitoring of performance, robustness, data and security; the logging of relevant events; the handling of incidents; and the orderly adaptation and maintenance of the system during live operation.

# <span id="page-47-1"></span>6.1 OPS.1 Monitoring in Production

# <span id="page-47-2"></span>6.1.1 OPS.1.1. Data management process for operational and input data

**Criterion:** The responsible party should establish a data management process for operational and input data**.**

**Dependency:** [DEI.1.1](#page-34-2)

# **Guidance**

**Provider:** The aim is to ensure that the data generated during operations is specified in such a way that quality, traceability and compliance can be guaranteed even during ongoing use. To this end, requirements for operational and input data, a data model or data architecture, as well as guidelines on logging, retention and deletion of operational data, can be defined. Procedures for ongoing data quality assurance and for detecting distribution shifts (drift) can be described, and roles, resources and responsibilities can be specified. In addition, compliance with legal requirements, as well as versioning and approvals, are recommended.

**Deployer:** The aim is to ensure that operational and input data are continuously quality assured, used for their intended purpose and handled in compliance with regulations within the operational context. To this end, operational data can be regularly checked for suitability, quality and distribution shifts; relevant data states can be logged to ensure reproducibility; and retention and deletion policies can be implemented. Access management and integrity checks are recommended. In addition, quality deviations or anomalies can be documented and reported back to the provider.

{48}------------------------------------------------

# <span id="page-48-0"></span>6.1.2 OPS.1.2 Establish a monitoring process

**Criterion:** The responsible party should establish a monitoring process comprising the definition of monitoring objects as well as (where applicable, missing) metrics and thresholds, taking into account quality and risk management; the implementation of monitoring mechanisms; the continuous collection and evaluation of metrics; the assessment of deviations; the documentation of results**;** and regular review and adjustment**.**

**Dependency:** None

# **Guidance**

**Provider:** The aim is for monitoring to be designed as a coherent system that consistently links various monitoring dimensions – e.g. performance, robustness, security, data and conceptual drift, explainability – rather than considering them in isolation. An architecture with a common telemetry basis, harmonised metric definitions and a consistent time basis is appropriate; Risk and protection requirements can guide the granularity of monitoring. In addition, integration with logging, incident management and risk management, as well as consideration of false positive and false negative rates, are desirable. Tool support, including dashboards and automated alerts, can effectively assist in the assessment of anomalies.

**Deployer:** The purpose of this requirement is to ensure that monitoring provides meaningful insights within the operational context to support operational decisions. To this end, the framework provided by the vendor can be supplemented with context-specific metrics, e.g. business key performance indicators or domain-specific plausibility checks that cannot be captured by the vendor's monitoring system. Integration into existing IT monitoring and SIEM environments is advisable, as are clear responsibilities for the analysis. In addition, it is desirable to prevent alarm fatigue through sensibly calibrated thresholds and to conduct regular reviews of monitoring effectiveness; findings can be fed back to the provider in a structured manner.

{49}------------------------------------------------

# <span id="page-49-0"></span>6.1.3 OPS.1.3 Monitoring process for robustness

**Criterion:** The responsible party should establish a monitoring process to ensure the robustness of the AI system**.**

**Dependency:** [OPS. 1 .2](#page-48-0)

# **Guidance**

**Provider:** The aim is to identify and assess weaknesses in the AI system's robustness at an early stage, so that its resilience to disruptions and unfavourable input conditions is maintained. To this end, relevant aspects of robustness can be monitored on an ongoing basis, e.g. behaviour in the event of input disruptions, outliers, incomplete or noisy data, as well as in borderline and special cases; Results can be consolidated into robustness scenarios. The assessment may take into account model and algorithmic weaknesses, affected data features, and implementation references. In addition, appropriate technical responses are advisable, e.g. retraining, model downgrading, adjustment of the scope of application or a fallback option, in each case subject to validation and approval. Furthermore, a reassessment of robustness exposure at least once a year and on an ad hoc basis is desirable; in the case of transfer learning, it is advisable to take into account the robustness weaknesses of pre-trained models used.

**Deployer:** The purpose of this requirement is to ensure that robustness risks within the deployer's own operational environment are continuously identified and effectively addressed. To this end, the agreed robustness indicators can be monitored in production, and observations from live operations can be utilised, e.g. regarding behaviour in the event of atypical, corrupted or incomplete inputs. Relevant changes in the usage context, in interfaces or in the input data can be assessed on a case-by-case basis and fed back to the provider. In addition, responses can be triggered in accordance with operating manuals, e.g. activation of the fallback option, a reset mechanism or the initiation of retraining by the provider; updated models can be adopted following approval. Reviews should be carried out at least annually and on an eventdriven basis.

{50}------------------------------------------------

# <span id="page-50-0"></span>6.1.4 OPS.1.4 Monitoring process for data in operation

**Criterion:** The responsible party should establish a monitoring process for the AI system's data during operation**.**

**Dependency:** [OPS.1.2](#page-48-0)

# **Guidance**

**Deployer:** The purpose of this requirement is to ensure that the AI system's data is continuously monitored during ongoing operation with regard to quality, distortions and changes. To this end, the functions provided by the supplier and the recommended tests can be actively utilised, e.g. sanity checks to detect model drift, as well as checks for malicious or distorted input data. Thresholds for human review can be configured, and countermeasures triggered in the event of deviations. In addition, structured feedback to the provider is advisable if systematic problems are identified that cannot be resolved independently.

{51}------------------------------------------------

# <span id="page-51-0"></span>6.1.5 OPS.1.5 Monitoring process for performance

**Criterion:** The responsible party should establish a monitoring process for the performance of the AI system**.**

**Dependency:** [OPS.1.2](#page-48-0)

# **Guidance**

**Provider:** The aim is to ensure that deviations in the AI system's performance during operation are detected early and kept within stable limits, even in the event of model and concept drift. To this end, suitable tests and indicators can be provided, e.g. sanity checks to monitor performance limits, as well as suitable indicators for model and concept drift, distinguishable from pure data drift; Data collection procedures can be established, e.g. labels or proxy signals such as feedback and business metrics. A continuous testing plan with defined thresholds and human review is advisable, as are mechanisms for the automatic monitoring of major system changes. In addition, technical responses are advisable, e.g. retraining, model downgrading, adjustment of the scope of application or a fallback option, in each case subject to validation and approval. Furthermore, a clear rationale is recommended to demonstrate that the measures adequately maintain performance.

**Deployer:** The aim is to confirm the effectiveness of the performance measures in actual operation and to respond in a manner appropriate to the risk in the event of deviations or drift. To this end, the sanity checks and drift indicators provided can be evaluated on an ongoing basis; available labels can be collected and, where scarce, supplemented with substitute signals, e.g. feedback or business metrics. It can be checked whether the performance limits and residual risks documented by the provider are confirmed in operation or whether new risks arise due to the context. In addition, responses in accordance with operating manuals can be triggered, e.g. activation of the fallback option, a reset mechanism or initiation of a retraining process with the provider; updated models can be implemented following approval. If risk mitigation proves insufficient, it is advisable to escalate the matter to the provider, adjust usage or temporarily suspend operations. It is recommended to distinguish this from mere data drift.

{52}------------------------------------------------

# <span id="page-52-0"></span>6.1.6 OPS.1.6 Monitoring process for AI-specific cybersecurity

**Criterion:** The responsible party should establish a monitoring process for AI-specific cybersecurity**.**

**Dependency:** [OPS.1.2](#page-48-0)

# **Guidance**

**Provider:** The aim is to embed AI-specific security risks within an overarching security monitoring framework and to detect new attack risks and robustness weaknesses at an early stage. To this end, security telemetry for AI components can be established to record model-related events, resource and infrastructure anomalies, as well as access and query patterns; alarm-based thresholds and severity levels can be defined for threat patterns typical of AI. In addition, continuous monitoring of the threat landscape can be carried out, including regular research into the state of the art, the results of which can be consolidated into threat scenarios; this can take into account model and algorithmic vulnerabilities, specific attack vectors, affected data attributes, as well as the objectives, knowledge and capabilities of potential attackers. Integration into the overarching security monitoring framework (e.g. SIEM, SOC processes) can be provided for and linked with logging and incident management. A reassessment of risk exposure, at least annually and as and when required, is desirable; in the case of transfer learning, it is advisable to take into account threats posed by pre-trained models that are in use. Implementation should be based on the state of the art; relevant recognised standards and frameworks (e.g. BSI IT-Grundschutz) must be taken into account in their current versions.

**Deployer:** The aim is to ensure that AI-specific security incidents are detected promptly during operations and integrated into the organisation's own security monitoring, and that new security and robustness risks are continuously assessed. To this end, the security and telemetry functions provided by the supplier can be integrated into the organisation's own SIEM/SOC environment, severity levels and thresholds can be finetuned, and alerts can be routed into defined response processes. In addition, threat intelligence, the organisation's own security reports and observations from live operations can be utilised; relevant changes in the usage context, in interfaces or in the threat landscape can be assessed on a case-by-case basis and fed back to the provider. Reviews should be carried out at least annually and on an event-driven basis; any resulting measures can be implemented in line with the provider's specifications. Implementation should be based on the state of the art; relevant recognised standards and frameworks must be taken into account in their current versions.

{53}------------------------------------------------

# <span id="page-53-0"></span>6.1.7 OPS.1.7 Monitoring process for security-related incidents in the supply chain

**Criterion:** The responsible party should establish a monitoring process for security-related incidents in the supply chain**.**

**Dependency:** [OPS.1.2](#page-48-0)

# **Guidance**

**Provider:** The aim is to ensure that security-related events in the supply chain are specifically monitored and logged in such a way that their origin, impact path and affected components remain traceable, as changes to data sources, pre-trained models or integrated services can affect the AI system without being noticed. To this end, supply chain-specific monitoring points can be established, e.g. integrity checks on pretrained models, vulnerability feeds for model libraries in use, schema and quality monitoring of external data sources, or status reports from upstream API services. In addition, supply chain-related events can be recorded, e.g. the procurement and integrity checks of pre-trained models, version changes to external data sources, security alerts regarding model libraries in use, or authentication events at supplier interfaces; contextual information on supplier identity, the affected component and the origin of the version is useful in this regard. A logging structure that enables correlation along the supply chain and with a software or model bill of materials is desirable. In addition, threat intelligence sources relating to AI supply chains are useful. Furthermore, a periodic reassessment of the supply chain topology is recommended, so that new dependencies and risks can be incorporated into the monitoring process in a timely manner.

**Deployer:** The purpose of this requirement is to ensure that changes and anomalies originating from upstream components of the supply chain are detected at an early stage within the deployer's own operational context and recorded with sufficient forensic context. To this end, status information, security advisories and updates from the provider and other suppliers can be systematically monitored and assessed, e.g. regarding model versions, pre-trained components or integrated third-party services. Anomalies at interfaces to upstream services can be monitored, e.g. unusual response times, schema deviations or availability outages. In addition, interactions with upstream services can be consistently logged, e.g. model references, version changes, incoming security alerts, and authentication and integrity events at supplier interfaces; a central repository linked to the supply chain topology is advisable. Retaining and protecting the logs in line with the risk posed by supply chain dependency is desirable, so that supply chain-related incidents can be investigated at a later date. In addition, it is advisable to periodically adapt the monitoring priorities to changes in the supply chain.

{54}------------------------------------------------

### <span id="page-54-0"></span>6.1.8 OPS.1.8 Establish a logging process

**Criterion:** The responsible party should establish a logging process comprising the definition of log content and metadata, taking into account quality and risk management, defining retention periods and storage structures, implementing technical and organisational safeguards, recording and storing log data, analysing the logs, and reviewing and adapting the logging concept to identify events and incidents in the AI system**.**

**Dependency:** None

### **Guidance**

**Provider:** The aim is for logging to serve as a robust basis for traceability, fault analysis, security monitoring and regulatory compliance, whilst covering specific requirements for AI systems. It is advisable to follow established standards such as structured log formats and uniform time bases; the confidentiality, integrity and protection against tampering of the logs can be supported by appropriate cryptographic and organisational measures. In addition, a careful balance between evidential value and data requiring protection is desirable, e.g. through the pseudonymisation of sensitive content or differentiated retention rules. The interpretability of the logs for audits, automated evaluation and forensic analysis is a key quality feature.

**Deployer:** The purpose of this requirement is to ensure that logging meets the organisation's own legal, organisational and operational requirements and is consistently integrated into the existing logging infrastructure. To this end, integration with central log management or SIEM systems may be implemented, supplemented by specifications regarding retention, access and deletion in accordance with internal policies, legal requirements and sector-specific retention obligations. It is desirable to distinguish between different confidentiality levels and to protect against unauthorised access. In addition, regular spot checks for completeness, deliberate control of log volume and processes for audit-proof preservation of evidence in the event of an incident are advisable.

{55}------------------------------------------------

# <span id="page-55-0"></span>6.2 OPS.2 Incident Response & Rollback

# <span id="page-55-1"></span>6.2.1 OPS.2.1 Establish a security incident reporting process

**Criterion:** The responsible party should establish a security incident reporting process comprising the definition, identification and reporting of serious incidents to the relevant reporting bodies within the organisation, taking the AI policy into account**.**

#### **Dependency:** None

# **Guidance**

**Provider:** The purpose of this requirement is to ensure that the reporting of serious incidents is carried out in accordance with regulatory requirements and within the prescribed time limits. To this end, relevant reporting obligations may be identified and incorporated into a taxonomy of serious incidents; reporting deadlines, templates for incident files and procedures for notifying the deployer, users and, where applicable, affected individuals are appropriate. In addition, detection and classification mechanisms with threshold values can be established. Furthermore, follow-up reports and documentation during deployment, operation, validation and monitoring are desirable.

**Deployer:** The aim is to ensure that serious incidents are detected, escalated and reported to the relevant reporting bodies within the prescribed time limits. To this end, the provider's guidelines can be adapted to the operational context and contact points and escalation channels—both internal and external—can be established. In addition, deadlines set by supervisory authorities must be observed; incident records containing a description, root cause analysis, scope of impact, timeline and measures taken can be maintained, and notifications to users and, where applicable, affected individuals can be arranged. Furthermore, follow-up reports to authorities are advisable; findings can be fed back to the provider.

{56}------------------------------------------------

# <span id="page-56-0"></span>6.2.2 OPS.2.2 Establish emergency shutdown and fallback mechanisms

**Criterion:** The responsible party should establish emergency shutdown and fallback mechanisms for the AI product, including fail-safe states and behaviour**.**

**Dependency:** None

# **Guidance**

**Provider:** The aim is to ensure that, in the event of malfunctions, the AI product is rapidly transitioned to a safe state and that essential functions are either systematically deactivated or restored. To this end, an accessible emergency stop function with clear priority across all control levels can be designed; safe states and behaviour must be defined, e.g. defined shutdowns or degraded modes. In addition, testing and validation covering relevant fault scenarios are advisable, e.g. outside the intended operating range. This also includes the documentation of emergency procedures, fallback behaviour, recovery processes and times, as well as a reasoned safety case.

<span id="page-56-1"></span>**Deployer:** The purpose of this requirement is to ensure safe shutdown and continuity of operation. To this end, the emergency stop function should be configured to be easily accessible and practised regularly; operating limits and indicators for breaches of the operating range must be defined and monitored. In addition, recovery processes, including defined restart times, can be prepared and verified in the target environment. Furthermore, a clear hierarchy of roles and escalation procedures is advisable; staff training on emergency and recovery procedures, as well as the logging of activations and tests, can demonstrate effectiveness.

{57}------------------------------------------------

# <span id="page-57-0"></span>6.2.3 OPS.2.3 Establish an incident management process

**Criterion:** The responsible party should establish an incident management process comprising the definition of (any missing) incident types and classification, taking into account quality and risk management; the definition of roles, reporting channels and escalation paths, the identification, classification and documentation of incidents, the containment and restoration to a secure state, the notification of relevant stakeholders, the analysis of root causes, and the implementation of corrective and recovery measures**.**

#### **Dependency:** None

# **Guidance**

**Provider:** The aim is for incident management to be structured as a closed-loop system with measurable effectiveness, treating AI-specific incident types on an equal footing with traditional IT security incidents. Integration with the existing security organisation is advisable, supplemented by AI-specific expertise for phenomena such as model manipulation, prompt injection or data poisoning. Exercises, e.g. tabletop exercises with realistic AI scenarios, are desirable. In addition, the process can be designed so that findings are fed back in a structured manner into development, monitoring and risk management processes; interfaces with security incident reporting obligations and communication with Deployer are advisable.

**Deployer:** The purpose of this requirement is to ensure that incidents in an operational context are reliably addressed and that AI-specific aspects are appropriately taken into account. Integration into the organisation's existing incident management framework is advisable, so as to avoid the creation of isolated, specialised AI processes; incident types typical of AI, such as model misuse, hallucinations with knock-on effects or drift-driven erroneous decisions, can be explicitly incorporated. Clear interfaces with the provider are desirable, e.g. for escalation, information exchange and the provision of model updates. In addition, regular exercises and the incorporation of lessons learnt into risk management, training and configuration adjustments are advisable.

{58}------------------------------------------------

# <span id="page-58-0"></span>6.2.4 OPS.2.4 Incident management process for security-related events in the supply chain

**Criterion:** The responsible party should establish an incident management process for security-related events in the supply chain**.**

**Dependency:** [OPS.2.3](#page-56-1)

# **Guidance**

**Provider:** The aim is to ensure that security-related events originating from the supply chain are specifically identified and addressed, as these arise outside the direct sphere of influence but can have a direct impact on the AI system. To this end, supply chain-related event types can be catalogued, e.g. compromised training data sources, manipulated pre-trained models, vulnerable libraries in model pipelines, or security incidents at cloud or API providers. In addition, investigation and response procedures that take into account the involvement of upstream suppliers, contractual reporting obligations and joint forensic analysis are advisable. Furthermore, sources of threat intelligence relating to AI supply chains and software bill-of-materials data can be incorporated into the detection logic.

**Deployer:** The purpose of this requirement is to ensure that supply chain-related security incidents originating with the provider, model suppliers or data suppliers are effectively addressed within the organisation's own operational context. To this end, reports from upstream providers regarding vulnerabilities, model updates or incidents can be received and assessed in a structured manner, e.g. regarding compromised models or affected training data. Escalation procedures to suppliers with defined response times are advisable. In addition, it is desirable to assess the consequential risk to one's own operations, including prepared measures such as temporarily suspending use, switching to a fallback model, or implementing additional input and output checks.

{59}------------------------------------------------

# <span id="page-59-0"></span>6.3 OPS.3 Iteration: Retraining & Updates

# <span id="page-59-1"></span>6.3.1 OPS.3.1 Establish a quality metric adjustment process

**Criterion:** The responsible party should establish a quality metric adjustment process comprising the definition of suitable quality metrics and adequacy criteria (e.g. use-case relevance, risk profile, metric definition and thresholds), a traceable derivation including assumptions, data sources and validation results, the definition of adjustment triggers in the event of changes to requirements, data, models or risks, formal approval and regular review, as well as the definition of responsibilities and audit-proof documentation**.**

#### **Dependencies:** None

# **Guidance**

**Provider:** The aim is to establish a robust and traceable procedure for defining and adjusting appropriate quality metrics, so that the performance and risks of the AI system can be consistently assessed throughout its lifecycle. To this end, the process can be documented, formally approved and regularly reviewed; criteria for appropriateness, such as use-case relevance, risk profile, metric definition and thresholds, can be defined. Procedures and triggers for adjustment in the event of changes to requirements, data, models or risks can be specified. The derivation, including assumptions, data sources and validation results, can be documented in a traceable manner; responsibilities can be assigned, and supporting evidence can be versioned and stored in an audit-proof manner.

**Deployer:** The aim is to ensure that the quality metrics defined by the provider are effectively applied within the deployer's own operational context and that operational assessment processes are aligned with them. This may involve incorporating the provider's quality metrics into operational monitoring and reporting processes; in addition, organisation-specific KPIs, such as user satisfaction, process turnaround times or escalation frequency, can be defined for the organisation's own management purposes without altering the AI system's own quality metrics. Measurement results can be logged, compared against the thresholds specified by the provider and incorporated into management reviews. In addition, deviations from the provider's specifications can be documented and reported to the provider.

{60}------------------------------------------------

# <span id="page-60-0"></span>6.4 OPS.4 Maintenance & Support

# <span id="page-60-1"></span>6.4.1 OPS.4.1 Establish a complaints and feedback process

**Criterion:** The responsible party should establish a complaints and feedback process for the submission and handling of complaints, including regular review of user feedback and the provision of information on the appeals procedure, feedback channels and feedback mechanisms, as well as the use of the findings for risk and quality management**.**

#### **Dependency:** None

# **Guidance**

**Provider:** The aim is to facilitate effective complaint channels and actionable user feedback for quality assurance and risk management. To this end, accessible submission methods can be provided, e.g. via a form within the application or by email; clear instructions regarding feedback or complaint procedures can be placed within the user interface. Categorisation, deadlines and escalation should be organised as a workflow; regular evaluation and documentation can support traceability. In addition, form and workflow tests, as well as usability and accessibility checks, can be carried out.

**Deployer:** The aim is to ensure that users are aware of complaint channels, can use them and receive feedback. To this end, channels can be configured within the organisation, and points of contact and service levels defined; a ticketing system and logging can promote traceability. Users can be informed about complaint channels, e.g. in frequently asked questions, via support or during induction. Feedback can be reviewed regularly, trends and risks addressed, and relevant points fed back to the provider. In addition, accessibility should be assessed in the specific context of use; findings regarding user-friendliness can be incorporated into improvements to processes and texts.

{61}------------------------------------------------

# <span id="page-61-0"></span>7 Retirement (RET)

The following section lists measures designed to establish a regulated framework for the orderly decommissioning of the AI system by enshrining the assessment of dependencies and impacts, as well as the regulated deactivation, archiving or deletion of the system and its data.

# <span id="page-61-1"></span>7.1 RET.1 Decommissioning / Retirement

# <span id="page-61-2"></span>7.1.1 RET.1.1 Establish an end-of-life process

**Criterion:** The responsible party should establish an end-of-life process comprising the definition, documentation and implementation of regulations and procedures for decommissioning, the assessment of dependencies and impacts, and the orderly deactivation, archiving or deletion of the AI system and its data**.**

**Dependency:** None

# **Guidance**

**Provider:** The aim is to ensure an orderly decommissioning process characterised by transparency and traceability. To this end, a deactivation plan may be drawn up for technical components, including roles and permissions as well as defined triggers; timely, channel-appropriate communication to those affected, including a replacement solution where appropriate, is advisable. Provision may be made for the archiving or discarding – with justification – of model parameters, training and operational data, user communications and logs. In addition, guidelines and procedures can be consistently documented and aligned with quality requirements for operations and security.

**Deployer:** The aim is to minimise operational disruptions and maintain compliance during the transition. To this end, communication with the provider can be utilised at an early stage for transition and contingency planning, including the assessment of interface and data dependencies; deactivation measures can be supported operationally, e.g. through authorisation management as well as change and incident coordination. Archiving or deletion can be coordinated with the provider, taking into account internal retention periods, contractual obligations and logs. In addition, it is advisable to coordinate business continuity aspects and user information within the organisation's own context.