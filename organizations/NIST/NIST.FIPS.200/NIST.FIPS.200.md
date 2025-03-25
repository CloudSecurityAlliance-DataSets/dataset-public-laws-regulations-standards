**FEDERAL INFORMATION PROCESSING STANDARDS PUBLICATION** 

_______________________________________________________________

# **Minimum Security Requirements for Federal Information and Information Systems**

_______________________________________________________________

Computer Security Division Information Technology Laboratory National Institute of Standards and Technology Gaithersburg, MD 20899-8930

**March 2006**

![](_page_0_Picture_5.jpeg)

**U.S. DEPARTMENT OF COMMERCE** *Carlos M. Gutierrez, Secretary* 

**NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY** *William Jeffrey, Director*

#### **FOREWORD**

________________________________________________________________________________________________

The Federal Information Processing Standards (FIPS) Publication Series of the National Institute of Standards and Technology (NIST) is the official series of publications relating to standards and guidelines adopted and promulgated under the provisions of the Federal Information Security Management Act (FISMA) of 2002. Comments concerning FIPS publications are welcomed and should be addressed to the Director, Information Technology Laboratory, National Institute of Standards and Technology, 100 Bureau Drive, Stop 8900, Gaithersburg, MD 20899-8900.

-- CITA M. FURLANI, ACTING DIRECTOR INFORMATION TECHNOLOGY LABORATORY

#### **AUTHORITY**

________________________________________________________________________________________________

Federal Information Processing Standards Publications (FIPS PUBS) are issued by the National Institute of Standards and Technology after approval by the Secretary of Commerce pursuant to Section 5131 of the Information Technology Management Reform Act of 1996 (Public Law 104-106) and the Federal Information Security Management Act of 2002 (Public Law 107-347).

#### **Federal Information Processing Standards 200** *March 9, 2006*

________________________________________________________________________________________________

#### **Announcing the Standard for Minimum Security Requirements for Federal Information and Information Systems**

Federal Information Processing Standards Publications (FIPS PUBS) are issued by the National Institute of Standards and Technology (NIST) after approval by the Secretary of Commerce pursuant to the Federal Information Security Management Act (FISMA) of 2002.

## **1. Name of Standard.**

FIPS Publication 200: *Minimum Security Requirements for Federal Information and Information Systems*.

## **2. Category of Standard.**

Information Security.

## **3. Explanation.**

The E-Government Act (P.L. 107-347), passed by the one hundred and seventh Congress and signed into law by the President in December 2002, recognized the importance of information security to the economic and national security interests of the United States. Title III of the E-Government Act, entitled the Federal Information Security Management Act (FISMA), emphasizes the need for each federal agency to develop, document, and implement an enterprise-wide program to provide information security for the information and information systems that support the operations and assets of the agency including those provided or managed by another agency, contractor, or other source. FISMA directed the promulgation of federal standards for: (i) the security categorization of federal information and information systems based on the objectives of providing appropriate levels of information security according to a range of risk levels; and (ii) minimum security requirements for information and information systems in each such category. This standard addresses the specification of minimum security requirements for federal information and information systems.

## **4. Approving Authority.**

Secretary of Commerce.

## **5. Maintenance Agency.**

Department of Commerce, NIST, Information Technology Laboratory.

## **6. Applicability.**

This standard is applicable to: (i) all information within the federal government other than that information that has been determined pursuant to Executive Order 12958, as amended by Executive Order 13292, or any predecessor order, or by the Atomic Energy Act of 1954, as amended, to require protection against unauthorized disclosure and is marked to indicate its classified status; and (ii) all federal information systems other than those information systems designated as national security systems as defined in 44 United States Code Section 3542(b)(2). The standard has been broadly developed from a technical perspective to complement similar standards for national security systems. In addition to the agencies of the federal government, state, local, and tribal governments, and private sector organizations that compose the critical infrastructure of the United States are encouraged to consider the use of this standard, as appropriate.

## **7. Specifications.**

