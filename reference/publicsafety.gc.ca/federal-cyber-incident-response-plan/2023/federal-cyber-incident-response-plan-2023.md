# Federal Cyber Incident Response Plan

## Table of contents

- [1. Preamble](#s1)
  - [1.1 About this document](#s1.1)
  - [1.2 Effective Date](#s1.2)
  - [1.3 Authorities](#s1.3)
  - [1.4 Definitions](#s1.4)
- [2. Introduction](#s2)
  - [2.1 Context](#s2.1)
  - [2.2 Purpose](#s2.2)
  - [2.3 Scope](#s2.3)
  - [2.4 Objectives](#s2.4)
  - [2.5 Assumptions](#s2.5)
- [3. Management Process for Cyber Security Incidents Affecting Non-GC cyber systems](#s3)
  - [3.1 Stakeholders](#s3.1)
  - [3.2 Process Overview](#s3.2)
  - [3.3 GC Response Levels](#s3.3)
  - [3.4 Governance](#s3.4)
- [4. Reporting and Information Sharing](#s4)
  - [4.1 Reporting Events to the GC](#s4.1)
  - [4.2 Reporting Examples](#s4.2)
  - [4.3 Internal GC Information Sharing](#s4.3)
- [5. External Communications](#s5)
- [6. Management Process for Cyber Security Incidents that Affect both GC and non-GC Cyber Systems](#s6)
  - [6.1 Process overview](#s6.1)
  - [6.2 Governance](#s6.2)
  - [6.3 Internal GC Information Sharing](#s6.3)
  - [6.4 External Communications](#s6.4)
- [Appendix A: Glossary of acronyms and abbreviations](#sA)
- [Appendix B: Roles and Responsibilities](#sB)
  - [1. Core Stakeholders](#sB1)
  - [2. Secondary stakeholders](#sB2)
- [Appendix C: GC Response Levels](#sC)
- [Appendix D: Event Impact Assessment](#sD)
- [Appendix E: FCIRP Governance](#sE)
- [Appendix F: FCIRP Information Sharing Flow](#sF)
- [Appendix G: FCIRP and GC CSEMP Information Sharing Flow](#sG)

## 1. Preamble

### 1.1 About this document

This document describes Government of Canada (GC) coordination protocols for responding to cyber security events or incidents affecting non-GC systems. It outlines the stakeholders and actions required to ensure that cyber security incidents and events affecting non-GC systems are addressed by the GC in a consistent, coordinated and timely fashion. The purpose of this plan is to promote the adoption of best practices that would allow decision makers to have the necessary information and situational awareness to support Canadians when significant cyber security incidents or events occur.

The plan outlined below will be tested, reviewed, and modified every year.

A glossary of acronyms and abbreviations can be found at Appendix A.

### 1.2 Effective Date

This plan takes effect on May 12, 2023.

### 1.3 Authorities

This plan is prepared in the exercise of the responsibilities conferred to the Minister of Public Safety and Emergency Preparedness under the [*Emergency Management Act*](https://laws-lois.justice.gc.ca/eng/acts/e-4.56/), the [*Department of Public Safety and Emergency Preparedness Act*](https://laws-lois.justice.gc.ca/eng/acts/P-31.55/), the Minister of National Defence under the [*CSE Act*](https://laws-lois.justice.gc.ca/eng/acts/C-35.3/page-1.html)[Footnote 1](#fn1), and in line with the goals of [*Canada's National Cyber Security Strategy*](https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/ntnl-cbr-scrt-strtg/index-en.aspx).

### 1.4 Definitions

**Note:** These definitions are adapted from the [*Policy on Government Security*](https://www.tbs-sct.gc.ca/pol/doc-eng.aspx?id=16578) and the [*Government of Canada Cyber Security Event Management plan*](https://www.canada.ca/en/government/system/digital-government/online-security-privacy/security-identity-management/government-canada-cyber-security-event-management-plan.html). For some terms, additional examples are provided to clarify their interpretation for the purposes of this plan.

Compromise
:   A breach of cyber systems. Includes, but is not limited to:

    - Any action or event that results in the intentional or unintentional disclosure of information, which adversely impacts the confidentiality, integrity, or availability of information and computer systems.
    - Unauthorized access to, disclosure, modification, use, interruption, removal or destruction of sensitive information or assets, causing a loss of confidentiality, integrity, availability, or value.

Privacy Breach
:   The improper or unauthorized access, creation, collection, use, disclosure, retention or disposition of personal information.

Critical service
:   A critical service is one that, if disrupted, would result in a high or very high degree of injury to the health, safety, security or economic well-being of Canadians, or to the effective functioning of the Government of Canada.

Cyber system
:   A system of interdependent digital services, technologies, assets or facilities that form the infrastructure for the reception, transmission, processing or storing of information.

Cyber security
:   The protection of digital information, as well as the integrity of the infrastructure housing and transmitting digital information. More specifically, cyber security includes the body of technologies, processes, practices and response and mitigation measures designed to protect networks, computers, programs and data from malicious activity, damage, disruption, or unauthorized access so as to ensure confidentiality, integrity and availability.

Cyber security event
:   Any event, act, omission, or situation, whether successful or not, to gain access to, modify, destroy, delete, or render unavailable any computer network or system resource.

    - Examples of cyber security events: disclosure of a new vulnerability; intelligence that a threat actor may be planning malicious activity against a cyber system; attempts to breach the network perimeter; suspicious or targeted emails with attachments/links that were not detected by existing security controls; or suspicious or unauthorized network activity that represents a deviation from baseline.

Cyber security incident
:   Any event or collection of events, act, omission, or situation that has resulted in a compromise.

    - Examples of cyber security incidents: Data breaches, exfiltration of data, or compromise/corruption of information; intentional or accidental introduction of malware to a network; credential stuffing attacks; phishing campaigns; successful ransomware attempts; exploitation of vulnerability; failure of a security control; denial of service activities; or web or online presence defacement or compromise.

    A cyber security incident can result in a compromise or a privacy breach if it involves the inappropriate creation, collection, use, disclosure, retention or disposition of personal information.

    Throughout this document, for ease of reading, the term cyber security incident will be used[Footnote 2](#fn2).

Threat
:   Any potential event or act, deliberate or unintentional, or natural hazard that could result in a compromise.

Cyber Threat
:   Any potential event or act, deliberate, accidental or natural hazard, that could compromise IT assets[Footnote 3](#fn3).

Vulnerability
:   Weakness in an information system, system security procedures, internal controls, or implementation that could be exploited or triggered by a threat source.

## 2. Introduction

### 2.1 Context

Cyber systems increasingly underpin every component of our daily lives. A cyber security incident affecting assets that are not owned or operated by the GC could have significant negative consequences for Canadians, the economy, our democracy, and Canada's national security. To bolster Canada's overall cyber security posture, the GC must be prepared, when necessary, to take timely and coordinated action when significant cyber security incidents affect non-GC cyber systems.

### 2.2 Purpose

The purpose of this document is to provide a framework for the GC's management of cyber incidents that affect assets that are not owned or operated by the GC and are essential to the health, safety, security, defence, or economic well-being of Canadians.

This document will be both complementary to, and separate from, existing response mechanisms, such as the [Government of Canada Cyber Security Event Management Plan](https://www.canada.ca/en/government/system/digital-government/online-security-privacy/security-identity-management/government-canada-cyber-security-event-management-plan.html) (GC CSEMP) and the [Federal Emergency Response Plan](/cnt/rsrcs/pblctns/mrgnc-rspns-pln/index-en.aspx) (FERP)[Footnote 4](#fn4).

### 2.3 Scope

This plan is limited to cyber security incidents that require an integrated GC response to minimize negative repercussions for Canadians.

It is intended to streamline the GC's response to cyber security incidents affecting Canadian organizations that are not afforded cyber security services under the authority of the GC CSEMP and/or the FERP. These organizations could include, but are not limited to:

- Canadian organizations that affect services and assets which are essential to the health, safety, security, defence or economic well-being of Canadians;
- Federal Crown corporations;
- Research & development entities;
- The academic sector; and
- Provincial, territorial, or municipal government bodies and assets.

In the case of cyber security incidents that affect both GC and non-GC systems, the FCIRP and GC CSEMP may be activated in parallel to coordinate the GC response. This process is described in section 6.

### 2.4 Objectives

The objectives of the FCIRP are to:

- enhance situational awareness of cyber security incidents across stakeholders;
- inform decision-making at all levels;
- facilitate timely coordination and management of the GC's response to cyber security incidents affecting non-GC systems;
- contribute to mitigating the consequences of cyber security incidents and events;
- support GC-wide cyber risk assessment practices and remediation prioritization efforts;
- protect the confidentiality, availability, and integrity of programs and services, information, and operations relevant to non-GC cyber systems; and
- enhance public confidence in the GC's ability to coordinate responses to cyber security incidents across Canada.

### 2.5 Assumptions

The following assumptions were made during the development of this plan:

- each GC stakeholder will operate and support FCIRP in accordance with their legislated mandates;
- Entities that experience cyber security incidents that involve the disclosure of personal information will act in accordance with established legislation governing privacy protection (e.g., [*Personal Information Protection and Electronic Documents Act*](https://laws-lois.justice.gc.ca/ENG/ACTS/P-8.6/index.html) or provincial or territorial equivalents) and policy requirements ([*Policy on Privacy Protection*](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=12510)); and
- private sector stakeholders will engage collaboratively with the assurance of protection through existing privacy protocols and laws.

## 3. Management Process for Cyber Security Incidents Affecting Non-GC cyber systems

This section of the plan outlines the management process for cyber security incidents affecting non-GC cyber systems, identifies implicated stakeholders, defines response levels, and describes escalation triggers.

### 3.1 Stakeholders

Stakeholders are organized into two major categories: core stakeholders, who will always be engaged and play a key role in the FCIRP process; and secondary stakeholders, who may play a role depending on the nature of the cyber security incident. Detailed roles and responsibilities of each stakeholder can be found in Appendix B.

#### GC stakeholders

- **Core stakeholders**
  - The Canadian Centre for Cyber Security (the Cyber Centre), including the Communications Security Establishment (CSE) -Comms
  - PS-National Cyber Security Directorate (NCSD), including PS-Comms
  - Royal Canadian Mounted Police (RCMP)
  - Canadian Security Intelligence Service (CSIS)
  - Privy Council Office (PCO) Security and Intelligence, including PCO-Strategic Communications (PCO-SC)
  - Department of National Defence/Canadian Armed Forces (DND/CAF)
  - Global Affairs Canada (GAC)
- **Secondary stakeholders**
  - Shared Services Canada (SSC)
  - Treasury Board of Canada Secretariat (TBS)
  - PS-Government Operations Centre (GOC)
  - Lead Federal Departments and Agencies (LFDAs) for critical infrastructure sectors, as listed in Appendix B
  - Other GC stakeholders, where applicable

### 3.2 Process Overview

The FCIRP management process has four phases.

#### Phase 1: Preparation

The Preparation phase involves general readiness activities to ensure that the GC is ready to respond to a broad range of cyber security incidents across Canada. This phase includes putting in place the appropriate means to support the full spectrum of cyber security incident management requirements. A key component of this phase also includes the application of protective and preventive measures by owners and operators of assets and infrastructure underpinned by cyber systems.

In this phase:

- **PS-NCSD** will maintain and update the FCIRP;
- **PS-NCSD** will review lessons-learned reports from past events and facilitate any required cyber security policy development and information sharing sessions;
- **All stakeholders** will ensure the synchronization of the FCIRP with existing departmental plans, processes and procedures, participate in exercises, and ensure that applicable GC-wide lessons learned are implemented.
- **The Cyber Centre, PS-Critical Infrastructure Directorate (CID), and other LFDAs (see Appendix B for detailed list)** that liaise with owners and operators of non-GC cyber systems continue ongoing engagements that work to raise the overall cyber security baseline in Canada.

#### Phase 2: Notification, Detection and Assessment

The Notification, Detection and Assessment phase involves the discovery of a cyber security incident. The GC may become aware of a cyber security incident through various channels, such as the reports made to GC departments or agencies, reports made to local police, media, etc.  Regardless of how the GC becomes aware, cyber security incidents should be reported to CSE's Cyber Centre at the earliest opportunity through regular reporting channels or through the [Cyber Centre's Incident Reporting Portal](https://www.cyber.gc.ca/en/incident-management).

If there is reasonable evidence of suspected criminal activity, in addition to standard reporting to the Cyber Centre, affected entities should to report cyber security incidents directly to the RCMP's National Cybercrime Coordination Centre (NC3), police of jurisdiction, and CSIS, as required.

When merited, the Cyber Centre will discuss the cyber security incident with PS-NCSD for possible FCIRP activation and the determination of an appropriate GC response level. This process is summarized in the graphic below:

**Figure 1: Process Overview**

Image description

The process of activating the Federal Cyber Incident Response Plan (FCIRP) and determining the appropriate federal response level:

- A cyber incident is brought to the Government of Canada's attention.
- The stakeholder department should immediately notify the Cyber Centre of a potential incident.
- The Cyber Centre conducts an initial assessment of the incident to determine if the activation of the FCIRP is merited.
- As co-chairs, the Public Safety National Cyber Security Directorate and the Cyber Centre will jointly confirm whether activation of the FCIRP is merited. They will jointly determine the appropriate governance bodies.
- The incident is brought to the FCIRP Governance Body Meeting (see section 3.4).

In this phase:

- In monitoring information sources, an FCIRP stakeholder notices precursors of a real or potential cyber security incident that could reasonably be expected to have detrimental effects on a non-GC cyber system and **immediately notifies the Cyber Centre**;
- **The Cyber Centre** will conduct an impact assessment of the incident to determine if activation of the FCIRP is merited;
- Considering input if received from a stakeholder as mentioned in step 1, when activation of the FCIRP is believed to be merited, **the Cyber Centre** and **PS-NCSD** will then determine the appropriate FCIRP response level (as outlined in section 3.3), based on an analysis of available information; and
- **PS-NCSD and the Cyber Centre**, as co-chairs, will convene the appropriate governance bodies (as outlined in section 3.4), in accordance with the response level; and
- **The Treasury Board of Canada Secretariat (TBS)** will be engaged during this phase, as a third co-chair, if the cyber security incident affects both GC systems or information assets (GC CSEMP) and non-GC systems (FCIRP) (as outlined in section 6.1).

#### Phase 3: Mitigation, Support, and Investigation

The Mitigation, Support and Investigation phase consists of the coordinating actions that are required to minimize the impact on Canadians, facilitate information flows for senior decision makers (as outlined in section 3.3), and support the restoration of normal operations. Stakeholders listed in section 3.1 will play a critical role in sharing information and coordinating action. Concurrent criminal and national security investigations, by the RCMP and CSIS respectively may be required in the event of a possible cybercrime or threat to national security. The degree of GC involvement will vary, based on the established GC response level.

In this phase:

- **The Cyber Centre**, as Canada's technical and operational authority for cyber security, will coordinate inter-departmental operational incident response activities. This includes issuing advice and guidance, including technical assistance to GC and non-GC stakeholders, as required, as well as tracking and reporting these measures;
- **PS-NCSD and the Cyber Centre** will ensure relevant information is shared within the FCIRP governance bodies (as outlined in section 3.4) and, where appropriate, with other GC stakeholders to maintain situational awareness and support decision makers;
- **PS-Communications (Comms)** will be responsible for coordinating the GC communications approach (as outlined in section 5); and
- **PS-Government Operations Centre (GOC)**, for level 4 events, will perform strategic coordination, as described in the FERP (as outlined in section 3.3).

#### Phase 4: Post-Event Activity

The final phase, Post-Event Activity, is vital for continuous improvement of the overall process and, as such, feeds back into the preparation phase to complete the cyber security incident management life cycle. This phase consists of post-event analysis, preparation and review of lessons learned, and implementing changes to processes or procedures in order to continually mature the GC's cyber security incident response.

In this phase:

- **The Cyber Centre, when they are engaged by the affected entities**, will collate all findings and produce a post-event report, including a timeline of events, as well as any recommended actions for GC stakeholders;
- **PS-NCSD** will produce a strategic lessons-learned report for level 2, 3, and 4 events, including an action plan for implementing and addressing any associated recommendations or findings. These lessons-learned will be based on post-event reports developed by the Cyber Centre;
- **PS-GOC** will produce a complementary lessons-learned report and action plan for implementation of the lessons learned on behalf of the GC and monitor the implementation of the recommendations for level 4 events only, as outlined in the FERP; and
- **All other FCIRP stakeholders** will support the development of this report and assist with the implementation of related action items under their particular areas of responsibility.

These reports will be shared among core stakeholders (as outlined in section 3.2), secondary stakeholders as required, as well as any additional governance bodies that were engaged in the cyber security incident management process.

Barring any limitations created by non-disclosure agreements (NDAs) set out between GC organizations and affected entities, communication and reporting across all stakeholders will occur from the time that a cyber incident is detected to the conclusion of post-event activities, reporting and communication across all stakeholders occurs. Entrenching these ongoing activities into the life cycle of cyber security incident management is imperative to ensuring mitigation advice and status updates are shared in a timely fashion, enabling situational awareness, and supporting informed decision-making.

### 3.3 GC Response Levels

There are four response levels that govern the FCIRP process, as shown in Appendix C.

Response levels dictate the level of coordination required for any given cyber security incident, as well as stakeholder participation and reporting requirements.

**Level 1** represents day-to-day operations. The dynamic nature of the cyber threat environment and the constant disclosure of new cyber security vulnerabilities indicate that, in general, the GC will typically operate in a level 1 state. At a GC-wide level, no further coordination among core or secondary stakeholders is required, aside from already established information-sharing forums.

**Level 2** indicates that heightened attention is required, and is set by co-decision at the Director level (the Cyber Centre, PS-NCSD). This level will trigger the invocation of the **Event Coordination Team** (ECT) (as outlined in section 3.4) for all confirmed events and implies that some limited GC-wide coordination is required to share information, where appropriate, and inform decision makers. At this level, core and, as required, secondary FCIRP stakeholders at the working / Director-level will formally convene in person or virtually. The impacted entity may be invited to participate in the FCIRP response process. The ECT will be co-chaired at the Director-level by the Cyber Centre and PS-NCSD. Frequency of ECT meetings will be determined by the co-chairs, in consultation with participating stakeholders. ECT members will ensure situational awareness is maintained by briefing their respective management chain. A robust public communications plan may be required for cyber security incidents at this level. PS-Comms will lead, in close collaboration with CSE Comms, the GC communications approach (see section 5 and Appendix B for additional details).

**Level 3** indicates that immediate focus and action is required at the GC-level, and is set by decision at the Director-General level (the Cyber Centre, PS-NCSD). The ECT continues to meet, and level 3 triggers the invocation of the **Executive Management Team** (EMT) (as outlined in section 3.4) for all confirmed events. The EMT is scalable in scope but, at its base, consists of the Director-General Cyber Operations (DG Cyber Ops)[Footnote 5](#fn5) community, with additional secondary stakeholder representation as required. In addition to DG-level meetings, ad hoc meetings with relevant members of the Assistant Deputy Minister and/or Deputy Minister Cyber Security Committees (ADMCS/DMCS) may occur. At this level, information will be coordinated and shared between the ECT and EMT committees to inform and support decision makers. A robust public communications plan will be required for most cyber security incidents at this level. PS-Comms will lead, in close collaboration with CSE Comms and PCO Comms, the GC communications approach (see section 5 and Appendix B for additional details).

**Level 4** is reserved for severe or catastrophic events affecting non-GC cyber systems. Cyber security incidents that reach this level will shift to the FERP governance structure and will be coordinated by the PS-GOC in order to ensure the harmonization of federal response efforts. ECT and EMT meetings will continue to occur and focus on operational coordination while feeding necessary operational outputs into the FERP-level response.

#### Determination of FCIRP response levels

FCIRP response levels are determined based on the analysis of two factors: impact assessment (as outlined in Appendix D) and scope of the cyber security incident in question.

Impact assessments are initially performed by the Cyber Centre, using the Event Impact Assessment Matrix outlined in Appendix D of this document. The Cyber Centre may engage with the impacted organization to inform impact assessments. This process, applicable to all cyber security incidents in scope of this plan, is based on a standardized injury test designed to measure the degree of injury that has occurred or could reasonably be expected to occur due to a compromise. This injury assessment considers both the severity and scope of the event. Once the degree of injury is assessed, a modifier is applied to account for the probability of injury realization in cases where a cyber security incident has not yet occurred (for example, unrealized cyber threats and vulnerabilities).

When available, impact assessments from affected parties are also used by the ECT chairs to assess the urgency and establish an appropriate FCIRP response level.

### 3.4 Governance

During a cyber security incident, the appropriate governance bodies will focus both on coordination and information sharing to prevent, detect, respond to, and recover from cyber security incidents in a coherent manner. A diagram outlining the flow of information-sharing can be found in Appendix G.

#### Escalation Model

The governance structure, as outlined in Appendix E, identifies the GC stakeholders involved in the decision to escalate or de-escalate the status of a cyber security incident.

Given the short time frames in which cyber security incidents can cause significant damage, rapid meeting of the appropriate governance bodies is essential. For example, should an event be assessed at a level 3 from the outset, governance will immediately convene at the EMT level, with the ECT stood up concurrently to support the coordination and flow of information directly to the EMT, who will then share this information with the relevant senior officials.

Additional notes about the escalation model include:

- For **all** events:
  - stakeholders in level 1 of the escalation model are engaged (or remain active if already engaged) when higher levels are engaged during an event.
- For **Level 2** events:
  - The ECT co-chairs will recommend whether a level 2 cyber security incident should be declared, based on impact assessments and the Event Impact Assessment matrix (see Appendix D); and
  - The ECT co-chairs will decide whether to convene ECT meetings in person or virtually to establish a level 2 event, coordinate and share information. Information shared by the ECT members could factor into the to the decision to de-escalate or escalate an event. Each department/agency is responsible for designating leads.
- For **Level 3** events:
  - The ECT co-chairs will recommend whether a level 3 cyber security incident should be declared, based on impact assessments and the Event Impact Assessment matrix (see Appendix D); and
  - EMT activation implies that implicated stakeholders at the ECT and the EMT levels convene formally in person or virtually to establish a level 3 event, coordinate and share information. Information shared by the ECT and the EMT members could factor into the to the decision to de-escalate or escalate an event.
- For **Level 4** events:
  - the decision to escalate and move to FERP response coordination will be made by the PS-GOC, in consultation with the EMT;
  - ECT co-chairs and the Director General, Cyber Centre Operations, will ensure that subject matter expertise is made available to FERP event teams;
  - ECT and EMT meetings will continue parallel to FERP governance;
  - existing information-sharing mechanisms will be used to maintain situational awareness; and
  - Components of the EMT may be embedded within the FERP's DG Emergency Management Committee (DG EMC).

#### De-escalation

Several de-escalating factors will need to be considered including whether a cyber security incident is determined to be less severe than originally determined, or if the threat is reduced or vulnerability mitigated.

The decision to de-escalate from one level to the next is made by the ECT co-chairs for level 2 and based on input from ECT stakeholders.  For level 3 events, decision to de-escalate is made by recommendation of the ECT co-chairs and on direction from the EMT. However, the decision to de-escalate level 4 cyber security incidents will be made in consultation with PS-GOC.

Depending on the nature of the event, the Event Impact Assessment matrix outlined in Appendix D may need to be re-evaluated in order to accurately assess the response level required. For cyber threat and vulnerability events, de-escalation will be triggered based on a decrease in exposure to injury (for example, less likelihood of occurrence, decreased exploitability or exposure of vulnerable systems, increased effectiveness of security controls). For confirmed cyber security incidents, de-escalation will be triggered based on a decrease in severity or scope of the injury.

## 4. Reporting and Information Sharing

GC stakeholders and decision makers need to be informed of, and to understand the cyber security incident from a holistic viewpoint to inform decision-making.

### 4.1 Reporting Events to the GC

It is highly recommended and expected that all cyber security incidents that GC stakeholders become aware of, especially those that could negatively affect the national interest, be reported to the Cyber Centre. Through the Cyber Centre, the GC is able to offer advice and guidance, including technical assistance to the affected entities, on detection, assessment, mitigation, and recovery. However, as per the *CSE Act*, the Cyber Centre may not be able to respond in the same way to entities that are covered by the FCIRP but that have not been designated as a system of importance by the Minister of National Defence. This designation affects the Cyber Centre's available response options.

If a cyber security incident has occurred, in addition to reporting to the Cyber Centre, non-GC organizations are, and should be, encouraged to report directly to the RCMP, CSIS, and/or local law enforcement. The RCMP and/or local law enforcement will work with affected entities to begin the criminal investigation process and will engage provincial or national policing resources, if a cybercrime is suspected. Although not every complaint will result in an active investigation, the data will contribute to law enforcement's efforts to disrupt criminal activities and dismantle cybercriminal infrastructure. Material privacy breaches should be reported to the Office of the Privacy Commissioner or the provincial or territorial privacy commissioner, depending on the privacy legislation that applies to the organization.

### 4.2 Reporting Examples

The following examples, while not a complete list, can be used as a guide for types of events that could trigger activation of the FCIRP. :

- data breaches or compromise or corruption of information that affects or could affect Canadians' privacy;
- malware on a network that has the potential to cause a disruption to a vital service to Canadians;
- denial-of-service activities that have the potential to cause a disruption to a vital service to Canadians; or
- ransomware attempts that have the potential to cause a disruption to a service to Canadians.
- Significant event that may affect, or has the potential to affect, multiple departments, and where the safety and/or security of Government of Canada (GC) employees may be at risk (e.g., single point of failure of non-GC cyber systems that may impact delivery of trusted GC services to Canadians and/or disruption of critical services).

Non-GC stakeholders should be reminded that if in doubt, it is better to over-report than under-report.

### 4.3 Internal GC Information Sharing

At the GC-wide level, reporting will be handled as follows:

- **The Cyber Centre**, in line with existing procedures, will coordinate messaging to the operational (IT Security) community and disseminate technical information products (Cyber Flashes, Advisories, Alerts), including FCIRP response level status and situation reports to implicated stakeholders throughout the FCIRP process (all events).
- **ECT Co-Chairs** (PS-NCSD and the Cyber Centre) will ensure common, regular updates are provided to EMT committees throughout level 3 and 4 events; and
- as described in the FERP, **PS-GOC** will disseminate FERP governance updates and situational awareness products and briefings as required throughout the cyber security incidents affecting non-GC cyber systems management process for level 4 events.

A graph of the information-sharing flow can be found in Appendix F. Note that information-sharing at the ECT level will inform information-sharing at the EMT level.

In cases where entities are voluntarily working in coordination with the GC, information shared with the GC may be sensitive to the operation and reputation of the entity. The Cyber Centre will obtain the consent of the impacted entity prior to sharing information with other GC departments. As such, all GC stakeholders will pay due regard in the handling of potentially sensitive third-party information. The default for transmitting such information within the GC will be, at minimum, through encrypted technology. More secure means of communication are available if needed.

In cases where GC departments or agencies enter into NDAs with affected entities covered by the FCIRP, such agreements should accommodate necessary information sharing between GC departments and agencies responsible for carrying out specific core responsibilities of the FCIRP.

## 5. External Communications

During an FCIRP cyber security incident, PS-Comms is designated as responsible for coordinating the GC communications approach. PS-Comms, in close partnership with CSE-Comms and PCO-SC, will coordinate the development of communications products with appropriate stakeholders, including with the LFDA representing the affected sector.

PS-Comms will respond/coordinate the response to media requests related to the overall posture or response of the GC, while CSE-Comms will retain their lead role of speaking to technical issues and cyber security advice and guidance.

To facilitate coordination within the communications community, PS-Comms will hold regular stakeholder meetings during level 2, 3, and 4 incidents.

- **PS-Comms**, in close collaboration with **CSE-Comms**, will act as the communications lead for the following:
  - media requests; and
  - the development of a communications strategy and/or media relations protocol. Further details can be found in Appendix C.
- **LFDAs** will develop their own stakeholder, client and public communications products. This will be done in consultation with PS-Comms, CSE-Comms and PCO-SC.
- **GAC**, when appropriate, will be responsible for coordinating and communicating with international partners and multilateral organizations at a state-to-state level on matters pertaining to cybercrime and malicious cyber security incidents taking place in Canada.[Footnote 6](#fn6)

## 6. Management Process for Cyber Security Incidents that Affect both GC and non-GC Cyber Systems

This section of the plan outlines the management process for cyber security incidents that affect both GC and non-GC cyber systems. Specifically, it will examine areas where the management process will differ from the process overview as outlined in section 3.1, governance as outlined in section 3.4, internal GC information sharing process in section 4.3, and external communications process as outlined in section 5. The remaining sections in this document remain relevant in the event that the FCIRP and GC CSEMP are activated concurrently, measured by a clear and material effect on both GC and non-GC systems. If there is a clear conflict that arises between the FCIRP and GC CSEMP, the GC CSEMP shall prevail.

### 6.1 Process overview

Similar to the FCIRP management process, cyber security incidents that affect both non-GC and GC cyber systems have four phases. A graphic summarizing these phases can be found at Appendix C.

#### Phase 1: Preparation

The Preparation phase involves general readiness activities to ensure that the GC is ready to respond to a broad range of cyber security incidents across Canada. This phase remains as described in section 3.1.

#### Phase 2: Notification, Detection, and Assessment

The Notification, Detection and Assessment Phase involves the discovery of a cyber security incident. Cyber security incidents that affect both non-GC and GC cyber systems will be brought to the attention of the Cyber Centre. The Cyber Centre would then convene a meeting with     PS-NCSD and TBS to discuss possible FCIRP and GC CSEMP activation and determine the appropriate response level.

In this phase:

- **FCIRP stakeholders** will monitor their respective information sources for precursors of emerging cyber security incidents or events, or indicators of confirmed cyber security incidents, and **immediately notify the Cyber Centre** of any cyber security incidents that may affect or have detrimental effects on non-GC and GC cyber systems;
- **The Cyber Centre**, **PS-NCSD, and TBS** will then determine the appropriate FCIRP and GC CSEMP response level (as outlined in section 3.3 and Appendix D of this document), based on an analysis of available information; and
- **The Cyber Centre, PS-NCSD and TBS**, as tripartite co-chairs, will call a meeting with the appropriate governance bodies (as outlined in section 6.2), and provide an initial and ongoing assessment of the situation to the applicable governance bodies, in accordance with the response level. Depending on the nature of the cyber security incident and the computer system most affected, TBS or PS-NCSD may play more of a leadership role than the other. For example, if the cyber security incident affects mostly non-GC cyber systems, PS-NCSD will take more of a leadership role in partnership with the Cyber Centre. If the cyber security incident or event affects mostly GC cyber systems, TBS will take more of a leadership role in partnership with the Cyber Centre.

#### Phase 3: Mitigation, Support, and Investigation

The Mitigation, Support and Investigation Phase will require a varying degree of GC involvement, based on the established FCIRP and GC CSEMP response level.

In this phase:

- **The Cyber Centre, PS-NCSD, and TBS,** will ensure relevant information is shared within the governance bodies (as outlined in section 6.2) and across GC stakeholders to maintain situational awareness and support decision makers;
- **TBS** will, in line with existing procedures, coordinate messaging to the **Chief Information Officer** (CIO), **Chief Security Officer** (CSO), and **Designated Official for Cyber security** (DOCS) community and disseminate updates regarding affected systems as required throughout all cyber security incidents affecting non-GC and GC cyber systems;
- **The Cyber Center**, as Canada's technical and operational authority for cyber security, will perform operational coordination. This includes issuing advice and guidance, including technical assistance, to GC and non-GC stakeholders as required on measures to mitigate or contain impact to systems, as well as tracking and reporting these measures;
- **PS-GOC**, for level 4 events, will perform strategic coordination, as described in the FERP; and
- **The RCMP** will lead on the coordination of law enforcement investigations as appropriate.

#### Phase 4: Post-Event Activity

The Post-Event Activity phase is vital for continuous improvement of the overall GC cyber security incident management process for situations that affect both non-GC and GC cyber systems and, as such, feeds back into the preparation phase to complete the life cycle. This phase consists of post-event analysis, preparing and reviewing event lessons learned, and recommending changes to processes or procedures in order to continually mature the GC's cyber security event response.

In this phase:

- **The Cyber Centre** will collate all findings and produce a post-event report, including a timeline of events, as well as any recommended actions for GC stakeholders;
- **PS-NCSD and TBS** will produce a strategic lessons-learned report, including an action plan for implementing/addressing any associated recommendations/findings. The lead on this report and accompanying action plan will be determined by which cyber system was affected the most. For example, if the cyber security incident or event affected mostly non-GC cyber systems, PS-NCSD will lead. If the cyber security incident or event affected mostly GC cyber systems, TBS will lead;
- **PS-GOC** will produce a lessons-learned report and action plan on behalf of the GC and monitor the implementation of the recommendations for level 4 events only as outlined in section 3.3; and
- **All other FCIRP stakeholders** will support the development of these reports and assist with the implementation of related action items under their particular areas of responsibility.

### 6.2 Governance

When the FCIRP and the GC CSEMP are activated concurrently, the governance structure described in this section will leverage governance bodies that will manage the coordination and sharing of information regarding the cyber security incident: the ECT (level 2 events and above); the EMT committees (level 3 and 4 events); and the FERP's governance structure (level 4 events). A diagram outlining the flow of information can be found in Appendix G.

#### Event Coordination Team

Similar to the ECTs that are stood up during FCIRP or GC CSEMP activation, the ECT during an FCIRP and a GC CSEMP event is a group of working/Director-level stakeholders that is activated during level 2 events and above. However, in the case of concurrent FCIRP and GC CSEMP activation, the ECT becomes a tripartite committee co-chaired at the Director-level by PS-NCSD, TBS, and the Cyber Centre.

The ECT has core stakeholder representation with additional representation from SSC and, as required, secondary stakeholder representation as listed in section 3.2. The LFDA who represents the affected sector may also be invited to participate in the ECT (as listed in Appendix B). At level 2, ECT members will formally convene in person or virtually to coordinate and share information on the cyber security incident in question. For level 2 and 3 events, the ECT will ensure situational awareness is maintained among EMT members and may receive strategic direction from the EMT as required.

During level 4 events, the ECT continues to meet and co-chairs will ensure that subject matter expert are readily available to the PS-GOC to provide advice and ensure that situational awareness is maintained.

#### Executive Management Team

Unlike the three separate EMT committees that can be activated during an FCIRP event, the EMT during an FCIRP and a GC CSEMP event is a group of Director/DG-level stakeholders that is activated during level 3 events or above. In the case of concurrent FCIRP and GC CSEMP activation, the EMT becomes one tripartite committee chaired at the DG-level by the Cyber Centre, TBS, and PS-NCSD. The EMT co-chairs may recommend the invocation of ad hoc committees at the ADM and DM level, depending on the nature of the cyber security incident in question. These ad hoc committees at the ADM and DM level would provide executive direction and guidance to the EMT. Similar to the ECT, PS-NCSD or TBS may play more of a leadership role depending on the computer systems most affected.

The EMT has core stakeholder representation with additional representation from SSC and, as required, secondary stakeholder representation as listed in section 3.2. The LFDA who represents the affected sector may also be invited to participate on the EMT. However, any final decisions around participation will be determined by the chairs, who may limit invitations to ensure optimal operation of the committee. At level 3, EMT members will formally convene in person or virtually on an ad-hoc basis to share information and ensure situational awareness is maintained among relevant senior officials.

During level 4 events, the EMT may be integrated within the FERP's DG EMC.

### 6.3 Internal GC Information Sharing

At the GC-wide level, reporting during FCIRP and GC CSEMP activation will be handled as follows:

- **ECT co-chairs** will ensure common, regular updates are provided to the EMT committee throughout level 3 events or above;
- as described in the FERP, **PS-GOC** will disseminate FERP governance updates and situational awareness products and briefings as required throughout the combined FCIRP/GC CSEMP process for level 4 events; and
- **The Cyber Centre**, in line with existing procedures, will coordinate messaging to the operational (IT Security) community and disseminate technical information products, including FCIRP and GC CSEMP response level status and situation reports to implicated stakeholders as required throughout all cyber security incidents affecting non-GC and GC cyber systems; and
- **TBS**, in line with existing procedures, will coordinate messaging to the Chief Information Officer (CIO), Chief Security Officer (CSO), and Designated Official for Cyber security (DOCS) community and disseminate updates regarding affected systems as required throughout all cyber security incidents affecting non-GC and GC cyber systems.

A graph of the information-sharing flow can be found in Appendix G. Note that information-sharing at the ECT level will continue in parallel to information-sharing among the EMT level.

### 6.4 External Communications

TBS-SCMA, PS-Comms and CSE Comms, will coordinate the development of stakeholder, client and public communications products with Comms teams from core and secondary stakeholders as listed in section 3.2, in close collaboration with PCO-SC. For level 2 and 3 combined FCIRP/GC CSEMP incidents, TBS-SCMA will act as the GC communications lead. For level 4 cyber security incidents, PS-Comms will coordinate the GC communications response, as outlined in the FERP. To facilitate coordination within the Comms community, the GC Communications lead may hold regular meetings with stakeholders.

- The GC Communications lead, **TBS-SCMA**, in close collaboration with **CSE Comms, PS Comms, and PCO-SC**, will act as the communications lead during level 2 and 3 cyber security incidents for the following:
  - media requests;
  - the development of a communications strategy; and
  - publication of external communications materials (required during the cyber security event management life cycle, in close collaboration with CSE-Comms and PCO-SC for all events that require external communications or coordinated messaging.
- **PS-Comms** will coordinate the communications response during level 4 events, as outlined in the FERP. **LFDAs for the affected sectors,** as listed in Appendix B, will develop their own stakeholder, client and public communications products when necessary, and during level 2 events and above, in consultation with the designated GC communications lead and PCO-SC as required.
- **GAC**, when appropriate, will be responsible for coordinating and communicating with international partners and multilateral organizations at a state-to-state level on matters pertaining to cybercrime and malicious cyber security incidents taking place in Canada.

## Appendix A: Glossary of acronyms and abbreviations

ADM
:   Assistant Deputy Minister

CCCS
:   Canadian Centre for Cyber Security, part of the Communications Security Establishment

CCNSS
:   Canadian Committee on National Security Systems

CID
:   Critical Infrastructure Directorate

CIO
:   Chief Information Officer

Comms
:   Communications

CSE
:   Communications Security Establishment

CSEMP
:   Cyber Security Event Management Plan

CSIS
:   Canadian Security Intelligence Service

CSO
:   Chief Security Officer

DG
:   Director General

DG ERC
:   Director General Event Response Committee

DND-CAF
:   Department of National Defence/Canadian Armed Forces

DOCS
:   Designated Official for Cyber security

ECT
:   Event Coordination Team

EMT
:   Executive Management Team

ERC
:   Event Response Committee

FERP
:   Federal Emergency Response Plan

GC
:   Government of Canada

GAC
:   Global Affairs Canada

GOC
:   Government Operations Centre

IMOC
:   Incident Management and Operational Coordination, part of the Canadian Centre for Cyber Security

IT
:   Information technology

ITSec
:   Information technology security

LFDA
:   Lead Federal Departments and Agencies

NCSD
:   National Cyber Security Directorate

NSDS
:   Networks, Security and Digital Services, part of Shared Services Canada

NSS
:   National Security Systems

PCO
:   Privy Council Office

PS
:   Public Safety Canada

RCMP
:   Royal Canadian Mounted Police

RFA
:   Request for Action

S&I
:   Security and intelligence

SC
:   Strategic communications

SSC
:   Shared Services Canada

TBS
:   Treasury Board of Canada Secretariat

## Appendix B: Roles and Responsibilities

This appendix describes roles and responsibilities of FCIRP stakeholders. Roles and responsibilities will vary depending on the type of cyber security incident or event and its response level. A stakeholder may be called on to take a larger role, not described in this appendix, during an FCIRP cyber security incident depending on the sector affected and the response level. All stakeholders have a responsibility to bring cyber security incidents to the attention of the Cyber Centre for possible FCIRP activation.

It is possible that a cyber security incident could impact both GC systems as well as non-GC systems, resulting in the activation of the GC CSEMP and the FCIRP concurrently. The roles and responsibilities described in this appendix are in addition to those described in the associated appendix of the GC CSEMP. Should the GC CSEMP and FCIRP be activated together, departments and agencies will fulfil responsibilities described in both plans.

### 1. Core Stakeholders

The following is a list of core stakeholders in the FCIRP cyber security incident management process that will be engaged in all incidents that meet the appropriate FCIRP activation criteria. The degree of involvement from each stakeholder will vary based on the impact, severity, and sector affected by the incident or event.

#### Public Safety Canada

Under the *Emergency Management Act*, the Minister of Public Safety is the primary federal Minister responsible for coordinating the GC's response to an emergency. PS executes these responsibilities on behalf of the Minister. With regards to the management of cyber security incidents or events affecting non-GC cyber systems, PS-NCSD and PS-Comms each play a role.

In the context of this plan, PS-NCSD's roles include:

- acting as the co‑chair and secretariat for all FCIRP governance teams alongside the Cyber Centre.
- acting as a tripartite co-chair and secretariat for all FCIRP and GC CSEMP governance teams alongside The Cyber Centre and TBS for cyber security incidents affecting both GC and non-GC systems designated as level 2, 3, and 4. Depending on the nature of the cyber security incident and the computer systems most affected, TBS or PS-NCSD may play more of a leadership role than the other.;
- ensuring strategic coordination and information sharing to facilitate the GC response, and ministerial awareness of cyber security incidents designated as level 2, 3, and 4;
- establishing, maintaining and testing the FCIRP and related procedures;
- remaining engaged with the FERP event teams leading up to and during level 4 cyber security incidents;
- ensuring that PS-Comms is provided with timely information required to develop communications products and ensure a coordinated and aligned approach is in place for public communications amongst stakeholders; and
- analyzing post-event reports from The Cyber Centre and conducting lessons-learned exercises (when warranted) to drive improvements in cyber security policy.

In the context of this plan, PS-Comms' role includes:

- acting as the designated party responsible for speaking about GC action for cyber security incidents affecting non-GC cyber systems (excluding technical advice and guidance, which CSE is responsible for);
- developing external communications materials related to all phases of cyber security incident management, in collaboration with CSE-Comms and PCO-SC, and in consultation with communications teams from implicated FCIRP stakeholders;
- determining the necessity and timing of public statements (proactive and reactive);
- reviewing all communications plans (internal, stakeholder, client and public), in collaboration with affected organizations and PCO-SC; and
- coordinating the comms response for level 4 events affecting both non-GC and GC cyber systems, as outlined in the FERP.

#### Communications Security Establishment – The Cyber Centre

The Cyber Centre, which is housed at CSE, is Canada's technical authority for cyber security and information assurance, responsible for preventing, mitigating, preparing for, responding to and recovering from cyber security incidents for entities designed as systems of importance to the Government of Canada. The Cyber Centre also acts as the lead GC agency responsible for victim engagement to administer victim notifications, advice and guidance. The Cyber Centre and CSE-Comms each play a role in responding to cyber security incidents or events affecting non-GC cyber systems.

In the context of this plan, the Cyber Centre's roles include:

- acting as the co‑chair and secretariat for all FCIRP governance teams alongside PS-NCSD (including escalation and de‑escalation decisions);
- acting as a tripartite co-chair and secretariat for all FCIRP and GC CSEMP governance teams alongside PS-NCSD and TBS for cyber security incidents affecting both GC and non-GC systems designated as level 2, 3, and 4;
- acting as the central cyber operational contact in the GC, both for distributing technical information products and for collecting event-related reports from GC and non-GC organizations for cyber security incidents designated as level 2, 3, and 4;
- ensuring operational coordination of the GC response to cyber security incidents, including:
  - working with affected entities to monitor technical information sources of cyber threat or vulnerability events or indicators of potential or confirmed cyber security incidents;
  - collating and tracking affected organizations(s) reports on and responses to cyber security incidents or events; and
  - coordinating prevention, mitigation and recovery efforts, including providing timely situational awareness updates to other FCIRP stakeholders as required.
- producing post-event reports (based on departments' analyses and reports on lessons learned), and sharing them with PS-NCSD and other relevant organizations, as required (for example, PCO); and

CSE's Cyber Centre may offer advice, guidance, and services to support entities under the FCIRP response to cyber security incidents.

In the context of this plan, CSE-Comms roles include:

- Lead for communications related to technical aspects of a cyber security incident; and
- coordinating efforts with PS-Comms to produce and finalize all federal public communications-related efforts during a cyber security incident.

#### Royal Canadian Mounted Police

The RCMP will lead on assessing and coordinating investigations for cyber security incidents involving the compromise of a cyber system. The RCMP or local law enforcement are responsible for criminal investigations.

In the context of this plan, the RCMP's roles include:

- leading the criminal investigation on cyber security when a cyber security incident falls under the Federal Policing mandate (including criminal investigations involving terrorist activity);
- participating on FCIRP governance teams in an advice and guidance capacity, when warranted by a particular cyber security event or threat event;
- Participating in lessons learned activity post-events;
- Liaising with domestic and international law enforcement partners to coordinate and assist with cybercrime and fraud investigations linked to Canada; and,
- De-conflicting with CSIS for suspected state sponsored activity, such as an APT, to determine the lead investigative agency.

#### Canadian Security Intelligence Service

CSIS is the primary investigative agency for all cyber security incidents dealing with actual or suspected cyber threat activity against Canada's national security.

In the context of this plan, CSIS's roles include:

- leading the investigation on cyber security incidents that constitute a threat to Canada's security, as defined by the *CSIS Act* (including espionage, sabotage, foreign influence activity, and terrorism);
- providing advice to the Government of Canada on these threats via intelligence products and briefings;
- participating on FCIRP governance teams in an advice and guidance capacity, as well as to inform the decision as to whether our involvement or a CSIS investigation is warranted by a particular cyber security incident; and
- participating in lessons learned activity post-events.

#### Privy Council Office

As a central agency and the hub of non-partisan advice to the Prime Minister and Cabinet, PCO helps to clearly articulate and implement the GC's policy agenda and to coordinate timely responses to issues facing Canada that are of national, intergovernmental and international importance. PCO may take a larger role in coordinating the GC response and Communications depending on the type of incident event, its response level, and resources available.

In the context of this plan, PCO-S&I's roles include:

- supporting the GC decision-making process by ensuring that senior officials are apprised in a timely manner of cyber security incidents affecting non-GC cyber systems;
- participating on FCIRP governance teams in an advice and guidance capacity. Of note, depending on the nature of the incident, PCO-S&I may play a more active role in all levels of the governance structures;
- engaging with other PCO stakeholders such as PCO Inter-Governmental Affairs (IGA) and the Minister of Emergency Preparedness's staff. For some incidents, it may be appropriate to have additional PCO representation as part of the governance structure.

In the context of this plan, PCO-SC's roles include:

- providing communications advice to Cabinet and senior officials of PCO, and collaborating with PS-Comms and CSE-Comms on government-wide communications, including crisis management, during a cyber security incident.

#### Department of National Defence/Canadian Armed Forces

DND/CAF is the primary department responsible for addressing actual or suspected cyber threats against DND-CAF systems and networks.

In the context of this plan, DND/CAF's roles include:

- leading the investigation on any cyber security activities directed against DND-CAF systems and networks, including information technology, operational technology, and platform technology;
- supporting investigations on any cyber security activities directed against the military manufacturing supply chain;
- providing additional support and assistance to other government departments, including advice on defensive foreign policy and coordination with international allies, if requested through a Request for Federal Assistance (RFA);
- participating on FCIRP governance teams in an advice and guidance capacity; and
- participating in lessons learned activity post-events.

#### Global Affairs Canada

GAC plays a core role in exercising Canada's leadership in protecting and strengthening the rules-based international order and advancing Canadian interests and values related to human rights, freedoms and inclusion, democracy, peace and stabilization programming, and security cooperation. Working closely with Canada's bilateral, multilateral, and intergovernmental partners, GAC guides Canada's policy and programming responses to pressing and emerging global security issues such as foreign interference, cyber security, and international crime.

In the context of this plan, GAC's roles include:

- Coordinating and communicating with States, international partners, and multilateral organizations on matters pertaining to cybercrime and malicious cyber security incidents taking place in Canada;
- Providing foreign policy advice to the GC and international coordination in the context of cyber crimes or malicious cyber events that have international ramifications;
- Leading GC coordination efforts in developing public attribution statements of malicious cyber activity to foreign state actors or their proxies; and
- Developing and using national deterrence and response policies and capabilities to protect Canada and its interests.

### 2. Secondary stakeholders

#### Shared Services Canada

SSC is responsible for the GC network infrastructure, delivering programs and services to Canadians, and for managing the network perimeter including gateways and secret infrastructure.

If a cyber security incident occurs, SSC can provide expertise and coordinate with partners to determine whether any infrastructure it manages has to be shut down or be isolated from the network and will respond to recommendations from the Cyber Centre and direction from TBS.

SSC also develops, provides and operates capabilities and tools for preventive defence of network infrastructure for partners.

In the context of this plan, SSC is responsible for:

- assessing government‑wide program and service impact of cyber threats, vulnerabilities and security incidents to support government‑wide reporting, to be submitted to the Cyber Centre and TBS in the event of an FCIRP and GC CSEMP cyber security incident;
- providing reporting and other information products to key stakeholders;
- responding to the Cyber Centre and TBS recommendations, and ensuring that updates and mitigating measures are applied in a timely manner;
- implementing prevention, mitigation and recovery efforts, including timely situational awareness updates to stakeholders;
- supporting the identification, risk assessment, mitigation, recovery and post‑analysis of cyber security incidents in partnership with stakeholders;
- producing post‑event reports, including timeline of events and root cause analysis and submitting to the Cyber Centre, TBS and other relevant organizations, as required (for example, PCO); and
- extend or complement the Cyber Centre's role in non-GC Cyber response activities, as needed, by mobilizing SSC's broad IT infrastructure operations subject matter experts.

#### Treasury Board of Canada Secretariat

TBS provides strategic oversight and direction in the GC cyber security event management process, ensuring that events affecting GC cyber systems in the context of the GC CSEMP are effectively coordinated to support decision‑making and minimize potential impacts and losses to the GC.

In the context of this plan, TBS's roles include:

- acting as a tripartite co-chair for all FCIRP and GC CSEMP governance teams as required. Depending on the nature of the cyber security incident and the computer systems most affected, TBS or PS-NCSD may play more of a leadership role than the other;
- defining cyber security requirements to ensure that the GC and departmental information and data, applications, systems, and networks are secure, reliable, and trusted, as per section 4.4.1.8 of the Policy on Service and Digital (PSD);
- receiving and reviewing material privacy breach reports and advising institutions on the management of multi-institutional privacy breaches that require a coordinated response, as per the *Policy on Privacy Protection*;  and
- participating in lessons learned activity post-events.

#### Government Operations Centre

The PS-GOC, on behalf of the GC, leads and supports response coordination of any type of event affecting the national interest. It provides 24/7 monitoring and reporting, national-level situational awareness, warning products and integrated risk assessments, as well as national-level planning and whole-of-government response management. During periods of heightened response, the PS-GOC is augmented by staff from other organizations (both government and non-government) that physically work in the PS-GOC or connect to it virtually.

In the context of this plan, the PS-GOC's roles include:

- monitoring level 2 and 3 cyber security incidents for potential escalation, which includes:
  - providing warning and situational awareness products to operations centres across government;
  - conducting risk assessments and planning;
  - briefing the FERP governance; and
- coordinating the overall GC response during level 4 events, in accordance with the FERP.

#### Lead Federal Departments and Agencies for Critical Infrastructure Sectors

LFDAs are GC departments and agencies that lead each critical infrastructure (CI) sector. They are responsible for advancing collaboration between federal, provincial, and territorial governments, national associations, and critical infrastructure owners and operators. Each lead department is responsible for facilitating the development of sector networks to suit the need of their stakeholders which includes the identification of issues of national, regional, or sectoral concern. They also develop tools and best practices for strengthening the resiliency of critical infrastructure across the full spectrum of prevention, mitigation, preparedness, response, and recovery. In the case of FCIRP activation, LFDAs would likely play more of a leadership role as the main point of contact for the affected sector, and would be invited to participate on the FCIRP governance bodies.

In the case of a non-LFDA department or agency receiving word from an affected non-CI entity that a cyber security incident has taken place, that non-LFDA department or agency will be responsible for reporting and liaising with the affected entity throughout the management cycle of the incident.

The relationship between sectors and LFDAs is as follows:

| Sector | Lead Federal Departments and Agencies |
| Energy and Utilities | Natural Resources Canada |
| Information and communication technology | Innovation, Science and Economic Development Canada |
| Finance | Finance Canada |
| Health | Public Health Agency of Canada |
| Food | Agriculture and Agri-Food Canada |
| Water | Environment and Climate Change Canada |
| Transportation | Transport Canada |
| Safety | Public Safety Canada |
| Government | Public Safety Canada |
| Manufacturing | Innovation, Science and Economic Development Canada, Department of National Defence |

#### Other GC Stakeholders

Other GC departments and agencies play a key role in cyber security event management. Detailed departmental roles and responsibilities related to security event management can be found in departmental governance, plans and procedures.

In the context of this plan, other GC departments and agencies' roles may include:

- reporting cyber security incidents to the Cyber Centre for possible FCIRP activation;
- monitoring the Cyber Centre's technical information products;
- notifying appropriate law enforcement or national security authorities when a cyber event affects external stakeholders;
- participating on FCIRP governance teams, when requested;
- developing and disseminating applicable stakeholder and client management communications products (in consultation with PS-Comms, CSE-Comms and PCO-SC as required); and
- encouraging that management and reporting requirements related to cyber security incidents are clearly stipulated in contracts, memoranda of understanding or other formal arrangements with external partners (for example, private sector suppliers and other levels of government) and that these address the requirements established in applicable GC and departmental policy instruments including, but not limited to, this plan.

Departments and agencies providing services to non-GC organizations are responsible for establishing mechanisms to inform service recipients of cyber security incidents that impact their systems or information.

## Appendix C: GC Response Levels

**Figure 2: GC Response Levels**

Image description

Figure 2 represents the four response levels that govern the Government of Canada's cyber security event management activities and dictate the necessity and degree of enterprise response required.

- At Level 1, the FCIRP stands at day-to-day operations. The FCIRP stakeholders hold standard monitoring activities and coordination.
- At Level 2, the cyber incident requires heightened attention from the FCIRP stakeholders. This will lead to the coordination of activities through the FCIRP.
- At Level 3, the cyber incident requires immediate focus and attention from the FCIRP stakeholders. This will lead to the coordination of activities through the FCIRP.
- At Level 4, the cyber incident has become a severe or catastrophic event. The FCIRP will transition to the Federal Emergency Response Plan (FERP) governance structure.

## Appendix D: Event Impact Assessment

The purpose of this Appendix is to outline a high‑level process that could be used to assess the impact related to a cyber security event. The following process can be adopted and leveraged as required to inform their incident response plan. This is a two-step process:

- **Step 1: Injury test:** Assessment of impact for all cyber security incidents and events (threats, vulnerabilities and confirmed incidents) begins with an injury test to measure the degree of injury that could reasonably be expected to occur due to a compromise
- **Step 2: Risk Assessment:** For cyber threat and vulnerability events, determine the probability of injury occurrence to obtain a more accurate representation of potential departmental impact

#### Step 1: Injury test – for all cyber security incidents and events

The injury test, performed using the table below, is based on severity and scope of the injury that could reasonably be expected to occur.

##### Severity

The severity of the injury refers to the level of harm, damage or loss (for example, from physical injury to loss of life, from minor financial losses to loss of financial viability, from minor inconvenience to significant hardship). The severity of the injury may be characterized as limited, serious or severe, based on an assessment of the following types of injury:

- harm to the health and safety of individuals
- financial losses or economic hardship
- impacts to government programs and services
- loss of civil order or national sovereignty
- damage to reputations or relationships

Other factors may also be considered.

##### Scope

The scope of injury refers to the number of people, organizations, facilities or systems impacted, the geographical area affected (for example, localized or widespread), or duration of the injury (for example, short term or long term). The scope of injury can be characterized as:

- **Wide:** widespread; national or international; multiple countries or jurisdictions; major government programs or sectors
- **Medium:** jurisdiction, business sector, government program; group or community
- **Narrow:** individual, small business

##### Injury test

The impact of the incident is determined by the scope and the severity:

| Severity | Scope | | |
| --- | --- | --- | --- |
| Narrow | Medium | Wide |
| **Severe** | Medium | High | Very high |
| **Serious** | Low | Medium | High |
| **Limited** | Low | Low | Medium |

The following table can be consulted to analyze potential expected results of a compromise and validate the outcome of the initial injury test. Once confirmed, this value can be entered in the incident report and submitted to the Cyber Centre.

Expected results of compromise

| Impact | Result of compromise |
| **Very high** | - Widespread loss of life - Major long‑term damage to the Canadian economy - Severe impediment to national security (for example, compromising capabilities of Canadian Armed Forces or national intelligence operations) - Severe damage to diplomatic or international relations - Long‑term loss of public confidence in the GC that disrupts the stability of government |
| **High** | - Severe injury or loss of life to a group of individuals, or widespread serious injury - Serious financial loss that impedes the Canadian economy or reduces international competitiveness - Serious impediment to one or more critical services or impediment to national security - Serious damage to international relations that could result in a formal protest or sanction - Long‑term loss of public confidence in the GC that disrupts a priority objective of the government |
| **Medium** | - Threat to the life or safety of an individual, or serious injury to a group of individuals - Financial loss that affects performance across a sector of the economy or affects the well‑being of a large number of Canadians - Damage to federal‑provincial relations - Serious loss of public trust or confidence in the GC or embarrassment to the GC |
| **Low** | - Physical or psychological harm to an individual - Financial stress or hardship to an individual - Harm to the reputation of an individual or business - Minor loss of public trust or confidence in the GC |

#### Step 2: Risk assessment – for cyber threat and vulnerability events only

Unlike cyber security incidents, where injury has been realized, injury is still in a potential state for cyber threat and vulnerability events. In order to establish an accurate potential impact level, a risk assessment is expected to be conducted (using the Risk Assessment table below) to determine the probability of occurrence for the injury.

Using the results of the injury test performed in Step 1, a risk‑modified departmental impact level is determined based on factors such as intelligence indicators (likelihood of compromise), exploitability, exposure of affected information systems, and implementation of compensating controls.

##### Low exposure:

- Low likelihood that threat will target Canada's national security
- Vulnerability very difficult to exploit
- Vulnerable systems are not directly exposed (for example, stand‑alone systems)
- Existing security controls effectively counter threat or vulnerability

##### Medium exposure:

- Medium likelihood that threat will target Canada's national security
- Vulnerability exploitable with significant resources
- Vulnerable cyber systems are visible to one system only
- Existing security controls partially counter threat or vulnerability

##### High exposure:

- High likelihood that threat will target Canada's national security
- Vulnerability exploitable with moderate resources
- Vulnerable systems are visible to many cyber systems
- Existing security controls provide limited protection against threat or vulnerability

##### Very high exposure:

- Threat or compromise imminent
- Vulnerability easily exploitable with limited resources
- Vulnerable cyber systems are highly exposed
- Existing security controls do not provide protection against threat or vulnerability

The Risk modified impact level is determined by the impact level (as per the injury test in Step 1), and the exposure of the incident

| Impact Level | Exposure | | | |
| --- | --- | --- | --- | --- |
| Low | Medium | High | Very High |
| **Very high** | High | High | High | Very high |
| **High** | Medium | Medium | High | High |
| **Medium** | Low | Medium | Medium | Medium |
| **Low** | Low | Low | Low | Low |

This risk‑modified departmental impact level is to be reported to the Cyber Centre, when requested via a request for information, for consumption at the GC‑wide level.

Cyber threat or vulnerability events are to be classified as cyber security incidents as soon as injury is realized. When injury moves from a potential state to a realized state, the injury tests in this appendix will require re‑evaluation and resubmission to the Cyber Centre to determine whether changes to event response or further escalation are required.

## Appendix E: FCIRP Governance

**Figure 3: FCIRP Governance**

Image description

Figure 3 represents the FCIRP governance model. This figure identifies the required governance based on the response level identified in figure 2. It identifies the working level and senior management stakeholders required, differentiating between core stakeholders and specialized members who vary based on event type.

At Level 1, during day-to-day operations:

- The Cyber Centre receives the information about a cyber incident from all Government of Canada's stakeholders.
- The Cyber Centre then share the information with Public Safety – National Cyber Security Directorate and they both make the decision, at the Director-level, to raise the FCIRP to Level 2.

At Level 2, which requires heightened attention from the FCIRP stakeholders:

- The FCIRP co-chairs (Cyber Centre and Public Safety) stand up the Event Coordination Team, which includes the Canadian Security Intelligence Service (CSIS), The Department of National Defence/Canadian Armed Forces (DND-CAF), Global Affairs Canada (GAC), the Royal Canadian Mounted Police (RCMP), the Private Council Office (PCO), and any secondary FCIRP stakeholders invited to the meeting.
- The FCIRP co-chairs may decide to raise the FCIRP to Level 3. This decision is made at the Director-General (DG)-level.

At Level 3, which requires immediate focus and action by the FCIRP stakeholders:

- The FCIRP co-chairs (Cyber Centre and Public Safety) stand up the Executive Management Team.
- This is comprised of the Director General Cyber Ops and any secondary FCIRP stakeholders invited to the meeting.
- The Communication Security Establishment (CSE), who chairs the Director General Cyber Ops, may decide to move the FCIRP to an ad hoc meeting of the relevant members of the Assistant Deputy Minister Cyber Security (ADMCS) Community.
- Members from the Assistant Deputy Minister Cyber Security (ADMCS) Community may move the FCIRP to an ad hoc meeting of the relevant members of the Deputy Minister Cyber Security (DMCS) Community.
- The FCIRP co-chairs of the Executive Management Team (Cyber Centre and Public Safety) may raise the cyberincident to Level 4 of the FCIRP if it has become a severe or catastrophic event. They will then refer to the Federal Emergency Response Plan (FERP)'s governance.

## Appendix F: FCIRP Information Sharing Flow

**Figure 4: FCIRP Information Sharing Flow**

Image description

Figure 4 identifies the FCIRP information sharing flow separated by the different GC response levels outlined in figure 2. Figure 4 applies only to the first three levels of response and does not address information sharing at Level 4 (emergency or crisis response).

At Level 1, during day-to-day operations:

- A cyberincident can be brought to the attention of the Government of Canada through multiple sources, including but not limited to:

- Technical information sources
- Reports from the affected entity
- Law enforcement
- Media
- Federal Departments and Agencies, Provinces and Territories
- Other

- The Cyber Centre receives the information about a cyberincident.
- The Cyber Centre then share the information with Public Safety – National Cyber Security Directorate and they both make the decision to raise the FCIRP to Level 2.

At Level 2, which requires heightened attention from the FCIRP stakeholders:

- The FCIRP co-chairs (Cyber Centre and Public Safety) stand up the Event Coordination Team, which includes the Canadian Security Intelligence Service (CSIS), The Department of National Defence/Canadian Armed Forces (DND-CAF), Global Affairs Canada (GAC), the Royal Canadian Mounted Police (RCMP), the Private Council Office (PCO), and any secondary FCIRP stakeholders invited to the meeting.
- The information gathered from the FCRIP stakeholders will be distributed to the affected entity and Lead Federal Departments and Agencies (LFDAs).
- The public communications products will be coordinated and prepared by the Communications departments of Public Safety, the Communication Security Establishment (CSE), and other relevant departments and agencies.

At Level 3, which requires immediate focus and action by the FCIRP stakeholders:

- The FCIRP co-chairs (Cyber Centre and Public Safety) stand up the Executive Management Team. This is compromised of the Director General Cyber Ops and any secondary FCIRP stakeholders invited to the meeting.
- The FCIRP may move to an ad hoc meeting of the relevant members of the Assistant Deputy Minister Cyber Security (ADMCS) Community.
- The FCIRP may move to an ad hoc meeting of the relevant members of the Deputy Minister Cyber Security (DMCS) Community.
- The FCIRP co-chairs of the Executive Management Team (Cyber Centre and Public Safety) may raise the cyber incident to Level 4 of the FCIRP if it has become a severe or catastrophic event. They will then refer to the Federal Emergency Response Plan (FERP)'s governance.

## Appendix G: FCIRP and GC CSEMP Information Sharing Flow

**Figure 5: FCIRP and GC CSEMP Information Sharing Flow**

Image description

Figure 5 identifies the information sharing flow separated by the different GC response levels outlined in figure2 when the FCIRP and the GCCSEMP are concurrently activated. Figure 5 applies only to the first three levels of response and does not address information sharing at Level 4 (emergency or crisis response).

At Level 1, during day-to-day operations:

- A cyber incident can be brought to the attention of the Government of Canada through multiple sources, including but not limited to:

- Technical information sources
- Reports from the affected entity
- Law enforcement
- Media
- Federal Departments and Agencies, Provinces and Territories
- Other

- The Treasury Board Secretariat (TBS) receives the information about a cyber incident.
- The Treasury Board Secretariat then share the information with Cyber Centre and Public Safety – National Cyber Security Directorate and they all make the decision to raise the FCIRP to Level 2.

At Level 2, which requires heightened attention from the FCIRP stakeholders:

- The FCIRP co-chairs (Treasury Board Secretariat, Cyber Centre and Public Safety) stand up the Event Coordination Team, which includes the Canadian Security Intelligence Service (CSIS), The Department of National Defence/Canadian Armed Forces (DND-CAF), Global Affairs Canada (GAC), the Royal Canadian Mounted Police (RCMP), the Private Council Office (PCO), Shared Services Canada (SSC) and any secondary FCIRP stakeholders invited to the meeting.
- The information gathered from the FCRIP stakeholders will be distributed to the affected entity and Lead Federal Departments and Agencies (LFDAs).
- The public communications products will be coordinated and prepared by the Communications departments of the Treasury Board SecretariatPublic Safety, the Communication Security Establishment (CSE), and other relevant departments and agencies.

At Level 3, which requires immediate focus and action by the FCIRP stakeholders:

- The FCIRP co-chairs (Treasury Board Secretariat, Cyber Centre and Public Safety) stand up the Executive Management Team, which includes the Canadian Security Intelligence Service (CSIS), The Department of National Defence/Canadian Armed Forces (DND-CAF), Global Affairs Canada (GAC), the Royal Canadian Mounted Police (RCMP), the Private Council Office (PCO), Shared Services Canada (SSC) and any secondary FCIRP stakeholders invited to the meeting.
- The FCIRP may move to an ad hoc meeting of the relevant members of the Assistant Deputy Minister Cyber Security (ADMCS) Community.
- The FCIRP may move to an ad hoc meeting of the relevant members of the Deputy Minister Cyber Security (DMCS) Community.
- The FCIRP co-chairs of the Executive Management Team (Treasury Board Secretariat, Cyber Centre and Public Safety) may raise the cyber incident to Level 4 of the FCIRP if it has become a severe or catastrophic event. They will then refer to the Federal Emergency Response Plan (FERP)'s governance.

## Footnotes

Footnote 1
:   As per the *CSE Act*, CSE has been given Ministerial authority to respond to incidents impacting systems of importance to the GC as per SC2019, c 13, s 76. CSE's response to cyber security incidents affecting non-GC entities that are designated by the Minister have specific policies and procedures in place. However CSE's Cyber Centre may not be able to respond in the same way to entities that are covered by the FCIRP but that have not been designated as a system of importance by the Minister.

    [Return to first footnote 1 referrer](#fn1-1-rf)

Footnote 2
:   Every cyber security incident is a cyber security event, but not every cyber security event is a cyber security incident.

    [Return to first footnote 2 referrer](#fn2-1-rf)

Footnote 3
:   The GC CSEMP further defines a cyber threat as a threat actor, using the internet, who takes advantage of a known vulnerability in a product for the purposes of exploiting a network and the information the network carries.

    [Return to first footnote 3 referrer](#fn3-1-rf)

Footnote 4
:   Cyber incidents affecting GC cyber systems are currently covered by the GC CSEMP, and cyber incidents that have, or escalate to a point of having severe or catastrophic effects on GC and non-GC cyber systems are currently covered by the FERP.

    [Return to first footnote 4 referrer](#fn4-1-rf)

Footnote 5
:   DG Cyber Ops consists of the following departments: CSE (Chair); PS-NCSD; RCMP; CSIS; DND/CAF; GAC; and TBS. DMCS consists of the following departments: CSE; PS-NCSD; RCMP; CSIS; PCO; DND/CAF; the Department of Finance; GAC; Health Canada; Innovation, Science and Economic Development (ISED); Justice Canada; the Department of Natural Resources Canada (NRCAN); TBS; and Transport Canada (TC).

    [Return to first footnote 5 referrer](#fn5-1-rf)

Footnote 6
:   Other government departments may also engage with their international counterparts, in line with their departmental mandate, as required to facilitate operational information sharing.

    [Return to first footnote 6 referrer](#fn6-1-rf)

Footnote 7
:   Other government departments may also engage with their international counterparts, in line with their departmental mandate, as required to facilitate operational information sharing.

    [Return to first footnote 7 referrer](#fn7-1-rf)
