# CSA Cloud Security Glossary

Source: <https://cloudsecurityalliance.org/cloud-security-glossary>

Extracted via `extract_cloud_security_glossary.py`. Inclusion in this public dataset is authorized by CSA as the publisher and rights-holder; see the directory-level metadata.json for the authorization record.

**Total terms: 1119**


## #

### 802.1x

An IEEE standard for local and metropolitan area networks–Port-Based Network Access Control. IEEE 802 LANs are deployed in networks that convey or provide access to critical data, that support mission critical applications, or that charge for service. Port-based network access control regulates access to the network, guarding against transmission and reception by unidentified or unauthorized parties, and consequent network disruption, theft of service, or data loss.

*Sources:* https://1.ieee802.org/security/802-1x/ | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf


## A

### ACLs

Access Control Lists (ACLs) indicate the permissions that subjects are granted regarding accessing or changing the objects within a system.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### AI Hallucination

AI hallucinations are incorrect or misleading results that AI models generate. These errors can be caused by a variety of factors, including insufficient training data, incorrect assumptions made by the model, or biases in the data used to train the model.

*Sources:* https://cloud.google.com/discover/what-are-ai-hallucinations

### AI Risk Management Framework

The framework has an aim of improving the governance and trustworthiness around the usage of AI systems and models. The framework itself provides guidance around identifying risks associated with AI systems and recommends a four-step approach to govern, map, measure, and manage the risks throughout the AI lifecycle.

*Sources:* https://www.nist.gov/itl/ai-risk-management-framework

### AI as a Service (AIaaS)

A model where third-party providers offer AI capabilities and services over the Internet on a subscription basis. Organizations can access pre-trained AI models, APIs, and tools to integrate AI functionality into their applications and workflows.

*Sources:* https://www.zendesk.com/blog/ai-as-a-service/

### AWS API Access Key

The credentials pair of an AWS user, different to username/password credentials as they are intended for programmatic use with AWS API.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

### AWS EC2

The amazon web services server workloads (elastic compute) service, mostly used for virtual machines run by customers on AWS infrastructure.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

### Abstraction

Abstraction in computing refers to the process of hiding the complex implementation details of a system or component, exposing only the necessary and relevant aspects to the user. This allows users to interact with the system at a higher level without needing to understand the intricate workings beneath. In cloud computing, abstraction typically involves creating virtualized environments where physical resources are managed and allocated dynamically, simplifying the user interaction with underlying hardware and infrastructure.

*Sources:* https://www.cs.cornell.edu/courses/cs211/2006sp/Lectures/L08-Abstraction/08_abstraction.html

### Accepting Host (AH)

The SDP policy enforcement points (PEPs) that control access to any resource (or service) to which an identity might need to connect, and to which the responsible enterprise needs to hide and control access. AHs can be located on-premises, in a private cloud, public cloud, etc. A trusted node within an SDP. The accepting host (AH) accepts the communication from the initiating host (IH) after the SDP controller authenticates and authorizes the connection. The SDP controller instructs the accepting SDP hosts to accept communication from the initiating host by leveraging policies required for two-way encrypted communications such as mutual TLS.

*Sources:* https://cloudsecurityalliance.org/artifacts/software-defined-perimeter-zero-trust-specification-v2/ | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Accepting Host Controller Path

The channel used for communication between each accepting host (AH) and the controller.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf

### Accepting Host Session

The period of time that a particular accepting host (AH) is connected to a controller.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf

### Accepting Host Session ID

A 256-bit randomized arbitrary number used once (NONCE), managed by the SDP controller and used to refer to a particular accepting host (AH) session.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf

### Access

To make contact with one or more discrete functions of an online, digital service.

*Sources:* https://csrc.nist.gov/glossary/term/access

### Access control

Restricting access to a resource, based on the permissions granted to the entity.

*Sources:* https://www.microsoft.com/en-us/security/business/security-101/what-is-access-control

### Access Policy (SDP Policy)

For every connection established, SDP must fundamentally determine which users (and/or devices) are permitted to access which resources (e.g. services, gateways), and under which circumstances (e.g. from certain locations). SDPs provide policy decision points and policy enforcement points for connections. A cloud service provider (CSP), who elects to protect its resources behind a SDP, must develop a balanced “registered user access control policy”, as an undue restricted policy is likely to result in the denial of access/service. Expected access control policy’s performance attributes should become a part of the service level agreement (SLA).

*Sources:* https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Acknowledgement (ACK)

Confirmation that the destination has received the micropacket without errors.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec:11518:-10:ed-1:v1:en:term:3.1.1

### Active Directory (AD)

A Microsoft directory service for the management of identities in Windows domain networks.

*Sources:* https://csrc.nist.gov/glossary/term/active_directory

### Active Directory Federation Services (ADFS)

ADFS provides simplified, secured identity federation, and Web Single Sign- On (SSO) capabilities.

*Sources:* https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/ deployment/how-to-connect-fed-azure-adfs

### Active Directory Services

Active Directory Service serves as a central location for network administration and security. The AD is responsible for authenticating and authorizing all users and computers within a Windows domain network, assigning and enforcing security policies within all computers in a network, and installing or updating software on network computers.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Activity reporting

With respect to compliance and assurance processes, this is an artifact that summarize user activities, access patterns, and system interactions. Activity reports can help identify unauthorized access, track user actions, and ensure that operational practices align with compliance requirements.

*Sources:* https://www.isaca.org/resources/isaca-journal/issues/2019/volume-4/effective-user-access-reviews

### Actuators

An actuator is a component of a machine that is responsible for moving and controlling a mechanism or system, for example by opening a valve. In simple terms, it is a “mover”. An actuator requires a control signal and a source of energy. The control signal for an actuator is relatively low energy and may be electric voltage or current, pneumatic or hydraulic pressure, or even human power. Its main energy source may be an electric current, hydraulic fluid pressure, or pneumatic pressure. When it receives a control signal, an actuator responds by converting the signal’s energy into mechanical motion.

*Sources:* An actuator is a mechanism by which a control system acts upon an environment. The control system can be simple (a fixed mechanical or electronic system), software-based (e.g. a printer driver, robot control system), a human, or any other input. | https://en.wikipedia.org/wiki/Actuator

### Adaptive Authentication

Risk-based or adaptive authentication systems evaluate a host of user, system, and environmental attributes; other such signals; and behavioral profiles to make an authentication decision. IP address, geolocation, time of day, transaction type, mouse movements, keystroke, and variances from typical usage norms are some of the signals used in these systems. These solutions do not currently count as a valid authenticator in and of themselves, as this information does not necessarily constitute a “secret”, and most solutions leverage proprietary ways of making an authentication decision.

*Sources:* https://pages.nist.gov/800-63-FAQ/

### Adaptive Multi-Factor Authentication (MFA)

Adaptive MFA, otherwise known as risk-based MFA, provides users with authentication factors that adapt each time a user logs in depending on the calculated risk level of the user based on contextual information. Some examples of contextual information include: • The number of consecutive login failures • The physical location (geolocation) of the user requesting access • The type of device • The day of the week and the time of the day • The IP address

*Sources:* https://www.manageengine.com/products/self-service-password/ adaptive-multi-factor-authentication.html

### Address Space Layout Randomization (ASLR)

Address space layout randomization (ASLR) is a technique that randomizes the location of executables in memory space.

*Sources:* https://www.sciencedirect.com/topics/computer-science/address-space-layout-randomization

### Advanced Cloud Security Practitioner (ACSP)

This is an advanced, hands-on, cloud security class that expands on the basics of the CCSK Plus hands-on training. This course delves deep into practical cloud security and applied DevSecOps for enterprise-scale cloud deployments.

*Sources:* https://knowledge.cloudsecurityalliance.org/advanced-cloud-security-practitioner-2021

### Advanced Message Queuing Protocol (AMQP)

The Advanced Message Queuing Protocol is an open internet protocol for business messaging. AMQP is comprised of several layers. The lowest level defines an efficient, binary, peer-to-peer protocol for transporting messages between two processes over a network. Above this, the messaging layer defines an abstract message format, with concrete standard encoding. Every compliant AMQP process MUST be able to send and receive messages in this standard encoding.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec:19464:ed-1:v1:en

### Advanced Persistent Threats (APT)

Advanced persistent threats (APTs) is a broad term used to describe attack campaigns in which an intruder establishes an illicit, long-term presence on a network to mine highly sensitive data. These teams can include nationstates as well as organized criminal gangs.

*Sources:* https://cloudsecurityalliance.org/blog/2022/12/04/top-threat-10-to-cloud-computing-organized-crime-hackers-and-apt/

### Advanced maturity stage

With respect to zero trust maturity stages, at the Advanced maturity stage, organizations have significantly progressed in implementing Zero Trust practices and technologies across multiple domains.

*Sources:* https://www.cisa.gov/resources-tools/resources/zero-trust-maturity-model

### Agent ID (AID)

A 32-bit unique unsigned value that identifies a given initiating host (IH) and/or accepting host (AH) during single packet authorization.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf

### Agile

Software development approach based on iterative development, frequent inspection and adaptation, and incremental deliveries, in which requirements and solutions evolve through collaboration in cross-functional teams and through continual stakeholder feedback.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec-ieee:24748:-1:ed-1:v1:en:term:3.4

### Air-Gapped

An interface between two systems in which (a) they are not connected physically and (b) any logical connection is not automated (i.e., data is transferred through the interface only manually, under human control).

*Sources:* https://csrc.nist.gov/glossary/term/air-gap

### Air-Gapped Networks

An interface between two systems at which (a) they are not connected physically and (b) any logical connection is not automated (i.e., data is transferred through the interface only manually, under human control).

*Sources:* SDP is designed to provide an on-demand, dynamically provisioned, network that is the “equivalent of” an air-gapped network. | https://csrc.nist.gov/glossary/term/air_gap | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Amplification Attack

Any attack where an attacker causes more resource usage than what a single connection should be capable of. The amplification factor multiplies the attack’s power through asymmetry, where a low level of resources causes a large level of target failures. Memcached server - General purpose distributed memory caching system used for increasing speed on dynamic database-driven websites. Memcrashing - utilizing a weakness in Memcached server on UDP port 11211 to execute an Amplification Attack and paralyze the hosting server Port 11211 - Memcached clients use client-side libraries to contact servers. By default, Memchached servers expose their service at port 11211 on both TCP and UDP.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

### Anti-Phishing

The ability to detect phishing attacks targeted at an organization’s users such as inbound phishing emails.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### AntiVirus

See Anti-Virus, Anti-Spam, Anti-Malware.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### AntiVirus, AntiSpam, AntiMalware

A software program used to prevent, detect, and remove malware, including but not limited to computer viruses, computer worm, trojan horses, spam, spyware, and adware.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Appliance

Network based visualization provided by a dedicated hardware appliance (e.g., a NAS filer).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Application

Computer software designed to help the user to perform specific tasks. Examples include enterprise software, accounting software, office suites, graphics software, and media players.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Application / System Owner

Person or organization having responsibility for the development, procurement, integration, modification, operation and maintenance, and/or final disposition of an information system

*Sources:* https://csrc.nist.gov/glossary/term/system_owner#:~:text=NISTIR%20 8011%20Vol.,disposition%20of%20an%20information%20system

### Application Container

An application container is a construct designed to package and run an application or its components running on a shared operating system. Application containers are isolated from other application containers and share the resources of the underlying operating system, allowing for efficient restart, scale-up, or scale-out of applications across clouds. Application containers typically contain microservices.

*Sources:* NIST Special Publication (SP) 800-180 (Draft), NIST Definition of Microservices, Application Containers and System Virtual Machines, National Institute of Standards and Technology, Gaithersburg, Maryland, February 2016, 12pp. http://csrc.nist.gov/publications/drafts/800-180/sp800-180_draft.pdf

### Application Events

Specific events within an application may be deemed useful for security monitoring, such as access to protected data or execution of transactions subject to fraud.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Application Firewall

A form of firewall which controls input, output, and/or access from, to, or by an application or service. It operates by monitoring and potentially blocking the input, output, or system service calls that do not meet the firewall’s configured policy.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Application Layer

Layer of the TCP/IP protocol stack that sends and receives data for particular applications such as DNS, HTTP, and SMTP.

*Sources:* https://csrc.nist.gov/glossary/term/application_layer

### Application Monitoring

This capability is a collection of application-related events, including logins, access to sensitive data, transactions, administrative activity.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Application Performance Monitoring

Provides alerting, incremental resource provisioning, etc., when application performance measurements (e.g., response time) exceed service level objectives.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Application Programming Interface (API)

A system access point or library function that has a well-defined syntax and is accessible from application programs or user code to provide well-defined functionality.

*Sources:* https://csrc.nist.gov/glossary/term/application_programming_interface

### Application Services

Think of application services as the processes that developers use to write code, as well as the code itself. Application services are the rules and processes behind the user interface that manipulate the data and perform transactions for the user. In an online bank, this might be a bill payment transaction that deducts the payment amount from the user’s account and sends a check to the payee. In addition to the application services of an IT solution, the Application Services domain also represents the development processes that programmers go through when creating applications.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Application Virtualization

Removes the link between the application and the server(s) that host it. A consumer would access an application instance without regard to where or on what the application was hosted.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Application Vulnerability Scanning

Application vulnerability scanning is an automated capability that will examine the running application and identify areas where weaknesses exist that can be exploited.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Approval Workflow

The process of reviewing requested changes to ensure their appropriateness and receive authorization to continue from the necessary reviewers.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Architect

The individual or organization responsible for the set of processes to deploy and manage IT services. They ensure the smooth functioning of the infrastructure and operational environments that support application deployment to internal and external customers, including the network infrastructure, server and device management, computer operations, IT infrastructure library (ITIL) management, and help desk services20.

*Sources:* CSA. _Challenges in Securing Application Containers and Microservices Integrating Application Container Security Considerations into the Engineering of Trustworthy Secure Systems _(Cloud Security Alliance: 2019) 42

### Architectural Pattern

A general, reusable solution to a commonly occurring problem in software architecture within a given context. Architectural patterns are similar to software design patterns but have a broader scope. The architectural patterns address various issues in software engineering, such as computer hardware performance limitations, high availability and minimization of a business risk.

*Sources:* Wikipedia contributors. (2020, March 20). Architectural pattern. Wikipedia. https://en.wikipedia. org/wiki/Architectural_pattern

### Architecture

Fundamental concepts or properties of a system in its environment embodied in its elements, relationships, and in the principles of its design and evolution.

*Sources:* ISO/IEC/IEEE 42010. (2011). Systems and Software Engineering — Architecture: A Conceptual Model of Architecture Description. Retrieved August 11, 2021, from http://www.iso-architecture.org/ieee1471/cm/.

### Architecture Description

A conceptual model, an architecture description:

*Sources:* ISO/IEC/IEEE 42010. (2011). Systems and Software Engineering — Architecture: A Conceptual Model of Architecture Description. Retrieved August 11, 2021, from http://www.iso-architecture.org/ieee1471/cm/.

### Architecture Governance

Set of tools that can be used for developing a broad range of different architecture perspectives usually integrated as a common Architecture Framework.

*Sources:* Elements that the governance process must cover are: | Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Artificial Intelligence

the ability of a digital computer or computer-controlled robot to perform tasks commonly associated with intelligent beings.

*Sources:* https://www.britannica.com/technology/artificial-intelligence

### Assertion

Assertions are statements from an Identity Provider (IdP) to a relying party (RP) that contain information about a subscriber. Federation technology is generally used when the IdP and the RP are not a single entity or are not under common administration. The RP uses the information in the assertion to identify the subscriber and make authorization decisions about their access to resources controlled by the RP. An assertion typically includes an identifier for the subscriber, allowing association of the subscriber with their previous interactions with the RP. Assertions may additionally include attribute values or attribute references that further characterize the subscriber and support the authorization decision at the RP. Additional attributes may also be available outside of the assertion as part of the larger federation protocol. These attribute values and attribute references are often used in determining access privileges for Attribute Based Access Control (ABAC) or facilitating a transaction (e.g., shipping address).

*Sources:* https://pages.nist.gov/800-63-3/sp800-63c.html

### Asset Handling

The processes and procedures involved with managing physical assets (e.g., inventory control, location management, etc.).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Asset Management

This container manages all the financial aspects of the Configuration Items and Services provided by the Information Technology organization.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Assets

An asset is anything of value to the organization. Assets can be abstract assets (like processes or reputation), virtual assets (data, for instance), physical assets (cables, a piece of equipment), human resources, money, et cetera.

*Sources:* ENISA 2015, Technical Guideline on Threats and Assets, https://www.enisa.europa.eu/publications/technical-guideline-on-threats-and-assets

### Asymmetric Encryption

Also known as public-key encryption, is a form of data encryption. Two mathematically related keys, one called the public key and another called the private key , are generated to be used together. The encryption key (also called the public key) and the corresponding decryption key (also called the private key) are different. The encryption (public) key is used to digitally sign the data (encrypt it). The data can be decrypted only with the mathematically corresponding private key. It is computationally infeasible to derive the private key from the public key and only the recipient of the data is the holder of the private key.

*Sources:* https://www.sciencedirect.com/topics/computer-science/symmetric-encryption

### Asymmetric Keys

Also referred to as an asymmetric cipher, the encryption key and the decryption keys are separate. In an asymmetric system, each person has two keys. One key, the public key, is shared publicly. The second key, the private key, should never be shared with anyone.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Asynchronous (out-of-band) Testing

There are generally two categories of asynchronous testing: 1) Certain crucial security activities cannot be fully automated as they require human intelligence. These include threat modeling, penetration testing, and peer code review. 2) Heavyweight automated tests that take a long time to perform, such as SAST.

*Sources:* These activities can be triggered and performed “out of band” rather than inline with automated deployment so as to not disrupt the software deployment pipeline. | https://cloudsecurityalliance.org/artifacts/devsecops-automation/

### Asynchronous Communication

Communication in which a producer (or client) task sends a message to a consumer (or server) task and does not wait for a response.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec-ieee:24765:ed-2:v1:en:term:3.286

### Attack Patterns

Attack Patterns are descriptions of common attacks used by malicious parties that programmers must be aware of to defend against. For instance, the Open Web Application Security Project (OWASP) Top 10 Security Risks describes the top 10 attack patterns used to exploit web applications.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Attack Surface

The set of points on the boundary of a system, a system element, or an environment where an attacker can try to enter, cause an effect on, or extract data from, that system, system element, or environment.

*Sources:* https://csrc.nist.gov/glossary/term/attack_surface

### Attack surface

The set of points on the boundary of a system, a system element, or an environment where an attacker can try to enter, cause an effect on, or extract data from, that system, system element, or environment.

*Sources:* https://csrc.nist.gov/glossary/term/attack_surface

### Attribute Provisioning

The creation, maintenance and deactivation of user attributes as they exist in one or more systems, directories or applications, in response to automated or interactive business processes.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Attribute-Based Access Control (ABAC)

An access control approach in which access is mediated based on attributes associated with subjects (requesters) and the objects to be accessed. Each object and subject has a set of associated attributes, such as location, time of creation, access rights, etc. Access to an object is authorized or denied depending upon whether the required (e.g., policy-defined) correlation can be made between the attributes of that object and of the requesting subject.

*Sources:* SDPs can use attributes to control access to protected resources, as part of an SDP policy. | https://csrc.nist.gov/glossary/term/abac | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Attributes

An attribute or set of attributes that uniquely describe a subject within a given context. The set of attribute values (i.e., characteristics) by which an entity is recognizable and that, within the scope of an identity manager’s responsibility, is sufficient to distinguish that entity from any other entity.

*Sources:* https://csrc.nist.gov/glossary/term/identity#:~:text=An%20 attribute%20or%20set%20of,subject%20within%20a%20given%20 context.&text=The%20set%20of%20attribute%20values,entity%20 from%20any%20other%20entity

### Audit Logs

With respect to compliance and assurance processes, this is an artifact that provides detailed records of events, actions, and changes within the cloud environment. Audit Logs are chronological records of system activities, documenting events and transactions that occur within an IT environment. These logs provide a detailed account of who did what and when, serving as a critical tool for security monitoring, forensic investigations, and compliance reporting. Audit logs help organizations detect and investigate suspicious activities, ensuring accountability and transparency in system operations.

*Sources:* https://cloud.google.com/resources/data-governance-logs-best-practices-whitepaper

### Audit Findings

Documentation regarding the specific gaps in an organization’s controls discovered through an audit process.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Audit Management

It must be possible for an independent auditor to verify that the system conforms to the security policy. To enable this, systems and processes must ensure that security related events are recorded in a tamper-resistant audit log.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Audit Planning

Audit planning ensures the audits are scheduled and take place, are adequately staffed, and are considered part of the overall business delivery aspects.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Authentication

Verifying the identity of a user, process, or device, often as a prerequisite to allowing access to resources in an information system. Policies governing authentication may require single or multiple factors.

*Sources:* https://csrc.nist.gov/glossary/term/authentication | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Authentication

Verifying the identity of a user, process, or device, often as a prerequisite to allowing access to resources in a system.

*Sources:* https://csrc.nist.gov/glossary/term/authentication

### Authentication Events

Events indicating a successful or unsuccessful attempt to verify the identity of a user.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Authentication Factors

Authentication using two or more factors to achieve authentication. Factors include: (i) something you know (e.g., password/personal identification number [PIN]); (ii) something you have (e.g., cryptographic identification device, token); or (iii) something you are (e.g., biometric).

*Sources:* https://csrc.nist.gov/glossary/term/mfa#:~:text=Authentication%20 using%20two%20or%20more,are%20(e.g.%2C%20biometric)

### Authentication Services

The function or API or process of determining if someone or something is who or what it is declared to be.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Authenticators

Something that the claimant possesses and controls (typically a key or password) that is used to authenticate the claimant’s identity.

*Sources:* https://csrc.nist.gov/glossary/term/authenticator

### Authoritative Time Source

Assures a traceable, standard time source for use within an infrastructure (e.g., server clocks are synced to the time source to enable events occurring on one server to be correlated with those occurring on another during incident response).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Authoritative source

A trusted system that holds the most accurate and up-to-date information about an entity’s identity attributes. This information is then used by other IAM components for tasks like authentication and authorization.

*Sources:* https://csrc.nist.gov/glossary/term/authoritative_source

### Authorization

The right or a permission that is granted to a system entity to access a system resource.

*Sources:* https://csrc.nist.gov/glossary/term/authorization | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Authorization

The decision to permit or deny a subject access to system objects (network, data, application, service, etc.)

*Sources:* https://csrc.nist.gov/glossary/term/authorization

### Authorization Events

Events indicating policy decision outcomes about a given subject access to a given object.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Authorization Services

A function, API or process that facilitates access control to restricted areas of the operating system/application/service/data and allows the administrator to restrict a user’s or device’s access to particular features.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Automated security code review

This is also known as Static Application Security Testing (SAST). With respect to application pre-deployment testing, this process examines an application’s source code to identify existing security flaws or vulnerabilities. It is an automated way to perform a Security Code Review and might be integrated into a CI/CD pipeline or in the developer’s IDE.

*Sources:* https://docs.gitlab.com/ee/user/application_security/sast/

### Automated Asset Discovery

This capability allows the Configuration Management process to identify new and changing assets across the infrastructure and maintains the existing inventory of Configuration Items. Usually a process must be in place to formalize ownership for these new assets.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Automated Ticketing

The capability of having system generated events automatically spawn incidents.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Automation Gateway

Automation gateways are single or multiple devices that can operate as masters “host” or subordinates “slaves” to transmit data using serial lines or TCP/IP between disparate electronic devices. Manufacturers build automation gateways to transmit signals from instrumentation and control devices back to a main controller or data gathering system.

*Sources:* http://www.bb-elec.com/Learning-Center/All-White-Papers/Modbus/The-Answer-to-the-14-Most-Frequently-

### Availability

The ability of a configuration item or IT Service to perform its agreed Function when required. Availability is usually calculated as a percentage. This calculation is often based on Agreed Service Time and Downtime. It is best practice to calculate availability using measurements of the Business output of the IT Service.

*Sources:* Information Technology Infrastructure Library (ITIL). IT Service Management and the IT Infrastructure Library (ITIL). IT Infrastructure Library (ITIL) at the University of Utah. Retrieved June 15, 2021, from https://itil.it.utah.edu/index.html.

### Availability Management

The overall process that manages the availability of services to their users (both internal and external).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Availability Services

Concerned with assuring the availability of infrastructure components to match the service level objectives. Controls at this level include mirroring of data between geographically dispersed sites, redundant components and the processes for switching between them.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services


## B

### BIA

Business Impact Assessment (BIA) information regarding the consequences to the organization if a business process and/or its data was unavailable, lost, or stolen.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### BOSS

Business Operation Support Services (BOSS).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### BQP

The class of problems that can be efficiently solved by quantum computers is called BQP (bounded error, quantum, polynomial time). Quantum computers only run probabilistic algorithms, so BQP on quantum computers is the counterpart of BPP (bounded error, probabilistic, polynomial time) on classical computers. BQP is defined as a set of problems solvable with a polynomial-time algorithm, whose probability of error is bounded away from one half. A quantum computer is said to “solve” a problem if, for every instance, its answer will be correct with high probability. If that solution runs in polynomial time, then the problem is in BQP. It is suspected that no Nondeterministic Polynomial-time hardness (NP-hard) problems exist in BQP.

*Sources:* Quantum Safe Security Glossary : CSA

### Background Screening

Background verification for personnel, contractors, and third-parties must be in place and should be proportional to the data classification to be accessed under local laws, regulations, and ethics.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Barriers

Deny or limit physical access to a facility or portions of it (e.g., bollards placed between a facility and roadways to prohibit vehicular approach).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Basic Input/Output System (BIOS)

Fundamental system firmware that modern computers rely on to facilitate the hardware initialization process and transition control to the hypervisor or operating system.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-147B.pdf

### Bastion

Platform that provides secure Remote Desktop Protocol (RDP) and Secure Shell (SSH) connectivity to all of the VMs in the virtual network in which it is provisioned.

*Sources:* https://docs.microsoft.com/en-us/azure/bastion/bastion-overview

### Behavioral Malware Prevention

The ability to identify the behavior of malware based on events. For example, an inbound email with attached targeted malware to be filtered via the use of a secure virtual machine to identify when the payload is triggering atypical activity.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Benchmarking

The process of identifying a leader in a given practice area and comparing the organization’s practices against the leader and other organizations. This can help the organization to understand where they compare with other organizations in the industry with respect to knowledge, competency and capability

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Best Practices

The process of developing and following a standard way of doing things that multiple organizations execute in an efficient manner, the process includes methods, techniques, or frameworks that consistently show results superior to those achieved with other means, and that is used as a benchmark. These practices can evolve to become better as improvements are discovered (using mechanisms such as lessons learned).

*Sources:* This capability is intended to maintain quality as an alternative to mandatory legislated standards and can be based on self-assessment or benchmarking. | Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Best Practices & Regulatory Correlation

A mapping of best practices to mandated regulatory requirements. If a regulatory mandate requires a certain type of data to be encrypted (e.g., PHI in HIPPA), then a vendor best practice document would be correlated with the regulatory mandate to show how the best practices implement it for compliance.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Biometrics

Biometrics consists of methods for uniquely recognizing humans based upon one or more intrinsic physical or behavioral traits. Biometrics are considered a form of identity and are used for authentication and access control.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Black Box

Idealized mechanism that accepts inputs and produces outputs, but is designed such that an observer cannot see inside the box or determine exactly what is happening inside that box.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec:20543:ed-1:v1:en:term:3.3

### Black Box Testing

A method of software testing that examines the functionality of an application without peering into its internal structures or workings. This method of test can be applied to virtually every level of software testing: unit, integration, system and acceptance.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-192.pdf

### Black Listing Filtering

Blacklisting is a form of filtering where a list is created that registers entities that are prohibited access or are unwelcome signatures. When a blacklist is used, the default is to ‘permit all’ except for those entries that are enumerated in the filter. These are typically used when it is easier (and therefore a shorter list) to determine what entities should not be allowed.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### BlockBased Virtualization

Virtualization at the level of block level devices (e.g., the host is presented with a virtual disk device).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Branding Protection

The monitoring of external entities and activity that poses risk to the organization’s brand, such as imposter web sites, typosquatting, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Breach

Also known as a data breach. In the context of cloud security, signify a successful penetration or circumvention of security measures, leading to unauthorized access or extraction of data.

*Sources:* https://csrc.nist.gov/glossary/term/breach

### Break Glass Administrator

Are emergency access accounts that are highly privileged, and they are not assigned to specific individuals. Emergency access accounts are limited to emergency or “break glass”’ scenarios where normal administrative accounts can’t be used.

*Sources:* https://docs.microsoft.com/en-us/azure/active-directory/roles/security-emergency-access

### Bridge Network

With respect to docker networking, This is the default networking mode in Docker. Each container connects to a virtual bridge network on the host, allowing containers to communicate with each other. The bridge network is isolated from the host’s stack, providing network isolation.

*Sources:* https://docs.docker.com/network/drivers/bridge/#:~:text=A%20bridge%20can%20be%20a,connected%20to%20that%20bridge%20network .

### Bring-Your-Own-Device (BYOD)

An enterprise policy used to permit partial or full integration of user-owned mobile devices for business purposes

*Sources:* https://www.isaca.org/resources/glossary#glossz

### Broad Network Access

Services are available over the network and accessed through web browsers or specialized applications while using heterogeneous thin client platforms (e.g., servers, mobile phones, laptops, IoT devices, and tablets).

*Sources:* https://www.devx.com/terms/broad-network-access/#:~:text=Broad%20Network%20Access%20refers%20to,%2C%20laptops%2C%20or%20desktop%20computers .

### Broker

In computing, a broker is an intermediary that manages the communication and exchange of information between different systems or components. It is commonly used in software architecture to enable disparate systems to work together by translating messages and protocols.

*Sources:* https://csrc.nist.gov/glossary/term/cloud_broker#:~:text=An%20entity%20that%20manages%20the,Cloud%20Providers%20and%20Cloud%20Consumers

### Brute Force

A method of accessing an obstructed device by attempting multiple combinations of numeric/alphanumeric passwords

*Sources:* https://csrc.nist.gov/glossary/term/brute_force_password_attack

### Brute Force Attacks

An attempt to discover a password by systematically trying every possible combination of letters, numbers, and symbols until you discover the one correct combination that works.

*Sources:* https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks

### Build

The process of compiling source code and configurations into one or more deployable units to be handed off to the change management process.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Business Information Security Officer (BISO)

The Business Information Security Officer (BISO) is a role within an organization responsible for bridging the gap between the business and its information security functions. The BISO ensures that security measures are aligned with business objectives, working closely with business units to integrate security into business processes and strategies. This role helps in mitigating risks while supporting the organization’s overall goals.

*Sources:* https://www.infosecinstitute.com/resources/professional-development/what-does-a-business-information-security-officer-do/

### Business Assessment

Ensure that the business risks are identified, documented, and appropriate treatments are identified.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Business Continuity

Ensures that business continuity is considered in the risk management process. This should not only address business continuity but business resumption as well.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Business Continuity Planning

Preparing a business continuity plan and all the steps required to put it into action should it be required.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Business Continuity Testing

Testing a business continuity plan to ensure that it is effective.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Business Continuity and Disaster Recovery (BCDR)

The implementation of measures designed to ensure operational resiliency in the event of any service interruptions.

*Sources:* Defined Categories of Service 2011 : CSA

### Business Impact Analysis (BIA)

Process of analyzing operational functions and the effect that a disruption might have on them.

*Sources:* https://csrc.nist.gov/glossary/term/business_impact_analysis

### Business Intelligence

Business intelligence refers to techniques used in identifying, extracting and analyzing business data. BI technologies provide historical, current and predictive views of business operations.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Business Operation Support Services (BOSS)

The BOSS domain is all the corporate support functions such as Human Resources, Compliance, and Legal that are critical to a security program. It is also the place where the company’s operations and its systems are monitored for any signs of abuse or fraud.

*Sources:* BOSS was designed based on best practices and reference frameworks with the proven success of aligning the business and transforming the information security practice across organizations into a business enabler. | Enterprise Architecture Reference Guide v2 : CSA: Business Operation Support Services (BOSS) Domain

### Business Owner

A Product Ownership role that represents the person who is accountable to the Business for maximizing the overall value of the Deliverable Results; A role defined to represent management outside the Team. In practice the Business Owner is either the ‘lead’ Stakeholder, the Team’s Sponsor, or the Product Owner’s Product Owner.

*Sources:* Scrum Dictionary. Business Owner. ScrumDictionary.Com. Retrieved April 17, 2021, from https:// scrumdictionary.com/term/business-owner/.

### Business Strategy

Documentation of the business goals and objectives that can be used to determine the information technology and security strategies in support of the business.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Business-to-Business (B2B)

Business-to-Business (B2B) applications allow enterprises to exchange common transactions in bulk, for example purchase orders, invoices, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Business-to-Consumer (B2C)

Business-to-Consumer (B2C) applications are the online presence of an enterprise that allow it’s customers to conduct business with the enterprise over the internet.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Business-to-Employee (B2E)

Business-to-Employee (B2E) applications allow employees of an enterprise to transact the business of the company

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Business-to-Mobile (B2M)

Business-to-Mobile (B2M) applications utilize a mobile device such as a smartphone to enable customers or employees to interact with a business’s systems from anywhere at any time.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain


## C

### CFS

This is a code-based signature scheme designed by N. Courtois, N. Sendrier and M. Finiasz in 2001 [CFS01].

*Sources:* [CFS01] N. Courtois, M. Finiasz, and N. Sendrier. How to Achieve a McEliece-Based Digital Signature Scheme, ASIACRYPT 2001.

### CIA Triad

Three information security goals: Confidentiality, Integrity, Availability.

*Sources:* Confidentiality: Preserving authorized restrictions on information access and disclosure, including means for protecting personal privacy and proprietary information. | Integrity: Guarding against improper information modification or destruction, and includes ensuring information nonrepudiation and authenticity. | Availability: Ensuring timely and reliable access to and use of information. | https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.199.pdf

### CMDB

A configuration management database (CMDB) is a repository of information related to an information system’s components. It contains the details of the configuration items (CI) in the IT infrastructure. A CMDB helps an organization understand the relationships between these components and track their configuration. The CMDB records CIs and details about the important attributes and relationships between CIs. Configuration managers usually describe CIs using three configurable attributes: Technical, Ownership, Relationship

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### CNI Plugins

a standard for connecting containers to various networking technologies. It defines how networking plugins interface with container runtimes, enabling containers to communicate with each other and the external network. CNI plugins are modular components that implement the CNI specification, allowing container runtimes to configure network interfaces, manage IP addresses, and establish connectivity for containers within the networking environment.

*Sources:* https://www.cni.dev/docs/spec/

### CPS (Cyber Physical Systems)

Cyber-Physical Systems (CPS) are systems of collaborating computational entities that are in intensive connection with the surrounding physical world and its on-going processes, providing and using, at the same time, data-accessing and data-processing services available on the internet. In other words, CPS can generally be characterized as “physical and engineered systems whose operations are monitored, controlled, coordinated, and integrated by a computing and communicating core” (Rajkumar et al 2010). The interaction between the physical and cyber elements is of key importance: “CPS is about the intersection, not the union, of the physical and cyber. It is not sufficient to separately understand the physical components and the computational components. We must understand their interaction” (Lee and Seshia 2014).

*Sources:* https://link.springer.com/referenceworkentry/10.1007/978-3-642-35950-7_16790-1

### CRLs

A certificate revocation list (CRL) is a list of certificates that have been revoked, and therefore should not be relied upon.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### CSA Enterprise Architecture (EA) Model

both a methodology and a set of tools. It is a framework, that is, a comprehensive approach for the architecture of a secure cloud infrastructure. It can be used to assess opportunities for improvement, create roadmaps for technology adoption, identify reusable security patterns, and assess various CSPs and security technology vendors against a common set of capabilities.

*Sources:* https://cloudsecurityalliance.org/artifacts/enterprise-architecture-reference-guide-v2

### CSA STAR Attestation

A process where CSPs self-assess their security controls against the CSA CCM and publicly disclose the results of their assessments. This provides transparency into a provider’s security posture and enables CSCs to make informed decisions about utilizing their services.

*Sources:* https://cloudsecurityalliance.org/star

### CSA DevSecOps Software Delivery Pipeline (CDDP)

Security-enabled software delivery pipeline aligned with DevSecOps principles.

*Sources:* The Six Pillars of DevSecOps: Automation : CSA

### CSA STAR Certification

an independent third-party evaluation of a CSP’s security controls against the CSA CCM and other recognized industry standards like ISO/IEC 27001.

*Sources:* https://cloudsecurityalliance.org/star

### CSP Contact

In a cloud deployment registry, contact information for customer support and account management at the CAP. This information is essential for addressing any service-related issues and maintaining a healthy relationship with the CSP.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-210.pdf

### CSP Policy

Sometimes referred to as an organization policy type, this is a construct that allows enabling and disabling services for deployments on the deployment or group level. Some providers also support detective or corrective policies that identify policy violations and automatically fix them by restoring the correct settings. Corrective and detective policies are useful for situations where the orchestration engine of the CSP involves multiple steps to coordinate multiple resources, and none of the individual steps are sufficient for a decision.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-210.pdf

### Cache

Caching is a requirement for building scalable microservice applications. Data can be cached in memory or on fast local disks.

*Sources:* Microservices Architecture Pattern : CSA

### Capability Mapping

The capabilities of an Information Security Program can be described by a Security Service Catalog that is part of a larger catalog that some IT organizations document and publish to the business. These capabilities can be mapped in a way that describes what a business does to reach its objectives and promotes a strong relationship between the business model and the technical security infrastructure that supports the business requirements resulting in a view that can be understood by both the business and IT.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Capability Maturity Model (CMM)

The Software Capability Maturity Model (CMM) is a maturity framework for evaluating and improving the software development process.

*Sources:* https://www.sciencedirect.com/topics/computer-science/capability-maturity-model

### Capacity Planning

The process for assuring that the capacity (CPU power, network bandwidth, etc.) to deliver a service is continuously in line with the demand for that service.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Capital Expenditure (CAPEX)

Capital Expenditure (CAPEX) refers to funds used by an organization to acquire, upgrade, and maintain physical assets such as property, industrial buildings, or equipment. In IT, CAPEX typically includes spending on hardware, software licenses, and infrastructure that will be used over a long period. CAPEX investments are essential for growth and sustaining operations.

*Sources:* https://www.investopedia.com/ask/answers/112814/whats-difference-between-capital-expenditures-capex-and-operational-expenditures-opex.asp

### Center for Internet Security (CIS)

The Center for Internet Security (CIS) is a nonprofit organization focused on enhancing cybersecurity readiness and response among public and private sector entities. CIS provides a range of resources, including the CIS Controls and CIS Benchmarks, which are globally recognized best practices for securing IT systems and data against cyber threats​.

*Sources:* https://www.cisecurity.org/about-us

