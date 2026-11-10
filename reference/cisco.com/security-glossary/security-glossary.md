# Cisco Security Glossary

Source: https://www.cisco.com/c/en/us/td/docs/security/glossary/b_security_glossary_terms.html

License: LicenseRef-Vendor-Copyright (Cisco Systems, Inc.; internal CSA use only — not redistributable).

Extracted: 461 terms.

---

## 3DES (Triple Data Encryption Standard)

A stronger version of DES, which is the default encryption method for SSH version 1.5. Used when establishing an SSH session with the appliance. 3DES is a protocol that can be used to encrypt data in a VPN tunnel between two devices.

## ABR (Area Border Router)

In OSPF, a router with interfaces in multiple areas.

## access control

A policy-based feature that allows you to inspect, log, and direct network traffic. Also considered a security concept that concerns those firewall services and policies and rules that allow or deny network traffic to flow between internal and external networks.

## access policy

Access policies block, allow, or redirect inbound HTTP, FTP, and decrypted HTTPS traffic. Access policies also manage inbound encrypted HTTPS traffic if the HTTPS proxy is disabled.

## ACE (access control entry)

Products ASA Definition An ACE evaluates network traffic using one or more characteristics, including source and destination IP address, IP protocol, ports, EtherType, and other parameters, depending on the type of ACL. By default, traffic that is not explicitly permitted is denied. The ASA stores ACEs like this and each entry is also considered an access control entry. Consider the ACE permit ip Foo Bar where these are the object groups: object-group Foo 192.168.10.1 192.168.10.2 object-group Bar 10.10.20.1 10.10.20.2 ASA stores the ACE like this: permit ip 192.168.10.1 10.20.1.1 permit ip 192.168.10.1 10.20.1.2 permit ip 192.168.10.2 10.20.1.1 permit ip 192.168.20.2 10.20.1.2 Note The running config shows: access-list permit_foo_bar extended permit ip object Foo object Bar So, this example doesn’t imply that 4 individual entries are entered into the running config, they're just stored on the ASA that way. Usage Docs—Expand on first use.

## ACL (access control list)

One or more access control entries (ACEs) that identify traffic flows by one or more characteristics, including source and destination IP address, IP protocol, ports, EtherType, and other parameters, depending on the type of ACL. ACLs are named or numbered. ASA has these types of ACLs: extended ACL standard ACL webtype ACL EtherType ACL

## ACS server

The Cisco Secure Access Control System (ACS) server is a RADIUS security server that is the centralized control point for managing network users, network administrators, and network infrastructure resources. This product has reached its end-of-life. Migration path is to the Cisco Identity Services Engine (ISE).

## action (rule action)

A component of a rule that determines how the system handles traffic that matches the rule.

## actionable intelligence

The prioritization, remediation, and attribution of risk from malware that allows you to clean up, prioritize, remediate, and prevent threats more effectively in the future.

## active host

A host that is known to the Stealthwatch Flow Collector and that has transmitted a data packet in the last 5 minutes. Contrast with 'inactive host.'

## actor

See 'threat actor.'

## Advanced Persistent Threat

Attack against a network during which an unauthorized person gains access and remains undetected for an extended period of time. The purpose of the attack is to illicitly obtain data, such as financial or competitive information, rather than to cause damage to the network.

## affected

A term used to describe an asset or host when it has been touched by a finding, ranging from anomalous observed data to a threat or malware.

## alarm

A notification of unusual network activity or event that meets or exceeds a defined set of criteria that can indicate unacceptable behavior on your network.

## alarm category

A “bucket” toward which a defined list of security events contributes. When network activity meets or exceeds a defined set of criteria specified, it triggers an alarm. Contains only host alarms. Alarm categories contain only host alarms. A host alarm is a security event that has triggered an alarm.

## alert

A type of alarm to prepare for action, or to warn of an approaching threat. To be on the alert is to be on the lookout for danger and ready to act. See also 'alarm.'

## allow (rule action)

A rule action that allows matching traffic to continue to the next stage of analysis or handling. Note that an allow rule does not necessarily allow traffic to continue directly to its destination. For example, traffic that is allowed by a Firepower access control rule is still subject to network discovery, identity requirements, intrusion inspection, malware inspection, and rate limiting (QoS). Contrast 'allow' with the 'trust' and 'fastpath' actions, which bypass more inspection.

## allow/allowed list

A list of senders, domains, or applications that are allowed or permitted access. For example: In the SMA, the list specifies senders and domains that are never treated as spam. In the ESA, the list specifies known good senders that are not subjected to anti-spam scanning or rate limiting by the $TRUSTED mail flow policy. In Umbrella, this is a type of destination list with approved DNS addresses. Contrast with 'block list' and 'blocked list.'

## AMP (Advanced Malware Protection)

Protective technology that monitors files, processes, memory, and network connections to detect and block known and unknown threats based on a variety of engines.

## analysis engine

A process that takes information from sensors and processes it. Subtypes include: detection engine—consumes information (such as events, telemetry, and intelligence) and produces alerts enforcement engine—controls which activity on a network or an endpoint can take place (may also be known as enforcement agent or controller) enrichment engine—takes events and alerts and combines them with other data to annotate and aggregate them to support actions (such as triage and response) intelligence engine—extracts threat intelligence (in forms such as judgments and indicators) from a flow of information statistics engine—summarizes and generates telemetry from a flow of events and alerts triage engine—takes events and alerts, and escalates them into incidents, or otherwise helps to classify and filter them for presentation

## analyze (rule action)

A rule action that allows matching traffic to continue to the next stage of analysis or handling. Firepower prefilter policies use the analyze action instead of the allow action.

## ancestor policy

A policy that has one or more descendant policies of the same type. These descendant policies inherit settings from the ancestor policy. See also 'parent policy.'

## anomalous observed data

Information or event that was observed or happened in the network, that deviates from the baseline of normal network behavior monitored and established by the Cognitive system. Contrast with 'sighting,' which implies recognition.

## anomaly

A deviation from what's normal or expected. For instance, in Cognitive Intelligence, an anomaly is any unusual activity, trend, or event found by real-time monitoring or offline analysis of network property or entity behaviors.

## AnyConnect local policy

Determines when AnyConnect software and profile updates can occur, as well as when to exclude certificate stores, enable FIPS mode, restrict caching, and so on.

## APCF (Application Profile Customization Framework)

Lets a security appliance handle nonstandard applications so that they render correctly over a WebVPN connection.

## app

A computer program generally accessed using web browsers in desktop operating systems, and natively on mobile devices. Apps are often associated with cloud services, and frequently offer limited and/or targeted functionality. Apps may not be versioned, particularly when they represent the user interface for a cloud-based service. Contrast with 'application.'

## appliance

A device designed to perform a task such as protect computer networks from unwanted traffic.

## application

A computer program that runs natively in a desktop operating system. Applications are generally versioned. Contrast with 'app.'

## archive hour

User-defined time when each Stealthwatch Flow Collector in the domain resets itself. Acceptable values are 0 to 23, where 0 is midnight local time. At the defined time, the Flow Collector resets all index counts to zero, saves the log and web files it has gathered during the preceding 24 hours, and then begins a new day (24 hours) of data collection. Defined on the Domain page of the Domain Properties dialog.

## artifact

A file or other object generated by a submitted sample during analysis. An artifact may be any type of file, such a Word document, a graphic (.png, .jpg, etc.), or a downloaded executable. An artifact may be a file-like object, such as an image of a process running in memory. An artifact may be a SHA256, or an IP address or domain implicated in a compromise.

## ASA (Adaptive Security Appliance)

Combines firewall, VPN concentrator, and intrusion prevention into one software image. Operates in single mode and multimode.

## ASA FirePOWER

The short name for ASA with FirePOWER Services.

## ASA with FirePOWER Services

An ASA device running an ASA FirePOWER module (NGIPS).

## ASDM (Adaptive Security Device Manager)

An application for managing and configuring a single ASA.

## asset

A component of the network environment, such as hardware, software, and information, that enables and supports the communication of data. In business terminology, something the business can put value on and hence evaluate the risk of a finding.

## authenticate

Validate that a user, device, or software process is who or what they say they are based on credentials, such as password, digital certificate, biometrics, or some combination.

## authorized network

A network that has been authorized for organization members (including devices) to access the Threat Grid Panacea server. Defined in the Authorized Networks field on the Organization page.

## autostate

In normal autostate mode, the Layer 3 interfaces remain up if at least 1 port in the VLAN remains up. If you have appliances, such as load balancers or firewall servers that are connected to the ports in the VLAN, you can configure these ports to be excluded from the autostate feature to make sure that the forwarding SVI does not go down if these ports become inactive.

## AVC (Application Visibility and Control)

Products Firepower Usage Docs—Expand on first use. GUI—Always spell out, unless it's in a part of the GUI that's all about AVC, such as when a page title already clearly identifies the context as Application Visibility and Control, then you can abbreviate as needed.

## backhaul

Refers to the idea that traffic is not directed immediately to its ultimate destination (for example, facebook.com ), but is first routed through a nonoptimal hop- like NGFW running at the central datacenter, or the idea that all traffic from a remote office goes through the central office before heading out to the internet. Often referred to when VPN traffic gets routed through the central node before letting it back out to the ultimate destination on the public internet.

## backplane

The physical connection between an interface processor or card and the data buses and the power distribution buses inside a chassis.

## base policy

If you're configuring policy inheritance or policy layers, the base policy is the lowest-level policy in the stack. Other policies of the same type inherit rules and settings from the base policy.

## behavioral indicator

Key traits and behaviors that have been identified as indicators of malicious activity. Behavioral indicators include threat severity levels, HTTP traffic, DNS traffic, TCP/IP network sessions, processes, artifacts, registry activities, and more.

## BIOS (Basic Input/Output System)

The program that starts the sensor and communicates between the devices in the appliance and the system.

## blacklist

Usage Do not use. Instead, standardize use around 'block list' (to mean a list that blocks). In cases where it makes more sense, it's okay to use 'blocked list' (to mean a list of blocked items).

## block (rule action)

A rule action that blocks matching traffic without further inspection of any kind.

## block page bypass code

A code that can be given to certain individuals (or a group of individuals) to allow them to go to some or all blocked websites until the code expires.

## block page bypass user

A special user account that gives the rights to certain individuals (or a group of individuals) to go to blocked sites while still being part of the enforcement given to the larger policy group they belong to. For users of the Umbrella dashboard, it is a similar—but distinctly different—concept to Grant Permissions to a User in the Umbrella dashboard.

## block with reset (rule action)

A rule action that blocks matching traffic without further inspection of any kind, and resets the connection.

## block/blocked list

A list of senders, domains, or applications that are blocked or restricted from access. For example, in the ESA, the list specifies known bad senders that get rejected by the $BLOCKED mail flow policy. Contrast with 'allow list' and 'allowed list.'

## botnet

A collection of software robots, or bots, that run autonomously and automatically. The term is often associated with malicious software but it can also refer to the network of computers using distributed computing software. The term botnet is used to refer to a collection of compromised computers (called Zombie computers) running software, usually installed through worms, Trojan horses, or back doors, under a common command-and-control infrastructure.

## box