FIPS Publication 200, *Minimum Security Requirements for Federal Information and Information Systems*.

________________________________________________________________________________________________

## **8. Implementations.**

This standard specifies minimum security requirements for federal information and information systems in seventeen security-related areas. Federal agencies must meet the minimum security requirements as defined herein through the use of the security controls in accordance with NIST Special Publication 800-53, *Recommended Security Controls for Federal Information Systems*, as amended.

## **9. Effective Date.**

This standard is effective immediately. Federal agencies must be in compliance with this standard not later than one year from its effective date.

## **10. Qualifications.**

The application of the security controls defined in NIST Special Publication 800-53 required by this standard represents the current state-of-the-practice safeguards and countermeasures for information systems. The security controls will be reviewed by NIST at least annually and, if necessary, revised and extended to reflect: (i) the experience gained from using the controls; (ii) the changing security requirements within federal agencies; and (iii) the new security technologies that may be available. The minimum security controls defined in the low, moderate, and high security control baselines are also expected to change over time as well, as the level of security and due diligence for mitigating risks within federal agencies increases. The proposed additions, deletions, or modifications to the catalog of security controls and the proposed changes to the security control baselines in NIST Special Publication 800-53 will go through a rigorous, public review process to obtain government and private sector feedback and to build consensus for the changes. Federal agencies will have up to one year from the date of final publication to fully comply with the changes but are encouraged to initiate compliance activities immediately.

## **11. Waivers.**

No provision is provided under FISMA for waivers to FIPS made mandatory by the Secretary of Commerce.

## **12. Where to Obtain Copies.**

This publication is available from the NIST Computer Security Division web site by accessing http://csrc.nist.gov/publications.

## **TABLE OF CONTENTS**

________________________________________________________________________________________________

| SECTION 1 | PURPOSE 1 |
| --- | --- |
| SECTION 2 | INFORMATION SYSTEM IMPACT LEVELS 1 |
| SECTION 3 | MINIMUM SECURITY REQUIREMENTS 2 |
| SECTION 4 | SECURITY CONTROL SELECTION 4 |
| APPENDIX A | TERMS AND DEFINITIONS 6 |
| APPENDIX B | REFERENCES 10 |
| APPENDIX C | ACRONYMS 11 |

# **1 PURPOSE**

The E-Government Act of 2002 (Public Law 107-347), passed by the one hundred and seventh Congress and signed into law by the President in December 2002, recognized the importance of information security to the economic and national security interests of the United States. Title III of the E-Government Act, entitled the Federal Information Security Management Act (FISMA) of 2002, tasked NIST with the responsibility of developing security standards and guidelines for the federal government including the development of:

________________________________________________________________________________________________

- Standards for categorizing information and information systems 1 collected or maintained by or on behalf of each federal agency based on the objectives of providing appropriate levels of information security according to a range of risk levels;
- Guidelines recommending the types of information and information systems to be included in each category; and
- Minimum information security requirements for information and information systems in each such category.

FIPS Publication 199, *Standards for Security Categorization of Federal Information and Information Systems*, approved by the Secretary of Commerce in February 2004, is the first of two mandatory security standards required by the FISMA legislation.2 FIPS Publication 200, the second of the mandatory security standards, specifies minimum security requirements for information and information systems supporting the executive agencies of the federal government and a risk-based process for selecting the security controls necessary to satisfy the minimum security requirements. This standard will promote the development, implementation, and operation of more secure information systems within the federal government by establishing minimum levels of due diligence for information security and facilitating a more consistent, comparable, and repeatable approach for selecting and specifying security controls for information systems that meet minimum security requirements.

# **2 INFORMATION SYSTEM IMPACT LEVELS**

FIPS Publication 199 requires agencies to categorize their information systems as low-impact, moderate-impact, or high-impact for the security objectives of confidentiality, integrity, and availability. The potential impact values assigned to the respective security objectives are the highest values (i.e., high water mark3 ) from among the security categories that have been determined for each type of information resident on those information systems. 4 The generalized format for expressing the security category (SC) of an information system is:

