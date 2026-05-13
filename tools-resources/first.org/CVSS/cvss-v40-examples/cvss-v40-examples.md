![](_page_0_Picture_0.jpeg)

![](_page_0_Picture_1.jpeg)

# Common Vulnerability Scoring System version 4.0 Examples

Document Version: 1.4.1

The Common Vulnerability Scoring System (CVSS) is an open framework for communicating the characteristics and severity of software vulnerabilities. CVSS consists of four metric groups: Base, Threat, Environmental, and Supplemental. The Base group represents the intrinsic qualities of a vulnerability that are constant over time and across user environments, the Threat group reflects the characteristics of a vulnerability that change over time, and the Environmental group represents the characteristics of a vulnerability that are unique to a user's environment. Base metric values are combined with default values that assume the highest severity for Threat and Environmental metrics to produce a score ranging from 0 to 10. To further refine a resulting severity score, Threat and Environmental metrics can then be amended based on applicable threat intelligence and environmental considerations. Supplemental metrics do not modify the final score, and are used as additional insight into the characteristics of a vulnerability. A CVSS vector string consists of a compressed textual representation of the values used to derive the score. This document provides the official specification for CVSS version 4.0.

CVSS is owned and managed by FIRST.Org, Inc. (FIRST), a US-based non-profit organization, whose mission is to help computer security incident response teams across the right to update CVSS and this document periodically at its sole discretion. While FIRST owns all right and interest in CVSS, it licenses it to the public freely for use, subject to the conditions below. Membership in FIRST is not required to use or implement CVSS. FIRST does, however, require that any individual or entity using CVSS give proper attribution, where applicable, that CVSS is owned by FIRST and used by permission. Further, FIRST requires as a condition of use that any individual or entity which publishes scores conforms to the guidelines described in this document and provides both the score and the scoring vector so others can understand how the score was derived.

![](_page_1_Picture_0.jpeg)

# Contents

# Resources & Links

Below are useful references to additional CVSS v4.0 documents.

| Resource                           | Location                                                                                                                               |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Specification Document             | Includes metric descriptions, formulas, and vector strings.<br>Available at<br>https://www.first.org/cvss/v4.0/specification-document  |
| User Guide                         | Includes further discussion of CVSS v4.0, a scoring rubric, and a<br>glossary. Available at https://www.first.org/cvss/v4.0/user-guide |
| Examples Document                  | Includes examples of CVSS v4.0 scoring in practice. Available at<br>https://www.first.org/cvss/v4.0/examples                           |
| CVSS v4.0 Calculator               | Reference implementation of the CVSS v4.0 equations, available<br>at https://www.first.org/cvss/calculator/4.0                         |
| JSON & XML Data<br>Representations | Schema definition available at<br>https://www.first.org/cvss/data-representations                                                      |
| CVSS v4.0 Main Page                | Main page for all other CVSS resources:<br>https://www.first.org/cvss/v4-0/                                                            |

![](_page_2_Picture_0.jpeg)

## Introduction

This document demonstrates how to apply the CVSS version 4.0 standard to assess specific vulnerabilities. Every vulnerability example includes a summary and a breakdown of the assessment. CVSS version 3.0 scores are provided to show differences between the two standards.

Details of the vulnerabilities and attacks were sourced primarily from the National Vulnerability Database (NVD) at https://nvd.nist.gov/vuln/search. Information from additional sources was also used when more details were required.

# Common Vulnerability Scoring System version 4.0 Examples

The Common Vulnerability Scoring System (CVSS) is an open framework for communicating the characteristics and severity of software vulnerabilities. CVSS consists of four metric groups: Base, Threat, Environmental, and Supplemental. The Base group represents the intrinsic qualities of a vulnerability that are constant over time and across user environments, the Threat group reflects the characteristics of a vulnerability that change over time, and the Environmental group represents the characteristics of a vulnerability that are unique to a user's environment. Base metric values are combined with default values that assume the highest severity for Threat and Environmental metrics to produce a score ranging from 0 to 10. To further refine a resulting severity score, Threat and Environmental metrics can then be amended based on applicable threat intelligence and environmental considerations. Supplemental metrics do not modify the final score, and are used as additional insight into the characteristics of a vulnerability. A CVSS vector string consists of a compressed textual representation of the values used to derive the score. This document provides the official specification for CVSS version 4.0.

The most current CVSS resources can be found at https://www.first.org/cvss/

![](_page_3_Picture_0.jpeg)

CVSS is owned and managed by FIRST.Org, Inc. (FIRST), a US-based non-profit organization, whose mission is to help computer security incident response teams across the right to update CVSS and this document periodically at its sole discretion. While FIRST owns all rights and interest in CVSS, it licenses it to the public freely for use, subject to the conditions below. Membership in FIRST is not required to use or implement CVSS. FIRST does, however, require that any individual or entity using CVSS give proper attribution, where applicable, that CVSS is owned by FIRST and used by permission. Further, FIRST requires as a condition of use that any individual or entity which publishes scores conforms to the guidelines described in this document and provides both the score and the scoring vector so others can understand how the score was derived.

# New metric coverage

This section includes scoring examples that illustrate aspects of changed or modified metrics.

## New Metric - Attack Requirements

## CVE-2022-41741

A vulnerability in the module ngx http_mp4_module might allow a local attacker to corrupt NGINX worker memory, resulting in its termination or potential other impact using a specially crafted audio or video file. The attack is only possible if an attacker can gain privileged access to the host running NGINX, place a specially crafted audio or video file within the webroot, and then trigger NGINX to process the specially crafted file.

| v3.1                                               | v4.0 Base                                                           |
|----------------------------------------------------|---------------------------------------------------------------------|
| 7.0                                                | 7.3                                                                 |
| CVSS:3.1/AV:L/AC:H/PR:L/Ul:N/S:U/C:  <br>H/I:H/A:H | CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/<br>SI:N/SA:N |

## CVSS v4 Score: Base 7.3

| Metric        | Value | Comments                                                 |
|---------------|-------|----------------------------------------------------------|
| Attack Vector | Local | An attacker must be able to access the vulnerable system |

![](_page_4_Picture_0.jpeg)

|                                      |         | with a local, interactive session.                                                                                                                                         |
|--------------------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                                                                                           |
| Attack Requirements                  | Present | Multiple conditions that require target specific<br>reconnaissance and preparation must be satisfied in order<br>to achieve successful exploitation of this vulnerability. |
| Privileges Required                  | Low     | An attacker must be able to place a file within the web<br>root to be processed by NGINX.                                                                                  |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                                              |
| Vulnerable System<br>Confidentiality | High    | The attacker could execute arbitrary code on the<br>vulnerable system with elevated privileges.                                                                            |
| Vulnerable System<br>Integrity       | High    | The attacker could execute arbitrary code on the<br>vulnerable system with elevated privileges.                                                                            |
| Vulnerable System<br>Availability    | High    | The attacker could execute arbitrary code on the<br>vulnerable system with elevated privileges.                                                                            |
| Subsequent System<br>Confidentiality | None    | There is no impact to the subsequent system<br>confidentiality.                                                                                                            |
| Subsequent System<br>Integrity       | None    | There is no impact to the subsequent system integrity.                                                                                                                     |
| Subsequent System<br>Availability    | None    | There is no impact to the subsequent system availability.                                                                                                                  |

## CVE-2020-3549

A vulnerability in the sftunnel functionality of Cisco Firepower Management Center (FMC) Software and Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to obtain the device registration hash.

The vulnerability is due to insufficient sftunnel negotiation protection during initial device registration. An attacker in a man-in-the-middle position could exploit this vulnerability by

![](_page_5_Picture_0.jpeg)

intercepting a specific flow of the sftunnel communication between an FMC device and an FTD device. A successful exploit could allow the attacker to decrypt and modify the sftunnel communication between FMC and FTD devices, allowing the attacker to modify configuration data sent from an FMC device to an FTD device or alert data sent from an FTD device to an FMC device.

|               | v3.1                                                    | v4.0                                                                               |
|---------------|---------------------------------------------------------|------------------------------------------------------------------------------------|
| Base          | 8.1<br>CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U<br>/C:H/I:H/A:H | 7.7<br>CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P<br>/VC:H/VI:H/VA:H/SC:N/SI:N/SI:N/SA:N    |
| Base + Threat |                                                         | 5.2<br>CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P<br>/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:<br>U |

## CVSS v4 Score: Base + Threat 5.2

| Metric                               | Value   | Comments                                                                                                           |
|--------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                                          |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                                   |
| Attack Requirements                  | Present | An attacker must be on-path to be able to intercept<br>communications between affected systems.                    |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                           |
| User Interaction                     | Passive | A user must be logged in and using the application for<br>ltraffic to be generated that an attacker could capture. |
| Vulnerable System<br>Confidentiality | High    | An attacker could gain access to the system with a highly<br>privileged user account.                              |
| Vulnerable System<br>Integrity       | High    | An attacker could gain access to the system with a highly<br>privileged user account.                              |

![](_page_6_Picture_0.jpeg)

| Vulnerable System<br>Availability    | High       | An attacker could gain access to the system with a highly<br>privileged user account.       |
|--------------------------------------|------------|---------------------------------------------------------------------------------------------|
| Subsequent System<br>Confidentiality | None       | There is no impact to the vulnerable system confidentiality.                                |
| Subsequent System<br>Integrity       | None       | There is no impact to the vulnerable system integrity.                                      |
| Subsequent System<br>Availability    | None       | There is no impact to the vulnerable system availability.                                   |
| Exploit Maturity                     | Unreported | There is no known proof-of-concept code or malicious<br>exploitation of this vulnerability. |

## CVE-2023-3089

Description: A compliance problem was found in the Red Hat OpenShift Container Platform. Red Hat discovered that, when FIPS mode was enabled, not all of the cryptographic modules in use were FIPS-validated.

|                         | v3.1                                                    | v4.0                                                                                                                                 |
|-------------------------|---------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| Base                    | 7.5<br>CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/<br>C:H/I:N/A:N | 8.3<br>CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:<br>N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N                                                           |
| Base +<br>Environmental |                                                         | 8.1<br>CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:<br>N/VC:H/VI:L/VA:L/SC:N/SI:N/SI:N/SA:N/C<br>R:H/IR:L/AR:L/MAV:N/MAC:H/MVC:<br>H/MVI:L/MVA:L |

## CVSS v4 Score: Base + Environmental 8.1

| Metric<br>Value | Comments |
|-----------------|----------|
|-----------------|----------|

![](_page_7_Picture_0.jpeg)

| Attack Vector                                    | Network | The vulnerable system is accessible from remote networks.                                                                                                            |
|--------------------------------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Complexity                                | Low     | There is no inherent vulnerability, but a lower level of<br>cryptography than expected was being used, resulting in a<br>lower-than-configured certificate security. |
| Attack Requirements                              | Present | Attack requirements are present. Only applications built<br>with a specific configuration are vulnerable.                                                            |
| Privileges Required                              | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                             |
| User Interaction                                 | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                                        |
| Vulnerable System<br>Confidentiality             | High    | This CVE particularly affects high-security systems (FIPS<br>users) and lowers the requirements to access confidential<br>information.                               |
| Vulnerable System<br>Integrity                   | Low     | Integrity will be at a lower cryptographic level than desired,<br>but is still always encrypted.                                                                     |
| Vulnerable System<br>Availability                | Low     | Integrity will be at a lower cryptographic level than desired,<br>but is still always encrypted.                                                                     |
| Subsequent System<br>Confidentiality             | None    | There is no impact to subsequent systems.                                                                                                                            |
| Subsequent System<br>Integrity                   | None    | There is no impact to subsequent systems.                                                                                                                            |
| Subsequent System<br>Availability                | None    | There is no impact to subsequent systems.                                                                                                                            |
| Modified Attack<br>Vector                        | Network | This still requires spoofing a cryptographically secure<br>certificate, just not always an FIPS-approved algorithm.                                                  |
| Modified Attack<br>Complexity                    | High    | This still requires spoofing a cryptographically secure<br>certificate, just not always an FIPS-approved algorithm.                                                  |
| Modified Vulnerable<br>System<br>Confidentiality | High    | This still requires spoofing a cryptographically secure<br>certificate, just not always an FIPS-approved algorithm.                                                  |
| Modified Vulnerable<br>System Integrity          | Low     | Integrity will be at a lower cryptographic level than desired,<br>but is still always encrypted.                                                                     |
| Modified Vulnerable                              | Low     | Integrity will be at a lower cryptographic level than desired,                                                                                                       |

![](_page_8_Picture_0.jpeg)

| System Availability             |      | but is still always encrypted.                                                                                                                                                       |
|---------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Confidentiality<br>Requirements | High | System certificates are still encrypted correctly, but at a<br>weaker level than expected, resulting in a hard-to-abuse<br>system, but easier than intended/designed for the system. |
| Integrity<br>Requirements       | Low  | There is a low chance of integrity being modified, but<br>higher than expected behavior.                                                                                             |
| Availability<br>Requirements    | Low  | There is a low chance of availability being affected, but<br>higher than expected behavior.                                                                                          |

## Revised Metric – User Interaction

Analysts assessing User Interaction should consider the necessary actions taken by a user. As per the specification document, operations normally taken by a user would be User Interaction:Passive. Actions that are out of the ordinary, against recommended guidance, or subverting security controls, would be User Interaction:Active.

## CVE-2021-44714

Acrobat Reader DC version 21.007.20099 (and earlier), 20.004.30017 (and earlier) and 17.011.30204 (and earlier) are affected by a Violation of Secure Design Principles that could lead to a Security feature bypass. Acrobat Reader DC displays a warning message when a user clicks on a PDF file, which could be used by an attacker to mislead the user. In affected versions, this warning message does not include custom protocols when used by the sender. User interaction is required to abuse this vulnerability as they would need to click 'allow' on the warning message of a malicious file.

| v3.1                                               | v4.0 Base                                                           |
|----------------------------------------------------|---------------------------------------------------------------------|
| 3.3                                                | 4.6                                                                 |
| CVSS:3.1/AV:L/AC:L/PR:N/Ul:R/S:U/C:L  <br>/I:N/A:N | CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:L/VI:N/VA:N/SC:N/<br>SI:N/SA:N |

## CVSS v4 Score: Base 4.6

![](_page_9_Picture_0.jpeg)

| Metric                               | Value  | Comments                                                                                                                                                                                         |
|--------------------------------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Local  | The document must be present on the local disk.                                                                                                                                                  |
| Attack Complexity                    | Low    | No specialized conditions or advanced knowledge are<br>required.                                                                                                                                 |
| Attack Requirements                  | None   | No attack requirements are present.                                                                                                                                                              |
| Privileges Required                  | None   | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                                                         |
| User Interaction                     | Active | User interaction is required to abuse this vulnerability<br>because they would need to click allow on the warning<br>message of a malicious file.                                                |
| Vulnerable System<br>Confidentiality | Low    | Warning dialog messages do not contain all information<br>about the document. Important omitted information about<br>the document may allow the attacker to conduct further<br>spoofing attacks. |
| Vulnerable System<br>Integrity       | None   | There is no impact on vulnerable systems.                                                                                                                                                        |
| Vulnerable System<br>Availability    | None   | There is no impact on vulnerable systems.                                                                                                                                                        |
| Subsequent System<br>Confidentiality | None   | There is no impact to subsequent systems.                                                                                                                                                        |
| Subsequent System<br>Integrity       | None   | There is no impact to subsequent systems.                                                                                                                                                        |
| Subsequent System<br>Availability    | None   | There is no impact to subsequent systems.                                                                                                                                                        |

## CVE-2022-21830

Description A blind self XSS vulnerability exists in RocketChat <v1.9 that could allow an attacker to trick a victim pasting malicious code in their chat instance.

![](_page_10_Picture_0.jpeg)

| 6.1      | 5.1                                                                                                        |
|----------|------------------------------------------------------------------------------------------------------------|
| /I:L/A:N | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L   CVSS:4.0/AV:N/AC:L/AT:N/PR:N/Ul:A/VC:N/V1:N/VA:N/SC:L/<br>SI:L/SA:N |

## CVSS v4 Score: Base 5.1