Usage Do not use to refer to an appliance, chassis, or device.

## BPDU (bridge protocol data unit)

Spanning tree protocol hello packet that is sent out at configurable intervals to exchange information among bridges in the network. Protocol data unit is the OSI term for packet.

## brownfield

Usage Do not use. Instead, standardize use around 'existing deployment.' See also 'greenfield.'

## bypass mode

Mode that lets packets continue to flow through the appliance even if the appliance fails. Bypass mode is only applicable to inline-paired interfaces.

## byte distribution

Histogram giving the frequency of occurrence for each byte value, or range of values, in the first N bytes of application payload for a flow.

## C-Rank

Algorithmic classifier derived from co-occurrence patterns among domains. Co-occurrence of domains means that a statistically significant number of clients have requested both domains consecutively in a short time frame.

## CA (certificate authority)

The certificate issuer used to create server certificates or user public key certificates. Server and user certificates provide an additional confirmation of a server or a user identity. A third-party entity that is responsible for issuing and revoking certificates. Each host with the public key of the CA can authenticate a host that has a certificate issued by the CA. The term CA also refers to software that provides CA services.

## CA certificate

Certificate for one CA issued by another CA.

## CacheCheck

Tool that allows internet users insight into what is happening in their DNS, empowering them to manually refresh DNS caches on their own. When a domain is failing and a website appears to be down, internet users can refresh the massive Umbrella caches and update them with the most current addresses for websites, in many cases enabling access automatically.

## CASB (Cloud Access Security Broker)

Placed between cloud service providers and their consumers, a CASB enforces security policies as cloud-based resources are being accessed, thereby addressing cloud service risks, even when cloud services are beyond the enterprise perimeter and out of the organization's direct control.

## CC (Common Criteria)

An international set of guidelines and specifications developed for evaluating information security products, specifically to ensure they meet an agreed-upon security standard for government deployments.

## Centralized Settings

From Umbrella service provider consoles (MSP, MSSP, ISP, Multi-Org), these settings are applied to a customer’s Umbrella policy settings (default policy or all policies depending on settings). They can be applied concurrently to multiple customers, including new customers as they come on board.

## certificate

A signed cryptographic object that contains the identity of a user or device and the public key of the CA that issued the certificate. Certificates have an expiration date and may also be placed on a CRL if known to be compromised. Certificates also establish nonrepudiation for IKE negotiation, which means that you can prove to a third party that IKE negotiation was completed with a specific peer.

## certificate authentication

The use of a digital certificate to identify users, appliances (that need to communicate with back-end services), desktops, laptops, and any mobile devices before granting access to a resource, network, application, and so on. The certificates are stored locally on the device. Unlike other solutions that only work for users (like biometrics or username/password), the same solution can be used for all endpoints.

## certificate matching

Those certificates that match a specific set of keys established in the AnyConnect client profile with criteria such as key usage, extended key usage, and distinguished name.

## CHAP (Challenge Handshake Authentication Protocol)

An authentication protocol for communicating with the RADIUS server for configuring external authentication or two-factor authentication on the appliance.

## chassis

A physical structure that houses the hardware components.

## child policy

A descendant policy that inherits rules and settings from its immediate ancestor, or parent , policy.

## CIMC

Cisco Integrated Management Controller

## Cisco DNA (Digital Network Architecture)

Cisco’s enterprise architecture for intent-based networking across the campus, branch, WAN, and extended enterprise. Cisco DNA is the core architecture that is the platform for software innovations and infrastructure. The Cisco DNA architecture is delivered through: Cisco DNA Center: command and control for policy, automation, and analytics Cisco DNA Solutions: SD-Access, SD-WAN, and Assurance and Network Security Cisco DNA-ready physical and virtual infrastructure: switching, routing and wireless

## Cisco IOS (Internetwork Operating System)

Cisco system software that provides common functionality, scalability, and security for all products under the CiscoFusion architecture. Cisco IOS allows centralized, integrated, and automated installation and management of internetworks while supporting a wide variety of protocols, media, services, and platforms.

## Cisco Threat Response

An investigative tool that leverages AMP, Investigate, Talos, Threat Grid, and other Cisco and 3rd party products and services, to simplify and speed up common incident response tasks by automating and collating research and response functions across those multiple products and tools.

## Cisco TrustSec

Provides access control that builds upon an existing identity-aware infrastructure to ensure data confidentiality between network devices and integrate security access services on one platform. In the feature, enforcement devices use a combination of user attributes and endpoint attributes to make role-based and identity-based access control decisions. The availability and propagation of this information enables security across networks at the access, distribution, and core layers of the network. https://www.cisco.com/c/en/us/solutions/enterprise-networks/trustsec/index.html

## Cisco Umbrella

Cloud-based security platform that uses the internet’s infrastructure to block malicious destinations before a connection is ever established. Umbrella builds on a flexible, scalable cloud platform to continuously evolve ahead of the pace of threats, providing cloud-delivered network security for any device, anywhere, anytime.

## Cisco VRT

Cisco Vulnerability Research Team

## claimed (CDO)

Used in the context of CDO and serial number onboarding: A device is 'claimed' if its serial number has been onboarded to a CDO tenant.

## class map

Used for Modular Policy Framework; the class map, using an ACL or other criteria, matches traffic for a service policy.

## client policy

Determines various options in the Network Access Manager, such as connection settings, media types, end user controls, and administrative status.

## cluster (Cognitive)

Incidents that have similar malware symptoms and correlated behaviors are grouped into a cluster.

## cluster (Threat Grid Appliance)

Two or more appliances joined together and saving data in a shared file system such that all nodes have the same data as the other nodes in the cluster. The main goal of clustering is to increase the capacity and scalability of a single system by joining several appliances together, and to support redundancy and recovery from failure.

## collection name

The name of a collection of threat feeds that is hosted on the TAXII server. For example, 'guest.Abuse.ch.'

## command-and-control callback

Cisco Umbrella blocks the command-and-control callbacks made by the botnet to prevent compromised devices from communicating with the attackers' infrastructure.

## command-and-control server

Server controlled by an attacker which is used to remotely send commands to a network of devices infected by malware or botnet.

## compromised

When a computer or device is in a hazardous or objectionable state as the result of one or more potentially related events, such as malware infection, credential theft, and so on.

## computer

An outside computer, not the Cisco product.

## concern index

Primary means by which the system notifies you of suspicious activity. The Stealthwatch Flow Collector adds points to the concern index whenever it observes possible attacks on one or more hosts. The greater the concern index, the greater the level of concern over that behavior. When activity surpasses 100% of the index threshold set for a particular host, the Flow Collector generates a High Concern Index alarm against that host. See also 'alarm.'

## connect on demand

How Apple iOS checks other applications that start network connections, using the Domain Name System (DNS) and how match domain and host are defined.

## connection failure policy

This policy blocks traffic if a connection to the Cisco Cloud Web Security proxy server cannot be established or allows traffic when it can.

## connection profile

Determines how the user connects to the headend and to which tunnel group based on both its authentication and authorization configuration.

## console

A window in which the user interacts with an application or device using a command line interface.

## console (Umbrella)

Web-based portion of the service provider products through which the user interacts with the software, configuring and monitoring the system. The parent org uses the console, child the dashboard.

## console port

A physical interface on an appliance into which you plug an Ethernet or other cable so that you can administer a device, or an application on that device, using a console.

## content category

A grouping of websites with similarly themed content matching one of the types listed here: https://support.umbrella.com/hc/en-us/articles/231265768-Getting-Started-Category-Settings-and-Content-Category-Details

## content filter

Used to process messages during the Per-Recipient Scanning phase of the work queue in the email pipeline. Content filters are evoked after Message filters and act on individual, splintered messages.

## content matching classifier

The detection component of the data loss prevention scanning engine. A classifier contains a number of rules for detecting sensitive data, along with context rules that search for supporting data. For example, a credit card classifier not only requires that the message contain a string that matches a credit card number, but that it also contains supporting information such as an expiration data, a credit card company name, or an address.

## control subject

Internal convention for a virtual machine image used for sample analysis.

## conversational bounce

A bounce that occurs within the SMTP conversation. The two types of conversational bounces are hard bounces and soft bounces: hard bounce—a message that is permanently undeliverable soft bounce—a message that is temporarily undeliverable

## coordinates

An incident is located by coordinates that describe where and when the incident happened. With sufficient granularity, you can use the coordinates to locate the incident and correlate with other systems. Coordinates are composed of username, IP address, or MAC address coupled with a corresponding time span. For example, IP address 10.0.0.1 from Thursday to Friday. A single set of coordinates may refer to only one incident at a time.

## CRL (Certificate Revocation List)

A digitally signed message that lists all of the current but revoked certificates listed by a given CA. This is analogous to a book of stolen charge card numbers that allow stores to reject bad credit cards. When certificates are revoked, they are added to a CRL. When you implement authentication using certificates, you can choose to use CRLs or not. Using CRLs lets you easily revoke certificates before they expire, but the CRL is generally only maintained by the CA or an RA. If you are using CRLs and the connection to the CA or RA is not available when authentication is requested, the authentication request fails.

## CRUD (Create, Read, Update, and Delete)

This is a developer term used to describe the implementation of basic functionality. In computer programming, create, read, update, and delete are the four basic functions of persistent storage. Alternate words are sometimes used, such as retrieve instead of read, modify instead of update, and destroy instead of delete.

## CSA integration

Other Cisco appliances and products, such as the ESA/WSA appliances, that connect with Threat Grid through the Cisco Sandbox API ("CSA API").

## CSM (Cisco Security Manager)

The provisioning component of the Cisco Self-Defending Networks solution. CSM is fully integrated with CS-MARS.

## CTIM (Cisco Threat Intelligence Model)

Closely based on STIX, CTIM includes common data models used by Cisco Threat Intelligence services. Allows us to decompose the massive, comprehensive artifacts generated during malware sample analysis and extract the details most relevant to incident response into a data model specifically designed for rapid storage, retrieval, and enrichment.

## CTIQBE (Computer Telephony Interface Quick Buffer Encoding)

A protocol used in IP telephony between the Cisco CallManager and CTI TAPI and JTAPI applications. CTIQBE is used by the Cisco CallManager for call setup and voice traffic across the ASA.

## cut-through proxy

Enables the ASA to provide faster traffic flow after user authentication. The cut-through proxy challenges a user initially at the application layer. After the ASA authenticates the user, it shifts the session flow and all traffic flows directly and quickly between the source and destination while maintaining session state information.

## dashboard (Umbrella)

Web-based portion of the Umbrella product through which the user interacts with the software to configure and monitor the system. In *SP, dashboard is what child org sees. Do not use dashboard for service provider consoles.

## data collection policy

Determines what type of data (VPN, trusted, or untrusted) to send and whether the data (type, fields, or network state of the interface) is anonymized or not in NVM. The policy associates this data with a network type or connectivity scenario.

## DCE (data circuit-terminating equipment)

Devices and connections of a communications network that comprise the network end of the user-to-network interface. The DCE provides a physical connection to the network, forwards traffic, and provides a clocking signal used to synchronize data transmission between DCE and DTE devices. Modems and interface cards are examples of DCE.

## decrypt (rule action)