**SC** information system = {(**confidentiality**, *impact*), (**integrity**, *impact*), (**availability**, *impact*)},

where the acceptable values for potential impact are low, moderate, or high.

1 An *information system* is a discrete set of information resources organized for the collection, processing, maintenance, use, sharing, dissemination, or disposition of information. Information resources include information and related resources, such as personnel, equipment, funds, and information technology.

<sup>2</sup> NIST security standards and guidelines referenced in this publication are available at http://csrc.nist.gov.

<sup>3</sup>  The *high water mark* concept is employed because there are significant dependencies among the security objectives of confidentiality, integrity, and availability. In most cases, a compromise in one security objective ultimately affects the other security objectives as well.

<sup>4</sup>  NIST Special Publication 800-60, *Guide for Mapping Types of Information and Information Systems to Security Categories*, provides implementation guidance on the assignment of security categories to information and information systems.

Since the potential impact values for confidentiality, integrity, and availability may not always be the same for a particular information system, the high water mark concept must be used to determine the overall impact level of the information system. Thus, a *low-impact system* is an information system in which all three of the security objectives are low. A *moderate-impact system* is an information system in which at least one of the security objectives is moderate and no security objective is greater than moderate. And finally, a *high-impact system* is an information system in which at least one security objective is high. The determination of information system impact levels must be accomplished prior to the consideration of minimum security requirements and the selection of appropriate security controls for those information systems.

________________________________________________________________________________________________

## **3 MINIMUM SECURITY REQUIREMENTS**

The minimum security requirements cover seventeen security-related areas with regard to protecting the confidentiality, integrity, and availability of federal information systems and the information processed, stored, and transmitted by those systems. The security-related areas include: (i) access control; (ii) awareness and training; (iii) audit and accountability; (iv) certification, accreditation, and security assessments; (v) configuration management; (vi) contingency planning; (vii) identification and authentication; (viii) incident response; (ix) maintenance; (x) media protection; (xi) physical and environmental protection; (xii) planning; (xiii) personnel security; (xiv) risk assessment; (xv) systems and services acquisition; (xvi) system and communications protection; and (xvii) system and information integrity. The seventeen areas represent a broad-based, balanced information security program that addresses the management, operational, and technical aspects of protecting federal information and information systems.

Policies and procedures play an important role in the effective implementation of enterprise-wide information security programs within the federal government and the success of the resulting security measures employed to protect federal information and information systems. Thus, organizations must develop and promulgate formal, documented policies and procedures governing the minimum security requirements set forth in this standard and must ensure their effective implementation.

## *Specifications for Minimum Security Requirements*

**Access Control (AC):** Organizations must limit information system access to authorized users, processes acting on behalf of authorized users, or devices (including other information systems) and to the types of transactions and functions that authorized users are permitted to exercise.

**Awareness and Training (AT):** Organizations must: (i) ensure that managers and users of organizational information systems are made aware of the security risks associated with their activities and of the applicable laws, Executive Orders, directives, policies, standards, instructions, regulations, or procedures related to the security of organizational information systems; and (ii) ensure that organizational personnel are adequately trained to carry out their assigned information security-related duties and responsibilities.

**Audit and Accountability (AU):** Organizations must: (i) create, protect, and retain information system audit records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful, unauthorized, or inappropriate information system activity; and (ii) ensure that the actions of individual information system users can be uniquely traced to those users so they can be held accountable for their actions.

**Certification, Accreditation, and Security Assessments (CA):** Organizations must: (i) periodically assess the security controls in organizational information systems to determine if the controls are effective in their application; (ii) develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities in organizational information systems; (iii) authorize the operation of organizational information systems and any associated information system connections; and (iv) monitor information system security controls on an ongoing basis to ensure the continued effectiveness of the controls.

**Configuration Management (CM):** Organizations must: (i) establish and maintain baseline configurations and inventories of organizational information systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles; and (ii) establish and enforce security configuration settings for information technology products employed in organizational information systems.

________________________________________________________________________________________________

