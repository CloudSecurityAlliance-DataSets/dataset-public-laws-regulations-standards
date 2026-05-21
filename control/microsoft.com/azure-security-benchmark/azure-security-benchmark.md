[ Skip to main content ](#main) [ Skip to Ask Learn chat experience ](#)

This browser is no longer supported.

Upgrade to Microsoft Edge to take advantage of the latest features, security
updates, and technical support.

[ Download Microsoft Edge ](https://go.microsoft.com/fwlink/p/?LinkID=2092881
) [ More info about Internet Explorer and Microsoft Edge
](https://learn.microsoft.com/en-us/lifecycle/faq/internet-explorer-microsoft-
edge)

Table of contents  Exit editor mode

Ask Learn Ask Learn

Reading mode Table of contents [ Read in English ](#) Add Add to plan [ Edit
]()

* * *

Copy Markdown Print

* * *

Note

Access to this page requires authorization. You can try [signing in](#) or
changing directories.

Access to this page requires authorization. You can try changing directories.

# Overview of Microsoft cloud security benchmark v2 (preview)

Feedback

Summarize this article for me

##  In this article

For an introduction to the Microsoft cloud security benchmark project,
including key concepts, implementation guidance, and terminology, see the
[Microsoft cloud security benchmark introduction](introduction).

The Microsoft cloud security benchmark v2 (preview) provides enhanced Azure-
focused guidance with expanded security domains and comprehensive technical
implementation details. This version builds upon the foundation of the
Microsoft cloud security benchmark with refined security controls, AI security
guidance, and expanded Azure Policy mappings.

## Key features

Note

Microsoft cloud security benchmark v2 is currently in preview. This version
supersedes [Microsoft cloud security benchmark v1](overview-mcsb-v1). We
welcome your feedback to help improve it. For any questions or comments, email
us at
[benchmarkfeedback@microsoft.com](mailto:benchmarkfeedback@microsoft.com).

The Microsoft cloud security benchmark v2 (preview) includes:

  1. **Artificial Intelligence Security** \- A new security domain with seven recommendations covering AI platform security, AI application security, and AI security monitoring to address threats and risks in artificial intelligence deployments.

  2. **Comprehensive Azure Policy mappings** \- More than 420 Azure Policy built-in definitions to help you measure and monitor your security posture in Azure by using **Azure Policy** and **Defender for Cloud**.

  3. **Risk and threat-based guidance** \- Comprehensive guidelines with granular technical implementation examples and detailed references to help you understand the security risks and threats that each security control mitigates, and how to implement the security controls in your Azure environment.

## Security domains

Security domain | Description  
---|---  
[Network security (NS)](mcsb-v2-network-security) | Network Security covers controls to secure and protect networks, including securing virtual networks, establishing private connections, preventing and mitigating external attacks, and securing DNS.  
[Identity Management (IM)](mcsb-v2-identity-management) | Identity Management covers controls to establish a secure identity and access controls by using identity and access management systems, including the use of single sign-on, strong authentications, managed identities (and service principals) for applications, conditional access, and account anomalies monitoring.  
[Privileged Access (PA)](mcsb-v2-privileged-access) | Privileged Access covers controls to protect privileged access to your tenant and resources, including a range of controls to protect your administrative model, administrative accounts, and privileged access workstations against deliberate and inadvertent risk.  
[Data Protection (DP)](mcsb-v2-data-protection) | Data Protection covers control of data protection at rest, in transit, and via authorized access mechanisms, including discover, classify, protect, and monitor sensitive data assets by using access control, encryption, key management, and certificate management.  
[Asset Management (AM)](mcsb-v2-asset-management) | Asset Management covers controls to ensure security visibility and governance over your resources, including recommendations on permissions for security personnel, security access to asset inventory, and managing approvals for services and resources (inventory, track, and correct).  
[Logging and Threat Detection (LT)](mcsb-v2-logging-threat-detection) | Logging and Threat Detection covers controls for detecting threats on cloud, and enabling, collecting, and storing audit logs for cloud services, including enabling detection, investigation, and remediation processes with controls to generate high-quality alerts with native threat detection in cloud services. It also includes collecting logs with a cloud monitoring service, centralizing security analysis with a SIEM, time synchronization, and log retention.  
[Incident Response (IR)](mcsb-v2-incident-response) | Incident Response covers controls in incident response life cycle - preparation, detection and analysis, containment, and post-incident activities, including using Azure services (such as Microsoft Defender for Cloud and Sentinel) and/or other cloud services to automate the incident response process.  
[Posture and Vulnerability Management (PV)](mcsb-v2-posture-vulnerability-management) | Posture and Vulnerability Management focuses on controls for assessing and improving cloud security posture, including vulnerability scanning, penetration testing and remediation, as well as security configuration tracking, reporting, and correction in cloud resources.  
[Endpoint Security (ES)](mcsb-v2-endpoint-security) | Endpoint Security covers controls in endpoint detection and response, including use of endpoint detection and response (EDR) and anti-malware service for endpoints in cloud environments.  
[Backup and Recovery (BR)](mcsb-v2-backup-recovery) | Backup and Recovery covers controls to ensure that data and configuration backups at the different service tiers are performed, validated, and protected.  
[DevOps Security (DS)](mcsb-v2-devops-security) | DevOps Security covers the controls related to the security engineering and operations in the DevOps processes, including deployment of critical security checks (such as static application security testing, vulnerability management) prior to the deployment phase to ensure the security throughout the DevOps process. It also includes common topics such as threat modeling and software supply security.  
[Artificial Intelligence Security (AI)](mcsb-v2-artificial-intelligence-security) | Artificial Intelligence Security covers controls to ensure the secure development, deployment, and operation of AI models and services, including AI platform security, AI application security and AI security monitoring.  
  
## Security control structure in Microsoft cloud security benchmark v2
(preview)

Each security control in the benchmark includes the following sections:

  * **ID** : A unique identifier for each security control, consisting of a domain abbreviation and number (for example, AI-1 for Artificial Intelligence Security control 1, DP-1 for Data Protection control 1, NS-2 for Network Security control 2). This ID is used throughout the documentation to reference specific security controls.
  * **Azure Policy** : Links to Azure built-in policy definitions that you can use to measure and enforce the security control. Note that not every security control includes an Azure Policy link, as some security controls provide guidance for scenarios or configurations that Azure Policy automation can't enforce.
  * **Security principle** : High-level description of the security control at the technology-agnostic level, explaining the "what" and "why" of the security control.
  * **Risk to mitigate** : The specific security risks and threats that the security control aims to address.
  * **MITRE ATT &CK**: The MITRE ATT&CK tactics, techniques, and procedures (TTPs) relevant to the security risks. Learn more at <https://attack.mitre.org/>.
  * **Implementation guidance** : Detailed Azure-specific technical guidance organized in numbered sub-sections (for example, NS-1.1, NS-1.2) explaining how to implement the security control using Azure features and services.
  * **Implementation example** : Practical real-world scenario demonstrating how to implement the security control, including the challenge, solution approach, and outcome.
  * **Criticality level** : Indicates the relative importance of the security control for security posture. Possible values are "Must have" (essential for baseline security), "Should have" (important for enhanced security), or "Nice to have" (beneficial for advanced security scenarios).
  * **Control Mapping** : Mappings to industry security standards and frameworks, including: 
    * **[NIST SP 800-53 Rev.5](https://csrc.nist.gov/pubs/sp/800/53/r5/final)** : NIST SP 800-53 r5 security control IDs
    * **[PCI-DSS v4](https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf)** : PCI-DSS v4 requirement IDs
    * **[CIS Controls v8.1](https://www.cisecurity.org/controls/v8)** : CIS Controls v8.1 IDs
    * **[NIST CSF v2.0](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final)** : NIST Cybersecurity Framework v2.0 function and category IDs
    * **[ISO 27001:2022](https://www.iso.org/standard/27001)** : ISO/IEC 27001:2022 security control IDs
    * **[SOC 2](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2)** : SOC 2 Trust Services Criteria

The security control mappings between MCSB and industry benchmarks (such as
CIS, NIST, PCI, ISO, and others) only indicate that you can use specific Azure
features to fully or partially address a security control requirement defined
in these industry benchmarks. Such implementation doesn't necessarily
translate to the full compliance of the corresponding security controls in
these industry benchmarks.

We welcome your detailed feedback and active participation in the Microsoft
cloud security benchmark effort. If you want to provide direct input, email us
at [benchmarkfeedback@microsoft.com](mailto:benchmarkfeedback@microsoft.com).

## Next steps

  * Review the [Microsoft cloud security benchmark introduction](introduction) for general MCSB concepts and implementation guidance
  * Explore the security domains starting with [Network security](mcsb-v2-network-security)
  * See the [MCSB v2 to CIS Controls mapping](mcsb-v2-cis-controls-mapping) for a consolidated view of all CIS Controls v8.1 mappings
  * Learn about [Azure Security Fundamentals](/en-us/azure/security/fundamentals)

* * *

## Feedback

Was this page helpful?

Yes No No

Need help with this topic?

Want to try using Ask Learn to clarify or guide you through this topic?

Ask Learn Ask Learn

Suggest a fix?

* * *

##  Additional resources

* * *

  * Last updated on  2026-01-15 

### In this article

Was this page helpful?

Need help with this topic?

Want to try using Ask Learn to clarify or guide you through this topic?

Ask Learn Ask Learn

Suggest a fix?

[en-us](#)

[ Your Privacy Choices](https://aka.ms/yourcaliforniaprivacychoices)

Theme

  * Light 
  * Dark 
  * High contrast 

  *   * [AI Disclaimer](https://learn.microsoft.com/en-us/principles-for-ai-generated-content)
  * [Previous Versions](https://learn.microsoft.com/en-us/previous-versions/)
  * [Blog](https://techcommunity.microsoft.com/t5/microsoft-learn-blog/bg-p/MicrosoftLearnBlog)
  * [Contribute](https://learn.microsoft.com/en-us/contribute)
  * [Privacy](https://go.microsoft.com/fwlink/?LinkId=521839)
  * [Consumer Health Privacy](https://go.microsoft.com/fwlink/?linkid=2259814)
  * [Terms of Use](https://learn.microsoft.com/en-us/legal/termsofuse)
  * [Trademarks](https://www.microsoft.com/legal/intellectualproperty/Trademarks/)
  * © Microsoft 2026