### Central Authentication Service (CAS)

CAS is a single sign-on (SSO) protocol that allows users to access multiple applications with one set of login credentials. This approach eliminates the need for users to remember multiple login credentials for different applications, reducing the risk of weak or reused passwords. CAS acts as a trusted intermediary between the user’s identity provider and the service providers that the user wishes to access. It helps to enhance security by ensuring that users are authenticated only once and are then granted access to all applications that they are authorized to use. For example, a university may use CAS to provide access to various campus services, such as email, course management systems, and library resources, with one set of credentials.

### Certificate Authority (CA)

A trusted entity that issues and revokes public key certificates.

*Sources:* SDP architectures rely on a CA, which the controllers use as a root of trust, and for generation of the TLS certificate. SDPs can also leverage U2F or UAF for user or device authentication without additional CA requirements, separate rom the CA utilized for mutual TLS. | https://csrc.nist.gov/glossary/term/certification_authority#:~:text=Definition(s)%3A,and%20revoke%20public%20key%20certificates | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Certificate Forgery

Data transmitted from an online certificate issuing server to output devices (such as a PC or printer) can be accessed by a hacker and modified into a false certificate.

*Sources:* https://ieeexplore.ieee.org/document/6922060

### Certificate of Cloud Auditing Knowledge (CCAK)

Created by the Cloud Security Alliance, the CCAK is the first credential available for industry professionals to demonstrate their expertise in the essential principles of auditing cloud computing systems.

*Sources:* https://cloudsecurityalliance.org/education/ccak/

### Certificate of Cloud Security Knowledge (CCSK)

Created by the Cloud Security Alliance, the CCSK is widely recognized as the standard of expertise for cloud security. It provides a cohesive and vendor-neutral understanding of how to secure data in the cloud.

*Sources:* https://cloudsecurityalliance.org/education/ccsk/

### Change Logs

From a security standpoint, monitoring the change logs and comparing it to configuration management changes could detect an unauthorized change in the environment.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Change Management

The process of managing the life cycle of changes in the IT environment. Change is a major pattern that acts as an intermediary between request, release and configuration/provisioning. Change management allows for management of scope, impact analysis, as well as scheduling of change. Change management provides one of the primary inputs into configuration management from a data maintenance perspective to keep application data up to date.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Change Review Board

A cross-functional team charged with ensuring that all changes to the environment are carefully considered and reviewed to minimize impact to users and existing services.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Chargeback

This process manages the IT service consumption by an area or user across the organization, as well calculates the associated costs to those services including People, Technology and supporting materials. The process ensures that there is a clear understanding on the TCO and costs per service (i.e. Desktop support, Network services, Security Services, etc.).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Chief Information Security Officer (CISO)

The Chief Information Security Officer (CISO) is a senior executive responsible for establishing and maintaining the enterprise vision, strategy, and program to ensure information assets and technologies are adequately protected. The CISO oversees the IT security department, manages cybersecurity risks, and ensures compliance with regulatory requirements. This role involves strategic planning, coordination of security efforts, and collaboration with other executives to integrate security into all aspects of the business.

*Sources:* https://www.isaca.org/resources/glossary#glossc

### Ciphertext

Data in its encrypted form.

*Sources:* https://csrc.nist.gov/glossary/term/ciphertext

### Circle

Circle is CSA’s online community forum platform where you can connect with peers and industry leaders. Circle is a global community that facilitates resources and security discussion within a diverse group of CSA partners.

*Sources:* https://circle.cloudsecurityalliance.org/

### Clear Desk Policy

A corporate policy that ensures sensitive information is not left out in the open for viewing or theft by unauthorized users.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Client Application Streaming

The Endpoint component of an application streaming solution. Clients could be tablets, phones, smart devices.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Client-Side Discovery

The client requests the network locations of available services from the service registry.

*Sources:* Best Practices in Implementing a Secure Microservices Architecture

### Client-to-Authenticator Protocol (CTAP)

An application layer protocol for communication between a roaming authenticator and another client/platform, as well as bindings of this application protocol to a variety of transport protocols using different physical media. The application layer protocol defines requirements for such transport protocols.

*Sources:* SDP can use this as an alternative to UAF and U2F for authenticating users to online services. CTAP enables external devices such as mobile handsets or FIDO security keys to work with W3C web authentication and serve as authenticators to desktop applications and web services. | https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### ClientID

256-bit numeric identifier, assigned per user-device pair. This field is used to distinguish the user, device, or logical group that is sending the packet.

*Sources:* https://cloudsecurityalliance.org/artifacts/software-defined-perimeter-zero-trust-specification-v2/

### Closest Vector Problem (CVP)

The Closest Vector Problem is Non-deterministic Polynomial-time hardness (NP-hard) and requires the closest vector of a given vector to be found in a lattice. This is a hard problem that occurs in lattice-based cryptography.

*Sources:* Quantum Safe Security Glossary : CSA

### Cloud Advisory Council

include a group of senior leaders from IT, risk management, compliance, security, and general business functions that are responsible for setting the vision and direction of the CSC’s cloud strategy and operating plan.

*Sources:* https://www.gartner.com/en/conferences/hub/cloud-conferences/insights/how-to-build-a-cloud-center-of-excellence

### Cloud Center of Excellence (CCoE)

a centralized team or department that provides guidance, best practices, and support to the rest of the organization regarding cloud adoption and usage. The CCoE helps ensure consistency, standardization, and alignment with the CSC’s goals and objectives.

*Sources:* https://www.gartner.com/en/conferences/hub/cloud-conferences/insights/how-to-build-a-cloud-center-of-excellence

### Cloud Computing

“Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction.”

*Sources:* https://csrc.nist.gov/glossary/term/cloud_computing

### Cloud Detection and Response (CDR)

tools designed to detect and respond to security threats and incidents within cloud environments. They leverage advanced analytics, threat intelligence, and possibly machine learning algorithms to identify suspicious activities, anomalous behavior, and indicators of compromise.

*Sources:* https://sysdig.com/learn-cloud-native/detection-and-response/cdr-an-overview/

### Cloud Registries

Typically referes to a cloud service registry and a cloud deployment registry. A Cloud Service Registry is the list of which cloud platforms and services are approved for which kinds of data (e.g., SaaS provider X is approved for data with classification Y). A Cloud Deployment Registry is a tool used in maintaining an inventory of an organization’s cloud presence across multiple providers and services. This is a centralized repository that maintains information about the organization’s deployed cloud resources, including details such as ownership, usage, and security controls.

*Sources:* https://www.redhat.com/en/topics/integration/what-is-a-service-registry

### Cloud Risk Profile

Serving as a foundational guide for cyber risk analysts and auditors, the profile provides insights into the organization’s risk landscape associated with cloud technologies.

*Sources:* https://csrc.nist.gov/glossary/term/risk_profile#:~:text=Definitions:,a%20complete%20inventory%20of%20risks .

### Cloud Service Customer (CSC)

Cloud Security Alliance (CSA) uses the term CSC to interchangeably mean any of Cloud Service Customer, Cloud Service Consumer, Cloud Service Client.

*Sources:* https://csrc.nist.gov/glossary/term/cloud_consumer_or_customer

### Cloud Service Provider (CSP)

A Cloud Service Provider (CSP) is an entity that offers cloud computing services to customers, providing various IT resources such as infrastructure, platforms, and software over the internet. The CSP is responsible for managing the underlying infrastructure and ensuring the availability, scalability, and security of the cloud services offered. Examples of services include Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS)​

*Sources:* https://csrc.nist.gov/glossary/term/cloud_provider_or_provider

### Cloud Workload Protection Platform (CWPP)

tools that provide targeted security for workloads deployed across hybrid cloud architectures. These tools safeguard physical servers, virtual machines, containers, and cloud deployments, regardless of location (on-premises or public cloud).

*Sources:* https://www.isaca.org/resources/isaca-journal/issues/2023/volume-3/navigating-the-new-distributed-enterprise

### Cloud sprawl

efers to the widespread proliferation of diverse workload types and the adoption of multiple CSPs within a CSC’s cloud environment. This phenomenon of dispersed cloud assets across various platforms and services complicates security monitoring and management. Managing cloud sprawl requires comprehensive strategies that address the complexities of monitoring and securing the diverse range of cloud assets.

*Sources:* https://www.crowdstrike.com/cybersecurity-101/secops/cloud-sprawl/

### Cloud workload

refers to the various tasks, applications, services, and processes run in cloud computing environments. Cloud workloads allow for scalability, flexibility, and efficiency, enabling businesses and individuals to access and run applications or data processing tasks without investing heavily in physical hardware. Cloud workloads encompass a range of resources, including virtual machines, containers, serverless functions (also referred to as Function as a Service (FaaS)), AI, and Platform as a Service (PaaS).

*Sources:* https://csrc.nist.gov/glossary/term/cloud_workload

### Cloud Access Security Broker (CASB)

On-premises, or cloud-based security policy enforcement points, placed between cloud service consumers and cloud service providers to combine and interject enterprise security policies as the cloud-based resources are accessed. CASBs consolidate multiple types of security policy enforcement.

*Sources:* SDPs typically rely on an organization’s existing identity and access management system (and/or external CASB) or an external federated identity service for user authentication and user attributes (such as role or group membership). | https://www.gartner.com/en/information-technology/glossary/cloud-access-security-brokers-casbs | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Cloud Controls Matrix (CCM)

A controls framework aligned to the CSA Security Guidance for Cloud Computing that is considered a de-facto standard for cloud security assurance and compliance.

*Sources:* https://cloudsecurityalliance.org/research/cloud-controls-matrix/

### Cloud Identity Management

Cloud identity management is the management of user identities and their access to resources that are stored and accessed in the cloud. It enables organizations to control user access to cloud-based applications and data through a central console. Cloud identity management provides authentication, authorization, and access management to cloud-based resources. It can be used to manage both employee and customer identities, with the aim of improving security, reducing administrative costs, and enhancing user experience. For example, an organization may use cloud identity management to manage access to cloud-based applications like Salesforce, Google Workspace, or Microsoft 365, ensuring that only authorized users have access to these applications.

### Cloud Incident Response (CIR)

CIR can be defined as the process designed to manage cyberattacks in a cloud environment and comprises four phases: • Phase 1: Preparation • Phase 2: Detection and Analysis • Phase 3: Containment, Eradication and, Recovery • Phase 4: Postmortem

*Sources:* Cloud Penetration Testing : CSA

### Cloud Monitoring

Collection of events associated with the usage of the services provided by cloud solutions at all layers of the application stack.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Cloud Security Monitoring and Compliance

Security technology that monitors virtual servers and assesses data, applications, and infrastructure for security risks.

*Sources:* The Six Pillars of DevSecOps: Automation : CSA

### Cloud Security Posture Management (CSPM)

Security technology that can discover, assess, and resolve cloud infrastructure misconfigurations vulnerable to attack.

*Sources:* The Six Pillars of DevSecOps: Automation : CSA

### Cloud Service Customer (CSC)

A party which is in a business relationship for the purpose of using cloud services.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso:tr:22428:-1:ed-1:v1:en:term:3.10

### Cloud Service Provider (CSP)

A cloud service provider, or CSP, is a company that offers some component of cloud computing

*Sources:* https://cloudsecurityalliance.org/blog/2020/04/30/what-is-a-cloud-service-provider/

### Cloud operating system

A type of operating system (OS) designed to operate within cloud computing and virtualization environments. A cloud operating system manages the operation, execution, and processes of virtual machines, virtual servers, and virtual infrastructure, as well as back-end hardware and software resources.

*Sources:* Cloud OS Security Specification v2.0

### Cloud-Native KMS

The KMS is built and owned by the same provider that delivers the cloud service the customer consumes, and all components of the KMS are in the cloud.

*Sources:* https://cloudsecurityalliance.org/artifacts/key-management-whenusing-cloud-services/

### Cloud-native databases

With respect to cloud-based database solutions, when DBaaS is used, the CSP provides and manages the database capability and the customer uses the database.

*Sources:* https://www.percona.com/blog/what-is-a-cloud-native-database/

### Code Samples

Code samples provide snippets of code that demonstrate to programmers how to code a specific algorithm. For secure coding purposes, examples could include writing a database query that is not susceptible to SQL injection.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Code-based cryptography

This is a sub-area of quantum-safe cryptography and includes cryptographic schemes whose security is related to the computational hard problem of decoding linear error-correcting codes.

*Sources:* Quantum Safe Security Glossary : CSA

### Collaboration

A presentation modality geared towards joint efforts on a combined effort such as a project or a document. Collaboration applications share files, allow multiple editors of documents, and often provide calendars, task tracking, and messaging for its participants.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Community cloud

The cloud infrastructure is provisioned for exclusive use by a specific community of consumers from organizations that have shared concerns (e.g., mission, security requirements, policy, and compliance considerations). It may be owned, managed, and operated by one or more of the organizations in the community, a third party, or some combination of them, and it may exist on or off-premises.

*Sources:* NIST 2011, The NIST Definition of Cloud Computing, https://csrc.nist.gov/publications/detail/ sp/800-145/final

### Company Owned

Devices purchased, owned, and managed by the enterprise and given out to employees or perhaps rented by customers.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Compliance

The goal that organizations aspire to achieve in their efforts to ensure that they are aware of and take steps to comply with relevant laws, policies, and regulations.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Compliance Classification

Used to categorize each environment based on regulatory and compliance needs, such as PCI DSS, HIPAA, GDPR, and so on. Proper classification ensures that the appropriate security measures and controls are applied to meet compliance requirements.

*Sources:* https://csrc.nist.gov/pubs/ir/8496/ipd

### Compliance Inheritance

A technique used to relieve some of the burden from the customer, by allowing the customer to acquire a control set from a compliant provider.

*Sources:* https://csrc.nist.gov/glossary/term/control_inheritance

### Compliance Management

It analyzes compliance with all specified internal information security policies, control standards and procedures.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Compliance Monitoring

Processes and procedures for assuring that a service is being provided in compliance with applicable policies and regulatory frameworks. This can be implemented through either periodic audit or continuous monitoring.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Compliance Testing

Compliance testing determines the degree to which information security policies, standards, and control procedures are being adhered to. One example is scanning to detect the presence or absence of mandated patches and updates on virtual and physical machines.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Compliance as Code (CaC)

The moderinization from manual document based compliance management to automated processes for continuous compliance in agile environments.

*Sources:* https://ieeexplore.ieee.org/document/9860731

### Computer Events

Events generated by servers, desktops and other Endpoint devices including start ups, shutdowns, configuration changes, and system errors.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Conceptual Models

frameworks include visualizations and descriptions used to explain cloud security concepts and principles, such as the NIST model in this document.

*Sources:* https://www.nist.gov/publications/conceptual-modeling

### Confidential Computing

an approach to computing in the cloud that focuses on ensuring that sensitive data remains encrypted and secure even while it is being processed or analyzed (data-in-use). By using hardware-based enclaves, the entire workload runtime and memory are encrypted, enabling very tight security at all layers of the processing stack.

*Sources:* https://csrc.nist.gov/glossary/term/confidential_computing

### Configuration Management

The process and procedures for managing the configuration of assets (servers, storage arrays, network equipment, etc.) to assure that their configuration as deployed matches that specified by policy, standards and guidelines.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Configuration Management Database (CMDB)

A configuration management database (CMDB) is a repository of information related to all the components of an information system. It contains the details of the configuration items (CI) in the IT infrastructure. A CMDB helps an organization understand the relationships between these components and track their configuration. The CMDB records CIs and details about the important attributes and relationships between CIs. Configuration managers usually describe CIs using three configurable attributes: Technical, Ownership, Relationship

*Sources:* https://ea.cloudsecurityalliance.org/display.php?id=data_info4018&_ga=2.250011589.277413644.1656439470-2107700575.1655484199

### Configuration Rules (Metadata)

This metadata contains the configuration rules for how to deploy configuration changes to specific configuration items.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Connectivity & Delivery

Connectivity & Delivery services are the underlying mechanisms that Integration Middleware uses to move the messages between applications. These services must also protect the messages being delivered, including encrypting the messages to hide their contents.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Consensus Assessment Initiative Questionnaire (CAIQ)

Offers an industry-accepted way to document what security controls exist in IaaS, PaaS, and SaaS services. It provides a set of Yes/No questions a cloud consumer and cloud auditor may wish to ask of a cloud provider to ascertain their compliance to the Cloud Controls Matrix.

*Sources:* https://cloudsecurityalliance.org/artifacts/consensus-assessments-initiative-questionnaire-v3-1/

### Consumer Service Platform

This container holds the various types of presentation modalities that are consumer-oriented as opposed to enterprise-oriented.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Contact / Authority Maintenance

Ensures that contact information for relevant authorities and critical business partners is kept up-to-date, so it is correct when you need it and it also enforces a risk limit for the corporate role level.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Container Image

A package of software that can run within a container. Note 1 to entry: Typically, it includes dependencies except for the operating system kernel.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec:22123:-1:ed-2:v1:en:term:3.12.5

### Container Lifecycle Events

The main events in the life cycle of a container are create container, run container, pause container, unpause container, start container, stop container, restart container, kill container, destroy container.

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Container Management Platform

A container management platform is an application designed to manage containers and their various operations, including but not limited to deployment, configuration, scheduling, and destruction.

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Container Rehosting

Redeploying containers on another platform.

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Container Resource Limit

The maximum amount of resources (CPU, memory (+swap) and disk (space + speed)) that the system will allow a container to use.

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Container Resource Requests

The amount of CPU, memory (+swap), and disk (space + speed) that the system will allocate to the container considering the resource limit.

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Container Resources

Four resources required for containers to operate are CPU, memory (+swap), disk (space + speed), and Network.

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Containers

See: Application Container

*Sources:* https://cloudsecurityalliance.org/cloud-security-glossary#A

### Content Delivery Networks (CDNs)

Content Delivery Networks (CDNs) are systems of distributed servers that deliver web content and other resources to users based on their geographic location. CDNs improve the performance, speed, and reliability of websites by caching content closer to end-users and reducing the distance data must travel.

*Sources:* https://csrc.nist.gov/glossary/term/content_delivery_networks

### Content Filtering

The technique whereby content is blocked or allowed based on analysis of its content, rather than its source or other criteria. It is most widely used on the internet to filter email and web access.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Context Based Access Control (CBAC)

Context Based Access Control (CBAC) is a type of access control that makes decisions based on the context of a user’s request. This includes factors such as the user’s identity, the time of the request, the device being used, and the location. CBAC enhances security by allowing more granular and dynamic control over access to resources.

*Sources:* https://www.cisco.com/c/en/us/support/docs/security/ios-firewall/13814-32.html

### Continuous Assessment

The practice of continually evaluating IAM configurations and actual access patterns within a cloud environment for misconfigurations, unnecessary privileges, and other security lapses. These issues can then be addressed manually or through automated remediation processes.

*Sources:* https://www.isaca.org/resources/isaca-journal/issues/2019/volume-4/effective-user-access-reviews

### Continuous Multi-Factor Authentication (CMFA)

Continuous Multi-Factor Authentication (CMFA) is an advanced security approach that continuously verifies a user’s identity throughout a session using multiple authentication factors. CMFA enhances security by ensuring that the user’s identity is authenticated at all times, reducing the risk of unauthorized access.

*Sources:* https://csrc.nist.gov/csrc/media/Presentations/2022/multi-factor-authentication-and-sp-800-63-digital/images-media/Federal_Cybersecurity_and_Privacy_Forum_15Feb2022_NIST_Update_Multi-Factor_Authentication_and_SP800-63_Digital_Identity_%20Guidelines.pdf

### Continuous Assessment

Assessments that improve the overall security posture of an organization while minimizing the disruption that comes with implementing major security changes. They also provide more agility in responding to evolving threats and vulnerabilities, while minimizing the risk of a security incident.

*Sources:* https://cloudsecurityalliance.org/

### Continuous Auditing

Allows an organization to show control compliance at all times. As a consequence of the shortcomings of traditional assurance tools, organizations that want continuous assurance must rethink their approach to security assessments. For continuous assurance, manual assessments must be traded for automated measurements, which largely leave humans out of the loop. Instead of assessing controls directly, tools are used to measure the security attributes of an information system and infer indirectly whether controls are effectively in place.

*Sources:* The Continuous Audit Metrics Catalog : CSA

### Continuous Authentication

Continuous authentication is a security approach that verifies a user’s identity on an ongoing basis, rather than just during the initial login. It helps to prevent unauthorized access by continuously monitoring user behavior, such as typing speed, mouse movements, and location, and comparing it to established patterns. Continuous authentication can help to detect and prevent account takeovers by identifying suspicious behavior in real- time. For example, a bank may use continuous authentication to monitor a customer’s behavior while they are accessing their account, ensuring that any unusual activity is detected and addressed promptly.

### Continuous Monitoring

performs the function of continuous risk management presenting the current security posture of the organization. Using industry approved risk management frameworks, Continuous Monitoring collects inventory of deployed organizational assets (including but not limited to current patch/version status, vulnerabilities, threats, and traffic) and generates ongoing risk scores across the enterprise. The intent of Continuous Monitoring is to reduce the time and effort required to identify security risks, assist in defining mitigation strategies, and implement any necessary controls reducing the security risk window.

*Sources:* Defining Categories of Security as a Service: Continuous Monitoring : CSA

### Continuous deployment (CD)

The process of automatically deploying code into an environment which includes automated scanning, testing, and building activities.

*Sources:* https://cloudsecurityalliance.org/artifacts/devsecops-pillar-4-bridging-compliance-and-development/

### Continuous integration (CI)

The frequent commitment and merging of new code and code changes to coding repositories that are validated by creating a build and running automated tests against the build.

*Sources:* https://cloudsecurityalliance.org/artifacts/devsecops-pillar-4-bridging-compliance-and-development/

### Continuous integration/continuous delivery (CI/CD) pipeline

These pipelines are workflows for taking the developer’s source code through various stages, such as building, testing, packaging, deployment, and operations supported by automated tools with feedback mechanisms.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204C.pdf

### Contractors

All third-parties bound to a contract to provide a service for the organization are not considered employees but have access to various resources and data across the company. This capability is intended to manage these contractors and the associated processes to onboard and release them.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Contracts

An agreement between two or more parties with the serious intent of creating a legal obligation or obligations. Contracts between an enterprise and its service providers designate the responsibilities of each party and the penalties associated when service level agreements are not met.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Control

The means of managing risk, including policies, procedures, guidelines, practices or organizational structures, which can be of an administrative, technical, management, or legal nature. Scope Notes: Also used as a synonym for safeguard or countermeasure. See also Internal control.

*Sources:* ISACA. Interactive Glossary & Term Translations. Retrieved August 11, 2021, from https://www. isaca.org/resources/glossary.

### Control Specifications and Implementation Guidance

In IT governance, these are the base level of the governance hierarchy. These are the technical embodiments that satisfy the control objectives. Control specifications are unique depending on the CSP and platform being used, such as AWS or Azure. They outline the technical controls that should be in place to achieve the desired security outcomes.

*Sources:* https://csrc.nist.gov/pubs/sp/800/53/b/upd1/final

### Control Models

or frameworks categorize and detail specific cloud security controls or categories of controls, such as the CSA CCM.

*Sources:* https://csrc.nist.gov/Projects/Access-Control-Policy-and-Implementation-Guides

### Control Specifications

Outline the detailed technical control capabilities that must be implemented to meet specific security requirements. It is important to note that control specifications should be vendor and technology-specific, meaning that there can be significant differences between different CSPs.

*Sources:* https://csrc.nist.gov/pubs/sp/800/53/b/upd1/final

### Control Framework

A set of fundamental controls that facilitates the discharge of business process owner responsibilities to prevent financial or information loss in an enterprise.

*Sources:* ISACA. Interactive Glossary & Term Translations. Retrieved August 11, 2021, from https://www. isaca.org/resources/glossary.

### Control Layer

An SDN control layer, which consists of four main components, namely a high level language, a rule update process, a network status collection process and a network status synchronization process. The control layer bridges the application layer and the infrastructure layer.

*Sources:* https://ieeexplore.ieee.org/abstract/document/6834762

### Control Loop

A control loop is the fundamental building block of industrial control systems. It consists of all the physical components and control functions necessary to automatically adjust the value of a measured process variable (PV) to equal the value of a desired set-point (SP). It includes the process sensor, controller function, and final control element (FCE) which are all required for automatic control.

*Sources:* https://en.wikipedia.org/wiki/Control_loop

### Control Objective

A statement of the desired result or purpose to be achieved by implementing control procedures in a particular process.

*Sources:* ISACA. Interactive Glossary & Term Translations. Retrieved August 11, 2021, from https://www. isaca.org/resources/glossary.

### Control Plane

Used by various infrastructure components (both enterprise-owned and from service providers) to maintain and configure assets; judge, grant, or deny access to resources; and perform any necessary operations to set up communication paths between resources.

*Sources:* SDP architectures separate the control of connections called the ‘control plane’ from the actual connections used to transfer data. The control plane consists of those connections that enable the vetting of users, devices, and ensure access to authorized services only providing extra security for those connections used to transfer data. | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Control-Flow Integrity (CFI)

Control-Flow Integrity (CFI) is a defense which prevents control-flow hijacking attacks.

*Sources:* https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/carlini

### Controlled Physical Access

The security controls that limit physical access to a facility and its contents.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Controller (SDP Controller)

Determines which SDP hosts can communicate with each other. The controller may relay information to external authentication services such as attestation, geo-location, and/or identity servers.

*Sources:* An appliance or process that controls secure access to isolated servicesby ensuring that users are authenticated and authorized, devices are validated, communications are established, and user and management traffic are separated. Initiating hosts (often user devices) and accepting hosts (services and in some instances the SDP gateway) connect to the SDP controller. | https://downloads.cloudsecurityalliance.org/initiatives/sdp/Software_Defined_Perimeter.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Controllers (or Control Server)

Controllers (or control servers) are most often comprised of Programmable Logic Controllers (PLC), designed to perform logic functions executed by electrical hardware such as relays, switches or sensors. Other types of controllers include Remote Terminal Units (RTUs) that differ from PLCs in that RTUs are more suitable for wide geographical telemetry, often using wireless communications while PLCs are more suitable for local area control.

*Sources:* Master Terminal Units (MTU’s) are controllers that serve as the Master in an ICS system, controlling the operation of the Slave subsystems (PLCs and RTUs). | https://www.sciencedirect.com/topics/computer-science/industrial-control-system

### Convolutional Neural Network

A deep learning neural network designed for processing structured arrays of data such as images. Convolutional neural networks are widely used in computer vision and have become the state of the art for many visual applications such as image classification, and have also found success in natural language processing for text classification.

*Sources:* https://deepai.org/machine-learning-glossary-and-terms/convolutional-neural-network

### Counter Threat Management

The overall process of managing threats and countermeasures.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Credential

A credential is a set of login credentials, such as a username and password, that a user provides to authenticate themselves to access a system or application. Credentials are used to verify a user’s identity and ensure that only authorized individuals can access resources. The security of credentials is critical in protecting against unauthorized access to systems and data. For example, a user’s credentials may include a username and password that they use to log in to their email account.

### Credential Stuffing

A cyberattack method in which attackers use lists of compromised user credentials to breach into a system. The attacker uses bots for automation and scale and is based on the assumption that many users reuse usernames and passwords across multiple services.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

### Crisis Management

The overall coordination of an organization’s response to a crisis effectively with the overall goal of avoiding or minimizing damage to the organization’s profitability, reputation, or ability to operate.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Cross Cloud Security Incident Response

Because of the ubiquitous nature of cloud computing, a security incident may be detected in or affect several cloud instances. The incident response plan must include processes and procedures for handling trans-cloud security incidents.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Cross Site Scripting (XSS)

A vulnerability that allows attackers to inject malicious code into an otherwise benign website. These scripts acquire the permissions of scripts generated by the target website and can therefore compromise the confidentiality and integrity of data transfers between the website and client. Websites are vulnerable if they display user-supplied data from requests or forms without sanitizing the data so that it is not executable.

*Sources:* https://csrc.nist.gov/glossary/term/cross_site_scripting

### Cross-cloud capabilities

Unified data management platform that facilitates secure data sharing should carry out cross-cloud management. The platform gives the organization a single source of truth by allowing data to move freely across clouds. Cross-cloud compatibility drives operational efficiency in the multi-cloud.

*Sources:* https://www.cloudbolt.io/blog/driving-operational-efficiency-in-multi-cloud-with-cross-cloud-management/

### Cryptographic Algorithm

A well-defined computational procedure that takes variable inputs, including a cryptographic key, and produces an output.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf

### Cryptographic Services

A set of cryptographic functions (e.g., encoding and decoding, encryption and decryption), which computer application programs may use, to implement security solutions (e.g., strong user authentication or secure email). For example, in Microsoft Windows, a Cryptographic Service Provider (CSP) is a software library that implements the Microsoft CryptoAPI (CAPI).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Customer Identity Access Management (CIAM)

Customer Identity Access Management (CIAM) is a subcategory of Identity Access Management (IAM) that focuses on managing and securing customer identities and their access to resources. CIAM solutions enable organizations to provide customers with seamless and secure access to digital services and applications, such as online shopping or banking, across multiple channels and devices. CIAM solutions typically include features such as identity verification, registration, authentication, authorization, and consent management. For example, a retailer may use CIAM to manage customer identities and access to their online store, ensuring that only authorized customers can make purchases.

### Customer-Managed Encryption Keys (CMEK)

Customer-Managed Encryption Keys (CMEK) are encryption keys that are managed and controlled by the customer rather than the cloud service provider. CMEK provides customers with greater control over their data security, ensuring that only they have access to the keys used to encrypt and decrypt their data.

*Sources:* https://csrc.nist.gov/projects/key-management

### CxO

A term for Cloud Security Alliance programs that are targeted towards C-Level executives.

*Sources:* https://cloudsecurityalliance.org/cxo-trust/

### cloud-native application protection platform (CNAPP)

A tool or set of tools that provide monitoring and management capabilities for deviations from security and compliance baselines. Specifically,

*Sources:* https://medium.com/@cloud_tips/cnapp-gartner-definition-4f75c2bd5027


## D

### D-Wave machine

This is the first quantum machine publicly available (from D-Wave Systems, Canada). The machine is not a general purpose quantum computer, but instead is targeted at quantum annealing.

*Sources:* Quantum Safe Security Glossary : CSA

### DB

See Databases (earlier)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### DBMS Repositories

Database Management Systems used to store user accounts and their data as tables within a database.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### DCS (Distributed Control Systems)

Refers to control achieved by intelligence that is distributed throughout the system, rather than by a centrally located single unit.

*Sources:* NIST SP 800-82r2 https://csrc.nist.gov/publications/detail/sp/800-82/rev-2/final

### DETECT (DE)

In the NIST Cybersecurity Framework (CSF), the process that is used to find and analyze possible cybersecurity attacks and compromises.

*Sources:* https://csrc.nist.gov/glossary/term/detect_csf

### DLP Events

Data Leakage Prevention (DLP) events are triggered whenever privileged data is intercepted on its way out of the organization.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### DMZ (Demilitarized Zone)

In computer security, a demilitarized zone (DMZ) or perimeter network is a network area (a subnetwork) that sits between an internal network and an external network. The purpose of a DMZ is that connections from the internal and the external network to the DMZ are permitted, whereas connections from the DMZ are only permitted to the external network – hosts in the DMZ may not connect to the internal network. This allows the DMZ’s hosts to provide services to the external network while protecting the internal network in case intruders compromise a host in the DMZ. For someone on the external network who wants to illegally connect to the internal network, the DMZ is a dead end.

*Sources:* The Security DMZ is used for providing controlled and secure access to services used by external personnel or systems. Access may be granted to control system networks, control system equipment, or other applications services provided. | https://www.us-cert.gov/ics/Control_System_Security_DMZ-Definition.html

### DPI

Deep Packet Inspection (DPI) (also called complete packet inspection and Information extraction - IX -) is a form of computer network packet filtering that examines the data part (and possibly also the header) of a packet as it passes an inspection point, searching for protocol non-compliance, viruses, spam, intrusions or predefined criteria to decide if the packet can pass or if it needs to be routed to a different destination, or to collect statistical information.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### DR & BC Plans

Documentation of Disaster Recover (DR) Plans to restore IT operations and Business Continuity (BC) Plans to ensure continuous service by the enterprise during planned or unplanned outages.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### DRP

The document defines the resources, actions, tasks, and data required to manage the business recovery process in the event of a business interruption. The plan is designed to assist in restoring the business process within the stated disaster recovery goals.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Daemon

A software application that is not invoked explicitly, but lies dormant waiting for some condition(s) to occur

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec:tr:13066:-4:ed-1:v1:en:term:2.10

### Dashboard

The dashboard provides a top-level view of various aspects of the information services. The dashboard usually includes aggregated Key Performance Indicators (KPIs) and Key Quality Indicators (KQIs).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Data

The digital representation of anything in any form (SNIA Dictionary).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Data Encryption Keys (DEKs)

Data Encryption Keys (DEKs) are cryptographic keys used to encrypt and decrypt data. DEKs are typically protected by other keys, such as Key Encryption Keys (KEKs), to ensure their security. DEKs play a critical role in safeguarding data confidentiality and are managed through key management services to maintain their lifecycle.

*Sources:* https://csrc.nist.gov/projects/key-management

### Data Lake

A data lake is a centralized repository that allows organizations to store vast amounts of structured and unstructured data at any scale. Data lakes support various data processing and analytics tools, enabling flexible data exploration, analysis, and machine learning across diverse data sources.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1500-4r2.pdf

### Data Security Posture Management (DSPM)

tools that protect sensitive data and ensure compliance with data protection regulations within cloud environments. They offer capabilities, such as data discovery, classification, encryption policy enforcement, and ensuring proper access controls to safeguard data against unauthorized access, data breaches, and insider threats. DSPM tools help maintain data privacy, integrity, and confidentiality across cloud-based applications, databases, and storage repositories.

*Sources:* https://csrc.nist.gov/publications/detail/sp/800-154/draft

### Data / Asset Classification

A way to approach security policy and its implementation that involves the classification of information into one of several categories, each of which has an associated security policy. Other assets such as servers and endpoints, can be similarly classified. In some cases, data can only be processed or stored on computers that share the same classification designation.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data Breach

A data breach occurs when unauthorized individuals gain access to sensitive or confidential information, such as personal information or financial data. Data breaches can occur due to a variety of reasons, such as cyber attacks, employee negligence, or physical theft. The consequences of a data breach can be severe, including financial loss, damage to reputation, and legal penalties. For example, a data breach at a healthcare organization may result in the theft of patient records, including medical history and personal information, which can be used for identity theft or sold on the dark web.

### Data Breach Prevention

Data Breach Prevention is the practice of implementing security measures and strategies to avoid unauthorized access or disclosure of sensitive information. This is important in the IAM domain to protect the confidentiality, integrity, and availability of data. Data Breach Prevention includes implementing access controls, monitoring user activities, regularly updating security policies, and ensuring that all security systems are up to date. For example, an organization may deploy multifactor authentication and data encryption to protect data from unauthorized access.

### Data Classification

The process to describe data’s business value to separate it into categories such as public, private, secret, to guide data handling procedures.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Data De-Identification

The process for removing identifying information from datasets, most commonly to protect the privacy of individuals, by using methods such as data masking. Data de-identification may also be used to protect organizations, such as businesses included in statistical surveys, or other information such as the spatial location of mineral or archaeological finds or endangered species.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data Discovery

Scanning and classifying data held in Network, Endpoint, and Server.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data Governance

As the organization manages data between Applications, Services, and Enterprise Information Integration activities, the need to have a well define governance model that outlines and looks for compliance on how data is massaged, transformed, and stored throughout the IT infrastructure including internal and external services (i.e., SaaS, PaaS, IaaS, ASP, or others).

*Sources:* Processes included in data governance include data ownership, how data should be classified, and responsibilities that data/ asset owners have for their applications and services, and the necessary controls for data throughout the lifecycle. | Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Data Historian

A centralized database located in the control system LAN supporting data archival and data analysis using statistical process control techniques.

*Sources:* https://www.us-cert.gov/ics/Control_System_Historian-Definition.html

### Data Life Cycle Management

The Data Life Cycle Management covers the following six phases: create, store, use, share, archive, and destroy. Although it is shown as a linear progression, once created, data may flow between stages without restriction, and may not pass through all stages during usefulness.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data Loss Prevention (DLP)

DLP refers to systems that enforce policies to safeguard critical data such as Intellectual Property and customer information and ensure it doesn’t escape from the enterprise to unintended parties. These solutions discover and classify sensitive data, define and manage policies based on content and context, monitor and enforce movement of data, as well as report, audit, and document incidents of data leakage.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data Masking

The process of obscuring (masking) specific data elements within data stores. It ensures that sensitive data is replaced with realistic but not real data. The goal is that sensitive data are not available outside of the authorized environment.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data Mining

Data mining is the ability to drill-down on KPIs and KQIs in order to find the underlying root cause for the indicators’ results. The actual data mining task can be an automatic or semi-automatic analysis of large quantities of data to extract previously unknown interesting patterns such as groups of data records (cluster analysis), unusual records (anomaly detection), and dependencies (association rule mining). These patterns can then be seen as a kind of summary of the input data and used in further analysis or, for example, in machine learning and predictive analytics. For example, the data mining step might identify multiple groups in the data, which can then be used to obtain more accurate prediction results by a decision support system.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Data Obscuring

A method of protecting fields or records of data by some form of obfuscation such as encryption. Data obscuring techniques can be used in source code, for example, to prevent reverse engineering of applications. There are also low tech solutions such as ink stamps to redact sensitive information on hard copies.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data Ownership / Stewardship

This capability manages the communications, responsibilities, and associated processes for personnel that interacts with data throughout its lifecycle. Roles associated with the data interaction include Data Owners, Asset Custodians, Data Users, Supporting Services, and Delegates.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Data Plane

Used for communication between software components. This communication channel may not be possible before the path has been established via the control plane.

*Sources:* SDP architectures separate the control of connections from the actual connections used to transfer data called the ‘data plane’. The data plane consists of two-way encrypted connections typically using mutual TLS or another mutual authentication mechanism. | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Data Protection

In the information age, data is an asset. However, most data is valuable only if it is protected. Data protection needs to cover all data lifecycle stages, data types, and data states. Data stages include create, store, access, roam, share, and retire. Data types include unstructured data such as word processing documents, structured data such as data within databases, and semi-structured data such as emails. Data states include data at rest (DAR), data in transit (DIT) (aka data in motion, data in flight), and data in use (DIU). Data Protection controls include data lifecycle management, data loss prevention, intellectual property protection with digital rights management, and cryptographic services such as key management and PKI/symmetric encryption.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data Protection Addendum (DPA)

A DPA consists of regulatory requirements stating data security and processing terms, including disclosure, security incident notification, data transfers, use of subprocessors, and compliance with data privacy regimes (e.g., GDPR, CCPA). DPAs are good practice for any organization to eliminate ambiguity with respect to organization data handling.