A rule action that decrypts encrypted traffic and passes it to the next phase of analysis. There are two kinds of decrypt actions: decrypt known key decrypt re-sign

## decryption policy

Decryption policies determine whether HTTPS transactions should be decrypted, dropped, or passed through.

## default action

In a policy, the action the system uses when network traffic does not match any of that policy's rules or other settings.

## delayed bounce

A bounce that occurs within the SMTP conversation. The recipient host accepts the message for delivery, only to bounce it at a later time.

## DES (data encryption standard)

Published in 1977 by the National Bureau of Standards and is a secret key encryption scheme based on the Lucifer algorithm from IBM. Cisco uses DES in classic crypto (40-bit and 56-bit key lengths), IPsec crypto (56-bit key), and 3DES (triple DES), which performs encryption three times using a 56-bit key. 3DES is more secure than DES but requires more processing for encryption and decryption. See also 'AES' and 'ESP.'

## descendant policy

A policy that inherits rules and settings from another policy of the same type. See also 'child policy.'

## destination

Where the traffic is destined to arrive. A target network, host, port, domain, URL, or IP address for which a request is being made.

## destination list

A list of destinations (for example, domain name, URL, or IP address) that is used to manage—block or allow—customer or organization access to specific internet destinations.

## device

Generic term that may refer to a Cisco security product after you've officially introduced it. May also refer to a device connected to the Cisco security product to communicate with the network, such as a firewall, router, switch, or computer. Can be a physical hardware or virtual device.

## device (Threat Grid)

User. Each device is treated as a user record.

## device user

Licensing authority for device entitlements.

## digital certificate

Usage See 'certificate.'

## directional policy

A set of rules that offers additional control through the policy feature. It is a solution to either of the following scenarios when you are investigating a security event: The behavior you discovered is of concern in general, but not for the current situation. The behavior you discovered is of concern, but in only a few specific situations.

## disposition

Calculated from an analysis engine about the intent or nature of an observable: whether it's malicious, suspicious, unknown, common, clean, and so on.

## DLP (data loss prevention) incident

A data loss prevention incident occurs when a DLP policy detects one or more DLP violations that merit attention in an outgoing message.

## DLP (data loss prevention) policy

A set of conditions used to determine whether content contains sensitive data and the actions that can be taken on the content that contains such data.

## DLP (data loss prevention) violation

An instance of data being found in a message that violates your organization’s DLP rules.

## DNS-O-Matic

A free service from Cisco Umbrella that gives you an easy way to distribute your dynamic IP changes to multiple services with a single update.

## DNSCrypt

Cisco Umbrella approach to securing the critical 'last mile' of DNS traffic and resolving an entire class of serious security concerns with the DNS protocol.

## do not decrypt (rule action)

A rule action that passes encrypted traffic to the next phase of analysis, without decrypting it.

## DoDIN APL (Department of Defense Information Network Approved Products List)

The DoDIN APL is the single approving authority for all Military Departments (MILDEPs) and DoD agencies in the acquisition of communications equipment that is to be connected to the Defense Information Systems Network (DISN) as defined by the Unified Capabilities Requirements (UCR).

## domain

An identification string that refers to one or more IP addresses. Registered in the Domain Name System (DNS) and used to provide recognizable names to numerically addressed resources on the internet. A domain is the name of a website.

## DoS (denial-of-service), DDoS (distributed denial-of-service)

An attack in which a multitude of compromised systems attack a single target, thereby causing denial of service for users of the targeted system. The flood of incoming messages to the target system essentially forces it to shut down, thereby disrupting access and denying service to the system to legitimate users.

## drive

Generic term to refer to a drive when it is not necessary to point out what specific drive it is.

## drop (rule action)

Block.

## drop and generate events

An intrusion rule action that drops (blocks) matching packets, and logs an intrusion event. You cannot block without logging. Contrast with the generate events action, which logs an intrusion event without dropping matching packets. An intrusion rule with a drop and generate events action is like an access control rule with a block action and logging enabled.

## DTP (Dynamic Trunking Protocol)

A Cisco-proprietary protocol in the VLAN group used for negotiating trunking on a link between two devices and for negotiating the type of trunking encapsulation (ISL or 802.1q) to be used.

## dynamic analysis

Sample analysis includes processes that capture any actions that are performed by the file. This is the dynamic analysis of the sample submission. For example, making a change to the registry, creating other files, launching executables, communicating with a remote IP address, generating other artifacts, and so on. Dynamic analysis also includes emulating user behavior with playbooks. These are canned sets of user behaviors, such as clicking the OK button in a dialog, which may be selected during sample submission. Many user actions will trigger malware. The results of running a playbook is part of the dynamic analysis.

## dynamic NAT

Translates a group of real addresses to a pool of mapped addresses that are routable on the destination network. The mapped pool typically includes fewer addresses than the real group. When a host you want to translate accesses the destination network, the ASA assigns the host an IP address from the mapped pool. The translation is added only when the real host initiates the connection. The translation is in place only for the duration of the connection, and a given user does not keep the same IP address after the translation times out.

## dynamic PAT

Translates multiple real addresses to a single mapped IP address by translating the real address and source port to the mapped address and a unique port. Lets multiple outbound sessions appear to originate from a single IP address. With PAT enabled, the appliance dynamically chooses a unique port number from the PAT IP address for each outbound translation slot (xlate). This feature is valuable when an ISP cannot allocate enough unique IP addresses for your outbound connections. The global pool addresses always come first, before a PAT address is used.

## egress

The action of traffic going out.

## EIGRP (Enhanced Interior Gateway Routing Protocol)

This is a Cisco-proprietary protocol. The ASA does not support EIGRP.

## Email Security Manager

A single, comprehensive dashboard to manage all email security services and applications on IronPort appliances. Email Security Manager lets you manage outbreak filters, anti-spam, anti-virus, and email content policies on a per recipient or per sender basis through distinct inbound and outbound policies.

## EMBLEM (Enterprise Management BaseLine Embedded Manageability)

A syslog format designed to be consistent with the Cisco IOS system log format and is more compatible with CiscoWorks management applications.

## encounter

Detection of an observable outside of my environment (off network). See also 'sighting.'

## endpoint

A computing device used to connect to and communicate on a network.

## endpoint (Threat Grid)

API endpoints are URIs representing server resources that can be used by client applications.

## Endpoint Concentrator

An appliance that analyzes high-value endpoint contextual data collected by the AnyConnect NVM.

## endpoint isolation

Process of isolating a compromised endpoint by blocking all network traffic to and from the endpoint. This prevents command-and-control communication, exfiltration of sensitive information, and further spread of malware. Can allow certain IP addresses to access the endpoint to perform forensics and cleaning of threats. Synonym: node isolation

## enrichment

Annotating or collecting events with threat intelligence, correlated events, and security context. For example, in Threat Grid, the process of using the database to build up context around an observation or a piece of suspicious information, such as a behavioral indicator. By searching the database for related indicators, and following those relationships to other information, you can enrich the information with the context necessary to generate the actionable intelligence to address the problem.

## entitlement

A Threat Grid product or service that has been purchased and is covered in the license agreement. For example, access to Threat Grid Cloud portal and APIs. Entitlements are listed on the Organization Details page. Use the following to describe times and dates related to entitlements: entitlement start—the date the entitlement goes into effect entitlement stop—the last day of the entitlement subscription period entitlement lapse—time from the entitlement stop date to the end of the entitlement grace period entitlement grace period—five days after the entitlement stop date entitlement terminated—end of the entitlement grace period

## entity

Host or endpoint on the network, whether in the cloud or on the local network.

## entity modeling

Analysis of the behavior for every entity on the network or in the public cloud to determine abnormal, suspicious, and malicious activity.

## envelope recipient

The recipient of an email message as defined in the RCPT TO: SMTP command. Also, sometimes referred to as the 'Recipient To' or 'Envelope To' address.

## envelope sender

The sender of an email message as defined in the MAIL FROM: SMTP command. Also, sometimes referred to as the 'Mail From' or 'Envelope From' address.

## EPM (Ethernet Port Module)

Products Hardware Usage Do not use. Instead, use 'network module.'

## ESD (electrostatic discharge)

The rapid movement of a charge from one object to another object, which produces several thousand volts of electrical charge that can cause severe damage to electronic components or entire circuit card assemblies.

## ETF (External Threat Feed) source

Used to download information about a collection of threats that is available on a TAXII server.

## EtherType ACL

An ACL that applies to non-IP layer-2 traffic on bridge group member interfaces only. You can use these rules to permit or drop traffic based on the EtherType value in the layer 2 packet. With EtherType ACLs, you can control the flow of non-IP traffic across the device.

## event

A change of state or observed activity that has occurred on the network or endpoint which has a security significance for the management of the network. Not necessarily suspicious, a cause for alarm, or a security threat.

## exception expression

Pattern allowed by a DLP policy.

## exclusions

A type of list that specifies an application, process, directory, and so on that should be ignored (not scanned) by the endpoint Connector.

## exploit

Attack on a computer system that takes advantage of a particular vulnerability that the system offers to intruders.

## exploit kit

Server-based toolkit used to automate attacks by targeting client-side vulnerabilities in browsers and other software. For example, the Blackhole exploit kit is the most prevalent web threat (as of 2012). Its purpose is to deliver a malicious payload to a victim's computer. It incorporates tracking mechanisms, so that intruders maintaining the kit can obtain information about the victims.

## extended ACL

A group of ACEs with the same ACL ID or name. This is more obvious in ASDM where ACLs are named and the ACEs that comprise them are nested under the name. These ACLs are used for access rules to permit and deny traffic through the device, and for traffic matching by many features, including service policies, AAA rules, WCCP, Botnet Traffic Filter, and VPN group and DAP policies. Extended ACLs are also used to determine the traffic to which other services will be provided. Types of extended access rules: extended access rules (Layer 3+ traffic) assigned to interfaces extended access rules (Layer 3+ traffic) assigned to Bridge Virtual Interfaces (BVI routed mode) extended access rules assigned globally management access rules (Layer 3+ traffic) EtherType rules (Layer 2 traffic) assigned to interfaces (bridge group member interfaces only)

## external event

Data received from technologies other than flow export technologies and associated with behavior-based, flow-driven events.

## fail closed

The state of a device or software where traffic is blocked when traffic handling is busy or down. For example, an AnyConnect fail closed policy disables network connectivity when the VPN is unreachable. Contrast with 'fail open.'

## fail open

The state of a device or software where traffic continues flowing when traffic handling is busy or down. For example, you can configure Firepower to allow traffic to pass without intrusion inspection when the inspection engine is down. For example, an AnyConnect fail open policy permits network connectivity when the VPN is unreachable. Contrast with 'fail closed.'

## fail-to-wire

A physical layer bypass that allows paired interfaces to go into bypass mode so that the hardware forwards packets between these port pairs without software intervention. Provides network connectivity when there are software or hardware failures.

## failover

