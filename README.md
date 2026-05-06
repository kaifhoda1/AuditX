# 🔐 AuditX — AI-Powered GRC Compliance Tool
**By ByteFortix Security**

AuditX is a fully local, offline AI-powered GRC compliance analysis tool.
It analyzes company policy documents against major regulatory frameworks
and generates gap reports, compliance scores, and fix recommendations.

## Frameworks Supported
- DPDP Act 2023 + Rules 2025 (India)
- GDPR (EU)
- EU AI Act 2024
- NIST SP 800-53 Rev 5
- RBI Digital Payment Security Controls

## Features
- Upload PDF or TXT policy documents
- Compliance scoring (0-100) per framework
- Gap analysis with specific fix recommendations
- Downloadable audit reports
- 100% local processing — no data leaves your machine
- Powered by Mistral 7B via Ollama

## Tech Stack
- Python 3.10
- Streamlit (UI)
- ChromaDB (local vector database)
- Ollama + Mistral 7B (LLM)
- PyMuPDF (PDF extraction)

## Setup

```bash
git clone https://github.com/kaifhoda1/AuditX.git
cd AuditX
python3 -m venv venv
source venv/bin/activate
pip install pymupdf chromadb ollama streamlit python-dotenv
python3 core/ingestor.py
streamlit run app.py --server.headless true
```

## Contact
**ByteFortix Security**
kaifhoda1@gmail.com
github.com/kaifhoda1

## Disclaimer
DRAFT outputs only. Not legal advice.
Always verify findings with a qualified compliance professional.

## License
Proprietary — ByteFortix Security © 2026. All rights reserved.
Unauthorized use, copying, or distribution is prohibited.