**Contingency Planning (CP):** Organizations must establish, maintain, and effectively implement plans for emergency response, backup operations, and post-disaster recovery for organizational information systems to ensure the availability of critical information resources and continuity of operations in emergency situations.

**Identification and Authentication (IA):** Organizations must identify information system users, processes acting on behalf of users, or devices and authenticate (or verify) the identities of those users, processes, or devices, as a prerequisite to allowing access to organizational information systems.

**Incident Response (IR):** Organizations must: (i) establish an operational incident handling capability for organizational information systems that includes adequate preparation, detection, analysis, containment, recovery, and user response activities; and (ii) track, document, and report incidents to appropriate organizational officials and/or authorities.

**Maintenance (MA):** Organizations must: (i) perform periodic and timely maintenance on organizational information systems; and (ii) provide effective controls on the tools, techniques, mechanisms, and personnel used to conduct information system maintenance.

**Media Protection (MP):** Organizations must: (i) protect information system media, both paper and digital; (ii) limit access to information on information system media to authorized users; and (iii) sanitize or destroy information system media before disposal or release for reuse.

**Physical and Environmental Protection (PE):** Organizations must: (i) limit physical access to information systems, equipment, and the respective operating environments to authorized individuals; (ii) protect the physical plant and support infrastructure for information systems; (iii) provide supporting utilities for information systems; (iv) protect information systems against environmental hazards; and (v) provide appropriate environmental controls in facilities containing information systems.

**Planning (PL):** Organizations must develop, document, periodically update, and implement security plans for organizational information systems that describe the security controls in place or planned for the information systems and the rules of behavior for individuals accessing the information systems.

**Personnel Security (PS):** Organizations must: (i) ensure that individuals occupying positions of responsibility within organizations (including third-party service providers) are trustworthy and meet established security criteria for those positions; (ii) ensure that organizational information and information systems are protected during and after personnel actions such as terminations and transfers; and (iii) employ formal sanctions for personnel failing to comply with organizational security policies and procedures.

**Risk Assessment (RA):** Organizations must periodically assess the risk to organizational operations (including mission, functions, image, or reputation), organizational assets, and individuals, resulting from the operation of organizational information systems and the associated processing, storage, or transmission of organizational information.

**System and Services Acquisition (SA):** Organizations must: (i) allocate sufficient resources to adequately protect organizational information systems; (ii) employ system development life cycle processes that incorporate information security considerations; (iii) employ software usage and installation restrictions; and (iv) ensure that third-party providers employ adequate security measures to protect information, applications, and/or services outsourced from the organization.

**System and Communications Protection (SC):** Organizations must: (i) monitor, control, and protect organizational communications (i.e., information transmitted or received by organizational information systems) at the external boundaries and key internal boundaries of the information systems; and (ii) employ architectural designs, software development techniques, and systems engineering principles that promote effective information security within organizational information systems.

________________________________________________________________________________________________

**System and Information Integrity (SI):** Organizations must: (i) identify, report, and correct information and information system flaws in a timely manner; (ii) provide protection from malicious code at appropriate locations within organizational information systems; and (iii) monitor information system security alerts and advisories and take appropriate actions in response.

## **4 SECURITY CONTROL SELECTION**

Organizations must meet the minimum security requirements in this standard by selecting the appropriate security controls and assurance requirements as described in NIST Special Publication 800-53, *Recommended Security Controls for Federal Information Systems*. 5 The process of selecting the appropriate security controls and assurance requirements for organizational information systems to achieve *adequate security*6 is a multifaceted, risk-based activity involving management and operational personnel within the organization. Security categorization of federal information and information systems, as required by FIPS Publication 199, is the first step in the risk management process.7 Subsequent to the security categorization process, organizations must select an appropriate set of security controls for their information systems that satisfy the minimum security requirements set forth in this standard. The selected set of security controls must include one of three, appropriately tailored8 security control baselines from NIST Special Publication 800-53 that are associated with the designated impact levels of the organizational information systems as determined during the security categorization process.