| Metric                               | Value   | Comments                                                                                 |
|--------------------------------------|---------|------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                         |
| Attack Requirements                  | None    | No attack requirements are present.                                                      |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability. |
| User Interaction                     | Active  | The attacker must convince the user to input malicious<br>script into the application.   |
| Vulnerable System<br>Confidentiality | None    | No impact to the vulnerable application.                                                 |
| Vulnerable System<br>Integrity       | None    | No impact to the vulnerable application.                                                 |
| Vulnerable System<br>Availability    | None    | No impact to the vulnerable application.                                                 |
| Subsequent System<br>Confidentiality | Low     | An attacker could read data from the user's browser.                                     |
| Subsequent System<br>Integrity       | Low     | An attacker could modify data in the user's browser.                                     |
| Subsequent System<br>Availability    | None    | No direct availability impact to the user's browser.                                     |

# New Metric – Subsequent Confidentiality, Availability, Integrity

Some examples of subsequent systems include:

![](_page_11_Picture_0.jpeg)

- Guest host in a VMM hypervisor ●
- Device attached to a network gateway ●
- A managed Device ●
	- Including OT / ICS / SCADA equipment

## CVE-2022-22186

Due to an Improper Initialization vulnerability in Junos OS on EX4650 devices, packets received on the em0 but not destined to the device, may be improperly forwarded to an egress interface, instead of being discarded. Such traffic being sent by a client may appear genuine, but is non-standard in nature and should be considered as potentially malicious.

| v3.1                                             | v4.0 Base                                                           |
|--------------------------------------------------|---------------------------------------------------------------------|
| 7.2                                              | 6.9                                                                 |
| CVSS:3.1/AV:N/AC:L/PR:N/Ul:N/S:C/C:<br>L/I:L/A:N | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L<br>/SI:L/SA:N |

## CVSS v4 Score: Base 6.9

| Metric                               | Value   | Comments                                                                                       |
|--------------------------------------|---------|------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                      |
| Attack Complexity                    | Low     | An attacker must be able to access the vulnerable system<br>with a local, interactive session. |
| Attack Requirements                  | None    | No attack requirements are present.                                                            |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.       |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.  |
| Vulnerable System<br>Confidentiality | None    | There is no impact to the vulnerable system confidentiality.                                   |
| Vulnerable System<br>Integrity       | None    | There is no impact to the vulnerable system integrity.                                         |

![](_page_12_Picture_0.jpeg)

| Vulnerable System<br>Availability    | None | There is no impact to the vulnerable system availability.                                                                                             |
|--------------------------------------|------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Subsequent System<br>Confidentiality | Low  | Network traffic or information from restricted hosts may be<br>detected.                                                                              |
| Subsequent System<br>Integrity       | Low  | Network traffic may be sent to an undesired interface,<br>impacting networks and other systems that should be<br>restricted by the vulnerable system. |
| Subsequent System<br>Availability    | None | There is no impact to subsequent systems.                                                                                                             |

## CVE-2023-21989

#### Description

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core). Supported versions that are affected are Prior to 6.1.44 and Prior to 7.0.8. Easily exploitable vulnerability allows high privileged attackers with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox. While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in unauthorized access to critical data or complete access to all Oracle VM VirtualBox accessible data.

| v3.1                                             | v4.0 Base                                                           |
|--------------------------------------------------|---------------------------------------------------------------------|
| 6.0                                              | 5.9                                                                 |
| CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:<br>H/I:N/A:N | CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:N/SC:H<br>/SI:N/SA:N |

## CVSS v4 Score: Base 5.9

| Metric            | Value | Comments                                                                                       |
|-------------------|-------|------------------------------------------------------------------------------------------------|
| Attack Vector     | Local | An attacker must be able to access the vulnerable system<br>with a local, interactive session. |
| Attack Complexity | Low   | No specialized conditions or advanced knowledge are<br>lrequired.                              |

![](_page_13_Picture_0.jpeg)

| Attack Requirements                  | None | No attack requirements are present.                                                                                                |
|--------------------------------------|------|------------------------------------------------------------------------------------------------------------------------------------|
| Privileges Required                  | High | An attacker must have administrative control over a virtual<br>machine within the virtual machine host.                            |
| User Interaction                     | None | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                      |
| Vulnerable System<br>Confidentiality | None | There is no impact to the vulnerable system confidentiality.                                                                       |
| Vulnerable System<br>Integrity       | None | There is no impact to the vulnerable system integrity.                                                                             |
| Vulnerable System<br>Availability    | None | There is no impact to the vulnerable system availability.                                                                          |
| Subsequent System<br>Confidentiality | High | An attacker could exploit this vulnerability to access<br>confidential information stored within the VM host<br>hypervisor system. |
| Subsequent System<br>Integrity       | None | There is no impact to subsequent systems.                                                                                          |
| Subsequent System<br>Availability    | None | There is no impact to subsequent systems.                                                                                          |

## CVE-2020-3947

VMware Workstation (15.x before 15.5.2) and Fusion (11.5.2) contain a use-after vulnerability in vmnetdhcp. Successful exploitation of this issue may lead to code execution on the host from the guest or may allow attackers to create a denial-of-service condition of the vmnetdhcp service running on the host machine.

| v3.1  | v4.0 Base                                                                                                     |
|-------|---------------------------------------------------------------------------------------------------------------|
| 9.3   | 9.4                                                                                                           |
| H/A:H | CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:   CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC<br>:H/SI:H/SA:H |

![](_page_14_Picture_0.jpeg)

## CVSS v4 Score: Base 9.4

| Metric                               | Value                    | Comments                                                                                                   |
|--------------------------------------|--------------------------|------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Local                    | An attacker must be able to access the vulnerable system<br>with a local, interactive session.             |
| Attack Complexity                    | Low                      | No specialized conditions or advanced knowledge are<br>required.                                           |
| Attack Requirements                  | None                     | No attack requirements are present.                                                                        |
| Privileges Required                  | High                     | An attacker must have administrative control over a virtual<br>machine within the virtual machine host.    |
| User Interaction                     | None                     | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.              |
| Vulnerable System<br>Confidentiality | High                     | An attacker could execute arbitrary code on the vulnerable<br>system, the hypervisor host.                 |
| Vulnerable System<br>Integrity       | High                     | An attacker could execute arbitrary code on the vulnerable<br>system, the hypervisor host.                 |
| Vulnerable System<br>Availability    | High                     | An attacker could execute arbitrary code on the vulnerable<br>system, the hypervisor host.                 |
| Subsequent System<br>Confidentiality | High                     | An attacker could take actions on other virtualized guest<br>systems hosted within the virtual hypervisor. |
| Subsequent System<br>Integrity       | High                     | An attacker could take actions on other virtualized guest<br>systems hosted within the virtual hypervisor. |
| Subsequent System<br>Availability    | High                     | An attacker could take actions on other virtualized guest<br>systems hosted within the virtual hypervisor. |
| Exploit Maturity                     | Proof-of-Conc<br>ept (P) | A proof of concept is available                                                                            |

## CVE-2023-48228

#### Description

authentik is an open-source identity provider. When initialising a oauth2 flow with a `code_challenge` and `code_method` (thus requesting PKCE), the single sign-on provider (authentik) must check if there is a matching and existing `code_verifier` during the token step. Prior to versions 2023.10.4 and 2023.8.5, authentik checks if the contents of `code_verifier` is

![](_page_15_Picture_0.jpeg)

matching only when it is provided. When it is left out completely, authentik simply accepts the token request without it; even when the flow was started with a `code_challenge`. authentik 2023.8.5 and 2023.10.4 fix this issue.

| v3.1                                               | v4.0 Base                                                           |
|----------------------------------------------------|---------------------------------------------------------------------|
| 7.5                                                | ರಿ.3                                                                |
| CVSS:3.1/AV:N/AC:L/PR:N/Ul:N/S:U/C:  <br>N/I:H/A:N | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H<br>/SI:H/SA:H |

## CVSS v4 Score: Base 9.4

| Metric                               | Value  | Comments                                                                                                               |
|--------------------------------------|--------|------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Remote | An attacker must be able to send requests to a system<br>using the vulnerable application.                             |
| Attack Complexity                    | Low    | No specialized conditions or advanced knowledge are<br>required.                                                       |
| Attack Requirements                  | None   | No attack requirements are present.                                                                                    |
| Privileges Required                  | None   | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                               |
| User Interaction                     | None   | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                          |
| Vulnerable System<br>Confidentiality | None   | There is no impact to the vulnerable system confidentiality.                                                           |
| Vulnerable System<br>Integrity       | High   | The attacker could cause the application to generate an<br>arbitrary authentication token.                             |
| Vulnerable System<br>Availability    | None   | There is no impact to the vulnerable system availability.                                                              |
| Subsequent System<br>Confidentiality | High   | An attacker could potentially use a token generated by the<br>vulnerable application to gain access to another system. |
| Subsequent System<br>Integrity       | High   | An attacker could potentially use a token generated by the<br>vulnerable application to gain access to another system. |

![](_page_16_Picture_0.jpeg)

| Subsequent System    High |  | iAn attacker could potentially use a token generated by the |
|---------------------------|--|-------------------------------------------------------------|
| Availability              |  | vulnerable application to gain access to another system.    |

## New Metric – Safety

Safety is a Supplemental metric which may be optionally assessed by a scoring provider with values of Not Defined (X), Present (P), or Negligible (N). In the case of a system that intends to have health-related functions, it might also have a Safety-related consequence if a vulnerability is exploited. Let's look at an example.

#### CVE-2023-30560

There are two known configurations of a product known as the Becton Dickinson PCU which can be modified without authentication using physical connection to the PCU. A PCU is commonly used for infusion delivery in a healthcare provider environment. With that context in mind, it could be inferred that an exploit of this vulnerability might have Safety impact. The below is only an example of how this, or a similar vulnerability, could be scored.

| v3.1   | v4.0 Base                                                                                                            |
|--------|----------------------------------------------------------------------------------------------------------------------|
| 6.8    | 8.3                                                                                                                  |
| :H/A:H | CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:U/C:H/I   CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/V/:H/VA:H/S<br>C:N/SI:H/SA:N/S:P/V:D |

#### CVSS v4 Score: Base 8.3

| Metric                     | Value    | Comments                                                         |
|----------------------------|----------|------------------------------------------------------------------|
| Attack Vector              | Physical | An attacker must be able to physically access the system.        |
| Attack Complexity          | Low      | No specialized conditions or advanced knowledge are<br>required. |
| Attack Requirements   None |          | No attack requirements are present.                              |
| Privileges Required        | None     | An attacker is unauthorized prior to the attack.                 |
| User Interaction           | None     | No user interaction is required for an attacker to               |

![](_page_17_Picture_0.jpeg)

|                                      |      | successfully exploit the vulnerability.                                                                                                                        |
|--------------------------------------|------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vulnerable System<br>Confidentiality | High | An attacker could execute arbitrary code on the vulnerable<br>system.                                                                                          |
| Vulnerable System<br>Integrity       | High | An attacker could execute arbitrary code on the vulnerable<br>system.                                                                                          |
| Vulnerable System<br>Availability    | High | An attacker could execute arbitrary code on the vulnerable<br>system.                                                                                          |
| Subsequent System<br>Confidentiality | None | If the scoring provider assumes that a patient is the<br>subsequent system, a successful exploit would not result<br>in loss of confidentiality.               |
| Subsequent System<br>Integrity       | High | If the scoring provider assumes that a patient is the<br>subsequent system, a successful exploit could result in loss<br>of health integrity for that patient. |
| Subsequent System<br>Availability    | None | lf the scoring provider assumes that a patient is the<br>subsequent system, the attribute of availability might be<br>metaphorically ambiguous.                |

## CVSS v4 Supplemental Metrics

| Metric        | Value   | Comments                                                                                                                                             |
|---------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| Safety        | Present | Consequences of exploiting this vulnerability could have a<br>Safety impact that is equal to or worse than "marginal", as<br>described in IEC 61508. |
| Value Density | Diffuse | The system with the vulnerable component is fairly limited<br>in resources.                                                                          |

# CISA KEV Examples

This section will list a rotating sample of CVEs published as part of the CISA KEV list.

## CVE-2025-31324

![](_page_18_Picture_0.jpeg)

### Description

SAP NetWeaver Visual Composer Metadata Uploader is not protected with a proper authorization, allowing unauthenticated agent to upload potentially malicious executable binaries that could severely harm the host system. This could significantly affect the confidentiality, integrity, and availability of the targeted system.

| v3.1                                             | v4.0 Base+Threat                                                        |
|--------------------------------------------------|-------------------------------------------------------------------------|
| 10.0                                             | 10.0                                                                    |
| CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:<br>H/I:H/A:H | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H<br>/SI:H/SA:H/E:A |

## CVSS v4 Score: Base+Threat 10.0

| Metric                               | Value   | Comments                                                                                                           |  |
|--------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------|--|
| Attack Vector                        | Network | An attacker must be able to send network requests to the<br>vulnerable application, possibly from remote networks. |  |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                                   |  |
| Attack Requirements                  | None    | No attack requirements are present.                                                                                |  |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                           |  |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                      |  |
| Vulnerable System<br>Confidentiality | High    | Attackers could upload malicious files to the vulnerable<br>system.                                                |  |
| Vulnerable System<br>Integrity       | High    | Attackers could upload malicious files to the vulnerable<br>system.                                                |  |
| Vulnerable System<br>Availability    | High    | Attackers could upload malicious files to the vulnerable<br>system.                                                |  |
| Subsequent System<br>Confidentiality | High    | Subsequent systems could suffer expanded impacts.                                                                  |  |

![](_page_19_Picture_0.jpeg)

| Subsequent System<br>Integrity    | High     | Subsequent systems could suffer expanded impacts.         |
|-----------------------------------|----------|-----------------------------------------------------------|
| Subsequent System<br>Availability | High     | Subsequent systems could suffer expanded impacts.         |
| Threat                            | Attacked | CISA has reported attempts to exploit this vulnerability. |

# Classic Examples

These were in the previous version and we are carrying them forward to show the change between version 3 and 4.

# OpenSSL Heartbleed Vulnerability (CVE-2014-0160)

## Vulnerability

The (1) TLS and (2) DTLS implementations in OpenSSL 1.0.1 before 1.0.1g do not properly handle Heartbeat Extension packets, which allows remote attackers to obtain sensitive information from process memory via crafted packets that trigger a buffer over-read, as demonstrated by reading private keys, related to d1_both.c and t1_lib.c, aka the Heartbleed bug.

## Attack

A successful attack requires only sending a specially crafted message to a web server running OpenSSL. The attacker constructs a malformed "heartbeat request" with a large field length and small payload size. The vulnerable server does not validate the length of the payload against the provided field length and will return up to 64 kB of server memory to the attacker. It is likely that this memory was previously utilized by OpenSSL. Data returned may contain sensitive information such as encryption keys or user names and passwords that could be used by the attacker to launch further attacks

| v3.1 Base | v3.1 Base + Temporal | v4.0 Base + Threat |
|-----------|----------------------|--------------------|
| 7.5       | 7.0                  | , 8.7              |

![](_page_20_Picture_0.jpeg)

|                   |      | CVSS:3.1/AV:N/AC:L/PR:N/U:   CVSS:3.1/AV:N/AC:L/PR:N/UI:   CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N |
|-------------------|------|----------------------------------------------------------------------------------------------|
| N/S:U/C:H/I:N/A:N | RC:C | N/S:U/C:H/I:N/A:N/E:F/RL:O/   /VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:A                             |
|                   |      |                                                                                              |

## CVSS v4 Score: Base + Threat 8.7