Failover lets you configure two ASAs so that one takes over operation if the other one fails. The ASA supports two failover configurations, Active/Active failover and Active/Standby failover. Each failover configuration has its own method for determining and performing failover. With Active/Active failover, both units can pass network traffic. This lets you configure load balancing on your network. Active/Active failover is only available on units running in multiple context mode. With Active/Standby failover, only one unit passes traffic while the other unit waits in a standby state. Active/Standby failover is available on units running in either single or multiple context mode. For an ASA, high availability is a condition achieved when two ASAs are configured in an Active/Standby or Active/Active failover mode.

## failsafe

A characteristic of an inline set that lets packets bypass processing and continue through the device if internal traffic buffers are full.

## FamilyShield

A special service offered by Cisco Umbrella that is distinct from our standard packages. Meant for home users who want to keep their children from seeing inappropriate images on their computers, FamilyShield always blocks domains categorized in our system as Tasteless, Proxy/Anonymizer, Sexuality, or Pornography.

## fastpath

Exempt traffic from all further inspection and control, most often used in the context of prefiltering.

## feed

Curated security-related information such as behavioral indicators, malware signatures, security policies and so on, that are often delivered by security service providers on a subscription basis, to enhance the security posture of an application or device. The goal of these feeds is to give customers the most up-to-date security information possible.

## Fetch Stats

Tool to enable administrators to download the Top Domains log data that has been collected for a network. Useful when downloading data ranges that are greater than 200 records, which is the file-size limit for an online download from the Umbrella Stats page.

## field

A single piece of information within an object model.

## file-sharing index

Tracks atypical file transfers, which could indicate peer-to-peer activity, that could place an organization at risk. Once the file-sharing activity for a particular host causes its file-sharing index points to surpass 100% of its threshold, the Stealthwatch Flow Collector generates a High File-Sharing Index alarm. See also 'alarm.'

## FIPS (Federal Information Processing Standards)

Federal Information Processing Standards (FIPS) specify requirements for cryptographic modules that are used by all government agencies to protect sensitive but unclassified information. For hardware, it refers to the opacity shield with tamper-resistant labels covering the front panel of the chassis.

## Flow Collector

A physical or virtual device that aggregates and normalizes NetFlow and application data collected from up to 4000 exporters (such as Cisco routers and switches) per Flow Collector.

## Flow Sensor

A physical or virtual device that provides an overlay solution for generating NetFlow data for older Cisco network infrastructures not capable of natively producing unsampled NetFlow data at line rates, for third-party components that do not support unsampled NetFlow, and for other environments where additional security context is required.

## FMT (Firepower Migration Tool)

A tool to migrate ASA firewall configurations to Firepower Threat Defense (FTD).

## FPS (flows per second)

Number of NetFlow packets detected per second. Used for licensing.

## FQDN (fully qualified domain name)

A domain name that specifies its exact location in the tree hierarchy of the Domain Name System (DNS). It specifies all domain levels, including the top-level domain and the root zone. Always written in this format: [host name].[domain].[tld]. For example, a mail server on the example.com domain may use the FQDN mail.example.com.

## Gb (Gigabit)

Products Any Usage Do not expand.

## GB (Gigabyte)

Products Any Usage Do not expand.

## geodiversity and geodistance scores

Algorithmic classifier that looks at where DNS requests originate, and how far away the requests are from the IP address’ geolocation. The classifier then compares the geographic distribution of DNS requests with the predicted one for the top-level domain (for example, RU, CN, COM).

## global

Setting that applies to everything.

## global configuration mode

Lets you change the ASA configuration. All user EXEC, privileged EXEC, and global configuration commands are available in this mode.

## Global domain

In a multidomain deployment, the top-level domain. If you do not configure multitenancy, all devices, configurations, and events belong to the Global domain. Administrators in the Global domain can manage the entire Firepower System deployment.

## global network (Umbrella)

The Cisco Umbrella global network is comprised of geographically distributed data centers serving 50 million active users daily in more than 160 countries, and delivering the industry’s best uptime. Combined with Umbrella network security services, it provides the ultimate coverage, efficacy, and performance. Umbrella's infrastructure that handles more than 2 percent of the world’s daily internet requests with proven 100 percent uptime. It enforces security policies with no added latency, and in minutes covers any device worldwide, for Umbrella.

## global network resolver

Network of servers managed by Cisco Umbrella that are used to resolve DNS queries.

## globally meshed VPNs

A community of VPN-enabled gateways located at various points throughout the world. Each VPN can communicate with every other member of the community through a VPN tunnel.

## greenfield

Usage Do not use. Instead, standardize use around 'new deployment.' See also 'brownfield.'

## group policy

A collection of attributes and their values that define behaviors of a remote access VPN connection. Attributes in the group policy are stored internally on the ASA, or externally on a AAA server. Group policies are associated with connection profiles (tunnel groups) and local user accounts. Based on the system’s configuration, a group policy is determined and assigned to remote access clients upon the establishment of a VPN connection.

## guardrail

Trusted signing authority that is included on allowed lists.

## hardware bypass

Ensures that traffic continues to flow between an interface pair during a power outage. This feature can be used to maintain network connectivity in the case of software or hardware failures.

## hardware-bypass card

A specialized interface card that pairs physical interfaces so that when a software error is detected, a bypass mechanism is engaged that directly connects the physical interfaces and allows traffic to flow through the pair. The hardware bypass passes traffic at the network interface; it does not pass it to the system.

## HAT (Host Access Table)

Maintains a set of rules that controls incoming connections from remote hosts for a listener. Every listener has its own HAT. HATs are defined for public and private listeners, and contain mail flow policies and sender groups.

## HDD (hard disk drive)

Products Hardware Usage Do not expand.

## high availability

A pair of devices configured for failover to provide redundancy. Common configurations to achieve high availability are active/standby and active/active.

## host

A device that is connected to a network and has an IP address.

## host alarm

A security event that has triggered an alarm for an endpoint Stealthwatch is monitoring.

## host identity

Contextual information about a host gathered by network discovery. Can contain attributes such as basic topology data, device type, operating system, and applications installed on the host.

## hostname

A label used to identify a host on a network.

## hot plug

Lets you add components that expand the system but would not cause interruption to the system.

## hot swap

Lets you add, replace, or remove components without interrupting the system power, entering console commands, or causing other software or interfaces to shut down.

## hotfix

A minor update to a security device that addresses a particular, urgent problem that cannot wait for the next release. Hotfixes are applied to “hot" (in use) devices. As much as possible, a hotfix should not interrupt normal operations.

## identity

A set of attributes, maintained by an authoritative identity source (such as Microsoft Active Directory or LDAP server) that describes a user. Examples of attributes include username, password, group associations, and so on.

## identity (Umbrella)

An entity you create in Umbrella that you can apply policy to and report on. An identity can be an entire network, or as granular as an individual user or device.

## identity firewall

Products ASA Definition Provides granular access control based on users’ identities rather than through source IP addresses. This concept, along with detailed implementations, is documented in the ASA configuration guide. Note Firepower does not identify 'identity firewall' as a feature or a kind of firewall. Customers simply implement security policies based on identity.

## identity NAT

A real address is statically translated to itself, essentially bypassing NAT. You might want to configure NAT this way when you want to translate a large group of addresses, but then want to exempt a smaller subset of addresses.

## identity policy

An identity policy associates traffic on your network with an authoritative identity source and a realm. You can configure access rules and security policies based on identity attributes rather than through source IP addresses. After configuring one or more identity policies, you can associate one with an access control policy and deploy the access control policy to a managed device.

## identity type

A category in which an identity is included. For example, networks, network devices, and roaming computers are identity types. Identities are grouped by type in order to design and apply policies consistently.

## inactive host

A host that is known to the Stealthwatch Flow Collector but has not transmitted a data packet in the last 5 minutes. Contrast with 'active host.'

## inbound rule

Inbound access rules apply to traffic as it enters an interface. Global and management access rules are always inbound.

## incident

An event, use, or behavior that does not conform to an established standard, and that is considered a possible security threat. Can be comprised of multiple events. For example, a malicious PDF file exploits an Acrobat vulnerability to execute a PE file, which in turn downloads malware, which is then detected and quarantined. Each of those events – exploit, download, detection, quarantine – makes up the single incident.

## indeterminate

A verdict that indicates the subject's risk cannot be determined.

## index point

A value that represents an observed use of behavior that matches a defined set of criteria. When the accumulated index points meet or exceed a designated threshold, Stealthwatch triggers the applicable alarm.

## indicator

A trait, behavior, pattern, or set of conditions that indicates the presence of malicious activity or the possibility of a compromise as observed in the field. Not all indicators are behavioral. See 'behavioral indicator.' Additionally, in Threat Response, an indicator can be a collection of judgements or a pattern specification that a sensor uses to characterize events or observed activity.

## infected

A term used to describe an asset or host when you know it is affected by a threat or malware and needs remediation.

## inline

A configuration where devices can affect network traffic flow. Contrast with passive, where you can analyze and respond to, but not affect, the flow of traffic.

## innocuous

A verdict that indicates the subject is listed in the National Software Reference Library (NSRL) database, a repository of known software.

## inside

The first interface, usually port 1, that connects your internal "trusted" network protected by the appliance.

## inspect (rule action)

A rule action used when any inspection properties are applied to the match criteria. Within an access control policy, access control rules provide a granular method of handling network traffic across multiple managed devices. Each rule also has an action, which determines whether you monitor, trust, block, or allow matching traffic. When you allow traffic, you can specify that the system first inspect it with intrusion or file policies to block any exploits, malware, or prohibited files before they reach your assets or exit your network.

## intelligence source

An engine, website, or group of people that produces indicators and related data around malware, attack patterns, weaknesses, campaigns, actors, and targets.

## Intelligent Proxy

When your computer makes a DNS query for a site that sometimes hosts bad content, the Intelligent Proxy kicks in to protect you. Instead of returning the correct address of the website, the DNS server returns the address of the Intelligent Proxy, where Umbrella security software can take a deeper look at the site and protect you as needed.

## interactive block (rule action)

A rule action that allows users to load an initially blocked website after reading a warning.

## interface

The connection between a particular network and an appliance.

## interface PAT (Port Address Translation)

The use of PAT where the PAT IP address is also the IP address of the outside interface.

## intrusion alert

An IPS alert was an alert generated by the Sourcefire Intrusion Prevention System (IPS).

## intrusion event

An event logged when network traffic hits an intrusion rule.

## intrusion set

A grouped set of adversarial behaviors and resources with common properties that is believed to be orchestrated by a single organization. An intrusion set may capture multiple campaigns or other activities that are all tied together by shared attributes indicating a common known or unknown threat actor.

## Investigate (Umbrella)

A Cisco Umbrella threat intelligence product.

## IP (Internet Protocol)

Used to communicate across any set of interconnected networks. Well suited for LAN and WAN communications.

## IP address

An Internet Protocol address.

## IPS alert

Usage Legacy term. Going forward, do not use. Instead, use 'intrusion alert.'

## IPS event

Usage Legacy term. Going forward, do not use. Instead, use 'intrusion event.'

## judgement

A statement by a human or analysis engine that declares the perceived, calculated disposition of an observable: whether it's malicious, clean, suspicious, common, unknown, and so on. There can be many judgements. Judgements are the basis for returned verdicts. They're also the primary means by which users of Threat Response go from observables on their system, to the indicators and threat intelligence data in Threat Response. The judgement has more than just the disposition. It’s a record of which engine made the judgement, how long it is valid, why the judgement was made, and where more details can be seen.