*Sources:* Recommendations for Adopting a Cloud-Native Key Management Service with an External Key Origin : CSA

### Data Seeding

A way of detecting and tracking data scraping, plagiarism, and theft is to seed the data with either easily identifiable items to trace where the data ends up or with bogus records to destroy the value of the data. For example, by inserting a record in a phone number database with an odd name, the true originator/owner could identify that bogus record if it appears in a competitor’s database.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data Segregation

Data segregation is the process and controls that ensure data is segregated in a multi-tenant environment, so each tenant has access to his and only his data

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Data Tagging

A data tag is a keyword or term assigned typically as a form of metadata to a piece of information. It helps describe an item and facilitates it being found again by browsing or searching.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data at Rest Encryption (DB, File, SAN, Desktop, Mobile)

Encryption of “Data at Rest” (data recorded on storage media).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data in Transit Encryption (Transitory, Fixed)

Encryption of “Data in Transit” (data being transferred between two nodes in a network).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data in Use Encryption (Memory)

Encryption of “Data in Use” (data in resident memory, or swap, or processor cache or disk cache, etc.).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Data, Applications, Assets, and Services (DAAS)

Data, Applications, Assets, and Services (DAAS) encompass the critical components that organizations must protect to ensure operational continuity and security. This includes sensitive data, software applications, physical and virtual assets, and essential services that support business functions.

*Sources:* https://www.nccoe.nist.gov/sites/default/files/2022-12/zta-nist-sp-1800-35a-preliminary-draft-2.pdf

### Database Storage

With respect to cloud-based storage, services that offer relational and non-relational databases that are highly scalable and can handle large amounts of unstructured data

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-209.pdf

### Database as a Service (DBaaS)

With respect to cloud-based database solutions, when DBaaS is used, the CSP provides the database capability and the customer configures and manages the database

*Sources:* https://www.ibm.com/topics/dbaas

### Database Events

Events regarding activity within the database management systems including logins, transactions, and administrative changes.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Database Monitoring

This capability is a collection of database management system related events, including logins, queries, transactions, and administrative activity.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Database Virtualization

Database virtualization is the decoupling of the database layer, which lies between the storage and application layers within the application stack. Virtualization at the database layer allows hardware resources to be extended to allow for better sharing resources between applications and users, masking of the physical location and configuration of a database from querying programs, as well as enable more scalable computing.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Databases (DBs)

Compliance testing against a collection of data that is organized so that its contents can easily be accessed, managed, and updated.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Deepfake

Falsified or faked media generated with a machine-learning system, specifically a deep neural network.

*Sources:* https://www.unite.ai/what-are-deepfakes/

### Default-drop Firewalls

Also known as: Drop-all Firewalls

*Sources:* The system should drop all TCP and UDP packets and not respond to those attempts, providing no information to potential attackers that the port is being monitored. After authentication and authorization, the user is granted access to the service. | https://s3.amazonaws.com/content-production.cloudsecurityalliance/78LUxxzkrWjbh625ALBt1jk9?response-content-disposition=inline%3B%20filename%3D%22SDP_Architecture_Guide_Web.pdf%22%3B%20filename%2A%3DUTF-8%27%27SDP_Architecture_Guide_Web.pdf&response-content-type=application%2Fpdf&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAS6XDIRHKHO4F5SU4%2F20220906%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220906T182512Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=3633d75a35c372f801c17a446ce92851ea411fb4a5ae988166a988693d4b06c3

### Defense-in-Depth

Information security strategy integrating people, technology, and operations capabilities to establish variable barriers across multiple layers and missions of the organization.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf

### Denial of Service (DoS)

The act of making a system, feature or resource unavailable for intended users. In cloud testing, denial of service often takes the form of destruction or encryption of cloud resources, disablement of accounts, credentials or users.

*Sources:* Cloud Penetration Testing : CSA

### Deployment

With respect to cloud deployments, an isolated environment within a cloud provider analogous to an AWS Account, an Azure Subscription, or a GCP Project.

*Sources:* https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-145.pdf

### Deprovisioning

Deprovisioning refers to the process of revoking access to resources when an employee or contractor leaves an organization or their role changes. This is a critical component of the IAM domain, as it ensures that former employees do not have access to sensitive information. Deprovisioning may involve disabling accounts, revoking permissions, and removing any associated digital certificates or keys. For instance, when an employee leaves an organization, their account should be deactivated, and access to their credentials should be revoked to prevent unauthorized access.

### Design patterns

reusable solutions to particular problems. In security, an example is IaaS log management. As with reference architectures, they can be more or less abstract or specific, even down to common implementation patterns on particular cloud platforms.

*Sources:* https://www.cs.ubc.ca/~gregor/teaching/papers/4+1view-architecture.pdf

### Desktop 'Client' Virtualization

Concerned with how virtual instances of the traditional desktop are created, presented and managed.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Desktops

Desktops are the classic computer that typically sits on or under a desktop and includes a CPU, monitor, keyboard, mouse, and other peripheral devices.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### DevOps

Application of software development methodologies to infrastructure operations.

*Sources:* As defined in ISO 27000 and Information Security Management through Reflexive Security : CSA .

### DevOps Research and Assessments (DORA) Metrics

Four key metrics that indicate the performance of software development teams. The metrics are focused on deployment frequency, lead time for changes, change failure rate, and time to restore service.

*Sources:* https://docs.gitlab.com/ee/user/analytics/dora_metrics.html

### DevSecOps (DSO)

The integration of continuous security principles, processes, and technologies into DevOps culture, practices, and workflows.

*Sources:* As defined in ISO 27000 and Information Security Management through Reflexive Security : CSA .

### Developer

A business or technology professional that builds software programs; a computer programmer (syn.) can refer to a specialist in one area of computers, or to a generalist who writes code for many kinds of software in one or more computer programming languages.

*Sources:* Wikipedia contributors. (2021b, August 7). Programmer. Wikipedia. https://en.wikipedia.org/wiki/ Programmer

### Development Process

The Development Process must address security concerns while the solution is being built using tools like source code scanners that can locate common security flaws in the code and web application vulnerability scanners that can test if a web application can be manipulated with common techniques used by hackers.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Device Attestation

The ability to provide proof that elements of the device (e.g., firmware) have not been tampered with.

*Sources:* SDPs should include a mechanism to prove that the proper device holds the private key and that the software running on the device can be trusted. Device attributes and contents (e.g. files, registry keys) may be used to validate the device. | https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.09082020-draft.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Device Onboarding Process

Involves the installation of the physical device and the setup of credentials so that it can securely communicate with its target cloud or platform.

*Sources:* Device onboarding for SDP entails the process of including new devices such as mobile phones, servers, and other IoT elements into an SDP. | https://media.fidoalliance.org/wp-content/uploads/2021/04/Introduction-to-FIDO-Device-Onboard-1.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Device agent / gateway-based deployment

In this deployment model, the PEP is divided into two components that reside on the resource or as a component directly in front of a resource.

*Sources:* https://csrc.nist.gov/publications/detail/sp/1800-35/draft

### Device application sandboxing

Another variation of the agent/gateway deployment model is having vetted applications or processes run compartmentalized on assets. These compartments could be virtual machines, containers, or some other implementation, but the goal is the same: to protect the application or instances of applications from a possibly compromised host or other applications running on the asset.

*Sources:* https://csrc.nist.gov/publications/detail/sp/1800-35/draft

### Digital Certificate

A Digital Certificate is an electronic document that verifies the identity of an entity and is used to establish secure communication between parties. In the IAM domain, digital certificates are commonly used for authentication and encryption purposes. They are issued by a trusted third party called a Certificate Authority (CA). For example, an organization may use digital certificates to authenticate the identity of employees accessing the network remotely or to encrypt sensitive data transmitted over the internet.

### Digital Rights Management

DRM is a term for access control technologies used by hardware manufacturers, publishers, copyright holders, enterprises, and individuals to limit the use of digital content and devices. The term has taken on at least two meanings. One refers to technology supporting the 1998 Digital Millennium Copyright Act to protect copyrighted media, maintain royalties, and ensure artistic control. The other definition applies to enterprise rights management technologies that attempt to put security controls closer to the enterprise data itself, often in encryption and metadata that carry access control information.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Directory Service

A Directory Service is a centralized database that stores and manages user and device identities and their attributes, such as access permissions, roles, and credentials. It is used to simplify and streamline user authentication and authorization in the IAM domain. For example, an organization may use a directory service such as Microsoft Active Directory to manage user identities and access permissions across multiple systems.

### Directory Traversal

A directory traversal occurs when you are able to traverse out of the current directory into parent directories, usually by supplying a series of “../” (dot dot slashes). Typically, directory traversal attacks allow the attacker to access or overwrite files that are not intended to be accessible.

*Sources:* https://www.sciencedirect.com/topics/computer-science/directory-traversal

### Disaster Recovery as a Service (DRaaS)

A cloud computing service model that allows an organization to back up its data and IT infrastructure in a third-party cloud computing environment from which it is possible to regain access and functionality to IT infrastructure after a disaster.

*Sources:* Disaster Recovery as a Service : CSA

### Discriminative Model

Learn about the boundary between classes within a dataset, with the goal to identify the decision boundary between classes to apply reliable class labels to data instances. Discriminative models separate the classes in the dataset by using conditional probability, not making any assumptions about individual data points.

*Sources:* https://www.unite.ai/generative-vs-discriminative-machine-learning-models/

### Distributed Denial-of-Service (DDoS)

Involves multiple computing devices in disparate locations sending repeated requests to a server with the intent to overload it and ultimately render it inaccessible.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-15.pdf

### Distribution and Segregation

Cloud resources are spread out and isolated, like compartmentalized sections of a large warehouse. Proper distribution and segregation ensure that a breach in one area does not compromise the entire system. That said, a degree of centralization of the logs is also required to provide an overview of the entirety of the cloud estate.

*Sources:* https://pecb.com/article/navigating-the-network-segmentation-vs-segregation

### Domain Name System (DNS) Poisoning

Results in a DNS resolver storing (i.e., caching) invalid or malicious mappings between symbolic names and IP addresses.

*Sources:* https://www.cs.cornell.edu/~shmat/shmat_securecomm10.pdf

### Domain Unique Identifier

