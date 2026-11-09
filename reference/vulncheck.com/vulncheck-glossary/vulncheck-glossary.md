# VulnCheck Exploit Intelligence Glossary

Source: https://docs.vulncheck.com/kb

License: LicenseRef-Vendor-Copyright (VulnCheck Inc.; internal CSA use only — not redistributable).

Extracted: 42 terms.

---

## Active C2 Servers

Active C2 servers refers to actively-responsive and recently detected attacker infrastructure used for command and control (C2).

## Advanced Persistent Threat (APT)

A type of threat actor, often with a name (e.g., "Comment Crew") or other form of unique identifier (e.g., a MITRE identifier such as "G0006" or a MISP identifier such as "1cb7e1cc-d695-42b1-92f4-fd0112a3c9be").

## Attacker Infrastructure

Attacker Infrastructure refers to the many software components attackers use to execute attacks and maintain access. Examples include C2 servers, relays, and proxies.

## Botnet

A collection of computers that have been infected and controlled by a common attacker.

## Command and Control (C2 or C&C) Infrastructure

Attacker network infrastructure, typically previously compromised infrastructure (servers and applications), used to command and control downstream infrastructure.

## Common Vulnerabilities and Exposures (CVE)

A standard for assessing the severity of software vulnerabilities, which assigns a score from 0.0 to 10.0 based on the vulnerability's characteristics.

## Common Vulnerability Scoring System (CVSS)

A standard for assessing the severity of software vulnerabilities, which assigns a score from 0.0 to 10.0 based on the vulnerability's characteristics.

## Cybersecurity Supply Chain Risk Management (C-SCRM)

Defined by NIST SP 800-161 publication as a "systematic process for managing exposure to cybersecurity risks through the supply chain and developing appropriate response strategies, policies, processes, and procedures." One such process is the generation of SBOM for a software product, performing a security analysis on the resulting data, remediating any found vulnerabilities, and repeating those steps to verify that the remediation occurred as a part of a SSDLC.

## CycloneDX

A Bill of Materials (BOM) standard developed by OWASP that supports the inclusion of software, hardware, machine learning, operations, and other BOM types, as well as additional information such as VDR and VEX data, in order to aid understanding the contents and relationships between system components. Serialization formats include both JSON and XML.

## Dependency Graph

A graph depicting the hierarchy of software dependencies for a given package or software component.

## Exploit Availability

A field used to denote whether an exploit is publicly available, commercially available, or reported to be privately available.

## Exploit Chain

When two or more vulnerabilities are used together to achieve more access on the target, than if each vulnerability was independently exploited, without exploiting other vulnerabilities.

## Exploit Intelligence

A field used to distinguish the maturity of a given exploit. The values range from (no known public exploit exists) to proof of concept (PoC) to weaponized exploit.

## Exploit Maturity

A field used to distinguish the maturity of a given exploit. The values range from (no known public exploit exists) to proof of concept (PoC) to weaponized exploit.

## Exploit Proof of Concept (PoC)

An exploit which may not work against the majority of targets, which is likely distributed as a one-off, to demonstrate triggering the vulnerability.

## Implant

Malicious software that provides advanced features like persistence, file and process hiding, and network communication obfuscation.

## Initial Access Exploit

A proof of concept exploit that demonstrates remote code execution on the target, remotely via a network-bound application/port.

## Initial Access Vulnerability

Initial Access vulnerabilities are those vulnerabilities, which may be exploited remotely and result in code execution. In contract to Remote Code Execution vulnerabilities, which have come to include vulnerabilities that may be exploited client-side, initial access vulnerabilities are almost exclusively exploited over the network, remotely, without user interaction.

## IP Fingerprinting

A method of detecting C2 infrastructure on IPv4 and IPv6 networks.

## Named Threat Actor

A specified threat actor with a name or identifier, see also: Advanced Persistent Threat (APT). Meant to be distinguished against reports of generic exploitation in the wild, see also: Reported Exploited In-The-Wild (ITW).

## Open Directory

An HTTP server configured to allow directory listings that is sometimes used by attackers to host malware.

## Package URL (purl)

A method of encoding a software package, its version, and where it was sourced from (e.g., "pkg:pypi/aioxmpp@0.6.0").

## Potentially Vulnerable Servers

Servers or otherwise network-facing applications that show some indication of potentially being vulnerable to a known vulnerability (N-day), but which when interacted with directly, may actually not be vulnerable.

## Proxy

