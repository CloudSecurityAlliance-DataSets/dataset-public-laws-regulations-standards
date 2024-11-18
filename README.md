# AI Security Resources Categorized

This is a public repository of public laws, regulations, standards and so on that are related to cloud and AI security. Please note that many items will be mentioned in this repo but the actual data is not present due to licensing issues (e.g. the ISO standards and IEEE documents). 

## Categories and types of data:

### Acts and Regulations
- EU AI Act: Regulation governing AI use and governance in the EU.
- EU DORA (Digital Operational Resilience Act): Focuses on cybersecurity and operational resilience in financial institutions.
- EU GDPR Act: General Data Protection Regulation (GDPR).

### International Standards
- NIST AI Risk Management Framework (RMF) AI-600: Framework for managing risks associated with AI systems, promoting trustworthy and responsible development and use.

- ISO/IEC 42001: Specifies requirements for establishing, implementing, maintaining, and continually improving an AI management system within organizations.
- IEEE 7001-2021: Standard for Transparency of Autonomous Systems, providing guidelines to ensure transparency in AI operations.
- OECD AI Principles: International recommendations focusing on the responsible development of AI, including security and trustworthiness.

### Industry-Specific Security Controls
- IBM Generative AI Security Controls: Best practices for securing generative AI systems.

- Microsoft AI Security Guidelines: Security principles for AI solutions.
- Google Responsible AI Practices: Emphasizes security, fairness, and transparency in AI development.
- OpenAI Safety Guidelines: Practices for secure and aligned AI model deployment.

### Control Frameworks and Matrices
- AI Controls Matrix (CSA): Security and compliance framework for AI systems.
- MITRE ATLAS: Framework categorizing adversarial threats to AI.

### Research and Academic Studies
- arXiv.org Papers: Preprints on adversarial AI, robustness, and alignment research.
- OpenAI Safety Papers: Research on secure and responsible AI development.

### News and Current Affairs
- AI Security Incidents: Reports on real-world AI security breaches.
- Industry News Analysis: Coverage of trends and challenges in AI security.
- TechCrunch Articles on AI: Updates on AI security initiatives from major tech companies.
- The New York Times: Articles on government and industry AI security developments.

### Policy Proposals and Government Guidance
- White House Memos on AI: Proposals outlining national AI security strategies.
- U.S. National AI Initiative: Government-wide strategic plan for AI governance.

## Layout of the data

* country
    * EU
    * Germany
* companies
    * Amazon
    * CISCO
    * ...
* organizations
    * CSA
    * MITRE
    * ...
* working (copies of documents that are frequently used)

## Data conversion notes

For PDF we mostly use [marker](https://github.com/VikParuchuri/marker) with the command:

```
marker_single file.pdf ./ --ocr_all_pages
```

We generally convert the data to markdown, then split it up into a csv sheet (e.g. each article or control becomes a row), and from this we also commonly create a JSON file.