A unique reference number used as an identifier in computer software (for example GUID, 32-character hexadecimal string, used for Microsoft’s implementation of the Universally unique identifier standard.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Dynamic Analysis (Fuzzing)

With respect to application pre-deployment testing, involves inputting unpredictable data into the software to identify errors and vulnerabilities that could be exploited during operation.

*Sources:* https://csrc.nist.gov/glossary/term/fuzz_testing

### Dynamic Vulnerability Scanning

With respect to post-deplyment testing, involves actively probing the running environment, and emulating real-world attack scenarios to identify vulnerabilities that could be exploited by malicious actors. Unlike static analysis, which examines code and configurations at rest, dynamic scanning assesses the system’s security posture in real time, providing insights into potential weaknesses that may have been missed during pre-deployment static analysis.

*Sources:* https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf

### Dynamic Application Security Testing (DAST)

Security testing that analyzes a running application by exercising application functionality and detecting vulnerabilities based on application behavior and response. Note 1 to entry: Also called “blackbox testing”

*Sources:* The Six Pillars of DevSecOps: Automation : CSA

### Dynamic Policies

Access to resources is determined by dynamic policy—including the observable state of client identity, application/service, and the requesting asset—and may include other behavioral and environmental attributes.

*Sources:* Policy is the set of access rules based on attributes that an organization assigns to a subject, data asset, or application. | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf

### Dynamic Tunnel Mode (DTM)

The proposed SDP protocol and encapsulation for the IH to communicate with one or more AHs.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf


## E

### E-Readers

A presentation modality that simulates the reading of a book or other printed material.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### E-mail

A presentation modality that presents an in-box of messages and allows users to send new messages or organize old messages into folders. Often email is combined with calendar functions and contact management functions.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### EMS (Energy Management System)

An energy management system (EMS) is a computer-aided tool used by power system operators to monitor, control, and carry out optimal energy management. The purpose of an EMS is to determine power generation or power demands that minimize a certain objective such as generation cost, power loss, or environmental effect.

*Sources:* https://www.sciencedirect.com/topics/engineering/energy-management-system

### ENISA Risk Management Process

Used by organizations to establish a robust framework for managing cloud risks, integrated with their overall risk management strategy and operational practices. This approach helps mitigate specific cloud-related risks and enhances the organization’s resilience and agility in navigating the complexities of the cloud computing environment.

*Sources:* https://csrc.nist.gov/glossary/term/enisa

### Economic Denial of Service (EDoS)

EDoS attacks exploit the elasticity of clouds, particularly auto-scaling capabilities, to inflate the billing of a cloud user until the account reaches bankruptcy or large-scale service withdrawal.

*Sources:* https://www.cisa.gov/news-events/news/understanding-denial-service-attacks

### Elasticsearch

An open-source, distributed data search and analytics engine built on Apache Lucene. You can send data in the form of JSON documents to Elasticsearch using the RESTful API or ingestion tools such as Logstash. Elasticsearch automatically stores the original document and adds a searchable reference to the document in the cluster’s index. You can then search and retrieve the document using the Elasticsearch API. Amazon provides fully managed Elasticsearch services that enables you to deploy, secure, and run Elasticsearch at scale.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

### Electronic Surveillance

Continuous observation of an area to detect intrusion, record access and monitor movement.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Elevation of Privileges

The act of leveraging a vulnerability or configuration to enable or achieve an elevation of access or privilege beyond what was intended. In cloud testing, elevation of privileges often takes the form leveraging misconfigured IAM permissions that allow escalation or permissions employed by compromised or targeted services and systems.

*Sources:* Cloud Penetration Testing : CSA

### Email Journaling

Monitoring the contents of email to detect data loss, malware spread, or other email-based threats. Email journaling is the processes and procedures that ensure all email traffic is recorded and preserved as required for regulatory compliance or support litigation.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Email Security

Provides control over inbound and outbound email, protecting the organization from phishing, malicious attachments, and spam, and providing business continuity options.

*Sources:* Defined Categories of Service 2011 : CSA

### Emergency Changes

Changes generated to fix an issue on a production service or application.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Employee Awareness

This capability will focus on the management of materials and tools associated with the process of providing awareness to ensure compliance with regulatory requirements, security policies, and risk management best practices that will ensure that the organization will have a secure, compliant, and safe working environment. Examples of this include Clean-Desk Policy, Disaster Recovery, On-Line training, PII/PHI information protection, among others.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Employee Code of Conduct

This capability is intended to manage the lifecycle for a formal agreement between the personnel that interacts with the organization’s data, assets, and services. The code of conduct must include expected behavior relevant to the organization from the Regulatory perspective, Information Security Policies and Risk Management best practices.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Employee Identity Management

Encryption is the process of converting plaintext into ciphertext using an algorithm and a key. It is used to protect the confidentiality of data in transit or at rest. Encryption is an essential component of the IAM domain, as it helps to prevent unauthorized access to sensitive information. For example, an organization may use encryption to protect sensitive data transmitted over the internet or stored on a device.

### Employee Termination

The process for ensuring that an employee exit procedure minimizes the risk of an ex-employee misusing information assets after their term of employment. The process includes access removal to electronic accounts typically, turn off VPN or external email services, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Employment Agreements

All contractual agreements entered between the organization and the employees, contractors, third party users, and customers, which specify the terms and conditions of their employment or service contract before granting access to data and services, which must explicitly include the parties responsible for information security. Examples include a privacy policy, intellectual property agreements, acceptable use, website terms, and conditions.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Enclave-based deployment

This deployment model is a variation of the device agent/gateway model. In this model, the gateway components may not reside on assets or in front of individual resources but instead reside at the boundary of a resource enclave (e.g., on-location data center).

*Sources:* https://csrc.nist.gov/publications/detail/sp/1800-35/draft

### Encryption

The process of obfuscating data using cryptographic and numerical ciphers. Transforming clear-text into cipher-text to make it unreadable.

*Sources:* Defined Categories of Service 2011 : CSA

### Encryption

Encryption is the process of converting plain text into an unreadable format using a cryptographic algorithm to protect the confidentiality, integrity and availability of data. In the context of IAM within Information Security, encryption is commonly used to protect sensitive data such as passwords, authentication tokens, and personal information stored in databases or transmitted over networks. Encryption helps to prevent unauthorized access, interception, or modification of the data by attackers or eavesdroppers. There are various encryption techniques and algorithms available, such as symmetric key encryption, asymmetric key encryption, and hashing. An example of encryption in IAM is the use of encrypted passwords. When users create an account, they are prompted to create a password. The password is then encrypted and stored in a database in an unreadable format using a strong encryption algorithm. When the user logs in, the password they enter is also encrypted and compared to the stored encrypted password. If the two encrypted values match, the user is granted access. This way, even if an attacker gains access to the database, they will not be able to read the passwords in plain text and use them to gain unauthorized access to the system.

### Endpoint

Computing devices used by users (e.g., desktop, tablet, smartphone).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Endpoint Detection and Response (EDR)

Agents that perform runtime monitoring and some support vulnerability assessment.

*Sources:* https://csrc.nist.gov/glossary/term/endpoint_detection_and_response

### Endpoint (Data in Use)

See Data in Use Encryption (DLP in this case)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Endpoint Monitoring

Collection of events associated with end user usage of devices.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Endpoints

Endpoints are the devices that users interact with when using an IT solution. They are called Endpoints because they are at the edge of the solution where technology meets humans.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Enterprise Architect

The individual or organization responsible for strategic design recommendations. They determine, by applying their knowledge of cloud, container and microservices components to the problems of the business; the best architecture to meet the strategic needs of the business. Additionally, they develop and maintain solution roadmaps and oversee their adoption working with Developers and Operators to ensure an efficient and effective solution implementation.

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Enterprise Architecture

Is both a methodology and a set of tools that enable security architects, enterprise architects and risk management professionals to fulfill a set of common requirements that risk managers must use to assess the operational status of internal IT security and cloud provider controls.

*Sources:* https://cloudsecurityalliance.org/research/working-groups/enterprise-architecture/

### Enterprise Operator

The individual or organization responsible for the set of processes to deploy and manage IT services. They ensure the smooth functioning of the infrastructure and operational environments that support application deployment to internal and external customers, including the network infrastructure, server and device management, computer operations, IT infrastructure library (ITIL) management, and help desk services.

*Sources:* Wikipedia. Information technology operations. Retrieved from https://en.wikipedia.org/wiki/Information_ technology_operations

### Enterprise Service Bus (ESB)

An Enterprise Service Bus (ESB) is a type of software platform known as middleware, which works behind the scenes to aid application-to-application communication. Think of an ESB as a “bus” that picks up information from one system and delivers it to another. An ESB provides a secure, scalable and cost-effective infrastructure that enables real-time data exchange among many systems. Data from one system, known as a service provider, can be put on the enterprise service bus as a message, which is sent immediately to a service consumer of the data. If a new system wants to consume this same data, all it has to do is plug into the bus in the same manner.

*Sources:* https://it.ucla.edu/news/what-esb

### Enterprise Service Platform

This container holds the various types of presentation modalities oriented to enterprise users in the workplace, or towards customers and partners of an enterprise.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Enterprise risk management (ERM)

An effective agency-wide approach to addressing the full spectrum of the organization’s significant risks by understanding the combined impact of risks as an interrelated portfolio, rather than addressing risks only within silos.

*Sources:* https://csrc.nist.gov/glossary/term/enterprise_risk_management

### Entitlement

An entitlement maps identities to authorizations and any required attributes (e.g. user x is allowed access to resource y when z attributes have designated values). We commonly refer to a map of these entitlements as an entitlement matrix. Entitlements are often encoded as technical policies for distribution and enforcement.

*Sources:* https://downloads.cloudsecurityalliance.org/assets/research/security-guidance/security-guidance-v4-FINAL.pdf?_ga=2.141556790.523273906.1661959123-2107700575.1655484199

### Entitlement Review

A process checking appropriate existing user and role authorization access.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Entity

An entity refers to a unique, identifiable actor in a computer system. In the context of cybersecurity, an entity can be a user, a device, an application, or a system that is identified and authenticated by an IAM system. Entities can have different roles and permissions within the system, and their actions and access to resources are typically logged for auditing and security purposes. An individual (person), organization, device, or process. Used interchangeably with “party”. (Ref: NIST SP 800-102, NIST SP 800-89, NIST SP 800-152, NIST SP 800-175B Rev. 1, NIST SP 800-56B Rev. 2, NIST SP 800-57 Part 1 Rev. 5) A person, device, service, network, domain, manufacturer, or other party who might interact with an IoT device. (Ref: NIST SP 800-213, NISTIR 8259A, NISTIR 8259B)

### Entropy source

The combination of a noise source—such as a Quantum Random Number Generator, health tests and an (optional) conditioning component—to produce full-entropy random bits [NIST].

*Sources:* [NIST] M. S. Turan, E. Barker, J. Kelsey, K. A. McKay, M. L. Baish and M. Boyle. Recommendation for the Entropy Sources Used for Random Bit Generation (Second DRAFT). NIST Special Publication 800-90B, 2016.

### Environment Classification

In a cloud deployment registry, this is used to distinguish between different types of environments, such as development, staging, and production. This classification helps manage and govern each environment based on its specific requirements.

*Sources:* https://csrc.nist.gov/pubs/sp/800/145/final

### Environment ID

In a cloud deployment registry, a unique identifier to each cloud environment to facilitate tracking and management. This ID should appear in logs and other monitoring tools, providing a precise reference point for each environment.

*Sources:* https://csrc.nist.gov/pubs/sp/800/145/final

### Environmental Risk Management

The general process of assessing and controlling risks arising from the environment surrounding an infrastructure (e.g., estimating the size of a backup generator plant to provide power continuity in case of utility power loss).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Ephemeral workloads

Also knows as short-running workloads, in a cloud-native architecture, most workloads operate under the short-running model. These are transient services – they come and go as needed, sometimes only existing for a brief period to handle specific tasks or workloads. Security in short-running workloads is proactive and baked in; it is part of the creation process of the VM or container image and does not require manual configuration or post-deployment.

*Sources:* https://csrc.nist.gov/pubs/sp/800/145/final

### Equipment Location

The processes and procedures involved in siting equipment in appropriate locations (e.g., locating critical network equipment is a secured room with redundant power, temperature controls, etc.).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Equipment Maintenance

Concerned with assuring that physical infrastructure devices are appropriately maintained to assure their continuous operations. Examples include periodic inspection, cleaning and replacement of air filters, proactive replacement of components when degradation is detected, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Evaluation

Evaluation in the context of IT and cybersecurity refers to the process of systematically examining and assessing the performance, effectiveness, and compliance of systems, controls, and processes. It involves measuring against predefined criteria or benchmarks to determine whether objectives are being met and identifying areas for improvement. Evaluation is a critical component of risk management, helping organizations ensure that their security measures are effective and aligned with their goals.

*Sources:* https://csrc.nist.gov/glossary/term/evaluation_criteria

### Event Classification

An event may or may not indicate that an incident has occurred or is in progress. Event classification provides processes for analysis and event correlation to provide an assessment and confidence estimate for the occurrence of an incident

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Event Correlation

Process of analyzing and associating an event from one source with events from the same or other sources to derive additional information or detect activity patterns.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Event Mining

Statistical analysis of historical events to determine patterns of normal and abnormal behavior.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Events

Events in the context of information security refer to occurrences within a system or network that can be significant for security, operational, or troubleshooting purposes. These events are often logged and monitored to detect anomalies, security breaches, or system failures.

*Sources:* https://csrc.nist.gov/glossary/term/event

### Exceptions

A deviation that includes granting an exception to a standing policy when it cannot be met or can only partially be met. In this way, the Information Security team is aware of a scenario that is out of compliance and can, therefore, understand the associated risk and monitor the exception. Sometimes the exception is time-bound and reviewing periodically to assess risk and allow a remediation plan to be met.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### External

Focuses on the ability of a remote attacker to get to the internal network. This form of penetration testing aims to access data located within the internal network by exploiting externally exposed devices, including servers, clients, applications and wireless access points.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### External (VLAN)

a VLAN is a group of hosts (on premise, in the cloud, between clouds or hybrid) with a common set of requirements that communicate as if they were attached to the same broadcast domain, regardless of their physical location.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### External SLAs

Service Level Agreements with external entities that codify the specific services to be delivered and the performance criteria governing that delivery.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### eDiscovery

e-discovery is concerned with how data responsive to a planned or ongoing litigation is identified, preserved, and produced.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### eDiscovery Events

Electronic Discovery (eDiscovery) Events regarding retention of data for legal hold and investigation purposes.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### eSignature (Unstructured Data)

An electronic signature indicates that a person adopts the contents of digital data or that the person who claims to have written a message is the one who wrote it. This is most frequently used on unstructured data.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### eXtensible Access Control Markup Language (XACML)

is a standard for defining attribute-based access controls and authorizations. It is a policy language for defining access controls at a Policy Decision Point (PDP) and then passing them to a Policy Enforcement Point (PEP).

*Sources:* https://csrc.nist.gov/publications/detail/sp/800-178/final


## F

### FIDO (Fast IDentity Online)

Maintained by the FIDO Alliance and also known as passkeys or webauthz, FIDO represents a technology step forward by providing a phishing-resistant authentication method. FIDO allows the user to define trusted devices that can be used as authentication factors during the login process. FIDO can also be enhanced with physical tokens that are plugged into or wireless connected to the access device.

*Sources:* https://csrc.nist.gov/glossary/term/fido

### Facility Security

Concerned with the security controls applied at the cloud computing facility that assure a safe and secure operational environment for the physical components of a cloud infrastructure. Examples include restrictions applied to physical access, environmental controls, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Factor Analysis for Information Risk (FAIR)

Factor Analysis for Information Risk (FAIR) is a quantitative risk analysis framework that helps organizations understand, analyze, and quantify information risk. FAIR provides a structured approach to measure the probable frequency and magnitude of loss from cybersecurity events. It is used to improve risk management decisions by providing a consistent and repeatable methodology for assessing risks.

*Sources:* https://www.fairinstitute.org/

### Fault Injection

A method to evaluate the effect of a fault (3.54) within an element (3.41) by inserting faults (3.54), errors (3.46), or failures (3.50) in order to observe the reaction by observation points (3.101). Fault injection can be performed at various levels of abstraction including item (3.84) or element (3.41) level depending on the scope, feasibility, observability and level of required detail. Depending on purpose, it can be performed at different stages of the safety lifecycle and by considering different faultmodels (3.58).

*Sources:* https://www.iso.org/obp/ui#search

### Federal Information Processing Standard (FIPS)

The international standard for certifying the protection levels of cryptographic modules.

*Sources:* Key Management in Cloud Services: Understanding Encryption’s Desired Outcomes and Limitations : CSA

### Federated Identity Brokers (FIM)

Allows users to access multiple systems or applications using a single set of credentials, often provided by an Identity Provider (IdP). This is the key enabler of Single Sign-On (SSO) and is a core capability in cloud computing.

*Sources:* https://csrc.nist.gov/glossary/term/federated_identity_management

### Federated IDM

Refers to a new standard based approach to directory services that streamlines and secures user access to networked resources, with the ability to establish trust relationships between various security domains to enable the passing of authentication, authorization, and privacy assertions.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Federated Identity

Federated Identity allows users to access multiple systems or applications using a single set of credentials, often provided by an Identity Provider (IdP).

*Sources:* https://www.gartner.com/en/information-technology/glossary/ federated-identity-management#:~:text=Federated%20identity%20 management%20enables%20identity,entities%20and%20across%20 trust%20domains

### Federated Identity Management

The process of asserting an identity across different systems or organizations. This is the key enabler of Single Sign On and also core to managing IAM in cloud computing.

*Sources:* https://downloads.cloudsecurityalliance.org/assets/research/security-guidance/security-guidance-v4-FINAL.pdf?_ga=2.225992666.1359049959.1661450515-2107700575.1655484199

### Federated Services

Information regarding the trust between an organization’s directories and 3rd party directories.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### FileBased Virtualization

A higher-level view of files that make the file largely independent of how it is presented. For example, a consumer would access mybudget.global without regard to whether it was hosted in a NAS appliance, a SAN or on a physical server.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Firewall

An inter-network connection device that restricts data communication traffic between two connected networks. A firewall may be either an application installed on a general-purpose computer or a dedicated platform (appliance), which forwards or rejects/drops packets on a network. Typically firewalls are used to define zone borders. Firewalls generally have rules restricting which ports are open.

*Sources:* SDP architectures can enforce a ‘deny-all’ firewall policy ensuring that the trusted network enabled by SDP ensures the SDP will not respond to any connections from any clients until they have provided an authentic SPA. | https://csrc.nist.gov/glossary/term/firewall | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Forensic Analysis

Forensic analysis is concerned with preserving, identifying, extracting, and analyzing potential evidentiary value items relevant to questions of fact regarding a policy or criminal violation.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Forensic Tools

Assures that the proper tools are available to authorized parties and processes to facilitate identification and preservation of relevant digital artifacts pertinent to an investigation (e.g., policy violation, e-discovery request or criminal investigation)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Foundation Model

Also know as general-purpose AI, they are designed to produce a wide and general variety of outputs. They are capable of a range of possible tasks and applications, such as text, image or audio generation. They can be standalone systems or can be used as a ‘base’ for many other applications.

*Sources:* https://www.adalovelaceinstitute.org/resource/foundation-models-explainer/

### Fourth Industrial Revolution

The phrase Fourth Industrial Revolution was first introduced by Klaus Schwab, executive chairman of the World Economic Forum. In the 2015 article in Foreign Affairs, “Mastering the Fourth Industrial Revolution” was the theme of the World Economic Forum Annual Meeting 2016 in Davos-Klosters, Switzerland. On October 10, 2016, the Forum announced the opening of its Centre for the Fourth Industrial Revolution in San Francisco. This was also the subject and title of Schwab’s 2016 book. Schwab includes in this fourth era technologies that combine hardware, software, and biology (cyberphysical systems), and emphasizes advances in communication and connectivity. This Fourth Industrial Revolution is, however, fundamentally different. It is characterized by a range of new technologies that are fusing the physical, digital and biological worlds, impacting all disciplines, economies and industries, and even challenging ideas about what it means to be human. The resulting shifts and disruptions mean that we live in a time of great promise and great peril. The world has the potential to connect billions of more people to digital networks, dramatically improve the efficiency of organizations and even manage assets in ways that can help regenerate the natural environment, potentially undoing the damage of previous industrial revolutions. (WEFORUM)

*Sources:* https://www.weforum.org/about/the-fourth-industrial-revolution-by-klaus-schwab

### Full

A fully virtualized environment or fabric that includes processor, storage and network capabilities. Can be provided as part of a physical machine or across multiple physical machines.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Function as a Service (FaaS)

Also known as serverless, a cloud computing model whereby developers write and deploy individual functions that are executed in response to events or requests, without the need to manage the underlying infrastructure. This serverless model entrusts a greater share of security responsibilities to the CSP.

*Sources:* https://www.ibm.com/topics/faas#:~:text=Function%20as%20a%20service%20(FaaS)%20is%20a%20cloud%2Dcomputing,building%20and%20launching%20microservices%20applications .

### Fuzz Testing

Similar to fault injection in that invalid data is input into the application via the environment, or input by one process into another process. Fuzz testing is implemented by tools called fuzzers, which are programs or script that submit some combination of inputs to the test target to reveal how it responds.

*Sources:* https://csrc.nist.gov/glossary/term/fuzz_testing


## G

### GOVERN (GV)

In the NIST Cybersecurity Framework (CSF), the process that is used to establish and monitor the organization’s cybersecurity risk management strategy, expectations, and policy.

*Sources:* https://www.nist.gov/blogs/blogrige/cybersecurity-framework-20-expands-scope-and-adds-focus-governance

### GRC

Governance, Risk and Compliance (GRC) describes the overall management approach through which senior executives direct and control the entire organization, using management information and hierarchical management control structures. Governance activities ensure that critical information reaching the executive team is sufficiently complete, accurate, and timely to enable appropriate management decision making and provide the control mechanisms to ensure that strategies, directions, and instructions from management are carried out systematically and effectively. Risk management is the set of processes through which management identifies, analyzes, and, where necessary, responds appropriately to risks that might adversely affect realization of the organization’s business objectives. The response to risks typically depends on their perceived gravity, and involves controlling, avoiding, accepting or transferring them to a third party. Whereas organizations routinely manage a wide range of risks (e.g. technological risks, commercial/financial risks, information security risks etc.), external legal and regulatory compliance risks are arguably the key issue in GRC. Compliance means conforming with stated requirements. At an organizational level, it is achieved through management processes which identify the applicable requirements (defined for example in laws, regulations, contracts, strategies and policies), assess the state of compliance, assess the risks and potential costs of non-compliance against the projected expenses to achieve compliance, and hence prioritize, fund and initiate any corrective actions deemed necessary.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Gap analysis

Gap analysis consists of (1) listing of attributes, competencies, and/or performance levels of the present situation (“what is”), (2) cross listing factors required to achieve the future objectives (“what should be”), and then (3) highlighting the gaps that exist and need to be filled.

*Sources:* https://www.hsph.harvard.edu/wp-content/uploads/sites/1678/2014/10/Gap_Analysis.pdf

### Gateway (SDP Gateway)

Provides authorized users and devices with access to protected processes and services. The gateway can also enact monitoring, logging, and reporting on these connections.

*Sources:* An SDP gateway is an appliance or process that, once a user or device is authorized, allows access to protected processes or services. This gateway can also be used to effectively allow monitoring, logging, and reporting on connections protecting processes or services. | https://cloudsecurityalliance.org/artifacts/sdp-architecture-guide-v2/ | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### General Data Protection Regulation (GDPR)

The General Data Protection Regulation (GDPR) is the toughest privacy and security law in the world. Though it was drafted and passed by the European Union (EU), it imposes obligations onto organizations anywhere, so long as they target or collect data related to people in the EU. The regulation was put into effect on May 25, 2018. The GDPR will levy harsh fines against those who violate its privacy and security standards, with penalties reaching into the tens of millions of euros.

*Sources:* https://gdpr.eu/what-is-gdpr/

### Generative AI

Any type of artificial intelligence system that relies on unsupervised or semi-supervised learning algorithms to create new digital images, video, audio, and text so that computers can learn fundamental patterns relevant to input, which enables them to output similar content. These systems rely on generative adversarial networks (GANs), variational autoencoders, and transformers.

*Sources:* https://www.unite.ai/what-is-generative-ai/

### Generative Adversarial Network

Types of neural network architectures capable of generating new data that conforms to learned patterns. GANs can be used to generate images of human faces or other objects, to carry out text-to-image translation, to convert one type of image to another, and to enhance the resolution of images (super resolution) among other applications.

*Sources:* https://www.unite.ai/what-is-a-generative-adversarial-network-gan/

### Generative Model

Center on the distribution of the classes within the dataset. The machine learning algorithms typically model the distribution of the data points. Generative models rely on finding joint probability. Creating points where a given input feature and a desired output/label exist concurrently.

*Sources:* https://www.unite.ai/generative-vs-discriminative-machine-learning-models/

### Generative Pre-trained Transformer

A complex mathematical representation of text or other types of media that allows a computer to perform some tasks, such as interpreting and producing language, recognizing or creating images, and solving problems, in a way that seems similar to the way a human brain works.

*Sources:* https://dictionary.cambridge.org/us/dictionary/english/gpt

### Geolocation

Provides access to geographical location information associated with the hosting device.

*Sources:* Geolocation can be used as a source of information upon which to make access decisions in an SDP. For example, access to resources from users located in certain countries may be blocked. SDPs may also compare user geolocation with connection attempts to detect credential theft. | https://www.w3.org/TR/geolocation/ | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Governance

Governance is the method by which an enterprise ensures that: Stakeholder needs, conditions and options are evaluated to determine balanced, agreed-on enterprise objectives. Direction is set through prioritization and decision-making. Performance and compliance are monitored against agreed-on direction and objectives.

*Sources:* Management plans, builds, runs and monitors activities in alignment with the direction set by the governance body to achieve enterprise objectives | https://www.isaca.org/resources/news-and-trends/industry-news/2020/effective-capability-and-maturity-assessment-using-cobit-2019

### Governance Hierarchy

A Governance Hierarchy refers to the structured framework within an organization that defines the levels of authority, roles, and responsibilities for decision-making and oversight of governance processes. This hierarchy ensures that governance policies and procedures are effectively implemented and monitored at various levels of the organization, facilitating accountability and compliance with regulatory requirements.

*Sources:* https://www.nist.gov/cyberframework/online-learning/components-framework

### Governance Risk & Compliance

The fundamental issues of governance and enterprise risk management in Cloud Computing concern the identification and implementation of the appropriate organizational structures, processes, and controls to maintain effective information security governance, risk management and compliance. GRC encompasses, integrates and aligns activities such as corporate governance, enterprise risk management, and corporate compliance with applicable laws and regulations. Components include: a. compliance management (which assures compliance with all internal information security policies and standards), b. vendor management (to ensure that service providers and outsourcers adhere to intended and contractual information security policies applying ownership and custody), c. audit management (to highlight areas for improvement), d. IT risk management (to ensure that risk of all types is identified, understood, communicated, and either accepted, remediated, transferred or avoided), e. policy management (to maintain an organizational structure and process that supports the creation, implementation, exception handling, and frameworks that support business requirements), and f. technical awareness and training (to increase the ability to select and implement effective technical security mechanisms, products, processes, and tools).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Graphics Processing Units (GPUs)

Graphics Processing Units (GPUs) are specialized electronic circuits designed to accelerate the processing of images and videos. GPUs are widely used in various applications, including computer graphics, artificial intelligence, and high-performance computing, due to their ability to handle parallel processing efficiently.

*Sources:* https://www.intel.com/content/www/us/en/products/docs/processors/what-is-a-gpu.html

### Group

With respect to cloud deployments, a collection of deployments, similar to an AWS Organization Unit, an Azure Management Group, or a GCP Folder.

*Sources:* https://csrc.nist.gov/pubs/sp/800/145/final

### Grover’s algorithm

This is an algorithm named after L.K. Grover [Grover96]. The algorithm provides a quadratic speed-up for an exhaustive search on quantum computers. It was designed as a database search algorithm, but can be used to reduce the cryptographic strength of symmetric algorithms by half.

*Sources:* [Grover96] Lov K. Grover. A Fast Quantum Mechanical Algorithm for Database Search. STOC 1996.

### Guardrails

Guardrails in product development are typically a set of metrics that define boundaries and help guide the decision-making process for product development. Metrics keep organizations and product teams on the right track and are used as a tool to ensure that what you’re doing is aligned with your business goals and objectives.

*Sources:* https://cisr.mit.edu/publication/2020_0801_DecisionRights_Meulen


## H

### HIPS / HIDS

Host Intrusion Detection Systems (HIDS) can detect actions that attempt to compromise the confidentiality, integrity, or availability of a resource. Host Intrusion Prevention Systems (HIPS) includes taking a preventive measure without direct human intervention.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### HMI (Human Machine Interface)

A Human-Machine Interface (HMI) is a user interface or dashboard that connects a person to a machine, system, or device. While the term can technically be applied to any screen that allows a user to interact with a device, HMI is most commonly used in the context of an industrial process. In industrial settings, HMIs can be used to visually display data, track production time, trends, and tags, oversee key performance indicators, and monitor machine inputs and outputs.

*Sources:* https://www.inductiveautomation.com/resources/article/what-is-hmi

### HR Data (Employees & Contractors)

Information regarding the employees and contractors of an organization that can be used for various processes including access control, business continuity planning, data governance, and background checks.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Handling / Labeling / Security Policy

This capability manages policies, procedures, and communication associated with labeling, handling, and security of data and objects which contain data.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Handwriting (ICR)

Handwriting, or interactive character recognition (ICR) can translate handwritten text into computer input.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Presentation Services

### Hard tokens

physical devices that generate one-time passwords for human entry or need to be plugged into a reader.

*Sources:* https://www.cdw.com/content/cdw/en/articles/security/hard-tokens-vs-soft-tokens.html

### Hardware

Generally, physical items of equipment used in providing infrastructure services (e.g., a server, a router, etc.).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Hardware Assisted

Support in a given processor architecture for hypervisor execution (usually through provision of specialized instructions that support switching between guest instances, etc).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Hardware Based Trusted Assets

Assets with trust rooted to hardware (e.g. computers with TPM chip).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Hardware Security Modules (HSMs)

Are hardened, tamper-resistant hardware devices that strengthen encryption practices by generating keys, encrypting and decrypting data, and creating and verifying digital signatures.

*Sources:* https://cpl.thalesgroup.com/faq/hardware-security-modules/what-general-purpose-hardware-security-module-hsm

### Hash Functions

A hash function is a cryptographic function that takes a variable-length of input and produces a fixed-length output. It takes an input text — no matter how long or small it is — but the hash function’s output will always be in a fixed length. Hash functions are used for data integrity and often in combination with digital signatures.

*Sources:* https://www.sciencedirect.com/topics/computer-science/hash-function

### Hash-based cryptography

This is a sub-area of quantum-safe cryptography which refers to signature schemes whose security are based on the hardness of finding a collision in a hash-function. The signature schemes are usually constructed by combining a one-time signature scheme or few time signature scheme with a Merkle tree. Some examples are the Leighton-Micali scheme [LM], SPHINCS [SPHINCS], and XMSS [XMSS].

*Sources:* [LM] F.T. Leighton and S. Micali. Large Provably Fast and Secure Digital Signature Schemes based on Secure Hash Functions. US Patent 5,432,852, July 11, 1995. | [SPHINCS] D. J. Bernstein, D. Hopwood, A. Hülsing, T. Lange, R. Niederhagen, L. Papachristodoulou, M. Schneider, P. Schwabe and Z. Wilcox-O’Hearn. SPHINCS: Practical Stateless Hash-Based Signatures. EUROCRYPT 2015. | [XMSS] J. Buchmann, E. Dahmen, and A. Hülsing. XMSS - a Practical Forward Secure Signature Scheme Based on Minimal Security Assumptions. Post-Quantum Cryptography, 2011.

### Hashed One-Time Password (HOTP)

This hashed one-time password (hashed OTP) is generated by an algorithm as described by RFC 4226, based on a shared secret. The use of an OTP is required in SPA packets to establish authenticity; other OTP algorithms can be substituted with the overarching goal of providing authenticity of the SPA packet.

*Sources:* https://cloudsecurityalliance.org/artifacts/software-defined-perimeter-zero-trust-specification-v2/

### Hidden Field Equations (HFE)

This is multivariate public-key scheme (encryption and signature) proposed by J. Patarin [HFE] in 1996. HFEv- [PCG01] is a secure variant of HFE which only permits a signature that can not be utilized to encrypt data.

*Sources:* [HFE] J. Patarin. Hidden Fields Equations (HFE) and Isomorphisms of Polynomials (IP): Two New Families of Asymmetric Algorithms. EUROCRYPT’96. | [PCG01] J. Patarin, N. Courtois, and L. Goubin. Quartz. 128-bit Long Digital Signatures. CT-RSA’01.

### High Availability (HA)

​​High availability means that an IT system, component, or application can operate at a high level, continuously, without intervention, for a given time period. High-availability infrastructure is configured to deliver quality performance and handle different loads and failures with minimal or zero downtime.

*Sources:* https://www.cisco.com/c/en/us/solutions/hybrid-work/what-is-high-availability.html

### Honey Pot

A real or virtual system configured to attract and detect an intruder by mirroring a real production system.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Host

OS supporting the container environment.

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Host Network

With respect to docker networking, a mode where containers share the same network stack as the host machine. This means containers directly access the host’s network interfaces and can bind to host ports. However, this mode sacrifices network isolation for simplicity.

*Sources:* https://docs.docker.com/network/network-tutorial-host/

### Host Based

Virtualized file systems may be presented by a server (e.g., a file server that provides several file shares).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Host Firewall

A software program or function running on a single host that can restrict incoming and outgoing network activity for that host only.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Human Resources Security

This section focuses on the security and risk management perspective for those processes and best practices associated with the interaction that persons (employees, contractors, or any other third-party) have with the organization’s human resources function.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Hybrid Cloud

The cloud infrastructure is a composition of two or more distinct cloud infrastructures (private, community, or public) that remain unique entities, but are bound together by standardized or proprietary technology that enables data and application portability (e.g., cloud bursting for load-balancing between clouds).

*Sources:* NIST 2011, The NIST Definition of Cloud Computing, https://csrc.nist.gov/publications/detail/ sp/800-145/final

### Hybrid multi-cloud

Refers to an organization that uses multiple public clouds from several vendors to deliver its IT services, in addition to private cloud and traditional on-premises IT. A hybrid multi-cloud environment consists of a combination of private, public and hybrid infrastructure-as-a-service (IaaS) environments all of which are interconnected and work together to avoid data silos. Many enterprise companies are failing to make their various data repositories and systems ‘talk to each other’ effectively and efficiently, if at all. The result: more data silos that hinder or prevent data movement and sharing. With a modern hybrid multi-cloud architecture in place, you gain access to a single source of truth as it relates to your data. If optimized properly, you can quickly access data that is reliable and accurate. Moreover, data that is unified in one location is accessible whether it resides on-premises or off-premises.

*Sources:* IBM, Hybrid cloud: The best of all worlds, https://www.ibm.com/downloads/cas/E97LZYVG

### Hypertext Transport Protocol Secure (HTTPS)

A secure network communication method, technically not a protocol in itself, HTTPS is the result of layering the hypertext transfer protocol (HTTP) on top of the SSL/TLS protocol, thus adding the security capabilities of SSL/TLS to standard HTTP communications.

*Sources:* SDPs require mutual TLS and provides additional user verification not provided by HTTPS. | https://iapp.org/resources/article/hypertext-transfer-protocol-secure/ | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Hypervisor Compliance and Governance

The capability of privilege management and monitoring by role and user associated with hypervisor administrators. This also includes the management of virtual networks, servers, and applications in a cloud environment.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain


## I

### IAM Principal

A principal is a human user or workload that can request for an action or operation on a CSP resource.

*Sources:* https://medium.com/@reach2shristi.81/aws-principal-vs-identity-3d8eacc5377f

### IANS Cloud Security Maturity Model (CSMM)

The IANS Cloud Security Maturity Model (CSMM) is a framework designed to help organizations assess and improve their cloud security posture. The model outlines stages of maturity from initial to optimized, providing guidance on best practices and processes to achieve higher levels of cloud security and governance. It assists organizations in identifying gaps and implementing strategies to enhance their overall cloud security capabilities.

*Sources:* https://sf-cdn.iansresearch.com/sitefinity/docs/default-source/ians-documents/csmm/intro_to_the_cloud_security_maturity_model_2.0.pdf?sfvrsn=d46e587_1/Intro_to_the_Cloud_Security_Maturity_Model_2.0.pdf

### IDENTIFY (ID)

In the NIST Cybersecurity Framework (CSF), the process that is used to help determine the current cybersecurity risk to the organization.

*Sources:* https://www.nist.gov/cyberframework/identify

### IEC (International Electrotechnical Commission)

Founded in 1906 IEC prepares and publishes International Standards for all electrical, electronic and related technologies. These are known collectively as “electrotechnology”. The IEC is one of three global sister organizations (IEC, ISO, ITU) that develop International Standards for the world. Of particular interest to the CSA WG is IEC’s work on the IEC-62443 series of standards addressing Security for industrial automation and control systems. The IEC-62443 series of standards was adopted from the ISA-99 series developed by the ISA (International Society of Automation) providing a framework for mitigating vulnerabilities in Industrial Automation and Control Systems (IACS) associated with Industry 4.0 and Critical Infrastructure.

*Sources:* https://www.iec.ch/homepage | https://isaeurope.com/how-can-the-62443-series-of-standards-help-your-company/

### IED (Intelligent Electronic Device)

An Intelligent Electronic Device (IED) is a term used in the electric power industry to describe microprocessor-based controllers of power system equipment, such as circuit breakers, transformers and capacitor banks.

*Sources:* https://en.wikipedia.org/wiki/Intelligent_electronic_device

### IIoT (Industrial Internet of Things)

A system that connects and manages sensors as well as actuators while integrating them with mainly cloud-based control components that act together to exercise control in the physical world. IIoT connects and integrates industrial control systems with enterprise systems, business processes and analytics. This combination of machines, computers, and people, enable intelligent industrial operations using advanced data analytics for transformational business outcomes.

*Sources:* IIoT may also refer to the integration of a cloud-based IIoT device management solution with on-premise SCADA systems to enable new business processes and analytics. | Industrial internet Consortium (IIC). The Industrial Internet of Things Vocabulary Technical Report V2.2. https://www.iiconsortium.org/ vocab/

### IIoT Edge Gateway & Device

An Edge Gateway is an intelligent device in edge computing. It is deployed between networks and fulfills mainly two functions:

*Sources:* https://www.itwissen.info/edge-gateway-EGW-Edge-Gateway.html%20and%20https://brainly.in/question/2436258

### INVEST

An acronym for independent, negotiable, valuable, estimable, small, and testable that can be used as a checklist of widely accepted criteria to assess the quality of a user story. If the criteria isn’t met, the team can reword the user story so it meets the criteria.

*Sources:* https://www.agilealliance.org/glossary/invest/

### IOC (Indicators of Compromise)

IOCs are technical artifacts or observables that suggest an attack is imminent or is currently underway, or that a compromise may have already occurred. Indicators can be used to detect and defend against potential threats. Examples of indicators include the Internet Protocol (IP) address of a suspected command and control server, a suspicious Domain Name System (DNS) domain name, a Uniform Resource Locator (URL) that references malicious content, a file hash for a malicious executable, or the subject line text of a malicious email message.

*Sources:* Page 2: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-150.pdf

### IPv4

Internet Protocol Version 4 is the fourth version of the Internet Protocol (IP). It is one of the core protocols of standards-based internetworking methods in the Internet and other packet-switched networks. IPv4 was the first version deployed for production on SATNET in 1982 and on the ARPANET in January 1983. It still routes most Internet traffic today, despite the ongoing deployment of a successor protocol, IPv6.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### IPv6

Internet Protocol Version 6 is the most recent version of the Internet Protocol (IP), the communications protocol that provides an identification and location system for computers on networks and routes traffic across the Internet. IPv6 was developed by the Internet Engineering Task Force (IETF) to deal with the long-anticipated problem of IPv4 address exhaustion.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### ISA (International Society of Automation)

Founded in 1945 ISA set the standards for those who apply engineering and technology to improve the management, safety, and cybersecurity of modern automation and control systems used across industry and critical infrastructure. Of particular interest to the CSA WG is IEC’s work on the ISA-99 series of standards addressing Security Technologies for Industrial Automation and Control Systems. The ISA-99 series of standards developed by ISA (International Society of Automation) was adopted by the International Electrotechnical Commission (IEC) as IEC-62443 providing a framework for mitigating vulnerabilities in Industrial Automation and Control Systems (IACS) associated with Industry 4.0 and Critical Infrastructure.

*Sources:* https://www.isa.org/about-isa/ | https://isaeurope.com/how-can-the-62443-series-of-standards-help-your-company/

### IT / OT (Operational Technology) Convergence

IT and OT are primarily seen as different technology areas with different responsibilities. This is due to the different requirements in regards to CIA and safety.

*Sources:* IT/OT convergence is the end state sought by organizations, where instead of a separation of IT and OT as technology areas, a integrated process and information flow is used. | https://www.gartner.com/en/information-technology/glossary/it-ot-integration

### IT Governance

This capability covers all processes and components oriented to establish decision rights and accountability framework to encourage desirable behavior in the life cycle for IT services.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### IT Operation

IT operation defines the organizational structure and skill requirements of an IT organization and a set of standard operational management procedures and practices to allow the organization to manage an IT operation and associated infrastructure.

*Sources:* IT Operation capabilities are oriented to align the business and IT Strategies, management of the project and technological portfolios, and ensure architecture governance throughout IT. | Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### IT Risk Management

Information risk management is the act of aligning exposure to risk and capability of managing it with the risk tolerance of the data owner. It is the primary means of decision support for information technology resources designed to protect the confidentiality, integrity, and availability of information assets. Ensures that risk of all types are identified, understood, communicated, and either accepted, remediated, transferred or avoided. IT Risk Management can look at the output of Compliance Management activities to assist the organization in evaluating the overall security posture and aligning with the defined risk objectives.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### ITOS

Information Technology Operations & Support (ITOS)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Identifier

The artifact used to assert the identity. This could be digital as in the case of a cryptographic token, or it could be physical, such as your driver’s license and passport.

*Sources:* https://www.isaca.org/resources/glossary#glossi

### Identity Federation

establishes the relationship between an Identity Provider (IdP), which handles authentication and a Relying Party, where authorizations are managed. In cloud, the relying party is typically a cloud service or application. Because one identity provider can federate to many relying parties this consolidates user management (creation, role assignment, attributes, authentication, and deletion) while supporting authorizations and access controls among distributed systems.

*Sources:* https://doi.org/10.6028/NIST.SP.800-63c

### Identity Provider (IdP)

The source of the identity in a federation. Responsible for enforcing authentication policies. IdP can also play an important role in authorization strategy by mapping CSP roles to IdP attributes. The identity provider isn’t always the authoritative source, but can sometimes rely on the authoritative source.

*Sources:* https://doi.org/10.6028/NIST.SP.800-63c

### Identity and Access Management (IAM)

An identity management tool that ensures that only authorized identities have access to the right resources. With cloud platforms consolidating numerous administrative functions of data centers and services into unified, internet-accessible web consoles and API interfaces, IAM acts as the new perimeter in cloud-native security, protecting sensitive resources from unauthorized access and misuse.

*Sources:* https://www.isaca.org/resources/glossary#glossi

### Identity (ID)

The set of attribute values (i.e., characteristics) by which an entity is recognizable and that, within the scope of an identity manager’s responsibility, is sufficient to distinguish that entity from any other entity.

*Sources:* https://csrc.nist.gov/glossary/term/identity

### Identity Management

Ensure that credible identities can be used for authentication, entitlement, and access management by oversight of the full lifecycle of an identity.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Identity Management

Identity Management (IM) is the process of managing and controlling user identities and access to systems, applications, and data. IM includes tasks such as user registration, authentication, authorization, and password management. The goal of IM is to ensure that only authorized users can access resources and that access is granted based on the principle of least privilege. IM is a critical component of information security and helps organizations to protect against unauthorized access and data breaches. For example, an organization may use an IM system to manage the identities and access of its employees and partners to its network and applications.

### Identity Provider

An Identity Provider (IdP) is a service that manages and controls user identities and authentication in a federated identity environment. An IdP is responsible for verifying the identity of users and providing authentication tokens that enable users to access resources on behalf of an identity provider. IdPs are commonly used in single sign-on (SSO) scenarios, where users can access multiple applications and services using a single set of credentials. For example, Google provides an IdP service that enables users to use their Google accounts to access a range of third-party applications and services.

### Identity Provider (IdP)

A trusted entity that issues or registers subscriber authenticators and issues electronic credentials to subscribers. A cloud service provider may be an independent third party or issue credentials for its own use.

*Sources:* https://csrc.nist.gov/glossary/term/identity_provider

### Identity Provisioning

The creation, maintenance and deactivation of user objects as they exist in one or more systems, directories or applications, in response to automated or interactive business processes.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Identity Stores

Identity stores refer to databases or directories that store information about user identities and attributes. Identity stores are a critical component of IAM systems and enable organizations to manage user identities and access to systems and applications. Identity stores typically include information such as user names, passwords, email addresses, and access privileges. For example, Microsoft Active Directory is a popular identity store that is used by many organizations to manage user identities and access to resources.

### Identity Verification

The process of identifying living individuals by using their physiological and behavioral characteristics, or derived documents issued by an authority.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Identity and Access Management (IAM)

Identity and Access Management (IAM) refers to the policies, technologies, and processes that enable organizations to manage and control user identities, access, and privileges to systems and applications. IAM solutions typically include user provisioning, authentication, authorization, and auditing capabilities. IAM helps organizations to ensure that only authorized users can access sensitive data and applications and that access is granted based on the principle of least privilege. IAM also enables organizations to streamline user management processes and reduce the risk of insider threats. For example, a bank may use an IAM solution to manage the access of its employees and customers to its online banking platform, ensuring that only authorized users can perform transactions and access account information.

### Identity and Access Management (IAM)

The set of technology, policies, and processes that are used to manage access to resources.

*Sources:* SDPs typically rely on an organization’s existing identity and access management system (and/or external CASB) for user authentication and user attributes (such as role or group membership). | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-203.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Identity as a Service (IDaaS)

Identity as a Service (IDaaS) is a cloud-based delivery model for IAM services. It allows organizations a secure way to manage and control identities, access, and privileges across multiple applications and platforms. IDaaS providers offer a range of services including user provisioning, authentication, single sign-on, and multifactor authentication. IDaaS enables businesses to reduce the complexity and cost of managing IAM systems in-house and to provide secure access to employees, partners, and customers from anywhere and on any device. For example, Okta is an IDaaS provider that offers a cloud-based platform for managing user identities and access to applications and data.

### Identity, Credential, and Access Management (ICAM)

Identity, Credential, and Access Management (ICAM) encompasses the policies, processes, and technologies used to manage digital identities, credentials, and access rights. ICAM solutions ensure that the right individuals have appropriate access to resources, enhancing security and compliance.

*Sources:* https://www.cisa.gov/safecom/icam

### Image Management

Processes and procedures for managing the collection of software images within an infrastructure.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Immutable Workloads

Also knows as long-running workloads, are those that are carefully nurtured and maintained over extended periods. These workloads are often unique, manually built and managed, and have security software installed and updated manually. Such an approach is time-consuming and prone to human error, which can lead to inconsistent security practices. long-running workloads are typically seen in scenarios where traditional on-premises workloads are moved to the cloud without altering the underlying management philosophy (known as ‘lift and shift’).

*Sources:* https://devops.stackexchange.com/questions/412/what-are-immutable-servers

### Incident

An issue that harms the operation of network and information systems core services.

*Sources:* Cloud Penetration Testing : CSA

### Incident

In the context of cloud security, incidents are events that demand immediate attention to contain and mitigate their effects, preventing escalation. At the apex are breaches which signify a successful penetration or circumvention of security measures, leading to unauthorized access or extraction of data.

*Sources:* https://www.isaca.org/resources/glossary#glossi

### Incident Response (IR)

Focused on with unexpected events. This necessitates a clear differentiation between events, incidents, and breaches, each representing a distinct level of threat and requiring tailored response strategies.

*Sources:* https://www.isaca.org/resources/glossary#glossi

### Incident Handling

The corrective action to address an issue/incidence in violation of security practices and recommended practices.

*Sources:* NIST.SP800-61r2: Computer Security Incident Handling Guide

### Incident Impact

A measure of the extent of damage caused by an incident before it can be resolved.

*Sources:* Cloud Penetration Testing : CSA

### Incident Management

Process for managing an incident from detection through review and resolution.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Incident Reporting

The procedure by which the reporting party (cloud provider or cloud operator) shall submit to a national competent authority a report with information on the incident on an ad-hoc basis.

*Sources:* Cloud Penetration Testing : CSA

### Incident Response Legal Preparation

Processes and procedures to ensure that relevant information is identified, collected and preserved to support future litigation regarding the incident.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Incident Response Plan

A clear set of instructions that helps an organization prepare, detect, analyze and recover from an incident.

*Sources:* Cloud Penetration Testing : CSA

### Incident Response Planning

Incident Response Planning (IRP) is a process that organizations use to prepare for and respond to security incidents. IRP involves creating a plan that outlines the steps that will be taken in the event of a security incident, including identifying the incident, containing the damage, and restoring normal operations. IRP also involves training employees on how to respond to security incidents and conducting regular testing to ensure that the plan is effective. For example, an organization may have an IRP in place that outlines the steps that will be taken in the event of a data breach, such as notifying affected parties, conducting a forensic investigation, and implementing measures to prevent future incidents.

### Incident Root Cause

The reason (ultimate root cause) that caused the incident. (A root cause analysis could identify multiple “causes and effects” but will have a single root cause).

*Sources:* Cloud Penetration Testing : CSA

### Independent Audits

Independent audits effectively prevent you from ‘fooling yourself.’ It ensures an unbiased review of the current business state of affairs related to security and compliance.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Independent Risk Management

Risk Assessments performed by a third-party to assess the maturity of the organization’s controls from a reference framework perspective (i.e., COBIT, ISO27001), regulatory perspective (i.e., SOX, PCI), this type of assessment could also include Security Testing (Black-Box, White-Box, Pen-Testing).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Industrial Control Plane

Carries the control information in the network. In industrial networks, control-plane activity consists of any engineering activity related to the maintenance life cycle of the industrial controllers, including any read/change of controller state, control-logic, configuration settings, or firmware. In industrial networks, industrial controllers (e.g. PLCs, RTUs, DCS) are the “brains” responsible for the continuous execution of the entire industrial process lifecycle. These controllers are specialized computers, provided by vendors like Rockwell Automation, Siemens, GE, Schneider Electric and others. These industrial solid-state computers monitor inputs and outputs, and make logic-based decisions. The control plane uses protocols for communicating activities (e.g. firmware download/ upload, configuration updates, code and logic changes) and are mostly proprietary and undocumented. Each vendor uses their own unique implementation of the IEC-61131 standard for programmable controllers. Therefore, they vary based on the vendor and device models. Usually, these control-plane protocols are unnamed because of the fact they were meant to be used internally only via the vendor’s engineering software.

*Sources:* Pages 2, 3 and 7 from: https://info.indegy.com/wp-5-things-industrial-control-planety?submissionGuid=84f66e5e-db70-419c-817f-b678e5ed08f4

### Industrial Control Systems (ICS)

General term that encompasses several types of control systems, including supervisory control and data acquisition (SCADA) systems, distributed control systems (DCS), and other control system configurations such as programmable logic controllers (PLC) often found in the industrial sectors and critical infrastructures. An ICS consists of combinations of control components (e.g., electrical, mechanical, hydraulic, pneumatic) that act together to achieve an industrial objective (e.g., manufacturing, transportation of matter or energy).

*Sources:* See also: Process Control System (PSC) | https://csrc.nist.gov/glossary/term/industrial_control_system

### Industrial Data Plane

Sometimes referred to as the user plane, Industrial Data Plane carries the user-data traffic. In industrial networks, the data-plane is used by the HMI and SCADA applications to communicate process parameters and physical measurements between the human operator and the industrial equipment (I/Os). The Data Plane uses protocols like Modbus, PROFINET and DNP3 which are used by HMI/ SCADA applications to communicate physical measurements and process parameters (e.g. current temperature, current pressure, valve status, etc.). These protocols are typically well documented and standardized.

*Sources:* Pages 2 and 6 from: https://info.indegy.com/wp-5-things-industrial-control-planety?submissionGuid=84f66e5e-db70-419c-817f-b678e5ed08f4

### Industry 4.0

Industry 4.0 is the subset of the fourth industrial revolution that concerns industry. The fourth industrial revolution encompasses areas that are not normally classified as industry, such as smart cities for instance. Although the terms “industry 4.0” and “fourth industrial revolution” are often used interchangeably, “industry 4.0” factories have machines which are augmented with wireless connectivity and sensors, connected to a system that can visualize the entire production line and make decisions on its own. In essence, industry 4.0 is the trend towards automation and data exchange in manufacturing technologies and processes which include cyber-physical systems (CPS), the internet of things (IoT), industrial internet of things (IIOT), cloud computing, cognitive computing, and artificial intelligence. The concept includes:

*Sources:* https://en.wikipedia.org/wiki/Industry_4.0

### Industry 4.0 Technologies

Below are some of the technologies that will transform manufacturing and the supply chain allowing Industry 4.0 to realize its full potential: “Big Data and Analytics, Autonomous Robots , Simulation, Horizontal and Vertical System Integration, The Industrial, Internet of Things, Cybersecurity, The Cloud, Additive Manufacturing, Augmented Reality”BCG, “Artificial Intelligence, Robotics, Internet of Things, Autonomous Vehicles, 3-D Printing, Nanotechnology, Biotechnology, Materials Science, Energy Storage, Quantum Computing” (WEFORUM)

*Sources:* https://www.bcg.com/capabilities/operations/embracing-industry-4.0-rediscovering-growth.aspx | https://www.weforum.org/agenda/2016/01/the-fourth-industrial-revolution-what-it-means-and-how-to-respond/

### InfoSec Management

The main objective of Information Security Management is to implement the appropriate measurements to minimize or eliminate the impact that security-related threats and vulnerabilities might have on an organization. Measurements include Capability Maturity Models (which identify stages of development of an organization from an immature state through several levels of maturity as the organization gains experience and knowledge), Capability Mapping Models (which describe what a business does to reach its objectives and promotes a strong relationship between the business model and the technical infrastructure that supports the business requirements resulting in a view that can be understood by both the business and IT), Roadmaps in the form of security architectures (which provide a guideline to be followed by individual projects serving individual business initiatives), and Risk Portfolios (where identified risks are registered, monitored, and reported). Dashboards for security management and risk management are used to measure and report the effectiveness of decisions and help the organization make new decisions that will maintain and improve that effectiveness. Analysis and plans for remediating residual risks are also part of the overall risk management framework.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Information Security Officer (ISO)

An Information Security Officer (ISO) is responsible for overseeing and implementing an organization’s information security program. The ISO develops, implements, and enforces policies and procedures to protect the organization’s data and information systems from cyber threats. This role involves coordinating security measures, conducting risk assessments, and ensuring compliance with relevant regulations and standards.

*Sources:* https://csrc.nist.gov/glossary/term/chief_information_security_officer

### Information Technology Infrastructure Library (ITIL)

The Information Technology Infrastructure Library (ITIL) is a set of best practices for IT service management (ITSM) that aims to align IT services with the needs of the business. ITIL provides a systematic and professional approach to managing IT services, covering areas such as service strategy, service design, service transition, service operation, and continual service improvement. ITIL helps organizations deliver quality IT services and improve overall efficiency.

*Sources:* https://www.cio.com/article/272361/infrastructure-it-infrastructure-library-itil-definition-and-solutions.html

### Information Disclosure

The breach of privacy or leak of information to unauthorized persons or to the public domain. In cloud testing information disclosure often takes the form of leak of data from misconfigured public cloud data stores.

*Sources:* Cloud Penetration Testing : CSA

### Information Leakage Metadata

Metadata that is attached to critical pieces of information to mark it for detection by data leakage prevention tools.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Information Security Policies

Broad statements of management intent that guide the information security operations of an organization. Policies are implemented by standards and procedures and compliance can be verified through audits.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Information Services

Information Services refers to the storage of data, usually in databases, but sometimes just in files.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Information System Regulatory Mapping

The main focus here is to ensure that all regulatory requirements are identified and that the business’s compliance effort takes them into account.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Information Technology Operation & Support (ITOS)

ITOS outlines all the necessary services an IT organization will have to support its business needs. ITOS is the IT Department. It is the help desk that takes the call when a problem is found. It is the teams that coordinate changes and roll them out in the middle of the night. It is the planning and process that keep the systems going even in the event of a disaster.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Information Technology Resiliency

The attributes of an information technology entity and its services to continue to provide adequate services when events occur (power interruption, loss of network links, etc.).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Information-theoretic secure

A cryptosystem is information-theoretically secure if its security derives purely from information theory. That is, the cryptosystem cannot be breached even when the adversary has unlimited computing power. Examples of information-theoretically secure cryptosystems include the classical one-time pad and Quantum-Key Distribution (QKD).

*Sources:* Quantum Safe Security Glossary : CSA

### Infrastructure

A shared, evolving, open, standardized, and heterogeneous installed base and as all of the people, processes, procedures, tools, facilities, and technology which supports the creation, use, transport, storage, and destruction of information (also referred to as information infrastructure).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Infrastructure Layer

At the lowest layer in the SDN reference model, the infrastructure layer consists of switching devices (e.g., switches, routers, etc.), which are interconnected to formulate a single network.

*Sources:* https://ieeexplore.ieee.org/abstract/document/68347622

### Infrastructure Protection Services

Infrastructure Protection Services secure Server, Endpoint, Network, and Application layers. This discipline uses a traditional defense in depth approach to ensure containers and pipes of data are healthy. The controls of Infrastructure Protection Services are usually considered as preventive technical controls such as Intrusion Detection/Prevention Systems ( IDS/IPS), Firewall, Anti-Malware, White/Black Listing, and more. They are relatively cost-effective in defending against the majority of traditional or non-advanced attacks.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Infrastructure Services

Not to be confused with Infrastructure as a Service, Infrastructure Services can be visualized as the foundational capabilities provided by the rows of computers, network cables, power supplies, cooling vents, and fire suppression pipes you will see inside any standard data center. These capabilities include virtualization, compute, storage and network; facilities and environmentals; and physical security and access restrictions. Infrastructure Services may also reference Facilities, Hardware, Network and Virtual Environments. Infrastructure Services are the layered basic core capabilities that support higher-level capabilities in other architecture areas. These levels include virtual machines, applications, databases, as well as networking and the physical hardware and facilities..

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Infrastructure as a Service (IaaS)

Offers access to a resource pool of fundamental6 computing infrastructure, such as compute, network, or storage.

*Sources:* Disaster Recovery as a Service : CSA

### Infrastructure-as-code (IaC)

The process of managing and provisioning an organization’s IT infrastructure using machine-readable configuration files, rather than employing physical hardware configuration or interactive configuration tools.

*Sources:* https://csrc.nist.gov/glossary/term/infrastructure_as_code

### Ingress

With respect to Kurbernetes networking, Ingress is a Kubernetes resource that manages external access to services within a cluster. It acts as a single entry point for HTTP/HTTPS traffic and provides features like URL routing, SSL termination, and virtual hosting. Ingress controllers, such as NGINX or Traefik, implement the ingress rules.

*Sources:* https://www.isaca.org/resources/glossary#glossi

### Initiating Host (IH)

The host that initiates communication to the controller and to the AHs.

*Sources:* An initiating host is a trusted node in an SDP. The initiating host (IH) is the host that initiates communication to the controller and to the AHs. It initiates a two-way encrypted connection to authorized accepting hosts. | https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Initiating Host (IH) Session

The period of time that a particular IH is connected to a controller.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf

### Initiating Host (IH) Session ID

A 256-bit randomized arbitrary number used once (NONCE) managed by the SDP controller and used to refer to a particular IH session.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf

### Input Validation

Input validation examines the user’s input and determines what input is acceptable input to the system. This process helps with data quality as well as allows malicious input from being injected into the system.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Insider Threats

The threat that an insider will use her/his authorized access, wittingly or unwittingly, to do harm to the security of organizational operations and assets, individuals, other organizations, and the Nation. This threat can include damage through espionage, terrorism, unauthorized disclosure of national security information, or through the loss or degradation of organizational resources or capabilities.

*Sources:* https://csrc.nist.gov/glossary/term/insider_threat

### Integrated Circuit Chip (ICC)

The ICC is part of a smart card and is embedded into the physical plastic. Smart cards are often used in two-factor authentication solutions where the user enters a pin which is used by an operating system on the smart card to release evidence of identity such as a digital certificate or to allow a private key to sign an identity token which is sent to an enforcement agent that determines if the identity is valid.

*Sources:* https://ea.cloudsecurityalliance.org/display.php?id=data_sec6036&_ga=2.215953620.277413644.1656439470-2107700575.1655484199

### Integrated Development Environment (IDE)

Set of software tools or applications to provide comprehensive facilities for software development.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec-ieee:24765:ed-2:v1:en:term:3.2029

### Integration Middleware

Integration Middleware is a set of tools like service buses and message queues that allow applications to exchange information without talking directly. Security concerns for these services include making sure the messages being exchanged are not read or tampered with during delivery, and reliable sources are only sending them.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Integrity Measurement Architecture (IMA)

Integrity Measurement Architecture (IMA) is the accredited remote attestation methods which formulates the integrity measurement process and integrity reporting protocol.

*Sources:* https://ieeexplore.ieee.org/document/5557396

### Intellectual Property

A term referring to a number of distinct types of creations of the mind for which a set of exclusive rights are recognized-and the corresponding fields of law. Under intellectual property law, owners are granted certain exclusive rights to various intangible assets, such as musical, literary, and artistic works; discoveries and inventions; and words, phrases, symbols, and designs. Common types of intellectual property rights include copyrights, trademarks, patents, industrial design rights, and trade secrets in some jurisdictions.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Intellectual Property Protection

The activity (e.g. applying process or technical control) of preventing misuse and improper disclosure of intellectual property.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Inter-Mediation

An API Facade is a layer or gateway that sits between the microservices and the API exposed to external services. The facade creates a buffer or layer between the interface exposed to apps and app developers and the complex services. You may have several API’s into different microservices, the facade abstracts the complexity with a simple singular interface.

*Sources:* Microservices Architecture Pattern : CSA

### Interactive Application Security Testing (IAST)

Software component deployed with an application that assesses application behavior and detects presence of vulnerabilities on an application being exercised in realistic testing scenarios.

*Sources:* The Six Pillars of DevSecOps: Automation : CSA

### Internal

It focuses on attacks that could be launched by an insider. In contrast to a remote attacker, this attacker may have some form of authorized access and already has access to the internal network. The insider can also have more knowledge of the location of valuable data.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Internal Identity

Internal Identity refers to the unique identification of individuals within an organization, used to manage access to systems and resources. It ensures that only authorized personnel can access sensitive data and perform specific tasks within the organization’s IT infrastructure.

*Sources:* https://developer.okta.com/docs/concepts/iam-overview/

### Internal (VNIC)

A VNIC is a virtualized network interface that presents the same media access control (MAC) interface that an actual interface would provide.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Internal Audits

Provides a cross-checking mechanism within the organization. In larger organizations, there is likely to be some level of independence as well.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Internal Infrastructure

The internal infrastructure services are mainly concerned with the physical assets used by the cloud service provider to support the virtualized services actually seen by cloud users. In many ways, these services are the lowest-level and least visible to the end cloud user though they are the foundation that underlies reliable and secure operation of the cloud service. For instance, without good facility security, there is no need for an adversary to mount a network attack on a cloud service as it is easier to just walk into the facility and unplug a server or network connection.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Internal Investigations

Internal investigations are concerned with determining the factual truth and implications of a policy or criminal investigation. This process includes fraud detection, prevention, and forensic investigation.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Internal SLAs

Service level agreements within an organization that codify the specific services to be delivered and the performance criteria governing that delivery.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Internet Protocol Security (IPSec)

Provide(s) interoperable, high quality, cryptographically-based security for IPv4 and IPv6. The set of security services offered includes access control, connectionless integrity, data origin authentication, detection and rejection of replays (a form of partial sequence integrity), confidentiality (via encryption), and limited traffic flow confidentiality.

*Sources:* SDPs provide two-way secure connections over IPSec for the upper network layers. | https://csrc.nist.gov/glossary/term/ip_security | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Interoperability

Interoperability refers to the ability of different systems, devices, or applications to work together seamlessly within and across organizational boundaries. This capability ensures that information and data can be exchanged and utilized effectively between various IT environments, enabling comprehensive integration and functionality across diverse platforms​

*Sources:* https://www.isaca.org/resources/glossary#glossi

### Intrusion Management

The process of using pattern recognition to detect statistically unusual events, prevent or detect intrusion attempts, and manage the incidents.

*Sources:* Defined Categories of Service 2011 : CSA

### Inventory Control

To provide management control and accountability over the organization’s physical and digital assets. Cloud and virtualization can create a challenge in terms of attempting to inventory virtual machines in the way physical machines have traditionally been tracked.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Investment Budgeting

The planning process used to determine whether an organization’s long term investments such as new infrastructure, replacement of existing services and infrastructure, new data centers, new products or services, research, application development, security, and project deployment are worth pursuing. Usually, a cost-benefit analysis is used as part of the investment budgeting process.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### IoT Search Engine

Internet of Things (IoT) search engine which enables you to find physical devices with embedded computing capabilities - such as webcams, home appliances, medical devices - that are connected to and can exchange data over the Internet. Two examples of IoT search engines are Thingful (https://www.thingulf.com) and Shodan (https://www.shodan.io).

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

### Isogeny

This is a particular type of mapping between two elliptic curves.

*Sources:* Quantum Safe Security Glossary : CSA

### Isogeny-based cryptography

This is a sub-area of quantum-safe cryptography that constructs publickey schemes whose security is dependent on the difficulty of recovering an unknown isogeny between a pair of elliptic curves. An example is the scheme of D. Jao and L. De Feo [JF].

*Sources:* [JF] D. Jao and L. De Feo. Towards Quantum-Resistant Cryptosystems from Supersingular Elliptic Curve Isogenies, Post-Quantum Cryptography 2011.


## J

### JSON Web Token (JWT)

JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA. Although JWTs can be encrypted to also provide secrecy between parties, we will focus on signed tokens. Signed tokens can verify the integrity of the claims contained within it, while encrypted tokens hide those claims from other parties. When tokens are signed using public/private key pairs, the signature also certifies that only the party holding the private key is the one that signed it.

*Sources:* https://jwt.io/introduction

### Java Message Service (JMS)

The Java messaging service (JMS) is a middlewareoriented messaging technology working according to the publish/ subscribe principle.

*Sources:* https://ieeexplore.ieee.org/abstract/document/1648916

### Job Aid Guidelines

A job aid (aka Standard Operating Procedures or Playbooks) stores information or instruction external to a user and guides them to perform a task correctly. It is used during the actual performance when the user needs to know the information or procedure. It can be consulted quickly when needed and provides specific, concise information to the user. It reduces the need for individuals to remember so much information and is an efficient method to reduce problems associated with relying strictly on recall to perform in certain situations.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Job Descriptions

Clear definitions of the responsibilities of a job help to identify the data access requirements of people with that job to ensure that they only have the minimum required access.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Just in Time (JIT) Privileges

privileges are requested and granted as needed. Entities use templates to access a predetermined set of privileges for specific resources during a designated time frame, like during a maintenance window. JIT access is granted if it complies with policy constraints, and it may require additional authorization. JIT can be further enhanced when integrated with risk-scoring systems.

*Sources:* https://www.cyberark.com/what-is/just-in-time-access/

### Just in Time Access (JIT)

JIT access is a process of granting a level of access as fast as possible, at the time it is needed, and removed as soon as possible, after the access is no longer needed.

*Sources:* https://www.cyberark.com/what-is/just-in-time-access/

### Just-In-Time (JIT) access

Just-in-time (JIT) access is the capability to provide access only when needed. In these scenarios, the user requests access and is timeboxed and at the end of the time the access is removed. JIT access can be manually or automatically approved through policy actions.

*Sources:* Recommendations for Adopting a Cloud-Native Key Management Service : CSA


## K

### Keep-Alive Message

The keep-alive message is sent by the initiating host (IH), accepting host (AH) or controller to indicate that it is still active.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf?_ga=2.222448153.38415640.1663010462-1480344219.1663010462

### Kernel

Primary (of three) components of an operating system

*Sources:* https://www.isaca.org/resources/glossary#glossk

### Key Control Indicators (KCI)

Key Control Indicators (KCI) are metrics that help in monitoring the effectiveness of control mechanisms within an organization’s risk management framework. KCIs are used to measure how well controls are performing in mitigating identified risks and ensuring compliance with policies and procedures. They provide valuable insights into the operational health of controls and help in identifying areas that require improvement .

*Sources:* https://www.isaca.org/resources/isaca-journal/issues/2018/volume-4/integrating-kris-and-kpis-for-effective-technology-risk-management

### Key Management Services (KMS)

Key Management Services (KMS) are systems and tools designed to manage cryptographic keys throughout their lifecycle, including generation, distribution, rotation, and revocation. KMS ensures the secure handling of keys, supporting data encryption and decryption processes while maintaining compliance with security policies.

*Sources:* https://www.isaca.org/resources/isaca-journal/issues/2018/volume-4/integrating-kris-and-kpis-for-effective-technology-risk-management

### Key Management

Key management covers the entire lifecycle of keys beginning to end including generation, communication and distribution, storage, entry, and installation, checking the validity, usage, changing the active key, archiving, destruction, an audit of key operations and usage, key backup and recovery, and emergency reserve keys.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Key Management Interoperability Protocol (KMIP)

The KMIP establishes a single, comprehensive protocol for communication between enterprise key management servers and cryptographic clients. It addresses the critical need for a comprehensive key management protocol built into the information infrastructure so that enterprises can deploy effective unified key management for all their encryption, certificate-based device authentication, digital signature, and other cryptographic capabilities.

*Sources:* http://xml.coverpages.org/KMIP/KMIP-WhitePaper.pdf

### Key Management System (KMS)

The management of cryptographic keys in a cryptosystem for data control and security with cloud services. The KMS can be native to a cloud platform, external, self-operated, or other cloud service.

*Sources:* Key Management in Cloud Services: Understanding Encryption’s Desired Outcomes and Limitations : CSA

### Key Risk Indicators

Identifies what the key risks are from a management or executive level. These are the key risk factors that can affect a specific business.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Keyed-Hash Message Authentication Code (HMAC)

A message authentication code that uses a cryptographic key in conjunction with a hash function. It is an integral element of the initial packet that initiates connections into the SDP.

*Sources:* https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.198-1.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Keyloggers

A reconnaissance tool–with keylogging and screen capture functionality–used for information gathering on compromised systems.

*Sources:* https://attack.mitre.org/software/

### Keystroke / Session Logging

Methodologies for capturing a detailed record of interactions with an entity (either at the level of individual keystrokes or interactions with the entity)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Kill Chain for Industrial Control Systems

In 2011, Lockheed Martin analysts Eric M. Hutchins, Michael J. Cloppert and Rohan M. Amin created the Cyber Kill Chain™ to help the decision-making process for better detecting and responding to adversary intrusions. This model was adapted from the concept of military kill chains and has been a highly successful and widely popular model for defenders in IT and enterprise networks. This model is not directly applicable to the nature of ICS-custom cyber attacks, but it serves as a great foundation and concept on which to build.

*Sources:* The ICS Kill Chain has 2 stages: | https://www.sans.org/reading-room/whitepapers/ICS/industrial-control-system-cyber-kill-chain-36297

### Knowledge Base

A repository of knowledge about the organization’s infrastructure and operations to enable the Security Operations Center to respond to events efficiently.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Knowledge Management

The process of organizing information and providing search capabilities such that problems and incidents can be handled quickly by referring to experience. In the Information domain, this represents the actual knowledge stored in the knowledge base regarding security FAQs, best practices, and job aids.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Knowledge Repository

The Knowledge Repository contains information about known patterns, processes, and procedures

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Kubernetes

An open-source container-orchestration system for automating deployment, scaling, and management of containerized applications across multiple hosts.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA


## L

### LDAP Repositories

Lightweight Directory Access Protocol (LDAP) Repositories organize users and groups of users into a hierarchical organizational structure.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### LDM

Logical Device Manager (LDM). A Microsoft Windows capability similar in function to LVM.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### LUN

Acronym for the SCSI protocol’s Logical Unit Number (LUN) and commonly used as a term for the block device presented to a host via a SAN.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### LVM

Logical Volume Management (LVM). Allows grouping of several physical disks into a single logical volume as viewed by the host

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Lamport one-time signature scheme

This is the scheme that inspired hash-based signature scheme. The technique proposed by L. Lamport [LamportRR] requires a one-way function and can be used to sign, at most, one message.

*Sources:* [LamportRR] L. Lamport. Constructing Digital Signatures from a One Way Function. Technical Report SRICSL-98, SRI International Computer Science Laboratory, 1979.

### Large Language Model

Advanced AI systems that leverage massive amounts of data and sophisticated algorithms to understand, interpret, and generate human language. They are primarily built using deep learning techniques, particularly neural networks, which allow them to process and learn from vast amounts of text data. The term “large” refers to both the extensive training data and the considerable size of the models, often featuring millions or even billions of parameters.

*Sources:* https://www.unite.ai/large-language-models/

### Lateral Movement

Lateral action from a compromised internal host to strengthen the attacker foothold inside the organizational network, to control additional machines, and to eventually control strategic assets.

*Sources:* Cyber Weapons Report 2016, LightCyber, Ramat Gan, Israel, 2016, 14pp. http://lightcyber.com/cyber-weapons-report-network-traffic-analytics-revealsattacker-tools/ [accessed 5/11/17].

### Lattice-based cryptography

This is a sub-area of quantum-safe cryptography and includes cryptographic schemes whose security is related to the Closest Vector Problem (CVP), the Learning with Errors (LWE) problem or the Shortest Vector Problem (SVP).

*Sources:* Quantum Safe Security Glossary : CSA

### Learning with Errors (LWE) problem

This is a hard problem used in lattice-based cryptography. The solution to the problem, an issue introduced by O. Regev [Reg05], requires the recovery of a noisy linear equations system.

*Sources:* [Reg05] O. Regev. On Lattices, Learning with Errors, Random Linear Codes, and Cryptography. STOC 2005.

### Least Privileged Access Control

Least Privilege Access Control is a mechanism through which an identity is provided just enough access to a resource to carry out the work - not more / not less. For example, if a Developer needs to create resources in Development Env for his application development work, he / she will be provided to create resources only in development env (and not in test / production env). This concept is very important for enhancing the security of a system and is critical for implementing Zero Trust principles.

*Sources:* https://csrc.nist.gov/glossary/term/least_privilege

### Legal Services

As security incidents occur, the need for legal counsel is critical for organizations. There are several capabilities included that may help legal counsels lead compliance activities, deal with lawsuits, and track preventive awareness across the organization.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Life Cycle Management

Policies, processes, and procedures for managing the lifecycle of data from creation through use, archiving and eventual destruction

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Lifecycle Management

Lifecycle Management is a process through which identities are managed throughout its lifecycle such as from creation to deletion. For example, in the Joiner - Mover - Leaver (JML) case, an employee joins an organization, his / her / their identity is created / granted certain access to systems / resources needed for their job execution. Later on, they move to a different department, their access to systems / resources are modified (added / deleted) to make sure they can do their job for his / her / their new department. Once that employee leaves the organization, his / her / their accesses are removed and ultimately, identities are deleted as per the corporate policy.

### Lift and Shift

Lift and Shift is a strategy for moving applications and workloads to the cloud without redesigning them. This approach involves replicating an existing IT stack to a cloud environment, allowing organizations to take advantage of cloud infrastructure without modifying their existing applications.

*Sources:* https://www.ibm.com/topics/lift-and-shift#:~:text=%E2%80%9CLift%20and%20shift%2C%E2%80%9D%20also,to%20public%20or%20private%20cloud .

### Lightweight Directory Access Protocol (LDAP)

LDAP (Lightweight Directory Access Protocol) is a software protocol for enabling anyone to locate data about organizations, individuals, and other resources such as files and devices in a network – whether on the public internet or a corporate intranet. LDAP is a “lightweight” version of Directory Access Protocol (DAP), which is part of X.500, a standard for directory services in a network. LDAP is considered lightweight because it uses a smaller amount of code than other protocols. A directory tells the user where in the network something is located. On TCP/IP networks – including the internet – the domain name system (DNS) is the directory system used to relate the domain name to a specific network address, which is a unique location on the network. However, the user may not know the domain name. LDAP allows a user to search for an individual without knowing where they’re located, although additional information will help with the search.

*Sources:* https://www.techtarget.com/searchmobilecomputing/definition/ LDAP#:~:text=LDAP%20(Lightweight%20Directory%20Access%20 Protocol)%20is%20a%20software%20protocol%20for,internet%20or%20 a%20corporate%20intranet

### Lightweight Directory Access Protocols (LDAP)

A networking protocol for querying and modifying directory services running over TCP/IP.

*Sources:* https://csguide.cs.princeton.edu/email/setup/ldap

### Line of business (LOB)

A line of business is a collection of similar products that are managed together for production synergy, economies of scale, or focus on a market segment.

*Sources:* https://www.sciencedirect.com/topics/computer-science/line-of-business

### Link Layer Network Security

Protection of data can be applied at the OSI Layer 2 Data Link Layer. Network switches are key components at Layer 2 communications and are susceptible to attacks such as CAM table overflow, VLAN hopping, spanning-tree protocol manipulation, MAC address spoofing, and ARP attacks. Mitigations include configuration of port security on a switch, modification to VLAN configurations, ACLs’ configuration on router ports, and 802.1X.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Linting

Linting is the automated checking of your source code for programmatic and stylistic errors. This is done by using a lint tool (otherwise known as linter). A lint tool is a basic static code analyzer.

*Sources:* https://owasp.org/www-project-devsecops-guideline/latest/01b-Linting-Code

### Loadable Kernel Module (LKM)

Loadable Kernel Modules (LKMs) are pieces of code that can be loaded and unloaded into the kernel upon demand. They extend the functionality of the kernel without the need to reboot the system. For example, one type of module is the device driver, which allows the kernel to access hardware connected to the system.

*Sources:* https://attack.mitre.org/techniques/T1547/006/

### Local

A virtual machine or application sandbox that is installed and managed on the endpoint but isolated from the rest of the endpoint. Management can be centralized but the virtual machine runs locally on the endpoint device (tablet, pc, etc.).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Local File Inclusion

Local file inclusion (also known as LFI) is the process of including files, that are already locally present on the server, through the exploiting of vulnerable inclusion procedures implemented in the application.

*Sources:* https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion

### Location Services

Geolocation information regarding the physical location of assets, resources, facilities, people.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Log

A record of the events occurring within an organization’s systems and networks

*Sources:* https://csrc.nist.gov/glossary/term/log

### Long Short-term Memory

A special neural network architecture that are able to process sequential data, data where chronological ordering matters. LSTMs are essentially improved versions of RNNs, capable of interpreting longer sequences of data.

*Sources:* https://www.unite.ai/what-are-rnns-and-lstms-in-deep-learning/


## M

### MES (Manufacturing Execution System)

A system that uses network computing to automate production control and process automation. By downloading recipes and work schedules, and uploading production results, a MES bridges the gap between business and plant-floor or process-control systems. NIST Manufacturing Execution Systems (MES) solutions that ensure quality and efficiency are built into the manufacturing process and are proactively and systematically enforced. Manufacturing Execution Systems connect multiple plants, sites, vendors’ live production information, and integrate easily with equipment, controllers and enterprise business applications. The result is complete visibility, control and manufacturing optimization of production and processes across the enterprise. (SIEMENS)

*Sources:* NIST: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r2.pdf Page B 10 SIEMENS: https://www.plm.automation.siemens.com/global/en/ourstory/glossary/manufacturing-execution-systems-mes/38072

### MITRE ATT&CK® framework

The MITRE ATT&CK® Framework is a comprehensive, globally-accessible knowledge base of adversary tactics and techniques based on real-world observations. It provides a structured foundation for developing specific threat models and methodologies, helping organizations understand and mitigate cyber threats through detailed insights into attacker behaviors and techniques.

*Sources:* https://attack.mitre.org/

### MITRE ATT&CK for ICS Matrix™

A knowledge base useful for describing the actions an adversary may take while operating within an ICS network. The knowledge base can be used to better characterize and describe post-compromise adversary behavior.

*Sources:* An overview of the tactics and techniques described in the ATT&CK for ICS knowledge base. It visually aligns individual techniques under the tactics in which they can be applied. | https://collaborate.mitre.org/attackics/index.php/Main_Page

### MQTT (Message Queuing Telemetry Transport)

A Client-Server publish/subscribe messaging transport protocol. It is lightweight, open, simple, and designed to be easy to implement. These characteristics make it ideal for use in many situations, including constrained environments such as communication in Machine to Machine (M2M) and Internet of Things (IoT) contexts where a small code footprint is required and/or network bandwidth is at a premium. The protocol runs over TCP/IP, or over other network protocols that provide ordered, lossless, bidirectional connections.

*Sources:* Abstract at bottom, Page 1: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.pdf

### MTUs (Master Terminal Unit or SCADA Server)

A controller that also acts as a server that hosts the control software which communicates with lower-level control devices, such as Remote Terminal Units (RTUs) and Programmable Logic Controllers (PLCs), over an ICS network. In a SCADA system, this is often called a SCADA server, MTU, or supervisory controller.

*Sources:* NIST, page B-3: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r2.pdf

### Machine Identity

A machine identity is a digital identity associated with a device or machine, such as a server, a computer, or a mobile device. Machine identities are used to authenticate and authorize devices and systems that access network resources. Examples of machine identities include a digital certificate or a security token that is used to establish trust between the device and the network.

*Sources:* https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8320C.ipd.pdf

### Macvlan Network

With respect to docker networking, a type of network that assigns a unique MAC address to each container, making them appear as different physical devices on the network. Containers can be connected directly to the physical network, bypassing the host’s network stack. This mode is useful when containers need to have their IP addresses on the physical network.

*Sources:* https://docs.docker.com/network/drivers/macvlan/

### Man-in-the-middle (MITM) attacks

An attack where the adversary positions himself in between the user and the system so that he can intercept and alter data traveling between them.

*Sources:* https://csrc.nist.gov/glossary/term/mitm

### Managed Security Services

An outsourced arrangement to provide some or all part of the security operations capabilities for an organization.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Management Plane Logs

detail the commands and controls executed in the cloud environment. They provide critical insights into how cloud resources are being managed. Analysis of management plane logs provides an organization visibility into who accessed the cloud infrastructure, what actions were performed, and when they occurred.

*Sources:* https://www.ciscopress.com/articles/article.asp?p=2928193&seqNum=2

### Management Plane

The management plane in IT refers to the layer of a network architecture responsible for managing, configuring, and monitoring network devices and systems. It is distinct from the data plane (which handles actual data transfer) and the control plane (which makes decisions about where traffic should be sent). The management plane provides the tools and interfaces for administrators to manage network operations, ensuring visibility, control, and security of the IT environment.

*Sources:* https://www.ciscopress.com/articles/article.asp?p=2928193&seqNum=2

### Mandatory Access Control (MAC)

A means of restricting access to objects based on the sensitivity (as represented by a security label) of the information contained in the objects and the formal authorization (i.e., clearance, formal access approvals, and need-to-know) of subjects to access information of such sensitivity.

*Sources:* https://www.dni.gov/files/NCSC/documents/nittf/CNSSI-4009_National_Information_Assurance.pdf

### Manual Security Code Review

Human process of reading source code to identify security issues.

*Sources:* The Six Pillars of DevSecOps: Automation : CSA

### Market Threat Intelligence

Cyber Intelligence information collected by distributed IDS sensors and analyzed by security firms. Also, this capability can consolidate Threat Intelligence from industry peers (i.e., HITRUST, Commercial branches from NSA, etc.)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Maturity Stage

With respect to zero trust maturity stages, the Optimal maturity stage represents the highest level of Zero Trust maturity, where organizations have fully integrated Zero Trust principles into their security strategy and operations.

*Sources:* https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf

### Maturity Mode

Tracking the organization’s capabilities against industry best practices, benchmarking, and maturity to show progress over time.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Maturity Model

Identify the stages of development of an organization from an immature state through several maturity levels as the organization gains experience and knowledge. COBIT defines a Capability Maturity Model with six levels of maturity: non-existent, initial, repeatable, defined, managed, and optimized.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### McEliece encryption scheme

This is a code-based public-key encryption scheme proposed by R.-J. McEliece in 1978 [McE78].

*Sources:* [McE78] R.-J. McEliece. A Public-Key System Based on Algebraic Coding Theory, pages 114—116. Jet Propulsion Lab, 1978. DSN Progress Report 44.

### Measured Service

Cloud systems automatically control and optimize resource use by leveraging a metering capability at some level of abstraction appropriate to the type of service (e.g., storage, bandwidth, active user accounts). Resource usage can be measured, monitored, controlled, and reported, providing transparency for both the CSP and the CSCs of the utilized service. This enables billing based on usage, which promotes cost efficiency and accountability (e.g. pay-as-you-go model).

*Sources:* https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-145.pdf

### Media Access Control (MAC) address

A hardware address that uniquely identifies each component of an IEEE 802-based network. On networks that do not conform to the IEEE 802 standards but do conform to the OSI Reference Model, the node address is called the Data Link Control (DLC) address. (NIST)

*Sources:* A Media Access Control (MAC) address is the unique hardware address of an Ethernet network interface card (NIC), typically “burned in” at the factory. MAC addresses may be changed in software. | https://www.sciencedirect.com/topics/computer-science/media-access-control

### Media Lockdown

Also referred to as removable media lockdown, a control to block user access to writable devices such as USB Flash memory sticks and CD/DVD-RW drives to prevent data leak.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Medical Devices

Medical devices in the context of this CSA Enterprise Architecture mean devices with connectivity to networks or the ability to download data so that information can be exchanged with the device, such as a monitoring device, worn by a patient.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Merkle Tree Signature Scheme

This is a typical example of a hash-based signature proposed by R. Merkle. The scheme’s principle is to use a Merkle tree whose leaves are the public/private keys of a one-time signature. This allows the Lamport one-time signature scheme (or other one-time or few-time signature schemes) to be extended for signing more than one message. The number of messages that can be signed depends on the height of the Merkle tree. The signature scheme requires a collision-resistant hash-function or a pre-image-resistant hash-function.

*Sources:* Quantum Safe Security Glossary : CSA

### Merkle tree

This a data structure named after R. Merkle [Merkle89] that is also known as a hash tree. It is a binary tree whose leaves are blocks of data which are hashed and then combined with other blocks through hashing. This hashing combination is repeated until all blocks have been combined into a single hash.

*Sources:* [Merkle89] R. Merkle. A Certified Digital Signature. CRYPTO ’89.

### Meta Data Control

Controlling what types of metadata accompany the underlying data (e.g., the record of changes to a document maintained as metadata by a word processing application should not be released with the document)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Meta Directory Services

Provides for the flow of one or more directory services and databases to import or maintain synchronization of those data sources.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Micro-segmentation

Is the technique of creating secure zones within a data center and cloud deployments that allow the organization to separate and secure each workload. This makes network security more granular and effective. These secure zones are created based on business services, and rules are defined to secure information workflow.

*Sources:* https://www.techtarget.com/searchnetworking/definition/microsegmentation

### Microservice Architectural Style

A microservices architecture usually refers to an application that has been structured to use basic elements called microservices, each running in its own process and communicating with lightweight mechanisms, often an HTTP resource API. These services are built around business capabilities and independently deployable by fully automated deployment machinery. There is a bare minimum of centralized management of these services, which may be written in different programming languages and use different data storage technologies.

*Sources:* Cloud Security Alliance. _Challenges in Securing Application Containers and Microservices Integrating Application Container Security Considerations into the Engineering of Trustworthy Secure Systems _(Cloud Security Alliance: 2019) 42

### Microservices

A microservice is a basic element that results from the architectural decomposition of an application’s components into loosely coupled patterns consisting of self-contained services that communicate with each other using a standard communications protocol and a set of well-defined APIs, independent of any vendor, product, or technology. Microservices are built around capabilities as opposed to services, build on SOA, and are implemented using Agile techniques. Microservices are typically deployed inside application containers.

*Sources:* NIST Special Publication (SP) 800-180 (Draft), NIST Definition of Microservices, Application Containers and System Virtual Machines, National Institute of Standards and Technology, Gaithersburg, Maryland, February 2016, 12pp. http://csrc.nist.gov/publications/drafts/800-180/sp800-180_draft.pdf

### Microservices Architecture

A microservices architecture usually refers to an application that has been structured to use basic elements called microservices, each running in its own process and communicating with lightweight mechanisms, often an HTTP resource API. These services are built around business capabilities and independently deployable by fully automated deployment machinery. There is a bare minimum of centralized management of these services, which may be written in different programming languages and use different data storage technologies

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Microservices Systems Software Development

The process of breaking down an application into components (microservices) via code extraction or rewrite, into a microservices architecture of self-contained services that achieve a business objective.

*Sources:* Challenges in Securing Application Containers and Microservices : CSA

### Middleware Authentication

Authentication of applications/services/components that users never, ever see directly.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Minimum Viable Network (MVN)

the network components required for minimum connectivity are deployed, and each layer in the architecture only allows the absolute minimum routes, ports, and protocols required for the application. This is enforceable per resource and inherent to the network design, enabling and supporting micro-segmentation.

*Sources:* https://www.alliedtelesis.com/us/en/white-paper/understanding-enterprise-sdn

### Misconfiguration

An incorrect or suboptimal configuration of an information system or system component that may lead to vulnerabilities.

*Sources:* https://csrc.nist.gov/glossary/term/misconfiguration

### Mobile Device Management

Mobile device management enables an enterprise to manage mobile endpoints’ security similar to the way that desktops are managed. The security features include locking or wiping the device if compromised, pushing software updates to the device, and requiring certain security features to be enabled before allowing a device to connect to the corporate network.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Mobile Device Virtualization

Mobile Device Virtualization allows the organization to test compatibility with new technologies for different mobile devices.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Mobile Devices

Mobile devices include smartphones, PDAs and tablets.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Modular Construction

Some monolithic applications may be built from a large number of components and libraries that may have been supplied by different vendors and some components (such as database) may also be distributed across the network.

*Sources:* https://cloudsecurityalliance.org/artifacts/best-practices-in-implementing-a-secure-microservices-architecture/ | Best Practices in Implementing a Secure Microservices Architecture : CSA

### Monolith

The earliest architecture for application systems is the “monolith” in which the entire application is designed to run as a single process and is hosted on a resource-intensive computing platform called the “server.” Although the application may be structured as different modules, a change in any module requires the recompilation and redeployment of the entire application. Communication between the modules is carried out by local procedure/function calls.

*Sources:* https://cloudsecurityalliance.org/artifacts/best-practices-in-implementing-a-secure-microservices-architecture/ | Best Practices in Implementing a Secure Microservices Architecture : CSA

### Multi-cloud

In a multi-cloud environment, a CSC utilizes multiple public cloud services, such as applications and systems, from different CSPs. This approach is commonly adopted to reduce dependency on a single cloud provider and build technical resilience into the architecture design.

*Sources:* https://cloud.google.com/learn/what-is-multicloud#:~:text=Multicloud%20refers%20to%20using%20services,or%20a%20combination%20of%20both .

### Multi-factor Authentication (MFA)

Authentication using two or more factors to achieve authentication. Factors include: (i) something you know (e.g. password/personal identification number (PIN)); (ii) something you have (e.g., cryptographic identification device, token); or (iii) something you are (e.g., biometric).

*Sources:* SDP access policies should support MFA for user authentication. There are several protocols such as UAF and U2F used for multi-factor authentication. SDPs can leverage U2F or UAF for user or device authentication without additional CA requirements, separate from the CA utilized for mutual TLS. | https://csrc.nist.gov/glossary/term/multi_factor_authentication | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Multiprotocol Label Switching (MPLS)

An Internet Engineering Task Force (IETF)-specified framework that provides for the efficient designation, routing, forwarding, and switching of traffic flows through the network. MPLS performs the following functions: specifies mechanisms to manage traffic flows of various granularities, remains independent of the Layer-2 and Layber-3 protocols, provides a means to map IP addresses to simple, fixed-length labels used by different packet-forwarding and packet-switching technologies, interfaces to existing routing protocols, and supports the IP, ATM, and frame-relay Layer-2 protocols.

*Sources:* SDP architectures define several connection types and each of these connections needs to be secure from layer 2 or 3 up to layer 7; MPLS is one such mechanism. | http://tele1.dee.fct.unl.pt/rit1_2020_2021/pages/IEC_MPLS.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Multivariate Public-Key Cryptography (MPQC)

This refers to public-key multivariate cryptosystems.

*Sources:* Quantum Safe Security Glossary : CSA

### Multivariate Quadratic (MQ) problem

This is a restriction of the PoSSo problem to quadratic polynomials.

*Sources:* Quantum Safe Security Glossary : CSA

### Multivariate-based cryptography

This is a sub-area of quantum-safe cryptography which includes cryptographic schemes whose security is related to PoSSo problem or Multivariate Quadratic (MQ) problems. This problem is also called an MQ problem when the non-linear equations are of degree (at most 2) and remains NP-hard.

*Sources:* Quantum Safe Security Glossary : CSA

### Mutual Transport Layer Security (mTLS)

An approach where each microservice can identify who it talks to, in addition to achieving confidentiality and integrity of the transmitted data. Each microservice in the deployment has to carry a public/private key pair and uses that key pair to authenticate to the recipient microservices via mTLS.

*Sources:* https://cheatsheetseries.owasp.org/cheatsheets/Microservices_security.html#mutual-transport-layer-security

### Mux ID

A 64-bit used to multiplex connections across a single IH-AH tunnel in dynamic tunnel mode. The most significant 32 bits form a unique value assigned by the controller for each remote Service. It is referred to as the service ID of the MID. The least significant 32 bits form a value maintained by the IH and the AH to differentiate among different TCP connections for a specific remote service. This is referred to as the session ID of the MID.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf


## N

### NIPS / NIDS

Network Intrusion Prevention includes taking a preventive measure without direct human intervention. Network Intrusion Detection is the capability to detect actions that attempt to compromise the confidentiality, integrity, or availability of a resource over the network.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### NIPS Events

Network Intrusion Prevention Services (NIPS) events regarding the source and destination of the intrusion attempt.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### NIST Cybersecurity Framework (CSF)

The NIST Cybersecurity Framework (CSF) is a set of guidelines developed by the National Institute of Standards and Technology (NIST) to help organizations manage and reduce cybersecurity risk. The CSF provides a flexible and comprehensive approach to identifying, protecting, detecting, responding to, and recovering from cybersecurity threats. It is widely used across industries to enhance cybersecurity practices and improve resilience against cyber incidents​.

*Sources:* https://www.nist.gov/cyberframework

### NTRU

This is a patented and open-sourced lattice-based cryptosystem used to encrypt and decrypt data. It was developed by J. Hoffstein, J. Pipher, and J. H. Silverman [HPS98]. The signature scheme pqNTRUsign is based on the same underlying hard problem as NTRU and is also quantum-resistant.

*Sources:* [HPS98] J. Hoffstein, J. Pipher, and J. H. Silverman. NTRU: A Ring-Based Public Key Cryptosystem. ANTS-998.

### Network

See Networks

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Network Access Control List (NACL)

A Network Access Control List (NACL) is a set of rules used to control inbound and outbound traffic to and from network subnets. NACLs are used to enhance security by defining which traffic is allowed or denied, providing an additional layer of protection for network access.

*Sources:* https://www.fortinet.com/resources/cyberglossary/network-access-control-list#:~:text=An%20access%20control%20list%20(ACL)%20is%20made%20up%20of%20rules,are%20allowed%20in%20the%20doors .

### Network Policies

With respect to Kubernetes networking, policies that allow rule definitions for controlling traffic flow between pods and namespaces. A CSC can specify which pods can communicate with each other based on labels and selectors. Network policies provide a way to enforce network segmentation and restrict unauthorized access within the cluster.

*Sources:* https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Network Function Virtualization (NFV)

Technology that enables the creation of logically isolated network partitions over shared physical networks so that heterogeneous collections of multiple virtual networks can simultaneously coexist over the shared networks

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec:tr:22417:ed-1:v1:en:term:3.8

### Network (Data in Transit)

See Data in Transit Encryption (DLP in this case)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Network Access Control (NAC)

A method of bolstering the security of a private or “on-premise” network by restricting the availability of network resources to endpoint devices that comply with a defined security policy. NACs address layer 3 access control and connectivity.

*Sources:* SDPs bolster the security of a private or “on-premise” network by securing layer 2 through 7 connectivity. | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Network Address Space

The ability to define network addresses within a virtual workspace to create a virtual network segment separate from that of the physical host machine.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Network Address Translation (NAT)

A function by which internet protocol addresses within a packet are replaced with different IP addresses. This function is most commonly performed by either routers or firewalls. It enables private IP networks that use unregistered IP addresses to connect to the internet. NAT operates on a router, usually connecting two networks together, and translates the private (not globally unique) addresses in the internal network into legal addresses before packets are forwarded to another network.

*Sources:* https://csrc.nist.gov/glossary/term/network_address_translation

### Network Authentication

Authentication services provide methods/protocols for users (or devices) to logon to a network and other benefits (e.g., SSO).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Network Based

Virtualization at the filesystem level (i.e., the host is presented with a virtual filesystem).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Network Events

Events generated by various network elements within the infrastructure including network health, KPIs, and threshold alarms.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Network Security

Consists of security services that allocate network access, distribute, monitor, and protect network services

*Sources:* Defined Categories of Service 2011 : CSA

### Network Segmentation

Splitting a network into sub-networks, for example, by creating separate areas on the network which are protected by firewalls configured to reject unnecessary traffic. Network segmentation minimizes the harm of malware and other threats by isolating it to a limited part of the network.

*Sources:* SDPs provide network segmentation policies using gateways and in addition the segments behind the gateways will block connections and not respond to any requests from clients until they have provided an authentic SDP. | https://www.nist.gov/itl/smallbusinesscyber/cybersecurity-basics/glossary | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Network Services

Concerned with managing the security risks posed by the network environment. Controls at this level include proper network segmentation (for example, assets used by organization A are not visible to organization B) and provision of basic network services such as an accurate and traceable time standard.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Network Virtualization

Concerned with providing appropriate virtual network services. Controls at this level assure that the virtual network implements proper isolation (see ‘segmentation’ above), required connectivity and proper access controls.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Networks

Compliance testing against a series of points or nodes interconnected by communication paths. Networks can interconnect with other networks and contain subnetworks.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Next Generation Firewall (NGFW)

Deep-packet inspection firewalls that move beyond port/protocol inspection and blocking to add application-level inspection, intrusion prevention, and bringing intelligence from outside the firewall. An NGFW should not be confused with a stand-alone network intrusion prevention system (IPS), which includes a commodity or non enterprise firewall, or a firewall and IPS in the same appliance that are not closely integrated.

*Sources:* SDPs can sit behind the NGFWs and look for specific SPA packets prior to allowing authorized connections to services behind the firewall; thus, explicitly allowing authorized connections. | https://www.gartner.com/en/information-technology/glossary/next-generation-firewalls-ngfws | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Next-generation firewall (NGFW)

The distinguishing feature of NGFW is application data awareness. It can look at data not only at layers 3 and 4 of an Open Systems Interconnection (OSI) stack but also at layer 7 – the application level. Its capabilities extend beyond packet filtering and stateful inspection. There are multiple deployment options available for NGFWs, such as an appliance in the data center, as a software running in a VM in a cloud, or as a cloud service (FWaaS). Some capabilities of NGFW include: a. Deep Packet Inspection (DPI) b. TLS decryption and inspection of packet payload c. Intrusion prevention system (IPS) feature

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-215.pdf

### Nodes

Point at which terminals are given access to a network.

*Sources:* https://www.isaca.org/resources/glossary#glossn

### Noise Source

A system the produces non-deterministic random numbers. The noise source contains the non-deterministic, entropy-producing activity [NIST].

*Sources:* [NIST] M. S. Turan, E. Barker, J. Kelsey, K. A. McKay, M. L. Baish and M. Boyle. Recommendation for the Entropy Sources Used for Random Bit Generation (Second DRAFT). NIST Special Publication 800-90B, 2016.

### Non-Human Identity

A non-human identity refers to an identity that is not associated with a human user. This could include an identity associated with an automated process or service, such as a script or an application. Non-human identities are often used to perform tasks that are not performed by human users, such as running a scheduled task or accessing a web service. They also can be used in cases like Internet of Things devices or other machines that can interact with systems with certain permissions.

*Sources:* https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-63a.pdf

### Non-Person Entity (NPE)

An entity with a digital identity that acts in cyberspace, but is not a human actor. This can include organizations, hardware devices, software applications, and information artifacts.

*Sources:* https://csrc.nist.gov/glossary/term/non_person_entity

### Non-deterministic Polynomial time (NP)

This is a complexity class of decision problems in which affirmations (occurrences where the answer is “yes”) can be verified in deterministic polynomial-time.

*Sources:* Quantum Safe Security Glossary : CSA

### Non-deterministic Polynomial-time Hardness (NP-Hard)

Computational problems can be classified in function of their (intrinsic) hardnesses. NP-hard problems are at least as hard as the hardest problem in Non-deterministic Polynomial time (NP). An efficient algorithm for solving any NP-hard problem would lead to an efficient algorithm for all problems in NP. A fundamental assumption of quantum-resistant cryptography is that no NP-hard problem can be solved in deterministic polynomial-time in the classical and quantum setting.

*Sources:* Quantum Safe Security Glossary : CSA

### NonProduction Data

For testing and development purposes in non-production environments, test data should be generated to not host live data in environments with fewer controls. When live data must be used, it should be masked or tokenized to de-identify the personal information it contains.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Nonce

A limited or single-use, typically small value used as an initialization, seed or other special-purpose value.

*Sources:* https://www.isaca.org/resources/glossary#glossz


## O

### OAuth 2.0

OAuth is an IETF standard for authorization that is very widely used for web services (including consumer services). OAuth is designed to work over HTTP and is currently on version 2.0, which is not compatible with version 1.0. To add a little confusion to the mix, OAuth 2.0 is more of a framework and less rigid than OAuth 1.0, which means implementations may not be compatible. It is most often used for delegating access control/authorizations between services.

*Sources:* https://downloads.cloudsecurityalliance.org/assets/research/security-guidance/security-guidance-v4-FINAL.pdf?_ga=2.225992666.1359049959.1661450515-2107700575.1655484199

### OAuth 2.0

OAuth 2.0 is a flexible framework for securing application access to protected resources through APIs. OAuth allows you to decouple clients and resources from the business processes and policy decisions used to authorize access. It’s truly a framework, though, which means that it gives you a structure, but you ultimately must make the decisions about how to authorize access.

*Sources:* https://www.pingidentity.com/en/resources/blog/post/setting-oauth- security-policies-secure-access.html

### OS Virtualization

The capability to have a virtual workspace where different operating systems can be installed based on customer needs.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### OT (Operational Technology)

Operational technology (OT) is hardware and software that detects or causes a change, through the direct monitoring and/or control of industrial equipment, assets, processes and events

*Sources:* https://www.gartner.com/en/information-technology/glossary/operational-technology-ot

### OTP

One Time Password (OTP) is a valid password for a short period (e.g., only one login session or transaction) and is aimed at avoiding several shortcomings associated with traditional static passwords. One of the most popular approaches for generating OTPs is time-synchronization between the authentication server and the client. OTP implementations are often used in two-factor authentication solutions where the user enters a pin used as a variable in an algorithm that generates evidence of identity sent to an enforcement agent that determines if the identity is valid.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Object storage

With respect to cloud-based storage, designed to store and retrieve large amounts of unstructured data, such as documents, images, videos, and backups. It provides a simple application programming interface (API) for storing and accessing objects identified by unique keys. Object storage is highly scalable and durable, making it suitable for various use cases like backup, archiving, and serving static website content

*Sources:* https://cloud.google.com/learn/what-is-object-storage

### Objectives

Measurable objectives for services and their delivery used in assessing performance versus a service level agreement.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Obligation

In XACML, an obligation is a directive from the Policy Decision Point to the Policy Enforcement Point on what action must be completed before or after an access is granted.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### On-Premises

Refers to computers and software installed at an organization’s facility rather than at a remote location or in the cloud.

*Sources:* Disaster Recovery as a Service : CSA

### On-demand self-service

A CSC can unilaterally request cloud resources on demand for automatic provisioning by the CSP and computing capabilities, such as computing time and network storage, as needed without requiring human interaction with each CSP.

*Sources:* https://www.isaca.org/resources/glossary#glosso

### Online Certificate Status Protocol (OCSP)

An online protocol used to determine the status of a public key certificate.

*Sources:* https://csrc.nist.gov/glossary/term/online_certificate_status_protocol

### Open Policy Agent (OPA)

Embraces policy-as-code, complete with tools that help people use and understand the policies they put in place for infrastructure as code (IaC) environments as we as Integrated development environments.

*Sources:* https://www.openpolicyagent.org/

### Open Systems Interconnection (OSI)

Qualifies standards for the exchange of information among systems that are “open” to one another for this purpose by virtue of their mutual use of applicable standards.

*Sources:* https://www.ecma-international.org/wp-content/uploads/s020269e.pdf

### Open-Source Intelligence (OSINT)

Intelligence produced by collecting, evaluating and analyzing publicly available information with the purpose of answering a specific intelligence question.

*Sources:* https://www.sans.org/blog/what-is-open-source-intelligence/

### OpenID Connect

OpenID is a standard for federated authentication that is very widely supported for web services. It is based on HTTP with URLs used to identify the identity provider and the user/ identity (e.g. identity.identityprovider.com). The current version is OpenID Connect 1.0 and it is very commonly seen in consumer services.

*Sources:* https://downloads.cloudsecurityalliance.org/assets/research/security-guidance/security-guidance-v4-FINAL.pdf?_ga=2.225992666.1359049959.1661450515-2107700575.1655484199

### Operational Expenditure (OPEX)

Operational Expenditure (OPEX) refers to the ongoing costs for running a product, business, or system. In the context of IT, OPEX includes expenses related to the day-to-day functioning of IT services, such as salaries, utilities, maintenance, and consumables. OPEX is crucial for the continuous operation and support of IT services and infrastructure​.

*Sources:* https://www.investopedia.com/ask/answers/112814/whats-difference-between-capital-expenditures-capex-and-operational-expenditures-opex.asp

### Operational Budgeting

The planning process used to determine day to day investments such as Maintenance of existing services and infrastructure, applications, among other associated elements that allow the organization to operate. Usually, the Chargeback process is used to distribute these costs across medium to large organizations.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Operational Changes

A type of planned change resulting from ongoing maintenance activities of existing services.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Operational Risk Committee

Ensures that operational considerations are given to all identified business risks. It is not possible to adequately prioritize risk unless true operational considerations are considered.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Operational Risk Management

Operational Risk Management provides a holistic perspective for risk evaluation from the business perspective, using the risk management framework will help to have insight into risks and threats to the organization, as well the framework will provide means to assess, manage, and control the different risks across the organization. The use of an Operational Risk Committee (ORC) should be in place to periodically discuss the threat and compliance landscape that the organization has throughout time. Usually, the participants for this committee are conformed by the business (i.e., CEO, COO, CIO, CFO), compliance (CRO, Compliance Officers), and Control personnel (Audit, Security, and Risk Management). The use of Business Impact Assessment methodologies will help the organization identify which processes are critical for the organization and plan accordingly to protect them, ensure proper continuity plans and measure the associated risk using Key Risk Indicators. Key Risk Indicators can be monitored periodically through a Risk Scorecard, integrating information from Security Monitoring Services or information consolidated on the Information Services Domain.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Operational Security Baselines

A baseline specifies a policy compliant starting point that may be further specialized (e.g., a move to production process may include a baseline configuration that requires all default users/passwords, SNMP community names, etc. be changed from their default values before the equipment may be used in production. If the equipment were subject to additional hardening, such as deployment in the DMZ, further specialized baselines would apply).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Operational-Level Agreement (OLA)

An operational-level agreement (OLA) defines the interdependent relationships among the internal support groups of an organization working to support a service-level agreement (SLA). The agreement describes each internal support group’s responsibilities toward other support groups, including the process and timeframe for delivery of their services. The OLA’s objective is to present a clear, concise, and measurable description of the service provider’s internal support relationships.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Operator

The individual or organization responsible for the set of processes to deploy and manage IT services. They ensure the smooth functioning of the infrastructure and operational environments that support application deployment to internal and external customers, including the network infrastructure, server and device management, computer operations, IT infrastructure library (ITIL) management, and help desk services.

*Sources:* Cloud Security Alliance. Challenges in Securing Application Containers and Microservices Integrating Application Container Security Considerations into the Engineering of Trustworthy Secure Systems (Cloud Security Alliance: 2019) 42

### Orchestration

Orchestration in cloud computing involves the automated arrangement, coordination, and management of complex computer systems, middleware, and services. It ensures that workflows and processes are executed efficiently across multiple systems, often utilizing tools that automate the deployment, scaling, and operation of applications. This helps in managing dependencies, scaling resources, and optimizing performance in a cloud environment.

*Sources:* https://www.sumologic.com/glossary/cloud-orchestration/

### Organization

With respect to cloud deployments, denotes the highest level of structure within a cloud provider, equivalent to an Organization in AWS or GCP, or a Tenant in Azure.

*Sources:* https://www.isaca.org/resources/glossary#glosso

### Orphan Incident Management

Identification of incidents that do not have a current owner, so that appropriate resources can be engaged to resolve the problems.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Out of the Box (OTB) Authentication

A method for implementing user login functionality in the applications through the identity provider’s service without custom authentication code.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Out-of-Vocabulary

Words that a language model has not encountered during its training phase. These could be new words, rare words, or words from languages that the model was not trained on. The challenge with OOV words is that since the model has no prior knowledge of these words, it struggles to interpret them and their context, leading to potential inaccuracies in understanding and generating language.

*Sources:* https://www.chatgptguide.ai/2024/03/01/what-is-out-of-vocabulary-oov-words-llms-explained/

### Overlay Network

With respect t odocker networking, Overlay networks allow containers running on different hosts to communicate seamlessly. This is achieved by creating a distributed network across multiple hosts using VXLAN or IPSec tunnels. Overlay networks are commonly used in multi-host Docker deployments.

*Sources:* https://docs.docker.com/network/drivers/overlay/

### Owner

In a cloud deployment registry, the business owner responsible for each cloud environment. This ensures accountability, responsibility, and clear lines of communication for decision-making and resource allocation.

*Sources:* https://www.isaca.org/resources/glossary#glosso


## P

### PAC (Programmable Automation Controllers)

A programmable automation controller (PAC) is a term used to describe any type of automation controller that incorporates higher-level instructions.

*Sources:* A PAC makes it possible to provide more complex instructions to automated equipment, enabling similar capabilities as that of PCbased controls, in an all-in-one package, like a programmable logic controller (PLC). | Higher-end PLCs with increased capabilities are often marketed as PAC. | https://whatis.techtarget.com/definition/programmable-automation-controller-PAC

### PCS (Process Control System)

Process control systems (PCS) — sometimes called industrial control systems (ICS) — function as pieces of equipment along the production line during manufacturing that tests the process in a variety of ways, and returns data for monitoring and troubleshooting. Many types of process control systems exist, including supervisory control and data acquisition (SCADA), programmable logic controllers (PLC), or distributed control systems (DCS), and they work to gather and transmit data obtained during the manufacturing process

*Sources:* https://www.thebalancesmb.com/process-control-systems-pcs-2221184

### PERA (Purdue Enterprise Reference Architecture)

PERA is a structure with which to design enterprise architectures. It includes a generalized model of the life cycle of an enterprise, and a methodology for planning the evolution of the enterprise. The PERA methodology is unique, in that it: 1. Specifically addresses the human and organizational aspects of the enterprise. 2. It is designed to address all phases of an enterprise from planning, to operations and renewal. 3. Integrates facility engineering and IT systems development methodologies 4. Addresses both process industries and discrete manufacturing (PERA). This model can be used for a variety of purposes including ICS Kill Chain Analysis (SANS) as well as ICS Network Segmentation Analysis (SEQ).

*Sources:* http://www.pera.net/ and https://www.sans.org/reading-room/whitepapers/ICS/industrial-control-system-cyber-kill-chain-36297 Page 13 and: https://seqred.pl/en/ot_network_segmentation/

### PLC (Programmable Logic Controllers)

A solid-state control system with a user-programmable memory to store instructions for the purpose of implementing specific functions such as I/O control, logic, timing, counting, three mode (PID) control, communication, arithmetic, and data and file processing.

*Sources:* NIST SP 800-82r2 https://csrc.nist.gov/publications/detail/sp/800-82/rev-2/final

### PROTECT (PR)

In the NIST Cybersecurity Framework (CSF), the process that is used as safeguards to prevent or reduce cybersecurity risk.

*Sources:* https://www.nist.gov/cyberframework/protect

### Paravirtualization

A virtualized operating system where the source code for the guest operating system is modified to run specifically as a guest operating system instead of a binary equivalent of the original hardware-targeted operating system.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Pass-The-Hash

Adversaries may “pass the hash” using stolen password hashes to move laterally within an environment, bypassing normal system access controls. Pass the hash (PtH) is a method of authenticating as a user without having access to the user’s cleartext password. This method bypasses standard authentication steps that require a cleartext password, moving directly into the portion of the authentication that uses the password hash.

*Sources:* https://attack.mitre.org/techniques/T1550/002/

### Pass-The-Ticket

Adversaries may “pass the ticket” using stolen Kerberos tickets to move laterally within an environment, bypassing normal system access controls. Pass the ticket (PtT) is a method of authenticating to a system using Kerberos tickets without having access to an account’s password. Kerberos authentication can be used as the first step to lateral movement to a remote system.

*Sources:* https://attack.mitre.org/techniques/T1550/003/

### Password

A string of characters (letters, numbers, and other symbols) used to authenticate an identity or to verify access authorization.

*Sources:* https://csrc.nist.gov/glossary/term/password#:~:text=memorized%20 secret%20show%20sources,or%20to%20verify%20access%20 authorization

### Password Management

The process to specify multiple password policies, define password composition constraints, maintain password history, restrict passwords, configure password validity period, create password rules, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Password Spray

Password spraying is a type of brute force attack. In this attack, an attacker will brute force logins based on a list of usernames with default passwords on the application. For example, an attacker will use one password (say, Secure@123) against many different accounts on the application to avoid account lockouts that would normally occur when brute forcing a single account with many passwords. This attack can be found commonly where the application or admin sets a default password for the new users.

*Sources:* https://owasp.org/www-community/attacks/Password_Spraying_ Attack#:~:text=Password%20spraying%20is%20a%20type,default%20 passwords%20on%20the%20application

### Password Vaulting

A software based solution to securely store and manage multiple passwords.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Passwordless Authentication

Passwordless authentication is signing into a service without using a password. This is often done with certificates, security tokens, one-time passwords (OTPs), or biometrics. Passwordless authentication is generally considered more secure than using passwords.

*Sources:* https://www.techtarget.com/searchsecurity/definition/passwordless- authentication

### Patch Management

Concerned with assuring that required software fixes are applied in a controlled and timely fashion within the infrastructure. This includes both inventorying the services (operating systems, applications, embedded software, etc.) actually present in the infrastructure to identify the applicability of a particular fix and monitoring the infrastructure to assure that required fixes are actually present and installed.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Peer-to-Peer (P2P)

Peer-to-Peer (P2P) applications allow users within an enterprise to connect directly to each other to exchange instant messages or files.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Penetration Testing

A method of evaluating the security of a computer system or network by simulating an attack from malicious outsiders (who do not have an authorized means of accessing the organization’s systems) and malicious insiders (who have some level of authorized access), also referred as pentest.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Persona

A user-centric view to help understand how different user types interact with the system. It represents a category of users with similar characteristics and leads to the development of roles.

*Sources:* https://csrc.nist.gov/glossary/term/persona

### Personally identifiable information (PII)

Information that can be used to distinguish or trace an individual’s identity—such as name, social security number, biometric data records—either alone or when combined with other personal or identifying information that is linked or linkable to a specific individual (e.g., date and place of birth, mother’s maiden name, etc.).

*Sources:* https://csrc.nist.gov/glossary/term/personally_identifiable_information

### Phishing

A technique for attempting to acquire sensitive data, such as bank account numbers, through a fraudulent solicitation in email or on a web site, in which the perpetrator masquerades as a legitimate business or reputable person.

*Sources:* https://csrc.nist.gov/glossary/term/phishing

### Physical Authentication

The process of verifying an asserted identity by physical means (e.g., a security guard verifying the photograph on an ID as matching the person providing it).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Physical Inventory

This process tracks all the physical components across the Information Technology organization. Also tracks the ownership and custody for these assets.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Physical Security

Concerned with mitigating physical threats to a facility and its employees (e.g., fire suppression equipment and regular fire drills).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Plan Management

The overall process for assuring that the DRP is continuously updated to reflect changes in the business and its critical functions.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Planned Changes

Planned changes are changes that are identified well in advance of their needed implementation. These changes are carefully thought through and fully documented.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Platform as a Service (PaaS)

abstracts and provides platforms, such as application platforms (e.g., a place to develop and run code), databases, file storage, and collaborative environments. Other examples include application processing environments for machine learning, big data processing or API access to SaaS functions. The key differentiator is that, with PaaS, the CSC does not manage the underlying infrastructure.

*Sources:* https://csrc.nist.gov/glossary/term/platform_as_a_service

### Playbook

Generic documents, outlining the organization’s approach and worker responsibilities that result in a standard set of operational procedures (playbook) to be used in planning and conducting cybersecurity vulnerability and incident response activity.

*Sources:* https://www.cisa.gov/sites/default/files/2024-03/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf

### PoSSo problem

This is the Non-deterministic Polynomial-time hardness (NP-hard) problem of solving a set of non-linear equations.

*Sources:* Quantum Safe Security Glossary : CSA

### Pod Networking

With respect to Kubernetes networking, pods are the smallest deployable units and can contain one or more containers. Each pod gets its IP address, and containers within a pod share the same network namespace, allowing them to communicate using localhost. Kubernetes requires a Container Network Interface (CNI) plugin to handle pod networking.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf

### Point-in-time Assessment (PITA)

A complete, consolidated, and fully integrated reviews that provides assurance activities, giving DevSecOps teams confidence that a significant number of security issues have been addressed during each build.

*Sources:* https://cloudsecurityalliance.org/

### Policies & Standards

Security policies are part of a logical abstraction of an Enterprise Security Architecture. They are derived from risk-based business requirements and exist at several different levels including, Information Security Policy, Physical Security Policy, Business Continuity Policy, Infrastructure Security Policies, Application Security Policies, and the overarching Business Operational Risk Management Policy. Security Policies are statements that capture requirements specifying what type of security and how much should be applied to protect the business. Policies typically state what should be done while avoiding reference to particular technical solutions. Security Standards are an abstraction at the component level and are needed to ensure that the many different components can be integrated into systems. There are many internationally recognized standards for security from standards bodies such as ISO, IETF, IEEE, ISACA, OASIS, and TCG. Direction can also be provided in operational security baselines, job aid guidelines, best practices, correlation of regulatory requirements, and role-based awareness. One way to approach security policy and its implementation is to classify information and associate policies with the resulting classes of data.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Policy

Policy intentions and direction of an organization as formally expressed by its top management.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso:9000:ed-4:v1:en:term:3.5.8

### Policy Administrator

This component is responsible for establishing and/or shutting down the communication path between a subject and a resource (via commands to relevant PEPs).

*Sources:* See also: Policy Engine | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf

### Policy Definition

A phase in authorization services that describe course or fine grained access or constraints to resources.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Policy Enforcement

A phase in Authorization Services, where access requests are approved or disapproved.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Policy Engine

This component is responsible for the ultimate decision to grant access to a resource for a given subject. The PE uses enterprise policy as well as input from external sources as input to a trust algorithm to grant, deny, or revoke access to the resource. The PE is paired with the policy administrator component. The policy engine makes and logs the decision (as approved, or denied), and the policy administrator executes the decision.

*Sources:* See also: Policy Administrator | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf

### Policy Management

A process or platform for centralized policy creation, repository and management. Policy management strives to maintain an organization structure and process that supports the creation, implementation, exception handling, and frameworks that represent business requirements.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Policy as Code (PaC)

Enables organizations to implement, validate, and measure policies at scale.

*Sources:* https://ieeexplore.ieee.org/document/10162940

### Policy decision point (PDP)

Mechanism that examines requests to access resources, and compares them to the policy that applies to all requests for accessing that resource to determine whether specific access should be granted to the particular requester who issued the request under consideration.

*Sources:* https://csrc.nist.gov/glossary/term/policy_decision_point

### Policy enforcement point (PEP)

A system entity that requests and subsequently enforces authorization decisions.

*Sources:* https://csrc.nist.gov/glossary/term/policy_enforcement_point

### Policy information point (PIP)

Serves as the retrieval source of attributes, or the data required for policy evaluation to provide the information needed by the PDP to make the decisions.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-162.pdf

### Policy-Based Access Control (PBAC)

A strategy for managing user access to one or more systems, where the business roles of users is combined with policies to determine what access privileges users of each role should have. Theoretical privileges are compared to actual privileges, and differences are automatically applied. For example, a role may be defined for a manager. Specific types of accounts on the single sign-on server, Web server, and database management system may be attached to this role. Appropriate users are then attached to this role.

*Sources:* https://csrc.nist.gov/glossary/term/policy_based_access_control

### Politically Exposed Person

Someone who, through their prominent position or influence, is more susceptible to being involved in bribery or corruption.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

### Port

Another essential asset through which security can be breached. In computer science, ports are of two types - physical ports (which is a physical docking point where other devices connect) and logical ports (which is a well-programmed docking point through which data flows over the internet). Security and its consequences lie in a logical port.

*Sources:* https://www.w3schools.in/cyber-security/ports-and-its-security/

### Port Address Translations (PAT)

Port Address Translation (PAT) is a feature of a network device that translates communications made between hosts on a private network and hosts on a public network.

*Sources:* http://web.cse.ohio-state.edu/~athreya.14/cse3461-5461/Cse3461.NAT-PAT.pdf

### Port Knocking

Port-knocking is the concept of hiding remote services behind a firewall which allows access to the services’ listening ports only after the client has successfully authenticated to the firewall.

*Sources:* https://ieeexplore.ieee.org/document/7600145

### Portable Devices

Devices that are not easily movable and are designed to be used from only one location.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Portfolio Management

This container is focused on planning, tracking, prioritizing current and future projects and programs for the enterprise.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Post-quantum cryptography

This refers to the set of cryptographic schemes which will remain secure even in a world where quantum computers exist. This includes quantum cryptosystems such as Quantum-Key Distribution (QKD); algorithmic-based cryptosystems such as lattice-based, code-based, multivariate-based, hashbased and isogeny-based cryptosystems; and symmetric key cryptographic systems such as AES. Terminology related to post-quantum cryptography appeared in academic literature soon after P.W Shor’s quantum polynomialtime algorithm for solving integer factorizations and discrete logarithm was introduced. Note that there remains some ambiguity around this term, with some organizations not including QKD.

*Sources:* Quantum Safe Security Glossary : CSA

### Power Redundancy

Providing multiple sources of electrical power to assure continuous operation in spite of loss of external utility power.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Presentation Modality

The Presentation Modality Services focus on the security concerns that differ based on user and service type. The two major types are Consumer Service Platforms like Social Media, Collaboration, Search, Email and e-Readers, and Enterprise Service Platforms like Business-to-Consumer (B2C), Business-to-Employee(B2E), Business-to-Business (B2B), etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Presentation Platform

The Presentation Platform Services focus on the different types of Endpoints that end-users utilize to interact with a solution such as Desktops, Mobile Devices (smartphones, tablets), Portable Devices (laptops), or special purposes devices such as medical devices or smart appliances. The presentation platform also includes different interaction technologies such as Speech Recognition or Handwriting Recognition that could be used to interact with a solution.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Presentation Services

The Presentation Services domain is where the end-user interacts with an IT solution. Presentation is the website you see when you go to an online bank. It is the voice on the phone when you call the airline reservation system or the mobile platform when you order remotely.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Principal Data Management

The capability for the management of all attributes regarding the subjects of access control decisions. These principals can be users, machines, or services. Authorization decisions may need to consider many attributes about the principals, including role, location, relationships to accounts, other principals, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Principle of Least Privilige

The principle that a security architecture is designed so that each entity is granted the minimum system authorizations and resources that the entity needs to perform its function.

*Sources:* See also: Principle of Need to Know | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r2.pdf

### Principle of Need to Know

Decision made by an authorized holder of official information that a prospective recipient requires access to specific official information to carry out official duties.

*Sources:* See also: Principle of Least Privilige | https://csrc.nist.gov/glossary/term/need_to_know

### Private cloud

The cloud infrastructure is provisioned for exclusive use by a single organization comprising multiple consumers (e.g., business units). It may be owned, managed, and operated by the organization, a third party, or some combination of them, and it may exist on or off-premises.

*Sources:* NIST 2011, The NIST Definition of Cloud Computing, https://csrc.nist.gov/publications/detail/ sp/800-145/final

### Privilege Management Infrastructure

Privilege Management Infrastructure ensures users have access and privileges required to execute their duties and responsibilities with Identity and Access Management (IAM) functions such as identity management, authentication services, authorization services, and privilege usage management. This security discipline enables the right individuals to access the right resources at the right times for the right reasons. It addresses the mission-critical need to ensure appropriate access to resources across increasingly heterogeneous technology environments and meet increasingly rigorous compliance requirements. This security practice is a crucial undertaking for any enterprise. The technical controls of Privilege Management Infrastructure focus on identity provisioning, password, and multi-factor authentication, policy management, etc. It is also increasingly business-aligned, and it requires business skills, not just technical expertise.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Privilege Usage Events

Events indicating administrative changes made to the system which could impact confidentiality, availability, or integrity of the system.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Privilege Usage Gateway

A gateway to grant/deny connection for sessions based on usage privilege on that workload.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Privilege Usage Management

Management of access to sensitive information resources by privileged users such as administrators. Characteristics of robust management include that it be centralized, policy-driven, automated, granular, and auditable. A privileged user management system can control access to the administrative accounts used to install, configure, administer, and manage operating systems, applications, and databases.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Privileged Account Management

A domain within identity and access management (IdAM) that focuses on monitoring and controlling the use of privileged accounts. Privileged accounts include local and domain administrative accounts, emergency accounts, application management, and service accounts.

*Sources:* SDP is often used to control access by users or services with privileged accounts, increasing the security and visibility of access by these accounts by instantly providing information about the users making connections and from what device. | https://www.nccoe.nist.gov/sites/default/files/legacy-files/fs-pam-nist-sp1800-18-draft.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Privileged Identity Management (PIM)

Data types such as contacts, calendar entries, tasks, notes, memos, and email that may be synchronized from PC to device and vice-versa.

*Sources:* https://csrc.nist.gov/glossary/term/personal_information_management

### Privileged access workstation (PAW)

A Privileged Access Workstation (PAW) is a dedicated computing environment for sensitive tasks that is protected from Internet attacks and other threat vectors.

*Sources:* https://uit.stanford.edu/service/paw

### Problem Management

Process of managing recurring incidents as problems to find and fix root causes to prevent future events from recurring.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Problem Resolution

The process of identifying the appropriate changes to configuration items and/or processes necessary to address the root cause of a problem to minimize the likelihood of recurrence.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Process Ownership

Documentation regarding the business processes and the responsible parties for oversight and operations of those processes.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Product Owner

The person who identifies the customer need and the larger business objectives that a product or feature will fulfill, articulates what success looks like for a product, and drives a team to turn product vision into a reality

*Sources:* Mansour, S. (2020). Product Manager . Atlassian Software. https://www.atlassian.com/agile/ product-management/product-manager. | Agile Alliance. Product Owner . Accessed August 10, 2021 at https://www.agilealliance.org/ glossary/product-owner/.

### Program Management

Program management deals with the incident after it has begun the cycle through the remediation process. Program management architecture interacts with the service desk. Program management offers advanced root cause analysis tools and technologies and interfaces with the information repositories to perform trending and prevention services within the environment.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Programming Interfaces

[Application] Programming Interfaces (APIs) allow applications or services to talk to another or allow pieces of an application to talk to each other. Input validation is important for these interfaces to make sure that only the expected input is being provided. Lack of this validation can create vulnerabilities by allowing attackers to inject malicious code into the application or retrieve more data than they are supposed to access.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Project Changes

A type of planned change resulting from a project. Project changes occur due to implementation or changes to business requirements.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Project Management

All processes, artifacts, and methodologies associated with the Project Management Office to track projects (best practices include PMI Body of Knowledge among others).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Project Management Office (PMO)

The Project Management Office (PMO) is the department or group that defines and maintains the standards of process, generally related to project management within the organization. The PMO strives to standardize and introduce economies of repetition in the execution of projects. The PMO is the source of documentation, guidance, and metrics on the practice of project management and execution. In some organizations, this is known as the Program Management Office.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Prompt Engineering

A way to get the desired output with an AI tool. Prompts come in various forms, such as statements, blocks of code, and strings of words. Multitasking promt engineering is used with natural language processing to accurately depict a logical thought process. Zero-shot learning has been applied when cues such as “Let’s think step by step”.

*Sources:* https://www.unite.ai/what-is-prompt-engineering-in-ai-why-it-matters/

### Prompt Temperature

A parameter that is a crucial element in AI text generation, controlling the level of randomness in the model’s output. A higher temperature value (e.g., 1.0 or above) will result in more diverse and creative text, while a lower value (e.g., 0.5 or below) will yield more focused and deterministic outputs.

*Sources:* http://www.aicontentcreate.com/prompt-engineering/advanced-prompt-engineering/prompt-engineering-temperature-and-top-k-sampling.html

### Propagation

Propagation refers to the propagation of a security context through different services.

*Sources:* Microservices Architecture Pattern : CSA

### Protect surface

The area that the zero trust policy protects. ▪ Each protect surface contains a single data, applications, assets, and services (DAAS) element. ▪ Each zero trust environment will have multiple protect surfaces.

*Sources:* https://cloudsecurityalliance.org/artifacts/report-to-the-president-on-zero-trust-and-trusted-identity-management/

### Public Cloud

The cloud infrastructure is provisioned for open use by the general public. It may be owned, managed, and operated by a business, academic, or government organization, or some combination of them. It exists on the premises of the cloud provider.

*Sources:* NIST 2011, The NIST Definition of Cloud Computing, https://csrc.nist.gov/publications/detail/ sp/800-145/final

### Public Key Infrastructure (PKI)

The framework and services that provide for the generation, production, distribution, control, accounting, and destruction of public key certificates. Components include the personnel, policies, processes, server platforms, software, and workstations used for the purpose of administering certificates and public-private key pairs, including the ability to issue, maintain, recover, and revoke public key certificates.

*Sources:* SDPs may use PKI for generation of TLS certificates and for secure connections. If no PKI infrastructure exists, SDPs can provide TLS certificates for use to secure connections. | https://csrc.nist.gov/glossary/term/public_key_infrastructure | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Public Kiosk

Public Kiosks are devices, often PCs, that are used by multiple people in a shared space.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain


## Q

### Qualitative Risk Assessment

A method for risk analysis that is based on the assignment of a descriptor such as low, medium, or high.

*Sources:* https://csrc.nist.gov/glossary/term/qualitative_risk_analysis

### Quality of Service (QoS)

The ability to provide different priority to different applications, users, or data flows, or to guarantee a certain level of performance to a data flow.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso:20205:ed-1:v1:en:term:1.6.3

### Quantum Random Number Generator (QRNG)

This refers to quantum-based noise source that derives random numbers from measurements conducted on a quantum process or quantum system. The uniqueness and randomness of these measurements/outcomes are of quantum origin, as described by quantum mechanics. Examples of QRNGs include several commercial systems that generate random numbers from measurements made on optical quantum states of light.

*Sources:* Quantum Safe Security Glossary : CSA

### Quantum annealing

This is a quantum process that solves optimization problems faster than if utilizing a classical computer.

*Sources:* Quantum Safe Security Glossary : CSA

### Quantum bit or Qubit

Quantum Safe Security Glossary : CSA

### Quantum computer

A variant of quantum-resistant cryptography used recently by the International Organization for Standardization (ISO).

*Sources:* Quantum Safe Security Glossary : CSA

### Quantum cryptography

This refers to cryptosystems whose security is guaranteed by the physical law of quantum mechanics. It differs from classical public-key cryptography, whose security relies on the difficulty of solving certain mathematical problems.

*Sources:* Quantum Safe Security Glossary : CSA

### Quantum-Key Distribution (QKD)

Quantum-Key Distribution is an example of quantum cryptography that allows the information-theoretically secure distribution of keys between two spatially separate parties who are also connected by an insecure optical channel. There are two complementary approaches to QKD: (1) discrete variable quantum key distribution (DVQKD) uses single-photons or weak coherent states and single photon detectors; and (2) continuous variable quantum key distribution (CVQKD), which uses coherent or squeezed states of light and homodyne detectors. Both continuous and discrete approaches have been experimentally demonstrated; just as importantly, both have been proven to be information-theoretically secure.

*Sources:* Quantum Safe Security Glossary : CSA

### Quantum-resistant cryptography

This term also refers to the set of cryptographic schemes which will remain secure even in a world where quantum computers exist. This terminology was used by the United States National Security Agency in their announcement regarding their, “preliminary plans for transitioning to quantum resistant algorithms.” This term is not completely equivalent to post-quantum cryptography, as it only refers to algorithmic techniques. Additionally, it does not appear to include physical technology such as Quantum-Key Distribution (QKD).

*Sources:* Quantum Safe Security Glossary : CSA

### Quantum-safe cryptography

This refers to the set of cryptographic schemes which will remain secure even in a world where quantum computers exist. The term was recently coined, but is often used interchangeably with the term “post-quantum cryptography.” Furthermore, it has been used by working groups in the European Telecommunications Standards Institute (ETSI) and the Cloud Security Alliance (CSA).

*Sources:* Quantum Safe Security Glossary : CSA


## R

### RA

Documentation of the scope and results of Risk Assessments (RA).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### RECIPE PICKS

a mnemonic developed by Rich Mogull of Securosis for training cloud incident responders on their initial analysis priorities. These represent the first places to focus analysis during a cloud management plane incident and can be used to resolve a high percentage of incidents. The mnemonic stands for Resource, Events, Changes, Identity, Permissions, Entitlements, Public, IP, Caller, TracK, ForenSics.

*Sources:* https://securosis.com/blog/resolve-90-of-cloud-incidents-with-recipe-picks/

### RECOVER (RC)

In the NIST Cybersecurity Framework (CSF), the process that is used to restore assets and operations that were impacted by a cybersecurity incident.

*Sources:* https://www.nist.gov/cyberframework/recover

### RESPOND (RS)

In the NIST Cybersecurity Framework (CSF), the process that is used to take action regarding a detected cybersecurity incident.

*Sources:* In the NIST Cybersecurity Framework (CSF), the process that is used to take action regarding a detected cybersecurity incident.

### REST (Representational State Transfer)

REST (REpresentational State Transfer) is an architectural style that defines a set of constraints to be used for developing web services that use the Hypertext Transfer Protocol (HTTP/S). A RESTful interface provides interoperability between computer systems on the Internet and allows the requesting system to access and manipulate data by a uniform set of stateless operations. Data in devices not yet IoT enabled can be utilized by any application that can make RESTful HTTPS requests to read and write data from devices such as controllers.

*Sources:* https://www.controldesign.com/articles/2016/it-invades-controller-programming/ and https://en.wikipedia.org/wiki/Representational_state_transfer

### RTUs (Remote Terminal Units)

Remote Terminal Units (RTU) are also referred to as Remote Telemetry Units. An RTU is an electronic device which is controlled by a microprocessor. The main function of an RTU is to interface the SCADA or Distributed Control System (DCS) to physically present objects. The functionality of RTUs and PLCs has started to overlap due to cheaper hardware, thus encouraging the industry to standardize the language for programs on which RTUs run.

*Sources:* http://www.differencebetween.net/technology/industrial/difference-between-plc-and-rtu/

### Ransomware

Ransomware is malicious software that gains access to an organization’s systems and data and then encrypts these systems and data rendering them inaccessible without the encryption key. The attacker supplies the decrypt key only if the victim pays a fee (ransom). Ransomware can gain access to systems through such avenues as users interacting with phishing emails or infected websites.

*Sources:* Disaster Recovery as a Service : CSA

### Rapid Elasticity

Resources can be rapidly and elastically provisioned, in some cases automatically, to rapidly scale out and back. To the CSC, the provisioned capabilities often appear unlimited and can be purchased in any quantity at any time

*Sources:* https://csrc.nist.gov/glossary/term/rapid_elasticity

### Real Time Filtering

A control to track use patterns and information like what sites are visited and blocked some in real-time based on policies.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Real-Time Internet Work Defense (SCAP)

Security Content Automation Protocol is a continuous assurance process that verifies compliance with security policies and procedures in real time.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Recovery Plans

Recovery plans describe the processes and procedures required to restore service delivery after interruption or disaster. The plans will often include steps to gradually restore the service while monitoring the performance and system health of every reached milestone.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Recovery Point Objective (RPO)

The point in time to which data must be recovered after an outage.

*Sources:* https://csrc.nist.gov/glossary/term/recovery_point_objective

### Recovery Time Objectives (RTO)

The overall length of time an information system’s components can be in the recovery phase before negatively impacting the organization’s mission or mission/business processes.

*Sources:* https://csrc.nist.gov/glossary/term/recovery_time_objective

### Recurrent Neural Network

A type of Neural Network where the output from the previous step is fed as input to the current step. In traditional neural networks, all the inputs and outputs are independent of each other. The main and most important feature of RNN is its Hidden state, which remembers some information about a sequence. The state is also referred to as Memory State since it remembers the previous input to the network.

*Sources:* https://www.geeksforgeeks.org/introduction-to-recurrent-neural-network/

### Red Teaming

the process of testing your cybersecurity effectiveness through the removal of defender bias by applying an adversarial lens to your organization. Red teaming occurs when ethical hackers are authorized by your organization to emulate real attackers’ tactics, techniques and procedures (TTPs) against your own systems.

*Sources:* https://csrc.nist.gov/glossary/term/red_team

### Reduced Instruction Set Computer (RISC)

RISC is a design philosophy aimed at delivering simple but powerful instructions that execute within a single cycle at a high clock speed. The RISC philosophy concentrates on reducing the complexity of instructions performed by the hardware because it is easier to provide greater flexibility and intelligence in software rather than hardware. As a result, a RISC design places greater demands on the compiler.

*Sources:* https://www.sciencedirect.com/topics/computer-science/reduced-instruction-set-computer

### Refactoring

applications are modified and optimized to leverage cloud-native services and features as much as possible, it is more time consuming than rehosting, but allows for improved performance, scalability, and resilience. It requires updating security policies, procedures, and staff skills for the refactored application.

*Sources:* https://www.agilealliance.org/glossary/refactoring/

### Reference architectures

Templates for implementing cloud security, typically generalized (e.g., an IaaS security reference architecture). They can be very abstract, bordering on conceptual, or they can be quite detailed, down to specific controls and functions.

*Sources:* https://dodcio.defense.gov/Portals/0/Documents/Ref_Archi_Description_Final_v1_18Jun10.pdf

### Reflexive Security

Reflexive Security is an approach for information security management built upon the principles of Agile and DevOps. It is a non-prescriptive framework that is purely needs-based, emphasizes collective responsibility, and considers information security and its responses to be a holistic function of the organization.

*Sources:* Reflexive Security emphasizes security across organizational roles that reacts to external and internal threats in an agile and dynamic way. It aims to be a new information security management strategy that is dynamic, interactive, effective and holistic. | As defined in ISO 27000 and Information Security Management through Reflexive Security : CSA .

### Registry Services

Registry services catalog services available within the IT infrastructure and the metadata around how they should be accessed.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Rehosting (Lift & Shift)

applications are moved to the cloud with minimal changes, retaining the existing architecture, it is the fastest migration approach but the least optimized for the cloud. In terms of security considerations, existing security controls and issues may not effectively transfer to the cloud due to architectural differences.

*Sources:* https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html

### Release Management

The release management architecture is the set of conceptual patterns that support the movement of pre-production technical resources into production. Pre-production includes all the activities that are necessary to prove that a particular resource is appropriate for the technical, business, and operational environment and does not exceed a risk profile for a particular task. Significant release management patterns include those for release scheduling, release acceptance, and audit. Release management plays a vital role both as a process and as a set of technologies and it provides a vital control point for request, change, and configuration management processes and architectures.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Relying party (RP)

A service that relies on an identity provider (IdP) to verify a user’s identity and access rights and then grants entitlements to its own resources. Sometimes referred to as Service Provider.

*Sources:* https://csrc.nist.gov/glossary/term/relying_party

### Remediation

This capability is focused on projects that are remediating existing gaps, or findings that affect the enterprise. A remediation dashboard is recommended to be used to track progress for senior management.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Remote

A virtual machine that is delivered over the network as opposed to being installed locally on a device.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Reportable Incidents

Incidents deemed to have a significant enough impact that they need to be reported outside the entity according to laws or regulations.

*Sources:* Cloud Penetration Testing : CSA

### Reporting Services

Reporting services provide the ability to present data in various ways going from a top-level aggregated dashboard, drilling down to raw data. Reporting services also offer the ability to mine and analyze data and provide business intelligence to decision-makers

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Reporting Tools

Reporting tools provide end-users with the ability to generate reports, share reports with other users, and analyze the information domain’s data.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Repudiation

Creating a situation of dispute, lack or compromise of the authenticity of a record or data. In cloud testing repudiation often takes the form of deleting or turning off cloud logs or leveraging cloud services and mechanisms to mask an action or occurrence.

*Sources:* Cloud Penetration Testing : CSA

### Residual Risk Management

Analysis and plans for remediating information security risk that remains after the theoretical or applied implementation of mitigating controls with the intent of increasing control effectiveness and ultimately reducing risk to an acceptable level.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Resiliency Analysis

The process that assesses the ability of an organization to continue to deliver services despite the occurrence of various events (e.g., loss of power, loss of network connectivity, etc.).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Resource logs

For resources like VMs, databases, and software-defined networks that record every operation and change. These include events, such as resource provisioning, configuration changes, data access and transfers, and system-level activities. They provide insight into operations that were performed within the resource. The content of resource logs varies by service and resource type.

*Sources:* https://learn.microsoft.com/en-us/azure/azure-monitor/data-sources

### Resource pooling

Cloud computing pools various physical and virtual resources to serve multiple CSCs using a multi-tenant model. These resources, like storage, processors, memory, and network bandwidth, are dynamically assigned and reassigned according to demand.

*Sources:* https://csrc.nist.gov/glossary/term/resource_pooling

### Resource Data Management

Authorization plays a key role in data management by simultaneously providing access and protection to application information resources.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Resource Management

Resource management deals with the accurate assignment of resources to IT service delivery functions. It is considered a sharable service, separate from project management since the same patterns can be applied to solve operational, production, and emergency resource allocations. Resource management includes technologies that assist in resource pooling, forecasting, and leveling. Other resource management functions are more strictly related to solutions for Human Resources management. This service does provide valuable input into the BOSS Domain for costing, forecasting, and planning activities.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Resource Protection

Prevention of misuse of computer resources.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Resource portal-based deployment

In this deployment model, the PEP is a single component that acts as a gateway for subject requests. The gateway portal can be for an individual resource or a secure enclave for a collection of resources used for a single business function.

*Sources:* https://csrc.nist.gov/publications/detail/sp/1800-35/draft

### Responsible, Accountable, Consulted, and Informed (RACI) chart

A RACI chart (RACI matrix) clarifies roles and responsibilities, making sure that nothing falls through the cracks. RACI charts also prevent confusion by assigning clear ownership for tasks and decisions.

*Sources:* https://racichart.org/

### Ring-LWE (RLWE) problem

This is a variant of the Learning with Errors (LWE) problem in which the (noisy) linear system to be solved is structured [LPR].

*Sources:* [LPR] V. Lyubashevsky, C. Peikert and Oded Regev. On Ideal Lattices and Learning with Errors over Rings. J. ACM, 2013.

### Risk

A subset of “business risks” and, as such, should be talked about in business terms. Instead of defining risk in technical terms, cybersecurity professionals—when speaking to executives—can adopt the definition of risk used by almost every business manager and board of directors: the potential for monetary loss. In this context, “risk” is the possibility that an event will lead to reduced profitability. Therefore, a cyber event causing damage to an organization’s brand or reputation can be quantified.

*Sources:* Information Technology Governance, Risk and Compliance in Healthcare : CSA

### Risk Classification

In a cloud deployment registry, risk criteria captures the risk level of each environment to align with the CSC’s risk management strategy. This helps prioritize resources and efforts for risk mitigation and ensures that the appropriate level of security controls is implemented.

*Sources:* https://www.isaca.org/resources/glossary#glossr

### Risk Scoring

A method where each entity and action is assigned a risk score based on a range of attributes, such as the IP address or time of the action. These scores are then input into a policy engine that permits or denies actions—not solely based on preset entitlements but on whether the risk level is acceptable for a given situation.

*Sources:* https://csrc.nist.gov/presentations/2021/nist-cyber-risk-scoring-crs-program-overview

### Risk Treatment

Risk Treatment involves selecting and implementing measures to mitigate, transfer, accept, or avoid identified risks. This process is part of a broader risk management strategy and aims to reduce the potential impact of risks to an acceptable level. Organizations choose appropriate risk treatment options based on their risk appetite and the effectiveness of available controls.

*Sources:* https://www.isaca.org/resources/glossary#glossr

### Risk Acceptance

Risk acceptance is a strategy in which the company accepts the potential consequences of a given risk.

*Sources:* https://www.sciencedirect.com/topics/computer-science/risk-acceptance

### Risk Appetite

The tolerance level organizations have for risk. One aspect of this is understanding how much risk an organization is willing to tolerate, while another is thinking about how much an organization is willing to invest or spend to manage the risk.

*Sources:* Information Technology Governance, Risk and Compliance in Healthcare : CSA

### Risk Assessments

Risk Assessments measure the maturity of the organization’s controls from a reference framework perspective (i.e., COBIT, ISO27001), regulatory perspective (i.e., SOX, PCI).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Risk Avoidance

1. Course of action that removes a risk factor from further consideration 2. A risk response strategy whereby the project team acts to eliminate the threat or protect the project from its impact [A Guide to the Project Management Body of Knowledge (PMBOK® Guide) — Fifth Edition]

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec-ieee:24765:ed-2:v1:en:term:3.3517

### Risk Based Authentication

A non-static authentication system which takes into account the profile(IP address, User-Agent HTTP header, time of access, and so on) of the agent requesting access to the system to determine the risk profile associated with that transaction. The risk profile is then used to determine the complexity of the challenge. Higher risk profiles leads to stronger challenges, whereas a static username/password may suffice for lower-risk profiles. Risk-based implementation allows the application to challenge the user for additional credentials only when the risk level is appropriate

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Risk Dashboard

Graphically measure and report the level of potential, inherent, and residual risks and the effectiveness of controls to help the organization understand threats and vulnerabilities and make risk-based decisions to maintain or improve control effectiveness.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Risk Management

Risk management is the identification, assessment, and prioritization of risks followed by coordinated and economical application of resources to minimize, monitor, and control the probability and/or impact of unfortunate events.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Risk Management Framework

Ensures that a repeatable process is defined and documented that is workable within the business. The risk management framework must be used within the business context for which it is defined.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Risk Mitigation

Prioritizing, evaluating, and implementing the appropriate risk-reducing controls/countermeasures recommended from the risk management process.

*Sources:* https://csrc.nist.gov/glossary/term/risk_mitigation

### Risk Portfolio Management

An articulation of the Information Security Program’s scope and charter includes, for example, such focus areas as reputation, corporate governance and regulation, corporate social responsibility, and information assurance. The portfolio can change as necessary to remain consistent with the business objectives and to remain relevant and responsive to a changing threat landscape and evolving laws and regulations.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Risk Taxonomy

A taxonomy to identify, capture, and classify known threats. One example used in the SABSA threat modeling framework defines threat domains (people, processes, systems, external events) and threat categories based on experience and observation.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Risk Tolerance

The level of risk or degree of uncertainty acceptable to organizations. An organization’s risk tolerance level is the amount of data and systems that can be risked to an acceptable level.

*Sources:* Information Technology Governance, Risk and Compliance in Healthcare : CSA

### Risk Transfer

Risk transference is where the exposure to the risk is transferred to a third party, usually as part of a financial transaction.

*Sources:* https://www.sciencedirect.com/topics/computer-science/risk-transference

### Rivest-Shamir-Adleman (RSA)

A public-key algorithm that is used for key establishment and the generation and verification of digital signatures.

*Sources:* https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-175Br1.pdf

### Roadmap

Strategic direction and plans for changes to capabilities and solutions within the technology portfolio (including the security roadmap) to accomplish a desired future state (e.g., continuous innovation, integration of capabilities, etc.). This process must be aligned with the business strategy).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Role

Provides a permission-centric view, defining the access level for users to perform specific tasks. Roles can be unique or shared. A single user might have multiple roles depending on their responsibilities. Conversely, multiple users can share the same role if they have the same access needs.

*Sources:* https://csrc.nist.gov/glossary/term/role

### Role Based Access Control (RBAC)

Access control based on user roles (i.e., a collection of access authorizations a user receives based on an explicit or implicit assumption of a given role). Role permissions may be inherited through a role hierarchy and typically reflect the permissions needed to perform defined functions within an organization. A given role may apply to a single individual or to several individuals.

*Sources:* SDPs can make use of role information (typically housed in an identity management system) to control connections to resources such as servers, devices, processes, and data as part of an SDP policy. | https://csrc.nist.gov/glossary/term/role_based_access_control | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Role Based Awareness

Association of policy with a given role. For example, a user might be designated as a ‘local user’ and a function such as data transfers might be configured to only be available to the ‘local user’ role and not be available to a user with a role of ‘mobile user’.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Role Management

A role represents a set of permissions and privileges, and role management assures that roles are correctly defined to include only the required permissions and privileges and adequately assigned to entities.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Roles and Responsibilities

Dividing the work among multiple positions with different roles and responsibilities allows for the segregation of duties to ensure appropriate integrity within an organization’s processes.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Root Cause Analysis

An important component of incident response that looks beyond the face details of an incident to determine the root cause of the incident (e.g., a missing patch might enable a successful intrusion but root cause analysis might reveal that the vulnerable service should never have been running anyway).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Rule-based security policy

A security policy based on global rules imposed for all subjects. These rules usually rely on a comparison of the sensitivity of the objects being accessed and the possession of corresponding attributes by the subjects requesting access.

*Sources:* https://csrc.nist.gov/glossary/term/rule_based_security_policy

### Rules for Data Retention

This capability manages the policies, procedures, or requirements associated with keeping data (transactions information, email, document images, card swipes, online browsing history) as long as required to do so from the business and regulatory perspective, then secured disposal.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Rules for Information Leakage Prevention

This capability manages policies, procedures, and business requirements associated with data loss prevention and controls related to data privacy and protection throughout the organization. Examples of this include Content Management, Share File Repositories, and Data usage from the Endpoint perspective.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Runbook

A set of instructions for completing a routine task. With respect to incident response, runbooks should be updated to provide guidance when an event is detected exposure and abuse of cloud credentials obtained by an attacker in a non-cloud attack an attacks on cloud resources from compromised resources such as a server or workstation in the non-cloud environment.

*Sources:* https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r2.pdf

### Runtime Application Security Protection (RASP)

Security technology deployed within the target application in production for detecting, alerting, and blocking attacks. Note 1 to entry: Similar to a WAF but instrumented within the application

*Sources:* The Six Pillars of DevSecOps: Automation : CSA


## S

### SAML Assertion

Conveys information from a verifier to an relying party about a successful act of authentication that took place between the verifier and a subscriber.

*Sources:* SDPs can use a SAML assertion to authenticate and authorize users into the perimeter. | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63-2.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### SAML Token

Security Assertion Markup Language (SAML) tokens are XML representations of claims. SAML tokens carry statements that are sets of claims made by one entity about another entity.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### SCADA (Supervisory Control And Data Acquisition)

SCADA systems are used to control dispersed assets where centralized data acquisition is as important as control. These systems are used in various industrial systems. SCADA systems integrate data acquisition systems with data transmission systems and HMI software to provide a centralized monitoring and control system for numerous process inputs and outputs. SCADA systems are designed to collect field information, transfer it to a central computer facility, and display the information to the operator graphically or textually, thereby allowing the operator to monitor or control an entire system from a central location in near realtime. Based on the sophistication and setup of the individual system, control of any individual system, operation, or task can be automatic, or it can be performed by operator commands.

*Sources:* NIST SP 800-82r2 https://csrc.nist.gov/publications/detail/sp/800-82/rev-2/final

### SIEM Platform

The Security Information and Event Management Platform collects, correlates, reports, on multiple security information sources to maintain situational awareness.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### SIS (Safety Instrumented System)

Safety Instrumented Systems are used to monitor the condition of values and parameters of a plant within the operational limits and, when risk conditions occur, they trigger alarms and place the plant in a safe condition or even at the shutdown condition. The main objective is to avoid accidents inside and outside plants.

*Sources:* http://www.smar.com/en/technical-article/sis-safety-instrumented-syst02

### SOC Portal

A dashboard application maintained by the Security Operations Center to give overall visibility of the organization’s security status.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### SPI Stack

The acronym used to refer to the three cloud delivery models - software-as-a-service, platform-as-a-service, and infrastructure-as-a-service.

*Sources:* https://www.isaca.org/resources/glossary#glosss

### SPIFFE Runtime Environment (SPIRE)

The SPIFFE Runtime Environment (SPIRE) is a production-ready implementation of the SPIFFE standards. SPIRE provides the infrastructure needed to issue and manage SPIFFE identities, enabling secure service-to-service authentication and authorization in complex, dynamic environments.

*Sources:* https://spiffe.io/docs/latest/spiffe-about/overview/#:~:text=SPIFFE%2C%20the%20Secure%20Production%20Identity,authenticate%20wherever%20they%20are%20running .

### SSL

SSL (Secure Sockets Layer) is a standard security protocol for establishing encrypted links between a web server and a browser in online communication. SSL ensures that all data transmitted between the web server and browser remains encrypted and secure, protecting sensitive information from interception.

*Sources:* https://www.isaca.org/resources/glossary#glosss

### STRIDE

a framework used for identifying and categorizing security threats. It stands for Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, and Elevation of privilege.

*Sources:* https://cyberinsight.co/what-is-stride-in-cyber-security/

### SVP

This stands for the Shortest Vector Problem, which requires the shortest vector in a lattice to be found. The problem is Non-deterministic Polynomialtime hardness (NP-hard) under randomized reduction for the Euclidean norm. This is a hard problem that occurs in lattice-based cryptography.

*Sources:* Quantum Safe Security Glossary : CSA

### SaaS Security Posture Management (SSPM)

tools that enable organizations to manage and monitor SaaS applications, ensuring proper configuration and entitlements. These tools offer centralized visibility into security controls, configurations, and compliance status across multiple SaaS applications.

*Sources:* https://www.cloudflare.com/learning/cloud/what-is-sspm/

### SaaS Storage

With respect to cloud-based storage, solutions that services enable users to securely access and share files and resources, enabling robust collaboration over the Internet.

*Sources:* https://docs.aws.amazon.com/whitepapers/latest/multi-tenant-saas-storage-strategies/multi-tenant-saas-storage-strategies.html

### Sandboxing

A restricted, controlled execution environment that prevents potentially malicious software, such as mobile code, from accessing any system resources except those for which the software is authorized.

*Sources:* https://csrc.nist.gov/glossary/term/sandbox

### Scheduling

As part of release management, a detailed schedule of releases and their features should be developed to bundle many change requests into a single change calendar.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Search

A presentation modality that allows users to query a single site or multiple sites for content related to the terms in the query. This modality is often used as an initial form of navigation across the internet or within the site.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### SecDevOps

Application of DevOps culture, practices, and workflows for the achievement of information security and compliance management.

*Sources:* As defined in ISO 27000 and Information Security Management through Reflexive Security : CSA .

### Secure Access Service Edge (SASE)

Secure Access Service Edge (SASE) is an emerging cybersecurity framework that combines wide-area networking (WAN) and network security services like secure web gateways, firewalls, and zero trust network access (ZTNA) into a single cloud-delivered service model. SASE aims to provide secure and fast cloud-based networking capabilities.

*Sources:* https://csrc.nist.gov/glossary/term/secure-access-service-edge

### Secure Repositories

With respect to compliance and assurance processes, a repository used for storing compliance artifacts requires secure, accessible repositories that protect the integrity and confidentiality of the data. These repositories should adhere to security standards and be capable of restricting access to authorized personnel only.

*Sources:* https://github.blog/2021-10-22-github-actions-for-security-compliance/

### Secure Build

The standard software image that is assured to comply with security policies.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Secure Collaboration

A technology or solution for securing collaboration service (e.g., SharePoint) to extend access to employees on the go, partners, vendors, and even customers.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Secure Disposal of Data

Ensure that data is destroyed appropriately to preclude its recovery (e.g., through digital forensic techniques).Documentation of such destruction should be in place and should be included in information lifecycle management processes.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Secure Messaging

A server-based approach to protect sensitive data when sent beyond the corporate borders and provides compliance with industry regulations such as HIPAA, GLBA and SOX.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Secure Sandbox

An isolated environment that provides abstraction of trust concerns between custom or third party code and the underlying system. Allows applications to run in a context that does not affect each other or the host operating system and allows the enterprise to have an area with managed security controls for applications with sensitive data.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Secure Shell (SSH)

A protocol for secure remote login and other secure network services over an insecure network, which typically runs on top of TCP/IP. The protocol can be used as a basis for a number of secure network services. It provides strong encryption, server authentication, and integrity protection. It may also provide compression.

*Sources:* SDPs require using mutual TLS v1.2 and higher to enable secure connections and better management of keys that are typically not managed effectively with SSH remote logins and file transfers. | https://datatracker.ietf.org/doc/html/rfc4253 | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Secure Socket Layer (SSL)

A popular implementation of public-key encryption, is an internet security protocol used by web browsers and servers to transmit sensitive information. SSL has become part of an overall security protocol known as Transport Layer Security (TLS). You can look in your browser to determine when a website is using a secure protocol such as TLS; locations of websites that use SSL begin with the prefix “https” rather than “http,” and you will often see the icon of a closed padlock or a solid, unbroken key in your browser’s address bar to indicate that SSL is enabled.

*Sources:* https://iam.harvard.edu/glossary

### Secure Software Development Lifecycle (SSDLC)

The secure software development life cycle allows software developers and their teams to streamline the creation and implementation of a product in a secure manner.

*Sources:* https://www.indeed.com/career-advice/career-development/what-is-secure-software-development-life-cycle

### Secure Token Service (STS)

A Secure Token Service (STS) is a component that issues, validates, renews, and cancels security tokens for trusted systems, users, and resources requesting access within a federation.

*Sources:* https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html

### Secure Web Authentication (SWA)

A compatibility layer provided by Sign-On product, allowing the integration of legacy applications that don’t support federated authentication and would not otherwise be able to take advantage of organization-wide single sign-on. The feature stores a unique password for each application, and securely posts the credentials directly to the application’s authentication handler, resulting in a near-seamless SSO user experience.

*Sources:* https://www.okta.com/resources/identity-and-access-management- glossary/

### Security Champion

A Security Champion is an individual within a development team who is responsible for promoting security best practices and ensuring that security is integrated into the software development lifecycle. Security Champions act as liaisons between the security team and the development team, providing guidance on security issues, conducting security reviews, and helping to embed a security-focused culture within the organization.

*Sources:* https://owasp.org/www-project-developer-guide/release/culture_building_and_process_maturing/security_champions/security_champions_program/

### Security Production Identity Framework For Everyone ( SPIFFE)

The Security Production Identity Framework For Everyone (SPIFFE) is a set of open-source standards for securely identifying and authenticating services in dynamic and heterogeneous environments. SPIFFE provides a secure identity framework for workloads, enabling secure service-to-service communication in cloud-native applications.

*Sources:* https://spiffe.io/docs/latest/spiffe-about/overview/#:~:text=SPIFFE%2C%20the%20Secure%20Production%20Identity,authenticate%20wherever%20they%20are%20running .

### Security Service Edge (SSE)

A tool or set of tools that provide monitoring and management capabilities for deviations from security and compliance baselines. Specifically,

*Sources:* https://www.microsoft.com/en-us/security/business/security-101/what-is-sase

### Security and Risk Management (SRM)

Security Risk Management is the process of identifying future harmful events (“threats”) that may affect the achievement of objectives. It involves assessing the likelihood and impact of these threats to determine the assessed level of risk and identifying an appropriate response. Security Risk Management involves four key strategies: controlling, avoiding, transferring and accepting security risk. Security risks are controlled through prevention (lowering the likelihood) and mitigation (lowering the impact).

*Sources:* https://policy.un.org/sites/policy.un.org/files/files/documents/2020/Oct/spm_-_chapter_iv_-_section_a_-_security_risk_management_2.pdf

### Security Application Framework

Application frameworks provide a set of components that act as the fundamental starting point of an application. Frameworks enable application developers to reuse standard components across multiple applications and focus their efforts on the specific business needs of the applications. Security Application Frameworks provide security components that extend a specific application framework. For example, the ACEGI security framework became an official part of the Spring Framework for building web applications with Java.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Security Architecture

Represents the portion of the enterprise architecture that specifically addresses information system resilience and provides architectural information for the implementation of capabilities to meet security requirements.

*Sources:* Gantz, S. D., & Philpott, D. R. (2013). FISMA and the Risk Management Framework . ScienceDirect.

### Security Assertion Markup Language (SAML)

A language for exchanging authentication and authorization information. SAML standardizes the representation of credentials in an XML format called assertions, enhancing the interoperability between disparate applications.

*Sources:* https://nvlpubs.nist.gov/nistpubs/Legacy/SP/ nistspecialpublication800-95.pdf/

### Security Assertion Markup Language 2.0 (SAML2)

Security Assertion Markup Language (SAML) 2.0 is an OASIS standard for federated identity management that supports both authentication and authorization. It uses XML to make assertions between an identity provider and a relying party. Assertions can contain authentication statements, attribute statements, and authorization decision statements. SAML is very widely supported by both enterprise tools and cloud providers but can be complex to initially configure.

*Sources:* https://downloads.cloudsecurityalliance.org/assets/research/security-guidance/security-guidance-v4-FINAL.pdf?_ga=2.225992666.1359049959.1661450515-2107700575.1655484199

### Security Assessment

Third party audits of cloud services based on industry standards.

*Sources:* Defined Categories of Service 2011 : CSA

### Security Code Review

Security code review capabilities from a self-service point of view refers to the ability to use a source code analyzer tool to read the source code of a program and identify areas of the code vulnerable to well-known attack patterns.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Security Controls Overlay

An overlay is a fully-specified set of controls, control enhancements, and supplemental guidance derived from the application of tailoring guidance to control baselines. For more information about Control Overlays, NIST Special Publication NIST SP 800-53 Rev 4., Section 3.3 Creating Overlays, and Appendix I, Overlay Template.

*Sources:* NIST Information Technology Laboratory: Computer Security Resource Center (CRSC). (2009, June 12). FISMA Implementation Project . https://www.nist.gov/programs-projects/federal-informationsecurity-management-act-fisma-implementation-project.

### Security Design Patterns

Design Patterns are blueprints and instructions for solving commonly occurring technical challenges. Security Design Patterns focus on designs of security capabilities such as authentication, authorization, log monitoring, single sign-on, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Security FAQ

One of the outcomes from the knowledge management process would be to establish a standard and consistent answer to questions that employees ask frequently. This process captures those questions associated with information security and compliance.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Security Group

Are sets of IP filter rules that are applied to all project instances, which define networking access to the instance.

*Sources:* Cloud security groups can be effectively used with a SDP, by being set to ensure that inbound network access to cloud-based resources is only permitted from an SDP gateway. By doing so, the SDP policy will act as the access control enforcement point, rather than the cloud security group. The cloud security group can also be used to require that outbound traffic be directed through the SDP gateway, if supported by the SDP implementation. | https://docs.openstack.org/nova/train/admin/security-groups.html#:~:text=Security%20groups%20are%20sets%20of,networking%20access%20to%20the%20instance.&text=By%20default%2C%20security%20groups%20 (and,by%20the%20Neutron%20networking%20service | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Security Guidance

CSA’s flagship research document, it provides both guidance and inspiration to manage and mitigate the risks associated with the adoption of cloud computing technology while supporting business goals.

*Sources:* https://cloudsecurityalliance.org/research/guidance/

### Security Incident Response

The process and procedures for responding to a declared security incident.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Security Job Aids

As security standards and patterns are created across the organization, they should include guidelines and processes that can help employees comply with regulatory requirements or security standards in a consistent manner.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Security Knowledge Life Cycle

To build secure applications, a development team must keep up to date with the latest threats and appropriate countermeasures in their development process. A security framework is often used to provide reusable components when a development team is building multiple applications.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Security Monitoring

This container groups together the information sources coming from the BOSS - Security Monitoring Services.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Security Monitoring Services

All capabilities associated with proactive security and risk management situational awareness across the organization with a business focus to prevent internal or external attacks, misuse of privilege, and data loss, while maintaining proper monitoring for the organization’s data and access regardless where these services are allocated or managed (Cloud, Internal, Hosted, etc.)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Security Orchestration Automation and Response (SOAR)

Refers to technologies that enable organizations to collect inputs monitored by the security operations team. SOAR tools allow an organization to define incident analysis and response procedures in a digital workflow format.

*Sources:* https://www.gartner.com/en/information-technology/glossary/security-orchestration-automation-response-soar

### Security Patrols

Periodic rounds by human or animal guards to deter and detect illicit activity as well as verify the status of other security controls (e.g., verifying doors are locked).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Security Policy

A high-level document representing an enterprise’s information security philosophy and commitment.

*Sources:* ISACA. Interactive Glossary & Term Translations. Retrieved August 11, 2021, from https://www. isaca.org/resources/glossary.

### Security Procedure

The formal documentation of operational steps and processes that specify how security goals and objectives set forward in the security policy and standards are to be achieved.

*Sources:* ISACA. Interactive Glossary & Term Translations. Retrieved August 11, 2021, from https://www. isaca.org/resources/glossary.

### Security Standard

Practices, directives, guidelines, principles or baselines that state what needs to be done and focus areas of current relevance and concern; they are a translation of issues already mentioned in the security policy.

*Sources:* ISACA. Interactive Glossary & Term Translations. Retrieved August 11, 2021, from https://www. isaca.org/resources/glossary.

### Security Testing

Ensuring that the modified or new system includes appropriate controls and does not introduce any security holes that might compromise other systems or misuses of the system or its’ information.

*Sources:* ISACA. Interactive Glossary & Term Translations. Retrieved August 11, 2021, from https://www. isaca.org/resources/glossary.

### Security Token

A small hardware device (sometimes called an authentication token) that the owner carries to authorize access to a network service. The device may be in the form of a smart card or may be embedded in a commonly used object such as a key fob.

*Sources:* Security tokens provide an extra level of assurance through a method known as multi-factor authentication for SDPs. | https://archive.unescwa.org/secure-token | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Security information and event management (SIEM)

This technology supports threat detection, compliance and security incident management through the collection and analysis (both near real time and historical) of security events, as well as a wide variety of other event and contextual data sources. The core capabilities are a broad scope of log event collection and management, the ability to analyze log events and other data across disparate sources, and operational capabilities (such as incident management, dashboards and reporting).

*Sources:* https://www.gartner.com/en/information-technology/glossary/security-information-and-event-management-siem

### Segmentation

The process of testing small individual units of source code and integrated compartments of an application as they are developed to enable defects to be found earlier and remediated faster and at less cost. Typically, segmentation is performed as an activity by developers, and its code is prepared by developers before deployment occurs. Since it is a review-code and test-code process, it is considered a continuous activity for developers.

*Sources:* https://cloudsecurityalliance.org/

### Self Assessment

A tool and process that involves performing an analysis/assessment of risk or compliance by the owner/user rather than by a third party.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Self-Service

This capability allows anyone in the organization to report an incident and begin the incident management process.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Self-service provisioning

Refers to the provisioning of resources provided to cloud services performed by cloud service customers through automated means.

*Sources:* https://www.techopedia.com/definition/29433/self-provisioning

### Sensitive File Protection

The ability to protect sensitive information from being read or modified by administrators who have access to a file system but are not authorized to read the protected data within certain files. Also, the ability to monitor changes to sensitive files to audit who is making changes to them or reading them.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Sensors

A Sensor is a device that identifies the progressions in electrical or physical or other quantities and in a way to deliver a yield as an affirmation of progress in the quantity. In simple terms, Industrial Automation and Control Sensors are input devices that provide an output (signal) with respect to a specific physical quantity (input). Examples of sensor types include temperature, pressure, vacuum, motion, and torque.

*Sources:* https://www.plantautomation-technology.com/articles/types-of-sensors-used-in-industrial-automation

### Separation (Segregation of Duties)

Segregation of Duties - is a basic building block of sustainable risk management and internal controls for a business. The principle of SOD is based on shared responsibilities of a key process that disperses the critical functions of that process to more than one person or department.

*Sources:* https://www.aicpa.org/interestareas/informationtechnology/resources/value-strategy-through-segregation-of-duties.html

### Separation of Duties

Separation of duties (SoD) is the concept of having more than one person required to complete a task to prevent fraud and error.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Server

See Servers

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Server (Data at Rest)

See Data at Rest Encryption (DLP in this case)

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Server Application Streaming

The server-side component of an application streaming solution responsible for delivering content to multiple clients.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Server Redundancy

Server redundancy refers to a measure of setting up backup servers to support a primary server. For example, a site hosted on a single network server without any backups is not redundant. A redundant or backup server is essentially a mirror image of your primary server.

*Sources:* https://community.fs.com/blog/server-redundancy-types-benefits-and-design.html

### Server Virtualization

Concerned with creating, accessing and managing a virtual server. Controls at this level assure that a server is configured correctly, includes the proper software image, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Server-Side Discovery

The Server requests the load balancer for the network locations of available services from the service registry.

*Sources:* Best Practices in Implementing a Secure Microservices Architecture

### Service Networking

With respect to Kurbernetes networking, Kubernetes services provide a stable IP address and DNS name for a set of pods. Services act as load balancers, distributing traffic to the pods based on labels and selectors. There are several types of services, including ClusterIP (internal to the cluster), NodePort (exposed on each node’s IP), and LoadBalancer (externally accessible through a CSP’s load balancer).

*Sources:* https://kubernetes.io/docs/concepts/services-networking/service/

### Service Control Policies (SCPs)

allow organizations to specify and control which services and features can be accessed and used for the main account.

*Sources:* https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html

### Service Catalog

Service Catalog is a list of services that an organization provides, often to its employees or customers. Each service within the catalog typically includes: Service Description, Timeframes or service level agreement for fulfilling the service, Who is entitled to request/view the service, Service Costs (if any) and how to fulfill the service.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Service Costing

The internal function that analyzes the overall costs accrued in delivering a particular service so that revenue (whether external or internal chargeback) is adequate to support the delivery of that service.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Service Dashboard

All SLAs, OLAs, and contracts should have associated and defined Key Performance Indicators, Key Goal Indicators, and Key Risk Indicators that must be tracked periodically to manage these agreements. The service dashboard should present these metrics for decision making.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Service Delivery

Service Delivery deals with those technologies that are essential in maintaining uninterrupted technical services. Services in this category typically include those that are more appropriate to the technical staff, such as availability management, service level management, service continuity, and capacity management. Service Delivery is primarily concerned with the proactive and forward-looking services that the business requires from Information Technology to provide adequate support to the business users.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Service Discovery

Processes and procedures for identifying the services actually present (as opposed to those documented as being present) in order to assume that appropriate patches are installed.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Service Events

Information regarding services provided in support of IT operations could include deployments, changes, and maintenance events. Events can be based on key performance indicators crossing a threshold, network alarms, device metrics.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Service ID

A unique value assigned by the controller for each remote service, is the most significant 32 bits of the Mux ID.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf

### Service Level Indicators (SLIs)

A carefully defined quantitative measure of some aspect of the level of service that is provided.

*Sources:* https://sre.google/sre-book/service-level-objectives/

### Service Level Management

The function responsible for assuring that the level of services provided is in agreement with contractual obligations on an ongoing basis.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Service Level Objectives (SLOs)

A target value or range of values for a service level that is measured by an SLI. A natural structure for SLOs is thus SLI ≤ target, or lower bound ≤ SLI ≤ upper bound.

*Sources:* https://sre.google/sre-book/service-level-objectives/

### Service Management

Service management is a discipline for managing information technology (IT) systems, philosophically centered on the customer’s perspective of IT’s contribution to the business.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Service Oriented Architecture (SOA)

In SOA, the entire gamut of solutions (e.g. supporting a business process) is broken up into multiple parts or components called services. This approach makes the development, maintenance and deployment of the entire application easier as operations can be limited to a specific service rather than to an entire application.

*Sources:* https://cloudsecurityalliance.org/artifacts/best-practices-in-implementing-a-secure-microservices-architecture/ | Best Practices in Implementing a Secure Microservices Architecture : CSA

### Service Provider

A system that provides a generic service to the user in a federated system. To users, a service provider is the same thing as the application they are trying to use.

*Sources:* https://iam.harvard.edu/glossary

### Service Provisioning

The process of implementing a new configuration item or changes to an existing configuration item.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Service Registry

The registry contains the locations of available instances of services. Service instances are registered with the service registry on startup and deregistered on shutdown. Client of the service and/or routers query the service registry to find the available instances of a service.

*Sources:* Best Practices in Implementing a Secure Microservices Architecture

### Service Support

Service Support is focused on the User of Information Technology services and is primarily concerned with ensuring that they have access to the appropriate services to support the business functions.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Service boundaries

Service boundaries are defined by the declarative description of the functionality provided by the service. A service - within its boundary - owns, encapsulates and protects its private data and only chooses to expose certain (business) functions outside the boundary.

*Sources:* How to Design a Secure Serverless Architecture

### Service-Level Agreement (SLA)

A Service-Level Agreement (SLA) is a negotiated agreement between two parties, where one is the customer (or end-user), and the other is the service provider. This can be a legally binding formal or an informal ‘contract’ (for example, internal department relationships). The SLA records a common understanding about services, priorities, responsibilities, guarantees, and warranties. The SLA may specify the levels of availability, serviceability, performance, operation, or other attributes of the service, such as billing. The ‘level of service’ can also be specified as ‘target’ and ‘minimum,’ which allows customers to be informed what to expect (the minimum) while providing a measurable (average) target value that shows the level of organization performance. In some contracts, penalties may be agreed upon in the case of non-compliance with the SLA (but see ‘internal’ customers below). It is important to note that the ‘agreement’ relates to the services the customer receives, and not how the service provider delivers that service. SLAs commonly include segments to address: a definition of services, performance measurement, problem management, customer duties, warranties, disaster recovery and termination of the agreement.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Session Events

Events indicating the beginning and ending of a user interaction with a computing resource.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Session ID

A value maintained by the IH and the AH to differentiate among different TCP connections for a specific remote service, is the least significant 32 bits of the Mux ID.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf

### SessionBased

A remote desktop presentation of any device where the presentation is controlled from a remote endpoint.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Shadow Access

Shadow Access is unauthorized, invisible, unsafe, and generally over permissioned access that has grown along with cloud identities, apps and data. Today, identities, human, and nonhuman are automatically created, along with access pathways to cloud data. Current tools are blind to many cloud identities and access pathways, creating vulnerabilities that are exploited to breach cloud data.

*Sources:* https://cloudsecurityalliance.org/blog/2023/03/16/shadow-access-in-your- cloud/

### Shared Security Responsibility Model (SSRM)

Somestimes shortened to SRM, is a public responsibility matrix each cloud service provider that describes the responsibilities the cloud provider and cloud consumer are responsible for for groups of services.

*Sources:* https://www.cisa.gov/sites/default/files/2023-02/cisa_cloud_security_technical_reference_architecture_version_1_1.pdf

### Shared Responsibility

The customer security team maintains some responsibilities for security as you move applications, data, containers, and workloads to the cloud. At the same time, the provider takes some responsibility, but not all. Defining the line between customer responsibilities and providers is imperative for reducing the risk of introducing vulnerabilities into your public, hybrid, and multi-cloud environments.

*Sources:* https://cloudsecurityalliance.org/blog/2020/08/26/shared-responsibility-model-explained/

### Sherwood Applied Business Security Architecture (SABSA)

The Sherwood Applied Business Security Architecture (SABSA) is a comprehensive framework for developing risk-driven enterprise information security architectures. It integrates business requirements with security needs, ensuring that security measures align with business goals and strategies, providing a structured approach to designing and managing security infrastructure.

*Sources:* https://sabsa.org/sabsa-executive-summary/

### Shift Left

Among developers, the term “shift left” describes moving a particular function to earlier phases of their processes to make identifying and fixing bugs and other errors easier and less time-consuming. The longer they wait, the more difficult making a fix becomes, and that creates delays.

*Sources:* https://cloudsecurityalliance.org/blog/2019/07/18/shift-left-to-harden-your-cloud-security-posture/

### Shor’s algorithm

This refers to the P.W. Shor algorithm [Shor], published in 1994, which allows integers to be factored and to find discrete logarithms in polynomial-time on a quantum computer. By using Shor’s algorithm, most of today’s commonly used asymmetric cryptosystems can be broken.

*Sources:* Quantum Safe Security Glossary : CSA

### Signature Services

A software program or function to provide an electronic coded message which is unique to both the document and the signer and binds both of them together. The digital signature ensures the authenticity of the signer. After it is signed, any changes made to the document invalidate the signature, thereby protecting against signature forgery and information tampering.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Silos

Teams, tools, anmd processes that isolate collaboration and result in not achieving agility with stability and quality.

*Sources:* https://devops.com/breaking-down-silos/

### Single Packet Authorization (SPA)

A single packet protocol for service protection behind a defaultdrop packet filter that offers 1) asymmetric ciphers for encryption, 2) authentication with a keyed-hash message authentication code (HMAC) in the encrypt-then-authenticate model, 3) non-replayable packets that cannot be broken by trivial sequence busting attacks. Within SDP, SPA plays a key role by hiding servers (including the SDP controller and gateway) until and unless the initiating host sends a valid SPA packet as the initial connection request.