- For *low-impact* information systems, organizations must, as a minimum, employ appropriately tailored security controls from the low baseline of security controls defined in NIST Special Publication 800-53 and must ensure that the minimum assurance requirements associated with the low baseline are satisfied.
- For *moderate-impact* information systems, organizations must, as a minimum, employ appropriately tailored security controls from the moderate baseline of security controls defined in NIST Special Publication 800-53 and must ensure that the minimum assurance requirements associated with the moderate baseline are satisfied.
- For *high-impact* information systems, organizations must, as a minimum, employ appropriately tailored security controls from the high baseline of security controls defined in NIST Special Publication 800-53 and must ensure that the minimum assurance requirements associated with the high baseline are satisfied.

Organizations must employ all security controls in the respective security control baselines unless specific exceptions are allowed based on the tailoring guidance provided in NIST Special Publication 800-53.

<sup>5</sup>  Organizations must use the most current version of NIST Special Publication 800-53, as amended, for the security control selection process.

<sup>6</sup> The Office of Management and Budget (OMB) Circular A-130, Appendix III, defines *adequate security* as security commensurate with the risk and the magnitude of harm resulting from the loss, misuse, or unauthorized access to or modification of information.

<sup>7</sup>  Security categorization must be accomplished as an enterprise-wide activity with the involvement of senior-level organizational officials including, but not limited to, chief information officers, senior agency information security officers, authorizing officials (a.k.a. accreditation authorities), information system owners, and information owners.

<sup>8</sup> Tailoring guidance for security control baselines is provided in NIST Special Publication 800-53.

To ensure a cost-effective, risk-based approach to achieving adequate security across the organization, security control baseline tailoring activities must be coordinated with and approved by appropriate organizational officials (e.g., chief information officers, senior agency information security officers, authorizing officials, or authorizing officials designated representatives). The resulting set of security controls must be documented in the security plan for the information system.

________________________________________________________________________________________________

## **APPENDIX A TERMS AND DEFINITIONS**

**ACCREDITATION:** The official management decision given by a senior agency official to authorize operation of an information system and to explicitly accept the risk to agency operations (including mission, functions, image, or reputation), agency assets, or individuals, based on the implementation of an agreed-upon set of security controls.

________________________________________________________________________________________________

**ADEQUATE SECURITY:** Security commensurate with the risk and the magnitude of harm resulting from the loss, misuse, or unauthorized access to or modification of information. [OMB Circular A-130, Appendix III]

**AGENCY:** Any executive department, military department, government corporation, government controlled corporation, or other establishment in the executive branch of the government (including the Executive Office of the President), or any independent regulatory agency, but does not include: (i) the Government Accountability Office; (ii) the Federal Election Commission; (iii) the governments of the District of Columbia and of the territories and possessions of the United States, and their various subdivisions; or (iv) government-owned contractor-operated facilities, including laboratories engaged in national defense research and production activities. [44 U.S.C., SEC. 3502]

**AUTHENTICATION:** Verifying the identity of a user, process, or device, often as a prerequisite to allowing access to resources in an information system.

**AUTHORIZING OFFICIAL:** Official with the authority to formally assume responsibility for operating an information system at an acceptable level of risk to agency operations (including mission, functions, image, or reputation), agency assets, or individuals. *Synonymous with Accreditation Authority.* 

**AVAILABILITY:** Ensuring timely and reliable access to and use of information. [44 U.S.C., SEC. 3542]

**CERTIFICATION:** A comprehensive assessment of the management, operational, and technical security controls in an information system, made in support of security accreditation, to determine the extent to which the controls are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting the security requirements for the system.

**CHIEF INFORMATION OFFICER:** Agency official responsible for: (i) providing advice and other assistance to the head of the executive agency and other senior management personnel of the agency to ensure that information technology is acquired and information resources are managed in a manner that is consistent with laws, Executive Orders, directives, policies, regulations, and priorities established by the head of the agency; (ii) developing, maintaining, and facilitating the implementation of a sound and integrated information technology architecture for the agency; and (iii) promoting the effective and efficient design and operation of all major information resources management processes for the agency, including improvements to work processes of the agency. [44 U.S.C., Sec. 5125(b)]