## kill chain

A model of the progress of a security compromise. The dominant one being from Lockheed Martin, using it as a structure for modeling intrusion attacks on a network. The phases are: recon weaponization delivery exploitation installation command and control actions

## KVM (Kernel-based Virtual Machine)

Products Hardware Usage Expand on first use to differentiate from other uses.

## KVM (Keyboard, Video, and Mouse)

Products Hardware Usage Expand on first use to differentiate from other uses.

## last VPN local resource

When a VPN is unreachable, the client applies the last client firewall received from the ASA.

## lexical feature scores

Classifiers used to detect fast flux. Fast flux is a DNS technique that botnet command-and-control infrastructures use to hide behind a compromised system that acts like a proxy.

## lina

A process on a Firepower Threat Defense device. It is closely associated with the ASA software and is frequently used by engineering as a reference to the ASA side of the bicameral FTD brain (the other side being Snort). Lina is closely associated with deploying and interpreting ASA configuration commands, which are used to configure ASA-based features such as routing.

## load balancer

A network device that distributes traffic to optimize performance and resource use. Using discovery, the system can identify load balancers.

## local device manager

An application used to configure a device dedicated to performing a single function. It is "local" because it is installed on the same appliance as the device's software, or it is delivered with the device's software. A local device manager only manages the device it is installed on or delivered with. Firepower Device Manager and Stealthwatch Central Manager are examples of local device managers. The command line interface for a device is also considered a local device manager.

## LOM (LAN on motherboard)

Products Hardware Usage Expand on first use to differentiate from other uses.

## LOM (Lights-Out Management)

The ability for an administrator to monitor and manage systems and their power by remote control.

## low-touch provisioning (CDO)

Refers to the process of shipping an FTD from the factory to a customer site (typically a branch office). An employee at the site connects the FTD to their network, and the device contacts the Cisco Cloud. At that point, the device is onboarded to the CDO tenant if its serial number has already been claimed, or the FTD is parked in the Cisco cloud until it is claimed by a CDO tenant. The device is configured to receive its address by DHCP and the FTD’s default password has not been changed. The user interacting with the hardware is expected to have limited or no interaction with the device other than to plug it in and assess the status lights. See also 'claimed,' 'parked,' and 'serial number onboarding.'

## machine

Products Any Usage Do not use to refer to an appliance, chassis, or device. Exceptions include 'machine-generated,' 'machine learning,' and 'virtual machine.'

## mail flow policy

A way of expressing a group of Host Access Table (HAT) parameters (an access rule, followed by rate limiting parameters and custom SMTP codes and responses) for a listener. Together, sender groups and mail flow policies are defined in a listener’s HAT. Your Cisco appliance ships with the predefined mail flow policies and sender groups for listeners.

## malicious

Something that is known to be dangerous or harmful.

## master

Usage In some cases, used to describe the active unit when 2 units are operating in failover mode with each other. In this context, do not use 'master.' Instead, standardize terminology around 'active' or 'primary.' However, in ASA VPN load balancing, do not use 'master' (and 'backup'). Instead, use 'director' (and 'member').

## MD5

Message-digest algorithm that's a hash function widely used to produce a 128-bit hash value.

## MDI

Media-dependent interface.

## MDIX

Media-dependent interface crossover.

## method

Methods are the possible actions a user can perform on a REST API service. These include GET, PUT, POST, and DELETE.

## MITRE ATT&CK

The MITRE Corporation is a non-profit organization, founded in 1958, that provides engineering and technical guidance on advanced technology problems like cybersecurity for a safer world. MITRE ATT&CK is a knowledge base of the methods that attackers use against enterprise systems, cloud apps, mobile devices, and industrial control systems. ATT&CK, which stands for Adversarial Tactics, Techniques, and Common Knowledge, can help you understand how cyber attackers think and work. See MITRE ATT&CK White Paper at Cisco .

## model

Usage Do not use generically. Instead, use when referring to the actual model number. For example, Firepower 2140 model.

## module (hardware)

A removable component in a chassis, such as a network module or security module.

## module (software)

A software module package that provides additional and complimentary functionality to the primary software on an appliance. A software module is installed separately and licensed separately from the primary function of the device. For example, the FirePOWER services module runs on an ASA and is installed and licensed separately from the ASA software.

## monitor (rule action)

A rule action that ensures logging of matching connections without affecting traffic flow. Monitored traffic is matched against additional rules, if present, to determine how the traffic is handled.

## MPF (Modular Policy Framework)

This is a name given to a strategy which combines ASA objects to achieve an outcome. Combines an access control list (ACL), class map, policy map, and service policy to provide a consistent and flexible way to configure ASA features. The ACL is applied to a class map. The class map defines a traffic matching condition. The class map is associated with a policy map which defines enforcement. The policy map is associated with an interface using a service policy. MPFs can be used to direct traffic to IPS inspection, application inspection, and define Quality of Service requirements for an application.

## MSP (malware storage pack)

A secondary solid-state drive supplied by Cisco that you can install in certain devices to store captured files, which frees space on the device's primary hard drive for event and configuration storage.

## MSP (Managed Service Provider)

A third-party vendor that provides and manages internet services to a client.

## MSSP (Managed Security Service Provider)

A third-party vendor that provides and manages security services to a client.

## MTA (Mail Transfer Agent)

The program responsible for accepting, routing, and delivering email messages. Upon receiving a message from a Mail User Agent or another MTA, the MTA stores a message temporarily locally, analyses the recipients, and routes it to another MTA. It may edit and/or add to the message headers.

## MUA (Mail User Agent)

The program that lets the user compose and read email messages. The MUA provides the interface between the user and the Mail Transfer Agent. Outgoing mail is eventually handed over to an MTA for delivery.

## multi-device manager

A client-based or cloud-based application used to configure a device. A multi-device manager is not installed on the appliance or delivered with the device's software. This kind of manager can manage a single device type or multiple device types. Adaptive Security Device Manager, Cisco Defense Orchestrator, Firepower Management Center, and Cisco Security Manager are examples of multi-device managers. See also 'remote device manager.'

## multi-factor authentication (MFA)

Strengthens access security by requiring two or more different methods (also referred to as factors) to verify your identity. These factors can include something you know (username and password), something you are (fingerprint), or something you have (secondary trusted device like a smartphone app or token to approve authentication requests). Two-factor authentication (2FA) is a subset of MFA.

## NAT (Network Address Translation)

Substituting an IP address in the header of a packet for another IP address so that the packet can be routed from one network to another. One of the main functions of NAT is to enable private IP networks to connect to the internet with a translated, public IP address.

## NEBS (Network Equipment Building System)

Network Equipment Building System (NEBS) compliance refers to the conformance of a network product to the requirements of the NEBS standard. Compliance to this standard indicates that a network product or a telecommunications equipment performs at its optimum capacity.

## NetFlow

An embedded instrumentation within Cisco IOS Software to characterize network operation. By analyzing the data provided by NetFlow, you can determine things such as the source and destination of traffic, class of service, and the causes of congestion.

## network exit localization

Similar in concept to VPN, the Network Exit Localization setting makes any outgoing network traffic that is generated during the analysis to appear to exit from that location. Users may select a different location from the default while submitting samples for analysis, whether from the dropdown list on the Submit Sample modal, or by API.

## NGFW (Next-Generation Firewall)

Means different things to different people. For example, some people consider an ASA with FirePOWER Services to be an NGFW. Other people consider only a Firepower Threat Defense (FTD) device to be an NGFW. The FTD device can be managed by command-line interface, Firepower Device Manager (FDM), Firepower Management Center (FMC), or Cisco Defense Orchestrator. Sometimes, FDM and FMC are confused with next-generation firewalls. These managers are not next-generation firewalls. They're user interfaces to manage traditional firewalls, next-generation firewalls, and even other device types. 'NGFW' is used extensively by Marketing and is the official product name in the Cisco.com product path.

## NGIPS (Next-Generation Intrusion Prevention System)

Firepower software that runs on older/legacy Firepower devices (7000 series, 8000 Series, NGIPSv).

## NLPRank

Classifier that leverages natural language processing (NLP) techniques to detect cyber-squatting and targeted phishing domains.

## node

A node is any device within a connected network of other devices that’s able to send, receive, and/or forward information. The computer is the most the common node and is often called the computer node or internet node. Modems, switches, hubs, bridges, servers, and printers are also nodes, as are other devices that connect over WiFi or Ethernet. Nodes within a computer network must have some form of identification, like an IP address, MAC address, or Data Link Control (DLC) address for it to be recognized by other network devices. A node without this information, or one that has been taken offline, no longer functions as a node.

## NPU (network processor unit)

Products Hardware Usage Expand on first use to differentiate from other uses.

## NTP (Network Time Protocol)

Networking protocol for clock synchronization. For example, the ntpconfig command configures IronPort AsyncOS to use NTP to synchronize the system clock with other computers.

## object

An individual instance of a service.

## object model

The list of data which a service may contain.

## observable

A single, atomic identifier, in the form of a discreet string, that can be recognized and communicated by sensors; such as IP address, domain, file hash, email, MAC address, file name, sensor-specific GUID, and web request. See also 'observation.' For example, the first thing that Threat Response does with an observable is determine its disposition, by aggregating what we know about that observable from the various enrichment modules we have configured. The disposition tells us whether the observable is clean, malicious, suspicious, unknown, and so on. Once we have a disposition for an observable, we begin to enrich it, gathering information about it from enrichment sources such as AMP and the Cisco Threat Intelligence API. Unknown observables are not enriched. See also 'disposition.'

## observation

A fact about your traffic, such as endpoints making connections they have not made before. Observations are not necessarily suspicious. See also 'observable.'

## off-box manager

Usage Do not use. Instead, see 'remote device manager' and 'multi-device manager.'

## OIR (online insertion and removal)

Lets you add, replace, or remove components. OIR requires performing Cisco IOS commands before and after the OIR.

## on premises

Software that runs on computers within an organization. Contrast with cloud software.

## on-box manager

Usage Do not use. Instead, see 'local device manager.'

## open relay

An open relay (sometimes called an 'insecure relay' or a 'third-party relay') is an SMTP email server that allows unchecked third-party relay of email messages. By processing email that is neither for nor from a local user, an open relay makes it possible for unknown senders to route large volumes of email (typically spam) through your gateway.

## OpenDNS

The original company name of Cisco Umbrella. Still used for the public free offering of Umbrella.

## OpenDNS Updater

Software that ensures that Umbrella preferences are preserved whenever IP addresses change.

## Orbital, Orbital Advanced Search

Near real-time endpoint search and forensic snapshot service. Uses osquery.io schema for SQL queries. Currently a beta service installed by AMP for Endpoints Windows Connector.

## organization (Threat Grid)

An entity created within Threat Grid that is used to group users according to how the privacy and visibility rules are to be applied. Only users within the same organization can see samples that have been designated as private. A Threat Grid organization on the cloud can only be created by Threat Grid staff. Organizations can only be created on a Threat Grid appliance by an admin user.

## organization, org (Umbrella)