*Sources:* https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Single Packet Authorization OTP

Based on RFC 4226 (a document describing an algorithm to generate one-time password values, based on hashed message authentication code (HMAC)) but modified to include a counter value which ensures a different password each time. It is used to uniquely identify the IH when initiating communication to both the SDP controller and the AH.

*Sources:* https://downloads.cloudsecurityalliance.org/initiatives/sdp/SDP_Specification_1.0.pdf

### Single Responsibility Principle (SRP)

The SRP defines a responsibility of class as a reason to change, and that a class should have only one reason to change.

*Sources:* https://cloudsecurityalliance.org/artifacts/best-practices-in-implementing-a-secure-microservices-architecture/ | Best Practices in Implementing a Secure Microservices Architecture : CSA

### Single Sign-On (SSO)

SSO provides the capability to authenticate once, and be subsequently and automatically authenticated when accessing various target systems. It eliminates the need to separately authenticate and sign on to individual applications and systems, essentially serving as a user surrogate between client workstations and target systems. Target applications and systems still maintain their own credential stores and present sign-on prompts to client devices. Behind the scenes, SSO responds to those prompts and maps the credentials to a single login/password pair. SSO is commonly deployed in enterprise, Web, and federated models.

*Sources:* https://www.gartner.com/en/information-technology/glossary/