A computer that acts as an intermediary between two or more computers.

## Relay (Redirector)

A relay, sometimes referred to as a redirector, is a proxy placed in front of the attacker's C2 infrastructure in order to hide where C2 communications are terminated.

## Remote Code Execution (RCE) Exploit

A proof of concept exploit that demonstrates remote code execution on the target.

## Remote Code Execution (RCE) Vulnerability

Remote Code Execution vulnerabilities are those vulnerabilities, which may be exploited remotely and result in code execution. Originally, remote code execution vulnerabilities were exploitable over the network, via an application bound to a port. Over time, remote code execution vulnerabilities have come to include client-side vulnerabilities, where an attacker sends document to the remote party.

## Reported Exploited by Threat Actors

A boolean value set to true if one or more named threat actors (specific threat actors) have been reported in industry publications to have exploit that specific vulnerability in-the-wild (ITW).

## Reported Exploited In-The-Wild (ITW)

A boolean value set to true if one or more of the following example conditions are true: if a CISA Alert has been issued on the vulnerability with reports of exploitation in-the-wild; if Google Project Zero's 0day In-The-Wild (ITW) list is reporting exploitation in-the-wild; or if named threat actors have been publicly reported to have exploited the vulnerability in-the-wild.

## Secure Software Development Lifecycle (SSDLC)

The set of methods and processes for developing secure software as part of the overall software development lifecycle (SDLC). This can include, but is not limited to, iterative scanning of developed software for security vulnerabilities, remediating them, and scanning to ensure they were fixed.

## Software Bill of Materials (SBOM)

An artifact, typically a JSON or XML file, expressed in CycloneDX or SPDX format, which contains metadata associated with delivered software, including the dependencies included in that software.

## Software Dependency Graphs

A graph depicting the hierarchy of software dependencies for a given package or software component.

## Software Identification (SWID) Tag

A structured metadata format for describing a software product that is defined by the ISO/IEC 19770-2 published standard in order to aid asset and information security management. There are tag types that represent certain states of the software lifecycle and each will provide different information based on this type. Some common information is the product name, version, and a (proxy) tag identifier. A given tag document will be in XML format.

## Software Package Data Exchange (SPDX) blog/vulnerability-exchange-formats#software-package-data-exchange-spdx-a-flexible-and-open-sbom-standard

An international open standard (ISO/IEC 5962:2021) for supporting the communication of SBOM information in order to aid in security, license compliance, and other software supply chain use cases. Serialization formats include JSON, RDF/XML, tag-value, and YAML.

## Software Supply Chain Security

The set of methods and processes for securing the software supply chain, including the software development lifecycle (SSDLC), software bill of materials (SBOM), and vulnerability management.

## Understanding Exploits

A non-specific threat actor, not currently associated with a name, identifier, or country; see also: Advanced Persistent Threat (APT).

## Unnamed Threat Actor

A non-specific threat actor, not currently associated with a name, identifier, or country; see also: Advanced Persistent Threat (APT).

## Vulnerability Alias

A name assigned to a vulnerability, by a vendor or security researcher, such as Log4Shell or URGENT/11.

## Vulnerability Disclosure Report (VDR)

A vendor produced document that discloses vulnerabilities in products and services. Both the ISO/IEC 29147:2018 international open standard and NIST SP 800-161 publication provide guidance on handling receiving reports of vulnerabilities, disclosing remediation actions, and other aspects of responsible vulnerability handling to reduce users' risk.

## Vulnerability Exploitability eXchange (VEX)

A format developed by the National Telecommunications and Information Administration (NTIA) for the purpose of providing users additional information on whether an included component in a product is impacted by a specific vulnerability and justification for this statement. Additionally, the standard provides the ability to include recommended steps for remediation, if any exist. The primary use case is for inclusion in SBOMs in order to help avoid spending time on non-exploitable vulnerabilities, but it is not the only use case.

## Weaponized Exploit

An exploit which is either explicitly malicious, such as cases where the exploit is contained within malware (e.g., a malicious Microsoft Word document) or has been reported as exploited in the wild, or cases where the exploit facilitates "point & click" exploitation (e.g., works against all or most targets and works reliably -- such as exploits in MetaSploit, CANVAS, or Core Impact). Additionally, weaponized exploits typically have secondary payloads, droppers, or implants.

## Web Shell

A malicious file uploaded to a victim HTTP server. Accessing the file allows the attacker to execute arbitrary code on the victim server.