Generally, a term used in conjunction with service provider console. An organization is the term used to describe a customer.

## outbound rule

Outbound rules apply to traffic as it exits an interface. An outbound ACL is useful, for example, if you want to allow only certain hosts on the inside networks to access a web server on the outside network. Rather than creating multiple inbound ACLs to restrict access, you can create a single outbound ACL that allows only the specified hosts. The outbound ACL prevents any other hosts from reaching the outside network. This term does not refer to a higher security to lower security interface, commonly known as outbound. This term does not apply to Firepower firewalls: All access control rules in Firepower are modeled as global rules in the data plane. Global rules are always inbound.

## Outbreak Filters

IronPort’s Outbreak Filters feature provides an additional layer of protection from viruses. The Outbreak Filters feature quarantines suspicious email messages, holding the messages until an updated virus IDE is available, or until they are deemed not a threat.

## outside

The first interface, usually port 0, that connects to other "untrusted" networks outside the appliance.

## PAN (Policy Administration Node)

See PAP (Policy Administration Point). Policy administration node is the Cisco term for this function.

## PAP (Password Authentication Protocol)

An authentication protocol for communicating with the RADIUS server for configuring external authentication or two-factor authentication on the appliance.

## PAP (Policy Administration Point)

Defines and inserts policies into the authorization system. Also acts as an identity repository by providing Cisco TrustSec tag-to-user identity mapping and Cisco TrustSec tag-to-server resource mapping. Policy administration point is the industry standard term for this function. In the Cisco TrustSec solution, the Cisco Identity Services Engine (ISE) acts as the PAP. However, ISE diverged from industry standard terms: they call their PAP a policy administration node (PAN).

## parameter

A variable added to a REST API request which provides information for executing the method on the service. This can be as simple as the UUID of the specific resource being deleted or include the entire model when creating an object.

## parked (CDO)

Used in the context of CDO and serial number onboarding: A device is 'parked' if it has connected to the Cisco Cloud and its serial number has not been claimed by a CDO tenant.

## Partner console

Console used to create and start trials of Cisco Umbrella.

## pass through

Allow encrypted traffic to pass without decryption or further checks.

## passive interface

A sensing interface configured to analyze traffic in a passive deployment.

## PAT (Port Address Translation)

PAT translates multiple real addresses to a single mapped IP address by translating the real address and source port to the mapped address and a unique port. If available, the real source port number is used for the mapped port. However, if the real port is not available, by default the mapped ports are chosen from the same range of ports as the real port number: 0 to 511, 512 to 1023, and 1024 to 65535. Therefore, ports below 1024 have only a small PAT pool that can be used. Each connection requires a separate translation because the source port differs for each connection. For example, 10.1.1.1:1025 requires a separate translation from 10.1.1.1:1026.

## patch

A minor upgrade that includes a limited range of fixes.

## PBR (policy-based routing)

Traditional routing is destination-based, meaning packets are routed based on destination IP address. However, it's difficult to change the routing of specific traffic in a destination-based routing system. With PBR, you can define routing based on criteria other than destination network. PBR lets you route traffic based on source address, source port, destination address, destination port, protocol, or a combination of these. PBR is defined by access lists and route maps. PBR is available in routed mode only.

## peer

Devices that communicate with each other without having to go through a server, such as sharing files over a peer-to-peer network.

## phantom host

A host that was previously unknown to the Stealthwatch Flow Collector and that was sent a data packet, but did not respond within 10 seconds. A large number of phantom hosts can be an indication of network scanning.

## PhishTank

The first and most successful collaborative clearinghouse for data and information about phishing on the internet. PhishTank is based on the idea that security researchers, exploited brands, technology developers, academic institutions and internet users are stronger together in fighting phishing than they are on their own.

## PID (product identifier)

The orderable product identifier that is 1 of the 3 parts of the UDI. The UDI is part of the PEP policy.

## platform

Refers to a series of hardware models.

## playbook

Products Threat Grid Usage See 'user emulation playbook.'

## policy

A mechanism for grouping and applying rules or settings. For more information, see the Policy archetype .

## policy (Stealthwatch Enterprise)

A set of rules that you can apply to entities within your network that monitors and can alert on behavior.

## policy (Umbrella)

Access to content rules and controls that determine how an Identity is protected by Umbrella. Created through the Policy wizard.

## polling interval

Defines the frequency of fetching threat feeds from a TAXII server.

## polling path

The part of the URL that identifies the polling service in the TAXII server. For example, '/taxii-data.'

## popularity and page rank scores

A ranking score based on the number of distinct origin IP addresses that have visited a domain name. This is a Bayesian average, similar to reputation scores.

## POST (Power-On Self Test)

Set of hardware diagnostics that runs on a hardware device when that device is powered on.

## PPoV (Partner Proof of Value)

Partner Proof of Value and Partner console.

## preshared key

Provides a method of IKE authentication that is suitable for networks with a limited, static number of IPsec peers. This method is limited in scalability because the preshared key must be configured for each pair of IPsec peers. When a new IPsec peer is added to the network, the preshared key must be configured for every IPsec peer with which it communicates. Using certificates and CAs provides a more scalable method of IKE authentication.

## private

A privacy setting that controls access to sample analysis results. Samples designated as private are only available to members of the same organization as the submitting user or integration. Users who belong to a different organization than the submitting user have no access to the the analysis results.

## private key

A cryptographic key known only to the owner of the paired public key certificate. The public key and private key are used for Secure Sockets Layer (SSL) and Transport Layer Security (TLS) encryption and decryption.

## privleged EXEC mode

Privileged EXEC mode lets you change current settings. Any user EXEC mode command works in privileged EXEC mode.

## promiscuous mode

A passive interface for monitoring packets of the network segment. The sensing interface does not have an IP address assigned to it and is therefore invisible to attackers.

## provision (FTD)

Strictly speaking there are two sets of actions that occur at the beginning of the FTD setup: provisioning accept EULA create new password system initialization configure management IP address (IP type, DHCP/static) set FQDN set DNS servers choose to manage the device locally (with FDM) However, to the user, all of this is initial provisioning. This definition is useful to differentiate a claiming error and a provisioning error in CDO.

## PUA (Potentially Unwanted Application)

An application that is not malicious but may be considered to be unsuitable and undesirable for the business network.

## public

A privacy setting that controls access to sample analysis results. Samples designated as public are available to all other users, regardless of which organization they belong to. (The one exception to this rule is for public samples submitted by integrations: integrations from a different organization will only have partial access to the analysis results.)

## public key

A public key is one of a pair of keys that is generated by devices involved in public key infrastructure (PKI). Data encrypted with a public key can only be decrypted using the associated private key. When a private key is used to produce a digital signature, the receiver can use the public key of the sender to verify that the message was signed by the sender. These characteristics of key pairs provide a scalable and secure method of authentication over an insecure media, such as the internet.

## pxGrid (Cisco Platform Exchange Grid)

Enables collaboration between components of the network infrastructure, including security-monitoring and network-detection systems, identity and access management platforms, and so on. These components can use pxGrid to exchange information through a publish/subscribe method.

## RAID (Redundant Array of Independent Disks)

Products Hardware Usage Do not expand.

## RAT (Recipient Access Table)

Defines which recipients are accepted by a public listener. Specifies the address (which may be a partial address or hostname) and whether to accept or reject it. Optionally, you can include the SMTP response to the RCPT TO command for that recipient. The RAT typically contains your local domains.

## rate limit (Threat Grid)

A setting that controls the number of samples that may be submitted to Threat Grid for analysis by API within a particular timeframe. The sample rate limit is set in the Threat Grid license entitlements and maintained at the organization level. Additional rate limits within the organization can be further specified for greater control, including limits set on individual users and devices. A rate limit is set as [[N,minutes]], where N is the number of samples and minutes is the timeframe. For example, [[100,1440]] is 100 samples within 1440 minutes (24 hours). Multiple limits may be set for additional control. For example, [[100,1440],[50, 720]]. The rate limit timeframe begins when the first sample is submitted for analysis. Rate limits use a turnstile model: once the rate limit is reached for the timeframe specified, no more samples may be submitted until the timeframe has expired. Each sample expires one at a time. As each sample reaches the timeframe limit, it is cleared from the rate limit, and another sample may be submitted. Note that the rate limit order does not matter: the more restrictive limit is applied first.

## RCM (Resource Conservation Mode)

When an SMA becomes overloaded, it enters into the Resource Conservation Mode (RCM), and sends a critical system alert. This is designed to protect the appliance and allow it to process any backlog of messages.

## regular expression

A sequence of characters that defines a search pattern.

## remote device manager

A client-based or cloud-based application used to configure a device. A remote device manager is not installed on the appliance or delivered with the device's software. Adaptive Security Device Manager, Cisco Defense Orchestrator, Firepower Management Center, Cisco Security Manager, and a Meraki dashboard are examples of remote device managers. See also 'multi-device manager.'

## report

Mechanism used to track all activities within an organization over time.

## reputation filter

A way of filtering suspicious senders based on their reputation. The SenderBase Reputation Service provides an accurate, flexible way for you to reject or throttle suspected spam based on the connecting IP address of the remote host.

## response action

An effect automatically triggered when a security incident is generated by a policy in which the response action is stored. Box: Quarantine User Files—Response action specific to the Box platform that places files that violate a policy in a quarantine state (as defined by Box). Delay Next—Response action that adds a delay between a set of response actions in a workflow. A use case can be delaying a response action that restricts sharing or changes file ownership to give the current document owner an opportunity to correct the policy violation. Incident Status Update—Response action that updates the status of an incident (for example, from New to Resolved) when previous response actions have automatically mitigated the policy violation. Send Admin Notification—Response action that sends an email to designated administrators informing them of a security incident generated by a DLP policy scanning content stored in a customer's cloud platform. Send User Notification—Response action that sends an email to the user account(s) owning files containing content that triggered a security incident generated by a DLP policy scanning content stored in a customer's cloud platform.

## revert

Return to a previous state. In most cases, this action is a willful initiation and not the outcome of a failed process.

## RMA (return material authorization)

The Cisco program for returning faulty hardware and obtaining a replacement.

## roaming client

Umbrella product that when installed lets you work off-network and yet still remain protected by Umbrella

## roaming computer

A computer onto which the Umbrella roaming client is installed.

## role (Stealthwatch Cloud)

Assigned to entities, representing one task or set of tasks for what an endpoint does. More than 1 can be assigned to a given endpoint, as they are not exclusive or 1:1 relationship.

## rollback

Restore (device, setup, system, database, and so on) to a previously defined state. In most cases, this action is for returning to a stable state as a fallback mechanism due to a failed process. For instance, in Firepower, a software upgrade rollback is the process of restoring a device to its previous software version.

## routed firewall mode

In routed firewall mode, the ASA is counted as a router hop in the network. It performs NAT between connected networks and can use OSPF or RIP.

## routed interface

An interface that routes traffic in a Layer 3 deployment. You can set up physical routed interfaces for handling untagged VLAN traffic, and logical routed interfaces for handling traffic with designated VLAN tags. You can also add static Address Resolution Protocol (ARP) entries to routed interfaces.

## routing policy