### Site Reliability Engineering (SRE)

Site reliability engineering (SRE) is the practice of using software tools to automate IT infrastructure tasks such as system management and application monitoring. Organizations use SRE to ensure their software applications remain reliable amidst frequent updates from development teams. SRE especially improves the reliability of scalable software systems because managing a large system using software is more sustainable than manually managing hundreds of machines.

*Sources:* https://aws.amazon.com/what-is/sre/

### Smart Appliances

Devices whose primary purpose is not computation, but include connectivity to a network to provide real-time updates on their status or to be controlled remotely.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Smart Card

A smart card (aka microprocessor card, chip card, or integrated circuit card) has traditionally taken a pocket-sized card with embedded integrated circuits. Smart cards are often used in two-factor authentication solutions where the user enters a pin which is used by an operating system on the smart card to release evidence of identity such as a digital certificate or to allow a private key to sign an identity token which is sent to an enforcement agent that determines if the identity is valid.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Smartcard Virtualization

Methods and systems that allow users to virtualize a local smart card so that they can remotely connect to a server and interact with the server as if the local smart card was physically connected to the server.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Smoke Testing

A quality assurance practice where a series of tests are performed by both the development and testing teams. The tests are the initial check on post-deployment from the development team and a very preliminary check on pretesting activity starts from the testing teams in the software industry. Smoke testing activity is helping to give more confirmation on the successful deployment for the development team if it is passed then this will give more confidence to continue the further testing activities from the testing team.