**CHIEF INFORMATION SECURITY OFFICER:** See Senior Agency Information Security Officer.

**CONFIDENTIALITY:** Preserving authorized restrictions on information access and disclosure, including means for protecting personal privacy and proprietary information. [44 U.S.C., SEC. 3542]

**COUNTERMEASURES:** Actions, devices, procedures, techniques, or other measures that reduce the vulnerability of an information system. [CNSS Instruction 4009] *Synonymous with security controls and safeguards.*

**ENVIRONMENT:** Aggregate of external procedures, conditions, and objects affecting the development, operation, and maintenance of an information system. [CNSS Instruction 4009]

**EXECUTIVE AGENCY:** An executive department specified in 5 U.S.C., SEC. 101; a military department specified in 5 U.S.C., SEC. 102; an independent establishment as defined in 5 U.S.C., SEC. 104(1); and a wholly-owned Government corporation fully subject to the provisions of 31 U.S.C., CHAPTER 91. [41 U.S.C., SEC. 403]

**FEDERAL AGENCY:** See Agency.

**FEDERAL INFORMATION SYSTEM:** An information system used or operated by an executive agency, by a contractor of an executive agency, or by another organization on behalf of an executive agency. [40 U.S.C., SEC. 11331]

________________________________________________________________________________________________

**HIGH-IMPACT SYSTEM:** An information system in which at least one security objective (i.e., confidentiality, integrity, or availability) is assigned a FIPS 199 potential impact value of high.

**INCIDENT:** An occurrence that actually or potentially jeopardizes the confidentiality, integrity, or availability of an information system or the information the system processes, stores, or transmits or that constitutes a violation or imminent threat of violation of security policies, security procedures, or acceptable use policies.

**INFORMATION:** An instance of an information type. [FIPS Publication 199]

**INFORMATION OWNER:** Official with statutory or operational authority for specified information and responsibility for establishing the controls for its generation, collection, processing, dissemination, and disposal. [CNSS Instruction 4009]

**INFORMATION RESOURCES:** Information and related resources, such as personnel, equipment, funds, and information technology. [44 U.S.C., SEC. 3502]

**INFORMATION SECURITY:** The protection of information and information systems from unauthorized access, use, disclosure, disruption, modification, or destruction in order to provide confidentiality, integrity, and availability. [44 U.S.C., SEC. 3542]

**INFORMATION SYSTEM:** A discrete set of information resources organized for the collection, processing, maintenance, use, sharing, dissemination, or disposition of information. [44 U.S.C., SEC. 3502]

**INFORMATION SYSTEM OWNER:** Official responsible for the overall procurement, development, integration, modification, or operation and maintenance of an information system. [CNSS Instruction 4009 Adapted]

**INFORMATION TECHNOLOGY:** Any equipment or interconnected system or subsystem of equipment that is used in the automatic acquisition, storage, manipulation, management, movement, control, display, switching, interchange, transmission, or reception of data or information by the executive agency. For purposes of the preceding sentence, equipment is used by an executive agency if the equipment is used by the executive agency directly or is used by a contractor under a contract with the executive agency which: (i) requires the use of such equipment; or (ii) requires the use, to a significant extent, of such equipment in the performance of a service or the furnishing of a product. The term information technology includes computers, ancillary equipment, software, firmware and similar procedures, services (including support services), and related resources. [40 U.S.C., SEC. 1401]

**INFORMATION TYPE:** A specific category of information (e.g., privacy, medical, proprietary, financial, investigative, contractor sensitive, security management), defined by an organization or, in some instances, by a specific law, Executive Order, directive, policy, or regulation. [FIPS Publication 199]

**INTEGRITY:** Guarding against improper information modification or destruction, and includes ensuring information non-repudiation and authenticity. [44 U.S.C., SEC. 3542]