Directs web traffic through upstream proxies or directs it to destination servers. You might want to redirect traffic through upstream proxies to preserve your existing network design, to off-load processing from the WSA, or to leverage additional functionality provided by 3rd-party proxy systems. If multiple upstream proxies are available, the WSA can use load balancing techniques to distribute data to them.

## RU (rack unit)

A rack is measured in rack units. An RU is equal to 44 mm or 1.75 inches.

## rule

A configuration of conditions or criteria and the action taken as a result of meeting those criteria.

## rule preemption

Rule preemption occurs when a rule in a security policy will never match traffic because a rule earlier in the evaluation order matches the traffic first.

## rule set

A way to group rules with a logical name to organize the rules.

## SAML (Security Assertion Markup Language)

Products Any Usage GUI—Do not expand. Docs—Expand on first use.

## sample

A sample is an example of possible malware. It may be a type of file, a URL, or even a file-like object, such as a process running in memory. Samples are submitted for malware analysis.

## SAS (Serial Attached SCSI)

Products Hardware Usage Do not expand.

## SATA (Serial Advanced Technology Attachment)

Connects the host bus adapters to mass storage devices such as hard disk drives, optical drives, and SSDs.

## SBRS (SenderBase Reputation Score)

A numeric value assigned to an IP address based on information received from the SenderBase Reputation Service.

## SCEP (Simple Certificate Enrollment Protocol)

Protocol used for client enrollment and other PKI operations. An encrypted certificate issued by a certificate authority provides unalterable confirmation of the server identity. You can request a certificate from any certificate authority and upload that custom certificate to your appliance.

## SCSI (Small Computer System Interface)

Products Hardware Usage Do not expand.

## seat

An internet-connected user who may have access to the service. Equivalent to a user of a service.

## secret key

A key shared only between the sender and receiver.

## SecureRank

An algorithmic classifier based on graph theory that effectively finds domains guilty by association. It creates a large bipartite graph of the internet, and examines where known compromised systems are going, as well as other systems that are hitting malicious locations. Then this classifier finds other common locations that those systems are visiting and determines those locations that are malicious. This classifier ranks the security risks of all domain names by applying an iterative process similar to Google’s PageRank algorithm.

## security appliance

Usage See 'appliance.'

## security certifications compliance

Compliance with security standards established by organizations such as the U.S. Department of Defense and other global certification organizations.

## security context (ASA)

You can partition a single ASA into multiple virtual devices known as security contexts. Each context is an independent device with its own security policy, interfaces, and administrators. Multiple contexts are similar to having multiple standalone devices. Many features are supported in multiple context mode, including routing tables, firewall features, IPS, and management.

## security context (Threat Response)

Information about the assets, data policy, and customer environment. For example: Where was the observable seen in the environment? What value are the assets involved? What's the policy regarding priority?

## security event

The algorithm Stealthwatch uses that looks for specific behavior and can alert on that behavior on your network. It does this by directly generating a host alarm (if set to do so), or by assigning index points to alarm categories that can in turn trigger a host alarm. A security event can indicate a security breach, a misconfigured device, malfunctioning server, or other source of networking issues. Every time that behavior is seen on your network, the number of index points increases.

## security policy

A description of security requirements that define access to corporate assets. A security policy is implemented by creating things like rules and filters that evaluate traffic and allow or block access to resources. A security policy is not an object or a feature that is enabled or created. There can be different kinds of security policies. For example, Firepower considers these types of policies security policies: access control identity policies intrusion policies security intelligence In addition, the ASA considers these actions aspects of a security policy: applying application inspection applying HTTP/HTTPS/FTP filtering enabling threat detection protecting from IP fragments

## sender group

A list of senders gathered together for the purpose of handling email from those senders in the same way, such as applying a mail flow policy to a group of senders. In a sender group, the senders (identified by IP address, IP range, host/domain, SenderBase Reputation Service classification, SenderBase Reputation score range, or DNS List query response) are separated by commas in a listener’s Host Access Table (HAT).

## sensing interface

The interface on the appliance that monitors the chosen network segment. The sensing interface is in promiscuous mode; it has no IP address and is not visible on the monitored segment.

## sensor

Analyzes network traffic by searching for signs of unauthorized activity.

## sensor (Threat Response)

A process or device which observes activity on a network or endpoint and generates events, alerts, or other data flows. Examples include a NetFlow-generating router or an AMP for Endpoints connector.

## serial number onboarding

Refers to the process of onboarding an FTD by using its serial number, which has already been installed and set up. Could also be onboarding with a serial number. The goal is not to rigidly define this term but point out that this process is different from low-touch provisioning.

## server certificate

An encrypted certificate issued by a certificate authority that provides unalterable confirmation of the server identity. You can request a certificate from any certificate authority and upload that custom certificate to your appliance.

## service

The object or function which can be manipulated using the REST API. These are presented to the user as a URL, sometimes with other options within the URL.

## service policy

A service policy consists of multiple actions or rules applied to an interface or applied globally. Use service policies to apply advanced services to the traffic you are allowing. Any traffic permitted by access rules can have service policies applied, and thus receive special processing, such as being redirected to a service module or having application inspection applied. Features configured with service policies: https://www.cisco.com/c/en/us/td/docs/security/asa/asa98/configuration/firewall/asa-98-firewall-config/inspect-service-policy.html#ID-2094-0000007b

## SFP transceiver (small form-factor pluggable)

A fiber optic transceiver that adapts optical cabling to fiber interfaces.

## SHA-256

SHA-256 value or hash.

## shared secret

A piece of data known only to the parties involved in a secure communication. The shared secret can be a password, a passphrase, a big number, or an array of randomly chosen bytes.

## sighting

Detection of an observable within my environment (on network). For example, a data object encoding an event, alert, or observed behavior that is security-significant, and a limited set of information about the context of the observation. See also 'encounter.'

## sinkhole

A server that gives out false DNS responses so that the domain requested cannot be reached. Often used to block botnets from connecting to their command-and-control servers.

## slave

Usage Do not use. Instead, use 'backup,' 'secondary,' 'standby,' or 'subordinate,' contextually. For example, when 2 units are operating in failover mode with each other, instead of 'master' and 'slave,' use 'primary' and 'secondary.' However, in ASA VPN load balancing, do not use 'backup' (and 'master'). Instead, use 'member' (and 'director').

## SmartCache

Makes websites that are effectively down for others accessible only on Umbrella. SmartCache uses the intelligence of the Umbrella network at large, providing DNS service to tens of millions of people around the world, to locate the last known correct address for a website when its authoritative name server is offline or otherwise failing.

## SN (serial number)

Part of the UDI. The SN is the serial number of your Cisco product.

## Snort

Firepower's access control and intrusion inspection engine. Includes (but is not limited to) Security Intelligence, application control, URL filtering, user control, file control and device-side AMP for Networks, intrusion inspection, and SSL decryption/reencryption.

## SOCKS policy

Allows or blocks SOCKS (Socket Secure) communication requests.

## software agent

For instance, in Cisco Tetration, a software agent is a small software application running on a host system. Its core functionality is to monitor and collect network flow information.

## SOL (Serial Over LAN)

Mechanism that enables the input and output of the serial port of a managed system to be redirected over IP.

## spam quarantine

Provides a safeguard mechanism for organizations that are concerned about false positives. Quarantines legitimate email messages that the SMA has deemed to be spam.

## SPAN (Switched Port Analyzer)

Feature of the Catalyst 5000 switch that extends the monitoring abilities of existing network analyzers into a switched Ethernet environment. SPAN mirrors the traffic at one switched segment onto a predefined SPAN port. A network analyzer attached to the SPAN port can monitor traffic from any other Catalyst switched port.

## SPRank

A detection model that uses mathematical concepts more commonly used to analyze sound waves in real time. Instead of sound waves, the model tracks patterns in network traffic, "listening" for categorized malicious patterns.

## SSD (Solid State Drive)

Products Hardware Usage Do not expand.

## SSL (Secure Sockets Layer) decryption

Some protocols, such as HTTPS, use Secure Sockets Layer (SSL) or its successor, Transport Layer Security (TLS), to encrypt traffic for secure transmissions. Undesirable traffic can be hidden within encrypted connections. Because the system cannot inspect encrypted connections, you must decrypt them if you want to apply access rules that consider higher-layer traffic characteristics to make access decisions. SSL decryption can decrypt connections, inspect them to ensure that they do not contain threats or other undesirable traffic, and then re-encrypt them before allowing the connection to proceed. The decrypted traffic goes through your access control policy and matches rules based on inspected characteristics of the decrypted connection, not on the encrypted characteristics.

## SSP (Security Services Processor)

Products Hardware Usage Expand on first use to differentiate from other uses.

## stack, stacked

A feature that lets you increase the amount of traffic inspected on a network segment by connecting 2 to 4 physical devices in a stacked configuration. When you establish a stacked configuration, you combine the resources of each stacked device into a single, shared configuration.

## standard ACL (ASA)

An ACL that identifies traffic by destination address only. There are few features that use them: route maps and VPN filters. Because VPN filters also allow extended access lists, limit standard ACL use to route maps.

## standard ACL (Cisco IOS)

Filters traffic (performs access control) by source address only. Contrast with standard ACLs in ASA, which are primarily for matching traffic in features other than access control. When it comes to access control, IOS and ASA are fundamentally very different.

## static analysis

The basic analysis of the sample submission as a file, including file type, metadata, its contents, attachments, and so on.

## static NAT

Creates a fixed translation of a real address to a mapped address. Because the mapped address is the same for each consecutive connection, static NAT allows bidirectional connection initiation, both to and from the host (if an access rule exists that allows it).

## Stealthwatch Cloud Sensor

The deployed software that connects to Stealthwatch Cloud and submits log and other data from your local network.

## Stealthwatch Management Console

Aggregates, organizes, and presents analysis from up to 25 Flow Collectors, the Cisco Identity Services Engine, and other sources. This interface uses graphical representations of network traffic, identity information, customized summary reports, and integrated security and network intelligence for comprehensive analysis. The capacity of the console determines the volume of telemetry data that can be analyzed and presented, as well as the number of Flow Collectors that are deployed. The console is available as a hardware or virtual machine.

## STIX (Structured Threat Information eXpression)

The industry standard, structured language to represent cyber threat information.

## submission

A sample of suspected malware that has been submitted (uploaded) for analysis.

## support mode

A live support session that gives Threat Grid appliance support engineers remote access to an appliance or account.

## suspicious

A verdict that indicates the subject should be examined thoroughly because it contains logic that must be emulated, or there are anomalies that suggest some sort of obfuscation or malicious intent.

## system

A set of things working together as parts of a mechanism or an interconnecting network; a complex whole.

## TAC (Cisco Technical Assistance Center)

There are 4 centers worldwide providing technical assistance to Cisco customers.

## TACACS+ (Terminal Access Controller Access Control System Plus)

Proprietary Cisco enhancement to Terminal Access Controller Access Control System (TACACS). Provides additional support for authentication, authorization, and accounting.

## Talos (Cisco Talos Intelligence Group)

The Talos team protects customers' people, data, and infrastructure. Researchers, data scientists, and engineers collect information about existing and developing threats. They then deliver protection against attacks and malware. For more information, see https://talosintelligence.com/ .