*Sources:* https://ieeexplore.ieee.org/document/10059686

### Social Engineering Attacks

The act of deceiving an individual into revealing sensitive information, obtaining unauthorized access, or committing fraud by associating with the individual to gain confidence and trust.

*Sources:* https://csrc.nist.gov/glossary/term/social_engineering

### Social Media

A presentation modality links users together to exchange messages, photos, etc. to network and communicate one-on-one or in groups.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Software

A collection of data or computer instructions that tell the computer how to work. Physical hardware, from which the system is built, performs the work.

*Sources:* Cambridge Dictionary. (2021, August 11). Software . https://dictionary.cambridge.org/dictionary/ english/software.

### Software Architecture

The structure or structures of the system, which comprise software elements, the externally visible properties of those elements, and the relationships among them.

*Sources:* Bass, L., Clements, P. C., & Kazman, R. (2012, September). Software Architecture in Practice, Third Edition. https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=30264.

### Software Composition Analysis (SCA)

Security testing that analyzes application source code or compiled code for software components with known vulnerabilities.

*Sources:* Note 1 to entry: software components in software composition analysis may include open source, libraries and common code. Note 2 to entry: known vulnerabilities may be discovered via vulnerability databases such as CVE. | The Six Pillars of DevSecOps: Automation : CSA

### Software Delivery Pipeline

Set of automated processes used for delivering software from conception to deployment.

*Sources:* The Six Pillars of DevSecOps: Automation : CSA

### Software Design Pattern

A general, reusable solution to a commonly occurring problem within a given context in software design. It is not a finished design that can be transformed directly into source or machine code. Rather, it is a description or template for how to solve a problem that can be used in many different situations.

*Sources:* Wikipedia contributors. (2021a, June 14). Software design pattern . Wikipedia. https://en.wikipedia. org/wiki/Software_design_pattern

### Software Development Lifecycle (SDLC)

A formal or informal methodology for designing, creating, and maintaining software (including code built into hardware)

*Sources:* https://csrc.nist.gov/glossary/term/software_development_life_cycle