**LOW-IMPACT SYSTEM:** An information system in which all three security objectives (i.e., confidentiality, integrity, and availability) are assigned a FIPS 199 potential impact value of low.

**MANAGEMENT CONTROLS:** The security controls (i.e., safeguards or countermeasures) for an information system that focus on the management of risk and the management of information system security.

**MEDIA:** Physical devices or writing surfaces including, but not limited to, magnetic tapes, optical disks, magnetic disks, Large-Scale Integration (LSI) memory chips, printouts (but not including display media) onto which information is recorded, stored, or printed within an information system.

________________________________________________________________________________________________

**MODERATE-IMPACT SYSTEM:** An information system in which at least one security objective (i.e., confidentiality, integrity, or availability) is assigned a FIPS 199 potential impact value of moderate, and no security objective is assigned a FIPS 199 potential impact value of high.

**NATIONAL SECURITY INFORMATION:** Information that has been determined pursuant to Executive Order 12958 as amended by Executive Order 13292, or any predecessor order, or by the Atomic Energy Act of 1954, as amended, to require protection against unauthorized disclosure and is marked to indicate its classified status.

**NATIONAL SECURITY SYSTEM:** Any information system (including any telecommunications system) used or operated by an agency or by a contractor of an agency, or other organization on behalf of an agency— (i) the function, operation, or use of which involves intelligence activities; involves cryptologic activities related to national security; involves command and control of military forces; involves equipment that is an integral part of a weapon or weapons system; or is critical to the direct fulfillment of military or intelligence missions (excluding a system that is to be used for routine administrative and business applications, for example, payroll, finance, logistics, and personnel management applications); or (ii) is protected at all times by procedures established for information that have been specifically authorized under criteria established by an Executive Order or an Act of Congress to be kept classified in the interest of national defense or foreign policy. [44 U.S.C., SEC. 3542]

**OPERATIONAL CONTROLS:** The security controls (i.e., safeguards or countermeasures) for an information system that primarily are implemented and executed by people (as opposed to systems).

**ORGANIZATION:** A federal agency or, as appropriate, any of its operational elements.

**POTENTIAL IMPACT:** The loss of confidentiality, integrity, or availability could be expected to have a limited adverse effect, a serious adverse effect, or a severe or catastrophic adverse effect on organizational operations, organizational assets, or individuals. [FIPS Publication 199]

**RECORDS:** All books, papers, maps, photographs, machine-readable materials, or other documentary materials, regardless of physical form or characteristics, made or received by an agency of the United States Government under Federal law or in connection with the transaction of public business and preserved or appropriate for preservation by that agency or its legitimate successor as evidence of the organization, functions, policies, decisions, procedures, operations or other activities of the Government or because of the informational value of the data in them. [44 U.S.C. SEC. 3301]

**RISK:** The level of impact on organizational operations (including mission, functions, image, or reputation), organizational assets, or individuals resulting from the operation of an information system given the potential impact of a threat and the likelihood of that threat occurring.

**RISK MANAGEMENT:** The process of managing risks to organizational operations (including mission, functions, image, or reputation), organizational assets, or individuals resulting from the operation of an information system, and includes: (i) the conduct of a risk assessment; (ii) the implementation of a risk mitigation strategy; and (iii) employment of techniques and procedures for the continuous monitoring of the security state of the information system.

**SAFEGUARDS:** Protective measures prescribed to meet the security requirements (i.e., confidentiality, integrity, and availability) specified for an information system. Safeguards may include security features, management constraints, personnel security, and security of physical structures, areas, and devices. [CNSS Instruction 4009 Adapted] *Synonymous with security controls and countermeasures.* 

**SANITIZATION:** Process to remove information from media such that information recovery is not possible. It includes removing all labels, markings, and activity logs. [CNSS Instruction 4009 Adapted] **SECURITY CATEGORY:** The characterization of information or an information system based on an assessment of the potential impact that a loss of confidentiality, integrity, or availability of such information or information system would have on organizational operations, organizational assets, or individuals. [FIPS Publication 199]