## Talos Threat Level

Talos reputation verdict scores are referred to with Talos Threat Levels in integration documentation and on TalosIntelligence.com. CTR and SSE-Eventing both use Talos Web Reputation, and all Talos consumers should align with the same terminology and score ranges for consistency across the Cisco security product portfolio.

## target (Threat Response)

Any device, user, identity, asset, or resource which is infected, compromised, or impacted by a threat. A target is identified by one or more observables. Targets are always part of a sighting.

## target index

Tracks hosts that appear to be victims of the suspicious behavior of other hosts. Every time a Stealthwatch Flow Collector sees that a host is the target of suspicious behavior, it adds points to the target index for that host. When the number of points exceeds 100% of the acceptable threshold for that host, the Flow Collector generates a High Target Index alarm, alerting you to the possibility that the host is under attack. See also 'alarm.'

## TAXII (Trusted Automated eXchange of Indicator Information)

Defines a set of specifications to exchange cyber threat information using services (TAXII servers) across different organizations or product lines.

## threat actor

Individuals, groups, or organizations believed to be operating with malicious intent. A threat actor is not an intrusion set, but may support or be affiliated with various intrusion sets, groups, or organizations over time.

## threat hunting

The process of proactively and iteratively searching the network to detect and isolate advanced threats that may have evaded your existing security solutions. For more information, see https://www.threathunting.net/reading-list .

## threat intelligence

What threat information becomes once it has been collected, analyzed, and evaluated in the context of its source and reliability.

## threat root cause

The parent file or application that allowed a threat onto an endpoint. An example of a threat root cause is the vulnerable application that was exploited and allowed the threat to be downloaded and executed on the endpoint.

## threat score

A measure of the amount of system weakening, obfuscation, persistence, modification, data exfiltration, and other behaviors discovered during sample analysis, that may be a threat to the host system's integrity. It is intended as an overall threat indicator--a triage metric--that can be used as a guide to the likelihood that a submission is malicious. 'Look at this first.' The threat score can range from 0 - 100. It is not an authoritative classification of good and bad software; for that we use allowed lists.

## TLS (Transport Layer Security) decryption

By default, the Firepower system cannot inspect traffic encrypted with the Secure Socket Layer (SSL) protocol or its successor, the Transport Layer Security (TLS) protocol. TLS/SSL decryption and inspection enables you to either block encrypted traffic without inspecting it, or inspect encrypted or decrypted traffic with access control. The combination of inspecting encrypted traffic and analyzing encrypted session data allows greater awareness and control of the encrypted traffic in your network.

## trajectory

The course of actions a threat takes on an endpoint or across a network. An example of a trajectory is when Threat A exploits a vulnerability, downloads files X, Y, and Z, executes files X, Y, and Z, and then copies itself to all network shares.

## transparent firewall mode

A mode in which the ASA is not a router hop. You can use transparent firewall mode to simplify your network configuration or to make the ASA invisible to attackers. You can also use transparent firewall mode to allow traffic through that would otherwise be blocked in routed firewall mode.

## transparent inline mode

An advanced inline set option that lets a device act as a bump in the wire and forward all the network traffic it sees regardless of its source and destination.

## trust (rule action)

A rule action that allows matching traffic to pass without further deep inspection, while still being subject to limited further handling. For example, traffic that is trusted by a Firepower access control rule is still subject to identity requirements and rate limiting (QoS), but is not subject to network discovery, intrusion inspection, and malware inspection. Contrast 'trust' with the 'fastpath' action, which exempts matching traffic from all further inspection and control.

## trusted certificate

Certificate upon which a certificate user relies as being valid without the need for validation testing; especially a public-key certificate that is used to provide the first public key in a certification path.

## trusted key

Public key upon which a user relies; especially a public key that can be used as the first public key in a certification path.

## trusted server validation

The process of analyzing and validating a server's certificate chain sent in an authentication exchange, such as TLS. The client validates that the server's certificate was issued by a trusted CA and also validates the name of the server contained in the certificate (as compared to the DNS name used to connect), the certificate purpose, key usages, and dates of validity.

## two-factor authentication (2FA)

Strengthens access security by requiring two different methods (also referred to as factors) to verify your identity. These factors can include something you know (username and password), something you are (fingerprint), or something you have (secondary trusted device like a smartphone app or token to approve authentication requests). Compare with two-step verification, which can use the same type of information delivered by different sources. For example, a password you know plus a code you're sent over SMS.

## two-step authentication

A method of confirming a user's claimed identity by utilizing something they know (password) and a second step other than something they have or something they are. An example of a second step is the user repeating back something that was sent to them through an out-of-band mechanism.

## two-step verification

A method used to prove one’s identity by entering 2 different components, something one knows and something one possesses. Most often, two-step verification is a password plus a unique and randomly generated string of numbers sent to the user.

## UDI (Unique Device Identifier)

Provides a unique identity for every Cisco product. The UDI is composed of the PID, VID, and SN. The UDI is stored in the Cisco IPS ID PROM.

## UDP Director

A physical or virtual device that allows NetFlow data to be sent transparently to multiple collection points, such as network management solutions.

## Umbrella Threat Intelligence

Automates detection of both known and emergent threats. Umbrella threat intelligence analyzes a cross section of the world’s internet activity to observe infrastructure being staged. It is a tool built by Cisco Umbrella security researchers that allows us to block sites that are going to host malware, bot networks, and phishing, before they actually become malicious. It is Umbrella technology that automates protection against both known and emergent threats before an attack is launched.

## unit

A device that has been enabled for high availability.

## update

A change that provides new information for use by a product, but that does not change functionality. For example, you can update rules, reputation data, vulnerabilities, geolocation information, and so on. Contrast with 'upgrade' and 'patch.'

## upgrade

A change that introduces new features and functionality, changes behavior, fixes bugs, or otherwise improves a product. Upgrades are usually associated with a change in version number. See also 'patch.' Contrast with 'update.'

## URL categories

URL categories are predefined or custom categories of websites, such as News, Business, Social Media, and so on. These can be used to identify or apply actions to web requests.

## USB (Universal Serial Bus)

USB Type A USB Type B USB Type C USB Mini B USB Micro B USB 3.0 Type B

## user emulation playbook

A predefined set of user actions that may be selected when submitting a sample, which is performed automatically during analysis as if a user were present and operating the keyboard and mouse, for example, mouse movements, clicking mouse buttons, entering data, or opening a browser. If the sample submission is looking for user actions that are defined in the selected playbook, then those requirements are fulfilled and the sample continues its execution.

## user EXEC mode

User EXEC mode lets you see the ASA settings.

## USGv6 (U.S. Government Compliance for IPv6)

The U.S. Government Compliance for IPv6 (USGv6) indicates that it is compliant to U.S. government profiles for products that implement IPv6.

## verdict

The most current, unexpired judgement with the highest priority for an observable. A verdict is chosen from among the unexpired judgements for a particular observable. The judgement with the highest priority becomes the active verdict. If there is more than one judgement with that priority, then they are prioritized as follows: a 'clean' disposition has priority over all others, 'malicious' is next, and so on down to 'unknown.'

## VID (version identifier)

Part of the UDI.

## virtual appliance

Created by the installation of a software appliance on a virtual machine. Packaged into an image file, a virtual appliance consists of a pre-configured operating system environment and an application. The purpose of a virtual appliance is to simplify delivery and operation of an application. Virtual appliances are a subset of the broader class of software appliances.

## virtual device

While it exists only in software form, a virtual device can mimic a physical hardware device. In UNIX, a virtual device is a file that is treated as a device, although it is generated by the kernel without reference to hardware.

## virtual machine

A virtual machine is an operating system or application that is installed on software, which imitates dedicated hardware. An emulation of a computer system, virtual machines are based on computer architectures and provide the functionality of a physical computer.

## visibility

The level of access a user has to the contents of a sample analysis report. It is based on the privacy setting of the sample, and the organization membership of the submitting user and the viewing user. Full visibility grants users full access to the sample and the analysis results. Users with no visibility have no access. Partial visibility grants access to reports that have been scrubbed of sensitive, identifying information.

## VPC (Virtual Private Cloud)

Similar to NetFlow, it allows the service to monitor AWS environments without the need for a software agent.

## VPN load balancing

A mechanism for equitably distributing remote-access VPN traffic among the devices in a VPN load-balancing group. It's based on simple distribution of traffic without taking into account throughput or other factors. A VPN load-balancing group consists of two or more devices. One device is the director, and the other devices are member devices. Group devices do not need to be of the exact same type, or have identical software versions or configurations. All active devices in a VPN load-balancing group carry session loads. VPN load balancing directs traffic to the least-loaded device in the group, distributing the load among all devices. It makes efficient use of system resources and provides increased performance and high availability.

## VPN local policy

Specifies security authorizations with update policy settings when AnyConnect is installed manually or deployed to a device using an enterprise software development system.

## VSA (vendor-specific attribute)

An attribute in a RADIUS packet that is defined by a vendor rather than by RADIUS RFCs. The RADIUS protocol uses IANA-assigned vendor numbers to help identify VSAs. This lets different vendors have VSAs of the same number. The combination of a vendor number and a VSA number makes a VSA unique. For example, the cisco-av-pair VSA is attribute 1 in the set of VSAs related to vendor number 9. Each vendor can define up to 256 VSAs. A RADIUS packet contains any VSAs attribute 26, named Vendor-specific. VSAs are sometimes referred to as subattributes.

## warn (policy action)

In the WSA access policy, the warn action displays a notification to the end user, who may then choose to click through to continue.

## WBRS (Web-Based Reputation Score)

Web Reputation Filters assign a Web-Based Reputation Score (WBRS) to a URL to determine the likelihood that it contains URL-based malware. This granular score of -10 to +10 offers increased flexibility, since different security policies can be implemented based on different scoring ranges. The WSA uses WBRS to identify and stop malware attacks before they occur.

## WCCP (Web Cache Communication Protocol)

Transparently redirects selected types of traffic to a group of web cache engines to optimize resource usage and lower response times.

## WCCP (Web Cache Communication Protocol) service

An appliance configuration that defines a service group to a WCCP v2 router. It includes information such as the service ID and ports used. Service groups allow a web proxy to establish connectivity with a WCCP router and to handle redirected traffic from the router.

## Web Reputation Filters

Web Reputation Filters analyze web server behavior and assign a Web-Based Reputation Score to a URL to determine the likelihood that it contains URL-based malware.

## webtype ACL

An ACL used for filtering clientless SSL VPN traffic. These ACLs can deny access based on URLs or destination addresses.

## whitelist

Usage Do not use. Instead, standardize use around 'allow list' (to mean a list that allows). In cases where it makes more sense, it's okay to use 'allowed list' (to mean a list of allowed items).

## XAUTH (extended authentication)

Provides the capability of authenticating a user within IKE using TACACS+ or RADIUS. Authenticates a user using RADIUS or any of the other supported user authentication protocols. The XAUTH username and password parameters are used when secure unit authentication is disabled and the server requests XAUTH credentials.

## xlate

Also referred to as a translation entry, an xlate represents the mapping of 1 IP address to another, or the mapping of 1 IP address and port pair to another.