### Software Development Lifecycle (SDLC)

A formal or informal methodology for designing, creating, and maintaining software (including code built into hardware). The scope of activities associated with a system, encompassing the system’s initiation, development and acquisition, implementation, operation and maintenance, and ultimately its disposal that instigates another system initiation.

*Sources:* https://csrc.nist.gov/glossary/term/sdlc

### Software Management

The application of management activities-planning, coordinating, measuring, monitoring, controlling, and reporting-to ensure that the development and maintenance of software is systematic, disciplined, and quantified. This includes measurement at distinct points in time for the purpose of systematically controlling changes to the configuration and maintaining the integrity and traceability of the configuration throughout the system life cycle.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Software Quality Assurance

Software Quality Assurance is the process of testing software and tracking the defects found. Applications should be tested for security vulnerabilities as part of the software quality assurance process.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Software Token

Are applications that run on a phone or computer that generate one time passwords for human entry or need to be plugged into a reader. Software tokens could be compromised if the user’s device is compromised, and this risk needs to be considered in any threat model.

*Sources:* SDP systems can rely on software tokens as a form of MFA, just as they can rely on a hardware token for MFA. SDPs may use cryptographically secured tokens to transmit information (such as application authorizations) between its components. | https://downloads.cloudsecurityalliance.org/assets/research/security-guidance/security-guidance-v4-FINAL.pdf | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Software as a Service (SaaS)

Is a full application that is managed and hosted by the provider. Consumers access it with a web browser, mobile app, or a lightweight client app.

*Sources:* Disaster Recovery as a Service : CSA

### Software bill of materials (SBOM)

A formal record containing the details and supply chain relationships of various components used in building software. Software developers and vendors often create products by assembling existing open source and commercial software components. The SBOM enumerates these components in a product.

*Sources:* https://csrc.nist.gov/glossary/term/software_bill_of_materials

### Software-Defined Network (SDN)

An approach to computer networking that allows network administrators to manage network services through abstractions of higher-level functionality. SDNs manage the networking infrastructure. This is done by decoupling the system that makes decisions about where traffic is sent (the control plane) from the underlying systems that forward traffic to the selected destination (the data plane).

*Sources:* SDPs secure all connections to the services running on the networking infrastructure. So, while SDN is the notion of establishing a dynamic networking infrastructure… getting users to connect point to point, fast and efficiently, with as much throughput as possible, SDP is about the ability to secure every connection at all layers of this dynamic network infrastructure. | https://ieeexplore.ieee.org/abstract/document/6819788 | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Software-Defined Perimeter (SDP)

A network security architecture that is implemented to provide security at Layers 1-7 of the OSI network stack. An SDP implementation hides assets and uses a single packet to establish trust via a separate control and data plane prior to allowing connections to hidden assets.

*Sources:* A secure perimeter that is created based on policies to isolate services from unsecured networks. It’s designed to provide an on-demand, dynamically provisioned air-gapped network, by first authenticating users and devices prior to authorizing the user/device combination to securely connect to the isolated services. Unauthorized users and devices are unable to connect to the protected resources. SDPs make extensive use of encryption, including mutual TLS for inter-component communications, and an HMAC within the single-packet authorization packet. | https://cloudsecurityalliance.org/artifacts/software-defined-perimeter-and-zero-trust/ | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Software-Defined Wide Area Network (SD WAN)

Provides a replacement for traditional WAN routers and are agnostic to WAN transport technologies. SD-WAN provides dynamic, policy-based, application path selection across multiple WAN connections and supports service chaining for additional services such as WAN optimization and firewalls.

*Sources:* While SD-WANs manage the infrastructure for IP networking, SDPs secure connections that use the infrastructure provided by SD-WANs. | https://www.gartner.com/en/information-technology/glossary/software-defined-wan-sd-wan | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Solution

A solution is the application of architecture, patterns, and design effort to solve a specific industry need or business problem. A solution intends to provide ongoing customer and business owner value.

*Sources:* Microservices Architecture Pattern : CSA

### Source Code Management

A form of version control for source code that allows for versioning of software, branching software into different releases, and controlling access to software.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Source Code Scanning

The method of identifying security bugs in software with static code analysis tools.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Speech Recognition (IVR)

Speech recognition can translate the spoken word into computer input. Interactive Voice Response (IVR) systems provide a menu of choices that a person can respond to to interact with a system.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Spoofing

Impersonating, masquerading or otherwise falsely assuming an identity, characteristic or claim about oneself. In cloud testing, spoofing often takes the form of stealing cloud environment credentials to leverage their identity’s privileges.

*Sources:* Cloud Penetration Testing : CSA

### Sprints

Short time frame, in which a set of software features is developed, leading to a working product that can be demonstrated to stakeholders

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec-ieee:24765:ed-2:v1:en:term:3.3914

### Stakeholders

A person or organization (3.3) that can affect, be affected by, or perceive itself to be affected by a decision or activity. A system stakeholder is a individual, team, organization, or classes (3.1.12.2) thereof, having an interest in a system (3.1.2.1)

*Sources:* Stakeholder is defined in https://www.iso.org/obp/ui#iso:std:iso:ts:37008:ed-1:v1:en:term:3.7 System Stakeholder is defined in https://www.iso.org/obp/ui#iso:std:iso:ts:14812:ed-1:v1:en:term:3.1.3.4

### Standards & Guidelines

This capability is a complement for the Architecture Governance, outlines all the technology standards, and guidelines regarding how they can be consumed across the organization. These standards should include alignment with the organization’s strategy, industry standards, principles, patterns that can be reused across the organization, among other elements necessary to ensure consistent implementation and adoption.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Stateful Firewall

a firewall that maintains a “state” or stores information about active network connections. When a connection is opened, the firewall begins tracking it and updates its internal state as new packets are inspected and processed by the firewall. A stateless firewall differs from a stateful one in that it doesn’t maintain an internal state from one packet to another. Instead, each packet is evaluated based on the data that it contains in its header.

*Sources:* https://www.checkpoint.com/cyber-hub/network-security/what-is-firewall/what-is-a-stateful-firewall/stateful_vs_stateless_firewall/

### Static Vulnerability Scanning

With respect to application pre-deployment testing, used to identify and mitigate potential security threats. There are two main types of scans: static and dynamic. Static scanning analyzes source code (Infrastructure as Code - IaC) and configurations at rest, including files like Virtual Machine images or templates, container images, Dockerfiles, docker-compose files, Kubernetes YAMLs, Terraform or Cloudformation files, etc.

*Sources:* https://www.isaca.org/resources/glossary#glosss

### Static Application Security Testing (SAST)

Security testing that analyzes application source code for software vulnerabilities and gaps against best practices. Note 1 to entry: Static analysis can be performed in multiple environments including the developer’s IDE, source code, and binaries. Note 2 to entry: Also called “white box testing”

*Sources:* The Six Pillars of DevSecOps: Automation : CSA

### Storage

A function that records data and supports retrieval (SNIA Dictionary).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Storage Services

Concerned with the provisioning, migration and sanitization of physical storage in the infrastructure. Controls at this level assure that storage is available when required, its redundancy/reliability requirements match the service requirements, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Storage Virtualization

Concerned with how virtualized storage is created, allocated and managed. This includes both ‘block-based’ storage such as a SAN (Storage Area Network) and ‘file-based’ virtualization such as NAS (Network Attached Storage) whether provided by a file server or appliance. Controls at this level assure that the storage is adequate to requirements, properly segregated and secured and that its performance matches the profile specified in the service level agreement.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### StorageDevice Based

Storage device controllers may allow virtualization of disk volumes (e.g., a hardware RAID controller that groups multiple physical volumes or sections of columns into a single host-visible RAID-5 array).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Strangle

A “Strangler” is a reference model that is used to describe the process of modernizing a monolithic application into a microservices architecture, by adding new microservices to the application over time, while decommissioning certain features of the monolith over time. It is a dissect and transition as you develop on the go model.

*Sources:* Microservices Architecture Pattern : CSA

### Strategy

The strategy information within ITOS represents the business and technology trends affecting the enterprise, gap analysis of current capabilities against desired capabilities, and the investments required to fill the gaps.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Strategy Alignment

Process-oriented to understand the business needs and strategy and ensure that Information Technology and the Security and Risk Management strategies are aligned to support those objectives within the roadmap.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Stress & Volume Testing

Performance and capacity tests seek to determine the workload level at which a service level objective is violated or the maximum workload that can be supported without violating a service level objective, respectively.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Application Services

### Structured Query Language (SQL) Injection

These attacks, which are still quite common on the Internet, look for web sites that pass insufficiently processed user input to database back-ends and then send carefully-crafted input that will cause exposure of database records, and possibly allow destruction of databases.

*Sources:* https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7682.pdf

### Switched

A more complex storage area network architecture that includes a switching network to connect hosts with LUNs. Switched SANs may either be based on fibre channel or fibre channel over Ethernet (FCoE) or iSCSI.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Symmetric Encryption

A single shared secret held by one or more authorized parties for encrypting and decrypting data and communications.

*Sources:* https://www.sciencedirect.com/topics/computer-science/symmetric-encryption

### Symmetric Keys

Also referred to as a symmetric cryptographic cipher, both parties must use the same key for encryption and decryption. The encryption keys must be shared between the parties before any decryption of the message can take place.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Synchronous Communication

A form of communication in which a producer (or client) task sends a message to a consumer (or server) task and waits for a reply.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso-iec-ieee:24765:ed-2:v1:en:term:3.4082

### Syndrome decoding

This is a Non-deterministic Polynomial-time hardness (NP-hard) problem that occurs in code-based cryptography. The goal is to find a constrained solution of a linear system; that solution must have a small number of nonzero components.

*Sources:* Quantum Safe Security Glossary : CSA

### System for Cross-Domain Identity Management (SCIM)

System for Cross-domain Identity Management (SCIM) is a standard for exchanging identity information between domains. It can be used for provisioning and deprovisioning accounts in external systems and for exchanging attribute information.

*Sources:* https://downloads.cloudsecurityalliance.org/assets/research/security-guidance/security-guidance-v4-FINAL.pdf?_ga=2.225992666.1359049959.1661450515-2107700575.1655484199


## T

### TAISE

Trusted AI Safety Expert

### TCP / IP Ports

In computer science, ports are of two types - physical ports (which is a physical docking point where other devices connect) and logical ports (which is a well-programmed docking point through which data flows over the internet). Security and its consequences lie in a logical port.

*Sources:* SDP communications between Client, Controller, and Gateway use the TCP / IP ports. | https://www.w3schools.in/cyber-security/ports-and-its-security/#:~:text=Cyber%20Security%20Tutorials&text=In%20computer%20science%2C%20ports%20are,lie%20in%20a%20logical%20port . | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### TPM Virtualization

A Trusted Platform Module can store code signatures or keys that the software trusts to be unalterable by an attacker. This capability refers to a virtualized TPM instance. TPM is defined by Trusted Computing Group.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Tampering

Sabotage, modification or forgery of records, process or product in a harmful way, or otherwise in a fashion that serves an attacker’s other objective or attack chain. In cloud testing tampering often takes the form of altering cloud logs, changing hosted images, and tampering with API, repositories or data.

*Sources:* Cloud Penetration Testing : CSA

### Technical Assessment

Ensure that the technical risks identified, documented, and appropriate treatments are identified.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Technical Awareness & Training

To increase the ability to select and implement effective technical security mechanisms, products, process and tools.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Technical Debt

A design or construction approach that’s expedient in the short term but that creates a technical context in which the same work will cost more to do later than it would cost to do now (including increased cost over time).

*Sources:* McConnell, S. (2013). “Managing Technical Debt (slides),” in Workshop on Managing Technical Debt (part of ICSE 2013): IEEE, 2013.

### Technical Security Standards

Stipulate how specific technical security controls must be implemented (for example, a security policy might mandate at-rest encryption for a particular class of data and a technical security standard might specify that the encryption implementation must be FIPS 140-2 certified AES-256).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Technology Solution Services (TSS)

IT solutions can be thought of as a technology stack: at the top level are the actual interactions that the users have with the stack, with applications that accept the interactions and push data down where it may be manipulated, followed by the data that runs on them, with the computers and networks at the bottom layer. The four technology solution domains (Presentation Services, Application Services, Information Services, and Infrastructure Services) are based on the standard multi-tier architecture used to build these solutions.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Telehealth

Telehealth encompasses clinical health care as well as a wide range of other services. Telehealth uses innovative technologies, such as kiosks, website monitoring applications, mobile phone applications, wearable devices, and videoconferencing, to remotely connect health care providers to patients.

*Sources:* Marcoux Rita M., and Vogenberg F. Randy, 2016. _Telehealth: Applications from a Legal and Regulatory Perspective, Pharmacy and Therapeutics _Vol 41 (9): P. 567–570. Retrieved from https://www.ncbi. nlm.nih.gov/pmc/articles/PMC5010268/

### Telemetry

In the technology and software industries, which is the focus of this article, telemetry is the process that automatically collects data from various deployments of software products.

*Sources:* https://csrc.nist.gov/glossary/term/telemetry

### Tensor Processing Units (TPUs)

Tensor Processing Units (TPUs) are application-specific integrated circuits (ASICs) developed by Google specifically to accelerate machine learning workloads. TPUs are designed to efficiently handle large-scale neural network computations, providing significant performance improvements over general-purpose processors for specific AI tasks.

*Sources:* https://cloud.google.com/tpu/docs/intro-to-tpu

### Terms of Service (ToS)

Terms of Service (ToS) are legal agreements between a service provider and the user, outlining the rules, responsibilities, and limitations of using the service. ToS documents typically cover aspects such as acceptable use, privacy policies, intellectual property rights, and liability limitations. They are crucial for setting clear expectations and protecting both the service provider and the user from potential legal disputes.

*Sources:* https://www.techtarget.com/whatis/definition/terms-of-service-ToS

### Test Management

The function that manages the overall process of periodic testing and subsequent review of the DRP.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Testing

The process of testing all changes associated with a release to ensure they meet the requirements and will not disrupt existing services. This is a Quality Assurance function coordinated through Release Management.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Third Party Audits

Ensures that the services you rely upon are consistent with your security requirements.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### Third-Party Security Service Provider (TSSP)

A common, alternative term for TPSSP is managed security service provider (MSSP). Gartner states that an MSSP provides outsourced monitoring and management of security devices and systems to cloud customers. Typical services include managed firewalls, intrusion detection, virtual private networks, vulnerability scanning, and antivirus services. The MSSPs use high availability security operation centers (either from their facilities or other data center providers) to provide 24/7 services that reduce the number of operational security personnel an enterprise needs to hire, train and retain to maintain an appropriate security maturity.

*Sources:* https://www.gartner.com/en/information-technology/glossary/mssp-managed-security-service-provider https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf

### ThirdParty

Third-party devices are owned by one business and provided for use by another business.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain

### Threat

A threat is any circumstance or event with the potential to cause harm to an information system in the form of destruction, disclosure, adverse modification of data, and/or denial of service.

*Sources:* NIST SP 800-32 under Threat NSTISSI 4009

### Threat & Vulnerability Management

This discipline deals with core security, such as vulnerability management, threat management, compliance testing, and penetration testing. Vulnerability management is a complex endeavor in which enterprises track their assets, monitor, scan for known/emerging vulnerabilities, and take action by patching the software, changing configurations, or deploying other controls to reduce the attack surface at the resource layer. Threat modeling and security testing are also part of activities to identify the vulnerabilities effectively. This discipline aims to proactively inspect the infrastructure that runs the cloud to address new security threats using vulnerability scanning, virtual patching, and other aspects of security testing and response.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Threat Management

Threat Management focuses on threats, threat sources, and threat agents that can compromise confidentiality, integrity, and availability of data. Threat management can leverage a threat taxonomy to provide structure. Threat management also contributes to the overall risk assessment process.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Threat Modeling

Methodology to identify and understand threats impacting a resource or set of resources.

*Sources:* Note to entry: Common methodologies of threat modeling include STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) and OCTAVE (Operationally Critical Threat, Asset, and Vulnerability Evaluation). | The Six Pillars of DevSecOps: Automation : CSA

### Ticketing

The process of creating a record of incidents that can be tracked through their lifecycle. These incidents should be referenced by a unique identifier.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Time-Based One- Time Password (TOTP)

An algorithmically-generated code that is deterministic based on the current date and time and a secret “seed” value. The server knows the seed, and can easily verify that a given code is valid for the current time period. TOTP can significantly increase security because even if a code is intercepted, it is worthless after the time window has passed (usually less than a minute). This makes the logistics of an attack much more difficult. TOTP can be implemented on a simple and inexpensive hardware device or on a smartphone. The seed is installed and is made difficult or impossible to recover or duplicate.

*Sources:* https://www.okta.com/resources/identity-and-access-management- glossary/

### Token

The basic units of data processed by LLMs. In the context of text, a token can be a word, part of a word (subword), or even a character — depending on the tokenization process. Tokens are the representations of text in the form of a vector. Tokens are the linguistic units, while vectors are the mathematical representations of these units. Every token is mapped to a vector in the LLM’s processing pipeline.

*Sources:* https://thenewstack.io/the-building-blocks-of-llms-vectors-tokens-and-embeddings/

### Token Authentication

A method of authenticating to an application using a signed cookie containing session state information. A more traditional authentication method is usually used to initially establish user identity, and then a token is generated for re-authentication when the user returns.

*Sources:* https://www.okta.com/resources/identity-and-access-management- glossary/

### Tokenization

A process using a tokenizer to segment unstructured data and natural language text into distinct chunks of information, treating them as different elements. The tokens within a document can be used as vector, transforming an unstructured text document into a numerical data structure suitable for machine learning.

*Sources:* https://www.geeksforgeeks.org/nlp-how-tokenizing-text-sentence-words-works/

### Tooling

Tooling is a term that comes from manufacturing. In general, it refers to the building of various kinds of equipment, gear, software, checklists, procedures and rules required for production. With respect to DevSecOps, tooling is the introduction of security checks, scans, and management of data. Some steps imght use automation with triggers at the deployment pipeline.

*Sources:* https://cloudsecurityalliance.org/

### Traditional Maturity Stage

With respect to zero trust maturity stages, the traditional maturity stage represents the starting point for organizations on their Zero-Trust journey. At this stage, security practices are typically perimeter-focused, with implicit trust in internal network traffic.

*Sources:* https://www.techrepublic.com/article/nist-cybersecurity-framework-the-smart-persons-guide/

### Transform

Transformation of data implies extracting data from a source, transforming it or converting it to one format or another, and loading it into a target system.

*Sources:* Microservices Architecture Pattern : CSA

### Transformation Services

Translation and normalization services for the security monitoring events in order to do data mining and event correlation.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Translate

An adapter microservice wraps and translates (usually function based) services into an entity-based REST interface. This allows an interface of an existing class to be used as another interface.

*Sources:* Microservices Architecture Pattern : CSA

### Transmission Control Protocol (TCP)

A transport protocol that is used on top of IP to ensure reliable transmission of packets. TCP includes mechanisms to solve many of the problems that arise from packet-based messaging, such as lost packets, out of order packets, duplicate packets, and corrupted packets. Since TCP is the protocol used most commonly on top of IP, the Internet protocol stack is sometimes referred to as TCP/IP.

*Sources:* SDP communications between client, controller, and gateway use the TCP protocol. | https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:the-internet/xcae6f4a7ff015e7d:transporting-packets/a/transmission-control-protocol--tcp | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Transmission Control Protocol/ Internet Protocol (TCP/IP)

A set of protocols covering (approximately) the network and transport layers of the seven-layer OSI network model.

*Sources:* https://www.gartner.com/en/information-technology/glossary/tcpip-transmission-control-protocolinternet-protocol

### Transport Layer Security (TLS)

A cryptographic protocol, successor to SSL, that provides security for communications over a computer or IP network.

*Sources:* SDPs utilize a mutual TLS (mTLS) connection between pairs of components, in which both components validate the authenticity of the other component while establishing a secure connection. | https://csrc.nist.gov/glossary/term/transport_layer_security | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Trend Analysis

Analysis of requests for help regarding security in terms of consulting on projects, questions asked about policies, end-user training feedback, etc. to identify frequently asked questions and new areas of documentation required for the knowledge base.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Trust Assessment

Remote posture checking of an user’s device to verify if endpoint protection is operating and if any blacklisted processes are running. Additionally trust assessment can also verify if a device is patched and the hash values of software to detect tampering. Typically trust assessment is implemented over the SDP control channel before access to authorized applications is granted.

*Sources:* https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Trusted Execution Environments (TEEs)

Trusted Execution Environments (TEEs) are secure areas within a processor that ensure sensitive data is processed in an isolated and trusted environment. TEEs provide a higher level of security by protecting data from unauthorized access or tampering, even if the main operating system is compromised.

*Sources:* https://csrc.nist.gov/glossary/term/trusted_execution_environment

### Trusted Platform Module (TPM)

A cryptographic microprocessor designed to secure hardware by integrating cryptographic keys and services. A TPM functions as a root of trust for storage, measurement, and reporting. TPMs are currently included in many computing devices.

*Sources:* https://circle.cloudsecurityalliance.org/HigherLogic/System/DownloadDocumentFile.ashx?DocumentFileKey=a8c459b5-b927-4193-89e3-bf7bd1cc28c2&_ga=2.68892241.1579405153.1655930705-2107700575.1655484199

### Two-Factor Authentication (2FA)

It requires two different proofs of identity to provide authentication.This authentication is a subset of multifactor authentication, and significantly increases security, because each authentication factor requires a different style of attack to compromise.

*Sources:* https://csrc.nist.gov/glossary/term/2fa


## U

### Unbalanced Oil and Vinegar (UOV)

This is a multivariate signature scheme which was proposed in 1999 by A. Kipnis, L. Goubin and J. Patarin [KPG99].

*Sources:* [KPG99] A. Kipnis, J. Patarin, and L. Goubin. Unbalanced Oil and Vinegar Signature Schemes. EUROCRYPT’99, LNCS 1592, pages 206–222. Springer, 1999.

### Unified Threat Management (UTM)

A typical unified threat management (UTM) system has a firewall, malware detection and eradication, sensing and blocking of suspicious network probes, and so on. Deploying a UTM reduces complexity by making a single system responsible for multiple security objectives, but it also requires that the UTM have all the desired features to meet every one of the objectives.

*Sources:* https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf

### Unified endpoint management (UEM)

Unified Endpoint Management (UEM) allows IT to manage, secure, and deploy corporate resources and applications on any device from a single console.

*Sources:* https://www.vmware.com/topics/glossary/content/unified-endpoint-management.html

### Unified modeling language (UML)

language for specifying, visualizing, constructing, and documenting the artifacts of software systems and abstract models in general

*Sources:* https://www.iso.org/obp/ui#iso:std:iso:24622:-1:ed-1:v1:en:term:2.31

### Universal 2nd Factor (U2F)

This protocol allows online services to augment the security of their existing password infrastructure by adding a strong second factor to user login. The user logs in with a username and password as before. The service can also prompt the user to present a second factor device at any time it chooses. The strong second factor allows the service to simplify its passwords (e.g. 4-digit PIN) without compromising security. During registration and authentication, the user presents the second factor by simply pressing a button on a USB device or tapping over NFC. The user can use their U2F device across all online services that support the protocol leveraging built-in support in web browsers.

*Sources:* SDPs also leverage U2F or UAF for user or device authentication without additional CA requirements, separate from the CA utilized for mutual TLS. | https://fidoalliance.org/specs/u2f-specs-master/fido-u2f-overview.html | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Universal Authentication Framework (UAF)

This protocol allows online services to offer password-less and multifactor security. The user registers their device to the online service by selecting a local authentication mechanism such as swiping a finger, looking at the camera, speaking into the mic, entering a PIN, etc. The UAF protocol allows the service to select which mechanisms are presented to the user. Once registered, the user simply repeats the local authentication action whenever they need to authenticate to the service. The user no longer needs to enter their password when authenticating from that device. UAF also allows experiences that combine multiple authentication mechanisms such as fingerprint + PIN.

*Sources:* SDPs can leverage U2F or UAF for user or device authentication without additional CA requirements, separate from the CA utilized for mutual TLS. | https://fidoalliance.org/specs/fido-uaf-v1.1-id-20170202/fido-uaf-overview-v1.1-id-20170202.html | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Universal Authentication Frameworks (UAF)

UAF is an open standard developed by the FIDO Alliance with the goal of enabling a secure passwordless experience for primary authentication, as opposed to a second factor as described in U2F. Under the spec, the user presents a local biometric or PIN and is authenticated into the service.

*Sources:* https://www.okta.com/resources/identity-and-access-management- glossary/

### Universal Naming Convention (UNC)

Provided by Windows as an early method of identifying systems within an enterprise environment.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

### Unknown Threat Actor

Unauthorized access was confirmed, but the identity of the attacker, nor any information on the attacker was not made available. It is doubtful whether much is known at all.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

### User

A person or entity with authorized access.

*Sources:* https://csrc.nist.gov/glossary/term/user

### User Behavior & Profile Patterns

Collection of events and information about users that profiles and identifies normal and abnormal behavior patterns such as application usage by specific users or roles.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Business Operation Support Services (BOSS) Domain

### User Datagram Protocol (UDP)

A lightweight data transport protocol that works on top of IP. UDP provides a mechanism to detect corrupt data in packets, but it does not attempt to solve other problems that arise with packets, such as lost or out of order packets. That’s why UDP is sometimes known as the Unreliable Data Protocol. UDP is simple but fast, at least in comparison to other protocols that work over IP. It’s often used for time-sensitive applications (such as real-time video streaming) where speed is more important than accuracy.

*Sources:* SPA packets used to initiate connections could use UDP to ensure the SDP will not respond to any connections from any clients until they have provided an authentic SPA. | https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:the-internet/xcae6f4a7ff015e7d:transporting-packets/a/user-datagram-protocol-udp | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### User Directory Services

User directory service is the system that stores, organizes, and provides access to information about users in a directory. The directory allows the lookup of values given a user ID where the ID may be associated with multiple, different types of data.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### User Entity Behavior Analytics (UEBA)

UEBA is a type of cybersecurity process that uses machine learning, algorithms, and statistical analyses to detect real-time network attacks.

*Sources:* https://ieeexplore.ieee.org/document/8855782

### User Provisioning

User provisioning or account provisioning technology creates, modifies, disables, and deletes user accounts and their profiles across IT infrastructure and business applications. Provisioning tools use approaches such as cloning, roles, and business rules so that businesses can automate onboarding, offboarding, and other administration workforce processes (for example, new hires, transfers, promotions and terminations). Provisioning tools also automatically aggregate and correlate identity data from HR, CRM, email systems, and other “identity stores.” Fulfillment is initiated via self-service, management request, or HR system changes. Regulatory compliance and security efficiencies continue to drive most user-provisioning implementations.

*Sources:* https://www.gartner.com/en/information-technology/glossary/

### User Threat Management (UTM)

Security appliances unify and integrate multiple security features onto a single hardware platform, including network firewall capabilities, network intrusion detection and prevention, and gateway anti-virus. Some UTM offerings go further, incorporating an anti-spam and URL filtering capability on a hardened operating system as well.

*Sources:* The disadvantage of these appliances is that they can represent a single point of failure. To counter this vulnerability UTM’s can be combined with SDP’s to catch anything that gets through or around the UTM. | https://www.sciencedirect.com/topics/computer-science/unified-threat-management | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Utility

Sidecar mesh abstracts the underlying infrastructure through a proxy of services below the application. The proxy handles traffic flow, inter-microservice communication, connection, management, load balancing, availability and telemetry data. The sidecar mesh paradigm provides orchestration and architectural independence from underlying cloud architectures, across multiple clouds.

*Sources:* Microservices Architecture Pattern : CSA


## V

### VMBased (VDI)

A virtual desktop integrated with a presentation server to control access and manage multiple users.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### VRA

Documentation regarding risk assessments of 3rd party vendors used by the organization.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Value Stream Security Mapping (VSSM)

A centralized function or team responsible for improving an organization’s cybersecurity posture and preventing, detecting, and responding to threats. The team monitors identities, endpoints, servers, databases, network applications, websites, and other systems to uncover potential cyberattacks in real time. It also does proactive security work by using the latest threat intelligence to stay current on threat groups and infrastructure and identify and address system or process vulnerabilities before attackers exploit them.

*Sources:* we coined this - https://cloudsecurityalliance.org/artifacts/six-pillars-devsecops-pragmatic-implementation

### Value-Stream Mapping

method to develop the current state map of product and information flows within organizations. Value stream mapping is one step of the overall procedure VSM.

*Sources:* https://www.iso.org/obp/ui#iso:std:iso:22468:ed-1:v1:en:term:3.15

### Variational Autoencoder

Provides a probabilistic manner for describing an observation in latent space. Rather than building an encoder that outputs a single value to describe each latent state attribute, a variational autoencoder describes a probability distribution for each latent attribute.

*Sources:* https://www.geeksforgeeks.org/variational-autoencoders/

### Vendor Management

This capability governs the process of managing vendor relationships, including selection, vetting, evaluation, security, and compliance. Usually, these processes also include risk evaluation and a rating against the type of data that the vendor can access, process, host or see (given their maturity on their risk profile, financial, among other areas), and type of connectivity

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Version Control

The process of tracking all changes to source code, configuration items, and documentation and assigning these changes a version identifier.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Information Technology Operation & Support (ITOS) Domain

### Vertical Isolation

Vertical isolation separates all virtualized components of the workspace, such as usage details, communication, memory or data, may not be leaked between workspaces.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Virtual Private Network (VPN)

A virtual network built on top of existing physical networks that can provide a secure communications mechanism for data and IP information transmitted between networks or between different nodes on the same network.

*Sources:* SDPs provide the benefits of a VPN (message confidentiality and integrity) while overcoming the limitations of traditional VPN products like fine-grained access control. | https://csrc.nist.gov/glossary/term/virtual_private_network | https://downloads.cloudsecurityalliance.org/assets/research/sdp/SDP-glossary.pdf

### Virtual Directory Services

Virtual Directory Services aggregate multiple directories into a consolidated view which looks to the consumer application as a single directory.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### Virtual Infrastructure

The virtual infrastructure inherits some of the same services as are present in the physical infrastructure. For example, software images must be securely built and managed for the virtual servers that are hosted on the virtualization platform provided on the physical server. However, there are also unique requirements for the virtualized infrastructure itself.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Virtual Local Area Networks (VLANs)

A broadcast domain that is partitioned and isolated within a network at the data link layer. A single physical local area network (LAN) can be logically partitioned into multiple, independent VLANs; a group of devices on one or more physical LANs can be configured to communicate within the same VLAN, as if they were attached to the same physical LAN.

*Sources:* https://csrc.nist.gov/glossary/term/virtual_local_area_network_vlan

### Virtual Machines (HostBased)

A physical host may virtualize various of its components and capabilities to provide the illusion of multiple machines, applications, etc.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Virtual Machines (VMs)

A software-defined complete execution stack consisting of virtualized hardware, operating system (guest OS), and applications.

*Sources:* https://csrc.nist.gov/glossary/term/virtual_machine

### Virtual Memory

An operating system feature that uses a combination of physical memory and backing storage (usually disk) to create the illusion that much larger memory space is available. For good performance, it relies on the principle of locality that assumes that only a small part of a program’s address space (the working set) is actually in use at any point in time.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Virtual Trusted Platform Module (vTPM)

A vTPM is a software-based representation of a physical Trusted Platform Module 2.0 chip.

*Sources:* See: TPM. | https://circle.cloudsecurityalliance.org/HigherLogic/System/DownloadDocumentFile.ashx?DocumentFileKey=a8c459b5-b927-4193-89e3-bf7bd1cc28c2&_ga=2.68892241.1579405153.1655930705-2107700575.1655484199 | https://cloudsecurityalliance.org/cloud-security-glossary#T

### Virtual Workspaces

The template of the virtualized infrastructure defined by the cloud provider which defines characteristics of the virtual infrastructure instances such as number of hosts, network segmentation, storage and security elements. For High-Availability workspaces can be replicated across instances or cloud providers to provide redundant capabilities for failover purposes.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Infrastructure Services

### Virtual desktop infrastructure (VDI)

Virtual desktop infrastructure (VDI) is a full, thick-client user environment run as a VM on a server and accessed remotely. VDI implementations comprise: ▪ Server virtualization software to host desktop software (as a server workload) ▪ Brokering/session management software to connect users to their desktop environments ▪ Tools for managing the provisioning and maintenance (for example, reimages) of the virtual desktop software stack

*Sources:* https://www.gartner.com/en/information-technology/glossary/virtual-desktop-infrastructure-vdi

### Virtualization

Virtualization is the process of creating virtual instances of physical hardware resources, such as servers, storage devices, and networks. It enables more efficient use of hardware by running multiple virtual machines on a single physical machine, thus optimizing resource utilization and reducing costs.

*Sources:* https://csrc.nist.gov/glossary/term/virtualization

### Volume Storage

With respect to cloud-based storage, provides virtual hard drives that can be attached to virtual machines in the cloud. It allows you to store and access data in a way similar to traditional hard drives. Volume storage is typically used for operating system files, application data, and other persistent data that require low-latency access.

*Sources:* https://aws.amazon.com/what-is/cloud-storage

### Vulnerability

A vulnerability is a weakness in an information system, system security procedures, internal controls, or implementation exploitable by a threat source.

*Sources:* Examples of different vulnerabilities include: | National Institute of Standards and Technology. (2012). Special Publication 800-30 Revision 1 Guide for Conducting Risk Assessments , National Institute of Standards and Technology, Gaithersburg, MD. Retrieved from https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf

### Vulnerability Management

The cyclical practice of identifying, classifying, remediating, and mitigating vulnerabilities (generally in software).

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Vulnerability Scanning

Scans the target infrastructure or systems for security vulnerabilities via a public network.

*Sources:* Defined Categories of Service 2011 : CSA


## W

### WSSecurity

A flexible and feature-rich extension to Simple Object Access Protocol (SOAP) to apply security to web services. The protocol specifies how integrity and confidentiality can be enforced on messages and allows the communication of various token formats such as SAML, Kerberos, and X.509.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Web Authentication (WebAuth)

A core component of FIDO Alliance’s FIDO2 set of specifications, is a web-based API that allows websites to update their login pages to add FIDO-based authentication on supported browsers and platforms. FIDO2 enables users to leverage common devices to easily authenticate to online services in both mobile and desktop environments.

*Sources:* https://fidoalliance.org/fido2/fido2-web-authentication-webauthn/

### Web Application Firewall (WAF)

Application firewall that monitors, alerts, and blocks attacks by inspecting HTTP traffic.

*Sources:* The Six Pillars of DevSecOps: Automation : CSA

### Web Security

Offers real-time protection of public facing application services generally offered by proxying web traffic through the cloud service provider.

*Sources:* Defined Categories of Service 2011 : CSA

### WebAuthn

An evolution of the FIDO, U2F, and UAF protocols. WebAuthn continues in the FIDO tradition of allowing for using credentials for step up authentication. However, its biggest innovation is in enabling users to authenticate to services without necessarily needing the user to identify themselves first (through the use of a username and password combination).

*Sources:* https://www.okta.com/resources/identity-and-access-management- glossary/

### White Listing

A list or register of entities that, for one reason or another, are being provided a particular privilege, service, mobility, access or recognition.

*Sources:* When a whitelist is used, the default is to “deny all” except for those entries that are enumerated in the filter. These are typically used when it is easier (or a shorter list) to identify what is desirable rather than what is not desirable. | Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Wireless Protection

Protection of data in transit over wireless media, including 802.11 Wi-Fi, cellular, and Bluetooth. Some forms of encryption are the typical protection approach, e.g., Wi-Fi Protected Access (WPA) leveraging TKIP or AES.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### Write Once Read Many (WORM)

A data storage technology that ensures information written on the disc can’t be erased. This means that the data cannot be changed by anyone except the original writer, or destroyed by someone who has physical access to the media.

*Sources:* https://cio-wiki.org/wiki/WORM_%28Write_Once_Read_Many%29


## X

### X.500 Repositories

X.500 Repositories store hierarchical organization of entries according to the X.500 series of computer networking standards for electronic directory services.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Technology Solution Services (TSS) Domain - Information Services

### XACML

eXtensible Access Control Markup Language is a declarative access control policy language implemented in XML.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain

### XML Appliance

A special-purpose network device used to secure, manage and mediate XML traffic. They are most popularly implemented in Service-Oriented Architectures to control XML based Web Services traffic, and increasingly in cloud-oriented computing to help enterprises integrate on-premise applications with off-premise cloud-hosted applications. XML Appliances are also commonly referred to as SOA Appliances, SOA Gateways, XML Gateways, Cloud Brokers.

*Sources:* Enterprise Architecture Reference Guide v2 : CSA : Security and Risk Management (SRM) Domain


## Z

### Zero Trust (ZT)

Zero Trust is a cybersecurity strategy premised on the idea that no user or asset is to be implicitly trusted. It assumes that a breach has already occurred or will occur, and therefore, a user should not be granted access to sensitive information by a single verification done at the enterprise perimeter. Instead, each user, device, application, and transaction must be continually verified.

*Sources:* https://www.cisa.gov/sites/default/files/publications/NSTAC%20Report%20to%20the%20President%20on%20Zero%20Trust%20and%20Trusted%20Identity%20Management.pdf

### Zero Trust Architecture (ZTA)

1) A Zero Trust Architecture (ZTA) enables secure authorized access to each individual resource, whether located on-premises or in the cloud, for a hybrid workforce and partners based on an organization’s defined access policy.

*Sources:* 2) A Zero Trust Architecture (ZTA) uses Zero Trust principles to plan industrial and enterprise infrastructure and workflows. | 1) https://circle.cloudsecurityalliance.org/HigherLogic/System/DownloadDocumentFile.ashx?DocumentFileKey=a7c73ffe-be02-48e1-a439-3510b06a0bce&forceDialog=0&_ga=2.260269199.38415640.1663010462-1480344219.1663010462 | 2) https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf

### Zero Trust Maturity Model (ZTMM)

CISA’s Zero Trust Maturity Model (ZTMM) provides an approach to achieve continued modernization efforts related to zero trust within a rapidly evolving environment and technology landscape.

*Sources:* The ZTMM represents a gradient of implementation across five distinct pillars, in which minor advancements can be made over time toward optimization. The pillars include Identity, Devices, Networks, Applications and Workloads, and Data. Each pillar includes general details regarding the following cross-cutting capabilities: Visibility and Analytics, Automation and Orchestration, and Governance. | https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf

### Zero Trust Network Access (ZTNA)

ZTNA is a secure access tool that allows users to connect safely to workloads inside an enterprise network.

*Sources:* https://cloudsecurityalliance.org/blog/2022/03/01/how-zero-trust-security-will-revolutionize-devsecops/

### Zoombombing

The practice of hijacking video conversations by uninvited parties to disrupt the usual proceedings.

*Sources:* Top Threats to Cloud Computing: Egregious Eleven Deep Dive : CSA

