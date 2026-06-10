# AuditX
### Private GRC Intelligence Platform

**ByteFortix Security**

---

AuditX is an AI-powered compliance analysis platform that audits company policy documents against major regulatory frameworks and delivers professional gap reports with exact legal citations, penalty references, and prioritized fix recommendations.

All processing is local. No data leaves the operator's machine.

---

## What It Does

AuditX accepts a company's policy document and produces a structured compliance audit covering:

- Compliance score per framework (0-100)
- Passed and failed checks with exact article citations
- Gap analysis with applicable penalty references
- Prioritized remediation plan
- Downloadable PDF and Word audit report

---

## Frameworks

| Framework | Coverage |
|---|---|
| DPDP Act 2023 + Rules 2025 | Full text — 277 chunks |
| GDPR (EU) | Full text — 452 chunks |
| EU AI Act 2024 | Full text — 750 chunks |
| NIST SP 800-53 Rev 5 | Full text — 2065 chunks |
| RBI Digital Payment Security Controls | Full text — 58 chunks |

---

## Architecture

- Local LLM inference via Ollama (Mistral 7B)
- Vector search via ChromaDB
- RAG pipeline grounded in official framework documents
- Zero cloud dependency — no API keys, no external calls
- Air-gapped compatible

---

## Reports

Every audit generates three downloadable formats:

- PDF report — branded, client-ready
- Word document — editable, structured gap analysis
- TXT report — plain text for internal records

---

## Security

- Login protected
- Credentials managed via environment variables
- Client documents processed in memory — not stored permanently
- ChromaDB and outputs excluded from version control

---

## Status

Active development. Currently in private beta testing with select clients.

---

## Contact

ByteFortix Security
kaifhoda1@gmail.com
github.com/kaifhoda1

---

## License

Proprietary — ByteFortix Security 2026. All rights reserved.
Unauthorized use, copying, or distribution is prohibited.
For licensing inquiries contact kaifhoda1@gmail.com