________________________________________________________________________________________________

**SECURITY CONTROLS:** The management, operational, and technical controls (i.e., safeguards or countermeasures) prescribed for an information system to protect the confidentiality, integrity, and availability of the system and its information. [FIPS Publication 199]

**SECURITY CONTROL BASELINE:** The set of minimum security controls defined for a low-impact, moderate-impact, or high-impact information system.

**SECURITY OBJECTIVE:** Confidentiality, integrity, or availability. [FIPS Publication 199]

**SECURITY PLAN:** See System Security Plan.

**SECURITY REQUIREMENTS:** Requirements levied on an information system that are derived from applicable laws, Executive Orders, directives, policies, standards, instructions, regulations, or procedures, or organizational mission/business case needs to ensure the confidentiality, integrity, and availability of the information being processed, stored, or transmitted.

**SENIOR AGENCY INFORMATION SECURITY OFFICER:** Official responsible for carrying out the Chief Information Officer responsibilities under FISMA and serving as the Chief Information Officer's primary liaison to the agency's authorizing officials, information system owners, and information system security officers. [44 U.S.C., Sec. 3544]

**SYSTEM:** See information system.

**SYSTEM SECURITY PLAN:** Formal document that provides an overview of the security requirements for an information system and describes the security controls in place or planned for meeting those requirements. [NIST Special Publication 800-18, Revision 1]

**TECHNICAL CONTROLS:** The security controls (i.e., safeguards or countermeasures) for an information system that are primarily implemented and executed by the information system through mechanisms contained in the hardware, software, or firmware components of the system.

**THREAT:** Any circumstance or event with the potential to adversely impact organizational operations (including mission, functions, image, or reputation), organizational assets, or individuals through an information system via unauthorized access, destruction, disclosure, modification of information, and/or denial of service. Also, the potential for a threat-source to successfully exploit a particular information system vulnerability. [CNSS Instruction 4009 Adapted]

**THREAT SOURCE:** The intent and method targeted at the intentional exploitation of a vulnerability or a situation and method that may accidentally trigger a vulnerability. *Synonymous with threat agent.* 

**USER:** Individual or (system) process authorized to access an information system. [CNSS Instruction 4009]

**VULNERABILITY:** Weakness in an information system, system security procedures, internal controls, or implementation that could be exploited or triggered by a threat source. [CNSS Instruction 4009 Adapted]

## **APPENDIX B REFERENCES**

- [1] Committee for National Security Systems (CNSS) Instruction 4009, *National Information Assurance Glossary*, May 2003.
________________________________________________________________________________________________

- [2] E-Government Act of 2002 (Public Law 107-347), December 2002.
- [3] Federal Information Processing Standards Publication 199, *Standards for Security Categorization of Federal Information and Information Systems*, February 2004.
- [4] Federal Information Security Management Act of 2002 (Public Law 107-347, Title III), December 2002.
- [5] Information Technology Management Reform Act of 1996 (Public Law 104-106), August 1996.
- [6] National Institute of Standards and Technology Special Publication 800-18, Revision 1, *Guide for Developing Security Plans for Federal Information Systems*, February 2006.
- [7] National Institute of Standards and Technology Special Publication 800-53, *Recommended Security Controls for Federal Information Systems*, February 2005.
- [8] National Institute of Standards and Technology Special Publication 800-60, *Guide for Mapping Types of Information and Information Systems to Security Categories*, June 2004.
- [9] Office of Management and Budget, Circular A-130, Transmittal Memorandum #4, *Management of Federal Information Resources*, Appendix III, *Security of Federal Automated Information Resources*, November 2000.

________________________________________________________________________________________________

## **APPENDIX C ACRONYMS**

| CIO | Chief Information Officer |
| --- | --- |
| CNSS | Committee for National Security Systems |
| FIPS | Federal Information Processing Standards |
| FISMA | Federal Information Security Management Act |
| NIST | National Institute of Standards and Technology |
| OMB | Office of Management and Budget |
| USC | United States Code |