| Metric                               | Value    | Comments                                                                                                                                                                                                                                                                      |
|--------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network  | The vulnerable system is accessible from remote networks.                                                                                                                                                                                                                     |
| Attack Complexity                    | Low      | No specialized conditions or advanced knowledge are<br>required.                                                                                                                                                                                                              |
| Attack Requirements                  | None     | No attack requirements are present.                                                                                                                                                                                                                                           |
| Privileges Required                  | None     | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                                                                                                                                      |
| User Interaction                     | None     | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                                                                                                                                                 |
| Vulnerable System<br>Confidentiality | High     | Access to only some restricted information is obtained, but<br>the disclosed information presents a direct, serious impact<br>to the affected scope (e.g. the attacker can read the<br>administrator's password, or private keys in memory are<br>disclosed to the attacker). |
| Vulnerable System<br>Integrity       | None     | There is no impact to the vulnerable system integrity.                                                                                                                                                                                                                        |
| Vulnerable System<br>Availability    | None     | There is no impact to the vulnerable system availability.                                                                                                                                                                                                                     |
| Subsequent System<br>Confidentiality | None     | There is no impact to subsequent systems.                                                                                                                                                                                                                                     |
| Subsequent System<br>Integrity       | None     | There is no impact to subsequent systems.                                                                                                                                                                                                                                     |
| Subsequent System<br>Availability    | None     | There is no impact to subsequent systems.                                                                                                                                                                                                                                     |
| Exploit Maturity                     | Attacked | There are known exploits in the wild.                                                                                                                                                                                                                                         |

![](_page_21_Picture_0.jpeg)

# Apache log4j JNDI Command Execution "log4shell" Vulnerability (CVE-2021-44228)

A vulnerability in the Apache log4j library could allow an unauthenticated, remote attacker to execute arbitrary commands with the privileges of the service using the vulnerable library.

#### Notes:

 In most circumstances all impacts to this vulnerability are constrained to the vulnerable system using the vulnerable library. This example has been updated to indicate impacts only to the vulnerable system.

| v3.1 Base | v4.0 Base + Threat                                                                                                    |
|-----------|-----------------------------------------------------------------------------------------------------------------------|
| 10.0      | 9.3                                                                                                                   |
|           | CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/1:H/A:H   CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/V:H/V<br>A:H/SC:N/SI:N/SA:N/E:A |

## CVSS v3.1 Base Score: 10.0

| Metric              | Value   | Comments                                                                                         |
|---------------------|---------|--------------------------------------------------------------------------------------------------|
| Attack Vector       | Network | The vulnerability is in a network service that uses log4j.                                       |
| Attack Complexity   | Low     | No conditions outside of the user's control.                                                     |
| Privileges Required | None    | An attacker requires no privileges to mount an attack.                                           |
| User Interaction    | None    | The attacker requires no user interaction to successfully<br>exploit the vulnerability           |
| Scope               | Changed | The vulnerable component could allow an attacker to affect<br>downstream components and systems. |
| Confidentiality     | High    | An attacker can execute arbitrary commands with elevated<br>privileges.                          |
| Integrity           | High    | An attacker can execute arbitrary commands with elevated<br>privileges.                          |
| Availability        | High    | An attacker can execute arbitrary commands with elevated                                         |

![](_page_22_Picture_0.jpeg)

|  |  | privileges. |
|--|--|-------------|
|--|--|-------------|

## CVSS v4 Score: Base + Threat 9.3

| Metric                               | Value    | Comments                                                                                                                                                                                                                           |
|--------------------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network  | The vulnerable system is accessible from remote networks.                                                                                                                                                                          |
| Attack Complexity                    | Low      | No specialized conditions or advanced knowledge are<br>required.                                                                                                                                                                   |
| Attack Requirements                  | None     | Although the attacker must prepare the environment to<br>achieve the worst possible outcome of an attack, (for<br>example, code execution) through control of a reachable<br>LDAP server, the system should be assumed vulnerable. |
| Privileges Required                  | None     | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                                                                                           |
| User Interaction                     | None     | The attack does not require any user interaction.                                                                                                                                                                                  |
| Vulnerable System<br>Confidentiality | High     | The attacker can run arbitrary commands with elevated<br>privileges and access sensitive system information.                                                                                                                       |
| Vulnerable System<br>Integrity       | High     | The attacker can run arbitrary commands with elevated<br>privileges and modify the system configuration.                                                                                                                           |
| Vulnerable System<br>Availability    | High     | The attacker can run arbitrary commands with elevated<br>privileges and gain access sufficient to reset or turn off the<br>device.                                                                                                 |
| Subsequent System<br>Confidentiality | None     | Impacts constrained to the vulnerable system.                                                                                                                                                                                      |
| Subsequent System<br>Integrity       | None     | Impacts constrained to the vulnerable system.                                                                                                                                                                                      |
| Subsequent System<br>Availability    | None     | Impacts constrained to the vulnerable system.                                                                                                                                                                                      |
| Exploit Maturity                     | Attacked | There are known exploits in the wild.                                                                                                                                                                                              |

![](_page_23_Picture_0.jpeg)

# GNU Bourne-Again Shell (Bash) 'Shellshock' Vulnerability (CVE-2014-6271)

## Vulnerability

GNU Bash through 4.3 processes trailing strings after function definitions in the values of environment variables, which allows remote attackers to execute arbitrary code via a crafted environment, as demonstrated by vectors involving the ForceCommand feature in OpenSSH sshd, the mod_cgi and mod_cgid modules in the Apache HTTP Server, scripts executed by unspecified DHCP clients, and other situations in which setting the environment occurs across a privilege boundary from Bash execution, aka "Shellshock."

#### Attack

A successful attack can be launched by an attacker directly against the vulnerable GNU Bash shell, or in certain cases, by an unauthenticated, remote attacker through services either written in GNU Bash or services spawning GNU Bash shells. In the case of an attack against the Apache HTTP Server running dynamic content CGI modules, an attacker can submit a request while providing specially crafted commands as environment variables. These commands will be interpreted by the handler program, the GNU Bash shell, with the privilege of the running HTTPD process. As such, environment variables passed by the attacker could allow installation of software, account enumeration, denial of service, etc. Attacks against other services that have a relationship with the GNU Bash shell are similarly possible.

| v3.1 Base                                          | v4.0 Base + Threat                                                      |
|----------------------------------------------------|-------------------------------------------------------------------------|
| ರಿ.8                                               | ರಿ.3                                                                    |
| CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:  <br>H/I:H/A:H | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N<br>/SI:N/SA:N/E:A |

## CVSS v3.1 Base Score: 9.8

| Metric        | Value   | Comments                                                                           |
|---------------|---------|------------------------------------------------------------------------------------|
| Attack Vector | Network | l The reasonable worst-case scenario is a network attack<br> through a web server. |

![](_page_24_Picture_0.jpeg)

| Attack Complexity   | Low       | An attacker needs only to gain access to a listening service<br>that uses the GNU Bash shell as an interpreter or interact<br>with a GNU Bash shell directly.                                                                                                                                  |
|---------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Privileges Required | None      | The reasonable worst-case scenario is an attack through a<br>web server, which does not require any privileges, for<br>example, a simple CGI script.                                                                                                                                           |
| User Interaction    | None      | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                                                                                                                                                                  |
| Scope               | Unchanged | The vulnerable component is the GNU Bash shell, which is<br>used as an interpreter for various services or can be<br>accessed directly. It runs within the security authority of the<br>operating system. The impacted component is also the<br>operating system, so there is no scope change. |
| Confidentiality     | High      | An attacker can take complete control of the affected<br>system.                                                                                                                                                                                                                               |
| Integrity           | High      | An attacker can take complete control of the affected<br>system.                                                                                                                                                                                                                               |
| Availability        | High      | An attacker can take complete control of the affected<br>system.                                                                                                                                                                                                                               |

## CVSS v4 Score: Base + Threat 9.3

| Metric                               | Value   | Comments                                                                                                     |
|--------------------------------------|---------|--------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                                    |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                             |
| Attack Requirements   None           |         | No attack requirements are present.                                                                          |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                     |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                |
| Vulnerable System<br>Confidentiality | High    | The attacker can run arbitrary commands with elevated<br>privileges and access sensitive system information. |

![](_page_25_Picture_0.jpeg)

| Vulnerable System<br>Integrity       | High     | The attacker can run arbitrary commands with elevated<br>privileges and modify the system configuration.                           |
|--------------------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------|
| Vulnerable System<br>Availability    | High     | The attacker can run arbitrary commands with elevated<br>privileges and gain access sufficient to reset or turn off the<br>device. |
| Subsequent System<br>Confidentiality | None     | There is no impact to subsequent systems.                                                                                          |
| Subsequent System<br>Integrity       | None     | There is no impact to subsequent systems.                                                                                          |
| Subsequent System<br>Availability    | None     | There is no impact to subsequent systems.                                                                                          |
| Exploit Maturity                     | Attacked | There are known exploits in the wild.                                                                                              |

# Juniper Proxy ARP Denial of Service Vulnerability (CVE-2013-6014)

## Vulnerability

If Proxy ARP is enabled on an unnumbered interface, an attacker can poison the ARP cache and create a bogus forwarding table entry for an IP address, effectively creating a denial of service for that subscriber or interface. When Proxy ARP is enabled on an unnumbered interface, the router will answer any ARP message from any IP address which could lead to exploitable information disclosure. This issue can affect any product or platform running Junos OS 10.4, 11.4, 11.4X27, 12.1, 12.1X44, 12.1X45, 12.2, 12.3, or 13.1, supporting unnumbered interfaces.

## Attack

Exploitation of this vulnerability requires network adjacency with the target system and the ability to generate arbitrary ARP replies sent to the connected interface. A rogue subscriber can poison the ARP cache and/or create a rogue forwarding table entry for an IP of choice, effectively obscuring that IP address or redirecting IP traffic to the attacker.

The resultant impact can be observed as unauthorized modification of a database on the vulnerable component, or as an impact on confidentiality or availability on attached devices (impacted component). Since the CVSSv3 score for a high confidentiality (or availability) impact on a changed scope is higher than a partial impact on the vulnerable component, CVSSv3 guidance recommends to score for the higher overall impact.

![](_page_26_Picture_0.jpeg)

| v3.1                                             | v4.0 Base                                                           |
|--------------------------------------------------|---------------------------------------------------------------------|
| ਰੇ 3                                             | 6.4                                                                 |
| CVSS:3.1/AV:A/AC:L/PR:N/Ul:N/S:C/C:<br>H/I:N/A:H | CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:H/<br>SI:N/SA:H |

## CVSS v4 Score: Base 6.4

| Metric                               | Value    | Comments                                                                                      |
|--------------------------------------|----------|-----------------------------------------------------------------------------------------------|
| Attack Vector                        | Adjacent | The attacker must be within the local proximity of the<br>device.                             |
| Attack Complexity                    | Low      | No specialized conditions or advanced knowledge are<br>required.                              |
| Attack Requirements                  | None     | No attack requirements are present.                                                           |
| Privileges Required                  | None     | No privileges are required for an attacker to successfully<br>exploit the vulnerability.      |
| User Interaction                     | None     | No user interaction is required for an attacker to<br>successfully exploit the vulnerability. |
| Vulnerable System<br>Confidentiality | None     | There is no impact to the vulnerable system confidentiality.                                  |
| Vulnerable System<br>Integrity       | Low      | Unauthorized modification of a database on the vulnerable<br>system.                          |
| Vulnerable System<br>Availability    | None     | There is no impact to the vulnerable system availability.                                     |
| Subsequent System<br>Confidentiality | High     | The attacker can hijack and redirect the IP traffic to<br>themselves.                         |
| Subsequent System<br>Integrity       | None     | There is no impact to the subsequent system integrity.                                        |
| Subsequent System<br>Availability    | High     | Adding the rogue forwarding table can redirect the end<br>user to rogue IP addresses.         |

![](_page_27_Picture_0.jpeg)

# Lenovo ThnkPwn Exploit (CVE-2016-5729)

### Vulnerability

The SmmRuntime BIOS EFI Driver allows local administrators to execute arbitrary code with System Management Mode (SMM) privileges via unspecified vectors.

#### Attack

Attacker creates a buffer in memory containing exploit code to be executed in SMM context. Attacker then creates a structure with a pointer to the exploit code's entry point and triggers an SMI passing a reference to that structure. The SMM driver then calls the exploit code via the supplied function pointer.

#### Notes:

The previous assessment that notes impacts to subsequent systems was based on outdated understanding from CVSS 3.1. A new consensus has evolved with the understanding that hardware, firmware, and software running on a physical device in most cases are considered a single system, per definition in the CVSS Specification Document section 2.2 and the definition of a system of interest.

| v3.1                                             | v4.0 Base + Threat                                                      |
|--------------------------------------------------|-------------------------------------------------------------------------|
| 8.2                                              | 8.4                                                                     |
| CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:<br>H/I:H/A:H | CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N<br>/SI:N/SA:N/R:I |

#### CVSS v4 Score: Base + Threat 9.3

| Metric                     | Value | Comments                                                                                                                                       |
|----------------------------|-------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector              | Local | An attacker must be able to execute code on the system.                                                                                        |
| Attack Complexity          | Low   | This attack leverages a failure to verify input parameters in<br>the SmmRuntime driver and can be reproduced<br>consistently with simple code. |
| Attack Requirements   None |       | No attack requirements are present.                                                                                                            |
| Privileges Required        | High  | The attacker must be able to run kernel level (ring 0) code                                                                                    |

![](_page_28_Picture_0.jpeg)

|                                      |               | on the affected system.                                                                                                                                                                                                |
|--------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| User Interaction                     | None          | The vulnerability is built into the BIOS and is always<br>available. There is no user configuration involved.                                                                                                          |
| Vulnerable System<br>Confidentiality | High          | SMM has complete control over the system, including all<br>information on the system.                                                                                                                                  |
| Vulnerable System<br>Integrity       | High          | SMM access allows an attacker to modify any part of the<br>system.                                                                                                                                                     |
| Vulnerable System<br>Availability    | High          | The attacker could keep the system in SMM, denying<br>access to the system and never returning to a normal<br>operation mode.                                                                                          |
| Subsequent System<br>Confidentiality | None          | While impacts may be expanded from BIOS to any<br>operating system running on the device, the combination<br>of hardware, firmware and software is considered a<br>singular system as defined by a system of interest. |
| Subsequent System<br>Integrity       | None          | Impacts constrained to the vulnerable system.                                                                                                                                                                          |
| Subsequent System<br>Availability    | None          | Impacts constrained to the vulnerable system.                                                                                                                                                                          |
| Recovery                             | Irrecoverable | The attacker could keep the system in SMM, and could<br>prevent recovery of the system by automatically running<br>their code and locking down the system to prevent a user<br>from accessing it.                      |

# Failure to Lock Flash on Resume from sleep (CVE-2015-2890)

## Vulnerability

Some UEFI BIOS implementations failed to set Flash write protections such as the BIOS_CNTL locking on resume from the S3 suspend to RAM sleep state.

#### Attack

Attacker causes or waits until the system resumes from suspend, and then writes over the current BIOS image in Flash with a new BIOS image modified by the attacker.

![](_page_29_Picture_0.jpeg)

| v3.1                                             | v4.0 Base + Threat                                                      |
|--------------------------------------------------|-------------------------------------------------------------------------|
| 6.0                                              | 7.1                                                                     |
| CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:<br>N/I:H/A:H | CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/<br>SI:N/SA:N/R:I |

## CVSS v4 Score: Base + Threat 8.7

| Metric                               | Value   | Comments                                                                                                                                         |
|--------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Local   | An attacker must be able to execute code on the system.                                                                                          |
| Attack Complexity                    | Low     | An attacker has unfettered access to the Flash part on<br>which the BIOS is stored.                                                              |
| Attack Requirements                  | Present | The vulnerability is introduced by firmware failing to<br>enable correct flash memory protections upon the resume<br>from S3 system sleep state. |
| Privileges Required                  | High    | An attacker must be able to run kernel level (ring 0) code<br>on the target system, in order to access the Flash part.                           |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                    |
| Vulnerable System<br>Confidentiality | High    | An attacker that can modify the BIOS image can install<br>components to completely monitor and control the<br>vulnerable system.                 |
| Vulnerable System<br>Integrity       | High    | An attacker that can modify the BIOS image can modify<br>anything on the vulnerable system.                                                      |
| Vulnerable System<br>Availability    | High    | An attacker could cause a denial of service by corrupting<br>the BIOS image or could encrypt the vulnerable system.                              |
| Subsequent System<br>Confidentiality | None    | lmpacts constrained to the vulnerable system.                                                                                                    |
| Subsequent System<br>Integrity       | None    | Impacts constrained to the vulnerable system.                                                                                                    |
| Subsequent System<br>Availability    | None    | Impacts constrained to the vulnerable system.                                                                                                    |

![](_page_30_Picture_0.jpeg)

| IRecovery |  | lrrecoverable    An attacker could cause a denial of service through |
|-----------|--|----------------------------------------------------------------------|
|           |  | encryption or corruption, neither of which could be fixed            |
|           |  | lby a user.                                                          |

# Intel DCI Issue (CVE-2018-3652)

## Vulnerability

Existing UEFI setting restrictions for DCI (Direct Connect Interface) in 5th and 6th generation Intel Xeon Processor E3 Family, Intel Xeon Scalable processors, and Intel Xeon Processor D Family allows a limited physical presence attacker to potentially access platform secrets via debug interfaces.

#### Attack

An attacker with physical access can attach a debug device to the DCI interface and directly interrogate and control the processor state starting from very early in the boot process.

| v3.1                                             | v4.0 Base                                                           |
|--------------------------------------------------|---------------------------------------------------------------------|
| 7.6                                              | 7.0                                                                 |
| CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:C/C:<br>H/I:H/A:H | CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N<br>/SI:N/SA:N |

#### CVSS v4 Score: Base 8.6

| Metric                     | Value    | Comments                                                                                          |
|----------------------------|----------|---------------------------------------------------------------------------------------------------|
| Attack Vector              | Physical | An attacker must have physical access to the DCI port in<br>order to attach the debugging device. |
| Attack Complexity          | Low      | The debugging device is off-the-shelf hardware that can be<br>purchased from Intel.               |
| Attack Requirements   None |          | No attack requirements are present.                                                               |

![](_page_31_Picture_0.jpeg)

| Privileges Required                  | None | Only physical presence is required; no system privileges<br>are required.                                  |
|--------------------------------------|------|------------------------------------------------------------------------------------------------------------|
| User Interaction                     | None | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.              |
| Vulnerable System<br>Confidentiality | High | An attacker can view all memory and CPU instructions.                                                      |
| Vulnerable System<br>Integrity       | High | An attacker can modify all contents of memory and control<br>the CPU directly.                             |
| Vulnerable System<br>Availability    | High | An attacker can cause a denial of service by stopping the<br>CPU from executing the desired functionality. |
| Subsequent System<br>Confidentiality | None | Impacts constrained to the vulnerable system.                                                              |
| Subsequent System<br>Integrity       | None | Impacts constrained to the vulnerable system.                                                              |
| Subsequent System<br>Availability    | None | Impacts constrained to the vulnerable system.                                                              |

# Common Vulnerabilities Classes

This section contains examples of commonly-seen vulnerabilities from across the industry. The examples here are meant to be illustrative of common issues, but should not be considered authoritative. Unique vulnerabilities may have different impacts.

Note as well that some examples show the use of Threat and Environmental scores. Threat and Environmental metrics should typically only be used by CVSS consumers. The Threat and Environmental metrics shown here illustrate how to use the metrics.

# regreSSHion - CVE-2024-6387

## Description

A security regression (CVE-2006-5051) was discovered in OpenSSH's server (sshd). There is a race condition which can lead to sshd to handle some signals in an unsafe manner. An

![](_page_32_Picture_0.jpeg)

unauthenticated, remote attacker may be able to trigger it by failing to authenticate within a set time period.

Notes:

The scenario below assumes a standalone Linux-based system without dependent managed systems that has ASLR protections enabled.

| v3.1                                             | v4.0 Base+Threat                                                        |
|--------------------------------------------------|-------------------------------------------------------------------------|
| 8.1                                              | 8.2                                                                     |
| CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:<br>H/I:H/A:H | CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N<br>/SI:N/SA:N/E:P |

## CVSS v4 Score: Base 8.2

| Metric                               | Value   | Comments                                                                                                                      |
|--------------------------------------|---------|-------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | An attacker must be able to connect to the system from a<br>remote network.                                                   |
| Attack Complexity                    | High    | Attackers must be able to defeat mitigations on platforms<br>where ASLR and other memory defenses are present.                |
| Attack Requirements                  | Present | An attacker must defeat a race condition, making the<br>exploit unreliable.                                                   |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                      |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                 |
| Vulnerable System<br>Confidentiality | High    | The attacker could execute arbitrary code, which could<br>allow the attacker to completely compromise the affected<br>system. |
| Vulnerable System<br>Integrity       | High    | The attacker could execute arbitrary code, which could<br>allow the attacker to completely compromise the affected<br>system. |

![](_page_33_Picture_0.jpeg)

| Vulnerable System<br>Availability    | High | The attacker could execute arbitrary code, which could<br>allow the attacker to completely compromise the affected<br>system. |
|--------------------------------------|------|-------------------------------------------------------------------------------------------------------------------------------|
| Subsequent System<br>Confidentiality | None | There is no direct impact to subsequent systems.                                                                              |
| Subsequent System<br>Integrity       | None | There is no direct impact to subsequent systems.                                                                              |
| Subsequent System<br>Availability    | None | There is no direct impact to subsequent systems.                                                                              |
| Exploit Maturity                     | ept  | Proof-of-conc   A proof-of-concept that demonstrates the vulnerability is<br>available publicly.                              |

#### Variation 1: Login Mitigation

In this variation, the application of the mitigation to reduce LoginGraceTime to 0 prevents exploitation of arbitrary code execution. However, the modified configuration leaves the SSH service vulnerable to resource exhaustion attacks. The resulting assessment reflects only the potential to cause a denial of service (DoS) condition.

The below score uses modified base metrics to reflect the changes to exploitability and impact values.

Modified Attack Complexity and Modified Attack Requirements replace the base Attack Complexity and Attack Requirements. With the mitigation in place, an attacker must no longer defeat a race condition or memory protections to exhaust available connections.

Modified Vulnerable System Confidentiality and Modified System Integrity values replace the base Vulnerable System Confidentiality and Vulnerable System Integrity. There are no longer impacts to system confidentiality or integrity with the mitigation in place.

| v3.1                                             | v4.0 Base+Threat+Environmental                                                                              |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| 8.1                                              | 5.5                                                                                                         |
| CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:<br>H/I:H/A:H | CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N<br>/SI:N/SA:N/E:P/MAC:L/MAT:N/MVC:N/MVI:N/MVI:N/MVA:L |

![](_page_34_Picture_0.jpeg)

## CVSS v4 Score: BTE 5.5

| Metric                                           | Value                | Comments                                                                                                                      |
|--------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                                    | Network              | An attacker can connect to the system from a remote<br>network.                                                               |
| Attack Complexity                                | High                 | Attackers must be able to defeat mitigations on platforms<br>where ASLR and other memory defenses are present.                |
| Attack Requirements                              | Present              | An attacker must defeat a race condition, making the<br>exploit unreliable.                                                   |
| Privileges Required                              | None                 | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                      |
| User Interaction                                 | None                 | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                 |
| Vulnerable System<br>Confidentiality             | High                 | The attacker could execute arbitrary code, which could<br>allow the attacker to completely compromise the affected<br>system. |
| Vulnerable System<br>Integrity                   | High                 | The attacker could execute arbitrary code, which could<br>allow the attacker to completely compromise the affected<br>system. |
| Vulnerable System<br>Availability                | High                 | The attacker could execute arbitrary code, which could<br>allow the attacker to completely compromise the affected<br>system. |
| Subsequent System<br>Confidentiality             | None                 | There is no direct impact to subsequent systems.                                                                              |
| Subsequent System<br>Integrity                   | None                 | There is no direct impact to subsequent systems.                                                                              |
| Subsequent System<br>Availability                | None                 | There is no direct impact to subsequent systems.                                                                              |
| Exploit Maturity                                 | Proof-of-conc<br>ept | A proof-of-concept that demonstrates the vulnerability is<br>available publicly.                                              |
| Modified Vulnerable<br>System<br>Confidentiality | None                 | With the mitigation in place, the attacker cannot impact<br>system confidentiality.                                           |

![](_page_35_Picture_0.jpeg)

| Modified Vulnerable    None<br>System Integrity    |  | With the mitigation in place, the attacker cannot impact<br>Isystem integrity.               |
|----------------------------------------------------|--|----------------------------------------------------------------------------------------------|
| Modified Vulnerable    Low<br> System Availability |  | The attacker could exhaust available connections,<br> rendering the SSH service unavailable. |

# SQL Injection – CVE-2023-30545

## Description

PrestaShop is an Open Source e-commerce web application. Prior to versions 8.0.4 and 1.7.8.9, it is possible for a user with access to the SQL Manager (Advanced Options -> Database) to arbitrarily read any file on the operating system when using SQL function `LOAD_FILE` in a `SELECT` request. This gives the user access to critical information. A patch is available in PrestaShop 8.0.4 and PS 1.7.8.9

| v3.1                                             | v4.0 Base                                                           |
|--------------------------------------------------|---------------------------------------------------------------------|
| 6.5                                              | 7.1                                                                 |
| CVSS:3.1/AV:N/AC:L/PR:L/Ul:N/S:U/C:<br>H/I:N/A:N | CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N<br>/SI:N/SA:N |

## CVSS v4 Score: Base 7.1

| Metric                     | Value   | Comments                                                                                      |
|----------------------------|---------|-----------------------------------------------------------------------------------------------|
| Attack Vector              | Network | The vulnerable system is accessible from remote networks.                                     |
| Attack Complexity          | Low     | No specialized conditions or advanced knowledge are<br>required.                              |
| Attack Requirements   None |         | No attack requirements are present.                                                           |
| Privileges Required        | Low     | Attacker has to have database access (non-root user access).                                  |
| User Interaction           | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability. |
| Vulnerable System          | High    | An attacker can read any file on the operating system                                         |

![](_page_36_Picture_0.jpeg)

| Confidentiality                      |      |                                                           |
|--------------------------------------|------|-----------------------------------------------------------|
| Vulnerable System<br>Integrity       | None | There is no impact to the vulnerable system integrity.    |
| Vulnerable System<br>Availability    | None | There is no impact to the vulnerable system availability. |
| Subsequent System<br>Confidentiality | None | There is no impact to subsequent systems Confidentiality. |
| Subsequent System<br>Integrity       | None | There is no impact to subsequent systems Integrity.       |
| Subsequent System<br>Availability    | None | There is no impact to subsequent systems Availability.    |

# On-path Attacker – CVE-2021-23846

#### Description

Firmware for Bosch devices transmits in clear text over HTTP, allowing on-path attackers to gain access to user credentials.

| v3.1      | v4.0 Base                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------|
| 5.9       | 8.2                                                                                                       |
| H/I:N/A:N | CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:   CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/V/:N/VA:N/SC:N<br>/SI:N/SA:N |

## CVSS v4 Score: Base 8.2

| Metric              | Value   | Comments                                                         |
|---------------------|---------|------------------------------------------------------------------|
| Attack Vector       | Network | The vulnerable system is accessible from remote networks.        |
| l Attack Complexity | LOW     | No specialized conditions or advanced knowledge are<br>required. |

![](_page_37_Picture_0.jpeg)

| Attack Requirements                  | Present | An attacker must be on-path to be able to intercept<br>communications between affected systems. |
|--------------------------------------|---------|-------------------------------------------------------------------------------------------------|
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.        |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.   |
| Vulnerable System<br>Confidentiality | High    | An attacker could access plain text user credentials.                                           |
| Vulnerable System<br>Integrity       | None    | There is no impact to the vulnerable system integrity.                                          |
| Vulnerable System<br>Availability    | None    | There is no impact to the vulnerable system availability.                                       |
| Subsequent System<br>Confidentiality | None    | There is no impact to subsequent systems.                                                       |
| Subsequent System<br>Integrity       | None    | There is no impact to subsequent systems.                                                       |
| Subsequent System<br>Availability    | None    | There is no impact to subsequent systems.                                                       |

# Denial of Service – CVE-2023-22394

#### Description

Memory leak due to receipt of specially crafted SIP calls (CVE-2023-22394)

An Improper Handling of Unexpected Data Type vulnerability in the handling of SIP calls in Junos OS on SRX Series and MX Series platforms allows an attacker to cause a memory leak leading to Denial of Services (DoS).

|      | v3.1                                                                                       | v4.0                                   |
|------|--------------------------------------------------------------------------------------------|----------------------------------------|
| Base | 7.5<br>CVSS:3.1/AV:N/AC:L/PR:N/Ul:N/S:U/   CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:<br>C:N/I:N/A:H | 8.7<br>N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L |

![](_page_38_Picture_0.jpeg)

| Base + Threat |  | 6.6                               |
|---------------|--|-----------------------------------|
|               |  | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:  |
|               |  | N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E |
|               |  | :U                                |

## CVSS v4 Score: Base + Threat 6.6

| Metric                               | Value   | Comments                                                                                                                                                                                                                                       |
|--------------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                                                                                                                                                                      |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                                                                                                                                                               |
| Attack Requirements                  | None    | No attack requirements are present.                                                                                                                                                                                                            |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                                                                                                       |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                                                                                                                  |
| Vulnerable System<br>Confidentiality | None    | There is no impact to the vulnerable system confidentiality.                                                                                                                                                                                   |
| Vulnerable System<br>Integrity       | None    | There is no impact to the vulnerable system integrity.                                                                                                                                                                                         |
| Vulnerable System<br>Availability    | High    | An Improper Handling of Unexpected Data Type<br>vulnerability in the handling of SIP calls in Juniper Networks<br>Junos OS on SRX Series and MX Series platforms allows an<br>attacker to cause a memory leak leading to denial of<br>service. |
| Subsequent System<br>Confidentiality | None    | There is no confidentiality impact to subsequent systems.                                                                                                                                                                                      |
| Subsequent System<br>Integrity       | None    | There is no impact to the integrity of subsequent systems.                                                                                                                                                                                     |
| Subsequent System<br>Availability    | Low     | The subsequent device could be unavailable/unreachable<br>for a brief period of time.                                                                                                                                                          |

![](_page_39_Picture_0.jpeg)

| Exploit Maturity | Unreported | There is no known proof-of-concept or malicious |
|------------------|------------|-------------------------------------------------|
|                  |            | lexploitation of this vulnerability.            |
|                  |            |                                                 |

# Cross-Site Scripting (Reflected) – CVE-2022-24682

Categories: XSS

An issue was discovered in the Calendar feature in Zimbra Collaboration Suite 8.8.x before 8.8.15 patch 30 (update 1), as exploited in the wild starting in December 2021. An attacker could place HTML containing executable JavaScript inside element attributes. This markup becomes unescaped, causing arbitrary markup to be injected into the document.

| v3.1     | v4.0 Base                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 6.1      | 5.1                                                                                                        |
| /I:L/A:N | CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L   CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/V/:N/VA:N/SC:L/<br>SI:L/SA:N |

## CVSS v4 Score: Base 5.1

| Metric                               | Value   | Comments                                                                                 |
|--------------------------------------|---------|------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                         |
| Attack Requirements                  | None    | No attack requirements are present.                                                      |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability. |
| User Interaction                     | Active  | A targeted user must click a malicious link that is provided<br>by an attacker.          |
| Vulnerable System<br>Confidentiality | None    | There is no direct impact to the web application<br>confidentiality.                     |

![](_page_40_Picture_0.jpeg)

| Vulnerable System<br>Integrity       | None | There is no direct impact to the web application integrity.    |
|--------------------------------------|------|----------------------------------------------------------------|
| Vulnerable System<br>Availability    | None | There is no direct impact to the web application availability. |
| Subsequent System<br>Confidentiality | Low  | An attacker could read data from the user's browser.           |
| Subsequent System<br>Integrity       | Low  | An attacker could modify data in the user's browser.           |
| Subsequent System<br>Availability    | None | There is no direct availability impact to the user's browser.  |

## Variation 1: Impact to Vulnerable Application

Typical cross-site scripting CVSS assessments show simple, direct impacts to a user's browser. Some evaluations, however, may expand impacts to the vulnerable web application to show how an attacker can use access in the user's browser to impact the vulnerable web application. An example of this evaluation, a variant of CVE-2022-24682 based on reported attacks in the wild, is shown below.

| v4.0 Base                                                           |  |  |
|---------------------------------------------------------------------|--|--|
| 5.1                                                                 |  |  |
| CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:L/VI:L/VA:N/SC:L/<br>SI:L/SA:N |  |  |

## CVSS v4 Score: Base+Threat 5.1

| Metric                     | Value   | Comments                                                                                 |
|----------------------------|---------|------------------------------------------------------------------------------------------|
| Attack Vector              | Network | The vulnerable system is accessible from remote networks.                                |
| Attack Complexity          | Low     | No specialized conditions or advanced knowledge are<br>required.                         |
| Attack Requirements   None |         | No attack requirements are present.                                                      |
| Privileges Required        | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability. |

![](_page_41_Picture_0.jpeg)

| User Interaction                     | Active   | A targeted user must click a malicious link that is provided<br>by an attacker.                                      |
|--------------------------------------|----------|----------------------------------------------------------------------------------------------------------------------|
| Vulnerable System<br>Confidentiality | Low      | User sessions could be abused to extract data from the<br>application, including email content.                      |
| Vulnerable System<br>Integrity       | Low      | User privileges could be abused to modify or delete data<br>from the application, or send emails as a targeted user. |
| Vulnerable System<br>Availability    | None     | No direct identified vulnerable system availability impact.                                                          |
| Subsequent System<br>Confidentiality | Low      | An attacker could read data from the user's browser.                                                                 |
| Subsequent System<br>Integrity       | Low      | An attacker could modify data in the user's browser.                                                                 |
| Subsequent System<br>Availability    | None     | There is no direct availability impact to the user's browser.                                                        |
| Threat                               | Reported | Reported by the vendor to be used in attacks.                                                                        |

# Cross-Site Scripting (Stored) – CVE-2020-0926

Microsoft Office SharePoint XSS Vulnerability

## Description

A cross-site-scripting (XSS) vulnerability exists when Microsoft SharePoint Server does not properly sanitize a specially crafted web request to an affected SharePoint server, aka 'Microsoft Office SharePoint XSS Vulnerability'.

An authenticated attacker could exploit the vulnerability by sending a specially crafted request to an affected SharePoint server. The attacker who successfully exploited the vulnerability could then perform cross-site scripting attacks on affected systems and run script in the security context of the current user. The attacks could allow the attacker to read content that the attacker is not authorized to read, use the victim's identity to take actions on the SharePoint site on behalf of the user, such as change permissions and delete content, and inject malicious content in the browser of the user.

![](_page_42_Picture_0.jpeg)

| v3.1     | v4.0 Base                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 5.4      | 5.1                                                                                                        |
| /I:L/A:N | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L   CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:N/V/:N/VA:N/SC:L/<br>SI:L/SA:N |

## CVSS v4 Score: Base 5.1

| Metric                               | Value   | Comments                                                                                             |
|--------------------------------------|---------|------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                            |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                     |
| Attack Requirements                  | None    | No attack requirements are present.                                                                  |
| Privileges Required                  | Low     | The attacker requires privileges sufficient to store data<br>within the application.                 |
| User Interaction                     | Passive | A targeted user must browse to the application as part of<br>normal operations.                      |
| Vulnerable System<br>Confidentiality | None    | There is no direct impact to the web application<br>confidentiality.                                 |
| Vulnerable System<br>Integrity       | None    | There is no direct impact to the web application integrity.                                          |
| Vulnerable System<br>Availability    | None    | There is no direct impact to the web application availability.                                       |
| Subsequent System<br>Confidentiality | Low     | An attacker can read content that the attacker is not<br>authorized to read from the user's browser. |
| Subsequent System<br>Integrity       | Low     | An attacker could inject malicious content that could be<br>executed within the user's browser.      |
| Subsequent System<br>Availability    | None    | There is no direct impact to the user's browser availability.                                        |

![](_page_43_Picture_0.jpeg)

# Cross-Site Scripting Expanded Impact – CVE-2024-55228

#### Categories: XSS

A cross-site scripting (XSS) vulnerability in the Product module of Dolibarr v21.0.0-beta allows attackers to execute arbitrary web scripts or HTMI via a crafted payload injected into the Title parameter.

Like other cross-site scripting examples as evaluated in CVSS vectors, the vulnerable system is defined as the web application that allows attackers to pass unfiltered input to the subsequent system, a browser application on a targeted user's system. This scoring example demonstrates an expanded impact from the targeted user's browser to the vulnerable application.

Note that this example may be atypical of cross-site scripting vulnerabilities. Depending on the privileges of the user who participates in an attack, impacts on the vulnerable application may differ or be entirely nonexistent. Assessments that include impacts to the vulnerable application should make certain to clearly define and document application impacts as a result of cross-site scripting exploitation.

| v3.1     | v4.0 Base                                                                                                  |
|----------|------------------------------------------------------------------------------------------------------------|
| 9.0      | 8.5                                                                                                        |
| /I:H/A:H | CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H   CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/V/:H/VA:H/SC:L/<br>SI:L/SA:N |

#### CVSS v4 Score: Base 8.5

| Metric                     | Value   | Comments                                                                            |
|----------------------------|---------|-------------------------------------------------------------------------------------|
| Attack Vector              | Network | The vulnerable system is accessible from remote networks.                           |
| Attack Complexity          | Low     | No specialized conditions or advanced knowledge are<br>Irequired.                   |
| Attack Requirements   None |         | No attack requirements are present.                                                 |
| Privileges Required        | Low     | An attacker requires privileges sufficient to access the<br>vulnerable application. |
| User Interaction           | Active  | A targeted user must interact with an embedded element in                           |

![](_page_44_Picture_0.jpeg)

|                                      |      | the application that is provided by an attacker.                                                                                                                                        |
|--------------------------------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vulnerable System<br>Confidentiality | High | The attacker could trigger the execution of commands with<br>the privileges of the targeted user, which could allow the<br>attacker to gain access to sensitive information.            |
| Vulnerable System<br>Integrity       | High | The attacker could trigger the execution of commands with<br>the privileges of the targeted user, which could allow the<br>attacker to modify the configuration or remove files.        |
| Vulnerable System<br>Availability    | High | The attacker could trigger the execution of commands with<br>the privileges of the targeted user, which could allow the<br>attacker to disable features and impact system availability. |
| Subsequent System<br>Confidentiality | Low  | An attacker could read data from the user's browser.                                                                                                                                    |
| Subsequent System<br>Integrity       | Low  | An attacker could modify data in the user's browser.                                                                                                                                    |
| Subsequent System<br>Availability    | None | There is no direct availability impact to the user's browser.                                                                                                                           |

# Cross-Site Request Forgery – CVE-2023-5602

WordPress Social Media Share Buttons & Social Sharing Icons Cross-Site Request Forgery

#### Description

The Social Media Share Buttons & Social Sharing Icons plugin for WordPress is vulnerable to Cross-Site Request Forgery in all versions up to, and including, 2.8.5. This is due to missing or incorrect nonce validation on several functions corresponding to AJAX actions. This makes it possible for unauthenticated attackers to invoke those actions via a forged request granted they can trick a site administrator into performing an action such as clicking on a link.

| v3.1                                               | v4.0 Base                                                           |
|----------------------------------------------------|---------------------------------------------------------------------|
| 4.3                                                | 5.1                                                                 |
| CVSS:3.1/AV:N/AC:L/PR:N/Ul:R/S:U/C:  <br>N/I:L/A:N | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:L/VA:N/SC:N/<br>SI:N/SA:N |

![](_page_45_Picture_0.jpeg)

## CVSS v4 Score: Base 5.1

| Metric                               | Value   | Comments                                                                                                                    |  |
|--------------------------------------|---------|-----------------------------------------------------------------------------------------------------------------------------|--|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                                                   |  |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                                            |  |
| Attack Requirements                  | None    | No attack requirements are present.                                                                                         |  |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                    |  |
| User Interaction                     | Active  | A targeted user must actively click on a malicious link that<br>is provided by an attacker to initiate the attack sequence. |  |
| Vulnerable System<br>Confidentiality | None    | There is no direct impact to the web application<br>confidentiality.                                                        |  |
| Vulnerable System<br>Integrity       | Low     | The attacker could modify some values within the web<br>application.                                                        |  |
| Vulnerable System<br>Availability    | None    | There is no direct impact to the web application availability.                                                              |  |
| Subsequent System<br>Confidentiality | None    | There is no impact to subsequent systems.                                                                                   |  |
| Subsequent System<br>Integrity       | None    | There is no impact to subsequent systems.                                                                                   |  |
| Subsequent System<br>Availability    | None    | There is no impact to subsequent systems.                                                                                   |  |

# Privilege Escalation (Unprivileged) CVE-2022-20759

## Description

Cisco Adaptive Security Appliance Firepower Threat Defense (FTD) Privilege Escalation Vulnerability (CVE-2022-20759)

![](_page_46_Picture_0.jpeg)

A vulnerability in the web services interface for remote access VPN features of Cisco Adaptive Security Appliance (ASA) Software and Cisco Firepower Threat Defense (FTD) Software could allow an authenticated, but unprivileged, remote attacker to elevate privileges to level 15.

An attacker could exploit this vulnerability by sending crafted HTTPS messages to the web services interface of an affected device. A successful exploit could allow the attacker to gain privilege level 15 access to the web management interface of the device.

| v3.1                                             | v4.0 Base                                                           |
|--------------------------------------------------|---------------------------------------------------------------------|
| 8.8                                              | 7.7                                                                 |
| CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:<br>H/I:H/A:H | CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/<br>SI:N/SA:N |

## CVSS v4 Score: Base 7.7

| Metric                               | Value   | Comments                                                                                                                                                                                   |  |
|--------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| Attack Vector                        | Network | Attacks are executed through HTTPS requests.                                                                                                                                               |  |
| Attack Complexity                    | Low     | No advanced knowledge is required                                                                                                                                                          |  |
| Attack Requirements                  | Present | HTTP Management Access and IKEv2 Client Service must be<br>enabled on at least one interface, or HTTP management<br>interface and WebVPN must be enabled on at least one<br>interface.     |  |
| Privileges Required                  | Low     | An attacker must have valid credentials for the VPN.                                                                                                                                       |  |
| User Interaction                     | None    | No additional user interaction is required for successful<br>exploitation.                                                                                                                 |  |
| Vulnerable System<br>Confidentiality | High    | Successful exploitation could result in a complete<br>compromise (enable 15) of the targeted device, which<br>results in a complete (High) impact on the confidentiality of<br>the device. |  |
| Vulnerable System<br>Integrity       | High    | Successful exploitation could result in a complete<br>compromise resulting in High integrity impact.                                                                                       |  |
| Vulnerable System<br>Availability    | High    | Successful exploitation could result in a complete<br>compromise resulting in High availability impact.                                                                                    |  |

![](_page_47_Picture_0.jpeg)

| Subsequent System<br>Confidentiality | None | There is no impact to subsequent systems. |
|--------------------------------------|------|-------------------------------------------|
| Subsequent System<br>Integrity       | None | There is no impact to subsequent systems. |
| Subsequent System<br>Availability    | None | There is no impact to subsequent systems. |

# Privilege Escalation (Highly Privileged) CVE-2021-34724

## Description

A vulnerability in the Cisco IOS XE SD-WAN Software CLI could allow an authenticated, local attacker to elevate privileges and execute arbitrary code on the underlying operating system as the root user. An attacker must be authenticated on an affected device as a PRIV15 administrative user.

|               | v3.1                                                    | v4.0                                                                               |
|---------------|---------------------------------------------------------|------------------------------------------------------------------------------------|
| Base          | 6.0<br>CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/<br>C:H/I:H/A:N | 8.3<br>CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:<br>N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N         |
| Base + Threat |                                                         | 5.6<br>CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:<br>N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/<br>E:U |

## CVSS v4 Score: Base + Threat 5.6

| Metric        | Value | Comments                                                                                        |
|---------------|-------|-------------------------------------------------------------------------------------------------|
| Attack Vector | Local | An attacker must be able to access the vulnerable system<br> with a local, interactive session. |

![](_page_48_Picture_0.jpeg)

| Attack Complexity                    | Low        | No specialized conditions or advanced knowledge are<br>required.                                                                                                                                                                                               |
|--------------------------------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Requirements                  | None       | No attack requirements are present.                                                                                                                                                                                                                            |
| Privileges Required                  | High       | An attacker must have administrator privileges within the<br>affected system.                                                                                                                                                                                  |
| User Interaction                     | None       | No additional user interaction is required for exploit                                                                                                                                                                                                         |
| Vulnerable System<br>Confidentiality | High       | An attacker could execute arbitrary commands on the<br>affected system with the privileges of the root user, allowing<br>the privileged attacker to access sensitive files that would<br>otherwise be inaccessible to the administrative user.                 |
| Vulnerable System<br>Integrity       | High       | An attacker could execute arbitrary commands on the<br>affected system with the privileges of the root user, allowing<br>the privileged attacker to modify system values that would<br>otherwise be inaccessible to the administrative user.                   |
| Vulnerable System<br>Availability    | None       | An attacker does not gain any additional privileges to<br>impact system availability. Privileges required to exploit this<br>vulnerability already allow the attacker to turn off the<br>system, so there is no privilege gain as a result of<br>exploitation. |
| Subsequent System<br>Confidentiality | None       | There is no impact to subsequent systems.                                                                                                                                                                                                                      |
| Subsequent System<br>Integrity       | None       | There is no impact to subsequent systems.                                                                                                                                                                                                                      |
| Subsequent System<br>Availability    | None       | There is no impact to subsequent systems.                                                                                                                                                                                                                      |
| Exploit Maturity                     | Unreported | There is no known proof-of-concept code or malicious<br>exploitation of this vulnerability.                                                                                                                                                                    |

# Remote Code Execution (CVE-2023-28311)

Microsoft Word Remote Code Execution Vulnerability

![](_page_49_Picture_0.jpeg)

An attacker must send the user a malicious file and convince the user to open said file which results in RCE.

| v3.1                                             | v4.0 Base                                                           |
|--------------------------------------------------|---------------------------------------------------------------------|
| 7.8                                              | 8.5                                                                 |
| CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:<br>H/I:H/A:H | CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/<br>SI:N/SA:N |

## CVSS v4 Score: Base 8.5

| Metric                               | Value   | Comments                                                                                                                      |
|--------------------------------------|---------|-------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Local   | The document must be present on the local disk.                                                                               |
| Attack Complexity                    | Low     | Nothing outside of the attacker's control.                                                                                    |
| Attack Requirements                  | None    | No attack requirements are present.                                                                                           |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                      |
| User Interaction                     | Passive | A user must open a document.                                                                                                  |
| Vulnerable System<br>Confidentiality | High    | The attacker could execute arbitrary code, which could<br>allow the attacker to compromise the affected system<br>completely. |
| Vulnerable System<br>Integrity       | High    | The attacker could execute arbitrary code, which could<br>allow the attacker to compromise the affected system<br>completely. |
| Vulnerable System<br>Availability    | High    | The attacker could execute arbitrary code, which could<br>allow the attacker to compromise the affected system<br>completely. |
| Subsequent System<br>Confidentiality | None    | There is no impact to subsequent systems.                                                                                     |
| Subsequent System<br>Integrity       | None    | There is no impact to subsequent systems.                                                                                     |

![](_page_50_Picture_0.jpeg)

| Subsequent System<br> Availability | There is no impact to subsequent systems. |
|------------------------------------|-------------------------------------------|
|------------------------------------|-------------------------------------------|

## Arbitrary Code Execution CVE-2022-22965

## Spring4shell

A Spring MVC or Spring WebFlux application running on JDK 9+ may be vulnerable to remote code execution (RCE) via data binding. The specific exploit requires the application to run on Tomcat as a WAR deployment. If the application is deployed as a Spring Boot executable jar, i.e. the default, it is not vulnerable to the exploit. However, the nature of the vulnerability is more general, and there may be other ways to exploit it.

#### Attack

An RCE can be established by simply sending a series of malicious web requests to a web server running on a vulnerable version of Spring. Spring4Shell allows attackers to get arbitrary code execution in the context of the user that is running the vulnerable application. Once the attackers achieve RCE, they can install malware or can use the server as an initial foothold to escalate privileges and compromise the whole system, or even access subsequent backend systems that the vulnerable server has privileged access to.

| v3.1                                             | v4.0 Base + Threat                                                      |
|--------------------------------------------------|-------------------------------------------------------------------------|
| 9.8                                              | 9.2                                                                     |
| CVSS:3.1/AV:N/AC:L/PR:N/Ul:N/S:U/C:<br>H/I:H/A:H | CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N<br>/SI:N/SA:N/E:A |

## CVSS v4 Score: Base + Threat 9.2

| Metric                        | Value   | Comments                                                                                            |
|-------------------------------|---------|-----------------------------------------------------------------------------------------------------|
| Attack Vector                 | Network | The vulnerable system is accessible from remote networks.                                           |
| Attack Complexity             | Low     | No specialized conditions or advanced knowledge are<br>required.                                    |
| Attack Requirements   Present |         | A successful attack depends on the deployment and<br>execution conditions of the vulnerable system. |

![](_page_51_Picture_0.jpeg)

| Privileges Required                  | None     | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                                                                                                                                                                           |
|--------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| User Interaction                     | None     | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                                                                                                                                                                                      |
| Vulnerable System<br>Confidentiality | High     | The vulnerability allows an attacker to execute arbitrary<br>code in the context of the user that is running the<br>vulnerable application and gain complete control over the<br>system.                                                                                                                           |
| Vulnerable System<br>Integrity       | High     | The vulnerability allows an attacker to execute arbitrary<br>code in the context of the user that is running the<br>vulnerable application and gain complete control over the<br>system.                                                                                                                           |
| Vulnerable System<br>Availability    | High     | The vulnerability allows an attacker to execute arbitrary<br>code in the context of the user that is running the<br>vulnerable application and gain complete control over the<br>system.                                                                                                                           |
| Subsequent System<br>Confidentiality | None     | There is no immediate loss of confidentiality within the<br>subsequent systems. But, based on how Spring is deployed<br>in the target environment, the compromised server could<br>be used as a pivot to leverage further. If there are<br>subsequent impacts, they should be defined in<br>environmental metrics. |
| Subsequent System<br>Integrity       | None     | There is no immediate loss of integrity within the<br>subsequent systems. But, based on how Spring is deployed<br>in the target environment, the compromised server could<br>be used as a pivot to leverage further. If there are<br>subsequent impacts, they should be defined in<br>environmental metrics.       |
| Subsequent System<br>Availability    | None     | There is no immediate loss of availability within the<br>subsequent system. But, based on how Spring is deployed<br>in the target environment, the compromised server could<br>be used as a pivot to leverage further. If there are<br>subsequent impacts, they should be defined in<br>environmental metrics.     |
| Exploit Maturity                     | Attacked | There are known exploits in the wild.                                                                                                                                                                                                                                                                              |

![](_page_52_Picture_0.jpeg)

## Physical Access (CVE-2022-20826)

A vulnerability in the secure boot implementation of Cisco Secure Firewalls 3100 Series that are running Cisco Adaptive Security Appliance (ASA) Software or Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated attacker with physical access to the device to bypass the secure boot functionality. This vulnerability is due to a logic error in the boot process. An attacker could exploit this vulnerability by injecting malicious code into a specific memory location during the boot process of an affected device. A successful exploit could allow the attacker to execute persistent code at boot time and break the chain of trust.

| v3.1      | v4.0 Base                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------|
| 6.4       | 5.4                                                                                                       |
| H/I:H/A:H | CVSS:3.1/AV:P/AC:H/PR:N/UI:N/S:U/C:   CVSS:4.0/AV:P/AC:L/AT:P/PR:N/UI:N/VC:H/V1:H/VA:H/SC:N/<br>SI:N/SA:N |

## CVSS v4 Score: Base 5.4

| Metric                               | Value    | Comments                                                                                             |
|--------------------------------------|----------|------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Physical | An attacker requires physical access to a vulnerable<br>system.                                      |
| Attack Complexity                    | Low      | No specialized conditions or advanced knowledge are<br>lrequired.                                    |
| Attack Requirements                  | Present  | There are timing requirements outside the attacker's<br>control, making exploit attempts unreliable. |
| Privileges Required                  | None     | No privileges are required for an attacker to successfully<br>exploit the vulnerability.             |
| User Interaction                     | None     | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.        |
| Vulnerable System<br>Confidentiality | High     | An attacker could inject malicious, unsigned code and<br>execute arbitrary commands.                 |
| Vulnerable System                    | High     | An attacker could inject malicious, unsigned code and                                                |

![](_page_53_Picture_0.jpeg)

| Integrity                            |      | execute arbitrary commands.                                                          |
|--------------------------------------|------|--------------------------------------------------------------------------------------|
| Vulnerable System<br>Availability    | High | An attacker could inject malicious, unsigned code and<br>execute arbitrary commands. |
| Subsequent System<br>Confidentiality | None | There is no impact to subsequent systems.                                            |
| Subsequent System<br>Integrity       | None | There is no impact to subsequent systems.                                            |
| Subsequent System<br>Availability    | None | There is no impact to subsequent systems.                                            |

# Information Disclosure - CVE-2022-21500

## Description

Vulnerability in Oracle E-Business Suite (component: Manage Proxies). The supported version that is affected is 12.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle E-Business Suite. Successful attacks of this vulnerability can result in unauthorized access to critical data or complete access to all Oracle E-Business Suite accessible data.

Note: Authentication is required for successful attack, however the user may be self-registered. Oracle E-Business Suite 12.1 is not impacted by this vulnerability. Customers should refer to the Patch Availability Document for details.

| v3.1                                               | v4.0 Base                                                           |
|----------------------------------------------------|---------------------------------------------------------------------|
| 7.5                                                | 8.7                                                                 |
| CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:  <br>H/I:N/A:N | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N<br>/SI:N/SA:N |

## CVSS v4 Score: Base 8.7

| Metric            | Value   | Comments                                                         |
|-------------------|---------|------------------------------------------------------------------|
| Attack Vector     | Network | The vulnerable system is accessible from remote networks.        |
| Attack Complexity | i Low   | No specialized conditions or advanced knowledge are<br>required. |

![](_page_54_Picture_0.jpeg)

| Attack Requirements                  | None | No attack requirements are present.                                                                                      |
|--------------------------------------|------|--------------------------------------------------------------------------------------------------------------------------|
| Privileges Required                  | None | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                 |
| User Interaction                     | None | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                            |
| Vulnerable System<br>Confidentiality | High | An attacker could exploit the vulnerability to access critical<br>data that is stored within the vulnerable application. |
| Vulnerable System<br>Integrity       | None | There is no impact to the vulnerable system integrity.                                                                   |
| Vulnerable System<br>Availability    | None | There is no impact to the vulnerable system availability.                                                                |
| Subsequent System<br>Confidentiality | None | There is no impact to subsequent systems.                                                                                |
| Subsequent System<br>Integrity       | None | There is no impact to subsequent systems.                                                                                |
| Subsequent System<br>Availability    | None | There is no impact to subsequent systems.                                                                                |

# Information Disclosure - CVE-2021-32570

In Ericsson Network Manager (ENM) releases before 21.2, users belonging to the same AMOS authorization group can retrieve the data from certain log files. All AMOS users are considered to be highly privileged users in the ENM system and all must be previously defined and authorized by the Security Administrator. Those users can access some log's files, under a common path, and read information stored in the log's files in order to conduct privilege escalation.

| v3.1      | v4.0 Base                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------|
| 4.9       | 6.9                                                                                                       |
| H/I:N/A:N | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:   CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/V/:N/VA:N/SC:N<br>/SI:N/SA:N |

![](_page_55_Picture_0.jpeg)

#### CVSS v4 Score: Base 6.9

| Metric                               | Value   | Comments                                                                                                    |
|--------------------------------------|---------|-------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                                   |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                            |
| Attack Requirements                  | None    | No attack requirements are present.                                                                         |
| Privileges Required                  | High    | An attacker must have membership in the AMOS<br>authorization group sufficient to read data from log files. |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.               |
| Vulnerable System<br>Confidentiality | High    | An attacker could exploit the vulnerability to view sensitive<br>data within the application log files.     |
| Vulnerable System<br>Integrity       | None    | There is no impact to the vulnerable system integrity.                                                      |
| Vulnerable System<br>Availability    | None    | There is no impact to the vulnerable system availability.                                                   |
| Subsequent System<br>Confidentiality | None    | There is no impact to subsequent systems.                                                                   |
| Subsequent System<br>Integrity       | None    | There is no impact to subsequent systems.                                                                   |
| Subsequent System<br>Availability    | None    | There is no impact to subsequent systems.                                                                   |

# Command Injection (CVE-2022-26134)

Description

Atlassian Confluence Server and Data Center OGNL Injection Vulnerability (CVE-2022-26134)

In Confluence Server and Data Center, an OGNL injection vulnerability exists that would allow an unauthenticated attacker to execute arbitrary code on a Confluence Server or Data Center instance.

![](_page_56_Picture_0.jpeg)

A remote attacker could exploit it by requests injecting specially crafted OGNL templates in order to execute arbitrary code.

| v3.1                                               | v4.0 Base                                                           |
|----------------------------------------------------|---------------------------------------------------------------------|
| ರಿ.8                                               | ਰੇ.3                                                                |
| CVSS:3.1/AV:N/AC:L/PR:N/Ul:N/S:U/C:  <br>H/I:H/A:H | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N<br>/SI:N/SA:N |

## CVSS v4 Score: Base 9.3

| Metric                               | Value   | Comments                                                                                                                                                                                                   |
|--------------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | Attacks are executed through HTTP(s) requests and are<br>accessible from remote networks.                                                                                                                  |
| Attack Complexity                    | Low     | No advanced knowledge is required                                                                                                                                                                          |
| Attack Requirements                  | None    | No attack requirements are present.                                                                                                                                                                        |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                                                                   |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                                                                              |
| Vulnerable System<br>Confidentiality | High    | Successful exploitation could result in a complete<br>compromise (command execution as root) of the affected<br>device, which results in a complete (High) impact on the<br>confidentiality of the device. |
| Vulnerable System<br>Integrity       | High    | Successful exploitation could result in a complete<br>compromise (command execution as root) of the affected<br>device, which results in a complete (High) impact on the<br>integrity of the device.       |
| Vulnerable System<br>Availability    | High    | Successful exploitation could result in a complete<br>compromise (command execution as root) of the affected<br>device, which results in a complete (High) impact on the<br>availability of the device.    |

![](_page_57_Picture_0.jpeg)

| Subsequent System<br>Confidentiality | None   | There are no additional impacts to subsequent systems. |
|--------------------------------------|--------|--------------------------------------------------------|
| Subsequent System<br>Integrity       | I None | There are no additional impacts to subsequent systems. |
| Subsequent System<br>Availability    | None   | There are no additional impacts to subsequent systems. |

# ACL Bypass (CVE-2023-20245)

A vulnerability in the per-user-override feature of Cisco Adaptive Security Appliance (ASA) Software and Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to bypass a configured access control list (ACL) and allow traffic that should be denied to flow through an affected device. The vulnerability is due to a logic error that could occur when the affected software constructs and applies per-user-override rules. An attacker could exploit the vulnerability by connecting to a network through an affected device that has a vulnerable configuration. A successful exploit could allow the attacker to bypass the interface ACL and access resources that should be protected.

| v3.1                      | v4.0 Base                                                                                     | v4.0 BTE                                                                                   |
|---------------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| 5.8                       | 6.9                                                                                           | 2.7                                                                                        |
| CVSS:3.1/AV:N/AC:L/P<br>N | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:<br>R:N/UI:N/S:C/C:N/I:L/A:   N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:<br>N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N/E<br>:U/CR:L/IR:L/AR:L |

## CVSS v4 Score: Base 6.9

| Metric                     | Value   | Comments                                                                                 |
|----------------------------|---------|------------------------------------------------------------------------------------------|
| Attack Vector              | Network | The vulnerable system is accessible from remote networks.                                |
| Attack Complexity          | Low     | No specialized conditions or advanced knowledge are<br>required.                         |
| Attack Requirements   None |         | No attack requirements are present.                                                      |
| l Privileges Required      | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability. |

![](_page_58_Picture_0.jpeg)

| User Interaction                     | None | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                |
|--------------------------------------|------|--------------------------------------------------------------------------------------------------------------|
| Vulnerable System<br>Confidentiality | None | There is no impact to the vulnerable system confidentiality.                                                 |
| Vulnerable System<br>Integrity       | None | There is no impact to the vulnerable system integrity.                                                       |
| Vulnerable System<br>Availability    | None | There is no impact to the vulnerable system availability.                                                    |
| Subsequent System<br>Confidentiality | None | There is no impact to subsequent systems.                                                                    |
| Subsequent System<br>Integrity       | Low  | The attacker could send network traffic to downstream<br>destinations that should otherwise be inaccessible. |
| Subsequent System<br>Availability    | None | There is no impact to subsequent systems.                                                                    |

## Variation 1: ACL Bypass with Downstream Impacts

In this example, we imagine a scenario in which the failure of an ACL to protect internal systems could result in impact to downstream systems.

| v4.0 Base                                                           |  |  |
|---------------------------------------------------------------------|--|--|
| 7.8                                                                 |  |  |
| CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/<br>VC:N/VI:L/VA:N/SC:L/SI:N/SA:H |  |  |

## CVSS v4 Score: Base 7.8

| Metric            | Value   | Comments                                                    |
|-------------------|---------|-------------------------------------------------------------|
| Attack Vector     | Network | l The vulnerable system is accessible from remote networks. |
| Attack Complexity | Low     | No specialized conditions or advanced knowledge are         |

![](_page_59_Picture_0.jpeg)

|                                      |      | required.                                                                                                                                        |
|--------------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Requirements                  | None | No attack requirements are present.                                                                                                              |
| Privileges Required                  | None | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                         |
| User Interaction                     | None | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                    |
| Vulnerable System<br>Confidentiality | None | There is no impact to the vulnerable system confidentiality.                                                                                     |
| Vulnerable System<br>Integrity       | Low  | The attacker could send network traffic through the device<br>to downstream destinations that should otherwise be<br>inaccessible.               |
| Vulnerable System<br>Availability    | None | There is no impact to the vulnerable system availability.                                                                                        |
| Subsequent System<br>Confidentiality | Low  | The attacker could gather information about or access<br>services on subsequent systems.                                                         |
| Subsequent System<br>Integrity       | None | There is no impact to subsequent systems.                                                                                                        |
| Subsequent System<br>Availability    | High | The attacker could send streams of network traffic that<br>could overwhelm the subsequent system, resulting in a<br>denial of service condition. |

#### Variation 2: ACL Bypass in open or low-value network segment

## CVSS v4 Score: BTE 2.7

The following threat and environmental metrics further enrich the ACL Bypass (CVE-2023-20245) example. The scoring scenario demonstrates impacts to an affected device that provides filtering for an open network with systems of minimal value such as a testing environment or lab environment regularly re-imaged and that does not contain any sensitive data. The security requirements for systems within this network are Low, because they are not critical to the environment, and impacts would, per the CVSS Specification Document – "likely to have only a limited adverse effect on the organization or individuals associated with the organization." Refer to the Threat and Environmental metric choices that further enrich the CVSS vector in the table above.

![](_page_60_Picture_0.jpeg)

| Metric                          | Value      | Comments                                                                                        |
|---------------------------------|------------|-------------------------------------------------------------------------------------------------|
| Threat                          | Unreported | No known public exploit exists.                                                                 |
| Confidentiality<br>Requirements | Low        | Networks impacted by this ACL bypass contain only<br>low-value systems with non-sensitive data. |
| Integrity<br>Requirements       | Low        | Networks impacted by this ACL bypass contain only<br>low-value systems with non-sensitive data. |
| Availability<br>Requirements    | Low        | Networks impacted by this ACL bypass contain only<br>low-value systems with non-sensitive data. |

# Server-Side Request Forgery (SSRF) (CVE-2024-1233)

Description:

A flaw was found in |wtValidator.resolvePublicKey in JBoss EAP, where the validator checks jku and sends a HTTP request. During this process, no whitelisting or other filtering behavior is performed on the destination URL address, which may result in a server-side request forgery (SSRF) vulnerability.

#### Notes:

lmpacts for server-side request forgery vulnerabilities may depend on both the configuration of the vulnerable system as well as the presence of other systems in the environment that could be accessed as part of exploitation.

The vulnerable system is the JBoss application server, while subsequent systems may be other applications on the same host or different back-end systems that are reachable by the vulnerable application server.

| v3.1                                               | v4.0                                                                |
|----------------------------------------------------|---------------------------------------------------------------------|
| 7.3                                                | 6.9                                                                 |
| CVSS:3.1/AV:N/AC:L/PR:N/Ul:N/S:U/C:  <br>L/I:L/A:L | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:L/<br>SI:L/SA:L |

## CVSS v4 Score: Base 6.9

| Metric<br>Value | Comments |
|-----------------|----------|
|-----------------|----------|

![](_page_61_Picture_0.jpeg)

| Attack Vector                        | Network | An attacker must be able to send requests to an<br>application that implements the vulnerable JBoss EAP<br>feature.                                                                                                |
|--------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Complexity                    | Low     | No built-in security-enhancing conditions exist within the<br>product to inhibit successful exploitation.                                                                                                          |
| Attack Requirements                  | None    | The attacker can execute the exploit with no specific<br>difficulty. No attack requirements are present.                                                                                                           |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                                                                           |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                                                                                      |
| Vulnerable System<br>Confidentiality | None    | There is no impact to the vulnerable system confidentiality.                                                                                                                                                       |
| Vulnerable System<br>Integrity       | Low     | The attacker could cause the vulnerable system to send<br>arbitrary HTTP requests.                                                                                                                                 |
| Vulnerable System<br>Availability    | None    | There is no impact to the vulnerable system availability.                                                                                                                                                          |
| Subsequent System<br>Confidentiality | Low     | The attacker could cause the vulnerable system to send<br>HTTP requests on the attacker's behalf to another system,<br>potentially allowing the attacker to gain information about<br>or from a subsequent system. |
| Subsequent System<br>Integrity       | Low     | The attacker could send HTTP requests to another system<br>and modify the application state of a subsequent system.                                                                                                |
| Subsequent System<br>Availability    | Low     | The attacker could send HTTP requests to another system<br>and potentially impact the availability of a subsequent<br>system.                                                                                      |

## Variation 1:

In this variation, the system implementing the vulnerable JBoss EAP application allows access only to limited endpoints, reducing the subsequent system impact to Confidentiality only, allowing the attacker to gather information about systems that should be unreachable. This represents a more typical impact of a SSRF vulnerability.

In the metric strings below, the Modified Subsequent System Integrity and Availability are selected as None and replace the base Subsequent System Integrity and Availability impacts.

![](_page_62_Picture_0.jpeg)

| v3.1                                               | v4.0                                                                            |
|----------------------------------------------------|---------------------------------------------------------------------------------|
| 7.3                                                | 6.9                                                                             |
| CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:  <br>L/I:L/A:L | CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:L/<br>SI:L/SA:L/MSI:N/MSA:N |

## CVSS v4 Score: Base+Environmental 6.9

| Metric                               | Value   | Comments                                                                                                                                                                                                                |
|--------------------------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network | An attacker must be able to send requests to an<br>application that implements the vulnerable JBoss EAP<br>feature.                                                                                                     |
| Attack Complexity                    | Low     | No built-in security-enhancing conditions exist within the<br>product to inhibit successful exploitation.                                                                                                               |
| Attack Requirements                  | None    | The attacker can execute the exploit with no specific<br>difficulty. No attack requirements are present.                                                                                                                |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                                                                                |
| User Interaction                     | None    | A user, other than the attacker, must be present for the<br>vulnerability to be exploited. However, the actions taken by<br>the user are typical, because a user must open a file within<br>the vulnerable application. |
| Vulnerable System<br>Confidentiality | None    | There is no impact to the vulnerable system confidentiality.                                                                                                                                                            |
| Vulnerable System<br>Integrity       | Low     | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.                                                                                                                              |
| Vulnerable System<br>Availability    | None    | There is no impact to the vulnerable system availability.                                                                                                                                                               |
| Subsequent System<br>Confidentiality | Low     | The attacker could cause the vulnerable system to send<br>HTTP requests on the attacker's behalf to another system,<br>potentially allowing the attacker to gain information about                                      |

![](_page_63_Picture_0.jpeg)

|                                                   |     | or from a subsequent system.                                                                                                  |
|---------------------------------------------------|-----|-------------------------------------------------------------------------------------------------------------------------------|
| Subsequent System<br>Integrity                    | Low | The attacker could send HTTP requests to another system<br>and modify the application state of a subsequent system.           |
|                                                   |     | Note: the Modified Subsequent System Integrity replaces<br>this metric.                                                       |
| Subsequent System<br>Availability                 | Low | The attacker could send HTTP requests to another system<br>and potentially impact the availability of a subsequent<br>system. |
|                                                   |     | Note: the Modified Subsequent System Availability replaces<br>this metric.                                                    |
| Modified Subsequent   None<br>System Integrity    |     | No applications reachable by the vulnerable system accept<br>HTTP requests, resulting in no integrity impact.                 |
| Modified Subsequent   None<br>System Availability |     | No applications reachable by the vulnerable system accept<br>HTTP requests, resulting in no availability impact.              |

# Industrial Control Systems (ICS) (CVE-2023-28728)

Description:

In Panasonic Control FPWIN versions 7.6.0.3 and prior, a stack-based buffer overflow condition is a condition where the buffer being overwritten is allocated on the stack (i.e., is a local variable or a parameter to a function) when a file is opened within the application.

| v3.1                                             | v4.0                                                                    |
|--------------------------------------------------|-------------------------------------------------------------------------|
| 7.8                                              | 8.5                                                                     |
| CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:<br>H/I:H/A:H | CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/<br>SI:N/SA:N/S:P |

## CVSS v4 Score: Base 8.5

| Value<br>Metric | Comments |
|-----------------|----------|
|-----------------|----------|

![](_page_64_Picture_0.jpeg)

| Attack Vector                        | Local   | An attacker must be locally connected to the vulnerable<br>system.                                                                                                                                                                                                                                                                       |
|--------------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attack Complexity                    | Low     | No built-in security-enhancing conditions exist within the<br>product to inhibit successful exploitation.                                                                                                                                                                                                                                |
| Attack Requirements                  | None    | The attacker can execute the exploit with no specific<br>difficulty. No attack requirements are present.                                                                                                                                                                                                                                 |
| Privileges Required                  | None    | No privileges are required for an attacker to successfully<br>exploit the vulnerability.                                                                                                                                                                                                                                                 |
| User Interaction                     | Passive | A user, other than the attacker, must be present for the<br>vulnerability to be exploited. However, the actions taken by<br>the user are typical, because a user must open a file within<br>the vulnerable application.                                                                                                                  |
| Vulnerable System<br>Confidentiality | High    | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.                                                                                                                                                                                                                                               |
| Vulnerable System<br>Integrity       | High    | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.                                                                                                                                                                                                                                               |
| Vulnerable System<br>Availability    | High    | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.                                                                                                                                                                                                                                               |
| Subsequent System<br>Confidentiality | None    | The impact on confidentiality is limited to the vulnerable<br>system. No direct downstream impact is indicated.                                                                                                                                                                                                                          |
| Subsequent System<br>Integrity       | None    | The impact on integrity is limited to the vulnerable system.<br>No direct downstream impact is indicated.                                                                                                                                                                                                                                |
| Subsequent System<br>Availability    | None    | The impact on availability is limited to the vulnerable<br>system. No direct downstream impact is indicated.                                                                                                                                                                                                                             |
| Safety                               | Present | The impact from an attacker gaining full control of<br>software that is running on a programmable logic<br>controller (PLC) may meet the definition of IEC 61508<br>consequence category marginal, critical or catastrophic<br>for certain usage of the PLC in an Operational Technology<br>(OT) environment where humans may be harmed. |

![](_page_65_Picture_0.jpeg)

# Operational Technology (OT) (CVE-2022-47379)

An authenticated, remote attacker may use an out-of-bounds write vulnerability in multiple CODESYS products in multiple versions to write data into memory which can lead to a denial-of-service condition, memory overwriting, or remote code execution.

| v3.1                                             | v4.0                                                                                  |
|--------------------------------------------------|---------------------------------------------------------------------------------------|
| 8.8                                              | 9.4                                                                                   |
| CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:<br>H/I:H/A:H | CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H<br>/SI:H/SA:H/S:P/AU:Y/V:C/RE:L |

## CVSS v4 Score: Base 9.4

| Metric                               | Value  | Comments                                                                                                 |
|--------------------------------------|--------|----------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Remote | The vulnerable system is accessible from remote networks.                                                |
| Attack Complexity                    | Low    | No specialized conditions or advanced knowledge are<br>required.                                         |
| Attack Requirements                  | None   | The attacker can execute the exploit with no specific<br>difficulty. No attack requirements are present. |
| Privileges Required                  | Low    | The attacker must require privileges sufficient to access the<br>device.                                 |
| User Interaction                     | None   | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.            |
| Vulnerable System<br>Confidentiality | High   | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.               |
| Vulnerable System<br>Integrity       | High   | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.               |
| Vulnerable System<br>Availability    | High   | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.               |
| Subsequent System<br>Confidentiality | High   | The attacker could impact the confidentiality of connected<br>OT devices.                                |
| Subsequent System                    | High   | The attacker could impact the integrity of connected OT                                                  |

![](_page_66_Picture_0.jpeg)

| Integrity                         |              | devices.                                                                                                                                                                                                                                                           |
|-----------------------------------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Subsequent System<br>Availability | High         | The attacker could impact the availability of connected OT<br>devices.                                                                                                                                                                                             |
| Safety                            | Present      | Connections to OT devices can impact the safety of<br>humans and may meet the definition of IEC 61508<br>consequence category marginal, critical or catastrophic<br>for certain usage in an Operational Technology (OT)<br>environment where humans may be harmed. |
| Automatable                       | Yes          | Attacks against the vulnerability can be performed in an<br>automated fashion with little oversight against multiple<br>targets.                                                                                                                                   |
| Value Density                     | Concentrated | The value of OT devices in a facility has a highly<br>concentrated value as a target.                                                                                                                                                                              |
| Vulnerability<br>Response Effort  | Low          | A simple device reboot would correct the issue.                                                                                                                                                                                                                    |

#### Variation 1: Elevator Operational Technology

In this variation of the vulnerability, the vulnerable device manages an elevator. The following metric score variation demonstrates the possible impacts of an exploit against such a deployment.

| B+E v4.0                                                                                                                                                                   |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 7.0                                                                                                                                                                        |
| CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/V<br>C:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:<br>L/IR:H/AR:L/MAV:L/MAC:H/MAT:N/MAT:N/MP<br>R:N/MUI:N/MVC:N/MVI:H/MVA:L/MSC<br>:N/MSI:S/MSA:L |

## Variation 1: CVSS v4 Score: B+E 7.0

| Metric | Value | nmment |
|--------|-------|--------|
|        |       |        |

![](_page_67_Picture_0.jpeg)

| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                                |
|--------------------------------------|---------|----------------------------------------------------------------------------------------------------------|
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                         |
| Attack Requirements                  | None    | The attacker can execute the exploit with no specific<br>difficulty. No attack requirements are present. |
| Privileges Required                  | Low     | The attacker must require privileges sufficient to access the<br>device.                                 |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.            |
| Vulnerable System<br>Confidentiality | High    | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.               |
| Vulnerable System<br>Integrity       | High    | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.               |
| Vulnerable System<br>Availability    | High    | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.               |
| Subsequent System<br>Confidentiality | High    | The attacker could impact the confidentiality of connected<br>OT devices.                                |
| Subsequent System<br>Integrity       | High    | The attacker could impact the confidentiality of connected<br>OT devices.                                |
| Subsequent System<br>Availability    | High    | The attacker could impact the confidentiality of connected<br>OT devices.                                |
| Modified Attack<br>Vector            | Local   | The system is disconnected from the Internet.                                                            |
| Modified Attack<br>Complexity        | High    | There are FW and Data Diodes that prevent access to the<br>PLC.                                          |
| Modified Attack<br>Requirements      | None    | Same as Base.                                                                                            |
| Modified Privileges<br>Required      | Low     | Same as Base.                                                                                            |
| Modified User<br>Interaction         | None    | Same as Base.                                                                                            |
| Modified Vulnerable                  | None    | No sensitive information contained within the PLC.                                                       |

![](_page_68_Picture_0.jpeg)

| System<br>Confidentiality                        |      |                                                                                  |
|--------------------------------------------------|------|----------------------------------------------------------------------------------|
| Modified Vulnerable<br>System Integrity          | High | The attacker could modify the operation of the elevator.                         |
| Modified Vulnerable<br>System Availability       | Low  | Loss of an elevator compensated by other facility features.                      |
| Modified Subsequent<br>System<br>Confidentiality | None | No sensitive information contained within the elevator<br>device.                |
| Modified Subsequent<br>System Integrity          | High | The attacker could modify the operation of the elevator.                         |
| Modified Subsequent   Low<br>System Availability |      | Loss of an elevator compensated by other facility features.                      |
| Confidentiality<br>Requirements                  | Low  | The system contains no secrets and the requirement is<br>reduced.                |
| Integrity<br>Requirements                        | High | There could be a high risk of injury during malfunction to<br>operations.        |
| Availability<br>Requirements                     | Low  | Facility redundancy of other elevators reduces the<br>availability requirements. |

## Variation 2: Oil Field Facility Operational Technology

In this variation of the vulnerability, the vulnerable device manages a facility such as an oil field. The following metric score variation demonstrates the possible impacts of an exploit against such a deployment.

| B+E v4.0                                                                                                     |
|--------------------------------------------------------------------------------------------------------------|
| 7.4                                                                                                          |
| CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/V<br>C:H/VI:H/VA:H/SC:H/SI:H/SA:H/MAV:A/<br>MAC:H/MAT:N/MPR:L/MUI:N/MVC:L/ |

![](_page_69_Picture_0.jpeg)

MVI:H/MVA:H/MSC:L/MSI:S/MSA:S/CR :L/IR:H/AR:H/E:P

## Variation 1: CVSS v4 Score: B+E 7.4

| Metric                               | Value    | Comments                                                                                                                               |
|--------------------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------|
| Attack Vector                        | Network  | The vulnerable system is accessible from remote networks.                                                                              |
| Attack Complexity                    | Low      | No specialized conditions or advanced knowledge are<br>required.                                                                       |
| Attack Requirements                  | None     | The attacker can execute the exploit with no specific<br>difficulty. No attack requirements are present.                               |
| Privileges Required                  | None     | The attacker must require privileges sufficient to access the<br>device.                                                               |
| User Interaction                     | None     | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                          |
| Vulnerable System<br>Confidentiality | High     | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.                                             |
| Vulnerable System<br>Integrity       | High     | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.                                             |
| Vulnerable System<br>Availability    | High     | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.                                             |
| Subsequent System<br>Confidentiality | High     | The attacker could impact the confidentiality of connected<br>OT devices.                                                              |
| Subsequent System<br>Integrity       | High     | The attacker could impact the confidentiality of connected<br>OT devices.                                                              |
| Subsequent System<br>Availability    | High     | The attacker could impact the confidentiality of connected<br>OT devices.                                                              |
| Modified Attack<br>Vector            | Adjacent | The system is disconnected from the Internet. However<br>there is a possibility for lateral control from nearby<br>management systems. |
| Modified Attack<br>Complexity        | High     | There are FW and Data Diodes that prevent access to the<br>PLC.                                                                        |

![](_page_70_Picture_0.jpeg)

| Modified Attack<br>Requirements                  | None   | Same as Base.                                                                                              |  |
|--------------------------------------------------|--------|------------------------------------------------------------------------------------------------------------|--|
| Modified Privileges<br>Required                  | Low    | Same as Base.                                                                                              |  |
| Modified User<br>Interaction                     | None   | Same as Base.                                                                                              |  |
| Modified Vulnerable<br>System<br>Confidentiality | Low    | The attacker could recover some information regarding<br>facility data.                                    |  |
| Modified Vulnerable<br>System Integrity          | High   | The attacker could modify the operation of the facility.                                                   |  |
| Modified Vulnerable<br>System Availability       | High   | The attacker could impact the availability of the PLC.                                                     |  |
| Modified Subsequent<br>System<br>Confidentiality | Low    | The attacker could recover information regarding<br>production facility data.                              |  |
| Modified Subsequent<br>System Integrity          | Safety | The attacker could modify the facility operations, possibly<br>impacting the safety of facility personnel. |  |
| Modified Subsequent<br>System Availability       | Safety | The attacker could impact facility availability, possibly<br>impacting the safety of facility personnel.   |  |
| Confidentiality<br>Requirements                  | High   | The device and facility may hold trade secrets.                                                            |  |
| Integrity<br>Requirements                        | High   | Improper operation of the facility could impact the safety<br>of nearby personnel.                         |  |
| Availability<br>Requirements                     | High   | Equipment failure could result in facility downtime.                                                       |  |

## Variation 3: Assembly Line Robots Operational Technology

In this variation of the vulnerability, the vulnerable device manages robotic devices in an assembly line. The following metric score variation demonstrates the possible impacts of an exploit against such a deployment.

![](_page_71_Picture_0.jpeg)

#### B+E v4.0

8.7

CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/V C:H/VI:H/VA:H/SC:H/SI:H/SA:H/MAV:N /MAC:H/MAT:N/MPR:L/MUI:N/MVC:H/ MVI:H/MVA:H/MSC:H/MSI:S/MSA:H/C R:M/IR:H/AR:M/E:P

## Variation 3: CVSS v4 Score: B+E 8.7

| Metric                               | Value   | Comments                                                                                                 |  |
|--------------------------------------|---------|----------------------------------------------------------------------------------------------------------|--|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                                |  |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                         |  |
| Attack Requirements                  | None    | The attacker can execute the exploit with no specific<br>difficulty. No attack requirements are present. |  |
| Privileges Required                  | None    | The attacker must require privileges sufficient to access the<br>device.                                 |  |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.            |  |
| Vulnerable System<br>Confidentiality | High    | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.               |  |
| Vulnerable System<br>Integrity       | High    | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.               |  |
| Vulnerable System<br>Availability    | High    | Exploitation of the vulnerability results in complete control<br>of the vulnerable system.               |  |
| Subsequent System<br>Confidentiality | High    | The attacker could impact the confidentiality of connected<br>OT devices.                                |  |
| Subsequent System<br>Integrity       | High    | The attacker could impact the confidentiality of connected<br>OT devices.                                |  |

![](_page_72_Picture_0.jpeg)

| Subsequent System<br>Availability                | High    | The attacker could impact the confidentiality of connected<br>OT devices.                                                |  |
|--------------------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------------|--|
| Modified Attack<br>Vector                        | Network | The system is connected to the Internet for maintenance<br>and services by the robot's suppliers.                        |  |
| Modified Attack<br>Complexity                    | High    | There are FW and Data Diodes that prevent access to the<br>PLC.                                                          |  |
| Modified Attack<br>Requirements                  | None    | Same as Base.                                                                                                            |  |
| Modified Privileges<br>Required                  | Low     | Same as Base.                                                                                                            |  |
| Modified User<br>Interaction                     | None    | Same as Base.                                                                                                            |  |
| Modified Vulnerable<br>System<br>Confidentiality | High    | The attacker could recover highly valuable information<br>regarding production line data.                                |  |
| Modified Vulnerable<br>System Integrity          | High    | The attacker could modify the operation of the PLC.                                                                      |  |
| Modified Vulnerable<br>System Availability       | High    | The attacker could cause the PLC to stop responding.                                                                     |  |
| Modified Subsequent<br>System<br>Confidentiality | High    | Potential loss of production data from the connected<br>robotic device.                                                  |  |
| Modified Subsequent<br>System Integrity          | Safety  | Improper operation of robotic devices could impact the<br>safety of nearby personnel.                                    |  |
| Modified Subsequent<br>System Availability       | High    | Equipment failure could result in line downtime.                                                                         |  |
| Confidentiality<br>Requirements                  | Medium  | The line contains valuable information.                                                                                  |  |
| Integrity<br>Requirements                        | High    | lmpact to functionality could risk damage to facility and<br>personnel.                                                  |  |
| Availability<br>Requirements                     | Medium  | Although the line should be operational at all times, there<br>is no risk to operators in event of loss of availability. |  |

![](_page_73_Picture_0.jpeg)

# IOT - Healthcare (CVE-2020-10627)

Description:

Insulet Omnipod Insulin Management System insulin pump product ID 19191 and 40160 is designed to communicate using a wireless RF with an Insulet manufactured Personal Diabetes Manager device. This wireless RF communication protocol does not properly implement authentication or authorization. An attacker with access to one of the affected insulin pump models may be able to modify and/or intercept data. This vulnerability could also allow attackers to change pump settings and control insulin delivery.

|                         | v3.1                                                    | v4.0                                                                                     |
|-------------------------|---------------------------------------------------------|------------------------------------------------------------------------------------------|
| Base                    | 8.1<br>CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/<br>C:H/I:H/A:N | 8.6<br>CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:<br>N/VC:H/VI:H/VA:N/SC:N/SI:N/SI:N/SA:N/<br>S:P  |
| Base +<br>Environmental |                                                         | 9.7<br>CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:<br>N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/<br>MSI:S/S:P |

## CVSS v4 Score: Base + Environmental 9.7

| Metric                     | Value    | Comments                                                         |
|----------------------------|----------|------------------------------------------------------------------|
| Attack Vector              | Adjacent | An attacker must be within the local proximity of the<br>device. |
| Attack Complexity          | Low      | No specialized conditions or advanced knowledge are<br>required. |
| Attack Requirements   None |          | No attack requirements are present.                              |
| l Privileges Required      | None     | No attack requirements are present.                              |
| User Interaction           | None     | No user interaction is required for an attacker to               |

![](_page_74_Picture_0.jpeg)

|                                      |            | successfully exploit the vulnerability.                                                                                                      |  |
|--------------------------------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------|--|
| Vulnerable System<br>Confidentiality | High       | An attacker could exploit the vulnerability to intercept<br>critical data.                                                                   |  |
| Vulnerable System<br>Integrity       | High       | An attacker could exploit the vulnerability to change pump<br>settings and control insulin delivery.                                         |  |
| Vulnerable System<br>Availability    | None       | There is no impact to the vulnerable system availability.                                                                                    |  |
| Subsequent System<br>Confidentiality | None       | There is no impact to subsequent systems.                                                                                                    |  |
| Subsequent System<br>Integrity       | None       | There is no impact to subsequent systems.                                                                                                    |  |
| Subsequent System<br>Availability    | None       | There is no impact to subsequent systems.                                                                                                    |  |
| Exploit Maturity                     | Unreported | There is no known proof-of-concept code or malicious<br>exploitation of this vulnerability.                                                  |  |
| Modified Subsequent<br>System        | Safety     | Because control of insulin delivery can be changed, there is<br>a health and human safety impact.                                            |  |
| Safety                               | Present    | lmpact on health and human safety from a vulnerability in<br>an OT device may meet definition of IEC 61508<br>consequence category critical. |  |

# Value Density (CVE-2020-28196)

Description:

MIT Kerberos 5 (aka krb5) before 1.17.2 and 1.18.x before 1.18.3 allows unbounded recursion via an ASN.1-encoded Kerberos message because the lib/krb5/asn.1/asn1_encode.c support for BER indefinite lengths lacks a recursion limit.

|      | v3.1                                                    | v4.0 Base                                                                            |
|------|---------------------------------------------------------|--------------------------------------------------------------------------------------|
| Base | 7.5<br>CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/<br>C:N/I:N/A:H | ، 8.7<br>CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:<br>N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/<br>V:C |

![](_page_75_Picture_0.jpeg)

## CVSS v4 Score: Base 8.7

| Metric                               | Value        | Comments                                                                                                        |  |
|--------------------------------------|--------------|-----------------------------------------------------------------------------------------------------------------|--|
| Attack Vector                        | Network      | The vulnerable system is accessible from remote networks.                                                       |  |
| Attack Complexity                    | Low          | No specialized conditions or advanced knowledge are<br>required.                                                |  |
| Attack Requirements                  | None         | No attack requirements are present.                                                                             |  |
| Privileges Required                  | None         | No attack requirements are present.                                                                             |  |
| User Interaction                     | None         | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                   |  |
| Vulnerable System<br>Confidentiality | None         | There is no impact to the vulnerable system confidentiality.                                                    |  |
| Vulnerable System<br>Integrity       | None         | There is no impact to the vulnerable system integrity.                                                          |  |
| Vulnerable System<br>Availability    | High         | An attacker could cause the application to fail and restart,<br>resulting in a denial of service condition.     |  |
| Subsequent System<br>Confidentiality | None         | There is no impact to subsequent systems.                                                                       |  |
| Subsequent System<br>Integrity       | None         | There is no impact to subsequent systems.                                                                       |  |
| Subsequent System<br>Availability    | None         | There is no impact to subsequent systems.                                                                       |  |
| Value Density                        | Concentrated | The value of the Kerberos system is highly concentrated<br>due to its functionality in the network environment. |  |

## Management System (CVE-2023-20048)

Description:

A vulnerability in the web services interface of Cisco Firepower Management Center (FMC) Software could allow an authenticated, remote attacker to execute certain unauthorized configuration commands on a Firepower Threat Defense (FTD) device that is managed by the FMC Software.

![](_page_76_Picture_0.jpeg)

This vulnerability is due to insufficient authorization of configuration commands that are sent through the web service interface. An attacker could exploit this vulnerability by authenticating to the FMC web services interface and sending a crafted HTTP request to an affected device. A successful exploit could allow the attacker to execute certain configuration commands on the targeted FTD device. To successfully exploit this vulnerability, an attacker would need valid credentials on the FMC Software.

#### Notes:

The vulnerable system is the Firepower Management Center. The subsequent systems are devices managed by the FMC, such as FTD devices. Vulnerability impacts are then limited only to systems managed by the FMC. For the resulting CVSS metrics, there are only subsequent system impacts. There are no additional impacts on the vulnerable system.

|      | v3.1                                                      | v4.0 Base                                                                      | v4.0 BTE                                                                                             |
|------|-----------------------------------------------------------|--------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| Base | ਰੇ ਰੇ<br>CVSS:3.1/AV:N/AC:L/PR:L<br>/UI:N/S:C/C:H/I:L/A:H | 6.4<br>CVSS:4.0/AV:N/AC:L/AT:N<br>/PR:L/UI:N/VC:N/VI:N/VA:<br>N/SC:H/Sl:L/SA:H | 2.4<br>CVSS:4.0/AV:N/AC:L/AT:N<br>/PR:L/UI:N/VC:N/VI:N/VA:<br>N/SC:H/Sl:L/SA:H/E:U/M<br>AV:A/R:U/V:C |

## CVSS v4 Score: Base 6.4

| Metric                               | Value   | Comments                                                                                                                                                                 |  |
|--------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| Attack Vector                        | Network | The vulnerable system is accessible from remote networks.                                                                                                                |  |
| Attack Complexity                    | Low     | No specialized conditions or advanced knowledge are<br>required.                                                                                                         |  |
| Attack Requirements   None           |         | No attack requirements are present.                                                                                                                                      |  |
| Privileges Required                  | Low     | An attacker must have privileges sufficient to log in to the<br>application web-based management interface.                                                              |  |
| User Interaction                     | None    | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.                                                                            |  |
| Vulnerable System<br>Confidentiality | None    | There is no impact to the vulnerable system confidentiality.<br>An attacker would gain no additional privileges on the<br>vulnerable system as a result of exploitation. |  |

![](_page_77_Picture_0.jpeg)

| Vulnerable System<br>Integrity       | None | There is no impact to the vulnerable system integrity. An<br>attacker would gain no additional privileges on the<br>vulnerable system as a result of exploitation.    |
|--------------------------------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vulnerable System<br>Availability    | None | There is no impact to the vulnerable system availability. An<br>attacker would gain no additional privileges on the<br>vulnerable system as a result of exploitation. |
| Subsequent System<br>Confidentiality | High | An attacker could execute arbitrary commands on the<br>managed devices and gain access to sensitive information.                                                      |
| Subsequent System<br>Integrity       | Low  | An attacker could execute arbitrary commands on the<br>managed devices and change files or modify the<br>configuration.                                               |
| Subsequent System<br>Availability    | High | An attacker could execute arbitrary commands on the<br>managed devices and turn off or disable the device.                                                            |

## CVSS v4 Score: BTE 2.4

The following threat and environmental metrics further enrich the Management System CVE-2023-20048 example. The scoring scenario shows a Threat metric value of Unreported, and the Modified Attack Vector modified to Adjacent. In this scenario, network-based access controls restrict access to the affected system, changing the expected attack vector for vulnerable systems in this environment.

Additional Supplemental Metrics are chosen to provide more context to the nature of the vulnerability and the affected product, given the importance of the device in most environments.

Refer as well to the full CVSS BTE vector string above.

| Metric                    | Value      | Comments                                                                                                                                                              |
|---------------------------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Threat                    | Unreported | No known public exploit exists.                                                                                                                                       |
| Modified Attack<br>Vector | Adjacent   | The vulnerable system is not accessible from remote<br>networks. The system is protected by network access<br>control and access is restricted only to trusted hosts. |
| Recovery                  | User       | An exploited device does not recover on its own, and an<br>administrator must reconfigure and recover impacted<br>devices manually.                                   |

![](_page_78_Picture_0.jpeg)

| Value Density |  | Concentrated   An attacker who could exploit this vulnerability could gain |
|---------------|--|----------------------------------------------------------------------------|
|               |  | control over managed devices that serve as network                         |
|               |  | filtering devices.                                                         |

## Management System (CVE-2023-30911)

Description:

HPE Integrated Lights-Out 5, and Integrated Lights-Out 6 using iLOrest may cause denial of service.

Notes:

Recommended security guidelines instruct deployment of such systems on a private management network. Assessment by an analyst of a reasonable worst-case scenario considers the vendor's recommended deployment guideline in restricting access to impacted systems.

|      | v3.1                                                    | v4.0 Base                                                                  |
|------|---------------------------------------------------------|----------------------------------------------------------------------------|
| Base | 9.9<br>CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H<br>/I:L/A:H | 6.4<br>CVSS:4.0/AV:N/AC:L/AT:N/PR;L/UI:N/V<br>C:N/VI:N/VA:N/SC:H/SI:L/SA:H |

## CVSS v4 Score: Base 6.4

| Metric                     | Value    | Comments                                                                                                    |
|----------------------------|----------|-------------------------------------------------------------------------------------------------------------|
| Attack Vector              | Adjacent | The vulnerable system is accessible from remote networks.                                                   |
| Attack Complexity          | Low      | No specialized conditions or advanced knowledge are<br>required.                                            |
| Attack Requirements   None |          | No attack requirements are present.                                                                         |
| Privileges Required        | Low      | An attacker must have privileges sufficient to log in to the<br>application web-based management interface. |
| User Interaction           | None     | No user interaction is required for an attacker to<br>successfully exploit the vulnerability.               |
| Vulnerable System          | None     | There is no impact to the vulnerable system confidentiality.                                                |

![](_page_79_Picture_0.jpeg)

| Confidentiality                      |      | An attacker would gain no additional privileges on the<br>vulnerable system as a result of exploitation.                                                              |
|--------------------------------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Vulnerable System<br>Integrity       | None | There is no impact to the vulnerable system integrity. An<br>attacker would gain no additional privileges on the<br>vulnerable system as a result of exploitation.    |
| Vulnerable System<br>Availability    | None | There is no impact to the vulnerable system availability. An<br>attacker would gain no additional privileges on the<br>vulnerable system as a result of exploitation. |
| Subsequent System<br>Confidentiality | High | An attacker could execute arbitrary commands on the<br>managed devices and gain access to sensitive information.                                                      |
| Subsequent System<br>Integrity       | Low  | An attacker could execute arbitrary commands on the<br>managed devices and change files or modify the<br>configuration.                                               |
| Subsequent System<br>Availability    | High | An attacker could execute arbitrary commands on the<br>managed devices and turn off or disable the device.                                                            |

# Version History

| Date       | Ver  | Description                                                                                                                                                                     |
|------------|------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2023-08-10 | v0.1 | Initial Publication                                                                                                                                                             |
| 2023-09-29 | v0.2 | Grammatical editing changes, updated metrics score comments, and<br>corrected metric score mismatches. Updated CVE-2021-44228                                                   |
| 2023-10-30 | v0.3 | Added new examples for Value Density (CVE-2020-28196) and Safety<br>(CVE-2023-30560). Additional error corrections                                                              |
| 2023-11-01 | v1.0 | Official Release                                                                                                                                                                |
| 2024-02-01 | v1.1 | Error corrections in CVE-2020-3549 and CVE-2013-6014. Additional<br>examples for CVE-2022-47379 OT and CVE-2023-20245 ACL bypass.                                               |
| 2024-07-13 | v1.2 | Additional example for subsequent system (CVE-2023-20048)<br>Additional example for SSRF (CVE-2024-1233)<br>Additional example for CSRF (CVE-2023-5602), see accompanying entry |

![](_page_80_Picture_0.jpeg)

|            |            | in FAQ<br>Additional example, regreSSHion (CVE-2024-6387)                                                                                                                                                                                                                                                                                                                                                                                   |
|------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2024-12-12 | v1.3       | Additional example for subsequent system (CVE-2023-48228)<br>Included more detailed descriptions for metric choices to describe<br>vulnerable and subsequent systems (CVE-2020-3947)<br>Corrected examples for subsequent system (CVE-2016-5729,<br>CVE-2015-2890, CVE-2018-3652, CVE-2021-44228)                                                                                                                                           |
| 2025-03-14 | v1.4       | Including new section for CISA KEV example, currently CVE-2025-24201.<br>Adding variation example for XSS to show evaluation for vulnerable<br>system impact (CVE-2022-24682). Additional XSS example for<br>vulnerable system impact (CVE-2024-55228). Error correction on v4.0<br>Base score for CVE-2021-44228. Updating examples to include<br>variations for Threat and Environmental metrics for CVE-2023-20245<br>and CVE-2023-20048 |
| 2025-04-30 | v1.4<br>.1 | Rotated CISA KEV example, replaced CVE-2025-24201, added<br>CVE-2025-31324                                                                                                                                                                                                                                                                                                                                                                  |