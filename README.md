# AI Security Resources Categorized

This is a comprehensive public repository of laws, regulations, standards, frameworks, best practices, and AI transparency documentation related to cloud and AI security. Our goal is to provide structured, searchable access to critical AI governance and security resources.

*Note: Some standards organizations (ISO, IEEE) require purchase for full access. For these, we provide information and links to official sources.*

## Repository Structure

The repository is organized into **7 main categories**:

### `/regulations-mandatory/`
**Legally binding laws and regulations**
- EU AI Act, GDPR, DORA
- US federal and state laws (CHIPS Act, state privacy laws)
- National regulations (China Cybersecurity Law, UK Online Safety Bill)
- Government executive orders and mandates

### `/standards-voluntary/`
**Technical standards and certifications**
- **ISO/IEC standards**
- **IEEE standards**
- **NIST publications**
- **Industry standards** (PCI-DSS, HITRUST, etc.)

### `/frameworks-guidance/`
**Security frameworks and guidance documents**
- **Government frameworks** (FedRAMP, NIST AI RMF, UK NCSC)
- **Industry frameworks** (CSA CCM, MITRE ATLAS, OWASP)
- **International guidance** (OECD AI Principles)

### `/best-practices/`
**Company and organizational best practices**
- **Company guidelines** (Microsoft, Google, IBM, OpenAI, Anthropic)
- **Research papers** and academic studies
- **Industry reports** and analysis

### `/model-cards/`
**AI model transparency documentation**
- **Company model cards** (Google BERT, Meta Llama models)
- **Government model documentation**
- **Research institution models** (Stanford, MIT)
- **Community/open source models** (HuggingFace, Stable Diffusion)

### `/system-cards/`
**AI system transparency documentation**
- **Company system cards** (OpenAI GPT-4, Meta Llama systems)
- **Government AI system documentation**
- **Research AI systems**
- **Community AI systems**

### `/tools-resources/`
**Templates, tools, and utilities**
- **Conversion scripts** and processing tools
- **Templates** for model cards, system cards, and documentation
- **Working files** and frequently used processed documents

## Core System Files

The repository is governed by several key files that define how everything works:

### `PROMPT-CLASSIFICATION.md`
**The complete classification guide** - This is the main reference for:
- How to classify and organize any document type
- Repository structure and naming conventions
- Metadata requirements and examples
- Model cards vs system cards differences
- Decision trees for edge cases

### `TEMPLATE-PROCESSING-NOTES.md`
**Workflow documentation template** - Use this for documents that undergo conversion:
- Conversion process steps (PDF→Markdown→CSV→JSON)
- Data removal and cleanup notes
- Quality validation documentation
- File tracking and provenance

### `README.json` (in each folder)
**Standardized metadata** - Every document folder contains:
- Classification and discovery metadata
- Security relevance descriptions
- Source links and licensing information
- Geographic and industry scope

## Data Processing Workflow

For documents requiring conversion, we follow a structured process:

### 1. **Document Acquisition**
```bash
# Download from official sources
wget [official-url] -O document.pdf
```

### 2. **PDF Conversion**
We primarily use [marker](https://github.com/VikParuchuri/marker) for PDF processing:
```bash
# Run the marker_single command to produce markdown output.
#marker_single --output_dir ./ --output_format markdown "$id.pdf"
#
# Use the script:
#
~/GitHub/CSA-utils/utils/convert-pdf-to-markdown.sh --input filename.pdf
```

### 3. **Structured Processing**
1. **Markdown creation** - Clean, readable format
2. **CSV extraction** - Each article/control becomes a row
3. **JSON structuring** - Machine-readable format with metadata
4. **Quality validation** - Accuracy and completeness checks

### 4. **Documentation**
- Create `README.json` with classification metadata
- Create `PROCESSING-NOTES.md` for complex conversions
- Track all generated files and processing decisions

## Categories and Coverage

### **Regulations & Laws**
- EU AI Act, GDPR, DORA
- US CHIPS Act, state privacy laws
- National cybersecurity laws
- Executive orders and government mandates

### **Standards & Frameworks**
- NIST AI Risk Management Framework (AI-600)
- ISO/IEC 42001 (AI Management Systems)
- IEEE 7001-2021 (Autonomous Systems Transparency)
- CSA AI Controls Matrix, MITRE ATLAS

### **Industry Best Practices**
- **Microsoft**: AI Security Guidelines
- **Google**: Responsible AI Practices, model cards
- **OpenAI**: Safety Guidelines, system cards
- **IBM**: Generative AI Security Controls
- **Anthropic**: Constitutional AI principles

### **AI Transparency Documentation**
- **Model Cards**: Technical documentation of individual ML models
- **System Cards**: Comprehensive AI system safety and deployment documentation
- **Safety Evaluations**: Red teaming and adversarial testing results
- **Performance Metrics**: Bias, fairness, and robustness analysis

## How to Use This Repository

### **Finding Documents**
1. **Browse by category** using the folder structure
2. **Check README.json** files for metadata and descriptions
3. **Use classification tags** to find related documents
4. **Follow source links** for official versions

### **Adding New Documents**
1. **Consult PROMPT-CLASSIFICATION.md** for proper categorization
2. **Create README.json** with required metadata
3. **Add PROCESSING-NOTES.md** if conversion was needed
4. **Follow naming conventions** and folder structure

### **Understanding Content**
- **ISO/IEEE standards**: Information and links provided
- **NIST publications**: Full content available
- **Government regulations**: Full content available
- **Company guidelines**: Full content available

## Repository Statistics

*[This section could be auto-generated with counts of documents by category]*

- **Regulations**: [X] mandatory laws and regulations
- **Standards**: [X] technical standards and certifications  
- **Frameworks**: [X] security frameworks and guidance documents
- **Best Practices**: [X] company and organizational guidelines
- **Model Cards**: [X] AI model transparency documents
- **System Cards**: [X] AI system transparency documents
- **Tools**: [X] templates, scripts, and utilities

## Contributing

Contributions are welcome! Please:
1. **Follow the classification guide** in `PROMPT-CLASSIFICATION.md`
2. **Include proper metadata** in `README.json` format
3. **Document processing steps** in `PROCESSING-NOTES.md` when applicable

## Contact & Support

For questions about document classification, processing workflows, or repository structure, please refer to the documentation files or open an issue.

---

*This repository serves as a comprehensive resource for AI governance, security, and transparency documentation. All content is organized for maximum discoverability and usability.*
